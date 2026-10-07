"""Allegato di A1: baseline, controlli di A5 e guida di scrittura in un file solo.

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
INIZIO_BASELINE = "=== 1. BASELINE ==="


def testo_kernel(percorso):
    """Il file senza le note (righe ">") e senza il titolo ("# ")."""
    righe = [r.rstrip() for r in Path(percorso).read_text(encoding="utf-8").splitlines()
             if not r.startswith(">") and not r.startswith("# ")]
    return re.sub(r"\n{3,}", "\n\n", "\n".join(righe)).strip()


def testo_controlli(kernel):
    return testo_kernel(Path(kernel) / FILE_CONTROLLI)


def nome_file(baseline):
    ciclo = baseline.get("ciclo_da_valutare")
    return f"{PREFISSO}_{ciclo}.txt" if ciclo else f"{PREFISSO}.txt"


def componi(baseline, kernel, oggi):
    """(testo dell'allegato, file del kernel mancanti). Un file mancante non
    ferma niente, perche' la baseline basta ad A1 per lavorare, ma va detto:
    senza controlli e guida A1 risponde come prima del 02/10/2026."""
    kernel = Path(kernel)
    mancanti = [n for n in (FILE_CONTROLLI, FILE_GUIDA) if not (kernel / n).exists()]
    ciclo = baseline.get("ciclo_da_valutare") or "da valutare"
    parti = [f"INPUT DI A1 PER IL CICLO {ciclo}: scritto da esegui_ciclo_locale.py il {oggi}, da non modificare a mano.",
             "Tre parti: 1. BASELINE (JSON); 2. CONTROLLI che lo script (e A5 Challenger, se usato) applicano al tuo "
             "output; 3. GUIDA DI SCRITTURA.",
             "", INIZIO_BASELINE, json.dumps(baseline, ensure_ascii=False, indent=2)]
    s = baseline.get("straordinario")
    if s:                                            # D-75: in testa, perche' cambia che cosa A1 deve scrivere
        parti[2:2] = ["", f"CICLO STRAORDINARIO {ciclo}, deciso da {s['decisore']} il {s['data_decisione']}: {s['motivo']}",
                      f"Valuta SOLO questi rischi: {', '.join(s['rischi_da_rivalutare'])} (e un rischio nuovo solo se l'evento "
                      "lo crea); gli altri restano com'erano. Regole nella guida di scrittura, sezione \"Ciclo straordinario\"."]
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
    """La baseline dal testo di un allegato Input_A1 (il JSON della parte 1): la skill di Copilot Studio riceve solo
    l'allegato (D-70). ValueError se il testo non e' un allegato di A1."""
    inizio = testo.find(INIZIO_BASELINE)
    graffa = testo.find("{", inizio) if inizio >= 0 else -1
    if graffa < 0:
        raise ValueError(f"non e' un allegato {PREFISSO}: manca la parte \"{INIZIO_BASELINE}\" con il JSON della baseline")
    return json.JSONDecoder().raw_decode(testo, graffa)[0]


def scrivi(cartella, baseline, kernel, oggi):
    """Scrive l'allegato accanto a Baseline_corrente e toglie quelli dei cicli
    passati (file generati, rigenerabili: uno solo in cartella, quello giusto).
    Restituisce (percorso, file del kernel mancanti)."""
    cartella = Path(cartella)
    testo, mancanti = componi(baseline, kernel, oggi)
    percorso = cartella / nome_file(baseline)
    percorso.write_text(testo, encoding="utf-8")
    for vecchio in cartella.glob(f"{PREFISSO}*.txt"):
        if vecchio != percorso and re.fullmatch(rf"{PREFISSO}(_\d{{4}}Q[1-4](-S[1-9])?)?\.txt", vecchio.name):
            try:
                vecchio.unlink()
            except OSError:
                pass                    # aperto da qualcuno: resta, il ciclo nel nome dice che e' vecchio
    return percorso, mancanti
