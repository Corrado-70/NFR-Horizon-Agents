"""Funzioni amministrative dell'archivio e del registro (D-83, tappa M5; D-85, proposta). Solo per il manutentore.

Regola di fondo: NIENTE SI CANCELLA SUBITO. Cio' che un'operazione toglie va in un parcheggio,
Archivio_Cicli/_Parcheggio/<data_ora>_<operazione>/, con un atto (atto.json: chi, quando, perche', chi ha deciso,
ogni file con la sua impronta) e una traccia in Archivio_Cicli/Amministrazione/. Ogni operazione si puo' annullare
rimettendo a posto il parcheggio; un parcheggio si svuota solo con 'svuota', dopo un tempo minimo.

Comandi:
  parcheggi                      elenca i parcheggi (operazione, quando, chi, quanto, stato)
  pulizia [--esegui]             anteprima (senza --esegui) o spostamento nel parcheggio di: tentativi dei cicli
                                 validati, backup oltre gli ultimi N, versioni precedenti dei report, In_arrivo
                                 (Originali, Precedenti) dei periodi chiusi, log e verifiche del PC vecchi
  ritorno --ciclo C --motivo --decisore --conferma C
                                 il registro torna quello validato del ciclo C (Cicli/C/<registro>_C_validato.xlsx);
                                 nel parcheggio il registro di adesso, i periodi dopo C, la baseline, gli allegati e la
                                 knowledge di A7, che poi si rigenerano (baseline)
  annulla --parcheggio NOME --motivo
                                 rimette a posto un parcheggio; per un ritorno o una ripartenza solo se nel frattempo
                                 nessuno ha scritto nel registro (impronta uguale a quella lasciata dall'operazione)
  ripartenza --motivo --decisore --conferma <nome del registro> --ciclo-precedente AAAAQn [--settimana AAAA-MM-GG]
                                 registro nuovo vuoto (inizializza) e baseline; il vecchio registro e l'archivio dei
                                 cicli nel parcheggio (per esempio dopo i cicli di prova)
  svuota [--esegui]              cancella per sempre i parcheggi piu' vecchi di giorni_parcheggio (anteprima senza
                                 --esegui); l'elenco di cio' che si cancella resta nella traccia

Chi: solo con "ruolo": "manutentore" in configurazione.json (D-85, proposta). Ogni operazione che scrive prende il
lucchetto del registro. Configurazione (facoltativa): backup_da_tenere (10), giorni_log (90), giorni_parcheggio (30).

Uso: python amministrazione.py [--workbook F --kernel C --cartella-uscita C] <comando> [opzioni]
"""

import argparse
import datetime as dt
import json
import os
import re
import shutil
import sys
from pathlib import Path

import lucchetto

QUI = Path(__file__).resolve().parent
PARCHEGGIO = "_Parcheggio"
TRACCIA = "Amministrazione"
ESCLUSE = {PARCHEGGIO, TRACCIA, lucchetto.CARTELLA}      # mai spostate: servono alle operazioni stesse
PREDEFINITI = {"backup_da_tenere": 10, "giorni_log": 90, "giorni_parcheggio": 30}
PERIODO = re.compile(r"\d{4}Q[1-4](?:-S[1-9])?")
LUNEDI = re.compile(r"\d{4}-\d{2}-\d{2}")
MOTIVO_MINIMO = 20


class Fermo(Exception):
    """L'operazione non si fa: niente e' stato toccato."""


# ------------------------------------------------------------ configurazione e permessi
def impostazioni(conf_grezza):
    return {k: int(conf_grezza.get(k, v)) for k, v in PREDEFINITI.items()}


def autorizzato(conf_grezza):
    return str(conf_grezza.get("ruolo") or "").strip().lower() == "manutentore"


def controlla_ruolo(conf_grezza):
    if not autorizzato(conf_grezza):
        raise Fermo("Le funzioni amministrative sono del manutentore (D-85): su questo PC configurazione.json non ha "
                    "\"ruolo\": \"manutentore\". Chiedere a chi mantiene il pacchetto.")


def controlla_motivo(motivo, decisore=None, minimo=MOTIVO_MINIMO):
    if len(str(motivo or "").strip()) < minimo:
        raise Fermo(f"--motivo obbligatorio, almeno {minimo} caratteri: resta nell'atto.")
    if decisore is not None and not str(decisore).strip():
        raise Fermo("--decisore obbligatorio: chi ha deciso l'operazione resta nell'atto.")


# ------------------------------------------------------------ file e impronte
def impronta(percorso):
    import hashlib
    h = hashlib.sha256()
    with open(percorso, "rb") as f:
        for blocco in iter(lambda: f.read(1 << 20), b""):
            h.update(blocco)
    return h.hexdigest()[:16]


def dimensione(percorso):
    p = Path(percorso)
    if p.is_file():
        return p.stat().st_size
    return sum(f.stat().st_size for f in p.rglob("*") if f.is_file())


def leggibile(n):
    for unita in ("byte", "KB", "MB", "GB"):
        if n < 1024 or unita == "GB":
            return f"{n:.0f} {unita}" if unita == "byte" else f"{n:.1f} {unita}".replace(".", ",")
        n /= 1024


def radici(conf):
    """Le cartelle da cui un'operazione puo' spostare: l'archivio, la cartella del registro, quella della knowledge di
    A7. Un elemento del parcheggio si ricorda come (radice, percorso relativo)."""
    from esegui_ciclo_locale import cartella_spiegazioni
    return {"archivio": Path(conf["cartella_uscita"]).resolve(), "registro": Path(conf["workbook"]).parent.resolve(),
            "spiegazioni": Path(cartella_spiegazioni(conf)).parent.resolve()}


def relativo(percorso, conf):
    percorso = Path(percorso).resolve()
    for nome, radice in radici(conf).items():
        try:
            return nome, percorso.relative_to(radice).as_posix()
        except ValueError:
            continue
    raise Fermo(f"{percorso} non e' ne' nell'archivio ne' accanto al registro: non si sposta")


# ------------------------------------------------------------ parcheggio, atto, traccia
def chi(conf_grezza):
    io = lucchetto.chi_sono(conf_grezza.get("utente"))
    return {"utente": io["utente"], "pc": io["pc"]}


def parcheggia(conf, conf_grezza, operazione, elementi, motivo, decisore=None, extra=None, adesso=None):
    """Sposta 'elementi' (file o cartelle) in un parcheggio nuovo e scrive l'atto. Restituisce (cartella, atto)."""
    adesso = adesso or dt.datetime.now()
    uscita = Path(conf["cartella_uscita"])
    cartella = uscita / PARCHEGGIO / f"{adesso:%Y%m%d_%H%M%S}_{operazione}"
    n = 2
    while cartella.exists():
        cartella = cartella.with_name(f"{adesso:%Y%m%d_%H%M%S}_{operazione}_{n}")
        n += 1
    voci = []
    for e in senza_doppioni(elementi):
        if not e.exists():
            continue
        radice, rel = relativo(e, conf)
        voci.append({"radice": radice, "percorso": rel, "cartella": e.is_dir(), "dimensione": dimensione(e),
                     "impronta": None if e.is_dir() else impronta(e)})
    atto = {"operazione": operazione, "quando": adesso.replace(microsecond=0).isoformat(), **chi(conf_grezza),
            "motivo": motivo, "decisore": decisore, "stato": "attivo", "elementi": voci, **(extra or {})}
    cartella.mkdir(parents=True)
    _scrivi(cartella / "atto.json", atto)            # prima l'atto: se uno spostamento si interrompe, si sa cosa c'era
    for v in voci:
        origine = radici(conf)[v["radice"]] / v["percorso"]
        dest = cartella / v["radice"] / v["percorso"]
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(origine), str(dest))
    traccia(conf, atto, cartella)
    return cartella, atto


def senza_doppioni(elementi):
    """Una volta sola, e niente che stia dentro una cartella gia' nell'elenco (si sposta con lei)."""
    unici = list(dict.fromkeys(Path(e).resolve() for e in elementi))
    return [e for e in unici if not any(a != e and a in e.parents for a in unici)]


def traccia(conf, atto, cartella=None, nome=None):
    c = Path(conf["cartella_uscita"]) / TRACCIA
    c.mkdir(parents=True, exist_ok=True)
    nome = nome or f"{dt.datetime.now():%Y%m%d_%H%M%S}_{atto['operazione']}.json"
    _scrivi(c / nome, {**atto, "parcheggio": cartella.name if cartella else None})
    return c / nome


def _scrivi(percorso, dati):
    Path(percorso).write_text(json.dumps(dati, ensure_ascii=False, indent=2), encoding="utf-8")


def elenco_parcheggi(conf):
    base = Path(conf["cartella_uscita"]) / PARCHEGGIO
    out = []
    for c in sorted(base.iterdir()) if base.is_dir() else []:
        try:
            atto = json.loads((c / "atto.json").read_text(encoding="utf-8"))
        except (OSError, ValueError):
            atto = {"operazione": "?", "stato": "senza atto"}
        out.append((c, atto))
    return out


# ------------------------------------------------------------ pulizia
def periodo_chiuso(nome, uscita, oggi):
    """Un file dell'archivio e' di un periodo chiuso se il nome cita un ciclo validato o una settimana prima di questa
    che e' stata scritta. None se il nome non cita un periodo."""
    m = PERIODO.search(nome)
    if m:
        return (Path(uscita) / "Cicli" / m.group(0) / f"Validazione_{m.group(0)}.json").exists()
    m = LUNEDI.search(nome)
    if m:
        try:
            giorno = dt.date.fromisoformat(m.group(0))
        except ValueError:
            return None
        lunedi = oggi - dt.timedelta(days=oggi.weekday())
        return giorno < lunedi and (Path(uscita) / "Settimane" / m.group(0)).exists()
    return None


def da_pulire(conf, conf_grezza, oggi=None, adesso=None):
    """L'anteprima della pulizia: [(percorso, perche')]. Solo selezione, niente si sposta."""
    oggi = oggi or dt.date.today()
    adesso = adesso or dt.datetime.now()
    imp = impostazioni(conf_grezza)
    u = Path(conf["cartella_uscita"])
    scelti = []
    for c in sorted((u / "Cicli").glob("*")) if (u / "Cicli").is_dir() else []:
        if c.is_dir() and (c / f"Validazione_{c.name}.json").exists():
            scelti += [(t, f"tentativo del ciclo validato {c.name}") for t in sorted(c.glob("tentativo_*")) if t.is_dir()]
            scelti += [(f, f"versione precedente del report del ciclo {c.name}")
                       for f in sorted(c.glob(f"Report_comitato_{c.name}_*")) if f.is_file()]
    backup = sorted((f for f in (u / "Backup").glob("*") if f.is_file()), key=lambda f: f.stat().st_mtime, reverse=True) \
        if (u / "Backup").is_dir() else []
    scelti += [(f, f"backup oltre gli ultimi {imp['backup_da_tenere']}") for f in backup[imp["backup_da_tenere"]:]]
    limite = adesso - dt.timedelta(days=imp["giorni_log"])
    for sotto in ("Originali", "Precedenti"):
        for f in sorted((u / "In_arrivo" / sotto).glob("*")) if (u / "In_arrivo" / sotto).is_dir() else []:
            chiuso = periodo_chiuso(f.name, u, oggi)
            vecchio = dt.datetime.fromtimestamp(f.stat().st_mtime) < limite
            if f.is_file() and (chiuso or (chiuso is None and vecchio)):
                scelti.append((f, f"In_arrivo\\{sotto} di un periodo chiuso" if chiuso else f"In_arrivo\\{sotto} piu' vecchio "
                               f"di {imp['giorni_log']} giorni"))
    for cartella, cosa in (("Log", "log"), ("Verifiche_PC", "verifica del PC")):
        for f in sorted((u / cartella).glob("*")) if (u / cartella).is_dir() else []:
            if f.is_file() and dt.datetime.fromtimestamp(f.stat().st_mtime) < limite:
                scelti.append((f, f"{cosa} piu' vecchio di {imp['giorni_log']} giorni"))
    return scelti


def testo_anteprima(scelti, titolo):
    if not scelti:
        return f"{titolo}: niente da spostare."
    righe = [f"{titolo}: {len(scelti)} elementi, {leggibile(sum(dimensione(p) for p, _ in scelti))}"]
    gruppi = {}
    for p, perche in scelti:
        gruppi.setdefault(perche, []).append(p)
    for perche, elenco in gruppi.items():
        righe.append(f"  {perche}: {len(elenco)} ({leggibile(sum(dimensione(p) for p in elenco))})")
        righe += [f"    {p.name}" for p in elenco[:5]] + ([f"    ... e altri {len(elenco) - 5}"] if len(elenco) > 5 else [])
    return "\n".join(righe)


# ------------------------------------------------------------ ritorno indietro
def file_validato(conf, ciclo):
    return Path(conf["cartella_uscita"]) / "Cicli" / ciclo / f"{Path(conf['workbook']).stem}_{ciclo}_validato{Path(conf['workbook']).suffix}"


def da_spostare_nel_ritorno(conf, ciclo):
    """(elementi, settimane) del ritorno al ciclo C: registro di adesso, cartelle dei periodi dopo C (cicli e
    straordinari) e delle settimane scritte dopo la validazione di C, baseline, allegati, knowledge di A7 e le
    risposte in In_arrivo dei periodi spostati. Le settimane si restituiscono anche a parte (per riscriverle)."""
    from esegui_ciclo_locale import cartella_spiegazioni
    u = Path(conf["cartella_uscita"])
    validazione = u / "Cicli" / ciclo / f"Validazione_{ciclo}.json"
    quando = validazione.stat().st_mtime
    dopo = [c for c in sorted((u / "Cicli").glob("*")) if c.is_dir() and PERIODO.fullmatch(c.name) and c.name > ciclo]
    # scritte o validate dopo la validazione di C: il registro validato di C non le contiene
    settimane = [s for s in sorted((u / "Settimane").glob("*")) if s.is_dir() and LUNEDI.fullmatch(s.name)
                 and any(f.stat().st_mtime > quando for f in s.iterdir() if f.is_file())] if (u / "Settimane").is_dir() else []
    spostati = {c.name for c in dopo} | {s.name for s in settimane}
    elementi = [Path(conf["workbook"])] + dopo + settimane
    elementi += [f for f in u.glob("Baseline_corrente.*")] + [f for f in u.glob("Input_A*") if f.is_file()]
    spieg = Path(cartella_spiegazioni(conf))
    if spieg.exists():
        elementi.append(spieg)
    elementi += [f for f in sorted((u / "In_arrivo").glob("*.json"))
                 if any(p in f.name for p in spostati)] if (u / "In_arrivo").is_dir() else []
    return [e for e in elementi if e.exists()], settimane


def controlli_ritorno(conf, ciclo, corrente, versione_di=None):
    """Prima di spostare qualcosa: C validato, con il suo Excel validato, prima del ciclo corrente, della stessa
    versione del template (versione_di: funzione percorso -> versione; None = non controllata)."""
    if not PERIODO.fullmatch(str(ciclo or "")):
        raise Fermo(f"--ciclo {ciclo!r}: un ciclo come 2026Q3 o 2026Q3-S1.")
    u = Path(conf["cartella_uscita"])
    if not (u / "Cicli" / ciclo / f"Validazione_{ciclo}.json").exists():
        raise Fermo(f"Il ciclo {ciclo} non e' validato (manca Cicli/{ciclo}/Validazione_{ciclo}.json): si torna solo a un "
                    "ciclo validato.")
    validato = file_validato(conf, ciclo)
    if not validato.exists():
        raise Fermo(f"Manca l'Excel validato del ciclo {ciclo} ({validato}): senza, non c'e' a che cosa tornare.")
    if not corrente or ciclo >= corrente:
        raise Fermo(f"Il ciclo {ciclo} non e' prima del ciclo corrente ({corrente}): niente da cui tornare indietro.")
    if versione_di:
        from esegui_ciclo_locale import VERSIONE_TEMPLATE
        v = versione_di(validato)
        if v != VERSIONE_TEMPLATE:
            raise Fermo(f"L'Excel validato del ciclo {ciclo} e' del template {v or 'precedente al 25/09/2026'}, lo script "
                        f"vuole {VERSIONE_TEMPLATE}: prima aggiornarlo su una copia (aggiorna-registro, guida 0-bis).")
    return validato


def ritorno(conf, conf_grezza, ciclo, motivo, decisore, corrente, rigenera=None, versione_di=None):
    """Il ritorno al ciclo validato C. rigenera(conf): baseline, allegati e knowledge di A7 dal registro tornato
    (None nel collaudo senza Excel). Restituisce (cartella del parcheggio, atto, settimane spostate)."""
    from esegui_ciclo_locale import aperto_qui
    controlla_motivo(motivo, decisore)
    validato = controlli_ritorno(conf, ciclo, corrente, versione_di)
    registro = Path(conf["workbook"])
    if registro.exists() and aperto_qui(registro):
        raise Fermo(f"{registro.name} e' aperto in Excel su questo PC: chiuderlo e rilanciare.")
    elementi, settimane = da_spostare_nel_ritorno(conf, ciclo)
    cartella, atto = parcheggia(conf, conf_grezza, "ritorno", elementi, motivo, decisore,
                                {"ciclo": ciclo, "dal_ciclo": corrente, "settimane": [s.name for s in settimane]})
    shutil.copy2(validato, registro)
    atto["impronta_registro_dopo"] = impronta(registro)
    _scrivi(cartella / "atto.json", atto)
    if rigenera:
        rigenera(conf)
    return cartella, atto, settimane


# ------------------------------------------------------------ annulla
def annulla(conf, conf_grezza, nome, motivo):
    """Rimette a posto il parcheggio 'nome'. Cio' che nel frattempo occupa i posti (il registro tornato, la baseline
    rigenerata...) va in un parcheggio nuovo, 'annullamento': nemmeno l'annullamento cancella."""
    controlla_motivo(motivo, minimo=10)
    cartella = Path(conf["cartella_uscita"]) / PARCHEGGIO / nome
    if not (cartella / "atto.json").exists():
        raise Fermo(f"Parcheggio {nome} non trovato (python amministrazione.py parcheggi per l'elenco).")
    atto = json.loads((cartella / "atto.json").read_text(encoding="utf-8"))
    if atto.get("stato") != "attivo":
        raise Fermo(f"Il parcheggio {nome} e' {atto.get('stato')}: niente da rimettere.")
    registro = Path(conf["workbook"])
    if atto.get("impronta_registro_dopo"):
        attuale = impronta(registro) if registro.exists() else None
        if attuale != atto["impronta_registro_dopo"]:
            raise Fermo(f"Dopo l'operazione {atto['operazione']} del {atto['quando']} qualcuno ha scritto nel registro: "
                        "annullarla perderebbe quel lavoro. Niente e' stato toccato.")
    from esegui_ciclo_locale import aperto_qui
    if registro.exists() and aperto_qui(registro):
        raise Fermo(f"{registro.name} e' aperto in Excel su questo PC: chiuderlo e rilanciare.")
    rad = radici(conf)
    occupati = [rad[v["radice"]] / v["percorso"] for v in atto["elementi"] if (rad[v["radice"]] / v["percorso"]).exists()]
    occupati += [p for p in atto.get("creati", []) if Path(p).exists()]
    nuovo = None
    if occupati:
        nuovo, _ = parcheggia(conf, conf_grezza, "annullamento", occupati, f"annullamento di {nome}: {motivo}")
    for v in atto["elementi"]:
        origine = cartella / v["radice"] / v["percorso"]
        dest = rad[v["radice"]] / v["percorso"]
        if origine.exists():
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(origine), str(dest))
    atto.update(stato="annullato", annullato_il=dt.datetime.now().replace(microsecond=0).isoformat(),
                annullato_da=chi(conf_grezza)["utente"], motivo_annullamento=motivo,
                parcheggio_annullamento=nuovo.name if nuovo else None)
    _scrivi(cartella / "atto.json", atto)
    traccia(conf, {**atto, "operazione": f"annulla_{atto['operazione']}"}, cartella)
    return atto, nuovo


# ------------------------------------------------------------ ripartenza da zero
def da_spostare_nella_ripartenza(conf):
    from esegui_ciclo_locale import cartella_spiegazioni
    u = Path(conf["cartella_uscita"])
    elementi = [Path(conf["workbook"])]
    tenuti = ESCLUSE | {"Log", "Verifiche_PC"}
    elementi += [f for f in sorted(u.iterdir()) if f.name not in tenuti] if u.is_dir() else []
    spieg = Path(cartella_spiegazioni(conf))
    if spieg.exists() and not str(spieg).startswith(str(u)):
        elementi.append(spieg)
    return [e for e in elementi if e.exists()]


def ripartenza(conf, conf_grezza, motivo, decisore, crea=None):
    """Il vecchio registro e l'archivio dei cicli nel parcheggio, poi crea(conf): registro nuovo (inizializza) e
    baseline (None nel collaudo senza Excel). Restituisce (cartella, atto)."""
    from esegui_ciclo_locale import aperto_qui
    controlla_motivo(motivo, decisore)
    registro = Path(conf["workbook"])
    if registro.exists() and aperto_qui(registro):
        raise Fermo(f"{registro.name} e' aperto in Excel su questo PC: chiuderlo e rilanciare.")
    cartella, atto = parcheggia(conf, conf_grezza, "ripartenza", da_spostare_nella_ripartenza(conf), motivo, decisore)
    if crea:
        crea(conf)
    if registro.exists():
        atto["impronta_registro_dopo"] = impronta(registro)
        atto["creati"] = [str(registro)]
        _scrivi(cartella / "atto.json", atto)
    return cartella, atto


# ------------------------------------------------------------ svuota
def da_svuotare(conf, conf_grezza, adesso=None):
    adesso = adesso or dt.datetime.now()
    giorni = impostazioni(conf_grezza)["giorni_parcheggio"]
    out = []
    for c, atto in elenco_parcheggi(conf):
        try:
            quando = dt.datetime.strptime(c.name[:15], "%Y%m%d_%H%M%S")
        except ValueError:
            continue
        if adesso - quando >= dt.timedelta(days=giorni):
            out.append((c, atto))
    return out


def svuota(conf, conf_grezza, motivo, adesso=None):
    scelti = da_svuotare(conf, conf_grezza, adesso)
    atto = {"operazione": "svuota", "quando": dt.datetime.now().replace(microsecond=0).isoformat(), **chi(conf_grezza),
            "motivo": motivo, "cancellati": [{"parcheggio": c.name, "operazione": a.get("operazione"),
                                              "del": a.get("quando"), "di": a.get("utente"), "dimensione": dimensione(c),
                                              "elementi": [v["percorso"] for v in a.get("elementi", [])]}
                                             for c, a in scelti]}
    traccia(conf, atto)                              # prima la traccia: l'elenco resta anche se la cancellazione si ferma
    for c, _ in scelti:
        shutil.rmtree(c)
    return atto


# ------------------------------------------------------------ riga di comando
def _conf(arg):
    """Le cartelle come per il motore (configurazione.json, o le opzioni comuni); ruolo e tempi da configurazione.json.
    NFR_RUOLO (variabile d'ambiente) vale solo per il collaudo, come NFR_ATTESA_LUCCHETTO."""
    from esegui_ciclo_locale import configurazione
    import installazione
    conf = configurazione(arg)
    grezza = installazione.carica_configurazione(QUI / "configurazione.json")
    if os.environ.get("NFR_RUOLO"):
        grezza = {**grezza, "ruolo": os.environ["NFR_RUOLO"]}
    return conf, grezza


def _ciclo_corrente(conf):
    base = conf["cartella_uscita"] / "Baseline_corrente.json"
    try:
        return json.loads(base.read_text(encoding="utf-8-sig")).get("ciclo_precedente")
    except (OSError, ValueError):
        return None


def _rigenera(conf):
    """Dopo un ritorno: baseline, allegati e knowledge di A7 dal registro tornato (comando baseline, con Excel)."""
    import esegui_ciclo_locale as motore
    motore.comando_baseline(argparse.Namespace(uscita=None, straordinario=False), conf)


def _versione(percorso):
    import esegui_ciclo_locale as motore
    from excel_com import SessioneExcel
    with SessioneExcel(percorso, sola_lettura=True) as s:
        return motore.versione_workbook(s)


def main(argv=None):
    p = argparse.ArgumentParser(description="Funzioni amministrative dell'archivio e del registro (solo manutentore)")
    p.add_argument("--workbook")
    p.add_argument("--kernel")
    p.add_argument("--cartella-uscita", dest="cartella_uscita")
    sub = p.add_subparsers(dest="comando", required=True)
    sub.add_parser("parcheggi")
    pu = sub.add_parser("pulizia")
    pu.add_argument("--esegui", action="store_true")
    rt = sub.add_parser("ritorno")
    rt.add_argument("--ciclo", required=True)
    rt.add_argument("--motivo", required=True)
    rt.add_argument("--decisore", required=True)
    rt.add_argument("--conferma", required=True, help="il nome del ciclo, scritto di nuovo")
    an = sub.add_parser("annulla")
    an.add_argument("--parcheggio", required=True)
    an.add_argument("--motivo", required=True)
    rp = sub.add_parser("ripartenza")
    rp.add_argument("--motivo", required=True)
    rp.add_argument("--decisore", required=True)
    rp.add_argument("--conferma", required=True, help="il nome del file del registro, scritto di nuovo")
    rp.add_argument("--ciclo-precedente", dest="ciclo_precedente", required=True)
    rp.add_argument("--settimana")
    sv = sub.add_parser("svuota")
    sv.add_argument("--esegui", action="store_true")
    arg = p.parse_args(argv)
    try:
        conf, grezza = _conf(arg)
        controlla_ruolo(grezza)
        return esegui(arg, conf, grezza)
    except (Fermo, lucchetto.Occupato) as ex:
        print(f"FERMATO — niente e' stato toccato.\n{ex}")
        return 1
    except Exception as ex:                          # noqa: BLE001 - riportato con il motivo, come il motore
        nome = type(ex).__name__
        if nome == "Fermo":                          # i fermi del motore (baseline, inizializza)
            print(f"FERMATO dopo lo spostamento nel parcheggio: {ex}\nL'operazione si annulla con: python "
                  "amministrazione.py annulla --parcheggio <nome> --motivo \"...\" (python amministrazione.py parcheggi).")
            return 1
        print(f"ERRORE TECNICO — {nome}: {ex}")
        return 2


def esegui(arg, conf, grezza):
    utente = grezza.get("utente")
    uscita = conf["cartella_uscita"]
    if arg.comando == "parcheggi":
        elenco = elenco_parcheggi(conf)
        if not elenco:
            print("Nessun parcheggio.")
        for c, a in elenco:
            print(f"{c.name}: {a.get('operazione')} del {a.get('quando')} di {a.get('utente')} ({a.get('stato')}), "
                  f"{len(a.get('elementi', []))} elementi, {leggibile(dimensione(c))}"
                  + (f"; motivo: {a['motivo']}" if a.get("motivo") else ""))
        return 0
    if arg.comando == "pulizia":
        scelti = da_pulire(conf, grezza)
        print(testo_anteprima(scelti, "Pulizia dell'archivio" + ("" if arg.esegui else " (anteprima)")))
        if arg.esegui and scelti:
            with lucchetto.preso(uscita, "pulizia", utente):
                cartella, _ = parcheggia(conf, grezza, "pulizia", [p for p, _ in scelti], "pulizia dell'archivio")
            print(f"Spostato nel parcheggio: {cartella}\nSi annulla con: python amministrazione.py annulla --parcheggio "
                  f"{cartella.name} --motivo \"...\"")
        elif scelti:
            print("Per spostarli nel parcheggio: python amministrazione.py pulizia --esegui")
        return 0
    if arg.comando == "ritorno":
        if arg.conferma.strip() != arg.ciclo.strip():
            raise Fermo(f"--conferma {arg.conferma!r} non e' il ciclo {arg.ciclo!r}: riscriverlo uguale per confermare.")
        corrente = _ciclo_corrente(conf)
        with lucchetto.preso(uscita, "ritorno", utente):
            cartella, atto, settimane = ritorno(conf, grezza, arg.ciclo.strip(), arg.motivo.strip(), arg.decisore.strip(),
                                                corrente, _rigenera, _versione)
        print(f"Registro tornato al ciclo {arg.ciclo} validato (era al {corrente}). Nel parcheggio {cartella.name}: "
              f"{len(atto['elementi'])} elementi (registro di prima, periodi dopo {arg.ciclo}, baseline, allegati, knowledge "
              f"di A7).\nSi annulla, finche' nessuno scrive nel registro, con: python amministrazione.py annulla "
              f"--parcheggio {cartella.name} --motivo \"...\"")
        for s in settimane:
            a3 = next(iter(sorted((cartella / "archivio" / "Settimane" / s.name).glob("A3_*.json"))), None)
            if a3:
                print(f"Settimana {s.name} uscita dal registro: per riscriverla  python esegui_ciclo_locale.py settimanale "
                      f"--payload \"{a3}\"")
        return 0
    if arg.comando == "annulla":
        with lucchetto.preso(uscita, "annulla", utente):
            atto, nuovo = annulla(conf, grezza, arg.parcheggio.strip(), arg.motivo.strip())
        print(f"Annullata l'operazione {atto['operazione']} del {atto['quando']}: file rimessi al loro posto."
              + (f"\nCio' che occupava i loro posti e' nel parcheggio {nuovo.name}." if nuovo else ""))
        return 0
    if arg.comando == "ripartenza":
        if arg.conferma.strip() != Path(conf["workbook"]).name:
            raise Fermo(f"--conferma {arg.conferma!r} non e' il nome del registro ({Path(conf['workbook']).name}): "
                        "riscriverlo uguale per confermare.")
        import esegui_ciclo_locale as motore
        oggi = dt.date.today()
        settimana = arg.settimana or (oggi - dt.timedelta(days=oggi.weekday())).isoformat()

        def crea(c):
            motore.comando_inizializza(argparse.Namespace(template=None, ciclo_precedente=arg.ciclo_precedente,
                                                          settimana=settimana), c)
            motore.comando_baseline(argparse.Namespace(uscita=None, straordinario=False), c)
        with lucchetto.preso(uscita, "ripartenza", utente):
            cartella, atto = ripartenza(conf, grezza, arg.motivo.strip(), arg.decisore.strip(), crea)
        print(f"Ripartenza da zero: il vecchio registro e l'archivio dei cicli sono nel parcheggio {cartella.name} "
              f"({len(atto['elementi'])} elementi). Si annulla, finche' nessuno scrive nel registro nuovo, con: python "
              f"amministrazione.py annulla --parcheggio {cartella.name} --motivo \"...\"")
        return 0
    if arg.comando == "svuota":
        scelti = da_svuotare(conf, grezza)
        giorni = impostazioni(grezza)["giorni_parcheggio"]
        if not scelti:
            print(f"Nessun parcheggio piu' vecchio di {giorni} giorni.")
            return 0
        print(f"Parcheggi piu' vecchi di {giorni} giorni: {len(scelti)}, {leggibile(sum(dimensione(c) for c, _ in scelti))}")
        for c, a in scelti:
            print(f"  {c.name}: {a.get('operazione')} di {a.get('utente')} ({a.get('stato')})")
        if not arg.esegui:
            print("Per cancellarli per sempre: python amministrazione.py svuota --esegui")
            return 0
        atto = svuota(conf, grezza, f"svuota: parcheggi piu' vecchi di {giorni} giorni")
        print(f"Cancellati {len(atto['cancellati'])} parcheggi; l'elenco resta in {TRACCIA}.")
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
