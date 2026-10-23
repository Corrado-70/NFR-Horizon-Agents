"""Accesso al workbook tramite Excel desktop (automazione COM, pywin32).

Perche' COM e non una libreria che scrive il file .xlsx: Excel e' gia' parte
di Microsoft 365, quindi non si aggiunge un motore esterno; le formule si
ricalcolano davvero (una libreria lascerebbe i valori congelati fino alla
prossima apertura); le tabelle crescono con la loro logica nativa.

Requisiti: Windows, Excel desktop, pacchetto pywin32. Nessuna registrazione
applicativa, nessun ruolo amministrativo.
"""

import time
from pathlib import Path

# Errori COM transitori all'avvio di Excel: un'istanza appena chiusa non ha
# ancora liberato le risorse, o Excel e' occupato. Si riprova, non si fallisce.
#   -2146959355  CO_E_SERVER_EXEC_FAILURE ("Esecuzione del server non riuscita")
#   -2147418111  RPC_E_CALL_REJECTED (Excel occupato)
#   -2147023174  RPC_S_SERVER_UNAVAILABLE
ERRORI_TRANSITORI = {-2146959355, -2147418111, -2147023174}
TENTATIVI_AVVIO = 5

# Codici con cui COM restituisce gli errori di formula nelle celle.
CODICI_ERRORE = {
    -2146826281: "#DIV/0!", -2146826246: "#N/A", -2146826259: "#NAME?",
    -2146826288: "#NULL!", -2146826252: "#NUM!", -2146826265: "#REF!",
    -2146826273: "#VALUE!", -2146826256: "#SPILL!", -2146826238: "#CALC!",
}


class SessioneExcel:
    """Apre un workbook in un'istanza di Excel dedicata e invisibile.

    Istanza dedicata (DispatchEx): non tocca le finestre di Excel che
    l'utente ha gia' aperte. Alla chiusura l'istanza termina sempre, anche
    in caso di errore, cosi' non restano processi EXCEL.EXE orfani.
    """

    def __init__(self, percorso, sola_lettura=False):
        self.percorso = str(Path(percorso).resolve())
        self.sola_lettura = sola_lettura
        self.app = None
        self.wb = None

    def __enter__(self):
        import pythoncom
        import win32com.client
        pythoncom.CoInitialize()
        for tentativo in range(1, TENTATIVI_AVVIO + 1):
            try:
                self.app = win32com.client.DispatchEx("Excel.Application")
                self.app.Visible = False
                self.app.DisplayAlerts = False
                self.app.AskToUpdateLinks = False
                self.wb = self.app.Workbooks.Open(self.percorso, UpdateLinks=0, ReadOnly=self.sola_lettura)
                break
            except pythoncom.com_error as ex:
                self.__exit__(None, None, None)
                if ex.hresult not in ERRORI_TRANSITORI or tentativo == TENTATIVI_AVVIO:
                    raise
                time.sleep(3 * tentativo)          # 3, 6, 9, 12 secondi
        if not self.sola_lettura and self.wb.ReadOnly:
            self.__exit__(None, None, None)
            raise RuntimeError(f"Il file e' aperto da qualcun altro (o sincronizzazione in corso): {self.percorso}")
        if not self.sola_lettura:
            try:                                   # D-83: mai salvataggi a meta' (un file in OneDrive lo avrebbe acceso)
                self.wb.AutoSaveOn = False
            except Exception:
                pass                               # Excel senza la proprieta' o file locale: niente da spegnere
        return self

    def salva(self):
        self.wb.Save()

    def __exit__(self, tipo, valore, traccia):
        try:
            if self.wb is not None:
                self.wb.Close(SaveChanges=False)
        except Exception:
            pass                                   # chiusura di un workbook gia' perso: si chiude comunque Excel
        finally:
            self.wb = None
            if self.app is not None:
                try:
                    self.app.Quit()
                except Exception:
                    pass
                self.app = None
        return False

    # ------------------------------------------------------------ utilita'
    def ricalcola(self):
        self.app.CalculateFull()

    def foglio(self, nome):
        return self.wb.Worksheets(nome)

    def tabella(self, nome):
        for ws in self.wb.Worksheets:
            for lo in ws.ListObjects:
                if lo.Name == nome:
                    return lo
        raise KeyError(f"tabella {nome} non trovata")

    def intervallo_nome(self, nome):
        return self.wb.Names(nome).RefersToRange

    def errori_formula(self):
        """Elenca le celle con errore. #N/A prodotto da NA() e' voluto (punto
        vuoto sui grafici) e non conta; ogni altro errore si'."""
        trovati = []
        for ws in self.wb.Worksheets:
            ur = ws.UsedRange
            valori = ur.Value
            formule = ur.Formula
            if not isinstance(valori, tuple):
                valori, formule = ((valori,),), ((formule,),)
            r0, c0 = ur.Row, ur.Column
            for i, riga in enumerate(valori):
                for j, v in enumerate(riga):
                    if isinstance(v, int) and v in CODICI_ERRORE:
                        f = formule[i][j]
                        if CODICI_ERRORE[v] == "#N/A" and "NA()" in str(f):
                            continue
                        trovati.append((ws.Name, ws.Cells(r0 + i, c0 + j).Address, CODICI_ERRORE[v], f))
        return trovati


def valori_tabella(lo):
    """Righe di una tabella come lista di dict {colonna: valore}."""
    nomi = [c.Name for c in lo.ListColumns]
    if lo.DataBodyRange is None:
        return []
    dati = lo.DataBodyRange.Value
    if not isinstance(dati[0], tuple):
        dati = (dati,)
    return [dict(zip(nomi, riga)) for riga in dati]
