"""Stato del processo e prossimo passo, senza Excel (D-83, tappa M2; TODO AU2).

L'app NFR mostra in testa a che punto e' il lavoro e propone il prossimo passo. Lo stato si legge solo dall'archivio
condiviso (Archivio_Cicli, News_Inbox), che OneDrive porta su tutti i PC: piu' analisti vedono lo stesso stato e uno
puo' riprendere il lavoro di un altro. Il registro non si apre: i comandi del motore lasciano nell'archivio tutto
cio' che serve.

  - Baseline_corrente.json: il ciclo corrente (ciclo_precedente: l'ultimo scritto), il periodo da valutare, lo
    straordinario deciso;
  - Cicli/<ciclo>/: Validazione_<ciclo>.json (validato), Riapertura_<ciclo>.json (riapertura aperta),
    Schede_<ciclo>.xlsx, Report_comitato_<ciclo>.pdf, Straordinario_<periodo>.json;
  - Settimane/<lunedi'>/: la settimana scritta (A3_<lunedi'>.json) e validata (Validazione_<lunedi'>.json);
  - News_Inbox/<lunedi'>/Raccolta_*.txt: la raccolta della settimana;
  - In_arrivo/: le risposte degli agenti gia' copiate (ingresso.py);
  - _Lucchetto/: chi sta scrivendo (lucchetto.py);
  - Stato/<periodo>.json: i passi che non lasciano file (per esempio "A1 richiesto da X alle 10:12"), scritti dall'app.

Le attivita' sono in ordine di priorita': il primo e' il prossimo passo. Solo libreria standard.
"""

import datetime as dt
import json
from pathlib import Path

import ingresso
import lucchetto

CARTELLA_STATO = "Stato"


def _json(percorso):
    try:
        return json.loads(Path(percorso).read_text(encoding="utf-8-sig"))
    except (OSError, ValueError):
        return None


def fine_trimestre(ciclo):
    anno, q = int(ciclo[:4]), int(ciclo[5])
    mese = 3 * q
    return dt.date(anno + (mese == 12), mese % 12 + 1, 1) - dt.timedelta(days=1)


def lunedi(giorno):
    return giorno - dt.timedelta(days=giorno.weekday())


def segna(cartella_uscita, periodo, passo, utente=None, nota=None):
    """Annota un passo dell'app che non lascia file (es. 'A1 richiesto'): chi e quando."""
    cartella = Path(cartella_uscita) / CARTELLA_STATO
    cartella.mkdir(parents=True, exist_ok=True)
    percorso = cartella / f"{periodo}.json"
    dati = _json(percorso) or {"periodo": periodo, "passi": {}}
    dati["passi"][passo] = {"da": lucchetto.chi_sono(utente)["utente"],
                            "il": dt.datetime.now().replace(microsecond=0).isoformat(), **({"nota": nota} if nota else {})}
    percorso.write_text(json.dumps(dati, ensure_ascii=False, indent=2), encoding="utf-8")
    return dati


def passi_segnati(cartella_uscita, periodo):
    return (_json(Path(cartella_uscita) / CARTELLA_STATO / f"{periodo}.json") or {}).get("passi", {})


def _attivita(chiave, titolo, chi, perche):
    return {"chiave": chiave, "titolo": titolo, "chi": chi, "perche": perche}


def leggi(conf, oggi=None):
    """Lo stato del processo: dict con i fatti, le righe da mostrare e le attivita' (la prima e' il prossimo passo).
    conf: le chiavi di esegui_ciclo_locale.configurazione() (cartella_uscita, news_inbox, utente)."""
    oggi = oggi or dt.date.today()
    uscita = Path(conf["cartella_uscita"])
    base = _json(uscita / "Baseline_corrente.json") or {}
    corrente = base.get("ciclo_precedente")
    da_valutare = base.get("ciclo_da_valutare")
    cicli = uscita / "Cicli"
    in_arrivo = {f.name: f for f in (uscita / ingresso.CARTELLA).glob("*.json")}

    s = {"oggi": oggi.isoformat(), "lucchetto": lucchetto.stato(uscita), "baseline": bool(base),
         "ciclo_corrente": corrente, "da_valutare": da_valutare, "in_arrivo": sorted(in_arrivo)}
    io = lucchetto.chi_sono(conf.get("utente"))
    altrui = s["lucchetto"] if s["lucchetto"] and (s["lucchetto"].get("utente"), s["lucchetto"].get("pc")) != (io["utente"], io["pc"]) else None

    # ciclo corrente: validato, riaperto, schede, report
    validazione = cicli / str(corrente) / f"Validazione_{corrente}.json" if corrente else None
    s["validato"] = bool(validazione and validazione.exists())
    s["riapertura"] = _json(cicli / str(corrente) / f"Riapertura_{corrente}.json") if corrente else None
    s["schede"] = bool(corrente and (cicli / str(corrente) / f"Schede_{corrente}.xlsx").exists())
    report = cicli / str(corrente) / f"Report_comitato_{corrente}.pdf" if corrente else None
    s["report"] = bool(report and report.exists() and s["validato"] and report.stat().st_mtime >= validazione.stat().st_mtime)
    # tappa M4: l'HTML esce con il PDF se il cancello lo lascia passare; senza, il report c'e' lo stesso (il PDF)
    html = report.with_suffix(".html") if report else None
    s["report_html"] = bool(s["report"] and html.exists() and html.stat().st_mtime >= validazione.stat().st_mtime)

    # straordinario deciso e non ancora scritto: la baseline lo porta come periodo da valutare
    s["straordinario"] = base.get("straordinario") if da_valutare and "-S" in str(da_valutare) else None

    # settimana
    lun = lunedi(oggi).isoformat()
    news = Path(conf.get("news_inbox") or uscita.parent / "News_Inbox")
    s["settimana"] = {"lunedi": lun,
                      "raccolta": any((news / lun).glob("Raccolta_*.txt")),
                      "a3": f"A3_{lun}.json" in in_arrivo,
                      "scritta": (uscita / "Settimane" / lun / f"A3_{lun}.json").exists(),
                      "validata": (uscita / "Settimane" / lun / f"Validazione_{lun}.json").exists()}

    # attivita', in ordine di priorita'
    att = []
    if altrui:
        att.append(_attivita("attesa", f"Attendere: {lucchetto.descrivi(altrui)}", "analista",
                             "un collega sta scrivendo nel registro"))
    if not base:
        att.append(_attivita("baseline", "Preparare la baseline (comando baseline)", "analista",
                             "nell'archivio non c'e' ancora Baseline_corrente.json"))
    elif corrente and s["riapertura"]:
        att.append(_attivita("validazione", f"Validare la riapertura del ciclo {corrente}", "validatore",
                             f"riaperta da {s['riapertura'].get('riaperta_da', '?')} il "
                             f"{str(s['riapertura'].get('riaperta_il', '?')).replace('T', ' ')}"))
    elif corrente and not s["validato"]:
        att.append(_attivita("validazione", f"Validare il ciclo {corrente}", "validatore",
                             "il ciclo e' scritto; il ciclo dopo non parte finche' non e' validato"))
    if s["straordinario"]:
        pronto = f"A8_{da_valutare}.json" in in_arrivo
        att.append(_attivita("straordinario", f"Ciclo straordinario {da_valutare}: "
                             + ("scrivere l'output di A8" if pronto else "A8 con i documenti dell'evento"), "analista",
                             f"deciso da {s['straordinario'].get('decisore', '?')}"))
    elif da_valutare and base and oggi > fine_trimestre(str(da_valutare)[:6]) and s["validato"] and not s["riapertura"]:
        pronto = f"A1_{da_valutare}.json" in in_arrivo
        att.append(_attivita("trimestrale", f"Ciclo trimestrale {da_valutare}: "
                             + ("scrivere l'output di A1" if pronto else "A1"), "analista",
                             f"il trimestre {str(da_valutare)[:6]} e' chiuso il {fine_trimestre(str(da_valutare)[:6]):%d/%m/%Y}"))
    if corrente and s["validato"] and not s["riapertura"]:
        if not s["report"]:
            att.append(_attivita("report", f"Report al comitato del ciclo {corrente}", "analista",
                                 "manca il PDF del ciclo validato"))
        if not s["schede"]:
            att.append(_attivita("schede", f"Schede dei rischi del ciclo {corrente}", "analista",
                                 "il ciclo e' validato e le schede non ci sono"))
    w = s["settimana"]
    if not w["scritta"]:
        passo = ("raccolta delle notizie" if not w["raccolta"] else "scrivere l'output di A3" if w["a3"] else "A3")
        att.append(_attivita("settimanale", f"Settimana del {dt.date.fromisoformat(lun):%d/%m}: {passo}", "analista",
                             "aggiornamento settimanale"))
    elif not w["validata"]:
        att.append(_attivita("valida_settimana", f"Validare le notizie della settimana del {dt.date.fromisoformat(lun):%d/%m} "
                             "(facoltativo)", "validatore", "consigliato"))
    s["attivita"] = att
    s["prossimo"] = att[0] if att else _attivita("niente", "Niente da fare adesso", "—", "prossimo passo: lunedi'")
    s["righe"] = righe(s)
    return s


def righe(s):
    """Le righe dello stato in testa alla finestra."""
    out = []
    if s["ciclo_corrente"]:
        fase = ("RIAPERTO, da validare" if s["riapertura"] else "VALIDATO" if s["validato"] else "scritto, DA VALIDARE")
        extra = ([] if not s["validato"] or s["riapertura"] else
                 ["report " + (("pronto, PDF e HTML" if s.get("report_html") else "pronto, solo PDF (HTML: vedere il log)")
                               if s["report"] else "da fare"), "schede " + ("pronte" if s["schede"] else "da fare")])
        out.append(f"Ciclo {s['ciclo_corrente']}: " + ", ".join([fase] + extra))
    if s["da_valutare"]:
        out.append(f"Prossimo periodo: {s['da_valutare']}" + (" (straordinario deciso)" if s["straordinario"] else ""))
    w = s["settimana"]
    fasi = ("validata" if w["validata"] else "scritta" if w["scritta"] else "A3 copiato" if w["a3"]
            else "raccolta fatta, A3 da fare" if w["raccolta"] else "raccolta da fare")
    out.append(f"Settimana del {dt.date.fromisoformat(w['lunedi']):%d/%m/%Y}: {fasi}")
    out.append("Registro: " + (f"in uso da {lucchetto.descrivi(s['lucchetto'])}" if s["lucchetto"] else "libero"))
    return out
