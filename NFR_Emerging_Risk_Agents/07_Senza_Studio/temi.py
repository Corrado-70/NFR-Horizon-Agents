"""Temi da verificare indicati dall'analista (P9, D-98, 04/11/2026).

L'analista chiede ad A1 di verificare un tema preciso (un fenomeno visto in una notizia, una domanda del comitato): la
richiesta resta scritta in temi_da_verificare.md, si vede e si modifica dall'app (finestra "Temi da verificare", che
l'app propone prima di ogni ciclo trimestrale) e arriva ad A1 nella baseline ("temi_da_verificare", solo i temi
aperti; l'allegato resta in tre parti). A1 risponde citando il codice del tema in un rischio o fra i fenomeni non
censiti (guida di scrittura); un tema senza risposta e' un'Osservazione in validazione (controlli_a5.controlla_temi).

Il file sta nella library Kernel, accanto alla guida di scrittura, ma non e' nel pacchetto: lo scrive l'app, e
installa.cmd non lo tocca. Sul PC di sviluppo, dove il kernel e' 01_Kernel del pacchetto, sta nella cartella di uscita
(come la knowledge di A7). Solo libreria standard.
"""

import datetime as dt
import hashlib
import re
from pathlib import Path

QUI = Path(__file__).resolve().parent
NOME_FILE = "temi_da_verificare.md"
CAMPI = ["codice", "tema", "chiesto_da", "perche", "data", "stato"]
INTESTAZIONI = ["Codice", "Tema", "Chiesto da", "Perche'", "Data", "Stato"]
APERTO, CHIUSO = "aperto", "chiuso"
CODICE = re.compile(r"^TEMA-(\d{2,3})$")
TESTA = """# Temi da verificare

> Scritto dall'app NFR (finestra "Temi da verificare"): si puo' anche modificare a mano, una riga per tema, senza il
> carattere | nei testi. Un tema aperto arriva ad A1 nella baseline del ciclo trimestrale; A1 risponde citando il codice
> in un rischio o fra i fenomeni non censiti. Un tema chiuso resta qui come traccia (P9, D-98).
"""


def file_temi(conf):
    """Il file dei temi: nella library Kernel; nella cartella di uscita se il kernel e' 01_Kernel del pacchetto."""
    kernel = Path(conf["kernel"])
    if kernel.resolve() == (QUI.parent / "01_Kernel").resolve():
        return Path(conf["cartella_uscita"]) / NOME_FILE
    return kernel / NOME_FILE


def _cella(testo):
    return re.sub(r"\s+", " ", str(testo or "").replace("|", "/")).strip()


def leggi(percorso):
    """I temi del file, nell'ordine scritto; [] se il file non c'e'. Le righe che non sono di un tema si saltano."""
    percorso = Path(percorso)
    if not percorso.exists():
        return []
    temi = []
    for riga in percorso.read_text(encoding="utf-8-sig").splitlines():
        celle = [c.strip() for c in riga.strip().strip("|").split("|")]
        if riga.strip().startswith("|") and len(celle) >= len(CAMPI) and CODICE.match(celle[0]):
            t = dict(zip(CAMPI, celle))
            t["stato"] = CHIUSO if t["stato"].lower().startswith("chius") else APERTO
            temi.append(t)
    return temi


def impronta(percorso):
    """Impronta del contenuto ('' se il file non c'e'): chi salva controlla che nessun collega l'abbia cambiato nel
    frattempo (la library e' condivisa)."""
    percorso = Path(percorso)
    return hashlib.sha256(percorso.read_bytes()).hexdigest()[:12] if percorso.exists() else ""


def normalizza(temi, oggi=None):
    """Temi pronti da scrivere: codice ai nuovi (TEMA-nn, il primo libero dopo il piu' alto), data di oggi se manca,
    stato aperto se non e' chiuso; un tema senza testo si toglie. Solleva ValueError su un codice ripetuto."""
    oggi = oggi or dt.date.today().isoformat()
    numeri = [int(CODICE.match(t["codice"]).group(1)) for t in temi if CODICE.match(str(t.get("codice") or ""))]
    prossimo = max(numeri, default=0) + 1
    out = []
    for t in temi:
        if not _cella(t.get("tema")):
            continue
        x = {c: _cella(t.get(c)) for c in CAMPI}
        if not CODICE.match(x["codice"]):
            x["codice"] = f"TEMA-{prossimo:02d}"
            prossimo += 1
        x["data"] = x["data"] or oggi
        x["stato"] = CHIUSO if x["stato"].lower().startswith("chius") else APERTO
        out.append(x)
    codici = [x["codice"] for x in out]
    doppi = sorted({c for c in codici if codici.count(c) > 1})
    if doppi:
        raise ValueError(f"Codici ripetuti: {', '.join(doppi)}.")
    return out


def scrivi(percorso, temi, impronta_letta=None):
    """Scrive il file (temi gia' normalizzati). Con impronta_letta si ferma (RuntimeError) se il file e' cambiato da
    quando e' stato letto: un collega lo ha modificato nel frattempo."""
    percorso = Path(percorso)
    if impronta_letta is not None and impronta(percorso) != impronta_letta:
        raise RuntimeError(f"{percorso.name} e' stato modificato da un'altra persona dopo che l'hai aperto: riaprilo e "
                           "rifai le modifiche.")
    righe = [TESTA, "| " + " | ".join(INTESTAZIONI) + " |", "|" + "---|" * len(CAMPI)]
    righe += ["| " + " | ".join(_cella(t.get(c)) for c in CAMPI) + " |" for t in temi]
    percorso.parent.mkdir(parents=True, exist_ok=True)
    percorso.write_text("\n".join(righe) + "\n", encoding="utf-8")
    return percorso


def aperti(temi):
    return [t for t in temi if t.get("stato") != CHIUSO]


def per_baseline(temi):
    """Cio' che A1 riceve nella baseline: i soli temi aperti, senza data e stato."""
    return [{"codice": t["codice"], "tema": t["tema"], "chiesto_da": t.get("chiesto_da") or None,
             "perche": t.get("perche") or None} for t in aperti(temi)]
