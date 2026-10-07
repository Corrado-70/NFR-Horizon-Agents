"""Compone i prompt operativi degli agenti dai modelli e dal kernel.

Uso:
    python componi_prompt.py            rigenera A1/A3/A4/A5/A6 in 02_Agenti/
    python componi_prompt.py --verifica  non scrive; esce con 1 se un prompt e'
                                         fuori data rispetto al kernel o supera
                                         il limite di caratteri

Perche' esiste: le istruzioni di un agente (Agent Builder e Copilot Studio)
hanno un limite di 8.000 caratteri, e il kernel deve stare NELLE istruzioni,
non in una knowledge source che il planner puo' saltare. Quindi ogni prompt
riceve solo le sezioni del kernel che gli servono, prese dai file del kernel:
una modifica alla rubrica si propaga rilanciando questo script, senza copie
a mano da tenere allineate.

Segnaposto nei modelli (02_Agenti/modelli/*.md):
    {{TASSONOMIA}}      tutte le sezioni "##" di 01_Kernel/tassonomia_nfr.md
    {{RUBRICA:1,3}}     le sezioni numerate indicate di 01_Kernel/rubrica_scoring.md
    {{FONTI}}           elenco compatto (codice, nome, canale) di 01_Kernel/fonti.md,
                        senza le fonti escluse; lo legge 07_Senza_Studio/fonti.py
    {{CONTROLLI}}       i nove controlli di 01_Kernel/controlli_A5.md (D-69); lo
                        legge 07_Senza_Studio/input_a1.py, che mette lo stesso
                        testo nell'allegato di A1
Nei file del kernel le righe che iniziano con ">" sono note per chi legge e
non entrano nei prompt. I modelli non contengono commenti: tutto cio' che sta
in un prompt viene letto come istruzione.
"""

import re
import sys
from pathlib import Path

QUI = Path(__file__).resolve().parent
KERNEL = QUI.parent / "01_Kernel"
sys.path.insert(0, str(QUI.parent / "07_Senza_Studio"))
from fonti import elenco_compatto, leggi_fonti   # noqa: E402  un solo lettore dell'elenco fonti
from input_a1 import testo_controlli             # noqa: E402  un solo lettore dei controlli di A5
MODELLI = QUI / "modelli"
LIMITE_CARATTERI = 8000

AGENTI = {
    "A1.md": "A1_Horizon_Scanner.md",
    "A3.md": "A3_Interim_Update.md",
    "A4.md": "A4_News_Assessor.md",
    "A5.md": "A5_Challenger.md",
    "A6.md": "A6_Schede.md",
    "A7.md": "A7_Assistente_registro.md",
}


def sezioni(testo):
    """{titolo della sezione '##': corpo}, nell'ordine del file."""
    out = {}
    corrente = None
    for riga in testo.splitlines():
        if riga.startswith("## "):
            corrente = riga[3:].strip()
            out[corrente] = []
        elif corrente is not None:
            out[corrente].append(riga)
    return out


def rendi(titolo, righe):
    """Markdown del kernel -> testo compatto da prompt."""
    corpo = []
    for riga in righe:
        if riga.startswith(">"):
            continue
        if riga.startswith("|"):
            celle = [c.strip() for c in riga.strip().strip("|").split("|")]
            if all(set(c) <= set("-: ") for c in celle):
                continue                      # riga separatrice della tabella
            if celle[0] in ("Score", "Intensita", "Codice"):
                continue                      # intestazione della tabella
            if len(celle) == 2:
                corpo.append(f"- {celle[0]}: {celle[1]}")
            else:
                corpo.append(f"- {celle[0]} {celle[1]}: {' '.join(celle[2:])}")
            continue
        if riga.startswith("### "):
            corpo.append(riga[4:].strip() + ":")
            continue
        corpo.append(riga.rstrip())
    testo = re.sub(r"\n{3,}", "\n\n", "\n".join(corpo)).strip()
    titolo = re.sub(r"^\d+\.\s*", "", titolo)
    return f"## {titolo}\n{testo}"


def componi(modello):
    tass = sezioni((KERNEL / "tassonomia_nfr.md").read_text(encoding="utf-8"))
    rubr = sezioni((KERNEL / "rubrica_scoring.md").read_text(encoding="utf-8"))
    per_numero = {t.split(".", 1)[0]: (t, r) for t, r in rubr.items()}

    def rubrica(m):
        blocchi = []
        for n in m.group(1).split(","):
            titolo, righe = per_numero[n.strip()]
            blocchi.append(rendi(titolo, righe))
        return "\n\n".join(blocchi)

    testo = modello.replace("{{TASSONOMIA}}", "\n\n".join(rendi(t, r) for t, r in tass.items()))
    testo = re.sub(r"\{\{RUBRICA:([0-9,\s]+)\}\}", rubrica, testo)
    if "{{FONTI}}" in testo:
        testo = testo.replace("{{FONTI}}", elenco_compatto(leggi_fonti(KERNEL / "fonti.md")))
    if "{{CONTROLLI}}" in testo:
        testo = testo.replace("{{CONTROLLI}}", testo_controlli(KERNEL))
    if "{{" in testo:
        raise ValueError(f"segnaposto non risolto: {re.findall(r'{{[^}]*}}', testo)}")
    return testo.strip() + "\n"


def main(argv):
    verifica = "--verifica" in argv
    problemi = []
    for sorgente, destinazione in AGENTI.items():
        testo = componi((MODELLI / sorgente).read_text(encoding="utf-8"))
        n = len(testo)
        stato = f"{destinazione}: {n} caratteri (limite {LIMITE_CARATTERI})"
        if n > LIMITE_CARATTERI:
            problemi.append(f"{destinazione} supera il limite di {n - LIMITE_CARATTERI} caratteri")
        percorso = QUI / destinazione
        if verifica:
            attuale = percorso.read_text(encoding="utf-8") if percorso.exists() else None
            if attuale != testo:
                problemi.append(f"{destinazione} e' fuori data: rilanciare componi_prompt.py")
        else:
            percorso.write_text(testo, encoding="utf-8")
        print(stato)
    for p in problemi:
        print("PROBLEMA:", p)
    return 1 if problemi else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
