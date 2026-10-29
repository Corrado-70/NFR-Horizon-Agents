"""Copilot Studio pieno (D-82): istruzioni dei sotto-agenti, testi dei prompt, feed, controllo degli argomenti.

Per chi mantiene il pacchetto, come componi_prompt.py: rilanciarlo dopo ogni modifica a 02_Agenti/*.md, a
01_Kernel/fonti.md o agli argomenti in Da_caricare/argomenti. Il collaudo (test_controlli.py,
test_copilot_studio_pieno) si ferma se un file generato non corrisponde ai sorgenti o se un argomento non passa i
controlli. Sostituisce genera_A1_CS.py (K6-ter): stesse sostituzioni per A1, variabili globali rinominate.

Scrive in Da_caricare/:
  agenti/A1_CS.md, A8_CS.md, A3_CS.md
      istruzioni dei sotto-agenti, che leggono la knowledge. L'ingresso e' il valore di {Global.ingresso};
      la risposta, solo JSON, va in {Global.uscita}; A3 legge la settimana da {Global.periodo}. Sotto 8.000
      caratteri con il margine per le variabili inserite con "/" (il testo scritto a mano non diventa variabile).
  prompt/A5.txt, A6.txt, Correggi.txt, Motore.txt
      testi dei prompt (strumenti senza knowledge, chiamati dal flusso NFR_Motore). Ogni [nome] in fondo e' un
      ingresso di testo da creare con Add content -> Text, con lo stesso nome.
  flussi/Fonti_rss.json
      i feed approvati di 01_Kernel/fonti.md, da incollare nel flusso Raccolta_notizie.
Controlla argomenti/*.yaml: prima riga kind: AdaptiveDialog, niente tab, id unici, solo i segnaposto <<...>> di
ID_tenant.txt, solo le variabili globali del progetto, solo i tipi di nodo noti.

Uso:  python 09_Copilot_Studio/genera_CS.py            scrive e controlla
      python 09_Copilot_Studio/genera_CS.py --verifica  non scrive; codice 1 se un file e' fuori data o un
                                                        argomento non passa i controlli
Solo libreria standard.
"""

import json
import re
import sys
from pathlib import Path

QUI = Path(__file__).resolve().parent
PACCHETTO = QUI.parent
AGENTI = PACCHETTO / "02_Agenti"
CARICARE = QUI / "Da_caricare"
ARGOMENTI = CARICARE / "argomenti"
ID_TENANT = CARICARE / "ID_tenant.txt"
sys.path.insert(0, str(PACCHETTO / "07_Senza_Studio"))
from fonti import leggi_fonti   # noqa: E402  un solo lettore dell'elenco fonti

LIMITE = 8000
MARGINE = 60                      # caratteri lasciati alle variabili inserite con "/"
VAR_IN, VAR_OUT, VAR_PERIODO = "{Global.ingresso}", "{Global.uscita}", "{Global.periodo}"
GLOBALI = {"periodo", "ingresso", "uscita"}
NODI = {"AdaptiveDialog", "OnActivity", "SendActivity", "SetVariable", "ConditionGroup", "Question",
        "InvokeFlowAction", "BeginDialog", "CancelAllDialogs"}

# Accorciamenti comuni ad A1 e A8 (K6-ter): titoli piu' corti e modelli dei razionali ridotti ai puntini, che
# descrive la guida di scrittura dell'allegato.
ACCORCIA = [
    ("## Categorie di rischio (tassonomia interna, in perimetro)", "## Categorie (in perimetro)"),
    ("## Regole di variazione fra cicli", "## Regole di variazione"),
    ('"RISCHIO: causa, evento, danno. IMPATTO: fatto e documento. PROBABILITA: ... PROSSIMITA: ... VELOCITY: ... '
     'ADEGUAMENTO: se serve"',
     '"RISCHIO: ... IMPATTO: ... PROBABILITA: ... PROSSIMITA: ... VELOCITY: ... ADEGUAMENTO: ..."'),
    ('"razionale":"perche\'. EFFETTO: cosa cambia"', '"razionale":"perche\'. EFFETTO: ..."'),
    ('"razionale":"cosa misura. EFFETTO: andamento atteso"', '"razionale":"cosa misura. EFFETTO: ..."'),
]

SOTTO_AGENTI = {
    "A1_CS.md": ("A1_Horizon_Scanner.md", [
        ("Allegato Input_A1: baseline, controlli di A5, guida di scrittura.",
         f"Allegato Input_A1 = valore di {VAR_IN}: baseline, controlli di A5, guida di scrittura."),
        ("Solo JSON, nessun testo attorno. Date AAAA-MM-GG.",
         f"Solo JSON, nessun testo attorno; la stessa risposta va in {VAR_OUT}. Date AAAA-MM-GG."),
        # Analisi a fondo e rianalisi (K6-ter, 22/10): il primo run in Copilot Studio e' durato un minuto e ha perso
        # fonti su quattro rischi. La frase del ruolo (D-64) passa nell'Input, accanto alla ricerca.
        (" Prima di valutare analizza nel dettaglio ogni fonte.", ""),
        ("Utilizza **sempre** lo strumento di ricerca file o altri strumenti di ricerca aziendale per accedere ai file "
         "della knowledge.",
         "Usa sempre la ricerca file o aziendale: piu' ricerche per rischio (nome, meccanismo, fonti della baseline); "
         "leggi e analizza nel dettaglio ogni fonte prima di valutare."),
        ("10. Verifica con controlli e guida dell'allegato e correggi.",
         "10. Rianalizza tutto con controlli e guida (fonti valide della baseline riprese, una voce in variazioni per "
         "valore cambiato, max un punto); correggi."),
    ] + ACCORCIA),
    "A8_CS.md": ("A8_Evento_critico.md", [
        ("Allegato Input_A8 dello straordinario (baseline, controlli, guida) e documenti sull'evento dati "
         "dall'utente.",
         f"Allegato Input_A8 dello straordinario = valore di {VAR_IN} (baseline, controlli, guida). Documenti "
         "sull'evento: in knowledge, Analisi_Esterne, cartella Eventi/<ciclo_da_valutare>."),
        ("Utilizza **sempre** lo strumento di ricerca file o altri strumenti di ricerca aziendale per accedere ai file "
         "della knowledge.",
         "Usa sempre la ricerca file o aziendale per la knowledge."),
        ("Solo JSON, nessun testo attorno. Date AAAA-MM-GG.",
         f"Solo JSON, nessun testo attorno; la stessa risposta va in {VAR_OUT}. Date AAAA-MM-GG."),
    ] + ACCORCIA),
    "A3_CS.md": ("A3_Interim_Update.md", [
        ("Baseline: SOLO l'allegato Input_A3_A4.txt della chat, mai dalla knowledge;",
         f"Baseline: SOLO il valore di {VAR_IN} (Input_A3_A4.txt), mai dalla knowledge;"),
        ("1. settimana = data del lunedi' della settimana in corso (AAAA-MM-GG).",
         f"1. settimana = valore di {VAR_PERIODO} (lunedi', AAAA-MM-GG)."),
        ("Solo JSON, nessun testo attorno, nessun campo in piu'. Date AAAA-MM-GG.",
         f"Solo JSON, nessun testo attorno, nessun campo in piu'; la stessa risposta va in {VAR_OUT}. Date "
         "AAAA-MM-GG."),
    ]),
}

# Prompt: niente knowledge, ingresso e uscita fissi (output record, testo nel campo text). Gli ingressi sono in fondo.
PROMPT = {
    "A5.txt": ("A5_Challenger.md", [
        ("Solo l'allegato Input_A5_<ciclo>.txt: parte 1 l'output di A1 (JSON), parte 2 la baseline, parte 3 le lunghezze "
         "minime dei testi.",
         "Solo il testo in fondo: INPUT_A5, cioe' Input_A5_<ciclo>.txt: parte 1 l'output di A1 (JSON), parte 2 la baseline, "
         "parte 3 le lunghezze minime dei testi (C10, D-86)."),
    ], "INPUT_A5: [input_a5]"),
    "A6.txt": ("A6_Schede.md", [
        ("Un solo file allegato: Input_A6_<ciclo>.json, scritto dallo script dal registro validato.",
         "Un solo testo, in fondo: INPUT_A6, cioe' Input_A6_<ciclo>.json, scritto dal motore dal registro "
         "validato."),
    ], "INPUT_A6: [input_a6]"),
}

CORREGGI = """Sei l'agente che ha prodotto JSON_A1: A1 Horizon Scanner, o A8 Evento critico in un ciclo straordinario. Il controllo del motore vi ha trovato i punti in CORREZIONE.
Correggi solo quei punti, usando la baseline, i controlli (parte 2) e la guida di scrittura (parte 3) di ALLEGATO. Tutto il resto resta identico: stessi rischi, id, valori, fonti e testi.
"Da correggere": correggi sempre.
"Da verificare": correggi se il punto e' fondato; se confermi il valore, scrivi il perche' nel razionale del rischio.
Ogni valore diverso dal ciclo precedente ha una voce in variazioni, con un'evidenza specifica datata dopo il ciclo precedente; al massimo un punto per dimensione.
Fonti: riprendi quelle della baseline ancora valide.
Rispondi solo con il JSON intero corretto: nessun testo attorno, nessun blocco di codice.
CORREZIONE: [correzione]
JSON_A1: [json_a1]
ALLEGATO: [allegato]
"""

# Prompt con code interpreter (prova K9): esegue il codice del motore che sta nel file, non codice suo. La sandbox
# non lancia processi (23/10: "python motore.py" rifiutato), quindi il motore gira nella sessione con runpy. Il
# caricatore e' lo stesso che prepara_busta.py esegue sul PC: cambiano solo i due valori fra virgolette.
CARICATORE = """import runpy, sys
import openpyxl
busta = r"PERCORSO_DELLA_BUSTA"
comando = "NOME_DEL_COMANDO"
foglio = openpyxl.load_workbook(busta)["_Motore"]
codice = "".join(r[0] for r in foglio.iter_rows(min_row=2, max_col=1, values_only=True) if r[0])
with open("motore.py", "w", encoding="utf-8", newline="\\n") as f:
    f.write(codice)
sys.argv = ["motore.py", busta, comando]
try:
    runpy.run_path("motore.py", run_name="__main__")
except SystemExit:
    pass
"""
MOTORE = """Esegui un programma gia' scritto, contenuto nel file in ingresso. Non scrivere codice tuo, non riassumere, non interpretare i risultati.
1. Esegui nel code interpreter, in questa sessione, esattamente il codice qui sotto. Cambia solo i due valori fra virgolette: PERCORSO_DELLA_BUSTA con il percorso del file in ingresso, NOME_DEL_COMANDO con il COMANDO scritto in fondo. Non lanciare processi esterni: il codice esegue motore.py nella stessa sessione.
2. Rispondi solo con la riga JSON che il codice stampa, copiata identica.
3. Se l'esecuzione fallisce, rispondi solo ERRORE: seguito dal messaggio copiato identico. Non riprovare con codice diverso.
```python
""" + CARICATORE + """```
COMANDO: [comando]
BUSTA: [busta]
"""


def compatta(testo):
    """Stesso contenuto in meno caratteri: elenchi senza trattino, niente righe vuote (K6-ter)."""
    testo = re.sub(r"(?m)^- ", "", testo)
    return re.sub(r"\n\n(?=\S)", "\n", testo)


def sostituisci(testo, sostituzioni, sorgente):
    for vecchio, nuovo in sostituzioni:
        if testo.count(vecchio) != 1:
            raise ValueError(f"frase non trovata una volta sola in {sorgente}: {vecchio[:60]}...")
        testo = testo.replace(vecchio, nuovo)
    return testo


def sotto_agente(nome):
    sorgente, sostituzioni = SOTTO_AGENTI[nome]
    return compatta(sostituisci((AGENTI / sorgente).read_text(encoding="utf-8"), sostituzioni, sorgente))


def prompt(nome):
    if nome == "Correggi.txt":
        return CORREGGI
    if nome == "Motore.txt":
        return MOTORE
    sorgente, sostituzioni, ingressi = PROMPT[nome]
    return compatta(sostituisci((AGENTI / sorgente).read_text(encoding="utf-8"), sostituzioni, sorgente)).rstrip("\n") \
        + "\n" + ingressi + "\n"


def ingressi(testo):
    """I nomi fra parentesi quadre delle righe in fondo al prompt (MAIUSCOLE: [nome])."""
    return re.findall(r"(?m)^[A-Z_0-9]+: \[([a-z_0-9]+)\]$", testo)


def feed_rss():
    fonti = leggi_fonti(PACCHETTO / "01_Kernel" / "fonti.md")
    elenco = [{"codice": f["codice"], "nome": f["nome"], "indirizzo": f["indirizzo"], "escludi": f["escludi"],
               "max_voci": f["max_voci"]}
              for f in fonti if f["canale"] == "rss" and f["stato"] == "approvata" and f["indirizzo"].startswith("http")]
    return json.dumps(elenco, ensure_ascii=False, indent=1) + "\n"


def file_generati():
    """{percorso: testo atteso} di tutti i file che questo script scrive."""
    out = {CARICARE / "agenti" / nome: sotto_agente(nome) for nome in SOTTO_AGENTI}
    out.update({CARICARE / "prompt" / nome: prompt(nome) for nome in ("A5.txt", "A6.txt", "Correggi.txt", "Motore.txt")})
    out[CARICARE / "flussi" / "Fonti_rss.json"] = feed_rss()
    return out


def segnaposto_noti():
    return set(re.findall(r"(?m)^(<<[A-Za-z0-9_]+>>)", ID_TENANT.read_text(encoding="utf-8")))


def controlla_argomento(testo, noti):
    """Problemi di un argomento YAML (lista vuota se va bene). Controlli testuali: il pacchetto non usa PyYAML."""
    problemi = []
    if not testo.startswith("kind: AdaptiveDialog\n"):
        problemi.append("la prima riga deve essere kind: AdaptiveDialog")
    if "\t" in testo:
        problemi.append("contiene tabulazioni")
    for n, riga in enumerate(testo.splitlines(), start=1):
        rientro = len(riga) - len(riga.lstrip(" "))
        if riga.strip() and rientro % 2:
            problemi.append(f"riga {n}: rientro dispari")
    ids = re.findall(r"(?m)^\s*(?:- )?id: (\S+)$", testo)
    doppi = sorted({i for i in ids if ids.count(i) > 1})
    if doppi:
        problemi.append(f"id ripetuti: {doppi}")
    ignoti = sorted(set(re.findall(r"<<[A-Za-z0-9_]+>>", testo)) - noti)
    if ignoti:
        problemi.append(f"segnaposto non in ID_tenant.txt: {ignoti}")
    globali = sorted(set(re.findall(r"Global\.(\w+)", testo)) - GLOBALI)
    if globali:
        problemi.append(f"variabili globali fuori elenco: {globali}")
    nodi = sorted(set(re.findall(r"(?m)^\s*(?:- )?kind: (\w+)$", testo)) - NODI)
    if nodi:
        problemi.append(f"tipi di nodo non previsti: {nodi}")
    if not re.search(r"(?m)^  kind: OnActivity\n  id: main\n  type: Message\n  condition: =StartsWith\(System\.Activity\.Text, \"\w+\"\)$", testo):
        problemi.append("trigger atteso: OnActivity, type Message, condition =StartsWith(System.Activity.Text, \"Comando\")")
    return problemi


def controlla_argomenti():
    noti = segnaposto_noti()
    return {p.name: controlla_argomento(p.read_text(encoding="utf-8"), noti) for p in sorted(ARGOMENTI.glob("*.yaml"))}


def main(argv):
    verifica = argv[1:] == ["--verifica"]
    errori = []
    try:
        attesi = file_generati()
    except ValueError as errore:
        print(f"Fermo: {errore}. Aggiornare le sostituzioni in genera_CS.py.")
        return 1
    for percorso, testo in attesi.items():
        nome = percorso.relative_to(QUI).as_posix()
        if percorso.parent.name in ("agenti", "prompt") and percorso.suffix in (".md", ".txt"):
            limite = LIMITE - MARGINE if percorso.parent.name == "agenti" else LIMITE
            if len(testo) > limite:
                errori.append(f"{nome}: {len(testo)} caratteri, oltre {limite}")
        if verifica:
            if not percorso.exists() or percorso.read_text(encoding="utf-8") != testo:
                errori.append(f"{nome}: fuori data (python 09_Copilot_Studio/genera_CS.py)")
        else:
            percorso.parent.mkdir(parents=True, exist_ok=True)
            if not percorso.exists() or percorso.read_text(encoding="utf-8") != testo:
                percorso.write_text(testo, encoding="utf-8", newline="\n")
            print(f"{nome}: {len(testo)} caratteri")
    for nome, problemi in controlla_argomenti().items():
        errori.extend(f"argomenti/{nome}: {p}" for p in problemi)
    for e in errori:
        print("ERRORE " + e)
    print(f"{len(attesi)} file generati, {len(list(ARGOMENTI.glob('*.yaml')))} argomenti: "
          + ("tutto in ordine" if not errori else f"{len(errori)} problemi"))
    return 1 if errori else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
