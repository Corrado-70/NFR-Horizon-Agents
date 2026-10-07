"""Anteprima v2 dello stile: registro e report in un solo file, schede dei rischi a parte.

Uso:
    python Analisi_Architettura/09_genera_anteprima_v2.py

Scrive, in Analisi_Architettura/:
- 09_Anteprima_v2_registro.xlsx  report al comitato + registro ridisegnato, in un solo
                                 file senza doppioni (struttura proposta nel foglio omonimo);
- 09_Anteprima_v2_schede.xlsx    una scheda per rischio, file a parte (a tendere prodotto
                                 da un agente dedicato).
Dati di esempio del pacchetto (ciclo 2026Q2), calcolati in Python e scritti come valori:
NON e' collegato al registro. Riprende la valutazione della v1 (09_Anteprima_v1_valutata.xlsx).
Riusa gli strumenti di 09_genera_anteprima.py (v1).
"""

import importlib.util
import math
from datetime import date, timedelta
from pathlib import Path

from openpyxl import Workbook
from openpyxl.chart import Reference, ScatterChart, Series
from openpyxl.chart.data_source import StrRef
from openpyxl.chart.label import DataLabel, DataLabelList
from openpyxl.chart.layout import Layout, ManualLayout
from openpyxl.chart.series import SeriesLabel
from openpyxl.chart.shapes import GraphicalProperties
from openpyxl.drawing.line import LineProperties
from openpyxl.formatting.rule import DataBarRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.worksheet.pagebreak import Break

QUI = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("anteprima_v1", QUI / "09_genera_anteprima.py")
v1 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(v1)
g = v1.g

USCITA_REGISTRO = QUI / "09_Anteprima_v2_registro.xlsx"
USCITA_SCHEDE = QUI / "09_Anteprima_v2_schede.xlsx"
NOME_ANALISI = "Horizon Scan NFR"
BLU_NOTTE, BLU_MEDIO, BLU_CHIARO = v1.BLU_NOTTE, v1.BLU_MEDIO, v1.BLU_CHIARO
ROSSO, AMBRA, GRIGIO, BLU_DIM = v1.ROSSO, v1.AMBRA, v1.GRIGIO, v1.BLU_DIM
TESTO, TESTO_TENUE, FONDO_TENUE = v1.TESTO, v1.TESTO_TENUE, v1.FONDO_TENUE
ROSSO_TENUE, AMBRA_TENUE, VERDE_TENUE = v1.ROSSO_TENUE, v1.AMBRA_TENUE, v1.VERDE_TENUE
GIALLO_VIGILANZA = "FFC000"          # bordo dei temi all'attenzione del supervisore (v1: rosso, confuso con Mosca)
fill = v1.fill
bordo_sottile = v1.bordo_sottile
SCALA = {1: "F2F2F2", 2: "FCE4D6", 3: "F8CBAD", 4: "F4B183", 5: "C55A11"}          # dimensioni 1-5
SCALA_CONF = {1: "F2F2F2", 2: "DEEBF7", 3: "BDD7EE", 4: "9DC3E6", 5: "2E75B6"}     # confidence
PROCESSO = {"trimestrale": ("DDEBF7", "1F4E79"), "settimanale": ("E2EFDA", "375623"),
            "validatore": ("FFF2CC", "7F6000"), "calcolo": ("EDEDED", "404040")}
TAB = {"report": BLU_NOTTE, "lavoro": "2E75B6", "dati": "A6A6A6", "guida": "FFC000"}


def fascia(ws, ultima_col, sottotitolo):
    """Fascia di intestazione, con il nome dell'analisi (nota 1 della valutazione v1)."""
    fine = get_column_letter(ultima_col)
    ws.merge_cells(f"A1:{fine}1")
    ws.merge_cells(f"A2:{fine}2")
    ws["A1"] = f"{NOME_ANALISI} — {sottotitolo}"
    ws["A1"].font = Font(size=16, bold=True, color="FFFFFF")
    ws["A1"].fill = fill(BLU_NOTTE)
    ws["A1"].alignment = Alignment(vertical="center", indent=1)
    ws["A2"] = "Ciclo 2026Q2  ·  dati al 30/06/2026  ·  ciclo validato il 15/07/2026  ·  Uso interno"
    ws["A2"].font = Font(size=10, color="FFFFFF")
    ws["A2"].fill = fill(BLU_MEDIO)
    ws["A2"].alignment = Alignment(vertical="center", indent=1)
    ws.row_dimensions[1].height = 30
    ws.row_dimensions[2].height = 18
    ws.sheet_view.showGridLines = False


v1.fascia = fascia      # Classifica e Delta della v1 usano la fascia nuova


def guida(ws, riga, ultima_col, testo, processo="calcolo", altezza=None):
    fine = get_column_letter(ultima_col)
    ws.merge_cells(f"A{riga}:{fine}{riga}")
    c = ws[f"A{riga}"]
    c.value = testo
    c.fill = fill(PROCESSO[processo][0])
    c.font = Font(size=9.5, color=TESTO)
    c.alignment = Alignment(wrap_text=True, vertical="top", indent=1)
    larghezza = sum((ws.column_dimensions[get_column_letter(j)].width or 8.43) for j in range(1, ultima_col + 1))
    righe = sum(max(1, -(-len(p) // int(larghezza * 1.25))) for p in testo.split("\n"))
    ws.row_dimensions[riga].height = altezza or 13 * righe + 6


def cella(ws, r, c, v=None, **stile):
    x = ws.cell(row=r, column=c, value=v)
    for k, val in stile.items():
        setattr(x, k, val)
    return x


# ============================================================== dati
SETTIMANA_CORRENTE = date(2026, 6, 29)


def segnali_netti():
    inizio = SETTIMANA_CORRENTE - timedelta(days=21)
    netti = {}
    for dt, _, _, _, _, rid, seg, _, _ in g.NEWS_ESEMPIO:
        lun = dt - timedelta(days=dt.weekday())
        if inizio <= lun <= SETTIMANA_CORRENTE and seg in ("Peggiorativo", "Migliorativo"):
            netti[rid] = netti.get(rid, 0) + (1 if seg == "Peggiorativo" else -1)
    return netti


def dati():
    rischi, kri = v1.dati()
    netti = segnali_netti()
    for i, r in enumerate(rischi, start=1):
        r["rank"] = i
        propri = [k for k in kri if k["rischio"] == r["id"]]
        r["kri_r"] = sum(k["stato"] == "Rosso" for k in propri)
        r["kri_a"] = sum(k["stato"] == "Ambra" for k in propri)
        r["kri_v"] = sum(k["stato"] == "Verde" for k in propri)
        r["netti"] = netti.get(r["id"], 0)
        r["adeguamento"] = g.ANNI_ADEGUAMENTO.get(r["id"])
    return rischi, kri


def num(v, d=2):
    return f"{v:.{d}f}".replace(".", ",")


def data_it(s):
    a, m, gg = s.split("-")
    return f"{gg}/{m}/{a}"


NOMI_DIM = {"severity": "Severity", "probabilita": "Probabilita", "gap_controlli": "Gap_Controlli",
            "velocity": "Velocity", "prossimita": "Prossimita", "confidence": "Confidence"}


def perche_segnalato(r, kri):
    """Perche' il rischio e' fra quelli segnalati: solo fatti del registro, calcolabili con formule."""
    parti = []
    if r["rank"] <= 3:
        d = "" if r["delta"] in (None, 0) else f", {'+' if r['delta'] > 0 else '−'}{num(abs(r['delta']))} sul ciclo prima"
        parti.append(f"{r['rank']}° per score composito ({num(r['score'])}{d})")
    if r["urgenza"] == "AGIRE ORA":
        extra = f", di cui {num(r['adeguamento'], 0)} anni di adeguamento strutturale" if r["adeguamento"] else ""
        parti.append(f"AGIRE ORA: servono X + Y = {num(r['x'] + r['y'])} anni per decidere e mitigare{extra}; "
                     f"ne restano Z = {num(r['z'], 1)} prima che possa manifestarsi")
    elif r["urgenza"] == "Entro l'anno" and r["rank"] <= 3:
        parti.append(f"margine di Mosca sotto l'anno ({num(r['margine'])})")
    if r["esito"] == "Variato":
        su = [v for v in r["var"] if v[0] != "confidence"]
        verso = "peggiora" if any(b > a for _, a, b, _, _ in su) else "migliora"
        parti.append(f"variato nel ciclo: {verso}")
    if r["vigilanza"]:
        parti.append("tema all'attenzione del supervisore")
    if r["kri_r"]:
        parti.append(f"{r['kri_r']} KRI in rosso")
    if r["netti"] >= 3:
        parti.append(f"notizie in peggioramento (+{r['netti']} segnali netti in 4 settimane)")
    elif r["netti"] <= -3:
        parti.append(f"notizie in miglioramento ({r['netti']} segnali netti in 4 settimane)")
    return "; ".join(parti) + "."


def cosa_cambiato(r):
    if not r["var"]:
        return "Nessun valore cambiato: confermato sulle fonti del ciclo precedente."
    return "\n".join(f"• {NOMI_DIM[d]} {a} → {b}: {ev} ({data_it(dt)})" for d, a, b, ev, dt in r["var"])


# Testi estesi: esempi di cio' che produrrebbe l'agente delle schede (nota 11 della v1).
ESTESI = {
    "NFR-01": dict(
        descr=("Frodi di tipo APP (pagamento autorizzato dal cliente) in cui il truffatore usa voci o video sintetici "
               "generati con l'intelligenza artificiale per impersonare un familiare, un dirigente o un operatore della "
               "Banca e indurre il cliente a disporre un bonifico istantaneo verso un conto che controlla. Il bonifico "
               "istantaneo e' accreditato in pochi secondi ed e' irrevocabile: una volta disposto non si recupera. Oggi il "
               "danno ricade sul cliente; con le linee guida europee sul rimborso obbligatorio delle frodi APP ricadrebbe "
               "sempre piu' sulla Banca. Il rischio nasce da un fattore esterno (AI generativa accessibile a tutti) e da un "
               "punto debole interno: la verifica fuori banda non copre ancora i bonifici istantanei."),
        dim={"severity": "Importi medi per caso triplicati sui bonifici istantanei (report trimestrale frodi, 10/06/2026); con il rimborso obbligatorio la perdita passerebbe alla Banca.",
             "probabilita": "Perdite rilevanti attese una volta in 1-2 anni: i tentativi sono frequenti (4,2 ogni 10.000 bonifici, KRI K1) ma quasi tutti bloccati.",
             "gap_controlli": "La verifica fuori banda esiste per i bonifici ordinari ma non per gli istantanei; azione approvata a 6 mesi.",
             "velocity": "Il danno si produce in minuti; il blocco di un beneficiario fraudolento richiede in media 2,5 ore (KRI K3).",
             "prossimita": "Casi con voce sintetica in due banche italiane comparabili (12/02/2026) e allerta del CERT finanziario (09/06/2026).",
             "confidence": "Due fonti interne recenti e quantitative, due esterne concordanti."},
        fonti={"Analisi interna sulle frodi da ingegneria sociale": "base del rischio: casistica sui canali digitali",
               "Threat intelligence: campagne di frode con voce sintetica verso banche UE": "prossimita': campagne attive in Europa",
               "Report trimestrale frodi — Funzione Antifrode": "severity: importi triplicati; valori dei KRI",
               "Relazione annuale sui pagamenti al dettaglio dell'autorita' di vigilanza": "contesto: crescita di istantanei e frodi APP"}),
    "NFR-07": dict(
        descr=("Un attacco ransomware al fornitore esterno che gestisce il gateway di pagamento della Banca cifra o rende "
               "indisponibili i suoi sistemi. I pagamenti della clientela si fermano finche' il fornitore non ripristina il "
               "servizio, e la Banca non ha un gateway alternativo attivabile nei tempi di ripristino previsti. Oltre al "
               "disservizio: penali, reclami, segnalazione DORA di incidente grave. Il fornitore e' classificato critico nel "
               "registro DORA, ma il ripristino da ransomware non e' mai stato provato insieme."),
        dim={"severity": "Blocco dei pagamenti della clientela: funzione essenziale interrotta, incidente grave da segnalare (DORA).",
             "probabilita": "Attacchi ransomware a processori di pagamento europei nel 2026; il fornitore ha 2 vulnerabilita' critiche aperte oltre 30 giorni (KRI K3).",
             "gap_controlli": "Piano di continuita' presente ma ripristino mai testato con il fornitore; test congiunto approvato a 6 mesi.",
             "velocity": "Il blocco e' immediato: i pagamenti si fermano appena il gateway e' irraggiungibile.",
             "prossimita": "Precursore nel settore bancario europeo (processore di pagamenti, febbraio 2026), nessun incidente presso il fornitore.",
             "confidence": "Una fonte interna (registro DORA) e una esterna."},
        fonti={"Registro DORA: fornitore del gateway di pagamento classificato critico": "severity: servizio critico senza alternativa",
               "Attacco ransomware a un processore di pagamenti europeo": "probabilita' e prossimita': minaccia attiva nel settore"}),
    "NFR-12": dict(
        descr=("Dall'obbligo di offrire i bonifici istantanei a tutta la clientela, i volumi sono cresciuti piu' in fretta "
               "dei controlli di processo. Errori di esecuzione, doppi addebiti e differenze di riconciliazione vanno risolti "
               "in giornata, perche' il pagamento e' gia' regolato; oggi la riconciliazione e' settimanale. Ne derivano "
               "rimborsi indebiti, perdite contabili e reclami. A maggio 2026 si sono visti i primi casi interni."),
        dim={"severity": "Rimborsi indebiti e disservizi su un processo critico, senza effetti sulla continuita': 5 rimborsi nel trimestre (KRI K2).",
             "probabilita": "Errori ricorrenti gia' osservati: 14 differenze aperte oltre un giorno (KRI K1, soglia di attenzione 10).",
             "gap_controlli": "Riconciliazione solo settimanale; controllo giornaliero automatico approvato a 3 mesi.",
             "velocity": "Gli errori si propagano in giornata sulle scritture contabili.",
             "prossimita": "Primi rimborsi indebiti e differenze di riconciliazione presso la Banca (report operativo, 15/05/2026).",
             "confidence": "Due fonti interne, una quantitativa e recente."},
        fonti={"Piano di adeguamento al regolamento sui bonifici istantanei": "contesto: obbligo e tempi di adeguamento",
               "Report operativo dei pagamenti istantanei — maggio": "prossimita': primi casi interni; valori dei KRI"}),
    "NFR-11": dict(
        descr=("Componenti del sistema di pagamento sono fuori dal supporto del produttore: non ricevono piu' patch di "
               "sicurezza e dipendono da poche persone che ne conoscono il funzionamento. Una vulnerabilita' sfruttata o un "
               "guasto non riparabile interromperebbe i pagamenti. La sostituzione richiede un programma di circa 3 anni "
               "(anni di adeguamento indicati dal validatore), molto piu' lungo dell'orizzonte delle singole azioni: per "
               "questo il rischio va affrontato ora anche se non e' imminente."),
        dim={"severity": "Disservizi sui pagamenti di durata limitata, senza effetti sulla solvibilita'.",
             "probabilita": "5 vulnerabilita' senza patch disponibile (KRI K2) e 7 componenti fuori supporto (KRI K1): un incidente in 2-5 anni e' plausibile.",
             "gap_controlli": "Nessuna patch per le componenti fuori supporto; solo presidi generici (segmentazione, monitoraggio).",
             "velocity": "Degrado progressivo: da 6 a 12 mesi fra la scoperta di una vulnerabilita' e il pieno impatto.",
             "prossimita": "Fine del supporto esteso annunciata dal produttore (31/01/2026).",
             "confidence": "Una fonte interna (inventario IT) e una esterna (produttore)."},
        fonti={"Inventario delle componenti fuori supporto — IT": "gap_controlli; valore del KRI K1",
               "Comunicazione del produttore sulla fine del supporto esteso": "prossimita'"}),
}

COMMENTO_ESTESO = [
    ("Messaggio chiave", "Il trimestre peggiora sui pagamenti istantanei: frodi con voce sintetica (NFR-01) ed errori "
                         "operativi (NFR-12) crescono insieme sullo stesso canale. Due rischi chiedono di agire ora."),
    ("Priorita' e perche'",
     "1) NFR-01 — importi medi per frode triplicati (report frodi del 10/06) e verifica fuori banda che non copre ancora "
     "i bonifici istantanei; e' anche l'unico rischio in fascia rossa di gravita'.\n"
     "2) NFR-11 — la sostituzione dei sistemi fuori supporto richiede circa 3 anni, piu' del tempo disponibile (1,5): "
     "va avviata ora anche se il rischio non e' imminente.\n"
     "3) NFR-07 — il ripristino da ransomware con il fornitore del gateway non e' mai stato provato; il blocco dei "
     "pagamenti sarebbe immediato."),
    ("Cosa e' cambiato", "Peggiorano NFR-01 (severity 3 → 4), NFR-12 (prossimita' 3 → 4, primi rimborsi indebiti interni "
                         "a maggio) e NFR-04 (prossimita' 2 → 3 dopo l'alluvione di maggio). Migliora NFR-05 (gap 4 → 3 "
                         "dopo l'audit del 20/05). Gli altri otto rischi sono confermati."),
    ("Decisioni richieste", "Approvare la verifica fuori banda sui bonifici istantanei (6 mesi); avviare il programma "
                            "pluriennale di sostituzione dei sistemi legacy; pianificare il test congiunto di ripristino con "
                            "il fornitore del gateway."),
]


# ============================================================== radar (grande e piccolo)
def dati_radar(ws, rischi, base=40):
    """Appoggio del radar in colonne nascoste di ws (da 'base'): lo usano il foglio Radar e la Sintesi."""
    k = len(g.TASSONOMIA)
    col = lambda n: base + n
    r0 = 5
    anelli = [0, 1, 2, 3]
    for a, m in enumerate(anelli):
        for p in range(73):
            ang = 2 * math.pi * p / 72
            ws.cell(row=r0 + p, column=col(2 * a), value=round((m + 2) * math.sin(ang), 4))
            ws.cell(row=r0 + p, column=col(2 * a) + 1, value=round((m + 2) * math.cos(ang), 4))
    for s in range(k):
        ang = 2 * math.pi * s / k
        ws.cell(row=r0 + 2 * s, column=col(8), value=0)
        ws.cell(row=r0 + 2 * s, column=col(9), value=0)
        ws.cell(row=r0 + 2 * s + 1, column=col(8), value=round(6.3 * math.sin(ang), 4))
        ws.cell(row=r0 + 2 * s + 1, column=col(9), value=round(6.3 * math.cos(ang), 4))
    corti = {"L1-03": "Impiego e sicurezza", "L1-04": "Clientela e prodotti", "L1-06": "Interruzione e sistemi", "L1-07": "Processi"}
    for s, (cod, nome) in enumerate(g.TASSONOMIA):
        ang = 2 * math.pi * (s + 0.5) / k
        ws.cell(row=r0 + s, column=col(10), value=f"{cod}\n{corti.get(cod, nome)}")
        ws.cell(row=r0 + s, column=col(11), value=round(6.95 * math.sin(ang), 4))
        ws.cell(row=r0 + s, column=col(12), value=round(6.95 * math.cos(ang), 4))
    per_settore = {}
    for r in rischi:
        per_settore.setdefault(r["et"], []).append(r)
    posizioni = []
    for s, (cod, _) in enumerate(g.TASSONOMIA):
        gruppo = per_settore.get(cod, [])
        for n_, r in enumerate(gruppo):
            ang = 2 * math.pi * (s + (n_ + 0.5) / len(gruppo)) / k
            raggio = max(0.6, min(6, r["margine"] + 2))
            posizioni.append(r)
            i = len(posizioni) - 1
            ws.cell(row=r0 + i, column=col(13), value=r["id"])
            ws.cell(row=r0 + i, column=col(14), value=round(raggio * math.sin(ang), 4))
            ws.cell(row=r0 + i, column=col(15), value=round(raggio * math.cos(ang), 4))
    # Legenda nel grafico: tre aree di riferimento (in basso a destra) e il bordo giallo (in basso a sinistra).
    for i, (v, x) in enumerate(((4, 3.5), (12, 4.8), (25, 6.5))):
        ws.cell(row=r0 + i, column=col(16), value=f"{v}")
        ws.cell(row=r0 + i, column=col(17), value=x)
        ws.cell(row=r0 + i, column=col(18), value=-6.6)
    ws.cell(row=r0, column=col(19), value="attenzione del supervisore")
    ws.cell(row=r0, column=col(20), value=-6.9)
    ws.cell(row=r0, column=col(21), value=-6.6)
    ws.cell(row=r0 + 1, column=col(19), value="Area = P x I")
    ws.cell(row=r0 + 1, column=col(20), value=4.3)
    ws.cell(row=r0 + 1, column=col(21), value=-5.6)
    for c_ in range(base, col(22)):
        ws.column_dimensions[get_column_letter(c_)].hidden = True
    return dict(base=base, r0=r0, posizioni=posizioni, col=col)


def grafico_radar(ws, info, piccolo=False):
    col, r0, posizioni = info["col"], info["r0"], info["posizioni"]
    ch = ScatterChart()
    ch.scatterStyle = "lineMarker"
    ch.varyColors = False
    ch.visible_cells_only = False
    scala = 0.62 if piccolo else 1

    def punti(r_da, r_a, cx, cy, nome):
        s = Series(Reference(ws, min_col=cy, min_row=r_da, max_row=r_a), xvalues=Reference(ws, min_col=cx, min_row=r_da, max_row=r_a))
        s.tx = SeriesLabel(v=nome)
        return s

    def etichetta(s, pos="ctr", indice=None, sz=900, b=True, colore=TESTO):
        base_l = dict(showSerName=True, showVal=False, showCatName=False, showLegendKey=False, showPercent=False, dLblPos=pos)
        if indice is None:
            s.dLbls = DataLabelList(**base_l)
        else:
            s.dLbls = DataLabelList(dLbl=[DataLabel(idx=indice, txPr=v1.testo_rich(sz, b, colore), **base_l)],
                                    showVal=False, showSerName=False, showCatName=False, showLegendKey=False, showPercent=False)
        s.dLbls.txPr = v1.testo_rich(sz, b, colore)

    anelli = [("Mosca: dentro = AGIRE ORA", ROSSO, 28575, None), ("1 anno", "8C8C8C", 12700, "dash"),
              ("2 anni", "BFBFBF", 9525, None), ("3 anni", "BFBFBF", 9525, None)]
    for a, (nome, colore, spessore, tratto) in enumerate(anelli):
        s = punti(r0, r0 + 72, col(2 * a), col(2 * a) + 1, nome)
        s.smooth = True
        s.marker.symbol = "none"
        s.graphicalProperties.line.solidFill = colore
        s.graphicalProperties.line.width = spessore
        if tratto:
            s.graphicalProperties.line.prstDash = tratto
        if not piccolo or a == 0:
            etichetta(s, pos="r", indice=26, sz=800 if not piccolo else 700, b=a == 0, colore=colore if a == 0 else TESTO_TENUE)
        ch.series.append(s)
    for s_ in range(len(g.TASSONOMIA)):
        s = punti(r0 + 2 * s_, r0 + 2 * s_ + 1, col(8), col(9), f"raggio {s_}")
        s.marker.symbol = "none"
        s.graphicalProperties.line.solidFill = "E7E6E6"
        s.graphicalProperties.line.width = 9525
        ch.series.append(s)
    for s_ in range(len(g.TASSONOMIA)):
        s = punti(r0 + s_, r0 + s_, col(11), col(12), "")
        s.tx = SeriesLabel(strRef=StrRef(f"'{ws.title}'!${get_column_letter(col(10))}${r0 + s_}"))
        s.marker.symbol = "none"
        s.graphicalProperties.line.noFill = True
        etichetta(s, sz=850 if not piccolo else 650, b=True, colore=BLU_NOTTE)
        ch.series.append(s)
    lato = lambda v: max(2, round(10 * scala * v ** 0.5))
    for i, r in enumerate(posizioni):
        s = punti(r0 + i, r0 + i, col(14), col(15), r["id"] if not piccolo else r["id"][4:])
        s.marker.symbol = "circle"
        s.marker.size = lato(r["prob"] * r["sev"])
        s.marker.graphicalProperties = GraphicalProperties(solidFill=v1.RIEMPIMENTO_CERCHIO)
        s.marker.graphicalProperties.line.solidFill = GIALLO_VIGILANZA if r["vigilanza"] else "1F4E79"
        s.marker.graphicalProperties.line.width = 34925 if r["vigilanza"] else 9525
        s.graphicalProperties.line.noFill = True
        etichetta(s, sz=800 if not piccolo else 650, b=True, colore=BLU_NOTTE)
        ch.series.append(s)
    if not piccolo:
        for i, v in enumerate((4, 12, 25)):
            s = punti(r0 + i, r0 + i, col(17), col(18), f"{v}")
            s.marker.symbol = "circle"
            s.marker.size = lato(v)
            s.marker.graphicalProperties = GraphicalProperties(solidFill=v1.RIEMPIMENTO_CERCHIO)
            s.marker.graphicalProperties.line.solidFill = "1F4E79"
            s.marker.graphicalProperties.line.width = 9525
            s.graphicalProperties.line.noFill = True
            etichetta(s, pos="b", sz=800, b=False, colore=TESTO_TENUE)
            ch.series.append(s)
        s = punti(r0 + 1, r0 + 1, col(20), col(21), "Area del cerchio = P x I")
        s.marker.symbol = "none"
        s.graphicalProperties.line.noFill = True
        etichetta(s, pos="ctr", sz=800, b=True, colore=TESTO_TENUE)
        ch.series.append(s)
    # Campione del bordo giallo, con la sua spiegazione nel grafico (nota 9 della v1).
    s = punti(r0, r0, col(20), col(21), "attenzione del supervisore")
    s.marker.symbol = "circle"
    s.marker.size = lato(6)
    s.marker.graphicalProperties = GraphicalProperties(solidFill=v1.RIEMPIMENTO_CERCHIO)
    s.marker.graphicalProperties.line.solidFill = GIALLO_VIGILANZA
    s.marker.graphicalProperties.line.width = 34925
    s.graphicalProperties.line.noFill = True
    etichetta(s, pos="r", sz=800 if not piccolo else 650, b=True, colore="7F6000")
    ch.series.append(s)
    for asse in (ch.x_axis, ch.y_axis):
        asse.scaling.min, asse.scaling.max = -7.6, 7.6
        asse.delete = True
        asse.majorGridlines = None
    ch.legend = None
    ch.graphical_properties = GraphicalProperties(ln=LineProperties(noFill=True))
    ch.plot_area.layout = Layout(manualLayout=ManualLayout(layoutTarget="inner", xMode="edge", yMode="edge", x=0.01, y=0.01, w=0.98, h=0.98))
    ch.height = ch.width = 7 if piccolo else 17
    return ch


# ============================================================== fogli del file unico
def foglio_valuta(ws):
    ws.sheet_properties.tabColor = TAB["guida"]
    fascia(ws, 7, "anteprima v2: come valutare")
    for l, w in zip("ABCDEFG", [5, 34, 16, 58, 50, 17, 36]):
        ws.column_dimensions[l].width = w
    guida(ws, 4, 7, "Seconda anteprima, sempre con dati di esempio e non collegata al registro. Su tua indicazione: "
                    "report e registro stanno in UN SOLO FILE, senza doppioni (foglio Struttura proposta); le schede dei "
                    "rischi sono in un file a parte (09_Anteprima_v2_schede.xlsx), a tendere prodotto da un agente dedicato. "
                    "La prima tabella dice cosa ho fatto delle tue note; la seconda chiede un giudizio sulle novita'.",
          "validatore")
    def tabella(r, intest, righe, colonne_input):
        for j, t in enumerate(intest, start=1):
            cella(ws, r, j, t, font=Font(bold=True, color="FFFFFF"), fill=fill(BLU_NOTTE),
                  alignment=Alignment(wrap_text=True, vertical="center"))
        for i, riga in enumerate(righe, start=1):
            for j, v in enumerate(riga, start=1):
                c = cella(ws, r + i, j, v, alignment=Alignment(wrap_text=True, vertical="top"),
                          border=Border(bottom=bordo_sottile))
                if j in colonne_input:
                    c.fill = fill(AMBRA_TENUE)
            ws.row_dimensions[r + i].height = max(30, 15 * (max(len(str(v or "")) for v in riga) // 55 + 1))
        return r + len(righe) + 2
    note = [
        (1, "Fascia di intestazione", "tutti", "Invece di \"Comitato Rischi\" l'analisi va chiamata \"Horizon Scan NFR\"",
         "Il titolo di ogni pagina e' \"Horizon Scan NFR — ...\"; tolto il nome del validatore dalla fascia (resta nella Sintesi, stato del ciclo)."),
        (3, "Primi cinque / matrice", "Sintesi", "Non e' immediato nella matrice capire di quali rischi si tratta: legenda in basso",
         "Sotto la mini matrice, legenda con ID e nome di tutti i rischi (◆ = attenzione del supervisore); nella matrice gli ID completi."),
        (4, "Mini matrice, mini radar, commento", "Sintesi",
         "Aggiungere il mini radar di Mosca; espandere il commento: per ogni rischio perche' varia e perche' lo si segnala",
         "Mini radar accanto alla legenda. La Sintesi diventa di due fogli: il quadro e il perche'. Nel secondo, \"Rischi segnalati e perche'\" (calcolabile dal registro: posizione, "
         "urgenza con X, Y e Z, variazioni con l'evidenza, KRI, notizie). Commento di A1 in quattro parti (messaggio, priorita' "
         "e perche', cosa e' cambiato, decisioni)."),
        (5, "Matrice grande", "Matrice", "Anche qui riportare i rischi", "Sotto la matrice l'elenco dei rischi dal piu' grave, con ID, nome, P · S e P x I."),
        (9, "Radar", "Radar", "Il bordo rosso si confonde con la frontiera di azione: bordo giallo; spiegarlo nel grafico",
         "Bordo giallo spesso; anello di 1 anno grigio tratteggiato (non piu' ambra, per non confondersi); nel grafico, in basso a "
         "sinistra, un cerchio campione con la scritta \"attenzione del supervisore\"."),
        (11, "Scheda del rischio", "file schede", "Razionale piu' lungo, descrizione lunga, fonti",
         "File a parte con una scheda per rischio: descrizione estesa, razionale per dimensione con l'evidenza, fonti con data, tipo "
         "e cosa sostengono, variazioni, urgenza spiegata, azioni, KRI. Testi estesi per NFR-01, 07, 11, 12 (esempio di cosa "
         "produrrebbe l'agente delle schede)."),
    ]
    r = tabella(6, ["#", "Tua nota su", "Foglio", "Cosa hai scritto", "Cosa ho cambiato", "Va bene ora?", "Nota"],
                [(*n, None, None) for n in note], {6, 7})
    nuovi = [
        ("A", "Struttura del file unico", "Struttura proposta", "Stessi dati, niente doppioni: otto viste che ripetevano gli stessi numeri diventano quattro; le schede vanno in un file a parte."),
        ("B", "Registro (vista del ciclo)", "Registro", "Una riga per rischio con tutto: dimensioni colorate, score, urgenza, KRI, notizie, owner. Sostituisce Dashboard e Approfondimento."),
        ("C", "Dati ridisegnati", "Dati_RiskRegister", "Tabella dati con gruppi di colonne, riga \"chi · cosa · come si calcola\", righe alterne."),
        ("D", "Dizionario dei dati", "Dizionario", "Ogni dato: chi lo scrive, quando, cosa significa, come si calcola, valori, esempio."),
        ("E", "Validazione ridisegnata", "Validazione", "Operazioni e criteri in testa, colonne da compilare in giallo, esempi di rettifica."),
        ("F", "Rischi segnalati e perche'", "Sintesi (perche')", "Per ogni rischio segnalato: perche' e cosa e' cambiato, con l'evidenza."),
        ("G", "File delle schede", "09_Anteprima_v2_schede.xlsx", "Indice e una scheda per rischio."),
    ]
    tabella(r, ["", "Novita'", "Dove", "Cosa guardare", "", "Ti piace?", "Nota"], [(a, b, c_, d, None, None, None) for a, b, c_, d in nuovi], {6, 7})
    dv = DataValidation(type="list", formula1='"Sì,No,Sì con modifiche"', allow_blank=True)
    ws.add_data_validation(dv)
    dv.add(f"F7:F{6 + len(note)}")
    dv.add(f"F{r + 1}:F{r + len(nuovi)}")
    v1.stampa(ws)


def foglio_struttura(ws):
    ws.sheet_properties.tabColor = TAB["guida"]
    fascia(ws, 5, "struttura proposta del file unico")
    for l, w in zip("ABCDE", [22, 26, 22, 58, 12]):
        ws.column_dimensions[l].width = w
    guida(ws, 4, 5, "Oggi il registro ha 20 fogli e diverse viste si ripetono (Dashboard, Trend, Delta, Classifica, KRI_Correnti, "
                    "Andamento_KRI, Approfondimento, Schede mostrano gli stessi numeri in modi diversi). Proposta: tre gruppi di "
                    "fogli con colori di linguetta diversi — REPORT (blu notte, si stampano per il comitato), LAVORO (blu, per "
                    "chi analizza e valida), DATI (grigio, li scrive solo lo script) — piu' la Guida. Le schede dei rischi escono "
                    "in un file a parte. Nessun dato si perde: cambiano solo le viste.", "calcolo")
    intest = ["Oggi", "Proposta", "Gruppo", "Perche'", "In anteprima"]
    for j, t in enumerate(intest, start=1):
        cella(ws, 6, j, t, font=Font(bold=True, color="FFFFFF"), fill=fill(BLU_NOTTE))
    righe = [
        ("Leggimi", "Guida", "guida", "Come si usa, chi aggiorna cosa, quando si lancia A5, dove si scrive a mano: un solo foglio iniziale.", "—"),
        ("Sintesi", "Sintesi + Sintesi (perche')", "report", "Due pagine: il quadro (numeri, priorita', matrice, radar) e il "
                                                               "perche' (rischi segnalati, commento, controllo, limiti).", "Sì"),
        ("Classifica", "Classifica", "report", "Invariata nella sostanza; stile nuovo.", "Sì"),
        ("Radar_Mosca", "Radar", "report", "Grafico piu' leggibile; la tabella di calcolo va nel foglio Registro.", "Sì"),
        ("—", "Matrice", "report", "Nuova: gravita' P x I.", "Sì"),
        ("Delta", "Delta", "report", "Invariato nella sostanza; stile nuovo.", "Sì"),
        ("Metodologia", "Metodologia", "report", "Resta per il comitato; rimanda al Dizionario per i dettagli.", "—"),
        ("Schede", "file Schede_<ciclo>.xlsx", "file a parte", "Testi lunghi per rischio: a tendere li scrive un agente dedicato, "
                   "partendo dal registro validato.", "file a parte"),
        ("Dashboard + Approfondimento", "Registro", "lavoro", "Una riga per rischio con tutto il ciclo; il resto e' gia' in Sintesi e Schede.", "Sì"),
        ("Trend", "Storico", "lavoro", "Score degli ultimi otto cicli, con i cicli come colonne e una mini-tendenza per riga.", "—"),
        ("KRI_Correnti + Andamento_KRI", "KRI", "lavoro", "I KRI del ciclo e, scelto un KRI, la sua storia: un foglio invece di due.", "—"),
        ("Analisi_News", "Notizie", "lavoro", "Pressione delle notizie e aree non presidiate.", "—"),
        ("Validazione", "Validazione", "lavoro", "Stessa tabella, istruzioni e criteri in testa, colonne da compilare in giallo.", "Sì"),
        ("Parametri", "Parametri", "lavoro", "Invariato; stile nuovo.", "—"),
        ("—", "Dizionario", "lavoro", "Nuovo: ogni dato con chi lo scrive, quando, significato, calcolo, valori, esempio.", "Sì"),
        ("RiskRegister, Azioni, KRI, NewsLog, Sintesi_Cicli", "stessi nomi, in fondo", "dati", "Tabelle ridisegnate, con gruppi di "
         "colonne e la riga \"chi · cosa · come si calcola\". Lo script non cambia.", "RiskRegister"),
    ]
    colori = {"report": BLU_NOTTE, "lavoro": "2E75B6", "dati": "A6A6A6", "guida": "BF8F00", "file a parte": "7030A0"}
    for i, riga in enumerate(righe, start=7):
        for j, v in enumerate(riga, start=1):
            c = cella(ws, i, j, v, alignment=Alignment(wrap_text=True, vertical="top"), border=Border(bottom=bordo_sottile))
            if j == 3:
                c.font = Font(bold=True, color=colori[v])
            if j == 2:
                c.font = Font(bold=True)
        ws.row_dimensions[i].height = 30
    ws.merge_cells(start_row=7 + len(righe) + 1, start_column=1, end_row=7 + len(righe) + 1, end_column=5)
    ws.row_dimensions[7 + len(righe) + 1].height = 45
    cella(ws, 7 + len(righe) + 1, 1, "Da 20 a 19 fogli, ma senza doppioni: Dashboard, Approfondimento, KRI_Correnti, Andamento_KRI e Schede spariscono, "
          "entrano Guida, Matrice, Dizionario e Registro; le schede vanno in un file a parte. Lo script di campo scrive "
          "solo nelle tabelle dati, che non cambiano: la struttura nuova si porta sul registro in uso con aggiorna-registro.",
          font=Font(bold=True, color=BLU_NOTTE), alignment=Alignment(wrap_text=True, vertical="top"))
    v1.stampa(ws)


def foglio_sintesi(ws, rischi, kri, ws_radar, info_radar):
    """Prima pagina del report: il quadro in una pagina."""
    ws.sheet_properties.tabColor = TAB["report"]
    fascia(ws, 15, "Sintesi per il comitato: il quadro")
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
        ("Variati · nuovi", f"{len(variati)} · {len(nuovi)}", "rispetto al 2026Q1", FONDO_TENUE, BLU_NOTTE),
        ("KRI in rosso", str(len(rossi)), f"su {len(kri)} in vigore", ROSSO_TENUE if rossi else FONDO_TENUE, ROSSO),
        ("Validazione", "✓", "validato il 15/07/2026", VERDE_TENUE, "375623"),
    ]
    for (da, a), (didascalia, numero, sotto, fondo, colore) in zip([(1, 3), (4, 6), (7, 9), (10, 12), (13, 15)], riquadri):
        l1, l2 = get_column_letter(da), get_column_letter(a)
        for r, testo, font in [(4, didascalia, Font(size=9, bold=True, color=TESTO_TENUE)),
                               (5, numero, Font(size=28, bold=True, color=colore)), (6, sotto, Font(size=9, color=TESTO_TENUE))]:
            ws.merge_cells(f"{l1}{r}:{l2}{r}")
            cella(ws, r, da, testo, font=font, alignment=Alignment(horizontal="center", vertical="center", wrap_text=True))
            for x in range(da, a + 1):
                ws.cell(row=r, column=x).fill = fill(fondo)
            ws.cell(row=r, column=a).border = Border(right=Side(style="thick", color="FFFFFF"))
    ws.row_dimensions[5].height = 42
    ws.row_dimensions[6].height = 26

    v1.sezione(ws, "A8", "H8", "Priorita' — primi cinque per score composito")
    v1.sezione(ws, "J8", "O8", "Gravita': Probabilita x Severity")
    for j, t in [(1, "#"), (2, "Rischio"), (6, "Score"), (7, "Variazione"), (8, "Urgenza")]:
        cella(ws, 9, j, t, font=Font(size=9, bold=True, color=TESTO_TENUE))
    ws.merge_cells("B9:E9")
    for k, r in enumerate(rischi[:5], start=1):
        riga = 9 + k
        cella(ws, riga, 1, k, font=Font(bold=True, color=BLU_NOTTE), alignment=Alignment(vertical="center"))
        ws.merge_cells(f"B{riga}:E{riga}")
        cella(ws, riga, 2, f"{r['id']}  {r['nome']}" + ("  ◆" if r["vigilanza"] else ""), font=Font(size=10),
              alignment=Alignment(wrap_text=True, vertical="center"))
        cella(ws, riga, 6, r["score"], number_format="0.00", font=Font(bold=True), alignment=Alignment(vertical="center"))
        cella(ws, riga, 7, v1.freccia(r["delta"]), alignment=Alignment(vertical="center"),
              font=Font(size=10, color=ROSSO if (r["delta"] or 0) > 0 else BLU_DIM if (r["delta"] or 0) < 0 else TESTO_TENUE))
        v1.chip_urgenza(ws.cell(row=riga, column=8), r["urgenza"])
        ws.row_dimensions[riga].height = 27
        for j in range(1, 9):
            ws.cell(row=riga, column=j).border = Border(bottom=bordo_sottile)
    ws.conditional_formatting.add("F10:F14", DataBarRule(start_type="num", start_value=0, end_type="num", end_value=5, color="8EA9DB"))
    cella(ws, 15, 1, "◆ = tema all'attenzione del supervisore. Score 1-5, 5 = peggiore; barra su scala fissa 0-5.",
          font=Font(size=8, italic=True, color=TESTO_TENUE))
    cella(ws, 9, 10, "P \\ S", font=Font(size=8, bold=True, color=TESTO_TENUE))
    for s in range(1, 6):
        cella(ws, 9, 10 + s, s, font=Font(size=8, bold=True, color=TESTO_TENUE), alignment=Alignment(horizontal="center"))
    for i, p in enumerate(range(5, 0, -1)):
        riga = 10 + i
        cella(ws, riga, 10, p, font=Font(size=8, bold=True, color=TESTO_TENUE), alignment=Alignment(horizontal="center", vertical="center"))
        for s in range(1, 6):
            ids = [r["id"] for r in rischi if r["prob"] == p and r["sev"] == s]
            testo = "\n".join(" ".join(ids[i_:i_ + 2]) for i_ in range(0, len(ids), 2))
            bianco = Side(style="thin", color="FFFFFF")
            cella(ws, riga, 10 + s, testo or None, fill=fill(v1.fascia_pxi(p * s)), font=Font(size=7, bold=True),
                  alignment=Alignment(horizontal="center", vertical="center", wrap_text=True),
                  border=Border(left=bianco, right=bianco, top=bianco, bottom=bianco))
    cella(ws, 15, 10, "Verde P x I fino a 6, ambra 8-12, rosso da 15.", font=Font(size=8, italic=True, color=TESTO_TENUE))

    # Pagina 1, seconda meta': mini radar e legenda dei rischi (note 3 e 4 della v1).
    v1.sezione(ws, "A17", "H17", "Urgenza: radar di Mosca")
    v1.sezione(ws, "J17", "O17", "I rischi del ciclo")
    radar = grafico_radar(ws_radar, info_radar, piccolo=True)
    ws.add_chart(radar, "B18")
    for i, r in enumerate(sorted(rischi, key=lambda x: x["id"])):
        riga = 18 + i
        ws.merge_cells(f"K{riga}:O{riga}")
        cella(ws, riga, 10, r["id"], font=Font(size=8, bold=True, color=BLU_NOTTE))
        cella(ws, riga, 11, r["nome"] + ("  ◆" if r["vigilanza"] else ""), font=Font(size=8),
              alignment=Alignment(vertical="center"))
        ws.row_dimensions[riga].height = 17.5
    cella(ws, 31, 1, "Radar: piu' vicino al centro = agire prima; dentro il cerchio rosso X + Y > Z. Area = P x I; bordo giallo = "
                     "attenzione del supervisore. Numeri = NFR-nn. Il perche' di ogni rischio segnalato: foglio seguente.",
          font=Font(size=8, italic=True, color=TESTO_TENUE))
    v1.stampa(ws)          # una pagina


def foglio_sintesi_perche(ws, rischi, kri):
    """Seconda pagina del report: i rischi segnalati, il perche', il commento (nota 4 della v1)."""
    ws.sheet_properties.tabColor = TAB["report"]
    fascia(ws, 15, "Sintesi per il comitato: il perche'")
    for j in range(1, 16):
        ws.column_dimensions[get_column_letter(j)].width = 10.5
    v1.sezione(ws, "A4", "O4", "Rischi segnalati e perche'")
    cella(ws, 5, 1, "Rischi fra i primi tre, da affrontare subito o variati nel ciclo. Tutto calcolato dai dati validati del registro.",
          font=Font(size=8, italic=True, color=TESTO_TENUE))
    for (da, a), t in [((1, 3), "Rischio"), ((4, 8), "Perche' lo segnaliamo"), ((9, 15), "Cosa e' cambiato, e su quale evidenza")]:
        ws.merge_cells(start_row=6, start_column=da, end_row=6, end_column=a)
        cella(ws, 6, da, t, font=Font(bold=True, color="FFFFFF"), fill=fill(BLU_MEDIO))
        for x in range(da, a + 1):
            ws.cell(row=6, column=x).fill = fill(BLU_MEDIO)
    segnalati = [r for r in rischi if r["rank"] <= 3 or r["urgenza"] == "AGIRE ORA" or r["esito"] == "Variato"]
    riga = 7
    for r in segnalati:
        for (da, a), testo, font in [((1, 3), f"{r['id']}\n{r['nome']}" + ("\n◆ attenzione del supervisore" if r["vigilanza"] else ""),
                                      Font(size=9, bold=True, color=BLU_NOTTE)),
                                     ((4, 8), perche_segnalato(r, kri), Font(size=9)),
                                     ((9, 15), cosa_cambiato(r), Font(size=9))]:
            ws.merge_cells(start_row=riga, start_column=da, end_row=riga, end_column=a)
            cella(ws, riga, da, testo, font=font, alignment=Alignment(wrap_text=True, vertical="top"))
            for x in range(da, a + 1):
                ws.cell(row=riga, column=x).border = Border(bottom=bordo_sottile)
        lunghezza = max(len(perche_segnalato(r, kri)) / 55, len(cosa_cambiato(r)) / 80 + cosa_cambiato(r).count("\n"), 3)
        ws.row_dimensions[riga].height = 13 * (int(lunghezza) + 1) + 4
        if r["urgenza"] == "AGIRE ORA":
            ws.cell(row=riga, column=1).fill = fill(ROSSO_TENUE)
        riga += 1

    riga += 1
    v1.sezione(ws, f"A{riga}", f"O{riga}", "Il commento dell'analisi (agente A1, scritto prima della validazione)")
    riga += 1
    for titolo, testo in COMMENTO_ESTESO:
        ws.merge_cells(start_row=riga, start_column=1, end_row=riga, end_column=3)
        ws.merge_cells(start_row=riga, start_column=4, end_row=riga, end_column=15)
        cella(ws, riga, 1, titolo, font=Font(size=10, bold=True, color=BLU_NOTTE), alignment=Alignment(vertical="top"))
        cella(ws, riga, 4, testo, font=Font(size=10), alignment=Alignment(wrap_text=True, vertical="top"))
        ws.row_dimensions[riga].height = 14 * (sum(len(p) // 120 + 1 for p in testo.split("\n"))) + 4
        riga += 1
    riga += 1
    _, a5, _ = g.SINTESI_ESEMPIO["2026Q2"]
    for titolo, testo, fondo in [("Controllo indipendente (A5)", a5 + " Osservazioni non bloccanti: 1.", None),
                                 ("Dopo il commento", "Il validatore ha applicato 3 rettifiche o respingimenti: numeri e grafici del report "
                                                      "sono quelli validati e prevalgono sul commento.", AMBRA_TENUE)]:
        ws.merge_cells(start_row=riga, start_column=1, end_row=riga, end_column=3)
        ws.merge_cells(start_row=riga, start_column=4, end_row=riga, end_column=15)
        cella(ws, riga, 1, titolo, font=Font(size=10, bold=True, color=BLU_NOTTE))
        c = cella(ws, riga, 4, testo, font=Font(size=10), alignment=Alignment(wrap_text=True, vertical="top"))
        if fondo:
            for x in range(4, 16):
                ws.cell(row=riga, column=x).fill = fill(fondo)
        ws.row_dimensions[riga].height = 28
        riga += 1
    ws.merge_cells(start_row=riga + 1, start_column=1, end_row=riga + 1, end_column=15)
    cella(ws, riga + 1, 1, "Limiti: " + g.leggi_limiti(), font=Font(size=8, italic=True, color=TESTO_TENUE),
          alignment=Alignment(wrap_text=True, vertical="top"))
    ws.row_dimensions[riga + 1].height = 36
    ws.page_setup.orientation = "landscape"
    ws.page_setup.paperSize = ws.PAPERSIZE_A4
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.oddFooter.left.text = "Anteprima di stile — dati di esempio"
    ws.oddFooter.right.text = "Pagina &P di &N"


def foglio_radar(ws, rischi):
    ws.sheet_properties.tabColor = TAB["report"]
    fascia(ws, 16, "Radar di Mosca: quanto presto agire")
    info = dati_radar(ws, rischi)
    ws.add_chart(grafico_radar(ws, info), "A4")
    cella(ws, 5, 12, "Come si legge", font=Font(bold=True, color=BLU_NOTTE))
    righe = ["Piu' vicino al centro = agire prima.",
             "Dentro il cerchio rosso: X + Y > Z, gia' in ritardo anche se l'evento non e' imminente.",
             "Cerchi grigi: 1 anno (tratteggiato), 2 e 3 anni di margine.",
             "Area del cerchio = Probabilita x Severity (riferimenti in basso a destra: 4, 12, 25).",
             "Bordo giallo spesso = tema all'attenzione del supervisore (campione in basso a sinistra).",
             "Cerchi semitrasparenti: due rischi vicini restano leggibili.",
             "Settore = event type, con il nome."]
    for i, t in enumerate(righe):
        ws.merge_cells(start_row=6 + i, start_column=12, end_row=6 + i, end_column=16)
        cella(ws, 6 + i, 12, "•  " + t, font=Font(size=10), alignment=Alignment(wrap_text=True, vertical="top"))
        ws.row_dimensions[6 + i].height = 30
    for j in range(1, 17):
        ws.column_dimensions[get_column_letter(j)].width = 9
    v1.stampa(ws)
    ws.print_area = "A1:P37"
    return info


def foglio_matrice(ws, rischi):
    ws.sheet_properties.tabColor = TAB["report"]
    fascia(ws, 7, "gravita': Probabilita x Severity")
    ws.column_dimensions["A"].width = 13
    ws.column_dimensions["B"].width = 5
    for j in range(3, 8):
        ws.column_dimensions[get_column_letter(j)].width = 20
    ws.column_dimensions["H"].width = 3
    for l, w in zip("IJKLM", [9, 44, 5, 5, 7]):
        ws.column_dimensions[l].width = w
    guida(ws, 4, 7, "Ogni rischio sta nella cella della sua Probabilita (righe) e Severity (colonne), valori validati. "
                     "Colore = P x I: verde fino a 6, ambra da 8 a 12, rosso da 15. ◆ = tema all'attenzione del supervisore. "
                     "La gravita' non dice quando agire: per quello c'e' il Radar di Mosca. Sotto, i rischi dal piu' grave.")
    descr_p = {5: "Quasi certa", 4: "Probabile", 3: "Possibile", 2: "Improbabile", 1: "Rara"}
    descr_s = {1: "Trascurabile", 2: "Contenuto", 3: "Rilevante", 4: "Grave", 5: "Critico"}
    cella(ws, 6, 1, "Probabilita", font=Font(bold=True, color=BLU_NOTTE))
    bianco = Side(style="medium", color="FFFFFF")
    for i, p in enumerate(range(5, 0, -1)):
        r = 7 + i
        cella(ws, r, 1, descr_p[p], font=Font(size=9, color=TESTO_TENUE), alignment=Alignment(vertical="center", horizontal="right"))
        cella(ws, r, 2, p, font=Font(bold=True, color=BLU_NOTTE), alignment=Alignment(horizontal="center", vertical="center"))
        for s in range(1, 6):
            voci = [f"{x['id']}{' ◆' if x['vigilanza'] else ''}" for x in rischi if x["prob"] == p and x["sev"] == s]
            testo = "\n".join("   ".join(voci[i_:i_ + 2]) for i_ in range(0, len(voci), 2))
            cella(ws, r, 2 + s, testo or None, fill=fill(v1.fascia_pxi(p * s)), font=Font(size=10, bold=True),
                  alignment=Alignment(horizontal="center", vertical="center", wrap_text=True),
                  border=Border(left=bianco, right=bianco, top=bianco, bottom=bianco))
        ws.row_dimensions[r].height = 50
    for s in range(1, 6):
        cella(ws, 12, 2 + s, s, font=Font(bold=True, color=BLU_NOTTE), alignment=Alignment(horizontal="center"))
        cella(ws, 13, 2 + s, descr_s[s], font=Font(size=9, color=TESTO_TENUE), alignment=Alignment(horizontal="center"))
    cella(ws, 14, 5, "Severity", font=Font(bold=True, color=BLU_NOTTE), alignment=Alignment(horizontal="center"))
    # Elenco dei rischi accanto alla matrice (nota 5 della v1).
    v1.sezione(ws, "A16", "G16", "I rischi, dal piu' grave")
    for j, t in zip((1, 3, 6, 7), ["ID", "Rischio", "P · S", "P x I"]):
        cella(ws, 17, j, t, font=Font(size=9, bold=True, color="FFFFFF"), fill=fill(BLU_MEDIO))
    for x in range(1, 8):
        ws.cell(row=17, column=x).fill = fill(BLU_MEDIO)
    ws.merge_cells("C17:E17")
    for i, r in enumerate(sorted(rischi, key=lambda x: (-x["prob"] * x["sev"], x["id"]))):
        riga = 18 + i
        v = r["prob"] * r["sev"]
        ws.merge_cells(f"A{riga}:B{riga}")
        ws.merge_cells(f"C{riga}:E{riga}")
        cella(ws, riga, 1, r["id"], font=Font(size=9, bold=True, color=BLU_NOTTE))
        cella(ws, riga, 3, r["nome"] + ("  ◆" if r["vigilanza"] else ""), font=Font(size=9))
        cella(ws, riga, 6, f"{r['prob']} · {r['sev']}", font=Font(size=9), alignment=Alignment(horizontal="center"))
        cella(ws, riga, 7, v, font=Font(size=9, bold=True), fill=fill(v1.fascia_pxi(v)), alignment=Alignment(horizontal="center"))
        for x in range(1, 8):
            ws.cell(row=riga, column=x).border = Border(bottom=bordo_sottile)
    v1.stampa(ws)


def foglio_registro(ws, rischi):
    """Vista del ciclo: una riga per rischio con tutto (sostituisce Dashboard e Approfondimento)."""
    ws.sheet_properties.tabColor = TAB["lavoro"]
    larghezze = [9, 40, 7, 6, 6, 6, 6, 6, 6, 8, 8, 13, 8, 5, 4, 4, 4, 9, 28]
    for j, w in enumerate(larghezze, start=1):
        ws.column_dimensions[get_column_letter(j)].width = w
    fascia(ws, 19, "Registro: il ciclo corrente, un rischio per riga")
    guida(ws, 4, 19,
          "COSA E': la fotografia del ciclo corrente, valori validati, ordinata per score. Sostituisce Dashboard e Approfondimento: "
          "la storia di un rischio e' nella sua scheda, quella degli score nel foglio Storico.\n"
          "COME SI CALCOLA: Score = 0,30 Severity + 0,20 Probabilita + 0,20 Gap_Controlli + 0,15 Velocity + 0,15 Prossimita (pesi in "
          "Parametri). Margine di Mosca = Z - (X + Y): Z dalla Prossimita, X = 0,25 anni, Y = orizzonte piu' lungo delle azioni non "
          "respinte o anni di adeguamento, se maggiori. Urgenza: margine < 0 AGIRE ORA, < 1 entro l'anno. KRI: quanti in rosso, "
          "ambra, verde. Segnali: notizie peggiorative meno migliorative delle ultime 4 settimane (soglia 3).\n"
          "COLORI: intestazioni come chi scrive (azzurro trimestrale, verde settimanale, giallo validatore, grigio calcolo); "
          "dimensioni dal chiaro (1) allo scuro (5). Dettaglio di ogni colonna: foglio Dizionario.", "calcolo")
    gruppi = [((1, 3), "Rischio", "calcolo"), ((4, 9), "Dimensioni 1-5 (A1, validate)", "trimestrale"),
              ((10, 13), "Calcolati dal foglio", "calcolo"), ((14, 14), "Valid.", "validatore"),
              ((15, 17), "KRI del ciclo", "trimestrale"), ((18, 18), "Settim.", "settimanale"), ((19, 19), "Anagrafica", "validatore")]
    for (da, a), t, p in gruppi:
        if da != a:
            ws.merge_cells(start_row=6, start_column=da, end_row=6, end_column=a)
        for x in range(da, a + 1):
            cella(ws, 6, x, t if x == da else None, fill=fill(PROCESSO[p][0]), font=Font(size=9, bold=True, color=PROCESSO[p][1]),
                  alignment=Alignment(horizontal="center"))
    intest = ["ID", "Nome", "Event type", "Sev", "Prob", "Gap", "Vel", "Pross", "Conf", "Score", "Δ ciclo prima", "Urgenza",
              "Margine (anni)", "◆", "R", "A", "V", "Segnali 4 sett.", "Owner"]
    for j, t in enumerate(intest, start=1):
        cella(ws, 7, j, t, font=Font(size=9, bold=True, color=TESTO), border=Border(bottom=Side(style="medium", color=BLU_NOTTE)),
              alignment=Alignment(horizontal="center" if j > 2 else "left", wrap_text=True, vertical="bottom"))
    ws.row_dimensions[7].height = 28
    for i, r in enumerate(rischi):
        riga = 8 + i
        zebra = fill("FAFAFA") if i % 2 else None
        valori = [r["id"], r["nome"], r["et"], r["sev"], r["prob"], r["gap"], r["vel"], r["pro"], r["conf"], r["score"],
                  v1.freccia(r["delta"]), None, r["margine"], "◆" if r["vigilanza"] else None,
                  r["kri_r"] or None, r["kri_a"] or None, r["kri_v"] or None,
                  ("▲ +" if r["netti"] >= 3 else "▼ " if r["netti"] <= -3 else "● ") + str(r["netti"]), r["owner"]]
        for j, v in enumerate(valori, start=1):
            c = cella(ws, riga, j, v, font=Font(size=10), alignment=Alignment(horizontal="center" if j > 2 else "left", vertical="center"),
                      border=Border(bottom=bordo_sottile))
            if zebra:
                c.fill = zebra
        for j, v in zip(range(4, 9), (r["sev"], r["prob"], r["gap"], r["vel"], r["pro"])):
            ws.cell(row=riga, column=j).fill = fill(SCALA[v])
            ws.cell(row=riga, column=j).font = Font(size=10, bold=True, color="FFFFFF" if v == 5 else TESTO)
        ws.cell(row=riga, column=9).fill = fill(SCALA_CONF[r["conf"]])
        ws.cell(row=riga, column=10).number_format = "0.00"
        ws.cell(row=riga, column=10).font = Font(size=10, bold=True)
        ws.cell(row=riga, column=11).font = Font(size=9, color=ROSSO if (r["delta"] or 0) > 0 else BLU_DIM if (r["delta"] or 0) < 0 else TESTO_TENUE)
        v1.chip_urgenza(ws.cell(row=riga, column=12), r["urgenza"])
        ws.cell(row=riga, column=13).number_format = "+0.00;-0.00;0.00"
        ws.cell(row=riga, column=14).font = Font(bold=True, color="BF8F00")
        for j, colore in ((15, ROSSO), (16, AMBRA), (17, "70AD47")):
            if ws.cell(row=riga, column=j).value:
                ws.cell(row=riga, column=j).fill = fill(colore)
                ws.cell(row=riga, column=j).font = Font(size=10, bold=True, color="FFFFFF" if j != 16 else TESTO)
        ws.cell(row=riga, column=18).font = Font(size=9, color=ROSSO if r["netti"] >= 3 else BLU_DIM if r["netti"] <= -3 else TESTO_TENUE)
        ws.row_dimensions[riga].height = 20
    ws.conditional_formatting.add(f"J8:J{7 + len(rischi)}", DataBarRule(start_type="num", start_value=0, end_type="num",
                                                                        end_value=5, color="8EA9DB"))
    ws.freeze_panes = "C8"
    v1.stampa(ws)


# Dizionario: una riga per dato (campo, dove, chi e quando, significato, come si calcola, valori, esempio).
DIZIONARIO = [
    ("Ciclo", "RiskRegister, Azioni, KRI", "Script, ciclo trimestrale", "Trimestre valutato.", "Dal payload di A1 (ciclo_da_valutare della baseline).", "AAAAQn", "2026Q2"),
    ("Data_Riferimento", "RiskRegister", "Script, trimestrale", "Data fino alla quale sono considerate le fonti.", "Fine del trimestre.", "data", "30/06/2026"),
    ("ID_Rischio", "tutte", "A1 (nuovi); stabile", "Codice del rischio, uguale in tutti i cicli.", "Rischio nuovo: primo NFR-nn non usato.", "NFR-nn", "NFR-01"),
    ("Event_Type", "RiskRegister", "A1, trimestrale", "Categoria di perdita di Basilea: il settore del radar.", "Scelta di A1 fra i sette codici della tassonomia.", "L1-01..L1-07", "L1-02"),
    ("Severity", "RiskRegister", "A1, validata", "Quanto danno se il rischio si manifesta.", "Descrittore della rubrica piu' aderente all'evidenza; al massimo un punto di variazione fra cicli.", "1-5", "4"),
    ("Probabilita", "RiskRegister", "A1, validata", "Quanto spesso, con i controlli attuali.", "Come sopra; un numero senza fonte e' dichiarato come valutazione.", "1-5", "4"),
    ("Gap_Controlli", "RiskRegister", "A1, validata", "Quanto manca a un presidio adeguato.", "Scende solo con un controllo testato.", "1-5", "3"),
    ("Velocity", "RiskRegister", "A1, validata", "Quanto in fretta arriva il pieno impatto.", "Descrittori in tempi (da oltre 12 mesi a entro 24 ore).", "1-5", "4"),
    ("Prossimita", "RiskRegister", "A1, validata", "Quando puo' manifestarsi.", "Descrittori in anni con precursori; da' la Z di Mosca.", "1-5", "4"),
    ("Confidence", "RiskRegister", "A1, validata", "Quanto e' solida l'evidenza (non la gravita').", "4 richiede almeno 2 fonti, 5 almeno 3; fuori dallo score.", "1-5", "4"),
    ("Score_Composito", "RiskRegister (formula)", "Foglio, a ogni ricalcolo", "Gravita' complessiva del rischio.",
     "0,30 Sev + 0,20 Prob + 0,20 Gap + 0,15 Vel + 0,15 Pross, pesi in Parametri, arrotondato a 2 decimali; vuoto se manca una dimensione.", "1,00-5,00", "3,80"),
    ("Δ score", "Delta, Registro", "Foglio", "Variazione sul ciclo precedente.", "Score del ciclo meno score del ciclo prima (stessi pesi).", "-1..+1 circa", "+0,30"),
    ("Esito", "RiskRegister", "A1, ricalcolato dopo la validazione", "Se il rischio e' cambiato.", "Confermato = nessun valore cambiato; Variato = almeno uno; Nuovo.", "3 valori", "Variato"),
    ("Variazioni", "RiskRegister", "A1, riscritte dopo la validazione", "Cosa e' cambiato e perche'.", "Per ogni valore cambiato: da, a, evidenza, data dell'evidenza (dopo il ciclo precedente).", "elenco", "Severity 3 → 4: report frodi..."),
    ("Fonti", "RiskRegister", "A1", "Su cosa si basa la valutazione.", "Riferimento, data, Interna/Esterna; nessuna fonte datata dopo il ciclo.", "elenco", "4 fonti"),
    ("Z", "Radar, Registro", "Foglio", "Anni prima che il rischio possa manifestarsi.", "Dalla Prossimita: 5 → 0; 4 → 0,5; 3 → 1,5; 2 → 2,5; 1 → 4 (Parametri).", "anni", "0,5"),
    ("X", "Radar, Registro", "Parametro", "Anni per decidere e avviare.", "Costante in Parametri: un ciclo.", "anni", "0,25"),
    ("Y", "Radar, Registro", "Foglio", "Anni per mitigare.", "Orizzonte piu' lungo delle azioni del ciclo non respinte (o 1 anno se non ce ne sono); se maggiori, gli anni di adeguamento dell'anagrafica.", "anni", "0,5"),
    ("Margine / Urgenza", "Radar, Registro, Classifica", "Foglio", "Quanto presto agire.", "Margine = Z - (X + Y). Sotto 0: AGIRE ORA; da 0 a 1: entro l'anno; oltre: margine in anni.", "anni", "-0,25 · AGIRE ORA"),
    ("Anni_Adeguamento", "Parametri, anagrafica", "Validatore, quando serve", "Durata di un adeguamento strutturale.", "Input; diventa la Y minima.", "anni o vuoto", "NFR-11: 3"),
    ("Attenzione_Supervisore", "Parametri, anagrafica", "Validatore", "Tema nelle priorita' di BCE, EBA o Banca d'Italia.", "Input Sì/No; bordo giallo nel radar, ◆ nelle tabelle. Non cambia score ne' urgenza.", "Sì/No", "Sì"),
    ("KRI Valore_Corrente", "KRI", "A1 (rilettura), validato", "Valore dell'indicatore nel ciclo.", "Rilevato dalla fonte interna; vuoto se non rilevato, mai ricopiato.", "numero", "4,2"),
    ("KRI Stato", "KRI (formula)", "Foglio", "Semaforo del KRI.", "Rosso se valore >= soglia di allerta; Ambra se >= attenzione; Verde sotto; Non rilevato senza valore.", "4 valori", "Ambra"),
    ("Segnali netti 4 sett.", "Registro, Dashboard", "Foglio, dopo il settimanale", "Direzione delle notizie sul rischio.", "Peggiorative meno migliorative delle ultime 4 settimane; badge oltre la soglia di Parametri (3). Non cambia lo score.", "intero", "+3 ▲"),
    ("Validazione", "tutte le tabelle", "Comando valida, dopo il validatore", "Esito della validazione della riga.", "Da validare → Accettato, Rettificato o Respinto.", "4 valori", "Accettato"),
]


def foglio_dizionario(ws):
    ws.sheet_properties.tabColor = TAB["lavoro"]
    larghezze = [22, 20, 22, 34, 58, 12, 22]
    for j, w in enumerate(larghezze, start=1):
        ws.column_dimensions[get_column_letter(j)].width = w
    fascia(ws, 7, "Dizionario dei dati")
    guida(ws, 4, 7, "Ogni dato del registro: dove sta, chi lo scrive e quando, cosa significa, come si calcola, che valori puo' "
                    "avere, un esempio (NFR-01, ciclo 2026Q2). Nel file vero il dizionario si genera dalla mappa delle colonne "
                    "(chiave significato) e dalla rubrica: una sola fonte, sempre allineata.", "calcolo")
    intest = ["Dato", "Dove", "Chi lo scrive, quando", "Che cosa significa", "Come si calcola / regola", "Valori", "Esempio"]
    for j, t in enumerate(intest, start=1):
        cella(ws, 6, j, t, font=Font(bold=True, color="FFFFFF"), fill=fill(BLU_NOTTE), alignment=Alignment(vertical="center"))
    for i, riga in enumerate(DIZIONARIO, start=7):
        chi = riga[2]
        colore = (PROCESSO["validatore"] if chi.startswith(("Validatore", "Comando valida")) else
                  PROCESSO["trimestrale"] if chi.startswith("A1") else PROCESSO["calcolo"])
        for j, v in enumerate(riga, start=1):
            c = cella(ws, i, j, v, font=Font(size=9, bold=j == 1), alignment=Alignment(wrap_text=True, vertical="top"),
                      border=Border(bottom=bordo_sottile))
            if j == 3:
                c.fill = fill(colore[0])
            if i % 2 and j != 3:
                c.fill = fill("FAFAFA")
        ws.row_dimensions[i].height = 13 * max(2, len(riga[4]) // 60 + 1) + 4
    ws.freeze_panes = "B7"
    v1.stampa(ws)
    ws.page_setup.fitToHeight = 0


def foglio_dati(ws, rischi):
    """La tabella dati RiskRegister ridisegnata (nel file vero: tutte le righe di tutti i cicli)."""
    ws.sheet_properties.tabColor = TAB["dati"]
    colonne = g.MAPPA["tabelle"]["tblRegister"]["colonne"]
    gruppi = [("Identita'", ["Ciclo", "Data_Riferimento", "ID_Rischio", "Nome", "Event_Type", "Driver"], "trimestrale"),
              ("Valutazione 1-5 (A1, validata)", ["Severity", "Velocity", "Prossimita", "Gap_Controlli"], "trimestrale"),
              ("Calcolato", ["Score_Composito"], "calcolo"),
              ("Valutazione", ["Confidence", "Probabilita", "Esito"], "trimestrale"),
              ("Testi e fonti (A1)", ["Descrizione", "Razionale", "Variazioni", "Fonti"], "trimestrale"),
              ("Script", ["Owner", "Chiave", "Data_Scrittura"], "calcolo"),
              ("Validazione", ["Approvato_Da", "Validazione", "Data_Validazione"], "validatore")]
    ordine = [c["nome"] for c in colonne]
    larg = {"Nome": 30, "Descrizione": 40, "Razionale": 50, "Variazioni": 34, "Fonti": 34, "Driver": 14}
    for j, nome in enumerate(ordine, start=1):
        ws.column_dimensions[get_column_letter(j)].width = larg.get(nome, 11)
    fascia(ws, 12, "dati: RiskRegister (li scrive solo lo script)")
    guida(ws, 4, 12, "CICLO TRIMESTRALE — una riga per rischio per ciclo, solo in aggiunta: la storia di tutte le valutazioni, con i "
                     "valori validati. Non si modifica a mano. Sopra ogni colonna: chi la scrive · cosa significa. Gruppi di colonne "
                     "e colori come nel resto del file. In anteprima solo le righe del ciclo 2026Q2.", "trimestrale")
    per_nome = {c["nome"]: c for c in colonne}
    for titolo, nomi, processo in gruppi:
        idx = [ordine.index(n) + 1 for n in nomi]
        da, a = min(idx), max(idx)
        if da != a:
            ws.merge_cells(start_row=6, start_column=da, end_row=6, end_column=a)
        for x in range(da, a + 1):
            cella(ws, 6, x, titolo if x == da else None, fill=fill(PROCESSO[processo][0]),
                  font=Font(size=9, bold=True, color=PROCESSO[processo][1]))
    for j, nome in enumerate(ordine, start=1):
        c = per_nome[nome]
        chi = v1.g.chi_colonna("tblRegister", c)
        etichetta = v1.g.ETICHETTA_CHI[chi][1]
        cella(ws, 7, j, f"{etichetta} · {c['significato']}", font=Font(size=7.5, italic=True, color=TESTO_TENUE),
              alignment=Alignment(wrap_text=True, vertical="top"))
        cella(ws, 8, j, nome, font=Font(size=9, bold=True, color="FFFFFF"), fill=fill(BLU_NOTTE))
    ws.row_dimensions[7].height = 62
    reg = [r for r in v1.g.fogli_dati.__globals__["dati_esempio"]()[0] if r["Ciclo"] == "2026Q2"]
    punteggi = {r["id"]: r["score"] for r in rischi}
    for i, r in enumerate(reg):
        riga = 9 + i
        for j, nome in enumerate(ordine, start=1):
            v = punteggi[r["ID_Rischio"]] if nome == "Score_Composito" else (
                f"{r['Ciclo']}|{r['ID_Rischio']}" if nome == "Chiave" else r.get(nome))
            c = cella(ws, riga, j, v, font=Font(size=9), alignment=Alignment(wrap_text=larg.get(nome, 0) >= 30, vertical="top"),
                      border=Border(bottom=bordo_sottile))
            if i % 2:
                c.fill = fill("F7F9FC")
            if nome in ("Data_Riferimento", "Data_Scrittura", "Data_Validazione"):
                c.number_format = "dd/mm/yyyy"
            if nome == "Score_Composito":
                c.number_format = "0.00"
                c.font = Font(size=9, bold=True)
            if nome in ("Severity", "Velocity", "Prossimita", "Gap_Controlli", "Probabilita"):
                c.fill = fill(SCALA[v])
                c.alignment = Alignment(horizontal="center", vertical="top")
        ws.row_dimensions[riga].height = 62
    ws.freeze_panes = "D9"
    v1.stampa(ws)
    ws.page_setup.fitToHeight = 0


def foglio_validazione(ws):
    ws.sheet_properties.tabColor = TAB["lavoro"]
    larghezze = [9, 9, 12, 34, 13, 11, 14, 12, 44, 15, 12, 11]
    for j, w in enumerate(larghezze, start=1):
        ws.column_dimensions[get_column_letter(j)].width = w
    fascia(ws, 12, "Validazione: decisioni sulle proposte degli agenti")
    guida(ws, 4, 6, "OPERAZIONI\n1. Filtra Stato = Da decidere e Periodo = il ciclo (o il lunedi').\n2. Per ogni riga scegli la "
                    "Decisione (celle gialle): Accettato, Rettificato (scrivi il valore giusto) o Respinto.\n3. Con Rettificato o "
                    "Respinto scrivi la Motivazione (almeno 10 caratteri, con l'evidenza).\n4. Salva e CHIUDI il file, poi lancia "
                    "il comando valida.", "validatore", altezza=96)
    ws.merge_cells("G4:L4")
    cella(ws, 4, 7, "CRITERI\nRischio: si rettifica, non si respinge; il valore deve corrispondere al descrittore della rubrica, "
                    "intero 1-5, al massimo un punto dal ciclo prima.\nKRI: respingi se la fonte dati non e' identificabile o se "
                    "non misura il rischio; rettifica soglie o valore.\nAzione: respingi se duplicata o non pertinente; rettifica "
                    "owner (una funzione) o orizzonte.\nNotizia: rettifica rischio o segnale; respingi se non pertinente.",
          fill=fill(PROCESSO["validatore"][0]), font=Font(size=9.5), alignment=Alignment(wrap_text=True, vertical="top", indent=1))
    gruppi = [((1, 6), "La proposta (script, dall'agente)", "calcolo"), ((7, 9), "La tua decisione (da compilare)", "validatore"),
              ((10, 12), "Registrato dal comando valida", "calcolo")]
    for (da, a), t, p in gruppi:
        ws.merge_cells(start_row=6, start_column=da, end_row=6, end_column=a)
        for x in range(da, a + 1):
            cella(ws, 6, x, t if x == da else None, fill=fill(PROCESSO[p][0]), font=Font(size=9, bold=True, color=PROCESSO[p][1]))
    intest = ["Periodo", "Oggetto", "ID", "Nome", "Campo", "Proposta", "Decisione", "Valore validato", "Motivazione",
              "Validato da", "Data", "Stato"]
    for j, t in enumerate(intest, start=1):
        cella(ws, 7, j, t, font=Font(size=9, bold=True, color="FFFFFF"), fill=fill(BLU_NOTTE))
    esempi = [
        ("2026Q3", "Rischio", "NFR-01", "Frodi su pagamenti istantanei abilitate da AI generativa", "Severity", 4, None, None, None, None, None, "Da decidere"),
        ("2026Q3", "Rischio", "NFR-01", "Frodi su pagamenti istantanei abilitate da AI generativa", "Probabilita", 5, "Rettificato", 4,
         "Frequenza di perdite sopra franchigia 1 in 1-2 anni: report frodi del 10/06.", None, None, "Da decidere"),
        ("2026Q3", "KRI", "NFR-06-K2", "Quota di dipendenti senza formazione sull'uso dell'AI", "Soglia_Attenzione", 30, "Rettificato", 20,
         "Soglia allineata all'obiettivo formativo approvato da HR.", None, None, "Da decidere"),
        ("2026Q3", "Azione", "2026Q3-NFR-05-A1", "Monitoraggio giornaliero degli incidenti post-migrazione", "Owner", "Funzione Operations",
         "Respinto", None, "Gia' coperto dal presidio giornaliero del PMO: azione duplicata.", None, None, "Da decidere"),
        ("2026Q2", "Rischio", "NFR-10", "Informazioni errate ai clienti da assistenti di AI generativa", "Probabilita", 4, "Rettificato", 3,
         "Chatbot in produzione da aprile: nessuna frequenza osservata.", "Comitato Rischi", "15/07/2026", "Applicata"),
    ]
    for i, riga in enumerate(esempi, start=8):
        for j, v in enumerate(riga, start=1):
            c = cella(ws, i, j, v, font=Font(size=9), alignment=Alignment(wrap_text=True, vertical="top"), border=Border(bottom=bordo_sottile))
            if j in (7, 8, 9) and riga[-1] == "Da decidere":
                c.fill = fill(AMBRA_TENUE)
        dec = ws.cell(row=i, column=7)
        if riga[6] == "Rettificato":
            dec.font = Font(size=9, bold=True, color=BLU_DIM)
        elif riga[6] == "Respinto":
            dec.font = Font(size=9, bold=True, color=ROSSO)
        st = ws.cell(row=i, column=12)
        st.fill = fill(AMBRA if riga[-1] == "Da decidere" else "E2EFDA")
        st.font = Font(size=9, bold=True)
        ws.row_dimensions[i].height = 30
    dv = DataValidation(type="list", formula1='"Accettato,Rettificato,Respinto"', allow_blank=True)
    ws.add_data_validation(dv)
    dv.add("G8:G12")
    ws.freeze_panes = "A8"
    v1.stampa(ws)


# ============================================================== file delle schede
def scheda(ws, r, kri):
    est = ESTESI.get(r["id"])
    for l, w in zip("ABCDEFGH", [18, 12, 16, 16, 16, 16, 16, 34]):
        ws.column_dimensions[l].width = w
    ws.sheet_view.showGridLines = False
    ws.merge_cells("A1:H1")
    cella(ws, 1, 1, f"{NOME_ANALISI} — scheda del rischio · ciclo 2026Q2 · dati validati", font=Font(size=10, color="FFFFFF"),
          fill=fill(BLU_MEDIO), alignment=Alignment(vertical="center", indent=1))
    ws.merge_cells("A2:F2")
    ws.merge_cells("G2:H2")
    cella(ws, 2, 1, f"{r['rank']} · {r['id']} · {r['nome']}", font=Font(size=14, bold=True, color="FFFFFF"),
          alignment=Alignment(vertical="center", indent=1))
    cella(ws, 2, 7, f"score {num(r['score'])}   {v1.freccia(r['delta'])}   ·   {r['urgenza']}", font=Font(size=12, bold=True, color="FFFFFF"),
          alignment=Alignment(horizontal="right", vertical="center"))
    for j in range(1, 9):
        ws.cell(row=2, column=j).fill = fill(BLU_NOTTE)
    ws.row_dimensions[2].height = 30
    etichette = [((1, 2), f"{r['et']} · {dict(g.TASSONOMIA)[r['et']]}"), ((3, 4), f"Driver: {r['drv']}"), ((5, 6), f"Owner: {r['owner']}"),
                 ((7, 7), "◆ Attenzione del supervisore" if r["vigilanza"] else ""), ((8, 8), f"Esito: {r['esito']} · validato")]
    for (da, a), t in etichette:
        if da != a:
            ws.merge_cells(start_row=3, start_column=da, end_row=3, end_column=a)
        for x in range(da, a + 1):
            ws.cell(row=3, column=x).fill = fill(AMBRA_TENUE if t.startswith("◆") else BLU_CHIARO)
        cella(ws, 3, da, t or None, font=Font(size=9, bold=t.startswith("◆"), color="7F6000" if t.startswith("◆") else TESTO_TENUE),
              alignment=Alignment(vertical="center", wrap_text=True))
    ws.row_dimensions[3].height = 28
    riga = 5

    def titolo(testo):
        nonlocal riga
        v1.sezione(ws, f"A{riga}", f"H{riga}", testo)
        riga += 1

    def testo_lungo(testo, sz=10, fondo=None):
        nonlocal riga
        ws.merge_cells(start_row=riga, start_column=1, end_row=riga, end_column=8)
        cella(ws, riga, 1, testo, font=Font(size=sz), alignment=Alignment(wrap_text=True, vertical="top"), fill=fill(fondo) if fondo else PatternFill())
        ws.row_dimensions[riga].height = 14 * sum(len(p) // 150 + 1 for p in testo.split("\n")) + 6
        riga += 1

    titolo("Il rischio")
    testo_lungo(est["descr"] if est else r["descr"] + "  [Nel file vero: descrizione estesa scritta dall'agente delle schede.]")
    riga += 1
    titolo("Valutazione, dimensione per dimensione")
    for j, t in enumerate(["Dimensione", "Valore", "Perche' (con l'evidenza)"], start=1):
        cella(ws, riga, j, t, font=Font(size=9, bold=True, color=TESTO_TENUE))
    ws.merge_cells(start_row=riga, start_column=3, end_row=riga, end_column=8)
    riga += 1
    pezzi_raz = [p.strip() for p in r["razionale"].split(";")]
    for dim, v in [("severity", r["sev"]), ("probabilita", r["prob"]), ("gap_controlli", r["gap"]), ("velocity", r["vel"]),
                   ("prossimita", r["pro"]), ("confidence", r["conf"])]:
        cella(ws, riga, 1, NOMI_DIM[dim], font=Font(size=10, bold=True, color=BLU_NOTTE), alignment=Alignment(vertical="center"))
        colore = (SCALA_CONF if dim == "confidence" else SCALA)[v]
        cella(ws, riga, 2, v, fill=fill(colore), font=Font(size=14, bold=True, color="FFFFFF" if v == 5 else TESTO),
              alignment=Alignment(horizontal="center", vertical="center"))
        if est:
            spiegazione = est["dim"][dim]
        else:
            chiave = {"severity": "severity", "probabilita": None, "gap_controlli": "gap", "velocity": "velocity",
                      "prossimita": "prossimita", "confidence": None}[dim]
            trovato = next((p for p in pezzi_raz if chiave and p.lower().startswith(chiave)), None)
            spiegazione = trovato or "Nel file vero: spiegazione scritta dall'agente delle schede."
        ws.merge_cells(start_row=riga, start_column=3, end_row=riga, end_column=8)
        cella(ws, riga, 3, spiegazione, font=Font(size=10), alignment=Alignment(wrap_text=True, vertical="center"))
        ws.row_dimensions[riga].height = 30 if len(spiegazione) < 120 else 42
        for x in range(1, 9):
            ws.cell(row=riga, column=x).border = Border(bottom=bordo_sottile)
        riga += 1
    cella(ws, riga, 1, f"Score composito {num(r['score'])} = 0,30 x {r['sev']} + 0,20 x {r['prob']} + 0,20 x {r['gap']} + 0,15 x "
                       f"{r['vel']} + 0,15 x {r['pro']}.  Confidence in blu: solidita' delle fonti, fuori dallo score.",
          font=Font(size=8, italic=True, color=TESTO_TENUE))
    riga += 2
    titolo("Urgenza (disuguaglianza di Mosca)")
    adeg = f" (anni di adeguamento strutturale indicati dal validatore)" if r["adeguamento"] else ""
    testo_lungo(f"{r['urgenza']}. Tempo necessario X + Y = {num(r['x'])} + {num(r['y'])}{adeg} = {num(r['x'] + r['y'])} anni; "
                f"tempo disponibile Z = {num(r['z'], 1)} anni (Prossimita {r['pro']}). Margine Z - (X + Y) = {num(r['margine'])}.",
                fondo=ROSSO_TENUE if r["urgenza"] == "AGIRE ORA" else None)
    riga += 1
    titolo("Cosa e' cambiato nel ciclo")
    testo_lungo(cosa_cambiato(r), sz=10)
    riga += 1
    titolo("Fonti")
    for j, t in zip((1, 4, 5, 6), ["Fonte", "Data", "Tipo", "A sostegno di"]):
        cella(ws, riga, j, t, font=Font(size=9, bold=True, color=TESTO_TENUE))
    ws.merge_cells(start_row=riga, start_column=1, end_row=riga, end_column=3)
    ws.merge_cells(start_row=riga, start_column=6, end_row=riga, end_column=8)
    riga += 1
    for rif, dt, tipo in [f for f in g.FONTI[r["id"]] if f[1] <= "2026-06-30"]:
        ws.merge_cells(start_row=riga, start_column=1, end_row=riga, end_column=3)
        ws.merge_cells(start_row=riga, start_column=6, end_row=riga, end_column=8)
        cella(ws, riga, 1, rif, font=Font(size=10), alignment=Alignment(wrap_text=True, vertical="top"))
        cella(ws, riga, 4, data_it(dt), font=Font(size=10), alignment=Alignment(vertical="top"))
        cella(ws, riga, 5, tipo, font=Font(size=10, bold=True, color=BLU_DIM if tipo == "Interna" else TESTO_TENUE), alignment=Alignment(vertical="top"))
        cella(ws, riga, 6, (est["fonti"].get(rif) if est else None) or "—", font=Font(size=10), alignment=Alignment(wrap_text=True, vertical="top"))
        for x in range(1, 9):
            ws.cell(row=riga, column=x).border = Border(bottom=bordo_sottile)
        ws.row_dimensions[riga].height = 30
        riga += 1
    riga += 1
    titolo("Azioni")
    for a in [a for a in g.AZIONI_ESEMPIO if a[0] == r["id"]]:
        testo_lungo(f"• {a[1]} — {a[2]}, {a[4]}, {a[6]}. Riduce: {a[3]}.")
    riga += 1
    titolo("KRI in vigore")
    for j, t in zip((1, 5, 6, 8), ["Indicatore", "Valore", "Soglie (attenzione / allerta)", "Stato"]):
        cella(ws, riga, j, t, font=Font(size=9, bold=True, color=TESTO_TENUE))
    riga += 1
    semaforo = {"Rosso": (ROSSO, "FFFFFF"), "Ambra": (AMBRA, TESTO), "Verde": ("70AD47", "FFFFFF"), "Non rilevato": ("D9D9D9", TESTO)}
    for k in [x for x in kri if x["rischio"] == r["id"]]:
        ws.merge_cells(start_row=riga, start_column=1, end_row=riga, end_column=4)
        ws.merge_cells(start_row=riga, start_column=6, end_row=riga, end_column=7)
        cella(ws, riga, 1, f"{k['nome']} ({k['unita']})", font=Font(size=10), alignment=Alignment(wrap_text=True))
        cella(ws, riga, 5, k["valore"], font=Font(size=10, bold=True), alignment=Alignment(horizontal="center"))
        cella(ws, riga, 6, f"{k['att']} / {k['all']}", font=Font(size=10), alignment=Alignment(horizontal="center"))
        f_, t_ = semaforo[k["stato"]]
        cella(ws, riga, 8, k["stato"], fill=fill(f_), font=Font(bold=True, color=t_), alignment=Alignment(horizontal="center"))
        ws.row_dimensions[riga].height = 20
        riga += 1
    ws.page_setup.orientation = "portrait"
    ws.page_setup.paperSize = ws.PAPERSIZE_A4
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.oddFooter.left.text = "Anteprima di stile — dati di esempio"
    ws.oddFooter.right.text = "Pagina &P di &N"


def file_schede(rischi, kri):
    wb = Workbook()
    ws = wb.active
    ws.title = "Indice"
    fascia(ws, 7, "Schede dei rischi del ciclo 2026Q2")
    for l, w in zip("ABCDEFG", [6, 10, 52, 9, 16, 22, 30]):
        ws.column_dimensions[l].width = w
    guida(ws, 4, 7, "File a parte rispetto al registro: una scheda per rischio, nell'ordine della classifica. A tendere lo "
                    "produce un agente dedicato partendo dal registro validato (descrizione estesa, razionale per dimensione, "
                    "fonti e cosa sostengono); in questa anteprima i testi estesi ci sono per NFR-01, NFR-07, NFR-11 e NFR-12, "
                    "gli altri usano i testi brevi del registro. Clic sull'ID per aprire la scheda.", "trimestrale")
    for j, t in enumerate(["#", "ID", "Rischio", "Score", "Urgenza", "Esito", "Testo"], start=1):
        cella(ws, 6, j, t, font=Font(bold=True, color="FFFFFF"), fill=fill(BLU_NOTTE))
    for r in rischi:
        riga = 6 + r["rank"]
        cella(ws, riga, 1, r["rank"], font=Font(bold=True, color=BLU_NOTTE))
        c = cella(ws, riga, 2, r["id"], font=Font(bold=True, color=BLU_DIM, underline="single"))
        c.hyperlink = f"#'{r['id']}'!A1"
        cella(ws, riga, 3, r["nome"] + ("  ◆" if r["vigilanza"] else ""))
        cella(ws, riga, 4, r["score"], number_format="0.00", font=Font(bold=True))
        v1.chip_urgenza(ws.cell(row=riga, column=5), r["urgenza"])
        cella(ws, riga, 6, r["esito"])
        cella(ws, riga, 7, "esteso (esempio dell'agente)" if r["id"] in ESTESI else "breve (dal registro)",
              font=Font(size=9, italic=True, color=TESTO_TENUE))
        for x in range(1, 8):
            ws.cell(row=riga, column=x).border = Border(bottom=bordo_sottile)
        ws.row_dimensions[riga].height = 20
    v1.stampa(ws)
    for r in rischi:
        scheda(wb.create_sheet(r["id"]), r, kri)
    wb.save(USCITA_SCHEDE)


def main():
    rischi, kri = dati()
    wb = Workbook()
    nomi = ["Come valutare", "Struttura proposta", "Sintesi", "Sintesi (perche')", "Classifica", "Radar", "Matrice", "Delta",
            "Registro", "Validazione", "Dizionario", "Dati_RiskRegister"]
    fogli = {nomi[0]: wb.active}
    wb.active.title = nomi[0]
    for n in nomi[1:]:
        fogli[n] = wb.create_sheet(n)
    foglio_valuta(fogli["Come valutare"])
    foglio_struttura(fogli["Struttura proposta"])
    info = foglio_radar(fogli["Radar"], rischi)
    foglio_sintesi(fogli["Sintesi"], rischi, kri, fogli["Radar"], info)
    foglio_sintesi_perche(fogli["Sintesi (perche')"], rischi, kri)
    foglio_matrice(fogli["Matrice"], rischi)
    foglio_registro(fogli["Registro"], rischi)
    foglio_validazione(fogli["Validazione"])
    foglio_dizionario(fogli["Dizionario"])
    foglio_dati(fogli["Dati_RiskRegister"], rischi)
    # Classifica e Delta della v1 (con la fascia nuova): li crea la v1 in coda, poi si spostano al loro posto.
    for n, f in (("Classifica", v1.foglio_classifica), ("Delta", v1.foglio_delta)):
        wb.remove(fogli[n])
        f(wb, rischi)
        wb[n].sheet_properties.tabColor = TAB["report"]
    wb._sheets.sort(key=lambda s: nomi.index(s.title))
    wb.active = 2
    wb.save(USCITA_REGISTRO)
    v1.trasparenza(USCITA_REGISTRO, v1.RIEMPIMENTO_CERCHIO)
    file_schede(rischi, kri)
    print(f"Anteprima v2 scritta:\n  {USCITA_REGISTRO}\n  {USCITA_SCHEDE}")


if __name__ == "__main__":
    main()
