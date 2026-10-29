"""L'aiuto dell'app NFR: i testi vengono dalla guida, 00_GUIDA_PASSO_PASSO.md, non da una copia (richiesta dell'utente
del 29/10/2026). Cambiata la guida, l'aiuto dell'app e' gia' aggiornato.

  - argomenti(): le parti della guida che l'aiuto mostra, tutte sull'uso dell'app: le sezioni del capitolo dell'app
    (la finestra, i tre gesti, una sezione per pulsante, se l'app si ferma), poi leggere i risultati e i file;
  - operazioni_admin(): le operazioni della finestra Admin con a che cosa servono e che cosa chiedono;
  - pulsanti(): per ogni pulsante dei processi le due colonne della tabella "I processi" (che cosa fa l'app, che
    cosa fai tu), per i suggerimenti che compaiono passando con il mouse;
  - parti_finestra(): la tabella "La finestra, dall'alto in basso" (Stato, Prossimo passo, Altro...);
  - righe(testo): il markdown in righe semplici con lo stile (titolo, sottotitolo, tabella, elenco, testo) e i pezzi
    in grassetto, per la finestra dell'aiuto; nessuna libreria in piu'.

Solo libreria standard.
"""

import re
from pathlib import Path

QUI = Path(__file__).resolve().parent
GUIDA = QUI.parent / "00_GUIDA_PASSO_PASSO.md"
CAPITOLO_APP = "## L'app NFR: uso passo per passo"
# Dopo le sezioni dell'app (una per pulsante: tutte le "### " del capitolo, nell'ordine della guida) l'aiuto mostra anche
# queste due, che non hanno comandi da scrivere. Le sezioni con i comandi restano nella guida completa (richiesta
# dell'utente del 29/10: l'aiuto parla dei pulsanti); test_app.py controlla che qui non ci siano comandi Python.
ALTRE = [("Leggere i risultati e il report", "## 4. Leggere i risultati"), ("Dove sono i file", "## 5. Dove sono i file")]


def testo_guida(percorso=None):
    p = Path(percorso or GUIDA)
    return p.read_text(encoding="utf-8") if p.exists() else ""


def sezione(testo, inizio):
    """La sezione che comincia con il titolo 'inizio' ('## ...' o '### ...'), fino al titolo seguente dello stesso
    livello o piu' alto. '' se non c'e'."""
    livello = len(inizio) - len(inizio.lstrip("#"))
    righe = testo.splitlines()
    for i, r in enumerate(righe):
        if r.startswith(inizio):
            fine = next((j for j in range(i + 1, len(righe))
                         if re.match(r"#{1,%d} " % livello, righe[j])), len(righe))
            return "\n".join(righe[i:fine]).strip()
    return ""


def argomenti(percorso=None):
    """[(titolo, testo)]: le sezioni del capitolo dell'app, una per pulsante, poi ALTRE."""
    t = testo_guida(percorso)
    capitolo = sezione(t, CAPITOLO_APP)
    out = []
    for titolo in re.findall(r"^### (.+)$", capitolo, flags=re.M):
        out.append((pulito(titolo), sezione(capitolo, "### " + titolo)))
    return out + [(titolo, sezione(t, inizio)) for titolo, inizio in ALTRE if sezione(t, inizio)]


def operazioni_admin(percorso=None):
    """{operazione: (a che cosa serve, che cosa chiede)} dalla tabella della sezione "Pulsante Admin"."""
    s = sezione(sezione(testo_guida(percorso), CAPITOLO_APP), "### Pulsante Admin")
    return {pulito(r[0]): (pulito(r[1]), pulito(r[2])) for r in tabella(s) if len(r) >= 3}


def celle(riga):
    return [c.strip() for c in riga.strip().strip("|").split("|")]


def tabella(testo):
    """Le righe di dati della prima tabella markdown del testo (senza intestazione e separatore)."""
    righe = [r for r in testo.splitlines() if r.strip().startswith("|")]
    return [celle(r) for r in righe[2:]] if len(righe) > 2 else []


def pulito(t):
    """Il testo di una cella senza i segni del markdown: grassetto, codice, collegamenti."""
    t = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", t)
    return t.replace("**", "").replace("`", "").replace("\\|", "|").replace("\\\\", "\\").strip()


def pulsanti(percorso=None):
    """{pulsante: (che cosa fa l'app, che cosa fai tu)} dalla tabella "I processi" della guida."""
    s = sezione(sezione(testo_guida(percorso), CAPITOLO_APP), "### I processi")
    return {pulito(r[0]): (pulito(r[1]), pulito(r[2])) for r in tabella(s) if len(r) >= 3}


def parti_finestra(percorso=None):
    """{parte della finestra: che cosa dice o fa} dalla tabella "La finestra, dall'alto in basso"."""
    s = sezione(sezione(testo_guida(percorso), CAPITOLO_APP), "### La finestra, dall'alto in basso")
    return {pulito(r[0]): pulito(r[1]) for r in tabella(s) if len(r) >= 2}


def suggerimento(nome, percorso=None, voci=None):
    """Il testo che compare passando sul pulsante: dalla guida; se la guida non c'e', un rimando."""
    voci = pulsanti(percorso) if voci is None else voci
    if nome not in voci:
        return f"{nome}: guida, sezione \"L'app NFR: uso passo per passo\" (pulsante Aiuto)."
    app, tu = voci[nome]
    return f"{nome}\nChe cosa fa l'app: {app}\nChe cosa fai tu: {tu}"


def _grassetto(t):
    """[(pezzo, in_grassetto)] dai ** del markdown; il codice `x` resta testo semplice."""
    t = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", t).replace("`", "").replace("\\\\", "\\")
    pezzi = t.split("**")
    return [(p, i % 2 == 1) for i, p in enumerate(pezzi) if p]


def blocchi(testo):
    """Il markdown in blocchi [(stile, testo grezzo)]: le righe di un paragrafo o di un punto elenco unite (la guida
    va a capo a mano, e un grassetto puo' continuare sulla riga dopo); una riga di tabella come (voce, (celle,
    intestazione))."""
    out, intestazione, in_codice = [], None, False
    for r in testo.splitlines():
        s = r.strip()
        if s.startswith("```"):
            in_codice = not in_codice
            continue
        if in_codice:
            out.append(("codice", r))
            continue
        if s.startswith("|"):
            c = celle(s)
            if all(re.fullmatch(r":?-+:?", x) for x in c if x):
                continue                              # separatore della tabella
            if intestazione is None:
                intestazione = c                      # la prima riga: i nomi delle colonne
            else:
                out.append(("voce", (c, intestazione)))
            continue
        intestazione = None
        if s.startswith("## "):
            out.append(("titolo", s[3:]))
        elif s.startswith("### "):
            out.append(("sottotitolo", s[4:]))
        elif re.match(r"(\d+\.|-|\*) ", s):
            rientro = "    " * ((len(r) - len(r.lstrip())) // 3)
            segno, resto = s.split(" ", 1)
            out.append(("elenco", f"{rientro}{'• ' if not segno[0].isdigit() else segno + ' '}{resto}"))
        elif not s:
            out.append(("vuota", ""))
        elif out and out[-1][0] in ("testo", "elenco"):
            out[-1] = (out[-1][0], out[-1][1] + " " + s)
        else:
            out.append(("testo", s))
    return out


def righe(testo):
    """Il markdown di una sezione in righe da mostrare: [(stile, [(pezzo, grassetto)])]. Stili: titolo, sottotitolo,
    voce (riga di tabella, la prima cella in grassetto), elenco, codice, testo, vuota."""
    out = []
    for stile, grezzo in blocchi(testo):
        if stile in ("titolo", "sottotitolo"):
            out.append((stile, [(pulito(grezzo), True)]))
        elif stile == "voce":
            c, intestazione = grezzo
            pezzi = [(pulito(c[0]), True)]
            for nome, valore in zip(intestazione[1:], c[1:]):
                if valore:
                    pezzi += [(f"\n    {pulito(nome)}: " if len(c) > 2 else "  —  ", False)] + _grassetto(valore)
            out.append(("voce", pezzi))
        elif stile == "codice":
            out.append((stile, [(grezzo, False)]))
        else:
            out.append((stile, _grassetto(grezzo)))
    return out
