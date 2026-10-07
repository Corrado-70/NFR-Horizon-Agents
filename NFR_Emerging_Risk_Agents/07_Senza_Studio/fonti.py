"""Lettura dell'elenco delle fonti (01_Kernel/fonti.md).

Un solo lettore per tutti: raccogli_notizie.py (feed da scaricare),
esegui_ciclo_locale.py (codici ammessi nelle notizie di A3),
02_Agenti/componi_prompt.py (elenco compatto nel prompt di A3), collaudo.
Solo libreria standard.
"""

import re
from pathlib import Path

CANALI = ("rss", "sito", "share")
STATI = ("da validare", "approvata", "esclusa")
CODICE_MANUALE = "MAN"          # notizia portata da un analista da una fonte fuori elenco
TITOLO = re.compile(r"^### (FNT-\d{2}) (.+)$")
CHIAVE = re.compile(r"^- ([a-z_]+): (.*)$")


def leggi_fonti(percorso):
    """[{codice, nome, canale, indirizzo, temi, stato, ...}] nell'ordine del file.
    Solleva ValueError con tutti i problemi di formato trovati."""
    fonti, problemi, corrente = [], [], None
    for n, riga in enumerate(Path(percorso).read_text(encoding="utf-8").splitlines(), start=1):
        if riga.startswith(">"):
            continue
        m = TITOLO.match(riga)
        if m:
            corrente = {"codice": m.group(1), "nome": m.group(2).strip()}
            fonti.append(corrente)
            continue
        if riga.startswith("#"):
            corrente = None
            continue
        m = CHIAVE.match(riga)
        if m and corrente is not None:
            corrente[m.group(1)] = m.group(2).strip()
    for f in fonti:
        for chiave in ("canale", "indirizzo", "temi", "stato", "licenza"):
            if not f.get(chiave):
                problemi.append(f"{f['codice']}: manca '{chiave}'")
        if f.get("canale") and f["canale"] not in CANALI:
            problemi.append(f"{f['codice']}: canale '{f['canale']}' non in {CANALI}")
        if f.get("stato") and f["stato"] not in STATI:
            problemi.append(f"{f['codice']}: stato '{f['stato']}' non in {STATI}")
        f["temi"] = [t.strip() for t in f.get("temi", "").split(",") if t.strip()]
        f["escludi"] = [t.strip().lower() for t in f.get("escludi", "").split(";") if t.strip()]
        f["max_voci"] = int(f.get("max_voci", 20))
        f["sito_agente"] = f.get("sito_agente", "no").lower() in ("si", "sì")
    codici = [f["codice"] for f in fonti]
    doppi = sorted({c for c in codici if codici.count(c) > 1})
    if doppi:
        problemi.append(f"codici duplicati: {doppi}")
    if problemi:
        raise ValueError("elenco fonti non valido:\n  - " + "\n  - ".join(problemi))
    return fonti


def codici_ammessi(fonti):
    """Codici che una notizia puo' citare: tutte le fonti non escluse, piu' MAN."""
    return {f["codice"] for f in fonti if f["stato"] != "esclusa"} | {CODICE_MANUALE}


def elenco_compatto(fonti):
    """Righe per il prompt: codice, nome, canale. Le escluse non compaiono."""
    return "\n".join(f"- {f['codice']} {f['nome']} [{f['canale']}]" for f in fonti if f["stato"] != "esclusa")
