"""Genera il template del workbook NFR (NFR_Dashboard_Template.xlsx).

Uso:
    python genera_dashboard.py [percorso_output.xlsx]

Dipendenza: openpyxl (solo per GENERARE il template; il sistema in esercizio
non richiede Python per leggere il workbook).

Principi, tutti da errori reali (vedi 00_LEGGIMI.md):
- Due livelli. DATI: quattro tabelle (tblRegister, tblAzioni, tblKRI, tblNews),
  l'unico posto dove si scrive. VISTA: fogli di sole formule che leggono i dati;
  appendendo una riga le viste si aggiornano da sole.
- Le colonne delle tabelle NON sono elencate qui: vengono da
  01_Kernel/mappatura_campi.json, la stessa mappa che usa lo scrittore.
- Le formule di vista usano nomi definiti su intervalli ASSOLUTI (RR_ID_Rischio =
  RiskRegister!$C$2:$C$20000), mai riferimenti strutturati di tabella, che si
  comportano in modo diverso fra Excel desktop, web e altri motori.
- Assi dei grafici a scala FISSA (0-5 per gli score, 0-3 per l'impatto news).
- Chi non e' valutato mostra #N/A (vuoto sul grafico), non zero: uno zero sul
  radar si legge "rischio nullo". Il controllo di copertura del Registro (righe
  4-5, nomi coperturaAnagrafica e coperturaValutati) resta comunque il presidio
  principale contro un ciclo scritto a meta'.
- Un solo file (DECISIONI D-39): Guida; report al comitato (Quadro..Metodologia);
  fogli di lavoro (Registro..Dizionario); tabelle dati in fondo. Le schede dei
  rischi sono un file a parte (comando schede, agente A6).
- Fascia del titolo in riga 1 con ciclo, data, stato di validazione e
  riservatezza (nome etichettaCiclo). Guida in testa a ogni foglio (riga 2: chi
  lo aggiorna, cosa contiene, come si legge, cosa fare), mai sotto una tabella:
  una tabella che cresce la inglobera' come riga di dati. Le tabelle dati hanno
  l'intestazione in riga 5: sopra, in riga 3, il gruppo di chi scrive le colonne
  e, in riga 4, il significato di ogni colonna (dalla mappa).
- Dati di ESEMPIO su fondo grigio: da eliminare al primo uso reale.
"""

import json
import sys
from datetime import date, timedelta
from pathlib import Path

from openpyxl import Workbook
from openpyxl.cell.rich_text import CellRichText, TextBlock
from openpyxl.cell.text import InlineFont
from openpyxl.chart import BarChart, LineChart, Reference, ScatterChart, Series
from openpyxl.chart.data_source import AxDataSource, StrRef
from openpyxl.chart.label import DataLabel, DataLabelList
from openpyxl.chart.layout import Layout, ManualLayout
from openpyxl.chart.series import SeriesLabel
from openpyxl.chart.shapes import GraphicalProperties
from openpyxl.chart.text import RichText, Text
from openpyxl.chart.title import Title
from openpyxl.drawing.line import LineProperties
from openpyxl.drawing.text import CharacterProperties, Paragraph, ParagraphProperties
from openpyxl.formatting.rule import DataBarRule, FormulaRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.workbook.defined_name import DefinedName
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.worksheet.pagebreak import Break
from openpyxl.worksheet.table import Table, TableStyleInfo

QUI = Path(__file__).resolve().parent
sys.path.insert(0, str(QUI.parent / "07_Senza_Studio"))
import radar  # noqa: E402  regola del registro unico (D-79): la stessa dello script

MAPPA = json.loads((QUI.parent / "01_Kernel" / "mappatura_campi.json").read_text(encoding="utf-8"))

# Capacita' fissate dal disegno. Se si superano, lo scrittore si ferma con un
# messaggio (non tronca in silenzio): allora si alza il valore e si rigenera.
MAX_RIGHE = 20000   # righe dati coperte dai nomi definiti delle colonne
MAX_RISCHI = 20     # righe dell'anagrafica e delle viste per rischio (i grafici si adattano al numero reale; D-55)
MAX_KRI_CORRENTI = 60   # righe di KRI_Correnti (20 rischi x 2 KRI dal D-64; resta 60 per i registri con 3 KRI di prima)
MAX_ELENCO_KRI = 150    # KRI distinti mai definiti, nell'elenco a discesa del foglio Indicatori
# Le due capacita' qui sopra sono scritte nel workbook come nomi definiti
# (capienzaKRICorrenti, capienzaElencoKRI): lo scrittore si ferma prima di superarle.

# Prefisso dei nomi definiti per colonna: RR_Impatto, KRI_Stato, NW_Segnale...
PREFISSI = {"tblRegister": "RR", "tblAzioni": "AZ", "tblKRI": "KRI", "tblNews": "NW", "tblValidazione": "VAL",
            "tblSintesi": "SI", "tblSettimane": "SE"}

# Versione della STRUTTURA del workbook (fogli, colonne, nomi). Scritta come nome
# definito 'versioneTemplate': lo script di campo si ferma su un registro creato
# con un template piu' vecchio e indica il comando aggiorna-registro. Va alzata a
# ogni modifica di struttura (non per un cambio di soli dati di esempio), insieme a
# VERSIONE_TEMPLATE in 07_Senza_Studio/esegui_ciclo_locale.py.
VERSIONE_TEMPLATE = "2026-10-09"
# Tabelle dati: riga 1 titolo, riga 2 guida, riga 3 gruppi di colonne per chi le
# scrive, riga 4 significato delle colonne, riga 5 intestazione, dati dalla riga 6
# (i nomi definiti delle colonne partono da qui).
RIGA_INTESTAZIONE = 5
PRIMA_RIGA_DATI = RIGA_INTESTAZIONE + 1
# Intestazione delle pagine stampate (report al comitato): adattarla
# all'etichetta di riservatezza della Banca.
ETICHETTA_RISERVATEZZA = "Uso interno"
NOME_ANALISI = "Horizon Scan NFR"

TASSONOMIA = [
    # D-74: categorie in perimetro della tassonomia interna della Banca (01_Kernel/tassonomia_nfr.md).
    ("9.1", "Condotta"),
    ("9.4", "Legale"),
    ("9.5", "Fiscale"),
    ("9.6", "Tecnologico"),
    ("9.7", "Sicurezza informatica"),
    ("9.8", "Sicurezza fisica"),
    ("9.9", "Terze parti"),
    ("9.11", "Employer"),
    ("9.13", "Processo"),
]
DRIVER = [
    ("DRV-CYB", "Cyber"), ("DRV-TPR", "Terze parti"),
    ("DRV-AI", "Intelligenza artificiale"), ("DRV-CLI", "Clima e ambiente"),
    ("DRV-CON", "Condotta"), ("DRV-GEO", "Geopolitica"),
    ("DRV-TEC", "Debito tecnologico"), ("DRV-HUM", "Capitale umano"),
]
SEGNALI = ["Peggiorativo", "Migliorativo", "Neutro", "Non rilevante"]
MAX_OSSERVAZIONE = 20                                         # rischi in osservazione al massimo (D-79)
CAPIENZA_RADAR = 15                                           # rischi nel radar all'inizio (D-79), fino a MAX_RISCHI
STATI_REGISTRO = ["Radar", "Radar, in uscita", "Osservazione", "Dismesso"]   # colonna Stato del RiskRegister (D-79)
DECISIONI_STATO = ["Automatico", "Radar", "Osservazione"]     # decisione del validatore sullo stato (D-79)
STATI_AZIONE = ["Proposta — da valutare", "Approvata", "Respinta", "In corso", "Completata", "Annullata"]

# ---------------------------------------------------------------- stili
GRIGIO = PatternFill("solid", fgColor="E7E6E6")      # dati di esempio
INPUT = PatternFill("solid", fgColor="FFF2CC")       # celle di input
TITOLO = Font(bold=True, size=14, color="1F3864")
GRASSETTO = Font(bold=True)
NOTA = Font(italic=True, color="595959")
A_CAPO = Alignment(wrap_text=True, vertical="top")
# Riempimenti dei formati condizionali: Excel li disegna con il colore di SFONDO (bgColor);
# con il solo fgColor la cella resta bianca. Si impostano entrambi.
ROSSO_CF = PatternFill("solid", fgColor="F8CBAD", bgColor="F8CBAD")
VERDE_CF = PatternFill("solid", fgColor="C6EFCE", bgColor="C6EFCE")
AMBRA_CF = PatternFill("solid", fgColor="FFEB9C", bgColor="FFEB9C")
AZZURRO_CF = PatternFill("solid", fgColor="DDEBF7", bgColor="DDEBF7")
GIALLO_CF = PatternFill("solid", fgColor="FFF2CC", bgColor="FFF2CC")   # da decidere dal validatore (es. soglie da definire)
FONT_NA = Font(color="BFBFBF")

# Chi aggiorna che cosa: un colore per processo, lo stesso in guide, intestazioni
# delle colonne e tabella "chi aggiorna cosa" del Leggimi.
#   chiave: (fondo chiaro, colore del testo, etichetta)
PROCESSI = {
    "trimestrale": ("DDEBF7", "1F4E79", "CICLO TRIMESTRALE"),   # A1 valuta, A5 controlla, lo script scrive
    "settimanale": ("E2EFDA", "375623", "CICLO SETTIMANALE"),   # A3 valuta le notizie, lo script scrive
    "validazione": ("FFF2CC", "7F6000", "VALIDATORE"),          # decisione umana: stesso giallo delle celle di input
    "calcolo": ("EDEDED", "404040", "CALCOLO"),                 # script o formula, nessun giudizio
    "misto": ("F2F2F2", "262626", ""),
}
# Chi scrive una colonna delle tabelle dati (intestazione colorata, riga del significato).
ETICHETTA_CHI = {"A1": ("trimestrale", "A1"), "A5": ("trimestrale", "A5"), "A3": ("settimanale", "A3"),
                 "script": ("calcolo", "Script"), "formula": ("calcolo", "Formula"),
                 "validazione": ("validazione", "Validazione"), "validatore": ("validazione", "Validatore")}
# Colonne che registrano l'esito della validazione (le scrive il comando valida, o a mano lo Stato delle azioni).
COLONNE_VALIDAZIONE = {
    "tblRegister": {"Approvato_Da", "Validazione", "Data_Validazione", "Decisione_Stato"},
    "tblAzioni": {"Stato", "Data_Decisione", "Decisa_Da", "Validazione"},
    "tblKRI": {"Validazione"}, "tblNews": {"Validazione"},
}
LEGENDA_COLORI = ("Colore delle intestazioni = chi scrive la colonna: azzurro l'agente del ciclo trimestrale (A1, A5), "
                  "verde l'agente settimanale (A3), giallo la validazione, grigio lo script o una formula.")
NON_A_MANO = ("Si scrive con lo script (le viste e la baseline leggono queste righe): a mano solo i testi elencati nel foglio "
              "Guida, DOVE SI SCRIVE A MANO; mai ID, numeri, date o righe intere (D-76).")
# Fascia dei gruppi di colonne delle tabelle dati (riga 3): chi scrive, quando.
GRUPPO_CHI = {"A1": "ciclo trimestrale, poi validato", "A5": "ciclo trimestrale", "A3": "ciclo settimanale",
              "script": "alla scrittura", "formula": "calcolata dal foglio", "validazione": "comando valida",
              "validatore": "a mano, dopo il ciclo"}

# Guida in testa a ogni foglio (riga 2): (processo che lo aggiorna, righe). La prima
# riga, in grassetto, dice chi agisce e quando; poi cosa contiene, come si legge,
# cosa fare. I fogli del report (Sintesi..Metodologia) si stampano: il testo e' per il comitato.
GUIDE = {
    # ---------------------------------------------------------------- report al comitato
    "Quadro": ("trimestrale", [
        "CICLO TRIMESTRALE — A1 valuta i rischi, lo script la controlla (e A5, se usato), il validatore la conferma o la "
        "rettifica.",
        "Come si legge: i cinque riquadri in alto dicono se il ciclo e' completo e validato; poi le priorita' per score, la "
        "gravita' (matrice) e l'urgenza (radar). A pagina 2 il commento di A1 (scritto prima della validazione: se dopo ci "
        "sono state rettifiche lo dice la riga \"Dopo il commento\" e valgono i numeri validati), le segnalazioni portate "
        "in validazione e i rischi segnalati, con il perche' calcolato dal foglio. Metodo e scale: Metodologia; ogni dato: "
        "Dizionario. Note dell'analista (cella gialla in prima pagina): testo libero scritto a mano, per esempio la "
        "sintesi delle spiegazioni chieste ad A7; a un ciclo nuovo passa nel foglio Sintesi_Cicli."]),
    "Classifica": ("trimestrale", [
        "CICLO TRIMESTRALE — calcolato dal foglio sui valori del ciclo; nessun agente ordina o stima l'urgenza.",
        "Come si legge: un rischio per barra, dal piu' alto per score composito (1-5, 5 = peggiore). Colore = urgenza di "
        "Mosca: rosso agire ora, ambra entro l'anno, grigio c'e' margine. A destra la lente di Mosca spiega il colore: "
        "tempo necessario per decidere e mitigare (X + Y) contro tempo prima che il rischio possa manifestarsi (Z)."]),
    "Radar_Mosca": ("trimestrale", [
        "CICLO TRIMESTRALE — calcolato dal foglio: Z dalla Prossimita', Y dalle azioni o dagli anni di adeguamento.",
        "Come si legge: piu' vicino al centro = agire prima. Dentro il cerchio rosso (X + Y > Z) si e' gia' in ritardo "
        "anche se l'evento non e' imminente. Area del cerchio = Probabilita x Impatto; colore = livello di allerta "
        "(rosso attivazione, giallo attenzione, verde monitoraggio: colonne U-AB); ◆ = tema all'attenzione del "
        "supervisore; settore = categoria di rischio. Parametri: foglio Parametri, righe 47-63."]),
    "Matrice": ("trimestrale", [
        "CICLO TRIMESTRALE — calcolata dal foglio sui valori validati di Probabilita e Impatto.",
        "Come si legge: ogni rischio nella cella della sua Probabilita (righe) e Impatto (colonne); colore = P x I (verde "
        "fino a 6, ambra 8-12, rosso da 15). Dice la gravita', non l'urgenza (quella e' nel radar). Sotto, i rischi dal "
        "piu' grave."]),
    "Delta": ("trimestrale", [
        "CICLO TRIMESTRALE — solo formule: ciclo corrente contro il precedente.",
        "Come si legge: una barra per rischio, dalla variazione piu' alta dello score composito; rosso in aumento, blu in "
        "diminuzione, grigio invariato. A fianco, nello stesso ordine, il motivo con l'evidenza e la sua data; sotto, "
        "quanto vale un punto di ogni dimensione e il dettaglio per dimensione (la Nota segnala una violazione della "
        "regola del punto). Velocity n.v. = non valutata in uno dei due cicli."]),
    "Fenomeni": ("trimestrale", [
        "CICLO TRIMESTRALE — A1 valuta i rischi in osservazione quando trova evidenza nuova, il validatore decide; lo stato "
        "(radar o osservazione) lo calcola lo script con la regola di Parametri (D-79).",
        "I rischi del registro rimasti fuori dal radar: stessa scala e stesso score dei rischi del radar, niente KRI ne' "
        "azioni. Per ognuno: perche' e' fuori (quale soglia di Prossimita o Probabilita manca, o la capienza), "
        "l'orizzonte stimato e il segnale che lo farebbe salire. Dal piu' alto per score; in fondo chi e' entrato o uscito "
        "dal radar nel ciclo."]),
    "Metodologia": ("calcolo", [
        "COME SI LEGGONO I NUMERI DEL REPORT — scale e regole dalla rubrica del pacchetto, pesi e parametri letti dal "
        "foglio Parametri: sono sempre quelli in vigore.",
        "Nessun punteggio composito, urgenza o stato di un KRI e' stimato da un agente: li calcola il foglio."]),
    # ---------------------------------------------------------------- lavoro
    "Registro": ("misto", [
        "CICLO TRIMESTRALE (dimensioni, score, urgenza, KRI, rilievi) · CICLO SETTIMANALE (colonna Q: segnali netti) · "
        "VALIDATORE (riga 4, presidio e anagrafica).",
        "Come si legge: prima le righe 4 e 5 — se il ciclo non e' validato o e' incompleto i numeri non sono definitivi. "
        "Un rischio per riga, dal piu' alto per score. Punteggi 1-5, 5 = peggiore; #N/A = non valutato, non zero; "
        "Velocity n.v. = nessuna fonte ne documenta i tempi (lo score usa le altre tre). Presidio = giudizio della Banca "
        "sui controlli, fuori dallo score. Rilievi = segnalazioni di A5 e dei controlli (⚑ = da motivare in validazione). "
        "Segnali netti = notizie peggiorative meno migliorative delle ultime 4 settimane (▲ ▼ oltre la soglia di "
        "Parametri): e' un allarme per il prossimo trimestre, non cambia lo score. L'andamento di un rischio e' nella sua "
        "scheda (file delle schede)."]),
    "Storico": ("trimestrale", [
        "CICLO TRIMESTRALE — solo formule: score composito di ogni rischio negli ultimi otto cicli.",
        "Scala fissa 0-5. Un punto mancante = rischio non valutato in quel ciclo, non score zero. I cicli passati sono "
        "ricalcolati con i pesi in vigore: il trend resta confrontabile."]),
    "Indicatori": ("trimestrale", [
        "CICLO TRIMESTRALE — solo formule: a sinistra i KRI in vigore nel ciclo corrente (A1 rilegge il valore a ogni "
        "ciclo); a destra la storia di un KRI, da scegliere in N4 (unica cella gialla; anche uno uscito di vigore).",
        "Stato: Verde sotto la soglia di attenzione, Ambra fino all'allerta, Rosso oltre, Non rilevato senza valore (mai "
        "zero), Soglie da definire finche' la Banca non le fissa in validazione. Tendenza sul ciclo prima: valori "
        "crescenti = peggio (▲ peggiora)."]),
    "Notizie": ("settimanale", [
        "CICLO SETTIMANALE — solo formule sulle notizie delle ultime 4 settimane (foglio NewsLog, scritto dopo A3).",
        "Per categoria quante notizie e quanto forti. AREA NON PRESIDIATA = notizie di intensita' 2 o piu' su una "
        "categoria senza rischi nel registro: tema da portare al prossimo ciclo trimestrale; In osservazione = nessun "
        "rischio nel radar, almeno uno in osservazione (D-79). Le notizie non cambiano score. "
        "A destra la sintesi di A3 della settimana corrente e i flag proposti, anche sui rischi in osservazione (foglio "
        "Sintesi_Settimane, D-66, D-79); in rosso la proposta di ciclo straordinario (D-75). "
        "A4 (pareri su richiesta) non scrive nel workbook."]),
    "Piano_azioni": ("validazione", [
        "CICLO TRIMESTRALE (A1 propone) · VALIDATORE (decide nel foglio Validazione; poi aggiorna lo Stato nel foglio Azioni).",
        "Tutte le azioni: prima le proposte da decidere, poi le altre. La validazione e' la delibera (Accettato o "
        "Rettificato = Approvata, Respinto = Respinta); In corso e Completata si scrivono a mano nella colonna Stato del "
        "foglio Azioni, quando l'owner lo comunica. Scadenza = data della decisione + orizzonte. Le azioni aperte passano "
        "ad A1 nel trimestre dopo."]),
    "Osservazione": ("trimestrale", [
        "CICLO TRIMESTRALE — solo formule sui rischi in osservazione del ciclo corrente (foglio RiskRegister, colonna "
        "Stato; registro unico, D-79).",
        "A sinistra i rischi fuori dal radar con le quattro dimensioni, lo score, il motivo dello stato, l'orizzonte e il "
        "segnale di avvicinamento, il razionale di A1; colonna O le notizie che A3 ha collegato a ogni rischio nelle ultime "
        "4 settimane. A destra dove si concentrano: rischi in osservazione per driver e categoria e, sotto, i rischi del "
        "radar con lo stesso incrocio. Si validano nel foglio Validazione con gli altri rischi; si leggono nel report "
        "alla pagina Fenomeni."]),
    "Dizionario": ("calcolo", [
        "OGNI DATO DEL WORKBOOK — chi lo scrive e quando (colore del processo), che cosa significa, come si calcola, "
        "valori ammessi, un esempio.",
        "Le colonne delle tabelle dati vengono dalla mappa dei campi del pacchetto (01_Kernel/mappatura_campi.json): "
        "sono sempre quelle in uso."]),
    "Parametri": ("validazione", [
        "CELLE GIALLE = INPUT, decisi dalla funzione di rischio e registrati in DECISIONI.md.",
        "Pesi, soglie e parametri dell'urgenza valgono per tutti i cicli, passati compresi. Ciclo e settimana correnti li "
        "scrive lo script. Nessuna costante e' nascosta nelle formule. Righe 65-75: la regola del registro unico, chi "
        "entra nel radar di Mosca (D-79)."]),
    # ---------------------------------------------------------------- dati
    "RiskRegister": ("trimestrale", [
        "CICLO TRIMESTRALE — lo script scrive la valutazione di A1 dopo i suoi controlli (e A5, se usato); il comando "
        "valida applica le decisioni del validatore. " + NON_A_MANO,
        "Cosa contiene: una riga per rischio per ciclo, solo in aggiunta: la storia di tutte le valutazioni, con i valori "
        "VALIDATI (la proposta dell'agente resta nel foglio Storico_Validazioni).",
        "Come si legge: quattro dimensioni intere 1-5 (5 = peggiore; la Velocity puo' mancare) con i descrittori del "
        "foglio Metodologia; Score_Composito = media pesata delle dimensioni valutate con i pesi di Parametri; ogni "
        "fonte ha una rilevanza 1-3 (colonna Fonti); Anni_Adeguamento = stima di A1. Fra due cicli ogni valore cambia al "
        "massimo di un punto e cita "
        "un'evidenza datata. Esito e \"da/a\" delle variazioni li calcola lo script; Rilievi = segnalazioni di A5 e dei "
        "controlli sul rischio (⚑ DA MOTIVARE = la validazione chiede una Motivazione), le stesse della colonna "
        "Segnalazioni del foglio Validazione. Registro unico (D-79): Stato = Radar (gestione completa), Radar, in uscita "
        "(sotto la regola per il primo ciclo) o Osservazione (fuori dal radar, niente KRI ne' azioni), con il motivo; "
        "Movimento = Entrato o Uscito dal radar nel ciclo; Decisione_Stato = scelta del validatore (Automatico = vale la "
        "regola). Orizzonte_Anni e Segnale_Avvicinamento: note di A1 per i rischi in osservazione.",
        LEGENDA_COLORI + " Righe grigie = dati di esempio."]),
    "Azioni": ("trimestrale", [
        "CICLO TRIMESTRALE — A1 propone da 1 a 5 azioni per rischio; la validazione e' la delibera (Accettato o "
        "Rettificato = Approvata, Respinto = Respinta).",
        "Mesi_Orizzonte alimenta la Y di Mosca: l'orizzonte piu' lungo fra le azioni del ciclo non respinte. Le azioni "
        "non Completate, Respinte o Annullate passano ad A1 come aperte nel ciclo dopo. Vista d'insieme: Piano_azioni.",
        "Modifiche a mano: la colonna Stato di un'azione approvata (In corso, Completata), quando l'owner lo "
        "comunica, e i testi Descrizione e Razionale (D-76). Owner e orizzonte di un'azione gia' decisa: comando riapri e "
        "validazione. Il resto si scrive solo con lo script.",
        LEGENDA_COLORI + " Righe grigie = dati di esempio."]),
    "KRI": ("trimestrale", [
        "CICLO TRIMESTRALE — A1 propone due KRI per rischio, uno di esposizione e uno di evoluzione (colonna Tipo, D-64; con "
        "le soglie solo se una fonte le sostiene) e rilegge "
        "i valori che trova; la validazione puo' rettificare valori e soglie o respingere un KRI. " + NON_A_MANO,
        "Cosa contiene: lo STORICO, una riga per KRI per ciclo (la fotografia del ciclo). Valore_Corrente e' il valore "
        "rilevato in quel ciclo: vuoto se non rilevato, mai ricopiato. In_Vigore = No: il KRI esce in quel ciclo.",
        "Come si legge: valori crescenti = peggio (un indicatore 'piu' alto e' meglio' si esprime come complemento). "
        "Stato: Verde sotto la soglia di attenzione, Ambra fino all'allerta, Rosso oltre; Soglie da definire: le fissa il "
        "validatore (rettifica di entrambe le soglie); SOGLIE INVERTITE va rettificato. I KRI del ciclo e la storia di "
        "uno: foglio Indicatori.",
        LEGENDA_COLORI + " Righe grigie = dati di esempio."]),
    "NewsLog": ("settimanale", [
        "CICLO SETTIMANALE — le notizie raccolte ogni giorno le valuta A3 il lunedi'; lo script le aggiunge senza "
        "duplicati. Validazione delle notizie facoltativa. " + NON_A_MANO,
        "Come si legge: Segnale = direzione per il rischio collegato (quattro valori, contati per testo esatto); "
        "Imp_ = intensita' 0-3 sulla categoria, senza segno. Le notizie non cambiano score: alimentano i segnali "
        "netti del Registro e il foglio Notizie. NON PRESIDIATO = tema senza rischio censito. Una notizia respinta "
        "diventa Non rilevante con impatti 0.",
        LEGENDA_COLORI + " Righe grigie = dati di esempio."]),
    "Sintesi_Settimane": ("settimanale", [
        "CICLO SETTIMANALE — lo script scrive una riga per settimana con la sintesi di A3 e i flag proposti (D-66); "
        "rilanciare la stessa settimana aggiorna la riga. " + NON_A_MANO,
        "Come si legge: la sintesi e' scritta da A3 PRIMA della validazione delle notizie (i numeri validati sono nei "
        "fogli Notizie e Registro). Un flag non cambia nessuno score: e' un tema da portare al prossimo ciclo "
        "trimestrale o, se critico, la proposta di un ciclo straordinario (D-41). Il foglio Notizie mostra la "
        "settimana corrente.",
        LEGENDA_COLORI + " Righe grigie = dati di esempio."]),
    "Sintesi_Cicli": ("trimestrale", [
        "CICLO TRIMESTRALE — lo script scrive una riga per ciclo con il commento di A1 per il comitato e la sintesi di A5 "
        "(se usato). " + NON_A_MANO,
        "Il commento di A1 ha la forma \"MESSAGGIO: ... DECISIONI: ...\": il Quadro lo divide in due righe. E' scritto "
        "PRIMA della validazione: il Quadro avvisa se dopo sono state applicate rettifiche. Rilievi_Ciclo: segnalazioni di "
        "A5 e dei controlli sul ciclo; Rilievi_Superati: quante segnalazioni sono da motivare in validazione (D-71; fino al "
        "05/10/2026: bloccanti di A5 superati con --procedi-con-rilievi).",
        LEGENDA_COLORI]),
    "Validazione": ("validazione", [
        "VALIDATORE — dopo ogni ciclo trimestrale (obbligatorio: il ciclo dopo non parte finche' non e' validato) e, se si "
        "vuole, dopo ogni settimana per le notizie. Qui ci sono solo i periodi ancora da validare (riga 3). Per cambiare "
        "valori di un ciclo GIA' VALIDATO: python esegui_ciclo_locale.py riapri (D-76), poi qui come sempre e valida, "
        "quante volte serve; in riapertura il grigio e' il valore validato, non c'e' il limite di un punto e Respingi = Sì "
        "toglie un KRI o annulla un'azione.",
        "Come si valida: una riga per rischio (nel radar o in osservazione), KRI, azione e notizia. Le celle GIALLE contengono gia' i valori proposti "
        "dagli agenti (accanto, in grigio, la proposta): se sei d'accordo non toccarle, la riga vale come accettata. Se non "
        "sei d'accordo scrivi il valore giusto nella cella gialla (anche piu' di uno nella stessa riga) e il perche' in "
        "Motivazione, almeno 10 caratteri: la cella cambiata diventa arancio, la Motivazione resta rossa finche' manca. "
        "Per togliere un KRI, un'azione o una notizia: Respingi = Sì, con la motivazione (un rischio non si respinge: si "
        "rettifica, o si toglie con il comando dismetti). Segnalazioni dei controlli (ultima colonna dei rischi): cio' che "
        "lo script e A5 (se usato) hanno trovato su quel rischio, anche sui suoi KRI e azioni; ⚑ davanti al nome = almeno "
        "una segnalazione DA MOTIVARE: la Motivazione e' obbligatoria anche se non cambi nulla. Score composito e Margine "
        "di Mosca si ricalcolano mentre scrivi, con i valori gialli e le azioni non respinte: rosso AGIRE ORA, giallo "
        "entro l'anno, verde con margine; tra parentesi il valore con le sole proposte, se diverso.",
        "Poi salvare e CHIUDERE il file e lanciare  python esegui_ciclo_locale.py valida --periodo <ciclo o lunedi'> "
        "--validatore \"<funzione>\". Il comando controlla tutte le righe prima di applicarne una (se una non va, non "
        "applica niente e le elenca con il numero di riga); poi le righe del periodo escono da questo foglio e il dettaglio "
        "campo per campo (proposta, valore deciso, motivazione, chi e quando) resta nel foglio Storico_Validazioni. Le "
        "colonne grigie si leggono soltanto; non inserire ne' cancellare righe (se succede: python esegui_ciclo_locale.py "
        "griglia ricostruisce il foglio e conserva cio' che hai gia' scritto).",
        "Criteri — Rischio: il punteggio corrisponde al descrittore della rubrica, dati razionale e fonti (foglio "
        "Metodologia); un valore cambiato e' intero 1-5, al massimo un punto dal ciclo precedente (non in riapertura), motivato con un'evidenza "
        "(la Velocity puo' restare vuota = non valutata, o entrare con qualunque valore); anni di adeguamento da 0 a 30 o "
        "vuoti. KRI: respingere se la fonte dati non e' identificabile o se non misura il rischio; cambiare le soglie "
        "(entrambe; allerta >= attenzione, crescente = peggio; vuote = da definire) o un valore rilevato errato. Azione: "
        "respingere se duplicata o non pertinente al rischio; cambiare Owner (una funzione: il nome di una persona non si "
        "accetta) o Orizzonte (3, 6 o 12 mesi). Notizia: cambiare Rischio o Segnale; respingere se non pertinente o gia' "
        "contata. Stato del rischio (D-79): la colonna Stato dice dove lo mette la regola e perche'; Decisione sullo stato "
        "= Automatico (vale la regola), Radar (resta o entra nel radar) o Osservazione (resta fuori), con la Motivazione; "
        "lo stato si ricalcola con valida.",
        "Prima di decidere leggere i rilievi di A5 e dei controlli (colonna Rilievi del RiskRegister; rilievi del ciclo "
        "in Sintesi_Cicli; file Esito_controlli del ciclo). La proposta dell'agente non si cancella mai: le rettifiche "
        "motivate servono a migliorare gli agenti."]),
    "Storico_Validazioni": ("validazione", [
        "COMANDO VALIDA — la scrittura (trimestrale, settimanale) aggiunge una riga Da decidere per ogni campo proposto; il "
        "comando valida la compila dalla griglia del foglio Validazione e la mette Applicata. " + NON_A_MANO,
        "Cosa contiene: una riga per oggetto e campo, per sempre: proposta dell'agente, decisione (Accettato = valore giallo "
        "invariato, Rettificato = cambiato, Respinto = Respingi Sì), valore deciso, motivazione, chi e quando. E' la "
        "traccia per l'audit e la base per migliorare gli agenti. Le validazioni si fanno nel foglio Validazione, non qui.",
        LEGENDA_COLORI]),
}
# Ultima colonna della guida dei fogli di vista e del report (le tabelle dati la calcolano da se').
COLONNE_GUIDA = {"Quadro": 15, "Classifica": 11, "Radar_Mosca": 12, "Matrice": 7, "Delta": 17, "Fenomeni": 11,
                 "Metodologia": 2, "Registro": 21, "Storico": 10, "Indicatori": 20, "Notizie": 10, "Piano_azioni": 10,
                 "Osservazione": 15, "Validazione": 15, "Dizionario": 7}

# ============================================================== DATI DI ESEMPIO
# Dodici rischi su tre cicli (2025Q4, 2026Q1, 2026Q2), ciclo corrente 2026Q2:
# riempiono il radar. Nessuno su 9.11 (Employer): e' l'area che la
# catena di prova scopre con A3 e copre con un rischio nuovo.
# Rispettano la rubrica: variazioni di al massimo un punto, sempre con
# evidenza datata dopo il ciclo precedente; nessuna Impatto scende. Casi
# limite esercitati:
#   Delta sopra soglia (0,40) in aumento: NFR-01 (Impatto +1, Velocity +1)
#   Delta in diminuzione:                  NFR-05 (Prossimita' -1)
#   Velocity non valutata (null, D-50):    NFR-10 (nessuna fonte ne documenta i tempi)
#   Badge: NFR-01 in peggioramento, NFR-05 in miglioramento, gli altri stabili
#   KRI: Verde, Ambra, Rosso, Non rilevato e Soglie da definire (NFR-10-K1)
#   Presidio dei controlli (D-49): Adeguato, Parziale, Assente, Non verificato
#   Segnalazione da motivare (Bloccante di A5, D-71): NFR-12 nel 2026Q2
#   Rischi entrati a meta' storia: NFR-06, NFR-09, NFR-10 (Nuovi nel 2026Q1)
#   Validazione del 2026Q2: una rettifica di un rischio (NFR-10 Probabilita),
#   una di un KRI (NFR-06-K2 soglia), un'azione respinta (NFR-05)

DATE_CICLO = {"2025Q4": date(2025, 12, 31), "2026Q1": date(2026, 3, 31), "2026Q2": date(2026, 6, 30)}
CICLO_CORRENTE = "2026Q2"
SETTIMANA_CORRENTE = date(2026, 6, 29)  # lunedi'

ANAGRAFICA = [
    ("NFR-01", "Frodi su pagamenti istantanei abilitate da AI generativa", "9.7", ["DRV-AI", "DRV-CYB"], "Funzione Antifrode",
     "Frodi a danno dei clienti tramite voci o video sintetici che inducono bonifici istantanei irrevocabili verso conti di terzi."),
    ("NFR-02", "Concentrazione su un fornitore cloud critico", "9.9", ["DRV-TPR", "DRV-CYB"], "Funzione ICT & Security Risk",
     "Indisponibilita' prolungata del fornitore cloud che ospita servizi critici, senza alternativa attivabile nei tempi di ripristino."),
    ("NFR-03", "Greenwashing nella commercializzazione di prodotti ESG", "9.1", ["DRV-CON", "DRV-CLI"], "Funzione Compliance",
     "Claim ambientali non sostanziati nella documentazione di prodotti di investimento ESG, con rischio di sanzioni e rimborsi."),
    ("NFR-04", "Eventi climatici estremi su sedi e data center", "9.8", ["DRV-CLI"], "Funzione Business Continuity",
     "Alluvioni o ondate di calore che rendono inagibili sedi operative o degradano il data center secondario."),
    ("NFR-05", "Errori di processo nella migrazione del core banking", "9.13", ["DRV-TEC"], "Funzione Operations",
     "Errori di conversione dati e controlli di processo non ridisegnati durante la migrazione a ondate del sistema core."),
    ("NFR-06", "Esfiltrazione di dati tramite strumenti di AI non autorizzati", "9.7", ["DRV-AI", "DRV-HUM"], "Funzione Sicurezza delle Informazioni",
     "Dipendenti che trasferiscono intenzionalmente dati riservati su servizi di AI generativa esterni per uso personale o a favore di terzi."),
    ("NFR-07", "Ransomware presso un fornitore di servizi di pagamento", "9.9", ["DRV-CYB", "DRV-TPR"], "Funzione ICT & Security Risk",
     "Blocco prolungato dei pagamenti per un attacco ransomware al fornitore esterno che gestisce il gateway di pagamento della Banca."),
    ("NFR-08", "Accessi impropri di dipendenti ai dati dei clienti", "9.7", ["DRV-HUM", "DRV-CON"], "Funzione Sicurezza delle Informazioni",
     "Dipendenti che consultano o estraggono dati di clienti senza motivo di servizio, per curiosita' o a favore di terzi."),
    ("NFR-09", "Violazione di sanzioni internazionali tramite triangolazioni", "9.4", ["DRV-GEO"], "Funzione Compliance",
     "Pagamenti di clientela corporate verso controparti sanzionate interposte in paesi terzi, non intercettati dal filtro sanzioni."),
    ("NFR-10", "Informazioni errate ai clienti da assistenti di AI generativa", "9.1", ["DRV-AI", "DRV-CON"], "Funzione Customer Experience",
     "Chatbot di assistenza basati su AI generativa che danno ai clienti informazioni errate su condizioni, costi o diritti, con reclami e rimborsi."),
    ("NFR-11", "Fine del supporto dei sistemi di pagamento legacy", "9.6", ["DRV-TEC"], "Funzione IT Operations",
     "Componenti del sistema di pagamento fuori supporto del produttore, senza patch di sicurezza e con competenze interne in riduzione."),
    ("NFR-12", "Errori operativi nei pagamenti istantanei obbligatori", "9.13", ["DRV-TEC"], "Funzione Operations",
     "Errori di riconciliazione e rimborsi indebiti dopo l'obbligo di offrire i bonifici istantanei a tutta la clientela."),
]

# Anni di adeguamento strutturale (anagrafica, input del validatore; rubrica,
# sezione 8): la sostituzione delle componenti legacy richiede un programma
# pluriennale, quindi Y di Mosca non e' l'orizzonte di 12 mesi dell'azione.
ANNI_ADEGUAMENTO = {"NFR-11": 3}
# Attenzione del supervisore (anagrafica, input del validatore; decisione D-35):
# temi nelle priorita' o nelle comunicazioni di BCE, EBA o Banca d'Italia. ◆ accanto all'ID nel radar.
ATTENZIONE_SUPERVISORE = {"NFR-01": "Sì", "NFR-02": "Sì", "NFR-07": "Sì", "NFR-09": "Sì"}
# Presidio dei controlli (anagrafica, input del validatore; decisione D-49): giudizio qualitativo della
# Banca, fuori dallo score. Gli altri rischi restano "Non verificato".
PRESIDI = ["Non verificato", "Adeguato", "Parziale", "Assente"]
PRESIDIO_ESEMPIO = {"NFR-05": "Adeguato", "NFR-01": "Parziale", "NFR-07": "Parziale", "NFR-12": "Parziale",
                    "NFR-06": "Assente", "NFR-11": "Assente"}
# Segnalazione da motivare (D-71) nel ciclo 2026Q2: NFR-12, un Bloccante di A5 portato in validazione. In validazione
# ogni riga di quel rischio ha una Motivazione, anche se Accettata.
RILIEVI_ESEMPIO = {("2026Q2", "NFR-12"): "⚑ DA MOTIVARE · C4 · A5: Prossimita 4: il report operativo di maggio "
                                         "documenta rimborsi indebiti, ma non un caso nominato fuori dalla Banca."}
SUPERAMENTO_ESEMPIO = {"2026Q2": "Segnalazioni da motivare in validazione: 1 (controlli 0, A5 1)."}
MOTIVAZIONI_ESEMPIO = {("Rischio", "NFR-12"): "Casi interni documentati dal report operativo di maggio: Prossimita 4 confermata."}

# Commento di A1 e sintesi del challenger per ciclo (tabella tblSintesi, foglio Sintesi).
# Sintesi di A3 per settimana (tabella tblSettimane, D-66): settimana = lunedi' in cui A3 ha valutato le notizie.
SETTIMANE_ESEMPIO = [
    (date(2026, 6, 15), 3, "Settimana con una nuova ondata di frodi con voce clonata segnalata dal CERT finanziario (NFR-01) "
     "e due notizie migliorative: stabilizzazione delle migrazioni a ondate in banche comparabili (NFR-05) e nuova "
     "region italiana del fornitore cloud (NFR-02). Nessuna area non presidiata.",
     "NFR-01 · Peggiorativo: campagne con voce clonata dirette ai clienti corporate; da riconsiderare nel prossimo "
     "trimestre la Prossimita' del rischio."),
    (date(2026, 6, 22), 3, "Un caso di deepfake video presso una banca tedesca rafforza la pressione su NFR-01; chiusura dei "
     "rilievi di vigilanza su una migrazione comparabile (NFR-05, migliorativo); allerta caldo senza impatti (NFR-04).",
     "Nessun flag proposto"),
    (date(2026, 6, 29), 3, "Linee guida europee sul rimborso delle frodi APP: la perdita si sposta sul prestatore di servizi di "
     "pagamento (NFR-01, peggiorativo). Il report di resilienza del fornitore cloud conferma tempi di ripristino oltre gli "
     "impegni (NFR-02). La migrazione del core banking chiude la wave 1 senza incidenti gravi (NFR-05).",
     "NFR-01 · Peggiorativo: tre segnali peggiorativi in quattro settimane e l'obbligo di rimborso in arrivo; da valutare "
     "nel prossimo ciclo trimestrale l'Impatto del rischio."),
]

SINTESI_ESEMPIO = {
    "2025Q4": ("Primo registro dei rischi emergenti: nove rischi su sei categorie. Le priorita' sono la concentrazione "
               "sul fornitore cloud critico (NFR-02), il ransomware presso il fornitore del gateway di pagamento (NFR-07) "
               "e la migrazione del core banking (NFR-05), per servizi critici con controlli non ancora testati. Al "
               "comitato si chiede di assegnare gli owner e di approvare le azioni proposte.",
               "Controlli superati; due osservazioni su rischi sostenuti da una sola fonte.", 2),
    "2026Q1": ("Entrano tre rischi nuovi legati all'intelligenza artificiale e alle sanzioni (NFR-06, NFR-09, NFR-10). "
               "Sale la prossimita' delle frodi con voce sintetica (NFR-01) dopo i primi casi in banche comparabili. "
               "Priorita': NFR-02, NFR-07 e NFR-01. Decisione richiesta: estendere il DLP ai servizi di AI generativa.",
               "Controlli superati; un'osservazione sui KRI del rischio NFR-10, non ancora rilevabili.", 1),
    "2026Q2": ("MESSAGGIO: trimestre con quattro rischi variati. Peggiorano le frodi su pagamenti istantanei (NFR-01, "
               "impatto da 3 a 4 per importi medi triplicati) e gli errori operativi sui bonifici istantanei (NFR-12, primi "
               "casi interni); l'alluvione di maggio avvicina il rischio climatico sulle sedi (NFR-04). Migliora la "
               "migrazione del core banking (NFR-05) dopo il test positivo dei controlli. Priorita': NFR-01, NFR-07, NFR-02. "
               "DECISIONI: approvare la verifica fuori banda sui bonifici istantanei (NFR-01) e il test di ripristino con il "
               "fornitore del gateway (NFR-07).",
               "Controlli superati. Osservazione: la probabilita' proposta per NFR-10 non e' sostenuta da frequenze osservate.", 1),
}

# Probabilita (rubrica, sezione 1): costante nei cicli di esempio, per non
# introdurre variazioni senza evidenza. NFR-10 nel 2026Q2: l'agente aveva
# proposto 4, il validatore ha rettificato a 3 (vedi VALIDAZIONE_ESEMPIO).
PROBABILITA = {"NFR-01": 4, "NFR-02": 2, "NFR-03": 3, "NFR-04": 3, "NFR-05": 3, "NFR-06": 3,
               "NFR-07": 3, "NFR-08": 2, "NFR-09": 2, "NFR-10": 3, "NFR-11": 3, "NFR-12": 4}

# fonti: (riferimento, data, tipo, rilevanza 1-3 per la previsione, D-58)
FONTI = {
    "NFR-01": [("Analisi interna sulle frodi da ingegneria sociale", "2025-10-20", "Interna", 3),
               ("Threat intelligence: campagne di frode con voce sintetica verso banche UE", "2026-04-15", "Esterna", 2),
               ("Report trimestrale frodi — Funzione Antifrode", "2026-06-10", "Interna", 3),
               ("Relazione annuale sui pagamenti al dettaglio dell'autorita' di vigilanza", "2026-05-28", "Esterna", 3)],
    "NFR-02": [("Contratto e piano di uscita del fornitore cloud", "2025-09-30", "Interna", 2),
               ("Registro delle informazioni DORA — servizi ICT critici", "2026-03-20", "Interna", 3),
               ("Esito del test di exit strategy sul fornitore cloud", "2026-05-12", "Interna", 3)],
    "NFR-03": [("Orientamenti dell'autorita' europea sui nomi dei fondi ESG", "2025-11-14", "Esterna", 3),
               ("Verifica interna dei claim ambientali — Compliance", "2026-02-18", "Interna", 2)],
    "NFR-04": [("Mappa del rischio idrogeologico delle sedi — BCM", "2025-10-30", "Interna", 2),
               ("Alluvione in Emilia-Romagna con chiusura di due filiali", "2026-05-06", "Esterna", 3)],
    "NFR-05": [("Piano di migrazione del core banking — PMO", "2025-09-15", "Interna", 3),
               ("Chiusura della wave 1 di migrazione — PMO", "2026-05-04", "Interna", 3),
               ("Relazione di audit sui controlli di riconciliazione post-migrazione", "2026-05-20", "Interna", 3)],
    "NFR-06": [("Log DLP: tentativi di caricamento verso servizi AI esterni", "2026-03-15", "Interna", 3),
               ("Survey interna sull'uso di strumenti di AI generativa", "2026-02-10", "Interna", 2)],
    "NFR-07": [("Registro DORA: fornitore del gateway di pagamento classificato critico", "2025-10-15", "Interna", 2),
               ("Attacco ransomware a un processore di pagamenti europeo", "2026-02-20", "Esterna", 3)],
    "NFR-08": [("Esiti del monitoraggio degli accessi ai dati clienti — SOC", "2025-11-10", "Interna", 3),
               ("Provvedimento dell'autorita' privacy su accessi abusivi in una banca", "2026-04-08", "Esterna", 3)],
    "NFR-09": [("Nuovo pacchetto di sanzioni UE con obblighi di due diligence rafforzata", "2026-02-24", "Esterna", 3),
               ("Analisi dei flussi verso paesi di transito — Compliance", "2026-03-12", "Interna", 2)],
    "NFR-10": [("Piano di rilascio del chatbot di assistenza con AI generativa", "2026-01-20", "Interna", 2),
               ("Sanzione a una compagnia aerea per risposte errate del proprio chatbot", "2026-02-15", "Esterna", 2)],
    "NFR-11": [("Inventario delle componenti fuori supporto — IT", "2025-09-30", "Interna", 3),
               ("Comunicazione del produttore sulla fine del supporto esteso", "2026-01-31", "Esterna", 3)],
    "NFR-12": [("Piano di adeguamento al regolamento sui bonifici istantanei", "2025-10-01", "Interna", 2),
               ("Report operativo dei pagamenti istantanei — maggio", "2026-05-15", "Interna", 3)],
}

# punteggi: (impatto, velocity, prossimita, esito, variazioni); velocity None = non valutata (D-58: niente Confidence)
# variazioni: (dimensione, da, a, evidenza, data_evidenza)
STORIA = {
    "2025Q4": {
        "NFR-01": (3, 4, 3, "Confermato", []),
        "NFR-02": (4, 4, 3, "Confermato", []),
        "NFR-03": (3, 2, 3, "Confermato", []),
        "NFR-04": (3, 2, 2, "Confermato", []),
        "NFR-05": (3, 3, 4, "Confermato", []),
        "NFR-07": (4, 5, 3, "Confermato", []),
        "NFR-08": (3, 3, 3, "Confermato", []),
        "NFR-11": (3, 2, 3, "Confermato", []),
        "NFR-12": (3, 4, 3, "Confermato", []),
    },
    "2026Q1": {
        "NFR-01": (3, 4, 4, "Variato", [
            ("prossimita", 3, 4, "Primi casi di frode con voce sintetica presso due banche italiane comparabili, riportati dalla threat intelligence di settore.", "2026-02-12")]),
        "NFR-02": (4, 4, 3, "Confermato", []),
        "NFR-03": (3, 2, 3, "Confermato", []),
        "NFR-04": (3, 2, 2, "Confermato", []),
        "NFR-05": (3, 3, 4, "Confermato", []),
        "NFR-06": (3, 3, 3, "Nuovo", []),
        "NFR-07": (4, 5, 3, "Confermato", []),
        "NFR-08": (3, 3, 3, "Confermato", []),
        "NFR-09": (4, 3, 2, "Nuovo", []),
        "NFR-10": (3, None, 3, "Nuovo", []),
        "NFR-11": (3, 2, 3, "Confermato", []),
        "NFR-12": (3, 4, 3, "Confermato", []),
    },
    "2026Q2": {
        "NFR-01": (4, 5, 4, "Variato", [
            ("impatto", 3, 4, "Il report trimestrale frodi documenta importi medi per caso triplicati sui bonifici istantanei rispetto al trimestre precedente.", "2026-06-10"),
            ("velocity", 4, 5, "Il report trimestrale frodi documenta che i fondi escono dal conto del beneficiario entro un'ora dal bonifico istantaneo.", "2026-06-10")]),
        "NFR-02": (4, 4, 3, "Confermato", []),
        "NFR-03": (3, 2, 3, "Confermato", []),
        "NFR-04": (3, 2, 3, "Variato", [
            ("prossimita", 2, 3, "Alluvione in Emilia-Romagna del maggio 2026 con chiusura di due filiali della Banca per tre giorni.", "2026-05-06")]),
        "NFR-05": (3, 3, 3, "Variato", [
            ("prossimita", 4, 3, "Wave 1 completata il 4 maggio 2026; la wave 2 e' pianificata per il 2027, quindi il prossimo punto di esposizione si allontana.", "2026-05-04")]),
        "NFR-06": (3, 3, 3, "Confermato", []),
        "NFR-07": (4, 5, 3, "Confermato", []),
        "NFR-08": (3, 3, 3, "Confermato", []),
        "NFR-09": (4, 3, 2, "Confermato", []),
        "NFR-10": (3, None, 3, "Confermato", []),
        "NFR-11": (3, 2, 3, "Confermato", []),
        "NFR-12": (3, 4, 4, "Variato", [
            ("prossimita", 3, 4, "Il report operativo di maggio registra i primi rimborsi indebiti e differenze di riconciliazione sui bonifici istantanei presso la Banca.", "2026-05-15")]),
    },
}

RAZIONALI = {
    "NFR-01": "Impatto 4 per importi medi in forte crescita su pagamenti irrevocabili; velocity 5 perche' i fondi escono dal conto del beneficiario entro un'ora; prossimita' 4 per casi gia' osservati in banche comparabili.",
    "NFR-02": "Impatto 4 per servizi critici ospitati su un solo fornitore; velocity 4 perche' un'interruzione e' immediata; prossimita' 3 senza incidenti gravi recenti.",
    "NFR-03": "Impatto 3 per sanzioni e rimborsi possibili su una clientela ampia; velocity 2 perche' l'esposizione emerge con ispezioni o reclami; prossimita' 3 per orientamenti europei gia' in vigore.",
    "NFR-04": "Impatto 3 per degrado di sedi e del sito secondario; velocity 2; prossimita' 3 dopo l'alluvione di maggio su filiali della Banca.",
    "NFR-05": "Impatto 3 per errori contabili e disservizi limitati nel tempo; velocity 3; prossimita' 3 perche' la wave 2 e' nel 2027.",
    "NFR-06": "Impatto 3 per possibile perdita di dati riservati; velocity 3; prossimita' 3 per tentativi rilevati dal DLP.",
    "NFR-07": "Impatto 4 perche' i pagamenti si fermano; velocity 5 perche' il blocco e' immediato; prossimita' 3 per attacchi a processori europei.",
    "NFR-08": "Impatto 3 per violazione di dati di clientela ampia; velocity 3; prossimita' 3 per casi sanzionati nel settore.",
    "NFR-09": "Impatto 4 per sanzioni e danno reputazionale nazionale; velocity 3; prossimita' 2 per precursori solo in altri paesi.",
    "NFR-10": "Impatto 3 per reclami e rimborsi su clientela ampia; velocity non valutata: nessuna fonte documenta i tempi fra una risposta errata e il danno; prossimita' 3 per casi nel settore europeo.",
    "NFR-11": "Impatto 3 per disservizi sui pagamenti; velocity 2; prossimita' 3 per fine supporto annunciata.",
    "NFR-12": "Impatto 3 per rimborsi indebiti e disservizi; velocity 4 perche' gli errori si propagano in giornata; prossimita' 4 dopo i primi casi interni di maggio.",
}

KRI_ESEMPIO = [
    # D-64: due KRI per rischio, uno di Esposizione e uno di Evoluzione.
    # id, rischio, tipo, nome, unita, fonte_dati, attenzione, allerta, ciclo_definizione,
    # valori rilevati (2025Q4, 2026Q1, 2026Q2): None = non rilevato; prima della
    # definizione il valore e' ignorato (il KRI non esiste in quei cicli).
    ("NFR-01-K1", "NFR-01", "Evoluzione", "Tentativi di frode APP per 10.000 bonifici istantanei", "n/10k", "Sistema antifrode transazionale", 3, 6, "2025Q4", (2.1, 3.4, 4.2)),
    ("NFR-01-K3", "NFR-01", "Esposizione", "Tempo medio di blocco di un beneficiario fraudolento", "ore", "Log del sistema di pagamento", 4, 12, "2025Q4", (5, 3.5, 2.5)),
    ("NFR-02-K1", "NFR-02", "Esposizione", "Quota di servizi critici sul fornitore cloud principale", "%", "Registro delle informazioni DORA", 60, 75, "2025Q4", (74, 76, 78)),
    ("NFR-02-K2", "NFR-02", "Evoluzione", "Incidenti dei fornitori cloud critici con impatto sui servizi nel trimestre", "n", "Incident management ICT", 2, 4, "2025Q4", (2, 0, 1)),
    ("NFR-03-K1", "NFR-03", "Evoluzione", "Reclami su prodotti ESG ogni 1.000 contratti", "n/1000", "Sistema di gestione reclami", 1.5, 3, "2025Q4", (0.6, 0.7, 0.8)),
    ("NFR-03-K2", "NFR-03", "Esposizione", "Quota di prodotti ESG senza revisione dei claim nell'anno", "%", "Inventario prodotti — Compliance", 20, 40, "2025Q4", (55, None, None)),
    ("NFR-04-K1", "NFR-04", "Esposizione", "Sedi critiche in aree a rischio idrogeologico senza piano specifico", "n", "Mappatura BCM delle sedi", 1, 3, "2025Q4", (2, 2, 2)),
    ("NFR-04-K2", "NFR-04", "Evoluzione", "Giorni di indisponibilita' di sedi per eventi climatici", "giorni", "Registro incidenti BCM", 2, 5, "2025Q4", (0, 1, 3)),
    ("NFR-05-K2", "NFR-05", "Evoluzione", "Incidenti di produzione legati alla migrazione", "n", "Incident management IT", 3, 6, "2025Q4", (4, 9, 7)),
    ("NFR-05-K3", "NFR-05", "Esposizione", "Quota di controlli di processo non ridisegnati sul nuovo core", "%", "Piano di migrazione — PMO", 30, 60, "2025Q4", (55, 40, 25)),
    ("NFR-06-K1", "NFR-06", "Evoluzione", "Tentativi di caricamento di dati riservati su servizi AI non autorizzati", "n/mese", "DLP e proxy web", 10, 30, "2026Q1", (None, 22, 14)),
    ("NFR-06-K2", "NFR-06", "Esposizione", "Quota di dipendenti senza formazione sull'uso dell'AI", "%", "Piattaforma di formazione", 20, 40, "2026Q1", (None, 48, 35)),
    ("NFR-07-K1", "NFR-07", "Esposizione", "Fornitori di pagamento critici senza test di ripristino da ransomware", "n", "Registro delle informazioni DORA", 1, 2, "2025Q4", (2, 2, 1)),
    ("NFR-07-K2", "NFR-07", "Evoluzione", "Ore di indisponibilita' del gateway di pagamento nel trimestre", "ore", "Incident management ICT", 4, 12, "2025Q4", (1.5, 6, 3)),
    ("NFR-08-K1", "NFR-08", "Evoluzione", "Accessi ai dati clienti senza pratica associata", "n/mese", "Log applicativi e SOC", 20, 50, "2025Q4", (35, 28, 24)),
    ("NFR-08-K2", "NFR-08", "Esposizione", "Utenze con profili di accesso non rivisti nell'anno", "%", "Sistema IAM", 5, 15, "2025Q4", (12, 9, 6)),
    ("NFR-09-K1", "NFR-09", "Evoluzione", "Pagamenti bloccati dal filtro sanzioni ogni 10.000 verso paesi di transito", "n/10k", "Sistema di filtro sanzioni", 2, 5, "2026Q1", (None, 3.1, 3.8)),
    ("NFR-09-K2", "NFR-09", "Esposizione", "Clienti corporate ad alto rischio senza due diligence rafforzata aggiornata", "%", "Anagrafe clienti — Compliance", 5, 15, "2026Q1", (None, 18, 11)),
    ("NFR-10-K1", "NFR-10", "Evoluzione", "Risposte del chatbot contestate ogni 1.000 conversazioni", "n/1000", "Piattaforma di assistenza", None, None, "2026Q1", (None, None, 1.4)),
    ("NFR-10-K3", "NFR-10", "Esposizione", "Quota di risposte del chatbot non campionate dal controllo qualita'", "%", "Controllo qualita' Customer Experience", 20, 50, "2026Q1", (None, 80, 60)),
    ("NFR-11-K1", "NFR-11", "Esposizione", "Componenti del sistema di pagamento fuori supporto", "n", "Inventario IT", 3, 8, "2025Q4", (9, 9, 7)),
    ("NFR-11-K2", "NFR-11", "Evoluzione", "Vulnerabilita' senza patch disponibile sui sistemi legacy", "n", "Vulnerability management", 2, 6, "2025Q4", (4, 5, 5)),
    ("NFR-12-K1", "NFR-12", "Evoluzione", "Differenze di riconciliazione sui bonifici istantanei aperte oltre 1 giorno", "n", "Sistema di riconciliazione", 10, 30, "2025Q4", (4, 6, 14)),
    ("NFR-12-K3", "NFR-12", "Esposizione", "Tempo medio di risoluzione delle eccezioni sui pagamenti istantanei", "ore", "Workflow delle eccezioni", 4, 12, "2025Q4", (3, 3.5, 5)),
]

DATA_VALIDAZIONE_Q2 = date(2026, 7, 15)
VALIDATORE = "Comitato Rischi"

# A3 collegava le notizie alle voci della lista di osservazione (D-73): con il registro unico (D-79) le collega ai
# rischi in osservazione con Rischio_ID, come a quelli del radar.

# Registro unico (D-79): rischi in osservazione, stessa scala e stesso score dei rischi del radar, niente KRI ne'
# azioni. Sono le tre voci della vecchia lista di osservazione (D-73), rivalutate con la rubrica: restano fuori dal
# radar perche' Prossimita o Probabilita sono sotto la soglia di Parametri. NFR-13 e NFR-14 dal 2026Q1, NFR-15 nuovo
# nel 2026Q2; NFR-14 aggiornato nel 2026Q2 con evidenza nuova, NFR-13 riportato com'era (periodo 2026Q1).
# rischio, nome, event type, driver, owner, descrizione, razionale, orizzonte anni, segnale di avvicinamento,
# fonti (riferimento, data, tipo, rilevanza), {ciclo: (impatto, velocity, prossimita, probabilita, esito, periodo)}
OSSERVAZIONE_ESEMPIO = [
    ("NFR-13", "Rottura della crittografia dei pagamenti con il calcolo quantistico", "9.7", ["DRV-TEC", "DRV-CYB"],
     "Funzione Sicurezza delle Informazioni",
     "Un calcolatore quantistico abbastanza potente renderebbe decifrabili le firme e le comunicazioni che proteggono "
     "pagamenti e accessi della Banca; dati intercettati oggi potrebbero essere letti domani. Danno: frodi, violazione "
     "di dati, sostituzione d'urgenza della crittografia.",
     "Impatto 5 perche' toccherebbe tutti i canali; Probabilita 1 e Prossimita 1: nessun calcolatore oggi ha la capacita' "
     "necessaria e nessun caso e' documentato; velocity non valutata: nessuna fonte sui tempi.",
     10, "Annuncio verificato di un calcolatore in grado di rompere RSA-2048, o una scadenza regolamentare per la "
     "migrazione post-quantistica dei sistemi di pagamento.",
     [("Rapporto sulla crittografia post-quantistica di un'agenzia europea per la cybersicurezza", "2026-02-10", "Esterna", 2)],
     {"2026Q1": (5, None, 1, 1, "Nuovo", "2026Q1"), "2026Q2": (5, None, 1, 1, "Confermato", "2026Q1")}),
    ("NFR-14", "Interruzione di cavi sottomarini per una crisi geopolitica", "9.6", ["DRV-GEO", "DRV-TPR"],
     "Funzione ICT & Security Risk",
     "Il taglio di piu' cavi sottomarini nel Mediterraneo degraderebbe la connettivita' verso i data center del "
     "fornitore cloud e i circuiti di pagamento internazionali. Danno: indisponibilita' dei servizi e dei pagamenti "
     "esteri per giorni.",
     "Impatto 4 per servizi e pagamenti esteri fermi per giorni; velocity 4 perche' il taglio e' immediato; "
     "Probabilita 2 dopo i danneggiamenti nel Mar Baltico e nel Mar Rosso; Prossimita 1: nessun caso sulle rotte italiane.",
     5, "Danneggiamento doloso di un cavo che serve l'Italia, o un'esercitazione delle autorita' sul ripristino della "
     "connettivita'.",
     [("Rapporto sulla resilienza delle infrastrutture critiche sottomarine", "2026-05-20", "Esterna", 3)],
     {"2026Q1": (4, 4, 1, 1, "Nuovo", "2026Q1"), "2026Q2": (4, 4, 1, 2, "Variato", "2026Q2")}),
    ("NFR-15", "Responsabilita' per decisioni di agenti di IA autonomi verso i clienti", "9.4", ["DRV-AI", "DRV-CON"],
     "Funzione Customer Experience",
     "Agenti di IA che agiscono per conto dei clienti (pagamenti, investimenti) potrebbero eseguire operazioni non volute; "
     "la ripartizione della responsabilita' fra cliente, fornitore dell'agente e Banca non e' definita. Danno: rimborsi "
     "e contenzioso.",
     "Impatto 3 per rimborsi e contenzioso; Prossimita 2 per sperimentazioni presso grandi piattaforme di pagamento; "
     "Probabilita 1: nessun caso in banca; velocity non valutata.",
     4, "Primo contenzioso o orientamento di un'autorita' europea su un'operazione bancaria disposta da un agente di IA.",
     [("Comunicato di una piattaforma di pagamento sugli acquisti delegati ad agenti di IA", "2026-06-03", "Esterna", 2)],
     {"2026Q2": (3, None, 2, 1, "Nuovo", "2026Q2")}),
]
VARIAZIONI_OSSERVAZIONE = {
    ("2026Q2", "NFR-14"): [("probabilita", 1, 2, "Il rapporto sulla resilienza delle infrastrutture critiche sottomarine "
                            "documenta tre danneggiamenti dolosi di cavi europei in un anno.", "2026-05-20")],
}

AZIONI_ESEMPIO = [
    # rischio, descrizione, owner, orizzonte, razionale, stato (dopo la validazione del 2026Q2)
    ("NFR-01", "Introdurre la verifica fuori banda per bonifici istantanei sopra soglia verso beneficiari nuovi.", "Funzione Antifrode", "6 mesi",
     "Oggi la verifica fuori banda esclude i bonifici istantanei: e' il punto debole che l'azione chiude.", "Approvata"),
    ("NFR-02", "Eseguire il test completo di exit strategy sui due servizi critici non ancora coperti.", "Funzione ICT & Security Risk", "12 mesi",
     "Finche' la exit strategy non e' testata su tutti i servizi critici, un guasto del fornitore non ha alternativa.", "Approvata"),
    ("NFR-03", "Revisione indipendente dei claim ambientali di tutti i prodotti ESG in catalogo.", "Funzione Compliance", "6 mesi",
     "Sostanzia i claim prima che un'ispezione o un reclamo li contesti.", "Approvata"),
    ("NFR-04", "Redigere piani di continuita' specifici per le due sedi critiche in aree a rischio.", "Funzione Business Continuity", "12 mesi",
     "Il KRI NFR-04-K1 mostra due sedi senza piano: e' il punto scoperto principale.", "Approvata"),
    ("NFR-05", "Monitoraggio giornaliero degli incidenti post-migrazione con escalation entro 4 ore.", "Funzione Operations", "3 mesi",
     "Intercetta gli errori prima che si propaghino alle scritture contabili.", "Respinta"),
    ("NFR-06", "Estendere il DLP a tutti i servizi di AI generativa e bloccare quelli non autorizzati.", "Funzione Sicurezza delle Informazioni", "3 mesi",
     "Il DLP copre solo parte dei servizi di AI generativa: l'azione estende il presidio.", "Approvata"),
    ("NFR-07", "Test congiunto di ripristino da ransomware con il fornitore del gateway di pagamento.", "Funzione ICT & Security Risk", "6 mesi",
     "Il ripristino da ransomware non e' mai stato testato con il fornitore.", "Approvata"),
    ("NFR-08", "Revisione trimestrale automatica degli accessi ai dati clienti senza pratica associata.", "Funzione Sicurezza delle Informazioni", "3 mesi",
     "Oggi la revisione degli accessi e' annuale e a campione.", "Approvata"),
    ("NFR-09", "Estendere lo screening sanzioni alle controparti indirette dei pagamenti verso paesi di transito.", "Funzione Compliance", "12 mesi",
     "Chiude la lacuna sulle triangolazioni, oggi non coperte dal filtro.", "Approvata"),
    ("NFR-10", "Campionamento settimanale delle risposte del chatbot con verifica umana.", "Funzione Customer Experience", "3 mesi",
     "Riduce la probabilita' che informazioni errate raggiungano molti clienti.", "Approvata"),
    ("NFR-11", "Piano di sostituzione delle componenti fuori supporto del sistema di pagamento.", "Funzione IT Operations", "12 mesi",
     "Oggi non ci sono patch per le componenti fuori supporto.", "Approvata"),
    ("NFR-12", "Controllo giornaliero automatico delle differenze di riconciliazione sui bonifici istantanei.", "Funzione Operations", "3 mesi",
     "La riconciliazione oggi e' settimanale: gli errori emergono troppo tardi.", "Approvata"),
]

# Esempi di rettifica nella validazione del 2026Q2 (foglio Validazione):
# (oggetto, id, campo, proposta dell'agente, decisione, valore validato, motivazione).
# Il registro contiene il valore VALIDATO; la proposta resta solo qui.
RETTIFICHE_ESEMPIO = [
    ("Rischio", "NFR-10", "Probabilita", 4, "Rettificato", 3,
     "Chatbot in produzione da aprile: nessuna frequenza osservata che giustifichi 'probabile'."),
    ("KRI", "NFR-06-K2", "Soglia_Attenzione", 30, "Rettificato", 20,
     "Soglia allineata all'obiettivo formativo annuale approvato dalla funzione HR."),
    ("Azione", "2026Q2-NFR-05-A1", "Owner", "Funzione Operations", "Respinto", None,
     "Gia' coperto dal presidio giornaliero del PMO: azione duplicata."),
]

# notizie: (data, id, titolo, fonte, codice_fonte (01_Kernel/fonti.md), rischio, segnale, {event_type: intensita'}, sintesi)
NEWS_ESEMPIO = [
    (date(2026, 5, 20), "N-20260520-01", "Guasto regionale del fornitore cloud per sei ore", "Agenzia di stampa", "FNT-17", "NFR-02", "Peggiorativo", {"9.9": 2},
     "Interruzione di sei ore di una region europea del fornitore; fuori dalla finestra delle 4 settimane del badge."),
    (date(2026, 6, 9), "N-20260609-01", "Nuova ondata di frodi con voce clonata su bonifici istantanei", "CERT finanziario nazionale", "FNT-34", "NFR-01", "Peggiorativo", {"9.7": 3, "9.1": 1},
     "Allerta del CERT su campagne con voce clonata di dirigenti verso clienti corporate."),
    (date(2026, 6, 10), "N-20260610-01", "Stabilizzazione dei sistemi dopo la wave 1 in banche comparabili", "Stampa specializzata", "MAN", "NFR-05", "Migliorativo", {"9.13": 2},
     "Le banche che hanno migrato con approccio a ondate riportano incidenti in calo."),
    (date(2026, 6, 11), "N-20260611-01", "Il fornitore cloud annuncia una nuova region in Italia", "Comunicato stampa del fornitore cloud, sito del fornitore", "MAN", "NFR-02", "Migliorativo", {"9.9": 1},
     "Una seconda region nazionale rende piu' semplice una strategia multi-region."),
    (date(2026, 6, 16), "N-20260616-01", "Frodi con deepfake video in una banca tedesca", "Stampa economica", "FNT-18", "NFR-01", "Peggiorativo", {"9.7": 2},
     "Videochiamata con deepfake del CFO: bonifico da 20 milioni verso conto estero."),
    (date(2026, 6, 17), "N-20260617-01", "Chiusi i rilievi di audit sulla migrazione presso un peer", "Relazione di vigilanza", "FNT-01", "NFR-05", "Migliorativo", {"9.13": 1},
     "L'autorita' chiude i rilievi su un'analoga migrazione di core banking."),
    (date(2026, 6, 18), "N-20260618-01", "Allerta caldo estremo nel Nord Italia", "Protezione civile", "FNT-23", "NFR-04", "Neutro", {"9.8": 1},
     "Ondata di calore prevista; nessun impatto segnalato su infrastrutture critiche."),
    (date(2026, 6, 23), "N-20260623-01", "Il fornitore cloud pubblica il report di resilienza", "Comunicato stampa del fornitore cloud, sito del fornitore", "MAN", "NFR-02", "Peggiorativo", {"9.9": 1},
     "Il report conferma tempi di ripristino superiori agli impegni contrattuali in due incidenti."),
    (date(2026, 6, 24), "N-20260624-01", "Linee guida europee sul rimborso delle frodi APP", "Autorita' bancaria europea", "FNT-03", "NFR-01", "Peggiorativo", {"9.7": 2, "9.1": 2},
     "Proposta di rimborso obbligatorio delle frodi APP a carico del prestatore di servizi di pagamento."),
    (date(2026, 6, 25), "N-20260625-01", "Wave 1 chiusa senza incidenti gravi nel trimestre", "Comunicazione interna PMO", "MAN", "NFR-05", "Migliorativo", {"9.13": 2},
     "Il PMO conferma zero incidenti di severita' alta nelle ultime otto settimane."),
]


# ============================================================== UTILITA'
def nome_definito(wb, nome, riferimento):
    wb.defined_names[nome] = DefinedName(nome, attr_text=riferimento)


def ass(foglio, colonna_lettera, riga_da, riga_a):
    return f"'{foglio}'!${colonna_lettera}${riga_da}:${colonna_lettera}${riga_a}"


def spec_tabella(nome_tabella):
    """Le tabelle dati sono in MAPPA['tabelle']; la tabella di validazione in MAPPA['validazione']."""
    if nome_tabella == MAPPA["validazione"]["tabella"]:
        return MAPPA["validazione"]
    return MAPPA["tabelle"][nome_tabella]


def righe_da_validare():
    """Righe della griglia di validazione del ciclo corrente (rischi, KRI, azioni) ancora da decidere: lo storico
    ha una riga per campo, quindi si conta un campo per oggetto (il primo della mappa). Nome decisioniDaPrendere."""
    return "+".join(f'COUNTIFS(VAL_Periodo,cicloCorrente,VAL_Stato,"Da decidere",VAL_Oggetto,"{o}",VAL_Campo,"{s["campi"][0]}")'
                    for o, s in MAPPA["validazione"]["oggetti"].items() if s["periodo"])


def colonne_tabella(nome_tabella):
    return [c["nome"] for c in spec_tabella(nome_tabella)["colonne"]]


def lettera(nome_tabella, colonna):
    return get_column_letter(colonne_tabella(nome_tabella).index(colonna) + 1)


def formula_riga(modello, nome_tabella, riga):
    """Sostituisce {Colonna} con la cella della stessa riga (es. {Impatto} -> G5)."""
    out = modello
    for c in colonne_tabella(nome_tabella):
        out = out.replace("{" + c + "}", f"{lettera(nome_tabella, c)}{riga}")
    return out


def titolo(ws, testo, ultima_colonna=8):
    """Fascia del titolo in riga 1: nome dell'analisi, titolo del foglio ed etichetta del
    ciclo (nome etichettaCiclo, in Parametri: ciclo, data, stato di validazione, riservatezza)."""
    testo_formula = f"{NOME_ANALISI} — {testo}   ·   ".replace('"', '""')
    ws["A1"] = f'="{testo_formula}"&etichettaCiclo'
    ws["A1"].font = Font(bold=True, size=14, color="FFFFFF")
    ws["A1"].alignment = Alignment(vertical="center", indent=1)
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=ultima_colonna)
    for j in range(1, ultima_colonna + 1):
        ws.cell(row=1, column=j).fill = PatternFill("solid", fgColor="1F3864")
    ws.row_dimensions[1].height = 28


def _larghezza(ws, colonna):
    d = ws.column_dimensions.get(get_column_letter(colonna))
    return d.width if d is not None and d.customWidth else 8.43


def _righe_stimate(testo, caratteri_per_riga):
    """Righe occupate da un testo a capo automatico: Excel non adatta l'altezza di una cella unita."""
    return sum(max(1, -(-len(par) // max(1, int(caratteri_per_riga)))) for par in testo.split("\n"))


def guida(ws, chiave, ultima_colonna, riga=2):
    """Guida in testa al foglio (GUIDE[chiave]): prima riga in grassetto con il processo
    che aggiorna il foglio, poi cosa contiene, come si legge, cosa fare. Una cella unita
    da A all'ultima colonna indicata, sul fondo del colore del processo."""
    processo, righe = GUIDE[chiave]
    fondo, colore, _ = PROCESSI[processo]
    prima, resto = righe[0], "\n".join(righe[1:])
    blocchi = [TextBlock(InlineFont(rFont="Calibri", sz=10, b=True, color=colore), prima)]
    if resto:
        blocchi.append(TextBlock(InlineFont(rFont="Calibri", sz=10, color="262626"), "\n" + resto))
    c = ws.cell(row=riga, column=1)
    c.value = CellRichText(blocchi)
    c.alignment = Alignment(wrap_text=True, vertical="top", horizontal="left")
    c.fill = PatternFill("solid", fgColor=fondo)
    ws.merge_cells(start_row=riga, start_column=1, end_row=riga, end_column=ultima_colonna)
    larghezza = sum(_larghezza(ws, j) for j in range(1, ultima_colonna + 1))
    # 10 pt: circa 1,3 caratteri per unita' di larghezza della colonna (misurato sul PDF).
    ws.row_dimensions[riga].height = 13.5 * _righe_stimate(prima + "\n" + resto, larghezza * 1.3) + 5


def colora(cella, processo, grassetto=True):
    """Intestazione o etichetta sul colore del processo che la aggiorna."""
    fondo, colore, _ = PROCESSI[processo]
    cella.fill = PatternFill("solid", fgColor=fondo)
    cella.font = Font(bold=grassetto, color=colore)


def chi_colonna(nome_tabella, c):
    """Chi scrive la colonna: A1/A3/A5 (payload), script, formula, validazione, validatore."""
    if nome_tabella == MAPPA["validazione"]["tabella"]:
        # Dal 01/10/2026 (D-67) il validatore scrive nella griglia del foglio Validazione: qui scrive il comando valida.
        return ("validazione" if c["nome"] in ("Decisione", "Valore_Validato", "Motivazione", "Validato_Da",
                                               "Data_Validazione", "Stato") else "script")
    if c["nome"] in COLONNE_VALIDAZIONE.get(nome_tabella, ()):
        return "validazione"
    sorgente = c.get("sorgente", "")
    if sorgente.startswith("formula:"):
        return "formula"
    if sorgente.startswith("payload:"):
        return spec_tabella(nome_tabella)["payload"]
    if sorgente == "derivato:sintesi_a5":
        return "A5"
    return "script"


def scrivi_tabella(wb, nome_tabella, righe, testo_titolo):
    """Crea la tabella dalla mappa, con righe = lista di dict {colonna: valore}.
    Riga 1 titolo, riga 2 guida, riga 3 gruppi di colonne per chi le scrive, riga 4
    significato di ogni colonna (dalla mappa, preceduto da chi la scrive), riga 5
    intestazione colorata per chi scrive."""
    spec = spec_tabella(nome_tabella)
    ws = wb[spec["foglio"]]
    colonne = spec["colonne"]
    titolo(ws, testo_titolo, min(len(colonne), 12))
    righe_significato = 1
    gruppi = []                                            # [(prima, ultima, chi)] di colonne consecutive
    for j, c in enumerate(colonne, start=1):
        larghezza = c.get("larghezza", 15)
        ws.column_dimensions[get_column_letter(j)].width = larghezza
        chi = chi_colonna(nome_tabella, c)
        processo, etichetta = ETICHETTA_CHI[chi]
        cella = ws.cell(row=RIGA_INTESTAZIONE, column=j, value=c["nome"])
        colora(cella, processo)
        testo = f"{etichetta} · {c['significato']}"
        s = ws.cell(row=RIGA_INTESTAZIONE - 1, column=j, value=testo)
        s.font = Font(italic=True, size=8, color="404040")
        s.alignment = A_CAPO
        righe_significato = max(righe_significato, _righe_stimate(testo, larghezza * 1.25))
        if gruppi and gruppi[-1][2] == chi:
            gruppi[-1][1] = j
        else:
            gruppi.append([j, j, chi])
    ws.row_dimensions[RIGA_INTESTAZIONE - 1].height = 11 * righe_significato + 3
    for da, a, chi in gruppi:
        processo, etichetta = ETICHETTA_CHI[chi]
        c = ws.cell(row=RIGA_INTESTAZIONE - 2, column=da, value=f"{etichetta} · {GRUPPO_CHI[chi]}")
        c.font = Font(size=9, bold=True, color=PROCESSI[processo][1])
        c.alignment = Alignment(horizontal="left", vertical="center")
        for x in range(da, a + 1):
            ws.cell(row=RIGA_INTESTAZIONE - 2, column=x).fill = PatternFill("solid", fgColor=PROCESSI[processo][0])
        if a > da:
            ws.merge_cells(start_row=RIGA_INTESTAZIONE - 2, start_column=da, end_row=RIGA_INTESTAZIONE - 2, end_column=a)
    for i, valori in enumerate(righe, start=PRIMA_RIGA_DATI):
        for j, c in enumerate(colonne, start=1):
            if c.get("sorgente", "").startswith("formula:"):
                valore = formula_riga(c["sorgente"][len("formula:"):], nome_tabella, i)
            else:
                valore = valori.get(c["nome"])
            cella = ws.cell(row=i, column=j, value=valore)
            cella.fill = GRIGIO
            if c.get("formato") == "data":
                cella.number_format = "dd/mm/yyyy"
            elif c.get("formato") == "decimale":
                cella.number_format = "0.00"
            if c.get("larghezza", 15) >= 40:
                cella.alignment = A_CAPO
    ultima = max(PRIMA_RIGA_DATI, PRIMA_RIGA_DATI + len(righe) - 1)  # una tabella deve avere almeno una riga dati
    rif = f"A{RIGA_INTESTAZIONE}:{get_column_letter(len(colonne))}{ultima}"
    tab = Table(displayName=nome_tabella, ref=rif)
    tab.tableStyleInfo = TableStyleInfo(name="TableStyleMedium2", showRowStripes=True)
    ws.add_table(tab)
    # Niente riquadri bloccati: la guida in testa occuperebbe mezzo schermo. Scorrendo
    # dentro la tabella, Excel mostra i nomi delle colonne al posto delle lettere.
    # La guida si estende fino a circa 170 caratteri: oltre, una riga non si legge piu'.
    fino, somma = 1, 0
    while fino < len(colonne) and somma + _larghezza(ws, fino) < 170:
        somma += _larghezza(ws, fino)
        fino += 1
    guida(ws, spec["foglio"], fino)
    # Un nome definito ASSOLUTO per ogni colonna: le viste usano questi.
    for c in colonne:
        l = lettera(nome_tabella, c["nome"])
        nome_definito(wb, f"{PREFISSI[nome_tabella]}_{c['nome']}", ass(spec["foglio"], l, PRIMA_RIGA_DATI, MAX_RIGHE))
    return ws


def convalida_lista(ws, intervallo, valori_o_formula):
    formula = valori_o_formula if valori_o_formula.startswith("=") else f'"{valori_o_formula}"'
    dv = DataValidation(type="list", formula1=formula, allow_blank=True)
    dv.add(intervallo)
    ws.add_data_validation(dv)


def fuori_dal_grafico(grafico):
    """Titolo e legenda NON sovrapposti all'area del grafico. openpyxl non scrive
    l'attributo 'overlay' ed Excel, senza, li disegna sopra linee ed etichette."""
    if grafico.title is not None:
        grafico.title.overlay = False
    if grafico.legend is not None:
        grafico.legend.overlay = False


def asse_fisso(grafico, minimo, massimo, passo=1):
    fuori_dal_grafico(grafico)
    grafico.y_axis.scaling.min = minimo
    grafico.y_axis.scaling.max = massimo
    grafico.y_axis.majorUnit = passo
    # openpyxl >= 3.1 marca gli assi come eliminati: senza questo Excel li nasconde.
    grafico.x_axis.delete = False
    grafico.y_axis.delete = False
    # Un colore per serie, non per punto: con varyColors (default di openpyxl)
    # un radar a una serie mostra in legenda le categorie come se fossero serie.
    grafico.varyColors = False
    if isinstance(grafico, LineChart):
        for serie in grafico.series:
            serie.smooth = False             # le curve fra punti trimestrali inventano valori intermedi
            serie.marker.symbol = "circle"   # un rischio con un solo ciclo deve comunque vedersi


# ============================================================== FOGLI
def foglio_parametri(wb):
    ws = wb["Parametri"]
    titolo(ws, "Parametri: pesi, soglie, urgenza e anagrafica dei rischi", 14)
    ws.column_dimensions["A"].width = 38
    ws.column_dimensions["B"].width = 14
    ws.column_dimensions["C"].width = 26

    # Pesi della decisione D-50 (rubrica, sezione 1): media pesata delle dimensioni valutate; se la
    # Velocity manca, i pesi si ridistribuiscono sulle altre tre (formula Score_Composito della mappa).
    ws["A3"] = "Pesi dello Score_Composito (D-50)"; ws["A3"].font = GRASSETTO
    for riga, (etichetta, nome, valore) in enumerate([
            ("Impatto", "pesoImpatto", 0.35), ("Probabilita", "pesoProbabilita", 0.25),
            ("Prossimita'", "pesoProssimita", 0.20), ("Velocity (solo se valutata)", "pesoVelocity", 0.20)], start=4):
        ws.cell(row=riga, column=1, value=etichetta)
        c = ws.cell(row=riga, column=2, value=valore); c.fill = INPUT; c.number_format = "0.00"
        nome_definito(wb, nome, f"Parametri!$B${riga}")
    ws["A8"] = "Somma dei pesi"
    ws["B8"] = "=SUM(B4:B7)"
    ws["C8"] = '=IF(ROUND(B8,6)=1,"OK","I PESI NON SOMMANO A 1")'

    ws["A10"] = "Soglie"; ws["A10"].font = GRASSETTO
    ws["A11"] = "Soglia di direzione (segnali netti in 4 settimane)"
    ws["B11"] = 2; ws["B11"].fill = INPUT        # D-61 (era 3)
    nome_definito(wb, "sogliaDirezione", "Parametri!$B$11")
    ws["A12"] = "Soglia di evidenziazione del Delta composito"
    ws["B12"] = 0.30; ws["B12"].fill = INPUT; ws["B12"].number_format = "0.00"     # D-61 (era 0,40)
    nome_definito(wb, "sogliaDelta", "Parametri!$B$12")

    ws["A14"] = "Cicli del radar"; ws["A14"].font = GRASSETTO
    # D-75: periodi delle viste scritti dallo script (imposta_ciclo) quando cambia il ciclo corrente, anche uno
    # straordinario AAAAQn-Sk; prima del 08/10/2026 erano formule che contavano solo trimestri.
    def trimestri_prima(c, n):
        out = []
        for _ in range(n):
            anno, q = int(c[:4]), int(c[5])
            c = f"{anno - 1}Q4" if q == 1 else f"{anno}Q{q - 1}"
            out.append(c)
        return out
    ws["A15"] = "Ciclo corrente (scritto dalla scrittura A2)"
    ws["B15"] = CICLO_CORRENTE; ws["B15"].fill = INPUT
    nome_definito(wb, "cicloCorrente", "Parametri!$B$15")
    ws["A16"] = "Periodo precedente (anche uno straordinario; scritto dallo script)"; ws["B16"] = trimestri_prima(CICLO_CORRENTE, 1)[0]
    nome_definito(wb, "cicloPrecedente", "Parametri!$B$16")
    ws["A17"] = "Trimestre di due trimestri prima (Delta 6 mesi; scritto dallo script)"; ws["B17"] = trimestri_prima(CICLO_CORRENTE, 2)[1]
    nome_definito(wb, "cicloMeno2", "Parametri!$B$17")
    ws["A18"] = "Data di riferimento del ciclo corrente (scritta dallo script)"
    ws["B18"] = DATE_CICLO[CICLO_CORRENTE]; ws["B18"].number_format = "dd/mm/yyyy"
    nome_definito(wb, "dataRiferimento", "Parametri!$B$18")

    ws["A19"] = "Periodi del trend (dal piu' vecchio; straordinari compresi; scritti dallo script)"; ws["A19"].font = GRASSETTO
    for i, c in enumerate(trimestri_prima(CICLO_CORRENTE, 7)[::-1] + [CICLO_CORRENTE]):   # righe 20..27, la 27 e' il corrente
        r = 20 + i
        ws.cell(row=r, column=1, value=f"T-{7 - i}" if i < 7 else "T (corrente)")
        ws.cell(row=r, column=2, value=c)
    nome_definito(wb, "cicliTrend", "Parametri!$B$20:$B$27")

    ws["A29"] = "Settimane"; ws["A29"].font = GRASSETTO
    ws["A30"] = "Settimana corrente (lunedi', scritta dalla scrittura A3)"
    ws["B30"] = SETTIMANA_CORRENTE; ws["B30"].fill = INPUT; ws["B30"].number_format = "dd/mm/yyyy"
    nome_definito(wb, "settimanaCorrente", "Parametri!$B$30")
    ws["A31"] = "Inizio finestra del badge (4 settimane)"
    ws["B31"] = "=settimanaCorrente-21"; ws["B31"].number_format = "dd/mm/yyyy"
    nome_definito(wb, "inizioFinestra4", "Parametri!$B$31")
    ws["A33"] = "Finestra di 12 settimane (dal piu' vecchio)"; ws["A33"].font = GRASSETTO
    for i in range(12):  # righe 34..45
        c = ws.cell(row=34 + i, column=2, value=f"=settimanaCorrente-7*{11 - i}")
        c.number_format = "dd/mm/yyyy"
    nome_definito(wb, "settimane12", "Parametri!$B$34:$B$45")

    # URGENZA (disuguaglianza di Mosca, rubrica sezione 8): X + Y > Z => agire ora.
    ws["A47"] = "Urgenza — disuguaglianza di Mosca (X + Y > Z = agire ora)"; ws["A47"].font = GRASSETTO
    ws["A48"] = "X: anni per decidere e avviare la mitigazione"
    ws["B48"] = 0.25; ws["B48"].fill = INPUT
    nome_definito(wb, "moscaX", "Parametri!$B$48")
    ws["A49"] = "Y di riserva: anni di mitigazione se il rischio non ha azioni"
    ws["B49"] = 1; ws["B49"].fill = INPUT
    nome_definito(wb, "moscaYDefault", "Parametri!$B$49")
    ws["A50"] = "Z: anni prima che il rischio possa manifestarsi, per Prossimita' (meta' della fascia)"; ws["A50"].font = GRASSETTO
    # D-59: Z = meta' della fascia del descrittore (con l'inizio della fascia la Prossimita 4 valeva
    # 0 come la 5 e quasi tutti i rischi finivano in AGIRE ORA).
    for k, (anni, testo) in enumerate([(3.5, "1 — oltre 3 anni"), (2.5, "2 — 2-3 anni"), (1.5, "3 — 1-2 anni"),
                                       (0.5, "4 — entro 12 mesi"), (0, "5 — in corso o imminente")]):
        ws.cell(row=51 + k, column=1, value=f"Prossimita {testo}")
        c = ws.cell(row=51 + k, column=2, value=anni); c.fill = INPUT
    nome_definito(wb, "anniProssimita", "Parametri!$B$51:$B$55")

    # Livello di allerta (D-63, rubrica sezione 8): calcolato dal Radar_Mosca, colore dei cerchi nel radar.
    ws["A59"] = "Livello di allerta (colore del radar)"; ws["A59"].font = GRASSETTO
    for riga, (etichetta, nome, valore, formato) in enumerate([
            ("P x I alta da (aggravante A1)", "livelloPxI", 12, "0"),
            ("Quota dei KRI in ambra o rosso da (aggravante A3)", "livelloQuotaKRI", 0.5, "0%"),
            ("Margine stretto: sotto (anni)", "livelloMargine", 1, "0.00"),
            ("Segnali forti per l'Attivazione", "livelloForti", 2, "0")], start=60):
        ws.cell(row=riga, column=1, value=etichetta)
        c = ws.cell(row=riga, column=2, value=valore); c.fill = INPUT; c.number_format = formato
        nome_definito(wb, nome, f"Parametri!$B${riga}")

    # Registro unico (D-79, rubrica sezione 9): chi entra nel radar di Mosca. La regola la applica lo script
    # (07_Senza_Studio/radar.py) a ogni ciclo e a ogni validazione, leggendo queste celle.
    ws["A65"] = "Registro unico: chi entra nel radar di Mosca (D-79)"; ws["A65"].font = GRASSETTO
    for riga, (etichetta, nome, valore, minimo, massimo, spiegazione) in enumerate([
            (f"Capienza del radar (fino a {MAX_RISCHI})", "capienzaRadar", CAPIENZA_RADAR, 1, MAX_RISCHI,
             "rischi con gestione completa: KRI, azioni, urgenza, report, schede"),
            ("Soglia di Prossimita' per entrare", "sogliaProssimitaRadar", 2, 1, 5, "2 = puo' manifestarsi entro 3 anni"),
            ("Soglia di Probabilita' per entrare", "sogliaProbabilitaRadar", 2, 1, 5, "2 = non solo teorico"),
            ("Cicli sotto la soglia prima di uscire", "cicliUscitaRadar", 2, 1, 2,
             "1 = esce subito; 2 = un ciclo come \"Radar, in uscita\"")], start=66):
        ws.cell(row=riga, column=1, value=etichetta)
        c = ws.cell(row=riga, column=2, value=valore); c.fill = INPUT
        ws.cell(row=riga, column=3, value=spiegazione).font = NOTA
        nome_definito(wb, nome, f"Parametri!$B${riga}")
        dv = DataValidation(type="whole", operator="between", formula1=str(minimo), formula2=str(massimo),
                            error=f"{etichetta}: un intero da {minimo} a {massimo}.", showErrorMessage=True)
        dv.add(f"B{riga}")
        ws.add_data_validation(dv)
    ws["A70"] = "Rischi in osservazione al massimo (fisso)"
    ws["B70"] = MAX_OSSERVAZIONE
    ws["C70"] = "oltre, A1 lascia fuori i meno rilevanti"; ws["C70"].font = NOTA
    nome_definito(wb, "capienzaOsservazione", str(MAX_OSSERVAZIONE))
    regola = ("LA REGOLA (la applica lo script a ogni ciclo e a ogni validazione). 1. Entra nel radar un rischio con "
              "Prossimita' e Probabilita' almeno pari alle soglie. 2. Restano sempre nel radar, anche sotto le soglie: un "
              "rischio AGIRE ORA, un tema all'attenzione del supervisore (◆), un rischio che il validatore mette nel radar "
              "(colonna Decisione sullo stato del foglio Validazione, con la Motivazione); mai nel radar un rischio che il "
              "validatore mette in osservazione. 3. Se i candidati sono piu' dei posti: prima le eccezioni, poi i piu' alti "
              "per score composito; gli altri restano in osservazione \"fuori per capienza\". 4. Un rischio del radar sotto "
              "la regola resta un ciclo come \"Radar, in uscita\" (con i cicli prima dell'uscita a 2), poi passa in "
              "osservazione; un rischio che sale entra subito, con i KRI e le azioni che A1 scrive. In osservazione: "
              "stessa scala e stesso score, niente KRI ne' azioni (fogli Osservazione e Fenomeni).")
    ws["A71"] = regola
    ws["A71"].alignment = A_CAPO
    ws.merge_cells("A71:C75")
    for r in range(71, 76):
        ws.row_dimensions[r].height = 30

    # Etichetta del ciclo nella fascia del titolo di ogni foglio: ciclo (straordinario se AAAAQn-Sk), data di
    # riferimento (dataRiferimento, D-75), stato di validazione, riservatezza. Niente TEXT: dipende dalla lingua.
    ws["A57"] = "Etichetta del ciclo (fascia del titolo)"; ws["A57"].font = GRASSETTO
    d = "dataRiferimento"
    ws["B57"] = (f'=IF(cicloCorrente="","nessun ciclo",IF(ISNUMBER(SEARCH("-S",cicloCorrente)),"Ciclo straordinario ","Ciclo ")'
                 f'&cicloCorrente&IF(ISNUMBER({d})," · dati al "&DAY({d})&"/"&RIGHT("0"&MONTH({d}),2)&"/"&YEAR({d}),"")'
                 f'&" · "&IF(decisioniDaPrendere>0,"da validare","validato"))&" · {ETICHETTA_RISERVATEZZA}"')
    nome_definito(wb, "etichettaCiclo", "Parametri!$B$57")

    # D-74: categorie della tassonomia interna (i nomi codiciL1/nomiL1 restano quelli di prima).
    n = len(TASSONOMIA)
    ws["E3"] = "Tassonomia interna — categorie di rischio in perimetro (D-74)"; ws["E3"].font = GRASSETTO
    for i, (cod, nome) in enumerate(TASSONOMIA):
        ws.cell(row=4 + i, column=5, value=cod)
        ws.cell(row=4 + i, column=6, value=nome)
    nome_definito(wb, "codiciL1", f"Parametri!$E$4:$E${3 + n}")
    nome_definito(wb, "nomiL1", f"Parametri!$F$4:$F${3 + n}")
    d0 = 5 + n                                             # riga del titolo dei driver
    ws[f"E{d0}"] = "Driver emergenti"; ws[f"E{d0}"].font = GRASSETTO
    for i, (cod, nome) in enumerate(DRIVER):
        ws.cell(row=d0 + 1 + i, column=5, value=cod)
        ws.cell(row=d0 + 1 + i, column=6, value=nome)
    nome_definito(wb, "codiciDriver", f"Parametri!$E${d0 + 1}:$E${d0 + len(DRIVER)}")
    nome_definito(wb, "nomiDriver", f"Parametri!$F${d0 + 1}:$F${d0 + len(DRIVER)}")
    ws.column_dimensions["E"].width = 10
    ws.column_dimensions["F"].width = 50

    # Anagrafica dei rischi attivi: H..O, righe 4..(3+MAX_RISCHI). H-K dal ciclo
    # trimestrale (A1, scritte dallo script); L-O input del validatore (gialle).
    ws["H2"] = ("ANAGRAFICA DEI RISCHI NEL RADAR DI MOSCA (registro unico, D-79: lo script vi mette e toglie i rischi con "
                "la regola delle righe 65-75; quelli in osservazione stanno solo nel RiskRegister) — colonne H-K: lo script "
                "le scrive a ogni ciclo trimestrale dalla valutazione di A1. Colonne gialle L-O: le decide il validatore e restano da un ciclo all'altro (M = anni di "
                "adeguamento: li stima A1 e li scrive la validazione, correggibili a mano; O = presidio dei controlli, "
                "giudizio della Banca fuori dallo score). Un rischio si toglie solo con il comando 'dismetti': "
                "una riga vuota in mezzo toglierebbe dal radar l'ultimo rischio.")
    ws["H2"].font = Font(bold=True, color=PROCESSI["trimestrale"][1])
    ws["H2"].alignment = A_CAPO
    ws.merge_cells("H2:O2")
    intest = [c["nome"] for c in MAPPA["anagrafica"]["colonne"]]
    input_validatore = ("Owner", "Anni_Adeguamento", "Attenzione_Supervisore", "Presidio_Controlli")
    for j, c in enumerate(MAPPA["anagrafica"]["colonne"]):
        cella = ws.cell(row=3, column=8 + j, value=c["nome"])
        colora(cella, "validazione" if c["nome"] in input_validatore else "trimestrale")
        cella.alignment = A_CAPO
    for i, (rid, nome, et, drv, owner, _) in enumerate(ANAGRAFICA):
        for j, v in enumerate([rid, nome, et, ", ".join(drv)]):
            ws.cell(row=4 + i, column=8 + j, value=v).fill = GRIGIO
    fine = 3 + MAX_RISCHI
    # L = Owner, M = Anni_Adeguamento (Y minima di Mosca), N = Attenzione_Supervisore
    # (◆ nel radar), O = Presidio_Controlli (D-49): input del validatore, gialli anche nelle righe libere.
    for i in range(MAX_RISCHI):
        rid = ANAGRAFICA[i][0] if i < len(ANAGRAFICA) else None
        for col, valore in ((12, ANAGRAFICA[i][4] if rid else None), (13, ANNI_ADEGUAMENTO.get(rid)),
                            (14, (ATTENZIONE_SUPERVISORE.get(rid, "No") if rid else None)),
                            (15, (PRESIDIO_ESEMPIO.get(rid, PRESIDI[0]) if rid else None))):
            ws.cell(row=4 + i, column=col, value=valore).fill = INPUT
    dv = DataValidation(type="decimal", operator="between", formula1="0", formula2="30", allow_blank=True,
                        error="Anni di adeguamento: un numero da 0 a 30, oppure vuoto.", showErrorMessage=True)
    dv.add(f"M4:M{fine}")
    ws.add_data_validation(dv)
    convalida_lista(ws, f"N4:N{fine}", "Sì,No")
    convalida_lista(ws, f"O4:O{fine}", ",".join(PRESIDI))
    nome_definito(wb, "anagrafica", f"Parametri!$H$4:$O${fine}")
    for j, nome in enumerate(intest):
        l = get_column_letter(8 + j)
        nome_definito(wb, f"ANA_{nome}", f"Parametri!${l}$4:${l}${fine}")
    for l, w in zip("HIJKLMNO", [10, 50, 10, 18, 34, 13, 13, 15]):
        ws.column_dimensions[l].width = w
    ws.row_dimensions[3].height = 30
    convalida_lista(ws, f"J4:J{fine}", "=codiciL1")
    # Versione della struttura: la legge lo script di campo (esegui_ciclo_locale.py).
    nome_definito(wb, "versioneTemplate", f'"{VERSIONE_TEMPLATE}"')
    guida(ws, "Parametri", 6)
    # La riga 2 ospita anche la nota dell'anagrafica (H2:O2): altezza per il piu' lungo dei due.
    nota = _righe_stimate(ws["H2"].value, sum(_larghezza(ws, j) for j in range(8, 16)) * 1.0) * 15 + 5
    ws.row_dimensions[2].height = max(ws.row_dimensions[2].height, nota)
    # Stampa (30/09 sera): orizzontale, parametri e anagrafica (A-O) in una pagina di larghezza.
    imposta_stampa(ws, f"A1:O{max(75, fine)}")


def lunedi_di(giorno):
    return giorno - timedelta(days=giorno.weekday())


def osservazione_esempio():
    """Righe del RiskRegister dei rischi in osservazione dei dati di esempio (D-79): stesse colonne dei rischi del
    radar; lo stato lo mette applica_stati_esempio."""
    righe = []
    for rid, nome, et, drv, owner, descr, raz, oriz, segn, fonti, storia in OSSERVAZIONE_ESEMPIO:
        for ciclo, (imp, vel, pro, prob, esito, periodo) in storia.items():
            var = VARIAZIONI_OSSERVAZIONE.get((ciclo, rid), [])
            righe.append({
                "Ciclo": ciclo, "Data_Riferimento": DATE_CICLO[ciclo], "ID_Rischio": rid, "Nome": nome,
                "Event_Type": et, "Driver": ", ".join(drv), "Impatto": imp, "Velocity": vel,
                "Prossimita": pro, "Probabilita": prob, "Anni_Adeguamento": None, "Rilievi": None,
                "Esito": esito, "Descrizione": descr, "Razionale": raz,
                "Variazioni": json.dumps([{"dimensione": d, "da": a, "a": b, "evidenza": ev, "data_evidenza": dt}
                                          for d, a, b, ev, dt in var], ensure_ascii=False),
                "Fonti": json.dumps([{"riferimento": r, "data": d, "tipo": t, "rilevanza": ril} for r, d, t, ril in fonti
                                     if d <= DATE_CICLO[periodo].isoformat()], ensure_ascii=False),
                "Owner": owner, "Data_Scrittura": DATE_CICLO[ciclo], "Approvato_Da": VALIDATORE,
                "Validazione": "Accettato", "Data_Validazione": DATE_CICLO[periodo] + timedelta(days=15),
                "Periodo_Valutazione": periodo, "Orizzonte_Anni": oriz, "Segnale_Avvicinamento": segn,
            })
    return righe


def applica_stati_esempio(register, azioni):
    """Stato, motivo e movimento di ogni riga del RiskRegister di esempio con la regola del registro unico (D-79),
    ciclo per ciclo come lo script: stesso modulo radar.py, valori del template."""
    regola = dict(radar.REGOLA_DEFAULT, capienza=CAPIENZA_RADAR, max_radar=MAX_RISCHI, max_osservazione=MAX_OSSERVAZIONE)
    prima = {}
    for ciclo in DATE_CICLO:
        righe = [r for r in register if r["Ciclo"] == ciclo]
        stati = radar.stati([{
            "id": r["ID_Rischio"], "impatto": r["Impatto"], "probabilita": r["Probabilita"],
            "prossimita": r["Prossimita"], "velocity": r["Velocity"],
            "supervisore": ATTENZIONE_SUPERVISORE.get(r["ID_Rischio"]) == "Sì",
            "anni_adeguamento": r["Anni_Adeguamento"],
            "y_azioni": radar.y_azioni([a["Orizzonte"] for a in azioni if a["ID_Rischio"] == r["ID_Rischio"]
                                        and a["Ciclo"] == r["Periodo_Valutazione"] and a["Stato"] != "Respinta"]),
            "stato_prima": prima.get(r["ID_Rischio"]), "decisione": radar.AUTOMATICO} for r in righe], regola)
        for r in righe:
            s = stati[r["ID_Rischio"]]
            r.update(Stato=s["stato"], Motivo_Stato=s["motivo"], Movimento=s["movimento"] or None,
                     Decisione_Stato=radar.AUTOMATICO)
            prima[r["ID_Rischio"]] = s["stato"]
    attesi = {r["ID_Rischio"] for r in register if r["Stato"] == radar.OSSERVAZIONE}
    assert attesi == {x[0] for x in OSSERVAZIONE_ESEMPIO}, f"rischi di esempio nello stato sbagliato: {attesi}"
    return register


def dati_esempio():
    anag = {r[0]: r for r in ANAGRAFICA}
    rettifiche = {(o, i, c): (prop, dec, val, mot) for o, i, c, prop, dec, val, mot in RETTIFICHE_ESEMPIO}
    rettificati = {(o, i): dec for o, i, _, _, dec, _, _ in RETTIFICHE_ESEMPIO}

    def esito_validazione(oggetto, ident, ciclo):
        return rettificati.get((oggetto, ident), "Accettato") if ciclo == CICLO_CORRENTE else "Accettato"

    register = []
    for ciclo, rischi in STORIA.items():
        for rid, (sev, vel, pro, esito, var) in rischi.items():
            _, nome, et, drv, owner, descr = anag[rid]
            register.append({
                "Ciclo": ciclo, "Data_Riferimento": DATE_CICLO[ciclo], "ID_Rischio": rid, "Nome": nome,
                "Event_Type": et, "Driver": ", ".join(drv), "Impatto": sev, "Velocity": vel,
                "Prossimita": pro, "Probabilita": PROBABILITA[rid], "Anni_Adeguamento": ANNI_ADEGUAMENTO.get(rid),
                "Rilievi": RILIEVI_ESEMPIO.get((ciclo, rid)),
                "Esito": esito, "Descrizione": descr, "Razionale": RAZIONALI[rid],
                "Variazioni": json.dumps([{"dimensione": d, "da": a, "a": b, "evidenza": ev, "data_evidenza": dt}
                                          for d, a, b, ev, dt in var], ensure_ascii=False),
                # Solo le fonti gia' esistenti alla data del ciclo: un esempio non cita il futuro.
                "Fonti": json.dumps([{"riferimento": r, "data": d, "tipo": t, "rilevanza": ril} for r, d, t, ril in FONTI[rid]
                                     if d <= DATE_CICLO[ciclo].isoformat()], ensure_ascii=False),
                "Owner": owner, "Data_Scrittura": DATE_CICLO[ciclo], "Approvato_Da": VALIDATORE,
                "Validazione": esito_validazione("Rischio", rid, ciclo),
                "Data_Validazione": DATE_CICLO[ciclo] + timedelta(days=15), "Periodo_Valutazione": ciclo,
                "Orizzonte_Anni": None, "Segnale_Avvicinamento": None,
            })
    register += osservazione_esempio()
    register.sort(key=lambda r: r["Ciclo"])                    # una riga per rischio per ciclo, ciclo dopo ciclo
    azioni = []
    for rid, descr, owner, oriz, raz, stato in AZIONI_ESEMPIO:
        ida = f"{CICLO_CORRENTE}-{rid}-A1"
        azioni.append({"Ciclo": CICLO_CORRENTE, "ID_Rischio": rid, "ID_Azione": ida,
                       "Descrizione": descr, "Owner": owner, "Orizzonte": oriz,
                       "Razionale": raz, "Stato": stato, "Data_Decisione": DATA_VALIDAZIONE_Q2, "Decisa_Da": VALIDATORE,
                       "Validazione": esito_validazione("Azione", ida, CICLO_CORRENTE)})
    # KRI: storico, una riga per KRI per ciclo, a partire dal ciclo di definizione.
    applica_stati_esempio(register, azioni)
    kri = []
    for i, ciclo in enumerate(DATE_CICLO):
        for kid, rid, tipo, nome, unita, fonte, att, all_, cdef, valori in KRI_ESEMPIO:
            if ciclo < cdef:
                continue
            val = valori[i]
            kri.append({"Ciclo": ciclo, "KRI_ID": kid, "ID_Rischio": rid, "Tipo": tipo, "Nome": nome, "Unita": unita,
                        "Fonte_Dati": fonte,
                        "Soglia_Attenzione": att, "Soglia_Allerta": all_, "Valore_Corrente": val,
                        "Data_Rilevazione": DATE_CICLO[ciclo] if val is not None else None,
                        "Fonte_Rilevazione": fonte if val is not None else None,
                        "Nota_Rilevazione": "Rilevazione di fine trimestre." if val is not None else "Dato non ancora prodotto dalla fonte.",
                        "In_Vigore": "Sì", "Ciclo_Definizione": cdef, "Ciclo_Aggiornamento": cdef,
                        "Razionale": (f"KRI di {tipo.lower()} del rischio {rid}: "
                                      + ("quanto la Banca e' esposta" if tipo == "Esposizione" else "quanto cresce il fenomeno")
                                      + "; valori crescenti indicano peggioramento."),
                        "Validazione": esito_validazione("KRI", kid, ciclo)})
    news = []
    for dt, nid, tit, fonte, codice, rid, seg, imp, sint in NEWS_ESEMPIO:
        riga = {"Data": dt, "ID_Notizia": nid, "Titolo": tit, "Fonte": fonte, "Codice_Fonte": codice, "Rischio_ID": rid,
                "Segnale": seg, "Sintesi": sint, "Validazione": "Accettato"}
        for cod, _ in TASSONOMIA:
            riga["Imp_" + cod.replace("-", "_").replace(".", "_")] = imp.get(cod, 0)
        news.append(riga)

    # Storico delle validazioni: righe del ciclo 2026Q2 (rischi, KRI, azioni) e delle notizie, tutte gia'
    # decise e applicate, come le scrive il comando valida dalla griglia (D-67): una Motivazione per oggetto,
    # riportata su ogni suo campo; Respingi vale per tutti i campi dell'oggetto. Il registro contiene i valori VALIDATI.
    oggetti = MAPPA["validazione"]["oggetti"]
    validazione = []

    def righe_oggetto(oggetto, righe, periodo_di, data):
        spec = oggetti[oggetto]
        for r in righe:
            ident = r[spec["id"]]
            suoi = {c: v for (o, i, c), v in rettifiche.items() if (o, i) == (oggetto, ident)}
            respinto = any(dec == "Respinto" for _, dec, _, _ in suoi.values())
            mot = next((m for _, _, _, m in suoi.values()), MOTIVAZIONI_ESEMPIO.get((oggetto, ident)))
            for campo in spec["campi"]:
                if respinto:
                    prop, dec, val = r[campo], "Respinto", None
                elif campo in suoi:
                    prop, dec, val, _ = suoi[campo]
                else:
                    prop, dec, val = r[campo], "Accettato", r[campo]
                validazione.append({"Periodo": periodo_di(r), "Oggetto": oggetto, "ID": r[spec["id"]],
                                    "Nome": r[spec["nome"]], "Campo": campo, "Proposta_Agente": prop,
                                    "Decisione": dec, "Valore_Validato": val, "Motivazione": mot,
                                    "Validato_Da": VALIDATORE, "Data_Validazione": data(r), "Stato": "Applicata"})

    corrente = lambda righe: [r for r in righe if r["Ciclo"] == CICLO_CORRENTE]
    # Un rischio riportato com'era (in osservazione, senza evidenza nuova) non si rivaluta: niente righe (D-79).
    righe_oggetto("Rischio", [r for r in corrente(register) if r["Periodo_Valutazione"] == CICLO_CORRENTE],
                  lambda r: CICLO_CORRENTE, lambda r: DATA_VALIDAZIONE_Q2)
    righe_oggetto("KRI", corrente(kri), lambda r: CICLO_CORRENTE, lambda r: DATA_VALIDAZIONE_Q2)
    righe_oggetto("Azione", azioni, lambda r: CICLO_CORRENTE, lambda r: DATA_VALIDAZIONE_Q2)
    # Periodo di una notizia = lunedi' in cui A3 l'ha valutata (la settimana DOPO la notizia),
    # come scrive il comando settimanale (Periodo = "settimana" dell'output di A3).
    righe_oggetto("Notizia", news, lambda r: (lunedi_di(r["Data"]) + timedelta(days=7)).isoformat(),
                  lambda r: lunedi_di(r["Data"]) + timedelta(days=9))
    return register, azioni, kri, news, validazione


def fogli_dati(wb):
    register, azioni, kri, news, validazione = dati_esempio()
    P = PRIMA_RIGA_DATI
    intervallo = lambda t, c: f"{lettera(t, c)}{P}:{lettera(t, c)}{MAX_RIGHE}"

    ws = scrivi_tabella(wb, "tblRegister", register, "RiskRegister — valutazioni dei rischi, una riga per rischio per ciclo")
    convalida_lista(ws, intervallo("tblRegister", "Event_Type"), "=codiciL1")
    convalida_lista(ws, intervallo("tblRegister", "Esito"), "Confermato,Variato,Nuovo")
    convalida_lista(ws, intervallo("tblRegister", "Stato"), ",".join(STATI_REGISTRO))
    convalida_lista(ws, intervallo("tblRegister", "Decisione_Stato"), ",".join(DECISIONI_STATO))

    ws = scrivi_tabella(wb, "tblAzioni", azioni, "Azioni — azioni di mitigazione proposte e loro stato")
    convalida_lista(ws, intervallo("tblAzioni", "Stato"), ",".join(STATI_AZIONE))

    ws = scrivi_tabella(wb, "tblKRI", kri, "KRI — storico degli indicatori, una riga per KRI per ciclo")
    stato = lettera("tblKRI", "Stato")
    colora_stato_kri(ws, f"{stato}{P}:{stato}{MAX_RIGHE}", f"{stato}{P}")

    ws = scrivi_tabella(wb, "tblNews", news, "NewsLog — notizie valutate ogni settimana")
    convalida_lista(ws, intervallo("tblNews", "Segnale"), ",".join(SEGNALI))

    ws = scrivi_tabella(wb, "tblSintesi", [
        {"Ciclo": ciclo, "Data_Riferimento": DATE_CICLO[ciclo], "Sintesi_A1": a1, "Sintesi_A5": a5,
         "Osservazioni_Controlli": oss, "Rilievi_Ciclo": None, "Rilievi_Superati": SUPERAMENTO_ESEMPIO.get(ciclo),
         "Data_Scrittura": DATE_CICLO[ciclo]}
        for ciclo, (a1, a5, oss) in SINTESI_ESEMPIO.items()], "Sintesi_Cicli — commento di A1 e sintesi di A5, una riga per ciclo")
    for riga in ws.iter_rows(min_row=P, max_row=P + len(SINTESI_ESEMPIO) - 1):
        for c in riga:
            c.alignment = A_CAPO

    ws = scrivi_tabella(wb, "tblSettimane", [
        {"Settimana": sett, "Notizie": n, "Sintesi_A3": testo, "Flag_Proposti": flag, "Data_Scrittura": sett}
        for sett, n, testo, flag in SETTIMANE_ESEMPIO], "Sintesi_Settimane — sintesi di A3 e flag proposti, una riga per settimana")
    for riga in ws.iter_rows(min_row=P, max_row=P + len(SETTIMANE_ESEMPIO) - 1):
        for c in riga:
            c.alignment = A_CAPO
    for c in ("A", "E"):
        for r in range(P, P + len(SETTIMANE_ESEMPIO)):
            ws[f"{c}{r}"].number_format = "dd/mm/yyyy"

    # STORICO DELLE VALIDAZIONI: una riga per oggetto e campo proposto da un agente. Non e' un foglio di input
    # (D-67: il validatore scrive nella griglia del foglio Validazione), quindi niente elenchi a discesa.
    ws = scrivi_tabella(wb, "tblValidazione", validazione,
                        "Storico_Validazioni — proposte degli agenti e decisioni, una riga per oggetto e campo")
    stato_v, dec_v = lettera("tblValidazione", "Stato"), lettera("tblValidazione", "Decisione")
    ws.conditional_formatting.add(f"{stato_v}{P}:{stato_v}{MAX_RIGHE}", FormulaRule(formula=[f'{stato_v}{P}="Da decidere"'], fill=AMBRA_CF))
    ws.conditional_formatting.add(f"{dec_v}{P}:{dec_v}{MAX_RIGHE}", FormulaRule(formula=[f'{dec_v}{P}="Rettificato"'], fill=AZZURRO_CF))
    ws.conditional_formatting.add(f"{dec_v}{P}:{dec_v}{MAX_RIGHE}", FormulaRule(formula=[f'{dec_v}{P}="Respinto"'], fill=ROSSO_CF))


# ============================================================== VISTE (struttura del 25/09 sera, D-39)
# Tutte le viste leggono i dati tramite nomi definiti. Il calcolo per posizione
# dell'anagrafica (ex Dashboard) sta in colonne nascoste del Registro, con i nomi
# pos*: posID, posNome, posImpatto, ... posScore, posBadge. Niente funzione TEXT (il
# formato dipende dalla lingua di Excel): i numeri nei testi passano da FIXED. Niente
# formule matriciali: gli elenchi ordinati usano AGGREGATE.

BLU_NOTTE, BLU_MEDIO, BLU_CHIARO = "1F3864", "2F5597", "DEEAF6"
ROSSO, AMBRA, GRIGIO_URG, BLU_DIM = "C00000", "FFC000", "A6A6A6", "2E75B6"
TESTO_TENUE = "595959"
ROSSO_TENUE, AMBRA_TENUE, VERDE_TENUE, FONDO_TENUE = "FBE5E5", "FFF2CC", "E2EFDA", "F2F2F2"
GIALLO_VIGILANZA = "FFC000"        # bordo dei temi all'attenzione del supervisore (D-35)
RIEMPIMENTO_CERCHIO = "9DC3E7"     # campioni delle aree nella legenda: genera() aggiunge la trasparenza nell'XML
# Livello di allerta (D-63): riempimento dei cerchi nel radar (colori usati solo qui: la trasparenza si aggiunge per colore)
# e fondo dell'ID nel Registro.
COL_LIVELLO = "AA"                  # Radar_Mosca: colonna del livello di allerta (U-Z i segnali, AB il motivo)
LIVELLI = [("Attivazione", "E06666", "F4CCCC"), ("Attenzione", "F6C342", "FFF2CC"), ("Monitoraggio", "93C47D", "D9EAD3")]
SCALA_DIM = {1: "F2F2F2", 2: "FCE4D6", 3: "F8CBAD", 4: "F4B183", 5: "C55A11"}
FORMATO_DELTA = '"▲ "+0.00;"▼ "-0.00;"● "0.00'
BORDO_SOTTILE = Border(bottom=Side(style="thin", color="D9D9D9"))
REG_PRIMA = 9                      # Registro: prima riga dei rischi (e del blocco per posizione)
POS = 27                           # Registro: prima colonna del blocco per posizione (AA), nascosto
MAX_AZIONI_PIANO = 150             # righe del Piano_azioni (nome costante capienzaPianoAzioni)
QUADRO_SEGNALATI = 45              # Quadro: prima riga dei rischi segnalati
# Colonne visibili del Registro (intestazione, larghezza): le lettere si calcolano da qui, mai scritte a mano.
COLONNE_REGISTRO = [("ID", 9), ("Nome", 38), ("Categoria", 8), ("Imp", 6), ("Prob", 6), ("Pross", 6), ("Vel", 6),
                    ("Score", 8), ("Δ ciclo prima", 9), ("Δ 6 mesi", 9), ("Urgenza", 16), ("Margine (anni)", 8),
                    ("◆", 4), ("R", 4), ("A", 4), ("V", 4), ("Segnali netti", 11), ("Presidio", 13), ("Rilievi", 11),
                    ("Owner", 28)]
LEG_RISCHIO = ("NFR-nn = codice del rischio; ◆ = tema all'attenzione del supervisore (BCE, EBA, Banca d'Italia), "
               "indicato dal validatore")
LEG_MOSCA = ("X = anni per decidere e avviare la mitigazione (un trimestre); Y = anni per mitigare (azioni o adeguamento "
             "strutturale); Z = anni prima che il rischio possa manifestarsi (dalla Prossimita); AGIRE ORA = X + Y > Z")
LEG_PXI = "P = Probabilita, I = Impatto, P x I = Probabilita x Impatto, da 1 a 25"
LEG_DIM = ("Imp = Impatto (danno se il rischio si manifesta); Prob = Probabilita (plausibilita' per la Banca); Pross = "
           "Prossimita (quando puo' manifestarsi); Vel = Velocity (quanto in fretta arriva il danno; n.v. = non valutata, "
           "lo score usa le altre tre); Presidio = giudizio della Banca sui controlli (fuori dallo score)")
fill = lambda colore: PatternFill("solid", fgColor=colore, bgColor=colore)   # bgColor: vedi ROSSO_CF


def rich(sz=900, b=False, colore="262626"):
    c = CharacterProperties(sz=sz, b=b, solidFill=colore)
    return RichText(p=[Paragraph(pPr=ParagraphProperties(defRPr=c), endParaRPr=c)])


def titolo_da_cella(ws, cella):
    """Titolo di grafico preso da una cella con formula: il titolo dice il messaggio."""
    return Title(tx=Text(strRef=StrRef(f"'{ws.title}'!{cella}")), overlay=False)


def stile_grafico(grafico):
    """Niente bordo, griglia grigio chiaro, testi 9 pt."""
    grafico.graphical_properties = GraphicalProperties(ln=LineProperties(noFill=True))
    for asse in (grafico.x_axis, grafico.y_axis):
        asse.delete = False
        asse.txPr = rich(900, colore=TESTO_TENUE)
    if grafico.y_axis.majorGridlines is not None:
        grafico.y_axis.majorGridlines.spPr = GraphicalProperties(ln=LineProperties(solidFill="EDEDED"))
    if grafico.legend is not None:
        grafico.legend.position = "b"
        grafico.legend.overlay = False
        grafico.legend.txPr = rich(900, colore=TESTO_TENUE)
    if grafico.title is not None:
        grafico.title.overlay = False


def etichette_valore(serie, colore="262626", posizione="outEnd"):
    """Valore scritto accanto alla barra, nel formato della cella di origine: le celle delle serie
    "per esito" hanno un formato che nasconde lo zero (rischio senza barra in quella serie)."""
    serie.dLbls = DataLabelList(showVal=True, showSerName=False, showCatName=False, showLegendKey=False,
                                showPercent=False, dLblPos=posizione)
    serie.dLbls.txPr = rich(900, True, colore)


def sezione(ws, riga, da, a, testo):
    """Titolo di sezione: blu notte, riga sotto."""
    ws.merge_cells(start_row=riga, start_column=da, end_row=riga, end_column=a)
    c = ws.cell(row=riga, column=da, value=testo)
    c.font = Font(size=12, bold=True, color=BLU_NOTTE)
    for x in range(da, a + 1):
        ws.cell(row=riga, column=x).border = Border(bottom=Side(style="medium", color=BLU_NOTTE))


def legenda(ws, riga, ultima_col, testo, altezza=None):
    """Legenda delle abbreviazioni in fondo a un foglio (per esteso)."""
    ws.merge_cells(start_row=riga, start_column=1, end_row=riga, end_column=ultima_col)
    c = ws.cell(row=riga, column=1, value="Legenda — " + testo)
    c.font = Font(size=8, italic=True, color=TESTO_TENUE)
    c.alignment = Alignment(wrap_text=True, vertical="top")
    larghezza = sum(_larghezza(ws, j) for j in range(1, ultima_col + 1))
    ws.row_dimensions[riga].height = altezza or 11 * (len(testo) // max(1, int(larghezza * 1.4)) + 1) + 4


def chip_livello(ws, intervallo, prima):
    """Livello di allerta come etichetta colorata, con i colori del radar (D-63)."""
    for livello, colore, _ in LIVELLI:
        ws.conditional_formatting.add(intervallo, FormulaRule(formula=[f'{prima}="{livello}"'], fill=fill(colore),
                                                              font=Font(bold=True, color="FFFFFF" if livello == "Attivazione" else "262626")))


def chip_urgenza(ws, intervallo, prima):
    """Urgenza come etichetta colorata: rosso agire ora, ambra entro l'anno, grigio con margine."""
    ws.conditional_formatting.add(intervallo, FormulaRule(formula=[f'LEFT({prima},9)="AGIRE ORA"'], fill=fill(ROSSO),
                                                          font=Font(bold=True, color="FFFFFF")))
    ws.conditional_formatting.add(intervallo, FormulaRule(formula=[f'OR(LEFT({prima},11)="Agire entro",LEFT({prima},12)="Entro l\'anno")'],
                                                          fill=fill(AMBRA), font=Font(bold=True)))
    ws.conditional_formatting.add(intervallo, FormulaRule(formula=[f'LEFT({prima},7)="Margine"'], fill=fill("D9D9D9"),
                                                          font=Font(bold=True)))


def colora_dimensioni(ws, intervallo, prima, scala=SCALA_DIM):
    for v, colore in scala.items():
        ws.conditional_formatting.add(intervallo, FormulaRule(formula=[f"{prima}={v}"], fill=fill(colore),
                                                              font=Font(bold=True, color="FFFFFF" if v == 5 else "262626")))


def colora_delta(ws, intervallo, prima):
    ws.conditional_formatting.add(intervallo, FormulaRule(formula=[f"AND(ISNUMBER({prima}),{prima}>0)"], font=Font(color=ROSSO)))
    ws.conditional_formatting.add(intervallo, FormulaRule(formula=[f"AND(ISNUMBER({prima}),{prima}<0)"], font=Font(color=BLU_DIM)))


def cella_str(testo):
    """Stringa letterale di Excel (virgolette raddoppiate)."""
    return '"' + testo.replace('"', '""') + '"'


# JSON delle Variazioni e delle Fonti reso leggibile con SUBSTITUTE annidati (lo script
# lo scrive con json.dumps: separatori ", " e ": ").
COPPIE_VARIAZIONI = [('[{"dimensione": "', "• "), ('"}, {"dimensione": "', ")\n• "), ('", "da": ', " "), (', "a": ', " → "),
                     (', "evidenza": "', ": "), ('", "data_evidenza": "', " ("), ('"}]', ")"),
                     (" null → ", " n.v. → "), (" → null:", " → n.v.:")] + \
                    [(f"• {d.lower()}", f"• {d}") for d in ("Impatto", "Velocity", "Prossimita", "Confidence", "Probabilita")] + \
                    [("• severity", "• Impatto")]      # variazioni dei cicli scritti prima del 30/09 sera (D-57)


def json_leggibile(espr, coppie, vuoto):
    x = f'{espr}&""'
    for da, a in coppie:
        sost = cella_str(a).replace("\n", '"&CHAR(10)&"')
        x = f"SUBSTITUTE({x},{cella_str(da)},{sost})"
    return f'IF({espr}&""="[]","{vuoto}",{x})'


def nome_col(nome_tabella, colonna, foglio):
    l = lettera(nome_tabella, colonna)
    return f"{foglio}!${l}:${l}"


# ---------------------------------------------------------------- Registro
def foglio_registro(wb):
    """Il ciclo corrente, un rischio per riga, ordinato per score (sostituisce Dashboard e Approfondimento).
    Blocco nascosto per posizione dell'anagrafica (colonne da AA): lo usano tutte le viste."""
    ws = wb["Registro"]
    ultima_col = len(COLONNE_REGISTRO)
    titolo(ws, "Registro: il ciclo corrente", ultima_col)
    fine = REG_PRIMA + MAX_RISCHI - 1
    # Controlli: stato della validazione e copertura del ciclo (nomi letti dallo script).
    ws["A4"] = "VALIDAZIONE DEL CICLO"; colora(ws["A4"], "validazione")
    ws["B4"] = "Righe da validare"
    # D-67: righe della griglia di validazione (rischi, KRI, azioni del ciclo), non campi: si conta il primo campo.
    ws["D4"] = "=" + righe_da_validare()
    ws["E4"] = "Rettifiche applicate"
    ws["G4"] = '=COUNTIFS(VAL_Periodo,cicloCorrente,VAL_Decisione,"Rettificato",VAL_Stato,"Applicata")'
    ws["H4"] = '=IF(D4>0,"CICLO NON ANCORA VALIDATO — vedi foglio Validazione","Ciclo validato")'
    ws["A5"] = "CONTROLLO DI COPERTURA"; colora(ws["A5"], "calcolo")
    ws["B5"] = "Rischi in anagrafica"
    ws["D5"] = '=COUNTIF(ANA_ID,"NFR-*")'
    ws["E5"] = "Valutati nel ciclo"
    ws["G5"] = '=SUMPRODUCT((ANA_ID<>"")*(COUNTIFS(RR_ID_Rischio,ANA_ID,RR_Ciclo,cicloCorrente)>0))'
    ws["H5"] = '=IF(D5=G5,"Ciclo completo","CICLO INCOMPLETO — i rischi mancanti non sono valutazioni")'
    for c in ("H4", "H5"):
        ws[c].font = GRASSETTO
    ws.merge_cells("H4:N4"); ws.merge_cells("H5:N5")
    ws.conditional_formatting.add("H4", FormulaRule(formula=["$D$4>0"], fill=AMBRA_CF))
    ws.conditional_formatting.add("H4", FormulaRule(formula=["$D$4=0"], fill=VERDE_CF))
    ws.conditional_formatting.add("H5", FormulaRule(formula=["$D$5<>$G$5"], fill=ROSSO_CF))
    ws.conditional_formatting.add("H5", FormulaRule(formula=["$D$5=$G$5"], fill=VERDE_CF))
    for nome, cella in (("decisioniDaPrendere", "$D$4"), ("rettificheApplicate", "$G$4"), ("statoValidazione", "$H$4"),
                        ("coperturaAnagrafica", "$D$5"), ("coperturaValutati", "$G$5"), ("statoCopertura", "$H$5")):
        nome_definito(wb, nome, f"Registro!{cella}")

    # Blocco per posizione dell'anagrafica (nascosto): come la vecchia tabella della Dashboard.
    # Indici delle colonne nel blocco, per nome: nessuna lettera scritta a mano (le colonne cambiano con il modello).
    blocco = ["ID", "Nome", "Impatto", "Probabilita", "Prossimita", "Velocity", "Score", "ScorePrec", "Score2",
              "Netti", "Badge", "Chiave d'ordine", "Posizione del k-esimo", "Livello"]
    b = {nome: j for j, nome in enumerate(blocco)}
    for j, t in enumerate(blocco):
        ws.cell(row=REG_PRIMA - 1, column=POS + j, value=t)
    L = lambda nome: get_column_letter(POS + b[nome])
    dims = [("Impatto", "RR_Impatto", "cicloCorrente"), ("Probabilita", "RR_Probabilita", "cicloCorrente"),
            ("Prossimita", "RR_Prossimita", "cicloCorrente"), ("Velocity", "RR_Velocity", "cicloCorrente"),
            ("Score", "RR_Score_Composito", "cicloCorrente"), ("ScorePrec", "RR_Score_Composito", "cicloPrecedente"),
            ("Score2", "RR_Score_Composito", "cicloMeno2")]
    for i in range(MAX_RISCHI):
        r, k = REG_PRIMA + i, i + 1
        a = f"${L('ID')}{r}"
        ws[f"{L('ID')}{r}"] = f'=IF(Parametri!$H{4 + i}="","",Parametri!$H{4 + i})'
        ws[f"{L('Nome')}{r}"] = f'=IF({a}="","",Parametri!$I{4 + i})'
        for nome, nome_c, ciclo in dims:
            # "<>" = cella non vuota: una Velocity non valutata (vuota) resta #N/D, non zero.
            ws[f"{L(nome)}{r}"] = (f'=IF({a}="",NA(),IF(COUNTIFS(RR_ID_Rischio,{a},RR_Ciclo,{ciclo},{nome_c},"<>")=0,NA(),'
                                   f'SUMIFS({nome_c},RR_ID_Rischio,{a},RR_Ciclo,{ciclo})))')
        ws[f"{L('Netti')}{r}"] = (f'=IF({a}="","",'
                                  f'COUNTIFS(NW_Rischio_ID,{a},NW_Segnale,"Peggiorativo",NW_Settimana,">="&inizioFinestra4,NW_Settimana,"<="&settimanaCorrente)'
                                  f'-COUNTIFS(NW_Rischio_ID,{a},NW_Segnale,"Migliorativo",NW_Settimana,">="&inizioFinestra4,NW_Settimana,"<="&settimanaCorrente))')
        n = f"{L('Netti')}{r}"
        ws[f"{L('Badge')}{r}"] = (f'=IF({a}="","",IF({n}>=sogliaDirezione,"▲ +"&{n},IF({n}<=-sogliaDirezione,"▼ "&{n},'
                                  f'"● "&IF({n}>0,"+","")&{n})))')
        chiave = L("Chiave d'ordine")
        ws[f"{chiave}{r}"] = f'=IF({a}="","",IF(ISNUMBER({L("Score")}{r}),{L("Score")}{r},-1)-{k}/100000)'
        ws[f"{L('Posizione del k-esimo')}{r}"] = (f'=IFERROR(MATCH(_xlfn.AGGREGATE(14,6,${chiave}${REG_PRIMA}:${chiave}${fine},{k}),'
                                                  f'${chiave}${REG_PRIMA}:${chiave}${fine},0),"")')
        ws[f"{L('Livello')}{r}"] = f'=IF({a}="","",Radar_Mosca!${COL_LIVELLO}${5 + i}&"")'     # D-63, per posizione
    for nome, colonna in [("posID", "ID"), ("posNome", "Nome"), ("posImpatto", "Impatto"), ("posProbabilita", "Probabilita"),
                          ("posProssimita", "Prossimita"), ("posVelocity", "Velocity"), ("posScore", "Score"),
                          ("posScorePrec", "ScorePrec"), ("posScore2", "Score2"),
                          ("posNetti", "Netti"), ("posBadge", "Badge"), ("posLivello", "Livello")]:
        nome_definito(wb, nome, f"Registro!${L(colonna)}${REG_PRIMA}:${L(colonna)}${fine}")
    for j in range(len(blocco)):
        ws.column_dimensions[get_column_letter(POS + j)].hidden = True

    # Tabella visibile, ordinata per score. Colonne da COLONNE_REGISTRO (una sola fonte per lettere e guide).
    C = {nome: get_column_letter(j) for j, (nome, _) in enumerate(COLONNE_REGISTRO, start=1)}
    gruppi = [(("ID", "Categoria"), "Rischio", "calcolo"), (("Imp", "Vel"), "Dimensioni 1-5 (A1, validate)", "trimestrale"),
              (("Score", "Margine (anni)"), "Calcolati dal foglio", "calcolo"), (("◆", "◆"), "Sup.", "validazione"),
              (("R", "V"), "KRI del ciclo", "trimestrale"), (("Segnali netti", "Segnali netti"), "Notizie · 4 settimane", "settimanale"),
              (("Presidio", "Presidio"), "Banca", "validazione"), (("Rilievi", "Rilievi"), "A5 e controlli", "calcolo"),
              (("Owner", "Owner"), "Anagrafica", "validazione")]
    indice = {nome: j for j, (nome, _) in enumerate(COLONNE_REGISTRO, start=1)}
    for (primo, ultimo), t, p in gruppi:
        da, a = indice[primo], indice[ultimo]
        if da != a:
            ws.merge_cells(start_row=REG_PRIMA - 2, start_column=da, end_row=REG_PRIMA - 2, end_column=a)
        c = ws.cell(row=REG_PRIMA - 2, column=da, value=t)
        for x in range(da, a + 1):
            ws.cell(row=REG_PRIMA - 2, column=x).fill = fill(PROCESSI[p][0])
        c.font = Font(size=9, bold=True, color=PROCESSI[p][1])
        c.alignment = Alignment(horizontal="center", wrap_text=True)
    for j, (t, _) in enumerate(COLONNE_REGISTRO, start=1):
        c = ws.cell(row=REG_PRIMA - 1, column=j, value=t)
        c.font = Font(size=9, bold=True)
        c.border = Border(bottom=Side(style="medium", color=BLU_NOTTE))
        c.alignment = Alignment(horizontal="center" if j > 2 else "left", vertical="bottom", wrap_text=True)
    ws.row_dimensions[REG_PRIMA - 2].height = 26
    ws.row_dimensions[REG_PRIMA - 1].height = 28
    pos_dim = {"Imp": "posImpatto", "Prob": "posProbabilita", "Pross": "posProssimita",
               "Score": "posScore"}
    for i in range(MAX_RISCHI):
        r = REG_PRIMA + i
        p = f"${L('Posizione del k-esimo')}{r}"
        vuoto = f'{p}=""'
        ws[f"{C['ID']}{r}"] = f'=IF({vuoto},"",INDEX(posID,{p}))'
        ws[f"{C['Nome']}{r}"] = f'=IF({vuoto},"",INDEX(posNome,{p}))'
        ws[f"{C['Categoria']}{r}"] = f'=IF({vuoto},"",INDEX(ANA_Event_Type,{p})&"")'
        for col, nome in pos_dim.items():         # NA() esplicito: il controllo degli errori lo riconosce come voluto
            ws[f"{C[col]}{r}"] = f'=IF({vuoto},"",IF(ISNUMBER(INDEX({nome},{p})),INDEX({nome},{p}),NA()))'
        # Velocity non valutata (D-50): "n.v.", non un errore.
        ws[f"{C['Vel']}{r}"] = f'=IF({vuoto},"",IF(ISNUMBER(INDEX(posVelocity,{p})),INDEX(posVelocity,{p}),"n.v."))'
        score = f"{C['Score']}{r}"
        for col, nome in (("Δ ciclo prima", "posScorePrec"), ("Δ 6 mesi", "posScore2")):
            ws[f"{C[col]}{r}"] = (f'=IF({vuoto},"",IF(ISNUMBER(INDEX({nome},{p})),IFERROR({score}-INDEX({nome},{p}),""),'
                                  f'IF(ISNUMBER({score}),"nuovo","")))')
        ws[f"{C['Urgenza']}{r}"] = f'=IF({vuoto},"",INDEX(Radar_Mosca!$L$5:$L${4 + MAX_RISCHI},{p})&"")'
        ws[f"{C['Margine (anni)']}{r}"] = f'=IF({vuoto},"",IFERROR(INDEX(Radar_Mosca!$K$5:$K${4 + MAX_RISCHI},{p}),""))'
        ws[f"{C['◆']}{r}"] = f'=IF({vuoto},"",IF(INDEX(ANA_Attenzione_Supervisore,{p})="Sì","◆",""))'
        ident = f"${C['ID']}{r}"
        for col, stato in (("R", "Rosso"), ("A", "Ambra"), ("V", "Verde")):
            ws[f"{C[col]}{r}"] = (f'=IF({ident}="","",COUNTIFS(KRI_ID_Rischio,{ident},KRI_Ciclo,cicloCorrente,KRI_In_Vigore,"Sì",'
                                  f'KRI_Stato,"{stato}"))')
            ws[f"{C[col]}{r}"].number_format = "0;-0;;@"
        ws[f"{C['Segnali netti']}{r}"] = f'=IF({vuoto},"",INDEX(posBadge,{p}))'
        ws[f"{C['Presidio']}{r}"] = f'=IF({vuoto},"",INDEX(ANA_Presidio_Controlli,{p})&"")'
        # Segnalazioni di A5 e dei controlli sul rischio nel ciclo (testo completo nel RiskRegister e nella colonna
        # Segnalazioni del foglio Validazione): ⚑ se almeno una e' da motivare (D-71; BLOCCANTE SUPERATO = registri
        # fino al 2026-10-02, D-56), altrimenti quante sono (una per riga).
        testo = f'IFERROR(INDEX(RR_Rilievi,MATCH(cicloCorrente&"|"&{ident},RR_Chiave,0))&"","")'
        ws[f"{C['Rilievi']}{r}"] = (f'=IF({ident}="","",IF(OR(ISNUMBER(SEARCH("DA MOTIVARE",{testo})),'
                                    f'ISNUMBER(SEARCH("BLOCCANTE SUPERATO",{testo}))),"⚑ da motivare",'
                                    f'IF({testo}="","",LEN({testo})-LEN(SUBSTITUTE({testo},CHAR(10),""))+1&" oss.")))')
        ws[f"{C['Owner']}{r}"] = f'=IF({vuoto},"",INDEX(ANA_Owner,{p})&"")'
        ws[f"{C['Score']}{r}"].number_format = "0.00"
        for col in ("Δ ciclo prima", "Δ 6 mesi"):
            ws[f"{C[col]}{r}"].number_format = FORMATO_DELTA
        ws[f"{C['Margine (anni)']}{r}"].number_format = "+0.00;-0.00;0.00"
        for j in range(1, ultima_col + 1):
            c = ws.cell(row=r, column=j)
            c.border = BORDO_SOTTILE
            c.alignment = Alignment(horizontal="center" if j > 2 else "left", vertical="center")
        ws.row_dimensions[r].height = 20
    rng = lambda col, fino=None: f"{C[col]}{REG_PRIMA}:{C[fino or col]}{fine}"
    colora_dimensioni(ws, rng("Imp", "Vel"), f"{C['Imp']}{REG_PRIMA}")
    ws.conditional_formatting.add(rng("Imp", "Score"), FormulaRule(formula=[f"ISNA({C['Imp']}{REG_PRIMA})"], font=FONT_NA))
    ws.conditional_formatting.add(rng("Vel"), FormulaRule(formula=[f'{C["Vel"]}{REG_PRIMA}="n.v."'], font=FONT_NA))
    ws.conditional_formatting.add(rng("Score"), DataBarRule(start_type="num", start_value=0, end_type="num",
                                                            end_value=5, color="8EA9DB"))
    colora_delta(ws, rng("Δ ciclo prima", "Δ 6 mesi"), f"{C['Δ ciclo prima']}{REG_PRIMA}")
    chip_urgenza(ws, rng("Urgenza"), f"{C['Urgenza']}{REG_PRIMA}")
    # D-63: fondo dell'ID = livello di allerta (nessuna colonna in piu'), dal blocco per posizione.
    livello_riga = (f"INDEX(${L('Livello')}${REG_PRIMA}:${L('Livello')}${fine},"
                    f"${L('Posizione del k-esimo')}{REG_PRIMA})")
    for livello, _, tenue in LIVELLI:
        ws.conditional_formatting.add(rng("ID"), FormulaRule(formula=[f'IFERROR({livello_riga}="{livello}",FALSE)'],
                                                             fill=fill(tenue), font=Font(bold=True)))
    for col, colore in (("R", ROSSO), ("A", AMBRA), ("V", "70AD47")):
        prima = f"{C[col]}{REG_PRIMA}"
        ws.conditional_formatting.add(rng(col), FormulaRule(formula=[f"AND(ISNUMBER({prima}),{prima}>0)"],
                                                           fill=fill(colore), font=Font(bold=True, color="FFFFFF" if col != "A" else "262626")))
    prima = f"{C['Segnali netti']}{REG_PRIMA}"
    ws.conditional_formatting.add(rng("Segnali netti"), FormulaRule(formula=[f'LEFT({prima},1)="▲"'], font=Font(bold=True, color=ROSSO)))
    ws.conditional_formatting.add(rng("Segnali netti"), FormulaRule(formula=[f'LEFT({prima},1)="▼"'], font=Font(bold=True, color=BLU_DIM)))
    prima = f"{C['Presidio']}{REG_PRIMA}"
    for valore, colore in (("Assente", ROSSO_TENUE), ("Parziale", AMBRA_TENUE), ("Adeguato", VERDE_TENUE),
                           ("Non verificato", FONDO_TENUE)):
        ws.conditional_formatting.add(rng("Presidio"), FormulaRule(formula=[f'{prima}="{valore}"'], fill=fill(colore)))
    prima = f"{C['Rilievi']}{REG_PRIMA}"
    ws.conditional_formatting.add(rng("Rilievi"), FormulaRule(formula=[f'LEFT({prima},1)="⚑"'], font=Font(bold=True, color=ROSSO)))
    for j, (_, larghezza) in enumerate(COLONNE_REGISTRO, start=1):
        ws.column_dimensions[get_column_letter(j)].width = larghezza
    ws[f"{C['◆']}{REG_PRIMA - 1}"].font = Font(size=9, bold=True, color="BF8F00")
    legenda(ws, fine + 2, ultima_col, f"Fondo dell'ID = livello di allerta (rosso attivazione, giallo attenzione, verde "
                                      f"monitoraggio: foglio Radar_Mosca). {LEG_DIM}; Δ = variazione dello score (ciclo prima, due cicli prima); Sup. / ◆ = tema "
                                      f"all'attenzione del supervisore; R, A, V = KRI in rosso, ambra, verde; Segnali netti = notizie "
                                      f"peggiorative meno migliorative nelle ultime 4 settimane (▲ ▼ oltre la soglia di Parametri); "
                                      f"Rilievi = segnalazioni di A5 e dei controlli sul rischio (⚑ = da motivare in validazione: "
                                      f"testo nel RiskRegister). Categoria = tassonomia interna della Banca (9.1 ... 9.13; FP fuori perimetro). {LEG_MOSCA}.")
    ws.freeze_panes = f"C{REG_PRIMA}"
    # Stampa (30/09 sera): orizzontale, tutte le colonne visibili in una pagina di larghezza.
    imposta_stampa(ws, f"A1:{get_column_letter(ultima_col)}{fine + 2}")
    ws.print_title_rows = f"{REG_PRIMA - 2}:{REG_PRIMA - 1}"


# ---------------------------------------------------------------- Storico (ex Trend)
def foglio_storico(wb):
    ws = wb["Storico"]
    titolo(ws, "Storico: score composito negli ultimi otto cicli", 10)
    ws["A4"] = "ID"; ws["B4"] = "Nome"
    for c in (ws["A4"], ws["B4"]):
        c.font = GRASSETTO
    for j in range(8):
        c = ws.cell(row=4, column=3 + j, value=f"=Parametri!$B${20 + j}")
        c.font = GRASSETTO
    for i in range(MAX_RISCHI):
        r = 5 + i
        ws[f"A{r}"] = f"=INDEX(posID,{i + 1})&\"\""
        ws[f"B{r}"] = f"=INDEX(posNome,{i + 1})&\"\""
        for j in range(8):
            l = get_column_letter(3 + j)
            ws[f"{l}{r}"] = (f'=IF(OR($A{r}="",{l}$4=""),NA(),IF(COUNTIFS(RR_ID_Rischio,$A{r},RR_Ciclo,{l}$4)=0,NA(),'
                             f'SUMIFS(RR_Score_Composito,RR_ID_Rischio,$A{r},RR_Ciclo,{l}$4)))')
            ws[f"{l}{r}"].number_format = "0.00"
    fine = 4 + MAX_RISCHI
    ws.conditional_formatting.add(f"C5:J{fine}", FormulaRule(formula=["ISNA(C5)"], font=FONT_NA))
    ws.column_dimensions["A"].width = 10
    ws.column_dimensions["B"].width = 48
    for j in range(8):
        ws.column_dimensions[get_column_letter(3 + j)].width = 10
    graf = LineChart()
    graf.title = "Score composito per rischio (scala fissa 0-5)"
    graf.add_data(Reference(ws, min_col=2, max_col=10, min_row=5, max_row=fine), from_rows=True, titles_from_data=True)
    graf.set_categories(Reference(ws, min_col=3, max_col=10, min_row=4, max_row=4))
    asse_fisso(graf, 0, 5)
    stile_grafico(graf)
    graf.height, graf.width = 13, 22
    ws.add_chart(graf, f"A{fine + 3}")


# ---------------------------------------------------------------- Delta
def foglio_delta(wb):
    """Variazione sul ciclo precedente: grafico ordinato, motivi a fianco, dettaglio per dimensione sotto."""
    ws = wb["Delta"]
    titolo(ws, "Delta: che cosa e' cambiato dal ciclo precedente", 17)
    B = 30                                                 # blocco nascosto (AD..)
    fine = 4 + MAX_RISCHI
    # Valori confrontati (D-50, D-58): quattro dimensioni e lo score. Indici per nome, non a mano.
    campi = ["RR_Impatto", "RR_Probabilita", "RR_Prossimita", "RR_Velocity", "RR_Score_Composito"]
    Lb = lambda j: get_column_letter(B + j)
    SC, CH, PO, ET, SU, GIU, ZE = 5, 6, 7, 8, 9, 10, 11          # colonne del blocco: Δ Score, chiave, posizione, serie
    for j, t in enumerate(["ID", "Δ Imp", "Δ Prob", "Δ Pross", "Δ Vel", "Δ Score", "Chiave", "Pos.",
                           "Etichetta", "In aumento", "In diminuzione", "Invariato"]):
        ws.cell(row=4, column=B + j, value=t)
    for i in range(MAX_RISCHI):
        r, k = 5 + i, i + 1
        a = f"${Lb(0)}{r}"
        ws[f"{Lb(0)}{r}"] = f"=INDEX(posID,{k})&\"\""
        for j, campo in enumerate(campi, start=1):
            # Valore presente in entrambi i cicli ("<>": una Velocity non valutata e' vuota, non zero): altrimenti #N/D.
            presenti = (f'COUNTIFS(RR_ID_Rischio,{a},RR_Ciclo,cicloCorrente,{campo},"<>")'
                        f'*COUNTIFS(RR_ID_Rischio,{a},RR_Ciclo,cicloPrecedente,{campo},"<>")')
            ws[f"{Lb(j)}{r}"] = (f'=IF({a}="",NA(),IF({presenti}=0,NA(),'
                                 f'SUMIFS({campo},RR_ID_Rischio,{a},RR_Ciclo,cicloCorrente)-SUMIFS({campo},RR_ID_Rischio,{a},RR_Ciclo,cicloPrecedente)))')
        ws[f"{Lb(CH)}{r}"] = f'=IF({a}="","",IF(ISNUMBER({Lb(SC)}{r}),{Lb(SC)}{r},-9)-{k}/100000)'
        ws[f"{Lb(PO)}{r}"] = f'=IFERROR(MATCH(_xlfn.AGGREGATE(14,6,${Lb(CH)}$5:${Lb(CH)}${fine},{k}),${Lb(CH)}$5:${Lb(CH)}${fine},0),"")'
    # Righe ordinate (dal maggiore aumento): serie del grafico, una per verso.
    for i in range(MAX_RISCHI):
        r = 5 + i
        p = f"${Lb(PO)}{r}"
        d = f"INDEX(${Lb(SC)}$5:${Lb(SC)}${fine},{p})"
        ws[f"{Lb(ET)}{r}"] = f'=IF({p}="","",INDEX(posID,{p})&"  "&LEFT(INDEX(posNome,{p}),30))'
        ws[f"{Lb(SU)}{r}"] = f'=IF({p}="",NA(),IF(ISNUMBER({d}),IF({d}>0,{d},0),NA()))'
        ws[f"{Lb(GIU)}{r}"] = f'=IF({p}="",NA(),IF(ISNUMBER({d}),IF({d}<0,{d},0),NA()))'
        ws[f"{Lb(ZE)}{r}"] = f'=IF({p}="",NA(),IF(ISNUMBER({d}),IF({d}=0,0,NA()),NA()))'
        for j in (SU, GIU, ZE):
            ws[f"{Lb(j)}{r}"].number_format = "+0.00;-0.00;;"     # lo zero non ha etichetta nel grafico
    for j in range(ZE + 1):
        ws.column_dimensions[Lb(j)].hidden = True
    n = f"MAX(1,COUNT(Delta!${Lb(SC)}$5:${Lb(SC)}${fine}))"      # in un nome definito, sempre con il foglio
    for nome, j in (("deltaEtichette", ET), ("deltaSu", SU), ("deltaGiu", GIU), ("deltaZero", ZE)):
        nome_definito(wb, nome, f"OFFSET(Delta!${Lb(j)}$5,0,0,{n},1)")
    ws["AT2"] = (f'=COUNTIF(${Lb(SC)}$5:${Lb(SC)}${fine},">0")&" in aumento, "&COUNTIF(${Lb(SC)}$5:${Lb(SC)}${fine},"<0")'
                 f'&" in diminuzione, "&COUNTIF(${Lb(SC)}$5:${Lb(SC)}${fine},0)&" invariati"')
    ws.column_dimensions["AT"].hidden = True

    ch = BarChart()
    ch.type = "bar"
    ch.grouping = "clustered"
    ch.overlap = 100
    ch.gapWidth = 50
    ch.visible_cells_only = False
    for j, (nome, testo, colore) in zip((SU, GIU, ZE), [("deltaSu", "In aumento", ROSSO), ("deltaGiu", "In diminuzione", BLU_DIM),
                                                       ("deltaZero", "Invariato", GRIGIO_URG)]):
        ch.add_data(Reference(ws, min_col=B + j, min_row=5, max_row=fine), titles_from_data=False)
        s = ch.series[-1]
        _serie_dinamica(s, nome, "deltaEtichette", testo)
        s.graphicalProperties.solidFill = colore
        s.graphicalProperties.line.noFill = True
        s.invertIfNegative = False        # altrimenti Excel disegna bianca la barra negativa
        if j != ZE:
            etichette_valore(s, colore)
    ch.title = titolo_da_cella(ws, "$AT$2")
    ch.x_axis.scaling.orientation = "maxMin"
    ch.x_axis.tickLblPos = "low"
    # ±1,5: quando la Velocity entra o esce (D-50) i pesi si ridistribuiscono e il Δ puo' superare un punto.
    ch.y_axis.scaling.min, ch.y_axis.scaling.max, ch.y_axis.majorUnit = -1.5, 1.5, 0.5
    ch.y_axis.numFmt = "+0.00;-0.00;0"
    ch.varyColors = False
    stile_grafico(ch)
    ch.height, ch.width = 11.5, 14.5
    ws.add_chart(ch, "A4")

    # A fianco: il motivo della variazione o della non variazione, nello stesso ordine delle barre.
    sezione(ws, 4, 11, 17, "Perche' varia (o no), nello stesso ordine")
    for j, t in [(11, "Rischio"), (12, "Δ"), (13, "Motivo, con l'evidenza")]:
        c = ws.cell(row=5, column=j, value=t)
        c.font = Font(size=9, bold=True, color="FFFFFF")
    for x in range(11, 18):
        ws.cell(row=5, column=x).fill = fill(BLU_MEDIO)
    ws.merge_cells("M5:Q5")
    for i in range(MAX_RISCHI):
        r = 6 + i
        rs = 5 + i
        p = f"${Lb(PO)}${rs}"
        ident = f"INDEX(posID,{p})"
        chiave = f'cicloCorrente&"|"&{ident}'
        var = f"INDEX(RR_Variazioni,MATCH({chiave},RR_Chiave,0))"
        esito = f"INDEX(RR_Esito,MATCH({chiave},RR_Chiave,0))"
        ws.merge_cells(start_row=r, start_column=13, end_row=r, end_column=17)
        ws[f"K{r}"] = f'=IF({p}="","",{ident})'
        ws[f"L{r}"] = f'=IF({p}="","",IFERROR(INDEX(${Lb(SC)}$5:${Lb(SC)}${fine},{p}),"nuovo"))'
        ws[f"L{r}"].number_format = "+0.00;-0.00;0.00"
        ws[f"M{r}"] = (f'=IF({p}="","",IFERROR(IF({esito}="Nuovo","Rischio nuovo nel ciclo.",'
                       f'{json_leggibile(var, COPPIE_VARIAZIONI, "Invariato: nessuna evidenza nuova dopo il ciclo precedente; restano valide le sue fonti.")}),"Non valutato nel ciclo."))')
        for x in range(11, 18):
            ws.cell(row=r, column=x).alignment = Alignment(wrap_text=True, vertical="top")
        ws[f"K{r}"].font = Font(size=8.5, bold=True, color=BLU_NOTTE)
        ws[f"L{r}"].font = Font(size=9, bold=True)
        ws[f"M{r}"].font = Font(size=8)
        # Lo script adatta le altezze (prepara_report); nel template le righe senza esempio nascono basse,
        # altrimenti con MAX_RISCHI righe la prima pagina non contiene piu' grafico e motivi.
        ws.row_dimensions[r].height = 30 if i < len(ANAGRAFICA) else 3
    colora_delta(ws, f"L6:L{5 + MAX_RISCHI}", "L6")
    ws.conditional_formatting.add(f"K6:Q{5 + MAX_RISCHI}", FormulaRule(formula=['$K6<>""'], border=BORDO_SOTTILE))
    nome_definito(wb, "deltaMotivi", f"Delta!$K$6:$Q${5 + MAX_RISCHI}")
    ws.column_dimensions["J"].width = 2
    for l, w in (("K", 8), ("L", 7), ("M", 14), ("N", 14), ("O", 14), ("P", 14), ("Q", 14)):
        ws.column_dimensions[l].width = w

    # Sotto: scala e dettaglio per dimensione (stesso ordine).
    r0 = 7 + MAX_RISCHI
    ws.merge_cells(start_row=r0, start_column=1, end_row=r0, end_column=17)
    # La nota legge i pesi da Parametri (D-50): nessun peso scritto nel testo.
    quattro = "(pesoImpatto+pesoProbabilita+pesoProssimita+pesoVelocity)"
    tre = "(pesoImpatto+pesoProbabilita+pesoProssimita)"
    quota = lambda nome, somma: f'FIXED({nome}/{somma},2)'
    c = ws.cell(row=r0, column=1, value=(
        '="Come si legge la scala: il Δ e\' la variazione dello score composito sul ciclo precedente. Ogni dimensione '
        'cambia al massimo di un punto fra due cicli; "&"un punto vale il suo peso diviso per la somma dei pesi delle '   # Excel: letterali <= 255 caratteri
        'dimensioni valutate (Parametri). Con la Velocity valutata: Impatto ±"&' + quota("pesoImpatto", quattro) +
        '&", Probabilita ±"&' + quota("pesoProbabilita", quattro) + '&", Prossimita ±"&' + quota("pesoProssimita", quattro) +
        '&", Velocity ±"&' + quota("pesoVelocity", quattro) + '&". Senza Velocity: Impatto ±"&' + quota("pesoImpatto", tre) +
        '&", Probabilita ±"&' + quota("pesoProbabilita", tre) + '&", Prossimita ±"&' + quota("pesoProssimita", tre) +
        '&". Quando la Velocity entra o esce i pesi si ridistribuiscono: lo score puo\' muoversi anche se nessun altro '
        'valore cambia. Un Δ oltre la soglia di Parametri ("&FIXED(sogliaDelta,2)&") '
        'va guardato."'))
    c.font = Font(size=9)
    c.fill = fill(FONDO_TENUE)
    c.alignment = Alignment(wrap_text=True, vertical="top")
    ws.row_dimensions[r0].height = 56
    sezione(ws, r0 + 2, 1, 10, "Dettaglio per dimensione")
    intest = ["ID", "Nome", "Δ Impatto", "Δ Probabilita", "Δ Prossimita'", "Δ Velocity", "Δ Score"]
    for j, t in enumerate(intest + [None, None, "Nota"], start=1):      # la Nota sta in K, come nella tabella sopra
        c = ws.cell(row=r0 + 3, column=j, value=t)
        c.font = Font(size=9, bold=True)
        c.alignment = Alignment(wrap_text=True, vertical="bottom")
        c.border = Border(bottom=Side(style="medium", color=BLU_NOTTE))
    ws.row_dimensions[r0 + 3].height = 28
    for i in range(MAX_RISCHI):
        r = r0 + 4 + i
        p = f"${Lb(PO)}${5 + i}"
        ws[f"A{r}"] = f'=IF({p}="","",INDEX(posID,{p}))'
        ws[f"B{r}"] = f'=IF({p}="","",INDEX(posNome,{p}))'
        for j in range(1, SC + 1):
            l = get_column_letter(2 + j)
            ws[f"{l}{r}"] = f'=IF({p}="",NA(),INDEX(${Lb(j)}$5:${Lb(j)}${fine},{p}))'
            ws[f"{l}{r}"].number_format = "+0.00;-0.00;0.00"
        ws.merge_cells(start_row=r, start_column=11, end_row=r, end_column=17)
        # AGGREGATE ignora i #N/D: una Velocity non valutata non nasconde un salto delle altre dimensioni.
        dim = f"C{r}:F{r}"
        ws[f"K{r}"] = (f'=IF($A{r}="","",IF(NOT(ISNUMBER(G{r})),"Nuovo o non valutato in uno dei due cicli",'
                       f'IF(_xlfn.AGGREGATE(4,6,{dim})>1,"Aumento > 1 punto: viola la rubrica",'
                       f'IF(_xlfn.AGGREGATE(5,6,{dim})<-1,"Riduzione > 1 punto: viola la rubrica",'
                       f'IF(ISNA(F{r}),"Velocity non valutata in uno dei due cicli: lo score ridistribuisce i pesi","")))))')
    ultima = r0 + 3 + MAX_RISCHI
    ws.conditional_formatting.add(f"C{r0 + 4}:G{ultima}", FormulaRule(formula=[f"ISNA(C{r0 + 4})"], font=FONT_NA))
    ws.conditional_formatting.add(f"G{r0 + 4}:G{ultima}", FormulaRule(formula=[f"AND(ISNUMBER(G{r0 + 4}),G{r0 + 4}>=sogliaDelta)"], fill=ROSSO_CF))
    ws.conditional_formatting.add(f"G{r0 + 4}:G{ultima}", FormulaRule(formula=[f"AND(ISNUMBER(G{r0 + 4}),G{r0 + 4}<=-sogliaDelta)"], fill=AZZURRO_CF))
    ws.column_dimensions["A"].width = 9
    ws.column_dimensions["B"].width = 30
    for l in "CDEFG":
        ws.column_dimensions[l].width = 10
    legenda(ws, ultima + 2, 17, f"Δ = variazione sul ciclo precedente; #N/D = valore assente in uno dei due cicli (nuovo o Velocity n.v.); rosso = in aumento, blu = in diminuzione. {LEG_RISCHIO}.")
    imposta_stampa(ws, f"A1:Q{ultima + 2}")
    ws.row_breaks.append(Break(id=r0 - 1))


# ---------------------------------------------------------------- Radar di Mosca
ANELLI = [(0, "Mosca", "C00000", 28575, None), (1, "1 anno", "8C8C8C", 12700, "dash"),
          (2, "2 anni", "BFBFBF", 9525, None), (3, "3 anni", "BFBFBF", 9525, None)]
PUNTI_ANELLO = 72          # punti per cerchio: con linee smussate il cerchio e' continuo
SCOSTAMENTO_RAGGIO, RAGGIO_MIN, RAGGIO_MAX = 2, 0.6, 6
LIMITE_ASSI = 7.6
SOTTO_RADAR = {False: 2.8, True: 0}     # fascia sotto il radar per le legende (D-74), in unita' degli assi
VALORI_PXI = sorted({p * s for p in range(1, 6) for s in range(1, 6)})
LATO_PER_RADICE = 10       # punti di marcatore per unita' di radice: 25 -> 50 pt, 1 -> 10 pt
NOMI_SETTORI = dict(TASSONOMIA)          # D-74: un settore per categoria (nove), con il nome


def _punti(foglio, righe, col_x, col_y, titolo_cella=None, titolo_testo=None):
    """Serie di un grafico a dispersione su un intervallo di righe."""
    s = Series(Reference(foglio, min_col=col_y, min_row=righe[0], max_row=righe[1]),
               xvalues=Reference(foglio, min_col=col_x, min_row=righe[0], max_row=righe[1]))
    if titolo_cella:
        s.tx = SeriesLabel(strRef=StrRef(f"'{foglio.title}'!{titolo_cella}"))
    elif titolo_testo is not None:
        s.tx = SeriesLabel(v=titolo_testo)
    return s


def _etichetta_serie(serie, solo_primo=False, posizione="r", indice=0, sz=800, b=True, colore="262626"):
    base = dict(showSerName=True, showVal=False, showCatName=False, showLegendKey=False,
                showPercent=False, showBubbleSize=False, dLblPos=posizione)
    if solo_primo:
        serie.dLbls = DataLabelList(dLbl=[DataLabel(idx=indice, txPr=rich(sz, b, colore), **base)], showVal=False,
                                    showSerName=False, showCatName=False, showLegendKey=False, showPercent=False,
                                    showBubbleSize=False)
    else:
        serie.dLbls = DataLabelList(**base)
    serie.dLbls.txPr = rich(sz, b, colore)


def grafico_radar(ws, base, piccolo=False):
    """Scrive in ws, da colonna 'base' (nascoste), l'appoggio del radar di Mosca e restituisce il grafico.
    I valori per rischio vengono dal foglio Radar_Mosca (righe 5..): cosi' il radar del Quadro d'insieme e
    quello del Radar_Mosca sono lo stesso grafico, e ciascuno legge celle del proprio foglio.
    Colonne (da base): 0 angolo; 1-8 anelli (x, y); 10-11 raggi dei settori; 13-15 etichette dei settori;
    17.. classi di P x I per livello di allerta (riga 3 = livello, D-63); poi x e ID di ogni rischio (con ◆ se
    il tema e' all'attenzione del supervisore), e i campioni della legenda."""
    C = lambda n: base + n
    Lx = lambda n: get_column_letter(base + n)
    rm = "" if ws.title == "Radar_Mosca" else "Radar_Mosca!"
    ultima = 4 + MAX_RISCHI
    ws.cell(row=3, column=base, value="Appoggio del grafico: non modificare")
    for k in range(PUNTI_ANELLO + 1):
        r = 5 + k
        ws.cell(row=r, column=C(0), value=f"=2*PI()*{k}/{PUNTI_ANELLO}")
        for a, (margine, *_resto) in enumerate(ANELLI):
            ws.cell(row=r, column=C(1 + 2 * a), value=f"={margine + SCOSTAMENTO_RAGGIO}*SIN(${Lx(0)}{r})")
            ws.cell(row=r, column=C(2 + 2 * a), value=f"={margine + SCOSTAMENTO_RAGGIO}*COS(${Lx(0)}{r})")
    fine_anelli = 5 + PUNTI_ANELLO
    for s in range(len(TASSONOMIA)):
        ws.cell(row=5 + 2 * s, column=C(10), value=0)
        ws.cell(row=5 + 2 * s, column=C(11), value=0)
        ws.cell(row=6 + 2 * s, column=C(10), value=f"={RAGGIO_MAX + 0.3}*SIN(2*PI()*{s}/ROWS(codiciL1))")
        ws.cell(row=6 + 2 * s, column=C(11), value=f"={RAGGIO_MAX + 0.3}*COS(2*PI()*{s}/ROWS(codiciL1))")
    for s, (cod, _) in enumerate(TASSONOMIA):
        r = 5 + s
        ws.cell(row=r, column=C(13), value=f"{cod}\n{NOMI_SETTORI[cod]}")
        ws.cell(row=r, column=C(14), value=f"={RAGGIO_MAX + 0.95}*SIN(2*PI()*({s}+0.5)/ROWS(codiciL1))")
        ws.cell(row=r, column=C(15), value=f"={RAGGIO_MAX + 0.95}*COS(2*PI()*({s}+0.5)/ROWS(codiciL1))")
    classi = [(v, livello) for livello, _, _ in LIVELLI for v in VALORI_PXI]
    cx, cid = C(17 + len(classi)), C(18 + len(classi))           # x, ID e y del rischio, copiati da Radar_Mosca
    cy = C(19 + len(classi))
    for i in range(MAX_RISCHI):
        r = 5 + i
        ws.cell(row=r, column=cx, value=f"=IF(ISNUMBER({rm}$R{r}),{rm}$R{r},NA())")
        ws.cell(row=r, column=cy, value=f"=IF(ISNUMBER({rm}$S{r}),{rm}$S{r},NA())")
        sup = f'IF({rm}$T{r}="Sì"," ◆","")'
        ws.cell(row=r, column=cid, value=f'=IF({rm}$A{r}="","",{rm}$A{r}&{sup})' if not piccolo else
                f'=IF({rm}$A{r}="","",MID({rm}$A{r},5,3)&{sup})')
    for n, (v, livello) in enumerate(classi):
        col = get_column_letter(C(17 + n))
        ws[f"{col}4"] = v
        ws[f"{col}3"] = livello
        for i in range(MAX_RISCHI):
            r = 5 + i
            ws[f"{col}{r}"] = (f"=IF(AND(ISNUMBER({rm}$F{r}),ISNUMBER({rm}$S{r})),IF(AND({rm}$F{r}={col}$4,"
                               f"{rm}${COL_LIVELLO}{r}={col}$3),{rm}$S{r},NA()),NA())")
    # Campioni della legenda: i tre livelli di allerta, linea rossa (AGIRE ORA), aree 4, 12, 25.
    cl = C(20 + len(classi))
    # D-74: con nove settori un'etichetta cade sempre vicino a un angolo del grafico: le legende stanno sotto il
    # radar, in una fascia aggiunta (SOTTO_RADAR), non negli angoli.
    sotto = SOTTO_RADAR[piccolo]
    y0 = -LIMITE_ASSI - 0.45
    if piccolo:                                           # due colonne: nel grafico piccolo il testo pesa di piu'
        (l1, _, _), (l2, _, _), (l3, _, _) = LIVELLI
        campioni = [(l1, -7.0, y0), (l2, 0.3, y0), (l3, -7.0, y0 - 1.35)]
        campioni += [("AGIRE ORA (X+Y>Z)", -0.15, y0 - 1.35), ("", 0.75, y0 - 1.35)]
    else:
        campioni = [(f"{livello}", -6.9, y0 - k * 0.6) for k, (livello, _, _) in enumerate(LIVELLI)]
        campioni += [("dentro il cerchio rosso: AGIRE ORA (X + Y > Z)", -7.35, y0 - 1.8), ("", -6.45, y0 - 1.8)]
    campioni += [("Area del cerchio = P x I", 4.4, y0), ("4", 3.5, y0 - 1.05), ("12", 4.8, y0 - 1.05),
                 ("25", 6.5, y0 - 1.05)]
    for k, (testo, x, y) in enumerate(campioni):
        ws.cell(row=5 + k, column=cl, value=testo)
        ws.cell(row=5 + k, column=cl + 1, value=x)
        ws.cell(row=5 + k, column=cl + 2, value=y)
    for l in range(base, cl + 3):
        ws.column_dimensions[get_column_letter(l)].hidden = True

    scala = 0.62 if piccolo else 1
    sz = (650, 700) if piccolo else (800, 850)
    ch = ScatterChart()
    ch.scatterStyle = "lineMarker"
    ch.visible_cells_only = False     # i dati di appoggio stanno in colonne nascoste: disegnarli comunque
    ch.varyColors = False
    for a, (_, testo, colore, spessore, tratto) in enumerate(ANELLI):
        s = _punti(ws, (5, fine_anelli), C(1 + 2 * a), C(2 + 2 * a), titolo_testo=testo)
        s.smooth = True
        s.marker.symbol = "none"
        s.graphicalProperties.line.solidFill = colore
        s.graphicalProperties.line.width = spessore
        if tratto:
            s.graphicalProperties.line.prstDash = tratto
        if not piccolo or a == 0:
            # Etichetta sul raggio fra il 2o e il 3o settore: nessun rischio vi cade mai.
            _etichetta_serie(s, solo_primo=True, indice=round(PUNTI_ANELLO * 2 / len(TASSONOMIA)), sz=sz[0],
                             b=a == 0, colore=colore if a == 0 else TESTO_TENUE)
        ch.series.append(s)
    for k in range(len(TASSONOMIA)):
        s = _punti(ws, (5 + 2 * k, 6 + 2 * k), C(10), C(11), titolo_testo=f"Settore {k + 1}")
        s.marker.symbol = "none"
        s.graphicalProperties.line.solidFill = "E7E6E6"
        s.graphicalProperties.line.width = 9525
        ch.series.append(s)
    for k in range(len(TASSONOMIA)):
        s = _punti(ws, (5 + k, 5 + k), C(14), C(15), titolo_cella=f"${Lx(13)}${5 + k}")
        s.marker.symbol = "none"
        s.graphicalProperties.line.noFill = True
        _etichetta_serie(s, posizione="ctr", sz=sz[1], colore=BLU_NOTTE)
        ch.series.append(s)
    lato = lambda v: max(2, round(LATO_PER_RADICE * scala * v ** 0.5))
    colore_livello = {livello: colore for livello, colore, _ in LIVELLI}
    for n, (v, livello) in enumerate(classi):
        s = _punti(ws, (5, ultima), cx, C(17 + n), titolo_testo=f"P x I = {v} ({livello})")
        s.marker.symbol = "circle"
        s.marker.size = lato(v)
        # Riempimento semitrasparente del colore del livello di allerta (D-63).
        s.marker.graphicalProperties = GraphicalProperties(solidFill=colore_livello[livello])
        s.marker.graphicalProperties.line.solidFill = "595959"
        s.marker.graphicalProperties.line.width = 9525
        s.graphicalProperties.line.noFill = True
        ch.series.append(s)
    for i in range(MAX_RISCHI):                        # etichette con l'ID, al centro dei cerchi
        r = 5 + i
        s = _punti(ws, (r, r), cx, cy, titolo_cella=f"${get_column_letter(cid)}${r}")
        s.marker.symbol = "none"
        s.graphicalProperties.line.noFill = True
        _etichetta_serie(s, posizione="ctr", sz=sz[0], colore=BLU_NOTTE)
        ch.series.append(s)
    # Legenda nel grafico (in basso a sinistra i tre livelli e, sotto, la linea rossa; a destra le aree). Nel radar
    # piccolo del Quadro non c'e' (D-74: con nove settori non ci sta): i colori li spiega la legenda del Quadro.
    for k, (livello, colore, _) in enumerate(LIVELLI if not piccolo else []):
        s = _punti(ws, (5 + k, 5 + k), cl + 1, cl + 2, titolo_cella=f"${get_column_letter(cl)}${5 + k}")
        s.marker.symbol = "circle"
        s.marker.size = lato(2)
        s.marker.graphicalProperties = GraphicalProperties(solidFill=colore)
        s.marker.graphicalProperties.line.solidFill = "595959"
        s.marker.graphicalProperties.line.width = 9525
        s.graphicalProperties.line.noFill = True
        _etichetta_serie(s, posizione="r", sz=sz[0], colore=TESTO_TENUE)
        ch.series.append(s)
    if not piccolo:
        s = _punti(ws, (8, 9), cl + 1, cl + 2, titolo_cella=f"${get_column_letter(cl)}$8")
        s.marker.symbol = "none"
        s.graphicalProperties.line.solidFill = ROSSO
        s.graphicalProperties.line.width = 28575
        _etichetta_serie(s, solo_primo=True, indice=1, posizione="r", sz=sz[0], colore=ROSSO)
        ch.series.append(s)
        s = _punti(ws, (10, 10), cl + 1, cl + 2, titolo_cella=f"${get_column_letter(cl)}$10")
        s.marker.symbol = "none"
        s.graphicalProperties.line.noFill = True
        _etichetta_serie(s, posizione="ctr", sz=800, colore=TESTO_TENUE)
        ch.series.append(s)
        for k, v in enumerate((4, 12, 25)):
            s = _punti(ws, (11 + k, 11 + k), cl + 1, cl + 2, titolo_cella=f"${get_column_letter(cl)}${11 + k}")
            s.marker.symbol = "circle"
            s.marker.size = lato(v)
            s.marker.graphicalProperties = GraphicalProperties(solidFill=RIEMPIMENTO_CERCHIO)
            s.marker.graphicalProperties.line.solidFill = "1F4E79"
            s.marker.graphicalProperties.line.width = 9525
            s.graphicalProperties.line.noFill = True
            _etichetta_serie(s, posizione="b", sz=800, b=False, colore=TESTO_TENUE)
            ch.series.append(s)
    for asse in (ch.x_axis, ch.y_axis):
        asse.scaling.min, asse.scaling.max = -LIMITE_ASSI, LIMITE_ASSI
        asse.delete = True
        asse.majorGridlines = None
    ch.y_axis.scaling.min = -LIMITE_ASSI - sotto            # fascia delle legende sotto il radar
    ch.legend = None
    ch.graphical_properties = GraphicalProperties(ln=LineProperties(noFill=True))
    ch.plot_area.layout = Layout(manualLayout=ManualLayout(layoutTarget="inner", xMode="edge", yMode="edge",
                                                           x=0.01, y=0.01, w=0.98, h=0.98))
    ch.width = 8.5 if piccolo else 17
    ch.height = ch.width * (2 * LIMITE_ASSI + sotto) / (2 * LIMITE_ASSI)    # stessa scala sui due assi: cerchi rotondi
    return ch


def foglio_radar_mosca(wb):
    """Urgenza e magnitudo di ogni rischio: rubrica, sezione 8.
    Distanza dal centro = margine di Mosca Z - (X + Y) + SCOSTAMENTO_RAGGIO, fra RAGGIO_MIN e RAGGIO_MAX
    (piu' vicino = agire prima); area del cerchio = Probabilita x Impatto; settore = categoria di rischio."""
    ws = wb["Radar_Mosca"]
    titolo(ws, "Radar di Mosca: quanto presto agire, e quanto e' grande ogni rischio", 12)
    intest = ["ID", "Nome", "Categoria", "Impatto", "Probabilita", "P x I", "Prossimita",
              "Z anni alla manifestazione", "X anni per decidere", "Y anni per mitigare (azioni o adeguamento)", "Margine Z-(X+Y)", "Urgenza",
              "Settore", "Posizione nel settore", "Rischi nel settore", "Angolo", "Raggio", "x", "y",
              "Attenzione del supervisore",
              # D-63: livello di allerta (rubrica, sezione 8). 1 = vero, 0 = falso.
              "F1 AGIRE ORA", "F2 KRI in rosso", "F3 notizie ▲", "A1 P x I alta", "A2 presidio assente",
              "A3 KRI in ambra o rosso", "Livello di allerta", "Motivo del livello"]
    for j, testo in enumerate(intest, start=1):
        c = ws.cell(row=4, column=j, value=testo); c.font = Font(size=9, bold=True); c.alignment = A_CAPO
    ultima = 4 + MAX_RISCHI
    cc = "cicloCorrente"
    for i in range(MAX_RISCHI):
        r = 5 + i
        ws[f"A{r}"] = f'=IF(Parametri!$H{4 + i}="","",Parametri!$H{4 + i})'
        ws[f"B{r}"] = f'=IF($A{r}="","",Parametri!$I{4 + i})'
        ws[f"C{r}"] = f'=IF($A{r}="","",Parametri!$J{4 + i})'
        for col, campo in (("D", "RR_Impatto"), ("E", "RR_Probabilita"), ("G", "RR_Prossimita")):
            ws[f"{col}{r}"] = (f'=IF($A{r}="",NA(),IF(COUNTIFS(RR_ID_Rischio,$A{r},RR_Ciclo,{cc})=0,NA(),'
                               f'SUMIFS({campo},RR_ID_Rischio,$A{r},RR_Ciclo,{cc})))')
        ws[f"F{r}"] = f"=IF(AND(ISNUMBER(D{r}),ISNUMBER(E{r})),D{r}*E{r},NA())"
        ws[f"H{r}"] = f"=IF(ISNUMBER(G{r}),INDEX(anniProssimita,G{r}),NA())"
        ws[f"I{r}"] = f'=IF($A{r}="",NA(),moscaX)'
        # Y = orizzonte piu' lungo delle azioni (o la riserva) e, se maggiore, gli anni di
        # adeguamento strutturale dell'anagrafica (Parametri, colonna M; N() = 0 se vuoto).
        # D-75: le azioni del periodo in cui il rischio e' stato valutato (colonna AC, nascosta): per un rischio non
        # rivalutato in un ciclo straordinario, quelle del ciclo da cui la riga e' riportata.
        pv = f"RR_Periodo_Valutazione,MATCH({cc}&\"|\"&$A{r},RR_Chiave,0)"
        ws[f"AC{r}"] = f'=IF($A{r}="","",IFERROR(IF(INDEX({pv})="",{cc},INDEX({pv})&""),{cc}))'
        ws[f"J{r}"] = (f'=IF($A{r}="",NA(),MAX(IF(COUNTIFS(AZ_ID_Rischio,$A{r},AZ_Ciclo,$AC{r},AZ_Stato,"<>Respinta",AZ_Mesi_Orizzonte,">0")=0,'
                       f'moscaYDefault,_xlfn.MAXIFS(AZ_Mesi_Orizzonte,AZ_ID_Rischio,$A{r},AZ_Ciclo,$AC{r},AZ_Stato,"<>Respinta")/12),'
                       f'N(Parametri!$M{4 + i})))')
        ws[f"K{r}"] = f"=IF(AND(ISNUMBER(H{r}),ISNUMBER(J{r})),H{r}-(I{r}+J{r}),NA())"
        ws[f"L{r}"] = (f'=IF(NOT(ISNUMBER(K{r})),"",IF(K{r}<0,"AGIRE ORA: X+Y > Z",'
                       f'IF(K{r}<1,"Agire entro l\'anno","Margine "&ROUND(K{r},1)&IF(ROUND(K{r},1)=1," anno"," anni"))))')
        ws[f"M{r}"] = f'=IF($A{r}="",NA(),MATCH(C{r},codiciL1,0)-1)'
        # Rischi dello stesso settore a distanze angolari uguali nel settore: due rischi con margine simile non si coprono.
        ws[f"N{r}"] = f'=IF($A{r}="",NA(),COUNTIF($C$4:C{r - 1},C{r}))'
        ws[f"O{r}"] = f'=IF($A{r}="",NA(),COUNTIF(ANA_Event_Type,C{r}))'
        ws[f"P{r}"] = f'=IF($A{r}="",NA(),2*PI()*(M{r}+(N{r}+0.5)/O{r})/ROWS(codiciL1))'
        ws[f"Q{r}"] = f"=IF(ISNUMBER(K{r}),MAX({RAGGIO_MIN},MIN({RAGGIO_MAX},K{r}+{SCOSTAMENTO_RAGGIO})),NA())"
        ws[f"R{r}"] = f"=IF(AND(ISNUMBER(Q{r}),ISNUMBER(P{r})),Q{r}*SIN(P{r}),NA())"
        ws[f"S{r}"] = f"=IF(AND(ISNUMBER(Q{r}),ISNUMBER(P{r})),Q{r}*COS(P{r}),NA())"
        for col in "HIJKPQRS":
            ws[f"{col}{r}"].number_format = "0.00"
        # T: tema all'attenzione del supervisore (anagrafica, colonna N, input del validatore): bordo giallo.
        ws[f"T{r}"] = f'=IF($A{r}="","",IF(Parametri!$N{4 + i}="Sì","Sì",""))'
        # Livello di allerta (D-63): segnali forti F1-F3, aggravanti A1-A3, livello e motivo. Solo dati gia' nel registro.
        kri = f'KRI_ID_Rischio,$A{r},KRI_Ciclo,{cc},KRI_In_Vigore,"Sì"'
        rossi, ambra, tutti = (f'COUNTIFS({kri},KRI_Stato,"Rosso")', f'COUNTIFS({kri},KRI_Stato,"Ambra")',
                               f'COUNTIFS({kri})')
        vuoto = f'OR($A{r}="",NOT(ISNUMBER(K{r})))'
        ws[f"U{r}"] = f'=IF({vuoto},"",IF(K{r}<0,1,0))'
        ws[f"V{r}"] = f'=IF({vuoto},"",IF({rossi}>0,1,0))'
        ws[f"W{r}"] = f'=IF({vuoto},"",IF(N(INDEX(posNetti,{i + 1}))>=sogliaDirezione,1,0))'
        ws[f"X{r}"] = f'=IF({vuoto},"",IF(AND(ISNUMBER(F{r}),F{r}>=livelloPxI),1,0))'
        ws[f"Y{r}"] = f'=IF({vuoto},"",IF(Parametri!$O{4 + i}="Assente",1,0))'
        ws[f"Z{r}"] = f'=IF({vuoto},"",IF(AND({tutti}>0,{rossi}+{ambra}>=livelloQuotaKRI*{tutti}),1,0))'
        forti, aggr = f"(U{r}+V{r}+W{r})", f"(X{r}+Y{r}+Z{r})"
        ws[f"{COL_LIVELLO}{r}"] = (f'=IF({vuoto},"",IF({forti}>=livelloForti,"Attivazione",IF(OR({forti}>=1,'
                                   f'AND(K{r}<livelloMargine,{aggr}>=1)),"Attenzione","Monitoraggio")))')
        l = f"{COL_LIVELLO}{r}"
        ws[f"AB{r}"] = (f'=IF({l}="","",IF({l}="Monitoraggio","nessun segnale forte",_xlfn.TEXTJOIN("; ",TRUE,'
                        f'IF(U{r}=1,"AGIRE ORA",""),IF(V{r}=1,"KRI in rosso",""),IF(W{r}=1,"notizie in peggioramento",""),'
                        f'IF({forti}=0,"margine sotto l\'anno con "&_xlfn.TEXTJOIN(", ",TRUE,IF(X{r}=1,"P x I alta",""),'
                        f'IF(Y{r}=1,"presidio dei controlli assente",""),IF(Z{r}=1,"KRI in ambra o rosso","")),""))))')
    chip_urgenza(ws, f"L5:L{ultima}", "L5")
    chip_livello(ws, f"{COL_LIVELLO}5:{COL_LIVELLO}{ultima}", f"{COL_LIVELLO}5")
    for l in ("U", "V", "W", "X", "Y", "Z", COL_LIVELLO, "AB"):
        ws.column_dimensions[l].width = 16 if l in (COL_LIVELLO, "AB") else 9
    ws.column_dimensions["AB"].width = 44
    ws.column_dimensions["AC"].hidden = True      # periodo di valutazione del rischio (D-75), per la Y
    ws.conditional_formatting.add(f"D5:S{ultima}", FormulaRule(formula=["ISNA(D5)"], font=FONT_NA))
    for l, w in zip("ABCDEFGHIJKL", [9, 40, 9, 10, 11, 7, 11, 13, 11, 11, 11, 20]):
        ws.column_dimensions[l].width = w
    ws.row_dimensions[4].height = 45
    for nome, col in (("rmID", "A"), ("rmZ", "H"), ("rmX", "I"), ("rmY", "J"), ("rmMargine", "K"), ("rmUrgenza", "L"),
                      ("rmPxI", "F"), ("rmLivello", COL_LIVELLO), ("rmMotivoLivello", "AB")):
        nome_definito(wb, nome, f"Radar_Mosca!${col}$5:${col}${ultima}")
    ch = grafico_radar(ws, 30)      # appoggio da AD (le colonne U-AB sono il livello di allerta)
    ws.add_chart(ch, f"A{ultima + 3}")
    legenda(ws, ultima + 2, 12, f"{LEG_PXI}. {LEG_MOSCA}. Cerchi grigi = 1 anno (tratteggiato), 2 e 3 anni di margine. "
                                f"Colore = livello di allerta: rosso Attivazione (almeno due fra AGIRE ORA, KRI in rosso, "
                                f"notizie in peggioramento), giallo Attenzione (uno di questi, o margine sotto l'anno con P x I "
                                f"alta, presidio assente o KRI in ambra), verde Monitoraggio (colonne U-AB). "
                                f"Settori = categorie della tassonomia interna (9.1 ... 9.13; un rischio FP, fuori perimetro, non compare). {LEG_RISCHIO}.")


# ---------------------------------------------------------------- KRI: indicatori correnti e storia di uno
def _cella_tab(nome_tabella, foglio, colonna, riga_appoggio, testo):
    """Valore di una colonna di una tabella dati alla riga indicata dalla cella di appoggio.
    Il testo si forza con &"" (un vuoto non diventa 0); un numero o una data vuoti restano vuoti."""
    l = lettera(nome_tabella, colonna)
    if testo:
        return f'=IF({riga_appoggio}="","",INDEX({foglio}!${l}:${l},{riga_appoggio})&"")'
    return (f'=IF({riga_appoggio}="","",IF(INDEX({foglio}!${l}:${l},{riga_appoggio})="","",'
            f'INDEX({foglio}!${l}:${l},{riga_appoggio})))')


def _cella_kri(colonna, riga_appoggio, testo):
    return _cella_tab("tblKRI", "KRI", colonna, riga_appoggio, testo)


def colora_stato_kri(ws, intervallo, prima_cella):
    for testo, colore in [("Rosso", ROSSO_CF), ("Ambra", AMBRA_CF), ("Verde", VERDE_CF), ("SOGLIE INVERTITE — correggere", ROSSO_CF),
                          ("Soglie da definire", GIALLO_CF)]:
        ws.conditional_formatting.add(intervallo, FormulaRule(formula=[f'{prima_cella}="{testo}"'], fill=colore))


def foglio_indicatori(wb):
    """A sinistra i KRI in vigore nel ciclo corrente; a destra la storia di un KRI scelto."""
    ws = wb["Indicatori"]
    nome_definito(wb, "capienzaKRICorrenti", str(MAX_KRI_CORRENTI))   # letti dallo scrittore
    nome_definito(wb, "capienzaElencoKRI", str(MAX_ELENCO_KRI))
    titolo(ws, "Indicatori: KRI del ciclo e storia di un KRI", 21)
    for j, stato in enumerate(["Verde", "Ambra", "Rosso", "Non rilevato", "Soglie da definire"]):     # D-53
        ws.cell(row=4, column=1 + 2 * j, value=stato).font = GRASSETTO
        ws.cell(row=4, column=2 + 2 * j, value=f'=COUNTIFS(KRI_Ciclo,cicloCorrente,KRI_In_Vigore,"Sì",KRI_Stato,"{stato}")')
    intest = ["KRI_ID", "Rischio", "Nome", "Unita'", "Soglia attenzione", "Soglia allerta", "Valore",
              "Data rilevazione", "Stato", "Valore ciclo precedente", "Tendenza"]
    for j, t in enumerate(intest, start=1):
        c = ws.cell(row=6, column=j, value=t); c.font = Font(size=9, bold=True, color="FFFFFF"); c.fill = fill(BLU_NOTTE)
        c.alignment = A_CAPO
    campi = [("KRI_ID", True), ("ID_Rischio", True), ("Nome", True), ("Unita", True), ("Soglia_Attenzione", False),
             ("Soglia_Allerta", False), ("Valore_Corrente", False), ("Data_Rilevazione", False), ("Stato", True)]
    # Colonna Z nascosta: riga del foglio KRI del k-esimo KRI corrente (AGGREGATE 15 = SMALL che ignora gli errori).
    for k in range(MAX_KRI_CORRENTI):
        r = 7 + k
        ws[f"Z{r}"] = f'=IFERROR(_xlfn.AGGREGATE(15,6,ROW(KRI_Ciclo)/((KRI_Ciclo=cicloCorrente)*(KRI_In_Vigore="Sì")),{k + 1}),"")'
        for j, (col, testo) in enumerate(campi, start=1):
            ws.cell(row=r, column=j, value=_cella_kri(col, f"$Z{r}", testo))
        ws[f"H{r}"].number_format = "dd/mm/yyyy"
        ws[f"J{r}"] = (f'=IF($A{r}="","",IF(COUNTIFS(KRI_KRI_ID,$A{r},KRI_Ciclo,cicloPrecedente,KRI_Valore_Corrente,"<>")=0,"—",'
                       f'SUMIFS(KRI_Valore_Corrente,KRI_KRI_ID,$A{r},KRI_Ciclo,cicloPrecedente)))')
        ws[f"K{r}"] = f'=IF(OR(G{r}="",NOT(ISNUMBER(J{r}))),"",IF(G{r}>J{r},"▲ peggiora",IF(G{r}<J{r},"▼ migliora","● invariato")))'
    fine = 6 + MAX_KRI_CORRENTI
    colora_stato_kri(ws, f"I7:I{fine}", "I7")
    ws.conditional_formatting.add(f"K7:K{fine}", FormulaRule(formula=['LEFT(K7,1)="▲"'], font=Font(bold=True, color=ROSSO)))
    ws.conditional_formatting.add(f"K7:K{fine}", FormulaRule(formula=['LEFT(K7,1)="▼"'], font=Font(bold=True, color=BLU_DIM)))
    ws.column_dimensions["Z"].hidden = True
    for l, w in zip("ABCDEFGHIJK", [11, 9, 46, 8, 10, 10, 9, 11, 13, 11, 12]):
        ws.column_dimensions[l].width = w
    # Colonna L: tipo del KRI (D-64), accanto alla tabella.
    c = ws.cell(row=6, column=12, value="Tipo"); c.font = Font(size=9, bold=True, color="FFFFFF"); c.fill = fill(BLU_NOTTE)
    for k in range(MAX_KRI_CORRENTI):
        ws[f"L{7 + k}"] = _cella_kri("Tipo", f"$Z{7 + k}", True)
        ws[f"L{7 + k}"].font = Font(size=9)
    ws.column_dimensions["L"].width = 12

    # Storia di un KRI (colonne M..T): scelta in N4 (unica cella gialla), tabella e grafico.
    ws["M4"] = "KRI da guardare"; ws["M4"].font = GRASSETTO
    ws["N4"] = KRI_ESEMPIO[0][0]; ws["N4"].fill = INPUT
    for k in range(MAX_ELENCO_KRI):
        ws[f"AB{12 + k}"] = (f'=IFERROR(INDEX(KRI_KRI_ID,_xlfn.AGGREGATE(15,6,(ROW(KRI_KRI_ID)-{PRIMA_RIGA_DATI - 1})/'
                             f'((KRI_Ciclo_Definizione=KRI_Ciclo)*(KRI_KRI_ID<>"")),{k + 1})),"")')
    fine_elenco = 11 + MAX_ELENCO_KRI
    nome_definito(wb, "elencoKRI", f"OFFSET(Indicatori!$AB$12,0,0,MAX(1,COUNTIF(Indicatori!$AB$12:$AB${fine_elenco},\"?*\")),1)")
    convalida_lista(ws, "N4", "=elencoKRI")
    ws["AA4"] = '=IFERROR(_xlfn.AGGREGATE(14,6,ROW(KRI_KRI_ID)/(KRI_KRI_ID=$N$4),1),"")'
    info = [("Nome", "Nome"), ("Rischio", "ID_Rischio"), ("Unita'", "Unita"), ("Fonte dati", "Fonte_Dati"),
            ("Definito nel ciclo", "Ciclo_Definizione")]
    for i, (etichetta, col) in enumerate(info, start=5):
        ws[f"M{i}"] = etichetta
        ws[f"N{i}"] = _cella_kri(col, "$AA$4", True)
    lnome = lettera("tblKRI", "Nome")
    ltipo = lettera("tblKRI", "Tipo")
    ws["N5"] = (f'=IF($AA$4="","KRI non presente nello storico",INDEX(KRI!${lnome}:${lnome},$AA$4)&'
                f'IF(INDEX(KRI!${ltipo}:${ltipo},$AA$4)="",""," ("&INDEX(KRI!${ltipo}:${ltipo},$AA$4)&")"))')
    lc, lv = lettera("tblKRI", "Ciclo"), lettera("tblKRI", "In_Vigore")
    ws["M10"] = "Ultima fotografia"
    ws["N10"] = f'=IF($AA$4="","",INDEX(KRI!${lc}:${lc},$AA$4)&" — in vigore: "&INDEX(KRI!${lv}:${lv},$AA$4))'
    intest = ["Ciclo", "Valore", "Soglia attenzione", "Soglia allerta", "Stato", "Data rilevazione", "Fonte rilevazione", "Nota"]
    for j, t in enumerate(intest):
        c = ws.cell(row=11, column=13 + j, value=t); c.font = Font(size=9, bold=True, color="FFFFFF"); c.fill = fill(BLU_NOTTE)
        c.alignment = A_CAPO
    for i in range(8):
        r = 12 + i
        ch = f'$M{r}&"|"&$N$4'
        ws[f"M{r}"] = f"=Parametri!$B${20 + i}"
        ws[f"N{r}"] = (f'=IF($M{r}="",NA(),IF(COUNTIFS(KRI_KRI_ID,$N$4,KRI_Ciclo,$M{r},KRI_Valore_Corrente,"<>")=0,NA(),'
                       f'SUMIFS(KRI_Valore_Corrente,KRI_KRI_ID,$N$4,KRI_Ciclo,$M{r})))')
        for l, campo in (("O", "KRI_Soglia_Attenzione"), ("P", "KRI_Soglia_Allerta")):
            # Soglia vuota (la fissa la Banca, D-53) = #N/D: il grafico non disegna una soglia a zero.
            ws[f"{l}{r}"] = (f'=IF($M{r}="",NA(),IF(COUNTIFS(KRI_KRI_ID,$N$4,KRI_Ciclo,$M{r},{campo},"<>")=0,NA(),'
                             f'SUMIFS({campo},KRI_KRI_ID,$N$4,KRI_Ciclo,$M{r})))')
        ws[f"Q{r}"] = f'=IFERROR(INDEX(KRI_Stato,MATCH({ch},KRI_Chiave,0)),"—")'
        ws[f"R{r}"] = f'=IFERROR(IF(INDEX(KRI_Data_Rilevazione,MATCH({ch},KRI_Chiave,0))="","",INDEX(KRI_Data_Rilevazione,MATCH({ch},KRI_Chiave,0))),"")'
        ws[f"R{r}"].number_format = "dd/mm/yyyy"
        ws[f"S{r}"] = f'=IFERROR(INDEX(KRI_Fonte_Rilevazione,MATCH({ch},KRI_Chiave,0))&"","")'
        ws[f"T{r}"] = f'=IFERROR(INDEX(KRI_Nota_Rilevazione,MATCH({ch},KRI_Chiave,0))&"","")'
    ws.conditional_formatting.add("N12:P19", FormulaRule(formula=["ISNA(N12)"], font=FONT_NA))
    colora_stato_kri(ws, "Q12:Q19", "Q12")
    ws.column_dimensions["AA"].hidden = True
    ws.column_dimensions["AB"].hidden = True
    for l, w in zip("MNOPQRST", [16, 14, 11, 11, 12, 12, 24, 30]):
        ws.column_dimensions[l].width = w
    graf = LineChart()
    graf.title = "Valore rilevato e soglie, ultimi otto cicli"
    graf.add_data(Reference(ws, min_col=14, max_col=16, min_row=11, max_row=19), titles_from_data=True)
    graf.set_categories(Reference(ws, min_col=13, min_row=12, max_row=19))
    graf.y_axis.scaling.min = 0      # unita' diverse per KRI: minimo fisso a zero, massimo automatico
    graf.varyColors = False
    for serie, colore, tratto, marcatore in zip(graf.series, [BLU_NOTTE, "BF9000", ROSSO],
                                                [None, "dash", "dash"], ["circle", "none", "none"]):
        serie.smooth = False
        serie.marker.symbol = marcatore
        serie.graphicalProperties.line.solidFill = colore
        if tratto:
            serie.graphicalProperties.line.prstDash = tratto
    stile_grafico(graf)
    graf.height, graf.width = 10, 20
    ws.add_chart(graf, "M22")
    ws.freeze_panes = "A7"


# ---------------------------------------------------------------- Notizie (ex Analisi_News)
def foglio_notizie(wb):
    ws = wb["Notizie"]
    titolo(ws, "Notizie: pressione sulle categorie di rischio", 10)
    n = len(TASSONOMIA)
    fine = 4 + n                                          # ultima riga delle categorie (D-74: nove)
    intest = ["Codice", "Categoria", "Intensita' max 4 sett. (0-3)", "Notizie con intensita' >= 2",
              "Rischi in anagrafica", "Presidio", "Intensita' 1: nesso indiretto", "Intensita' 2: nesso diretto",
              "Intensita' 3: diretto e immediato", "Etichetta del grafico"]
    for j, t in enumerate(intest, start=1):
        c = ws.cell(row=4, column=j, value=t); c.font = Font(size=9, bold=True); c.alignment = A_CAPO
    finestra = 'NW_Settimana,">="&inizioFinestra4,NW_Settimana,"<="&settimanaCorrente'
    for i, (cod, nome) in enumerate(TASSONOMIA):
        r = 5 + i
        col = "NW_Imp_" + cod.replace("-", "_").replace(".", "_")
        ws[f"A{r}"] = cod
        ws[f"B{r}"] = nome
        ws[f"C{r}"] = f"=_xlfn.MAXIFS({col},{finestra})"
        ws[f"D{r}"] = f'=COUNTIFS({col},">=2",{finestra})'
        ws[f"E{r}"] = f"=COUNTIF(ANA_Event_Type,A{r})"
        # D-79: una categoria senza rischi del radar ma con un rischio in osservazione non e' scoperta: e' osservata.
        ws[f"F{r}"] = (f'=IF(E{r}>0,"Presidiata",IF(COUNTIFS(RR_Ciclo,cicloCorrente,RR_Stato,"Osservazione",'
                       f'RR_Event_Type,A{r})>0,"In osservazione",IF(D{r}>0,"AREA NON PRESIDIATA","Nessun rischio censito")))')
        for k, l in enumerate("GHI", start=1):
            ws[f"{l}{r}"] = f"=COUNTIFS({col},{k},{finestra})"
        ws[f"J{r}"] = f'=IF(F{r}="AREA NON PRESIDIATA","NON PRESIDIATA ► ","")&A{r}&" "&B{r}'
    ws.conditional_formatting.add(f"F5:F{fine}", FormulaRule(formula=['F5="AREA NON PRESIDIATA"'], fill=ROSSO_CF))
    ws.conditional_formatting.add(f"F5:F{fine}", FormulaRule(formula=['F5="In osservazione"'], fill=fill(FONDO_OSSERVAZIONE),
                                                             font=Font(color=TESTO_OSSERVAZIONE)))
    nome_definito(wb, "presidioCodici", f"Notizie!$A$5:$A${fine}")      # letti dallo script (comando settimanale)
    nome_definito(wb, "presidioStato", f"Notizie!$F$5:$F${fine}")
    # Sintesi di A3 e flag della settimana corrente (tabella tblSettimane, D-66), a destra della tabella.
    for riga, (etichetta, colonna, vuoto) in ((4, ("Sintesi di A3 della settimana corrente", "SE_Sintesi_A3",
                                                    "Nessuna sintesi di A3 per la settimana corrente.")),
                                              (10, ("Flag proposti da A3 (non cambiano score)", "SE_Flag_Proposti", "—"))):
        c = ws.cell(row=riga, column=12, value=etichetta); c.font = GRASSETTO
        ws.merge_cells(start_row=riga + 1, start_column=12, end_row=riga + (5 if riga == 4 else 3), end_column=19)
        c = ws.cell(row=riga + 1, column=12,
                    value=f'=IFERROR(INDEX({colonna},MATCH(settimanaCorrente,SE_Settimana,0))&"","{vuoto}")')
        c.alignment = Alignment(wrap_text=True, vertical="top")
        c.font = Font(size=9)
        c.fill = fill(VERDE_TENUE)
    c = ws.cell(row=21, column=12, value="Proposta di ciclo straordinario di A3 (decide la funzione di rischio, D-75)")
    c.font = GRASSETTO
    ws.merge_cells(start_row=22, start_column=12, end_row=24, end_column=19)
    c = ws.cell(row=22, column=12, value='=IFERROR(INDEX(SE_Proposta_Straordinario,MATCH(settimanaCorrente,SE_Settimana,0))&"","—")')
    c.alignment, c.font, c.fill = Alignment(wrap_text=True, vertical="top"), Font(size=9, bold=True), fill(VERDE_TENUE)
    ws.conditional_formatting.add("L22", FormulaRule(formula=['LEFT($L$22,8)="PROPOSTA"'], fill=fill("F8CBAD"),
                                                     font=Font(bold=True, color="C00000")))
    c = ws.cell(row=15, column=12, value="Notizie di A3 sui rischi in osservazione (registro unico, D-79)")
    c.font = GRASSETTO
    ws.merge_cells(start_row=16, start_column=12, end_row=19, end_column=19)
    c = ws.cell(row=16, column=12, value=(
        '=IF(cicloCorrente="","—","Nelle ultime 4 settimane A3 ha collegato "&SUMPRODUCT((NW_Settimana>=inizioFinestra4)'
        '*(NW_Settimana<=settimanaCorrente)*(COUNTIFS(RR_ID_Rischio,NW_Rischio_ID,RR_Ciclo,cicloCorrente,'
        'RR_Stato,"Osservazione")>0))&" notizie a rischi in osservazione: quanti per rischio nel foglio Osservazione, '
        'colonna O; un flag di A3 su uno di questi rischi è fra i flag proposti qui sopra.")'))
    c.alignment, c.font, c.fill = Alignment(wrap_text=True, vertical="top"), Font(size=9), fill(VERDE_TENUE)
    for l in "LMNOPQRS":
        ws.column_dimensions[l].width = 12
    ws[f"A{fine + 2}"] = "Notizie non collegate a un rischio censito (4 settimane)"
    ws[f"D{fine + 2}"] = f'=COUNTIFS(NW_Rischio_ID,"NON PRESIDIATO",{finestra})'
    p0 = fine + 4                                         # pressione settimanale
    sezione(ws, p0, 1, 5, "Pressione settimanale (12 settimane)")
    for j, t in enumerate(["Settimana", "Notizie", "Peggiorativi", "Migliorativi", "Netto"], start=1):
        ws.cell(row=p0 + 1, column=j, value=t).font = GRASSETTO
    for i in range(12):
        r = p0 + 2 + i
        ws[f"A{r}"] = f"=Parametri!$B${34 + i}"; ws[f"A{r}"].number_format = "dd/mm/yyyy"
        ws[f"B{r}"] = f"=COUNTIFS(NW_Settimana,A{r})"
        ws[f"C{r}"] = f'=COUNTIFS(NW_Settimana,A{r},NW_Segnale,"Peggiorativo")'
        ws[f"D{r}"] = f'=COUNTIFS(NW_Settimana,A{r},NW_Segnale,"Migliorativo")'
        ws[f"E{r}"] = f"=C{r}-D{r}"
    for l, w in zip("ABCDEFGHIJ", [12, 50, 16, 16, 14, 24, 12, 12, 12, 40]):
        ws.column_dimensions[l].width = w
    ws.row_dimensions[4].height = 30
    barre_et = BarChart()
    barre_et.type = "bar"
    barre_et.grouping = "stacked"
    barre_et.overlap = 100
    barre_et.title = "Notizie delle ultime 4 settimane per categoria, per intensita'"
    barre_et.add_data(Reference(ws, min_col=7, max_col=9, min_row=4, max_row=fine), titles_from_data=True)
    barre_et.set_categories(Reference(ws, min_col=10, min_row=5, max_row=fine))
    for serie, colore in zip(barre_et.series, ["FCE4D6", "F4B183", "C55A11"]):
        serie.graphicalProperties.solidFill = colore
        serie.graphicalProperties.line.solidFill = "7F7F7F"
    barre_et.x_axis.scaling.orientation = "maxMin"     # la prima categoria in alto, come nella tabella
    barre_et.y_axis.scaling.min = 0
    barre_et.y_axis.majorUnit = 1
    stile_grafico(barre_et)
    barre_et.height, barre_et.width = 10, 22
    ws[f"A{p0 + 15}"] = "Grafici: notizie per categoria (sopra) e segnali per settimana (sotto)."; ws[f"A{p0 + 15}"].font = NOTA
    ws.add_chart(barre_et, f"A{p0 + 16}")
    barre = BarChart()
    barre.title = "Segnali per settimana"
    barre.add_data(Reference(ws, min_col=3, max_col=4, min_row=p0 + 1, max_row=p0 + 13), titles_from_data=True)
    barre.set_categories(Reference(ws, min_col=1, min_row=p0 + 2, max_row=p0 + 13))
    for serie, colore in zip(barre.series, [ROSSO, BLU_DIM]):
        serie.graphicalProperties.solidFill = colore
    stile_grafico(barre)
    barre.height, barre.width = 8, 22
    ws.add_chart(barre, f"A{p0 + 37}")


# ---------------------------------------------------------------- Classifica e lente di Mosca
def _serie_dinamica(serie, nome_valori, nome_categorie, titolo_serie):
    """Serie che legge nomi definiti OFFSET: tanti punti quanti i rischi valutati.
    Nel file del grafico un nome del workbook si scrive "[0]!nome"."""
    serie.tx = SeriesLabel(v=titolo_serie)
    serie.val.numRef.f = f"[0]!{nome_valori}"
    serie.cat = AxDataSource(strRef=StrRef(f=f"[0]!{nome_categorie}"))


def foglio_classifica(wb):
    """Rischi del ciclo corrente ordinati per score composito, con urgenza; lente di Mosca ordinata per ritardo."""
    ws = wb["Classifica"]
    titolo(ws, "Classifica e lente di Mosca", 11)
    intest = ["Pos.", "ID", "Nome", "Score composito", "Score ciclo prima", "Δ score", "Esito", "Urgenza (Mosca)",
              "Margine Z-(X+Y), anni", "Owner", "Etichetta del grafico"]
    for j, t in enumerate(intest, start=1):
        c = ws.cell(row=4, column=j, value=t); c.font = Font(size=9, bold=True); c.alignment = A_CAPO
    ultima = 4 + MAX_RISCHI
    rng = lambda foglio, col, r0: f"{foglio}!${col}${r0}:${col}${r0 + MAX_RISCHI - 1}"
    for i in range(MAX_RISCHI):
        r, k = 5 + i, i + 1
        # T: chiave d'ordine (score meno uno spareggio minimo per posizione); U: posizione del k-esimo.
        ws[f"T{r}"] = f'=IF(ISNUMBER(INDEX(posScore,{k})),INDEX(posScore,{k})-{k}/100000,"")'
        ws[f"U{r}"] = f'=IFERROR(MATCH(_xlfn.AGGREGATE(14,6,$T$5:$T${ultima},{k}),$T$5:$T${ultima},0),"")'
        vuoto = f'$U{r}=""'
        ws[f"A{r}"] = f'=IF({vuoto},"",{k})'
        ws[f"B{r}"] = f'=IF({vuoto},"",INDEX(posID,$U{r}))'
        ws[f"C{r}"] = f'=IF({vuoto},"",INDEX(posNome,$U{r}))'
        ws[f"D{r}"] = f'=IF({vuoto},"",INDEX(posScore,$U{r}))'
        ws[f"E{r}"] = f'=IF({vuoto},"",IFERROR(INDEX(posScorePrec,$U{r}),"—"))'
        ws[f"F{r}"] = f'=IF(AND(ISNUMBER(D{r}),ISNUMBER(E{r})),D{r}-E{r},"")'
        ws[f"G{r}"] = f'=IF({vuoto},"",IFERROR(INDEX(RR_Esito,MATCH(cicloCorrente&"|"&B{r},RR_Chiave,0))&"",""))'
        ws[f"H{r}"] = f'=IF({vuoto},"",INDEX({rng("Radar_Mosca", "L", 5)},$U{r}))'
        ws[f"I{r}"] = f'=IF({vuoto},"",IFERROR(INDEX({rng("Radar_Mosca", "K", 5)},$U{r}),""))'
        ws[f"J{r}"] = f'=IF({vuoto},"",INDEX(ANA_Owner,$U{r})&"")'
        ws[f"K{r}"] = (f'=IF({vuoto},"",B{r}&" "&IF(ISNUMBER(F{r}),IF(F{r}>0,"▲",IF(F{r}<0,"▼","●")),"○")'
                       f'&"  "&LEFT(C{r},34)&IF(LEN(C{r})>34,"…",""))')
        # Barre, una serie per esito dell'urgenza (NA() = nessuna barra).
        # Zero, non NA(), dove il rischio non ha quell'esito: l'etichetta di un punto #N/D si vedrebbe.
        agire, entro = f'LEFT(H{r},9)="AGIRE ORA"', f'LEFT(H{r},11)="Agire entro"'
        ws[f"V{r}"] = f'=IF({vuoto},NA(),IF({agire},D{r},0))'
        ws[f"W{r}"] = f'=IF({vuoto},NA(),IF({entro},D{r},0))'
        ws[f"X{r}"] = f'=IF({vuoto},NA(),IF(OR({agire},{entro}),0,D{r}))'
        # X, Y, Z del rischio (Radar_Mosca colonne I, J, H).
        ws[f"Y{r}"] = f'=IF({vuoto},NA(),INDEX({rng("Radar_Mosca", "I", 5)},$U{r}))'
        ws[f"Z{r}"] = f'=IF({vuoto},NA(),INDEX({rng("Radar_Mosca", "J", 5)},$U{r}))'
        ws[f"AA{r}"] = f'=IF({vuoto},NA(),INDEX({rng("Radar_Mosca", "H", 5)},$U{r}))'
        ws[f"AB{r}"] = f'=IF(LEFT(H{r},9)="AGIRE ORA",B{r},"")'
        for col in "DEFI":
            ws[f"{col}{r}"].number_format = "0.00"
        ws[f"F{r}"].number_format = FORMATO_DELTA
        for col in "VWX":
            ws[f"{col}{r}"].number_format = "0.00;-0.00;;"       # lo zero non ha etichetta nel grafico
        # Lente ordinata per margine (dal piu' in ritardo): AD chiave, AE posizione in classifica, AF..AJ serie.
        ws[f"AD{r}"] = f'=IF(ISNUMBER(I{r}),I{r}+{k}/100000,"")'
        ws[f"AE{r}"] = f'=IFERROR(MATCH(_xlfn.AGGREGATE(15,6,$AD$5:$AD${ultima},{k}),$AD$5:$AD${ultima},0),"")'
        q = f"$AE{r}"
        at = lambda col: f"INDEX(${col}$5:${col}${ultima},{q})"
        ws[f"AF{r}"] = (f'=IF({q}="","",{at("B")}&" ("&IF({at("I")}<0,"−","+")&FIXED(ABS({at("I")}),2)&")")')
        ws[f"AG{r}"] = f'=IF({q}="",NA(),{at("Y")})'
        ws[f"AH{r}"] = f'=IF({q}="",NA(),IF({at("Y")}+{at("Z")}>{at("AA")},NA(),{at("Z")}))'
        ws[f"AI{r}"] = f'=IF({q}="",NA(),IF({at("Y")}+{at("Z")}>{at("AA")},{at("Z")},NA()))'
        ws[f"AJ{r}"] = f'=IF({q}="",NA(),{at("AA")})'
    for testo, col in [("Chiave d'ordine", "T"), ("Posizione in anagrafica", "U"), ("Barra: agire ora", "V"),
                       ("Barra: entro l'anno", "W"), ("Barra: con margine", "X"), ("X anni", "Y"), ("Y anni", "Z"),
                       ("Z anni", "AA"), ("Da affrontare subito", "AB"), ("Chiave della lente", "AD"),
                       ("Posizione nella lente", "AE"), ("Etichetta della lente", "AF"), ("X", "AG"),
                       ("Y entro Z", "AH"), ("Y oltre Z", "AI"), ("Z", "AJ")]:
        ws[f"{col}4"] = testo
    for l in range(20, 37):
        ws.column_dimensions[get_column_letter(l)].hidden = True
    chip_urgenza(ws, f"H5:H{ultima}", "H5")
    colora_delta(ws, f"F5:F{ultima}", "F5")
    for l, w in zip("ABCDEFGHIJK", [6, 9, 46, 11, 11, 9, 12, 20, 12, 28, 36]):
        ws.column_dimensions[l].width = w
    ws.row_dimensions[4].height = 30
    # Titoli che dicono il messaggio (celle di appoggio).
    ws["AL2"] = (f'=IF(COUNTIF(H5:H{ultima},"AGIRE ORA*")=0,"Nessun rischio da affrontare subito",'
                 f'COUNTIF(H5:H{ultima},"AGIRE ORA*")&" da affrontare subito: "&_xlfn.TEXTJOIN(", ",TRUE,AB5:AB{ultima}))')
    ws["AL3"] = "Lente di Mosca: chi e' in ritardo, e di quanto (anni)"
    ws.column_dimensions["AL"].hidden = True

    n = f"MAX(1,COUNT(Classifica!$D$5:$D${ultima}))"
    for nome, col in [("classificaEtichette", "K"), ("classificaID", "B"), ("classificaAgire", "V"), ("classificaEntro", "W"),
                      ("classificaMargine", "X"), ("lenteEtichette", "AF"), ("lenteX", "AG"), ("lenteY", "AH"),
                      ("lenteYOltre", "AI"), ("lenteZ", "AJ")]:
        nome_definito(wb, nome, f"OFFSET(Classifica!${col}$5,0,0,{n},1)")

    barre = BarChart()
    barre.type = "bar"
    barre.grouping = "clustered"
    barre.overlap = 100               # le tre serie nello stesso posto: ogni rischio ha una sola barra
    barre.gapWidth = 45
    barre.visible_cells_only = False  # le serie stanno in colonne nascoste: senza, Excel le scarta tutte
    for col, (nome, testo, colore) in zip((22, 23, 24), [("classificaAgire", "Agire ora (X + Y > Z)", ROSSO),
                                                          ("classificaEntro", "Agire entro l'anno", AMBRA),
                                                          ("classificaMargine", "Con margine", GRIGIO_URG)]):
        barre.add_data(Reference(ws, min_col=col, min_row=5, max_row=ultima), titles_from_data=False)
        s = barre.series[-1]
        _serie_dinamica(s, nome, "classificaEtichette", testo)
        s.graphicalProperties.solidFill = colore
        s.graphicalProperties.line.noFill = True
        etichette_valore(s)
    asse_fisso(barre, 0, 5)
    barre.title = titolo_da_cella(ws, "$AL$2")
    barre.x_axis.scaling.orientation = "maxMin"       # il primo della classifica in alto
    stile_grafico(barre)
    barre.height, barre.width = 12.5, 15.5
    ws.add_chart(barre, f"A{ultima + 3}")

    colonne = BarChart()
    colonne.type = "col"
    colonne.grouping = "stacked"
    colonne.overlap = 100
    colonne.gapWidth = 60
    colonne.visible_cells_only = False
    for col, (nome, testo, colore) in zip((33, 34, 35), [("lenteX", "X: decidere e avviare", "BFBFBF"),
                                                         ("lenteY", "Y: mitigare, entro Z", "ED7D31"),
                                                         ("lenteYOltre", "Y: mitigare, OLTRE Z", ROSSO)]):
        colonne.add_data(Reference(ws, min_col=col, min_row=5, max_row=ultima), titles_from_data=False)
        s = colonne.series[-1]
        _serie_dinamica(s, nome, "lenteEtichette", testo)
        s.graphicalProperties.solidFill = colore
        s.graphicalProperties.line.noFill = True
    rombi = LineChart()
    rombi.add_data(Reference(ws, min_col=36, min_row=5, max_row=ultima), titles_from_data=False)
    s = rombi.series[0]
    _serie_dinamica(s, "lenteZ", "lenteEtichette", "Z: tempo disponibile")
    s.smooth = False
    s.graphicalProperties.line.noFill = True
    s.marker.symbol = "diamond"
    s.marker.size = 10
    s.marker.graphicalProperties = GraphicalProperties(solidFill=BLU_NOTTE)
    s.marker.graphicalProperties.line.solidFill = BLU_NOTTE
    colonne.y_axis.scaling.min = 0          # anni: minimo fisso, massimo automatico (Y puo' valere anni)
    colonne.y_axis.title = "anni"
    colonne.varyColors = False
    colonne.title = titolo_da_cella(ws, "$AL$3")
    stile_grafico(colonne)
    colonne += rombi                        # stessi assi (id 10 e 100): un solo grafico
    colonne.height, colonne.width = 12.5, 15.5
    ws.add_chart(colonne, f"H{ultima + 3}")
    nota = ultima + 29
    ws.merge_cells(f"A{nota}:K{nota}")
    ws[f"A{nota}"] = ("Come si legge: a sinistra un rischio per barra, dal piu' alto per score composito; colore = urgenza, "
                      "freccia = variazione sul ciclo prima. A destra la lente di Mosca, dal piu' in ritardo: colonna = "
                      "tempo necessario X + Y, rombo = tempo disponibile Z; la parte rossa sfora (tra parentesi il margine).")
    ws[f"A{nota}"].font = NOTA
    ws[f"A{nota}"].alignment = A_CAPO
    ws.row_dimensions[nota].height = 30
    legenda(ws, nota + 1, 11, f"{LEG_MOSCA}. Frecce: ▲ score in aumento, ▼ in diminuzione, ● invariato, ○ nuovo. {LEG_RISCHIO}.")
    imposta_stampa(ws, f"A1:K{nota + 1}")
    ws.page_setup.fitToHeight = 1


# ---------------------------------------------------------------- Matrice Probabilita x Impatto
DESCR_P = {5: "Quasi certa", 4: "Probabile", 3: "Possibile", 2: "Improbabile", 1: "Remota"}     # rubrica sez. 1 (D-52)
DESCR_S = {1: "Limitato", 2: "Contenuto", 3: "Rilevante", 4: "Grave", 5: "Critico"}     # rubrica sez. 1 (D-61)


def fascia_pxi(v):
    return ROSSO_TENUE if v >= 15 else AMBRA_TENUE if v >= 8 else VERDE_TENUE


def foglio_matrice(wb):
    """Gravita': ogni rischio nella cella della sua Probabilita e Impatto; sotto, i rischi dal piu' grave."""
    ws = wb["Matrice"]
    titolo(ws, "Matrice di gravita'", 7)
    B = 12                                    # blocco nascosto (L..)
    Lb = lambda j: get_column_letter(B + j)
    fine = 4 + MAX_RISCHI
    # Per posizione dell'anagrafica: ID, codice cella (P*10+S), P x I, etichetta con ◆.
    for i in range(MAX_RISCHI):
        r, k = 5 + i, i + 1
        ws[f"{Lb(0)}{r}"] = f'=INDEX(posID,{k})&""'
        ws[f"{Lb(1)}{r}"] = f'=IF(AND(ISNUMBER(INDEX(posProbabilita,{k})),ISNUMBER(INDEX(posImpatto,{k}))),INDEX(posProbabilita,{k})*10+INDEX(posImpatto,{k}),"")'
        ws[f"{Lb(2)}{r}"] = f'=IF({Lb(1)}{r}="","",INDEX(posProbabilita,{k})*INDEX(posImpatto,{k}))'
        ws[f"{Lb(3)}{r}"] = f'=IF({Lb(1)}{r}="","",{Lb(0)}{r}&IF(INDEX(ANA_Attenzione_Supervisore,{k})="Sì"," ◆",""))'
        ws[f"{Lb(4)}{r}"] = f'=IF({Lb(2)}{r}="","",{Lb(2)}{r}-{k}/1000)'
        ws[f"{Lb(5)}{r}"] = f'=IFERROR(MATCH(_xlfn.AGGREGATE(14,6,${Lb(4)}$5:${Lb(4)}${fine},{k}),${Lb(4)}$5:${Lb(4)}${fine},0),"")'
    # Per ognuna delle 25 celle, una colonna con l'etichetta dei rischi che ci cadono (poi TEXTJOIN).
    celle = [(p, s) for p in range(5, 0, -1) for s in range(1, 6)]
    for n, (p, s) in enumerate(celle):
        col = Lb(7 + n)
        ws[f"{col}4"] = p * 10 + s
        for i in range(MAX_RISCHI):
            r = 5 + i
            ws[f"{col}{r}"] = f'=IF(${Lb(1)}{r}={col}$4,${Lb(3)}{r},"")'
    for j in range(7 + len(celle)):
        ws.column_dimensions[Lb(j)].hidden = True
    ws["A4"] = "Probabilita"; ws["A4"].font = Font(bold=True, color=BLU_NOTTE)
    bianco = Side(style="medium", color="FFFFFF")
    for i, p in enumerate(range(5, 0, -1)):
        r = 5 + i
        c = ws.cell(row=r, column=1, value=DESCR_P[p]); c.font = Font(size=9, color=TESTO_TENUE)
        c.alignment = Alignment(horizontal="right", vertical="center")
        c = ws.cell(row=r, column=2, value=p); c.font = Font(bold=True, color=BLU_NOTTE)
        c.alignment = Alignment(horizontal="center", vertical="center")
        for s in range(1, 6):
            col = Lb(7 + celle.index((p, s)))
            c = ws.cell(row=r, column=2 + s, value=f'=_xlfn.TEXTJOIN("   ",TRUE,{col}5:{col}{fine})')
            c.fill = fill(fascia_pxi(p * s))
            c.font = Font(size=10, bold=True)
            c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
            c.border = Border(left=bianco, right=bianco, top=bianco, bottom=bianco)
        ws.row_dimensions[r].height = 50
    for s in range(1, 6):
        c = ws.cell(row=10, column=2 + s, value=s); c.font = Font(bold=True, color=BLU_NOTTE); c.alignment = Alignment(horizontal="center")
        c = ws.cell(row=11, column=2 + s, value=DESCR_S[s]); c.font = Font(size=9, color=TESTO_TENUE); c.alignment = Alignment(horizontal="center")
    ws["E12"] = "Impatto"; ws["E12"].font = Font(bold=True, color=BLU_NOTTE); ws["E12"].alignment = Alignment(horizontal="center")
    ws.column_dimensions["A"].width = 13
    ws.column_dimensions["B"].width = 5
    for l in "CDEFG":
        ws.column_dimensions[l].width = 20
    # Sotto: i rischi dal piu' grave.
    sezione(ws, 14, 1, 7, "I rischi, dal piu' grave")
    for j, t in ((1, "ID"), (3, "Rischio"), (6, "P · S"), (7, "P x I")):
        c = ws.cell(row=15, column=j, value=t); c.font = Font(size=9, bold=True, color="FFFFFF")
    for x in range(1, 8):
        ws.cell(row=15, column=x).fill = fill(BLU_MEDIO)
    ws.merge_cells("A15:B15"); ws.merge_cells("C15:E15")
    for i in range(MAX_RISCHI):
        r = 16 + i
        q = f"${Lb(5)}${5 + i}"
        ws.merge_cells(f"A{r}:B{r}"); ws.merge_cells(f"C{r}:E{r}")
        ws[f"A{r}"] = f'=IF({q}="","",INDEX(posID,{q}))'
        ws[f"C{r}"] = f'=IF({q}="","",INDEX(posNome,{q})&IF(INDEX(ANA_Attenzione_Supervisore,{q})="Sì","  ◆",""))'
        ws[f"F{r}"] = f'=IF({q}="","",INDEX(posProbabilita,{q})&" · "&INDEX(posImpatto,{q}))'
        ws[f"G{r}"] = f'=IF({q}="","",INDEX(${Lb(2)}$5:${Lb(2)}${fine},{q}))'
        ws[f"A{r}"].font = Font(size=9, bold=True, color=BLU_NOTTE)
        ws[f"C{r}"].font = Font(size=9)
        for col in "FG":
            ws[f"{col}{r}"].alignment = Alignment(horizontal="center")
        for x in range(1, 8):
            ws.cell(row=r, column=x).border = BORDO_SOTTILE
    ult = 15 + MAX_RISCHI
    for formula, colore in (("AND(ISNUMBER(G16),G16>=15)", ROSSO_TENUE), ("AND(ISNUMBER(G16),G16>=8,G16<15)", AMBRA_TENUE),
                            ("AND(ISNUMBER(G16),G16<8)", VERDE_TENUE)):
        ws.conditional_formatting.add(f"G16:G{ult}", FormulaRule(formula=[formula], fill=fill(colore), font=Font(bold=True)))
    legenda(ws, ult + 2, 7, f"{LEG_PXI}; verde fino a 6, ambra da 8 a 12, rosso da 15. {LEG_RISCHIO}.")
    imposta_stampa(ws, f"A1:G{ult + 2}")
    ws.page_setup.fitToHeight = 1


# ---------------------------------------------------------------- Quadro d'insieme (ex Sintesi)
def foglio_quadro(wb):
    """Prima pagina del report: il quadro; seconda: il commento e i rischi segnalati con il perche'."""
    ws = wb["Quadro"]
    titolo(ws, "Quadro d'insieme", 15)
    for j in range(1, 16):
        ws.column_dimensions[get_column_letter(j)].width = 10.5
    ws.column_dimensions["I"].width = 3
    # Appoggio (nascosto, da T): rischi in Attivazione (D-63), commento di A1.
    livelli = f"Radar_Mosca!${COL_LIVELLO}$5:${COL_LIVELLO}${4 + MAX_RISCHI}"
    ws["T4"] = f'=COUNTIF({livelli},"Attivazione")'
    for i in range(MAX_RISCHI):
        ws[f"T{5 + i}"] = f'=IF(Radar_Mosca!${COL_LIVELLO}${5 + i}="Attivazione",Radar_Mosca!$A${5 + i},"")'
    kri_vigore = 'COUNTIFS(KRI_Ciclo,cicloCorrente,KRI_In_Vigore,"Sì")'
    riquadri = [
        ("Rischi valutati", "=coperturaValutati",
         '="su "&coperturaAnagrafica&" in anagrafica · "&IF(coperturaValutati=coperturaAnagrafica,"completo","INCOMPLETO")', FONDO_TENUE, BLU_NOTTE),
        ("Livello di allerta: attivazione · attenzione", f'=$T$4&" · "&COUNTIF({livelli},"Attenzione")',
         f'=IF($T$4=0,"nessun rischio in attivazione","in attivazione: "&_xlfn.TEXTJOIN(", ",TRUE,$T$5:$T${4 + MAX_RISCHI}))'
         f'&" · in monitoraggio "&COUNTIF({livelli},"Monitoraggio")', ROSSO_TENUE, ROSSO),
        # D-79: variati e nuovi fra i rischi del radar ("Radar*" = Radar e Radar, in uscita); sotto i movimenti.
        ("Variati · nuovi (radar)", '=COUNTIFS(RR_Ciclo,cicloCorrente,RR_Stato,"Radar*",RR_Esito,"Variato")&" · "'
                                    '&COUNTIFS(RR_Ciclo,cicloCorrente,RR_Stato,"Radar*",RR_Esito,"Nuovo")',
         '="rispetto al "&cicloPrecedente&" · entrati nel radar "&COUNTIFS(RR_Ciclo,cicloCorrente,RR_Movimento,"Entrato")'
         '&", usciti "&COUNTIFS(RR_Ciclo,cicloCorrente,RR_Movimento,"Uscito")&" · in osservazione "'
         '&COUNTIFS(RR_Ciclo,cicloCorrente,RR_Stato,"Osservazione")', FONDO_TENUE, BLU_NOTTE),
        ("KRI in rosso", '=COUNTIFS(KRI_Ciclo,cicloCorrente,KRI_In_Vigore,"Sì",KRI_Stato,"Rosso")',
         f'="su "&{kri_vigore}&" in vigore"', ROSSO_TENUE, ROSSO),
        ("Validazione", '=IF(decisioniDaPrendere>0,decisioniDaPrendere,"✓")',
         '=IF(decisioniDaPrendere>0,"righe da validare: ciclo non validato","ciclo validato")', VERDE_TENUE, "375623"),
    ]
    for (da, a), (didascalia, valore, sotto, fondo, colore) in zip([(1, 3), (4, 6), (7, 9), (10, 12), (13, 15)], riquadri):
        for r, testo, font in [(4, didascalia, Font(size=9, bold=True, color=TESTO_TENUE)),
                               (5, valore, Font(size=26, bold=True, color=colore)), (6, sotto, Font(size=9, color=TESTO_TENUE))]:
            ws.merge_cells(start_row=r, start_column=da, end_row=r, end_column=a)
            c = ws.cell(row=r, column=da, value=testo)
            c.font = font
            c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
            for x in range(da, a + 1):
                ws.cell(row=r, column=x).fill = fill(fondo)
            ws.cell(row=r, column=a).border = Border(right=Side(style="thick", color="FFFFFF"))
    ws.row_dimensions[5].height = 36
    ws.row_dimensions[6].height = 34                  # D-79: sotto "Variati" anche i movimenti del radar
    # Senza rischi in attivazione o KRI rossi, il riquadro torna grigio.
    ws.conditional_formatting.add("D4:F6", FormulaRule(formula=["$T$4=0"], fill=fill(FONDO_TENUE)))
    ws.conditional_formatting.add("J4:L6", FormulaRule(formula=["$J$5=0"], fill=fill(FONDO_TENUE)))
    ws.conditional_formatting.add("M4:O6", FormulaRule(formula=["decisioniDaPrendere>0"], fill=fill(AMBRA_TENUE)))

    sezione(ws, 8, 1, 8, "Priorita' — primi cinque per score composito")
    sezione(ws, 8, 10, 15, "Gravita': Probabilita x Impatto")
    for j, t in [(1, "#"), (2, "Rischio"), (6, "Score"), (7, "Variazione"), (8, "Urgenza")]:
        ws.cell(row=9, column=j, value=t).font = Font(size=9, bold=True, color=TESTO_TENUE)
    ws.merge_cells("B9:E9")
    for k in range(5):
        r, cr = 10 + k, 5 + k
        ws[f"A{r}"] = f"=Classifica!$A${cr}"
        ws.merge_cells(f"B{r}:E{r}")
        ws[f"B{r}"] = (f'=IF(Classifica!$B${cr}="","",Classifica!$B${cr}&"  "&Classifica!$C${cr}'
                       f'&IFERROR(IF(INDEX(ANA_Attenzione_Supervisore,Classifica!$U${cr})="Sì","  ◆",""),""))')
        ws[f"F{r}"] = f'=IF(Classifica!$B${cr}="","",Classifica!$D${cr})'
        ws[f"G{r}"] = f'=IF(Classifica!$B${cr}="","",IF(ISNUMBER(Classifica!$F${cr}),Classifica!$F${cr},"nuovo"))'
        ws[f"H{r}"] = (f'=IF(Classifica!$B${cr}="","",IF(LEFT(Classifica!$H${cr},9)="AGIRE ORA","AGIRE ORA",'
                       f'IF(LEFT(Classifica!$H${cr},11)="Agire entro","Entro l\'anno",Classifica!$H${cr})))')
        ws[f"A{r}"].font = Font(bold=True, color=BLU_NOTTE)
        ws[f"A{r}"].alignment = Alignment(horizontal="center", vertical="center")
        ws[f"B{r}"].font = Font(size=9)
        ws[f"B{r}"].alignment = Alignment(wrap_text=True, vertical="center")
        ws[f"F{r}"].number_format = "0.00"; ws[f"F{r}"].font = Font(bold=True)
        ws[f"G{r}"].number_format = FORMATO_DELTA
        for col in "FG":
            ws[f"{col}{r}"].alignment = Alignment(horizontal="center", vertical="center")
        ws[f"H{r}"].font = Font(size=9)
        ws[f"H{r}"].alignment = Alignment(horizontal="center", vertical="center", shrink_to_fit=True)
        for j in range(1, 9):
            ws.cell(row=r, column=j).border = BORDO_SOTTILE
        ws.row_dimensions[r].height = 25
    ws.conditional_formatting.add("F10:F14", DataBarRule(start_type="num", start_value=0, end_type="num", end_value=5, color="8EA9DB"))
    colora_delta(ws, "G10:G14", "G10")
    chip_urgenza(ws, "H10:H14", "H10")
    ws["A15"] = "Score 1-5, 5 = peggiore; barra su scala fissa 0-5. Variazione sul ciclo precedente."
    ws["A15"].font = Font(size=8, italic=True, color=TESTO_TENUE)
    # Mini matrice (legge il foglio Matrice).
    ws["J9"] = "P \\ S"; ws["J9"].font = Font(size=8, bold=True, color=TESTO_TENUE)
    bianco = Side(style="thin", color="FFFFFF")
    for s in range(1, 6):
        c = ws.cell(row=9, column=10 + s, value=s); c.font = Font(size=8, bold=True, color=TESTO_TENUE)
        c.alignment = Alignment(horizontal="center")
    for i, p in enumerate(range(5, 0, -1)):
        r = 10 + i
        c = ws.cell(row=r, column=10, value=p); c.font = Font(size=8, bold=True, color=TESTO_TENUE)
        c.alignment = Alignment(horizontal="center", vertical="center")
        for s in range(1, 6):
            c = ws.cell(row=r, column=10 + s,
                        value=f'=SUBSTITUTE(SUBSTITUTE(Matrice!{get_column_letter(2 + s)}{5 + i}," ◆",""),"NFR-","")')
            c.fill = fill(fascia_pxi(p * s))
            c.font = Font(size=7, bold=True)
            c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
            c.border = Border(left=bianco, right=bianco, top=bianco, bottom=bianco)
    ws["J15"] = "Numeri = NFR-nn. Verde P x I fino a 6, ambra 8-12, rosso da 15."; ws["J15"].font = Font(size=8, italic=True, color=TESTO_TENUE)

    # D-72: Note dell'analista, unica cella del report scritta a mano (per esempio la sintesi delle spiegazioni
    # discusse con A7). trimestrale la archivia nel ciclo precedente di tblSintesi e la svuota.
    ws.merge_cells("A16:B16")
    ws["A16"] = "Note dell'analista"
    ws["A16"].font = Font(size=9, bold=True, color=BLU_NOTTE)
    ws["A16"].alignment = Alignment(vertical="top", wrap_text=True)
    ws.merge_cells("C16:O16")
    ws["C16"].font = Font(size=8.5)
    ws["C16"].alignment = Alignment(vertical="top", wrap_text=True)
    for x in range(3, 16):
        ws.cell(row=16, column=x).fill = fill("FFF2CC")
    ws.row_dimensions[16].height = 34
    nome_definito(wb, "quadroNote", "'Quadro'!$C$16")

    # Radar di Mosca (appoggio nel foglio stesso) e legenda dei rischi.
    sezione(ws, 17, 1, 8, "Urgenza: radar di Mosca")
    sezione(ws, 17, 10, 15, "I rischi del ciclo")
    ws.add_chart(grafico_radar(ws, 60, piccolo=True), "B18")
    for i in range(MAX_RISCHI):
        r = 18 + i
        ws.merge_cells(f"K{r}:O{r}")
        ws[f"J{r}"] = f"=INDEX(posID,{i + 1})&\"\""
        ws[f"K{r}"] = f'=IF(J{r}="","",INDEX(posNome,{i + 1})&IF(INDEX(ANA_Attenzione_Supervisore,{i + 1})="Sì","  ◆",""))'
        ws[f"J{r}"].font = Font(size=8, bold=True, color=BLU_NOTTE)
        ws[f"K{r}"].font = Font(size=8)
        ws.row_dimensions[r].height = 12          # 20 righe nello spazio che ne teneva 15 da 16 punti
    fine_radar = 18 + MAX_RISCHI
    ws[f"A{fine_radar}"] = ("Radar: piu' vicino al centro = agire prima; area del cerchio = P x I; colore = livello di allerta "
                            "(rosso attivazione, giallo attenzione, verde monitoraggio); ◆ = attenzione del supervisore. "
                            "Numeri nel radar = NFR-nn.")
    ws[f"A{fine_radar}"].font = Font(size=8, italic=True, color=TESTO_TENUE)
    ws.row_breaks.append(Break(id=fine_radar))

    # Pagina 2: il commento di A1 (messaggio e decisioni), A5, avviso; poi i rischi segnalati.
    r0 = fine_radar + 2                                 # 35
    sezione(ws, r0, 1, 15, "Il commento dell'analisi (agente A1, scritto prima della validazione)")
    uno = "MATCH(cicloCorrente,SI_Ciclo,0)"
    ws[f"T{r0 + 1}"] = f'=IFERROR(INDEX(SI_Sintesi_A1,{uno})&"","")'
    ws[f"T{r0 + 2}"] = f'=IFERROR(SEARCH("DECISIONI:",T{r0 + 1}),0)'
    t, d = f"T{r0 + 1}", f"T{r0 + 2}"
    # Valori rettificati piu' oggetti respinti (un'azione respinta conta una volta, non per ogni suo campo: D-67).
    rettifiche = ('(COUNTIFS(VAL_Periodo,cicloCorrente,VAL_Stato,"Applicata",VAL_Decisione,"Rettificato")'
                  + "".join(f'+COUNTIFS(VAL_Periodo,cicloCorrente,VAL_Stato,"Applicata",VAL_Decisione,"Respinto",'
                            f'VAL_Oggetto,"{o}",VAL_Campo,"{s["campi"][0]}")'
                            for o, s in MAPPA["validazione"]["oggetti"].items() if s["respingibile"] and s["periodo"])
                  + ")")
    righe = [
        ("Messaggio chiave", f'=IF({t}="","Nessun commento registrato per il ciclo corrente.",'
                             f'TRIM(SUBSTITUTE(SUBSTITUTE(IF({d}>0,LEFT({t},{d}-1),{t}),"MESSAGGIO:",""),"Messaggio:","")))'),
        ("Decisioni richieste", f'=IF({d}>0,TRIM(MID({t},{d}+10,4000)),"—")'),
        ("Controlli (A5 se usato)", f'=IFERROR(INDEX(SI_Sintesi_A5,{uno})&"","")&IFERROR(" Osservazioni: "&INDEX(SI_Osservazioni_Controlli,{uno})&".","")'),
        ("Dopo il commento", f'=IF({rettifiche}>0,"Il validatore ha applicato "&{rettifiche}&" rettifiche o respingimenti: numeri e '
                             f'grafici del report sono quelli validati e prevalgono sul commento.","")'),
        # D-71: segnalazioni da motivare (controlli dello script e Bloccanti di A5) portate in validazione.
        ("Segnalazioni da motivare", f'=IFERROR(IF(INDEX(SI_Rilievi_Superati,{uno})="","",INDEX(SI_Rilievi_Superati,{uno})&'
                                     f'" In validazione ogni rischio interessato chiede una motivazione (colonna Segnalazioni)."),"")'),
    ]
    altezze = [44, 30, 30, 30, 30]            # adattate dallo script al testo del ciclo (prepara_report)
    for k, (etichetta, formula) in enumerate(righe):
        r = r0 + 1 + k
        ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=3)
        ws.merge_cells(start_row=r, start_column=4, end_row=r, end_column=15)
        c = ws.cell(row=r, column=1, value=etichetta); c.font = Font(size=10, bold=True, color=BLU_NOTTE)
        c.alignment = Alignment(vertical="top")
        c = ws.cell(row=r, column=4, value=formula); c.font = Font(size=10)
        c.alignment = Alignment(wrap_text=True, vertical="top")
        ws.row_dimensions[r].height = altezze[k]
    for avviso in (r0 + 4, r0 + 5):                    # "Dopo il commento" e segnalazioni da motivare: evidenziati se presenti
        ws.conditional_formatting.add(f"D{avviso}:O{avviso}", FormulaRule(formula=[f'$D${avviso}<>""'], fill=fill(AMBRA_TENUE)))
    for col in "T":
        ws.column_dimensions[col].hidden = True

    rs = r0 + 7                                          # 42
    sezione(ws, rs, 1, 15, "Rischi segnalati e perche'")
    ws[f"A{rs + 1}"] = ("Rischi fra i primi tre per score, in attivazione o in attenzione, variati o nuovi nel ciclo. Tutto "
                        "calcolato dai dati validati del registro.")
    ws[f"A{rs + 1}"].font = Font(size=8, italic=True, color=TESTO_TENUE)
    h = rs + 2
    for (da, a), testo in [((1, 3), "Rischio"), ((4, 4), "Livello"), ((5, 8), "Perche' lo segnaliamo"),
                           ((9, 15), "Cosa e' cambiato, e su quale evidenza")]:
        if da != a:
            ws.merge_cells(start_row=h, start_column=da, end_row=h, end_column=a)
        c = ws.cell(row=h, column=da, value=testo); c.font = Font(bold=True, color="FFFFFF")
        for x in range(da, a + 1):
            ws.cell(row=h, column=x).fill = fill(BLU_MEDIO)
    prima = h + 1
    global QUADRO_SEGNALATI
    QUADRO_SEGNALATI = prima
    for k in range(1, MAX_RISCHI + 1):
        cr = 4 + k
        liv = f"INDEX(Radar_Mosca!${COL_LIVELLO}$5:${COL_LIVELLO}${4 + MAX_RISCHI},Classifica!$U${cr})"
        ws[f"U{prima + k - 1}"] = (f'=IF(Classifica!$B${cr}="","",IF(OR({k}<=3,{liv}="Attivazione",{liv}="Attenzione",'
                                   f'Classifica!$G${cr}="Variato",Classifica!$G${cr}="Nuovo"),{k},""))')
    for n in range(1, MAX_RISCHI + 1):
        r = prima + n - 1
        idx = f"$V{r}"
        ws[f"V{r}"] = f'=IFERROR(_xlfn.AGGREGATE(15,6,$U${prima}:$U${prima + MAX_RISCHI - 1},{n}),"")'
        cl = lambda col: f"INDEX(Classifica!${col}$5:${col}${4 + MAX_RISCHI},{idx})"
        pos = cl("U")
        ident, nome, score, delta, urg, marg, esito = cl("B"), cl("C"), cl("D"), cl("F"), cl("H"), cl("I"), cl("G")
        X, Y, Z = cl("Y"), cl("Z"), cl("AA")
        sup = f'INDEX(ANA_Attenzione_Supervisore,{pos})="Sì"'
        adeg = f"N(INDEX(ANA_Anni_Adeguamento,{pos}))"
        rossi = f'COUNTIFS(KRI_ID_Rischio,{ident},KRI_Ciclo,cicloCorrente,KRI_In_Vigore,"Sì",KRI_Stato,"Rosso")'
        netti = f"INDEX(posNetti,{pos})"
        perche = (
            f'IF({idx}<=3,{idx}&"° per score composito ("&FIXED({score},2)&IF(ISNUMBER({delta}),IF({delta}<>0,", "&IF({delta}>0,"+","")'
            f'&FIXED({delta},2)&" sul ciclo prima",""),"")&"); ","")'
            f'&IF(LEFT({urg},9)="AGIRE ORA","AGIRE ORA: servono X + Y = "&FIXED({X}+{Y},2)&" anni per decidere e mitigare"'
            f'&IF({adeg}>0,", di cui "&{adeg}&" di adeguamento strutturale","")&"; ne restano Z = "&FIXED({Z},1)&" prima che possa '
            f'manifestarsi; ",IF(AND({idx}<=3,LEFT({urg},11)="Agire entro"),"margine di Mosca sotto l\'anno ("&FIXED({marg},2)&"); ",""))'
            f'&IF({esito}="Variato","variato nel ciclo"&IF(ISNUMBER({delta}),IF({delta}>0,": peggiora",IF({delta}<0,": migliora","")),"")&"; ",'
            f'IF({esito}="Nuovo","nuovo nel ciclo; ",""))'
            f'&IF({sup},"tema all\'attenzione del supervisore; ","")'
            f'&IF(INDEX(ANA_Presidio_Controlli,{pos})="Assente","presidio dei controlli assente; ","")'
            f'&IF({rossi}>0,{rossi}&" KRI in rosso; ","")'
            f'&IF({netti}>=sogliaDirezione,"notizie in peggioramento (+"&{netti}&" segnali netti in 4 settimane); ",'
            f'IF({netti}<=-sogliaDirezione,"notizie in miglioramento ("&{netti}&" segnali netti in 4 settimane); ",""))')
        ws[f"W{r}"] = f'=IF({idx}="","",{perche})'
        chiave = f'cicloCorrente&"|"&{ident}'
        var = f"INDEX(RR_Variazioni,MATCH({chiave},RR_Chiave,0))"
        ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=3)
        ws.merge_cells(start_row=r, start_column=5, end_row=r, end_column=8)
        ws.merge_cells(start_row=r, start_column=9, end_row=r, end_column=15)
        ws[f"A{r}"] = (f'=IF({idx}="","",{ident}&CHAR(10)&{nome}&IF({sup},CHAR(10)&"◆ attenzione del supervisore",""))')
        ws[f"D{r}"] = f'=IF({idx}="","",INDEX(Radar_Mosca!${COL_LIVELLO}$5:${COL_LIVELLO}${4 + MAX_RISCHI},{pos})&"")'   # D-63
        ws[f"E{r}"] = f'=IF($W{r}="","",LEFT($W{r},LEN($W{r})-2)&".")'
        ws[f"I{r}"] = (f'=IF({idx}="","",IF({esito}="Nuovo","Rischio nuovo nel ciclo.",IFERROR('
                       f'{json_leggibile(var, COPPIE_VARIAZIONI, "Nessun valore cambiato: confermato sulle fonti del ciclo precedente.")},"")))')
        ws[f"A{r}"].font = Font(size=9, bold=True, color=BLU_NOTTE)
        for col in "AEI":
            ws[f"{col}{r}"].alignment = Alignment(wrap_text=True, vertical="top")
        ws[f"E{r}"].font = Font(size=9); ws[f"I{r}"].font = Font(size=9)
        ws[f"D{r}"].alignment = Alignment(horizontal="center", vertical="top", wrap_text=True)
        ws.row_dimensions[r].height = 46 if n <= 6 else 3     # lo script adatta le altezze (prepara_report)
    ultima = prima + MAX_RISCHI - 1
    chip_livello(ws, f"D{prima}:D{ultima}", f"D{prima}")
    # Bordo solo sulle righe con un rischio: le righe vuote (altezza minima) non lasciano linee in stampa.
    ws.conditional_formatting.add(f"A{prima}:O{ultima}", FormulaRule(formula=[f'$V{prima}<>""'], border=BORDO_SOTTILE))
    for col in "UVW":
        ws.column_dimensions[col].hidden = True
    nome_definito(wb, "quadroSegnalati", f"Quadro!$A${prima}:$O${ultima}")
    nome_definito(wb, "quadroCommento", f"Quadro!$A${r0 + 1}:$O${r0 + 5}")
    lim = ultima + 2
    ws.merge_cells(start_row=lim, start_column=1, end_row=lim, end_column=15)
    c = ws.cell(row=lim, column=1, value="Limiti: " + leggi_limiti())
    c.font = Font(size=8, italic=True, color=TESTO_TENUE)
    c.alignment = Alignment(wrap_text=True, vertical="top")
    ws.row_dimensions[lim].height = 34
    legenda(ws, lim + 1, 15, f"{LEG_RISCHIO}. {LEG_PXI}. {LEG_MOSCA}. Radar: colore del cerchio = livello di allerta (rosso "
                             f"Attivazione, giallo Attenzione, verde Monitoraggio); dentro il cerchio rosso AGIRE ORA (X + Y > Z); "
                             f"area = P x I; settore = categoria di rischio. KRI = indicatore di rischio (Key Risk Indicator). "
                             "A1 = agente che valuta i rischi ogni trimestre; A5 = agente di controllo indipendente.")
    imposta_stampa(ws, f"A1:O{lim + 1}")
    ws.sheet_properties.pageSetUpPr.fitToPage = False
    ws.page_setup.scale = 74          # D-72: la riga delle Note allunga la prima pagina; prepara_report la adatta
    ws.page_margins.top = ws.page_margins.bottom = 0.5
    ws.page_margins.header = ws.page_margins.footer = 0.2


# ---------------------------------------------------------------- Piano delle azioni
def foglio_piano_azioni(wb):
    """Tutte le azioni: prima le proposte da decidere, poi le altre (approvate, in corso, completate, respinte)."""
    ws = wb["Piano_azioni"]
    nome_definito(wb, "capienzaPianoAzioni", str(MAX_AZIONI_PIANO))
    titolo(ws, "Piano delle azioni", 10)
    # D-54: l'azione non dichiara piu' la dimensione che riduce (colonna "Riduce" tolta).
    gruppi = [((1, 6), "La proposta (A1)", "trimestrale"), ((7, 9), "La decisione (validazione) e l'avanzamento", "validazione"),
              ((10, 10), "Validazione", "validazione")]
    for (da, a), t, p in gruppi:
        if da != a:
            ws.merge_cells(start_row=4, start_column=da, end_row=4, end_column=a)
        c = ws.cell(row=4, column=da, value=t); c.font = Font(size=9, bold=True, color=PROCESSI[p][1])
        for x in range(da, a + 1):
            ws.cell(row=4, column=x).fill = fill(PROCESSI[p][0])
    intest = ["Ciclo", "Rischio", "ID azione", "Azione", "Owner", "Orizzonte", "Stato", "Decisa il", "Scadenza", "Validazione"]
    for j, t in enumerate(intest, start=1):
        c = ws.cell(row=5, column=j, value=t); c.font = Font(size=9, bold=True, color="FFFFFF"); c.fill = fill(BLU_NOTTE)
    proposta = STATI_AZIONE[0]
    # Righe mostrate: le proposte, poi le azioni aperte (di ogni ciclo), poi le chiuse (completate, respinte,
    # annullate) del ciclo corrente e del precedente. Il numero resta limitato (capienzaPianoAzioni): la
    # storia intera e' nel foglio Azioni. Chiave: riga + 1.000.000 x gruppo (0 proposta, 1 aperta, 2 chiusa).
    chiusa = '((AZ_Stato="Completata")+(AZ_Stato="Respinta")+(AZ_Stato="Annullata"))'
    incluse = f'((AZ_ID_Azione<>"")*((1-{chiusa})+{chiusa}*((AZ_Ciclo=cicloCorrente)+(AZ_Ciclo=cicloPrecedente)))>0)'
    chiave = f'(ROW(AZ_Stato)+1000000*((AZ_Stato<>"{proposta}")+{chiusa}))'
    campi = [("Ciclo", True), ("ID_Rischio", True), ("ID_Azione", True), ("Descrizione", True), ("Owner", True),
             ("Orizzonte", True), ("Stato", True), ("Data_Decisione", False)]
    lm = lettera("tblAzioni", "Mesi_Orizzonte")
    for k in range(1, MAX_AZIONI_PIANO + 1):
        r = 5 + k
        ws[f"N{r}"] = f'=IFERROR(MOD(_xlfn.AGGREGATE(15,6,{chiave}/{incluse},{k}),1000000),"")'
        for j, (col, testo) in enumerate(campi, start=1):
            ws.cell(row=r, column=j, value=_cella_tab("tblAzioni", "Azioni", col, f"$N{r}", testo))
        ws[f"H{r}"].number_format = "dd/mm/yyyy"
        ws[f"I{r}"] = (f'=IF(OR($N{r}="",H{r}=""),"",IF(OR(G{r}="Approvata",G{r}="In corso"),'
                       f'EDATE(H{r},N(INDEX(Azioni!${lm}:${lm},$N{r}))),""))')
        ws[f"I{r}"].number_format = "dd/mm/yyyy"
        ws.cell(row=r, column=10, value=_cella_tab("tblAzioni", "Azioni", "Validazione", f"$N{r}", True))
        for x in range(1, 11):
            c = ws.cell(row=r, column=x)
            c.border = BORDO_SOTTILE
            c.alignment = Alignment(wrap_text=x == 4, vertical="top")
    fine = 5 + MAX_AZIONI_PIANO
    ws.column_dimensions["N"].hidden = True
    for testo, fondo, colore in ((proposta, AMBRA_TENUE, "7F6000"), ("Approvata", BLU_CHIARO, BLU_NOTTE),
                                 ("In corso", VERDE_TENUE, "375623"), ("Completata", "70AD47", "FFFFFF"),
                                 ("Respinta", FONDO_TENUE, TESTO_TENUE), ("Annullata", FONDO_TENUE, TESTO_TENUE)):
        ws.conditional_formatting.add(f"G6:G{fine}", FormulaRule(formula=[f'G6="{testo}"'], fill=fill(fondo),
                                                                 font=Font(bold=True, color=colore)))
    for l, w in zip("ABCDEFGHIJ", [8, 8, 17, 60, 28, 9, 20, 11, 11, 12]):
        ws.column_dimensions[l].width = w
    ws.freeze_panes = "A6"
    legenda(ws, fine + 2, 10, "Orizzonte = tempo per completare l'azione; "
                              "Scadenza = data della decisione + orizzonte (per le azioni approvate o in corso). Stato: giallo "
                              "= da decidere nella validazione; azzurro = approvata; verde = in corso o completata; grigio = "
                              "respinta o annullata.")


# ---------------------------------------------------------------- Rischi in osservazione (registro unico, D-79)
# Due viste dei rischi del RiskRegister con Stato "Osservazione" nel ciclo corrente, solo formule: il foglio di lavoro
# Osservazione (tutto, piu' la concentrazione per driver e categoria) e la pagina Fenomeni del report. Ordine: colonna
# Ordine_Osservazione della tabella (score piu' alto prima), che vale solo per le righe in osservazione del ciclo
# corrente. Sotto, chi e' entrato o uscito dal radar nel ciclo (colonna Movimento).
FONDO_OSSERVAZIONE = "EDE7F6"           # lilla tenue: rischi in osservazione e loro movimenti
TESTO_OSSERVAZIONE = "5B3F8C"


def _riga_ordine(k):
    """Riga del foglio RiskRegister del k-esimo rischio in osservazione del ciclo corrente; "" se non c'e'."""
    return (f'=IFERROR(MATCH(_xlfn.AGGREGATE(14,6,RR_Ordine_Osservazione,{k}),RR_Ordine_Osservazione,0)'
            f'+{PRIMA_RIGA_DATI - 1},"")')


def _riga_movimento(k):
    """Riga del k-esimo rischio entrato o uscito dal radar nel ciclo corrente."""
    return f'=IFERROR(_xlfn.AGGREGATE(15,6,ROW(RR_Ciclo)/((RR_Ciclo=cicloCorrente)*(RR_Movimento<>"")),{k}),"")'


def _rr(colonna, appoggio, testo=True):
    return _cella_tab("tblRegister", "RiskRegister", colonna, appoggio, testo)


def _ix(colonna, appoggio):
    """INDEX della colonna di tblRegister alla riga di appoggio (senza il controllo del vuoto)."""
    l = lettera("tblRegister", colonna)
    return f"INDEX(RiskRegister!${l}:${l},{appoggio})"


def _nomi_driver(cella):
    """'DRV-AI, DRV-CYB' -> 'Intelligenza artificiale, Cyber', dalla tabella dei driver di Parametri."""
    out = cella
    for i in range(1, len(DRIVER) + 1):
        out = f"SUBSTITUTE({out},INDEX(codiciDriver,{i}),INDEX(nomiDriver,{i}))"
    return "=" + out


def _intestazione(ws, riga, colonne):
    for col, testo in colonne:
        c = ws[f"{col}{riga}"]
        c.value, c.font, c.fill = testo, Font(size=9, bold=True, color="FFFFFF"), fill(BLU_NOTTE)
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    ws.row_dimensions[riga].height = 28


def _colora_movimento(ws, area):
    """Entrato nel radar in blu, uscito in lilla."""
    c = area.split(":")[0]
    for testo, fondo, colore in (("Entrato", BLU_CHIARO, BLU_NOTTE), ("Uscito", FONDO_OSSERVAZIONE, TESTO_OSSERVAZIONE)):
        ws.conditional_formatting.add(area, FormulaRule(formula=[f'LEFT({c},{len(testo)})="{testo}"'], fill=fill(fondo),
                                                         font=Font(bold=True, color=colore)))


def _dimensioni(a):
    """'Imp · Prob · Pross · Vel' di un rischio alla riga di appoggio a (Velocity non valutata = —)."""
    vel = _ix("Velocity", a)
    return (f'=IF({a}="","",{_ix("Impatto", a)}&" · "&{_ix("Probabilita", a)}&" · "&{_ix("Prossimita", a)}'
            f'&" · "&IF({vel}="","—",{vel}))')


def foglio_osservazione(wb):
    """Foglio di lavoro: rischi in osservazione del ciclo corrente con tutti i testi, entrati e usciti dal radar,
    concentrazione per driver e categoria accanto a quella dei rischi del radar."""
    ws = wb["Osservazione"]
    titolo(ws, "Rischi in osservazione", 14)
    larghezze = [8, 30, 10, 16, 6, 6, 6, 6, 7, 36, 8, 40, 44, 11]
    for j, w in enumerate(larghezze, start=1):
        ws.column_dimensions[get_column_letter(j)].width = w
    ws.column_dimensions["AF"].hidden = True
    sezione(ws, 4, 1, 14, "Rischi in osservazione nel ciclo corrente (fuori dal radar: niente KRI ne' azioni), dallo "
                          "score piu' alto")
    _intestazione(ws, 5, list(zip("ABCDEFGHIJKLMN", ["ID", "Rischio", "Categoria", "Driver", "Imp.", "Prob.", "Pross.",
                                                       "Vel.", "Score", "Perché fuori dal radar (regola, D-79)",
                                                       "Orizz. (anni)", "Segnale che lo porterebbe nel radar",
                                                       "Meccanismo (descrizione)", "Validazione"])))
    campi = [("ID_Rischio", True), ("Nome", True), ("Event_Type", True), ("Driver", True), ("Impatto", False),
             ("Probabilita", False), ("Prossimita", False), ("Velocity", False), ("Score_Composito", False),
             ("Motivo_Stato", True), ("Orizzonte_Anni", False), ("Segnale_Avvicinamento", True), ("Descrizione", True),
             ("Validazione", True)]
    prima, ultima = 6, 5 + MAX_OSSERVAZIONE
    for k in range(1, MAX_OSSERVAZIONE + 1):
        r = 5 + k
        ws[f"AF{r}"] = _riga_ordine(k)
        for j, (col, testo) in enumerate(campi, start=1):
            c = ws.cell(row=r, column=j, value=_rr(col, f"$AF{r}", testo))
            c.font = Font(size=9, bold=j == 1, color=BLU_NOTTE if j == 1 else "262626")
            c.alignment = Alignment(wrap_text=True, vertical="top",
                                    horizontal="center" if j in (1, 3, 5, 6, 7, 8, 9, 11, 14) else "left")
            c.border = BORDO_SOTTILE
        ws[f"I{r}"].number_format = "0.00"
        ws.row_dimensions[r].height = 45
    finestra_a3 = 'NW_Settimana,">="&inizioFinestra4,NW_Settimana,"<="&settimanaCorrente'
    _intestazione(ws, 5, [("O", "Notizie di A3 (4 sett.)")])
    ws.column_dimensions["O"].width = 9
    for r in range(prima, ultima + 1):
        ws[f"O{r}"] = f'=IF($A{r}="","",COUNTIFS(NW_Rischio_ID,$A{r},{finestra_a3}))'
        ws[f"O{r}"].alignment, ws[f"O{r}"].border = Alignment(horizontal="center", vertical="top"), BORDO_SOTTILE
    ws.conditional_formatting.add(f"O{prima}:O{ultima}", FormulaRule(formula=[f'AND(ISNUMBER(O{prima}),O{prima}>0)'],
                                                                     fill=fill(AMBRA_TENUE), font=Font(bold=True)))
    colora_dimensioni(ws, f"E{prima}:H{ultima}", f"E{prima}")
    r = ultima + 2
    sezione(ws, r, 1, 14, "Entrati e usciti dal radar nel ciclo corrente (colonna Movimento del RiskRegister)")
    _intestazione(ws, r + 1, list(zip("ABCDEFGHIJ", ["ID", "Rischio", "Movimento", "Stato ora", "Imp.", "Prob.",
                                                   "Pross.", "Vel.", "Score", "Motivo (regola, D-79)"])))
    ws.merge_cells(start_row=r + 1, start_column=10, end_row=r + 1, end_column=14)
    campi_m = [("ID_Rischio", True), ("Nome", True), ("Movimento", True), ("Stato", True), ("Impatto", False),
               ("Probabilita", False), ("Prossimita", False), ("Velocity", False), ("Score_Composito", False),
               ("Motivo_Stato", True)]
    prima_m = r + 2
    for k in range(1, 11):
        rr = prima_m + k - 1
        ws[f"AF{rr}"] = _riga_movimento(k)
        for j, (col, testo) in enumerate(campi_m, start=1):
            c = ws.cell(row=rr, column=j, value=_rr(col, f"$AF{rr}", testo))
            c.font = Font(size=9, bold=j == 1)
            c.alignment = Alignment(wrap_text=True, vertical="top", horizontal="center" if 3 <= j <= 9 else "left")
            c.border = BORDO_SOTTILE
        ws[f"I{rr}"].number_format = "0.00"
        ws.merge_cells(start_row=rr, start_column=10, end_row=rr, end_column=14)
        ws.row_dimensions[rr].height = 30
    _colora_movimento(ws, f"C{prima_m}:C{prima_m + 9}")
    fine_lista = prima_m + 9

    # Concentrazione: driver (righe) x categoria (colonne), rischi in osservazione e rischi del radar.
    P0 = 16                                            # colonna P
    N = len(TASSONOMIA)
    for j in range(P0, P0 + N + 2):
        ws.column_dimensions[get_column_letter(j)].width = 22 if j == P0 else 8
    L = lambda j: get_column_letter(j)
    blocchi = [(4, "Dove si concentrano i rischi in osservazione (driver x categoria)",
                lambda et, drv: f'COUNTIFS(RR_Ciclo,cicloCorrente,RR_Stato,"Osservazione",RR_Event_Type,{et},'
                                f'RR_Driver,"*"&{drv}&"*")'),
               (8 + len(DRIVER), "Rischi del radar con lo stesso incrocio (anagrafica)",
                lambda et, drv: f'COUNTIFS(ANA_Event_Type,{et},ANA_Driver,"*"&{drv}&"*")')]
    for riga0, testo, conta in blocchi:
        sezione(ws, riga0, P0, P0 + N + 1, testo)
        _intestazione(ws, riga0 + 1, [(L(P0), "Driver")] + [(L(P0 + 1 + i), cod) for i, (cod, _) in enumerate(TASSONOMIA)]
                      + [(L(P0 + N + 1), "Totale")])
        for i, (cod, _) in enumerate(DRIVER):
            rr = riga0 + 2 + i
            ws[f"{L(P0)}{rr}"] = f"=INDEX(nomiDriver,{i + 1})"
            ws[f"{L(P0)}{rr}"].font = Font(size=9, bold=True)
            for e in range(len(TASSONOMIA)):
                c = ws[f"{L(P0 + 1 + e)}{rr}"]
                c.value = f'=IF({conta(f"{L(P0 + 1 + e)}${riga0 + 1}", f"INDEX(codiciDriver,{i + 1})")}=0,"",' \
                          f'{conta(f"{L(P0 + 1 + e)}${riga0 + 1}", f"INDEX(codiciDriver,{i + 1})")})'
                c.alignment, c.border, c.font = Alignment(horizontal="center"), BORDO_SOTTILE, Font(size=10, bold=True)
            ws[f"{L(P0 + N + 1)}{rr}"] = f"=SUM({L(P0 + 1)}{rr}:{L(P0 + N)}{rr})"
            ws[f"{L(P0 + N + 1)}{rr}"].alignment = Alignment(horizontal="center")
        area = f"{L(P0 + 1)}{riga0 + 2}:{L(P0 + N)}{riga0 + 1 + len(DRIVER)}"
        for soglia, colore in ((3, "F4B183"), (2, "F8CBAD"), (1, "FCE4D6")):
            ws.conditional_formatting.add(area, FormulaRule(formula=[f'AND(ISNUMBER({L(P0 + 1)}{riga0 + 2}),'
                                                                     f'{L(P0 + 1)}{riga0 + 2}>={soglia})'], fill=fill(colore)))
    nota = 9 + 2 * len(DRIVER) + 2
    ws.merge_cells(start_row=nota, start_column=P0, end_row=nota + 2, end_column=P0 + N + 1)
    c = ws.cell(row=nota, column=P0, value="Un rischio con piu' driver conta in ogni driver. Una casella piena sopra e "
                                           "vuota sotto e' un tema che il radar non gestisce: il registro lo osserva. "
                                           "Codici delle categorie: foglio Parametri (tassonomia interna).")
    c.font, c.alignment = Font(size=8, italic=True, color=TESTO_TENUE), Alignment(wrap_text=True, vertical="top")
    legenda(ws, fine_lista + 2, 14, "Registro unico (D-79): stessa scala e stesso score dei rischi del radar. Un rischio "
                                    "entra nel radar se Prossimita e Probabilita raggiungono le soglie di Parametri (righe "
                                    "65-75) e c'e' posto, o per eccezione (AGIRE ORA, tema del supervisore, decisione del "
                                    "validatore); esce dopo due cicli sotto la regola. Orizz. = anni stimati da A1 prima che "
                                    "possa manifestarsi. Storia completa: foglio RiskRegister (colonne Stato, Motivo_Stato, "
                                    "Movimento).")
    ws.freeze_panes = "C6"


def foglio_fenomeni(wb):
    """Pagina del report: i rischi in osservazione in forma compatta e chi e' entrato o uscito dal radar nel ciclo."""
    ws = wb["Fenomeni"]
    titolo(ws, "Rischi in osservazione", 11)
    for l, w in zip("ABCDEFGHIJK", [4, 8, 30, 18, 12, 7, 34, 9, 38, 16, 9]):
        ws.column_dimensions[l].width = w
    ws.column_dimensions["L"].hidden = True
    conta = lambda *crit: "COUNTIFS(RR_Ciclo,cicloCorrente" + "".join(f',{a},"{b}"' for a, b in crit) + ")"
    ws.merge_cells("A4:K4")
    ws["A4"] = (f'=IF(cicloCorrente="","","Registro unico: nel radar "&COUNTIF(ANA_ID,"NFR-*")&" rischi (capienza "&capienzaRadar'
                f'&"), in osservazione "&{conta(("RR_Stato", "Osservazione"))}&" (al massimo {MAX_OSSERVAZIONE}) · nel '
                f'ciclo: entrati nel radar "&{conta(("RR_Movimento", "Entrato"))}&", usciti "'
                f'&{conta(("RR_Movimento", "Uscito"))}&", in uscita "&{conta(("RR_Stato", "Radar, in uscita"))}&".")')
    ws["A4"].font = Font(bold=True, size=11, color=BLU_NOTTE)
    ws["A4"].alignment = Alignment(vertical="center", indent=1)
    ws.row_dimensions[4].height = 20
    _intestazione(ws, 6, list(zip("ABCDEFGHIJ", ["#", "ID", "Rischio", "Categoria", "Imp · Prob · Pross · Vel",
                                                   "Score", "Perché fuori dal radar", "Orizzonte",
                                                   "Segnale che lo porterebbe nel radar", "Driver"]))
                  + [("K", "Notizie A3 (4 sett.)")])
    prima, ultima = 7, 6 + MAX_OSSERVAZIONE
    for k in range(1, MAX_OSSERVAZIONE + 1):
        r = 6 + k
        a = f"$L{r}"
        ws[f"L{r}"] = _riga_ordine(k)
        ws[f"A{r}"] = f'=IF({a}="","",{k})'
        ws[f"B{r}"] = _rr("ID_Rischio", a)
        ws[f"C{r}"] = _rr("Nome", a)
        et = _ix("Event_Type", a)
        ws[f"D{r}"] = f'=IF({a}="","",{et}&" "&IFERROR(INDEX(nomiL1,MATCH({et},codiciL1,0)),""))'
        ws[f"E{r}"] = _dimensioni(a)
        ws[f"F{r}"] = _rr("Score_Composito", a, False)
        ws[f"F{r}"].number_format = "0.00"
        ws[f"G{r}"] = _rr("Motivo_Stato", a)
        ws[f"H{r}"] = f'=IF({a}="","",IF({_ix("Orizzonte_Anni", a)}="","—",{_ix("Orizzonte_Anni", a)}&" anni"))'
        ws[f"I{r}"] = _rr("Segnale_Avvicinamento", a)
        ws[f"J{r}"] = _nomi_driver(_rr("Driver", a)[1:])
        ws[f"K{r}"] = (f'=IF({a}="","",COUNTIFS(NW_Rischio_ID,{_ix("ID_Rischio", a)},'
                       f'NW_Settimana,">="&inizioFinestra4,NW_Settimana,"<="&settimanaCorrente))')
        for x in "ABCDEFGHIJK":
            c = ws[f"{x}{r}"]
            c.font = Font(size=9, bold=x == "B", color=BLU_NOTTE if x == "B" else "262626")
            c.alignment = Alignment(wrap_text=True, vertical="top", horizontal="center" if x in "AEFHK" else "left")
            c.border = BORDO_SOTTILE
        ws.row_dimensions[r].height = 3
    nome_definito(wb, "fenomeniLista", f"'Fenomeni'!$A${prima}:$K${ultima}")
    r = ultima + 2
    sezione(ws, r, 1, 11, "Entrati e usciti dal radar in questo ciclo")
    _intestazione(ws, r + 1, [("B", "ID"), ("C", "Rischio"), ("D", "Movimento"), ("E", "Motivo (regola, D-79)")])
    ws.merge_cells(start_row=r + 1, start_column=5, end_row=r + 1, end_column=11)
    prima_u = r + 2
    for k in range(1, 7):
        rr = prima_u + k - 1
        a = f"$L{rr}"
        ws[f"L{rr}"] = _riga_movimento(k)
        ws[f"B{rr}"] = _rr("ID_Rischio", a)
        ws[f"C{rr}"] = _rr("Nome", a)
        ws[f"D{rr}"] = _rr("Movimento", a)
        ws[f"E{rr}"] = _rr("Motivo_Stato", a)
        ws.merge_cells(start_row=rr, start_column=5, end_row=rr, end_column=11)
        for x in "BCDE":
            ws[f"{x}{rr}"].font = Font(size=9, bold=x == "B")
            ws[f"{x}{rr}"].alignment = Alignment(wrap_text=True, vertical="top")
            ws[f"{x}{rr}"].border = BORDO_SOTTILE
        ws.row_dimensions[rr].height = 3
    nome_definito(wb, "fenomeniUscite", f"'Fenomeni'!$A${prima_u}:$K${prima_u + 5}")
    _colora_movimento(ws, f"D{prima_u}:D{prima_u + 5}")
    fine = prima_u + 7
    legenda(ws, fine, 11, "Registro unico (D-79): tutti i rischi hanno la stessa scala (Impatto, Probabilita, Prossimita, "
                          "Velocity; — = non valutata) e lo stesso score; nel radar di Mosca entrano quelli con Prossimita "
                          "e Probabilita alle soglie di Parametri, fino alla capienza, piu' le eccezioni (AGIRE ORA, tema "
                          "del supervisore, decisione del validatore). Gli altri restano qui, senza KRI ne' azioni, con "
                          "l'orizzonte stimato e il segnale che li porterebbe nel radar. Notizie A3 = notizie delle ultime "
                          "4 settimane collegate al rischio (foglio Notizie).")
    imposta_stampa(ws, f"A1:K{fine}")
# ---------------------------------------------------------------- Validazione (griglia di lavoro, D-67)
# Una riga per oggetto: accanto a ogni proposta (grigia) il valore giallo, gia' compilato con la proposta. Sezioni a
# capienza fissa, una sotto l'altra: lo script scrive le righe dei periodi da validare e nasconde le altre (nel
# template tutto e' validato, quindi la griglia e' vuota). Lo script legge e scrive SOLO con i nomi definiti
# VG_<oggetto>_<campo> (valore), VG_<oggetto>_<campo>_P (proposta), _ID, _Nome, _Motivazione, _Respingi, _Periodo,
# _Appoggio, _Tipo (KRI), _Settimana (notizie), _righe (tutta la sezione), _titolo: le lettere stanno solo qui.
MAX_KRI_GRIGLIA = 80          # KRI del ciclo, anche quelli che escono di vigore (20 rischi x 2 + i terzi KRI di prima)
MAX_AZIONI_GRIGLIA = 100      # fino a 5 azioni per rischio (schema A1) x 20 rischi
MAX_NOTIZIE_GRIGLIA = 200     # notizie delle settimane non ancora validate; oltre, il settimanale si ferma
G_SEGN = "P"                  # D-71: segnalazioni di A5 e dei controlli sul rischio (solo la sezione Rischi)
# D-79 (solo Rischi): dopo le colonne nascoste, lo stato calcolato con il motivo e la decisione del validatore sullo
# stato (proposta grigia = la decisione in vigore, Automatico se nessuna).
G_STATO, G_DEC_P, G_DEC = "W", "X", "Y"
GRIGLIA = {
    # oggetto: (titolo, capienza, intestazioni di ID e Nome, {campo: (colonna proposta, colonna valore, etichetta)},
    #           colonna Respingi, {colonna extra: (lettera, intestazione)})
    "Rischio": ("RISCHI", MAX_RISCHI, ("ID", "Rischio"),
                {"Impatto": ("C", "D", "Imp."), "Velocity": ("I", "J", "Vel."), "Prossimita": ("G", "H", "Pross."),
                 "Probabilita": ("E", "F", "Prob."), "Anni_Adeguamento": ("K", "L", "Anni adeg."),
                 "Decisione_Stato": (G_DEC_P, G_DEC, "Decisione sullo stato")}, None,
                {"Segnalazioni": (G_SEGN, "Segnalazioni dei controlli (script e A5, se usato): ⚑ DA MOTIVARE = "
                                          "Motivazione obbligatoria"),
                 "Stato": (G_STATO, "Stato nel registro unico (calcolato con la regola, D-79)")}),
    "KRI": ("KRI", MAX_KRI_GRIGLIA, ("KRI", "Indicatore"),
            {"Valore_Corrente": ("D", "E", "Valore"), "Soglia_Attenzione": ("F", "G", "Soglia att."),
             "Soglia_Allerta": ("H", "I", "Soglia all.")}, "J", {"Tipo": ("C", "Tipo")}),
    "Azione": ("AZIONI", MAX_AZIONI_GRIGLIA, ("Azione", "Descrizione"),
               {"Owner": ("C", "E", "Owner"), "Orizzonte": ("G", "H", "Orizzonte")}, "I", {}),
    "Notizia": ("NOTIZIE", MAX_NOTIZIE_GRIGLIA, ("Notizia", "Titolo"),
                {"Rischio_ID": ("C", "E", "Rischio"), "Segnale": ("G", "H", "Segnale")}, "I",
                {"Settimana": ("J", "Settimana")}),
}
UNITE = {"Azione", "Notizia"}          # proposta e valore su due colonne unite (C:D, E:F): owner e rischio sono testi lunghi
G_MOT, G_SCORE, G_MARG = "M", "N", "O"
# Colonna P (solo Rischi, D-71): segnalazioni di A5 e dei controlli, scritte dallo script; sopra, nella riga del titolo,
# quelle sul ciclo (VG_Rischio_SegnalazioniCiclo).
# Colonne nascoste: Q periodo, R appoggio (Rischio: 1 = segnalazione da motivare; Azione: rischio dell'azione),
# S e T (Rischio: margine con i valori gialli e con le proposte; Azione: mesi dell'orizzonte giallo, 0 se respinta, e
# proposto), U e V (Rischio: score con i valori gialli e con le proposte).
G_PERIODO, G_APPOGGIO = "Q", "R"
GRIGIO_PROPOSTA, ARANCIO_CAMBIO, ROSSO_MOTIVAZIONE = "F2F2F2", "F8CBAD", "F4B183"
NOTA_GRIGLIA = ("Lo stato di ogni riga (da decidere, applicata), chi ha validato e quando e, per ogni valore, la proposta e il "
                "valore deciso li registra il comando valida nel foglio dati Storico_Validazioni: non si scrive a mano.")


def _score_griglia(r, imp, prob, pross, vel):
    """Formula Score_Composito della mappa (D-50) sulle colonne date della riga r."""
    i, p, x, v = (f"${c}{r}" for c in (imp, prob, pross, vel))
    return (f'IF(COUNT({i},{p},{x})<3,"",ROUND((pesoImpatto*{i}+pesoProbabilita*{p}+pesoProssimita*{x}'
            f'+IF(ISNUMBER({v}),pesoVelocity*{v},0))/(pesoImpatto+pesoProbabilita+pesoProssimita'
            f'+IF(ISNUMBER({v}),pesoVelocity,0)),2))')


def _margine_griglia(r, pross, anni, mesi, azioni):
    """Margine di Mosca del Radar_Mosca sulla riga r: Z dalla Prossimita, X costante, Y = orizzonte piu' lungo delle
    azioni della griglia non respinte (riserva se nessuna) o, se maggiori, gli anni di adeguamento (vuoti: quelli
    gia' in anagrafica, che valida non cancella)."""
    a_r, a_p = azioni
    return (f'IF(NOT(ISNUMBER(${pross}{r})),"",INDEX(anniProssimita,${pross}{r})-(moscaX+MAX(IF(COUNTIFS({a_r},$A{r},'
            f'{a_p},${G_PERIODO}{r},{mesi},">0")=0,moscaYDefault,_xlfn.MAXIFS({mesi},{a_r},$A{r},{a_p},${G_PERIODO}{r})/12),'
            f'IF(ISNUMBER(${anni}{r}),${anni}{r},IFERROR(N(INDEX(ANA_Anni_Adeguamento,MATCH($A{r},ANA_ID,0))),0)))))')


def foglio_validazione(wb):
    """Griglia di lavoro del validatore (D-67): sezioni Rischi, KRI, Azioni, Notizie una sotto l'altra."""
    ws = wb["Validazione"]
    oggetti = MAPPA["validazione"]["oggetti"]
    if list(GRIGLIA) != list(oggetti) or any(sorted(GRIGLIA[o][3]) != sorted(oggetti[o]["campi"]) for o in oggetti):
        raise SystemExit("GRIGLIA (genera_dashboard.py) e la sezione validazione della mappa devono avere gli stessi oggetti e campi")
    titolo(ws, "Validazione: una riga per rischio (nel radar o in osservazione), KRI, azione e notizia", 15)
    for j, w in enumerate([16, 42, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 46, 15, 25, 60, 12, 12, 10, 10, 10, 10, 36, 13, 15],
                          start=1):
        ws.column_dimensions[get_column_letter(j)].width = w
    for l in "QRSTUV":
        ws.column_dimensions[l].hidden = True
    fondo, colore, _ = PROCESSI["validazione"]
    ws.merge_cells("A3:O3")
    ws["A3"] = "Niente da validare: tutte le proposte degli agenti sono state decise (dettaglio nel foglio Storico_Validazioni)."
    ws["A3"].font = Font(bold=True, color=colore)
    ws["A3"].alignment = Alignment(vertical="center", indent=1)
    for x in range(1, 16):
        ws.cell(row=3, column=x).fill = fill(fondo)
    ws.row_dimensions[3].height = 22
    nome_definito(wb, "valStato", "'Validazione'!$A$3")
    ass_v = lambda col, da, a: f"'Validazione'!${col}${da}:${col}${a}"
    sottile = Border(bottom=Side(style="thin", color="D9D9D9"))
    centro = Alignment(horizontal="center", vertical="center", wrap_text=True)
    r = 5
    posizioni = {}
    for oggetto, (titolo_s, capienza, (int_id, int_nome), campi, respingi, extra) in GRIGLIA.items():
        ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=15)
        c = ws.cell(row=r, column=1, value=f"{titolo_s} — nessuna riga da validare")
        c.font = Font(bold=True, size=12, color=BLU_NOTTE)
        for x in range(1, 16):
            ws.cell(row=r, column=x).border = Border(bottom=Side(style="medium", color=BLU_NOTTE))
        nome_definito(wb, f"VG_{oggetto}_titolo", f"'Validazione'!$A${r}")
        if oggetto == "Rischio":                       # D-71: segnalazioni sul ciclo, sopra la colonna dei rischi
            c = ws[f"{G_SEGN}{r}"]
            c.font, c.alignment = Font(size=8, italic=True, color=BLU_NOTTE), Alignment(wrap_text=True, vertical="center")
            nome_definito(wb, "VG_Rischio_SegnalazioniCiclo", f"'Validazione'!${G_SEGN}${r}")
        r += 1
        # Intestazione: grigio la proposta, giallo il valore e la motivazione, azzurro i calcolati.
        intest = {"A": (int_id, "info"), "B": (int_nome, "info"),
                  G_MOT: ("Motivazione (se cambi un valore" + (" o respingi)" if respingi else ")"), "val")}
        for campo, (cp, cv, et) in campi.items():
            intest[cp] = ("Decisione in vigore" if campo == "Decisione_Stato" else f"{et} proposto", "prop")
            intest[cv] = ("Owner (una funzione)" if campo == "Owner" else
                          "Decisione sullo stato (Automatico = la regola)" if campo == "Decisione_Stato" else et, "val")
        if respingi:
            intest[respingi] = ("Respingi", "val")
        for col, et in extra.values():
            intest[col] = (et, "info")
        if oggetto == "Rischio":
            intest[G_SCORE] = ("Score composito (calcolato)", "calc")
            intest[G_MARG] = ("Margine di Mosca Z−(X+Y), anni (calcolato)", "calc")
        colori = {"prop": GRIGIO_PROPOSTA, "val": "FFE699", "info": "D9E1F2", "calc": "DDEBF7"}
        for col, (testo, tipo) in intest.items():
            c = ws[f"{col}{r}"]
            c.value, c.font, c.fill, c.alignment = testo, Font(bold=True, size=9), fill(colori[tipo]), centro
        if oggetto in UNITE:
            ws.merge_cells(f"C{r}:D{r}")
            ws.merge_cells(f"E{r}:F{r}")
        ws.row_dimensions[r].height = 30
        r += 1
        prima, ultima = r, r + capienza - 1
        posizioni[oggetto] = (prima, ultima)
        for i in range(prima, ultima + 1):
            ws[f"A{i}"].font = Font(bold=True, color=BLU_NOTTE, size=10 if oggetto in ("Rischio", "KRI") else 9)
            ws[f"A{i}"].alignment = Alignment(vertical="center")
            ws[f"B{i}"].font = Font(size=9)
            ws[f"B{i}"].alignment = Alignment(wrap_text=True, vertical="center")
            for cp, cv, _ in campi.values():
                ws[f"{cp}{i}"].font, ws[f"{cp}{i}"].fill, ws[f"{cp}{i}"].alignment = Font(size=9, color="7F7F7F"), fill(GRIGIO_PROPOSTA), centro
                ws[f"{cv}{i}"].font, ws[f"{cv}{i}"].fill, ws[f"{cv}{i}"].alignment = Font(size=10, bold=True), fill("FFF2CC"), centro
            if respingi:
                ws[f"{respingi}{i}"].fill, ws[f"{respingi}{i}"].alignment = fill("FFF2CC"), centro
            for col, _ in extra.values():
                ws[f"{col}{i}"].font, ws[f"{col}{i}"].alignment = Font(size=9), centro
            if oggetto == "Rischio":
                ws[f"{G_SEGN}{i}"].font = Font(size=8)
                ws[f"{G_SEGN}{i}"].alignment = Alignment(wrap_text=True, vertical="center")
                ws[f"{G_STATO}{i}"].font = Font(size=8)
                ws[f"{G_STATO}{i}"].alignment = Alignment(wrap_text=True, vertical="center")
                for x in (G_STATO, G_DEC_P, G_DEC):
                    ws[f"{x}{i}"].border = sottile
            ws[f"{G_MOT}{i}"].font, ws[f"{G_MOT}{i}"].fill = Font(size=9), fill("FFF2CC")
            ws[f"{G_MOT}{i}"].alignment = Alignment(wrap_text=True, vertical="center")
            for x in range(1, 17 if oggetto == "Rischio" else 16):
                ws.cell(row=i, column=x).border = sottile
            if oggetto in UNITE:
                ws.merge_cells(f"C{i}:D{i}")
                ws.merge_cells(f"E{i}:F{i}")
            ws.row_dimensions[i].height = 30
            ws.row_dimensions[i].hidden = True             # nel template non c'e' niente da validare
        # Nomi definiti: le sole cose che lo script conosce della griglia.
        for nome, col in [("ID", "A"), ("Nome", "B"), ("Motivazione", G_MOT), ("Periodo", G_PERIODO), ("Appoggio", G_APPOGGIO)] + \
                         ([("Respingi", respingi)] if respingi else []) + [(n, col) for n, (col, _) in extra.items()] + \
                         [(f"{campo}_P", cp) for campo, (cp, _, _) in campi.items()] + [(campo, cv) for campo, (_, cv, _) in campi.items()]:
            nome_definito(wb, f"VG_{oggetto}_{nome}", ass_v(col, prima, ultima))
        nome_definito(wb, f"VG_{oggetto}_righe", f"'Validazione'!$A${prima}:$V${ultima}")
        # Cella gialla diversa dalla proposta: arancio. Motivazione mancante con un cambio, un respingimento o un rilievo
        # di A5 superato (appoggio = 1): rossa.
        diverse = []
        for cp, cv, _ in campi.values():
            p, v = f"${cp}{prima}", f"{cv}{prima}"
            rng = f"{cv}{prima}:{cv}{ultima}"
            ws.conditional_formatting.add(rng, FormulaRule(formula=[f'AND({p}<>"n.v.",{p}<>"—",{v}<>{p})'], fill=fill(ARANCIO_CAMBIO)))
            ws.conditional_formatting.add(rng, FormulaRule(formula=[f'AND(OR({p}="n.v.",{p}="—"),{v}<>"")'], fill=fill(ARANCIO_CAMBIO)))
            diverse.append(f'IF(OR({p}="n.v.",{p}="—"),${cv}{prima}<>"",${cv}{prima}<>{p})')
        if respingi:
            sr = f"${respingi}{prima}"
            diverse.append(f'OR({sr}="Sì",{sr}="Si")')
            ws.conditional_formatting.add(f"{respingi}{prima}:{respingi}{ultima}",
                                          FormulaRule(formula=[f'OR({sr}="Sì",{sr}="Si")'], fill=fill("F8CBAD"), font=Font(bold=True)))
        if oggetto == "Rischio":
            diverse.append(f"${G_APPOGGIO}{prima}=1")
            segn = f"{G_SEGN}{prima}"
            ws.conditional_formatting.add(f"{G_SEGN}{prima}:{G_SEGN}{ultima}", FormulaRule(
                formula=[f'ISNUMBER(SEARCH("DA MOTIVARE",{segn}))'], fill=fill("FCE4D6")))
        m = f"{G_MOT}{prima}"
        ws.conditional_formatting.add(f"{G_MOT}{prima}:{G_MOT}{ultima}", FormulaRule(
            formula=[f'AND($A{prima}<>"",OR({",".join(diverse)}),LEN({m})<10)'], fill=fill(ROSSO_MOTIVAZIONE)))
        # Convalide: le stesse regole che controlla valida (che resta il controllo vero).
        if oggetto == "Rischio":
            dv = DataValidation(type="whole", operator="between", formula1="1", formula2="5", allow_blank=True,
                                error="Un intero da 1 a 5 (la Velocity puo' restare vuota = non valutata).", showErrorMessage=True)
            for campo in ("Impatto", "Probabilita", "Prossimita", "Velocity"):
                dv.add(f"{campi[campo][1]}{prima}:{campi[campo][1]}{ultima}")
            ws.add_data_validation(dv)
            dv = DataValidation(type="decimal", operator="between", formula1="0", formula2="30", allow_blank=True,
                                error="Anni di adeguamento: un numero da 0 a 30, oppure vuoto.", showErrorMessage=True)
            dv.add(f"{campi['Anni_Adeguamento'][1]}{prima}:{campi['Anni_Adeguamento'][1]}{ultima}")
            ws.add_data_validation(dv)
        if respingi:
            convalida_lista(ws, f"{respingi}{prima}:{respingi}{ultima}", "Sì")
        if oggetto == "Azione":
            convalida_lista(ws, f"H{prima}:H{ultima}", "3 mesi,6 mesi,12 mesi")
        if oggetto == "Rischio":                       # D-79
            convalida_lista(ws, f"{G_DEC}{prima}:{G_DEC}{ultima}", ",".join(DECISIONI_STATO))
            st = f"{G_STATO}{prima}"
            for testo, fondo, colore in (("Osservazione", FONDO_OSSERVAZIONE, TESTO_OSSERVAZIONE),
                                         ("Radar, in uscita", AMBRA_TENUE, "7F6000")):
                ws.conditional_formatting.add(f"{G_STATO}{prima}:{G_STATO}{ultima}", FormulaRule(
                    formula=[f'LEFT({st},{len(testo)})="{testo}"'], fill=fill(fondo), font=Font(size=8, bold=True, color=colore)))
        if oggetto == "Notizia":
            convalida_lista(ws, f"H{prima}:H{ultima}", ",".join(SEGNALI))
        r = ultima + 2

    # Appoggio delle azioni: mesi dell'orizzonte giallo (0 se respinta) e di quello proposto: la Y di Mosca.
    pa, ua = posizioni["Azione"]
    for i in range(pa, ua + 1):
        ws[f"S{i}"] = f'=IF($A{i}="","",IF(OR($I{i}="Sì",$I{i}="Si"),0,IFERROR(VALUE(LEFT($H{i},FIND(" ",$H{i})-1)),0)))'
        ws[f"T{i}"] = f'=IF($A{i}="","",IFERROR(VALUE(LEFT($G{i},FIND(" ",$G{i})-1)),0))'
    azioni = (f"${G_APPOGGIO}${pa}:${G_APPOGGIO}${ua}", f"${G_PERIODO}${pa}:${G_PERIODO}${ua}")
    nome_definito(wb, "VG_Azione_Mesi", ass_v("S", pa, ua))
    # Score e margine dei rischi con i valori gialli e con le sole proposte; IFERROR: un valore sbagliato scritto nella
    # griglia non deve mai produrre un errore di formula (fermerebbe ogni scrittura del registro, trappola 70).
    pr, ur = posizioni["Rischio"]
    for i in range(pr, ur + 1):
        ws[f"U{i}"] = f'=IFERROR({_score_griglia(i, "D", "F", "H", "J")},"")'
        ws[f"V{i}"] = f'=IFERROR({_score_griglia(i, "C", "E", "G", "I")},"")'
        ws[f"S{i}"] = f'=IFERROR({_margine_griglia(i, "H", "L", f"$S${pa}:$S${ua}", azioni)},"")'
        ws[f"T{i}"] = f'=IFERROR({_margine_griglia(i, "G", "K", f"$T${pa}:$T${ua}", azioni)},"")'
        ws[f"{G_SCORE}{i}"] = (f'=IF(NOT(ISNUMBER($U{i})),"",FIXED($U{i},2)&IF(AND(ISNUMBER($V{i}),$V{i}<>$U{i}),'
                               f'"  (era "&FIXED($V{i},2)&")",""))')
        ws[f"{G_MARG}{i}"] = (f'=IF(NOT(ISNUMBER($S{i})),"",IF($S{i}<0,"AGIRE ORA",IF($S{i}<1,"Entro l\'anno","Margine"))'
                              f'&" · "&FIXED($S{i},2)&IF(AND(ISNUMBER($T{i}),ROUND($T{i},2)<>ROUND($S{i},2)),'
                              f'"  (era "&FIXED($T{i},2)&")",""))')
        ws[f"{G_SCORE}{i}"].font = Font(size=10, bold=True)
        ws[f"{G_MARG}{i}"].font = Font(size=9.5, bold=True)
        ws[f"{G_SCORE}{i}"].alignment = ws[f"{G_MARG}{i}"].alignment = centro
    for nome, col in (("Score", G_SCORE), ("Margine", G_MARG), ("ScoreNum", "U"), ("MargineNum", "S")):
        nome_definito(wb, f"VG_Rischio_{nome}", ass_v(col, pr, ur))
    marg = f"{G_MARG}{pr}:{G_MARG}{ur}"
    ws.conditional_formatting.add(marg, FormulaRule(formula=[f'LEFT({G_MARG}{pr},9)="AGIRE ORA"'], fill=fill(ROSSO),
                                                    font=Font(bold=True, color="FFFFFF")))
    ws.conditional_formatting.add(marg, FormulaRule(formula=[f'LEFT({G_MARG}{pr},5)="Entro"'], fill=fill(AMBRA), font=Font(bold=True)))
    ws.conditional_formatting.add(marg, FormulaRule(formula=[f'LEFT({G_MARG}{pr},7)="Margine"'], fill=fill("C6EFCE"),
                                                    font=Font(bold=True, color="006100")))
    ws.conditional_formatting.add(f"{G_SCORE}{pr}:{G_SCORE}{ur}",
                                  FormulaRule(formula=[f'ISNUMBER(SEARCH("(era",{G_SCORE}{pr}))'], fill=fill(ARANCIO_CAMBIO)))
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=15)
    ws.cell(row=r, column=1, value=NOTA_GRIGLIA).font = Font(size=8, italic=True, color=TESTO_TENUE)
    ws.cell(row=r, column=1).alignment = Alignment(wrap_text=True)
    ws.row_dimensions[r].height = 24
    imposta_stampa(ws, f"A1:O{r}")


# ---------------------------------------------------------------- Dizionario dei dati
CHI_TESTO = {"A1": "A1, ciclo trimestrale; validato", "A3": "A3, ciclo settimanale", "A5": "A5, ciclo trimestrale",
             "script": "Script, quando scrive il ciclo", "formula": "Formula del foglio",
             "validazione": "Comando valida, dalla decisione del validatore", "validatore": "Validatore, a mano"}
COME = {
    "Score_Composito": "Media pesata delle dimensioni valutate con i pesi di Parametri (D-50): senza Velocity i pesi si ridistribuiscono sulle altre tre; 2 decimali; vuoto se manca Impatto, Probabilita o Prossimita.",
    "Chiave": "Ciclo e ID uniti da \"|\": serve alle viste per trovare la riga.",
    "Mesi_Orizzonte": "Il numero di mesi dell'orizzonte (3, 6, 12); il piu' lungo fra le azioni non respinte e' la Y di Mosca.",
    "Stato@tblKRI": "Soglie da definire se ne manca una (le fissa la Banca); SOGLIE INVERTITE se allerta < attenzione; Non rilevato senza valore; Rosso se valore >= allerta; Ambra se >= attenzione; Verde sotto.",
    "Settimana": "Lunedi' della settimana della data della notizia.",
    "Owner@tblRegister": "Copiato dall'anagrafica (Parametri, colonna L) al momento della scrittura.",
    "Periodo_Valutazione": "Il Ciclo della riga; in un ciclo straordinario, per un rischio non rivalutato, il periodo da cui la riga e' riportata (D-75).",
    "Straordinario": "Scritto dallo script dalla decisione di baseline --straordinario: chi, quando, perche', rischi rivalutati (D-75).",
    "Esito": "Dallo script (D-51): Nuovo se il rischio non e' nella baseline; Variato se cambia Impatto, Probabilita, Prossimita o Velocity (anche da n.v. a un valore); altrimenti Confermato. Ricalcolato dopo la validazione.",
    "Variazioni": "A1 scrive dimensione, evidenza e sua data (dopo il ciclo precedente); da e a li aggiunge lo script dalla baseline. Al massimo un punto per dimensione.",
    "Impatto": "Descrittore della rubrica piu' aderente all'evidenza; al massimo un punto di variazione fra cicli.",
    "Probabilita": "Plausibilita' secondo i descrittori della rubrica (da Remota a Quasi certa); al massimo un punto fra cicli.",
    "Prossimita": "Solo il tempo prima che il rischio si manifesti; 4-5 solo con un caso nominato o un evento datato.",
    "Velocity": "Facoltativa: vuota (n.v.) se nessuna fonte documenta i tempi fra innesco e pieno impatto; nello score solo se valutata; da n.v. entra con qualunque valore.",
    "Fonti": "Per ogni fonte riferimento, data, tipo e rilevanza 1-3 per la previsione (D-58); stesso ente o stesso fatto = una fonte.",
    "Anni_Adeguamento@tblRegister": "Stima di A1 (D-60); il valore validato va nell'anagrafica, colonna M. Non e' una dimensione: non fa variazioni.",
    "Rilievi@tblRegister": "Segnalazioni di A5 e dei controlli sul rischio, una per riga: gravita' · controllo · origine: testo. ⚑ DA MOTIVARE = la validazione chiede una Motivazione (D-71); BLOCCANTE SUPERATO = registri fino al 2026-10-02 (D-56).",
    "Rilievi_Ciclo": "Segnalazioni sul ciclo nel suo insieme, stesso formato della colonna Rilievi del registro.",
    "Rilievi_Superati": "Quante segnalazioni sono da motivare in validazione, dai controlli e da A5 (D-71). Fino al 05/10/2026: bloccanti di A5 superati con --procedi-con-rilievi.",
    "KRI_ID": "Riuso del codice se il KRI resta; altrimenti primo progressivo libero del rischio (NFR-nn-Kn), mai riusato.",
    "ID_Azione": "<ciclo>-<rischio>-A<n>, n = posizione dell'azione nel rischio.",
    "Valore_Corrente": "Rilevato dalla fonte interna; vuoto se non rilevato, mai ricopiato dal ciclo prima.",
    "Rischio_ID": "Rischio indicato da A3; NON PRESIDIATO se la notizia non tocca rischi censiti.",
    "Osservazioni_Controlli": "Conteggio dei rilievi 'Osservazione' di A5 e dei controlli dello script.",
    "Stato@tblAzioni": "Proposta — da valutare; Approvata o Respinta con la validazione; In corso e Completata a mano; Annullata se il rischio esce.",
    "Stato@tblValidazione": "Da decidere quando la scrive lo script; Applicata dopo il comando valida. Non si tocca a mano.",
    "Data_Scrittura": "Data del giorno in cui lo script scrive la riga.",
    "Approvato_Da": "Il nome passato al comando valida (--validatore).",
    "Data_Validazione": "Giorno in cui si lancia il comando valida.",
    "Validazione": "Da validare alla scrittura; il comando valida scrive Accettato, Rettificato o Respinto (un rischio non si respinge).",
    "Data_Decisione": "Giorno del comando valida che ha deciso l'azione.",
    "Decisa_Da": "Il nome passato al comando valida (--validatore).",
    "Data_Rilevazione": "Data di riferimento del ciclo se c'e' un valore rilevato; vuota altrimenti.",
    "In_Vigore": "Sì per i KRI proposti nel ciclo; No nella riga del ciclo in cui un KRI non e' riproposto o e' respinto.",
    "Ciclo_Definizione": "Ciclo in cui il KRI e' nato; non cambia quando se ne aggiorna la definizione.",
    "Periodo": "Ciclo (per il trimestrale) o lunedi' della settimana (per il settimanale) della scrittura.",
    "Oggetto": "Tipo della riga proposta dall'agente.",
    "ID": "Codice dell'oggetto proposto (rischio, KRI, azione, notizia).",
    "Nome@tblValidazione": "Copiato dall'oggetto, per riconoscerlo senza cambiare foglio.",
    "Campo": "Uno dei campi validati: 6 per rischio (con la decisione sullo stato, D-79), 3 per KRI, 2 per azione, 2 per notizia (una colonna gialla della griglia ciascuno).",
    "Proposta_Agente": "Valore scritto dall'agente, copiato qui alla scrittura; resta per sempre.",
    "Decisione": "Dal comando valida, confrontando la cella gialla della griglia con la proposta: uguale = Accettato, diversa = Rettificato; Respingi = Sì = Respinto per tutti i campi dell'oggetto. Dopo il comando riapri (D-76): Invariato, Rettificato o Respinto (riapertura), dove la proposta e' il valore validato prima.",
    "Valore_Validato": "Rischio: intero 1-5 a non piu' di un punto dal ciclo prima (in riapertura senza limite; Velocity anche vuota; da n.v. qualunque valore); KRI: numero, soglie entrambe o nessuna; azione: owner (una funzione) o 3/6/12 mesi.",
    "Motivazione": "Quella della riga della griglia, riportata su ogni campo dell'oggetto; obbligatoria se un valore cambia, se si respinge e per un rischio con una segnalazione da motivare (⚑): almeno 10 caratteri, con l'evidenza.",
    "Validato_Da": "Il nome passato al comando valida (--validatore).",
    "Ciclo": "Ciclo da valutare, dalla baseline.",
    "Data_Riferimento": "Fine del trimestre valutato, dalla baseline.",
    "Sintesi_A1": "Scritta da A1 nella forma \"MESSAGGIO: ... DECISIONI: ...\": il Quadro d'insieme la divide in due righe.",
    "Stato@tblRegister": "Dallo script con la regola del registro unico (07_Senza_Studio/radar.py, D-79) sui valori proposti alla scrittura e sui valori validati dopo valida: soglie di Prossimita e Probabilita, eccezioni, capienza (Parametri, righe 65-75); Dismesso con il comando dismetti.",
    "Motivo_Stato": "Dalla stessa regola: quale soglia manca o quale eccezione vale, la capienza; per Radar, in uscita il primo ciclo sotto la regola.",
    "Movimento": "Dallo script: Entrato se il ciclo prima il rischio era in osservazione e ora e' nel radar; Uscito se era nel radar e ora e' in osservazione.",
    "Decisione_Stato": "Automatico alla scrittura (o la decisione in vigore dal ciclo prima); il comando valida scrive quella della griglia (Radar, Osservazione o Automatico).",
    "Ordine_Osservazione": "Solo per le righe del ciclo corrente in osservazione: score x 100.000 piu' un decimale dalla riga, per ordinarle dallo score piu' alto (fogli Osservazione e Fenomeni).",
}
VALORI = {"Data_Riferimento": "data", "Impatto": "1-5", "Velocity": "1-5 o vuota (n.v.)", "Prossimita": "1-5",
          "Probabilita": "1-5", "Anni_Adeguamento": "anni 0-30 o vuoto", "Score_Composito": "1,00-5,00",
          "Soglia_Attenzione": "numero o vuota", "Soglia_Allerta": "numero o vuota",
          "Esito": "Confermato, Variato, Nuovo", "Event_Type": "9.1 ... 9.13 (FP fuori perimetro)", "Ciclo": "AAAAQn o AAAAQn-Sk (straordinario)", "Orizzonte": "3, 6, 12 mesi",
          "Segnale": "Peggiorativo, Migliorativo, Neutro, Non rilevante", "Decisione": "Accettato, Rettificato, Respinto",
          "Validazione": "Da validare, Accettato, Rettificato, Respinto", "In_Vigore": "Sì, No",
          "Stato@tblRegister": "Radar, Radar, in uscita, Osservazione, Dismesso", "Movimento": "Entrato, Uscito o vuoto",
          "Decisione_Stato": "Automatico, Radar, Osservazione", "Orizzonte_Anni": "anni 1-30 o vuoto"}
ESEMPI_EXTRA = {"Score_Composito": "3,80", "Chiave": "2026Q2|NFR-01", "Mesi_Orizzonte": "6", "Stato@tblKRI": "Ambra",
                "Settimana": "08/06/2026", "Variazioni": "impatto da 3 a 4: report frodi (2026-06-10)", "Fonti": "4 fonti, 2 interne"}
CALCOLATI = [
    ("Δ ciclo prima", "Registro, Delta, Classifica", "Formula del foglio", "Variazione dello score sul trimestre precedente.", "Score del ciclo meno score del ciclo prima, stessi pesi (ridistribuiti se la Velocity manca).", "circa -1,5..+1,5", "+0,35"),
    ("Δ 6 mesi", "Registro", "Formula del foglio", "Variazione dello score su due trimestri.", "Score del ciclo meno score di due cicli prima; \"nuovo\" se allora il rischio non c'era.", "circa -3..+3", "+0,55"),
    ("P x I", "Matrice, Radar_Mosca", "Formula del foglio", "Gravita': probabilita' per impatto.", "Probabilita x Impatto.", "1-25", "16"),
    ("Z", "Radar_Mosca, Registro", "Formula del foglio", "Anni prima che il rischio possa manifestarsi.", "Dalla Prossimita, meta' della fascia: 5 → 0; 4 → 0,5; 3 → 1,5; 2 → 2,5; 1 → 3,5 (Parametri).", "anni", "0,5"),
    ("X", "Radar_Mosca", "Parametro", "Anni per decidere e avviare.", "Costante in Parametri: un trimestre.", "anni", "0,25"),
    ("Y", "Radar_Mosca", "Formula del foglio", "Anni per mitigare.", "Orizzonte piu' lungo delle azioni non respinte (1 anno se non ce ne sono); se maggiori, gli anni di adeguamento.", "anni", "0,5"),
    ("Margine / Urgenza", "Radar_Mosca, Registro, Classifica, Quadro", "Formula del foglio", "Quanto presto agire.", "Margine = Z - (X + Y). Sotto 0: AGIRE ORA; da 0 a 1: entro l'anno; oltre: margine in anni.", "anni", "-0,25 · AGIRE ORA"),
    ("Livello di allerta", "Radar_Mosca (colore), Registro (fondo dell'ID), Quadro, schede", "Formula del foglio", "Che cosa si fa adesso per il rischio (D-63).", "Attivazione con almeno due segnali forti (AGIRE ORA, KRI in rosso, notizie oltre la soglia); Attenzione con uno, o con margine sotto l'anno e un aggravante (P x I alta, presidio assente, KRI in ambra o rosso); Monitoraggio negli altri casi.", "Attivazione, Attenzione, Monitoraggio", "Attenzione"),
    ("KRI R, A, V", "Registro", "Formula del foglio", "Semaforo dei KRI del rischio.", "Conteggio dei KRI in vigore per Stato (quelli con soglie da definire non contano).", "interi", "0, 2, 1"),
    ("Segnali netti", "Registro", "Formula del foglio, dopo il settimanale", "Direzione delle notizie sul rischio nelle ultime 4 settimane.", "Peggiorative meno migliorative; ▲ o ▼ oltre la soglia di Parametri (2). Non cambia lo score.", "intero", "▲ +3"),
    ("Posizione in classifica", "Classifica, Quadro", "Formula del foglio", "Ordine per score composito.", "Dal piu' alto; a parita', ordine dell'anagrafica.", "1..n", "1"),
    ("Perche' lo segnaliamo", "Quadro", "Formula del foglio", "Motivo per cui un rischio e' fra i segnalati.", "Primi tre per score, in attivazione o attenzione, variati o nuovi; con urgenza, supervisore, presidio, KRI rossi, notizie.", "testo", "1° per score..."),
    ("Scadenza", "Piano_azioni", "Formula del foglio", "Quando l'azione dovrebbe essere completata.", "Data della decisione + orizzonte, per le azioni approvate o in corso.", "data", "15/01/2027"),
    ("Score e Margine di Mosca in validazione", "Validazione (righe dei rischi)", "Formula del foglio, mentre si scrive",
     "Effetto delle celle gialle prima di lanciare valida (D-67).", "Stesse formule del Registro e del Radar_Mosca sui valori gialli e "
     "sulle azioni non respinte della griglia; tra parentesi il valore con le sole proposte, se diverso.", "come Score e Margine",
     "3,40 (era 3,10)"),
]
PARAMETRI_DIZ = [
    ("Pesi dello score", "Parametri B4:B8", "Funzione di rischio (DECISIONI D-50)", "Peso di Impatto, Probabilita, Prossimita e Velocity nello score.", "Somma controllata = 1; senza Velocity si ridistribuiscono sulle altre tre.", "0-1",
     '=FIXED(pesoImpatto,2)&" / "&FIXED(pesoProbabilita,2)&" / "&FIXED(pesoProssimita,2)&" / "&FIXED(pesoVelocity,2)'),
    ("Soglia di direzione", "Parametri B11", "Funzione di rischio (D-61)", "Segnali netti oltre cui c'e' una tendenza.", "Confronto con i segnali netti di 4 settimane.", "intero", "=FIXED(sogliaDirezione,0)"),
    ("Soglia del Delta", "Parametri B12", "Funzione di rischio (D-61)", "Variazione dello score da guardare.", "Evidenzia |Δ| >= soglia.", "decimale", "=FIXED(sogliaDelta,2)"),
    ("Anni per Prossimita (Z)", "Parametri B51:B55", "Funzione di rischio (D-59)", "Tempo prima della manifestazione per livello.", "Letti da Z.", "anni", "3,5 / 2,5 / 1,5 / 0,5 / 0"),
    ("Soglie del livello di allerta", "Parametri B60:B63", "Funzione di rischio (D-63)", "P x I alta, quota di KRI in ambra o rosso, margine stretto, segnali forti per l'Attivazione.", "Lette dal Radar_Mosca.", "numeri",
     '=FIXED(livelloPxI,0)&" / "&FIXED(livelloQuotaKRI*100,0)&"% / "&FIXED(livelloMargine,2)&" / "&FIXED(livelloForti,0)'),
    ("Owner", "Parametri, anagrafica L", "Validatore, a mano", "Funzione responsabile del rischio.", "Resta da un ciclo all'altro; Da assegnare per un rischio nuovo.", "testo", "Funzione Antifrode"),
    ("Anni_Adeguamento", "Parametri, anagrafica M", "Validazione (stima di A1), correggibile a mano", "Durata di un adeguamento strutturale (D-60).", "Diventa la Y minima di Mosca; una stima vuota di A1 non cancella il valore.", "anni o vuoto", "NFR-11: 3"),
    ("Attenzione_Supervisore", "Parametri, anagrafica N", "Validatore, a mano", "Tema nelle priorita' di BCE, EBA o Banca d'Italia.", "◆ nel radar e nelle tabelle; non cambia score, urgenza ne' livello di allerta.", "Sì, No", "Sì"),
    ("Presidio_Controlli", "Parametri, anagrafica O", "Validatore, a mano", "Giudizio della Banca sui controlli esistenti (D-49): gli agenti non li vedono.", "Non verificato per un rischio nuovo; resta da un ciclo all'altro; nel Registro e nelle schede, non nello score.", ", ".join(PRESIDI), "Parziale"),
]


def foglio_dizionario(wb):
    ws = wb["Dizionario"]
    titolo(ws, "Dizionario dei dati", 7)
    for j, w in enumerate([22, 19, 24, 38, 56, 14, 22], start=1):
        ws.column_dimensions[get_column_letter(j)].width = w
    intest = ["Dato", "Dove", "Chi lo scrive, quando", "Che cosa significa", "Come si calcola / regola", "Valori", "Esempio (NFR-01, 2026Q2)"]
    for j, t in enumerate(intest, start=1):
        c = ws.cell(row=4, column=j, value=t); c.font = Font(bold=True, color="FFFFFF"); c.fill = fill(BLU_NOTTE)
    register, azioni, kri, news, validazione = dati_esempio()
    trova = lambda righe, **k: next(r for r in righe if all(r.get(a) == b for a, b in k.items()))
    esempi = {"tblRegister": trova(register, Ciclo=CICLO_CORRENTE, ID_Rischio="NFR-01"), "tblAzioni": trova(azioni, ID_Rischio="NFR-01"),
              "tblKRI": trova(kri, Ciclo=CICLO_CORRENTE, KRI_ID="NFR-01-K1"), "tblNews": news[1],
              "tblSintesi": {"Ciclo": CICLO_CORRENTE, "Data_Riferimento": DATE_CICLO[CICLO_CORRENTE], "Sintesi_A1": "MESSAGGIO: ...",
                             "Sintesi_A5": "Controlli superati...", "Osservazioni_Controlli": 1, "Data_Scrittura": DATE_CICLO[CICLO_CORRENTE]},
              "tblSettimane": {"Settimana": SETTIMANE_ESEMPIO[-1][0], "Notizie": SETTIMANE_ESEMPIO[-1][1],
                               "Sintesi_A3": "Linee guida europee sul rimborso...", "Flag_Proposti": "NFR-01 · Peggiorativo: ...",
                               "Data_Scrittura": SETTIMANE_ESEMPIO[-1][0]},
              "tblValidazione": trova(validazione, ID="NFR-10", Campo="Probabilita")}
    proc = {"A1": "trimestrale", "A5": "trimestrale", "A3": "settimanale", "script": "calcolo", "formula": "calcolo",
            "validazione": "validazione", "validatore": "validazione"}
    r = 5

    def sez(testo):
        nonlocal r
        ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=7)
        c = ws.cell(row=r, column=1, value=testo); c.font = Font(bold=True, color=BLU_NOTTE); c.fill = fill(BLU_CHIARO)
        r += 1

    def voce(valori, processo):
        nonlocal r
        for j, v in enumerate(valori, start=1):
            c = ws.cell(row=r, column=j, value=v)
            c.font = Font(size=9, bold=j == 1)
            c.alignment = Alignment(wrap_text=True, vertical="top", horizontal="left")
            c.border = BORDO_SOTTILE
        ws.cell(row=r, column=3).fill = fill(PROCESSI[processo][0])
        ws.row_dimensions[r].height = 12 * max(2, len(str(valori[4] or "")) // 52 + 1, len(str(valori[3] or "")) // 36 + 1) + 4
        r += 1

    for nome_t, testo in [("tblRegister", "RiskRegister — valutazioni dei rischi"), ("tblAzioni", "Azioni — azioni di mitigazione"),
                          ("tblKRI", "KRI — storico degli indicatori"), ("tblNews", "NewsLog — notizie"),
                          ("tblSintesi", "Sintesi_Cicli — commenti di A1 e A5"),
                          ("tblSettimane", "Sintesi_Settimane — sintesi di A3 e flag"),
                          ("tblValidazione", "Storico_Validazioni — proposte e decisioni, campo per campo")]:
        sez(testo)
        spec = spec_tabella(nome_t)
        for c in spec["colonne"]:
            chi = chi_colonna(nome_t, c)
            n = c["nome"]
            come = COME.get(f"{n}@{nome_t}") or COME.get(n) or ("Dal payload dell'agente, scritto dallo script." if chi in ("A1", "A3", "A5") else "—")
            es = ESEMPI_EXTRA.get(f"{n}@{nome_t}") or ESEMPI_EXTRA.get(n) or esempi[nome_t].get(n)
            if hasattr(es, "strftime"):
                es = es.strftime("%d/%m/%Y")
            if isinstance(es, float):
                es = f"{es:.2f}".replace(".", ",")
            if es is not None and not isinstance(es, str):
                es = str(es)
            if isinstance(es, str) and len(es) > 38:
                es = es[:36] + "…"
            voce([n, spec["foglio"], CHI_TESTO[chi], c["significato"], come, VALORI.get(f"{n}@{nome_t}") or VALORI.get(n, "—"), es], proc[chi])
    sez("Valori calcolati nelle viste")
    for v in CALCOLATI:
        voce(list(v), "calcolo")
    sez("Parametri e anagrafica (input)")
    for v in PARAMETRI_DIZ:
        voce(list(v), "validazione")
    ws.freeze_panes = "B5"


# ---------------------------------------------------------------- Metodologia
def _testo_kernel(*parti):
    return (QUI.parent.joinpath(*parti)).read_text(encoding="utf-8")


def leggi_scale():
    """Scale della rubrica (sezioni 1 e 2): [(titolo, [(score, descrittore)])],
    lette da 01_Kernel/rubrica_scoring.md: una sola fonte per prompt e report."""
    scale, corrente = [], None
    for riga in _testo_kernel("01_Kernel", "rubrica_scoring.md").split("## 3.", 1)[0].splitlines():
        if riga.startswith("### "):
            corrente = (riga[4:].strip(), [])
            scale.append(corrente)
        elif riga.startswith("## 2."):
            corrente = ("Rilevanza di ogni fonte per la previsione (1-3, D-58)", [])
            scale.append(corrente)
        elif corrente and riga.startswith("| ") and riga[2:3].isdigit():
            celle = [c.strip() for c in riga.strip().strip("|").split("|")]
            corrente[1].append((int(celle[0]), celle[1]))
    return [s for s in scale if s[1]]


def leggi_regole_variazione():
    corpo = _testo_kernel("01_Kernel", "rubrica_scoring.md").split("## 3.", 1)[1].split("\n## ", 1)[0]
    return [r.strip() for r in corpo.splitlines() if r[:1].isdigit()]


def leggi_limiti():
    """Testo dei limiti da riportare in ogni memo: 04_Riferimenti/controlli_e_model_risk.md, sezione 5."""
    corpo = _testo_kernel("04_Riferimenti", "controlli_e_model_risk.md").split("## 5.", 1)[1].split("\n## ", 1)[0]
    return " ".join(r.lstrip("> ").strip() for r in corpo.splitlines() if r.startswith(">")).strip()


def imposta_stampa(ws, area, orizzontale=True):
    """Pagina A4 adattata in larghezza, intestazione con l'etichetta di riservatezza."""
    ws.page_setup.orientation = "landscape" if orizzontale else "portrait"
    ws.page_setup.paperSize = ws.PAPERSIZE_A4
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.print_area = area
    ws.page_margins.left = ws.page_margins.right = 0.4
    ws.oddHeader.left.text = "&A"
    ws.oddHeader.center.text = ETICHETTA_RISERVATEZZA
    ws.oddHeader.right.text = NOME_ANALISI
    ws.oddFooter.left.text = "&F"
    ws.oddFooter.right.text = "Pagina &P di &N"


def foglio_metodologia(wb):
    """Come si leggono i numeri: pesi e parametri letti da Parametri, scale e regole dalla rubrica."""
    ws = wb["Metodologia"]
    titolo(ws, "Metodologia: come si leggono i numeri", 2)
    r = 4

    def riga(a, b=None, sezione_=None, formato=None):
        nonlocal r
        ws[f"A{r}"] = a
        ws[f"A{r}"].alignment = A_CAPO
        if b is not None:
            ws[f"B{r}"] = b
            ws[f"B{r}"].alignment = Alignment(wrap_text=True, vertical="top", horizontal="left")
            if formato:
                ws[f"B{r}"].number_format = formato
        if sezione_:
            colora(ws[f"A{r}"], sezione_)
            colora(ws[f"B{r}"], sezione_)
        r += 1

    def spazio():
        nonlocal r
        r += 1

    riga("CHI PRODUCE I NUMERI", "", sezione_="trimestrale")
    riga("Ciclo trimestrale", "A1 legge le fonti e valuta ogni rischio; lo script verifica le regole (si ferma solo se il "
                             "registro diventerebbe incoerente) e scrive nel registro; A5, un secondo agente facoltativo che "
                             "vede solo la valutazione e la baseline, la controlla con nove controlli. Le segnalazioni dei "
                             "controlli e di A5 passano al validatore, che accetta, rettifica o respinge ogni valore proposto "
                             "e motiva le segnalazioni da motivare (D-71).")
    riga("Ciclo settimanale", "A3 valuta le notizie della settimana. Le notizie non cambiano nessuno score: segnalano "
                             "temi e direzioni da portare al trimestre successivo.")
    riga("Schede dei rischi", "Dopo la validazione, A6 scrive i testi estesi delle schede (descrizione, spiegazione di ogni "
                             "punteggio, a cosa serve ogni fonte) sui dati validati; lo script controlla che non cambi numeri "
                             "ne' fonti e produce il file delle schede.")
    riga("Calcoli del foglio", "Score composito, urgenza, classifica e stato dei KRI li calcola il foglio con i "
                               "parametri qui sotto: nessun agente li stima. Ogni dato e' spiegato nel foglio Dizionario.")
    spazio()
    riga("FONTI ED EVIDENZE", "", sezione_="trimestrale")
    riga("Da dove", "Analisi interne della Banca (audit, test, incidenti, report delle funzioni), notizie raccolte ogni "
                    "giorno dalle fonti del catalogo approvato (codici FNT) e siti pubblici configurati. Ogni rischio "
                    "cita le sue fonti con data, tipo (Interna o Esterna) e rilevanza (file delle schede).")
    riga("Evidenza nuova", "Solo cio' che e' datato dopo la data di riferimento del ciclo precedente e non dopo quella del "
                           "ciclo corrente. Senza evidenza nuova il punteggio resta quello del ciclo prima.")
    riga("Cosa non e' evidenza", "La copertura mediatica (dieci articoli sullo stesso fatto sono un fatto) e le frasi "
                                 "generiche. Un numero senza fonte e' una valutazione e il razionale lo dichiara.")
    riga("Rilevanza delle fonti", "Ogni fonte ha una rilevanza 1-3 per la previsione (scala sotto): alta per una fonte "
                                  "primaria o un caso documentato, bassa per la stampa generalista. Stesso ente o stesso "
                                  "fatto contano una volta. Probabilita 5 o Prossimita 4-5 chiedono almeno una fonte di "
                                  "rilevanza alta (D-58). Non entra nello score.")
    spazio()
    riga("ANALISI PER DIMENSIONI", "", sezione_="trimestrale")
    riga("Principio", "Un rischio per ogni meccanismo di perdita sostenuto da almeno una fonte specifica, anche piu' "
                      "d'uno nella stessa categoria; nessuna categoria e' obbligatoria. Ogni rischio e' valutato su "
                      "quattro dimensioni, intere da 1 a 5 (5 = peggiore): per ognuna il descrittore piu' aderente "
                      "all'evidenza, senza interpolare. Solo cio' che le fonti sostengono (D-49).")
    for dimensione, domanda in [("Impatto", "Quanto danno, se il rischio si manifesta?"),
                                ("Probabilita", "Quanto e' plausibile che accada alla Banca? (da Remota a Quasi certa; 4-5 "
                                                "solo se la Banca e' esposta)"),
                                ("Prossimita", "Quando puo' manifestarsi? 4-5 solo con casi documentati o un evento certo, "
                                               "salvo fenomeni ad altissimo impatto dichiarati (da' anche la Z dell'urgenza)"),
                                ("Velocity", "Quanto in fretta arriva il pieno impatto dopo l'innesco? Facoltativa: n.v. "
                                             "(non valutata) se nessuna fonte ne documenta i tempi; conta di piu' con i "
                                             "cicli, man mano che l'evidenza arriva.")]:
        riga(dimensione, domanda)
    riga("Anni di adeguamento", "Anni di un adeguamento strutturale della Banca (migrazione, sostituzione di sistemi, "
                                "uscita da un fornitore): li stima A1, li decide il validatore e vanno nell'anagrafica "
                                "(D-60). Non sono uno score: allungano la Y dell'urgenza.")
    riga("Presidio dei controlli", "Giudizio qualitativo della Banca sui controlli esistenti (Non verificato, Adeguato, "
                                   "Parziale, Assente), scritto dal validatore nell'anagrafica: gli agenti non vedono i "
                                   "controlli interni. Si legge nel Registro e nelle schede; non entra nello score.")
    spazio()
    riga("SCORE COMPOSITO", "", sezione_="calcolo")
    riga("Che cos'e'", "Media pesata delle dimensioni valutate, da 1 a 5, calcolata dal foglio: se la Velocity non e' "
                       "valutata, il suo peso si ridistribuisce su Impatto, Probabilita e Prossimita. I pesi valgono per "
                       "tutti i cicli, passati compresi: il trend resta confrontabile.")
    for etichetta, nome in [("Peso Impatto", "pesoImpatto"), ("Peso Probabilita", "pesoProbabilita"),
                            ("Peso Prossimita", "pesoProssimita"), ("Peso Velocity (se valutata)", "pesoVelocity")]:
        riga(etichetta, f"={nome}", formato="0.00")
    riga("Somma dei pesi", "=FIXED(Parametri!B8,2)&\" — \"&Parametri!C8")
    spazio()
    riga("SCALE (descrittori della rubrica)", "", sezione_="trimestrale")
    for titolo_scala, voci in leggi_scale():
        riga(titolo_scala)
        ws[f"A{r - 1}"].font = GRASSETTO
        for score, descr in voci:
            riga(f"  {score}", descr)
    spazio()
    riga("REGOLE DI VARIAZIONE FRA CICLI", "", sezione_="trimestrale")
    for regola in leggi_regole_variazione():
        riga("", regola)
    spazio()
    riga("URGENZA: DISUGUAGLIANZA DI MOSCA", "", sezione_="calcolo")
    riga("Principio", "Se il tempo necessario per decidere (X) e per mitigare (Y) supera il tempo prima che il rischio "
                      "possa manifestarsi (Z), cioe' X + Y > Z, si e' gia' in ritardo anche se l'evento non e' imminente "
                      "(M. Mosca, 2015, per la migrazione alla crittografia post-quantistica).")
    riga("X: anni per decidere e avviare", "=moscaX", formato="0.00")
    riga("Y: anni per mitigare", "L'orizzonte piu' lungo delle azioni del ciclo non respinte (3, 6 o 12 mesi); se il "
                                 "rischio non ha azioni, la riserva qui sotto; se l'anagrafica indica anni di "
                                 "adeguamento strutturale (stimati da A1 e validati) e sono di piu', quelli.")
    riga("Y di riserva (anni)", "=moscaYDefault", formato="0.00")
    for k in range(1, 6):
        riga(f"Z per Prossimita {k} (anni, meta' della fascia)", f"=INDEX(anniProssimita,{k})", formato="0.00")
    riga("Esito", "Margine = Z - (X + Y). Sotto zero: AGIRE ORA. Da 0 a 1 anno: agire entro l'anno. Oltre: margine in anni.")
    riga("Limite", "Z e' la meta' della fascia della Prossimita (D-59: 3,5 anni per 'oltre 3 anni' e' una convenzione) e Y viene "
                   "da orizzonti a scaglioni o dagli anni di adeguamento: l'urgenza e' una graduatoria ancorata, non una "
                   "previsione.")
    spazio()
    riga("LIVELLO DI ALLERTA (colore del radar)", "", sezione_="calcolo")
    riga("Principio", "Unisce in una decisione segnali che stanno in colonne diverse. Segnali forti: AGIRE ORA, un KRI in "
                      "rosso, notizie in peggioramento oltre la soglia di direzione. Aggravanti, che contano solo con il "
                      "margine stretto: P x I alta, presidio dei controlli assente, KRI in ambra o rosso (D-63). Lo calcola "
                      "il foglio: nessun agente lo stima e non e' uno score.")
    riga("Attivazione (rosso)", '="Almeno "&livelloForti&" segnali forti: al comitato con un piano d\'azione."')
    riga("Attenzione (giallo)", '="Un segnale forte, oppure margine sotto "&FIXED(livelloMargine,1)&" anni con un aggravante (P x I da "'
                                '&livelloPxI&", presidio assente, almeno il "&FIXED(livelloQuotaKRI*100,0)&"% dei KRI in ambra o '
                                'rosso): l\'owner verifica azioni e KRI."')
    riga("Monitoraggio (verde)", "Gli altri casi: ciclo trimestrale ordinario.")
    spazio()
    riga("KRI", "", sezione_="trimestrale")
    riga("Verso e soglie", "Due per rischio (D-64): uno di esposizione (quanto la Banca e' esposta: di solito un dato "
                           "interno) e uno di evoluzione (quanto cresce il fenomeno, anche da fonti esterne). Valori crescenti = peggio (un indicatore 'piu' alto e' meglio' si "
                           "esprime come complemento, es. quota NON testata). Le soglie le propone A1 solo se una fonte le "
                           "sostiene, altrimenti le fissa la Banca in validazione: finche' mancano lo stato e' 'Soglie da "
                           "definire'. Verde sotto la soglia di attenzione, Ambra fra attenzione e allerta, Rosso da allerta "
                           "in su, Non rilevato se il valore manca: mai ricopiato dal ciclo prima.")
    riga("Fonte", "Ogni KRI ha una fonte dati identificabile; A1 rilegge i valori che trova, gli altri restano "
                  "Non rilevato.")
    spazio()
    riga("REGISTRO UNICO: RADAR E OSSERVAZIONE (pagina Fenomeni)", "", sezione_="trimestrale")
    riga("Che cos'e'", "Un solo registro di rischi, tutti valutati con la stessa rubrica e lo stesso score (D-79). I "
                       "rischi nel radar di Mosca hanno la gestione completa (KRI, azioni, urgenza, schede); gli altri sono "
                       "in osservazione: niente KRI ne' azioni, fuori da radar, classifica e urgenza, con l'orizzonte "
                       "stimato e il segnale che li porterebbe nel radar.")
    riga("Chi entra nel radar", '="Prossimita almeno "&sogliaProssimitaRadar&" e Probabilita almeno "&sogliaProbabilitaRadar'
                                '&", fino a "&capienzaRadar&" rischi (i più alti per score); sempre dentro, anche oltre la '
                                'capienza: AGIRE ORA (margine di Mosca negativo), tema del supervisore, decisione Radar del '
                                'validatore; mai dentro: decisione Osservazione del validatore."')
    riga("Come cambia", '="Lo script ricalcola lo stato a ogni ciclo e a ogni validazione. Un rischio che sale entra subito '
                        '(KRI e azioni li propone A1); uno che scende resta Radar, in uscita per "&(cicliUscitaRadar-1)'
                        '&" ciclo ed esce se lo è ancora dopo: i suoi KRI escono di vigore, la storia resta. Al massimo '
                        f'{MAX_OSSERVAZIONE} rischi in osservazione. Regola e parametri: foglio Parametri, righe 65-75."')
    spazio()
    riga("COME SI LEGGONO I GRAFICI", "", sezione_="calcolo")
    riga("Classifica", "Una barra per rischio, dal piu' alto per score composito; colore = esito dell'urgenza; freccia = "
                       "variazione sul ciclo prima.")
    riga("Lente di Mosca", "Colonna = X + Y (tempo necessario), rombo = Z (tempo disponibile), dal piu' in ritardo: la parte "
                           "rossa della colonna sfora il tempo disponibile.")
    riga("Radar di Mosca", "Piu' vicino al centro = agire prima (dentro il cerchio rosso: X + Y > Z). Area del cerchio = "
                           "Probabilita x Impatto (riferimenti 4, 12, 25 nel grafico); colore = livello di allerta; ◆ "
                           "accanto all'ID = tema all'attenzione del supervisore (BCE, EBA, Banca d'Italia), indicato dal "
                           "validatore. Settore = categoria della tassonomia interna, con il nome.")
    riga("Matrice", "Ogni rischio nella cella della sua Probabilita e Impatto; colore = P x I (verde fino a 6, ambra 8-12, "
                    "rosso da 15). Dice la gravita', non l'urgenza.")
    riga("Delta", "Variazione dello score composito sul ciclo precedente, scala fissa da -1,5 a +1,5: un punto di una "
                  "dimensione vale il suo peso diviso per la somma dei pesi valutati (la nota sotto il grafico lo calcola "
                  "dai pesi in vigore); quando la Velocity entra o esce i pesi si ridistribuiscono. A fianco il motivo, con "
                  "l'evidenza.")
    spazio()
    riga("VALIDAZIONE", "", sezione_="validazione")
    riga("", "Ogni valore proposto dagli agenti passa dal validatore, una riga per rischio (nel radar o in "
             "osservazione), KRI, azione e notizia: "
             "accettato, rettificato con motivazione o respinto. Il report mostra i valori validati; la proposta originale "
             "resta nel foglio Storico_Validazioni del registro. Un rischio con una segnalazione da motivare dei controlli "
             "o di A5 richiede sempre una motivazione (Quadro, pagina 2).")
    ws.column_dimensions["A"].width = 34
    ws.column_dimensions["B"].width = 120
    imposta_stampa(ws, f"A1:B{r}")


# ---------------------------------------------------------------- Guida (ex Leggimi)
CHI_AGGIORNA = [
    ("REPORT AL COMITATO", None, None, None, None),
    ("Quadro", "", "commento di A1, sintesi di A5, segnalazioni da motivare, numeri", "stato della validazione; avviso rettifiche", "prima pagina: il quadro e il perche'"),
    ("Classifica", "", "score e urgenza", "valori validati", "rischi per score; lente di Mosca"),
    ("Radar_Mosca", "segnali netti (livello)", "score, azioni (Y), KRI", "anni di adeguamento, presidio, attenzione del supervisore", "quanto presto agire, quanto e' grande, livello di allerta"),
    ("Matrice", "", "Probabilita e Impatto", "valori validati", "gravita' dei rischi"),
    ("Delta", "", "confronto con il ciclo prima", "", "che cosa e' cambiato e perche'"),
    ("Fenomeni", "", "rischi in osservazione, entrati e usciti", "valori e decisioni sullo stato", "rischi fuori dal radar, perche', con il segnale"),
    ("Metodologia", "", "", "pesi e parametri (Parametri)", "come si leggono i numeri"),
    ("LAVORO", None, None, None, None),
    ("Registro", "segnali netti (colonna Q)", "dimensioni, score, urgenza, KRI, rilievi", "righe 4-5; presidio (anagrafica)", "il ciclo corrente, un rischio per riga"),
    ("Storico, Indicatori", "", "si aggiornano", "", "score negli ultimi cicli; KRI del ciclo e storia di uno"),
    ("Notizie", "si aggiorna; sintesi e flag di A3", "", "", "pressione delle notizie, aree non presidiate, sintesi della settimana"),
    ("Piano_azioni", "", "azioni proposte da A1", "decisione; Stato In corso/Completata (foglio Azioni)", "tutte le azioni e la loro scadenza"),
    ("Osservazione", "", "si aggiorna", "", "rischi in osservazione e dove si concentrano (driver x categoria)"),
    ("Validazione", "righe delle notizie", "righe di rischi, KRI, azioni; stato dei rischi", "valori gialli, decisione sullo stato, Motivazione, Respingi (a mano)",
     "unico foglio da compilare: una riga per oggetto"),
    ("Parametri", "settimana corrente", "ciclo corrente; anagrafica H-K (= il radar)", "celle gialle", "pesi, soglie, urgenza, regola del radar, anagrafica"),
    ("Dizionario", "", "", "", "ogni dato: chi lo scrive, come si calcola"),
    ("DATI (solo lo script)", None, None, None, None),
    ("RiskRegister", "", "valutazioni di A1; stato nel registro unico", "valori validati, decisione sullo stato", "una riga per rischio per ciclo, radar e osservazione"),
    ("Azioni", "", "azioni proposte da A1", "delibera; Stato In corso/Completata a mano", "una riga per azione"),
    ("KRI", "", "KRI e valori riletti da A1", "rettifiche, KRI respinti", "storico, una riga per KRI per ciclo"),
    ("NewsLog", "notizie valutate da A3", "", "rettifiche (facoltative)", "una riga per notizia"),
    ("Sintesi_Cicli", "", "commento di A1 e di A5", "", "una riga per ciclo"),
    ("Sintesi_Settimane", "sintesi di A3 e flag proposti", "", "", "una riga per settimana"),
    ("Storico_Validazioni", "proposte delle notizie", "proposte di rischi, KRI, azioni", "decisioni (comando valida)",
     "una riga per oggetto e campo: proposta, valore deciso, motivo"),
    ("FILE A PARTE", None, None, None, None),
    ("Schede_<ciclo>.xlsx", "", "testi di A6 dopo la validazione", "dati validati", "una scheda per rischio (comando schede)"),
]


def foglio_guida(wb):
    ws = wb["Guida"]
    titolo(ws, "Guida: come si usa questo workbook", 5)
    for l, w in zip("ABCDE", [30, 28, 34, 34, 40]):
        ws.column_dimensions[l].width = w
    r = 3

    def testo(t, sezione_=None, altezza=None):
        nonlocal r
        c = ws.cell(row=r, column=1, value=t)
        ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=5)
        c.alignment = Alignment(wrap_text=True, vertical="top")
        if sezione_:
            colora(c, sezione_)
        n = _righe_stimate(t, 166 * 1.25)
        ws.row_dimensions[r].height = altezza or (15 * n + 2 if n > 1 else None)
        r += 1

    testo("A COSA SERVE", "misto")
    testo(f"{NOME_ANALISI}: registro dei rischi non finanziari emergenti della Banca. Ogni trimestre gli agenti valutano i "
          "rischi, lo script controlla e scrive qui, il validatore decide; i fogli da Quadro a Metodologia sono il report al "
          "comitato, le schede dei rischi un file a parte. Ogni foglio ha in testa (riga 2) chi lo aggiorna, cosa contiene "
          "e come si legge; il foglio Dizionario spiega ogni dato.")
    r += 1
    testo("CHI AGGIORNA COSA E QUANDO", "misto")
    for j, (intest, processo) in enumerate([("Foglio", "misto"), ("Settimanale · lunedi', A3", "settimanale"),
                                            ("Trimestrale · A1, poi A5", "trimestrale"),
                                            ("Validatore · dopo il trimestre", "validazione"), ("A che cosa serve", "misto")],
                                           start=1):
        c = ws.cell(row=r, column=j, value=intest)
        colora(c, processo)
        c.alignment = A_CAPO
    r += 1
    for foglio, sett, trim, val, uso in CHI_AGGIORNA:
        if sett is None:
            c = ws.cell(row=r, column=1, value=foglio)
            c.font = Font(bold=True, italic=True, color="595959")
            r += 1
            continue
        for j, (valore, processo) in enumerate([(foglio, None), (sett, "settimanale"), (trim, "trimestrale"),
                                                (val, "validazione"), (uso, None)], start=1):
            c = ws.cell(row=r, column=j, value=valore)
            c.alignment = A_CAPO
            if processo and valore:
                c.fill = PatternFill("solid", fgColor=PROCESSI[processo][0])
        ws.cell(row=r, column=1).font = GRASSETTO
        r += 1
    testo("Giornaliero: la raccolta delle notizie riempie la cartella News_Inbox, non questo file. A4 (pareri su "
          "richiesta, in qualsiasi momento) non scrive qui: se un parere suggerisce di rivedere un rischio, la via e' il "
          "ciclo trimestrale successivo.")
    r += 1
    testo("QUANDO SI LANCIANO A5 E A6", "trimestrale")
    for t in [
        "A5 (challenger), facoltativo (D-71): se lo si usa, dopo A1 e prima del comando trimestrale, allegando SOLO l'output "
        "di A1 e la baseline (Input_A5_<ciclo>.txt, D-84), e di nuovo ogni volta che A1 viene rifatto (vale solo per l'output esaminato). I "
        "suoi rilievi non fermano il ciclo: vanno nella colonna Segnalazioni del foglio Validazione, e un suo Bloccante "
        "rende obbligatoria la Motivazione del rischio. Lo script ferma solo i difetti di integrita' del registro. Non si "
        "lancia per le settimane, per A4 ne' dopo la validazione.",
        "A6 (schede): dopo la validazione del trimestre. Il comando schede-input prepara i dati validati; A6 scrive i testi; "
        "il comando schede li controlla e produce Schede_<ciclo>.xlsx. Senza A6 il comando schede produce comunque le "
        "schede con i testi del registro.",
    ]:
        testo(t)
    r += 1
    testo("DOVE SI SCRIVE A MANO (solo qui)", "validazione")
    for t in [
        "Validazione: una riga per rischio, KRI, azione e notizia; si cambiano solo le celle gialle, la Motivazione e "
        "Respingi (istruzioni e criteri in testa al foglio), poi il comando valida.",
        "Parametri, celle gialle: pesi, soglie, urgenza (decisione della funzione di rischio); nell'anagrafica Owner, "
        "anni di adeguamento, attenzione del supervisore e presidio dei controlli (decisi dal validatore, restano da un "
        "ciclo all'altro).",
        "Azioni, colonna Stato: avanzamento di un'azione approvata (In corso, Completata); il Piano_azioni si aggiorna da solo.",
        "Indicatori, cella N4: il KRI di cui guardare la storia.",
        "Testi delle tabelle dati, per correggerne la forma (D-76): RiskRegister Descrizione e Razionale (lasciando le "
        "etichette RISCHIO:, IMPATTO:...); KRI Nome, Unita, Fonte_Dati, Razionale, Nota_Rilevazione; Azioni Descrizione e "
        "Razionale; RiskRegister Segnale_Avvicinamento dei rischi in osservazione. Mai ID, numeri, date, "
        "Validazione o righe intere. Non resta traccia automatica: dopo, salvare, chiudere e lanciare  python "
        "esegui_ciclo_locale.py baseline  (riallinea baseline e knowledge di A7).",
        "Valori di un ciclo gia' validato (punteggi, decisione sullo stato, KRI, owner e orizzonte delle azioni): non qui, "
        "ma con  python esegui_ciclo_locale.py riapri, poi la griglia del foglio Validazione e valida, quante volte serve.",
        "Tutto il resto lo scrive lo script o e' una formula: non modificarlo.",
    ]:
        testo(t)
    r += 1
    testo("REGOLE", "misto")
    for t in [
        "1. Score composito, urgenza e stato dei KRI li calcola il foglio. Nessun agente li fornisce.",
        "2. Solo un ciclo (trimestrale o straordinario) cambia uno score, al massimo di un punto per dimensione e con "
        "un'evidenza datata; fuori dai cicli solo la funzione di rischio, riaprendo la validazione (riapri, con la "
        "motivazione, D-76).",
        "3. Prima di leggere i numeri guardare Registro righe 4 e 5: ciclo non validato o incompleto = numeri non definitivi.",
        "4. Il trimestre dopo non parte finche' quello prima non e' validato (lo script si ferma e lo dice).",
        "5. I grafici hanno scala fissa: cicli diversi si confrontano a colpo d'occhio.",
        "6. Un rischio si toglie solo con il comando dismetti, mai svuotando righe dell'anagrafica.",
    ]:
        testo(t)
    r += 1
    testo("PRIMO USO REALE", "misto")
    testo("Le righe su fondo grigio sono dati di ESEMPIO. Il registro vero lo crea il comando  python esegui_ciclo_locale.py "
          "inizializza --ciclo-precedente <trimestre prima del primo da valutare> --settimana <lunedi'>  che copia il "
          "template, toglie gli esempi e imposta ciclo e settimana. La guida completa e' 00_GUIDA_PASSO_PASSO.md.")
    r += 1
    testo("Generato da 03_Excel/genera_dashboard.py (versione della struttura " + VERSIONE_TEMPLATE + "). Per rifarlo a "
          "mano: 03_Excel/costruzione_manuale_template.md.")


# ---------------------------------------------------------------- composizione
# I fogli del report al comitato stanno di seguito (da Quadro a Metodologia): nel PDF escono in quest'ordine.
FOGLI = ["Guida", "Quadro", "Classifica", "Radar_Mosca", "Matrice", "Delta", "Fenomeni", "Metodologia",
         "Registro", "Storico", "Indicatori", "Notizie", "Piano_azioni", "Osservazione", "Validazione", "Parametri",
         "Dizionario", "RiskRegister", "Azioni", "KRI", "NewsLog", "Sintesi_Cicli", "Sintesi_Settimane",
         "Storico_Validazioni"]
FOGLI_REPORT = FOGLI[1:8]
GRUPPO_FOGLIO = {**{f: "report" for f in FOGLI_REPORT}, "Guida": "guida",
                 **{f: "lavoro" for f in ("Registro", "Storico", "Indicatori", "Notizie", "Piano_azioni", "Osservazione",
                                          "Validazione", "Parametri", "Dizionario")},
                 **{f: "dati" for f in ("RiskRegister", "Azioni", "KRI", "NewsLog", "Sintesi_Cicli", "Sintesi_Settimane",
                                        "Storico_Validazioni")}}
COLORE_LINGUETTA = {"report": BLU_NOTTE, "lavoro": BLU_DIM, "dati": GRIGIO_URG, "guida": "BF8F00"}


def trasparenza(percorso, colore=RIEMPIMENTO_CERCHIO, alpha=55000):
    """openpyxl non scrive la trasparenza: la si aggiunge nell'XML dei grafici (Excel la conserva nei salvataggi)."""
    import zipfile
    tmp = Path(str(percorso) + ".tmp")
    with zipfile.ZipFile(percorso) as zi, zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zo:
        for item in zi.infolist():
            dati = zi.read(item.filename)
            if item.filename.startswith("xl/charts/"):
                dati = dati.replace(f'<a:srgbClr val="{colore}"/>'.encode(),
                                    f'<a:srgbClr val="{colore}"><a:alpha val="{alpha}"/></a:srgbClr>'.encode())
            zo.writestr(item, dati)
    # Riscritture ravvicinate (una per colore): l'antivirus puo' tenere il file per un attimo.
    import time
    for tentativo in range(10):
        try:
            tmp.replace(percorso)
            return
        except PermissionError:
            if tentativo == 9:
                raise
            time.sleep(0.5)


def genera(percorso):
    wb = Workbook()
    wb.active.title = FOGLI[0]
    for nome in FOGLI[1:]:
        wb.create_sheet(nome)
    foglio_parametri(wb)
    fogli_dati(wb)
    foglio_registro(wb)
    foglio_radar_mosca(wb)
    foglio_storico(wb)
    foglio_delta(wb)
    foglio_indicatori(wb)
    foglio_notizie(wb)
    foglio_classifica(wb)
    foglio_matrice(wb)
    foglio_quadro(wb)
    foglio_piano_azioni(wb)
    foglio_osservazione(wb)
    foglio_fenomeni(wb)
    foglio_validazione(wb)
    foglio_dizionario(wb)
    foglio_metodologia(wb)
    foglio_guida(wb)
    for nome, ultima_colonna in COLONNE_GUIDA.items():      # dopo le larghezze: l'altezza dipende da quelle
        guida(wb[nome], nome, ultima_colonna)
    imposta_stampa(wb["Radar_Mosca"], f"A1:L{4 + MAX_RISCHI + 40}", orizzontale=False)
    for ws in wb.worksheets:
        ws.sheet_properties.tabColor = COLORE_LINGUETTA[GRUPPO_FOGLIO[ws.title]]
        ws.sheet_view.showGridLines = GRUPPO_FOGLIO[ws.title] == "dati"
    wb.active = wb.sheetnames.index("Quadro")
    wb.save(percorso)
    trasparenza(percorso)
    for _, colore, _ in LIVELLI:                         # cerchi del radar: colore del livello, semitrasparente
        trasparenza(percorso, colore)
    return percorso


if __name__ == "__main__":
    uscita = Path(sys.argv[1]) if len(sys.argv) > 1 else QUI / "NFR_Dashboard_Template.xlsx"
    genera(uscita)
    print(f"Template generato: {uscita}")
