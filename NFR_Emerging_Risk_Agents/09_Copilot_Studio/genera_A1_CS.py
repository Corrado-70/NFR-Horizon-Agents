"""A1 per Copilot Studio con variabili globali (prova K6-ter, 22/10/2026).

Per chi mantiene il pacchetto, come componi_prompt.py: rilanciarlo dopo ogni modifica a
02_Agenti/A1_Horizon_Scanner.md. Il collaudo (test_controlli.py, test_a1_copilot_studio) si ferma se il file
generato non corrisponde all'A1 attuale.

Parte dalle istruzioni di A1 per Microsoft 365 e cambia solo:
  Input    l'allegato Input_A1 e' il valore della variabile globale {Global.allegato};
  Output   la risposta e' solo il JSON e la stessa risposta va nella variabile globale {Global.json_a1}
           (schema riuscito in Banca il 22/10);
  analisi  piu' ricerche nella knowledge per ogni rischio e rianalisi finale mirata (fonti della baseline,
           variazioni, un punto), in prova solo qui: il primo run in Copilot Studio e' durato un minuto;
  spazio   elenchi senza trattino e senza righe vuote, due titoli piu' corti, modelli dei razionali ridotti ai
           puntini (li descrive la guida di scrittura dell'allegato), per restare sotto 8.000 caratteri con il
           margine per le variabili inserite con "/".
Scale, regole, KRI e schema del JSON restano identici.

Scrive Da_caricare/A1_Horizon_Scanner_CS.md. In Copilot Studio i due segnaposto si sostituiscono con le variabili
vere, inserite con "/": il testo scritto a mano non diventa una variabile.

Uso:  python 09_Copilot_Studio/genera_A1_CS.py
Solo libreria standard.
"""

import re
import sys
from pathlib import Path

QUI = Path(__file__).resolve().parent
SORGENTE = QUI.parent / "02_Agenti" / "A1_Horizon_Scanner.md"
USCITA = QUI / "Da_caricare" / "A1_Horizon_Scanner_CS.md"
LIMITE = 8000
MARGINE = 60                      # caratteri lasciati alle variabili inserite con "/" (segnaposto di 16-17)
VAR_IN, VAR_OUT = "{Global.allegato}", "{Global.json_a1}"

SOSTITUZIONI = [
    # Variabili globali (K6-ter, 22/10)
    ("Allegato Input_A1: baseline, controlli di A5, guida di scrittura.",
     f"Allegato Input_A1 = valore di {VAR_IN}: baseline, controlli di A5, guida di scrittura."),
    ("Solo JSON, nessun testo attorno. Date AAAA-MM-GG.",
     f"Solo JSON, nessun testo attorno; la stessa risposta va in {VAR_OUT}. Date AAAA-MM-GG."),
    # Analisi a fondo e rianalisi (22/10): il primo run in Copilot Studio e' durato un minuto e ha perso fonti
    # su quattro rischi e una voce di variazione. La frase del ruolo (D-64) passa nell'Input, accanto alla ricerca.
    (" Prima di valutare analizza nel dettaglio ogni fonte.", ""),
    ("Utilizza **sempre** lo strumento di ricerca file o altri strumenti di ricerca aziendale per accedere ai file "
     "della knowledge.",
     "Usa sempre la ricerca file o aziendale: piu' ricerche per rischio (nome, meccanismo, fonti della baseline); "
     "leggi e analizza nel dettaglio ogni fonte prima di valutare."),
    ("10. Verifica con controlli e guida dell'allegato e correggi.",
     "10. Rianalizza tutto con controlli e guida (fonti valide della baseline riprese, una voce in variazioni per "
     "valore cambiato, max un punto); correggi."),
    # Spazio: titoli piu' corti; i modelli dei razionali li descrive la guida di scrittura dell'allegato.
    ("## Categorie di rischio (tassonomia interna, in perimetro)", "## Categorie (in perimetro)"),
    ("## Regole di variazione fra cicli", "## Regole di variazione"),
    ('"RISCHIO: causa, evento, danno. IMPATTO: fatto e documento. PROBABILITA: ... PROSSIMITA: ... VELOCITY: ... '
     'ADEGUAMENTO: se serve"',
     '"RISCHIO: ... IMPATTO: ... PROBABILITA: ... PROSSIMITA: ... VELOCITY: ... ADEGUAMENTO: ..."'),
    ('"razionale":"perche\'. EFFETTO: cosa cambia"', '"razionale":"perche\'. EFFETTO: ..."'),
    ('"razionale":"cosa misura. EFFETTO: andamento atteso"', '"razionale":"cosa misura. EFFETTO: ..."'),
]


def versione_cs(testo):
    """Le istruzioni di A1 per Copilot Studio a partire da quelle per Microsoft 365."""
    for vecchio, nuovo in SOSTITUZIONI:
        if testo.count(vecchio) != 1:
            raise ValueError(f"frase non trovata una volta sola in A1_Horizon_Scanner.md: {vecchio[:60]}...")
        testo = testo.replace(vecchio, nuovo)
    testo = re.sub(r"(?m)^- ", "", testo)            # elenchi: stesso contenuto, senza trattino
    return re.sub(r"\n\n(?=\S)", "\n", testo)        # niente righe vuote


def main():
    try:
        testo = versione_cs(SORGENTE.read_text(encoding="utf-8"))
    except ValueError as errore:
        sys.exit(f"Fermo: {errore}. Aggiornare SOSTITUZIONI in genera_A1_CS.py.")
    if len(testo) > LIMITE - MARGINE:
        sys.exit(f"Fermo: {len(testo)} caratteri, oltre {LIMITE - MARGINE} (limite {LIMITE} meno il margine per le "
                 "variabili). Accorciare A1 o le sostituzioni.")
    USCITA.write_text(testo, encoding="utf-8", newline="\n")
    print(f"{USCITA.relative_to(QUI.parent)}: {len(testo)} caratteri (limite {LIMITE}, margine {MARGINE})")


if __name__ == "__main__":
    main()
