"""Knowledge di A7 Assistente del registro (D-72): un file di testo per posto dell'anagrafica e uno per il ciclo.

A7 risponde in chat, senza allegati: legge questi file dalla knowledge (cartella Spiegazioni della library
Kernel). Li scrivono `trimestrale`, `valida` e `dismetti` alla fine. **Nomi sempre uguali**: `Ciclo.txt` e un
file per ogni posto dell'anagrafica, `Rischio_01.txt` ... `Rischio_20.txt` (un posto libero dice che e'
libero). Un file gia' indicizzato e aggiornato si reindicizza subito, uno nuovo puo' aspettare
l'indicizzazione giornaliera: con i posti fissi un rischio appena censito finisce in un file che esiste gia' ed
e' visibile subito. Un file per posto perche' la ricerca della knowledge trova il pezzo giusto senza leggere un
file unico enorme; il codice del rischio sta in testa al file.

Contenuto, tutto dal registro e dall'archivio, nessuna stima: valori, motivazioni di A1 per dimensione,
urgenza, livello di allerta, variazioni, fonti, azioni, KRI e storia (le stesse di `schede.input_schede`), piu'
le decisioni del validatore, le segnalazioni dei controlli, il commento di A1, i parametri del radar, i
fenomeni che A1 ha considerato e non censito, la lista di osservazione (D-73), i rischi dismessi e le Note
dell'analista.
Testo semplice e non JSON: e' cio' che la knowledge di Agent Builder legge meglio.
"""

import json
import re
from pathlib import Path

import schede

PARAMETRI = [("moscaX", "X di Mosca, anni per decidere e avviare"), ("moscaYDefault", "Y di riserva, anni (senza azioni)"),
             ("sogliaDirezione", "Soglia di direzione dei segnali netti"), ("sogliaDelta", "Soglia del Delta composito"),
             ("livelloPxI", "Livello di allerta: P x I alta da"), ("livelloQuotaKRI", "Livello di allerta: quota di KRI in ambra o rosso da"),
             ("livelloMargine", "Livello di allerta: margine stretto sotto (anni)"),
             ("livelloForti", "Livello di allerta: segnali forti per l'Attivazione")]
MOTIVI_SCARTO = {"nessun_meccanismo": "nessun meccanismo di perdita per la Banca",
                 "fonte_non_specifica": "fonte non specifica o fuori dalla finestra del ciclo",
                 "gia_coperto": "gia' coperto da un rischio del registro",
                 "troppo_lontano": "troppo lontano (lista di osservazione piena)",
                 "fuori_perimetro": "fuori dal perimetro della tassonomia (lo seguono altre funzioni)",
                 "altro": "altro"}
RISCHIO_IN_ID = re.compile(r"NFR-\d{2}")
IMPATTO = {1: "limitato", 2: "contenuto", 3: "rilevante", 4: "grave", 5: "critico"}     # rubrica, sezione 1 (D-61)


def _valore(sessione, nome):
    try:
        v = sessione.intervallo_nome(nome).Value
    except Exception:
        return None
    return v


def _it(v, decimali=2):
    if v is None or v == "":
        return "—"
    if isinstance(v, float) and v == int(v) and decimali == 0:
        return str(int(v))
    if isinstance(v, (int, float)):
        return f"{v:.{decimali}f}".replace(".", ",") if isinstance(v, float) else str(v)
    return str(v)


def segnali_a3(scr, oss_id, dopo):
    """Notizie e segnali settimanali di A3 su una voce in osservazione, datati dopo 'dopo' (la data di riferimento
    del ciclo): li legge A1 nella baseline (D-73). Le notizie respinte in validazione (Non rilevante) non contano."""
    notizie = [{"id_notizia": n["ID_Notizia"], "data": str(n["Data"]), "titolo": n["Titolo"], "segnale": n["Segnale"]}
               for n in scr.righe("tblNews") if n.get("Voce_Osservazione") == oss_id and n.get("Segnale") != "Non rilevante"
               and (dopo is None or str(n["Data"]) > str(dopo))]
    segnali = [{"settimana": str(w["Settimana"]), "segnale": riga.split(" · ", 1)[1]}
               for w in scr.righe("tblSettimane") if dopo is None or str(w["Settimana"]) > str(dopo)
               for riga in str(w.get("Segnali_Osservazione") or "").split("\n") if riga.startswith(f"{oss_id} · ")]
    return {"notizie_a3": notizie, "segnali_a3": segnali}


def raccogli(scr, sessione, cartella_uscita, ciclo, ciclo_prec, data_rif, validato, nota_quadro=None):
    """Tutto cio' che A7 deve sapere del ciclo corrente, dal registro aperto e dall'archivio."""
    dati = schede.input_schede(scr, sessione, ciclo, ciclo_prec, data_rif)
    decisioni = {}
    for r in scr.righe("tblValidazione"):
        if str(r.get("Periodo")) != str(ciclo) or r.get("Decisione") not in ("Rettificato", "Respinto"):
            continue
        m = RISCHIO_IN_ID.search(str(r.get("ID") or ""))
        if m and r.get("Oggetto") != "Notizia":
            decisioni.setdefault(m.group(0), []).append(r)
    rilievi = {r["ID_Rischio"]: r.get("Rilievi") for r in scr.righe("tblRegister") if str(r["Ciclo"]) == str(ciclo)}
    sintesi = next((r for r in scr.righe("tblSintesi") if str(r["Ciclo"]) == str(ciclo)), {}) or {}
    note_passate = [(r["Ciclo"], r.get("Note_Analista")) for r in scr.righe("tblSintesi") if r.get("Note_Analista")]
    parametri = [(etichetta, _valore(sessione, nome)) for nome, etichetta in PARAMETRI]
    z = _valore(sessione, "anniProssimita")
    z = [r[0] for r in z] if isinstance(z, tuple) else []
    cartella_uscita = Path(cartella_uscita)
    scartati = []
    archivio_a1 = cartella_uscita / "Cicli" / str(ciclo) / f"A1_{ciclo}.json"
    if archivio_a1.exists():
        try:
            scartati = json.loads(archivio_a1.read_text(encoding="utf-8-sig")).get("fenomeni_non_censiti") or []
        except (ValueError, OSError):
            scartati = []
    dismessi = []
    for f in sorted((cartella_uscita / "Dismissioni").glob("NFR-*.json")):
        try:
            dismessi.append(json.loads(f.read_text(encoding="utf-8")))
        except (ValueError, OSError):
            continue
    try:
        osservazione = [r for r in scr.righe("tblOsservazione") if str(r["Ciclo"]) == str(ciclo)]
    except KeyError:
        osservazione = []                           # registro precedente al 2026-10-07b
    a3_oss = {v["OSS_ID"]: segnali_a3(scr, v["OSS_ID"], data_rif) for v in osservazione}
    decisioni_oss = {}
    for r in scr.righe("tblValidazione"):
        if r.get("Oggetto") == "Osservazione" and str(r.get("Periodo")) == str(ciclo) and                 r.get("Decisione") in ("Rettificato", "Respinto"):
            decisioni_oss.setdefault(str(r.get("ID")), []).append(r)
    rng_anag, _ = scr.leggi_anagrafica()
    return {"ciclo": ciclo, "ciclo_precedente": ciclo_prec, "data_riferimento": data_rif, "validato": validato,
            "posti": rng_anag.Rows.Count,
            "rischi": dati["rischi"], "pesi": dati["pesi"], "decisioni": decisioni, "rilievi": rilievi,
            "sintesi": sintesi, "parametri": parametri, "z_prossimita": z, "scartati": scartati,
            "dismessi": dismessi, "nota_quadro": nota_quadro, "note_passate": note_passate,
            "osservazione": osservazione, "decisioni_osservazione": decisioni_oss, "a3_osservazione": a3_oss}


def _stato(dati):
    return ("valori VALIDATI dal validatore" if dati["validato"] else
            "valori PROPOSTI da A1, non ancora validati: la validazione puo' cambiarli")


def testo_rischio(r, dati, oggi):
    rid = r["id_rischio"]
    v = r["valori"]
    u = r["urgenza"]
    righe = [f"SPIEGAZIONI DEL REGISTRO NFR — RISCHIO {rid} — ciclo {dati['ciclo']} ({_stato(dati)}).",
             f"Scritto da esegui_ciclo_locale.py il {oggi}: dati del registro, da non modificare a mano.", "",
             f"{rid} {r['nome']}",
             f"Categoria: {r['event_type']} {r.get('event_type_nome') or ('fuori perimetro' if r['event_type'] == 'FP' else '')}; driver: {r.get('driver') or '—'}; owner: {r.get('owner') or '—'}.",
             f"Esito nel ciclo: {r['esito']}. Posizione in classifica per score: {r.get('posizione_in_classifica')} su {len(dati['rischi'])}.",
             f"Attenzione del supervisore: {'si' if r.get('attenzione_supervisore') else 'no'}. Presidio dei controlli "
             f"(giudizio della Banca, fuori dallo score): {r.get('presidio_controlli')}.", "",
             "DESCRIZIONE", str(r.get("descrizione") or "—"), "",
             "IL RISCHIO (razionale di A1)", str(r.get("razionale_rischio") or "—"), "",
             "VALORI E SCORE",
             f"Impatto {_it(v.get('impatto'), 0)}, Probabilita {_it(v.get('probabilita'), 0)}, Prossimita "
             f"{_it(v.get('prossimita'), 0)}, Velocity {_it(v.get('velocity'), 0) if v.get('velocity') is not None else 'non valutata'}.",
             f"Score composito {_it(r.get('score'))} (ciclo precedente {_it(r.get('score_ciclo_precedente'))}); pesi: "
             + ", ".join(f"{schede.NOMI_DIM[d]} {_it(p)}" for d, p in (dati.get('pesi') or {}).items()) + ".", ""]
    mot = r.get("motivazioni") or {}
    righe.append("PERCHE' OGNI VALORE (motivazioni scritte da A1, con fatti e documenti)")
    if mot:
        for d in schede.DIMENSIONI + ["adeguamento"]:
            if mot.get(d):
                righe.append(f"{d.upper()}: {mot[d]}")
    else:
        righe.append("A1 non ha diviso il razionale per dimensione: vale il razionale qui sopra.")
    righe += ["", "URGENZA (disuguaglianza di Mosca: agire ora se X + Y > Z)",
              f"X {_it(u.get('x'))} + Y {_it(u.get('y'))} contro Z {_it(u.get('z'))}: margine {_it(u.get('margine'))} anni, "
              f"esito {u.get('esito') or '—'}. Anni di adeguamento strutturale: {_it(r.get('anni_adeguamento'))}.",
              f"Livello di allerta: {(r.get('livello_allerta') or {}).get('livello') or '—'} — motivo: "
              f"{(r.get('livello_allerta') or {}).get('motivo') or '—'}. Segnali netti delle notizie nelle ultime 4 settimane: "
              f"{_it(r.get('segnali_netti_4_settimane'), 0)}.", "", "COSA E' CAMBIATO", schede.cosa_cambiato(r), "",
              "FONTI (riferimento, data, tipo, rilevanza 1-3 per la previsione)"]
    for f in r.get("fonti") or []:
        righe.append(f"- {f.get('riferimento')} ({f.get('data')}, {f.get('tipo')}, rilevanza {f.get('rilevanza')})")
    righe += ["", "AZIONI"]
    for a in r.get("azioni") or []:
        righe.append(f"- {a['id_azione']} [{a.get('stato')}, {a.get('orizzonte')}, {a.get('owner')}]: {a.get('descrizione')}"
                     + (f" Perche': {a['razionale']}" if a.get("razionale") else "")
                     + (f" Effetto atteso: {a['effetto_atteso']}" if a.get("effetto_atteso") else ""))
    righe += ["", "KRI IN VIGORE"]
    for k in r.get("kri") or []:
        righe.append(f"- {k['kri_id']} ({k.get('tipo') or 'senza tipo'}) {k['nome']} [{k.get('unita')}]: valore {_it(k.get('valore'))} "
                     f"(prima {_it(k.get('valore_ciclo_precedente'))}), soglie {_it(k.get('soglia_attenzione'))} / "
                     f"{_it(k.get('soglia_allerta'))}, stato {k.get('stato')}; fonte dati {k.get('fonte_dati')}."
                     + (f" Perche': {k['razionale']}" if k.get("razionale") else ""))
    righe += ["", "STORIA (cicli, dal piu' vecchio)"]
    for s in r.get("storia") or []:
        righe.append(f"- {s['ciclo']}: Impatto {_it(s.get('impatto'), 0)}, Probabilita {_it(s.get('probabilita'), 0)}, "
                     f"Prossimita {_it(s.get('prossimita'), 0)}, Velocity {_it(s.get('velocity'), 0)}, score {_it(s.get('score'))}")
    righe += ["", "DECISIONI DEL VALIDATORE IN QUESTO CICLO"]
    decisioni = dati["decisioni"].get(rid) or []
    if decisioni:
        for d in decisioni:
            righe.append(f"- {d.get('Oggetto')} {d.get('ID')} {d.get('Campo')}: {d.get('Decisione')} (proposta "
                         f"{d.get('Proposta_Agente')!s}, deciso {d.get('Valore_Validato')!s}) da {d.get('Validato_Da')}: "
                         f"{d.get('Motivazione') or '—'}")
    else:
        righe.append("Nessuna rettifica ne' respingimento: le proposte di A1 sono state accettate"
                     if dati["validato"] else "Ciclo non ancora validato.")
    righe += ["", "SEGNALAZIONI DEI CONTROLLI E DI A5", str(dati["rilievi"].get(rid) or "Nessuna."), ""]
    return "\n".join(righe) + "\n"


def testo_ciclo(dati, oggi):
    righe = [f"SPIEGAZIONI DEL REGISTRO NFR — CICLO {dati['ciclo']} — {_stato(dati)}.",
             f"Scritto da esegui_ciclo_locale.py il {oggi}: dati del registro, da non modificare a mano.",
             f"Data di riferimento: {dati['data_riferimento']}; ciclo precedente: {dati['ciclo_precedente']}.", "",
             "RISCHI DEL CICLO, DAL PIU' ALTO PER SCORE (dettaglio nel file Rischio_nn.txt che ha il codice in testa)"]
    for r in dati["rischi"]:
        righe.append(f"{r.get('posizione_in_classifica')}. {r['id_rischio']} {r['nome']}: score {_it(r.get('score'))}, "
                     f"{(r.get('urgenza') or {}).get('esito') or '—'}, livello {(r.get('livello_allerta') or {}).get('livello') or '—'}, "
                     f"esito {r['esito']}")
    s = dati["sintesi"]
    righe += ["", "COMMENTO DI A1 PER IL COMITATO", str(s.get("Sintesi_A1") or "—"), "",
              "CONTROLLI", f"Sintesi di A5: {s.get('Sintesi_A5') or '—'}",
              f"Segnalazioni sul ciclo: {s.get('Rilievi_Ciclo') or 'nessuna'}",
              f"Segnalazioni da motivare: {s.get('Rilievi_Superati') or 'nessuna'}", "",
              "PARAMETRI DEL RADAR"]
    righe.append("Pesi dello score composito: " + ", ".join(f"{schede.NOMI_DIM[d]} {_it(p)}" for d, p in (dati.get('pesi') or {}).items())
                 + " (media pesata delle dimensioni valutate).")
    if dati["z_prossimita"]:
        righe.append("Z di Mosca per Prossimita 1..5 (anni prima che il rischio possa manifestarsi): "
                     + ", ".join(f"{i} -> {_it(z)}" for i, z in enumerate(dati["z_prossimita"], start=1)) + ".")
    for etichetta, valore in dati["parametri"]:
        righe.append(f"{etichetta}: {_it(valore)}")
    righe += ["", "FENOMENI CONSIDERATI DA A1 E NON CENSITI COME RISCHI"]
    if dati["scartati"]:
        for f in dati["scartati"]:
            fonti = "; ".join(f"{x.get('riferimento')} ({x.get('data')})" for x in f.get("fonti") or [])
            righe.append(f"- {f.get('fenomeno')} [{f.get('event_type') or '—'}]: {MOTIVI_SCARTO.get(f.get('motivo'), f.get('motivo'))}. "
                         f"{f.get('spiegazione') or ''} Fonti: {fonti or '—'}")
    else:
        righe.append("A1 non ne ha registrati in questo ciclo: per un fenomeno dei documenti assente dal registro, il "
                     "motivo va cercato nei documenti con i criteri della rubrica, dichiarando che e' una lettura nuova.")
    righe += ["", "LISTA DI OSSERVAZIONE (fenomeni con un meccanismo di perdita, oggi troppo lontani o poco plausibili per "
                  "essere rischi: valutazione preliminare, niente KRI, azioni ne' score; fuori da radar e classifica)"]
    voci = dati.get("osservazione") or []
    if voci:
        for v in voci:
            fonti = "; ".join(f"{x.get('riferimento')} ({x.get('data')})" for x in json.loads(v.get("Fonti") or "[]"))
            stato = v.get("Stato") or "—"
            if v.get("Promosso_A"):
                stato += f" a {v['Promosso_A']}"
            righe.append(f"- {v['OSS_ID']} {v.get('Nome')} [{v.get('Event_Type') or '—'}; driver {v.get('Driver') or '—'}; "
                         f"rischi toccati {v.get('Rischi_Toccati') or 'nessuno'}]: stato {stato}, esito del ciclo "
                         f"{v.get('Esito')}, in osservazione dal {v.get('Prima_Osservazione') or '—'}. Impatto potenziale "
                         f"{v.get('Impatto_Potenziale')} ({IMPATTO.get(v.get('Impatto_Potenziale'), '—')}), "
                         f"orizzonte {v.get('Orizzonte_Anni')} anni, plausibilita' {v.get('Plausibilita')}. "
                         f"Meccanismo: {v.get('Descrizione')} Segnale che lo farebbe diventare un rischio: "
                         f"{v.get('Segnale_Avvicinamento')} Motivazione di A1 (REGISTRATO): {v.get('Motivazione')} "
                         f"Fonti: {fonti or '—'}. Validazione: {v.get('Validazione') or "invariata, gia' validata"}.")
            a3 = (dati.get("a3_osservazione") or {}).get(str(v["OSS_ID"])) or {}
            for n in a3.get("notizie_a3") or []:
                righe.append(f"  notizia collegata da A3 dopo il ciclo: {n['id_notizia']} {n['titolo']} ({n['data']}, {n['segnale']})")
            for x in a3.get("segnali_a3") or []:
                righe.append(f"  segnale di A3 della settimana del {x['settimana']}: {x['segnale']}")
            for d in (dati.get("decisioni_osservazione") or {}).get(str(v["OSS_ID"]), []):
                righe.append(f"  decisione del validatore su {d.get('Campo')}: {d.get('Decisione')}, proposta di A1 "
                             f"{d.get('Proposta_Agente')}, valore deciso {d.get('Valore_Validato') if d.get('Valore_Validato') is not None else '—'}; "
                             f"motivazione: {d.get('Motivazione') or '—'}")
    else:
        righe.append("Nessuna voce in questo ciclo.")
    righe += ["", "RISCHI DISMESSI (usciti dal registro)"]
    if dati["dismessi"]:
        for d in dati["dismessi"]:
            righe.append(f"- {d.get('rischio')} {d.get('nome')}: dismesso il {d.get('data')} da {d.get('decisore')}. Motivo: {d.get('motivazione')}")
    else:
        righe.append("Nessuno.")
    righe += ["", "NOTE DELL'ANALISTA (prima pagina del report)", str(dati.get("nota_quadro") or "Nessuna nota per il ciclo corrente.")]
    for c, n in dati["note_passate"]:
        righe.append(f"- note del ciclo {c}: {n}")
    return "\n".join(righe) + "\n"


def file_per_posto(dati):
    """{nome del file: rischio o None}: un posto per ogni riga dell'anagrafica, i rischi in ordine di codice."""
    rischi = sorted(dati["rischi"], key=lambda r: r["id_rischio"])
    posti = max(dati.get("posti") or 0, len(rischi))
    return {f"Rischio_{k:02d}.txt": (rischi[k - 1] if k <= len(rischi) else None) for k in range(1, posti + 1)}


def testo_posto_libero(nome, dati, oggi):
    return (f"SPIEGAZIONI DEL REGISTRO NFR — {nome[:-4].replace('_', ' ')} — ciclo {dati['ciclo']}: POSTO LIBERO, nessun "
            f"rischio in questo posto dell'anagrafica.\nScritto da esegui_ciclo_locale.py il {oggi}.\n")


def scrivi(cartella, dati, oggi):
    """Scrive Ciclo.txt e un Rischio_nn.txt per ogni posto dell'anagrafica (sempre gli stessi nomi); toglie i file dei
    nomi di prima del 07/10 (NFR-nn.txt) e i posti oltre la capienza. Non tocca altri file."""
    cartella = Path(cartella)
    cartella.mkdir(parents=True, exist_ok=True)
    (cartella / "Ciclo.txt").write_text(testo_ciclo(dati, oggi), encoding="utf-8")
    posti = file_per_posto(dati)
    for nome, r in posti.items():
        testo = testo_rischio(r, dati, oggi) if r else testo_posto_libero(nome, dati, oggi)
        (cartella / nome).write_text(testo, encoding="utf-8")
    for f in [*cartella.glob("NFR-*.txt"), *cartella.glob("Rischio_*.txt")]:
        if f.name not in posti:
            f.unlink()
    return ["Ciclo.txt", *posti]
