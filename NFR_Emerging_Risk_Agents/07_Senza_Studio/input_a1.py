"""Allegati degli agenti: Input_<agente> (D-84, 23/10/2026).

  Input_A1_<ciclo>.txt     A1: baseline, controlli di A5 e guida di scrittura (D-69);
  Input_A8_<periodo>.txt   A8, ciclo straordinario AAAAQn-Sk: lo stesso contenuto, con il blocco dello straordinario;
  Input_A3_A4.txt          A3 e A4: la sola baseline (AU7);
  Input_A5_<ciclo>.txt     A5: l'output di A1 (o A8) e la baseline, scritto dal precontrollo;
  Input_A6_<ciclo>.json    A6: i dati validati del ciclo (comando schede-input, schede.py).
Tutti accanto a Baseline_corrente.json nella cartella di uscita, tranne quello di A6 (cartella del ciclo); di ogni
tipo resta solo quello giusto: i vecchi si tolgono.

D-69 (02/10/2026). Le istruzioni di A1 sono al limite degli 8.000 caratteri:
i controlli che A5 applichera' al suo output (01_Kernel/controlli_A5.md) e la
guida di scrittura (01_Kernel/guida_scrittura_A1.md) viaggiano nell'allegato
che A1 riceve comunque a ogni ciclo, accanto alla baseline. Un file solo, un
solo gesto per chi lancia A1; testo semplice, che gli allegati e la knowledge
di Agent Builder leggono (i .json la knowledge non li legge).

Un solo lettore dei controlli per tutti: questo modulo (allegato di A1),
02_Agenti/componi_prompt.py (segnaposto {{CONTROLLI}} nel prompt di A5) e il
collaudo. Dal 05/10/2026 (D-70) e' anche dentro lo script della skill di
Copilot Studio, che legge la baseline dall'allegato (leggi_baseline). Solo
libreria standard.
"""

import json
import re
from pathlib import Path

FILE_CONTROLLI = "controlli_A5.md"
FILE_GUIDA = "guida_scrittura_A1.md"
PREFISSO = "Input_A1"
PREFISSO_STRAORDINARIO = "Input_A8"                  # D-84: l'allegato dello straordinario e' di A8 (D-77)
INIZIO_BASELINE = "=== 1. BASELINE ==="


def testo_kernel(percorso):
    """Il file senza le note (righe ">") e senza il titolo ("# ")."""
    righe = [r.rstrip() for r in Path(percorso).read_text(encoding="utf-8").splitlines()
             if not r.startswith(">") and not r.startswith("# ")]
    return re.sub(r"\n{3,}", "\n\n", "\n".join(righe)).strip()


def testo_controlli(kernel):
    return testo_kernel(Path(kernel) / FILE_CONTROLLI)


def prefisso(ciclo):
    return PREFISSO_STRAORDINARIO if "-S" in str(ciclo or "") else PREFISSO


def nome_file(baseline):
    ciclo = baseline.get("ciclo_da_valutare")
    return f"{prefisso(ciclo)}_{ciclo}.txt" if ciclo else f"{PREFISSO}.txt"


def componi(baseline, kernel, oggi):
    """(testo dell'allegato, file del kernel mancanti). Un file mancante non
    ferma niente, perche' la baseline basta ad A1 per lavorare, ma va detto:
    senza controlli e guida A1 risponde come prima del 02/10/2026."""
    kernel = Path(kernel)
    mancanti = [n for n in (FILE_CONTROLLI, FILE_GUIDA) if not (kernel / n).exists()]
    ciclo = baseline.get("ciclo_da_valutare") or "da valutare"
    agente = prefisso(baseline.get("ciclo_da_valutare")).split("_")[1]
    parti = [f"INPUT DI {agente} PER IL CICLO {ciclo}: scritto da esegui_ciclo_locale.py il {oggi}, da non modificare a mano.",
             "Tre parti: 1. BASELINE (JSON); 2. CONTROLLI che lo script (e A5 Challenger, se usato) applicano al tuo "
             "output; 3. GUIDA DI SCRITTURA.",
             "", INIZIO_BASELINE, json.dumps(baseline, ensure_ascii=False, indent=2)]
    s = baseline.get("straordinario")
    if s:                                            # D-75: in testa, perche' cambia che cosa A1 deve scrivere
        cosa = (f"Valuta SOLO questi rischi: {', '.join(s['rischi_da_rivalutare'])} (e un rischio nuovo solo se l'evento "
                "lo crea)" if s["rischi_da_rivalutare"] else
                "Nessun rischio da rivalutare: censisci SOLO i rischi nuovi che l'evento crea (almeno uno)")
        parti[2:2] = ["", f"CICLO STRAORDINARIO {ciclo}, deciso da {s['decisore']} il {s['data_decisione']}: {s['motivo']}",
                      f"{cosa}; gli altri restano com'erano. Scrivi anche analisi_evento. Regole nella guida di scrittura, "
                      "sezione \"Ciclo straordinario\"."]
    if FILE_CONTROLLI not in mancanti:
        parti += ["", "=== 2. CONTROLLI ===",
                  "Prima di rispondere verifica ogni rischio con questi controlli e correggi. Li applicano lo script e, se "
                  "usato, A5 Challenger: un difetto di completezza o di coerenza (C1, C2, C7, identificativi dei KRI) "
                  "ferma il ciclo e torna a te; ogni altro rilievo arriva al validatore, che dovra' motivarlo uno per uno.",
                  testo_controlli(kernel)]
    if FILE_GUIDA not in mancanti:
        parti += ["", "=== 3. GUIDA DI SCRITTURA ===", testo_kernel(kernel / FILE_GUIDA)]
    return "\n".join(parti) + "\n", mancanti


def leggi_baseline(testo):
    """La baseline dal testo di un allegato Input_A1, Input_A8 o Input_A3_A4 (il JSON della parte 1): la skill di
    Copilot Studio riceve solo l'allegato (D-70). ValueError se il testo non e' un allegato con la baseline."""
    inizio = testo.find(INIZIO_BASELINE)
    graffa = testo.find("{", inizio) if inizio >= 0 else -1
    if graffa < 0:
        raise ValueError(f"non e' un allegato {PREFISSO}: manca la parte \"{INIZIO_BASELINE}\" con il JSON della baseline")
    return json.JSONDecoder().raw_decode(testo, graffa)[0]


# AU7 (23/10/2026): A3 e A4 ricevono la baseline come allegato della chat, come A1, e non piu' dal file
# Baseline_corrente.txt nella knowledge (indicizzazione lenta, file singolo saltato: "Baseline mancante" del 13/10).
# D-84: un file solo per i due agenti, perche' il contenuto e' lo stesso.
FILE_A3_A4 = "Input_A3_A4.txt"
VECCHI_A3_A4 = ("Input_A3.txt", "Input_A4.txt")          # nomi fino alla sera del 23/10/2026: si tolgono


def componi_baseline(baseline, oggi):
    """Allegato di A3 e A4: intestazione con ciclo e data di riferimento, poi la baseline (JSON)."""
    prec = baseline.get("ciclo_precedente") or "nessuno"
    data = baseline.get("data_riferimento_precedente") or "n.d."
    # "dopo il ciclo", non "ciclo validato": la baseline si riscrive anche dopo trimestrale, prima della validazione.
    return (f"INPUT DI A3 E A4: baseline del registro NFR dopo il ciclo {prec} (data di riferimento {data}), scritta da "
            f"esegui_ciclo_locale.py il {oggi}, da non modificare a mano. Rischi del radar in \"rischi\", in osservazione "
            "in \"rischi_in_osservazione\".\n\n"
            f"{INIZIO_BASELINE}\n{json.dumps(baseline, ensure_ascii=False, indent=2)}\n")


def scrivi_allegato_a3_a4(cartella, baseline, oggi):
    """Scrive Input_A3_A4.txt accanto a Baseline_corrente (e toglie i due file con i nomi di prima)."""
    percorso = Path(cartella) / FILE_A3_A4
    percorso.write_text(componi_baseline(baseline, oggi), encoding="utf-8")
    for vecchio in VECCHI_A3_A4:
        try:
            (Path(cartella) / vecchio).unlink(missing_ok=True)
        except OSError:
            pass
    return percorso


# D-84: A5 riceve un file solo, come gli altri agenti: l'output di A1 (o A8) che esamina e la baseline usata.
PREFISSO_A5 = "Input_A5"
INIZIO_OUTPUT = "=== 1. OUTPUT DI A1 ==="
INIZIO_BASELINE_A5 = "=== 2. BASELINE ==="


def componi_a5(payload, baseline, oggi):
    ciclo = payload.get("ciclo") or baseline.get("ciclo_da_valutare") or "da valutare"
    autore = prefisso(ciclo).split("_")[1]
    return (f"INPUT DI A5 PER IL CICLO {ciclo}: l'output di {autore} da esaminare e la baseline su cui e' stato scritto, "
            f"scritto da esegui_ciclo_locale.py il {oggi}, da non modificare a mano.\n\n"
            f"{INIZIO_OUTPUT}\n{json.dumps(payload, ensure_ascii=False, indent=2)}\n\n"
            f"{INIZIO_BASELINE_A5}\n{json.dumps(baseline, ensure_ascii=False, indent=2)}\n")


def leggi_a5(testo):
    """(output di A1, baseline) dal testo di un allegato Input_A5. ValueError se non lo e'."""
    dec = json.JSONDecoder()
    parti = []
    for segno in (INIZIO_OUTPUT, INIZIO_BASELINE_A5):
        i = testo.find(segno)
        graffa = testo.find("{", i) if i >= 0 else -1
        if graffa < 0:
            raise ValueError(f"non e' un allegato {PREFISSO_A5}: manca la parte \"{segno}\"")
        parti.append(dec.raw_decode(testo, graffa)[0])
    return parti[0], parti[1]


def scrivi_a5(cartella, payload, baseline, oggi):
    """Scrive Input_A5_<ciclo>.txt accanto a Baseline_corrente e toglie quelli di altri cicli. Restituisce il percorso."""
    cartella = Path(cartella)
    ciclo = payload.get("ciclo") or baseline.get("ciclo_da_valutare")
    percorso = cartella / f"{PREFISSO_A5}_{ciclo}.txt"
    percorso.write_text(componi_a5(payload, baseline, oggi), encoding="utf-8")
    for vecchio in cartella.glob(f"{PREFISSO_A5}_*.txt"):
        if vecchio != percorso:
            try:
                vecchio.unlink()
            except OSError:
                pass
    return percorso


def togli_a5(cartella, ciclo):
    """L'output di A1 non va bene (punti da correggere): l'allegato di A5 di quel ciclo non vale piu'."""
    try:
        (Path(cartella) / f"{PREFISSO_A5}_{ciclo}.txt").unlink(missing_ok=True)
    except OSError:
        pass


NOME_A6 = "Input_A6_{ciclo}.json"                       # D-84: prima Schede_input_<ciclo>.json


def scrivi(cartella, baseline, kernel, oggi):
    """Scrive l'allegato accanto a Baseline_corrente e toglie quelli dei cicli
    passati (file generati, rigenerabili: uno solo in cartella, quello giusto).
    Restituisce (percorso, file del kernel mancanti)."""
    cartella = Path(cartella)
    testo, mancanti = componi(baseline, kernel, oggi)
    percorso = cartella / nome_file(baseline)
    percorso.write_text(testo, encoding="utf-8")
    for vecchio in cartella.glob("Input_A[18]*.txt"):
        if vecchio != percorso and re.fullmatch(r"Input_A[18](_\d{4}Q[1-4](-S[1-9])?)?\.txt", vecchio.name):
            try:
                vecchio.unlink()
            except OSError:
                pass                    # aperto da qualcuno: resta, il ciclo nel nome dice che e' vecchio
    return percorso, mancanti
