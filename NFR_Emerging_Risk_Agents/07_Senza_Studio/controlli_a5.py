"""Controlli meccanizzabili di A5 Challenger — controparte deterministica.

Stessi nove controlli (C1-C9) del prompt 02_Agenti/A5_Challenger.md, nella
parte esprimibile come regola. Copertura DICHIARATA, non sottintesa:
  - C1, C2, C3, C7, C9: per intero (C3 = date, frasi generiche, max 1 punto).
  - C5: date delle fonti per intero (Da motivare, D-71); fonte di rilevanza 3 per le
    valutazioni alte e fonti perse come Osservazioni (D-58).
  - C6, C8: euristica a stringhe, solo "Osservazione" (C8 dal 30/09/2026,
    D-54: il controllo dell'owner "persona" e' passato alla validazione; dal
    02/10/2026, D-69, anche un'azione uguale a un'azione aperta).
  - C4 (plausibilita' rispetto ai descrittori): NON coperto. Richiede il
    giudizio di A5. Questo modulo non sostituisce A5: lo affianca.

Dal 30/09/2026 (D-49..D-56) A1 non scrive esito ne' i "da/a" delle
variazioni (li calcola lo script: esegui_ciclo_locale.completa_payload), non
valuta Gap_Controlli, puo' lasciare la Velocity null e propone KRI con soglie
facoltative. Dal 30/09 sera (D-57, D-58, D-60) Severity si chiama Impatto, la
Confidence del rischio non c'e' piu' (ogni fonte ha una rilevanza 1-3) e A1
propone gli anni di adeguamento; i KRI sono due per rischio, uno di
Esposizione e uno di Evoluzione (D-64). I controlli lavorano sul payload COSI' COME L'HA
SCRITTO A1, confrontato con la baseline.

L'esito ha lo stesso formato dell'output di A5 (01_Kernel/schema_output_A5.json),
cosi' i due si leggono e si combinano allo stesso modo.

Dal 06/10/2026 (D-71) tre gravita':
  - "Bloccante": solo l'integrita' del registro (C1, C2, C7 e gli identificativi dei KRI di C9): ferma la
    scrittura, perche' senza queste regole il registro diventerebbe incoerente;
  - "Da motivare": regole di metodo (C3, date delle fonti di C5, coppia e soglie dei KRI di C9, KRI non riletti
    in un ciclo straordinario di C7, D-77) e i Bloccanti di A5. Non fermano: vanno nella colonna "Segnalazioni dei controlli" del foglio Validazione e chiedono una
    Motivazione al validatore; le soglie e il salto di piu' di un punto li corregge la validazione stessa;
  - "Osservazione": dubbi da considerare, senza obblighi.
A5 e' facoltativo: senza il suo esito valgono i soli controlli di questo modulo.

Dall'08/10/2026 (D-79, registro unico) i rischi sono nel radar o in osservazione: lo stato si prevede qui con la regola
della baseline (radar.stati, la stessa dello script). Completezza (C1) solo per il radar; KRI e azioni (C8, C9) solo per
chi sara' nel radar: mancano a un rischio che entra dall'osservazione = da motivare, a un altro rischio del radar =
Bloccante; scritti per un rischio in osservazione = Osservazione (lo script non li registra). Piu' di 20 rischi in
osservazione = C1 Bloccante. Le regole le legge A1 nella guida di scrittura (allegato).
"""

import re

import radar

# Dimensioni valutate da A1 (rubrica, sezione 1). La Velocity puo' essere null.
DIMENSIONI = ["impatto", "probabilita", "prossimita", "velocity"]
VALORI = DIMENSIONI
TIPI_KRI = ["Esposizione", "Evoluzione"]          # D-64: esattamente un KRI per tipo
# D-74: categorie della tassonomia interna della Banca in perimetro (01_Kernel/tassonomia_nfr.md; il collaudo verifica che
# coincidano con il kernel). FP = rischio esistente fuori perimetro, da togliere con dismetti.
CATEGORIE = ["9.1", "9.4", "9.5", "9.6", "9.7", "9.8", "9.9", "9.11", "9.13"]
FUORI_PERIMETRO = "FP"
BLOCCANTE, DA_MOTIVARE, OSSERVAZIONE = "Bloccante", "Da motivare", "Osservazione"     # D-71

# Frasi che non sono evidenza (rubrica, regola di variazione 3). Confronto
# in minuscolo, per sottostringa. Estendere qui se in esercizio ne emergono altre.
FRASI_GENERICHE = [
    "contesto in evoluzione", "maggiore attenzione mediatica", "trend di mercato",
    "scenario in evoluzione", "crescente attenzione", "clima di incertezza",
    "contesto generale", "evoluzione del contesto", "attenzione dei media",
]

# Parole che indicano una funzione aziendale (C8), confrontate come parole
# intere (altrimenti "cio" riconoscerebbe "Lucio"). Euristica: un owner senza
# nessuna di queste parole produce un'Osservazione. La stessa regola (sembra_persona)
# e' un fermo nella validazione umana (esegui_ciclo_locale.py, comando valida).
PAROLE_FUNZIONE = [
    "funzione", "direzione", "ufficio", "servizio", "area", "unita", "unità",
    "comitato", "team", "struttura", "dipartimento", "divisione", "presidio",
    "risk", "compliance", "audit", "operations", "operational", "ict", "it",
    "legale", "hr", "risorse umane", "sicurezza", "security", "cyber",
    "information", "resilience", "governance", "management", "comunicazione",
    "istituzionale", "antifrode", "continuity", "pmo", "cro", "cio",
    "ciso", "coo", "cfo", "dpo", "customer", "experience", "clienti",
    "procurement", "acquisti", "immobili", "infrastrutture", "tecnologia",
    "organizzazione", "operativa", "operativo", "controlli", "business",
]
NOME_COGNOME = re.compile(r"^[A-ZÀ-Ý][a-zà-ÿ']+(\s+[A-ZÀ-Ý][a-zà-ÿ']+){1,2}$")


def ha_funzione(owner):
    return any(re.search(r"\b" + re.escape(p) + r"\b", owner.lower()) for p in PAROLE_FUNZIONE)


def sembra_persona(owner):
    """Owner con la forma 'Nome Cognome' e nessuna parola di funzione.
    La usano C8 (Osservazione) e la validazione umana (fermo): stessa regola."""
    owner = owner.strip()
    return bool(NOME_COGNOME.match(owner)) and not ha_funzione(owner)


def _rilievo(controllo, id_rischio, gravita, descrizione):
    return {"controllo": controllo, "id_rischio": id_rischio, "gravita": gravita, "descrizione": descrizione}


def _diversi(a, b):
    return a != b                       # None contro None = uguali; None contro 3 = diversi


def _stesso_testo(testo):
    """Descrizione di un'azione a meno di maiuscole, spazi e punteggiatura finale (C8, D-69)."""
    return re.sub(r"\s+", " ", testo.lower()).strip(" .;")


def _controlla_analisi_evento(payload, base, ids, d_rif):
    """Ciclo straordinario (D-77): l'analisi dell'evento di A8. Tutte Osservazioni: l'analisi spiega, non scrive valori
    nel registro; un ciclo straordinario fatto con A1 (senza analisi) resta possibile."""
    O = OSSERVAZIONE
    analisi = payload.get("analisi_evento")
    if not analisi:
        return [_rilievo("C1", None, O, "Ciclo straordinario senza analisi_evento: manca l'analisi approfondita dell'evento "
                                        "(agente A8); il validatore la trova solo nei razionali e nella sintesi.")]
    r = []
    toccati = [t["id_rischio"] for t in analisi.get("rischi_toccati") or []]
    for rid in sorted(set(toccati) - set(ids) - set(base)):
        r.append(_rilievo("C1", rid, O, "analisi_evento: rischio toccato che non e' ne' nel registro ne' fra i rischi nuovi."))
    for rid in sorted({t for t in toccati if t in base} - set(ids)):
        r.append(_rilievo("C1", rid, O, "analisi_evento: rischio toccato dall'evento ma non indicato per lo straordinario: la "
                                        "funzione di rischio valuti se rivalutarlo (un altro straordinario o il trimestre)."))
    for rid in sorted(set(ids) - set(toccati)):
        r.append(_rilievo("C1", rid, O, "analisi_evento: rischio scritto nel ciclo ma assente da rischi_toccati: dire che "
                                        "cosa gli fa l'evento."))
    for d in analisi.get("documenti") or []:
        if d_rif and str(d.get("data")) > d_rif:
            r.append(_rilievo("C1", None, O, f"analisi_evento: documento datato dopo la data di riferimento ({d.get('data')}): "
                                             f"{d.get('riferimento')}."))
    return r


def stati_previsti(payload, baseline):
    """D-79: stato che ogni rischio avra' con i valori proposti da A1, con la regola della baseline (la stessa che applica
    lo script alla scrittura). Entrano i rischi scritti e quelli che lo script riporta: in osservazione non toccati e, in
    uno straordinario, quelli del radar non rivalutati. None per una baseline precedente al registro unico."""
    regola = baseline.get("regola_radar")
    if not regola:
        return None
    nel = {x["id_rischio"]: x for x in baseline.get("rischi", [])}
    oss = {x["id_rischio"]: x for x in baseline.get("rischi_in_osservazione", [])}
    scritti = {x["id_rischio"] for x in payload.get("rischi", [])}

    def ingresso(rid, valori, prima, y):
        return {"id": rid, **{d: valori.get(d) for d in radar.DIMENSIONI},
                "supervisore": bool((nel.get(rid) or {}).get("attenzione_supervisore")),
                "anni_adeguamento": (nel[rid].get("anni_adeguamento") if rid in nel else valori.get("anni_adeguamento")),
                "y_azioni": y, "stato_prima": (prima or {}).get("stato") or (radar.RADAR if rid in nel else None),
                "decisione": (prima or {}).get("decisione_stato")}
    ingressi = [ingresso(x["id_rischio"], x, nel.get(x["id_rischio"]) or oss.get(x["id_rischio"]),
                         radar.y_azioni([a["orizzonte"] for a in x.get("azioni_mitigazione") or []]))
                for x in payload.get("rischi", [])]
    riportati = {**oss, **(nel if baseline.get("straordinario") else {})}
    for rid, p in riportati.items():
        if rid not in scritti:
            y = radar.y_azioni([a.get("orizzonte") for a in baseline.get("azioni_aperte", []) if a.get("id_rischio") == rid])
            ingressi.append(ingresso(rid, p, p, y if rid in nel else None))
    return radar.stati(ingressi, regola)


def controlla(payload, baseline):
    """Applica i controlli meccanizzabili. Restituisce un dict conforme allo schema A5."""
    r = []
    B, M, O = BLOCCANTE, DA_MOTIVARE, OSSERVAZIONE
    base = {x["id_rischio"]: x for x in baseline.get("rischi", [])}          # il radar (D-79)
    osservati = {x["id_rischio"]: x for x in baseline.get("rischi_in_osservazione", [])}
    tutti = {**base, **osservati}
    previsti = stati_previsti(payload, baseline)
    nel_radar = lambda rid: previsti is None or radar.nel_radar(previsti[rid]["stato"])
    kri_base = {k["kri_id"]: k for k in baseline.get("kri_in_vigore", [])}
    d_prec = baseline.get("data_riferimento_precedente") or "0000-00-00"
    d_rif = payload.get("data_riferimento", "")
    rischi = payload.get("rischi", [])

    # ---------------- C1 Completezza
    if payload.get("ciclo") != baseline.get("ciclo_da_valutare"):
        r.append(_rilievo("C1", None, B, f"ciclo {payload.get('ciclo')} diverso dal ciclo da valutare della baseline ({baseline.get('ciclo_da_valutare')})."))
    if d_rif != baseline.get("data_riferimento"):
        r.append(_rilievo("C1", None, B, f"data_riferimento {d_rif} diversa da quella della baseline ({baseline.get('data_riferimento')})."))
    ids = [x["id_rischio"] for x in rischi]
    straord = baseline.get("straordinario")
    if straord:                                      # D-75: solo i rischi indicati, piu' quelli nuovi
        da_rivalutare = set(straord.get("rischi_da_rivalutare") or [])
        for rid in sorted(da_rivalutare - set(ids)):
            r.append(_rilievo("C1", rid, B, "Rischio da rivalutare nel ciclo straordinario assente dall'output."))
        for rid in sorted({i for i in ids if i in tutti} - da_rivalutare):
            r.append(_rilievo("C1", rid, B, "Rischio esistente non indicato per il ciclo straordinario: non va riscritto "
                                            "(lo script lo riporta com'era)."))
        if not da_rivalutare and not any(i not in tutti for i in ids):
            r.append(_rilievo("C1", None, B, "Ciclo straordinario di solo censimento (nessun rischio da rivalutare): serve "
                                             "almeno un rischio nuovo creato dall'evento."))
        r += _controlla_analisi_evento(payload, tutti, ids, d_rif)
    else:
        for rid in sorted(set(base) - set(ids)):
            r.append(_rilievo("C1", rid, B, "Rischio in anagrafica non valutato nel ciclo."))
        if payload.get("analisi_evento"):
            r.append(_rilievo("C1", None, O, "analisi_evento e' per i cicli straordinari (A8): in un ciclo trimestrale resta "
                                             "nell'output archiviato ma non va nel registro."))
    for rid in sorted({i for i in ids if ids.count(i) > 1}):
        r.append(_rilievo("C1", rid, B, "id_rischio ripetuto nel payload."))
    for x in rischi:
        prec = tutti.get(x["id_rischio"])
        et, et_prec = x["event_type"], (prec or {}).get("event_type")
        if et == FUORI_PERIMETRO:
            if prec is None:
                r.append(_rilievo("C1", x["id_rischio"], B, "Un rischio nuovo non e' mai fuori perimetro (FP): un tema fuori "
                                                           "perimetro va fra i fenomeni non censiti (motivo fuori_perimetro)."))
            elif et_prec != FUORI_PERIMETRO:
                r.append(_rilievo("C1", x["id_rischio"], M, f"Fuori perimetro (D-74): A1 non trova una categoria in perimetro per "
                                                           f"il meccanismo (era {et_prec}). Resta nel registro, fuori dal radar, "
                                                           "finche' la funzione di rischio non lo toglie con dismetti; motivare la "
                                                           "decisione."))
        elif prec is not None and et != et_prec:
            if et_prec not in CATEGORIE:             # codice di Basilea o FP di prima: riclassificazione (D-74)
                r.append(_rilievo("C1", x["id_rischio"], O, f"Riclassificato da {et_prec} alla categoria {et} (D-74): verificare "
                                                           "che corrisponda al meccanismo di perdita; se no, correggere la "
                                                           "categoria nell'anagrafica (Parametri, colonna J)."))
            else:
                r.append(_rilievo("C1", x["id_rischio"], B, f"Categoria {et} diversa da quella in anagrafica ({et_prec}): un "
                                                           "rischio esistente non cambia meccanismo; se e' un altro rischio, "
                                                           "serve un id nuovo."))

    for x in rischi:
        rid = x["id_rischio"]
        prec = tutti.get(rid)
        var = x.get("variazioni", [])

        # ---------------- C2 Variazioni: una voce per ogni valore cambiato, e solo per quelli
        if prec is not None:
            cambiati = [v for v in VALORI if _diversi(x.get(v), prec.get(v))]
            for v in cambiati:
                voci = [z for z in var if z["dimensione"] == v]
                if len(voci) != 1:
                    r.append(_rilievo("C2", rid, B, f"{v} passa da {prec.get(v)} a {x.get(v)}: serve una (e una sola) "
                                                    "voce in variazioni con l'evidenza."))
            for z in var:
                if z["dimensione"] not in cambiati:
                    r.append(_rilievo("C2", rid, B, f"Variazione dichiarata su {z['dimensione']} che non cambia rispetto alla baseline."))
            # C3b sul valore effettivo: al massimo un punto (una Velocity prima null entra con qualunque valore).
            for v in VALORI:
                a, b = prec.get(v), x.get(v)
                if a is not None and b is not None and abs(b - a) > 1:
                    r.append(_rilievo("C3", rid, M, f"{v} passa da {a} a {b}: piu' di un punto fra cicli consecutivi "
                                                    "(in validazione va riportato a un punto: valida non lo accetta)."))
        elif var:
            r.append(_rilievo("C2", rid, B, "Un rischio nuovo non ha variazioni: non esiste un valore precedente."))

        # ---------------- C3 Evidenza delle variazioni
        for z in var:
            if not (d_prec < z["data_evidenza"] <= d_rif):
                r.append(_rilievo("C3", rid, M, f"Evidenza su {z['dimensione']} datata {z['data_evidenza']}: deve essere dopo {d_prec} e non dopo {d_rif}."))
            testo = z["evidenza"].lower()
            generiche = [f for f in FRASI_GENERICHE if f in testo]
            if generiche:
                r.append(_rilievo("C3", rid, M, f"Evidenza su {z['dimensione']} generica ({', '.join(generiche)}): serve un fatto specifico."))

        # ---------------- C5 Fonti (D-58: rilevanza per fonte al posto della Confidence)
        fonti = x.get("fonti", [])
        for f in fonti:
            if f["data"] > d_rif:
                r.append(_rilievo("C5", rid, M, f"Fonte '{f['riferimento'][:60]}' datata {f['data']}, dopo la data di riferimento {d_rif}."))
        if (x.get("probabilita") == 5 or (x.get("prossimita") or 0) >= 4) and not any(f.get("rilevanza") == 3 for f in fonti):
            r.append(_rilievo("C5", rid, O, f"Probabilita {x.get('probabilita')} e Prossimita {x.get('prossimita')} senza una fonte "
                                            "di rilevanza 3: ammesso solo con la deroga per un fenomeno ad altissimo impatto, "
                                            "dichiarata nel razionale."))
        if prec is not None and len(fonti) < len(prec.get("fonti", [])) and not any(_diversi(x.get(v), prec.get(v)) for v in VALORI):
            r.append(_rilievo("C5", rid, O, f"Fonti scese da {len(prec['fonti'])} a {len(fonti)} con i valori invariati: "
                                            "verificare che restino sostenuti (regola di variazione 5)."))

        # ---------------- D-79 Registro unico: KRI e azioni solo per chi sara' nel radar
        if not nel_radar(rid):
            if x.get("kri_proposti") or x.get("azioni_mitigazione"):
                r.append(_rilievo("C9", rid, O, f"Rischio in osservazione ({previsti[rid]['motivo']}): KRI e azioni non si "
                                                "scrivono, lo script non li registra."))
            if rid in osservati and not any(d_prec < f["data"] for f in x.get("fonti", [])):
                r.append(_rilievo("C5", rid, O, f"Rischio in osservazione riscritto senza una fonte dopo {d_prec}: senza "
                                                "evidenza nuova non si riscrive (resta com'era)."))
            if not x.get("orizzonte_anni") or not x.get("segnale_avvicinamento"):
                r.append(_rilievo("C1", rid, O, "Rischio in osservazione senza orizzonte_anni o segnale_avvicinamento: "
                                                "servono a chi legge per capire quanto e' lontano e che cosa lo farebbe salire."))
            continue
        entra = previsti is not None and previsti[rid]["movimento"] == radar.ENTRATO
        if not x.get("kri_proposti") or not x.get("azioni_mitigazione"):
            manca = " e ".join(m for m, c in (("i due KRI", not x.get("kri_proposti")),
                                               ("le azioni", not x.get("azioni_mitigazione"))) if c)
            r.append(_rilievo("C9", rid, M if entra else B,
                              f"Rischio che entra nel radar senza {manca}: scriverli (o restano da definire al ciclo dopo)."
                              if entra else f"Rischio del radar senza {manca}: ogni rischio del radar ha due KRI e da 1 a 5 "
                                            "azioni."))

        # ---------------- C8 Azioni (euristica, solo Osservazioni)
        aperte = {_stesso_testo(z["descrizione"]): z["id_azione"] for z in baseline.get("azioni_aperte", [])
                  if z.get("id_rischio") == rid}
        for a in x.get("azioni_mitigazione", []):
            owner = a["owner"].strip()
            if sembra_persona(owner):
                r.append(_rilievo("C8", rid, O, f"Owner '{owner}' sembra una persona: deve essere una funzione "
                                                "(la validazione non accetta il nome di una persona)."))
            elif not ha_funzione(owner):
                r.append(_rilievo("C8", rid, O, f"Owner '{owner}': verificare che sia una funzione aziendale."))
            gemella = aperte.get(_stesso_testo(a["descrizione"]))
            if gemella:
                r.append(_rilievo("C8", rid, O, f"Azione '{a['descrizione'][:60]}' uguale all'azione aperta {gemella}: "
                                                "non riproporla; se resta valida, richiamala nel razionale e proponi il "
                                                "passo successivo."))

        # ---------------- C9 KRI
        kri = x.get("kri_proposti", [])
        if kri and sorted(k.get("tipo") or "" for k in kri) != TIPI_KRI:
            r.append(_rilievo("C9", rid, M, f"{len(kri)} KRI proposti ({', '.join(k.get('tipo') or 'senza tipo' for k in kri)}): "
                                            "servono due KRI, uno di Esposizione e uno di Evoluzione."))
        for k in kri:
            nome = k["nome"][:50]
            att, all_ = k.get("soglia_attenzione"), k.get("soglia_allerta")
            if (att is None) != (all_ is None):
                r.append(_rilievo("C9", rid, M, f"KRI '{nome}': soglie entrambe o nessuna (in validazione: scriverle "
                                                "entrambe o svuotarle; valida non accetta una sola)."))
            elif att is not None and all_ < att:
                r.append(_rilievo("C9", rid, M, f"KRI '{nome}': soglia_allerta {all_} < soglia_attenzione {att} (soglie "
                                                "invertite: in validazione vanno corrette, valida non le accetta)."))
            kid = k.get("kri_id")
            if kid:
                if not kid.startswith(rid + "-K"):
                    r.append(_rilievo("C9", rid, B, f"KRI {kid} appartiene a un altro rischio."))
                elif kid not in kri_base:
                    r.append(_rilievo("C9", rid, B, f"KRI {kid} non e' in vigore nella baseline: un KRI nuovo ha kri_id null."))
                elif kri_base[kid].get("tipo") and k.get("tipo") != kri_base[kid]["tipo"]:
                    r.append(_rilievo("C9", rid, O, f"KRI {kid}: tipo {k.get('tipo')}, nella baseline {kri_base[kid]['tipo']} "
                                                    "(un KRI in vigore conserva il tipo)."))
        if prec is not None:
            riproposti = {k.get("kri_id") for k in kri}
            usciti = sorted(k for k, v in kri_base.items() if v["id_rischio"] == rid and k not in riproposti)
            if usciti:
                r.append(_rilievo("C9", rid, O, f"KRI in vigore non riproposti, escono di vigore: {', '.join(usciti)}."))

    tutti_kid = [k["kri_id"] for x in rischi for k in x.get("kri_proposti", []) if k.get("kri_id")]
    for kid in sorted({k for k in tutti_kid if tutti_kid.count(k) > 1}):
        r.append(_rilievo("C9", None, B, f"kri_id {kid} usato piu' di una volta."))

    # ---------------- C6 Inflazione progressiva (euristica, livello ciclo)
    esistenti = [x for x in rischi if x["id_rischio"] in base]
    def aumenta(x):
        p = base[x["id_rischio"]]
        return any(x.get(v) is not None and p.get(v) is not None and x[v] > p[v] for v in DIMENSIONI)
    in_aumento = [x for x in esistenti if aumenta(x)]
    if esistenti and len(in_aumento) > len(esistenti) / 2:
        nuove = any(f["data"] > d_prec for x in in_aumento for f in x["fonti"])
        if not nuove:
            r.append(_rilievo("C6", None, O, f"{len(in_aumento)} rischi su {len(esistenti)} in aumento senza fonti nuove: possibile inflazione progressiva."))

    # ---------------- C7 Rilettura dei KRI del ciclo precedente: solo KRI in vigore, una volta ciascuno
    riletti = [z["kri_id"] for z in payload.get("ricalcolo_kri_ciclo_precedente", [])]
    for kid in sorted(set(riletti) - set(kri_base)):
        r.append(_rilievo("C7", None, B, f"KRI {kid} riletto ma non in vigore nella baseline."))
    for kid in sorted({k for k in riletti if riletti.count(k) > 1}):
        r.append(_rilievo("C7", None, B, f"KRI {kid} riletto piu' di una volta."))
    if baseline.get("straordinario"):
        # D-77: nello straordinario A8 rilegge ogni KRI in vigore dei rischi rivalutati che ripropone; un valore che
        # manca lascia il KRI Non rilevato e toglie al livello di allerta l'aggravante proprio quando il rischio sale.
        # Da motivare, non Bloccante: il dato puo' non essere nei documenti e il validatore lo scrive nella griglia.
        for x in rischi:
            if x["id_rischio"] not in base:
                continue
            mancanti = sorted({k.get("kri_id") for k in x.get("kri_proposti", [])}
                              & {kid for kid, k in kri_base.items() if k.get("id_rischio") == x["id_rischio"]}
                              - set(riletti))
            if mancanti:
                r.append(_rilievo("C7", x["id_rischio"], M, f"Ciclo straordinario: KRI in vigore non riletti "
                                                            f"({', '.join(mancanti)}): restano Non rilevati. Rileggerli, o "
                                                            "scrivere il valore nella griglia di validazione."))

    # ---------------- D-79 Al massimo 20 rischi in osservazione (Parametri, capienzaOsservazione)
    if previsti is not None:
        quanti = sum(1 for s in previsti.values() if s["stato"] == radar.OSSERVAZIONE)
        massimo = baseline["regola_radar"].get("max_osservazione", radar.REGOLA_DEFAULT["max_osservazione"])
        if quanti > massimo:
            r.append(_rilievo("C1", None, B, f"{quanti} rischi in osservazione dopo il ciclo, oltre il massimo di {massimo}: "
                                             "lasciare fuori i meno rilevanti (fra i fenomeni non censiti, troppo_lontano)."))

    bloccanti = sum(1 for x in r if x["gravita"] == B)
    da_motivare = sum(1 for x in r if x["gravita"] == M)
    return {
        "ciclo": payload.get("ciclo") or "0000Q1",
        "esito": "Da rivedere" if bloccanti else "Approvato",
        "rilievi": r,
        "sintesi": (f"Controlli meccanizzati: {bloccanti} rilievi bloccanti, {da_motivare} da motivare in validazione, "
                    f"{len(r) - bloccanti - da_motivare} osservazioni. Bloccanti solo per l'integrita' (C1, C2, C7, "
                    "identificativi dei KRI); C3, date di C5, coppia e soglie dei KRI da motivare; C5 (rilevanza), C6 e "
                    "C8 come Osservazioni; C4 non coperto: resta al giudizio di A5, se usato."),
    }


def combina(meccanico, agente=None):
    """Esito del ciclo (D-71): ferma solo un Bloccante dei controlli meccanizzati, cioe' un difetto di integrita'.
    A5 e' facoltativo; i suoi rilievi Bloccanti diventano "Da motivare": vanno nella colonna Segnalazioni del foglio
    Validazione e chiedono una Motivazione al validatore. I rilievi restano tutti, con l'origine."""
    rilievi = [dict(x, origine="script") for x in meccanico["rilievi"]] + \
              [dict(x, origine="A5", gravita=DA_MOTIVARE if x["gravita"] == BLOCCANTE else x["gravita"])
               for x in (agente["rilievi"] if agente else [])]
    fermo = meccanico["esito"] != "Approvato"
    return {"esito": "Da rivedere" if fermo else "Approvato", "rilievi": rilievi,
            "da_motivare": [x for x in rilievi if x["gravita"] == DA_MOTIVARE]}
