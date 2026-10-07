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
  - "Da motivare": regole di metodo (C3, date delle fonti di C5, coppia e soglie dei KRI di C9) e i Bloccanti
    di A5. Non fermano: vanno nella colonna "Segnalazioni dei controlli" del foglio Validazione e chiedono una
    Motivazione al validatore; le soglie e il salto di piu' di un punto li corregge la validazione stessa;
  - "Osservazione": dubbi da considerare, senza obblighi.
A5 e' facoltativo: senza il suo esito valgono i soli controlli di questo modulo.

Dal 07/10/2026 (D-73) anche la lista di osservazione (campo "osservazione" di A1), solo qui e non in A5 (il suo
prompt e' al limite degli 8.000 caratteri): codici delle voci e promozioni coerenti come C1 Bloccante, perche' cambiano
lo stato del registro; il resto come Osservazione. Le regole le legge A1 nella guida di scrittura (allegato).
"""

import re

# Dimensioni valutate da A1 (rubrica, sezione 1). La Velocity puo' essere null.
DIMENSIONI = ["impatto", "probabilita", "prossimita", "velocity"]
VALORI = DIMENSIONI
TIPI_KRI = ["Esposizione", "Evoluzione"]          # D-64: esattamente un KRI per tipo
MAX_OSSERVAZIONE = 30                             # D-73: voci in osservazione al massimo
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


def controlla(payload, baseline):
    """Applica i controlli meccanizzabili. Restituisce un dict conforme allo schema A5."""
    r = []
    B, M, O = BLOCCANTE, DA_MOTIVARE, OSSERVAZIONE
    base = {x["id_rischio"]: x for x in baseline.get("rischi", [])}
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
        for rid in sorted({i for i in ids if i in base} - da_rivalutare):
            r.append(_rilievo("C1", rid, B, "Rischio esistente non indicato per il ciclo straordinario: non va riscritto "
                                            "(lo script lo riporta com'era)."))
    else:
        for rid in sorted(set(base) - set(ids)):
            r.append(_rilievo("C1", rid, B, "Rischio in anagrafica non valutato nel ciclo."))
    for rid in sorted({i for i in ids if ids.count(i) > 1}):
        r.append(_rilievo("C1", rid, B, "id_rischio ripetuto nel payload."))
    for x in rischi:
        prec = base.get(x["id_rischio"])
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
        prec = base.get(rid)
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
        if sorted(k.get("tipo") or "" for k in kri) != TIPI_KRI:
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

    r.extend(controlla_osservazione(payload, baseline))

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


def controlla_osservazione(payload, baseline):
    """Lista di osservazione (D-73): A1 scrive solo le voci nuove e quelle con evidenza nuova. Rilievi sul ciclo
    (id_rischio None, il codice della voce nel testo): C1 Bloccante per codici e promozioni, Osservazione per il resto."""
    r = []
    voci = payload.get("osservazione") or []
    in_base = {v["oss_id"]: v for v in baseline.get("osservazione", [])}
    nuovi_rischi = {x["id_rischio"] for x in payload.get("rischi", [])} - {x["id_rischio"] for x in baseline.get("rischi", [])}
    noti = {x["id_rischio"] for x in payload.get("rischi", [])} | {x["id_rischio"] for x in baseline.get("rischi", [])}
    d_prec = baseline.get("data_riferimento_precedente") or "0000-00-00"
    d_rif = payload.get("data_riferimento", "")
    ids = [v.get("oss_id") for v in voci if v.get("oss_id")]
    for oid in sorted({i for i in ids if ids.count(i) > 1}):
        r.append(_rilievo("C1", None, BLOCCANTE, f"Osservazione: {oid} ripetuta nel payload."))
    for v in voci:
        oid, esito = v.get("oss_id"), v.get("esito")
        chi = oid or f"voce nuova '{v.get('nome', '')[:50]}'"
        if esito == "nuova" and oid:
            r.append(_rilievo("C1", None, BLOCCANTE, f"Osservazione: {oid} ha esito nuova ma ha gia' un codice: una voce "
                                                     "nuova ha oss_id null (lo assegna lo script)."))
        elif esito != "nuova" and not oid:
            r.append(_rilievo("C1", None, BLOCCANTE, f"Osservazione: {chi} ha esito {esito} senza oss_id: una voce gia' "
                                                     "in osservazione si indica con il suo codice della baseline."))
        elif esito != "nuova" and oid not in in_base:
            r.append(_rilievo("C1", None, BLOCCANTE, f"Osservazione: {oid} non e' fra le voci in osservazione della baseline."))
        if esito == "promossa" and v.get("promosso_a") not in nuovi_rischi:
            r.append(_rilievo("C1", None, BLOCCANTE, f"Osservazione: {chi} promossa a {v.get('promosso_a')}, che non e' un "
                                                     "rischio nuovo di questo ciclo: censire il rischio in rischi e indicarne "
                                                     "l'id in promosso_a (un fenomeno assorbito da un rischio esistente si archivia)."))
        elif esito != "promossa" and v.get("promosso_a"):
            r.append(_rilievo("C1", None, BLOCCANTE, f"Osservazione: {chi} ha promosso_a {v['promosso_a']} con esito {esito}: "
                                                     "promosso_a solo con esito promossa."))
        ignoti = sorted(set(v.get("rischi_toccati") or []) - noti)
        if ignoti:
            r.append(_rilievo("C1", None, OSSERVAZIONE, f"Osservazione: {chi} tocca rischi che non sono nel registro: "
                                                        f"{', '.join(ignoti)}."))
        for f in v.get("fonti") or []:
            if f["data"] > d_rif:
                r.append(_rilievo("C5", None, OSSERVAZIONE, f"Osservazione: {chi}, fonte '{f['riferimento'][:60]}' datata "
                                                            f"{f['data']}, dopo la data di riferimento {d_rif}."))
        if esito != "nuova" and oid in in_base and not any(d_prec < f["data"] for f in v.get("fonti") or []):
            r.append(_rilievo("C5", None, OSSERVAZIONE, f"Osservazione: {oid} aggiornata ({esito}) senza una fonte dopo "
                                                        f"{d_prec}: una voce senza evidenza nuova non si riscrive."))
        if esito == "nuova" and v.get("orizzonte_anni", 99) <= 2 and v.get("plausibilita") == "in crescita":
            r.append(_rilievo("C1", None, OSSERVAZIONE, f"Osservazione: {chi} in crescita entro {v['orizzonte_anni']} anni: "
                                                        "verificare se e' gia' un rischio del registro (Prossimita 1-2)."))
    usciti = {v.get("oss_id") for v in voci if v.get("esito") in ("promossa", "archiviata")}
    attive = (set(in_base) - usciti) | {v.get("oss_id") for v in voci if v.get("oss_id") and v.get("esito") not in ("promossa", "archiviata")}
    totale = len(attive) + sum(1 for v in voci if v.get("esito") == "nuova" and not v.get("oss_id"))
    if totale > MAX_OSSERVAZIONE:
        r.append(_rilievo("C1", None, BLOCCANTE, f"Osservazione: {totale} voci in osservazione dopo il ciclo, oltre le "
                                                 f"{MAX_OSSERVAZIONE}: archiviare le meno rilevanti."))
    return r


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
