"""Anteprima dello stile proposto per il report al comitato (documento 09).

Uso:
    python Analisi_Architettura/09_genera_anteprima.py

Scrive Analisi_Architettura/09_Anteprima_stile_report.xlsx: un Excel "laterale",
NON collegato al registro, con i dati di esempio del pacchetto (ciclo 2026Q2)
calcolati qui in Python e scritti come valori. Serve solo a decidere cosa piace
prima di cambiare genera_dashboard.py. Grafici nativi di Excel, come nel report
vero: cio' che si vede qui si puo' riprodurre nel generatore.
"""

import sys
import zipfile
from pathlib import Path

from openpyxl import Workbook
from openpyxl.chart import BarChart, LineChart, Reference, ScatterChart, Series
from openpyxl.chart.label import DataLabel, DataLabelList
from openpyxl.chart.layout import Layout, ManualLayout
from openpyxl.chart.series import SeriesLabel
from openpyxl.chart.shapes import GraphicalProperties
from openpyxl.chart.text import RichText, Text
from openpyxl.chart.title import Title
from openpyxl.drawing.line import LineProperties
from openpyxl.drawing.text import CharacterProperties, Paragraph, ParagraphProperties, RegularTextRun
from openpyxl.formatting.rule import DataBarRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

QUI = Path(__file__).resolve().parent
sys.path.insert(0, str(QUI.parent / "NFR_Emerging_Risk_Agents" / "03_Excel"))
import genera_dashboard as g   # noqa: E402  dati di esempio del pacchetto, una sola fonte

USCITA = QUI / "09_Anteprima_stile_report.xlsx"
CICLO, PRECEDENTE = "2026Q2", "2026Q1"

# ---------------------------------------------------------------- tavolozza (proposta 3.1)
BLU_NOTTE, BLU_MEDIO, BLU_CHIARO = "1F3864", "2F5597", "DEEAF6"
ROSSO, AMBRA, GRIGIO, BLU_DIM = "C00000", "FFC000", "A6A6A6", "2E75B6"
TESTO, TESTO_TENUE, FONDO_TENUE = "262626", "595959", "F2F2F2"
ROSSO_TENUE, AMBRA_TENUE, VERDE_TENUE = "FBE5E5", "FFF2CC", "E2EFDA"
RIEMPIMENTO_CERCHIO = "9DC3E7"      # colore unico: il post-processo gli aggiunge la trasparenza
fill = lambda c: PatternFill("solid", fgColor=c)
bordo_sottile = Side(style="thin", color="D9D9D9")


# ---------------------------------------------------------------- dati di esempio calcolati
def dati():
    anni_z = {5: 0, 4: 0.5, 3: 1.5, 2: 2.5, 1: 4}
    pesi = dict(sev=0.30, vel=0.15, pro=0.15, gap=0.20, prob=0.20)
    anag = {r[0]: r for r in g.ANAGRAFICA}
    rischi = []
    for rid, (sev, vel, pro, gap, conf, esito, var) in g.STORIA[CICLO].items():
        prob = g.PROBABILITA[rid]
        score = round(pesi["sev"] * sev + pesi["vel"] * vel + pesi["pro"] * pro + pesi["gap"] * gap + pesi["prob"] * prob, 2)
        prima = g.STORIA[PRECEDENTE].get(rid)
        score_prima = (round(pesi["sev"] * prima[0] + pesi["vel"] * prima[1] + pesi["pro"] * prima[2]
                             + pesi["gap"] * prima[3] + pesi["prob"] * prob, 2) if prima else None)
        mesi = [int(a[4].split()[0]) for a in g.AZIONI_ESEMPIO if a[0] == rid and a[6] != "Respinta"]
        y = max(max(mesi) / 12 if mesi else 1, g.ANNI_ADEGUAMENTO.get(rid, 0))
        z, x = anni_z[pro], 0.25
        margine = round(z - (x + y), 2)
        m1 = round(margine, 1)
        urgenza = ("AGIRE ORA" if margine < 0 else "Entro l'anno" if margine < 1
                   else f"Margine {m1:g} {'anno' if m1 == 1 else 'anni'}".replace(".", ","))
        _, nome, et, drv, owner, descr = anag[rid]
        rischi.append(dict(id=rid, nome=nome, et=et, drv=", ".join(drv), owner=owner, descr=descr, sev=sev, vel=vel,
                           pro=pro, gap=gap, prob=prob, conf=conf, esito=esito, var=var, score=score,
                           prima=score_prima, delta=None if score_prima is None else round(score - score_prima, 2),
                           x=x, y=y, z=z, margine=margine, urgenza=urgenza,
                           vigilanza=g.ATTENZIONE_SUPERVISORE.get(rid) == "Sì", razionale=g.RAZIONALI[rid]))
    rischi.sort(key=lambda r: -r["score"])
    kri = []
    for kid, rid, nome, unita, fonte, att, all_, cdef, valori in g.KRI_ESEMPIO:
        v = valori[2]
        stato = "Non rilevato" if v is None else "Rosso" if v >= all_ else "Ambra" if v >= att else "Verde"
        kri.append(dict(id=kid, rischio=rid, nome=nome, unita=unita, att=att, all=all_, valore=v, stato=stato))
    return rischi, kri


# ---------------------------------------------------------------- utilita' di stile
def cp(sz=900, b=False, colore=TESTO):
    return CharacterProperties(sz=sz, b=b, solidFill=colore, latin=None)


def testo_rich(sz=900, b=False, colore=TESTO):
    c = cp(sz, b, colore)
    return RichText(p=[Paragraph(pPr=ParagraphProperties(defRPr=c), endParaRPr=c)])


def titolo_grafico(testo, sz=1200):
    c = cp(sz, True, BLU_NOTTE)
    return Title(tx=Text(rich=RichText(p=[Paragraph(pPr=ParagraphProperties(defRPr=c), r=[RegularTextRun(rPr=c, t=testo)])])),
                 overlay=False)


def pulisci(grafico):
    """Niente bordo esterno, griglia grigio chiaro, testi 9 pt."""
    grafico.graphical_properties = GraphicalProperties(ln=LineProperties(noFill=True))
    for asse in (grafico.x_axis, grafico.y_axis):
        asse.delete = False
        asse.txPr = testo_rich(900, colore=TESTO_TENUE)
        asse.graphicalProperties = GraphicalProperties(ln=LineProperties(solidFill="D9D9D9"))
    if grafico.y_axis.majorGridlines is not None:
        grafico.y_axis.majorGridlines.spPr = GraphicalProperties(ln=LineProperties(solidFill="EDEDED"))
    if grafico.legend is not None:
        grafico.legend.position = "b"
        grafico.legend.overlay = False
        grafico.legend.txPr = testo_rich(900, colore=TESTO_TENUE)


def etichette_valore(serie, formato="0.00", posizione="outEnd", colore=TESTO):
    serie.dLbls = DataLabelList(showVal=True, showSerName=False, showCatName=False, showLegendKey=False,
                                showPercent=False, dLblPos=posizione)
    serie.dLbls.numFmt = formato
    serie.dLbls.txPr = testo_rich(900, True, colore)


def fascia(ws, ultima_col, sottotitolo):
    """Fascia di intestazione (proposta 3.1): titolo del report, ciclo e stato."""
    fine = get_column_letter(ultima_col)
    ws.merge_cells(f"A1:{fine}1")
    ws.merge_cells(f"A2:{fine}2")
    ws["A1"] = "Rischi non finanziari emergenti — " + sottotitolo
    ws["A1"].font = Font(name="Calibri", size=16, bold=True, color="FFFFFF")
    ws["A1"].fill = fill(BLU_NOTTE)
    ws["A1"].alignment = Alignment(vertical="center", indent=1)
    ws["A2"] = "Ciclo 2026Q2  ·  dati al 30/06/2026  ·  ciclo validato il 15/07/2026 (Comitato Rischi)  ·  Uso interno"
    ws["A2"].font = Font(size=10, color="FFFFFF")
    ws["A2"].fill = fill(BLU_MEDIO)
    ws["A2"].alignment = Alignment(vertical="center", indent=1)
    ws.row_dimensions[1].height = 30
    ws.row_dimensions[2].height = 18
    ws.sheet_view.showGridLines = False


def sezione(ws, cella_da, cella_a, testo):
    ws.merge_cells(f"{cella_da}:{cella_a}")
    c = ws[cella_da]
    c.value = testo
    c.font = Font(size=12, bold=True, color=BLU_NOTTE)
    c.border = Border(bottom=Side(style="medium", color=BLU_NOTTE))
    for riga in ws[f"{cella_da}:{cella_a}"]:
        for x in riga:
            x.border = Border(bottom=Side(style="medium", color=BLU_NOTTE))


def chip_urgenza(c, urgenza):
    colori = {"AGIRE ORA": (ROSSO, "FFFFFF"), "Entro l'anno": (AMBRA, TESTO)}
    fondo, testo = colori.get(urgenza, ("D9D9D9", TESTO))
    c.value = urgenza
    c.fill = fill(fondo)
    c.font = Font(size=9, bold=True, color=testo)
    c.alignment = Alignment(horizontal="center", vertical="center")


def freccia(delta):
    if delta is None:
        return "nuovo"
    # Mai un testo che inizia con "=": openpyxl lo scriverebbe come formula (file illeggibile per Excel).
    return ("▲ +" if delta > 0 else "▼ " if delta < 0 else "● ") + f"{delta:.2f}".replace(".", ",").replace("-", "−")


def stampa(ws, orizzontale=True):
    ws.page_setup.orientation = "landscape" if orizzontale else "portrait"
    ws.page_setup.paperSize = ws.PAPERSIZE_A4
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 1
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.page_margins.left = ws.page_margins.right = 0.4
    ws.oddFooter.left.text = "Anteprima di stile — dati di esempio"
    ws.oddFooter.right.text = "Pagina &P di &N"


def fascia_pxi(v):
    return ROSSO_TENUE if v >= 15 else AMBRA_TENUE if v >= 8 else VERDE_TENUE


# ---------------------------------------------------------------- fogli
def foglio_valuta(wb):
    ws = wb.active
    ws.title = "Come valutare"
    fascia(ws, 6, "anteprima dello stile del report")
    ws.column_dimensions["A"].width = 5
    ws.column_dimensions["B"].width = 44
    ws.column_dimensions["C"].width = 14
    ws.column_dimensions["D"].width = 62
    ws.column_dimensions["E"].width = 18
    ws.column_dimensions["F"].width = 40
    ws["A4"] = ("Questo file NON e' il registro: e' un'anteprima con i dati di esempio del pacchetto (ciclo 2026Q2), "
                "per decidere cosa ti piace prima di cambiare il report vero. Tutto e' fatto con celle e grafici nativi di "
                "Excel, quindi riproducibile nel generatore. Confronta con i fogli Sintesi..Metodologia di "
                "03_Excel/NFR_Dashboard_Template.xlsx. Proposta completa: Analisi_Architettura/09_Proposta_grafica_report.md.")
    ws.merge_cells("A4:F4")
    ws["A4"].alignment = Alignment(wrap_text=True, vertical="top")
    ws.row_dimensions[4].height = 48
    ws["A5"] = "Per ogni elemento scegli in colonna E (Sì / No / Sì, con modifiche) e scrivi in F cosa cambieresti."
    ws["A5"].font = Font(italic=True, color=TESTO_TENUE)
    intest = ["#", "Elemento", "Foglio", "Cosa guardare", "Ti piace?", "Nota"]
    for j, t in enumerate(intest, start=1):
        c = ws.cell(row=7, column=j, value=t)
        c.font = Font(bold=True, color="FFFFFF")
        c.fill = fill(BLU_NOTTE)
    voci = [
        ("Fascia di intestazione", "tutti", "Titolo su fascia blu, ciclo, data e stato della validazione in ogni pagina."),
        ("Riquadri a numeri grandi", "Sintesi", "Cinque numeri leggibili in 10 secondi; rosso tenue solo se richiedono attenzione."),
        ("Primi cinque con barra nella cella", "Sintesi", "Score con barra 0-5 nella cella, variazione con freccia, urgenza come etichetta colorata."),
        ("Mini matrice P x I", "Sintesi", "Dove stanno i rischi per probabilita' e impatto, accanto alle priorita'."),
        ("Matrice P x I grande", "Matrice", "Griglia 5 x 5 con gli ID, tre fasce di colore; ◆ = tema all'attenzione del supervisore."),
        ("Titoli che dicono il messaggio", "Classifica, Delta", "\"2 rischi da affrontare subito\" invece di \"Classifica per score\"."),
        ("Barre con valore e freccia", "Classifica", "Score scritto in fondo alla barra; freccia della variazione nell'etichetta."),
        ("Lente di Mosca ordinata per ritardo", "Classifica", "Dal piu' in ritardo; margine nell'etichetta; Y rossa se X + Y supera Z."),
        ("Radar: nomi dei settori, legenda delle aree, trasparenza", "Radar", "Settori con il nome; tre cerchi di riferimento; cerchi semitrasparenti; anello di 1 anno ambra tratteggiato."),
        ("Delta rosso e blu, ordinato", "Delta", "Aumenti rossi, diminuzioni blu (leggibile anche da chi confonde rosso e verde), valore scritto."),
        ("Scheda del rischio", "Scheda", "Fascia con score e urgenza, punteggi come celle colorate, KRI con semaforo."),
        ("Tavolozza e caratteri", "tutti", "Blu notte, rosso, ambra, grigio; Calibri; niente bordi ai grafici."),
    ]
    dv = DataValidation(type="list", formula1='"Sì,No,Sì con modifiche"', allow_blank=True)
    ws.add_data_validation(dv)
    for i, (el, foglio, cosa) in enumerate(voci, start=1):
        r = 7 + i
        for j, v in enumerate([i, el, foglio, cosa, None, None], start=1):
            c = ws.cell(row=r, column=j, value=v)
            c.alignment = Alignment(wrap_text=True, vertical="top")
            c.border = Border(bottom=bordo_sottile)
        ws.cell(row=r, column=5).fill = fill(AMBRA_TENUE)
        ws.cell(row=r, column=6).fill = fill(AMBRA_TENUE)
        dv.add(f"E{r}")
        ws.row_dimensions[r].height = 30
    stampa(ws)


def foglio_sintesi(wb, rischi, kri):
    ws = wb.create_sheet("Sintesi")
    fascia(ws, 15, "Sintesi per il comitato")
    for j in range(1, 16):
        ws.column_dimensions[get_column_letter(j)].width = 10.5
    ws.column_dimensions["I"].width = 3
    agire = [r for r in rischi if r["urgenza"] == "AGIRE ORA"]
    variati = [r for r in rischi if r["esito"] == "Variato"]
    nuovi = [r for r in rischi if r["esito"] == "Nuovo"]
    rossi = [k for k in kri if k["stato"] == "Rosso"]
    riquadri = [
        ("Rischi valutati", str(len(rischi)), f"su {len(rischi)} in anagrafica · completo", FONDO_TENUE, BLU_NOTTE),
        ("Da affrontare subito", str(len(agire)), "X + Y > Z: " + ", ".join(r["id"] for r in agire), ROSSO_TENUE, ROSSO),
        ("Variati · nuovi", f"{len(variati)} · {len(nuovi)}", "rispetto al " + PRECEDENTE, FONDO_TENUE, BLU_NOTTE),
        ("KRI in rosso", str(len(rossi)), f"su {len(kri)} in vigore", ROSSO_TENUE if rossi else FONDO_TENUE, ROSSO if rossi else BLU_NOTTE),
        ("Validazione", "✓", "validato il 15/07/2026", VERDE_TENUE, "375623"),
    ]
    colonne = [(1, 3), (4, 6), (7, 9), (10, 12), (13, 15)]
    for (da, a), (didascalia, numero, sotto, fondo, colore) in zip(colonne, riquadri):
        l1, l2 = get_column_letter(da), get_column_letter(a)
        for r, testo, font in [(4, didascalia, Font(size=9, bold=True, color=TESTO_TENUE)),
                               (5, numero, Font(size=28, bold=True, color=colore)),
                               (6, sotto, Font(size=9, color=TESTO_TENUE))]:
            ws.merge_cells(f"{l1}{r}:{l2}{r}")
            c = ws[f"{l1}{r}"]
            c.value, c.font = testo, font
            c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
            for x in range(da, a + 1):
                ws.cell(row=r, column=x).fill = fill(fondo)
    ws.row_dimensions[5].height = 42
    ws.row_dimensions[6].height = 26
    # Colonne di separazione fra i riquadri: bordo bianco spesso a destra.
    for da, a in colonne[:-1]:
        for r in (4, 5, 6):
            ws.cell(row=r, column=a).border = Border(right=Side(style="thick", color="FFFFFF"))

    sezione(ws, "A8", "H8", "Priorita' — primi cinque per score composito")
    sezione(ws, "J8", "O8", "Probabilita x Severity")
    for j, t in [(1, "#"), (2, "Rischio"), (6, "Score"), (7, "Variazione"), (8, "Urgenza")]:
        c = ws.cell(row=9, column=j, value=t)
        c.font = Font(size=9, bold=True, color=TESTO_TENUE)
    ws.merge_cells("B9:E9")
    for k, r in enumerate(rischi[:5], start=1):
        riga = 9 + k
        ws.cell(row=riga, column=1, value=k).font = Font(bold=True, color=BLU_NOTTE)
        ws.merge_cells(f"B{riga}:E{riga}")
        c = ws.cell(row=riga, column=2, value=f"{r['id']}  {r['nome']}" + ("  ◆" if r["vigilanza"] else ""))
        c.alignment = Alignment(wrap_text=True, vertical="center")
        c.font = Font(size=10)
        s = ws.cell(row=riga, column=6, value=r["score"])
        s.number_format = "0.00"
        s.font = Font(bold=True)
        d = ws.cell(row=riga, column=7, value=freccia(r["delta"]))
        d.font = Font(size=10, color=ROSSO if (r["delta"] or 0) > 0 else BLU_DIM if (r["delta"] or 0) < 0 else TESTO_TENUE)
        chip_urgenza(ws.cell(row=riga, column=8), r["urgenza"])
        ws.row_dimensions[riga].height = 30
        for j in range(1, 9):
            ws.cell(row=riga, column=j).border = Border(bottom=bordo_sottile)
            if j != 8:
                ws.cell(row=riga, column=j).alignment = Alignment(vertical="center", wrap_text=j == 2)
    ws.conditional_formatting.add("F10:F14", DataBarRule(start_type="num", start_value=0, end_type="num", end_value=5,
                                                         color="8EA9DB", showValue=True))
    ws["A15"] = "◆ = tema all'attenzione del supervisore (BCE, EBA, Banca d'Italia). Score 1-5, 5 = peggiore; barra su scala fissa 0-5."
    ws["A15"].font = Font(size=8, italic=True, color=TESTO_TENUE)

    # Mini matrice: righe Probabilita 5..1, colonne Severity 1..5.
    ws["J9"] = "P \\ S"
    ws["J9"].font = Font(size=8, bold=True, color=TESTO_TENUE)
    for s in range(1, 6):
        c = ws.cell(row=9, column=10 + s, value=s)
        c.font = Font(size=8, bold=True, color=TESTO_TENUE)
        c.alignment = Alignment(horizontal="center")
    for i, p in enumerate(range(5, 0, -1)):
        riga = 10 + i
        c = ws.cell(row=riga, column=10, value=p)
        c.font = Font(size=8, bold=True, color=TESTO_TENUE)
        c.alignment = Alignment(horizontal="center", vertical="center")
        for s in range(1, 6):
            ids = [r["id"][4:] for r in rischi if r["prob"] == p and r["sev"] == s]
            c = ws.cell(row=riga, column=10 + s, value=" ".join(ids) or None)
            c.fill = fill(fascia_pxi(p * s))
            c.font = Font(size=8, bold=True)
            c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
            c.border = Border(left=Side(style="thin", color="FFFFFF"), right=Side(style="thin", color="FFFFFF"),
                              top=Side(style="thin", color="FFFFFF"), bottom=Side(style="thin", color="FFFFFF"))
    ws["J15"] = "Numeri = NFR-nn. Verde P x I fino a 6, ambra 8-12, rosso da 15."
    ws["J15"].font = Font(size=8, italic=True, color=TESTO_TENUE)

    commento, a5, _ = g.SINTESI_ESEMPIO[CICLO]
    blocchi = [(17, "Messaggio dell'analisi (agente A1, scritto prima della validazione)", commento, 70),
               (20, "Controllo indipendente (agente A5)", a5 + " Osservazioni non bloccanti: 1.", 20),
               (23, "Dopo il commento", "Il validatore ha applicato 3 rettifiche o respingimenti: numeri e grafici di questo "
                                     "report sono quelli validati e prevalgono sul commento.", 20)]
    for r, titolo, testo, h in blocchi:
        sezione(ws, f"A{r}", f"O{r}", titolo)
        ws.merge_cells(f"A{r + 1}:O{r + 1}")
        c = ws[f"A{r + 1}"]
        c.value = testo
        c.alignment = Alignment(wrap_text=True, vertical="top")
        c.font = Font(size=10.5 if r == 17 else 10)
        if r == 23:
            c.fill = fill(AMBRA_TENUE)
        ws.row_dimensions[r + 1].height = h
    ws.merge_cells("A26:O26")
    ws["A26"] = "Limiti: " + g.leggi_limiti()
    ws["A26"].font = Font(size=8, italic=True, color=TESTO_TENUE)
    ws["A26"].alignment = Alignment(wrap_text=True, vertical="top")
    ws.row_dimensions[26].height = 36
    stampa(ws)


def foglio_matrice(wb, rischi):
    ws = wb.create_sheet("Matrice")
    fascia(ws, 8, "gravita': Probabilita x Severity")
    ws.column_dimensions["A"].width = 16
    ws.column_dimensions["B"].width = 6
    for j in range(3, 8):
        ws.column_dimensions[get_column_letter(j)].width = 24
    ws["A4"] = ("Ogni rischio sta nella cella della sua Probabilita (righe) e Severity (colonne), valori validati del ciclo. "
                "Colore = P x I: verde fino a 6, ambra da 8 a 12, rosso da 15. ◆ = tema all'attenzione del supervisore. "
                "La gravita' non dice quando agire: per quello c'e' il Radar di Mosca.")
    ws.merge_cells("A4:G4")
    ws["A4"].alignment = Alignment(wrap_text=True, vertical="top")
    ws["A4"].font = Font(size=10, color=TESTO_TENUE)
    ws.row_dimensions[4].height = 32
    descr_p = {5: "Quasi certa", 4: "Probabile", 3: "Possibile", 2: "Improbabile", 1: "Rara"}
    descr_s = {1: "Trascurabile", 2: "Contenuto", 3: "Rilevante", 4: "Grave", 5: "Critico"}
    ws["A6"] = "Probabilita"
    ws["A6"].font = Font(bold=True, color=BLU_NOTTE)
    for i, p in enumerate(range(5, 0, -1)):
        r = 7 + i
        ws.cell(row=r, column=1, value=descr_p[p]).font = Font(size=9, color=TESTO_TENUE)
        c = ws.cell(row=r, column=2, value=p)
        c.font = Font(bold=True, color=BLU_NOTTE)
        c.alignment = Alignment(horizontal="center", vertical="center")
        ws.cell(row=r, column=1).alignment = Alignment(vertical="center", horizontal="right")
        for s in range(1, 6):
            voci = [f"{r_['id']}{' ◆' if r_['vigilanza'] else ''}" for r_ in rischi if r_["prob"] == p and r_["sev"] == s]
            # Due per riga: una cella affollata resta leggibile senza allungare la matrice.
            testo = "\n".join("   ".join(voci[i:i + 2]) for i in range(0, len(voci), 2))
            c = ws.cell(row=r, column=2 + s, value=testo or None)
            c.fill = fill(fascia_pxi(p * s))
            c.font = Font(size=11, bold=True, color=TESTO)
            c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
            bianco = Side(style="medium", color="FFFFFF")
            c.border = Border(left=bianco, right=bianco, top=bianco, bottom=bianco)
        ws.row_dimensions[r].height = 62
    for s in range(1, 6):
        c = ws.cell(row=12, column=2 + s, value=s)
        c.font = Font(bold=True, color=BLU_NOTTE)
        c.alignment = Alignment(horizontal="center")
        d = ws.cell(row=13, column=2 + s, value=descr_s[s])
        d.font = Font(size=9, color=TESTO_TENUE)
        d.alignment = Alignment(horizontal="center")
    ws["E14"] = "Severity"
    ws["E14"].font = Font(bold=True, color=BLU_NOTTE)
    ws["E14"].alignment = Alignment(horizontal="center")
    conta = {"rosso": sum(r["prob"] * r["sev"] >= 15 for r in rischi),
             "ambra": sum(8 <= r["prob"] * r["sev"] < 15 for r in rischi),
             "verde": sum(r["prob"] * r["sev"] < 8 for r in rischi)}
    ws["A16"] = (f"Nel ciclo, rischi per fascia: rossa {conta['rosso']}, ambra {conta['ambra']}, verde {conta['verde']}.")
    ws["A16"].font = Font(bold=True, color=BLU_NOTTE)
    stampa(ws)


def foglio_classifica(wb, rischi):
    ws = wb.create_sheet("Classifica")
    fascia(ws, 20, "classifica e lente di Mosca")
    # Dati di appoggio (a destra, piccoli e grigi): li leggono i grafici.
    ws["W3"] = "Dati dei grafici (appoggio)"
    ws["W3"].font = Font(size=8, italic=True, color=GRIGIO)
    intest = ["Etichetta", "Agire ora", "Entro l'anno", "Con margine", "Etichetta lente", "X", "Y entro Z", "Y oltre Z", "Z"]
    for j, t in enumerate(intest):
        ws.cell(row=4, column=23 + j, value=t).font = Font(size=8, color=GRIGIO)
    n = len(rischi)
    for i, r in enumerate(rischi):
        riga = 5 + i
        etichetta = f"{r['id']} {freccia(r['delta']).split(' ')[0]}  {r['nome'][:34]}{'…' if len(r['nome']) > 34 else ''}"
        ws.cell(row=riga, column=23, value=etichetta)
        col = {"AGIRE ORA": 24, "Entro l'anno": 25}.get(r["urgenza"], 26)
        ws.cell(row=riga, column=col, value=r["score"]).number_format = "0.00"
    lente = sorted(rischi, key=lambda r: r["margine"])
    for i, r in enumerate(lente):
        riga = 5 + i
        m = f"{r['margine']:+.2f}".replace(".", ",").replace("-", "−")
        ws.cell(row=riga, column=27, value=f"{r['id']} ({m})")
        ws.cell(row=riga, column=28, value=r["x"])
        sfora = r["x"] + r["y"] > r["z"]
        ws.cell(row=riga, column=30 if sfora else 29, value=r["y"])
        ws.cell(row=riga, column=31, value=r["z"])
    for j in range(23, 32):
        for i in range(n + 1):
            ws.cell(row=4 + i, column=j).font = Font(size=8, color=GRIGIO)
    ultima = 4 + n

    agire = [r["id"] for r in rischi if r["urgenza"] == "AGIRE ORA"]
    barre = BarChart()
    barre.type = "bar"
    barre.grouping = "clustered"
    barre.overlap = 100
    barre.gapWidth = 45
    barre.title = titolo_grafico(f"{len(agire)} rischi da affrontare subito: {' e '.join(agire)}")
    for col, colore in ((24, ROSSO), (25, AMBRA), (26, GRIGIO)):
        barre.add_data(Reference(ws, min_col=col, min_row=4, max_row=ultima), titles_from_data=True)
        s = barre.series[-1]
        s.graphicalProperties.solidFill = colore
        s.graphicalProperties.line.noFill = True
        etichette_valore(s)
    barre.set_categories(Reference(ws, min_col=23, min_row=5, max_row=ultima))
    barre.x_axis.scaling.orientation = "maxMin"
    barre.y_axis.scaling.min, barre.y_axis.scaling.max, barre.y_axis.majorUnit = 0, 5, 1
    barre.varyColors = False
    pulisci(barre)
    barre.x_axis.graphicalProperties = GraphicalProperties(ln=LineProperties(noFill=True))
    barre.height, barre.width = 12.5, 15.5
    ws.add_chart(barre, "A4")

    col = BarChart()
    col.type = "col"
    col.grouping = "stacked"
    col.overlap = 100
    col.gapWidth = 60
    col.title = titolo_grafico("Lente di Mosca: chi e' in ritardo, e di quanto (anni)")
    for c_, colore in ((28, "BFBFBF"), (29, "ED7D31"), (30, ROSSO)):
        col.add_data(Reference(ws, min_col=c_, min_row=4, max_row=ultima), titles_from_data=True)
        s = col.series[-1]
        s.graphicalProperties.solidFill = colore
        s.graphicalProperties.line.noFill = True
    col.series[0].tx = SeriesLabel(v="X: decidere e avviare")
    col.series[1].tx = SeriesLabel(v="Y: mitigare, entro Z")
    col.series[2].tx = SeriesLabel(v="Y: mitigare, OLTRE Z")
    col.set_categories(Reference(ws, min_col=27, min_row=5, max_row=ultima))
    rombi = LineChart()
    rombi.add_data(Reference(ws, min_col=31, min_row=4, max_row=ultima), titles_from_data=True)
    s = rombi.series[0]
    s.tx = SeriesLabel(v="Z: tempo disponibile")
    s.graphicalProperties.line.noFill = True
    s.marker.symbol = "diamond"
    s.marker.size = 10
    s.marker.graphicalProperties = GraphicalProperties(solidFill=BLU_NOTTE)
    s.marker.graphicalProperties.line.solidFill = BLU_NOTTE
    col.y_axis.scaling.min = 0
    col.varyColors = False
    pulisci(col)
    col += rombi
    col.height, col.width = 12.5, 15.5
    ws.add_chart(col, "K4")
    ws["A30"] = ("Sinistra: un rischio per barra, colore = urgenza (rosso agire ora, ambra entro l'anno, grigio con margine), "
                 "freccia = variazione sul ciclo prima. Destra: colonna = tempo necessario X + Y, rombo = tempo disponibile Z; "
                 "la parte rossa sfora. Ordinata dal piu' in ritardo; tra parentesi il margine Z - (X + Y).")
    ws.merge_cells("A30:T30")
    ws["A30"].alignment = Alignment(wrap_text=True, vertical="top")
    ws["A30"].font = Font(size=9, italic=True, color=TESTO_TENUE)
    ws.row_dimensions[30].height = 30
    for j in range(1, 21):
        ws.column_dimensions[get_column_letter(j)].width = 8.5
    stampa(ws)
    ws.print_area = "A1:T30"


def foglio_radar(wb, rischi):
    import math
    ws = wb.create_sheet("Radar")
    fascia(ws, 16, "Radar di Mosca: quanto presto agire")
    settori = g.TASSONOMIA
    k = len(settori)
    # Appoggio in colonne a destra (Q in poi).
    base = 20
    col = lambda n: base + n
    r0 = 5
    ws.cell(row=3, column=base, value="Dati del grafico (appoggio)").font = Font(size=8, italic=True, color=GRIGIO)
    # Anelli: 73 punti per anello, 4 anelli (colonne x,y).
    anelli = [(0, "Mosca: dentro = AGIRE ORA", ROSSO, 28575, None), (1, "1 anno", "BF8F00", 15875, "dash"),
              (2, "2 anni", "BFBFBF", 9525, None), (3, "3 anni", "BFBFBF", 9525, None)]
    for a, (m, _, _, _, _) in enumerate(anelli):
        for p in range(73):
            ang = 2 * math.pi * p / 72
            ws.cell(row=r0 + p, column=col(2 * a), value=round((m + 2) * math.sin(ang), 4))
            ws.cell(row=r0 + p, column=col(2 * a) + 1, value=round((m + 2) * math.cos(ang), 4))
    # Raggi dei settori: colonne 8,9 (due punti per settore).
    for s in range(k):
        ang = 2 * math.pi * s / k
        ws.cell(row=r0 + 2 * s, column=col(8), value=0)
        ws.cell(row=r0 + 2 * s, column=col(9), value=0)
        ws.cell(row=r0 + 2 * s + 1, column=col(8), value=round(6.3 * math.sin(ang), 4))
        ws.cell(row=r0 + 2 * s + 1, column=col(9), value=round(6.3 * math.cos(ang), 4))
    # Etichette dei settori: colonne 10 (nome), 11, 12.
    for s, (cod, nome) in enumerate(settori):
        ang = 2 * math.pi * (s + 0.5) / k
        nome_corto = {"L1-03": "Impiego e sicurezza", "L1-04": "Clientela e prodotti", "L1-06": "Interruzione e sistemi",
                      "L1-07": "Processi"}.get(cod, nome)
        ws.cell(row=r0 + s, column=col(10), value=f"{cod}\n{nome_corto}")
        ws.cell(row=r0 + s, column=col(11), value=round(6.95 * math.sin(ang), 4))
        ws.cell(row=r0 + s, column=col(12), value=round(6.95 * math.cos(ang), 4))
    # Rischi: colonne 13 (ID), 14 x, 15 y.
    per_settore = {}
    for r in rischi:
        per_settore.setdefault(r["et"], []).append(r)
    posizioni = []
    for s, (cod, _) in enumerate(settori):
        gruppo = per_settore.get(cod, [])
        for n_, r in enumerate(gruppo):
            ang = 2 * math.pi * (s + (n_ + 0.5) / len(gruppo)) / k
            raggio = max(0.6, min(6, r["margine"] + 2))
            posizioni.append((r, round(raggio * math.sin(ang), 4), round(raggio * math.cos(ang), 4)))
    for i, (r, x, y) in enumerate(posizioni):
        ws.cell(row=r0 + i, column=col(13), value=r["id"])
        ws.cell(row=r0 + i, column=col(14), value=x)
        ws.cell(row=r0 + i, column=col(15), value=y)
    # Legenda delle aree: colonne 16 (etichetta), 17 x, 18 y.
    for i, v in enumerate((4, 12, 25)):
        ws.cell(row=r0 + i, column=col(16), value=f"{v}")
        ws.cell(row=r0 + i, column=col(17), value=(3.5, 4.8, 6.5)[i])
        ws.cell(row=r0 + i, column=col(18), value=-6.6)
    for c_ in range(base, col(19)):
        ws.column_dimensions[get_column_letter(c_)].hidden = True

    ch = ScatterChart()
    ch.scatterStyle = "lineMarker"
    ch.varyColors = False
    ch.visible_cells_only = False

    def punti(r_da, r_a, cx, cy, nome):
        s = Series(Reference(ws, min_col=cy, min_row=r_da, max_row=r_a), xvalues=Reference(ws, min_col=cx, min_row=r_da, max_row=r_a))
        s.tx = SeriesLabel(v=nome) if not str(nome).startswith("=") else SeriesLabel(strRef=None)
        return s

    def etichetta_nome(s, pos="ctr", indice=None, sz=900, b=True, colore=TESTO):
        base_l = dict(showSerName=True, showVal=False, showCatName=False, showLegendKey=False, showPercent=False, dLblPos=pos)
        if indice is None:
            s.dLbls = DataLabelList(**base_l)
        else:
            s.dLbls = DataLabelList(dLbl=[DataLabel(idx=indice, txPr=testo_rich(sz, b, colore), **base_l)],
                                    showVal=False, showSerName=False, showCatName=False, showLegendKey=False, showPercent=False)
        s.dLbls.txPr = testo_rich(sz, b, colore)

    for a, (m, nome, colore, spessore, tratto) in enumerate(anelli):
        s = punti(r0, r0 + 72, col(2 * a), col(2 * a) + 1, nome)
        s.smooth = True
        s.marker.symbol = "none"
        s.graphicalProperties.line.solidFill = colore
        s.graphicalProperties.line.width = spessore
        if tratto:
            s.graphicalProperties.line.prstDash = tratto
        etichetta_nome(s, pos="r", indice=26, sz=800, b=a == 0, colore=colore if a < 2 else TESTO_TENUE)
        ch.series.append(s)
    for s_ in range(k):
        s = punti(r0 + 2 * s_, r0 + 2 * s_ + 1, col(8), col(9), f"raggio {s_}")
        s.marker.symbol = "none"
        s.graphicalProperties.line.solidFill = "E7E6E6"
        s.graphicalProperties.line.width = 9525
        ch.series.append(s)
    from openpyxl.chart.data_source import StrRef
    for s_ in range(k):
        s = punti(r0 + s_, r0 + s_, col(11), col(12), "")
        s.tx = SeriesLabel(strRef=StrRef(f"'Radar'!${get_column_letter(col(10))}${r0 + s_}"))
        s.marker.symbol = "none"
        s.graphicalProperties.line.noFill = True
        etichetta_nome(s, sz=850, b=True, colore=BLU_NOTTE)
        ch.series.append(s)
    lato = lambda v: max(2, round(10 * v ** 0.5))
    for i, (r, x, y) in enumerate(posizioni):
        s = punti(r0 + i, r0 + i, col(14), col(15), r["id"])
        s.marker.symbol = "circle"
        s.marker.size = lato(r["prob"] * r["sev"])
        s.marker.graphicalProperties = GraphicalProperties(solidFill=RIEMPIMENTO_CERCHIO)
        s.marker.graphicalProperties.line.solidFill = ROSSO if r["vigilanza"] else "1F4E79"
        s.marker.graphicalProperties.line.width = 28575 if r["vigilanza"] else 9525
        s.graphicalProperties.line.noFill = True
        etichetta_nome(s, sz=800, b=True, colore=BLU_NOTTE)
        ch.series.append(s)
    for i, v in enumerate((4, 12, 25)):
        s = punti(r0 + i, r0 + i, col(17), col(18), f"{v}")
        s.marker.symbol = "circle"
        s.marker.size = lato(v)
        s.marker.graphicalProperties = GraphicalProperties(solidFill=RIEMPIMENTO_CERCHIO)
        s.marker.graphicalProperties.line.solidFill = "1F4E79"
        s.marker.graphicalProperties.line.width = 9525
        s.graphicalProperties.line.noFill = True
        etichetta_nome(s, pos="b", sz=800, b=False, colore=TESTO_TENUE)
        ch.series.append(s)
    for asse in (ch.x_axis, ch.y_axis):
        asse.scaling.min, asse.scaling.max = -7.6, 7.6
        asse.delete = True
        asse.majorGridlines = None
    ch.legend = None
    ch.graphical_properties = GraphicalProperties(ln=LineProperties(noFill=True))
    ch.plot_area.layout = Layout(manualLayout=ManualLayout(layoutTarget="inner", xMode="edge", yMode="edge", x=0.01, y=0.01, w=0.98, h=0.98))
    ch.height, ch.width = 17, 17
    ws.add_chart(ch, "A4")
    ws["L5"] = "Come si legge"
    ws["L5"].font = Font(bold=True, color=BLU_NOTTE)
    righe = ["Piu' vicino al centro = agire prima.",
             "Dentro il cerchio rosso: X + Y > Z, gia' in ritardo anche se l'evento non e' imminente.",
             "Anello ambra tratteggiato: 1 anno di margine.",
             "Area del cerchio = Probabilita x Severity (legenda in basso a destra: 4, 12, 25).",
             "Bordo rosso spesso = tema all'attenzione del supervisore.",
             "Cerchi semitrasparenti: due rischi vicini restano leggibili.",
             "Settore = event type, con il nome."]
    for i, t in enumerate(righe):
        c = ws.cell(row=6 + i, column=12, value="•  " + t)
        c.font = Font(size=10)
        c.alignment = Alignment(wrap_text=True, vertical="top")
        ws.merge_cells(start_row=6 + i, start_column=12, end_row=6 + i, end_column=16)
        ws.row_dimensions[6 + i].height = 30
    ws.cell(row=14, column=12, value="In basso a destra: cerchi di riferimento per P x I = 4, 12 e 25.").font = Font(
        size=9, italic=True, color=TESTO_TENUE)
    ws.merge_cells("L14:P14")
    for j in range(1, 17):
        ws.column_dimensions[get_column_letter(j)].width = 9
    stampa(ws)
    ws.print_area = "A1:P37"


def foglio_delta(wb, rischi):
    ws = wb.create_sheet("Delta")
    fascia(ws, 12, "che cosa e' cambiato dal ciclo precedente")
    ordinati = sorted([r for r in rischi if r["delta"] is not None], key=lambda r: -r["delta"])
    for j, t in enumerate(["Rischio", "In aumento", "In diminuzione", "Invariato"]):
        ws.cell(row=4, column=16 + j, value=t).font = Font(size=8, color=GRIGIO)
    for i, r in enumerate(ordinati):
        riga = 5 + i
        ws.cell(row=riga, column=16, value=f"{r['id']}  {r['nome'][:30]}{'…' if len(r['nome']) > 30 else ''}")
        colonna = 17 if r["delta"] > 0 else 18 if r["delta"] < 0 else None
        if colonna:
            ws.cell(row=riga, column=colonna, value=r["delta"]).number_format = "+0.00;-0.00;0.00"
        else:
            ws.cell(row=riga, column=19, value=0)
        for j in range(16, 20):
            ws.cell(row=riga, column=j).font = Font(size=8, color=GRIGIO)
    ultima = 4 + len(ordinati)
    su = sum(r["delta"] > 0 for r in ordinati)
    giu = sum(r["delta"] < 0 for r in ordinati)
    ch = BarChart()
    ch.type = "bar"
    ch.grouping = "clustered"
    ch.overlap = 100
    ch.gapWidth = 50
    ch.title = titolo_grafico(f"{su} rischi in aumento, {giu} in diminuzione, {len(ordinati) - su - giu} invariati")
    ch.visible_cells_only = False     # dati in colonne nascoste
    for c_, colore in ((17, ROSSO), (18, BLU_DIM), (19, GRIGIO)):
        ch.add_data(Reference(ws, min_col=c_, min_row=4, max_row=ultima), titles_from_data=True)
        s = ch.series[-1]
        s.graphicalProperties.solidFill = colore
        s.graphicalProperties.line.noFill = True
        s.invertIfNegative = False     # altrimenti Excel disegna bianca la barra negativa
        if c_ != 19:
            etichette_valore(s, formato="+0.00;-0.00;0.00", colore=colore)
    ch.set_categories(Reference(ws, min_col=16, min_row=5, max_row=ultima))
    ch.x_axis.scaling.orientation = "maxMin"
    ch.x_axis.tickLblPos = "low"
    ch.y_axis.scaling.min, ch.y_axis.scaling.max, ch.y_axis.majorUnit = -1, 1, 0.2
    ch.y_axis.numFmt = "+0.0;-0.0;0"
    ch.varyColors = False
    pulisci(ch)
    ch.height, ch.width = 11, 24
    ws.add_chart(ch, "A4")
    ws["A27"] = ("Scala fissa da -1 a +1. Rosso = score in aumento, blu = in diminuzione (distinguibili anche da chi confonde "
                 "rosso e verde). Dal maggiore aumento alla maggiore diminuzione. Nella versione vera: due linee tratteggiate "
                 "alla soglia di Parametri (0,40).")
    ws.merge_cells("A27:L27")
    ws["A27"].alignment = Alignment(wrap_text=True, vertical="top")
    ws["A27"].font = Font(size=9, italic=True, color=TESTO_TENUE)
    ws.row_dimensions[27].height = 30
    for c_ in range(16, 20):
        ws.column_dimensions[get_column_letter(c_)].hidden = True
    stampa(ws)
    ws.print_area = "A1:L27"


def foglio_scheda(wb, rischi, kri):
    import json
    ws = wb.create_sheet("Scheda")
    r = rischi[0]
    fascia(ws, 8, "scheda del rischio (esempio: il primo della classifica)")
    for l, w in zip("ABCDEFGH", [16, 16, 16, 16, 16, 16, 16, 40]):
        ws.column_dimensions[l].width = w
    # Fascia della scheda.
    ws.merge_cells("A4:F4")
    ws["A4"] = f"1 · {r['id']} · {r['nome']}"
    ws["A4"].font = Font(size=13, bold=True, color="FFFFFF")
    ws.merge_cells("G4:H4")
    ws["G4"] = f"score {r['score']:.2f}".replace(".", ",") + f"   {freccia(r['delta'])}   ·   {r['urgenza']}"
    ws["G4"].font = Font(size=12, bold=True, color="FFFFFF")
    ws["G4"].alignment = Alignment(horizontal="right", vertical="center")
    for j in range(1, 9):
        ws.cell(row=4, column=j).fill = fill(BLU_NOTTE)
    ws.row_dimensions[4].height = 26
    etichette = [f"{r['et']} · {dict(g.TASSONOMIA)[r['et']]}", f"Driver: {r['drv']}", f"Owner: {r['owner']}",
                 "◆ Tema all'attenzione del supervisore" if r["vigilanza"] else "", f"Esito: {r['esito']} · validato"]
    colonne = [(1, 2), (3, 4), (5, 6), (7, 7), (8, 8)]
    for (da, a), t in zip(colonne, etichette):
        if da != a:
            ws.merge_cells(start_row=5, start_column=da, end_row=5, end_column=a)
        c = ws.cell(row=5, column=da, value=t or None)
        c.font = Font(size=9, bold=t.startswith("◆"), color=ROSSO if t.startswith("◆") else TESTO_TENUE)
        c.fill = fill(BLU_CHIARO)
        c.alignment = Alignment(vertical="center", wrap_text=True)
        for x in range(da, a + 1):
            ws.cell(row=5, column=x).fill = fill(BLU_CHIARO)
    ws.row_dimensions[5].height = 28
    # Punteggi come celle colorate.
    scala = {1: "F2F2F2", 2: "FCE4D6", 3: "F8CBAD", 4: "F4B183", 5: "C55A11"}
    scala_conf = {1: "F2F2F2", 2: "DEEBF7", 3: "BDD7EE", 4: "9DC3E6", 5: "2E75B6"}
    dimensioni = [("Severity", r["sev"]), ("Probabilita", r["prob"]), ("Gap_Controlli", r["gap"]),
                  ("Velocity", r["vel"]), ("Prossimita", r["pro"]), ("Confidence", r["conf"])]
    for j, (nome, v) in enumerate(dimensioni, start=1):
        t = ws.cell(row=7, column=j, value=nome)
        t.font = Font(size=9, color=TESTO_TENUE)
        t.alignment = Alignment(horizontal="center")
        c = ws.cell(row=8, column=j, value=v)
        colore = (scala_conf if nome == "Confidence" else scala)[v]
        c.fill = fill(colore)
        c.font = Font(size=16, bold=True, color="FFFFFF" if v == 5 else TESTO)
        c.alignment = Alignment(horizontal="center", vertical="center")
        c.border = Border(left=Side(style="thick", color="FFFFFF"), right=Side(style="thick", color="FFFFFF"))
    ws.row_dimensions[8].height = 32
    ws["G8"] = "1-5, 5 = peggiore\nConfidence in blu: solidita' delle fonti, fuori dallo score"
    ws.merge_cells("G8:H8")
    ws["G8"].font = Font(size=8, italic=True, color=TESTO_TENUE)
    ws["G8"].alignment = Alignment(wrap_text=True, vertical="center")
    fonti = [f"• {a} ({d}, {t})" for a, d, t in g.FONTI[r["id"]] if d <= "2026-06-30"]
    variazioni = [f"• {d}: da {a_} a {b} — {ev} ({dt})" for d, a_, b, ev, dt in r["var"]] or ["Nessuna"]
    azioni = [f"• {a[1]} — {a[2]}, {a[4]}, {a[6]}" for a in g.AZIONI_ESEMPIO if a[0] == r["id"]]
    blocchi = [("Descrizione", r["descr"]), ("Razionale", r["razionale"]), ("Variazioni del ciclo", "\n".join(variazioni)),
               ("Fonti", "\n".join(fonti)), ("Azioni", "\n".join(azioni))]
    riga = 10
    for titolo, testo in blocchi:
        c = ws.cell(row=riga, column=1, value=titolo)
        c.font = Font(bold=True, color=BLU_NOTTE)
        c.alignment = Alignment(vertical="top")
        ws.merge_cells(start_row=riga, start_column=2, end_row=riga, end_column=8)
        t = ws.cell(row=riga, column=2, value=testo)
        t.alignment = Alignment(wrap_text=True, vertical="top")
        t.font = Font(size=10)
        righe = sum(max(1, len(x) // 125 + 1) for x in testo.split("\n"))
        ws.row_dimensions[riga].height = 15 * righe + 4
        for j in range(1, 9):
            ws.cell(row=riga, column=j).border = Border(bottom=bordo_sottile)
        riga += 1
    riga += 1
    ws.cell(row=riga, column=1, value="KRI in vigore").font = Font(bold=True, color=BLU_NOTTE)
    for j, t in enumerate(["Indicatore", "", "", "", "Valore", "Soglie", "Stato"], start=2):
        ws.cell(row=riga, column=j, value=t or None).font = Font(size=9, color=TESTO_TENUE)
    semaforo = {"Rosso": (ROSSO, "FFFFFF"), "Ambra": (AMBRA, TESTO), "Verde": ("70AD47", "FFFFFF"), "Non rilevato": ("D9D9D9", TESTO)}
    for k_ in [x for x in kri if x["rischio"] == r["id"]]:
        riga += 1
        ws.merge_cells(start_row=riga, start_column=2, end_row=riga, end_column=5)
        ws.cell(row=riga, column=2, value=f"{k_['nome']} ({k_['unita']})").alignment = Alignment(wrap_text=True)
        ws.cell(row=riga, column=6, value=k_["valore"]).alignment = Alignment(horizontal="center")
        ws.cell(row=riga, column=7, value=f"{k_['att']} / {k_['all']}").alignment = Alignment(horizontal="center")
        c = ws.cell(row=riga, column=8, value=k_["stato"])
        fondo, testo = semaforo[k_["stato"]]
        c.fill = fill(fondo)
        c.font = Font(bold=True, color=testo)
        c.alignment = Alignment(horizontal="center")
        ws.row_dimensions[riga].height = 18
    stampa(ws)


def trasparenza(percorso, colore, alpha=55000):
    """openpyxl non scrive la trasparenza: la si aggiunge nell'XML dei grafici."""
    tmp = percorso.with_suffix(".tmp")
    with zipfile.ZipFile(percorso) as zi, zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zo:
        for item in zi.infolist():
            dati_ = zi.read(item.filename)
            if item.filename.startswith("xl/charts/"):
                dati_ = dati_.replace(f'<a:srgbClr val="{colore}"/>'.encode(),
                                      f'<a:srgbClr val="{colore}"><a:alpha val="{alpha}"/></a:srgbClr>'.encode())
            zo.writestr(item, dati_)
    tmp.replace(percorso)


def main():
    rischi, kri = dati()
    wb = Workbook()
    foglio_valuta(wb)
    foglio_sintesi(wb, rischi, kri)
    foglio_matrice(wb, rischi)
    foglio_classifica(wb, rischi)
    foglio_radar(wb, rischi)
    foglio_delta(wb, rischi)
    foglio_scheda(wb, rischi, kri)
    wb.save(USCITA)
    trasparenza(USCITA, RIEMPIMENTO_CERCHIO)
    print(f"Anteprima scritta: {USCITA}")


if __name__ == "__main__":
    main()
