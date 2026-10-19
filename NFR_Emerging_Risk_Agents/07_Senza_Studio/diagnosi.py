"""Diagnosi delle valutazioni: le asimmetrie che il registro non mostra da solo (analisi 17, sezione 17.10).

Tre misure, su dati che il registro ha gia', senza scrivere niente:
1. valori all'ingresso: le dimensioni dei rischi nuovi (Esito "Nuovo" in qualunque ciclo), per vedere se entrano tutti
   bassi (per esempio Probabilita mai sopra 3);
2. verso delle rettifiche del validatore (Storico_Validazioni): quante volte una dimensione proposta dall'agente e' stata
   alzata o abbassata, distinguendo i rischi nuovi e la riapertura. Molte rettifiche nello stesso verso = la proposta e'
   sistematicamente bassa (o alta);
3. rischi lontani: Prossimita 1 (oltre 3 anni) con Impatto alto. Senza anni di adeguamento il margine di Mosca usa la Y
   di riserva e il rischio non puo' risultare AGIRE ORA: e' il caso per cui Mosca ha scritto la disuguaglianza;
4. esposizione non nota (D-81): i rischi del ciclo in cui A1 ha scritto che l'esposizione della Banca non e' nota alle
   fonti, con la Probabilita che darebbe e quella validata. Molte note, o sempre sugli stessi rischi, dicono che serve
   registrare l'esposizione (variante 3b dell'analisi 17) o che A1 la usa per alzare i valori.

Lo usa il comando `diagnosi` di esegui_ciclo_locale.py; il collaudo lo prova su righe finte. Solo libreria standard.
"""
from collections import Counter

import radar
from controlli_a5 import esposizione_non_nota

DIMENSIONI = (("impatto", "Impatto"), ("probabilita", "Probabilita"), ("prossimita", "Prossimita"),
              ("velocity", "Velocity"))
NV = "n.v."
IMPATTO_ALTO = 4            # da questo Impatto un rischio lontano senza anni di adeguamento si segnala


def _intero(v):
    if v is None or v == "" or isinstance(v, bool):
        return None
    try:
        return int(round(float(v)))
    except (TypeError, ValueError):
        return None


def _numero(v):
    if v is None or v == "" or isinstance(v, bool):
        return None
    try:
        return float(str(v).replace(",", "."))
    except ValueError:
        return None


def distribuzione(righe):
    """{dimensione: Counter(1..5, 'n.v.')} sulle righe del RiskRegister."""
    out = {d: Counter() for d, _ in DIMENSIONI}
    for r in righe:
        for d, col in DIMENSIONI:
            v = _intero(r.get(col))
            out[d][v if v is not None else NV] += 1
    return out


def rettifiche(storico, registro):
    """Verso delle rettifiche sulle dimensioni dei rischi: {dimensione: {gruppo: Counter(su, giu)}}, gruppi 'nuovi',
    'altri', 'riapertura'. Una rettifica da o verso n.v. (Velocity) non ha verso e non conta."""
    esito = {(str(r.get("Ciclo")), r.get("ID_Rischio")): r.get("Esito") for r in registro}
    out = {d: {g: Counter() for g in ("nuovi", "altri", "riapertura")} for d, _ in DIMENSIONI}
    accettati = Counter()
    colonne = {col: d for d, col in DIMENSIONI}
    for r in storico:
        if r.get("Oggetto") != "Rischio" or r.get("Campo") not in colonne:
            continue
        d, dec = colonne[r["Campo"]], str(r.get("Decisione") or "")
        if dec.startswith(("Accettato", "Invariato")):
            accettati[d] += 1
            continue
        if not dec.startswith("Rettificato"):
            continue
        da, a = _numero(r.get("Proposta_Agente")), _numero(r.get("Valore_Validato"))
        if da is None or a is None or da == a:
            continue
        gruppo = ("riapertura" if "riapertura" in dec else
                  "nuovi" if esito.get((str(r.get("Periodo")), r.get("ID"))) == "Nuovo" else "altri")
        out[d][gruppo]["su" if a > da else "giu"] += 1
    return out, accettati


def lontani(righe_ciclo, regola=radar.REGOLA_DEFAULT):
    """Rischi del ciclo con Prossimita 1, dal piu' alto Impatto: id, nome, valori, orizzonte, anni di adeguamento, stato,
    margine di Mosca (con la Y di riserva se mancano azioni e anni)."""
    out = []
    for r in righe_ciclo:
        if _intero(r.get("Prossimita")) != 1:
            continue
        ingresso = {d: _intero(r.get(col)) for d, col in DIMENSIONI}
        ingresso.update(anni_adeguamento=_numero(r.get("Anni_Adeguamento")), y_azioni=None)
        out.append({"id": r.get("ID_Rischio"), "nome": r.get("Nome"), "impatto": ingresso["impatto"],
                    "probabilita": ingresso["probabilita"], "orizzonte": _numero(r.get("Orizzonte_Anni")),
                    "anni_adeguamento": ingresso["anni_adeguamento"], "stato": r.get("Stato"),
                    "margine": radar.margine(ingresso, regola)})
    return sorted(out, key=lambda x: (-(x["impatto"] or 0), str(x["id"])))


def esposizioni(righe_ciclo):
    """Rischi del ciclo con la nota di esposizione non nota nel razionale: id, Probabilita validata, N della nota."""
    out = []
    for r in righe_ciclo:
        dichiarata, n = esposizione_non_nota(r.get("Razionale"))
        if dichiarata:
            out.append({"id": r.get("ID_Rischio"), "probabilita": _intero(r.get("Probabilita")), "se_esposta": n,
                        "nuovo": r.get("Esito") == "Nuovo"})
    return out


def diagnosi(registro, storico, ciclo, regola=radar.REGOLA_DEFAULT):
    """Le tre misure e una lettura in frasi. registro e storico = righe di tblRegister e tblValidazione."""
    attive = [r for r in registro if r.get("Stato") != "Dismesso"]
    nuovi = [r for r in attive if r.get("Esito") == "Nuovo"]
    correnti = [r for r in attive if str(r.get("Ciclo")) == str(ciclo)]
    vers, accettati = rettifiche(storico, registro)
    lont = lontani(correnti, regola)
    esp = esposizioni(correnti)
    letture = []
    if nuovi:
        prob = distribuzione(nuovi)["probabilita"]
        alti = sum(n for v, n in prob.items() if v != NV and v >= 4)
        letture.append(f"Probabilita all'ingresso dei {len(nuovi)} rischi nuovi: "
                       + (f"{alti} con 4 o 5." if alti else "nessuno con 4 o 5 (analisi 17, 17.10)."))
    for d, col in DIMENSIONI:
        tot = {g: vers[d][g] for g in vers[d]}
        su = sum(c["su"] for c in tot.values())
        giu = sum(c["giu"] for c in tot.values())
        if su or giu:
            letture.append(f"{col}: {_volte(su)} in su e {_volte(giu)} in giu' (rischi nuovi {tot['nuovi']['su']} su, "
                           f"{tot['nuovi']['giu']} giu'; in riapertura {tot['riapertura']['su']} su, "
                           f"{tot['riapertura']['giu']} giu'); proposte accettate {accettati[d]}.")
    if not any(sum(c.values()) for g in vers.values() for c in g.values()):
        letture.append("Nessuna rettifica delle dimensioni nello storico: il verso delle proposte non si puo' ancora misurare.")
    for x in lont:
        if (x["impatto"] or 0) >= IMPATTO_ALTO and x["anni_adeguamento"] is None:
            letture.append(f"{x['id']} (Impatto {x['impatto']}, Prossimita 1, orizzonte "
                           f"{_it(x['orizzonte']) + ' anni' if x['orizzonte'] is not None else 'non indicato'}) non ha anni di "
                           f"adeguamento: il margine di Mosca ({_it(x['margine'])} anni) usa la Y di riserva; se la difesa "
                           "richiede un adeguamento pluriennale, A1 deve stimarlo (guida di scrittura, rischi in osservazione).")
    if esp:
        alzati = [x for x in esp if x["se_esposta"] is not None and (x["probabilita"] or 0) >= x["se_esposta"]]
        letture.append(f"Esposizione non nota in {len(esp)} rischi su {len(correnti)} del ciclo "
                       f"({', '.join(str(x['id']) for x in esp)}); il validatore ha dato il valore \"se esposta\" in "
                       f"{len(alzati)}. Se la nota torna sugli stessi rischi ciclo dopo ciclo, conviene registrare "
                       "l'esposizione (analisi 17, 17.10, variante 3b).")
    return {"ciclo": ciclo, "rischi_nuovi": len(nuovi), "ingresso": distribuzione(nuovi), "esposizioni": esp,
            "ciclo_corrente": {s: distribuzione([r for r in correnti if r.get("Stato") == s])
                               for s in sorted({r.get("Stato") for r in correnti if r.get("Stato")})},
            "rettifiche": vers, "accettati": accettati, "lontani": lont, "letture": letture}


def _volte(n):
    return f"{n} rettifica" if n == 1 else f"{n} rettifiche"


def _it(v):
    return "—" if v is None else (f"{v:.2f}".rstrip("0").rstrip(".") if isinstance(v, float) else str(v)).replace(".", ",")


def _tabella(dist):
    righe = [f"    {'':12}" + "".join(f"{v:>6}" for v in (1, 2, 3, 4, 5, NV))]
    for d, col in DIMENSIONI:
        righe.append(f"    {col:12}" + "".join(f"{dist[d].get(v, 0):>6}" for v in (1, 2, 3, 4, 5, NV)))
    return righe


def testo(d):
    """Il rapporto leggibile del comando diagnosi."""
    out = [f"DIAGNOSI DELLE VALUTAZIONI — ciclo {d['ciclo']} (analisi 17, 17.10). Solo lettura: nessun dato cambiato.", "",
           "Lettura:"] + [f"  - {x}" for x in d["letture"]] + ["",
           f"1. Valori all'ingresso dei rischi nuovi ({d['rischi_nuovi']} rischi, tutti i cicli): quanti per valore"]
    out += _tabella(d["ingresso"])
    for stato, dist in d["ciclo_corrente"].items():
        out += ["", f"   Ciclo {d['ciclo']}, rischi «{stato}»:"] + _tabella(dist)
    out += ["", "2. Rettifiche del validatore sulle dimensioni (proposta dell'agente -> valore validato)"]
    for dim, col in DIMENSIONI:
        g = d["rettifiche"][dim]
        out.append(f"    {col:12} nuovi {g['nuovi']['su']} su / {g['nuovi']['giu']} giu' · altri {g['altri']['su']} su / "
                   f"{g['altri']['giu']} giu' · riapertura {g['riapertura']['su']} su / {g['riapertura']['giu']} giu' · "
                   f"accettate {d['accettati'][dim]}")
    out += ["", "3. Rischi lontani (Prossimita 1, oltre 3 anni), dal piu' alto Impatto"]
    if not d["lontani"]:
        out.append("    nessuno")
    for x in d["lontani"]:
        out.append(f"    {x['id']} {x['nome'] or ''} — Imp {x['impatto']}, Prob {x['probabilita']}, orizzonte "
                   f"{_it(x['orizzonte'])}, anni di adeguamento {_it(x['anni_adeguamento'])}, margine di Mosca "
                   f"{_it(x['margine'])}, {x['stato'] or '—'}")
    out += ["", "4. Esposizione non nota (nota di A1 nel razionale, D-81): Probabilita validata e valore \"se esposta\""]
    if not d.get("esposizioni"):
        out.append("    nessuna")
    for x in d.get("esposizioni", []):
        out.append(f"    {x['id']} — validata {_it(x['probabilita'])}, se esposta {_it(x['se_esposta'])}"
                   + (" (rischio nuovo)" if x["nuovo"] else ""))
    return "\n".join(out) + "\n"
