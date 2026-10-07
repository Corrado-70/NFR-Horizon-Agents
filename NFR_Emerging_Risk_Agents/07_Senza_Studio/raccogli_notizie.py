"""W0 della variante locale: raccolta deterministica delle notizie dai feed.

Legge le fonti con canale 'rss' da 01_Kernel/fonti.md, scarica i feed, tiene
le voci degli ultimi N giorni e scrive in News_Inbox (cartella SharePoint
sincronizzata) un file di testo per A3:

    News_Inbox/<lunedi'>/Raccolta_<AAAA-MM-GG>.txt
    News_Inbox/<lunedi'>/Manuali/          (qui gli analisti salvano a mano)
    News_Inbox/_visti.json                 link gia' raccolti, contro i doppioni

Nessun LLM: decide A3 cosa e' rilevante. Qui si filtra solo per data, per le
parole 'escludi' della fonte e per 'max_voci'. Il file e' .txt perche' Agent
Builder legge .txt ma non .md dalle library.

Uso:
  python raccogli_notizie.py [--giorni 7] [--anche-da-validare] [--oggi AAAA-MM-GG]
                             [--news-inbox CARTELLA] [--kernel CARTELLA]
Di default usa solo le fonti 'approvata': finche' l'elenco non e' validato,
per le prove serve --anche-da-validare.

Codice di uscita: 0 raccolta scritta (anche con fonti irraggiungibili, elencate
in testa al file); 2 errore tecnico (elenco fonti non valido, cartella assente).

Rete: urllib della libreria standard per lo scaricamento; il proxy pero' non e'
sempre un indirizzo fisso nel registro di Windows, spesso e' un file di
autoconfigurazione (PAC) che il browser sa leggere da solo e urllib no (visto
in collaudo: i domini europa.eu, instradati dal PAC sul proxy, andavano in
timeout da script pur aprendosi nel browser). Percio' il pacchetto **pypac**
(vedi README_variante_locale.md, "Setup dello script"): scopre il PAC di
sistema una sola volta e instrada ogni fonte come farebbe il browser; se non
c'e' nessun PAC configurato si comporta come prima (proxy di sistema o diretto).
Pianificazione: Utilita' di pianificazione di Windows, ogni lunedi' prima di A3
(o ogni giorno: i doppioni sono scartati).
"""

import argparse
import datetime as dt
import html
import json
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime
from pathlib import Path

from pypac import get_pac, pac_context_for_url

QUI = Path(__file__).resolve().parent
sys.path.insert(0, str(QUI))

from fonti import leggi_fonti          # noqa: E402

LUNGHEZZA_ESTRATTO = 400
TIMEOUT = 30
_pac_scoperto = {}          # cache: scoprire il PAC (interrogazione di rete) una sola volta, non per ogni fonte


# ================================================================ feed -> voci
def _locale(tag):
    return tag.rsplit("}", 1)[-1]


def _testo(x):
    """Testo semplice da un frammento che puo' contenere HTML."""
    t = re.sub(r"<[^>]+>", " ", html.unescape(x or ""))
    return re.sub(r"\s+", " ", t).strip()


def _data(valore):
    """Data di una voce (RFC 822 degli RSS o ISO 8601 degli Atom) -> date, o None."""
    if not valore:
        return None
    valore = valore.strip()
    try:
        return parsedate_to_datetime(valore).date()
    except (TypeError, ValueError, IndexError):
        pass
    try:
        return dt.datetime.fromisoformat(valore.replace("Z", "+00:00")).date()
    except ValueError:
        return None


def analizza_feed(dati):
    """Byte di un feed RSS 2.0, RSS 1.0 o Atom -> [{titolo, link, data, estratto}]."""
    radice = ET.fromstring(dati)
    voci = []
    for el in radice.iter():
        if _locale(el.tag) not in ("item", "entry"):
            continue
        v = {"titolo": "", "link": "", "data": None, "estratto": ""}
        for c in el:
            nome = _locale(c.tag)
            if nome == "title":
                v["titolo"] = _testo(c.text)
            elif nome == "link":
                href = c.get("href")
                if href and c.get("rel", "alternate") == "alternate":
                    v["link"] = href.strip()
                elif not href and c.text:
                    v["link"] = c.text.strip()
            elif nome in ("pubDate", "published", "updated", "date") and v["data"] is None:
                v["data"] = _data(c.text)
            elif nome in ("description", "summary", "content") and not v["estratto"]:
                v["estratto"] = _testo(c.text)[:LUNGHEZZA_ESTRATTO]
        if not v["link"] and el.get("{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about"):
            v["link"] = el.get("{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about")
        if v["titolo"] or v["link"]:
            voci.append(v)
    return voci


def seleziona(voci, fonte, oggi, giorni, visti):
    """Voci da tenere per una fonte. Regole, nell'ordine:
    - una voce senza data prende la data di oggi e lo dice (alcuni feed non la danno);
    - fuori dalla finestra [oggi-giorni, oggi]: scartata;
    - titolo con una parola di 'escludi': scartata;
    - link gia' raccolto in un giorno diverso da oggi: scartata (doppione);
    - al massimo 'max_voci', le piu' recenti."""
    tenute = []
    inizio = oggi - dt.timedelta(days=giorni)
    for v in voci:
        v = dict(v, senza_data=v["data"] is None)
        if v["senza_data"]:
            v["data"] = oggi
        if not inizio <= v["data"] <= oggi:
            continue
        if any(p in v["titolo"].lower() for p in fonte["escludi"]):
            continue
        chiave = v["link"] or v["titolo"]
        if chiave in visti and visti[chiave] != oggi.isoformat():
            continue
        tenute.append(v)
    tenute.sort(key=lambda v: v["data"], reverse=True)
    return tenute[:fonte["max_voci"]]


def pac_di_sistema():
    """PAC di sistema, scoperto una sola volta (WPAD/registro): None se non
    ce n'e' uno, nel qual caso scarica() si comporta come senza pypac."""
    if "valore" not in _pac_scoperto:
        _pac_scoperto["valore"] = get_pac()
    return _pac_scoperto["valore"]


def scarica(indirizzo):
    req = urllib.request.Request(indirizzo, headers={"User-Agent": "Mozilla/5.0 (NFR-raccolta-notizie)"})
    pac = pac_di_sistema()
    if pac is None:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            return r.read()
    with pac_context_for_url(indirizzo, pac=pac):        # instrada come farebbe il browser
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            return r.read()


# ================================================================ file per A3
def lunedi(giorno):
    return giorno - dt.timedelta(days=giorno.weekday())


def componi_raccolta(risultati, errori, oggi, giorni):
    n = sum(len(v) for _, v in risultati)
    righe = [
        f"RACCOLTA NOTIZIE — settimana del {lunedi(oggi).isoformat()} (raccolta del {oggi.isoformat()})",
        f"Finestra: dal {(oggi - dt.timedelta(days=giorni)).isoformat()} al {oggi.isoformat()}. "
        f"Fonti interrogate: {len(risultati) + len(errori)}; con notizie: {sum(1 for _, v in risultati if v)}; notizie: {n}.",
        "Raccolta automatica dai feed dell'elenco fonti (01_Kernel/fonti.md), senza selezione di merito.",
        "Ogni notizia porta il codice della fonte: usalo come codice_fonte.",
    ]
    if errori:
        righe += ["", "FONTI NON RAGGIUNGIBILI IN QUESTA RACCOLTA (la settimana e' incompleta per queste fonti):"]
        righe += [f"- {codice} {nome}: {errore}" for codice, nome, errore in errori]
    for fonte, voci in risultati:
        if not voci:
            continue
        righe += ["", f"== {fonte['codice']} {fonte['nome']} =="]
        for v in voci:
            data = v["data"].isoformat() + (" (data non indicata dalla fonte: prima raccolta)" if v["senza_data"] else "")
            righe.append(f"- [{fonte['codice']}] {data} | {v['titolo']}")
            if v["link"]:
                righe.append(f"  {v['link']}")
            if v["estratto"]:
                righe.append(f"  {v['estratto']}")
    return "\n".join(righe) + "\n"


def raccogli(fonti, inbox, oggi, giorni, anche_da_validare, scarica_feed=scarica):
    """Esegue la raccolta; restituisce (percorso del file, notizie, errori)."""
    stati = {"approvata", "da validare"} if anche_da_validare else {"approvata"}
    da_leggere = [f for f in fonti if f["canale"] == "rss" and f["stato"] in stati
                  and f["indirizzo"].startswith("http")]
    file_visti = inbox / "_visti.json"
    visti = json.loads(file_visti.read_text(encoding="utf-8")) if file_visti.exists() else {}
    risultati, errori = [], []
    for f in da_leggere:
        try:
            voci = seleziona(analizza_feed(scarica_feed(f["indirizzo"])), f, oggi, giorni, visti)
        except Exception as ex:                      # una fonte giu' non ferma le altre
            errori.append((f["codice"], f["nome"], f"{type(ex).__name__}: {str(ex)[:120]}"))
            continue
        risultati.append((f, voci))
        for v in voci:
            visti.setdefault(v["link"] or v["titolo"], oggi.isoformat())
    cartella = inbox / lunedi(oggi).isoformat()
    (cartella / "Manuali").mkdir(parents=True, exist_ok=True)
    uscita = cartella / f"Raccolta_{oggi.isoformat()}.txt"
    uscita.write_text(componi_raccolta(risultati, errori, oggi, giorni), encoding="utf-8")
    file_visti.write_text(json.dumps(visti, ensure_ascii=False, indent=0), encoding="utf-8")
    return uscita, sum(len(v) for _, v in risultati), errori


def main(argv=None):
    p = argparse.ArgumentParser(description="Raccolta delle notizie dai feed dell'elenco fonti (W0 locale).")
    p.add_argument("--kernel")
    p.add_argument("--news-inbox", dest="news_inbox")
    p.add_argument("--giorni", type=int, default=7)
    p.add_argument("--oggi")
    p.add_argument("--anche-da-validare", action="store_true")
    arg = p.parse_args(argv)
    from esegui_ciclo_locale import configurazione
    conf = configurazione(arg)
    try:
        fonti = leggi_fonti(conf["kernel"] / "fonti.md")
        oggi = dt.date.fromisoformat(arg.oggi) if arg.oggi else dt.date.today()
        conf["news_inbox"].mkdir(parents=True, exist_ok=True)
        uscita, n, errori = raccogli(fonti, conf["news_inbox"], oggi, arg.giorni, arg.anche_da_validare)
    except Exception as ex:
        print(f"ERRORE TECNICO — nessuna raccolta scritta: {type(ex).__name__}: {ex}")
        return 2
    print(f"Raccolta scritta: {uscita}\nNotizie: {n}")
    for codice, nome, errore in errori:
        print(f"ATTENZIONE: {codice} {nome} non raggiungibile ({errore})")
    if n == 0 and not arg.anche_da_validare:
        print("Nessuna notizia: nessuna fonte 'rss' e' ancora 'approvata' in fonti.md? Per le prove: --anche-da-validare.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
