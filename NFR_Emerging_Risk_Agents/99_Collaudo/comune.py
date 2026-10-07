"""Percorsi e utilita' condivise dalla suite di collaudo.

La suite NON ha copie del codice di campo: importa lo strumento vero da
07_Senza_Studio, cosi' collauda esattamente cio' che gira in esercizio.
"""

import json
import os
import sys
from pathlib import Path

RADICE = Path(__file__).resolve().parent.parent
KERNEL = RADICE / "01_Kernel"
EXCEL = RADICE / "03_Excel"
CAMPO = RADICE / "07_Senza_Studio"
DATI = Path(__file__).resolve().parent / "dati"
# NFR_TEMPLATE permette di collaudare un template costruito a mano.
TEMPLATE = Path(os.environ.get("NFR_TEMPLATE", EXCEL / "NFR_Dashboard_Template.xlsx"))

sys.path.insert(0, str(CAMPO))


def carica(percorso):
    with open(percorso, encoding="utf-8-sig") as f:
        return json.load(f)


def scrivi_decisioni(workbook, periodo, decisioni):
    """Fa cio' che fa il validatore nella griglia del foglio Validazione (D-67): per ogni decisione
    {oggetto, id, campo, decisione, valore, motivazione} trova la riga dell'oggetto nel periodo;
    Rettificato = scrive 'valore' nella cella gialla del campo, Respinto = Respingi "Sì"; la
    motivazione, se c'e', va nella Motivazione della riga; 'respingi', se c'e', si scrive cosi' com'e'
    (per provare un valore sbagliato). Le righe non citate restano come sono (= accettate). Salva."""
    from excel_com import SessioneExcel
    trovate = 0
    with SessioneExcel(workbook) as s:
        nome = lambda d, colonna: s.intervallo_nome(f"VG_{d['oggetto']}_{colonna}")
        for d in decisioni:
            ids = [r[0] for r in nome(d, "ID").Value]
            periodi = [str(r[0]) for r in nome(d, "Periodo").Value]
            riga = next((i for i, (x, p) in enumerate(zip(ids, periodi), start=1) if x == d["id"] and p == periodo), None)
            if riga is None:
                continue
            if d["decisione"] == "Rettificato":
                nome(d, d["campo"]).Cells(riga, 1).Value = d.get("valore")
            elif d["decisione"] == "Respinto":
                nome(d, "Respingi").Cells(riga, 1).Value = "Sì"
            if "respingi" in d:
                nome(d, "Respingi").Cells(riga, 1).Value = d["respingi"]
            if d.get("motivazione") is not None:
                nome(d, "Motivazione").Cells(riga, 1).Value = d["motivazione"]
            trovate += 1
        s.salva()
    if trovate != len(decisioni):
        raise AssertionError(f"decisioni scritte {trovate} su {len(decisioni)}: qualche riga non e' nella griglia")


def azzera_griglia(workbook):
    """Riporta la griglia del foglio Validazione alle sole proposte (cancella cio' che vi e' scritto) e salva."""
    import esegui_ciclo_locale as campo
    from excel_com import SessioneExcel
    with SessioneExcel(workbook) as s:
        campo.ricostruisci_griglia(campo.Scrittore(s, carica(KERNEL / "mappatura_campi.json")), modifiche={})
        s.salva()


class Esito:
    """Raccoglie verifiche con nome; stampa un riepilogo leggibile."""

    def __init__(self, titolo):
        self.titolo = titolo
        self.righe = []

    def verifica(self, condizione, descrizione, dettaglio=""):
        self.righe.append((bool(condizione), descrizione, dettaglio))
        return bool(condizione)

    @property
    def ok(self):
        return all(r[0] for r in self.righe)

    def stampa(self, dettagliato=False):
        # Di default stampa solo le verifiche fallite: un elenco di 60 "OK"
        # nasconde l'unico KO che conta. Con -v si vedono tutte.
        dettagliato = dettagliato or "-v" in sys.argv
        print(f"\n=== {self.titolo} ===")
        for passato, descrizione, dettaglio in self.righe:
            if passato and not dettagliato:
                continue
            print(f"  [{'OK ' if passato else 'KO '}] {descrizione}")
            if dettaglio and not passato:
                for riga in str(dettaglio).splitlines():
                    print(f"         {riga}")
        n_ko = sum(1 for r in self.righe if not r[0])
        print(f"  -> {len(self.righe) - n_ko}/{len(self.righe)} verifiche superate")
        return self.ok
