"""Demo di W1 e W2 nella variante senza Copilot Studio.

Esegue, come farebbe un analista, sulla copia del template NFR_Registro.xlsx:
  W0 reale   raccolta dai feed dell'elenco fonti, alla data di oggi (rete vera)
  W1 2026Q3  (allegato di A1; un A1 con un difetto di integrita' fermato dal
             precontrollo e poi anche da trimestrale, che scrive il messaggio per
             A1; il precontrollo e il ciclo con quello buono, con A5; D-69, D-71)
  Validazione del 2026Q3 (prima un tentativo di Q4 fermato perche' non validato)
  W2 settimana del 12/10/2026, e validazione delle notizie
  W1 2026Q4 senza A5 (facoltativo, D-71), e validazione
  Schede dei rischi del 2026Q4 (senza A6: testi del registro) e PDF del report
  (comando report), poi una correzione manuale del validatore e il PDF rigenerato
e salva in Grafici/ le immagini dei grafici dell'Excel finale.
Le decisioni del validatore (1_Input_agenti/Decisioni_validatore_*.json) sono
simulate: lo script le scrive nella griglia del foglio Validazione (una riga per
rischio, KRI, azione e notizia, D-67) come farebbe una persona; la griglia
compilata del 2026Q3 si salva in Grafici/Validazione_2026Q3.pdf prima di valida.

Gli output degli agenti (cartella 1_Input_agenti) sono SIMULATI da Claude
seguendo i prompt di 02_Agenti: non sono output dell'agente Copilot reale.
Lo script di campo e l'Excel, invece, girano davvero.

Uso:  python esegui_demo.py
"""

import copy
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

QUI = Path(__file__).resolve().parent
PACCHETTO = QUI.parent / "NFR_Emerging_Risk_Agents"
DATI = PACCHETTO / "99_Collaudo" / "dati"
AGENTI = QUI / "1_Input_agenti"
WB = QUI / "NFR_Registro.xlsx"
ARCHIVIO = QUI / "Archivio_Cicli"


def strumento(*argomenti):
    cmd = [sys.executable, str(PACCHETTO / "07_Senza_Studio" / "esegui_ciclo_locale.py"),
           "--workbook", str(WB), "--cartella-uscita", str(ARCHIVIO), *map(str, argomenti)]
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace",
                       env={**os.environ, "PYTHONIOENCODING": "utf-8"})
    print(r.stdout.strip(), f"\n[codice di uscita {r.returncode}]\n")
    return r.returncode


def file_aperti():
    """File della demo precedente aperti in Excel (o altrove): non si possono cancellare."""
    aperti = []
    for f in [WB, *ARCHIVIO.rglob("*.xlsx")] if ARCHIVIO.exists() else [WB]:
        if f.exists() and not f.name.startswith("~$"):     # ~$ = file di lock di Excel
            try:
                with open(f, "r+b"):
                    pass
            except PermissionError:
                aperti.append(f)
    return aperti


def prepara():
    aperti = file_aperti()
    if aperti:
        sys.exit("Demo non avviata: chiudere questi file della demo precedente e rilanciare:\n  "
                 + "\n  ".join(str(f) for f in aperti))
    for p in (ARCHIVIO, QUI / "Grafici", QUI / "News_Inbox"):
        shutil.rmtree(p, ignore_errors=True)
    AGENTI.mkdir(exist_ok=True)
    shutil.copy2(PACCHETTO / "03_Excel" / "NFR_Dashboard_Template.xlsx", WB)
    for sorgente, destinazione in [("run1_A1_2026Q3.json", "A1_2026Q3.json"), ("run_A5_2026Q3.json", "A5_2026Q3.json"),
                                   ("run_A3_2026-10-12.json", "A3_2026-10-12.json"),
                                   ("run3_A1_2026Q4.json", "A1_2026Q4.json"), ("run_A5_2026Q4.json", "A5_2026Q4.json"),
                                   ("decisioni_validatore_2026Q3.json", "Decisioni_validatore_2026Q3.json"),
                                   ("decisioni_validatore_2026-10-12.json", "Decisioni_validatore_2026-10-12.json")]:
        shutil.copy2(DATI / sorgente, AGENTI / destinazione)
    # Un A1 difettoso: un KRI con l'identificativo di un altro rischio (integrita': ferma, D-71) ed evidenza
    # generica (da motivare: da sola non fermerebbe).
    a1 = json.loads((AGENTI / "A1_2026Q3.json").read_text(encoding="utf-8"))
    difettoso = copy.deepcopy(a1)
    difettoso["rischi"][0]["kri_proposti"][0].update(kri_id="NFR-02-K1")
    difettoso["rischi"][2]["variazioni"][0]["evidenza"] = "Il contesto in evoluzione e la maggiore attenzione mediatica sul greenwashing."
    (AGENTI / "A1_2026Q3_difettoso.json").write_text(json.dumps(difettoso, ensure_ascii=False, indent=2), encoding="utf-8")


def raccolta_reale():
    """W0 vero: scarica OGGI i feed dell'elenco fonti (tutti 'da validare')."""
    cmd = [sys.executable, str(PACCHETTO / "07_Senza_Studio" / "raccogli_notizie.py"),
           "--news-inbox", str(QUI / "News_Inbox"), "--anche-da-validare"]
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace",
                       env={**os.environ, "PYTHONIOENCODING": "utf-8"})
    print(r.stdout.strip(), f"\n[codice di uscita {r.returncode}]\n")


def valida(periodo, pdf_griglia=False):
    """Il validatore compila la griglia del foglio Validazione (qui: dal file delle sue decisioni; le righe che non
    tocca valgono come accettate, D-67), poi il comando valida."""
    sys.path.insert(0, str(PACCHETTO / "99_Collaudo"))
    from comune import scrivi_decisioni
    dec = json.loads((AGENTI / f"Decisioni_validatore_{periodo}.json").read_text(encoding="utf-8"))
    print(f"=== Validazione del {periodo}: il validatore scrive {len(dec['decisioni'])} decisioni nella griglia del foglio Validazione")
    scrivi_decisioni(WB, periodo, dec["decisioni"])
    if pdf_griglia:
        griglia_pdf(f"Validazione_{periodo}")
    strumento("valida", "--periodo", periodo, "--validatore", dec["validatore"])


def griglia_pdf(nome):
    """Il foglio Validazione com'e' ora (griglia compilata, Score e Margine ricalcolati) in Grafici/<nome>.pdf."""
    sys.path.insert(0, str(PACCHETTO / "07_Senza_Studio"))
    from excel_com import SessioneExcel
    (QUI / "Grafici").mkdir(exist_ok=True)
    with SessioneExcel(WB, sola_lettura=True) as s:
        s.ricalcola()
        s.foglio("Validazione").ExportAsFixedFormat(0, str(QUI / "Grafici" / f"{nome}.pdf"))


def esporta_grafico(foglio, nome):
    """Un solo grafico, nello stato attuale del registro."""
    sys.path.insert(0, str(PACCHETTO / "07_Senza_Studio"))
    from excel_com import SessioneExcel
    (QUI / "Grafici").mkdir(exist_ok=True)
    with SessioneExcel(WB, sola_lettura=True) as s:
        s.ricalcola()
        s.foglio(foglio).ChartObjects(1).Chart.Export(str(QUI / "Grafici" / f"{nome}.png"))


def grafici():
    sys.path.insert(0, str(PACCHETTO / "07_Senza_Studio"))
    from excel_com import SessioneExcel
    uscita = QUI / "Grafici"
    uscita.mkdir(exist_ok=True)
    with SessioneExcel(WB, sola_lettura=True) as s:
        s.ricalcola()
        for foglio, n, nome in [("Quadro", 1, "Quadro_radar"), ("Classifica", 1, "Classifica"), ("Classifica", 2, "Lente_Mosca"),
                                ("Radar_Mosca", 1, "Radar_Mosca"), ("Delta", 1, "Delta"), ("Storico", 1, "Storico"),
                                ("Notizie", 1, "Notizie")]:
            s.foglio(foglio).ChartObjects(n).Chart.Export(str(uscita / f"{nome}.png"))
        for kri in ("NFR-01-K1", "NFR-02-K2"):      # uno in vigore, uno uscito nel 2026Q3
            s.foglio("Indicatori").Range("N4").Value = kri
            s.ricalcola()
            s.foglio("Indicatori").ChartObjects(1).Chart.Export(str(uscita / f"Indicatori_KRI_{kri}.png"))
    print("Grafici esportati in", uscita)


def correzione_manuale():
    """Dopo la validazione il validatore cambia a mano, nel registro, il presidio dei controlli di NFR-02
    (anagrafica, foglio Parametri): il PDF del report va rigenerato (D-62)."""
    sys.path.insert(0, str(PACCHETTO / "07_Senza_Studio"))
    from excel_com import SessioneExcel
    with SessioneExcel(WB) as s:
        ids = [r[0] for r in s.intervallo_nome("ANA_ID").Value]
        s.intervallo_nome("ANA_Presidio_Controlli").Cells(ids.index("NFR-02") + 1, 1).Value = "Parziale"
        s.salva()
    print("=== Correzione manuale del validatore: presidio dei controlli di NFR-02 da Non verificato a Parziale")


def main():
    prepara()
    print("=== W0 reale: raccolta dai feed dell'elenco fonti, oggi")
    raccolta_reale()
    print("=== W1 2026Q3, passo 2: baseline (input di A1 e A5) e allegato di A1 (baseline, controlli, guida)")
    strumento("baseline")
    shutil.copy2(ARCHIVIO / "Baseline_corrente.json", AGENTI / "Baseline_per_2026Q3.json")
    shutil.copy2(ARCHIVIO / "Input_A1_2026Q3.txt", AGENTI / "Input_A1_2026Q3.txt")
    print("=== W1 2026Q3, passo 5-bis: precontrollo di un A1 difettoso, prima di A5: deve fermarsi con il messaggio per A1")
    strumento("precontrollo", "--payload", AGENTI / "A1_2026Q3_difettoso.json")
    print("=== W1 2026Q3, passo 7 con lo stesso A1 difettoso: anche trimestrale si ferma (stessi controlli) e scrive il messaggio per A1")
    strumento("trimestrale", "--payload", AGENTI / "A1_2026Q3_difettoso.json", "--challenger", AGENTI / "A5_2026Q3.json")
    print("=== W1 2026Q3, passo 5-bis con l'A1 corretto: niente da correggere (razionale scritto prima del 02/10: punti di forma)")
    strumento("precontrollo", "--payload", AGENTI / "A1_2026Q3.json")
    print("=== W1 2026Q3, passo 7 con l'A1 corretto")
    strumento("trimestrale", "--payload", AGENTI / "A1_2026Q3.json", "--challenger", AGENTI / "A5_2026Q3.json")
    print("=== W1 2026Q4 tentato PRIMA di validare il 2026Q3: deve fermarsi")
    strumento("trimestrale", "--payload", AGENTI / "A1_2026Q4.json", "--challenger", AGENTI / "A5_2026Q4.json")
    valida("2026Q3", pdf_griglia=True)
    print("=== W2 settimana del 12/10/2026")
    strumento("settimanale", "--payload", AGENTI / "A3_2026-10-12.json")
    valida("2026-10-12")
    esporta_grafico("Notizie", "Notizie_settimana_2026-10-12")   # L1-03 ancora non presidiata
    shutil.copy2(ARCHIVIO / "Baseline_corrente.json", AGENTI / "Baseline_per_2026Q4.json")
    shutil.copy2(ARCHIVIO / "Input_A1_2026Q4.txt", AGENTI / "Input_A1_2026Q4.txt")
    print("=== W1 2026Q4, precontrollo dell'output di A1 (razionale in parti, azioni nuove)")
    strumento("precontrollo", "--payload", AGENTI / "A1_2026Q4.json")
    print("=== W1 2026Q4, senza A5 (facoltativo dal 06/10, D-71)")
    strumento("trimestrale", "--payload", AGENTI / "A1_2026Q4.json")
    print("=== Validazione del 2026Q4: tutto accettato (griglia non toccata)")
    strumento("valida", "--periodo", "2026Q4", "--validatore", "Comitato Rischi")
    print("=== Schede dei rischi del 2026Q4 (senza A6: testi di A1 dal registro)")
    strumento("schede-input")
    strumento("schede")
    print("=== Report al comitato del 2026Q4")
    strumento("report")
    correzione_manuale()
    print("=== Report rigenerato dopo la correzione, con Registro e Parametri")
    strumento("report", "--con-lavoro")
    grafici()


if __name__ == "__main__":
    main()
