"""Elenco delle fonti e raccolta delle notizie (W0 locale), senza rete.

1. fonti.md si legge, i codici sono unici e rispettano il pattern dello schema A3.
2. I siti per la knowledge web rispettano i limiti di Agent Builder: al massimo
   quattro, URL di al massimo due livelli, senza parametri.
3. I temi citati sono codici della tassonomia.
4. I codici fonte dei dati di esempio e dei dati di prova sono nell'elenco.
5. Il prompt di A3 contiene ogni fonte non esclusa.
6. La raccolta, con feed finti: RSS 2.0, Atom, voci senza data, finestra di
   date, parole escluse, max_voci, doppioni fra due giorni, fonte giu'.

Esecuzione: python test_fonti.py   (codice di uscita 0 = tutto ok)
"""

import datetime as dt
import re
import sys
import tempfile
from pathlib import Path

from comune import DATI, EXCEL, KERNEL, RADICE, Esito, carica
import raccogli_notizie as rn
from fonti import CODICE_MANUALE, codici_ammessi, leggi_fonti

RSS = b"""<?xml version="1.0"?><rss version="2.0"><channel><title>Prova</title>
<item><title>Nuova guida sulle terze parti ICT</title><link>https://es.eu/a</link><pubDate>Mon, 12 Oct 2026 10:00:00 +0200</pubDate><description>&lt;p&gt;Testo &amp;amp; html&lt;/p&gt;</description></item>
<item><title>Cambi di riferimento del 12 ottobre</title><link>https://es.eu/b</link><pubDate>Mon, 12 Oct 2026 09:00:00 +0200</pubDate></item>
<item><title>Notizia vecchia</title><link>https://es.eu/c</link><pubDate>Mon, 01 Jun 2026 09:00:00 +0200</pubDate></item>
<item><title>Voce senza data</title><link>https://es.eu/d</link></item>
</channel></rss>"""

ATOM = b"""<?xml version="1.0" encoding="utf-8"?><feed xmlns="http://www.w3.org/2005/Atom"><title>Prova</title>
<entry><title>Campagna di frode vocale</title><link rel="alternate" href="https://at.eu/1"/><updated>2026-10-11T08:00:00Z</updated><summary>Estratto</summary></entry>
<entry><title>Seconda voce</title><link href="https://at.eu/2"/><published>2026-10-10T08:00:00Z</published></entry>
<entry><title>Terza voce</title><link href="https://at.eu/3"/><published>2026-10-09T08:00:00Z</published></entry>
</feed>"""


def livelli(url):
    return len([p for p in url.split("://", 1)[1].split("/")[1:] if p])


def main():
    e = Esito("Elenco fonti e raccolta notizie")
    try:
        fonti = leggi_fonti(KERNEL / "fonti.md")
    except ValueError as ex:
        e.verifica(False, "1. fonti.md si legge senza errori di formato", str(ex))
        return 0 if e.stampa() else 1
    e.verifica(len(fonti) >= 10, f"1. fonti.md si legge ({len(fonti)} fonti)")
    pattern = carica(KERNEL / "schema_output_A3.json")["properties"]["notizie"]["items"]["properties"]["codice_fonte"]["pattern"]
    e.verifica(all(re.match(pattern, f["codice"]) for f in fonti) and re.match(pattern, CODICE_MANUALE),
               "1. ogni codice (e MAN) rispetta il pattern di codice_fonte dello schema A3", pattern)
    for canale in ("rss", "sito", "share"):
        e.verifica(any(f["canale"] == canale for f in fonti), f"1. almeno una fonte sul canale {canale}")
    rss_male = [f["codice"] for f in fonti if f["canale"] == "rss"
                and not (f["indirizzo"].startswith("https://") or f["indirizzo"] == "da compilare")]
    e.verifica(not rss_male, "1. ogni fonte rss ha un indirizzo https (o 'da compilare')", str(rss_male))

    siti = [f for f in fonti if f["sito_agente"]]
    e.verifica(len(siti) <= 4, f"2. al massimo 4 siti per la knowledge web di Agent Builder ({len(siti)})")
    male = [f"{f['codice']} {f['indirizzo']}" for f in siti
            if not f["indirizzo"].startswith("https://") or "?" in f["indirizzo"] or livelli(f["indirizzo"]) > 2]
    e.verifica(not male, "2. URL dei siti dell'agente: https, al massimo due livelli, senza parametri", "\n".join(male))

    tass = (KERNEL / "tassonomia_nfr.md").read_text(encoding="utf-8")
    noti = set(re.findall(r"^\| ((?:\d+\.\d+)|(?:DRV-[A-Z]+)) \|", tass, re.M))     # D-74: categorie interne
    ignoti = sorted({t for f in fonti for t in f["temi"]} - noti)
    e.verifica(not ignoti, "3. i temi delle fonti sono codici di tassonomia_nfr.md", str(ignoti))

    ammessi = codici_ammessi(fonti)
    sys.path.insert(0, str(EXCEL))
    import genera_dashboard as g
    esempio = {n[4] for n in g.NEWS_ESEMPIO}
    e.verifica(esempio <= ammessi, "4. i codici fonte delle notizie di esempio del template sono nell'elenco", str(sorted(esempio - ammessi)))
    prova = {n["codice_fonte"] for n in carica(DATI / "run_A3_2026-10-12.json")["notizie"]}
    e.verifica(prova <= ammessi, "4. i codici fonte dei dati di prova di A3 sono nell'elenco", str(sorted(prova - ammessi)))

    prompt = (RADICE / "02_Agenti" / "A3_Interim_Update.md").read_text(encoding="utf-8")
    assenti = [f["codice"] for f in fonti if f["stato"] != "esclusa" and f"- {f['codice']} " not in prompt]
    e.verifica(not assenti, "5. il prompt di A3 elenca ogni fonte non esclusa", str(assenti))

    # 6. Raccolta con feed finti: nessun accesso alla rete.
    voci = rn.analizza_feed(RSS)
    e.verifica(len(voci) == 4 and voci[0]["estratto"] == "Testo & html" and voci[0]["data"] == dt.date(2026, 10, 12),
               "6. RSS 2.0: titolo, link, data RFC 822, estratto senza HTML", str(voci[:1]))
    atom = rn.analizza_feed(ATOM)
    e.verifica([v["link"] for v in atom] == ["https://at.eu/1", "https://at.eu/2", "https://at.eu/3"]
               and atom[0]["data"] == dt.date(2026, 10, 11), "6. Atom: link da href, data ISO 8601", str(atom))
    elenco = [
        {"codice": "FNT-90", "nome": "Feed RSS", "canale": "rss", "indirizzo": "https://es.eu/feed", "stato": "da validare",
         "escludi": ["cambi di riferimento"], "max_voci": 20},
        {"codice": "FNT-91", "nome": "Feed Atom", "canale": "rss", "indirizzo": "https://at.eu/feed", "stato": "approvata",
         "escludi": [], "max_voci": 2},
        {"codice": "FNT-92", "nome": "Feed giu'", "canale": "rss", "indirizzo": "https://giu.eu/feed", "stato": "approvata",
         "escludi": [], "max_voci": 20},
        {"codice": "FNT-93", "nome": "Da compilare", "canale": "rss", "indirizzo": "da compilare", "stato": "approvata",
         "escludi": [], "max_voci": 20},
    ]
    feed = {"https://es.eu/feed": RSS, "https://at.eu/feed": ATOM}

    def finto(url):
        if url not in feed:
            raise OSError("connessione rifiutata")
        return feed[url]

    with tempfile.TemporaryDirectory() as tmp:
        inbox = Path(tmp)
        oggi = dt.date(2026, 10, 12)
        f1, n1, err = rn.raccogli(elenco, inbox, oggi, 7, anche_da_validare=False, scarica_feed=finto)
        testo = f1.read_text(encoding="utf-8")
        e.verifica(n1 == 2 and "FNT-90" not in testo, "6. di default solo le fonti approvate (la 'da validare' e' esclusa)", testo)
        e.verifica("Terza voce" not in testo, "6. max_voci rispettato (2 su 3 voci in finestra)", testo)
        e.verifica([c for c, _, _ in err] == ["FNT-92"] and "NON RAGGIUNGIBILI" in testo,
                   "6. una fonte irraggiungibile non ferma le altre ed e' dichiarata in testa al file", testo)
        e.verifica(f1 == inbox / "2026-10-12" / "Raccolta_2026-10-12.txt" and (inbox / "2026-10-12" / "Manuali").is_dir(),
                   "6. file nella cartella del lunedi', con la cartella Manuali", str(f1))
        f2, n2, _ = rn.raccogli(elenco, inbox, oggi, 7, anche_da_validare=True, scarica_feed=finto)
        testo = f2.read_text(encoding="utf-8")
        e.verifica(n2 == 4 and "Cambi di riferimento" not in testo and "Notizia vecchia" not in testo
                   and "data non indicata dalla fonte" in testo and "[FNT-90]" in testo,
                   "6. con --anche-da-validare: finestra di date, parole escluse, voce senza data dichiarata, codice su ogni voce", testo)
        e.verifica(n2 == 4, "6. rilancio nello stesso giorno: le voci gia' raccolte oggi restano nel file")
        f3, n3, _ = rn.raccogli(elenco, inbox, oggi + dt.timedelta(days=1), 7, anche_da_validare=True, scarica_feed=finto)
        testo = f3.read_text(encoding="utf-8")
        e.verifica(n3 == 1 and "Terza voce" in testo,
                   "6. il giorno dopo i doppioni sono scartati (_visti.json); entra solo la voce tagliata ieri da max_voci", testo)
    return 0 if e.stampa() else 1


if __name__ == "__main__":
    sys.exit(main())
