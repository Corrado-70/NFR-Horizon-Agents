"""Regola del registro unico (D-79, 08/10/2026): chi sta nel radar di Mosca e chi in osservazione.

Un solo registro di rischi NFR-nn, tutti valutati con la rubrica. I primi, secondo questa regola, sono **nel radar**
(gestione completa: KRI, azioni, urgenza, report, schede; sono l'anagrafica di Parametri); gli altri sono **in
osservazione** (stessa scala e stesso score, niente KRI ne' azioni). Rubrica, sezione 9.

La regola, in quattro passi:
1. candidato al radar: Prossimita >= soglia e Probabilita >= soglia;
2. sempre nel radar (eccezioni): AGIRE ORA (margine di Mosca < 0), tema del supervisore, decisione "Radar" del
   validatore; mai nel radar: decisione "Osservazione" del validatore;
3. se i candidati superano la capienza: prima le eccezioni, poi i piu' alti per score composito; gli altri restano
   fuori "per capienza";
4. un rischio del radar che non soddisfa piu' la regola diventa "Radar, in uscita" e passa in osservazione solo se lo
   e' anche al ciclo dopo (cicli_uscita = 2; con 1 esce subito). Un rischio che sale entra subito.
Oltre il massimo delle viste (max_radar, 20) nessun "in uscita": esce chi ha lo score piu' basso.

Un solo punto del codice per la regola: la usano esegui_ciclo_locale.py (trimestrale sui valori proposti, valida e la
riapertura sui valori validati, straordinario, aggiorna-registro), controlli_a5.py e il precontrollo (anche nella skill
di Copilot Studio). Solo libreria standard.
"""

RADAR, IN_USCITA, OSSERVAZIONE = "Radar", "Radar, in uscita", "Osservazione"
STATI = (RADAR, IN_USCITA, OSSERVAZIONE)
AUTOMATICO = "Automatico"
DECISIONI = (AUTOMATICO, RADAR, OSSERVAZIONE)
ENTRATO, USCITO = "Entrato", "Uscito"

# Valori del template (Parametri); la baseline porta quelli del registro (chiave regola_radar).
REGOLA_DEFAULT = {
    "capienza": 15, "soglia_prossimita": 2, "soglia_probabilita": 2, "cicli_uscita": 2,
    "max_radar": 20, "max_osservazione": 20,
    "pesi": {"impatto": 0.35, "probabilita": 0.25, "prossimita": 0.20, "velocity": 0.20},
    "anni_prossimita": [3.5, 2.5, 1.5, 0.5, 0.0],          # Z per Prossimita 1..5 (rubrica, sezione 8)
    "mosca_x": 0.25, "mosca_y_riserva": 1.0,
}
DIMENSIONI = ("impatto", "probabilita", "prossimita", "velocity")


def nel_radar(stato):
    return stato in (RADAR, IN_USCITA)


def _num(v):
    return v if isinstance(v, (int, float)) and not isinstance(v, bool) else None


def score(r, regola=REGOLA_DEFAULT):
    """Media pesata delle dimensioni valutate (D-50): una Velocity non valutata non conta."""
    pesi = regola["pesi"]
    usate = {d: _num(r.get(d)) for d in DIMENSIONI if _num(r.get(d)) is not None}
    if not usate:
        return None
    return sum(pesi[d] * v for d, v in usate.items()) / sum(pesi[d] for d in usate)


def margine(r, regola=REGOLA_DEFAULT):
    """Margine di Mosca Z - (X + Y), come il foglio Radar_Mosca: Z dalla Prossimita; Y = orizzonte piu' lungo delle
    azioni non respinte del periodo di valutazione (y_azioni, in anni) o la riserva senza azioni, e gli anni di
    adeguamento se maggiori."""
    p = _num(r.get("prossimita"))
    if p is None:
        return None
    z = regola["anni_prossimita"][int(p) - 1]
    y_azioni = _num(r.get("y_azioni"))
    y = max(y_azioni if y_azioni is not None else regola["mosca_y_riserva"], _num(r.get("anni_adeguamento")) or 0)
    return z - (regola["mosca_x"] + y)


def _it(v):
    return "—" if v is None else f"{v:.2f}".replace(".", ",")


def stati(rischi, regola=REGOLA_DEFAULT):
    """Stato di ogni rischio del ciclo. rischi: dict con id, impatto, probabilita, prossimita, velocity, supervisore
    (bool), anni_adeguamento, y_azioni (anni o None), stato_prima (None per un rischio nuovo), decisione (Automatico,
    Radar, Osservazione). Restituisce {id: {stato, motivo, movimento, score, margine}}."""
    sp, sb = regola["soglia_prossimita"], regola["soglia_probabilita"]
    dati = {}
    for r in rischi:
        d = dict(r)
        d["score"], d["margine"] = score(r, regola), margine(r, regola)
        d["decisione"] = r.get("decisione") or AUTOMATICO
        dati[r["id"]] = d

    def candidato(d):
        return (_num(d.get("prossimita")) or 0) >= sp and (_num(d.get("probabilita")) or 0) >= sb

    def eccezione(d):
        if d["decisione"] == RADAR:
            return "decisione del validatore"
        if d["margine"] is not None and d["margine"] < 0:
            return "AGIRE ORA (radar di Mosca)"
        if d.get("supervisore"):
            return "tema del supervisore"
        return None

    def ordine(d):
        return (-(d["score"] or 0), -(_num(d.get("impatto")) or 0), d["id"])

    esclusi = {i for i, d in dati.items() if d["decisione"] == OSSERVAZIONE}
    eccezioni = sorted((d for i, d in dati.items() if i not in esclusi and eccezione(d)), key=ordine)
    candidati = sorted((d for i, d in dati.items() if i not in esclusi and not eccezione(d) and candidato(d)), key=ordine)
    posti = max(regola["capienza"] - len(eccezioni), 0)
    dentro, fuori_capienza = candidati[:posti], {d["id"] for d in candidati[posti:]}
    ultimo = min((d["score"] for d in eccezioni + dentro if d["score"] is not None), default=None)

    esito = {}
    for d in eccezioni + dentro:
        sopra = f"Prossimita {d['prossimita']} e Probabilita {d['probabilita']}: sopra la soglia"
        e = eccezione(d)
        if e and candidato(d):
            motivo = f"{sopra}; posto garantito: {e}"
        elif e:
            motivo = f"sotto la soglia, nel radar per eccezione: {e}"
        else:
            motivo = sopra
        esito[d["id"]] = (RADAR, motivo)
    for i, d in dati.items():
        if i in esito:
            continue
        if i in esclusi:
            motivo = "in osservazione per decisione del validatore"
        elif i in fuori_capienza:
            motivo = f"fuori per capienza: score {_it(d['score'])}, ultimo nel radar {_it(ultimo)}"
        else:
            sotto = [f"{nome} {d.get(chiave)} sotto la soglia {s}" for nome, chiave, s in
                     (("Prossimita", "prossimita", sp), ("Probabilita", "probabilita", sb))
                     if (_num(d.get(chiave)) or 0) < s]
            motivo = "; ".join(sotto)
        if d.get("stato_prima") == RADAR and regola["cicli_uscita"] >= 2 and i not in esclusi:
            esito[i] = (IN_USCITA, f"{motivo} (primo ciclo: esce se lo e' anche al ciclo dopo)")
        else:
            esito[i] = (OSSERVAZIONE, motivo)
    # Oltre il massimo delle viste nessun "in uscita": esce chi ha lo score piu' basso.
    radar = sorted((dati[i] for i, (s, _) in esito.items() if nel_radar(s)), key=ordine)
    for d in radar[regola["max_radar"]:]:
        esito[d["id"]] = (OSSERVAZIONE, esito[d["id"]][1] + f"; oltre i {regola['max_radar']} posti del radar")

    out = {}
    for i, (stato, motivo) in esito.items():
        prima = dati[i].get("stato_prima")
        movimento = (ENTRATO if nel_radar(stato) and prima == OSSERVAZIONE else
                     USCITO if not nel_radar(stato) and nel_radar(prima) else "")
        out[i] = {"stato": stato, "motivo": motivo, "movimento": movimento, "score": dati[i]["score"],
                  "margine": dati[i]["margine"]}
    return out


def y_azioni(azioni):
    """Y delle azioni per il margine di Mosca: orizzonte piu' lungo, in anni, delle azioni non respinte (None senza
    azioni). azioni: elenco di orizzonti '3 mesi' / '6 mesi' / '12 mesi' (o numeri di mesi)."""
    mesi = []
    for a in azioni:
        try:
            mesi.append(int(str(a).split()[0]))
        except (ValueError, IndexError):
            continue
    return max(mesi) / 12 if mesi else None
