"""Test a catena su due cicli, con lo strumento di campo vero e il motore di Excel.

Le incoerenze di questo sistema stanno nelle CUCITURE fra componenti: per
questo il test non chiama funzioni isolate ma lancia esegui_ciclo_locale.py
come lo lancerebbe un analista, su una copia del template, e poi apre il
workbook in Excel per verificare cio' che e' stato davvero scritto.

Sequenza:
  0. la baseline estratta dal template e' quella su cui e' stato scritto run1
  1. payload difettosi (schema, kri_id di un altro rischio, A5 di un altro
     ciclo, A5 su altri rischi, file che non e' JSON): fermo, zero byte scritti;
     un JSON salvato "UTF-8 con BOM" e' accettato
  2. ciclo 2026Q3: scrittura, zero errori, formule integre, copertura Python = foglio,
     storico KRI in coda senza riscrivere il passato, KRI del ciclo nel foglio Indicatori;
     esito e "da/a" calcolati dallo script, Velocity
     non valutata, KRI senza soglie ("Soglie da definire"), soglie validate conservate
  2b. validazione umana nella griglia del foglio Validazione (D-67): una riga per oggetto, celle
     gialle uguali alle proposte, Score e Margine della griglia = quelli del registro; il ciclo
     dopo non parte senza (ne' le schede); righe non valide rifiutate in blocco, con il numero
     di riga (valore fuori regola, motivazione mancante, Respingi sbagliato, una soglia sola);
     rettifiche e respinte applicate (anche una Velocity da non valutata a 3 e le soglie
     fissate dalla Banca; anni di adeguamento rettificati, scritti nell'anagrafica, D-60);
     Score e Margine calcolati dalla griglia PRIMA di valida = quelli del registro DOPO;
     Variazioni coerenti con i valori validati; report al comitato rigenerato
     con il comando report (fermo prima della validazione, versione precedente
     conservata); il periodo esce dalla griglia;
     righe per le liste riscritte con i valori validati; proposta conservata
  2c. schede dei rischi (agente A6): input dal registro validato; output di A6
     con un rischio mancante, una fonte cambiata o un numero inventato fermato;
     file delle schede con e senza A6
  3. settimana 2026-10-12: codice fonte fuori elenco e id ripetuti fermati;
     titoli che iniziano con "=" o sembrano date restano testo; badge, area non
     presidiata 9.11, nessun duplicato al rilancio; una riga cancellata a mano dalla
     griglia ferma valida, il comando griglia la ripara conservando cio' che e' scritto
  4. la baseline dopo il 2026Q3 e' quella su cui e' stato scritto run3
  5. ciclo 2026Q4: NFR-16 entra nel radar dall'osservazione (D-79), anagrafica, KRI nuovi,
     9.11 ora presidiata; la storia di un KRI (Indicatori) coincide con lo storico, anche
     per un KRI uscito; Radar_Mosca = calcolo indipendente; Registro con una riga
     per rischio del radar
  6. gate di copertura: un ciclo scritto a meta' viene fermato prima del salvataggio
  7. scorrimento della finestra settimanale
  8. errore dopo il salvataggio: messaggio veritiero, baseline gia' aggiornata;
     rettifica del valore di un KRI mai rilevato: data e fonte della rilevazione
  9. primo uso reale: inizializza crea il registro vuoto (e non sovrascrive), il
     primo ciclo con tutti i rischi nuovi si scrive; dismetti toglie un rischio
     senza buchi nell'anagrafica, con KRI fuori vigore e azioni annullate
  10. registro di produzione, dal vuoto al secondo ciclo (il percorso reale fino
     al primo ciclo, DECISIONI D-07 e D-22): settimane su un registro senza
     rischi (notizie tutte NON PRESIDIATO, aree non presidiate, notizia collegata
     a un rischio inesistente fermata, validazione della settimana); primo ciclo
     con tutti i rischi nuovi; ciclo dopo bloccato finche' il primo non e'
     validato; validazione; baseline del secondo ciclo con i rischi validati
  11. aggiornamento di un registro creato con il template del 23/09 (quello in
     produzione): ogni comando si ferma finche' non e' aggiornato; aggiorna-registro
     copia tutto (stesse righe, stessa baseline, vecchio in Backup), ricalcola i
     compositi con i pesi D-50; poi un ciclo intero sul registro aggiornato, con
     gli anni di adeguamento conservati e usati da Mosca
  11b. aggiornamento di un registro del template 2026-09-25c (Gap_Controlli e
     Dimensione delle azioni, D-49 e D-54): fermo con righe "Da decidere" su campi
     tolti dal modello; righe "Da decidere" su campi attuali portate nella griglia con la
     decisione scritta nel vecchio foglio, poi validate; colonne dismesse lasciate nel
     backup, presidio "Non verificato", stessa baseline
  12. A5 facoltativo e segnalazioni in validazione (D-71): un difetto di integrita'
     ferma con il messaggio per A1; C3 (salto di due punti), soglie invertite di C9 e
     un Bloccante di A5 non fermano: stanno sui rischi (DA MOTIVARE), in Sintesi_Cicli,
     nel Quadro e nella colonna Segnalazioni della griglia (⚑); valida chiede le
     motivazioni e non accetta il salto ne' le soglie invertite; --procedi-con-rilievi
     accettata ma inutile; un settimanale scritto durante la validazione conserva cio'
     che e' gia' scritto nella griglia e non si ferma per un valore sbagliato li'
  11c. aggiornamento di un registro del template 2026-10-08b (lista di osservazione, D-73): le voci in
     osservazione diventano rischi in osservazione NFR-nn (D-79)
  13. riapertura della validazione (D-76), con le decisioni sullo stato (un rischio entra, uno esce)
  14. registro unico (D-79): un rischio sotto la soglia resta un ciclo "in uscita" ed esce al secondo; decisioni
     del validatore sullo stato (motivazione obbligatoria); capienza del radar ridotta; dismissione di un rischio
     in osservazione
Report al comitato (passi 2, 2b, 5, 11): score composito = formula D-50
calcolata a parte; Classifica ordinata come un ordinamento indipendente;
grafici della Classifica con un punto per rischio; Quadro con il commento di
A1 diviso in messaggio e decisioni, l'avviso dopo le rettifiche e i rischi
segnalati uguali a una selezione calcolata a parte (primi tre, AGIRE ORA,
variati, nuovi); Delta con un motivo per rischio.

Requisiti: Windows, Excel desktop, pywin32, openpyxl. Durata in sequenza: circa 50 minuti (Excel si apre e ricalcola
a ogni passo, circa 150 volte).

Uso (M1, 08/10/2026):
  python run_catena.py                  tutti i gruppi in sequenza
  python run_catena.py --parallelo [N]  tutti i gruppi in N processi (default 3), una istanza di Excel ciascuno
  python run_catena.py --passo <nome>   un gruppo solo (catena, gate, errore, primo_uso, produzione,
                                        aggiornamento, notizie, aggiornamento_25c, segnalazioni, riapertura,
                                        registro_unico, aggiornamento_08b)
  NFR_RIGENERA_ATTESI=1                 riscrive i file attesi di dati/ (baseline) con quelli prodotti: solo dopo
                                        una modifica voluta del formato, poi si guarda il diff
  -v                                    stampa anche le verifiche superate
"""

import copy
import datetime
import hashlib
import json
import os
import shutil
import stat
import subprocess
import sys
import tempfile
from pathlib import Path

from comune import CAMPO, DATI, KERNEL, TEMPLATE, Esito, azzera_griglia, carica, scrivi_decisioni
import controlli_a5
import esegui_ciclo_locale as campo
from excel_com import SessioneExcel

MAPPA = carica(KERNEL / "mappatura_campi.json")
RR_TEMPLATE = 38                 # righe del RiskRegister del template: 33 del radar + 5 dei 3 rischi in osservazione (D-79)
PRESIDIO_911_Q3 = "In osservazione"   # 9.11 nel 2026Q3: nessun rischio nel radar, NFR-16 in osservazione (D-79)


def uguale_ai_dati(nome, prodotto):
    """Il file prodotto e' uguale (come JSON) al file atteso dati/<nome>. Con NFR_RIGENERA_ATTESI=1 lo copia al posto
    dell'atteso e risponde si': solo dopo una modifica voluta del formato, poi si guarda il diff."""
    if os.environ.get("NFR_RIGENERA_ATTESI") == "1":
        shutil.copyfile(prodotto, DATI / nome)
        return True
    return carica(prodotto) == carica(DATI / nome)


def sha(percorso):
    return hashlib.sha256(Path(percorso).read_bytes()).hexdigest()


class Banco:
    """Una copia del template e i comandi dello strumento di campo su di essa."""

    def __init__(self, cartella, template=TEMPLATE):
        self.cartella = Path(cartella)
        self.wb = self.cartella / "NFR_workbook.xlsx"
        self.uscita = self.cartella / "uscita"
        shutil.copy2(template, self.wb)

    def esegui(self, *argomenti):
        cmd = [sys.executable, str(CAMPO / "esegui_ciclo_locale.py"), "--workbook", str(self.wb),
               "--kernel", str(KERNEL), "--cartella-uscita", str(self.uscita), *map(str, argomenti)]
        # NFR_ATTESA_LUCCHETTO=0: nel collaudo nessun collega sincronizza la cartella, la presa in due tempi non serve.
        r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace",
                           env={**__import__("os").environ, "PYTHONIOENCODING": "utf-8", "NFR_ATTESA_LUCCHETTO": "0"})
        return r.returncode, r.stdout + r.stderr

    def esegui_conf(self, chiavi, *argomenti):
        """Come esegui, con chiavi di configurazione passate come variabile d'ambiente NFR_CONF_EXTRA (solo collaudo)."""
        cmd = [sys.executable, str(CAMPO / "esegui_ciclo_locale.py"), "--workbook", str(self.wb),
               "--kernel", str(KERNEL), "--cartella-uscita", str(self.uscita), *map(str, argomenti)]
        r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace",
                           env={**os.environ, "PYTHONIOENCODING": "utf-8", "NFR_ATTESA_LUCCHETTO": "0",
                                "NFR_CARTELLA_LAVORO": chiavi.get("cartella_lavoro", "")})
        return r.returncode, r.stdout + r.stderr

    def scrivi_json(self, nome, dati):
        p = self.cartella / nome
        p.write_text(json.dumps(dati, ensure_ascii=False, indent=2), encoding="utf-8")
        return p

    def leggi(self):
        """Stato del workbook letto da Excel (sola lettura, ricalcolato)."""
        with SessioneExcel(self.wb, sola_lettura=True) as s:
            s.ricalcola()
            scr = campo.Scrittore(s, MAPPA)
            _, anag = scr.leggi_anagrafica()
            commento = s.intervallo_nome("quadroCommento")
            segnalati = s.intervallo_nome("quadroSegnalati")
            return {
                "errori": s.errori_formula(),
                "formule_mancanti": campo.formule_mancanti(s, MAPPA),
                "copertura_foglio": campo.copertura_foglio(s),
                "copertura_python": campo.copertura_python(scr, campo.da_excel(s.intervallo_nome("cicloCorrente").Value)),
                "ciclo": s.intervallo_nome("cicloCorrente").Value,
                "settimana": campo.da_excel(s.intervallo_nome("settimanaCorrente").Value),
                "kri": scr.righe("tblKRI"),
                "register": scr.righe("tblRegister"),
                "news": scr.righe("tblNews"),
                "anagrafica": [r for _, r in anag],
                "anagrafica_posizioni": [i for i, _ in anag],
                "badge": {i: b for i, b in zip(campo.colonna_nome(s, "posID"), campo.colonna_nome(s, "posBadge")) if i},
                "f8": s.intervallo_nome("statoValidazione").Value,
                "validazione": scr.righe("tblValidazione"),
                "griglia": campo.leggi_griglia(s, MAPPA),
                "griglia_stato": s.intervallo_nome("valStato").Value,
                "griglia_nomi": {i: n for i, n in zip(campo.colonna_nome(s, "VG_Rischio_ID"), campo.colonna_nome(s, "VG_Rischio_Nome")) if i},
                "griglia_segnalazioni": {i: n for i, n in zip(campo.colonna_nome(s, "VG_Rischio_ID"),
                                                               campo._colonna_o_niente(s, "VG_Rischio_Segnalazioni") or []) if i},
                "griglia_segnalazioni_ciclo": (campo._colonna_o_niente(s, "VG_Rischio_SegnalazioniCiclo") or [None])[0],
                "griglia_stati": {i: n for i, n in zip(campo.colonna_nome(s, "VG_Rischio_ID"),
                                                       campo._colonna_o_niente(s, "VG_Rischio_Stato") or []) if i},
                # Score e margine calcolati dalla griglia con i valori gialli: {ID: (score, margine)}.
                "griglia_rischi": {i: (sc, mg) for i, sc, mg in zip(campo.colonna_nome(s, "VG_Rischio_ID"),
                                                                    campo.colonna_nome(s, "VG_Rischio_ScoreNum"),
                                                                    campo.colonna_nome(s, "VG_Rischio_MargineNum")) if i},
                "registro": [v for v in (s.foglio("Registro").Range(f"A{r}").Value
                                         for r in range(9, 9 + s.intervallo_nome("anagrafica").Rows.Count)) if v],
                "mosca": [(m.Range(f"A{r}").Value, m.Range(f"F{r}").Value, m.Range(f"K{r}").Value, m.Range(f"L{r}").Value)
                          for m in [s.foglio("Radar_Mosca")] for r in range(5, 5 + s.intervallo_nome("anagrafica").Rows.Count)
                          if m.Range(f"A{r}").Value],
                "presidio": dict(zip(campo.colonna_nome(s, "presidioCodici"), campo.colonna_nome(s, "presidioStato"))),
                "f10": s.intervallo_nome("statoCopertura").Value,
                "kri_correnti": [v for v in (s.foglio("Indicatori").Range(f"A{r}").Value for r in range(7, 67)) if v],
                "versione": campo.versione_workbook(s),
                "sintesi_cicli": scr.righe("tblSintesi"),
                "settimane": scr.righe("tblSettimane"),
                "riquadro_settimana": (s.foglio("Notizie").Range("L5").Value, s.foglio("Notizie").Range("L11").Value),
                "messaggio": commento.Cells(1, 4).Value,
                "decisioni": commento.Cells(2, 4).Value,
                "avviso": commento.Cells(4, 4).Value,
                "rilievi_superati": commento.Cells(5, 4).Value,
                "segnalati": [str(c.Value).split("\n")[0] for c in segnalati.Columns(1).Cells if c.Value],
                "delta_motivi": [(c.Value, c.GetOffset(0, 2).Value) for c in s.intervallo_nome("deltaMotivi").Columns(1).Cells
                                 if c.Value],
                "classifica": [(c.Range(f"B{r}").Value, c.Range(f"D{r}").Value) for c in [s.foglio("Classifica")]
                               for r in range(5, 5 + s.intervallo_nome("anagrafica").Rows.Count) if c.Range(f"B{r}").Value],
                "classifica_punti": [c.Chart.SeriesCollection(i).Points().Count for f in [s.foglio("Classifica")]
                                     for c in [f.ChartObjects(1), f.ChartObjects(2)] for i in (1, 2, 3)],
                "radar_livello": radar_livello(s),
                "livello": {m.Range(f"A{r}").Value: (m.Range(f"AA{r}").Value, m.Range(f"AB{r}").Value)
                            for m in [s.foglio("Radar_Mosca")] for r in range(5, 5 + s.intervallo_nome("anagrafica").Rows.Count)
                            if m.Range(f"A{r}").Value},
                "delta_spazio": spazio_delta(s),
                # Pagina Fenomeni (D-79): (ID, score, perche' fuori dal radar) dei rischi in osservazione.
                "fenomeni": [(c.Value, c.GetOffset(0, 4).Value, c.GetOffset(0, 5).Value)
                             for c in s.intervallo_nome("fenomeniLista").Columns(2).Cells if c.Value],
                "fenomeni_uscite": [(c.Value, c.GetOffset(0, 2).Value) for c in s.intervallo_nome("fenomeniUscite").Columns(2).Cells
                                    if c.Value],
                "quadro_pagine": pagine_quadro(s),
            }

    def andamento(self, kri_id):
        """Foglio Indicatori con kri_id in N4: {ciclo: valore} dei cicli con un valore,
        e l'elenco a discesa (tutti i KRI mai definiti)."""
        with SessioneExcel(self.wb, sola_lettura=True) as s:
            f = s.foglio("Indicatori")
            f.Range("N4").Value = kri_id
            s.ricalcola()
            valori = {f.Range(f"M{r}").Value: f.Range(f"N{r}").Value for r in range(12, 20)
                      if isinstance(f.Range(f"N{r}").Value, float)}
            elenco = [c.Value for c in s.intervallo_nome("elencoKRI").Cells]
            return valori, elenco


def file_rischio(cartella, rid):
    """Testo del file della knowledge di A7 che contiene il rischio (posti fissi Rischio_nn.txt, D-72); None se manca."""
    for f in sorted(Path(cartella).glob("Rischio_*.txt")):
        testo = f.read_text(encoding="utf-8")
        if f"RISCHIO {rid} " in testo.split("\n", 1)[0]:
            return testo
    return None


def rischi_nei_posti(cartella):
    """(posti, posti occupati) della knowledge di A7."""
    file = sorted(Path(cartella).glob("Rischio_*.txt"))
    return len(file), sum(1 for f in file if "POSTO LIBERO" not in f.read_text(encoding="utf-8").split("\n", 1)[0])


def pagine_quadro(s):
    """Pagine del Quadro in PDF, con l'impaginazione salvata dallo script (prepara_report)."""
    import re
    import tempfile as tf
    with tf.TemporaryDirectory() as d:
        pdf = Path(d) / "quadro.pdf"
        s.foglio("Quadro").ExportAsFixedFormat(0, str(pdf))
        return len(re.findall(rb"/Type\s*/Page[^s]", pdf.read_bytes()))


def spazio_delta(s):
    """(fondo del grafico del Delta, inizio della riga della nota sulla scala), in punti."""
    ws, area = s.foglio("Delta"), s.intervallo_nome("deltaMotivi")
    g = ws.ChartObjects(1)
    return g.Top + g.Height, ws.Rows(area.Row + area.Rows.Count + 1).Top


LIVELLI = ("Attivazione", "Attenzione", "Monitoraggio")


def radar_livello(s):
    """{ID: (livelli delle serie in cui il punto e' disegnato, etichetta)} dal Radar_Mosca (D-63): le serie
    sono una per P x I e livello di allerta (riga 3 dell'appoggio); l'etichetta e' l'ID, con ◆ se il tema
    e' all'attenzione del supervisore. Un valore numerico = punto disegnato; #N/D = nessun punto."""
    m = s.foglio("Radar_Mosca")
    classi = [(c, m.Cells(3, c).Value) for c in range(30, 140) if m.Cells(3, c).Value in LIVELLI]
    etichetta = max(c for c, _ in classi) + 2          # dopo le classi e la x (genera_dashboard.grafico_radar)
    out = {}
    for r in range(5, 5 + s.intervallo_nome("anagrafica").Rows.Count):
        rid = m.Range(f"A{r}").Value
        if rid:
            out[rid] = ([v for c, v in classi if isinstance(m.Cells(r, c).Value, float)], m.Cells(r, etichetta).Value)
    return out


def livello_atteso(stato):
    """Livello di allerta calcolato a parte (rubrica, sezione 8; soglie del template): segnali forti AGIRE ORA,
    KRI in rosso, segnali netti >= 2; aggravanti P x I >= 12, presidio Assente, meta' dei KRI in ambra o rosso."""
    kri = [k for k in stato["kri"] if k["Ciclo"] == stato["ciclo"] and k["In_Vigore"] == "Sì"]
    presidio = {a["ID"]: a.get("Presidio_Controlli") for a in stato["anagrafica"]}
    attesi = {}
    for rid, pxi, margine, _ in stato["mosca"]:
        if not isinstance(margine, float):
            continue
        suoi = [k["Stato"] for k in kri if k["ID_Rischio"] == rid]
        rossi, ambra = suoi.count("Rosso"), suoi.count("Ambra")
        netti = int(str(stato["badge"].get(rid) or "0").split()[-1])
        forti = (margine < 0) + (rossi > 0) + (netti >= 2)
        aggravanti = (pxi >= 12) + (presidio.get(rid) == "Assente") + (bool(suoi) and rossi + ambra >= 0.5 * len(suoi))
        attesi[rid] = ("Attivazione" if forti >= 2 else
                       "Attenzione" if forti >= 1 or (margine < 1 and aggravanti >= 1) else "Monitoraggio")
    return attesi


def mosca_attesa(stato, azioni):
    """Margine di Mosca calcolato a parte: Z dalla Prossimita, X = 0,25, Y = max
    (orizzonte delle azioni non respinte o 1 anno, anni di adeguamento dell'anagrafica)."""
    anni = {5: 0, 4: 0.5, 3: 1.5, 2: 2.5, 1: 3.5}      # D-59: meta' della fascia della Prossimita
    adeguamento = {a["ID"]: a.get("Anni_Adeguamento") or 0 for a in stato["anagrafica"]}
    attesi = {}
    for r in (x for x in stato["register"] if x["Ciclo"] == stato["ciclo"] and x["ID_Rischio"] in adeguamento):   # il radar
        mesi =[int(a["Orizzonte"].split()[0]) for a in azioni
                if a["ID_Rischio"] == r["ID_Rischio"] and a["Ciclo"] == stato["ciclo"] and a["Stato"] != "Respinta"]
        y = max(max(mesi) / 12 if mesi else 1, adeguamento.get(r["ID_Rischio"], 0))
        attesi[r["ID_Rischio"]] = (r["Impatto"] * r["Probabilita"], round(anni[r["Prossimita"]] - (0.25 + y), 6))
    return attesi


def carica_tabella(banco, nome):
    with SessioneExcel(banco.wb, sola_lettura=True) as s:
        return campo.Scrittore(s, MAPPA).righe(nome)


def righe_visibili(banco):
    """Righe visibili di ogni sezione della griglia del foglio Validazione (le libere sono nascoste)."""
    with SessioneExcel(banco.wb, sola_lettura=True) as s:
        return {o: sum(1 for r in s.intervallo_nome(f"VG_{o}_righe").Rows if not r.EntireRow.Hidden)
                for o in MAPPA["validazione"]["oggetti"]}


def griglia_uguale_alle_proposte(stato, periodo):
    """La griglia ha una riga per oggetto da decidere del periodo, con le celle gialle uguali alle proposte."""
    proposte = {}
    for r in stato["validazione"]:
        if str(r["Periodo"]) == periodo and r["Stato"] == "Da decidere":
            proposte.setdefault((r["Oggetto"], periodo, r["ID"]), {})[r["Campo"]] = r["Proposta_Agente"]
    griglia = {k: g["valori"] for k, g in stato["griglia"].items() if k[1] == periodo}
    return set(griglia) == set(proposte) and all(campo._uguali(griglia[k].get(c), v) for k, p in proposte.items()
                                                 for c, v in p.items())


PESI_D50 = {"Impatto": 0.35, "Probabilita": 0.25, "Prossimita": 0.20, "Velocity": 0.20}


def score_d50(r):
    """Score composito calcolato a parte (D-50): media pesata delle dimensioni valutate (una
    Velocity vuota esce da numeratore e denominatore); ROUND di Excel = arrotondamento a meta' in su, sul valore con
    le cifre significative di Excel (2,1249999... in Python e' 2,125 in Excel: 2,13)."""
    from decimal import Decimal, ROUND_HALF_UP
    presenti = {d: p for d, p in PESI_D50.items() if r.get(d) is not None}
    valore = sum(p * r[d] for d, p in presenti.items()) / sum(presenti.values())
    return float(Decimal(repr(round(valore, 10))).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


def verifica_report(e, stato, etichetta, commento=None):
    """Report al comitato sul ciclo corrente, confrontato con calcoli indipendenti."""
    ciclo = stato["ciclo"]
    tutte = [r for r in stato["register"] if r["Ciclo"] == ciclo]
    attesi = {r["ID_Rischio"]: score_d50(r) for r in tutte}
    trovati = {r["ID_Rischio"]: round(r["Score_Composito"], 2) for r in tutte}
    e.verifica(trovati == attesi, f"{etichetta}: score composito = formula D-50 calcolata a parte ({len(tutte)} rischi, "
               "anche quelli in osservazione)", f"foglio {trovati}\natteso {attesi}")
    # Il report e' sui rischi del radar (l'anagrafica, D-79): quelli in osservazione stanno nella pagina Fenomeni.
    nel_radar = {a["ID"] for a in stato["anagrafica"]}
    righe = [r for r in tutte if r["ID_Rischio"] in nel_radar]
    attesi = {i: v for i, v in attesi.items() if i in nel_radar}
    posizione = {r["ID"]: i for i, r in enumerate(stato["anagrafica"])}
    ordine = sorted(attesi, key=lambda rid: (-attesi[rid], posizione[rid]))
    e.verifica([x[0] for x in stato["classifica"]] == ordine,
               f"{etichetta}: Classifica ordinata per score composito (a parita', ordine dell'anagrafica)",
               f"foglio {stato['classifica']}\natteso {ordine}")
    e.verifica(stato["classifica_punti"] == [len(righe)] * 6,
               f"{etichetta}: grafici della Classifica e lente di Mosca con un punto per rischio ({len(righe)})",
               str(stato["classifica_punti"]))
    # Livello di allerta (D-63): il foglio calcola lo stesso livello di un calcolo indipendente.
    livelli = livello_atteso(stato)
    e.verifica({rid: v[0] for rid, v in stato["livello"].items()} == livelli
               and all(v[1] for v in stato["livello"].values()),
               f"{etichetta}: livello di allerta del Radar_Mosca = calcolo indipendente, con il motivo",
               f"foglio {stato['livello']}\natteso {livelli}")
    # Rischi segnalati nel Quadro: primi tre per score, in attivazione o attenzione, variati, nuovi.
    esito = {r["ID_Rischio"]: r["Esito"] for r in righe}
    attesi_seg = [rid for k, rid in enumerate(ordine) if k < 3 or livelli.get(rid) in ("Attivazione", "Attenzione")
                  or esito[rid] in ("Variato", "Nuovo")]
    e.verifica(stato["segnalati"] == attesi_seg,
               f"{etichetta}: Quadro, rischi segnalati = primi tre, in attivazione o attenzione, variati e nuovi, "
               "in ordine di classifica",
               f"foglio {stato['segnalati']}\natteso {attesi_seg}")
    e.verifica(len(stato["delta_motivi"]) == len(righe) and all(m for _, m in stato["delta_motivi"]),
               f"{etichetta}: Delta, un motivo (o 'invariato') per ciascuno dei {len(righe)} rischi", str(stato["delta_motivi"])[:500])
    e.verifica(stato["quadro_pagine"] == 2, f"{etichetta}: Quadro in due pagine (scala adattata da prepara_report)",
               f"{stato['quadro_pagine']} pagine")
    fondo, nota = stato["delta_spazio"]
    e.verifica(fondo <= nota, f"{etichetta}: Delta, il grafico non copre la nota sulla scala dopo l'adattamento delle "
                              "altezze (prepara_report)", f"fondo del grafico {fondo:.0f} pt, nota a {nota:.0f} pt")
    if commento is not None:
        riga = [r for r in stato["sintesi_cicli"] if r["Ciclo"] == ciclo]
        if "DECISIONI:" in commento:
            m, d = commento.split("DECISIONI:", 1)
            attesi = (" ".join(m.replace("MESSAGGIO:", "").split()), " ".join(d.split()))
        else:
            attesi = (" ".join(commento.split()), "—")
        trovati = (stato["messaggio"], stato["decisioni"])
        e.verifica(len(riga) == 1 and riga[0]["Sintesi_A1"] == commento and trovati == attesi,
                   f"{etichetta}: Quadro, commento di A1 del ciclo diviso in messaggio e decisioni "
                   f"({'con' if 'DECISIONI:' in commento else 'senza'} i marcatori)", f"{trovati!r}\natteso {attesi!r}")


def a6_simulato(ingresso):
    """Output di A6 costruito dai dati del suo input (solo numeri presenti): prova i controlli e il
    file senza un agente vero. Un'uscita reale di A6 e' prosa; qui conta la forma."""
    schede = []
    for r in ingresso["rischi"]:
        descr = (f"{r['descrizione']} Il rischio ricade nell'event type {r['event_type']} ed e' presidiato dalla "
                 f"{r['owner']}. {r['razionale_rischio']}")
        schede.append({
            "id_rischio": r["id_rischio"],
            "descrizione_estesa": (descr + " " + descr)[:1400] if len(descr) < 300 else descr[:1400],
            "dimensioni": [{"dimensione": d, "spiegazione": f"Valore validato {v}: corrisponde al descrittore della rubrica, "
                                                             f"dati il razionale e le fonti del rischio."}
                           for d, v in r["valori"].items()],
            "fonti": [{"riferimento": f["riferimento"], "a_sostegno_di": "Evidenza citata nel razionale del rischio."}
                      for f in r["fonti"]],
        })
    return {"ciclo": ingresso["ciclo"], "schede": schede}


def schede_a6(e, b, s):
    """2c. Schede dei rischi sul 2026Q3 validato: input di A6, controlli sul suo output, file."""
    from openpyxl import load_workbook
    prima = sha(b.wb)
    codice, out = b.esegui("schede-input")
    percorso = b.uscita / "Cicli" / "2026Q3" / "Schede_input_2026Q3.json"
    ingresso = carica(percorso) if percorso.exists() else {"rischi": []}
    ordine = [x[0] for x in s["classifica"]]
    r01 = next((r for r in ingresso["rischi"] if r["id_rischio"] == "NFR-01"), {})
    e.verifica(codice == 0 and [r["id_rischio"] for r in ingresso["rischi"]] == ordine and sha(b.wb) == prima,
               "2c. schede-input: un rischio per rischio valutato, in ordine di classifica; registro intatto", out)
    e.verifica(len(r01.get("valori", {})) == 4 and r01.get("urgenza", {}).get("esito") and len(r01.get("storia", [])) >= 3
               and r01.get("kri") and all(k["stato"] for k in r01["kri"]),
               "2c. input di A6: valori validati, urgenza, storia, KRI del ciclo per ogni rischio", str(r01)[:400])
    # D-68: i dati di prova del 2026Q3 hanno il razionale scritto prima, senza parti: resta intero.
    e.verifica(r01.get("razionale_rischio") == next(r for r in carica(DATI / "run1_A1_2026Q3.json")["rischi"]
                                                    if r["id_rischio"] == "NFR-01")["razionale"]
               and r01.get("motivazioni") is None
               and all(a.get("razionale") for a in r01.get("azioni", [])) and all(k.get("razionale") for k in r01["kri"]),
               "2c. input di A6: razionale senza parti intero, motivazioni null; azioni e KRI con il loro razionale (D-68)",
               str({k: r01.get(k) for k in ("razionale_rischio", "motivazioni")})[:400])
    buono = a6_simulato(ingresso)
    difetti = [("rischio mancante", lambda p: p["schede"].pop(), "Rischi senza scheda"),
               ("fonte cambiata", lambda p: p["schede"][0]["fonti"][0].update(riferimento="Fonte inventata dall'agente"),
                "fonti devono essere quelle dell'input"),
               ("numero inventato", lambda p: p["schede"][0]["dimensioni"][0].update(
                   spiegazione="Perdite stimate in 7.345.000 euro nel trimestre, secondo l'agente."), "numeri che non stanno"),
               ("dimensione ripetuta", lambda p: p["schede"][1]["dimensioni"].__setitem__(3, dict(p["schede"][1]["dimensioni"][0])),
                "quattro dimensioni")]
    for nome, guasto, atteso in difetti:
        p = copy.deepcopy(buono)
        guasto(p)
        codice, out = b.esegui("schede", "--payload", b.scrivi_json(f"a6_{nome.replace(' ', '_')}.json", p))
        e.verifica(codice == 1 and atteso in out and not (b.uscita / "Cicli" / "2026Q3" / "Schede_2026Q3.xlsx").exists(),
                   f"2c. output di A6 con {nome}: fermo, nessun file", out)
    codice, out = b.esegui("schede", "--payload", b.scrivi_json("a6_buono.json", buono))
    file = b.uscita / "Cicli" / "2026Q3" / "Schede_2026Q3.xlsx"
    fogli = load_workbook(file).sheetnames if file.exists() else []
    e.verifica(codice == 0 and fogli == ["Indice"] + ordine and (b.uscita / "Cicli" / "2026Q3" / "A6_2026Q3.json").exists()
               and sha(b.wb) == prima,
               "2c. schede con i testi di A6: indice e una scheda per rischio in ordine di classifica; A6 archiviato; "
               "registro intatto", out + str(fogli))
    wb = load_workbook(file) if file.exists() else None
    testo = [c.value for c in wb[ordine[0]]["A"] if c.value] if wb else []
    e.verifica(wb is not None and buono["schede"][0]["descrizione_estesa"] in testo,
               "2c. la scheda riporta la descrizione estesa di A6", str(testo[:6])[:300])
    file.unlink(missing_ok=True)
    codice, out = b.esegui("schede")
    e.verifica(codice == 0 and file.exists() and "senza A6" in out,
               "2c. schede senza A6: stesso file con i testi di A1 dal registro", out)


def verifica_integrita(e, stato, etichetta):
    e.verifica(not stato["errori"], f"{etichetta}: zero errori di formula (Excel)", str(stato["errori"][:5]))
    e.verifica(not stato["formule_mancanti"], f"{etichetta}: tutte le colonne formula hanno la formula", str(stato["formule_mancanti"][:5]))
    e.verifica(stato["copertura_python"] == stato["copertura_foglio"],
               f"{etichetta}: copertura calcolata in Python = copertura del foglio",
               f"python {stato['copertura_python']} foglio {stato['copertura_foglio']}")
    chiavi = [(k["Ciclo"], k["KRI_ID"]) for k in stato["kri"]]
    e.verifica(len(chiavi) == len(set(chiavi)), f"{etichetta}: storico KRI senza doppioni per ciclo e KRI ({len(chiavi)} righe)")
    correnti = [k["KRI_ID"] for k in stato["kri"] if k["Ciclo"] == stato["ciclo"] and k["In_Vigore"] == "Sì"]
    e.verifica(stato["kri_correnti"] == correnti, f"{etichetta}: Indicatori mostra esattamente i KRI in vigore nel ciclo corrente ({len(correnti)})",
               f"vista {stato['kri_correnti']}\nstorico {correnti}")


def passi():
    """{nome: (funzione, descrizione)}: gruppi indipendenti, ognuno su copie proprie del template (M1, 08/10/2026).
    La catena principale e' il gruppo piu' lungo: in parallelo la durata e' circa la sua."""
    return {"catena": (catena, "la catena (passi 0-5, 7, 7b, 8s, 8a)"),
            "gate": (gate_copertura, "il gate di copertura (passo 6)"),
            "errore": (errore_dopo_salvataggio, "l'errore dopo il salvataggio (passi 8 e 8b)"),
            "primo_uso": (primo_uso, "il primo uso e la dismissione (passo 9)"),
            "produzione": (produzione, "il registro di produzione (passo 10)"),
            "aggiornamento": (aggiornamento, "l'aggiornamento del registro (passo 11)"),
            "notizie": (notizie_validate, "le notizie validate nelle viste (passo 3b)"),
            "aggiornamento_25c": (aggiornamento_25c, "l'aggiornamento dal template 2026-09-25c (passo 11b)"),
            "segnalazioni": (segnalazioni_in_validazione, "A5 facoltativo e segnalazioni in validazione (passo 12)"),
            "riapertura": (riapertura, "la riapertura della validazione (passo 13)"),
            "registro_unico": (registro_unico, "il registro unico: radar e osservazione (passo 14, D-79)"),
            "aggiornamento_08b": (aggiornamento_08b, "l'aggiornamento dal template 2026-10-08b, lista di osservazione (passo 11c)"),
            "piu_analisti": (piu_analisti, "lucchetto, copia di lavoro, allegati e archivi automatici (passo 15, D-83)")}


def esegui_passi(nomi, titolo):
    e = Esito(titolo)
    for nome in nomi:
        funzione, descrizione = passi()[nome]
        try:
            funzione(e)
        except Exception:                            # un passo rotto non deve nascondere i KO gia' trovati
            import traceback
            e.verifica(False, f"{descrizione} arriva in fondo senza eccezioni", traceback.format_exc(limit=3))
    return 0 if e.stampa() else 1


def in_parallelo(processi):
    """Ogni gruppo in un processo suo, con la sua istanza di Excel (SessioneExcel usa DispatchEx); stampa le uscite
    nell'ordine dei gruppi e il totale delle verifiche."""
    import re
    import time
    from concurrent.futures import ThreadPoolExecutor
    inizio = time.time()

    def lancia(nome):
        r = subprocess.run([sys.executable, str(Path(__file__)), "--passo", nome, *(["-v"] if "-v" in sys.argv else [])],
                           capture_output=True, text=True, encoding="utf-8", errors="replace",
                           env={**os.environ, "PYTHONIOENCODING": "utf-8"})
        return r.returncode, r.stdout + r.stderr

    nomi = list(passi())                             # la catena per prima: e' la piu' lunga
    with ThreadPoolExecutor(max_workers=processi) as pool:
        esiti = dict(zip(nomi, pool.map(lancia, nomi)))
    superate = totali = 0
    for nome in nomi:
        codice, uscita = esiti[nome]
        print(uscita.rstrip())
        conti = re.findall(r"-> (\d+)/(\d+) verifiche superate", uscita)
        if conti:
            superate += int(conti[-1][0])
            totali += int(conti[-1][1])
        else:
            print(f"  [KO ] il gruppo {nome} non ha stampato l'esito (codice {codice})")
            totali += 1
    ko = [n for n in nomi if esiti[n][0] != 0]
    print(f"\n=== Catena in parallelo ({processi} processi, {round((time.time() - inizio) / 60)} minuti) ===\n"
          f"  -> {superate}/{totali} verifiche superate" + (f"; gruppi con KO: {', '.join(ko)}" if ko else ""))
    return 1 if ko or superate != totali else 0


def main():
    """Senza opzioni: tutti i gruppi in sequenza. --passo <nome>: un gruppo solo. --parallelo [N]: tutti i gruppi in N
    processi (default 3), ognuno con la sua istanza di Excel."""
    argomenti = sys.argv[1:]
    if "--passo" in argomenti:
        nome = argomenti[argomenti.index("--passo") + 1]
        if nome not in passi():
            sys.exit(f"Passo sconosciuto: {nome}. Passi: {', '.join(passi())}")
        return esegui_passi([nome], f"Catena, {passi()[nome][1]}")
    if "--parallelo" in argomenti:
        i = argomenti.index("--parallelo")
        n = int(argomenti[i + 1]) if i + 1 < len(argomenti) and argomenti[i + 1].isdigit() else 3
        return in_parallelo(n)
    return esegui_passi(list(passi()), "Catena a due cicli con lo strumento di campo (Excel)")


def aggiornamento(e):
    """Il registro in produzione e' nato dal template del 23/09 (dati/registro_template_2026-09-23.xlsx:
    una settimana e il primo ciclo, validati, scritti con lo script del 24/09)."""
    vecchio = DATI / "registro_template_2026-09-23.xlsx"
    with SessioneExcel(vecchio, sola_lettura=True) as sess:
        righe_prima = {n: len(campo.Scrittore(sess, MAPPA).righe(n)) for n in ("tblRegister", "tblAzioni", "tblKRI", "tblNews", "tblValidazione")}
    with tempfile.TemporaryDirectory() as tmp:
        b = Banco(tmp, vecchio)
        prima = sha(b.wb)
        for comando in (["settimanale", "--payload", DATI / "run_A3_2026-10-12.json"], ["baseline", "--uscita", b.cartella / "x.json"]):
            codice, out = b.esegui(*comando)
            e.verifica(codice == 1 and "aggiorna-registro" in out and "precedente al 25/09/2026" in out and sha(b.wb) == prima,
                       f"11. registro del template precedente: '{comando[0]}' fermato con l'indicazione di aggiorna-registro, niente scritto", out)
        codice, out = b.esegui("aggiorna-registro")
        s = b.leggi()
        e.verifica(codice == 0 and s["versione"] == campo.VERSIONE_TEMPLATE and not s["errori"] and not s["formule_mancanti"],
                   "11. aggiorna-registro: registro sulla versione nuova, zero errori di formula, formule presenti", out + str(s["errori"][:3]))
        dopo = {"tblRegister": len(s["register"]), "tblAzioni": len(carica_tabella(b, "tblAzioni")), "tblKRI": len(s["kri"]),
                "tblNews": len(s["news"]), "tblValidazione": len(s["validazione"])}
        e.verifica(dopo == righe_prima and not s["sintesi_cicli"], "11. stesse righe in ogni tabella; Sintesi_Cicli vuota (nata ora)",
                   f"prima {righe_prima}\ndopo {dopo}")
        e.verifica(not s["griglia"] and str(s["griglia_stato"]).startswith("Niente da validare"),
                   "11. registro tutto validato: griglia del foglio Validazione vuota", str(s["griglia_stato"]))
        e.verifica(any((b.uscita / "Backup").glob("NFR_workbook_prima_di_aggiorna-registro_*.xlsx")),
                   "11. il registro vecchio e' conservato in Backup")
        codice, out = b.esegui("baseline", "--uscita", b.cartella / "base.json")
        base = carica(b.cartella / "base.json")
        e.verifica(codice == 0 and uguale_ai_dati("baseline_registro_template_2026-09-23.json", b.cartella / "base.json"),
                   "11. la baseline del registro aggiornato e' identica a quella del registro vecchio", out)
        verifica_report(e, s, "11. report sul registro aggiornato (pesi D-50 su un ciclo scritto con i pesi vecchi)")
        codice, out = b.esegui("aggiorna-registro")
        e.verifica(codice == 1 and "gia' sulla versione" in out, "11. rilanciare aggiorna-registro: niente da fare", out)

        # Ciclo intero sul registro aggiornato, con un anno di adeguamento deciso dal validatore.
        with SessioneExcel(b.wb) as sess:
            posizione = next(i for i, r in campo.Scrittore(sess, MAPPA).leggi_anagrafica()[1] if r["ID"] == "NFR-05")
            sess.intervallo_nome("ANA_Anni_Adeguamento").Cells(posizione, 1).Value = 4
            sess.salva()
        run1 = {r["id_rischio"]: r for r in carica(DATI / "run1_A1_2026Q3.json")["rischi"]}
        rischi = []
        for r in base["rischi"]:
            origine = run1[r["id_rischio"]]
            rischi.append({
                # Il registro di prima ha i codici di Basilea: A1 riclassifica nella tassonomia interna (D-74),
                # qui con la categoria dei dati di prova convertiti.
                "id_rischio": r["id_rischio"], "nome": r["nome"], "event_type": origine["event_type"], "driver": r["driver"],
                "descrizione": origine["descrizione"], **{k: r[k] for k in ("impatto", "velocity", "prossimita",
                                                                             "probabilita", "anni_adeguamento")},
                # Le fonti di un registro vecchio non hanno la rilevanza (D-58): A1 la darebbe; qui 2.
                "variazioni": [], "fonti": [dict(f, rilevanza=f.get("rilevanza", 2)) for f in r["fonti"]],
                "razionale": r["razionale"],
                "azioni_mitigazione": origine["azioni_mitigazione"][:1],
                # Il registro di prima ha tre KRI per rischio, senza tipo: A1 ne ripropone due e li classifica
                # (D-64); il terzo esce di vigore.
                "kri_proposti": [{"kri_id": k["kri_id"], "tipo": tipo, "nome": k["nome"], "unita": k["unita"],
                                  "fonte_dati": k["fonte_dati"], "soglia_attenzione": k["soglia_attenzione"],
                                  "soglia_allerta": k["soglia_allerta"],
                                  "razionale": "Indicatore confermato: misura ancora il meccanismo di perdita."}
                                 for k, tipo in zip([k for k in base["kri_in_vigore"] if k["id_rischio"] == r["id_rischio"]],
                                                    ("Esposizione", "Evoluzione"))]})
        payload = {"ciclo": "2026Q4", "data_riferimento": "2026-12-31", "rischi": rischi,
                   "sintesi": ("Trimestre stabile: tutti i rischi sono confermati con le fonti del ciclo precedente. Priorita' "
                               "invariate; nessuna decisione nuova richiesta al comitato oltre alle azioni gia' approvate."),
                   "ricalcolo_kri_ciclo_precedente": [{"kri_id": k["kri_id"], "valore": None, "fonte": "Sistema di rilevazione",
                                                       "commento": "Dato del trimestre non ancora disponibile."}
                                                      for k in base["kri_in_vigore"]]}
        a5 = {"ciclo": "2026Q4", "esito": "Approvato", "sintesi": "Nessun rilievo bloccante sul ciclo 2026Q4.", "rilievi": []}
        codice, out = b.esegui("trimestrale", "--payload", b.scrivi_json("q4.json", payload), "--challenger", b.scrivi_json("a5.json", a5))
        s = b.leggi()
        e.verifica(codice == 0, "11. ciclo 2026Q4 scritto sul registro aggiornato", out)
        q4 = [k for k in s["kri"] if k["Ciclo"] == "2026Q4"]
        e.verifica(len([k for k in q4 if k["In_Vigore"] == "Sì"]) == 2 * len(rischi)
                   and all(k["Tipo"] in ("Esposizione", "Evoluzione") for k in q4 if k["In_Vigore"] == "Sì")
                   and len([k for k in q4 if k["In_Vigore"] == "No"]) == len(base["kri_in_vigore"]) - 2 * len(rischi),
                   "11. da tre KRI per rischio a due (D-64): i riproposti prendono il tipo, il terzo esce di vigore",
                   str([(k["KRI_ID"], k["Tipo"], k["In_Vigore"]) for k in q4][:8]))
        verifica_integrita(e, s, "11. 2026Q4 sul registro aggiornato")
        verifica_report(e, s, "11. report 2026Q4 sul registro aggiornato", commento=payload["sintesi"])
        attesi = mosca_attesa(s, carica_tabella(b, "tblAzioni"))
        trovati = {m[0]: (m[1], round(m[2], 6)) for m in s["mosca"]}
        e.verifica(trovati == attesi and next(a for a in s["anagrafica"] if a["ID"] == "NFR-05")["Anni_Adeguamento"] == 4,
                   "11. anni di adeguamento conservati dalla scrittura del ciclo e usati dal Radar_Mosca",
                   f"foglio {trovati}\natteso {attesi}")


def aggiornamento_25c(e):
    """Registro nato dal template 2026-09-25c (dati/registro_template_2026-09-25c.xlsx: un ciclo validato,
    con Gap_Controlli nel RiskRegister e Dimensione nelle Azioni). Colonne dismesse dal 30/09 (D-49, D-54)."""
    vecchio = DATI / "registro_template_2026-09-25c.xlsx"
    tabelle = ("tblRegister", "tblAzioni", "tblKRI", "tblNews", "tblValidazione")
    with SessioneExcel(vecchio, sola_lettura=True) as sess:
        righe_prima = {n: sess.tabella(n).ListRows.Count for n in tabelle}
    def riapri(banco, oggetto, decisione=None):
        """Rimette 'Da decidere' le righe dello storico del primo oggetto del tipo dato nel ciclo 2026Q3, e scrive
        nel vecchio formato (una riga per campo) una decisione su un campo: (campo, valore, motivazione)."""
        with SessioneExcel(banco.wb) as sess:
            lo = sess.tabella("tblValidazione")
            col = {c.Name: c.Index for c in lo.ListColumns}
            righe = [lo.ListRows(i).Range for i in range(1, lo.ListRows.Count + 1)]
            ident = next(r.Cells(1, col["ID"]).Value for r in righe
                         if r.Cells(1, col["Oggetto"]).Value == oggetto and str(r.Cells(1, col["Periodo"]).Value) == "2026Q3")
            for r in righe:
                if r.Cells(1, col["ID"]).Value == ident and str(r.Cells(1, col["Periodo"]).Value) == "2026Q3":
                    r.Cells(1, col["Stato"]).Value = "Da decidere"
                    for c in ("Decisione", "Valore_Validato", "Motivazione", "Validato_Da", "Data_Validazione"):
                        r.Cells(1, col[c]).Value = None
                    if decisione and r.Cells(1, col["Campo"]).Value == decisione[0]:
                        r.Cells(1, col["Decisione"]).Value = "Rettificato"
                        r.Cells(1, col["Valore_Validato"]).Value = decisione[1]
                        r.Cells(1, col["Motivazione"]).Value = decisione[2]
            sess.salva()
        return ident

    with tempfile.TemporaryDirectory() as tmp:
        # Righe ancora da decidere su campi tolti dal modello (Severity, Confidence, Gap_Controlli): la griglia non
        # le puo' mostrare, quindi aggiorna-registro si ferma prima di copiare.
        b = Banco(tmp, vecchio)
        riapri(b, "Rischio")
        prima = sha(b.wb)
        codice, out = b.esegui("aggiorna-registro")
        e.verifica(codice == 1 and "campi che il modello non ha piu'" in out and sha(b.wb) == prima,
                   "11b. righe 'Da decidere' su campi tolti dal modello: aggiorna-registro fermo prima di copiare, registro intatto", out)
    with tempfile.TemporaryDirectory() as tmp:
        # Righe ancora da decidere su campi attuali, con una decisione gia' scritta nel vecchio foglio Validazione:
        # passano nella griglia con quella decisione e si validano con il comando valida.
        b = Banco(tmp, vecchio)
        motivo = "Valore definitivo comunicato dopo la scrittura del ciclo."
        kri = riapri(b, "KRI", ("Valore_Corrente", 7.5, motivo))
        codice, out = b.esegui("aggiorna-registro")
        s = b.leggi()
        voce = s["griglia"].get(("KRI", "2026Q3", kri), {})
        e.verifica(codice == 0 and "Righe ancora da validare: 1" in out and len(s["griglia"]) == 1
                   and voce.get("valori", {}).get("Valore_Corrente") == 7.5 and voce.get("motivazione") == motivo,
                   "11b. righe 'Da decidere' su campi attuali: nella griglia, con la decisione scritta nel vecchio formato",
                   out + str(s["griglia"]))
        codice, out = b.esegui("valida", "--periodo", "2026Q3", "--validatore", "Comitato Rischi")
        k = next(r for r in carica_tabella(b, "tblKRI") if r["Ciclo"] == "2026Q3" and r["KRI_ID"] == kri)
        e.verifica(codice == 0 and "rettificate 1" in out and k["Valore_Corrente"] == 7.5 and k["Validazione"] == "Rettificato",
                   "11b. la decisione migrata si valida con il comando valida", out + str(k))
    with tempfile.TemporaryDirectory() as tmp:
        b = Banco(tmp, vecchio)
        codice, out = b.esegui("aggiorna-registro")
        s = b.leggi()
        e.verifica(codice == 0 and s["versione"] == campo.VERSIONE_TEMPLATE and not s["errori"] and not s["formule_mancanti"],
                   "11b. aggiorna-registro dal 2026-09-25c: versione nuova, zero errori di formula", out + str(s["errori"][:3]))
        with SessioneExcel(b.wb, sola_lettura=True) as sess:
            dopo = {n: sess.tabella(n).ListRows.Count for n in tabelle}
            colonne = {n: [c.Name for c in sess.tabella(n).ListColumns] for n in ("tblRegister", "tblAzioni")}
        e.verifica(dopo == righe_prima and not {"Gap_Controlli", "Confidence", "Severity"} & set(colonne["tblRegister"])
                   and "Dimensione" not in colonne["tblAzioni"] and {"Rilievi", "Impatto", "Anni_Adeguamento"} <= set(colonne["tblRegister"]),
                   "11b. stesse righe; Gap_Controlli, Confidence e Dimensione (dismesse) non copiate; Severity diventa Impatto (D-57)",
                   f"prima {righe_prima}\ndopo {dopo}\n{colonne}")
        e.verifica(s["anagrafica"] and all(a.get("Presidio_Controlli") == "Non verificato" for a in s["anagrafica"]),
                   "11b. presidio dei controlli 'Non verificato' per ogni rischio (D-49)", str([a.get("Presidio_Controlli") for a in s["anagrafica"]]))
        e.verifica(any((b.uscita / "Backup").glob("NFR_workbook_prima_di_aggiorna-registro_*.xlsx")),
                   "11b. il registro vecchio (con le colonne dismesse) e' conservato in Backup")
        codice, out = b.esegui("baseline", "--uscita", b.cartella / "base.json")
        e.verifica(codice == 0 and uguale_ai_dati("baseline_registro_template_2026-09-25c.json", b.cartella / "base.json"),
                   "11b. baseline del registro aggiornato = quella attesa (senza Gap_Controlli, con il presidio)", out)
        verifica_report(e, s, "11b. report sul registro aggiornato dal 2026-09-25c")


def segnalazioni_in_validazione(e):
    """12. A5 facoltativo e segnalazioni in validazione (D-71): le regole di metodo (C3, soglie di C9) e i Bloccanti di A5
    non fermano il ciclo, vanno nella colonna Segnalazioni della griglia e chiedono una Motivazione; valida non accetta
    un salto di due punti ne' soglie invertite; un difetto di integrita' ferma comunque."""
    run1 = carica(DATI / "run1_A1_2026Q3.json")
    con_segnalazioni = copy.deepcopy(run1)
    next(r for r in con_segnalazioni["rischi"] if r["id_rischio"] == "NFR-03").update(prossimita=5)       # C3: da 3 a 5
    next(r for r in con_segnalazioni["rischi"] if r["id_rischio"] == "NFR-01")["kri_proposti"][0].update(
        soglia_attenzione=9, soglia_allerta=2)                                                          # C9: invertite
    a5 = copy.deepcopy(carica(DATI / "run_A5_2026Q3.json"))
    a5["esito"] = "Da rivedere"
    a5["rilievi"].append({"controllo": "C4", "id_rischio": "NFR-12", "gravita": "Bloccante",
                          "descrizione": "Prossimita 4 senza un caso nominato fuori dalla Banca: il descrittore chiede 3."})
    with tempfile.TemporaryDirectory() as tmp:
        b = Banco(tmp)
        f_a5 = b.scrivi_json("a5_bloccante.json", a5)
        prima = sha(b.wb)
        rotto = copy.deepcopy(con_segnalazioni)
        rotto["rischi"] = [r for r in rotto["rischi"] if r["id_rischio"] != "NFR-04"]
        codice, out = b.esegui("trimestrale", "--payload", b.scrivi_json("senza_04.json", rotto), "--challenger", f_a5)
        e.verifica(codice == 1 and "C1" in out and "Messaggio per A1" in out and sha(b.wb) == prima,
                   "12. un difetto di integrita' (rischio mancante, C1) ferma comunque, con il messaggio per A1 (D-10, D-71)", out)
        # --procedi-con-rilievi dei comandi gia' in uso: accettata, non serve piu' (lo dice).
        codice, out = b.esegui("trimestrale", "--payload", b.scrivi_json("seg.json", con_segnalazioni), "--challenger", f_a5,
                               "--procedi-con-rilievi", "--motivo", "ok")
        s = b.leggi()
        reg = {r["ID_Rischio"]: str(r["Rilievi"] or "") for r in s["register"] if r["Ciclo"] == "2026Q3"}
        e.verifica(codice == 0 and "non serve piu'" in out and "SEGNALAZIONI DA MOTIVARE: 3 su 3 rischi" in out
                   and all(campo.DA_MOTIVARE in reg[k] for k in ("NFR-01", "NFR-03", "NFR-12"))
                   and "C4 · A5" in reg["NFR-12"] and "C9 · controlli" in reg["NFR-01"] and "C3 · controlli" in reg["NFR-03"]
                   and "C5" in reg["NFR-06"] and campo.DA_MOTIVARE not in reg["NFR-06"],
                   "12. C3, soglie di C9 e il Bloccante di A5 non fermano: il ciclo si scrive e ogni segnalazione sta sul suo "
                   "rischio (DA MOTIVARE), l'osservazione di A5 resta osservazione", out + f"\n{reg}")
        sint = next(r for r in s["sintesi_cicli"] if r["Ciclo"] == "2026Q3")
        atteso = "Segnalazioni da motivare in validazione: 3 (controlli 2, A5 1)."
        e.verifica(sint["Rilievi_Superati"] == atteso and atteso in str(s["rilievi_superati"]),
                   "12. Sintesi_Cicli e Quadro dicono quante segnalazioni sono da motivare",
                   f"{sint['Rilievi_Superati']!r}\n{s['rilievi_superati']!r}")
        rapporto = carica(b.uscita / "Cicli" / "2026Q3" / "Esito_controlli_2026Q3.json")
        e.verifica(rapporto.get("a5_usato") is True and len(rapporto.get("da_motivare", [])) == 3,
                   "12. Esito_controlli: A5 usato e le tre segnalazioni da motivare", str(rapporto.get("da_motivare"))[:400])
        verifica_integrita(e, s, "12. ciclo scritto con segnalazioni da motivare")
        con_bandiera = {i for i, n in s["griglia_nomi"].items() if str(n).startswith("⚑ ")}
        seg = s["griglia_segnalazioni"]
        e.verifica(con_bandiera == {"NFR-01", "NFR-03", "NFR-12"}
                   and all(campo.DA_MOTIVARE in str(seg.get(k)) for k in con_bandiera)
                   and "soglie invertite" in str(seg["NFR-01"]) and "C4" in str(seg["NFR-12"])
                   and all(str(seg.get(k) or "") == reg[k] for k in seg),
                   "12. griglia: ⚑ sui soli rischi con segnalazioni da motivare; la colonna Segnalazioni riporta il testo "
                   "del registro (anche il KRI con le soglie invertite, sotto il suo rischio)", f"{con_bandiera}\n{seg}")
        prima = sha(b.wb)
        codice, out = b.esegui("valida", "--periodo", "2026Q3", "--validatore", "Comitato Rischi")
        e.verifica(codice == 1 and "NFR-12" in out and "segnalazioni da motivare" in out and "non accettabile" in out
                   and "minore della Soglia attenzione" in out and sha(b.wb) == prima,
                   "12. valida su righe non toccate: chiede le motivazioni, non accetta il salto di due punti ne' le soglie "
                   "invertite proposte da A1", out)
        motivo12 = "Casi interni documentati dal report operativo di maggio: valori confermati."
        proposta05 = next(r["Proposta_Agente"] for r in s["validazione"]
                          if r["Periodo"] == "2026Q3" and r["ID"] == "NFR-05" and r["Campo"] == "Prossimita")
        scrivi_decisioni(b.wb, "2026Q3", [
            {"oggetto": "Rischio", "id": "NFR-12", "campo": "", "decisione": "Accettato", "motivazione": motivo12},
            {"oggetto": "Rischio", "id": "NFR-03", "campo": "Prossimita", "decisione": "Rettificato", "valore": 4,
             "motivazione": "Un solo punto per ciclo: la sanzione di luglio porta la Prossimita a 4."},
            {"oggetto": "Rischio", "id": "NFR-01", "campo": "", "decisione": "Accettato",
             "motivazione": "Soglie del KRI corrette nella sua riga; valori del rischio confermati."},
            {"oggetto": "KRI", "id": "NFR-01-K1", "campo": "Soglia_Attenzione", "decisione": "Rettificato", "valore": 3,
             "motivazione": "Soglie invertite da A1: ripristinate quelle della Banca."},
            {"oggetto": "KRI", "id": "NFR-01-K1", "campo": "Soglia_Allerta", "decisione": "Rettificato", "valore": 6},
            {"oggetto": "Rischio", "id": "NFR-05", "campo": "Prossimita", "decisione": "Rettificato", "valore": 9,
             "motivazione": "Valore scritto per sbaglio durante la validazione."}])
        # Un settimanale scritto mentre il ciclo e' in validazione: la griglia aggiunge le notizie, conserva cio'
        # che il validatore ha gia' scritto e un valore sbagliato li' non produce errori di formula (IFERROR).
        codice, out = b.esegui("settimanale", "--payload", DATI / "run_A3_2026-10-12.json")
        s = b.leggi()
        g = s["griglia"]
        e.verifica(codice == 0 and not s["errori"] and len(g) == 53 + 5
                   and g[("Rischio", "2026Q3", "NFR-12")]["motivazione"] == motivo12
                   and g[("Rischio", "2026Q3", "NFR-05")]["valori"]["Prossimita"] == 9
                   and campo.DA_MOTIVARE in str(s["griglia_segnalazioni"].get("NFR-12")),
                   "12. settimanale durante la validazione: notizie aggiunte alla griglia, cio' che e' gia' scritto resta "
                   "(anche le segnalazioni), un valore sbagliato nella griglia non ferma la scrittura", out + str(s["errori"][:3]))
        codice, out = b.esegui("valida", "--periodo", "2026Q3", "--validatore", "Comitato Rischi")
        e.verifica(codice == 1 and "intero da 1 a 5" in out, "12. valida segnala il valore sbagliato rimasto nella griglia", out)
        scrivi_decisioni(b.wb, "2026Q3", [{"oggetto": "Rischio", "id": "NFR-05", "campo": "Prossimita", "decisione": "Rettificato",
                                           "valore": proposta05, "motivazione": ""}])
        codice, out = b.esegui("valida", "--periodo", "2026Q3", "--validatore", "Comitato Rischi")
        e.verifica(codice == 0, "12. validazione con le motivazioni, il salto riportato a un punto e le soglie corrette: applicata", out)
        s = b.leggi()
        riga = next(r for r in s["validazione"] if r["Periodo"] == "2026Q3" and r["ID"] == "NFR-12" and r["Campo"] == "Prossimita")
        r03 = next(r for r in s["register"] if r["Ciclo"] == "2026Q3" and r["ID_Rischio"] == "NFR-03")
        k01 = next(k for k in s["kri"] if k["Ciclo"] == "2026Q3" and k["KRI_ID"] == "NFR-01-K1")
        e.verifica(riga["Decisione"] == "Accettato" and riga["Motivazione"] == motivo12 and r03["Prossimita"] == 4
                   and (k01["Soglia_Attenzione"], k01["Soglia_Allerta"]) == (3, 6),
                   "12. la motivazione resta accanto alla proposta; Prossimita e soglie validate nel registro",
                   f"{riga}\n{r03['Prossimita']} {k01['Soglia_Attenzione']} {k01['Soglia_Allerta']}")
        e.verifica(set(k[0] for k in s["griglia"]) == {"Notizia"} and len(s["griglia"]) == 5
                   and str(s["griglia_stato"]).startswith("Da validare: settimana del 12/10/2026"),
                   "12. dopo valida restano nella griglia solo le notizie della settimana, ancora da validare", str(s["griglia_stato"]))


def produzione(e, template=TEMPLATE, etichetta="10"):
    """Il registro vero parte vuoto e, fino al primo ciclo, riceve solo le
    settimane: nessun rischio a cui collegare le notizie. Poi il primo ciclo
    (tutti i rischi nuovi), il blocco del ciclo dopo, la validazione e la
    baseline del secondo ciclo. `template` permette di rifare il percorso sul
    template con cui e' stato creato un registro gia' in uso."""
    run1 = carica(DATI / "run1_A1_2026Q3.json")
    a3 = carica(DATI / "run_A3_2026-10-12.json")
    with tempfile.TemporaryDirectory() as tmp:
        b = Banco(tmp, template)
        b.wb.unlink()
        codice, out = b.esegui("inizializza", "--ciclo-precedente", "2026Q2", "--settimana", "2026-10-05", "--template", template)
        s = b.leggi()
        e.verifica(codice == 0 and not s["register"] and not s["anagrafica"] and not s["kri"] and not s["news"]
                   and not s["validazione"] and not s["griglia"] and str(s["griglia_stato"]).startswith("Niente da validare")
                   and not s["errori"],
                   f"{etichetta}. registro di produzione: parte senza rischi, senza dati, griglia vuota, senza errori di formula",
                   out + str(s["errori"][:3]))

        # Settimane prima del primo ciclo: A3 non ha rischi a cui collegare le notizie.
        sett = copy.deepcopy(a3)
        sett["flag_proposti"] = []
        for n in sett["notizie"]:
            n["rischio_collegato"] = None
        collegata = copy.deepcopy(sett)
        collegata["notizie"][0]["rischio_collegato"] = "NFR-02"
        prima = sha(b.wb)
        codice, out = b.esegui("settimanale", "--payload", b.scrivi_json("a3_collegata.json", collegata))
        e.verifica(codice == 1 and "non sono nel registro" in out and sha(b.wb) == prima,
                   f"{etichetta}. registro vuoto: una notizia collegata a un rischio inesistente e' fermata, niente scritto", out)
        codice, out = b.esegui("settimanale", "--payload", b.scrivi_json("a3_vuoto.json", sett))
        s = b.leggi()
        e.verifica(codice == 0 and len(s["news"]) == len(sett["notizie"]) and not s["errori"] and not s["formule_mancanti"],
                   f"{etichetta}. settimana sul registro vuoto: {len(sett['notizie'])} notizie scritte, zero errori di formula",
                   out + str(s["errori"][:3]))
        e.verifica(all(r["Rischio_ID"] == campo.NON_PRESIDIATO for r in s["news"]),
                   f"{etichetta}. senza rischi ogni notizia e' NON PRESIDIATO", str([r["Rischio_ID"] for r in s["news"]]))
        forti = {i["event_type"] for n in sett["notizie"] for i in n["impatti"] if i["intensita"] >= 2}
        scoperte = {k for k, v in s["presidio"].items() if v == "AREA NON PRESIDIATA"}
        e.verifica(scoperte and scoperte <= forti,
                   f"{etichetta}. Notizie segnala come non presidiate le aree con notizie forti ({sorted(scoperte)})",
                   f"segnalate {sorted(scoperte)}, con intensita' >= 2 {sorted(forti)}")
        codice, out = b.esegui("valida", "--periodo", sett["settimana"], "--validatore", "Corrado")
        e.verifica(codice == 0, f"{etichetta}. validazione della settimana sul registro vuoto", out)

        # Primo ciclo: A1 individua i rischi da zero (tutti nuovi).
        primo = copy.deepcopy(run1)
        primo["ricalcolo_kri_ciclo_precedente"] = []
        for r in primo["rischi"]:
            r.update(variazioni=[])                   # l'esito "Nuovo" lo calcola lo script (D-51)
            for k in r["kri_proposti"]:
                k["kri_id"] = None
        # D-71: A5 facoltativo; qui il primo ciclo si scrive senza il suo esito.
        codice, out = b.esegui("trimestrale", "--payload", b.scrivi_json("primo.json", primo))
        s = b.leggi()
        # D-79: NFR-16 (Prossimita 1) nasce in osservazione: nel registro, non nell'anagrafica (= il radar).
        nel_radar = [r for r in primo["rischi"] if r["kri_proposti"]]
        e.verifica(codice == 0 and len(s["register"]) == len(primo["rischi"]) and len(s["anagrafica"]) == len(nel_radar)
                   and [r["ID_Rischio"] for r in s["register"] if r["Stato"] == "Osservazione"] == ["NFR-16"]
                   and all(r["Esito"] == "Nuovo" for r in s["register"]) and len(s["news"]) == len(sett["notizie"])
                   and "A5: non usato (facoltativo)" in out,
                   f"{etichetta}. primo ciclo sul registro di produzione, senza A5 (D-71): {len(primo['rischi'])} rischi nuovi, "
                   f"{len(nel_radar)} nel radar e NFR-16 in osservazione; notizie delle settimane intatte", out)
        sintesi_a5 = next((r["Sintesi_A5"] for r in s["sintesi_cicli"]), "")
        e.verifica(str(sintesi_a5).startswith("A5 non usato in questo ciclo"),
                   f"{etichetta}. senza A5 Sintesi_Cicli (e il Quadro) lo dice", str(sintesi_a5))
        verifica_integrita(e, s, f"{etichetta}. primo ciclo")
        e.verifica(str(s["f8"]).startswith("CICLO NON ANCORA VALIDATO"),
                   f"{etichetta}. Registro: primo ciclo non ancora validato", str(s["f8"]))

        # Il ciclo dopo non parte finche' il primo non e' validato.
        prima = sha(b.wb)
        codice, out = b.esegui("trimestrale", "--payload", DATI / "run3_A1_2026Q4.json",
                               "--challenger", DATI / "run_A5_2026Q4.json")
        e.verifica(codice == 1 and "non e' ancora validato" in out and sha(b.wb) == prima,
                   f"{etichetta}. il secondo ciclo e' bloccato finche' il primo non e' validato", out)

        # Validazione del primo ciclo e baseline del secondo. --accetta-il-resto non serve piu' (D-67): resta accettato
        # per i comandi gia' in uso, e lo dice.
        codice, out = b.esegui("valida", "--periodo", "2026Q3", "--validatore", "Corrado", "--accetta-il-resto")
        e.verifica(codice == 0 and "non serve piu'" in out, f"{etichetta}. --accetta-il-resto ancora accettato, con l'avviso", out)
        s = b.leggi()
        e.verifica(codice == 0 and s["f8"] == "Ciclo validato"
                   and all(r["Validazione"] == "Accettato" and r["Approvato_Da"] == "Corrado" for r in s["register"]),
                   f"{etichetta}. primo ciclo validato: ogni rischio accettato, validatore registrato", out + str(s["f8"]))
        codice, out = b.esegui("baseline", "--uscita", b.cartella / "base_secondo.json")
        base = carica(b.cartella / "base_secondo.json")
        e.verifica(codice == 0 and base["ciclo_precedente"] == "2026Q3" and base["ciclo_da_valutare"] == "2026Q4"
                   and len(base["rischi"]) == len(nel_radar) and all(r["esito_precedente"] == "Nuovo" for r in base["rischi"])
                   and [r["id_rischio"] for r in base["rischi_in_osservazione"]] == ["NFR-16"]
                   and len(base["kri_in_vigore"]) == 2 * len(nel_radar),
                   f"{etichetta}. baseline del secondo ciclo: {len(nel_radar)} rischi validati nel radar, NFR-16 in "
                   f"osservazione e {2 * len(nel_radar)} KRI in vigore (due per rischio del radar, D-64)", out)


def _notizia(nid, data, rischio, segnale, impatti, titolo):
    """Una notizia di A3 nel formato dello schema: impatti = {event type: intensita'} (gli altri 0)."""
    return {"id_notizia": nid, "data": data, "titolo": titolo, "fonte": "Agenzia di stampa", "codice_fonte": "FNT-17",
            "sintesi": "Notizia costruita per il collaudo delle viste dopo la validazione.",
            "rischio_collegato": rischio, "segnale": segnale,
            "impatti": [{"event_type": c, "intensita": impatti.get(c, 0),
                         "direzione": segnale if impatti.get(c, 0) else "Non rilevante"} for c in controlli_a5.CATEGORIE]}


def notizie_vista(banco):
    """Foglio Notizie per categoria (D-74): (intensita' massima nelle 4 settimane, presidio)."""
    with SessioneExcel(banco.wb, sola_lettura=True) as s:
        s.ricalcola()
        ws = s.foglio("Notizie")
        return {ws.Range(f"A{r}").Value: (ws.Range(f"C{r}").Value, ws.Range(f"F{r}").Value) for r in range(5, 5 + len(controlli_a5.CATEGORIE))}


def massimo_finestra(stato, codice):
    """Intensita' massima di una categoria nel NewsLog, nella finestra di 4 settimane che chiude con la settimana
    corrente: lo stesso calcolo della colonna C del foglio Notizie. La finestra si sposta quando arriva una
    settimana nuova, quindi il valore di prima non e' un riferimento."""
    def iso(v):
        if hasattr(v, "year"):
            return f"{v.year:04d}-{v.month:02d}-{v.day:02d}"
        if isinstance(v, (int, float)):
            return (datetime.date(1899, 12, 30) + datetime.timedelta(days=int(v))).isoformat()
        return str(v)[:10]
    fine = datetime.date.fromisoformat(iso(stato["settimana"]))
    inizio = (fine - datetime.timedelta(days=21)).isoformat()
    colonna = "Imp_" + codice.replace(".", "_")
    return max((n.get(colonna) or 0 for n in stato["news"] if inizio <= iso(n["Settimana"]) <= fine.isoformat()), default=0)


def notizie_validate(e):
    """Passo 3b: le notizie entrano nelle viste (Registro, Notizie, livello di allerta, Quadro) appena scritte, e
    la validazione le cambia anche li': una notizia respinta diventa "Non rilevante" con impatti 0 e sparisce dai
    conteggi, un segnale rettificato conta con il valore del validatore."""
    netti = lambda stato, rid: int(str(stato["badge"].get(rid) or "0").split()[-1])
    with tempfile.TemporaryDirectory() as tmp:
        b = Banco(tmp)
        s0, v0 = b.leggi(), notizie_vista(b)
        a3 = {"settimana": "2026-07-06", "flag_proposti": [],
              "sintesi": "Settimana di prova: due segnali peggiorativi su NFR-08, una notizia su un'area senza rischi, "
                         "una notizia neutra su NFR-09.",
              "notizie": [_notizia("N-20260701-01", "2026-07-01", "NFR-08", "Peggiorativo", {"9.7": 3},
                                   "Accessi impropri di un dipendente ai conti di clienti noti"),
                          _notizia("N-20260702-01", "2026-07-02", "NFR-08", "Peggiorativo", {"9.7": 1},
                                   "Sanzione a una banca per controlli deboli sugli accessi ai dati"),
                          _notizia("N-20260702-02", "2026-07-02", None, "Peggiorativo", {"9.11": 3},
                                   "Vertenza nazionale sui turni dei tecnici IT"),
                          _notizia("N-20260703-01", "2026-07-03", "NFR-09", "Neutro", {"9.4": 1},
                                   "Nuove linee guida sui controlli delle triangolazioni")]}
        codice, out = b.esegui("settimanale", "--payload", b.scrivi_json("a3_prova.json", a3))
        s1, v1 = b.leggi(), notizie_vista(b)
        e.verifica(codice == 0 and netti(s1, "NFR-08") == netti(s0, "NFR-08") + 2 and netti(s1, "NFR-09") == netti(s0, "NFR-09"),
                   "3b. notizie scritte: segnali netti del Registro (NFR-08 +2, NFR-09 invariato da un Neutro)",
                   f"{out}\nprima {s0['badge']}\ndopo {s1['badge']}")
        e.verifica(str(s1["badge"]["NFR-08"]).startswith("▲") and "notizie in peggioramento" in str(s1["livello"]["NFR-08"][1]),
                   "3b. due peggiorativi su NFR-08: badge ▲ e segnale forte F3 nel livello di allerta (D-63)",
                   f"{s1['badge']['NFR-08']} {s1['livello']['NFR-08']}")
        e.verifica(any(r["Settimana"] == "2026-07-06" and r["Flag_Proposti"] == "Nessun flag proposto" for r in s1["settimane"]),
                   "3b. una settimana senza flag: 'Nessun flag proposto' in Sintesi_Settimane", str(s1["settimane"]))
        e.verifica(v1["9.11"] == (3, "AREA NON PRESIDIATA") and v1["9.7"][0] == 3,
                   "3b. foglio Notizie: intensita' massima 3 su 9.7, 9.11 (Employer) area non presidiata", str(v1))
        verifica_report(e, s1, "3b. dopo la scrittura della settimana")

        # Stato cancellato a mano nello storico (successo in Banca il 01/10, quando si validava li'): valida lo dice e
        # indica il rimedio.
        def stato_settimana(valore):
            with SessioneExcel(b.wb) as sess:
                lo = sess.tabella("tblValidazione")
                col = {c.Name: c.Index for c in lo.ListColumns}
                for i in range(1, lo.ListRows.Count + 1):
                    riga = lo.ListRows(i).Range
                    if str(riga.Cells(1, col["Periodo"]).Value) == "2026-07-06":
                        riga.Cells(1, col["Stato"]).Value = valore
                sess.salva()
        stato_settimana(None)
        codice, out = b.esegui("valida", "--periodo", "2026-07-06", "--validatore", "Funzione Risk Management")
        e.verifica(codice == 1 and "Stato vuoto o modificato a mano" in out and "Da decidere" in out and "griglia" in out,
                   "3b. Stato cancellato a mano nello storico: valida si ferma e indica il rimedio", out)
        stato_settimana("Da decidere")
        codice, out = b.esegui("griglia")
        e.verifica(codice == 0 and "Notizia 4" in out, "3b. rimedio: il comando griglia riporta le notizie nel foglio Validazione", out)
        scrivi_decisioni(b.wb, "2026-07-06", [
            {"oggetto": "Notizia", "id": "N-20260701-01", "campo": "Segnale", "decisione": "Respinto",
             "motivazione": "Episodio isolato gia' gestito, non e' un segnale sul meccanismo di perdita."},
            {"oggetto": "Notizia", "id": "N-20260702-02", "campo": "Segnale", "decisione": "Respinto",
             "motivazione": "Vertenza conclusa prima della pubblicazione: nessun effetto sulla Banca."},
            {"oggetto": "Notizia", "id": "N-20260703-01", "campo": "Segnale", "decisione": "Rettificato", "valore": "Peggiorativo",
             "motivazione": "Le linee guida mostrano che le triangolazioni crescono: segnale peggiorativo per NFR-09."}])
        codice, out = b.esegui("valida", "--periodo", "2026-07-06", "--validatore", "Funzione Risk Management")
        s2, v2 = b.leggi(), notizie_vista(b)
        respinta = next(n for n in s2["news"] if n["ID_Notizia"] == "N-20260701-01")
        e.verifica(codice == 0 and respinta["Segnale"] == "Non rilevante" and respinta["Imp_9_7"] == 0,
                   "3b. notizia respinta: segnale 'Non rilevante' e impatti a zero nel NewsLog", out + str(respinta))
        e.verifica(netti(s2, "NFR-08") == netti(s0, "NFR-08") + 1 and netti(s2, "NFR-09") == netti(s0, "NFR-09") + 1,
                   "3b. dopo la validazione il Registro conta i valori validati (NFR-08 +1: uno respinto; NFR-09 +1: rettificato)",
                   f"prima {s0['badge']}\ndopo {s2['badge']}")
        e.verifica(s2["livello"]["NFR-08"][0] == s0["livello"]["NFR-08"][0]
                   and "notizie in peggioramento" not in str(s2["livello"]["NFR-08"][1]),
                   "3b. il livello di allerta di NFR-08 torna quello di prima: il segnale forte F3 cade con la notizia respinta",
                   f"prima {s0['livello']['NFR-08']}\nsettimana {s1['livello']['NFR-08']}\nvalidato {s2['livello']['NFR-08']}")
        e.verifica(v2["9.11"] == v0["9.11"] and v1["9.7"][0] == massimo_finestra(s1, "9.7") == 3
                   and v2["9.7"][0] == massimo_finestra(s2, "9.7") < 3,
                   "3b. foglio Notizie: la notizia respinta esce dai conteggi (9.11 come prima della settimana; "
                   "9.7 = il massimo delle notizie rimaste nella finestra di 4 settimane, sotto il 3 della respinta)",
                   f"prima {v0}\nsettimana {v1}\nvalidato {v2}\n"
                   f"NewsLog: settimana {massimo_finestra(s1, '9.7')}, validato {massimo_finestra(s2, '9.7')}")
        verifica_report(e, s2, "3b. dopo la validazione della settimana")


def riapertura(e):
    """Passo 13 (D-76): il ciclo corrente del template (2026Q2, validato) si riapre e si valida di nuovo, quante volte
    serve. Riga non toccata = niente cambia; valore cambiato = rettifica senza il limite di un punto, con la Motivazione;
    Respingi = Sì toglie un KRI; un'azione rettificata resta approvata. Decisione sullo stato (D-79): un rischio in
    osservazione entra nel radar, uno del radar esce."""
    validatore = "Funzione Risk Management"
    with tempfile.TemporaryDirectory() as tmp:
        b = Banco(tmp)
        s0 = b.leggi()
        ciclo = s0["ciclo"]
        rr = lambda s: {r["ID_Rischio"]: r for r in s["register"] if r["Ciclo"] == ciclo}
        per_oggetto = lambda s: {o: sum(1 for k in s["griglia"] if k[0] == o) for o in ("Rischio", "KRI", "Azione")}
        attesi = {"Rischio": len(rr(s0)), "KRI": sum(1 for k in s0["kri"] if k["Ciclo"] == ciclo and k["In_Vigore"] == "Sì"),
                  "Azione": len(carica_tabella(b, "tblAzioni")) - sum(1 for a in carica_tabella(b, "tblAzioni")
                                                                       if a["Stato"] in ("Respinta", "Completata", "Annullata"))}
        n_storico = len(s0["validazione"])
        codice, out = b.esegui("riapri")
        s1 = b.leggi()
        traccia = b.uscita / "Cicli" / ciclo / f"Riapertura_{ciclo}.json"
        e.verifica(codice == 0 and traccia.exists() and carica(traccia)["ciclo"] == ciclo and carica(traccia)["rischi"] == "tutti",
                   "13. riapri lascia la traccia Riapertura_<ciclo>.json per l'app (D-83)", out)
        e.verifica(codice == 0 and per_oggetto(s1) == attesi and rr(s1) == rr(s0),
                   "13. riapri: rischi (15: 12 del radar e 3 in osservazione), KRI in vigore e azioni aperte tornano nella "
                   "griglia; il registro non cambia", f"{out}\ngriglia {per_oggetto(s1)}\natteso {attesi}")
        e.verifica("RIAPERTURA" in str(s1["griglia_stato"]) or "Da validare" in str(s1["griglia_stato"]),
                   "13. il foglio Validazione dice che c'e' da validare", str(s1["griglia_stato"]))
        prima = sha(b.wb)
        codice, out = b.esegui("riapri")
        e.verifica(codice == 1 and "gia'" in out and sha(b.wb) == prima,
                   "13. riaprire un ciclo gia' riaperto: fermato, niente scritto", out)
        p_nfr02 = rr(s0)["NFR-02"]["Probabilita"]
        decisioni = [
            {"oggetto": "Rischio", "id": "NFR-02", "campo": "Probabilita", "decisione": "Rettificato", "valore": p_nfr02 + 2,
             "motivazione": "Secondo incidente del fornitore cloud con ripristino oltre i tempi contrattuali."},
            {"oggetto": "Rischio", "id": "NFR-05", "campo": "Impatto", "decisione": "Rettificato", "valore": 5},
            {"oggetto": "KRI", "id": "NFR-01-K1", "campo": "Valore_Corrente", "decisione": "Respinto",
             "motivazione": "Indicatore sostituito dal nuovo cruscotto antifrode."},
            {"oggetto": "Azione", "id": "2026Q2-NFR-04-A1", "campo": "Owner", "decisione": "Rettificato",
             "valore": "Funzione Continuita' Operativa", "motivazione": "Passaggio di responsabilita' deciso dal comitato IT."},
            {"oggetto": "Rischio", "id": "NFR-14", "campo": "Decisione_Stato", "decisione": "Rettificato", "valore": "Radar",
             "motivazione": "Il comitato vuole KRI e azioni sui cavi sottomarini dopo l'esercitazione delle autorita'."},
            {"oggetto": "Rischio", "id": "NFR-12", "campo": "Decisione_Stato", "decisione": "Rettificato",
             "valore": "Osservazione", "motivazione": "Adeguamento ai bonifici istantanei concluso: basta osservarlo."}]
        scrivi_decisioni(b.wb, ciclo, decisioni)
        prima = sha(b.wb)
        codice, out = b.esegui("valida", "--periodo", ciclo, "--validatore", validatore)
        e.verifica(codice == 1 and "NFR-05" in out and "Motivazione" in out and sha(b.wb) == prima,
                   "13. un valore cambiato senza Motivazione ferma la validazione riaperta: niente applicato", out)
        scrivi_decisioni(b.wb, ciclo, [dict(decisioni[1], motivazione="Perdita rilevante segnalata dalla funzione Operations.")])
        codice, out = b.esegui("valida", "--periodo", ciclo, "--validatore", validatore)
        s2 = b.leggi()
        r2 = rr(s2)
        e.verifica(codice == 0 and r2["NFR-02"]["Probabilita"] == p_nfr02 + 2 and r2["NFR-05"]["Impatto"] == 5
                   and r2["NFR-02"]["Validazione"] == "Rettificato" and r2["NFR-02"]["Approvato_Da"] == validatore,
                   "13. valida dopo riapri: due punti in piu' accettati (nessun limite in riapertura), con chi ha deciso",
                   f"{out}\nNFR-02 {r2['NFR-02']['Probabilita']} NFR-05 {r2['NFR-05']['Impatto']}")
        e.verifica(all(r2[i] == r for i, r in rr(s0).items() if i not in ("NFR-02", "NFR-05", "NFR-12", "NFR-14")),
                   "13. le righe non toccate restano identiche (valori, validazione, chi e quando)")
        anag = {a["ID"]: a for a in s2["anagrafica"]}
        kri_12 = [k for k in s2["kri"] if k["Ciclo"] == ciclo and k["ID_Rischio"] == "NFR-12"]
        e.verifica((r2["NFR-14"]["Stato"], r2["NFR-14"]["Movimento"], r2["NFR-14"]["Decisione_Stato"]) == ("Radar", "Entrato", "Radar")
                   and "nel radar per eccezione: decisione del validatore" in r2["NFR-14"]["Motivo_Stato"]
                   and (r2["NFR-12"]["Stato"], r2["NFR-12"]["Movimento"], r2["NFR-12"]["Decisione_Stato"])
                   == ("Osservazione", "Uscito", "Osservazione")
                   and "NFR-14" in anag and anag["NFR-14"]["Owner"] == "Funzione ICT & Security Risk" and "NFR-12" not in anag
                   and kri_12 and all(k["In_Vigore"] == "No" for k in kri_12) and len(s2["anagrafica"]) == 12
                   and s2["copertura_foglio"] == (12, 12),
                   "13. decisione sullo stato (D-79): NFR-14, in osservazione dal 2026Q1, entra nel radar per decisione del validatore (anagrafica con "
                   "l'owner della sua riga), NFR-12 esce subito (niente 'in uscita' per decisione): KRI fuori vigore, "
                   "anagrafica senza buchi",
                   str({i: (r2[i]["Stato"], r2[i]["Movimento"], r2[i]["Motivo_Stato"]) for i in ("NFR-12", "NFR-14")})
                   + " " + str(sorted(anag)) + " " + str([(k["KRI_ID"], k["In_Vigore"]) for k in kri_12]))
        kri = next(k for k in s2["kri"] if k["Ciclo"] == ciclo and k["KRI_ID"] == "NFR-01-K1")
        azione = next(a for a in carica_tabella(b, "tblAzioni") if a["ID_Azione"] == "2026Q2-NFR-04-A1")
        e.verifica(kri["In_Vigore"] == "No" and azione["Owner"] == "Funzione Continuita' Operativa"
                   and azione["Stato"] == "Approvata",
                   "13. Respingi toglie il KRI; l'azione rettificata resta Approvata",
                   f"KRI {kri['In_Vigore']}, azione {azione['Owner']} {azione['Stato']}")
        nuove = s2["validazione"][n_storico:]
        conta = {d: sum(1 for r in nuove if r["Decisione"] == d) for d in
                 ("Invariato (riapertura)", "Rettificato (riapertura)", "Respinto (riapertura)")}
        e.verifica(len(nuove) > 0 and sum(conta.values()) == len(nuove) and conta["Rettificato (riapertura)"] == 5
                   and conta["Respinto (riapertura)"] == 3 and all(r["Stato"] == "Applicata" for r in nuove),
                   "13. storico: decisioni con il suffisso (riapertura), distinte dalle proposte degli agenti", str(conta))
        e.verifica(not s2["griglia"], "13. dopo valida la griglia e' vuota", str(list(s2["griglia"])[:5]))
        chiuse = list(traccia.parent.glob(f"Riapertura_{ciclo}_*.json"))
        e.verifica(not traccia.exists() and len(chiuse) == 1 and carica(chiuse[0])["validata_da"] == validatore
                   and (traccia.parent / f"Report_comitato_{ciclo}.pdf").exists(),
                   "13. valida chiude la traccia della riapertura (con chi ha validato) e rigenera il report", out[-600:])
        verifica_integrita(e, s2, "13. dopo la validazione riaperta")
        verifica_report(e, s2, "13. dopo la validazione riaperta")

        # Seconda riapertura, solo NFR-02, chiusa senza cambiare niente.
        codice, out = b.esegui("riapri", "--rischi", "NFR-02")
        s3 = b.leggi()
        e.verifica(codice == 0 and per_oggetto(s3)["Rischio"] == 1
                   and per_oggetto(s3)["KRI"] == sum(1 for k in s2["kri"] if k["Ciclo"] == ciclo and k["ID_Rischio"] == "NFR-02"
                                                     and k["In_Vigore"] == "Sì"),
                   "13. riapri --rischi NFR-02: solo il rischio, i suoi KRI e le sue azioni", f"{out}\n{per_oggetto(s3)}")
        codice, out = b.esegui("valida", "--periodo", ciclo, "--validatore", validatore, "--senza-report")
        s4 = b.leggi()
        e.verifica(codice == 0 and "Report al comitato" not in out
                   and len(list(traccia.parent.glob(f"Report_comitato_{ciclo}_*.pdf"))) == 0,
                   "13. valida --senza-report: il report non si rigenera", out[-400:])
        e.verifica(codice == 0 and rr(s4) == rr(s2) and all(r["Decisione"] == "Invariato (riapertura)"
                                                             for r in s4["validazione"][len(s2["validazione"]):]),
                   "13. riaprire e validare senza toccare niente: il registro resta com'era", out)


def piu_analisti(e):
    """Passo 15 (D-83): piu' analisti sullo stesso registro. Il lucchetto di un collega ferma i comandi che scrivono
    (niente scritto); uno scaduto si prende; sblocca lo toglie e lo registra. Un registro aperto in un programma di
    questo PC ferma prima di scrivere. La scrittura avviene su una copia di lavoro: niente file lasciati accanto al
    registro, nessuna copia rimasta nella cartella di lavoro. In piu' (F1): allegati di A3 e A4 dalla baseline, prompt
    archiviati con il ciclo, PDF delle schede."""
    import datetime as dt_
    import win32con
    import win32file
    with tempfile.TemporaryDirectory() as tmp:
        b = Banco(tmp)
        cartella_lucchetto = b.uscita / "_Lucchetto"
        cartella_lucchetto.mkdir(parents=True)
        adesso = dt_.datetime.now().replace(microsecond=0)
        collega = {"id": "x", "utente": "Collega", "pc": "ALTRO-PC", "comando": "valida", "inizio": adesso.isoformat(),
                   "scadenza": (adesso + dt_.timedelta(hours=1)).isoformat()}
        (cartella_lucchetto / "registro.json").write_text(json.dumps(collega), encoding="utf-8")
        prima = sha(b.wb)
        codice, out = b.esegui("griglia")
        e.verifica(codice == 1 and "in uso" in out and "Collega" in out and sha(b.wb) == prima,
                   "15. lucchetto di un collega: il comando che scrive si ferma, niente scritto", out)
        codice, out = b.esegui("diagnosi")
        e.verifica("in uso" not in out, "15. un comando che non scrive (diagnosi) non guarda il lucchetto", out[-300:])
        codice, out = b.esegui("sblocca", "--motivo", "PC del collega spento a meta' validazione")
        log = (cartella_lucchetto / "sblocchi.log").read_text(encoding="utf-8")
        e.verifica(codice == 0 and not (cartella_lucchetto / "registro.json").exists() and "Collega" in log and "spento" in log,
                   "15. sblocca toglie il lucchetto e registra chi, perche' e di chi era", out + log)
        scaduto = dict(collega, scadenza=(adesso - dt_.timedelta(minutes=1)).isoformat())
        (cartella_lucchetto / "registro.json").write_text(json.dumps(scaduto), encoding="utf-8")
        lavoro = Path(tmp) / "lavoro"
        codice, out = b.esegui_conf({"cartella_lavoro": str(lavoro)}, "griglia")
        accanto = sorted(f.name for f in b.wb.parent.iterdir() if f.name.startswith("~$"))
        e.verifica(codice == 0 and sha(b.wb) != prima and not (cartella_lucchetto / "registro.json").exists()
                   and not accanto and lavoro.exists() and not any(lavoro.iterdir()),
                   "15. lucchetto scaduto: il comando lo prende, scrive dalla copia di lavoro, lo lascia; nessun file "
                   "temporaneo accanto al registro, nessuna copia rimasta", f"{out}\n{accanto}")
        handle = win32file.CreateFile(str(b.wb), win32con.GENERIC_READ, 0, None, win32con.OPEN_EXISTING, 0, None)
        try:
            codice, out = b.esegui("griglia")
        finally:
            handle.Close()
        e.verifica(codice == 1 and "aperto in un programma di questo PC" in out,
                   "15. registro aperto in un programma di questo PC: fermo prima di scrivere", out)
        codice, out = b.esegui("baseline")
        base = carica(b.uscita / "Baseline_corrente.json")
        import input_a1
        a3, a4 = (b.uscita / "Input_A3.txt").read_text(encoding="utf-8"), (b.uscita / "Input_A4.txt").read_text(encoding="utf-8")
        e.verifica(codice == 0 and input_a1.leggi_baseline(a3) == base and input_a1.leggi_baseline(a4) == base
                   and a3.startswith("INPUT DI A3") and a4.startswith("INPUT DI A4") and "Input_A3.txt" in out,
                   "15. baseline scrive gli allegati di A3 e A4 (AU7) con la stessa baseline del .json", out)
        codice, out = b.esegui("trimestrale", "--payload", DATI / "run1_A1_2026Q3.json", "--challenger", DATI / "run_A5_2026Q3.json")
        prompt = b.uscita / "Cicli" / "2026Q3" / "Prompt_in_uso"
        e.verifica(codice == 0 and sorted(f.name for f in prompt.glob("A*.md")) == sorted(f.name for f in (CAMPO.parent / "02_Agenti").glob("A*.md")),
                   "15. trimestrale archivia i prompt degli agenti del pacchetto con il ciclo (AU1)", out[-500:])


def registro_unico(e):
    """Passo 14 (D-79): la regola del radar sul registro vero. 2026Q3: NFR-08 scende sotto la soglia (Radar, in uscita);
    il validatore mette NFR-12 in osservazione e NFR-16 nel radar (lo stato si ricalcola con valida). 2026Q4 con la
    capienza a 10: NFR-08 esce al secondo ciclo, il piu' basso per score fuori per capienza resta un ciclo in uscita,
    NFR-12 resta fuori per decisione. Poi la dismissione di un rischio in osservazione."""
    run1 = carica(DATI / "run1_A1_2026Q3.json")
    with tempfile.TemporaryDirectory() as tmp:
        b = Banco(tmp)
        n08 = next(x for x in run1["rischi"] if x["id_rischio"] == "NFR-08")
        n08["probabilita"] = 1
        n08["variazioni"] = [{"dimensione": "probabilita", "data_evidenza": "2026-09-15",
                              "evidenza": "Il SOC documenta la revisione completa delle utenze: nessun accesso senza pratica "
                                          "nel trimestre, il fenomeno resta solo teorico per la Banca."}]
        codice, out = b.esegui("trimestrale", "--payload", b.scrivi_json("q3.json", run1))
        s = b.leggi()
        q3 = {r["ID_Rischio"]: r for r in s["register"] if r["Ciclo"] == "2026Q3"}
        e.verifica(codice == 0 and q3["NFR-08"]["Stato"] == "Radar, in uscita"
                   and q3["NFR-08"]["Motivo_Stato"] == ("Probabilita 1 sotto la soglia 2 (primo ciclo: esce se lo e' anche "
                                                         "al ciclo dopo)")
                   and "NFR-08" in {a["ID"] for a in s["anagrafica"]}
                   and {k["KRI_ID"] for k in s["kri"] if k["Ciclo"] == "2026Q3" and k["ID_Rischio"] == "NFR-08"
                        and k["In_Vigore"] == "Sì"} and "(in uscita: NFR-08)" in out,
                   "14. NFR-08 scende sotto la soglia di Probabilita: Radar, in uscita (resta nel radar con KRI e azioni "
                   "per un ciclo)", out[-700:] + str(q3["NFR-08"].get("Motivo_Stato")))
        e.verifica(s["griglia_stati"].get("NFR-08", "").startswith("Radar, in uscita: Probabilita 1"),
                   "14. griglia: la colonna Stato dice al validatore che NFR-08 e' in uscita e perche'", str(s["griglia_stati"]))
        scrivi_decisioni(b.wb, "2026Q3", [
            {"oggetto": "Rischio", "id": "NFR-12", "campo": "Decisione_Stato", "decisione": "Rettificato", "valore": "Osservazione"},
            {"oggetto": "Rischio", "id": "NFR-16", "campo": "Decisione_Stato", "decisione": "Rettificato", "valore": "Radar",
             "motivazione": "Il comitato vuole seguire da subito le vertenze con KRI e azioni."}])
        prima = sha(b.wb)
        codice, out = b.esegui("valida", "--periodo", "2026Q3", "--validatore", "Comitato Rischi")
        e.verifica(codice == 1 and "NFR-12" in out and "Motivazione" in out and sha(b.wb) == prima,
                   "14. una decisione sullo stato senza Motivazione ferma valida, niente applicato", out)
        scrivi_decisioni(b.wb, "2026Q3", [
            {"oggetto": "Rischio", "id": "NFR-12", "campo": "Decisione_Stato", "decisione": "Rettificato", "valore": "osservazione",
             "motivazione": "Adeguamento ai bonifici istantanei concluso: basta osservarlo."}])
        codice, out = b.esegui("valida", "--periodo", "2026Q3", "--validatore", "Comitato Rischi")
        s = b.leggi()
        q3 = {r["ID_Rischio"]: r for r in s["register"] if r["Ciclo"] == "2026Q3"}
        anag = {a["ID"]: a for a in s["anagrafica"]}
        kri12 = [k for k in s["kri"] if k["Ciclo"] == "2026Q3" and k["ID_Rischio"] == "NFR-12"]
        e.verifica(codice == 0
                   and (q3["NFR-12"]["Stato"], q3["NFR-12"]["Movimento"], q3["NFR-12"]["Decisione_Stato"])
                   == ("Osservazione", "Uscito", "Osservazione")
                   and q3["NFR-12"]["Motivo_Stato"] == "in osservazione per decisione del validatore"
                   and (q3["NFR-16"]["Stato"], q3["NFR-16"]["Movimento"], q3["NFR-16"]["Decisione_Stato"]) == ("Radar", None, "Radar")
                   and "entrato in validazione: KRI e azioni da definire al ciclo dopo" in q3["NFR-16"]["Motivo_Stato"]
                   and "NFR-12" not in anag and anag.get("NFR-16", {}).get("Owner") == "Da assegnare"
                   and kri12 and all(k["In_Vigore"] == "No" for k in kri12) and s["copertura_foglio"] == (12, 12)
                   and "NFR-16" in out and "NFR-12" in out,
                   "14. valida applica le decisioni sullo stato: NFR-12 esce subito (KRI fuori vigore, anagrafica senza buchi), "
                   "NFR-16, nuovo, va nel radar senza 'Entrato' (non era in osservazione prima: e' Nuovo; anagrafica, KRI e "
                   "azioni al ciclo dopo); copertura 12/12",
                   out[-800:] + str({i: (q3[i]["Stato"], q3[i]["Movimento"], q3[i]["Motivo_Stato"]) for i in ("NFR-12", "NFR-16")}))
        verifica_integrita(e, s, "14. dopo la validazione del 2026Q3")
        base = carica(b.uscita / "Baseline_corrente.json")
        e.verifica("NFR-16" in {x["id_rischio"] for x in base["rischi"]}
                   and next(x for x in base["rischi_in_osservazione"] if x["id_rischio"] == "NFR-12")["decisione_stato"] == "Osservazione"
                   and next(x for x in base["rischi"] if x["id_rischio"] == "NFR-08")["stato"] == "Radar, in uscita",
                   "14. baseline del 2026Q4: NFR-16 nel radar, NFR-12 in osservazione con la decisione, NFR-08 in uscita")

        # 2026Q4 con la capienza a 10 (cella gialla di Parametri).
        with SessioneExcel(b.wb) as sx:
            sx.intervallo_nome("capienzaRadar").Value = 10
            sx.salva()
        run3 = carica(DATI / "run3_A1_2026Q4.json")
        run3["rischi"] = [x for x in run3["rischi"] if x["id_rischio"] != "NFR-12"]
        # I KRI di NFR-12 sono usciti di vigore con la decisione del validatore: non si rileggono.
        run3["ricalcolo_kri_ciclo_precedente"] = [z for z in run3["ricalcolo_kri_ciclo_precedente"]
                                                  if not z["kri_id"].startswith("NFR-12-")]
        n08 = next(x for x in run3["rischi"] if x["id_rischio"] == "NFR-08")
        n08["probabilita"] = 1
        # run3 parte dalla Velocity di NFR-10 rettificata a 3 nella catena principale; qui il 2026Q3 non l'ha cambiata.
        next(x for x in run3["rischi"] if x["id_rischio"] == "NFR-10")["velocity"] = None
        n08["variazioni"] = [v for v in n08["variazioni"] if v["dimensione"] != "probabilita"]
        codice, out = b.esegui("trimestrale", "--payload", b.scrivi_json("q4.json", run3))
        s = b.leggi()
        q4 = {r["ID_Rischio"]: r for r in s["register"] if r["Ciclo"] == "2026Q4"}
        capienza = [i for i, r in q4.items() if str(r["Motivo_Stato"]).startswith("fuori per capienza")]
        nel = [i for i, r in q4.items() if r["Stato"] in ("Radar", "Radar, in uscita")]
        kri08 = [k for k in s["kri"] if k["Ciclo"] == "2026Q4" and k["ID_Rischio"] == "NFR-08"]
        e.verifica(codice == 0 and (q4["NFR-08"]["Stato"], q4["NFR-08"]["Movimento"]) == ("Osservazione", "Uscito")
                   and kri08 and all(k["In_Vigore"] == "No" for k in kri08) and "NFR-08" not in {a["ID"] for a in s["anagrafica"]}
                   and len(capienza) == 1 and q4[capienza[0]]["Stato"] == "Radar, in uscita"
                   and len(nel) == 11 and len(s["anagrafica"]) == 11 and s["copertura_foglio"] == (11, 11)
                   and (q4["NFR-12"]["Stato"], q4["NFR-12"]["Decisione_Stato"], q4["NFR-12"]["Validazione"])
                   == ("Osservazione", "Osservazione", "Rettificato")
                   and f"(in uscita: {capienza[0] if capienza else '?'})" in out and "usciti NFR-08" in out,
                   "14. 2026Q4 con capienza 10: NFR-08 esce al secondo ciclo sotto la soglia (KRI fuori vigore, fuori "
                   "dall'anagrafica); il piu' basso per score resta un ciclo 'in uscita' per capienza; 11 nel radar (10 + 1 in "
                   "uscita); NFR-12 riportato in osservazione con la decisione del validatore",
                   out[-800:] + str({i: (r["Stato"], r["Movimento"], r["Motivo_Stato"]) for i, r in q4.items()}))
        verifica_integrita(e, s, "14. 2026Q4 con la capienza a 10")
        verifica_report(e, s, "14. report 2026Q4 con il radar ridotto", commento=run3["sintesi"])

        # Dismissione di un rischio in osservazione: la riga del ciclo dice Dismesso, il ciclo dopo non lo riporta.
        codice, out = b.esegui("valida", "--periodo", "2026Q4", "--validatore", "Comitato Rischi")
        codice, out = b.esegui("dismetti", "--rischio", "NFR-15", "--motivazione",
                               "Pagamenti delegati ad agenti di IA esclusi dall'offerta della Banca.", "--decisore", "Comitato Rischi")
        s = b.leggi()
        r15 = next(r for r in s["register"] if r["Ciclo"] == "2026Q4" and r["ID_Rischio"] == "NFR-15")
        base = carica(b.uscita / "Baseline_corrente.json")
        e.verifica(codice == 0 and r15["Stato"] == "Dismesso" and "Comitato Rischi" in str(r15["Motivo_Stato"])
                   and "NFR-15" not in {x["id_rischio"] for x in base["rischi_in_osservazione"]}
                   and "NFR-15" not in [f[0] for f in s["fenomeni"]],
                   "14. dismetti su un rischio in osservazione: riga Dismesso con il motivo, fuori dalla baseline e dalla pagina "
                   "Fenomeni", out + str(r15.get("Stato")))


def aggiornamento_08b(e):
    """Passo 11c (D-79): un registro del template 2026-10-08b (lista di osservazione D-73, dati/registro_template_
    2026-10-08b.xlsx = il template di esempio di allora) si aggiorna al registro unico: le voci in osservazione
    diventano rischi in osservazione con un codice NFR-nn libero, le righe del registro restano nel radar."""
    vecchio = DATI / "registro_template_2026-10-08b.xlsx"
    with SessioneExcel(vecchio, sola_lettura=True) as sess:
        righe_prima = {n: sess.tabella(n).ListRows.Count for n in ("tblRegister", "tblKRI", "tblNews", "tblValidazione")}
        voci = [r for r in campo.Scrittore(sess, MAPPA).righe("tblOsservazione") if r["Ciclo"] == "2026Q2"
                and r["Stato"] == "In osservazione"]
    with tempfile.TemporaryDirectory() as tmp:
        b = Banco(tmp, vecchio)
        codice, out = b.esegui("baseline", "--uscita", b.cartella / "x.json")
        e.verifica(codice == 1 and "aggiorna-registro" in out, "11c. registro del template 2026-10-08b: fermo, va aggiornato", out)
        codice, out = b.esegui("aggiorna-registro")
        s = b.leggi()
        q2 = {r["ID_Rischio"]: r for r in s["register"] if r["Ciclo"] == "2026Q2"}
        nuovi = {i: r for i, r in q2.items() if r["Stato"] == "Osservazione"}
        e.verifica(codice == 0 and s["versione"] == campo.VERSIONE_TEMPLATE and not s["errori"]
                   and len(s["register"]) == righe_prima["tblRegister"] + len(voci) and len(voci) == 3
                   and sorted(nuovi) == ["NFR-13", "NFR-14", "NFR-15"]
                   and all(r["Validazione"] == "Accettato" and r["Approvato_Da"] == "Conversione D-79" for r in nuovi.values())
                   and all(r["Stato"] == "Radar" for i, r in q2.items() if i not in nuovi)
                   and "OSS-01 -> NFR-13" in out and len(s["anagrafica"]) == 12 and s["copertura_foglio"] == (12, 12),
                   "11c. aggiorna-registro: le 3 voci in osservazione diventano NFR-13, 14, 15 in osservazione (accettate, "
                   "'Conversione D-79'); le righe del registro restano nel radar; anagrafica e copertura invariate",
                   out + str({i: (r["Stato"], r["Impatto"], r["Probabilita"], r["Prossimita"]) for i, r in nuovi.items()}))
        oss1 = next((v for v in voci if v["OSS_ID"] == "OSS-01"), {})
        n13 = nuovi.get("NFR-13", {})
        e.verifica((n13.get("Impatto"), n13.get("Probabilita"), n13.get("Prossimita"), n13.get("Orizzonte_Anni"))
                   == (oss1.get("Impatto_Potenziale"), 1, 1, oss1.get("Orizzonte_Anni"))
                   and n13.get("Segnale_Avvicinamento") == oss1.get("Segnale_Avvicinamento")
                   and [f[0] for f in s["fenomeni"]] and set(f[0] for f in s["fenomeni"]) == set(nuovi),
                   "11c. valori convertiti in via provvisoria (Impatto = impatto potenziale, Probabilita dalla plausibilita' "
                   "teorica = 1, Prossimita dall'orizzonte oltre 3 anni = 1), orizzonte e segnale conservati; pagina Fenomeni",
                   f"{n13} {oss1}")
        codice, out = b.esegui("baseline", "--uscita", b.cartella / "base.json")
        base = carica(b.cartella / "base.json")
        e.verifica(codice == 0 and sorted(x["id_rischio"] for x in base["rischi_in_osservazione"]) == ["NFR-13", "NFR-14", "NFR-15"]
                   and len(base["rischi"]) == 12,
                   "11c. la baseline del registro aggiornato porta ad A1 i 12 rischi del radar e i 3 in osservazione", out)


def parametri_ciclo(banco):
    """Ciclo corrente, precedente, due trimestri prima, periodi del trend, etichetta e proposta del foglio Notizie."""
    with SessioneExcel(banco.wb, sola_lettura=True) as s:
        s.ricalcola()
        v = lambda n: campo.da_excel(s.intervallo_nome(n).Value)
        return {"ciclo": v("cicloCorrente"), "prec": v("cicloPrecedente"), "meno2": v("cicloMeno2"),
                "trend": [campo.da_excel(c.Value) for c in s.intervallo_nome("cicliTrend").Cells],
                "data": campo.da_excel(s.intervallo_nome("dataRiferimento").Value), "etichetta": v("etichettaCiclo"),
                "proposta": s.foglio("Notizie").Range("L22").Value}


def straordinario(e, b):
    """Ciclo straordinario (D-75): A3 lo propone, la funzione di rischio lo decide, A1 rivaluta solo NFR-01."""
    # 7b. Proposta di A3 in una settimana
    proposta = {"settimana": "2026-11-16", "notizie": [], "flag_proposti": [],
                "sintesi": "Settimana senza notizie nuove; resta la proposta di ciclo straordinario su NFR-01.",
                "proposta_straordinario": {"rischi": ["NFR-01"], "motivo": "Kit di clonazione vocale in vendita e casi presso "
                                                                              "banche comparabili: intensita' 3 su NFR-01, Impatto 4."}}
    codice, out = b.esegui("settimanale", "--payload", b.scrivi_json("a3_proposta.json", proposta))
    par = parametri_ciclo(b)
    e.verifica(codice == 0 and "PROPOSTA DI CICLO STRAORDINARIO di A3 per NFR-01" in out
               and str(par["proposta"]).startswith("PROPOSTA DI CICLO STRAORDINARIO per NFR-01"),
               "7b. A3 propone un ciclo straordinario (D-75): a video e nel riquadro del foglio Notizie", out + str(par["proposta"]))
    # 8s. Decisione: prima il 2026Q4 va validato
    codice, out = b.esegui("baseline", "--straordinario", "--rischi", "NFR-01", "--motivo",
                           "Primo caso di frode con voce clonata presso un cliente corporate della Banca.",
                           "--decisore", "Comitato Rischi", "--data", "2027-01-20")
    e.verifica(codice == 1 and "righe da validare" in out, "8s. lo straordinario parte solo da un ciclo validato", out)
    codice, out = b.esegui("valida", "--periodo", "2026Q4", "--validatore", "Comitato Rischi")
    e.verifica(codice == 0, "8s. validazione del 2026Q4 (tutto accettato)", out)
    prima = b.leggi()
    codice, out = b.esegui("baseline", "--straordinario", "--rischi", "NFR-01,NFR-99", "--motivo", "Motivo abbastanza lungo per "
                           "la prova.", "--decisore", "Comitato Rischi", "--data", "2027-01-20")
    e.verifica(codice == 1 and "NFR-99" in out, "8s. rischio da rivalutare che non e' in anagrafica: fermo", out)
    codice, out = b.esegui("baseline", "--straordinario", "--rischi", "NFR-01", "--motivo",
                           "Primo caso di frode con voce clonata presso un cliente corporate della Banca.",
                           "--decisore", "Comitato Rischi", "--data", "2027-01-20")
    base = carica(b.uscita / "Baseline_corrente.json")
    decisione = b.uscita / "Cicli" / "2026Q4-S1" / "Straordinario_2026Q4-S1.json"
    allegato = b.uscita / "Input_A1_2026Q4-S1.txt"
    e.verifica(codice == 0 and decisione.exists() and base["ciclo_da_valutare"] == "2026Q4-S1"
               and base["data_riferimento"] == "2027-01-20" and base["straordinario"]["rischi_da_rivalutare"] == ["NFR-01"]
               and allegato.exists() and "CICLO STRAORDINARIO 2026Q4-S1" in allegato.read_text(encoding="utf-8"),
               "8s. baseline --straordinario: periodo 2026Q4-S1, decisione archiviata, baseline e allegato di A1 con i rischi "
               "da rivalutare", out)
    run4 = carica(DATI / "run4_A1_2026Q4-S1.json")
    estraneo = json.loads(json.dumps(run4))
    estraneo["rischi"].append(json.loads(json.dumps(next(x for x in carica(DATI / "run3_A1_2026Q4.json")["rischi"]
                                                        if x["id_rischio"] == "NFR-02"))))
    firma = sha(b.wb)
    codice, out = b.esegui("trimestrale", "--payload", b.scrivi_json("s1_estraneo.json", estraneo))
    e.verifica(codice == 1 and "non indicato per il ciclo straordinario" in out and sha(b.wb) == firma,
               "8s. A1 riscrive un rischio non indicato (NFR-02): fermo C1, registro intatto", out)
    codice, out = b.esegui("trimestrale", "--payload", DATI / "run4_A1_2026Q4-S1.json")
    s = b.leggi()
    par = parametri_ciclo(b)
    s1 = {r["ID_Rischio"]: r for r in s["register"] if r["Ciclo"] == "2026Q4-S1"}
    q4 = {r["ID_Rischio"]: r for r in s["register"] if r["Ciclo"] == "2026Q4"}
    e.verifica(codice == 0 and "CICLO STRAORDINARIO 2026Q4-S1" in out and len(s1) == 16 and s["copertura_foglio"] == (13, 13)
               and s1["NFR-01"]["Probabilita"] == 5 and s1["NFR-01"]["Esito"] == "Variato"
               and s1["NFR-01"]["Validazione"] == "Da validare" and s1["NFR-01"]["Periodo_Valutazione"] == "2026Q4-S1"
               and all(s1[i]["Validazione"] == q4[i]["Validazione"] and s1[i]["Periodo_Valutazione"] == q4[i]["Periodo_Valutazione"]
                       and s1[i]["Impatto"] == q4[i]["Impatto"] and s1[i]["Stato"] == q4[i]["Stato"] for i in s1 if i != "NFR-01"),
               "8s. ciclo straordinario scritto: NFR-01 rivalutato (Probabilita da 4 a 5), gli altri 12 rischi del radar e i 3 "
               "in osservazione riportati dal 2026Q4, validati come allora, con il loro periodo di valutazione e lo stesso "
               "stato", out + str({i: (r["Validazione"], r.get(
                   "Periodo_Valutazione")) for i, r in s1.items()}))
    righe_s1 = [r for r in s["validazione"] if r["Periodo"] == "2026Q4-S1"]
    e.verifica({r["Oggetto"] for r in righe_s1} == {"Rischio", "KRI", "Azione"}
               and {r["ID"] for r in righe_s1 if r["Oggetto"] == "Rischio"} == {"NFR-01"}
               and all(str(r["ID"]).startswith(("NFR-01", "2026Q4-S1-NFR-01")) for r in righe_s1),
               "8s. in validazione solo il rischio rivalutato, i suoi KRI e la sua azione nuova",
               str(sorted({(r["Oggetto"], r["ID"]) for r in righe_s1})))
    e.verifica(par["ciclo"] == "2026Q4-S1" and par["prec"] == "2026Q4" and par["meno2"] == "2026Q2"
               and par["trend"][-2:] == ["2026Q4", "2026Q4-S1"] and par["data"] == "2027-01-20"
               and str(par["etichetta"]).startswith("Ciclo straordinario 2026Q4-S1 · dati al 20/01/2027"),
               "8s. periodi delle viste scritti dallo script: precedente 2026Q4, trend con lo straordinario, etichetta "
               "'Ciclo straordinario' con la sua data", str(par))
    margini_prima = {m[0]: round(m[2], 6) for m in prima["mosca"]}
    margini = {m[0]: round(m[2], 6) for m in s["mosca"]}
    e.verifica(all(margini[i] == margini_prima[i] for i in margini if i != "NFR-01"),
               "8s. Radar_Mosca: per i rischi non rivalutati la Y viene dalle azioni del 2026Q4 (margini invariati)",
               f"prima {margini_prima}\ndopo {margini}")
    sint = next(r for r in s["sintesi_cicli"] if r["Ciclo"] == "2026Q4-S1")
    e.verifica(str(sint.get("Straordinario", "")).startswith("Deciso da Comitato Rischi") and "NFR-01" in sint["Straordinario"],
               "8s. Sintesi_Cicli: chi ha deciso lo straordinario, perche' e quali rischi", str(sint.get("Straordinario")))
    # Validazione dello straordinario: la regola del punto si misura sul 2026Q4 (lo straordinario conta come ciclo)
    scrivi_decisioni(b.wb, "2026Q4-S1", [{"oggetto": "Rischio", "id": "NFR-01", "campo": "Impatto", "decisione": "Rettificato",
                                          "valore": 2, "motivazione": "Prova: due punti sotto il 2026Q4 non si accettano."}])
    codice, out = b.esegui("valida", "--periodo", "2026Q4-S1", "--validatore", "Comitato Rischi")
    e.verifica(codice == 1 and "piu' di un punto" in out and "(4)" in out,
               "8s. validazione dello straordinario: la regola del punto si misura sul periodo prima (2026Q4)", out)
    azzera_griglia(b.wb)
    codice, out = b.esegui("valida", "--periodo", "2026Q4-S1", "--validatore", "Comitato Rischi")
    base = carica(b.uscita / "Baseline_corrente.json")
    e.verifica(codice == 0 and base["ciclo_precedente"] == "2026Q4-S1" and base["ciclo_da_valutare"] == "2027Q1"
               and base["data_riferimento"] == "2027-03-31" and "straordinario" not in base
               and next(r for r in base["rischi"] if r["id_rischio"] == "NFR-01")["probabilita"] == 5,
               "8s. dopo la validazione dello straordinario il ciclo dopo e' il 2027Q1 e parte dai suoi valori", out)
    codice, out = b.esegui("baseline", "--straordinario", "--rischi", "NFR-02", "--motivo",
                           "Secondo evento critico dello stesso trimestre, per la prova.", "--decisore", "Comitato Rischi",
                           "--data", "2027-02-10")
    e.verifica(codice == 0 and carica(b.uscita / "Baseline_corrente.json")["ciclo_da_valutare"] == "2026Q4-S2",
               "8s. un secondo straordinario nello stesso trimestre e' il 2026Q4-S2", out)
    censimento_a8(e, b)


def censimento_a8(e, b):
    """8a. A8 Evento critico (D-77): straordinario di solo censimento (nessun --rischi), un rischio nuovo creato
    dall'evento, l'analisi dell'evento in Sintesi_Cicli e nella knowledge di A7."""
    codice, out = b.esegui("baseline", "--straordinario", "--motivo",
                           "Attacco a un fornitore di servizi di firma digitale usato da molte banche italiane.",
                           "--decisore", "Comitato Rischi", "--data", "2027-02-10")
    base = carica(b.uscita / "Baseline_corrente.json")
    allegato = (b.uscita / "Input_A1_2026Q4-S2.txt").read_text(encoding="utf-8")
    e.verifica(codice == 0 and base["straordinario"]["rischi_da_rivalutare"] == [] and "solo censimento" in out
               and "censisci SOLO i rischi nuovi" in allegato and "A8 Evento critico" in out,
               "8a. baseline --straordinario senza --rischi: censimento, allegato che lo dice in testa, prossimo passo A8", out)
    nuovo = json.loads(json.dumps(next(x for x in carica(DATI / "run3_A1_2026Q4.json")["rischi"] if x["id_rischio"] == "NFR-16")))
    nuovo.update(id_rischio="NFR-17", nome="Indisponibilita' del servizio di firma digitale di un fornitore unico",
                 event_type="9.9", driver=["DRV-TPR", "DRV-CYB"], variazioni=[],
                 fonti=[{"riferimento": "Comunicato del fornitore di firma digitale sull'attacco del 05/02/2027",
                         "data": "2027-02-05", "tipo": "Esterna", "rilevanza": 3}])
    for k in nuovo["kri_proposti"]:
        k["kri_id"] = None
    a8 = {"ciclo": "2026Q4-S2", "data_riferimento": "2027-02-10",
          "sintesi": "MESSAGGIO: l'attacco del 05/02/2027 al fornitore di firma digitale usato dalla Banca mostra un "
                     "meccanismo di perdita non coperto: censito NFR-17. DECISIONI: approvare il piano di uscita.",
          "analisi_evento": {
              "evento": "Il 05/02/2027 un attacco ha reso indisponibile per tre giorni il servizio di firma digitale di un "
                        "fornitore usato da molte banche italiane, Banca compresa (comunicato del fornitore).",
              "catena_causale": "Fornitore unico senza alternativa (causa), indisponibilita' del servizio (evento), contratti "
                                "e mutui non firmabili per giorni (danno per la Banca).",
              "rischi_toccati": [{"id_rischio": "NFR-17", "effetto": "Rischio nuovo: nessun rischio del registro copre il fornitore."}],
              "rischi_non_toccati": "NFR-02: riguarda il fornitore cloud, non questo servizio.",
              "documenti": [{"riferimento": "Comunicato del fornitore di firma digitale sull'attacco del 05/02/2027",
                             "data": "2027-02-05", "uso": "il fatto e la durata dell'indisponibilita'"}],
              "limiti": "Non si conosce ancora la causa tecnica dell'attacco."},
          "rischi": [nuovo], "ricalcolo_kri_ciclo_precedente": []}
    payload = b.scrivi_json("A8_2026Q4-S2.json", a8)
    codice, out = b.esegui("precontrollo", "--payload", payload)
    e.verifica("Messaggio per A1" not in out and "Precontrollo" in out,
               "8a. precontrollo dell'output di A8: nessun punto indirizzato ad A1", out)
    codice, out = b.esegui("trimestrale", "--payload", payload)
    s = b.leggi()
    s2 = {r["ID_Rischio"]: r for r in s["register"] if r["Ciclo"] == "2026Q4-S2"}
    e.verifica(codice == 0 and len(s2) == 17 and s2["NFR-17"]["Esito"] == "Nuovo" and s2["NFR-17"]["Validazione"] == "Da validare"
               and s2["NFR-17"]["Stato"] == "Radar" and s2["NFR-17"]["Movimento"] is None
               and all(r["Validazione"] != "Da validare" for i, r in s2.items() if i != "NFR-17"),
               "8a. censimento scritto: NFR-17 nuovo nel radar (sopra le soglie), da validare; i 16 rischi riportati gia' "
               "validati", out)
    righe = {(r["Oggetto"], r["ID"]) for r in s["validazione"] if r["Periodo"] == "2026Q4-S2" and r["Oggetto"] == "Rischio"}
    sint = next(r for r in s["sintesi_cicli"] if r["Ciclo"] == "2026Q4-S2")
    e.verifica(righe == {("Rischio", "NFR-17")} and "nuovi: NFR-17" in str(sint.get("Straordinario"))
               and "Evento (analisi di A8)" in str(sint.get("Straordinario")),
               "8a. in validazione solo il rischio nuovo; Sintesi_Cicli con il rischio nuovo e l'evento",
               f"{righe}\n{sint.get('Straordinario')}")
    ciclo_txt = (b.uscita / "Spiegazioni" / "Ciclo.txt").read_text(encoding="utf-8")
    e.verifica("ANALISI DELL'EVENTO DI A8" in ciclo_txt and "Fornitore unico senza alternativa" in ciclo_txt,
               "8a. knowledge di A7: Ciclo.txt con l'analisi dell'evento", ciclo_txt[:1500])


def catena(e):
    run1 = carica(DATI / "run1_A1_2026Q3.json")
    with tempfile.TemporaryDirectory() as tmp:
        b = Banco(tmp)

        # 0. Baseline di partenza
        codice, out = b.esegui("baseline", "--uscita", b.cartella / "base_q3.json")
        e.verifica(codice == 0 and uguale_ai_dati("baseline_2026Q3.json", b.cartella / "base_q3.json"),
                   "0. la baseline estratta dal template e' quella usata per run1", out)
        base_q3 = carica(b.cartella / "base_q3.json")
        e.verifica([x["id_rischio"] for x in base_q3["rischi_in_osservazione"]] == ["NFR-13", "NFR-14", "NFR-15"]
                   and base_q3["regola_radar"]["capienza"] == 15 and len(base_q3["rischi"]) == 12
                   and all(x["stato"] == "Radar" for x in base_q3["rischi"]),
                   "0. registro unico (D-79): la baseline ha i 12 rischi del radar, i 3 in osservazione e la regola di Parametri",
                   str(base_q3.get("regola_radar")))

        # 1. Payload difettosi: fermo e zero byte scritti
        prima = sha(b.wb)
        difettoso = json.loads(json.dumps(run1))
        difettoso["rischi"][0]["score_composito"] = 3.8
        codice, out = b.esegui("trimestrale", "--payload", b.scrivi_json("x1.json", difettoso),
                               "--challenger", DATI / "run_A5_2026Q3.json")
        e.verifica(codice == 1 and "non conforme allo schema" in out, "1. payload fuori schema: fermo (codice 1)", out)
        # D-71: ferma solo un difetto di integrita'; qui un kri_id di un altro rischio (lo schema non lo vede).
        estraneo = json.loads(json.dumps(run1))
        estraneo["rischi"][0]["kri_proposti"][0].update(kri_id="NFR-02-K1")
        correzione = b.uscita / "Cicli" / "2026Q3" / "Correzione_A1_2026Q3.txt"
        codice, out = b.esegui("trimestrale", "--payload", b.scrivi_json("x2.json", estraneo),
                               "--challenger", DATI / "run_A5_2026Q3.json")
        e.verifica(codice == 1 and "C9" in out and "Messaggio per A1" in out and correzione.exists()
                   and "NFR-01 · C9: " in correzione.read_text(encoding="utf-8"),
                   "1. kri_id di un altro rischio: fermo da C9 e messaggio per A1 scritto da trimestrale (D-71)", out)
        correzione.unlink()
        # 1-bis. Precontrollo (D-69): lo stesso difetto si vede prima, senza Excel e senza toccare il registro.
        codice, out = b.esegui("precontrollo", "--payload", b.cartella / "x2.json", "--baseline", b.cartella / "base_q3.json")
        e.verifica(codice == 1 and correzione.exists() and "NFR-01 · C9: " in correzione.read_text(encoding="utf-8")
                   and sha(b.wb) == prima,
                   "1-bis. precontrollo: kri_id estraneo trovato prima di scrivere, messaggio per A1 nell'archivio del ciclo, registro intatto", out)
        codice, out = b.esegui("precontrollo", "--payload", DATI / "run1_A1_2026Q3.json", "--baseline", b.cartella / "base_q3.json")
        e.verifica(codice == 0 and "0 punti da correggere" in out,
                   "1-bis. precontrollo di run1: niente che fermi il ciclo (solo la forma del razionale, scritto prima del 02/10)", out)
        codice, out = b.esegui("trimestrale", "--payload", DATI / "run1_A1_2026Q3.json",
                               "--challenger", DATI / "run_A5_2026Q4.json")
        e.verifica(codice == 1 and "e' del ciclo 2026Q4" in out, "1. esito di A5 di un altro ciclo: fermo (non si riusa un'approvazione)", out)
        a5_estraneo = carica(DATI / "run_A5_2026Q3.json")
        a5_estraneo["rilievi"] = [{"controllo": "C6", "id_rischio": "NFR-19", "gravita": "Osservazione",
                                   "descrizione": "Rilievo su un rischio che non esiste in questo ciclo."}]
        codice, out = b.esegui("trimestrale", "--payload", DATI / "run1_A1_2026Q3.json",
                               "--challenger", b.scrivi_json("a5_estraneo.json", a5_estraneo))
        e.verifica(codice == 1 and "NFR-19" in out, "1. esito di A5 che cita rischi non presenti in A1: fermo", out)
        rotto = b.cartella / "non_json.json"
        rotto.write_text("Ecco il JSON richiesto: {\"ciclo\": \"2026Q3\"", encoding="utf-8")
        codice, out = b.esegui("trimestrale", "--payload", rotto, "--challenger", DATI / "run_A5_2026Q3.json")
        e.verifica(codice == 1 and "non e' un JSON valido" in out, "1. file che non e' JSON: fermo (codice 1), non errore tecnico", out)
        e.verifica(sha(b.wb) == prima, "1. checksum del workbook identico: zero byte scritti")
        e.verifica(not (b.uscita / "Backup").exists(), "1. nessun backup creato: la scrittura non e' mai iniziata")

        # 2. Ciclo 2026Q3 (A1 salvato "UTF-8 con BOM", come puo' fare il Blocco note)
        con_bom = b.cartella / "A1_bom.json"
        con_bom.write_text(json.dumps(run1, ensure_ascii=False, indent=2), encoding="utf-8-sig")
        codice, out = b.esegui("trimestrale", "--payload", con_bom,
                               "--challenger", DATI / "run_A5_2026Q3.json")
        e.verifica(codice == 0, "2. ciclo 2026Q3 scritto (codice 0), anche da un file UTF-8 con BOM", out)
        e.verifica(sha(b.wb) != prima and any((b.uscita / "Backup").iterdir()), "2. workbook salvato, backup creato prima")
        s = b.leggi()
        verifica_integrita(e, s, "2. 2026Q3")
        spieg = b.uscita / "Spiegazioni"
        ciclo_txt = (spieg / "Ciclo.txt").read_text(encoding="utf-8") if (spieg / "Ciclo.txt").exists() else ""
        e.verifica(rischi_nei_posti(spieg) == (20, 12) and "CICLO 2026Q3" in ciclo_txt and "PROPOSTI" in ciclo_txt
                   and "Knowledge di A7 aggiornata" in out,
                   "2. knowledge di A7 (D-72): Ciclo.txt e 20 file fissi, uno per posto dell'anagrafica (12 rischi, 8 posti "
                   "liberi), valori dichiarati proposti",
                   out[-400:] + ciclo_txt[:300])
        e.verifica(s["copertura_foglio"] == (12, 12) and s["f10"] == "Ciclo completo", "2. controllo di copertura: 12/12, ciclo completo")
        e.verifica(s["ciclo"] == "2026Q3" and s["register"][-1]["Ciclo"] == "2026Q3" and len(s["register"]) == RR_TEMPLATE + 16,
                   "2. RiskRegister: 16 righe in coda alla tabella (12 del radar, NFR-16 nuovo, 3 in osservazione riportati), "
                   "ciclo corrente 2026Q3", str(len(s["register"])))
        righe_kri_template = 66     # due KRI per rischio (D-64): 18 nel 2025Q4 + 24 nel 2026Q1 + 24 nel 2026Q2
        kri = {k["KRI_ID"]: k for k in s["kri"] if k["Ciclo"] == "2026Q3"}
        e.verifica(len(s["kri"]) == righe_kri_template + 25 and len(kri) == 25,
                   "2. storico KRI: 25 righe del 2026Q3 in coda (24 in vigore prima + 1 nuovo), niente sovrascritto",
                   f"{len(s['kri'])} righe, {len(kri)} del 2026Q3")
        e.verifica(kri["NFR-01-K1"]["Valore_Corrente"] == 5.1 and kri["NFR-01-K1"]["Data_Rilevazione"] == "2026-09-30",
                   "2. rilettura KRI applicata per KRI_ID, con la data giusta", str(kri["NFR-01-K1"]))
        q2 = next(k for k in s["kri"] if k["KRI_ID"] == "NFR-01-K1" and k["Ciclo"] == "2026Q2")
        e.verifica(q2["Valore_Corrente"] == 4.2 and q2["Data_Rilevazione"] == "2026-06-30",
                   "2. la riga del 2026Q2 resta com'era: lo storico non si riscrive", str(q2))
        e.verifica(kri["NFR-03-K2"]["Valore_Corrente"] is None and kri["NFR-03-K2"]["Stato"] == "Non rilevato",
                   "2. valore non rilevato resta vuoto: stato 'Non rilevato', mai Verde")
        e.verifica("NFR-02-K3" in kri and kri["NFR-02-K3"]["Ciclo_Definizione"] == "2026Q3" and kri["NFR-02-K2"]["In_Vigore"] == "No",
                   "2. KRI nuovo = primo progressivo libero (K4, non K2 riusato); il sostituito esce di vigore")
        e.verifica(kri["NFR-02-K3"]["Valore_Corrente"] is None, "2. il KRI nuovo entra senza valore (non eredita quello del sostituito)")
        e.verifica(kri["NFR-02-K1"]["Stato"] == "Ambra", "2. lo stato dei KRI aggiornati e' ricalcolato dalla formula")
        k_q2 = next(k for k in s["kri"] if k["KRI_ID"] == "NFR-03-K1" and k["Ciclo"] == "2026Q2")
        e.verifica((kri["NFR-03-K1"]["Soglia_Attenzione"], kri["NFR-03-K1"]["Soglia_Allerta"])
                   == (k_q2["Soglia_Attenzione"], k_q2["Soglia_Allerta"]) and k_q2["Soglia_Attenzione"] is not None,
                   "2. KRI riproposto senza soglie: restano quelle in vigore (D-53)", f"{kri['NFR-03-K1']}\n{k_q2}")
        e.verifica(kri["NFR-10-K1"]["Soglia_Attenzione"] is None and kri["NFR-10-K1"]["Stato"] == "Soglie da definire",
                   "2. KRI senza soglie: stato 'Soglie da definire', mai un falso Rosso", str(kri["NFR-10-K1"]))
        q3 = {r["ID_Rischio"]: r for r in s["register"] if r["Ciclo"] == "2026Q3"}
        var03 = json.loads(q3["NFR-03"]["Variazioni"])
        e.verifica(q3["NFR-03"]["Esito"] == "Variato" and q3["NFR-06"]["Esito"] == "Confermato" and q3["NFR-02"]["Esito"] == "Confermato"
                   and q3["NFR-01"]["Esito"] == "Confermato" and len(var03) == 1 and var03[0]["da"] == 3 and var03[0]["a"] == 4,
                   "2. esito e 'da/a' dallo script (D-51): NFR-03 Variato (prossimita da 3 a 4); gli altri Confermati", f"{[(k, v['Esito']) for k, v in q3.items()]}\n{var03}")
        e.verifica(q3["NFR-10"]["Velocity"] is None and q3["NFR-10"]["Esito"] == "Confermato",
                   "2. Velocity non valutata resta vuota (non zero); rimasta non valutata = Confermato", str(q3["NFR-10"]))
        verifica_report(e, s, "2. report 2026Q3", commento=run1["sintesi"])
        q3 = {r["ID_Rischio"]: r for r in s["register"] if r["Ciclo"] == "2026Q3"}
        stati = {i: (r["Stato"], r["Esito"], r["Validazione"], r["Periodo_Valutazione"]) for i, r in q3.items()}
        e.verifica(all(stati[i][0] == "Radar" for i in s["registro"]) and len(s["registro"]) == 12
                   and stati["NFR-16"] == ("Osservazione", "Nuovo", "Da validare", "2026Q3")
                   and q3["NFR-16"]["Motivo_Stato"] == "Prossimita 1 sotto la soglia 2" and q3["NFR-16"]["Orizzonte_Anni"] == 5
                   and stati["NFR-13"] == ("Osservazione", "Confermato", "Accettato", "2026Q1")
                   and stati["NFR-14"] == ("Osservazione", "Confermato", "Accettato", "2026Q2")
                   and stati["NFR-15"] == ("Osservazione", "Confermato", "Accettato", "2026Q2")
                   and not any(r["Movimento"] for r in q3.values())
                   and "nel radar 12 rischi su 15 posti; in osservazione 4; entrati nel radar nessuno; usciti nessuno" in out,
                   "2. registro unico (D-79): NFR-16 nuovo resta in osservazione (Prossimita 1 sotto la soglia), da validare; "
                   "i tre in osservazione non toccati da A1 riportati com'erano, gia' validati, con il loro periodo di "
                   "valutazione; i 12 del radar restano nel radar", str(stati) + out[-600:])
        e.verifica(not [k for k in s["kri"] if k["ID_Rischio"] in ("NFR-13", "NFR-14", "NFR-15", "NFR-16")]
                   and not [a for a in carica_tabella(b, "tblAzioni") if a["ID_Rischio"] in ("NFR-13", "NFR-14", "NFR-15", "NFR-16")]
                   and "NFR-16" not in {a["ID"] for a in s["anagrafica"]},
                   "2. un rischio in osservazione non ha KRI ne' azioni e non e' nell'anagrafica (= il radar)")
        e.verifica([f[0] for f in s["fenomeni"]] == ["NFR-14", "NFR-13", "NFR-16", "NFR-15"]
                   and [round(f[1], 2) for f in s["fenomeni"]] == [2.9, 2.75, 2.19, 2.13]
                   and s["fenomeni"][1][2] == "Prossimita 1 sotto la soglia 2; Probabilita 1 sotto la soglia 2"
                   and s["copertura_foglio"] == (12, 12) and not s["fenomeni_uscite"],
                   "2. pagina Fenomeni: i 4 rischi in osservazione dallo score piu' alto, con il perche' (soglie); radar e "
                   "copertura contano solo i 12 del radar; nessun movimento", str(s["fenomeni"]))
        a5_q3 = carica(DATI / "run_A5_2026Q3.json")
        riga_q3 = next(r for r in s["sintesi_cicli"] if r["Ciclo"] == "2026Q3")
        e.verifica(riga_q3["Sintesi_A5"] == a5_q3["sintesi"] and isinstance(riga_q3["Osservazioni_Controlli"], int)
                   and riga_q3["Data_Riferimento"] == "2026-09-30" and not s["avviso"],
                   "2. Sintesi_Cicli: sintesi del challenger e numero di osservazioni; nessun avviso prima della validazione",
                   f"{riga_q3} {s['avviso']!r}")
        archivio_q3 = b.uscita / "Cicli" / "2026Q3"
        excel_q3 = archivio_q3 / "NFR_workbook_2026Q3.xlsx"
        e.verifica(excel_q3.exists() and sha(excel_q3) == sha(b.wb)
                   and all((archivio_q3 / f).exists() for f in ("A1_2026Q3.json", "A5_2026Q3.json", "Esito_controlli_2026Q3.json", "Baseline_usata_2026Q3.json")),
                   "2. archivio del ciclo: Excel di output con il nome del ciclo + output degli agenti ed esito dei controlli",
                   str(sorted(p.name for p in archivio_q3.iterdir())) if archivio_q3.exists() else "cartella assente")
        tentativi = [p for p in archivio_q3.iterdir() if p.name.startswith("tentativo_")]
        e.verifica(len(tentativi) == 4,
                   "2. ogni tentativo e' archiviato: 3 fermati dai controlli + 1 riuscito (fuori schema e non-JSON si fermano "
                   "prima; senza A5 non ci si ferma piu', D-71)",
                   str(sorted(p.name for p in tentativi)))
        base_json, base_txt = b.uscita / "Baseline_corrente.json", b.uscita / "Baseline_corrente.txt"
        e.verifica(base_txt.exists() and base_txt.read_bytes() == base_json.read_bytes(),
                   "2. Baseline_corrente anche in .txt, identica (knowledge di Agent Builder)")
        allegato = b.uscita / "Input_A1_2026Q4.txt"
        testo_allegato = allegato.read_text(encoding="utf-8") if allegato.exists() else ""
        e.verifica(testo_allegato and json.loads(testo_allegato.split("=== 1. BASELINE ===\n", 1)[1].split("\n\n=== 2.", 1)[0])
                   == carica(base_json) and "- C9 KRI:" in testo_allegato and "=== 3. GUIDA DI SCRITTURA ===" in testo_allegato,
                   "2. allegato di A1 per il ciclo dopo (D-69): Input_A1_2026Q4.txt con la stessa baseline, i controlli e la guida",
                   str(sorted(p.name for p in b.uscita.iterdir())))
        firma_q3 = sha(excel_q3)
        liste = carica(archivio_q3 / "Righe_liste_2026Q3.json")
        attese = {nome: [c for c in spec.get("colonne_aggiunte", [])] +
                  [c["nome"] for c in MAPPA["tabelle"][spec["da_tabella"]]["colonne"] if c["nome"] not in spec["colonne_escluse"]]
                  for nome, spec in MAPPA["liste_sharepoint"].items() if not nome.startswith("_")}
        e.verifica(all(list(liste[n][0]) == attese[n] for n in attese),
                   "2. righe per le liste SharePoint: colonne esattamente come da mappa", str({n: list(liste[n][0]) for n in attese}))
        kri_lista = {r["KRI_ID"]: r for r in liste["KRI_Storico"]}
        e.verifica(len(liste["RiskRegister_Storico"]) == 16 and len(liste["Azioni_Storico"]) == 15 and len(kri_lista) == 25
                   and kri_lista["NFR-02-K2"]["In_Vigore"] == "No" and kri_lista["NFR-02-K3"]["Valore_Corrente"] is None,
                   "2. liste: 16 rischi (radar e osservazione), 15 azioni, 25 KRI (incluso quello uscito); il KRI nuovo non "
                   "eredita valori",
                   f"{len(liste['RiskRegister_Storico'])} {len(liste['Azioni_Storico'])} {len(kri_lista)}")

        # 2b. Validazione umana del 2026Q3 nella griglia del foglio Validazione (D-67)
        s = b.leggi()
        val_q3 = [r for r in s["validazione"] if r["Periodo"] == "2026Q3"]
        e.verifica(len(val_q3) == 13 * 6 + 25 * 3 + 15 * 2 and all(r["Stato"] == "Da decidere" for r in val_q3),
                   "2b. lo storico ha una riga 'Da decidere' per ogni campo proposto (13 rischi x 6 con la decisione sullo "
                   "stato, 25 KRI x 3, 15 azioni x 2); i 3 rischi in osservazione riportati non si rivalutano",
                   str(len(val_q3)))
        e.verifica(len(s["griglia"]) == 13 + 25 + 15 and griglia_uguale_alle_proposte(s, "2026Q3")
                   and righe_visibili(b) == {"Rischio": 13, "KRI": 25, "Azione": 15, "Notizia": 0}
                   and str(s["griglia_stato"]).startswith("Da validare: ciclo 2026Q3 (53 righe)")
                   and s["griglia_stati"]["NFR-16"] == "Osservazione: Prossimita 1 sotto la soglia 2"
                   and s["griglia_stati"]["NFR-01"].startswith("Radar: Prossimita 4 e Probabilita 4: sopra la soglia")
                   and all(g["valori"]["Decisione_Stato"] == "Automatico" for k, g in s["griglia"].items() if k[0] == "Rischio"),
                   "2b. griglia: una riga per rischio (anche NFR-16 in osservazione), KRI e azione proposti da A1 (53, le "
                   "altre nascoste), celle gialle uguali alle proposte; colonna Stato con il motivo, decisione sullo stato "
                   "Automatico",
                   f"{len(s['griglia'])} {s['griglia_stato']!r} {s['griglia_stati']}")
        q3 = {r["ID_Rischio"]: r for r in s["register"] if r["Ciclo"] == "2026Q3"}
        radar = {m[0]: round(m[2], 6) for m in s["mosca"]}
        e.verifica(set(s["griglia_rischi"]) == set(radar) | {"NFR-16"}
                   and {i: (round(v[0], 2), round(v[1], 6)) for i, v in s["griglia_rischi"].items() if i in radar}
                   == {i: (score_d50(q3[i]), radar[i]) for i in radar},
                   "2b. griglia: Score composito e Margine di Mosca delle proposte = quelli del Registro e del Radar_Mosca",
                   f"griglia {s['griglia_rischi']}\nregistro {[(i, score_d50(q3[i]), radar[i]) for i in radar]}")
        e.verifica(s["f8"].startswith("CICLO NON ANCORA VALIDATO") and
                   all(r["Validazione"] == "Da validare" for r in s["register"] if r["Ciclo"] == "2026Q3"
                       and r["Periodo_Valutazione"] == "2026Q3"),   # i riportati (D-79) sono gia' validati
                   "2b. Registro e RiskRegister dicono che il ciclo non e' validato", s["f8"])
        codice, out = b.esegui("schede-input")
        e.verifica(codice == 1 and "righe da validare" in out and not (b.uscita / "Cicli" / "2026Q3" / "Schede_input_2026Q3.json").exists(),
                   "2b. le schede non si fanno su un ciclo non validato (schede-input fermo)", out)
        codice, out = b.esegui("report")
        e.verifica(codice == 1 and "righe da validare" in out and not (b.uscita / "Cicli" / "2026Q3" / "Report_comitato_2026Q3.pdf").exists(),
                   "2b. il report non si rigenera su un ciclo non validato (report fermo)", out)
        prima = sha(b.wb)
        codice, out = b.esegui("trimestrale", "--payload", DATI / "run3_A1_2026Q4.json", "--challenger", DATI / "run_A5_2026Q4.json")
        e.verifica(codice == 1 and "non e' ancora validato" in out and "53 righe" in out and sha(b.wb) == prima,
                   "2b. il ciclo dopo non parte finche' il 2026Q3 non e' validato (fermo, workbook intatto)", out)
        dec = carica(DATI / "decisioni_validatore_2026Q3.json")
        codice, out = b.esegui("valida", "--periodo", "2026Q2", "--validatore", dec["validatore"])
        e.verifica(codice == 1 and "niente da validare" in out and sha(b.wb) == prima,
                   "2b. valida su un periodo gia' validato: niente da fare", out)
        sbagliate = [{"oggetto": "Rischio", "id": "NFR-01", "campo": "Impatto", "decisione": "Rettificato", "valore": 1},
                     {"oggetto": "KRI", "id": "NFR-01-K1", "campo": "Valore_Corrente", "decisione": "Rettificato", "valore": "abc",
                      "motivazione": "Valore letto male dal report antifrode."},
                     {"oggetto": "KRI", "id": "NFR-10-K1", "campo": "Soglia_Attenzione", "decisione": "Rettificato", "valore": 2,
                      "motivazione": "Soglia di attenzione fissata dalla funzione di rischio."},
                     {"oggetto": "KRI", "id": "NFR-03-K1", "campo": "", "decisione": "", "respingi": "forse",
                      "motivazione": "Indicatore da rivedere con la funzione Compliance."},
                     {"oggetto": "Azione", "id": "2026Q3-NFR-08-A1", "campo": "", "decisione": "Respinto", "motivazione": "breve"}]
        scrivi_decisioni(b.wb, "2026Q3", sbagliate)
        prima = sha(b.wb)
        codice, out = b.esegui("valida", "--periodo", "2026Q3", "--validatore", dec["validatore"])
        e.verifica(codice == 1 and "6 problemi" in out and "cambiato Impatto senza una Motivazione" in out
                   and "piu' di un punto" in out and "deve essere un numero" in out and "Respingi 'forse'" in out
                   and "respinto senza una Motivazione" in out and "soglie entrambe o nessuna" in out
                   and "riga 7 del foglio Validazione" in out and sha(b.wb) == prima,
                   "2b. righe non valide (Impatto oltre un punto e senza motivazione, valore non numerico, Respingi "
                   "sbagliato, motivazione corta, una soglia sola): tutte elencate con la riga, niente applicato", out)
        azzera_griglia(b.wb)
        scrivi_decisioni(b.wb, "2026Q3", dec["decisioni"])
        s_prima = b.leggi()
        e.verifica(s_prima["griglia_rischi"]["NFR-06"][1] == 0.25 and s_prima["griglia_rischi"]["NFR-08"][1] == 0.25,
                   "2b. griglia: il margine si ricalcola mentre si scrive (NFR-06 con un anno di adeguamento, NFR-08 senza "
                   "l'azione respinta: da 0,75 e 1,00 a 0,25)", str(s_prima["griglia_rischi"]))
        codice, out = b.esegui("valida", "--periodo", "2026Q3", "--validatore", dec["validatore"])
        e.verifica(codice == 0 and "53 righe" in out and "rettificate 4 (5 valori cambiati), respinte 1" in out,
                   "2b. validazione del 2026Q3 applicata: 4 righe rettificate (5 valori), 1 respinta (un'azione)", out)
        pdf_valida = b.uscita / "Cicli" / "2026Q3" / "Report_comitato_2026Q3.pdf"
        e.verifica(pdf_valida.exists() and pdf_valida.stat().st_size > 10000 and "Report al comitato del ciclo 2026Q3" in out,
                   "2b. valida rigenera da sola il report al comitato del ciclo validato (D-83)", out[-600:])
        nfr10 = file_rischio(b.uscita / "Spiegazioni", "NFR-10") or ""
        nfr08 = file_rischio(b.uscita / "Spiegazioni", "NFR-08") or ""
        e.verifica("VALIDATI" in (b.uscita / "Spiegazioni" / "Ciclo.txt").read_text(encoding="utf-8")
                   and "Velocity: Rettificato" in nfr10 and "Soglia_Attenzione: Rettificato" in nfr10 and "Respinto" in nfr08,
                   "2b. knowledge di A7 dopo valida: valori validati, rettifiche e respingimenti con la motivazione nel file "
                   "del rischio", nfr10[-800:])
        s = b.leggi()
        q3 = {r["ID_Rischio"]: r for r in s["register"] if r["Ciclo"] == "2026Q3"}
        radar = {m[0]: round(m[2], 6) for m in s["mosca"]}
        e.verifica({i: (round(v[0], 2), round(v[1], 6)) for i, v in s_prima["griglia_rischi"].items() if i in radar}
                   == {i: (score_d50(q3[i]), radar[i]) for i in radar},
                   "2b. Score e Margine calcolati dalla griglia PRIMA di valida = quelli del Registro e del Radar_Mosca DOPO",
                   f"griglia {s_prima['griglia_rischi']}\nregistro {[(i, score_d50(q3[i]), radar[i]) for i in radar]}")
        e.verifica(not s["griglia"] and str(s["griglia_stato"]).startswith("Niente da validare")
                   and righe_visibili(b) == {"Rischio": 0, "KRI": 0, "Azione": 0, "Notizia": 0},
                   "2b. dopo valida il ciclo esce dalla griglia (niente da validare, righe nascoste)", str(s["griglia_stato"]))
        respinta = [r for r in s["validazione"] if r["ID"] == "2026Q3-NFR-08-A1"]
        e.verifica(len(respinta) == 2 and all(r["Decisione"] == "Respinto" and r["Valore_Validato"] is None
                                              and len(str(r["Motivazione"])) > 10 for r in respinta),
                   "2b. storico: Respingi vale per tutti i campi dell'azione, con la motivazione della riga", str(respinta))
        base_dopo = carica(b.uscita / "Baseline_corrente.json")
        n16 = next((x for x in base_dopo["rischi_in_osservazione"] if x["id_rischio"] == "NFR-16"), {})
        e.verifica(sorted(x["id_rischio"] for x in base_dopo["rischi_in_osservazione"]) == ["NFR-13", "NFR-14", "NFR-15", "NFR-16"]
                   and next(r for r in s["register"] if r["Ciclo"] == "2026Q3" and r["ID_Rischio"] == "NFR-16")["Stato"] == "Osservazione"
                   and (n16.get("orizzonte_anni"), n16.get("stato"), n16.get("decisione_stato")) == (5, "Osservazione", "Automatico")
                   and str(n16.get("segnale_avvicinamento")).startswith("Uno sciopero di settore")
                   and "Radar di Mosca dopo la validazione" not in out,      # nessun movimento: valida non ne parla
                   "2b. dopo valida lo stato si ricalcola sui valori validati: NFR-16 resta in osservazione; la baseline del "
                   "ciclo dopo ha i 4 rischi in osservazione con orizzonte, segnale e decisione",
                   str(base_dopo["rischi_in_osservazione"])[:800] + out[-400:])
        nfr06 = next(r for r in s["register"] if r["Ciclo"] == "2026Q3" and r["ID_Rischio"] == "NFR-06")
        e.verifica(nfr06["Anni_Adeguamento"] == 1 and nfr06["Validazione"] == "Rettificato" and nfr06["Approvato_Da"] == dec["validatore"]
                   and nfr06["Esito"] == "Confermato" and nfr06["Data_Validazione"] and json.loads(nfr06["Variazioni"]) == [],
                   "2b. rettifica degli anni di adeguamento applicata al registro, con chi e quando; non e' una variazione, "
                   "l'esito resta Confermato", str(nfr06))
        ana = {a["ID"]: a for a in s["anagrafica"]}
        e.verifica(ana["NFR-06"]["Anni_Adeguamento"] == 1 and ana["NFR-11"]["Anni_Adeguamento"] == 3,
                   "2b. anni di adeguamento validati scritti nell'anagrafica (D-60): NFR-06 rettificato a 1, NFR-11 accettato a 3",
                   str({k: ana[k]["Anni_Adeguamento"] for k in ("NFR-06", "NFR-11")}))
        nfr10 = next(r for r in s["register"] if r["Ciclo"] == "2026Q3" and r["ID_Rischio"] == "NFR-10")
        var10 = json.loads(nfr10["Variazioni"])
        e.verifica(nfr10["Velocity"] == 3 and nfr10["Esito"] == "Variato" and len(var10) == 1 and var10[0]["dimensione"] == "velocity"
                   and var10[0]["da"] is None and var10[0]["a"] == 3 and var10[0]["evidenza"].startswith("Rettifica del validatore"),
                   "2b. Velocity da non valutata a 3 in validazione: variazione 'da n.v.' ed esito Variato", str(nfr10))
        k10 = next(k for k in s["kri"] if k["Ciclo"] == "2026Q3" and k["KRI_ID"] == "NFR-10-K1")
        e.verifica(k10["Soglia_Attenzione"] == 2 and k10["Soglia_Allerta"] == 5 and k10["Stato"] != "Soglie da definire",
                   "2b. soglie fissate dalla Banca in validazione: lo stato del KRI si calcola", str(k10))
        liste_val = carica(archivio_q3 / "Righe_liste_2026Q3.json")
        r06 = next(r for r in liste_val["RiskRegister_Storico"] if r["ID_Rischio"] == "NFR-06")
        e.verifica(r06["Anni_Adeguamento"] == 1 and r06["Validazione"] == "Rettificato" and r06["Approvato_Da"] == dec["validatore"],
                   "2b. righe per le liste riscritte dalla validazione: valori validati, chi ha validato", str(r06))
        k1 = next(k for k in s["kri"] if k["Ciclo"] == "2026Q3" and k["KRI_ID"] == "NFR-01-K1")
        az = next(a for a in carica_tabella(b, "tblAzioni") if a["ID_Azione"] == "2026Q3-NFR-08-A1")
        e.verifica(k1["Valore_Corrente"] == 5.3 and k1["Validazione"] == "Rettificato" and az["Stato"] == "Respinta"
                   and az["Validazione"] == "Respinto", "2b. rettifica di un KRI e azione respinta applicate", f"{k1} {az}")
        riga = next(r for r in s["validazione"] if r["Periodo"] == "2026Q3" and r["ID"] == "NFR-06" and r["Campo"] == "Anni_Adeguamento")
        e.verifica(riga["Proposta_Agente"] in (None, "") and riga["Valore_Validato"] == 1 and riga["Decisione"] == "Rettificato"
                   and len(riga["Motivazione"]) > 10 and riga["Stato"] == "Applicata",
                   "2b. la proposta dell'agente resta accanto al valore deciso e al motivo (base per l'apprendimento)", str(riga))
        e.verifica(all(r["Stato"] == "Applicata" for r in s["validazione"] if r["Periodo"] == "2026Q3") and s["f8"] == "Ciclo validato",
                   "2b. tutte le righe del ciclo applicate; Registro: ciclo validato", s["f8"])
        e.verifica(str(s["avviso"]).startswith("Il validatore ha applicato 6 ") and not s["rilievi_superati"],
                   "2b. Quadro: avviso che il commento di A1 precede 6 rettifiche o respingimenti; nessun rilievo superato",
                   f"{s['avviso']!r} {s['rilievi_superati']!r}")
        verifica_report(e, s, "2b. report dopo la validazione")
        e.verifica((archivio_q3 / "Validazione_2026Q3.json").exists() and (archivio_q3 / "NFR_workbook_2026Q3_validato.xlsx").exists()
                   and sha(excel_q3) == firma_q3,
                   "2b. archivio: registro delle decisioni e Excel validato; l'Excel di output pre-validazione resta com'era")
        e.verifica(next(r for r in carica(b.uscita / "Baseline_corrente.json")["rischi"] if r["id_rischio"] == "NFR-06")["anni_adeguamento"] == 1,
                   "2b. la baseline del prossimo ciclo usa i valori validati (anni di adeguamento dall'anagrafica)")
        # Comando report (D-62): PDF del report rigenerato dall'Excel, la versione precedente resta.
        pdf = b.uscita / "Cicli" / "2026Q3" / "Report_comitato_2026Q3.pdf"
        prima = sha(b.wb)
        codice, out = b.esegui("report")
        e.verifica(codice == 0 and pdf.exists() and pdf.stat().st_size > 10000 and sha(b.wb) == prima,
                   "2b. report: PDF del report al comitato dal registro validato, registro intatto", out)
        codice, out = b.esegui("report", "--con-lavoro")
        vecchi = list(pdf.parent.glob("Report_comitato_2026Q3_*.pdf"))
        e.verifica(codice == 0 and pdf.exists() and len(vecchi) == 2 and "Registro, Parametri" in out,
                   "2b. report --con-lavoro: aggiunge Registro e Parametri; le versioni precedenti del PDF (di valida e del "
                   "primo report) sono conservate", out)
        codice, out = b.esegui("valida", "--periodo", "2026Q3", "--validatore", dec["validatore"])
        e.verifica(codice == 1 and "niente da validare" in out, "2b. rilanciare valida sullo stesso ciclo: niente da fare", out)
        schede_a6(e, b, s)

        # 3. Settimana 2026-10-12 (area scoperta al ciclo N)
        prima = sha(b.wb)
        fuori_elenco = carica(DATI / "run_A3_2026-10-12.json")
        fuori_elenco["notizie"][0]["codice_fonte"] = "FNT-99"
        codice, out = b.esegui("settimanale", "--payload", b.scrivi_json("a3_fonte.json", fuori_elenco))
        e.verifica(codice == 1 and "FNT-99" in out and sha(b.wb) == prima,
                   "3. notizia con un codice fonte fuori elenco: fermo, workbook intatto", out)
        fuori_registro = carica(DATI / "run_A3_2026-10-12.json")
        fuori_registro["notizie"][1]["rischio_collegato"] = "NFR-19"          # non e' nel registro (ne' radar ne' osservazione)
        codice, out = b.esegui("settimanale", "--payload", b.scrivi_json("a3_fuori.json", fuori_registro))
        e.verifica(codice == 1 and "NFR-19" in out and sha(b.wb) == prima,
                   "3. notizia collegata a un rischio che non e' nel registro (NFR-19): fermo, workbook intatto", out)
        doppia = carica(DATI / "run_A3_2026-10-12.json")
        doppia["notizie"].append(dict(doppia["notizie"][0]))
        codice, out = b.esegui("settimanale", "--payload", b.scrivi_json("a3_doppia.json", doppia))
        e.verifica(codice == 1 and "ripetuti" in out and sha(b.wb) == prima,
                   "3. stessa notizia due volte nello stesso output di A3: fermo, workbook intatto", out)
        # Titoli "pericolosi" (da feed esterni): devono restare testo, non formula ne' data.
        a3 = carica(DATI / "run_A3_2026-10-12.json")
        titoli = {a3["notizie"][0]["id_notizia"]: "=HYPERLINK(\"http://example.invalid\",\"clicca\") titolo da un feed",
                  a3["notizie"][1]["id_notizia"]: "5/6/2026"}       # minimo 5 caratteri (schema A3)
        for n in a3["notizie"]:
            n["titolo"] = titoli.get(n["id_notizia"], n["titolo"])
        codice, out = b.esegui("settimanale", "--payload", b.scrivi_json("a3_titoli.json", a3))
        e.verifica(codice == 0, "3. settimana 2026-10-12 scritta", out)
        s = b.leggi()
        verifica_integrita(e, s, "3. settimana")
        scritti = {n["ID_Notizia"]: n["Titolo"] for n in s["news"]}
        e.verifica(all(scritti.get(i) == t for i, t in titoli.items()),
                   "3. un titolo che inizia con '=' o che sembra una data resta testo, identico",
                   str({i: scritti.get(i) for i in titoli}))
        e.verifica(s["settimana"] == "2026-10-12", "3. la settimana corrente e' scorsa al 12/10/2026")
        collegata = {n["ID_Notizia"]: n.get("Rischio_ID") for n in s["news"]}
        flag = next((r.get("Flag_Proposti") for r in s["settimane"] if r["Settimana"] == "2026-10-12"), "")
        e.verifica(collegata.get("N-20261006-01") == "NFR-16" and "NFR-16 · Peggiorativo: " in str(flag),
                   "3. A3 collega la notizia dello sciopero al rischio in osservazione NFR-16 e propone un flag (D-79: "
                   "stesso meccanismo dei rischi del radar)", f"{collegata} {flag!r}")
        e.verifica((b.uscita / "Settimane" / "2026-10-12" / "NFR_workbook_2026-10-12.xlsx").exists()
                   and (b.uscita / "Settimane" / "2026-10-12" / "A3_2026-10-12.json").exists(),
                   "3. archivio della settimana: Excel di output con la data + output di A3")
        e.verifica(s["presidio"]["9.11"] == PRESIDIO_911_Q3, "3. 9.11 Employer: nessun rischio del radar, la notizia va "
                   "sul rischio in osservazione NFR-16", str(s["presidio"]))
        e.verifica(str(s["badge"]["NFR-01"]).startswith("▲"), "3. tre segnali peggiorativi: badge NFR-01 in peggioramento", str(s["badge"]))
        riga = [r for r in s["settimane"] if r["Settimana"] == "2026-10-12"]
        e.verifica(len(riga) == 1 and riga[0]["Sintesi_A3"] == a3["sintesi"] and riga[0]["Notizie"] == len(a3["notizie"])
                   and riga[0]["Flag_Proposti"].startswith("NFR-01 · Peggiorativo: ")
                   and s["riquadro_settimana"] == (a3["sintesi"], riga[0]["Flag_Proposti"]),
                   "3. sintesi di A3 e flag proposti nel foglio Sintesi_Settimane e nel riquadro del foglio Notizie (D-66)",
                   f"{riga}\n{s['riquadro_settimana']}")
        n = len(s["news"])
        codice, out = b.esegui("settimanale", "--payload", DATI / "run_A3_2026-10-12.json")
        s = b.leggi()
        e.verifica(codice == 0 and "0 notizie aggiunte" in out and len(s["news"]) == n
                   and len([r for r in s["settimane"] if r["Settimana"] == "2026-10-12"]) == 1,
                   "3. rilancio della stessa settimana: nessuna notizia duplicata, la sintesi della settimana si aggiorna",
                   out + str(s["settimane"]))

        dec_w = carica(DATI / "decisioni_validatore_2026-10-12.json")
        s = b.leggi()
        e.verifica(sum(1 for r in s["validazione"] if r["Periodo"] == "2026-10-12" and r["Stato"] == "Da decidere") == 10
                   and len(s["griglia"]) == 5 and griglia_uguale_alle_proposte(s, "2026-10-12")
                   and "settimana del 12/10/2026 (5 notizie)" in str(s["griglia_stato"]),
                   "3. la settimana: nello storico 2 righe per notizia (Rischio_ID, Segnale), nella griglia una per notizia",
                   str(s["griglia_stato"]))
        scrivi_decisioni(b.wb, dec_w["periodo"], dec_w["decisioni"])
        # Una riga cancellata a mano dalla griglia: valida si ferma e indica il comando griglia, che la ripara
        # conservando cio' che e' gia' scritto nelle altre righe.
        with SessioneExcel(b.wb) as sess:
            sess.intervallo_nome("VG_Notizia_ID").Cells(1, 1).Value = None
            sess.salva()
        prima = sha(b.wb)
        codice, out = b.esegui("valida", "--periodo", "2026-10-12", "--validatore", dec_w["validatore"])
        e.verifica(codice == 1 and "mancano 1 righe" in out and "esegui_ciclo_locale.py griglia" in out and sha(b.wb) == prima,
                   "3. una riga cancellata dalla griglia: valida si ferma e indica il comando griglia", out)
        codice, out = b.esegui("griglia")
        s = b.leggi()
        e.verifica(codice == 0 and len(s["griglia"]) == 5
                   and s["griglia"][("Notizia", "2026-10-12", "N-20261008-02")]["valori"]["Segnale"] == "Migliorativo",
                   "3. il comando griglia ripara la riga e conserva cio' che il validatore aveva scritto nelle altre", out)
        codice, out = b.esegui("valida", "--periodo", "2026-10-12", "--validatore", dec_w["validatore"])
        notizia = next(r for r in b.leggi()["news"] if r["ID_Notizia"] == "N-20261008-02")
        e.verifica(codice == 0 and notizia["Segnale"] == "Migliorativo" and notizia["Validazione"] == "Rettificato",
                   "3. validazione della settimana: la rettifica del segnale di una notizia e' applicata", out + str(notizia))

        # 4. Baseline per il ciclo N+1
        codice, out = b.esegui("baseline", "--uscita", b.cartella / "base_q4.json")
        base_q4 = carica(b.cartella / "base_q4.json")
        e.verifica(codice == 0 and uguale_ai_dati("baseline_2026Q4.json", b.cartella / "base_q4.json"),
                   "4. la baseline dopo il 2026Q3 e' quella usata per run3", out)
        n16 = next((v for v in base_q4["rischi_in_osservazione"] if v["id_rischio"] == "NFR-16"), {})
        e.verifica([n["id_notizia"] for n in n16.get("notizie_a3", [])] == ["N-20261006-01"]
                   and any("NFR-16" in str(x) or "Peggiorativo" in str(x) for x in n16.get("flag_a3", [])),
                   "4. la baseline porta ad A1 la notizia e il flag di A3 su NFR-16 (in osservazione), che run3 porta nel radar",
                   str(n16)[:900])

        # 5. Ciclo 2026Q4 sulla baseline del 2026Q3; prima l'analista scrive le Note del Quadro del 2026Q3 (D-72).
        nota = "Discusse con A7 le valutazioni di NFR-01 e NFR-10: confermate dalle fonti citate."
        with SessioneExcel(b.wb) as sx:
            sx.intervallo_nome("quadroNote").Value = nota
            sx.salva()
        codice, out = b.esegui("trimestrale", "--payload", DATI / "run3_A1_2026Q4.json",
                               "--challenger", DATI / "run_A5_2026Q4.json")
        e.verifica(codice == 0, "5. ciclo 2026Q4 scritto", out)
        sint_q3 = next(r for r in carica_tabella(b, "tblSintesi") if r["Ciclo"] == "2026Q3")
        with SessioneExcel(b.wb, sola_lettura=True) as sx:
            nota_dopo = sx.intervallo_nome("quadroNote").Value
        ciclo_q4 = (b.uscita / "Spiegazioni" / "Ciclo.txt").read_text(encoding="utf-8")
        scartati = carica(DATI / "run3_A1_2026Q4.json")["fenomeni_non_censiti"]
        e.verifica(sint_q3.get("Note_Analista") == nota and not nota_dopo and "archiviate" in out
                   and f"note del ciclo 2026Q3: {nota}" in ciclo_q4,
                   "5. Note dell'analista: archiviate nella riga del 2026Q3 di Sintesi_Cicli, cella del Quadro svuotata, "
                   "riportate nella knowledge di A7", f"{sint_q3.get('Note_Analista')!r} {nota_dopo!r}")
        e.verifica(all(f["fenomeno"] in ciclo_q4 for f in scartati) and file_rischio(b.uscita / "Spiegazioni", "NFR-16")
                   and rischi_nei_posti(b.uscita / "Spiegazioni") == (20, 13)
                   and "gia' coperto da un rischio del registro" in ciclo_q4,
                   "5. knowledge di A7: i fenomeni considerati e non censiti da A1 con il motivo, il file del rischio nuovo",
                   ciclo_q4[-900:])
        oss_txt = ciclo_q4.split("RISCHI IN OSSERVAZIONE")[-1]
        e.verifica("RISCHI IN OSSERVAZIONE" in ciclo_q4 and "- NFR-14 Interruzione di cavi sottomarini" in oss_txt
                   and "ENTRATI E USCITI DAL RADAR NEL CICLO" in ciclo_q4 and "- NFR-16 " in oss_txt.split("ENTRATI E USCITI")[-1]
                   and "Entrato" in oss_txt.split("ENTRATI E USCITI")[-1] and "- NFR-16 " not in oss_txt.split("ENTRATI E USCITI")[0],
                   "5. knowledge di A7: i rischi in osservazione del ciclo (NFR-14 con il perche') e NFR-16 entrato nel radar",
                   oss_txt[:1200])
        e.verifica(sha(excel_q3) == firma_q3 and (b.uscita / "Cicli" / "2026Q4" / "NFR_workbook_2026Q4.xlsx").exists(),
                   "5. l'Excel di output del 2026Q3 resta immutato; il 2026Q4 ha il suo")
        s = b.leggi()
        verifica_integrita(e, s, "5. 2026Q4")
        anag = {r["ID"]: r for r in s["anagrafica"]}
        e.verifica("NFR-16" in anag and anag["NFR-16"]["Owner"] == "Da assegnare" and anag["NFR-16"]["Event_Type"] == "9.11",
                   "5. NFR-16 entra nel radar: in anagrafica, owner da assegnare")
        e.verifica(s["copertura_foglio"] == (13, 13), "5. copertura 13/13: il rischio entrato e' contato", str(s["copertura_foglio"]))
        q4 = {r["ID_Rischio"]: r for r in s["register"] if r["Ciclo"] == "2026Q4"}
        stati = {i: (r["Stato"], r["Movimento"], r["Esito"], r["Validazione"]) for i, r in q4.items()}
        e.verifica(stati["NFR-16"] == ("Radar", "Entrato", "Variato", "Da validare")
                   and q4["NFR-16"]["Motivo_Stato"] == "Prossimita 2 e Probabilita 3: sopra la soglia"
                   and stati["NFR-14"] == ("Osservazione", None, "Variato", "Da validare") and q4["NFR-14"]["Orizzonte_Anni"] == 4
                   and stati["NFR-13"] == ("Osservazione", None, "Confermato", "Da validare")
                   and stati["NFR-15"] == ("Osservazione", None, "Confermato", "Accettato")
                   and q4["NFR-15"]["Periodo_Valutazione"] == "2026Q2"
                   and [f[0] for f in s["fenomeni"]] == ["NFR-14", "NFR-13", "NFR-15"]
                   and s["fenomeni_uscite"] == [("NFR-16", "Entrato")]
                   and sum(1 for r in s["validazione"] if r["Periodo"] == "2026Q4" and r["Oggetto"] == "Rischio") == 15 * 6
                   and "entrati nel radar NFR-16" in out,
                   "5. registro unico: il segnale di NFR-16 si e' verificato, Probabilita e Prossimita salgono di un punto ed "
                   "entra nel radar (Entrato, con KRI e azioni); NFR-14 aggiornato con evidenza nuova resta in osservazione "
                   "(Prossimita 1), NFR-13 confermato, NFR-15 riportato; in validazione i 15 rischi scritti da A1",
                   str(stati) + f" {s['fenomeni']} {s['fenomeni_uscite']}" + out[-500:])
        kri = {k["KRI_ID"]: k for k in s["kri"] if k["Ciclo"] == "2026Q4"}
        e.verifica({"NFR-16-K1", "NFR-16-K2"} <= set(kri) and len({k["KRI_ID"] for k in s["kri"]}) == 27
                   and not [k for k in kri if k.startswith(("NFR-13", "NFR-14", "NFR-15"))],
                   "5. due KRI nuovi per NFR-16 entrato nel radar (K1-K2, D-64), nessuno per chi resta in osservazione; 27 "
                   "indicatori distinti nello storico", str(sorted(kri)))
        e.verifica("NFR-02-K2" not in kri, "5. il KRI uscito nel 2026Q3 non ha righe nei cicli dopo")
        e.verifica(kri["NFR-02-K3"]["Valore_Corrente"] == 0 and kri["NFR-02-K3"]["Ciclo_Definizione"] == "2026Q3",
                   "5. il KRI nato nel 2026Q3 viene riletto nel 2026Q4 senza cambiare data di nascita")
        storia = {k["Ciclo"]: k["Valore_Corrente"] for k in s["kri"] if k["KRI_ID"] == "NFR-01-K1" and k["Valore_Corrente"] is not None}
        valori, elenco = b.andamento("NFR-01-K1")
        e.verifica(len(storia) == 5 and valori == storia,
                   "5. Indicatori, storia di un KRI: i valori di NFR-01-K1 ciclo per ciclo coincidono con lo storico (5 cicli)",
                   f"foglio {valori}\nstorico {storia}")
        valori_k2, _ = b.andamento("NFR-02-K2")
        e.verifica(max(valori_k2) == "2026Q3" and "2026Q4" not in valori_k2,
                   "5. Indicatori, storia di un KRI uscito: la storia si ferma al ciclo in cui e' uscito", str(valori_k2))
        e.verifica(len(elenco) == 27 and len(set(elenco)) == 27 and {"NFR-02-K2", "NFR-02-K3", "NFR-16-K1"} <= set(elenco),
                   "5. elenco a discesa degli Indicatori: i 27 KRI mai definiti, anche usciti, senza doppioni", str(elenco))
        e.verifica(s["presidio"]["9.11"] == "Presidiata", "5. la catena si chiude: 9.11 Employer ora presidiata da NFR-16", str(s["presidio"]))
        verifica_report(e, s, "5. report 2026Q4", commento=carica(DATI / "run3_A1_2026Q4.json")["sintesi"])
        e.verifica(q4["NFR-16"]["Owner"] == "Da assegnare",
                   "5. RiskRegister: owner derivato dall'anagrafica anche per il rischio entrato nel radar")

        # 5b. Radar di Mosca: il foglio calcola lo stesso margine di un calcolo indipendente in Python.
        attesi = mosca_attesa(s, carica_tabella(b, "tblAzioni"))
        trovati = {m[0]: (m[1], round(m[2], 6)) for m in s["mosca"]}
        e.verifica(trovati == attesi, "5b. Radar_Mosca: P x I e margine Z-(X+Y) coincidono con il calcolo indipendente (13 rischi)",
                   f"foglio {trovati}\natteso {attesi}")
        e.verifica(next(a for a in s["anagrafica"] if a["ID"] == "NFR-11")["Anni_Adeguamento"] == 3 and trovati["NFR-11"][1] < 0,
                   "5b. anni di adeguamento dell'anagrafica conservati dalla scrittura e usati come Y (NFR-11: 3 anni, AGIRE ORA)",
                   str(trovati["NFR-11"]))
        e.verifica(all((m[2] < 0) == m[3].startswith("AGIRE ORA") for m in s["mosca"]),
                   "5b. Radar_Mosca: 'AGIRE ORA' esattamente quando X + Y > Z")
        e.verifica(len(s["registro"]) == 13 and set(s["registro"]) == {a["ID"] for a in s["anagrafica"]},
                   "5b. il Registro ha esattamente una riga per rischio dell'anagrafica (13)", str(s["registro"]))
        vigilati = {a["ID"] for a in s["anagrafica"] if a.get("Attenzione_Supervisore") == "Sì"}
        attesi_radar = {rid: ([s["livello"][rid][0]], rid + (" ◆" if rid in vigilati else "")) for rid in s["radar_livello"]}
        e.verifica(vigilati == {"NFR-01", "NFR-02", "NFR-07", "NFR-09"} and s["radar_livello"] == attesi_radar,
                   "5b. Radar_Mosca: un solo cerchio per rischio, del colore del suo livello di allerta (D-63); ◆ "
                   "esattamente per i rischi all'attenzione del supervisore (anagrafica conservata dalla scrittura)",
                   f"vigilati {vigilati}\n{s['radar_livello']}")

        # 7. Scorrimento della finestra: quattro settimane dopo, senza notizie
        vuota = {"settimana": "2026-11-09", "notizie": [], "flag_proposti": [],
                 "sintesi": "Settimana senza notizie rilevanti per il registro dei rischi emergenti."}
        codice, out = b.esegui("settimanale", "--payload", b.scrivi_json("a3_vuota.json", vuota))
        s = b.leggi()
        e.verifica(codice == 0 and s["settimana"] == "2026-11-09" and str(s["badge"]["NFR-01"]).startswith("●"),
                   "7. la finestra scorre: i segnali di ottobre escono, badge NFR-01 torna stabile", out + str(s["badge"]))
        straordinario(e, b)


def gate_copertura(e):
    """6. Gate di copertura: si scrive un ciclo senza NFR-04 aggirando i controlli."""
    run1 = carica(DATI / "run1_A1_2026Q3.json")
    with tempfile.TemporaryDirectory() as tmp:
        b = Banco(tmp)
        prima = sha(b.wb)
        parziale = json.loads(json.dumps(run1))
        parziale["rischi"] = [r for r in parziale["rischi"] if r["id_rischio"] != "NFR-04"]
        with SessioneExcel(b.wb) as sess:
            scr = campo.Scrittore(sess, MAPPA)
            campo.scrivi_trimestrale(scr, parziale, "2026-10-01")
            try:
                campo.verifica_dopo_scrittura(sess, scr, "2026Q3")
                fermato, messaggio = False, "nessun fermo"
            except campo.Fermo as ex:
                fermato, messaggio = "CICLO INCOMPLETO" in str(ex), str(ex)
            copertura = (campo.copertura_python(scr, "2026Q3"), campo.copertura_foglio(sess))
        e.verifica(fermato, "6. gate: un ciclo scritto a meta' e' fermato prima del salvataggio", messaggio)
        e.verifica(copertura[0] == copertura[1] == (12, 11), "6. gate: Python e foglio concordano sul ciclo incompleto (11 su 12)", str(copertura))
        e.verifica(sha(b.wb) == prima, "6. gate: il file non e' stato salvato")


def errore_dopo_salvataggio(e):
    """8. Errore DOPO il salvataggio: l'Excel di output non si puo' scrivere (un file aperto da qualcuno
    nell'archivio; qui un file in sola lettura). Il messaggio non deve dire "non salvato", e la baseline deve essere
    gia' aggiornata, altrimenti il run dopo partirebbe da una baseline vecchia. Poi 8b."""
    with tempfile.TemporaryDirectory() as tmp:
        b = Banco(tmp)
        prima = sha(b.wb)
        bloccato = b.uscita / "Cicli" / "2026Q3" / "NFR_workbook_2026Q3.xlsx"
        bloccato.parent.mkdir(parents=True)
        bloccato.write_bytes(b"vecchio")
        os.chmod(bloccato, stat.S_IREAD)
        try:
            codice, out = b.esegui("trimestrale", "--payload", DATI / "run1_A1_2026Q3.json",
                                   "--challenger", DATI / "run_A5_2026Q3.json")
        finally:
            os.chmod(bloccato, stat.S_IREAD | stat.S_IWRITE)
        e.verifica(codice == 2 and "DOPO IL SALVATAGGIO" in out and "NON rilanciare" in out and "non e' stato salvato" not in out,
                   "8. errore dopo il salvataggio: il messaggio dice che il registro E' scritto e di non rilanciare", out)
        e.verifica(sha(b.wb) != prima and carica(b.uscita / "Baseline_corrente.json")["ciclo_da_valutare"] == "2026Q4",
                   "8. errore dopo il salvataggio: registro scritto e baseline gia' aggiornata al ciclo dopo")

        # 8b. Il validatore rileva il valore di un KRI nato in questo ciclo (mai rilevato):
        #     valore, data e fonte della rilevazione vanno insieme.
        scrivi_decisioni(b.wb, "2026Q3", [{"oggetto": "KRI", "id": "NFR-02-K3", "campo": "Valore_Corrente",
                                           "decisione": "Rettificato", "valore": 2,
                                           "motivazione": "Primo valore disponibile dal registro DORA di ottobre."}])
        codice, out = b.esegui("valida", "--periodo", "2026Q3", "--validatore", "Comitato Rischi")
        k4 = next(k for k in carica_tabella(b, "tblKRI") if k["Ciclo"] == "2026Q3" and k["KRI_ID"] == "NFR-02-K3")
        e.verifica(codice == 0 and k4["Valore_Corrente"] == 2 and k4["Data_Rilevazione"] == "2026-09-30"
                   and str(k4["Fonte_Rilevazione"]).startswith("Rettifica del validatore"),
                   "8b. rettifica del valore di un KRI mai rilevato: data (fine trimestre) e fonte della rilevazione compilate",
                   out + str(k4))


def primo_uso(e):
    """9. Primo uso reale e dismissione di un rischio."""
    run1 = carica(DATI / "run1_A1_2026Q3.json")
    with tempfile.TemporaryDirectory() as tmp:
        b = Banco(tmp)
        b.wb.unlink()                                  # inizializza crea il registro: il file non deve esistere
        codice, out = b.esegui("inizializza", "--ciclo-precedente", "2026Q2", "--settimana", "2026-09-28", "--template", TEMPLATE)
        e.verifica(codice == 0 and b.wb.exists(), "9. inizializza crea il registro vivo dal template", out)
        firma = sha(b.wb)
        codice, out = b.esegui("inizializza", "--ciclo-precedente", "2026Q2", "--settimana", "2026-09-28", "--template", TEMPLATE)
        e.verifica(codice == 1 and "esiste gia'" in out and sha(b.wb) == firma, "9. inizializza non sovrascrive mai un registro esistente", out)
        s = b.leggi()
        e.verifica(not s["errori"] and not s["register"] and not s["kri"] and not s["news"] and not s["validazione"]
                   and not s["anagrafica"] and s["ciclo"] == "2026Q2" and s["settimana"] == "2026-09-28",
                   "9. registro vuoto: nessun dato di esempio, nessun errore di formula, ciclo e settimana impostati",
                   f"errori {s['errori'][:3]} righe {len(s['register'])} {len(s['kri'])} {len(s['news'])} {len(s['validazione'])}")
        from openpyxl import load_workbook
        # read_only tiene il file aperto finche' non si chiude: senza close() Excel
        # non riesce piu' a salvarlo e il comando successivo resta bloccato.
        letto = load_workbook(b.wb, read_only=True)
        guida_rr, significato = [next(letto["RiskRegister"].iter_rows(min_row=r, max_row=r, max_col=1, values_only=True))[0]
                                 for r in (2, 4)]            # riga 3: gruppi di colonne; riga 4: significato
        letto.close()
        e.verifica(str(guida_rr).startswith("CICLO TRIMESTRALE") and str(significato).startswith("A1 · "),
                   "9. la guida in testa e il significato delle colonne restano nel registro vuoto", f"{guida_rr}\n{significato}")
        codice, out = b.esegui("baseline", "--uscita", b.cartella / "base_iniziale.json")
        base = carica(b.cartella / "base_iniziale.json")
        e.verifica(codice == 0 and base["ciclo_da_valutare"] == "2026Q3" and base["rischi"] == [] and base["kri_in_vigore"] == [],
                   "9. baseline del registro vuoto: primo ciclo da valutare 2026Q3, nessun rischio", out)
        primo = json.loads(json.dumps(run1))
        primo["ricalcolo_kri_ciclo_precedente"] = []
        for r in primo["rischi"]:
            r.update(variazioni=[])
            for k in r["kri_proposti"]:
                k["kri_id"] = None
        codice, out = b.esegui("trimestrale", "--payload", b.scrivi_json("primo.json", primo),
                               "--challenger", DATI / "run_A5_2026Q3.json")
        s = b.leggi()
        e.verifica(codice == 0 and s["copertura_foglio"] == (12, 12) and len(s["kri"]) == 24
                   and {k["KRI_ID"] for k in s["kri"] if k["ID_Rischio"] == "NFR-01"} == {"NFR-01-K1", "NFR-01-K2"},
                   "9. primo ciclo (tutti i rischi nuovi) scritto: 12/12, 24 KRI numerati da K1", out)
        verifica_integrita(e, s, "9. primo ciclo")

        codice, out = b.esegui("dismetti", "--rischio", "NFR-99", "--motivazione", "Prova su un rischio inesistente.",
                               "--decisore", "Comitato Rischi")
        e.verifica(codice == 1 and "non e' nell'anagrafica" in out, "9. dismettere un rischio inesistente: fermo", out)
        codice, out = b.esegui("dismetti", "--rischio", "NFR-04", "--motivazione",
                               "Sedi spostate fuori dalle aree a rischio: il rischio non e' piu' pertinente.", "--decisore", "Comitato Rischi")
        s = b.leggi()
        ids = [r["ID"] for r in s["anagrafica"]]
        e.verifica(codice == 0 and "NFR-04" not in ids and len(ids) == 11 and s["anagrafica_posizioni"] == list(range(1, 12)),
                   "9. dismetti: NFR-04 fuori dall'anagrafica, nessuna riga vuota in mezzo", out + str(s["anagrafica_posizioni"]))
        spieg = b.uscita / "Spiegazioni"
        e.verifica(file_rischio(spieg, "NFR-04") is None and rischi_nei_posti(spieg) == (20, 11)
                   and "NFR-04" in (spieg / "Ciclo.txt").read_text(encoding="utf-8").split("RISCHI DISMESSI")[1],
                   "9. knowledge di A7 dopo dismetti: il rischio non e' piu' in nessun posto, i posti restano 20, rischio "
                   "fra i dismessi con il motivo")
        e.verifica(len(s["registro"]) == 11 and s["copertura_foglio"] == (11, 11) and not s["errori"],
                   "9. dismetti: il Registro ha 11 righe (nessun rischio perso), ciclo completo 11/11, zero errori",
                   f"{s['registro']} {s['copertura_foglio']} {s['errori'][:3]}")
        kri04 = [k for k in s["kri"] if k["ID_Rischio"] == "NFR-04"]
        az04 = [a for a in carica_tabella(b, "tblAzioni") if a["ID_Rischio"] == "NFR-04"]
        e.verifica(kri04 and all(k["In_Vigore"] == "No" for k in kri04) and not any(k.startswith("NFR-04") for k in s["kri_correnti"])
                   and az04 and all(a["Stato"] == "Annullata" for a in az04),
                   "9. dismetti: KRI del rischio fuori vigore (non fra i KRI del ciclo negli Indicatori), azioni aperte annullate",
                   f"{[k['In_Vigore'] for k in kri04]} {[a['Stato'] for a in az04]}")
        base = carica(b.uscita / "Baseline_corrente.json")
        e.verifica("NFR-04" not in {r["id_rischio"] for r in base["rischi"]}
                   and not any(k["id_rischio"] == "NFR-04" for k in base["kri_in_vigore"] + base["azioni_aperte"])
                   and any((b.uscita / "Dismissioni").glob("NFR-04_*.json"))
                   and len([r for r in s["register"] if r["ID_Rischio"] == "NFR-04"]) == 1,
                   "9. dismetti: la baseline non lo contiene piu' (ne' KRI ne' azioni), atto archiviato, storia conservata")



if __name__ == "__main__":
    sys.exit(main())
