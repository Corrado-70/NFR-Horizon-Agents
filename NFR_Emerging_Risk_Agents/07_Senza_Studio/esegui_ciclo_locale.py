"""Strumento di campo della variante senza Copilot Studio: A2 e controlli di A5.

Sostituisce Power Automate. Gira sul PC di un analista, su file in una
cartella SharePoint sincronizzata con OneDrive: nessuna API Graph, nessuna
registrazione applicativa, nessun ruolo amministrativo.

Comandi:
  trimestrale  --payload A1.json [--challenger A5.json]
      valida A1 -> controlli meccanizzati (+ esito dell'agente A5, facoltativo,
      D-71) -> completa il payload (esito e "da/a" delle variazioni dal
      confronto con la baseline, D-51) -> scrive nel workbook vivo (append
      RiskRegister/Azioni, fotografia dei KRI del ciclo in coda allo storico
      KRI, anagrafica, ciclo corrente, segnalazioni di A5 e dei controlli sui
      rischi) -> ricalcola in Excel -> verifica zero errori e copertura del
      ciclo -> SOLO ALLORA salva (backup prima) -> archivia in Cicli/<ciclo>/
      l'Excel di output NFR_Registro_<ciclo>.xlsx, gli output degli agenti,
      l'esito dei controlli e le righe per le liste; aggiorna
      Baseline_corrente.json. Ferma solo un difetto di integrita' (Bloccante
      dei controlli: C1, C2, C7, identificativi dei KRI), e allora scrive
      Cicli/<ciclo>/Correzione_A1_<ciclo>.txt per A1. I rilievi "Da motivare"
      (C3, date di C5, coppia e soglie dei KRI, Bloccanti di A5) vanno nella
      colonna Segnalazioni del foglio Validazione e chiedono una Motivazione.
  settimanale  --payload A3.json
      valida A3 e i codici fonte (01_Kernel/fonti.md) -> aggiunge le
      notizie (senza duplicati) -> fa scorrere la
      settimana corrente -> ricalcola, verifica, salva -> archivia in
      Settimane/<lunedi'>/ l'Excel di output e l'output di A3.
  baseline     [--uscita file.json]
      esporta la baseline corrente (input di A1, A3, A4, A5) e, accanto,
      l'allegato di A1 Input_A1_<ciclo>.txt: baseline, controlli di A5 e guida
      di scrittura (D-69; lo riscrive ogni comando che aggiorna la baseline).
  precontrollo --payload A1.json [--baseline file.json]
      facoltativo, prima di A5 se lo si usa; senza Excel e senza aprire il registro: schema, controlli
      meccanizzati (gli stessi di trimestrale) e parti del razionale (D-68)
      dell'output di A1 rispetto a Baseline_corrente.json; se trova qualcosa
      scrive Cicli/<ciclo>/Correzione_A1_<ciclo>.txt, il messaggio da incollare
      nella chat di A1 (D-69). Codice 1 se un punto fermerebbe il ciclo.
  valida       --periodo 2026Q3|2026-10-12 --validatore "Comitato Rischi"
      legge la griglia del foglio Validazione (una riga per rischio, KRI,
      azione, notizia, D-67): valore giallo uguale alla proposta = Accettato,
      cambiato = Rettificato, Respingi = Si' = Respinto; controlla TUTTE le
      righe (se una non va non applica niente), applica ai dati, registra chi
      e quando nello storico (tblValidazione, foglio Storico_Validazioni),
      toglie il periodo dalla griglia, salva (backup prima), archivia
      Validazione_<periodo>.json e l'Excel validato; per un ciclo riscrive
      Righe_liste_<ciclo>.json con i valori validati; aggiorna la baseline.
      Il trimestrale si ferma se il ciclo precedente non e' validato.
  griglia
      ricostruisce la griglia del foglio Validazione dalle proposte ancora da
      decidere, conservando cio' che il validatore ha gia' scritto nelle righe
      intatte: per ripararla dopo una modifica a mano (righe cancellate, ID
      cambiati). La riscrivono comunque trimestrale, settimanale e valida.
  riapri       [--rischi NFR-02,NFR-06]
      riapre la validazione del ciclo corrente, gia' validato (D-76): rischi
      (nel radar e in osservazione, D-79), KRI in vigore e azioni aperte tornano
      nella griglia con il valore validato; poi valida come sempre, quante volte
      serve. Riga non toccata = niente cambia; valore cambiato = rettifica con
      Motivazione, senza limite di un punto; Respingi = Si' toglie un KRI o
      annulla un'azione; Decisione sullo stato = rischio nel radar o in
      osservazione. Nello storico: "(riapertura)".
  inizializza  --ciclo-precedente 2026Q3 --settimana 2026-09-28 [--template file.xlsx]
      crea il registro vivo (percorso --workbook o configurazione.json) dal
      template, SENZA i dati di esempio. Non sovrascrive mai un file esistente.
  dismetti     --rischio NFR-04 --motivazione "..." --decisore "Comitato Rischi"
      toglie un rischio dall'anagrafica (senza lasciare righe vuote), fa uscire
      di vigore i suoi KRI del ciclo corrente, annulla le sue azioni aperte;
      la storia resta. Archivia Dismissioni/<rischio>_<data>.json.
  schede-input
      dopo la validazione del ciclo corrente: scrive Cicli/<ciclo>/
      Schede_input_<ciclo>.json, l'unico allegato dell'agente A6 (valori
      validati, urgenza, variazioni, fonti, azioni, KRI, storia per rischio).
      Non modifica il registro.
  schede       [--payload A6_<ciclo>.json]
      controlla l'output di A6 rispetto ai dati validati (stessi rischi, cinque
      dimensioni, stesse fonti, nessun numero nuovo) e scrive Cicli/<ciclo>/
      Schede_<ciclo>.xlsx; senza --payload, schede con i testi del registro.
      Non modifica il registro.
  aggiorna-registro  [--template file.xlsx]
      porta il registro vivo sul template nuovo quando cambia la struttura del
      workbook (versioneTemplate): copia per nome di colonna tutte le righe,
      l'anagrafica e i parametri, ricalcola, verifica (righe, errori, baseline
      identica), conserva il vecchio in Backup e lo sostituisce. Le colonne
      tolte dal modello (colonne_dismesse della mappa) restano solo nel
      Backup, quelle rinominate (colonne_rinominate: Severity -> Impatto)
      passano alla nuova; pesi, soglie e Z sono quelli del template nuovo.
      Le righe ancora da validare passano nella griglia del foglio Validazione
      con cio' che il validatore aveva gia' scritto (anche nel vecchio foglio
      Validazione, una riga per campo, dei registri fino al 2026-10-01).
  report       [--file registro.xlsx] [--con-lavoro]
      rigenera il PDF del report al comitato (fogli da Quadro a Metodologia;
      con --con-lavoro anche Registro e Parametri) dal registro vivo, o
      dall'Excel indicato con --file, dopo modifiche manuali dei validatori
      (presidio, anni di adeguamento, attenzione del supervisore, stato delle
      azioni). Il ciclo deve essere validato. Scrive
      Cicli/<ciclo>/Report_comitato_<ciclo>.pdf (la versione precedente resta
      con la data e l'ora nel nome). Non modifica l'Excel.

Ogni comando (tranne inizializza e aggiorna-registro, e precontrollo che non
apre il registro) si ferma su un registro creato con un template di versione
diversa da VERSIONE_TEMPLATE.

Opzioni comuni: --workbook, --kernel, --cartella-uscita (default in
configurazione.json accanto allo script, se presente).

Codici di uscita: 0 eseguito; 1 fermato da validazione o controlli (il
workbook NON viene toccato); 2 errore tecnico, e il messaggio dice se e'
avvenuto prima del salvataggio (nulla scritto) o dopo (registro scritto,
archivio da completare: non rilanciare).

Requisiti: Windows, Excel desktop di Microsoft 365, Python 3.10+, pywin32;
openpyxl per il comando schede (file delle schede).
Le regole NON sono duplicate qui: lo schema e la mappa delle colonne si
leggono da 01_Kernel (libreria Kernel del sito), il validatore e' generico
(valida_output.py), i controlli di A5 stanno in controlli_a5.py.
"""

import argparse
import datetime as dt
import json
import os
import re
import shutil
import sys
from pathlib import Path

QUI = Path(__file__).resolve().parent
sys.path.insert(0, str(QUI))

import controlli_a5                      # noqa: E402
import input_a1                          # noqa: E402
import radar                             # noqa: E402  regola del registro unico (D-79)
from fonti import codici_ammessi, leggi_fonti   # noqa: E402
from precontrollo import ciclo_di, conta, impronta, messaggio_correzione, precontrolla, riga_esito   # noqa: E402
from precontrollo import agente as agente_di   # noqa: E402  A1 per un trimestre, A8 per uno straordinario (D-77)
from valida_output import carica_json, valida   # noqa: E402

# Versione della struttura del workbook richiesta (nome definito versioneTemplate,
# scritto da 03_Excel/genera_dashboard.py con lo stesso valore).
VERSIONE_TEMPLATE = "2026-10-09"
TEMPLATE_PREDEFINITO = QUI.parent / "03_Excel" / "NFR_Dashboard_Template.xlsx"
GIALLO_INPUT = 0xCCF2FF                  # FFF2CC in formato BGR di Excel: celle di input
STATO_AZIONE_INIZIALE = "Proposta — da valutare"
OWNER_NUOVO = "Da assegnare"
NON_PRESIDIATO = "NON PRESIDIATO"
ANNULLATA = "Annullata"                 # azione di un rischio dismesso
STATI_AZIONE_CHIUSI = {"Completata", "Respinta", ANNULLATA}
DA_VALIDARE = "Da validare"
DA_DECIDERE = "Da decidere"
APPLICATA = "Applicata"
SEGNALI = ["Peggiorativo", "Migliorativo", "Neutro", "Non rilevante"]
ORIZZONTI = ["3 mesi", "6 mesi", "12 mesi"]
PRESIDIO_NUOVO = "Non verificato"       # presidio dei controlli di un rischio nuovo (anagrafica, D-49)
BLOCCANTE_SUPERATO = "BLOCCANTE SUPERATO"     # registri fino al 2026-10-02: Bloccante di A5 superato (D-56)
DA_MOTIVARE = "DA MOTIVARE"                   # D-71: segnalazione che chiede una Motivazione in validazione
DISMESSO = "Dismesso"                         # D-79: Stato della riga del ciclo di un rischio tolto con dismetti
# D-79: conversione della lista di osservazione della D-73 (aggiorna-registro): plausibilita' -> Probabilita.
PROBABILITA_DA_PLAUSIBILITA = {"teorica": 1, "possibile": 2, "in crescita": 3}


def da_motivare(rilievi):
    """Il testo della colonna Rilievi di un rischio contiene una segnalazione che chiede una Motivazione?"""
    testo = str(rilievi or "")
    return DA_MOTIVARE in testo or BLOCCANTE_SUPERATO in testo
# Dimensioni che decidono l'esito (D-51): "Variato" se ne cambia almeno una;
# (la Confidence non c'e' piu', D-58). Coppie (campo del payload, colonna del registro).
DIMENSIONI_ESITO = [("impatto", "Impatto"), ("probabilita", "Probabilita"), ("prossimita", "Prossimita"),
                    ("velocity", "Velocity")]
DIMENSIONI_RISCHIO = [c for _, c in DIMENSIONI_ESITO]


class Fermo(Exception):
    """Il ciclo si ferma per una ragione di merito (codice di uscita 1)."""


def leggi_payload(percorso, etichetta):
    """File JSON di un agente. Un file mancante o che non e' JSON e' un fermo
    (codice 1, niente scritto), non un errore tecnico: e' un errore di copia."""
    try:
        return carica_json(percorso)
    except FileNotFoundError:
        raise Fermo(f"{etichetta}: file non trovato: {percorso}. Controllare nome, estensione (.json, non .json.txt) e cartella.")
    except (json.JSONDecodeError, UnicodeDecodeError) as ex:
        raise Fermo(f"{etichetta}: {percorso} non e' un JSON valido ({ex}). Risalvare copiando solo da '{{' a '}}', "
                    "codifica UTF-8.")


def per_cella(valore):
    """Valore da scrivere in una cella via COM. Un testo si scrive SEMPRE come
    testo (apostrofo iniziale, che Excel non mostra e non restituisce):
    altrimenti "=..." diventa una formula (un titolo di notizia da un feed
    esterno puo' iniziare cosi'), "5/6" una data, "0012" il numero 12."""
    if isinstance(valore, str) and valore:
        return "'" + valore
    return valore


# ================================================================ configurazione
def configurazione(argomenti):
    conf = {}
    file_conf = QUI / "configurazione.json"
    if file_conf.exists():
        conf = carica_json(file_conf)
    def scegli(nome, predefinito=None):
        valore = getattr(argomenti, nome, None) or conf.get(nome) or predefinito
        return Path(valore) if valore else None
    return {
        "workbook": scegli("workbook"),
        "kernel": scegli("kernel", QUI.parent / "01_Kernel"),
        "cartella_uscita": scegli("cartella_uscita", QUI / "Uscita"),
        "news_inbox": scegli("news_inbox", QUI / "News_Inbox"),
    }


# ================================================================ date e cicli
def ciclo_successivo(ciclo):
    anno, q = int(ciclo[:4]), int(ciclo[5])
    return f"{anno + 1}Q1" if q == 4 else f"{anno}Q{q + 1}"


def ciclo_precedente(ciclo):
    anno, q = int(ciclo[:4]), int(ciclo[5])
    return f"{anno - 1}Q4" if q == 1 else f"{anno}Q{q - 1}"


def fine_trimestre(ciclo):
    anno, q = int(ciclo[:4]), int(ciclo[5])
    mese = 3 * q
    prossimo = dt.date(anno + (mese == 12), mese % 12 + 1, 1)
    return (prossimo - dt.timedelta(days=1)).isoformat()


# Periodi (D-75): un trimestre AAAAQn o uno straordinario AAAAQn-Sk, deciso fra la fine del trimestre AAAAQn e quella
# del trimestre dopo. In ordine alfabetico i periodi sono in ordine di tempo (2026Q4 < 2026Q4-S1 < 2026Q4-S2 < 2027Q1).
PERIODO = re.compile(r"\d{4}Q[1-4](?:-S[1-9])?")


def trimestre_di(periodo):
    return str(periodo)[:6]


def e_straordinario(periodo):
    return "-S" in str(periodo or "")


def _righe_o_niente(scr, nome):
    """Righe di una tabella; [] per una tabella che un registro di un template precedente non ha (es. tblSintesi)."""
    try:
        return scr.righe(nome)
    except KeyError:
        return []


def periodi_registro(scr):
    """Periodi gia' scritti nel registro (trimestri e straordinari), in ordine di tempo."""
    return sorted({str(r["Ciclo"]) for r in _righe_o_niente(scr, "tblRegister") if r.get("Ciclo")} |
                  {str(r["Ciclo"]) for r in _righe_o_niente(scr, "tblSintesi") if r.get("Ciclo")})


def periodi_prima(scr, periodo, quanti, altri=()):
    """I 'quanti' periodi prima di 'periodo', dal piu' vicino, nella sequenza del registro (straordinari compresi);
    prima dell'inizio del registro, trimestri a ritroso."""
    seq = sorted(set(periodi_registro(scr)) | set(altri) | {periodo})
    prima = [p for p in seq if p < periodo][::-1][:quanti]
    base = trimestre_di(prima[-1] if prima else periodo)
    while len(prima) < quanti:
        base = ciclo_precedente(base)
        prima.append(base)
    return prima


def data_periodo(scr, periodo):
    """Data di riferimento di un periodo: quella scritta nel registro; altrimenti la fine del trimestre."""
    for nome in ("tblSintesi", "tblRegister"):
        d = next((r.get("Data_Riferimento") for r in _righe_o_niente(scr, nome) if str(r.get("Ciclo")) == str(periodo)
                  and r.get("Data_Riferimento")), None)
        if d:
            return str(d)
    return fine_trimestre(trimestre_di(periodo))


def imposta_ciclo(scr, ciclo, data_rif):
    """Ciclo corrente e periodi delle viste (D-75): lo script scrive in Parametri il ciclo corrente, il precedente
    (anche uno straordinario), il trimestre di due trimestri prima (Delta 6 mesi), gli otto periodi del trend e la data
    di riferimento. Prima del 08/10/2026 erano formule che contavano solo trimestri."""
    prima = periodi_prima(scr, ciclo, 7)
    scr.imposta_nome("cicloCorrente", ciclo)
    for nome, valore in (("cicloPrecedente", prima[0]),
                         ("cicloMeno2", ciclo_precedente(ciclo_precedente(trimestre_di(ciclo))))):
        scr.imposta_nome(nome, valore)
    trend = scr.x.intervallo_nome("cicliTrend")
    for i, p in enumerate(prima[::-1] + [ciclo], start=1):
        trend.Cells(i, 1).Value = per_cella(p)
    scr.x.intervallo_nome("dataRiferimento").Value = a_data(data_rif)


def a_data(valore):
    """Stringa ISO -> numero seriale di Excel. Non si passa un datetime a COM:
    pywin32 lo interpreta come ora locale e lo converte in UTC, e la data
    scritta slitta di un giorno. Il seriale non e' ambiguo; il formato data
    della colonna lo mostra come data."""
    if valore in (None, ""):
        return None
    return (dt.date.fromisoformat(valore) - dt.date(1899, 12, 30)).days


def da_excel(valore):
    """Valore letto da COM -> tipo Python semplice (date ISO, interi veri)."""
    if hasattr(valore, "year") and hasattr(valore, "month"):
        return f"{valore.year:04d}-{valore.month:02d}-{valore.day:02d}"
    if isinstance(valore, float) and valore.is_integer():
        return int(valore)
    return valore


# ================================================================ mappa -> righe
def contesti(payload, righe_da):
    """Genera un dict di contesti per ogni riga: {'': radice, 'rischi[]': ..., ...}.
    righe_da vuoto = una sola riga per payload (tblSintesi)."""
    if not righe_da:
        yield {"": payload}
        return
    parti = righe_da.split("[].")
    parti[-1] = parti[-1].rstrip("[]")

    def ricorri(nodo, i, prefisso, ctx):
        chiave = f"{prefisso}{parti[i]}[]"
        for elemento in nodo.get(parti[i], []):
            nuovo = dict(ctx)
            nuovo[chiave] = elemento
            if i == len(parti) - 1:
                yield nuovo
            else:
                yield from ricorri(elemento, i + 1, chiave + ".", nuovo)
    yield from ricorri(payload, 0, "", {"": payload})


ORDINE_CHIAVI = ["dimensione", "da", "a", "evidenza", "data_evidenza", "riferimento", "data", "tipo", "rilevanza"]


def ordina_chiavi(valore):
    """Liste di oggetti (variazioni, fonti) con le chiavi nell'ordine di ORDINE_CHIAVI,
    qualunque sia l'ordine dell'output dell'agente: il foglio legge il testo JSON."""
    if isinstance(valore, list):
        pos = lambda k: ORDINE_CHIAVI.index(k) if k in ORDINE_CHIAVI else len(ORDINE_CHIAVI)
        return [{k: v[k] for k in sorted(v, key=pos)} if isinstance(v, dict) else v for v in valore]
    return valore


# Codici che lo strumento di ricerca della chat mette in testa ai riferimenti
# ("turn1search17 - ORX ..."): non identificano un documento (trappola 51).
CODICE_RICERCA = re.compile(r"^\s*(?:turn\d+[a-z]+\d+\s*[-\u2013\u2014:]?\s*)+", re.I)


def pulisci_riferimento(testo):
    pulito = CODICE_RICERCA.sub("", testo).strip()
    return pulito if len(pulito) >= 5 else testo


def _vuoto(v):
    return None if v in (None, "") else v


def completa_payload(payload, baseline):
    """Cio' che A1 non scrive piu' (D-51): l'esito di ogni rischio e i "da/a" delle
    variazioni, dal confronto con la baseline (la stessa che ha letto A1 e che
    ha usato A5). Toglie anche dai riferimenti delle fonti i codici dello
    strumento di ricerca. Idempotente: si puo' chiamare due volte."""
    base = {r["id_rischio"]: r for r in baseline.get("rischi", []) + baseline.get("rischi_in_osservazione", [])}
    for x in payload["rischi"]:
        for f in x.get("fonti", []):
            f["riferimento"] = pulisci_riferimento(f["riferimento"])
        prec = base.get(x["id_rischio"])
        if prec is None:
            x["_esito"] = "Nuovo"
            continue
        cambiati = [v for v, _ in DIMENSIONI_ESITO if _vuoto(x.get(v)) != _vuoto(prec.get(v))]
        x["_esito"] = "Variato" if cambiati else "Confermato"
        for z in x.get("variazioni", []):
            z["da"], z["a"] = _vuoto(prec.get(z["dimensione"])), _vuoto(x.get(z["dimensione"]))
    return payload


def testo_rilievi(stato, id_rischio):
    """Segnalazioni di A5 e dei controlli su un rischio (id_rischio None: sul ciclo), una per riga, prima quelle da
    motivare (D-71). Le stesse righe compaiono nella colonna Segnalazioni del foglio Validazione. Un Bloccante dei
    controlli non arriva mai qui: ferma la scrittura."""
    rilievi = [x for x in ((stato.get("controlli") or {}).get("esito") or {}).get("rilievi", [])
               if x.get("id_rischio") == id_rischio]
    rilievi.sort(key=lambda x: x["gravita"] != controlli_a5.DA_MOTIVARE)
    righe = [f"{'⚑ ' + DA_MOTIVARE if x['gravita'] == controlli_a5.DA_MOTIVARE else 'Osservazione'} · {x['controllo']} · "
             f"{'A5' if x.get('origine') == 'A5' else 'controlli'}: {x['descrizione']}" for x in rilievi]
    return "\n".join(righe)[:30000] or None


def risolvi(sorgente, ctx, stato):
    tipo, resto = sorgente.split(":", 1)
    if tipo == "derivato":
        return DERIVATI[resto](ctx, stato)
    if tipo == "formula":
        return None                                # scritta a parte, come formula
    percorso, _, trasf = resto.partition("|")
    if trasf.startswith("intensita:"):
        codice = trasf.split(":", 1)[1]
        impatti = ctx["notizie[]"]["impatti"]
        return next(i["intensita"] for i in impatti if i["event_type"] == codice)
    if "[]." in percorso:
        chiave, campo = percorso.rsplit("[].", 1)
        valore = ctx[chiave + "[]"].get(campo)
    else:
        valore = ctx[""].get(percorso)
    if trasf == "json":
        return json.dumps(ordina_chiavi(valore), ensure_ascii=False)
    if trasf == "lista":
        return ", ".join(valore)
    if trasf == "non_presidiato":
        return valore if valore else NON_PRESIDIATO
    return valore


# Campi calcolati dalla scrittura, non dal payload (vedi 04_Riferimenti/workflow.md, "Campi
# derivati"). Il collaudo verifica che ogni 'derivato:' della mappa sia qui.
DERIVATI = {
    "vuoto": lambda ctx, s: None,
    "data_scrittura": lambda ctx, s: s["oggi"],
    "owner_da_anagrafica": lambda ctx, s: s["owner"].get(ctx["rischi[]"]["id_rischio"], OWNER_NUOVO),
    "owner_esistente_o_da_assegnare": lambda ctx, s: s["owner"].get(ctx["rischi[]"]["id_rischio"]) or OWNER_NUOVO,
    # Input del validatore nell'anagrafica: la scrittura lo conserva, non lo inventa.
    "anni_adeguamento_esistente": lambda ctx, s: s.get("anni_adeguamento", {}).get(ctx["rischi[]"]["id_rischio"]),
    "attenzione_supervisore_esistente": lambda ctx, s: s.get("attenzione_supervisore", {}).get(ctx["rischi[]"]["id_rischio"]),
    "presidio_esistente_o_non_verificato": lambda ctx, s: s.get("presidio", {}).get(ctx["rischi[]"]["id_rischio"]) or PRESIDIO_NUOVO,
    # Esito calcolato da completa_payload (D-51), non scritto da A1.
    "esito": lambda ctx, s: ctx["rischi[]"]["_esito"],
    # Segnalazioni di A5 e dei controlli (D-56, D-71): sul rischio, sul ciclo, e quante sono da motivare.
    "rilievi_rischio": lambda ctx, s: testo_rilievi(s, ctx["rischi[]"]["id_rischio"]),
    "rilievi_ciclo": lambda ctx, s: testo_rilievi(s, None),
    "rilievi_superati": lambda ctx, s: (s.get("controlli") or {}).get("superamento_testo"),
    "sintesi_a5": lambda ctx, s: (((s.get("controlli") or {}).get("agente") or {}).get("sintesi")
                                  or ("A5 non usato in questo ciclo (facoltativo, D-71): valgono i controlli dello script e "
                                      "la validazione." if s.get("controlli") else None)),
    "osservazioni_controlli": lambda ctx, s: (sum(1 for x in s["controlli"]["esito"]["rilievi"] if x["gravita"] == "Osservazione")
                                             if s.get("controlli") else None),
    "stato_azione_iniziale": lambda ctx, s: STATO_AZIONE_INIZIALE,
    # Posizione per IDENTITA' (is), non per uguaglianza: due azioni identiche avrebbero lo stesso ID.
    "id_azione": lambda ctx, s: (f"{ctx['']['ciclo']}-{ctx['rischi[]']['id_rischio']}-A"
                                 f"{next(i for i, a in enumerate(ctx['rischi[]']['azioni_mitigazione'], start=1) if a is ctx['rischi[].azioni_mitigazione[]'])}"),
    "kri_id": lambda ctx, s: ctx["rischi[].kri_proposti[]"]["_kri_id"],
    "data_rilevazione": lambda ctx, s: None,       # la valorizza solo la rilettura
    "in_vigore": lambda ctx, s: "Sì",
    "ciclo_definizione": lambda ctx, s: ctx[""]["ciclo"],
    "da_validare": lambda ctx, s: DA_VALIDARE,
    "vuoto": lambda ctx, s: None,                     # colonna scritta dopo, non dal payload (es. Note_Analista, D-72)
    # Sintesi della settimana (D-66): numero di notizie e flag di A3, uno per riga.
    "numero_notizie": lambda ctx, s: len(ctx[""]["notizie"]),
    # Registro unico (D-79): stato, motivo e movimento li calcola radar.stati; la decisione del validatore resta
    # quella del ciclo prima finche' non la cambia.
    "stato_radar": lambda ctx, s: s["stati"][ctx["rischi[]"]["id_rischio"]]["stato"],
    "motivo_stato": lambda ctx, s: s["stati"][ctx["rischi[]"]["id_rischio"]]["motivo"],
    "movimento": lambda ctx, s: s["stati"][ctx["rischi[]"]["id_rischio"]]["movimento"] or None,
    "decisione_stato": lambda ctx, s: s.get("decisioni", {}).get(ctx["rischi[]"]["id_rischio"]) or radar.AUTOMATICO,
    # Ciclo straordinario (D-75): periodo di valutazione della riga e, nella sintesi, chi l'ha deciso e perche'.
    "periodo_valutazione": lambda ctx, s: ctx[""]["ciclo"],
    "straordinario": lambda ctx, s: s.get("straordinario_testo"),
    "proposta_straordinario": lambda ctx, s: ((lambda p: f"PROPOSTA DI CICLO STRAORDINARIO per {', '.join(p['rischi'])}: "
                                                         f"{p['motivo']}" if p else "—")(ctx[""].get("proposta_straordinario"))),
    "flag_proposti": lambda ctx, s: ("\n".join(f"{f['id_rischio']} · {f['direzione']}: {f['motivazione']}"
                                               for f in ctx[""]["flag_proposti"]) or "Nessun flag proposto"),
}


def spec_tabella(mappa, nome_tabella):
    """Tabelle dati in mappa['tabelle']; la tabella di validazione in mappa['validazione']."""
    if nome_tabella == mappa["validazione"]["tabella"]:
        return mappa["validazione"]
    return mappa["tabelle"][nome_tabella]


def valori_riga(spec, ctx, stato):
    out = {}
    for c in spec["colonne"]:
        if c.get("aggiorna_per") or c["sorgente"].startswith("formula:"):
            continue      # scritte dalla rilettura KRI / formule: mai scritte come valore
        v = risolvi(c["sorgente"], ctx, stato)
        out[c["nome"]] = a_data(v) if c.get("formato") == "data" and isinstance(v, str) else v
    return out


# ================================================================ workbook: versione e costanti
def file_kernel(conf, nome):
    """Un file del kernel dalla cartella 'kernel' della configurazione (la library Kernel
    sincronizzata). Se manca e' un passo dell'installazione non fatto, non un guasto: FERMATO
    con il rimedio, invece di un errore tecnico."""
    percorso = conf["kernel"] / nome
    if not percorso.exists():
        raise Fermo(f"Manca {percorso}.\nCopiare TUTTI i file della cartella 01_Kernel del pacchetto nella cartella "
                    f"'kernel' di configurazione.json ({conf['kernel']}): e' la library Kernel sincronizzata "
                    "(guida, sezione 0-bis, punto 1).")
    return percorso


def carica_mappa(conf):
    """Mappa delle colonne (01_Kernel, o la library Kernel sincronizzata). Deve
    descrivere la stessa struttura che lo script si aspetta: una mappa vecchia
    con un template nuovo (o il contrario) scriverebbe colonne sbagliate."""
    mappa = carica_json(file_kernel(conf, "mappatura_campi.json"))
    if mappa.get("versione_template") != VERSIONE_TEMPLATE:
        raise Fermo(f"{conf['kernel'] / 'mappatura_campi.json'} e' della versione {mappa.get('versione_template') or 'precedente al 25/09/2026'}, "
                    f"lo script della {VERSIONE_TEMPLATE}: copiare nella cartella Kernel la mappatura_campi.json del pacchetto.")
    return mappa



def costante(sessione, nome):
    """Valore numerico di un nome definito costante (es. capienzaKRICorrenti = 60),
    scritto dal generatore. None se il workbook non lo dichiara."""
    try:
        return int(float(str(sessione.wb.Names(nome).RefersTo).lstrip("=")))
    except Exception:
        return None


def versione_workbook(sessione):
    """Versione della struttura (nome definito versioneTemplate); None per i
    template precedenti al 25/09/2026, che non la dichiaravano."""
    try:
        return str(sessione.wb.Names("versioneTemplate").RefersTo).lstrip("=").strip('"')
    except Exception:
        return None


def controlla_versione(sessione, cosa="Il registro"):
    """Un registro nato da un template con un'altra struttura non si scrive: le
    colonne e i nomi che lo script usa potrebbero non esserci, o essere altrove."""
    v = versione_workbook(sessione)
    if v != VERSIONE_TEMPLATE:
        origine = "precedente al 25/09/2026" if v is None else f"versione {v}"
        rimedio = ("Aggiornarlo con:  python esegui_ciclo_locale.py aggiorna-registro  (copia i dati nel template nuovo, "
                   "verifica e conserva il vecchio in Backup)." if cosa == "Il registro" else
                   "Usare il template del pacchetto (03_Excel/NFR_Dashboard_Template.xlsx) o rigenerarlo con genera_dashboard.py.")
        raise Fermo(f"{cosa} {sessione.percorso} e' stato creato con un template {origine}; questo script richiede la "
                    f"versione {VERSIONE_TEMPLATE}. {rimedio}")


def righe_di_testo(testo, larghezza, dimensione):
    """Righe occupate da un testo a capo in una cella larga 'larghezza' (unita' di colonna di Excel),
    con carattere di 'dimensione' punti: circa 1,3 caratteri per unita' a 10 punti."""
    per_riga = max(1, int(larghezza * 1.3 * 10 / dimensione))
    return sum(max(1, -(-len(par) // per_riga)) for par in str(testo).split("\n"))


def adatta_altezze(sessione, nome, vuota):
    """Altezza di ogni riga di un intervallo con nome = il testo piu' lungo fra le sue celle,
    unite o no (Excel non adatta da solo l'altezza delle celle unite). Riga senza testo:
    altezza 'vuota' (le righe dei rischi non segnalati quasi spariscono)."""
    for riga in sessione.intervallo_nome(nome).Rows:
        altezza = 0
        for c in riga.Cells:
            if c.MergeCells and c.MergeArea.Cells(1, 1).Address != c.Address:
                continue
            v = c.Value
            if not isinstance(v, str) or not v.strip():
                continue
            larghezza = sum(x.ColumnWidth for x in c.MergeArea.Cells)
            dimensione = c.Font.Size or 10
            altezza = max(altezza, righe_di_testo(v, larghezza, dimensione) * dimensione * 1.35 + 5)
        riga.RowHeight = min(409, max(altezza, 14)) if altezza else vuota


def spazio_per_il_grafico(sessione, foglio, nome):
    """Nel Delta il grafico sta accanto alle righe dei motivi: se, adattate ai testi, sono
    piu' basse del grafico, la riga vuota sotto di esse si allunga quanto serve (altrimenti il
    grafico coprirebbe la nota sulla scala e passerebbe il salto pagina)."""
    ws = sessione.foglio(foglio)
    area = sessione.intervallo_nome(nome)
    vuota = area.Row + area.Rows.Count                  # riga vuota sotto l'intervallo
    grafico = ws.ChartObjects(1)
    manca = grafico.Top + grafico.Height + 6 - ws.Rows(vuota + 1).Top
    riga = vuota
    while manca > 0 and riga >= area.Row:
        aggiunta = min(manca, 409 - ws.Rows(riga).RowHeight)
        ws.Rows(riga).RowHeight = ws.Rows(riga).RowHeight + aggiunta
        manca -= aggiunta
        riga -= 1


def scala_quadro(sessione, massima=78, minima=60):
    """Il Quadro si stampa in due pagine (quadro; commento e rischi segnalati): con molti rischi
    segnalati (dal 01/10 anche quelli in attenzione, D-63) la seconda pagina puo' non bastare e
    Limiti e legenda finirebbero da soli su una terza. Si riduce la scala quanto serve, mai sotto
    `minima` ne' sopra `massima`."""
    ws = sessione.foglio("Quadro")
    ps = ws.PageSetup
    ultima = ws.Range(ps.PrintArea).Row + ws.Range(ps.PrintArea).Rows.Count - 1
    # L'interruzione manuale del template (dopo il radar); quelle automatiche dipendono dalla scala attuale e
    # misurerebbero male la prima pagina (D-72: la riga delle Note la allunga).
    manuali = [ws.HPageBreaks(i).Location.Row for i in range(1, ws.HPageBreaks.Count + 1)
               if ws.HPageBreaks(i).Type == -4135]                   # xlPageBreakManual
    salto = min(manuali) if manuali else ultima + 1
    altezza = lambda da, a: sum(ws.Rows(r).RowHeight for r in range(da, a + 1))
    disponibile = 595.3 - ps.TopMargin - ps.BottomMargin           # A4 orizzontale, in punti
    serve = max(altezza(1, salto - 1), altezza(salto, ultima))
    ps.Zoom = int(max(minima, min(massima, disponibile * 0.98 / serve * 100)))


def prepara_report(sessione):
    """Impaginazione del report al comitato: altezza delle righe con testi calcolati dalle
    formule (Quadro: commento e rischi segnalati; Delta: motivi delle variazioni).
    Solo aspetto: se non riesce avvisa e basta."""
    try:
        adatta_altezze(sessione, "quadroCommento", 15)
        adatta_altezze(sessione, "quadroSegnalati", 3)
        adatta_altezze(sessione, "deltaMotivi", 3)
        adatta_altezze(sessione, "fenomeniLista", 3)              # D-79: rischi in osservazione
        adatta_altezze(sessione, "fenomeniUscite", 3)             # D-79: entrati e usciti dal radar
        spazio_per_il_grafico(sessione, "Delta", "deltaMotivi")
        scala_quadro(sessione)
    except Exception as ex:
        print(f"Avviso: impaginazione del report non aggiornata ({type(ex).__name__}: {ex}). I dati sono scritti comunque.")


def svuota_registro(sessione, mappa):
    """Toglie dal template i dati di esempio: tabelle (una riga segnaposto con le
    formule) e anagrafica. Usata da inizializza e aggiorna-registro."""
    for nome in [*mappa["tabelle"], mappa["validazione"]["tabella"]]:
        # Si lascia UNA riga, svuotata dei valori ma con le formule: e' il
        # segnaposto che la prima scrittura riempie (vedi Scrittore.segnaposto).
        lo = sessione.tabella(nome)
        for i in range(lo.ListRows.Count, 1, -1):
            lo.ListRows(i).Delete()
        riga = lo.ListRows(1).Range
        for c in spec_tabella(mappa, nome)["colonne"]:
            if not c.get("sorgente", "").startswith("formula:"):
                riga.Cells(1, lo.ListColumns(c["nome"]).Index).ClearContents()
        riga.Interior.ColorIndex = -4142        # le righe nuove non ereditano il grigio "esempio"
    anag = sessione.intervallo_nome("anagrafica")
    anag.ClearContents()
    anag.Interior.ColorIndex = -4142           # niente fondo grigio "esempio"
    for nome in ("ANA_Owner", "ANA_Anni_Adeguamento", "ANA_Attenzione_Supervisore", "ANA_Presidio_Controlli"):
        sessione.intervallo_nome(nome).Interior.Color = GIALLO_INPUT   # restano celle di input del validatore
    try:
        sessione.intervallo_nome("quadroNote").ClearContents()          # Note dell'analista del Quadro (D-72)
    except Exception:
        pass                                    # template precedente al 2026-10-07: la cella non c'e'


# ================================================================ scrittura COM
class Scrittore:
    """Scrive nel workbook aperto in Excel. Nessun salvataggio qui."""

    def __init__(self, sessione, mappa):
        self.x = sessione
        self.mappa = mappa

    def _colonne(self, lo):
        return {c.Name: c.Index for c in lo.ListColumns}

    def _formula(self, modello, idx, riga_foglio, lo):
        out = modello
        for nome, i in idx.items():
            col = lo.Range.Column + i - 1
            lettera = self.x.foglio(lo.Parent.Name).Cells(1, col).Address.split("$")[1]
            out = out.replace("{" + nome + "}", f"{lettera}{riga_foglio}")
        return out

    def _scrivi_riga(self, lo, riga_range, valori, spec):
        """Scrive i valori per nome colonna e rimette le formule della mappa."""
        idx = self._colonne(lo)
        for nome, v in valori.items():
            riga_range.Cells(1, idx[nome]).Value = per_cella(v)
        for c in spec["colonne"]:
            if c.get("sorgente", "").startswith("formula:"):
                riga_range.Cells(1, idx[c["nome"]]).Formula = self._formula(
                    c["sorgente"][len("formula:"):], idx, riga_range.Row, lo)

    @staticmethod
    def segnaposto(lo):
        """La tabella di un registro appena inizializzato ha UNA riga vuota (con le
        formule): la prima scrittura la riempie. Mai inserire una riga in una
        tabella vuota: Excel la metterebbe in cima all'intervallo dei nomi
        definiti (prima riga dati), che scivolerebbero in basso lasciando fuori i dati."""
        return lo.ListRows.Count == 1 and lo.ListRows(1).Range.Cells(1, 1).Value in (None, "")

    def _controlla_capienza(self, lo, nuove):
        limite = self.x.intervallo_nome(f"{self._prefisso(lo.Name)}_{lo.ListColumns(1).Name}").Rows.Count
        attuali = 0 if self.segnaposto(lo) else lo.ListRows.Count
        if attuali + nuove > limite:
            raise RuntimeError(f"{lo.Name}: {attuali}+{nuove} righe superano le {limite} coperte dalle formule. "
                               "Alzare MAX_RIGHE in genera_dashboard.py e rigenerare il template.")

    def capienza(self, nome):
        """Capacita' di una vista, scritta dal generatore come nome definito
        costante (capienzaKRICorrenti, capienzaElencoKRI). None in un template
        che non la dichiara."""
        return costante(self.x, nome)

    @staticmethod
    def _prefisso(nome_tabella):
        return {"tblRegister": "RR", "tblAzioni": "AZ", "tblKRI": "KRI", "tblNews": "NW", "tblValidazione": "VAL",
                "tblSintesi": "SI", "tblSettimane": "SE"}[nome_tabella]

    def append(self, nome_tabella, righe):
        """Append relativo alla TABELLA (ListRows.Add), mai all'ultima riga del foglio."""
        spec = spec_tabella(self.mappa, nome_tabella)
        lo = self.x.tabella(nome_tabella)
        self._controlla_capienza(lo, len(righe))
        for i, valori in enumerate(righe):
            riga = lo.ListRows(1).Range if i == 0 and self.segnaposto(lo) else lo.ListRows.Add().Range
            self._scrivi_riga(lo, riga, valori, spec)

    def righe(self, nome_tabella):
        """Righe dati della tabella; la riga segnaposto di una tabella vuota non conta."""
        from excel_com import valori_tabella
        lo = self.x.tabella(nome_tabella)
        if self.segnaposto(lo):
            return []
        return [{k: da_excel(v) for k, v in r.items()} for r in valori_tabella(lo)]

    def aggiorna(self, nome_tabella, n_riga, valori):
        """Aggiorna le colonne indicate della n-esima riga dati (1 = prima). Aggiornano
        righe esistenti solo la validazione e la sintesi della settimana rilanciata (D-66):
        la scrittura degli agenti aggiunge."""
        lo = self.x.tabella(nome_tabella)
        idx = self._colonne(lo)
        riga = lo.ListRows(n_riga).Range
        for nome, v in valori.items():
            riga.Cells(1, idx[nome]).Value = per_cella(v)

    # ---------------------------------------------------- anagrafica
    def leggi_anagrafica(self):
        rng = self.x.intervallo_nome("anagrafica")
        nomi = [c["nome"] for c in self.mappa["anagrafica"]["colonne"]]
        righe = []
        for i, valori in enumerate(rng.Value):
            if valori[0]:
                righe.append((i + 1, dict(zip(nomi, valori))))
        return rng, righe

    def upsert_anagrafica(self, payload, stato):
        """Una riga per rischio del payload, colonne dalla mappa: ID, Nome,
        Event_Type e Driver dal payload; Owner, Anni_Adeguamento,
        Attenzione_Supervisore e Presidio_Controlli (input umani) conservati
        dalla riga esistente. D-79: un rischio che rientra nel radar riprende
        owner e anni di adeguamento dalla sua ultima riga del registro
        (stato["owner_storico"], stato["anni_storici"])."""
        rng, righe = self.leggi_anagrafica()
        per_id = {r["ID"]: i for i, r in righe}
        occupate = {i for i, _ in righe}
        libere = [i for i in range(1, rng.Rows.Count + 1) if i not in occupate]
        spec = self.mappa["anagrafica"]
        stato = dict(stato, owner={**stato.get("owner_storico", {}), **{r["ID"]: r["Owner"] for _, r in righe}},
                     anni_adeguamento={**stato.get("anni_storici", {}), **{r["ID"]: r.get("Anni_Adeguamento") for _, r in righe}},
                     attenzione_supervisore={r["ID"]: r.get("Attenzione_Supervisore") for _, r in righe},
                     presidio={r["ID"]: r.get("Presidio_Controlli") for _, r in righe})
        for ctx in contesti(payload, spec["righe_da"]):
            rid = ctx["rischi[]"]["id_rischio"]
            if rid in per_id:
                i = per_id[rid]
            else:
                if not libere:
                    raise RuntimeError("Anagrafica piena: alzare MAX_RISCHI in genera_dashboard.py e rigenerare il template.")
                i = libere.pop(0)
            for j, c in enumerate(spec["colonne"], start=1):
                rng.Cells(i, j).Value = per_cella(risolvi(c["sorgente"], ctx, stato))

    def compatta_anagrafica(self, togli):
        """Riscrive l'anagrafica senza il rischio 'togli' e senza righe vuote in
        mezzo: le viste (radar compreso) leggono le prime N righe, N = rischi
        presenti, quindi un buco farebbe sparire l'ultimo rischio."""
        rng, righe = self.leggi_anagrafica()
        nomi = [c["nome"] for c in self.mappa["anagrafica"]["colonne"]]
        rimaste = [[r[n] for n in nomi] for _, r in righe if r["ID"] != togli]
        vuote = [[None] * len(nomi)] * (rng.Rows.Count - len(rimaste))
        rng.Value = tuple(tuple(per_cella(v) for v in riga) for riga in rimaste + vuote)

    def imposta_nome(self, nome, valore):
        self.x.intervallo_nome(nome).Value = per_cella(valore)


# ================================================================ registro unico: radar e osservazione (D-79)
def regola_radar(sessione):
    """Parametri della regola dal registro (celle gialle di Parametri, pesi, Z e X/Y di Mosca); per un nome che manca,
    il valore del template (radar.REGOLA_DEFAULT). La capienza non supera i posti dell'anagrafica."""
    r = json.loads(json.dumps(radar.REGOLA_DEFAULT))

    def numero(nome):
        try:
            v = sessione.intervallo_nome(nome).Value
        except Exception:
            return None
        return v if isinstance(v, (int, float)) and not isinstance(v, bool) else None
    for chiave, nome in (("capienza", "capienzaRadar"), ("soglia_prossimita", "sogliaProssimitaRadar"),
                         ("soglia_probabilita", "sogliaProbabilitaRadar"), ("cicli_uscita", "cicliUscitaRadar")):
        if numero(nome) is not None:
            r[chiave] = int(numero(nome))
    for dim, nome in (("impatto", "pesoImpatto"), ("probabilita", "pesoProbabilita"), ("prossimita", "pesoProssimita"),
                      ("velocity", "pesoVelocity")):
        if numero(nome) is not None:
            r["pesi"][dim] = float(numero(nome))
    try:
        z = sessione.intervallo_nome("anniProssimita").Value
        r["anni_prossimita"] = [float(x[0]) for x in z]
    except Exception:
        pass
    for chiave, nome in (("mosca_x", "moscaX"), ("mosca_y_riserva", "moscaYDefault")):
        if numero(nome) is not None:
            r[chiave] = float(numero(nome))
    r["max_radar"] = sessione.intervallo_nome("anagrafica").Rows.Count
    r["max_osservazione"] = costante(sessione, "capienzaOsservazione") or r["max_osservazione"]
    r["capienza"] = max(0, min(r["capienza"], r["max_radar"]))
    return r


def stato_prima_di(riga_prima, in_anagrafica):
    """Stato del rischio nel periodo prima: quello scritto; per un registro precedente al 2026-10-09 (senza Stato),
    Radar se il rischio era valutato. None per un rischio nuovo o dismesso."""
    if riga_prima is None:
        return radar.RADAR if in_anagrafica else None
    stato = riga_prima.get("Stato")
    if stato == DISMESSO:
        return None
    return stato if stato in radar.STATI else radar.RADAR


def y_azioni_di(azioni, rid, periodo):
    """Y delle azioni per il margine di Mosca: azioni del rischio nel periodo di valutazione, non respinte (come il
    foglio Radar_Mosca)."""
    return radar.y_azioni([a["Orizzonte"] for a in azioni
                           if a["ID_Rischio"] == rid and str(a["Ciclo"]) == str(periodo) and a["Stato"] != "Respinta"])


def ingresso_radar(rid, valori, stato_prima, decisione, supervisore, anni, y):
    """Un rischio per radar.stati: valori = {impatto, probabilita, prossimita, velocity}."""
    return {"id": rid, **{d: _vuoto(valori.get(d)) for d in radar.DIMENSIONI}, "supervisore": supervisore,
            "anni_adeguamento": _vuoto(anni), "y_azioni": y, "stato_prima": stato_prima,
            "decisione": decisione or radar.AUTOMATICO}


def valori_riga_rr(r):
    return {d: r.get(c) for d, c in (("impatto", "Impatto"), ("probabilita", "Probabilita"),
                                     ("prossimita", "Prossimita"), ("velocity", "Velocity"))}


def stati_del_ciclo(scr, ciclo):
    """D-79: stato di ogni rischio del ciclo dai valori scritti (validati o no) e dalle decisioni del validatore. La usano
    valida e la riapertura, dopo aver applicato le decisioni."""
    regola = regola_radar(scr.x)
    _, anag = scr.leggi_anagrafica()
    info = {r["ID"]: r for _, r in anag}
    registro = scr.righe("tblRegister")
    prima = periodi_prima(scr, ciclo, 1)
    prec = {r["ID_Rischio"]: r for r in registro if prima and str(r["Ciclo"]) == str(prima[0])}
    azioni = scr.righe("tblAzioni")
    ingressi = []
    for r in registro:
        if str(r["Ciclo"]) != str(ciclo) or r.get("Stato") == DISMESSO:
            continue
        rid = r["ID_Rischio"]
        a = info.get(rid, {})
        anni = a.get("Anni_Adeguamento") if rid in info else r.get("Anni_Adeguamento")
        ingressi.append(ingresso_radar(rid, valori_riga_rr(r), stato_prima_di(prec.get(rid), rid in info),
                                       r.get("Decisione_Stato"), a.get("Attenzione_Supervisore") == "Sì", anni,
                                       y_azioni_di(azioni, rid, r.get("Periodo_Valutazione") or ciclo)))
    return radar.stati(ingressi, regola)


def applica_stati(scr, ciclo, stati, extra_motivo=None):
    """Scrive stato, motivo e movimento nelle righe del ciclo e allinea l'anagrafica (= il radar): chi esce la lascia
    senza buchi e i suoi KRI del ciclo escono di vigore (la storia resta; le azioni aperte restano nel Piano_azioni);
    chi entra riprende owner e anni di adeguamento dalla sua riga. extra_motivo: {id: testo da aggiungere al motivo}.
    Restituisce (entrati, usciti)."""
    registro = scr.righe("tblRegister")
    _, anag = scr.leggi_anagrafica()
    attivi = [r["ID"] for _, r in anag]
    dentro = {i for i, s in stati.items() if radar.nel_radar(s["stato"])}
    righe_ciclo = {}
    for n, r in enumerate(registro, start=1):
        if str(r["Ciclo"]) == str(ciclo) and r["ID_Rischio"] in stati:
            righe_ciclo[r["ID_Rischio"]] = (n, r)
            s = stati[r["ID_Rischio"]]
            motivo = s["motivo"] + ((extra_motivo or {}).get(r["ID_Rischio"]) or "")
            if (r.get("Stato"), r.get("Motivo_Stato"), r.get("Movimento") or None) != (s["stato"], motivo, s["movimento"] or None):
                scr.aggiorna("tblRegister", n, {"Stato": s["stato"], "Motivo_Stato": motivo, "Movimento": s["movimento"] or None})
    usciti = [i for i in attivi if i in stati and i not in dentro]
    for rid in usciti:
        scr.compatta_anagrafica(rid)
    for n, k in enumerate(scr.righe("tblKRI"), start=1):
        if str(k["Ciclo"]) == str(ciclo) and k["ID_Rischio"] in usciti and k["In_Vigore"] == "Sì":
            scr.aggiorna("tblKRI", n, {"In_Vigore": "No"})
    entrati = sorted(dentro - set(attivi))
    if entrati:
        pseudo = {"ciclo": ciclo, "rischi": [{"id_rischio": rid, "nome": righe_ciclo[rid][1]["Nome"],
                                              "event_type": righe_ciclo[rid][1]["Event_Type"],
                                              "driver": elenco(righe_ciclo[rid][1]["Driver"])} for rid in entrati]}
        scr.upsert_anagrafica(pseudo, {"owner_storico": {rid: righe_ciclo[rid][1].get("Owner") for rid in entrati
                                                         if righe_ciclo[rid][1].get("Owner") not in (None, OWNER_NUOVO)},
                                       "anni_storici": {rid: righe_ciclo[rid][1].get("Anni_Adeguamento") for rid in entrati}})
    return entrati, usciti


def scrivi_trimestrale(scr, payload, oggi, controlli=None, baseline=None):
    """A2: sequenza deterministica di scrittura del payload di A1. controlli =
    {"agente": output di A5, "esito": esito combinato, "superamento_testo": ...}:
    va nella tabella delle sintesi e nei rilievi dei rischi. baseline: quella
    letta da A1 e da A5; se manca si estrae dal registro (stessa cosa)."""
    mappa = scr.mappa
    if baseline is None:
        baseline = estrai_baseline(scr.x, mappa)
    completa_payload(payload, baseline)
    ciclo = payload["ciclo"]
    _, anag = scr.leggi_anagrafica()
    stato = {"oggi": a_data(oggi), "owner": {r["ID"]: r["Owner"] for _, r in anag}, "controlli": controlli}
    # Ciclo straordinario (D-75): solo i rischi indicati sono rivalutati; gli altri si riportano com'erano, gia' validati.
    decisione = baseline.get("straordinario")
    valutati = {x["id_rischio"] for x in payload["rischi"]}
    if decisione:
        nuovi = sorted(valutati - set(decisione.get("rischi_da_rivalutare") or []))
        evento = (payload.get("analisi_evento") or {}).get("evento")       # D-77: l'analisi completa e' nella knowledge di A7
        stato["straordinario_testo"] = (f"Deciso da {decisione['decisore']} il {decisione['data_decisione']}: "
                                        f"{decisione['motivo']} Rischi rivalutati: "
                                        f"{', '.join(sorted(valutati - set(nuovi))) or 'nessuno'}"
                                        + (f"; nuovi: {', '.join(nuovi)}" if nuovi else "") + "."
                                        + (f" Evento (analisi di A8): {evento}" if evento else ""))

    # 0. Registro unico (D-79): stato di ogni rischio del ciclo sui valori proposti, cosi' le viste sono gia' giuste
    #    durante la validazione (valida lo ricalcola sui valori validati). Entrano nel calcolo i rischi scritti da A1 e
    #    quelli che si riportano dal ciclo prima: in osservazione e non toccati da A1, o (straordinario) nel radar e non
    #    rivalutati. KRI e azioni si scrivono solo per i rischi nel radar.
    ciclo_prec = da_excel(scr.x.intervallo_nome("cicloCorrente").Value)
    regola = regola_radar(scr.x)
    info = {r["ID"]: r for _, r in anag}
    righe_prec = {r["ID_Rischio"]: r for r in scr.righe("tblRegister") if str(r["Ciclo"]) == str(ciclo_prec)}
    azioni_tutte = scr.righe("tblAzioni")
    riportati = [r for rid, r in righe_prec.items() if rid not in valutati and r.get("Stato") != DISMESSO
                 and ((stato_prima_di(r, rid in info) == radar.OSSERVAZIONE and rid not in info)
                      or (decisione and rid in info))]
    ingressi = []
    for x in payload["rischi"]:
        rid, p = x["id_rischio"], righe_prec.get(x["id_rischio"])
        ingressi.append(ingresso_radar(rid, x, stato_prima_di(p, rid in info), (p or {}).get("Decisione_Stato"),
                                       info.get(rid, {}).get("Attenzione_Supervisore") == "Sì",
                                       info[rid].get("Anni_Adeguamento") if rid in info else x.get("anni_adeguamento"),
                                       radar.y_azioni([a["orizzonte"] for a in x.get("azioni_mitigazione") or []])))
    for r in riportati:
        rid = r["ID_Rischio"]
        ingressi.append(ingresso_radar(rid, valori_riga_rr(r), stato_prima_di(r, rid in info), r.get("Decisione_Stato"),
                                       info.get(rid, {}).get("Attenzione_Supervisore") == "Sì",
                                       info[rid].get("Anni_Adeguamento") if rid in info else r.get("Anni_Adeguamento"),
                                       y_azioni_di(azioni_tutte, rid, r.get("Periodo_Valutazione") or r["Ciclo"])))
    stati = radar.stati(ingressi, regola)
    in_osservazione = [i for i, s in stati.items() if s["stato"] == radar.OSSERVAZIONE]
    if len(in_osservazione) > regola["max_osservazione"]:
        raise Fermo(f"Rischi in osservazione {len(in_osservazione)}, oltre il massimo di {regola['max_osservazione']} "
                    "(D-79): A1 deve lasciare fuori i meno rilevanti (fra i fenomeni non censiti, motivo troppo_lontano).")
    dentro = {i for i, s in stati.items() if radar.nel_radar(s["stato"])}
    # Escono dal radar solo i rischi a cui la regola ha dato uno stato fuori dal radar: un rischio del radar che manca
    # dall'output (lo ferma C1; qui la seconda difesa) resta in anagrafica e il controllo di copertura ferma il ciclo.
    fuori = {i for i, s in stati.items() if not radar.nel_radar(s["stato"])}
    stato.update(stati=stati, decisioni={rid: r.get("Decisione_Stato") for rid, r in righe_prec.items()})
    payload_radar = dict(payload, rischi=[x for x in payload["rischi"] if x["id_rischio"] in dentro])

    # 1-2. KRI. La tabella e' STORICA: una riga per KRI per ciclo, mai
    #    modificata dopo. Il ciclo aggiunge la sua fotografia: ogni KRI in
    #    vigore nel ciclo precedente, con il valore riletto ORA (mai ricopiato
    #    dal ciclo prima), e i KRI nuovi. Id nuovi = primo progressivo libero
    #    del rischio, mai la posizione nell'array; un id usato non si riusa.
    tutte = scr.righe("tblKRI")
    attivi = {r["ID"] for _, r in anag}          # un rischio dismesso non porta avanti i suoi KRI
    in_vigore = [r for r in tutte if r["Ciclo"] == ciclo_prec and r["In_Vigore"] == "Sì" and r["ID_Rischio"] in attivi]
    riletti = {z["kri_id"]: z for z in payload["ricalcolo_kri_ciclo_precedente"]}
    ignoti = sorted(set(riletti) - {r["KRI_ID"] for r in in_vigore})
    if ignoti:
        raise Fermo(f"Rilettura di KRI non in vigore nel ciclo {ciclo_prec}: {ignoti}")
    usati = {r["KRI_ID"] for r in tutte}
    spec_kri = mappa["tabelle"]["tblKRI"]
    proposti, proposti_per_rischio = {}, {}
    for ctx in contesti(payload_radar, spec_kri["righe_da"]):          # D-79: niente KRI per chi e' in osservazione
        k, rid = ctx["rischi[].kri_proposti[]"], ctx["rischi[]"]["id_rischio"]
        if k.get("kri_id"):
            k["_kri_id"] = k["kri_id"]
        else:
            n = 1
            while f"{rid}-K{n}" in usati:
                n += 1
            k["_kri_id"] = f"{rid}-K{n}"
            usati.add(k["_kri_id"])
        proposti_per_rischio.setdefault(rid, set()).add(k["_kri_id"])
        proposti[k["_kri_id"]] = valori_riga(spec_kri, ctx, stato)

    formule = {c["nome"] for c in spec_kri["colonne"] if c["sorgente"].startswith("formula:")}
    date_kri = {c["nome"] for c in spec_kri["colonne"] if c.get("formato") == "data"}
    righe_kri, usciti = [], []
    for r in in_vigore:                              # stesso ordine del ciclo precedente
        # Le date tornano da COM come testo ISO: si riscrivono come seriale (un KRI riportato in uno straordinario
        # tiene la sua Data_Rilevazione, che altrimenti finirebbe nella cella come testo).
        riga = {k: a_data(v) if k in date_kri and isinstance(v, str) else v for k, v in r.items() if k not in formule}
        riga["Ciclo"] = ciclo
        riga["Validazione"] = DA_VALIDARE           # la fotografia del ciclo va validata di nuovo
        if r["ID_Rischio"] in fuori:
            # D-79: il rischio esce dal radar (passa in osservazione): i suoi KRI escono di vigore, la storia resta.
            riga.update(In_Vigore="No", Validazione=r.get("Validazione"), Valore_Corrente=None, Data_Rilevazione=None,
                        Fonte_Rilevazione=None, Nota_Rilevazione=None)
            usciti.append(r["KRI_ID"])
            righe_kri.append(riga)
            continue
        if decisione and r["ID_Rischio"] not in valutati and r["KRI_ID"] not in riletti:
            # Straordinario (D-75): il KRI di un rischio non rivalutato resta com'era, valore e validazione compresi.
            riga["Validazione"] = r.get("Validazione")
            righe_kri.append(riga)
            continue
        if r["KRI_ID"] in proposti:                  # riproposto: definizione aggiornata
            nuova = proposti.pop(r["KRI_ID"])
            nuova.pop("Ciclo_Definizione")           # la data di nascita non cambia
            if nuova.get("Soglia_Attenzione") is None and nuova.get("Soglia_Allerta") is None:
                # A1 non propone soglie (D-53): restano quelle in vigore, fissate o accettate dal validatore.
                nuova.pop("Soglia_Attenzione")
                nuova.pop("Soglia_Allerta")
            riga.update(nuova)
        elif r["ID_Rischio"] in proposti_per_rischio:
            riga["In_Vigore"] = "No"                 # non riproposto: esce di vigore in questo ciclo
            usciti.append(r["KRI_ID"])
        z = riletti.get(r["KRI_ID"])
        valore = z["valore"] if z else None
        riga.update({
            "Valore_Corrente": valore,
            "Data_Rilevazione": a_data(payload["data_riferimento"]) if valore is not None else None,
            "Fonte_Rilevazione": z["fonte"] if z else None,
            "Nota_Rilevazione": z["commento"] if z else None,
        })
        righe_kri.append(riga)
    righe_kri.extend(proposti.values())              # nuovi: nessun valore finche' non vengono riletti
    # Capacita' delle viste: i KRI del ciclo e l'elenco dei KRI del foglio Indicatori
    # hanno un numero fisso di righe; oltre, perderebbero KRI in silenzio.
    for nome, n in (("capienzaKRICorrenti", sum(1 for r in righe_kri if r.get("In_Vigore", "Sì") == "Sì")),
                    ("capienzaElencoKRI", len(usati))):
        limite = scr.capienza(nome)
        if limite is not None and n > limite:
            raise RuntimeError(f"{n} KRI superano le {limite} righe della vista ({nome}). Alzare MAX_KRI_CORRENTI / "
                               "MAX_ELENCO_KRI in genera_dashboard.py e rigenerare il template.")
    scr.append("tblKRI", righe_kri)

    # 3. Anagrafica = il radar (D-79): prima del RiskRegister, cosi' l'Owner derivato di un rischio nuovo e' gia'
    #    "Da assegnare" e il controllo di copertura lo conta. Chi esce la lascia senza buchi; chi entra dall'osservazione
    #    riprende owner e anni di adeguamento dalla sua ultima riga.
    for rid in [i for i in attivi if i in fuori]:
        scr.compatta_anagrafica(rid)
    entranti_riportati = [r for r in riportati if r["ID_Rischio"] in dentro and r["ID_Rischio"] not in attivi]
    scr.upsert_anagrafica(
        dict(payload_radar, rischi=payload_radar["rischi"] + [
            {"id_rischio": r["ID_Rischio"], "nome": r["Nome"], "event_type": r["Event_Type"], "driver": elenco(r["Driver"])}
            for r in entranti_riportati]),
        dict(stato, owner_storico={rid: r.get("Owner") for rid, r in righe_prec.items() if r.get("Owner") not in (None, OWNER_NUOVO)},
             anni_storici={rid: r.get("Anni_Adeguamento") for rid, r in righe_prec.items()}))
    _, anag = scr.leggi_anagrafica()
    stato["owner"] = {r["ID"]: r["Owner"] for _, r in anag}

    # Capacita' del Piano_azioni: proposte e azioni aperte di ogni ciclo, chiuse del ciclo e del precedente.
    limite = scr.capienza("capienzaPianoAzioni")
    if limite is not None:
        nuove = len(list(contesti(payload_radar, mappa["tabelle"]["tblAzioni"]["righe_da"])))
        mostrate = sum(1 for r in scr.righe("tblAzioni") if r.get("ID_Azione") and
                       (r.get("Stato") not in STATI_AZIONE_CHIUSI or r.get("Ciclo") in (ciclo, ciclo_prec)))
        if mostrate + nuove > limite:
            raise RuntimeError(f"{mostrate + nuove} azioni superano le {limite} righe del Piano_azioni "
                               "(capienzaPianoAzioni). Alzare MAX_AZIONI_PIANO in genera_dashboard.py e rigenerare il template.")

    # 4. Append su RiskRegister (tutti i rischi scritti da A1, con lo stato), Azioni (solo il radar) e Sintesi_Cicli
    #    (commento di A1 e del challenger).
    for nome, fonte in (("tblRegister", payload), ("tblAzioni", payload_radar), ("tblSintesi", payload)):
        spec = mappa["tabelle"][nome]
        scr.append(nome, [valori_riga(spec, ctx, stato) for ctx in contesti(fonte, spec["righe_da"])])
    # 4-bis. Rischi riportati dal ciclo prima, validati come allora (Periodo_Valutazione dice da dove vengono: il
    #    Radar_Mosca ne prende le azioni): i rischi in osservazione che A1 non ha toccato (D-79) e, nello straordinario,
    #    quelli del radar non rivalutati (D-75). Il periodo e' cosi' completo.
    spec_rr = mappa["tabelle"]["tblRegister"]
    formule_rr = {c["nome"] for c in spec_rr["colonne"] if c["sorgente"].startswith("formula:")}
    date_rr = {c["nome"] for c in spec_rr["colonne"] if c.get("formato") == "data"}
    riportate = []
    for r in riportati:
        s = stati[r["ID_Rischio"]]
        nuova = {k: v for k, v in r.items() if k not in formule_rr}
        nuova.update(Ciclo=ciclo, Data_Riferimento=payload["data_riferimento"], Esito="Confermato", Variazioni="[]",
                     Rilievi=None, Data_Scrittura=oggi, Periodo_Valutazione=r.get("Periodo_Valutazione") or r["Ciclo"],
                     Stato=s["stato"], Motivo_Stato=s["motivo"], Movimento=s["movimento"] or None,
                     Decisione_Stato=r.get("Decisione_Stato") or radar.AUTOMATICO,
                     Owner=stato["owner"].get(r["ID_Rischio"]) or r.get("Owner"))
        riportate.append({k: a_data(v) if k in date_rr and isinstance(v, str) else v for k, v in nuova.items()})
    scr.append("tblRegister", riportate)

    # 5. Righe da validare: nello storico una per oggetto e campo proposto, Stato "Da decidere"; nella griglia
    #    del foglio Validazione una per oggetto (D-67), accanto alle settimane ancora da validare. I rischi riportati
    #    (in osservazione non toccati, straordinario) sono gia' validati.
    aggiungi_da_validare(scr, ciclo, "Rischio", lambda r: r["Ciclo"] == ciclo and r["ID_Rischio"] in valutati)
    aggiungi_da_validare(scr, ciclo, "KRI", lambda r: r["Ciclo"] == ciclo and r.get("Validazione") == DA_VALIDARE)
    aggiungi_da_validare(scr, ciclo, "Azione", lambda r: r["Ciclo"] == ciclo)
    ricostruisci_griglia(scr)

    # 6. Ciclo corrente: fa scorrere radar, trend e delta (D-75: anche i periodi delle viste).
    imposta_ciclo(scr, ciclo, payload["data_riferimento"])
    return {"kri_usciti": usciti, "stati": stati,
            "entrati": sorted(i for i, s in stati.items() if s["movimento"] == radar.ENTRATO),
            "usciti": sorted(i for i, s in stati.items() if s["movimento"] == radar.USCITO)}


def elenco(testo):
    """'DRV-AI, DRV-CYB' -> ['DRV-AI', 'DRV-CYB'] (colonne scritte con la trasformazione lista)."""
    return [x.strip() for x in str(testo or "").split(",") if x.strip()]


def rischi_osservazione(scr, ciclo):
    """D-79: righe del ciclo dei rischi in osservazione (Stato Osservazione), per la baseline, i controlli e A7."""
    return [r for r in scr.righe("tblRegister") if str(r["Ciclo"]) == str(ciclo) and r.get("Stato") == radar.OSSERVAZIONE]


def notizie_a3(scr, rid, dopo):
    """Notizie e flag di A3 su un rischio, datati dopo 'dopo' (spiegazioni.notizie_a3, senza Excel)."""
    import spiegazioni
    return spiegazioni.notizie_a3(scr, rid, dopo)

def righe_liste(scr, ciclo):
    """Righe del ciclo per le tre liste SharePoint, lette dal workbook appena
    scritto: contengono gia' i campi derivati (KRI_ID assegnati, Owner). Le tre
    tabelle del workbook sono gia' storiche: le liste ne sono una copia per chi
    interroga SharePoint. Nella variante con Power Automate il flow le carica
    cosi' come sono; nella variante locale restano come archivio del ciclo."""
    def solo(riga, spec):
        tolte = set(spec["colonne_escluse"])
        return {k: v for k, v in riga.items() if k not in tolte}
    liste = scr.mappa["liste_sharepoint"]
    return {"ciclo": ciclo, **{nome: [solo(r, spec) for r in scr.righe(spec["da_tabella"]) if r["Ciclo"] == ciclo]
                               for nome, spec in liste.items() if not nome.startswith("_")}}


def scrivi_settimanale(scr, payload):
    spec = scr.mappa["tabelle"]["tblNews"]
    presenti = {r["ID_Notizia"] for r in scr.righe("tblNews")}
    righe = [valori_riga(spec, ctx, {}) for ctx in contesti(payload, spec["righe_da"])
             if ctx["notizie[]"]["id_notizia"] not in presenti]
    scr.append("tblNews", righe)
    # Sintesi e flag di A3 (D-66): una riga per settimana; rilanciare la stessa settimana la aggiorna.
    spec_s = scr.mappa["tabelle"]["tblSettimane"]
    sintesi = valori_riga(spec_s, {"": payload}, {"oggi": a_data(dt.date.today().isoformat())})
    esistente = next((n for n, r in enumerate(scr.righe("tblSettimane"), start=1) if r["Settimana"] == payload["settimana"]), None)
    if esistente:
        scr.aggiorna("tblSettimane", esistente, sintesi)
    else:
        scr.append("tblSettimane", [sintesi])
    nuove = {r["ID_Notizia"] for r in righe}
    aggiungi_da_validare(scr, payload["settimana"], "Notizia", lambda r: r["ID_Notizia"] in nuove)
    ricostruisci_griglia(scr)              # le righe gia' compilate dal validatore (anche del ciclo) restano
    scr.imposta_nome("settimanaCorrente", a_data(payload["settimana"]))
    return len(righe)


# ================================================================ validazione umana
# Ogni proposta degli agenti diventa una riga dello storico (tabella tblValidazione,
# foglio Storico_Validazioni): Periodo, Oggetto, ID, Campo, Proposta_Agente, Stato
# "Da decidere". Il validatore NON scrive li': lavora nella griglia del foglio
# Validazione, una riga per oggetto (D-67), e il comando 'valida' trasforma ogni
# riga nelle decisioni campo per campo, le controlla e le applica. Proposta_Agente
# non si cancella mai: le righe Rettificato sono la base dati per l'apprendimento.
def aggiungi_da_validare(scr, periodo, oggetto, filtro):
    o = scr.mappa["validazione"]["oggetti"][oggetto]
    righe = []
    for r in scr.righe(o["tabella"]):
        if not filtro(r):
            continue
        for campo in o["campi"]:
            # Periodo sempre come TESTO ("2026Q3" o "2026-10-12"): per_cella lo scrive
            # con l'apostrofo, cosi' Excel non trasforma la data della settimana in un numero.
            righe.append({"Periodo": periodo, "Oggetto": oggetto,
                          "ID": r[o["id"]], "Nome": r[o["nome"]], "Campo": campo, "Proposta_Agente": r[campo],
                          "Stato": DA_DECIDERE})
    scr.append("tblValidazione", righe)
    return len(righe)


def da_decidere(scr, periodo):
    return [r for r in scr.righe("tblValidazione") if str(r["Periodo"]) == periodo and r["Stato"] == DA_DECIDERE]


def righe_griglia(righe_storico):
    """Numero di righe della griglia (oggetti) a cui corrispondono le righe dello storico (una per campo)."""
    return len({(r["Oggetto"], str(r["Periodo"]), str(r["ID"])) for r in righe_storico})


# ---------------------------------------------------------------- griglia del foglio Validazione (D-67)
# Una riga per oggetto dei periodi non ancora validati: la proposta (grigia) e il valore giallo, gia'
# compilato con la proposta. Si legge e si scrive SOLO con i nomi definiti VG_<oggetto>_<colonna> scritti
# dal generatore (le lettere delle colonne stanno solo li'). La riscrivono trimestrale, settimanale, valida,
# griglia e aggiorna-registro, conservando cio' che il validatore ha gia' scritto per le righe ancora da validare.
FOGLIO_GRIGLIA = "Validazione"
RESPINGI_SI = {"sì", "si"}
TITOLI_GRIGLIA = {
    "Rischio": ("RISCHI", "i quattro punteggi, gli anni di adeguamento e la decisione sullo stato (Automatico, Radar, "
                          "Osservazione: D-79)"),
    "KRI": ("KRI", "valore rilevato e soglie; Respingi = Sì toglie il KRI"),
    "Azione": ("AZIONI", "owner e orizzonte; Respingi = Sì non approva l'azione"),
    "Notizia": ("NOTIZIE", "rischio collegato e segnale; Respingi = Sì: notizia non rilevante (validazione facoltativa, D-17)"),
}


def oggetti_pendenti(righe):
    """Righe dello storico [(n, riga)] raggruppate per oggetto, nell'ordine di scrittura:
    {(oggetto, periodo, id): {"Nome": ..., "campi": {campo: proposta}, "righe": [(n, riga)]}}."""
    out = {}
    for n, r in righe:
        voce = out.setdefault((r["Oggetto"], str(r["Periodo"]), str(r["ID"])), {"Nome": r["Nome"], "campi": {}, "righe": []})
        voce["campi"][r["Campo"]] = r["Proposta_Agente"]
        voce["righe"].append((n, r))
    return out


def _colonna_o_niente(sessione, nome):
    """Valori di un intervallo con nome di una colonna; None se il nome non c'e'."""
    try:
        v = sessione.intervallo_nome(nome).Value
    except Exception:
        return None
    return [r[0] for r in v] if isinstance(v, tuple) else [v]


def leggi_griglia(sessione, mappa):
    """Cio' che e' scritto nella griglia: {(oggetto, periodo, id): {"riga": riga del foglio, "valori": {campo:
    valore giallo}, "motivazione": ..., "respingi": ...}}. {} per un registro senza griglia (fino al 2026-10-01)."""
    out = {}
    for oggetto, o in mappa["validazione"]["oggetti"].items():
        ids = _colonna_o_niente(sessione, f"VG_{oggetto}_ID")
        if ids is None:
            return {}
        periodi = _colonna_o_niente(sessione, f"VG_{oggetto}_Periodo")
        motivazioni = _colonna_o_niente(sessione, f"VG_{oggetto}_Motivazione")
        respingi = _colonna_o_niente(sessione, f"VG_{oggetto}_Respingi") if o["respingibile"] else None
        valori = {c: _colonna_o_niente(sessione, f"VG_{oggetto}_{c}") for c in o["campi"]}
        prima = sessione.intervallo_nome(f"VG_{oggetto}_ID").Row
        for i, ident in enumerate(ids):
            if ident in (None, ""):
                continue
            out[(oggetto, str(da_excel(periodi[i]) or ""), str(ident).strip())] = {
                "riga": prima + i, "valori": {c: da_excel(valori[c][i]) for c in o["campi"]},
                "motivazione": motivazioni[i], "respingi": respingi[i] if respingi else None}
    return out


def modifiche_vecchio_formato(righe):
    """Decisioni gia' scritte a mano nel vecchio foglio Validazione (una riga per campo, registri fino al
    2026-10-01) per gli oggetti ancora da decidere: diventano valori gialli, Respingi e Motivazione della griglia."""
    out = {}
    for chiave, voce in oggetti_pendenti(righe).items():
        valori, motivi, respinto, cambiato = {}, [], False, False
        for _, r in voce["righe"]:
            dec = str(r.get("Decisione") or "").strip().lower()
            rettificato = dec == "rettificato" and r.get("Valore_Validato") not in (None, "")
            valori[r["Campo"]] = r.get("Valore_Validato") if rettificato else r["Proposta_Agente"]
            respinto, cambiato = respinto or dec == "respinto", cambiato or rettificato
            motivo = str(r.get("Motivazione") or "").strip()
            if motivo and motivo not in motivi:
                motivi.append(motivo)
        if respinto or cambiato or motivi:
            out[chiave] = {"riga": None, "valori": valori, "motivazione": " · ".join(motivi) or None,
                           "respingi": "Sì" if respinto else None}
    return out


def _data_settimana(periodo):
    return f"{periodo[8:10]}/{periodo[5:7]}/{periodo[:4]}" if len(periodo) == 10 else periodo


def _titolo_sezione(oggetto, voci):
    nome, cosa = TITOLI_GRIGLIA[oggetto]
    if not voci:
        return f"{nome} — nessuna riga da validare"
    periodi = sorted({periodo for (_, periodo, _), _ in voci})
    quando = (("settimana del " if len(periodi) == 1 else "settimane del ") + ", ".join(_data_settimana(p) for p in periodi)
              if oggetto == "Notizia" else ("ciclo " if len(periodi) == 1 else "cicli ") + ", ".join(periodi))
    return f"{nome} — {quando} ({len(voci)} righe): {cosa}"


# ---------------------------------------------------------------- riapertura della validazione (D-76)
# Un ciclo gia' validato si puo' riaprire (comando riapri) quante volte serve: gli oggetti tornano nella griglia con il
# valore validato al posto della proposta, e valida li tratta cosi': riga non toccata = niente cambia; cella cambiata =
# rettifica senza il limite di un punto (scelta dell'utente del 07/10/2026), con la Motivazione; Respingi = Si' toglie
# un KRI, annulla un'azione, archivia una voce della lista. Un oggetto e' "riaperto" se il suo dato ha gia' una
# validazione (le proposte degli agenti hanno "Da validare"). Nello storico la decisione ha il suffisso (riapertura).
SUFFISSO_RIAPERTURA = " (riapertura)"
DECISIONE_RIAPERTURA = {"Accettato": "Invariato", "Rettificato": "Rettificato", "Respinto": "Respinto"}


def riga_dato(righe_tabella, o, ident, periodo):
    """(posizione 1-based, riga) del dato di un oggetto della griglia, per ID e periodo; un'azione riaperta puo' essere
    di un ciclo prima (il suo ID e' unico): allora basta l'ID. (None, None) se non c'e'."""
    trovate = [(i, d) for i, d in enumerate(righe_tabella, start=1) if str(d[o["id"]]) == str(ident)]
    for i, d in trovate:
        if o["periodo"] is None or str(d[o["periodo"]]) == str(periodo):
            return i, d
    return trovate[-1] if trovate and o["tabella"] == "tblAzioni" else (None, None)


def oggetti_riaperti(scr, chiavi):
    """Le chiavi (oggetto, periodo, id) da decidere che vengono da una riapertura: il dato ha gia' una validazione."""
    out, cache = set(), {}
    for oggetto, periodo, ident in chiavi:
        if oggetto == "Notizia":
            continue
        o = scr.mappa["validazione"]["oggetti"][oggetto]
        if o["tabella"] not in cache:
            cache[o["tabella"]] = scr.righe(o["tabella"])
        _, d = riga_dato(cache[o["tabella"]], o, ident, periodo)
        if d is not None and d.get("Validazione") != DA_VALIDARE:
            out.add((oggetto, str(periodo), str(ident)))
    return out


def ricostruisci_griglia(scr, modifiche=None):
    """Riscrive la griglia del foglio Validazione con gli oggetti ancora da decidere (storico, Stato 'Da decidere').
    Per una riga gia' presente (stesso oggetto, periodo e ID) conserva i valori gialli, la Motivazione e Respingi
    scritti dal validatore, oppure quelli dati in 'modifiche' (aggiorna-registro). Le righe libere restano nascoste.
    Restituisce {oggetto: righe scritte}."""
    s, mappa = scr.x, scr.mappa
    spec = mappa["validazione"]
    if modifiche is None:
        modifiche = leggi_griglia(s, mappa)
    tutte = scr.righe(spec["tabella"])
    pendenti = oggetti_pendenti([(n, r) for n, r in enumerate(tutte, start=1) if r["Stato"] == DA_DECIDERE])
    riaperti = oggetti_riaperti(scr, pendenti)
    tipo_kri = {(str(r["Ciclo"]), r["KRI_ID"]): r.get("Tipo") for r in scr.righe("tblKRI")}
    # D-71: le segnalazioni di A5 e dei controlli su ogni rischio (colonna Rilievi del RiskRegister) vanno nella
    # colonna Segnalazioni della griglia; quelle "da motivare" chiedono una Motivazione (⚑).
    segnalazioni = {(str(r["Ciclo"]), r["ID_Rischio"]): r.get("Rilievi") or None for r in scr.righe("tblRegister")}
    superati = {k for k, v in segnalazioni.items() if da_motivare(v)}
    rischio_azione = {(str(r["Ciclo"]), r["ID_Azione"]): r["ID_Rischio"] for r in scr.righe("tblAzioni")}
    # D-79: lo stato calcolato del rischio, con il motivo (si ricalcola a ogni validazione).
    stato_rischio = {(str(r["Ciclo"]), r["ID_Rischio"]): (f"{r.get('Stato')}: {r.get('Motivo_Stato')}" if r.get("Stato") else None)
                     for r in scr.righe("tblRegister")}
    ws = s.foglio(FOGLIO_GRIGLIA)
    scritte = {}
    for oggetto, o in spec["oggetti"].items():
        voci = [(k, v) for k, v in pendenti.items() if k[0] == oggetto]
        capienza = s.intervallo_nome(f"VG_{oggetto}_ID").Rows.Count
        if len(voci) > capienza:
            if oggetto == "Notizia":
                settimane = sorted({k[1] for k, _ in voci})
                raise Fermo(f"Le notizie da validare ({len(voci)}, settimane {', '.join(settimane)}) superano le {capienza} "
                            "righe del foglio Validazione. Validare prima le settimane piu' vecchie (una riga non toccata vale "
                            f"come accettata):  python esegui_ciclo_locale.py valida --periodo {settimane[0]} --validatore "
                            "\"<chi valida>\"  e poi rilanciare.")
            raise RuntimeError(f"Validazione: {len(voci)} righe di {oggetto} superano le {capienza} della griglia. Alzare la "
                               "capienza in genera_dashboard.py (GRIGLIA) e rigenerare il template.")
        righe = []
        for (_, periodo, ident), voce in voci:
            m = modifiche.get((oggetto, periodo, ident))
            obbligo = oggetto == "Rischio" and (periodo, ident) in superati and (oggetto, periodo, ident) not in riaperti
            riga = {"ID": ident, "Periodo": periodo, "Nome": ("⚑ " if obbligo else "") + str(voce["Nome"] or ""),
                    "Motivazione": m["motivazione"] if m else None}
            for c in o["campi"]:
                p = voce["campi"].get(c)
                riga[f"{c}_P"] = p if p not in (None, "") else ("n.v." if c == "Velocity" else "—")
                riga[c] = m["valori"].get(c, p) if m else p
            if o["respingibile"]:
                riga["Respingi"] = m["respingi"] if m else None
            if oggetto == "Rischio":
                riga["Appoggio"] = 1 if obbligo else None             # Motivazione obbligatoria (formato condizionale)
                riga["Segnalazioni"] = segnalazioni.get((periodo, ident))
                riga["Stato"] = stato_rischio.get((periodo, ident))
            elif oggetto == "Azione":
                riga["Appoggio"] = rischio_azione.get((periodo, ident)) or "-".join(ident.split("-")[1:3])   # per la Y di Mosca
            elif oggetto == "KRI":
                riga["Tipo"] = tipo_kri.get((periodo, ident)) or "—"
            elif oggetto == "Notizia":
                riga["Settimana"] = _data_settimana(periodo)
            righe.append(riga)
        nomi = ["ID", "Nome", "Motivazione", "Periodo", "Appoggio", *(f"{c}_P" for c in o["campi"]), *o["campi"]] + \
               (["Respingi"] if o["respingibile"] else []) + \
               {"Rischio": ["Segnalazioni", "Stato"], "KRI": ["Tipo"], "Notizia": ["Settimana"]}.get(oggetto, [])
        for nome in nomi:
            vettore = [per_cella(r.get(nome)) for r in righe] + [None] * (capienza - len(righe))
            s.intervallo_nome(f"VG_{oggetto}_{nome}").Value = tuple((v,) for v in vettore)
        # Altezza delle righe dai testi (Excel non la adatta da solo con le celle unite); prima le altezze, poi
        # si nascondono le righe libere: un'altezza impostata rende visibile una riga nascosta.
        blocco = s.intervallo_nome(f"VG_{oggetto}_righe")
        larghezza = lambda nome: (lambda rng: rng.ColumnWidth * rng.Cells(1, 1).MergeArea.Columns.Count)(
            s.intervallo_nome(f"VG_{oggetto}_{nome}"))
        testi = [("Nome", 9), ("Motivazione", 9)] + ([(c, 10) for c in o["campi"]] if oggetto in ("Azione", "Notizia") else []) \
            + ([("Segnalazioni", 8), ("Stato", 8)] if oggetto == "Rischio" else [])
        misure = {nome: larghezza(nome) for nome, _ in testi}
        for i, riga in enumerate(righe, start=1):
            altezza = max([righe_di_testo(riga[nome], misure[nome], punti) * punti * 1.35 + 6
                           for nome, punti in testi if isinstance(riga.get(nome), str) and riga[nome]] + [24])
            blocco.Rows(i).RowHeight = min(409, altezza)
        if righe:
            ws.Range(blocco.Rows(1), blocco.Rows(len(righe))).EntireRow.Hidden = False
        if len(righe) < capienza:
            ws.Range(blocco.Rows(len(righe) + 1), blocco.Rows(capienza)).EntireRow.Hidden = True
        titolo_sezione = _titolo_sezione(oggetto, voci)
        if any(k in riaperti for k, _ in voci):         # D-76: il grigio non e' una proposta, e' il valore validato
            titolo_sezione += (" — RIAPERTURA: in grigio il valore validato; una riga non toccata resta com'e'"
                               + {"KRI": "; Respingi = Sì toglie il KRI", "Azione": "; Respingi = Sì annulla l'azione"}.get(oggetto, ""))
        s.intervallo_nome(f"VG_{oggetto}_titolo").Value = per_cella(titolo_sezione)
        scritte[oggetto] = len(righe)
    # D-71: segnalazioni che riguardano il ciclo e non un rischio (es. C6), sopra la colonna Segnalazioni dei rischi.
    cicli_rischi = {k[1] for k in pendenti if k[0] == "Rischio"}
    sul_ciclo = [f"{r['Ciclo']}: {r['Rilievi_Ciclo']}" for r in scr.righe("tblSintesi")
                 if str(r["Ciclo"]) in cicli_rischi and r.get("Rilievi_Ciclo")]
    s.intervallo_nome("VG_Rischio_SegnalazioniCiclo").Value = per_cella(
        "Sul ciclo — " + "\n".join(sul_ciclo) if sul_ciclo else None)
    cicli = sorted({k[1] for k in pendenti if k[0] != "Notizia"})
    settimane = sorted({k[1] for k in pendenti if k[0] == "Notizia"})
    if not pendenti:
        stato = ("Niente da validare: tutte le proposte degli agenti sono state decise (dettaglio nel foglio "
                 "Storico_Validazioni).")
    else:
        parti = [f"ciclo {c} ({sum(1 for k in pendenti if k[1] == c)} righe)" for c in cicli] + \
                [f"settimana del {_data_settimana(w)} ({sum(1 for k in pendenti if k[1] == w)} notizie)" for w in settimane]
        stato = ("Da validare: " + " · ".join(parti) + " — poi, con il file chiuso:  python esegui_ciclo_locale.py valida "
                 "--periodo <ciclo o lunedi'> --validatore \"<chi valida>\"")
    s.intervallo_nome("valStato").Value = per_cella(stato)
    return scritte


def _numero(v):
    if isinstance(v, bool):
        return None
    if isinstance(v, (int, float)):
        return v
    try:
        return float(str(v).replace(",", "."))
    except ValueError:
        return None


def _uguali(a, b):
    """Stesso valore, anche se uno e' scritto come testo ("3" e 3, "7,5" e 7.5)."""
    na, nb = _numero(a), _numero(b)
    if na is not None and nb is not None:
        return na == nb
    return str(a if a is not None else "").strip() == str(b if b is not None else "").strip()


def variazioni_dopo_rettifica(testo, precedente, rettifiche, oggi):
    """Variazioni di un rischio coerenti con i valori VALIDATI. Per ogni campo
    rettificato si toglie la variazione dichiarata dall'agente e, se il valore
    validato differisce dal ciclo precedente, se ne aggiunge una che cita la
    rettifica e il suo motivo. La proposta originale resta nel foglio
    Validazione e nell'output di A1 archiviato."""
    var = json.loads(testo or "[]")
    dimensioni = {c for _, c in DIMENSIONI_ESITO}
    for campo, (valore, motivo) in rettifiche.items():
        if campo not in dimensioni:
            continue                                  # es. Anni_Adeguamento: non e' una dimensione, niente variazione
        dim = campo.lower()
        var = [v for v in var if v["dimensione"] != dim]
        # Da vuota (Velocity non valutata) a un valore, o il contrario, e' una variazione ("da n.v.").
        if precedente is not None and _vuoto(valore) != _vuoto(precedente.get(campo)):
            var.append({"dimensione": dim, "da": _vuoto(precedente.get(campo)), "a": _vuoto(valore),
                        "evidenza": f"Rettifica del validatore: {motivo}"[:600], "data_evidenza": oggi})
    return json.dumps(ordina_chiavi(var), ensure_ascii=False)


def controlla_valore(oggetto, campo, valore, contesto):
    """Il valore rettificato rispetta le stesse regole della proposta?
    Restituisce (valore normalizzato, problema o None)."""
    if oggetto == "Rischio":
        if campo == "Velocity" and valore in (None, ""):
            return None, None                         # vuota = non valutata (D-50)
        if campo == "Decisione_Stato":                # D-79: decisione del validatore sullo stato
            testo = str(valore or "").strip().capitalize()
            return (testo, None) if testo in radar.DECISIONI else \
                (valore, f"Decisione sullo stato deve essere una di {', '.join(radar.DECISIONI)} (trovato {valore!r})")
        if campo == "Anni_Adeguamento":               # D-60: anni stimati da A1, vuoto = non serve
            if valore in (None, ""):
                return None, None
            n = _numero(valore)
            if n is None or not 0 <= n <= 30:
                return valore, f"Anni_Adeguamento deve essere un numero da 0 a 30 o vuoto (trovato {valore!r})"
            return n, None
        n = _numero(valore)
        if n is None or n != int(n) or not 1 <= n <= 5:
            return valore, f"{campo} deve essere un intero da 1 a 5 (trovato {valore!r})"
        prec = contesto.get("precedente")
        if prec is not None and prec.get(campo) is not None and abs(int(n) - prec[campo]) > 1:
            return int(n), (f"{campo} {int(n)}: piu' di un punto dal ciclo precedente ({prec[campo]}), "
                            "contro la rubrica (regola di variazione 2)")
        return int(n), None
    if oggetto == "KRI":
        if campo == "Valore_Corrente" and valore in (None, ""):
            return None, None                         # vuoto = non rilevato
        n = _numero(valore)
        return (n, None) if n is not None else (valore, f"{campo} deve essere un numero (trovato {valore!r})")
    if oggetto == "Azione":
        if campo == "Orizzonte":
            return (valore, None) if valore in ORIZZONTI else (valore, f"Orizzonte deve essere uno di {ORIZZONTI}")
        testo = str(valore or "").strip()
        if len(testo) < 3 or controlli_a5.sembra_persona(testo):
            return testo, "Owner deve essere una funzione aziendale, non vuoto e non il nome di una persona"
        return testo, None
    if oggetto == "Notizia":
        if campo == "Segnale":
            return (valore, None) if valore in SEGNALI else (valore, f"Segnale deve essere uno di {SEGNALI}")
        ammessi = contesto["rischi"] | {NON_PRESIDIATO}
        return (valore, None) if valore in ammessi else \
            (valore, f"Rischio_ID deve essere un rischio del registro (nel radar o in osservazione) o {NON_PRESIDIATO}")
    return valore, f"oggetto sconosciuto {oggetto}"


def applica_validazione(scr, periodo, validatore, oggi):
    """Decisioni del periodo dalla griglia del foglio Validazione (D-67): per ogni campo di ogni riga, valore
    giallo uguale alla proposta = Accettato, diverso = Rettificato; Respingi = Sì = Respinto per tutto l'oggetto.
    Le controlla TUTTE, poi le applica; se una sola non va non applica niente (Fermo) e le elenca tutte, con la
    riga del foglio. Restituisce (esiti per campo, esiti per riga della griglia, registro delle decisioni)."""
    spec = scr.mappa["validazione"]
    oggetti = spec["oggetti"]
    tutte = scr.righe("tblValidazione")
    aperte = [(n, r) for n, r in enumerate(tutte, start=1) if str(r["Periodo"]) == periodo and r["Stato"] == DA_DECIDERE]
    if not aperte:
        # Lo Stato lo scrivono solo lo script ("Da decidere") e valida ("Applicata"): uno Stato vuoto o diverso
        # viene da una modifica a mano dello storico (successo il 01/10/2026 in Banca, quando si validava li').
        strane = [r for r in tutte if str(r["Periodo"]) == periodo and r["Stato"] not in (DA_DECIDERE, APPLICATA)]
        if strane:
            raise Fermo(f"Il periodo {periodo} ha {len(strane)} righe nel foglio Storico_Validazioni con lo Stato vuoto o "
                        f"modificato a mano (es. '{strane[0]['Stato'] or ''}'): valida considera solo 'Da decidere'.\n"
                        "Rimettere 'Da decidere' nella colonna Stato di quelle righe, salvare, chiudere e lanciare  "
                        "python esegui_ciclo_locale.py griglia  (le riporta nel foglio Validazione); poi validare. Il foglio "
                        "Storico_Validazioni non si modifica a mano: si valida nel foglio Validazione.")
        raise Fermo(f"Nessuna riga da validare per il periodo {periodo}: niente da validare.")
    pendenti = oggetti_pendenti(aperte)
    griglia = leggi_griglia(scr.x, scr.mappa)
    mancanti = [k for k in pendenti if k not in griglia]
    estranee = [(k, g) for k, g in griglia.items() if k[1] == periodo and k not in pendenti]
    if mancanti or estranee:
        raise Fermo(f"Il foglio Validazione non corrisponde alle proposte del periodo {periodo}: "
                    + "; ".join(([f"mancano {len(mancanti)} righe (es. " + ", ".join(f"{k[0]} {k[2]}" for k in mancanti[:5]) + ")"]
                                 if mancanti else []) +
                                ([f"{len(estranee)} righe con un ID che non e' da validare (es. "
                                  + ", ".join(f"{k[0]} {k[2]}, riga {g['riga']}" for k, g in estranee[:5]) + ")"]
                                 if estranee else []))
                    + ".\nNel foglio Validazione non si cambiano gli ID e non si inseriscono ne' cancellano righe. Per "
                      "ricostruirlo dalle proposte (cio' che e' gia' scritto nelle righe intatte resta):  python "
                      "esegui_ciclo_locale.py griglia")

    # Contesto dei controlli: riga del ciclo precedente di ogni rischio, rischi in anagrafica.
    _, anag = scr.leggi_anagrafica()
    prec_ciclo = periodi_prima(scr, periodo, 1)[0] if "Q" in periodo else None      # D-75: anche uno straordinario
    registro = scr.righe("tblRegister")
    precedenti = {r["ID_Rischio"]: r for r in registro if r["Ciclo"] == prec_ciclo}
    # Una notizia si collega a un rischio del radar o in osservazione (D-79).
    contesto_base = {"rischi": {r["ID"] for _, r in anag} |
                               {r["ID_Rischio"] for r in rischi_osservazione(scr, da_excel(scr.x.intervallo_nome("cicloCorrente").Value))}}
    # Rischi con una segnalazione da motivare di A5 o dei controlli (D-71; prima, D-56, un Bloccante di A5 superato con
    # --procedi-con-rilievi): la loro riga vuole una Motivazione anche se i valori restano quelli proposti.
    superati = {r["ID_Rischio"] for r in registro if str(r["Ciclo"]) == periodo and da_motivare(r.get("Rilievi"))}
    vuoti_ammessi = {("KRI", "Valore_Corrente"), ("Rischio", "Velocity"), ("Rischio", "Anni_Adeguamento")}

    riaperti = oggetti_riaperti(scr, pendenti)       # D-76: valore validato al posto della proposta
    e_riaperto = lambda r: (r["Oggetto"], str(r["Periodo"]), str(r["ID"])) in riaperti

    problemi, decisioni = [], []
    esiti_righe = {"Accettato": 0, "Rettificato": 0, "Respinto": 0}
    for chiave, voce in pendenti.items():
        oggetto, _, ident = chiave
        riaperto = chiave in riaperti
        g = griglia[chiave]
        etichetta = f"{oggetto} {ident} (riga {g['riga']} del foglio Validazione)"
        scritto_resp = str(g["respingi"] or "").strip()
        respinto = scritto_resp.lower() in RESPINGI_SI
        if scritto_resp and not respinto and scritto_resp.lower() != "no":
            problemi.append(f"{etichetta}: Respingi '{scritto_resp}' non valido: scrivere Sì oppure lasciare vuoto")
        motivo = str(g["motivazione"] or "").strip()
        cambiati = [c for c in voce["campi"] if not _uguali(g["valori"].get(c), voce["campi"][c])]
        if (respinto or cambiati) and len(motivo) < 10:
            cosa = "respinto" if respinto else "cambiato " + ", ".join(cambiati)
            problemi.append(f"{etichetta}: {cosa} senza una Motivazione di almeno 10 caratteri, con l'evidenza")
        elif oggetto == "Rischio" and ident in superati and not riaperto and len(motivo) < 10:
            problemi.append(f"{etichetta}: il rischio ha segnalazioni da motivare (⚑; colonna Segnalazioni dei controlli): "
                            "scrivere una Motivazione di almeno 10 caratteri anche se i valori restano quelli proposti")
        esiti_righe["Respinto" if respinto else "Rettificato" if cambiati else "Accettato"] += 1
        for n, r in voce["righe"]:
            campo, proposta = r["Campo"], r["Proposta_Agente"]
            et_campo = f"{oggetto} {ident} {campo} (riga {g['riga']})"
            if respinto:
                dec, valore = "Respinto", proposta
            elif campo in cambiati:
                dec, scritto = "Rettificato", g["valori"].get(campo)
                if scritto in (None, "") and (oggetto, campo) not in vuoti_ammessi:
                    problemi.append(f"{et_campo}: cella gialla vuota, scrivere il valore (la proposta era {proposta!r})")
                    valore = scritto
                else:
                    # D-76: in una riapertura il limite di un punto non vale (motivazione obbligatoria comunque).
                    valore, problema = controlla_valore(oggetto, campo, scritto,
                                                        dict(contesto_base, precedente=None if riaperto else precedenti.get(ident)))
                    if problema:
                        problemi.append(f"{et_campo}: {problema}")
            else:
                dec, valore = "Accettato", proposta
                if oggetto == "Rischio" and campo in DIMENSIONI_RISCHIO and proposta not in (None, "") and not riaperto:
                    # D-71: il salto di piu' di un punto (C3) non ferma piu' la scrittura: lo ferma qui, anche se la
                    # proposta e' accettata cosi' com'e'.
                    _, problema = controlla_valore(oggetto, campo, proposta, dict(contesto_base, precedente=precedenti.get(ident)))
                    if problema:
                        problemi.append(f"{et_campo}: proposta di A1 non accettabile ({problema}): scrivere nella cella "
                                        "gialla un valore a non piu' di un punto, con la Motivazione")
                if oggetto == "Azione" and campo == "Owner" and controlli_a5.sembra_persona(str(proposta or "")):
                    problemi.append(f"{et_campo}: Owner '{proposta}' sembra il nome di una persona: scrivere nella cella "
                                    "gialla una funzione aziendale (una persona non si accetta come owner)")
            decisioni.append((n, r, dec, valore, motivo or None))

    # Vincoli fra campi dello stesso oggetto: soglie dei KRI dopo le rettifiche.
    finali = {}
    for n, r, dec, valore, _ in decisioni:
        if dec != "Respinto":                        # un KRI respinto esce di vigore: le sue soglie non contano
            finali.setdefault((r["Oggetto"], r["ID"]), {})[r["Campo"]] = valore
    for (oggetto, ident), campi in finali.items():
        if oggetto == "KRI":
            dove = f"KRI {ident} (riga {griglia[(oggetto, periodo, str(ident))]['riga']} del foglio Validazione)"
            att, all_ = _numero(campi.get("Soglia_Attenzione")), _numero(campi.get("Soglia_Allerta"))
            if att is not None and all_ is not None and all_ < att:
                problemi.append(f"{dove}: Soglia allerta {all_} minore della Soglia attenzione {att}")
            if "Soglia_Attenzione" in campi and "Soglia_Allerta" in campi and (att is None) != (all_ is None):
                problemi.append(f"{dove}: soglie entrambe o nessuna (ne e' scritta una sola)")
    if problemi:
        raise Fermo(f"Validazione del periodo {periodo} NON applicata ({len(problemi)} problemi, nessuna modifica):\n  - "
                    + "\n  - ".join(problemi))

    # Applicazione ai dati, un oggetto alla volta.
    esiti = {"Accettato": 0, "Rettificato": 0, "Respinto": 0}
    per_oggetto = {}
    for n, r, dec, valore, motivo in decisioni:
        per_oggetto.setdefault((r["Oggetto"], r["ID"]), []).append((r["Campo"], dec, valore, motivo))
        esiti[dec] += 1
    data = a_data(oggi)
    anni_validati = {}
    for (oggetto, ident), voci in per_oggetto.items():
        o = oggetti[oggetto]
        righe_dati = scr.righe(o["tabella"])
        pos, dato = riga_dato(righe_dati, o, ident, periodo)
        respinto = any(dec == "Respinto" for _, dec, _, _ in voci)
        rettificato = any(dec == "Rettificato" for _, dec, _, _ in voci)
        riaperto = (oggetto, str(periodo), str(ident)) in riaperti
        if riaperto and not respinto and not rettificato:
            continue                                 # D-76: riga riaperta e non toccata: il dato resta com'era
        nuovi = {campo: valore for campo, dec, valore, _ in voci if dec == "Rettificato"}
        nuovi["Validazione"] = "Respinto" if respinto else "Rettificato" if rettificato else "Accettato"
        if oggetto == "Rischio":
            nuovi.update(Approvato_Da=validatore, Data_Validazione=data)
            prec = precedenti.get(ident)
            if rettificato:
                # Variazioni ed Esito seguono i valori validati: nessuna riga dice
                # "prossimita da 3 a 4" se la Banca ha deciso che resta 3.
                nuovi["Variazioni"] = variazioni_dopo_rettifica(
                    dato["Variazioni"], prec, {c: (v, m) for c, dec, v, m in voci if dec == "Rettificato"}, oggi)
            if rettificato and prec is not None and dato["Esito"] != "Nuovo":
                # Stessa regola della scrittura (D-51): contano le quattro dimensioni.
                valori = {c: _vuoto(nuovi.get(c, dato[c])) for _, c in DIMENSIONI_ESITO}
                nuovi["Esito"] = "Confermato" if all(valori[c] == _vuoto(prec.get(c)) for _, c in DIMENSIONI_ESITO) else "Variato"
            # D-60: gli anni di adeguamento validati (proposta accettata o rettifica) vanno nell'anagrafica,
            # da cui li legge il Radar_Mosca. Vuoto = nessuna stima: il valore gia' in anagrafica resta.
            # In una riapertura (D-76) solo se cambiati qui: l'anagrafica puo' essere stata corretta a mano.
            anni = _vuoto(nuovi.get("Anni_Adeguamento", dato.get("Anni_Adeguamento")))
            if anni is not None and (not riaperto or "Anni_Adeguamento" in nuovi):
                anni_validati[ident] = anni
        elif oggetto == "KRI":
            if respinto:
                nuovi["In_Vigore"] = "No"
            if "Valore_Corrente" in nuovi:
                # Valore e data della rilevazione vanno insieme (mai un valore senza data, mai una data senza valore).
                if nuovi["Valore_Corrente"] is None:
                    nuovi["Data_Rilevazione"] = None
                else:
                    if dato["Data_Rilevazione"] in (None, ""):
                        nuovi["Data_Rilevazione"] = a_data(data_periodo(scr, periodo))
                    if not dato["Fonte_Rilevazione"]:
                        nuovi["Fonte_Rilevazione"] = f"Rettifica del validatore ({validatore})"
        elif oggetto == "Azione" and riaperto:
            # D-76: un'azione gia' decisa resta nel suo stato (Approvata, In corso); Respingi = Si' la annulla.
            nuovi.update(Decisa_Da=validatore, Data_Decisione=data, **({"Stato": ANNULLATA} if respinto else {}))
        elif oggetto == "Azione":
            nuovi.update(Stato="Respinta" if respinto else "Approvata", Decisa_Da=validatore, Data_Decisione=data)
        elif oggetto == "Notizia" and respinto:
            nuovi["Segnale"] = "Non rilevante"
            nuovi.update({c["nome"]: 0 for c in scr.mappa["tabelle"]["tblNews"]["colonne"] if c["nome"].startswith("Imp_")})
        scr.aggiorna(o["tabella"], pos, nuovi)
    if anni_validati:
        cella = scr.x.intervallo_nome("ANA_Anni_Adeguamento")
        for pos, a in anag:
            if a["ID"] in anni_validati:
                cella.Cells(pos, 1).Value = anni_validati[a["ID"]]
    # D-79: lo stato di ogni rischio si ricalcola sui valori validati (e sulle decisioni del validatore); un rischio che
    # entra nel radar qui, senza i KRI e le azioni che A1 scrive solo per il radar, li avra' al ciclo dopo.
    movimenti = {"entrati": [], "usciti": []}
    if "Q" in periodo and str(periodo) == str(da_excel(scr.x.intervallo_nome("cicloCorrente").Value)):
        stati = stati_del_ciclo(scr, periodo)
        con_kri = {k["ID_Rischio"] for k in scr.righe("tblKRI") if str(k["Ciclo"]) == str(periodo) and k["In_Vigore"] == "Sì"}
        extra = {rid: "; entrato in validazione: KRI e azioni da definire al ciclo dopo" for rid, s in stati.items()
                 if radar.nel_radar(s["stato"]) and rid not in con_kri}
        movimenti["entrati"], movimenti["usciti"] = applica_stati(scr, periodo, stati, extra)
    # Nello storico una decisione su un oggetto riaperto ha il suffisso (riapertura): il valore di partenza non era una
    # proposta di un agente (base dati per l'apprendimento: si distinguono).
    etichetta_dec = lambda r, dec: DECISIONE_RIAPERTURA[dec] + SUFFISSO_RIAPERTURA if e_riaperto(r) else dec
    for n, r, dec, valore, motivo in decisioni:
        scr.aggiorna("tblValidazione", n, {
            "Decisione": etichetta_dec(r, dec), "Valore_Validato": None if dec == "Respinto" else valore, "Motivazione": motivo,
            "Validato_Da": validatore, "Data_Validazione": data, "Stato": APPLICATA})
    registro = [dict(r, Decisione=etichetta_dec(r, dec), Valore_Validato=None if dec == "Respinto" else valore,
                     Motivazione=motivo, Validato_Da=validatore, Data_Validazione=oggi, Stato=APPLICATA)
                for n, r, dec, valore, motivo in decisioni]
    # Le righe del periodo escono dalla griglia; quelle degli altri periodi restano con cio' che c'e' scritto.
    ricostruisci_griglia(scr)
    return esiti, esiti_righe, registro, movimenti


# ================================================================ verifiche
def copertura_python(scr, ciclo):
    """Stessa logica del controllo di copertura del Registro (nomi coperturaAnagrafica e
    coperturaValutati), calcolata sui dati appena scritti.
    Serve perche' chi usa i dati senza Excel non ha il valore del foglio."""
    _, anag = scr.leggi_anagrafica()
    ids = [r["ID"] for _, r in anag if str(r["ID"]).startswith("NFR-")]
    valutati = {r["ID_Rischio"] for r in scr.righe("tblRegister") if r["Ciclo"] == ciclo}
    return len(ids), sum(1 for i in ids if i in valutati)


def colonna_nome(sessione, nome):
    """Valori di un intervallo con nome di una colonna, come lista."""
    v = sessione.intervallo_nome(nome).Value
    return [r[0] for r in v] if isinstance(v, tuple) else [v]


def copertura_foglio(sessione):
    return (int(sessione.intervallo_nome("coperturaAnagrafica").Value),
            int(sessione.intervallo_nome("coperturaValutati").Value))


def segnali_sopra_soglia(sessione):
    """Rischi con segnali netti delle notizie oltre la soglia (Registro, blocco per posizione)."""
    return [(i, b) for i, b in zip(colonna_nome(sessione, "posID"), colonna_nome(sessione, "posBadge"))
            if i and str(b)[:1] in "▲▼"]


def aree_non_presidiate(sessione):
    return [c for c, s in zip(colonna_nome(sessione, "presidioCodici"), colonna_nome(sessione, "presidioStato"))
            if s == "AREA NON PRESIDIATA"]


def formule_mancanti(sessione, mappa):
    """Ogni riga di ogni colonna formula deve contenere la formula. Una cella
    formula sovrascritta con un valore non da' errore: resta vuota, in silenzio."""
    mancanti = []
    for nome, spec in mappa["tabelle"].items():
        lo = sessione.tabella(nome)
        if lo.DataBodyRange is None:
            continue
        for c in spec["colonne"]:
            if c["sorgente"].startswith("formula:"):
                celle = lo.ListColumns(c["nome"]).DataBodyRange
                for i in range(1, celle.Rows.Count + 1):
                    if not celle.Cells(i, 1).HasFormula:
                        mancanti.append(f"{nome}.{c['nome']} riga {i}")
    return mancanti


def verifica_dopo_scrittura(sessione, scr, ciclo):
    sessione.ricalcola()
    mancanti = formule_mancanti(sessione, scr.mappa)
    if mancanti:
        raise Fermo("Formule mancanti dopo la scrittura: " + "; ".join(mancanti[:10]))
    errori = sessione.errori_formula()
    if errori:
        raise Fermo("Errori di formula dopo la scrittura: " + "; ".join(f"{e[0]}!{e[1]} {e[2]}" for e in errori[:10]))
    py, fg = copertura_python(scr, ciclo), copertura_foglio(sessione)
    if py != fg:
        raise Fermo(f"Copertura calcolata in Python {py} diversa da quella del foglio {fg}.")
    if fg[0] != fg[1]:
        raise Fermo(f"CICLO INCOMPLETO: {fg[1]} rischi valutati su {fg[0]} in anagrafica.")
    return fg


# ================================================================ baseline
# Valori di un rischio che A1 riceve (e rivaluta). Gap_Controlli non c'e' piu' (D-49), la Confidence
# nemmeno (D-58: la rilevanza sta sulle fonti); il presidio dei controlli e gli anni di adeguamento
# (anagrafica) sono passati come contesto.
DIMENSIONI_BASELINE = [("impatto", "Impatto"), ("velocity", "Velocity"), ("prossimita", "Prossimita"),
                       ("probabilita", "Probabilita")]


def colonna(riga, nome, mappa, tabella="tblRegister"):
    """Valore di una colonna di una riga letta dal registro; per un registro di un template
    precedente, la colonna col nome vecchio (colonne_rinominate della mappa, es. Severity -> Impatto)."""
    if nome in riga:
        return riga[nome]
    vecchi = [v for v, n in mappa.get("colonne_rinominate", {}).get(tabella, {}).items() if n == nome]
    return next((riga[v] for v in vecchi if v in riga), None)


def estrai_baseline(sessione, mappa, straordinario=None):
    """Baseline per il prossimo ciclo: e' l'input di A1, A3, A4 e A5. Con 'straordinario' (la decisione archiviata da
    baseline --straordinario, D-75) il ciclo da valutare e' quel periodo AAAAQn-Sk, con i rischi da rivalutare."""
    scr = Scrittore(sessione, mappa)
    ciclo_prec = da_excel(sessione.intervallo_nome("cicloCorrente").Value)
    register = scr.righe("tblRegister")
    _, anag = scr.leggi_anagrafica()
    per_ciclo = {}
    for r in register:
        per_ciclo.setdefault(r["Ciclo"], {})[r["ID_Rischio"]] = r
    correnti = per_ciclo.get(ciclo_prec, {})
    date_prec = [r["Data_Riferimento"] for r in correnti.values() if r["Data_Riferimento"]]
    storico_cicli = periodi_prima(scr, ciclo_prec, 2) if ciclo_prec else []

    rischi = []
    for _, a in anag:
        r = correnti.get(a["ID"])
        if r is None:
            continue                      # in anagrafica ma mai valutato: lo segnala C1
        rischi.append({
            "id_rischio": a["ID"], "nome": a["Nome"], "event_type": a["Event_Type"],
            "driver": [d.strip() for d in str(a["Driver"]).split(",")], "owner": a["Owner"],
            "presidio_controlli": a.get("Presidio_Controlli") or PRESIDIO_NUOVO,
            "anni_adeguamento": _vuoto(a.get("Anni_Adeguamento")),
            "attenzione_supervisore": a.get("Attenzione_Supervisore") == "Sì",
            **{v: _vuoto(colonna(r, k, mappa)) for v, k in DIMENSIONI_BASELINE},
            "esito_precedente": r["Esito"], "razionale": r["Razionale"],
            "fonti": json.loads(r["Fonti"] or "[]"),
            # D-79: stato nel registro unico e decisione del validatore (la regola li usa per il ciclo dopo).
            "stato": r.get("Stato") if r.get("Stato") in radar.STATI else radar.RADAR,
            "decisione_stato": r.get("Decisione_Stato") or radar.AUTOMATICO,
            "storico": [{"ciclo": c, **{v: _vuoto(colonna(per_ciclo[c][a["ID"]], k, mappa)) for v, k in DIMENSIONI_BASELINE}}
                        for c in storico_cicli if a["ID"] in per_ciclo.get(c, {})],
        })
    # D-79: i rischi in osservazione (fuori dall'anagrafica, che e' il radar); A1 li riscrive solo con evidenza nuova.
    in_osservazione = []
    for r in correnti.values():
        if r.get("Stato") != radar.OSSERVAZIONE or r["ID_Rischio"] in {a["ID"] for _, a in anag}:
            continue
        rid = r["ID_Rischio"]
        in_osservazione.append({
            "id_rischio": rid, "nome": r["Nome"], "event_type": r["Event_Type"], "driver": elenco(r["Driver"]),
            "descrizione": r["Descrizione"], "anni_adeguamento": _vuoto(r.get("Anni_Adeguamento")),
            **{v: _vuoto(colonna(r, k, mappa)) for v, k in DIMENSIONI_BASELINE},
            "orizzonte_anni": _vuoto(r.get("Orizzonte_Anni")), "segnale_avvicinamento": r.get("Segnale_Avvicinamento"),
            "esito_precedente": r["Esito"], "razionale": r["Razionale"], "fonti": json.loads(r["Fonti"] or "[]"),
            "stato": radar.OSSERVAZIONE, "motivo_stato": r.get("Motivo_Stato"),
            "decisione_stato": r.get("Decisione_Stato") or radar.AUTOMATICO,
            "storico": [{"ciclo": c, **{v: _vuoto(colonna(per_ciclo[c][rid], k, mappa)) for v, k in DIMENSIONI_BASELINE}}
                        for c in storico_cicli if rid in per_ciclo.get(c, {})],
            **notizie_a3(scr, rid, max(date_prec) if date_prec else None)})
    attivi = {a["ID"] for _, a in anag}        # solo i rischi in anagrafica: un rischio dismesso esce del tutto
    kri = [{"kri_id": k["KRI_ID"], "id_rischio": k["ID_Rischio"], "tipo": k.get("Tipo") or None,   # D-64
            "nome": k["Nome"], "unita": k["Unita"],
            "fonte_dati": k["Fonte_Dati"], "soglia_attenzione": k["Soglia_Attenzione"],
            "soglia_allerta": k["Soglia_Allerta"], "valore_corrente": k["Valore_Corrente"],
            "data_rilevazione": k["Data_Rilevazione"]}
           for k in scr.righe("tblKRI") if k["Ciclo"] == ciclo_prec and k["In_Vigore"] == "Sì" and k["ID_Rischio"] in attivi]
    azioni = [{"id_azione": z["ID_Azione"], "id_rischio": z["ID_Rischio"], "descrizione": z["Descrizione"],
               "owner": z["Owner"], "stato": z["Stato"], "orizzonte": z.get("Orizzonte"), "ciclo": str(z.get("Ciclo") or "")}
              for z in scr.righe("tblAzioni") if z["Stato"] not in STATI_AZIONE_CHIUSI and z["ID_Rischio"] in attivi]
    prossimo = ciclo_successivo(trimestre_di(ciclo_prec)) if ciclo_prec else None
    data_prossimo = fine_trimestre(prossimo) if prossimo else None
    if straordinario:
        prossimo, data_prossimo = straordinario["periodo"], straordinario["data_riferimento"]
    extra = {"straordinario": {k: straordinario[k] for k in ("rischi_da_rivalutare", "motivo", "decisore", "data_decisione")}} \
        if straordinario else {}
    return {
        "ciclo_precedente": ciclo_prec or None,
        "data_riferimento_precedente": max(date_prec) if date_prec else None,
        "ciclo_da_valutare": prossimo,
        "data_riferimento": data_prossimo,
        **extra,
        "rischi": rischi,
        "rischi_in_osservazione": in_osservazione,
        "kri_in_vigore": kri,
        "azioni_aperte": azioni,
        # D-79: la regola del registro unico, per A1 (guida di scrittura) e per i controlli dello script.
        "regola_radar": regola_radar(sessione),
    }


# ================================================================ archivio
# Struttura della cartella di uscita (in esercizio: la library Archivio_Cicli):
#   Baseline_corrente.json              input degli agenti per il prossimo run
#   Cicli/<ciclo>/                      il run trimestrale riuscito: output degli
#                                       agenti, esito dei controlli, baseline usata,
#                                       NFR_Registro_<ciclo>.xlsx, righe per le liste
#   Cicli/<ciclo>/tentativo_<ora>/      ogni tentativo, anche quelli fermati
#   Settimane/<lunedi'>/                un run settimanale: output di A3,
#                                       NFR_Registro_<lunedi'>.xlsx
#   Backup/                             il workbook vivo PRIMA di ogni scrittura
def _cartella(conf, *parti):
    c = conf["cartella_uscita"].joinpath(*parti)
    c.mkdir(parents=True, exist_ok=True)
    return c


def _scrivi_json(percorso, dati):
    percorso.write_text(json.dumps(dati, ensure_ascii=False, indent=2), encoding="utf-8")
    return percorso


def _scrivi_baseline(conf, dati):
    """Baseline_corrente in due copie identiche: .json per lo script e per gli
    allegati, .txt per la knowledge di Agent Builder (che dalle library legge
    .txt, .docx, .pdf..., non .json). Accanto, l'allegato di A1 (D-69):
    Input_A1_<ciclo>.txt con baseline, controlli di A5 e guida di scrittura.
    Un file del kernel mancante non ferma niente (la baseline basta ad A1): avviso."""
    percorso = _scrivi_json(_cartella(conf) / "Baseline_corrente.json", dati)
    shutil.copy2(percorso, percorso.with_suffix(".txt"))
    allegato, mancanti = input_a1.scrivi(_cartella(conf), dati, conf["kernel"], dt.date.today().isoformat())
    if mancanti:
        print(f"Avviso: nel kernel ({conf['kernel']}) mancano {', '.join(mancanti)}: l'allegato di A1 {allegato.name} ha "
              "solo la baseline. Copiare nella library Kernel tutti i file di 01_Kernel del pacchetto.")
    return percorso


def _valida_o_ferma(payload, schema_file, conf, etichetta):
    errori = valida(payload, carica_json(file_kernel(conf, schema_file)))
    if errori:
        raise Fermo(f"{etichetta} non conforme allo schema:\n  - " + "\n  - ".join(errori))


# Da quando il registro e' salvato, un errore NON e' piu' "workbook non
# salvato": main() lo dice in modo diverso e avverte di non rilanciare.
SALVATO = {"registro": None, "backup": None}


def _salva_con_backup(sessione, workbook, conf):
    copia = _cartella(conf, "Backup") / f"{workbook.stem}_{dt.datetime.now():%Y%m%d_%H%M%S}{workbook.suffix}"
    shutil.copy2(workbook, copia)                    # stato PRIMA della scrittura
    sessione.salva()
    SALVATO.update(registro=workbook, backup=copia)
    return copia


def _excel_di_output(workbook, cartella, etichetta):
    """Copia del workbook appena salvato, con il nome del ciclo o della settimana:
    e' l'Excel di output del run, che non cambia piu'."""
    uscita = cartella / f"{workbook.stem}_{etichetta}{workbook.suffix}"
    shutil.copy2(workbook, uscita)
    return uscita


# ================================================================ precontrollo (D-69)
# Le regole stanno in precontrollo.py (senza Excel: le usa anche la skill di Copilot Studio, D-70); qui il comando.
def comando_precontrollo(arg, conf):
    """Output di A1 controllato prima di A5, senza Excel e senza toccare il registro.
    Restituisce il codice di uscita: 1 se un punto fermerebbe il ciclo."""
    payload = leggi_payload(arg.payload, "Output di A1")
    file_base = Path(arg.baseline) if arg.baseline else conf["cartella_uscita"] / "Baseline_corrente.json"
    if not file_base.exists():
        raise Fermo(f"Baseline non trovata: {file_base}. Lanciare prima: python esegui_ciclo_locale.py baseline")
    baseline = leggi_payload(file_base, "Baseline")
    esito = precontrolla(payload, baseline, carica_json(file_kernel(conf, "schema_output_A1.json")))
    ciclo = ciclo_di(payload, baseline)
    da_correggere, da_verificare = conta(esito)
    file = conf["cartella_uscita"] / "Cicli" / ciclo / f"Correzione_A1_{ciclo}.txt"
    firma = f"Impronta dell'output di {agente_di(ciclo)}: {impronta(payload)}"
    if not da_correggere and not da_verificare:
        if file.exists():
            file.unlink()                            # messaggio di un output precedente: non vale piu'
        print(f"{riga_esito(ciclo, esito)} Ora il comando trimestrale; se si usa A5 (facoltativo), prima allegargli "
              f"l'output di {agente_di(ciclo)} e Baseline_corrente.json e scrivere \"Esegui i nove controlli\".\n{firma}")
        return 0
    testo = messaggio_correzione(ciclo, esito)
    _cartella(conf, "Cicli", ciclo)
    file.write_text(testo, encoding="utf-8")
    print(f"{riga_esito(ciclo, esito)}\n{firma}\n"
          f"Messaggio per {agente_di(ciclo)}: {file}\n(aprirlo con Blocco note, copiarlo tutto e incollarlo nella chat di "
          f"{agente_di(ciclo)})\n\n{testo}\n"
          + (f"Dopo la risposta di {agente_di(ciclo)}: salvarla di nuovo e ripetere il precontrollo. Il registro non e' stato toccato."
             if da_correggere else
             "Nessun punto ferma il ciclo: si puo' lanciare trimestrale (questi punti andranno nella colonna Segnalazioni "
             f"del foglio Validazione), oppure chiedere prima ad {agente_di(ciclo)} di rivederli."))
    return 1 if da_correggere else 0


def comando_trimestrale(arg, conf):
    from excel_com import SessioneExcel
    mappa = carica_mappa(conf)
    if getattr(arg, "procedi_con_rilievi", False):
        # Fino al 05/10/2026 (D-56) serviva a non fermarsi sui Bloccanti di A5; dal 06/10 (D-71) vanno sempre in
        # validazione: resta accettata solo per non rompere i comandi gia' in uso, e lo dice.
        print("Nota: --procedi-con-rilievi (con --motivo e --decisore) non serve piu': i rilievi di A5 vanno sempre nella "
              "colonna Segnalazioni del foglio Validazione e chiedono una Motivazione al validatore. Si puo' togliere.")
    payload = leggi_payload(arg.payload, "Output di A1")
    _valida_o_ferma(payload, "schema_output_A1.json", conf, "Output di A1")
    ciclo = payload["ciclo"]
    cartella = _cartella(conf, "Cicli", ciclo)
    # Ogni tentativo ha la sua sottocartella: un ciclo fermato e poi rilanciato
    # lascia traccia di entrambi. Solo il tentativo riuscito e' copiato alla
    # radice della cartella del ciclo.
    tentativo = _cartella(conf, "Cicli", ciclo, f"tentativo_{dt.datetime.now():%Y%m%d_%H%M%S}")
    _scrivi_json(tentativo / f"A1_{ciclo}.json", payload)

    # Ciclo straordinario (D-75): vale la decisione archiviata da baseline --straordinario.
    decisione = None
    if e_straordinario(ciclo):
        file_dec = conf["cartella_uscita"] / "Cicli" / ciclo / f"Straordinario_{ciclo}.json"
        if not file_dec.exists():
            raise Fermo(f"{ciclo} e' un ciclo straordinario, ma non c'e' la decisione ({file_dec}). Prima: python "
                        "esegui_ciclo_locale.py baseline --straordinario --rischi NFR-nn,... --motivo \"...\" --decisore \"...\", "
                        "poi A1 con l'allegato Input_A1 di quel periodo.")
        decisione = carica_json(file_dec)
    # Baseline letta dal workbook in sola lettura: nessun byte scritto finche'
    # i controlli non sono superati.
    with SessioneExcel(conf["workbook"], sola_lettura=True) as s:
        controlla_versione(s)
        baseline = estrai_baseline(s, mappa, straordinario=decisione)
        pendenti = da_decidere(Scrittore(s, mappa), baseline["ciclo_precedente"] or "")
    if pendenti:
        raise Fermo(f"Il ciclo precedente {baseline['ciclo_precedente']} non e' ancora validato: {righe_griglia(pendenti)} righe "
                    "da validare nel foglio Validazione. Validarlo prima (comando valida): un ciclo nuovo non si "
                    "costruisce su valutazioni non accettate.")
    _scrivi_json(tentativo / f"Baseline_usata_{ciclo}.json", baseline)
    meccanico = controlli_a5.controlla(payload, baseline)
    agente = None
    if arg.challenger:
        agente = leggi_payload(arg.challenger, "Output di A5")
        _valida_o_ferma(agente, "schema_output_A5.json", conf, "Output di A5")
        if decisione:                                # D-75: A5 non sa dello straordinario; i rischi non rivalutati non contano
            nel_payload = {x["id_rischio"] for x in payload["rischi"]}
            agente["rilievi"] = [x for x in agente["rilievi"] if not x["id_rischio"] or x["id_rischio"] in nel_payload]
        # L'esito di A5 vale solo per l'output di A1 che ha esaminato: un'approvazione
        # di un altro ciclo (o di un'altra versione) non si riusa.
        if agente["ciclo"] != ciclo:
            raise Fermo(f"L'esito di A5 ({arg.challenger}) e' del ciclo {agente['ciclo']}, non del {ciclo}: "
                        "far esaminare ad A5 QUESTO output di A1 e salvarne la risposta.")
        estranei = sorted({x["id_rischio"] for x in agente["rilievi"] if x["id_rischio"]} - {x["id_rischio"] for x in payload["rischi"]})
        if estranei:
            raise Fermo(f"L'esito di A5 cita rischi che non sono nell'output di A1 ({estranei}): A5 ha esaminato un "
                        "altro output. Rifare A5 su questo output di A1.")
        _scrivi_json(tentativo / f"A5_{ciclo}.json", agente)
    esito = controlli_a5.combina(meccanico, agente)
    oggi = dt.date.today().isoformat()
    da_mot = esito["da_motivare"]
    rapporto = _scrivi_json(tentativo / f"Esito_controlli_{ciclo}.json",
                            {"meccanico": meccanico, "agente": agente, "esito": esito["esito"],
                             "da_motivare": da_mot, "a5_usato": agente is not None})
    if esito["esito"] != "Approvato":
        # Solo difetti di integrita' (D-71): il messaggio per A1 e' lo stesso del precontrollo.
        bloccanti = [f"{x['controllo']} {x['id_rischio'] or ''} {x['descrizione']}"
                     for x in esito["rilievi"] if x["gravita"] == controlli_a5.BLOCCANTE]
        correzione = cartella / f"Correzione_A1_{ciclo}.txt"
        correzione.write_text(messaggio_correzione(
            ciclo, precontrolla(payload, baseline, carica_json(file_kernel(conf, "schema_output_A1.json")))), encoding="utf-8")
        raise Fermo("Ciclo da rivedere (difetti che renderebbero incoerente il registro):\n  - " + "\n  - ".join(bloccanti)
                    + f"\nMessaggio per {agente_di(ciclo)}: {correzione}\n(aprirlo con Blocco note, copiarlo tutto nella chat "
                    f"di {agente_di(ciclo)}, salvare "
                    f"la nuova risposta e rilanciare trimestrale)\nRapporto: {rapporto}")
    testo_superamento = (f"Segnalazioni da motivare in validazione: {len(da_mot)} (controlli "
                         f"{sum(1 for x in da_mot if x['origine'] == 'script')}, A5 {sum(1 for x in da_mot if x['origine'] == 'A5')})."
                         if da_mot else None)

    with SessioneExcel(conf["workbook"]) as s:
        scr = Scrittore(s, mappa)
        nota_archiviata = archivia_nota_quadro(s, scr, baseline["ciclo_precedente"])      # D-72
        esito_scrittura = scrivi_trimestrale(scr, payload, oggi, baseline=baseline,
                                             controlli={"agente": agente, "esito": esito,
                                                        "superamento_testo": testo_superamento})
        copertura = verifica_dopo_scrittura(s, scr, ciclo)
        stati = esito_scrittura["stati"]
        capienza_radar = regola_radar(s)["capienza"]
        prepara_report(s)
        copia = _salva_con_backup(s, conf["workbook"], conf)
        nuova_baseline = estrai_baseline(s, mappa)
        liste = righe_liste(scr, ciclo)
        rng_anag, occupate = scr.leggi_anagrafica()
        posti_liberi = rng_anag.Rows.Count - len(occupate)
        msg_a7 = aggiorna_spiegazioni(s, scr, conf, payload=payload)
    # Dopo il salvataggio, prima cio' che serve al prossimo run (la baseline),
    # per ultimo la copia dell'Excel, che fallisce se qualcuno ha aperto il file.
    file_baseline = _scrivi_baseline(conf, nuova_baseline)
    _scrivi_json(cartella / f"Righe_liste_{ciclo}.json", liste)
    for f in tentativo.iterdir():                    # il tentativo riuscito diventa l'archivio del ciclo
        shutil.copy2(f, cartella / f.name)
    excel = _excel_di_output(conf["workbook"], cartella, ciclo)

    fuori = sorted(x["id_rischio"] for x in payload["rischi"] if x["event_type"] == controlli_a5.FUORI_PERIMETRO)
    riclass = sorted(x["id_rischio"] for x in payload["rischi"]
                     if x["event_type"] in controlli_a5.CATEGORIE and x["id_rischio"] in {b["id_rischio"] for b in baseline["rischi"]
                                                                                       if b["event_type"] not in controlli_a5.CATEGORIE})
    if fuori or riclass:
        print("TASSONOMIA (D-74): " + (f"riclassificati nelle categorie interne {', '.join(riclass)}. " if riclass else "")
              + (f"FUORI PERIMETRO {', '.join(fuori)}: restano fuori dal radar; la funzione di rischio decide se toglierli con "
                 "dismetti (guida, sezione 3-bis)." if fuori else ""))
    print((f"CICLO STRAORDINARIO {ciclo} (D-75): rivalutati {', '.join(sorted(x['id_rischio'] for x in payload['rischi']))}; "
           "gli altri rischi sono riportati dal ciclo prima, gia' validati.\n" if decisione else "") +
          f"Ciclo {ciclo} scritto: {copertura[1]}/{copertura[0]} rischi, zero errori di formula.\n"
          f"KRI: {len(liste['KRI_Storico'])} righe di storico per il ciclo; usciti di vigore: {esito_scrittura['kri_usciti'] or 'nessuno'}.\n"
          f"A5: {'usato' if agente is not None else 'non usato (facoltativo)'}. Osservazioni: "
          f"{sum(1 for x in esito['rilievi'] if x['gravita'] == controlli_a5.OSSERVAZIONE)}.\n"
          f"Registro unico (D-79): nel radar {sum(1 for x in stati.values() if radar.nel_radar(x['stato']))} rischi su "
          f"{capienza_radar} posti"
          + (f" (in uscita: {', '.join(sorted(i for i, x in stati.items() if x['stato'] == radar.IN_USCITA))})"
             if any(x["stato"] == radar.IN_USCITA for x in stati.values()) else "")
          + f"; in osservazione {sum(1 for x in stati.values() if x['stato'] == radar.OSSERVAZIONE)}; entrati nel radar "
          f"{', '.join(esito_scrittura['entrati']) or 'nessuno'}; usciti {', '.join(esito_scrittura['usciti']) or 'nessuno'}.\n"
          + (f"SEGNALAZIONI DA MOTIVARE: {len(da_mot)} su "
             f"{len({x['id_rischio'] for x in da_mot if x['id_rischio']})} rischi (colonna Segnalazioni dei controlli del "
             "foglio Validazione, ⚑ davanti al nome): in validazione quei rischi chiedono una Motivazione.\n" if da_mot else "") +
          f"Excel di output: {excel}\nArchivio del ciclo: {cartella}\n"
          f"Backup (stato prima): {copia}\nBaseline per il prossimo run: {file_baseline}\n"
          f"DA FARE: validazione umana nel foglio Validazione (una riga per rischio scritto da A1, nel radar o in osservazione, "
          f"KRI e azione: si cambiano solo le celle gialle, la Motivazione e Respingi; lo stato si ricalcola sui valori "
          f"validati), poi: python esegui_ciclo_locale.py valida --periodo {ciclo} "
          "--validatore \"<chi valida>\". Nessuna auto-approvazione: il ciclo dopo non parte finche' questo non e' validato.\n"
          f"Righe per le liste (Righe_liste_{ciclo}.json): valori NON ancora validati; il comando valida le riscrive."
          + (f"\nNote dell'analista del Quadro archiviate nella riga del ciclo {nota_archiviata} (Sintesi_Cicli) e "
             "svuotate per il ciclo nuovo." if nota_archiviata else "")
          + (f"\n{msg_a7}" if msg_a7 else ""))
    if posti_liberi <= 2:
        print(f"Nota: il radar ha {posti_liberi} posti liberi su {rng_anag.Rows.Count} (D-79): oltre la capienza di Parametri "
              "entrano i rischi con lo score piu' alto, gli altri restano in osservazione.")
    # D-68: senza le parti del razionale le schede non possono mettere il perche' accanto a ogni valore.
    import schede
    non_divisi = [x["id_rischio"] for x in payload["rischi"] if not schede.parti_razionale(x["razionale"])]
    if non_divisi:
        print(f"Avviso per le schede: il razionale di {', '.join(non_divisi)} non e' diviso in parti (RISCHIO:, IMPATTO:, "
              "PROBABILITA:, PROSSIMITA:, VELOCITY:): nella scheda il perche' dei valori restera' nel Razionale. Le "
              "istruzioni di A1 dal 02/10/2026 chiedono le parti: verificare che siano quelle reincollate in Agent Builder.")


def comando_settimanale(arg, conf):
    from excel_com import SessioneExcel
    mappa = carica_mappa(conf)
    payload = leggi_payload(arg.payload, "Output di A3")
    _valida_o_ferma(payload, "schema_output_A3.json", conf, "Output di A3")
    id_notizie = [n["id_notizia"] for n in payload["notizie"]]
    doppie = sorted({i for i in id_notizie if id_notizie.count(i) > 1})
    if doppie:
        raise Fermo(f"id_notizia ripetuti nello stesso output di A3: {doppie}. Chiedere ad A3 un id diverso per ogni notizia.")
    # D-74: una intensita' per ogni categoria della tassonomia (le colonne Imp_ di NewsLog nella mappa).
    attesi = sorted(c["sorgente"].split("|intensita:")[1] for c in mappa["tabelle"]["tblNews"]["colonne"]
                    if "|intensita:" in c["sorgente"])
    for n in payload["notizie"]:
        if sorted(i["event_type"] for i in n["impatti"]) != attesi:
            raise Fermo(f"{n['id_notizia']}: gli impatti devono coprire una volta ciascuna categoria ({', '.join(attesi)}).")
    if dt.date.fromisoformat(payload["settimana"]).weekday() != 0:
        raise Fermo(f"settimana {payload['settimana']} non e' un lunedi'.")
    # Ogni notizia cita una fonte dell'elenco (o MAN): controparte deterministica
    # della regola del prompt di A3 "usa solo fonti dell'elenco".
    ammessi = codici_ammessi(leggi_fonti(file_kernel(conf, "fonti.md")))
    fuori = sorted({n["codice_fonte"] for n in payload["notizie"]} - ammessi)
    if fuori:
        raise Fermo(f"Codici fonte non nell'elenco (o esclusi) in 01_Kernel/fonti.md: {fuori}")

    with SessioneExcel(conf["workbook"]) as s:
        controlla_versione(s)
        scr = Scrittore(s, mappa)
        _, anag = scr.leggi_anagrafica()
        # D-79: A3 collega notizie, flag e proposte ai rischi del registro, nel radar o in osservazione.
        ids = {r["ID"] for _, r in anag} | {r["ID_Rischio"] for r in rischi_osservazione(
            scr, da_excel(s.intervallo_nome("cicloCorrente").Value))}
        sconosciuti = {n["rischio_collegato"] for n in payload["notizie"]} - ids - {None}
        if sconosciuti:
            raise Fermo(f"Notizie collegate a rischi che non sono nel registro: {sorted(sconosciuti)}")
        flag_ignoti = {f["id_rischio"] for f in payload["flag_proposti"]} - ids
        if flag_ignoti:
            raise Fermo(f"Flag proposti per rischi che non sono nel registro: {sorted(flag_ignoti)}")
        proposta = payload.get("proposta_straordinario")
        if proposta and set(proposta["rischi"]) - ids:
            raise Fermo(f"Proposta di ciclo straordinario per rischi che non sono nel registro: {sorted(set(proposta['rischi']) - ids)}")
        aggiunte = scrivi_settimanale(scr, payload)
        s.ricalcola()
        mancanti = formule_mancanti(s, mappa)
        if mancanti:
            raise Fermo("Formule mancanti dopo la scrittura: " + "; ".join(mancanti[:10]))
        errori = s.errori_formula()
        if errori:
            raise Fermo("Errori di formula dopo la scrittura: " + "; ".join(f"{e[0]}!{e[1]} {e[2]}" for e in errori[:10]))
        badge = segnali_sopra_soglia(s)
        scoperte = aree_non_presidiate(s)
        prepara_report(s)               # le notizie cambiano livelli e rischi segnalati: il Quadro resta in due pagine
        copia = _salva_con_backup(s, conf["workbook"], conf)
    cartella = _cartella(conf, "Settimane", payload["settimana"])
    _scrivi_json(cartella / f"A3_{payload['settimana']}.json", payload)
    excel = _excel_di_output(conf["workbook"], cartella, payload["settimana"])
    print(f"Settimana {payload['settimana']}: {aggiunte} notizie aggiunte.\n"
          f"Segnali netti oltre la soglia: {badge or 'nessuno'}\nAree non presidiate: {scoperte or 'nessuna'}\n"
          + (f"PROPOSTA DI CICLO STRAORDINARIO di A3 per {', '.join(payload['proposta_straordinario']['rischi'])}: "
             f"{payload['proposta_straordinario']['motivo']}\nDecide la funzione di rischio; per farlo: python "
             "esegui_ciclo_locale.py baseline --straordinario --rischi ... --motivo \"...\" --decisore \"...\" (guida, "
             "sezione 2-bis).\n" if payload.get("proposta_straordinario") else "") +
          f"Flag proposti da A3: {len(payload['flag_proposti'])}\n"
          f"Notizie da validare (facoltativo) nel foglio Validazione, poi: python esegui_ciclo_locale.py valida --periodo "
          f"{payload['settimana']} --validatore \"<chi valida>\"\n"
          f"Excel di output: {excel}\nBackup (stato prima): {copia}")


def comando_valida(arg, conf):
    from excel_com import SessioneExcel
    mappa = carica_mappa(conf)
    periodo, oggi = arg.periodo.strip(), dt.date.today().isoformat()
    if getattr(arg, "accetta_il_resto", False):
        print("Nota: --accetta-il-resto non serve piu' (D-67): nel foglio Validazione una riga non toccata vale gia' "
              "come accettata.")
    with SessioneExcel(conf["workbook"]) as s:
        controlla_versione(s)
        scr = Scrittore(s, mappa)
        esiti, esiti_righe, registro, movimenti = applica_validazione(scr, periodo, arg.validatore.strip(), oggi)
        s.ricalcola()
        mancanti = formule_mancanti(s, mappa)
        if mancanti:
            raise Fermo("Formule mancanti dopo la validazione: " + "; ".join(mancanti[:10]))
        errori = s.errori_formula()
        if errori:
            raise Fermo("Errori di formula dopo la validazione: " + "; ".join(f"{e[0]}!{e[1]} {e[2]}" for e in errori[:10]))
        ciclo_corrente = da_excel(s.intervallo_nome("cicloCorrente").Value)
        prepara_report(s)
        copia = _salva_con_backup(s, conf["workbook"], conf)
        # I valori validati cambiano la baseline del prossimo ciclo e le righe per le liste.
        nuova_baseline = estrai_baseline(s, mappa) if periodo == ciclo_corrente else None
        liste = righe_liste(scr, periodo) if "Q" in periodo else None
        msg_a7 = aggiorna_spiegazioni(s, scr, conf) if periodo == ciclo_corrente else None     # D-72
    if nuova_baseline is not None:
        _scrivi_baseline(conf, nuova_baseline)
    cartella = _cartella(conf, "Cicli" if "Q" in periodo else "Settimane", periodo)
    if liste is not None:
        _scrivi_json(cartella / f"Righe_liste_{periodo}.json", liste)   # sostituisce quelle "da validare"
    _scrivi_json(cartella / f"Validazione_{periodo}.json",
                 {"periodo": periodo, "esiti": esiti, "esiti_righe": esiti_righe, "righe": registro})
    excel = _excel_di_output(conf["workbook"], cartella, f"{periodo}_validato")
    print(f"Validazione del periodo {periodo} applicata: {sum(esiti_righe.values())} righe — accettate "
          f"{esiti_righe['Accettato']}, rettificate {esiti_righe['Rettificato']} ({esiti['Rettificato']} valori cambiati), "
          f"respinte {esiti_righe['Respinto']}.\n"
          + (f"Radar di Mosca dopo la validazione (D-79): entrati {', '.join(movimenti['entrati']) or 'nessuno'}; usciti "
             f"{', '.join(movimenti['usciti']) or 'nessuno'}.\n" if movimenti["entrati"] or movimenti["usciti"] else "") +
          f"Excel validato: {excel}\nRegistro delle decisioni: {cartella / f'Validazione_{periodo}.json'}\n"
          f"Backup (stato prima): {copia}"
          + ("\nBaseline per il prossimo ciclo aggiornata con i valori validati." if nuova_baseline is not None else "")
          + (f"\nRighe per le liste con i valori validati: {cartella / f'Righe_liste_{periodo}.json'}" if liste is not None else "")
          + (f"\n{msg_a7}" if msg_a7 else ""))


def comando_griglia(arg, conf):
    """Ricostruisce la griglia del foglio Validazione dalle proposte ancora da decidere (D-67), conservando cio'
    che il validatore ha gia' scritto nelle righe intatte. Serve dopo una modifica a mano del foglio."""
    from excel_com import SessioneExcel
    mappa = carica_mappa(conf)
    with SessioneExcel(conf["workbook"]) as s:
        controlla_versione(s)
        scr = Scrittore(s, mappa)
        scritte = ricostruisci_griglia(scr)
        s.ricalcola()
        errori = s.errori_formula()
        if errori:
            raise Fermo("Errori di formula dopo la ricostruzione: " + "; ".join(f"{e[0]}!{e[1]} {e[2]}" for e in errori[:10]))
        copia = _salva_con_backup(s, conf["workbook"], conf)
    print("Foglio Validazione ricostruito dalle proposte da decidere: "
          + ", ".join(f"{oggetto} {n}" for oggetto, n in scritte.items()) + " righe.\n"
          "Cio' che era gia' scritto nelle righe intatte (valori gialli, Motivazione, Respingi) e' stato conservato.\n"
          f"Backup (stato prima): {copia}")


def comando_riapri(arg, conf):
    """D-76: riapre la validazione del ciclo corrente, gia' validato. Gli oggetti tornano nella griglia del foglio
    Validazione con il valore validato in grigio e nella cella gialla; poi si valida come sempre (comando valida), quante
    volte serve. Senza --rischi riapre tutto: i rischi del registro (nel radar e in osservazione, D-79), i KRI in vigore
    e le azioni aperte. Anche lo stato si cambia cosi' (colonna Decisione sullo stato)."""
    from excel_com import SessioneExcel
    mappa = carica_mappa(conf)
    rischi_scelti = {x.strip().upper() for x in (arg.rischi or "").split(",") if x.strip()}
    with SessioneExcel(conf["workbook"]) as s:
        controlla_versione(s)
        scr = Scrittore(s, mappa)
        ciclo = da_excel(s.intervallo_nome("cicloCorrente").Value)
        if not ciclo or not scr.righe("tblRegister"):
            raise Fermo("Il registro non ha ancora un ciclo validato: niente da riaprire.")
        pendenti = da_decidere(scr, ciclo)
        if pendenti:
            raise Fermo(f"Il ciclo {ciclo} ha gia' {righe_griglia(pendenti)} righe da validare nel foglio Validazione: si "
                        "cambiano li', poi valida. Si riapre solo un ciclo gia' validato.")
        _, anag = scr.leggi_anagrafica()
        attivi = {r["ID"] for _, r in anag}
        osservati = {r["ID_Rischio"] for r in rischi_osservazione(scr, ciclo)}
        ignoti = sorted(rischi_scelti - attivi - osservati)
        if ignoti:
            raise Fermo(f"Da riaprire ma non nel ciclo {ciclo}: {', '.join(ignoti)} (nel radar: {', '.join(sorted(attivi))}; "
                        f"in osservazione: {', '.join(sorted(osservati)) or 'nessuno'}).")
        rischi = rischi_scelti or (attivi | osservati)
        conteggi = {
            "Rischio": aggiungi_da_validare(scr, ciclo, "Rischio", lambda r: str(r["Ciclo"]) == str(ciclo)
                                            and r["ID_Rischio"] in rischi),
            "KRI": aggiungi_da_validare(scr, ciclo, "KRI", lambda r: str(r["Ciclo"]) == str(ciclo) and r["In_Vigore"] == "Sì"
                                        and r["ID_Rischio"] in rischi),
            # Le azioni aperte di qualunque ciclo (approvate o in corso): restano nel loro ciclo, si validano con questo.
            "Azione": aggiungi_da_validare(scr, ciclo, "Azione", lambda r: r["ID_Rischio"] in rischi
                                           and r["Stato"] not in STATI_AZIONE_CHIUSI and r["Stato"] != STATO_AZIONE_INIZIALE),
        }
        campi = {o: len(scr.mappa["validazione"]["oggetti"][o]["campi"]) for o in conteggi}
        oggetti = {o: n // campi[o] for o, n in conteggi.items()}
        ricostruisci_griglia(scr)
        s.ricalcola()
        errori = s.errori_formula()
        if errori:
            raise Fermo("Errori di formula dopo la riapertura: " + "; ".join(f"{e[0]}!{e[1]} {e[2]}" for e in errori[:10]))
        copia = _salva_con_backup(s, conf["workbook"], conf)
    print(f"Validazione del ciclo {ciclo} RIAPERTA (D-76): rischi {oggetti['Rischio']}, KRI {oggetti['KRI']}, azioni "
          f"{oggetti['Azione']}, nel foglio Validazione.\n"
          "In grigio il valore validato, nella cella gialla lo stesso valore: una riga non toccata resta com'e'. Per cambiare "
          "un valore scriverlo nella cella gialla con la Motivazione (almeno 10 caratteri; in riapertura nessun limite di un "
          "punto); Respingi = Sì toglie un KRI o annulla un'azione; la colonna Decisione sullo stato mette un rischio nel "
          "radar o in osservazione (D-79). Score e margine di Mosca si ricalcolano mentre scrivi, lo stato con valida.\n"
          f"Poi, con il file chiuso:  python esegui_ciclo_locale.py valida --periodo {ciclo} --validatore \"<chi decide>\"\n"
          "Si puo' riaprire di nuovo dopo, quante volte serve. Finche' non si valida, trimestrale, report e schede aspettano.\n"
          f"Backup (stato prima): {copia}")


def comando_inizializza(arg, conf):
    """Registro vivo nuovo dal template, senza dati di esempio. Il template ha
    righe di esempio (grigie) che servono a vedere e collaudare le viste; il
    registro vero parte vuoto, con il ciclo PRIMA di quello da valutare."""
    import re
    from excel_com import SessioneExcel
    mappa = carica_mappa(conf)
    destinazione = conf["workbook"]
    template = Path(arg.template) if arg.template else TEMPLATE_PREDEFINITO
    ciclo = arg.ciclo_precedente.strip()
    if not re.fullmatch(r"\d{4}Q[1-4]", ciclo):
        raise Fermo(f"--ciclo-precedente {ciclo!r}: scrivere il trimestre PRIMA di quello da valutare, es. 2026Q3.")
    try:
        settimana = dt.date.fromisoformat(arg.settimana.strip())
    except ValueError:
        raise Fermo(f"--settimana {arg.settimana!r}: scrivere una data AAAA-MM-GG.")
    if settimana.weekday() != 0:
        raise Fermo(f"--settimana {settimana}: deve essere un lunedi'.")
    if destinazione.exists():
        raise Fermo(f"{destinazione} esiste gia': inizializza crea un registro NUOVO e non sovrascrive mai. "
                    "Per ricominciare, spostare prima il file esistente.")
    if not template.exists():
        raise Fermo(f"Template non trovato: {template}. Rigenerarlo con:  python \"{template.parent / 'genera_dashboard.py'}\"  "
                    "(richiede openpyxl: pip install openpyxl), oppure indicare un altro file con --template.")
    if not destinazione.parent.exists():
        raise Fermo(f"La cartella {destinazione.parent} non esiste (raccolta non sincronizzata?).")
    prova = destinazione.with_name(destinazione.stem + "_in_preparazione" + destinazione.suffix)
    shutil.copy2(template, prova)
    try:
        with SessioneExcel(prova) as s:
            controlla_versione(s, "Il template")
            scr = Scrittore(s, mappa)
            svuota_registro(s, mappa)
            ricostruisci_griglia(scr, modifiche={})       # niente da validare: griglia vuota
            imposta_ciclo(scr, ciclo, fine_trimestre(ciclo))
            s.intervallo_nome("settimanaCorrente").Value = a_data(settimana.isoformat())
            s.ricalcola()
            errori = s.errori_formula()
            if errori:
                raise Fermo("Errori di formula nel registro vuoto: " + "; ".join(f"{e[0]}!{e[1]} {e[2]}" for e in errori[:10]))
            piene = [n for n in [*mappa["tabelle"], mappa["validazione"]["tabella"]] if scr.righe(n)]
            if piene:
                raise Fermo(f"Tabelle non svuotate: {piene}")
            prepara_report(s)
            s.salva()
        shutil.move(str(prova), str(destinazione))
    finally:
        if prova.exists():
            prova.unlink()
    print(f"Registro creato: {destinazione}\nSenza dati di esempio; ciclo corrente {ciclo} (il primo da valutare e' "
          f"{ciclo_successivo(ciclo)}), settimana corrente {settimana}.\n"
          "Prossimo passo: python esegui_ciclo_locale.py baseline, poi il primo ciclo trimestrale "
          "(A1 proporra' tutti i rischi come Nuovi).")


def comando_dismetti(arg, conf):
    """Toglie un rischio dal registro attivo, lasciandone la storia."""
    from excel_com import SessioneExcel
    mappa = carica_mappa(conf)
    rid, motivo, decisore = arg.rischio.strip().upper(), arg.motivazione.strip(), arg.decisore.strip()
    if len(motivo) < 10:
        raise Fermo("--motivazione obbligatoria, almeno 10 caratteri: resta agli atti.")
    oggi = dt.date.today().isoformat()
    with SessioneExcel(conf["workbook"]) as s:
        controlla_versione(s)
        scr = Scrittore(s, mappa)
        _, anag = scr.leggi_anagrafica()
        ciclo = da_excel(s.intervallo_nome("cicloCorrente").Value)
        voce = next((r for _, r in anag if r["ID"] == rid), None)
        # D-79: si toglie anche un rischio in osservazione (non e' nell'anagrafica, che e' il radar).
        osservato = next((r for r in rischi_osservazione(scr, ciclo) if r["ID_Rischio"] == rid), None)
        if voce is None and osservato is None:
            raise Fermo(f"{rid} non e' nell'anagrafica dei rischi attivi ne' fra i rischi in osservazione del ciclo {ciclo}.")
        if voce is None:
            voce = {"ID": rid, "Nome": osservato["Nome"], "Event_Type": osservato["Event_Type"], "Owner": osservato.get("Owner")}
        else:
            scr.compatta_anagrafica(rid)
        # La riga del ciclo corrente dice che il rischio e' uscito dal registro: il ciclo dopo non lo riporta.
        for n, r in enumerate(scr.righe("tblRegister"), start=1):
            if str(r["Ciclo"]) == str(ciclo) and r["ID_Rischio"] == rid:
                scr.aggiorna("tblRegister", n, {"Stato": DISMESSO, "Movimento": None,
                                                "Motivo_Stato": f"dismesso il {oggi} da {decisore}: {motivo}"[:500]})
        # Unica modifica a righe storiche oltre alla validazione: i KRI del ciclo
        # corrente escono di vigore, come un KRI sostituito.
        usciti = []
        for n, k in enumerate(scr.righe("tblKRI"), start=1):
            if k["Ciclo"] == ciclo and k["ID_Rischio"] == rid and k["In_Vigore"] == "Sì":
                scr.aggiorna("tblKRI", n, {"In_Vigore": "No"})
                usciti.append(k["KRI_ID"])
        annullate = []
        for n, a in enumerate(scr.righe("tblAzioni"), start=1):
            if a["ID_Rischio"] == rid and a["Stato"] not in STATI_AZIONE_CHIUSI:
                scr.aggiorna("tblAzioni", n, {"Stato": ANNULLATA, "Decisa_Da": decisore, "Data_Decisione": a_data(oggi)})
                annullate.append(a["ID_Azione"])
        s.ricalcola()
        mancanti = formule_mancanti(s, mappa)
        if mancanti:
            raise Fermo("Formule mancanti dopo la dismissione: " + "; ".join(mancanti[:10]))
        errori = s.errori_formula()
        if errori:
            raise Fermo("Errori di formula dopo la dismissione: " + "; ".join(f"{e[0]}!{e[1]} {e[2]}" for e in errori[:10]))
        prepara_report(s)
        copia = _salva_con_backup(s, conf["workbook"], conf)
        nuova_baseline = estrai_baseline(s, mappa)
        msg_a7 = aggiorna_spiegazioni(s, scr, conf, dismesso={"rischio": rid, "nome": voce["Nome"], "data": oggi,
                                                              "decisore": decisore, "motivazione": motivo})   # D-72
    _scrivi_baseline(conf, nuova_baseline)
    atto = _scrivi_json(_cartella(conf, "Dismissioni") / f"{rid}_{oggi}.json", {
        "rischio": rid, "nome": voce["Nome"], "event_type": voce["Event_Type"], "owner": voce["Owner"],
        "ciclo_corrente": ciclo, "data": oggi, "decisore": decisore, "motivazione": motivo,
        "kri_usciti": usciti, "azioni_annullate": annullate})
    print(f"Rischio {rid} dismesso: tolto dall'anagrafica (nessuna riga vuota), KRI usciti di vigore {usciti or 'nessuno'}, "
          f"azioni annullate {annullate or 'nessuna'}. La storia resta in RiskRegister, KRI e Azioni.\n"
          f"Atto: {atto}\nBackup (stato prima): {copia}\nBaseline aggiornata: il prossimo ciclo non lo valuta piu'."
          + (f"\n{msg_a7}" if msg_a7 else ""))


def rischi_straordinario(decisione):
    """Testo dei rischi di uno straordinario: quelli da rivalutare o, senza, il solo censimento (D-77)."""
    da_rivalutare = decisione.get("rischi_da_rivalutare") or []
    return (f"rischi da rivalutare {', '.join(da_rivalutare)}" if da_rivalutare else
            "solo censimento di rischi nuovi creati dall'evento, nessun rischio da rivalutare")


def decisione_straordinario(arg, s, mappa):
    """D-75: la funzione di rischio decide un ciclo straordinario (dopo una proposta di A3 o A4, o di sua iniziativa).
    Periodo AAAAQn-Sk: il trimestre del ciclo corrente e il primo numero libero. Restituisce la decisione da archiviare."""
    scr = Scrittore(s, mappa)
    corrente = da_excel(s.intervallo_nome("cicloCorrente").Value)
    if not corrente or not scr.righe("tblRegister"):
        raise Fermo("Un ciclo straordinario si fa su un registro che ha gia' un ciclo trimestrale validato.")
    pendenti = da_decidere(scr, corrente)
    if pendenti:
        raise Fermo(f"Il ciclo {corrente} ha ancora {righe_griglia(pendenti)} righe da validare: lo straordinario parte dai valori "
                    "validati. Validare prima (comando valida).")
    _, anag = scr.leggi_anagrafica()
    # D-79: si puo' rivalutare anche un rischio in osservazione (se l'evento lo porta sopra le soglie entra nel radar).
    ids = {r["ID"] for _, r in anag} | {r["ID_Rischio"] for r in rischi_osservazione(scr, corrente)}
    # Senza --rischi lo straordinario e' di solo censimento: l'evento crea rischi nuovi e non ne rivaluta (D-77).
    rischi = sorted({x.strip().upper() for x in (arg.rischi or "").split(",") if x.strip()})
    if set(rischi) - ids:
        raise Fermo(f"--rischi: indicare i rischi da rivalutare, separati da virgole, fra quelli in anagrafica "
                    f"({', '.join(sorted(ids))}); non validi: {sorted(set(rischi) - ids)}. Senza --rischi lo straordinario "
                    "censisce solo rischi nuovi.")
    motivo, decisore = (arg.motivo or "").strip(), (arg.decisore or "").strip()
    if len(motivo) < 20 or len(decisore) < 3:
        raise Fermo("--motivo (almeno 20 caratteri: l'evento critico e perche' non puo' aspettare il trimestre) e --decisore "
                    "(chi decide: una funzione o un comitato) sono obbligatori per un ciclo straordinario.")
    oggi = dt.date.today().isoformat()
    data = (arg.data or oggi).strip()
    try:
        dt.date.fromisoformat(data)
    except ValueError:
        raise Fermo(f"--data {data!r}: scrivere una data AAAA-MM-GG.")
    data_corrente = data_periodo(scr, corrente)
    if data <= data_corrente:
        raise Fermo(f"--data {data}: la data di riferimento dello straordinario deve venire dopo quella del ciclo corrente "
                    f"{corrente} ({data_corrente}).")
    trimestre = trimestre_di(corrente)
    k = 1 + sum(1 for p in periodi_registro(scr) if p.startswith(trimestre + "-S"))
    if k > 9:
        raise Fermo(f"Il trimestre {trimestre} ha gia' 9 cicli straordinari.")
    return {"periodo": f"{trimestre}-S{k}", "data_riferimento": data, "rischi_da_rivalutare": rischi, "motivo": motivo,
            "decisore": decisore, "data_decisione": oggi, "ciclo_precedente": corrente}


def comando_baseline(arg, conf):
    from excel_com import SessioneExcel
    mappa = carica_mappa(conf)
    decisione = None
    with SessioneExcel(conf["workbook"], sola_lettura=True) as s:
        controlla_versione(s)
        if getattr(arg, "straordinario", False):
            decisione = decisione_straordinario(arg, s, mappa)
        dati = estrai_baseline(s, mappa, straordinario=decisione)
        pendenti = da_decidere(Scrittore(s, mappa), dati["ciclo_precedente"] or "")
        msg_a7 = None
        if not decisione and not arg.uscita:
            # D-76: dopo una correzione a mano dei testi (descrizioni, razionali, KRI, azioni) basta questo comando per
            # riallineare baseline, allegato di A1 e knowledge di A7.
            s.ricalcola()
            msg_a7 = aggiorna_spiegazioni(s, Scrittore(s, mappa), conf)
    if msg_a7:
        print(msg_a7)
    if decisione:
        archivio = _scrivi_json(_cartella(conf, "Cicli", decisione["periodo"]) / f"Straordinario_{decisione['periodo']}.json",
                                decisione)
        print(f"CICLO STRAORDINARIO {decisione['periodo']} deciso da {decisione['decisore']} (D-75): "
              f"{rischi_straordinario(decisione)}; data di riferimento {decisione['data_riferimento']}.\n"
              f"Decisione archiviata: {archivio}\n"
              f"Prossimi passi: A8 Evento critico con l'allegato Input_A1_{decisione['periodo']}.txt e i documenti "
              f"sull'evento (D-77), poi (facoltativo) python esegui_ciclo_locale.py precontrollo --payload "
              f"A8_{decisione['periodo']}.json e trimestrale --payload A8_{decisione['periodo']}.json, poi la validazione (solo i rischi rivalutati e "
              "quelli nuovi).")
    if pendenti:
        print(f"ATTENZIONE: il ciclo {dati['ciclo_precedente']} ha ancora {righe_griglia(pendenti)} righe da validare nel foglio "
              "Validazione. Questa baseline contiene valori NON validati; il comando trimestrale si fermera' finche' "
              "il ciclo non e' validato.")
    uscita = _scrivi_json(Path(arg.uscita), dati) if arg.uscita else _scrivi_baseline(conf, dati)
    print(f"Baseline scritta: {uscita}")
    if not arg.uscita:
        print(f"Allegato per {agente_di(dati.get('ciclo_da_valutare'))}: {uscita.parent / input_a1.nome_file(dati)} "
              "(baseline, controlli di A5 e guida di scrittura)")


def _input_schede(s, mappa):
    """Dati per le schede del ciclo corrente, solo se il ciclo e' validato."""
    import schede
    scr = Scrittore(s, mappa)
    ciclo = da_excel(s.intervallo_nome("cicloCorrente").Value)
    if not ciclo:
        raise Fermo("Nessun ciclo corrente nel registro: le schede si fanno dopo il primo ciclo trimestrale.")
    pendenti = da_decidere(scr, ciclo)
    if pendenti:
        raise Fermo(f"Il ciclo {ciclo} ha ancora {righe_griglia(pendenti)} righe da validare nel foglio Validazione: le schede "
                    "si fanno sui dati VALIDATI. Validare prima con il comando valida.")
    return schede.input_schede(scr, s, ciclo, periodi_prima(scr, ciclo, 1)[0], data_periodo(scr, ciclo))


def cartella_spiegazioni(conf):
    """Cartella della knowledge di A7 (D-72): `Spiegazioni` dentro la library Kernel. Quando il kernel e' la
    01_Kernel del pacchetto (collaudo, demo) va nella cartella di uscita, per non scrivere nel pacchetto."""
    kernel = Path(conf["kernel"]).resolve()
    if kernel == (QUI.parent / "01_Kernel").resolve():
        return conf["cartella_uscita"] / "Spiegazioni"
    return kernel / "Spiegazioni"


def aggiorna_spiegazioni(s, scr, conf, payload=None, dismesso=None):
    """Riscrive la knowledge di A7 dal registro aperto (dopo il ricalcolo). Un errore non ferma il comando: i dati
    sono gia' scritti, la knowledge si riallinea al comando dopo. Con 'payload' (trimestrale) fenomeni non censiti e
    analisi dell'evento vengono dall'output appena scritto, che si archiviera' nella cartella del ciclo solo dopo.
    Restituisce il messaggio da stampare."""
    import spiegazioni
    try:
        ciclo = da_excel(s.intervallo_nome("cicloCorrente").Value)
        if not ciclo or not scr.righe("tblRegister"):
            return None
        try:
            nota = s.intervallo_nome("quadroNote").Value
        except Exception:
            nota = None
        dati = spiegazioni.raccogli(scr, s, conf["cartella_uscita"], ciclo, periodi_prima(scr, ciclo, 1)[0], data_periodo(scr, ciclo),
                                    not da_decidere(scr, ciclo), nota)
        if payload is not None:
            dati["scartati"] = payload.get("fenomeni_non_censiti") or []
            dati["analisi_evento"] = payload.get("analisi_evento")
        if dismesso:                                 # l'atto della dismissione si archivia dopo la sessione
            dati["dismessi"].append(dismesso)
        cartella = cartella_spiegazioni(conf)
        file = spiegazioni.scrivi(cartella, dati, dt.date.today().isoformat())
        return f"Knowledge di A7 aggiornata: {cartella} ({len(file)} file)."
    except Exception as ex:                          # noqa: BLE001 - un avviso, mai un fermo
        return f"Avviso: knowledge di A7 non aggiornata ({type(ex).__name__}: {ex}); i dati del registro sono scritti."


def archivia_nota_quadro(s, scr, ciclo_prec):
    """D-72: le Note dell'analista della prima pagina valgono per il ciclo corrente. A un ciclo nuovo il testo va
    nella riga del ciclo precedente di tblSintesi (colonna Note_Analista) e la cella si svuota."""
    try:
        cella = s.intervallo_nome("quadroNote")
    except Exception:
        return None
    nota = cella.Value
    if nota in (None, "") or not ciclo_prec:
        return None
    righe = scr.righe("tblSintesi")
    pos = next((i for i, r in enumerate(righe, start=1) if str(r["Ciclo"]) == str(ciclo_prec)), None)
    if pos is None:
        return None                                  # nessuna riga del ciclo precedente: la nota resta dov'e'
    scr.aggiorna("tblSintesi", pos, {"Note_Analista": nota})           # aggiorna applica gia' per_cella
    cella.Value = None
    return ciclo_prec


FOGLI_REPORT = ["Quadro", "Classifica", "Radar_Mosca", "Matrice", "Delta", "Fenomeni", "Metodologia"]
FOGLI_LAVORO = ["Registro", "Parametri"]


def comando_report(arg, conf):
    """PDF del report al comitato rigenerato dall'Excel com'e' ora (D-62): dopo la
    validazione i validatori possono cambiare a mano presidio, anni di adeguamento,
    attenzione del supervisore e stato delle azioni, e il report deve seguirli.
    Sola lettura: ricalcola, adatta le altezze delle righe in memoria, esporta."""
    from excel_com import SessioneExcel
    mappa = carica_mappa(conf)
    file = Path(arg.file) if getattr(arg, "file", None) else conf["workbook"]
    if not file.exists():
        raise Fermo(f"Excel non trovato: {file}")
    fogli = FOGLI_REPORT + (FOGLI_LAVORO if getattr(arg, "con_lavoro", False) else [])
    with SessioneExcel(file, sola_lettura=True) as s:
        controlla_versione(s)
        s.ricalcola()
        ciclo = da_excel(s.intervallo_nome("cicloCorrente").Value)
        pendenti = da_decidere(Scrittore(s, mappa), ciclo or "")
        if pendenti:
            raise Fermo(f"Il ciclo {ciclo} ha ancora {righe_griglia(pendenti)} righe da validare (foglio Validazione): il report "
                        "si fa sui valori validati (comando valida).")
        errori = s.errori_formula()
        if errori:
            raise Fermo("Errori di formula nell'Excel: " + "; ".join(f"{e[0]}!{e[1]} {e[2]}" for e in errori[:10]))
        prepara_report(s)
        cartella = _cartella(conf, "Cicli", ciclo)
        pdf = cartella / f"Report_comitato_{ciclo}.pdf"
        precedente = None
        if pdf.exists():
            precedente = pdf.with_name(f"Report_comitato_{ciclo}_{dt.datetime.fromtimestamp(pdf.stat().st_mtime):%Y%m%d_%H%M%S}.pdf")
            os.replace(pdf, precedente)
        s.wb.Worksheets(fogli).Select()
        s.wb.ActiveSheet.ExportAsFixedFormat(0, str(pdf))
    print(f"Report al comitato del ciclo {ciclo} rigenerato da {file}:\n  {pdf}\n"
          f"Fogli: {', '.join(fogli)}."
          + (f"\nVersione precedente conservata: {precedente}" if precedente else ""))


def comando_schede_input(arg, conf):
    from excel_com import SessioneExcel
    mappa = carica_mappa(conf)
    with SessioneExcel(conf["workbook"], sola_lettura=True) as s:
        controlla_versione(s)
        s.ricalcola()
        dati = _input_schede(s, mappa)
    ciclo = dati["ciclo"]
    uscita = _scrivi_json(_cartella(conf, "Cicli", ciclo) / f"Schede_input_{ciclo}.json", dati)
    print(f"Input delle schede del ciclo {ciclo} ({len(dati['rischi'])} rischi): {uscita}\n"
          f"Allegarlo, da solo, all'agente A6; salvarne l'output come A6_{ciclo}.json e lanciare:\n"
          f"  python esegui_ciclo_locale.py schede --payload A6_{ciclo}.json")


def comando_schede(arg, conf):
    import schede
    from excel_com import SessioneExcel
    mappa = carica_mappa(conf)
    with SessioneExcel(conf["workbook"], sola_lettura=True) as s:
        controlla_versione(s)
        s.ricalcola()
        dati = _input_schede(s, mappa)
        validazione = str(s.intervallo_nome("etichettaCiclo").Value or "").split(" · ")[2:3]
    ciclo = dati["ciclo"]
    uscita_a6 = None
    if arg.payload:
        uscita_a6 = leggi_payload(arg.payload, "Output di A6")
        _valida_o_ferma(uscita_a6, "schema_output_A6.json", conf, "Output di A6")
        rubrica = file_kernel(conf, "rubrica_scoring.md").read_text(encoding="utf-8")
        problemi = schede.controlla_a6(dati, uscita_a6, rubrica)
        if problemi:
            raise Fermo("Output di A6 non coerente con i dati validati (nessun file scritto):\n  - " + "\n  - ".join(problemi))
    cartella = _cartella(conf, "Cicli", ciclo)
    _scrivi_json(cartella / f"Schede_input_{ciclo}.json", dati)
    if uscita_a6:
        _scrivi_json(cartella / f"A6_{ciclo}.json", uscita_a6)
    file = schede.scrivi_file_schede(dati, uscita_a6, cartella / f"Schede_{ciclo}.xlsx",
                                     validazione[0] if validazione else "")
    print(f"Schede del ciclo {ciclo}: {len(dati['rischi'])} rischi, "
          f"{'testi di A6 controllati' if uscita_a6 else 'testi di A1 dal registro (senza A6)'}.\nFile: {file}")


PARAMETRI_DA_CONSERVARE = ["cicloCorrente", "settimanaCorrente", "moscaX", "moscaYDefault", "quadroNote",   # quadroNote: D-72
                           "capienzaRadar", "sogliaProssimitaRadar", "sogliaProbabilitaRadar", "cicliUscitaRadar"]   # D-79


def prossimita_da_orizzonte(anni):
    """D-79, conversione della lista: orizzonte in anni -> Prossimita (1 oltre 3 anni, 2 da 2 a 3, 3 da 1 a 2)."""
    n = _numero(anni)
    return 1 if n is None or n > 3 else 2 if n >= 2 else 3


def rischi_da_lista(voci, ciclo, data_rif, usati, oggi):
    """D-79: le voci in osservazione della lista della D-73 (tabella tblOsservazione di un registro fino al 2026-10-08b)
    diventano rischi in osservazione del ciclo corrente, con un codice NFR-nn libero. Valori convertiti in via
    provvisoria (A1 li rivaluta al ciclo dopo): Impatto = impatto potenziale; Probabilita dalla plausibilita' (teorica 1,
    possibile 2, in crescita 3); Prossimita dall'orizzonte; Velocity non valutata. Restituisce (righe, {OSS: NFR})."""
    righe, codici = [], {}
    for v in voci:
        n = 1
        while f"NFR-{n:02d}" in usati:
            n += 1
        rid = f"NFR-{n:02d}"
        usati.add(rid)
        codici[v["OSS_ID"]] = rid
        motivo = (f"convertito dalla lista di osservazione ({v['OSS_ID']}, D-79): valori da rivalutare da A1 al prossimo ciclo")
        righe.append({
            "Ciclo": ciclo, "Data_Riferimento": a_data(data_rif), "ID_Rischio": rid, "Nome": v.get("Nome"),
            "Event_Type": v.get("Event_Type"), "Driver": v.get("Driver"), "Impatto": _numero(v.get("Impatto_Potenziale")),
            "Velocity": None, "Prossimita": prossimita_da_orizzonte(v.get("Orizzonte_Anni")),
            "Probabilita": PROBABILITA_DA_PLAUSIBILITA.get(str(v.get("Plausibilita") or "").lower(), 1),
            "Anni_Adeguamento": None, "Esito": "Nuovo", "Descrizione": v.get("Descrizione"),
            "Razionale": f"Voce {v['OSS_ID']} della lista di osservazione, convertita il {oggi}. {v.get('Motivazione') or ''}".strip(),
            "Variazioni": "[]", "Fonti": v.get("Fonti") or "[]", "Rilievi": None, "Owner": OWNER_NUOVO,
            "Data_Scrittura": a_data(oggi), "Approvato_Da": "Conversione D-79", "Validazione": "Accettato",
            "Data_Validazione": a_data(oggi), "Periodo_Valutazione": ciclo, "Stato": radar.OSSERVAZIONE,
            "Motivo_Stato": motivo, "Movimento": None, "Decisione_Stato": radar.AUTOMATICO,
            "Orizzonte_Anni": _numero(v.get("Orizzonte_Anni")), "Segnale_Avvicinamento": v.get("Segnale_Avvicinamento")})
    return righe, codici
# Parametri decisi con il template (pesi D-50, soglie D-61, Z per Prossimita D-59): valgono quelli del
# template nuovo; i vecchi si leggono solo per il messaggio finale (pesoGap e pesoSeverity: template precedenti).
PESI = ["pesoImpatto", "pesoSeverity", "pesoProbabilita", "pesoProssimita", "pesoVelocity", "pesoGap",
        "sogliaDirezione", "sogliaDelta", "anniProssimita"]


def _valore_migrato(valore, colonna):
    """Valore letto dal registro vecchio -> valore da scrivere nel nuovo. Le date
    tornano da COM come testo ISO (da_excel): si riscrivono come seriale."""
    if colonna.get("formato") == "data" and isinstance(valore, str) and len(valore) == 10 and valore[4] == "-":
        return a_data(valore)
    return valore


def comando_aggiorna_registro(arg, conf):
    """Registro vivo -> template nuovo, senza perdere niente. Copia per NOME di
    colonna (non per posizione) le righe di tutte le tabelle, l'anagrafica e i
    parametri di input; pesi, soglie e Z restano quelli del template nuovo. Prima
    di sostituire il file verifica: stesse righe per tabella, zero errori di
    formula, formule presenti, stessa copertura, baseline identica."""
    from excel_com import SessioneExcel
    mappa = carica_mappa(conf)
    vecchio = conf["workbook"]
    template = Path(arg.template) if arg.template else TEMPLATE_PREDEFINITO
    if not template.exists():
        raise Fermo(f"Template non trovato: {template}. Rigenerarlo con:  python \"{template.parent / 'genera_dashboard.py'}\"  "
                    "(richiede openpyxl: pip install openpyxl), oppure indicare un altro file con --template.")
    tabelle = [*mappa["tabelle"], mappa["validazione"]["tabella"]]

    # 1. Lettura del registro vecchio, in sola lettura.
    with SessioneExcel(vecchio, sola_lettura=True) as s:
        versione = versione_workbook(s)
        if versione == VERSIONE_TEMPLATE:
            raise Fermo(f"{vecchio} e' gia' sulla versione {VERSIONE_TEMPLATE}: niente da aggiornare.")
        scr = Scrittore(s, mappa)
        dati = {}
        for nome in tabelle:
            try:
                lo = s.tabella(nome)
            except KeyError:
                continue                              # tabella nata con il template nuovo (es. tblSintesi)
            dati[nome] = ([c.Name for c in lo.ListColumns], scr.righe(nome))
        anagrafica = [list(r) for r in s.intervallo_nome("anagrafica").Value if r[0]]
        try:                                         # D-79: la lista di osservazione di un registro fino al 2026-10-08b
            voci_lista = scr.righe("tblOsservazione")
        except KeyError:
            voci_lista = []
        parametri = {}
        for nome in PARAMETRI_DA_CONSERVARE + PESI:
            try:
                parametri[nome] = s.intervallo_nome(nome).Value
            except Exception:
                pass
        ciclo = da_excel(parametri.get("cicloCorrente"))
        baseline_prima = estrai_baseline(s, mappa)
        copertura_prima = copertura_python(scr, ciclo)
        # Righe ancora da validare (D-67): passano nella griglia del registro nuovo con cio' che il validatore aveva
        # gia' scritto, nella griglia (registri dal 2026-10-02) o nel vecchio foglio Validazione, una riga per campo.
        aperte = [(n, r) for n, r in enumerate(dati.get(mappa["validazione"]["tabella"], ([], []))[1], start=1)
                  if r.get("Stato") == DA_DECIDERE]
        modifiche = {**modifiche_vecchio_formato(aperte), **leggi_griglia(s, mappa)}
    # Un campo tolto dal modello (Severity, Confidence, Gap_Controlli dei registri fino al 2026-09-25c) non ha una
    # colonna nella griglia: quelle righe si validano con il pacchetto con cui sono state scritte.
    fuori_modello = sorted({(r["Oggetto"], r["Campo"]) for _, r in aperte
                            if r["Campo"] not in mappa["validazione"]["oggetti"].get(r["Oggetto"], {}).get("campi", [])})
    vuote = [n for n, r in aperte if not r.get("Oggetto") and not r.get("Campo")]
    if vuote:
        # Visto in Banca il 06/10/2026: righe vuote dello storico con lo Stato "Da decidere" (colonna riempita a mano).
        raise Fermo(f"Il registro ha {len(vuote)} righe vuote con lo Stato 'Da decidere' nella tabella dello storico delle "
                    f"validazioni (righe {vuote[:10]} della tabella tblValidazione): sono righe senza Oggetto ne' Campo, "
                    "probabilmente lo Stato copiato a mano oltre la fine dei dati. Con il registro chiuso farne una copia, "
                    "aprirlo, nel foglio dello storico (Validazione o Storico_Validazioni) eliminare quelle righe (tasto "
                    "destro -> Elimina -> Righe della tabella), salvare e rilanciare aggiorna-registro.")
    if fuori_modello:
        raise Fermo(f"Il registro ha righe 'Da decidere' su campi che il modello non ha piu' ({fuori_modello}, periodi "
                    f"{sorted({str(r['Periodo']) for _, r in aperte})}): validarle prima con il pacchetto con cui sono state "
                    "scritte (comando valida), poi aggiornare il registro.")

    # Colonne rinominate (mappa, colonne_rinominate, es. Severity -> Impatto, D-57): i valori passano alla nuova.
    rinominate = {k: v for k, v in mappa.get("colonne_rinominate", {}).items() if not k.startswith("_")}
    for nome, (colonne, righe) in dati.items():
        for vecchia, nuova in rinominate.get(nome, {}).items():
            if vecchia in colonne:
                for r in righe:
                    r.setdefault(nuova, r.get(vecchia))
    # D-75: un registro precedente al 2026-10-08 non ha Periodo_Valutazione: ogni riga e' stata valutata nel suo ciclo.
    # D-79: ne' lo stato del registro unico: ogni rischio valutato era nel radar (la regola vale dal ciclo dopo).
    for r in dati.get("tblRegister", ([], []))[1]:
        r.setdefault("Periodo_Valutazione", r.get("Ciclo"))
        if not r.get("Stato"):
            r.update(Stato=radar.RADAR, Decisione_Stato=radar.AUTOMATICO,
                     Motivo_Stato="registro precedente al registro unico (D-79): la regola vale dal ciclo dopo"
                     if str(r.get("Ciclo")) == str(ciclo) else None)
    # D-79: le voci ancora in osservazione della lista diventano rischi in osservazione del ciclo corrente; le notizie
    # collegate a una voce passano al rischio nuovo.
    voci_attive = [v for v in voci_lista if str(v.get("Ciclo")) == str(ciclo) and v.get("Stato") == "In osservazione"]
    usati = {str(r.get("ID_Rischio")) for r in dati.get("tblRegister", ([], []))[1]} | {str(r[0]) for r in anagrafica}
    convertiti, codici_oss = rischi_da_lista(voci_attive, ciclo, baseline_prima["data_riferimento_precedente"]
                                             or fine_trimestre(trimestre_di(ciclo)), usati, dt.date.today().isoformat())
    dati["tblRegister"][1].extend(convertiti)
    for n in dati.get("tblNews", ([], []))[1]:
        if n.get("Voce_Osservazione") in codici_oss and n.get("Rischio_ID") in (None, "", NON_PRESIDIATO):
            n["Rischio_ID"] = codici_oss[n["Voce_Osservazione"]]
    # Colonne tolte dal modello (mappa, colonne_dismesse): non si copiano; restano nel registro vecchio (Backup).
    dismesse = {k: set(v) for k, v in mappa.get("colonne_dismesse", {}).items() if not k.startswith("_")}
    for nome, cambi in rinominate.items():
        dismesse.setdefault(nome, set()).update(cambi)
    perse = {nome: [c for c in colonne if c not in {x["nome"] for x in spec_tabella(mappa, nome)["colonne"]}
                    and c not in dismesse.get(nome, set())]
             for nome, (colonne, _) in dati.items()}
    perse = {k: v for k, v in perse.items() if v}
    if perse:
        raise Fermo(f"Colonne del registro che il template nuovo non ha (i loro dati andrebbero persi): {perse}. "
                    "Serve un template che le contenga.")
    lasciate = {nome: sorted(c for c in colonne if c in dismesse.get(nome, set()) and c not in rinominate.get(nome, {}))
                for nome, (colonne, _) in dati.items()}
    lasciate = {k: v for k, v in lasciate.items() if v}

    # 2. Registro nuovo dal template, riempito con i dati del vecchio.
    nuovo = vecchio.with_name(vecchio.stem + "_aggiornamento_in_corso" + vecchio.suffix)
    shutil.copy2(template, nuovo)
    try:
        with SessioneExcel(nuovo) as s:
            controlla_versione(s, "Il template")
            svuota_registro(s, mappa)
            scr = Scrittore(s, mappa)
            for nome, (_, righe) in dati.items():
                scrivibili = [c for c in spec_tabella(mappa, nome)["colonne"] if not c.get("sorgente", "").startswith("formula:")]
                if righe:
                    scr.append(nome, [{c["nome"]: _valore_migrato(r.get(c["nome"]), c) for c in scrivibili} for r in righe])
            rng = s.intervallo_nome("anagrafica")
            if len(anagrafica) > rng.Rows.Count:
                raise Fermo(f"L'anagrafica del registro ha {len(anagrafica)} rischi, il template nuovo {rng.Rows.Count} posti.")
            nomi_ana = [c["nome"] for c in mappa["anagrafica"]["colonne"]]
            for i, riga in enumerate(anagrafica, start=1):
                for j, v in enumerate(riga[:rng.Columns.Count], start=1):
                    rng.Cells(i, j).Value = per_cella(da_excel(v))
                # Un registro nato prima del 30/09 non ha il presidio dei controlli (D-49): "Non verificato".
                j = nomi_ana.index("Presidio_Controlli") + 1
                if len(riga) < j or not riga[j - 1]:
                    rng.Cells(i, j).Value = per_cella(PRESIDIO_NUOVO)
            for nome in PARAMETRI_DA_CONSERVARE:
                if nome not in parametri:
                    continue
                v = parametri[nome]
                if nome == "settimanaCorrente":
                    v = a_data(da_excel(v))
                elif isinstance(v, str):
                    v = per_cella(v)
                s.intervallo_nome(nome).Value = v
            if ciclo:                                # D-75: periodi delle viste scritti dallo script
                imposta_ciclo(scr, ciclo, data_periodo(scr, ciclo))
            ricostruisci_griglia(scr, modifiche)
            s.ricalcola()
            mancanti = formule_mancanti(s, mappa)
            errori = s.errori_formula()
            differenze = [f"{nome}: {len(righe)} righe prima, {len(scr.righe(nome))} dopo"
                          for nome, (_, righe) in dati.items() if len(scr.righe(nome)) != len(righe)]
            copertura_dopo = copertura_python(scr, ciclo)
            baseline_dopo = estrai_baseline(s, mappa)
            # D-79: i rischi in osservazione convertiti dalla lista sono la sola differenza ammessa; la regola del radar
            # (pesi, soglie, capienza) e' quella del template nuovo, come gli altri parametri.
            senza_osservazione = lambda b: {k: v for k, v in b.items() if k not in ("rischi_in_osservazione", "regola_radar")}
            problemi = ([f"formule mancanti: {mancanti[:5]}"] if mancanti else []) + \
                       ([f"errori di formula: {[e[:3] for e in errori[:5]]}"] if errori else []) + differenze + \
                       ([f"copertura {copertura_prima} prima, {copertura_dopo} dopo"] if copertura_dopo != copertura_prima else []) + \
                       (["la baseline estratta dal registro nuovo e' diversa da quella del vecchio"]
                        if senza_osservazione(baseline_dopo) != senza_osservazione(baseline_prima) else []) + \
                       ([f"rischi in osservazione {len(baseline_dopo['rischi_in_osservazione'])} nella baseline, convertiti "
                         f"{len(convertiti)}"] if len(baseline_dopo["rischi_in_osservazione"]) != len(convertiti)
                        + len(baseline_prima["rischi_in_osservazione"]) else [])
            if problemi:
                raise Fermo("Aggiornamento NON applicato, il registro vecchio resta com'e':\n  - " + "\n  - ".join(problemi))
            prepara_report(s)
            s.salva()
        # 3. Il vecchio va in Backup, il nuovo prende il suo posto (stesso nome, stesso percorso).
        copia = _cartella(conf, "Backup") / f"{vecchio.stem}_prima_di_aggiorna-registro_{dt.datetime.now():%Y%m%d_%H%M%S}{vecchio.suffix}"
        shutil.copy2(vecchio, copia)
        try:
            os.replace(nuovo, vecchio)
        except PermissionError:
            raise Fermo(f"{vecchio} e' aperto (in Excel o dalla sincronizzazione): chiuderlo e rilanciare. Nessuna modifica fatta.")
        SALVATO.update(registro=vecchio, backup=copia)   # da qui un errore tecnico e' "dopo il salvataggio"
    finally:
        if nuovo.exists():
            nuovo.unlink()
    pesi_vecchi = {k: parametri[k] for k in PESI if k in parametri}
    print(f"Registro aggiornato alla versione {VERSIONE_TEMPLATE} (era: {versione or 'precedente al 25/09/2026'}): {vecchio}\n"
          f"Righe copiate: " + ", ".join(f"{nome} {len(righe)}" for nome, (_, righe) in dati.items()) + "\n"
          f"Anagrafica: {len(anagrafica)} rischi; ciclo corrente {ciclo}; baseline identica a prima.\n"
          + (f"Lista di osservazione (D-73) convertita nel registro unico (D-79): "
             + ", ".join(f"{o} -> {r}" for o, r in codici_oss.items())
             + " ora sono rischi in osservazione, con valori convertiti in via provvisoria (Impatto = impatto potenziale, "
               "Probabilita dalla plausibilita', Prossimita dall'orizzonte): A1 li rivaluta al prossimo ciclo.\n"
             if codici_oss else "")
          + (f"Registro unico (D-79): i rischi dell'anagrafica sono nel radar; la regola (capienza, soglie) vale dal "
             f"prossimo ciclo.\n" if not codici_oss else "") +
          f""
          f"Pesi, soglie e anni per Prossimita (Z): quelli del template nuovo (D-50, D-59, D-61). Nel registro vecchio erano "
          f"{pesi_vecchi}: i punteggi compositi e l'urgenza di tutti i cicli sono ricalcolati.\n"
          + (f"Colonne rinominate: {rinominate}.\n" if any(v in c for n, (c, _) in dati.items() for v in rinominate.get(n, {})) else "")
          + (f"Colonne tolte dal modello, non copiate (restano nel registro vecchio): {lasciate}.\n" if lasciate else "")
          + (f"Righe ancora da validare: {righe_griglia([r for _, r in aperte])} (periodi "
             f"{', '.join(sorted({str(r['Periodo']) for _, r in aperte}))}), ora nel foglio Validazione, una riga per oggetto, "
             f"con cio' che era gia' stato scritto ({len(modifiche)} righe); validarle con il comando valida.\n" if aperte else "") +
          f"Registro vecchio conservato in: {copia}")
    # D-74: i rischi con i codici di Basilea restano fuori dal radar finche' A1 non li riclassifica.
    j = [c["nome"] for c in mappa["anagrafica"]["colonne"]].index("Event_Type")
    vecchi = sorted(str(r[0]) for r in anagrafica if len(r) > j and r[j] not in controlli_a5.CATEGORIE
                    and r[j] != controlli_a5.FUORI_PERIMETRO)
    if vecchi:
        print(f"TASSONOMIA (D-74): {len(vecchi)} rischi hanno ancora un codice di Basilea ({', '.join(vecchi)}): il radar non li "
              "mostra finche' A1 non li riclassifica nelle categorie interne al prossimo ciclo (o la funzione di rischio non "
              "corregge la categoria nell'anagrafica, Parametri colonna J).")


def main(argv=None):
    p = argparse.ArgumentParser(description="Scrittura A2 e controlli A5 per la variante senza Copilot Studio.")
    p.add_argument("--workbook")
    p.add_argument("--kernel")
    p.add_argument("--cartella-uscita", dest="cartella_uscita")
    sub = p.add_subparsers(dest="comando", required=True)
    t = sub.add_parser("trimestrale"); t.add_argument("--payload", required=True)
    t.add_argument("--challenger", help="output di A5 (facoltativo, D-71): i suoi rilievi vanno nella colonna Segnalazioni")
    # Fino al 05/10/2026 (D-56) servivano a non fermarsi sui Bloccanti di A5; dal 06/10 (D-71) non servono piu':
    # restano accettate per non rompere i comandi gia' in uso, e lo script lo dice.
    t.add_argument("--procedi-con-rilievi", dest="procedi_con_rilievi", action="store_true", help=argparse.SUPPRESS)
    t.add_argument("--motivo", help=argparse.SUPPRESS)
    t.add_argument("--decisore", help=argparse.SUPPRESS)
    w = sub.add_parser("settimanale"); w.add_argument("--payload", required=True)
    b = sub.add_parser("baseline"); b.add_argument("--uscita")
    b.add_argument("--straordinario", action="store_true", help="decide un ciclo straordinario (D-75): con --rischi, --motivo, --decisore")
    b.add_argument("--rischi", help="rischi da rivalutare nello straordinario, separati da virgole (NFR-01,NFR-07)")
    b.add_argument("--motivo", help="l'evento critico e perche' non puo' aspettare il trimestre (almeno 20 caratteri)")
    b.add_argument("--decisore", help="chi decide lo straordinario: una funzione o un comitato")
    b.add_argument("--data", help="data di riferimento dello straordinario, AAAA-MM-GG (default: oggi)")
    pc = sub.add_parser("precontrollo", help="facoltativo: controlla l'output di A1 prima di A5 (senza Excel) e scrive il messaggio di correzione")
    pc.add_argument("--payload", required=True)
    pc.add_argument("--baseline", help="baseline da usare (default: Baseline_corrente.json nella cartella di uscita)")
    v = sub.add_parser("valida", help="applica la griglia del foglio Validazione per un ciclo o una settimana")
    v.add_argument("--periodo", required=True, help="ciclo (2026Q3) o lunedi' della settimana (2026-10-12)")
    v.add_argument("--validatore", required=True, help="chi valida: una funzione o un comitato")
    # Fino al 2026-10-01 accettava le righe senza Decisione; con la griglia (D-67) una riga non toccata e' gia'
    # accettata: resta solo per non rompere i comandi gia' in uso, e lo dice.
    v.add_argument("--accetta-il-resto", dest="accetta_il_resto", action="store_true", help=argparse.SUPPRESS)
    sub.add_parser("griglia", help="ricostruisce il foglio Validazione dalle proposte da decidere (dopo una modifica a mano)")
    ra = sub.add_parser("riapri", help="riapre la validazione del ciclo corrente, gia' validato, per cambiare dei valori (D-76)")
    ra.add_argument("--rischi", help="solo questi rischi, con i loro KRI e azioni (NFR-02,NFR-06); senza: tutto")
    i = sub.add_parser("inizializza", help="crea il registro vivo dal template, senza dati di esempio")
    i.add_argument("--ciclo-precedente", dest="ciclo_precedente", required=True,
                   help="il trimestre PRIMA del primo da valutare (es. 2026Q3 per valutare il 2026Q4)")
    i.add_argument("--settimana", required=True, help="lunedi' della settimana corrente, AAAA-MM-GG")
    i.add_argument("--template", help="template da usare (default: 03_Excel/NFR_Dashboard_Template.xlsx)")
    d = sub.add_parser("dismetti", help="toglie un rischio dall'anagrafica lasciandone la storia")
    d.add_argument("--rischio", required=True, help="ID del rischio, es. NFR-04")
    d.add_argument("--motivazione", required=True, help="perche' il rischio esce (almeno 10 caratteri)")
    d.add_argument("--decisore", required=True, help="chi ha deciso: una funzione o un comitato")
    sub.add_parser("schede-input", help="dopo la validazione: input dell'agente A6 per le schede dei rischi")
    sc = sub.add_parser("schede", help="dopo la validazione: file delle schede dei rischi (con l'output di A6 o senza)")
    sc.add_argument("--payload", help="output di A6 (A6_<ciclo>.json); senza, testi di A1 dal registro")
    r = sub.add_parser("report", help="rigenera il PDF del report al comitato dall'Excel, dopo modifiche manuali")
    r.add_argument("--file", help="Excel da cui fare il report (default: il registro vivo)")
    r.add_argument("--con-lavoro", dest="con_lavoro", action="store_true", help="aggiunge i fogli Registro e Parametri")
    a = sub.add_parser("aggiorna-registro", help="porta il registro vivo sul template nuovo, senza perdere dati")
    a.add_argument("--template", help="template da usare (default: 03_Excel/NFR_Dashboard_Template.xlsx)")
    arg = p.parse_args(argv)
    conf = configurazione(arg)
    try:
        if arg.comando not in ("inizializza", "precontrollo") and (not conf["workbook"] or not conf["workbook"].exists()):
            print(f"Workbook non trovato: {conf['workbook']}")
            return 2
        if arg.comando == "inizializza" and not conf["workbook"]:
            print("Manca il percorso del registro da creare: --workbook o 'workbook' in configurazione.json.")
            return 2
        codice = {"trimestrale": comando_trimestrale, "settimanale": comando_settimanale,
                  "baseline": comando_baseline, "precontrollo": comando_precontrollo,
                  "valida": comando_valida, "griglia": comando_griglia, "riapri": comando_riapri,
                  "inizializza": comando_inizializza, "dismetti": comando_dismetti,
                  "aggiorna-registro": comando_aggiorna_registro, "schede-input": comando_schede_input,
                  "schede": comando_schede, "report": comando_report}[arg.comando](arg, conf)
        return codice or 0
    except Fermo as e:
        print(f"FERMATO — il workbook non e' stato modificato.\n{e}")
        return 1
    except Exception as e:
        if SALVATO["registro"]:                      # errore DOPO il salvataggio: il registro e' gia' scritto
            print(f"ERRORE TECNICO DOPO IL SALVATAGGIO — il registro {SALVATO['registro']} E' STATO SCRITTO E SALVATO "
                  f"(stato prima: {SALVATO['backup']}). NON rilanciare lo stesso comando.\n"
                  f"Non completato: {type(e).__name__}: {e}\n"
                  "Rimuovere la causa (es. chiudere un file aperto nell'archivio) e completare a mano l'archivio: "
                  "l'Excel di output e' una copia del registro con il nome del ciclo o della settimana.")
        else:                                        # errore prima del salvataggio: nessun byte scritto
            print(f"ERRORE TECNICO — il workbook non e' stato salvato: {type(e).__name__}: {e}")
        return 2


if __name__ == "__main__":
    sys.exit(main())
