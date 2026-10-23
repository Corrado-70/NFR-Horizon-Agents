"""Precontrollo dell'output di A1 prima di A5 (D-69): cio' che lo script verifica senza Excel.

Schema, controlli meccanizzati (gli stessi di trimestrale, controlli_a5.py) e parti del razionale che servono alle
schede (D-68), con il messaggio di correzione da dare ad A1. Solo libreria standard e moduli del pacchetto che non
usano Excel: lo usano il comando precontrollo di esegui_ciclo_locale.py e, dal 05/10/2026 (D-70), lo script della
skill per Copilot Studio, che 09_Copilot_Studio/prepara_kit.py compone copiando senza modifiche questo modulo e quelli
che importa. Un solo codice: quello che il precontrollo trova in Copilot Studio, il comando lo trova sul PC.
"""

import hashlib
import json
import re

import controlli_a5
import schede
from valida_output import valida


def precontrolla(payload, baseline, schema):
    """Cio' che lo script verifica dell'output di A1 prima di A5: schema, controlli
    meccanizzati (gli stessi di trimestrale) e parti del razionale che servono alle
    schede (D-68). Con lo schema violato i controlli non girano: lavorano su campi
    che lo schema garantisce."""
    errori = valida(payload, schema)
    if errori:
        return {"schema": errori, "rilievi": [], "formato": []}
    formato = []                                     # una riga per rischio: il messaggio resta corto anche con A1 vecchio
    for x in payload["rischi"]:
        parti = schede.parti_razionale(x["razionale"])
        attese = [e for e, k in schede.ETICHETTE_RAZIONALE.items()
                  if k != "adeguamento" or x.get("anni_adeguamento") is not None]
        mancano = [e for e in attese if not parti.get(schede.ETICHETTE_RAZIONALE[e])]
        azioni = [str(n) for n, a in enumerate(x["azioni_mitigazione"], start=1) if schede.parti_effetto(a["razionale"])[1] is None]
        kri = [k["tipo"] for k in x["kri_proposti"] if schede.parti_effetto(k["razionale"])[1] is None]
        senza = ([("azione " if len(azioni) == 1 else "azioni ") + ", ".join(azioni)] if azioni else []) + \
                (["KRI di " + " e di ".join(kri)] if kri else [])
        problemi = ((["razionale senza le parti " + ", ".join(e + ":" for e in mancano)] if mancano else [])
                    + (["EFFETTO: mancante nel razionale di " + "; ".join(senza)] if senza else []))
        if problemi:
            formato.append({"id_rischio": x["id_rischio"], "descrizione": "; ".join(problemi) + " (parte 3 dell'allegato)."})
    return {"schema": errori, "rilievi": controlli_a5.controlla(payload, baseline)["rilievi"], "formato": formato}


def conta(esito):
    """(punti da correggere, punti da verificare): i primi fermerebbero il ciclo."""
    da_correggere = len(esito["schema"]) + sum(1 for x in esito["rilievi"] if x["gravita"] == "Bloccante")
    da_verificare = sum(1 for x in esito["rilievi"] if x["gravita"] != "Bloccante") + len(esito["formato"])
    return da_correggere, da_verificare


def ciclo_di(payload, baseline):
    """Il ciclo dell'output di A1; se manca o non e' un ciclo, quello da valutare della baseline."""
    ciclo = str(payload.get("ciclo") or "") if isinstance(payload, dict) else ""
    return ciclo if re.fullmatch(r"\d{4}Q[1-4](-S[1-9])?", ciclo) else (baseline.get("ciclo_da_valutare") or "senza_ciclo")


def agente(ciclo):
    """Chi ha scritto l'output: A1 per un trimestre, A8 Evento critico per uno straordinario AAAAQn-Sk (D-77)."""
    return "A8" if "-S" in str(ciclo) else "A1"


def riga_esito(ciclo, esito):
    """Prima riga dell'esito, uguale nel comando sul PC e nella skill di Copilot Studio."""
    da_correggere, da_verificare = conta(esito)
    if not da_correggere and not da_verificare:
        return f"Precontrollo dell'output di {agente(ciclo)} ({ciclo}): nessun rilievo."
    return (f"Precontrollo dell'output di {agente(ciclo)} ({ciclo}): {da_correggere} punti da correggere, {da_verificare} "
            "da verificare.")


def impronta(payload):
    """12 caratteri che identificano il contenuto dell'output di A1, a meno di spazi, a capo e ordine dei campi:
    la stessa impronta sul PC e in Copilot Studio vuol dire che i due precontrolli hanno visto lo stesso output."""
    testo = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(testo.encode("utf-8")).hexdigest()[:12]


def messaggio_correzione(ciclo, esito):
    """Testo da incollare nella chat di A1: i punti del precontrollo come richiesta
    di correzione, con le parole dei controlli (le stesse dell'allegato di A1)."""
    righe = [f"Il precontrollo dello script ha trovato questi punti nel tuo output del ciclo {ciclo}. Correggili e "
             "restituisci di nuovo l'intero JSON, solo JSON, senza cambiare cio' che non e' citato. I controlli sono "
             f"quelli della parte 2 dell'allegato Input_{agente(ciclo)}, la forma dei testi e' nella parte 3."]   # D-84

    def blocco(titolo, voci):
        if voci:
            righe.extend(["", titolo] + [f"{n}. {v}" for n, v in enumerate(voci, start=1)])
    voce = lambda x: f"{x['id_rischio'] or 'ciclo'} · {x['controllo']}: {x['descrizione']}"
    blocco("Schema (lo script non puo' leggere il JSON finche' non e' corretto):", esito["schema"])
    blocco("Da correggere (fermerebbero il ciclo):", [voce(x) for x in esito["rilievi"] if x["gravita"] == "Bloccante"])
    blocco("Da verificare (correggi se fondati; se confermi, spiega il perche' nel razionale):",
           [voce(x) for x in esito["rilievi"] if x["gravita"] != "Bloccante"])
    blocco("Forma dei testi (serve alle schede dei rischi):", [f"{x['id_rischio']} · {x['descrizione']}" for x in esito["formato"]])
    return "\n".join(righe) + "\n"
