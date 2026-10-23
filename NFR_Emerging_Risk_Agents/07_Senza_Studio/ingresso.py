"""Ingresso unico delle risposte degli agenti (D-83, tappa M2; TODO AU2).

L'analista preme "Copia" sotto la risposta di un agente (o sceglie un file): questo modulo estrae il JSON dal testo,
riconosce l'agente dallo schema, controlla lo schema e salva il file con il nome giusto in Archivio_Cicli/In_arrivo/.
Niente piu' Blocco note, codifica o nome da scrivere a mano: gli errori del 24/09 (".json.txt", JSON tagliato a
mano) non possono piu' capitare.

Regole:
  - il testo copiato puo' avere il BOM, i recinti ```json, frasi prima e dopo: si prendono gli oggetti JSON nel testo
    e si tiene il piu' grande che e' la risposta di un agente;
  - una risposta tagliata (le graffe non si chiudono) e' "troncata": l'app chiede all'agente "continua" e unisce le
    parti nell'ordine (unisci);
  - l'agente si riconosce dai campi obbligatori degli schemi del kernel (nessuna regola ricopiata qui); A8 scrive nel
    formato di A1 e si riconosce dal periodo straordinario (AAAAQn-Sk) o da analisi_evento; un testo senza JSON e' un
    parere di A4;
  - il file si salva anche con lo schema violato: il messaggio di correzione per l'agente lo prepara il precontrollo
    (A1, A8) o messaggio_correzione qui sotto (A3, A5, A6). Il testo copiato resta in In_arrivo/Originali/, e un file
    con lo stesso nome passa in In_arrivo/Precedenti/ con la data e l'ora: niente si perde.

Le risposte possono venire dagli agenti di Agent Builder o da quelli di Copilot Studio (stessi schemi): stessi nomi,
stessa cartella, stesso registro. L'origine si annota (ORIGINI) nel nome del testo originale e nello stato del
processo. Copilot Studio a volte restituisce il JSON dentro un campo di testo (l'uscita di un prompt e' un record con
il campo "text", prova K6): si legge anche da li'.

Solo libreria standard; nessun accesso a Excel.
"""

import datetime as dt
import json
import re
from pathlib import Path

from valida_output import carica_json, valida

SCHEMI = {"A1": "schema_output_A1.json", "A3": "schema_output_A3.json", "A5": "schema_output_A5.json",
          "A6": "schema_output_A6.json"}
CARTELLA = "In_arrivo"
PERIODO = re.compile(r"\d{4}Q[1-4](?:-S[1-9])?")
RECINTO = re.compile(r"```[a-zA-Z]*")

OK, TRONCATA, NESSUN_JSON = "ok", "troncata", "nessun JSON"
ORIGINI = ("Agent Builder", "Copilot Studio")


def carica_schemi(kernel):
    return {a: carica_json(Path(kernel) / f) for a, f in SCHEMI.items() if (Path(kernel) / f).exists()}


def pulisci(testo):
    """BOM e recinti di codice via; il resto com'e'."""
    return RECINTO.sub("", str(testo or "").lstrip("﻿"))


def oggetti_json(testo):
    """Gli oggetti JSON di primo livello nel testo, nell'ordine, con la loro lunghezza nel testo."""
    dec = json.JSONDecoder()
    out, i = [], testo.find("{")
    while i >= 0:
        try:
            obj, fine = dec.raw_decode(testo, i)
        except json.JSONDecodeError:
            i = testo.find("{", i + 1)
            continue
        if isinstance(obj, dict):
            out.append((obj, fine - i))
        i = testo.find("{", fine)
    return out


def _graffe_aperte(testo):
    """Quante graffe restano aperte (fuori dalle stringhe): > 0 = testo tagliato in mezzo a un oggetto."""
    aperte, in_stringa, escape = 0, False, False
    for c in testo:
        if in_stringa:
            if escape:
                escape = False
            elif c == "\\":
                escape = True
            elif c == '"':
                in_stringa = False
        elif c == '"':
            in_stringa = True
        elif c == "{":
            aperte += 1
        elif c == "}":
            aperte -= 1
    return aperte


def riconosci_agente(payload, schemi):
    """A1, A3, A5, A6, A8 o None, dai campi obbligatori degli schemi (il piu' specifico vince)."""
    if not isinstance(payload, dict):
        return None
    adatti = [a for a, s in schemi.items() if set(s.get("required", [])) <= set(payload)]
    if not adatti:
        return None
    agente = max(adatti, key=lambda a: len(schemi[a].get("required", [])))
    if agente == "A1" and ("analisi_evento" in payload or "-S" in str(payload.get("ciclo") or "")):
        return "A8"
    return agente


def estrai_json(testo, schemi):
    """(payload, stato): il JSON piu' grande del testo che e' la risposta di un agente (o, se nessuno lo e', il piu'
    grande); stato OK, TRONCATA (graffe non chiuse) o NESSUN_JSON."""
    t = pulisci(testo)
    oggetti = oggetti_json(t)
    # JSON dentro un campo di testo (record di un prompt di Copilot Studio): l'oggetto interno conta come gli altri.
    for o, _ in list(oggetti):
        for v in o.values():
            if isinstance(v, str) and "{" in v:
                oggetti += oggetti_json(pulisci(v))
    di_agente = [(o, n) for o, n in oggetti if riconosci_agente(o, schemi)]
    if di_agente:
        return max(di_agente, key=lambda x: x[1])[0], OK
    # Tagliata: l'oggetto esterno non si chiude (dentro possono esserci oggetti interi, come un rischio: non bastano).
    if "{" in t and _graffe_aperte(t[t.find("{"):]) > 0:
        return None, TRONCATA
    if oggetti:
        return max(oggetti, key=lambda x: x[1])[0], OK
    return None, NESSUN_JSON


def unisci(parti):
    """Le parti di una risposta tagliata, nell'ordine: si tolgono i recinti e si attaccano. L'agente che "continua"
    riparte dal punto esatto in cui si era fermato; uno spazio in piu' fra due parti non rompe il JSON."""
    return "".join(pulisci(p).strip("\n") for p in parti)


def nome_file(agente, payload):
    if agente == "A3":
        return f"A3_{payload.get('settimana') or 'senza_settimana'}.json"
    periodo = str(payload.get("ciclo") or "")
    return f"{agente}_{periodo if PERIODO.fullmatch(periodo) else 'senza_ciclo'}.json"


def _ora():
    return dt.datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]       # millisecondi: due copie nello stesso secondo


def _sigla(origine):
    return re.sub(r"[^A-Za-z0-9]+", "", str(origine or ""))[:20] or "origine"


def salva(cartella_uscita, agente, payload, testo_originale, origine=ORIGINI[0]):
    """Scrive In_arrivo/<nome> (UTF-8, senza BOM) e l'originale in In_arrivo/Originali/<nome>_<ora>_<origine>.txt; un
    file con lo stesso nome passa in In_arrivo/Precedenti/. Restituisce il percorso del JSON."""
    cartella = Path(cartella_uscita) / CARTELLA
    for sotto in ("Originali", "Precedenti"):
        (cartella / sotto).mkdir(parents=True, exist_ok=True)
    nome = nome_file(agente, payload)
    percorso = cartella / nome
    ora = _ora()
    if percorso.exists():
        percorso.replace(cartella / "Precedenti" / f"{percorso.stem}_{ora}.json")
    percorso.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    (cartella / "Originali" / f"{percorso.stem}_{ora}_{_sigla(origine)}.txt").write_text(str(testo_originale), encoding="utf-8")
    return percorso


def salva_parere(cartella_uscita, testo, origine=ORIGINI[0]):
    """Un parere di A4 (testo, non JSON) in Archivio_Cicli/Pareri/<data>_<titolo>_<origine>.txt; il titolo dalla prima
    riga."""
    prima = next((r.strip(" #*") for r in str(testo).splitlines() if r.strip(" #*")), "parere")
    titolo = re.sub(r"[^A-Za-z0-9]+", "_", prima)[:40].strip("_") or "parere"
    cartella = Path(cartella_uscita) / "Pareri"
    cartella.mkdir(parents=True, exist_ok=True)
    percorso = cartella / f"{_ora()}_{titolo}_{_sigla(origine)}.txt"
    percorso.write_text(str(testo), encoding="utf-8")
    return percorso


def proposta_straordinario(testo):
    """Il parere di A4 propone un ciclo straordinario? (la rubrica gli fa scrivere la frase in testa alla sezione 5)"""
    return "PROPOSTA DI CICLO STRAORDINARIO" in str(testo).upper()


def ricevi(testo, schemi, cartella_uscita, atteso=None, origine=ORIGINI[0]):
    """Una risposta copiata. Restituisce un dict:
      stato:   OK, TRONCATA (serve il resto: unire con unisci), NESSUN_JSON (un parere di A4, o un testo sbagliato);
      agente:  A1, A3, A5, A6, A8, "A4" per un parere, None se non riconosciuto;
      file:    il percorso salvato (JSON o parere);
      errori:  violazioni dello schema (vuoto = conforme);
      avviso:  l'agente non e' quello atteso dal passo (atteso), o il JSON non e' di nessun agente;
      origine: Agent Builder o Copilot Studio (annotata, non cambia nome ne' cartella)."""
    payload, stato = estrai_json(testo, schemi)
    if stato == TRONCATA:
        return {"stato": TRONCATA, "agente": None, "file": None, "errori": [], "avviso": None}
    if stato == NESSUN_JSON:
        if atteso in (None, "A4"):
            return {"stato": NESSUN_JSON, "agente": "A4", "file": salva_parere(cartella_uscita, testo, origine), "errori": [],
                    "avviso": None, "origine": origine}
        return {"stato": NESSUN_JSON, "agente": None, "file": None, "errori": [],
                "avviso": f"La risposta copiata non contiene un JSON: atteso l'output di {atteso}. Copiare la risposta "
                          "intera con il pulsante Copia sotto la risposta."}
    agente = riconosci_agente(payload, schemi)
    if agente is None:
        return {"stato": OK, "agente": None, "file": None, "errori": [],
                "avviso": "Il JSON copiato non e' l'output di un agente NFR (mancano i campi obbligatori di ogni schema)."}
    errori = valida(payload, schemi["A1" if agente == "A8" else agente])
    avviso = None
    if atteso and atteso != agente:
        avviso = f"Risposta di {agente}, ma il passo aspetta {atteso}: salvata comunque, il passo non avanza."
    return {"stato": OK, "agente": agente, "file": salva(cartella_uscita, agente, payload, testo, origine), "errori": errori,
            "avviso": avviso, "origine": origine}


def messaggio_correzione(agente, motivi):
    """Il testo da incollare nella chat di un agente dopo un fermo (A3, A5, A6; per A1 e A8 c'e' quello del
    precontrollo, piu' ricco). Lo stesso modello della guida, sezione 8."""
    righe = [f"- {m}" for m in motivi]
    return (f"Correggi solo questi punti e restituisci di nuovo l'intero JSON, nessun testo attorno ({agente}):\n"
            + "\n".join(righe) + "\n")
