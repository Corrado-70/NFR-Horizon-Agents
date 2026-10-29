"""Test senza Excel del report al comitato in HTML (D-83, tappa M4, 29/10/2026).

Sul registro della demo (Demo_W1_W2/NFR_Registro.xlsx, letto con openpyxl: i valori che Excel ha salvato):
  1. il report del ciclo corrente esce, con il cancello superato (numeri uguali a quelli di Excel);
  2. le pagine: il report al comitato, le schede di tutti i rischi e la guida; con --con-lavoro anche le viste di lavoro;
     validazione e validatore in testa; collegamento all'indice;
  3. file unico autosufficiente: niente script, fogli di stile o immagini da fuori; nessun collegamento interno rotto;
  4. il cancello scatta con un numero alterato (un valore dei dati o una cella delle viste di Excel): l'HTML non esce;
  5. l'indice dei cicli dai riassunti accanto ai report;
  6. pubblicazione nell'archivio (esegui_ciclo_locale.pubblica_html): versione precedente conservata, riassunto e
     indice; con il cancello scattato niente file, solo l'avviso.
La lettura via COM (RegistroExcel) e il cancello sulle viste ricalcolate da Excel sono nella catena (run_catena.py).

Uso: python test_report_html.py [-v]
"""

import copy
import json
import re
import sys
import tempfile
import time
from pathlib import Path

from comune import Esito, RADICE
import esegui_ciclo_locale as campo
import report_html as rh

DEMO = RADICE.parent / "Demo_W1_W2" / "NFR_Registro.xlsx"


def link_rotti(testo):
    ids = set(re.findall(r'id="([^"]+)"', testo))
    return sorted({r for r in re.findall(r'href="#([^"]+)"', testo) if r not in ids})


def test_report(e, reg):
    ciclo = reg.nome("cicloCorrente")
    testo, riga, uguali = rh.genera(reg)
    e.verifica(uguali >= 100 and riga["ciclo"] == ciclo and riga["file"] == f"{ciclo}/Report_comitato_{ciclo}.html",
               f"report del ciclo corrente ({ciclo}): cancello superato, {uguali} numeri uguali a quelli di Excel", riga)
    menu = re.findall(r'<a href="#([a-z]+)">', testo.split('<nav class="menu"')[1].split("</nav>")[0])
    e.verifica(menu == ["quadro", "classifica", "radar", "matrice", "delta", "fenomeni", "metodologia", "schede", "guida"],
               "pagine: il report al comitato (Quadro..Metodologia), l'indice delle schede, la guida", menu)
    schede = set(re.findall(r'id="scheda-([^"]+)"', testo))
    e.verifica(len(schede) == riga["nel_radar"] + riga["in_osservazione"] and len(schede) > 10,
               f"schede di tutti i rischi, del radar e in osservazione ({len(schede)})", sorted(schede))
    e.verifica("validato il" in testo.split("</header>")[0] and f'href="../{rh.INDICE}"' in testo,
               "testata: data della validazione e validatore; collegamento all'indice dei cicli")
    risorse = re.findall(r'<(?:script|img|link|iframe)[^>]*\b(?:src|href)=', testo) + re.findall(r'url\(\s*["\']?http', testo)
    e.verifica(not risorse and testo.count("<script>") == 1 and "<style>" in testo,
               "file unico autosufficiente: CSS e JavaScript dentro, nessuna risorsa da fuori", risorse[:5])
    e.verifica(not link_rotti(testo), "nessun collegamento interno rotto (rischi, schede, pagine)", link_rotti(testo)[:10])
    lavoro, _, _ = rh.genera(reg, con_lavoro=True)
    menu_l = re.findall(r'<a href="#([a-z]+)">', lavoro.split('<nav class="menu"')[1].split("</nav>")[0])
    e.verifica({"registro", "storico", "indicatori", "notizie", "piano", "parametri"} <= set(menu_l) and "dati" not in menu_l
               and not link_rotti(lavoro), "--con-lavoro: anche Registro, Storico, Indicatori, Notizie, Piano azioni, "
               "Parametri (e le altre viste di lavoro); niente tabelle dati dell'anteprima", menu_l)
    return testo, riga


def test_cancello(e, reg):
    ciclo = reg.nome("cicloCorrente")
    riga = next(r for r in reg.tab["tblRegister"] if r["Ciclo"] == ciclo)
    originale = riga["Prossimita"]
    riga["Prossimita"] = originale - 1 if originale > 1 else originale + 1          # Z (anni) cambia, Excel no
    try:
        rh.genera(reg)
        scattato = None
    except rh.Cancello as ex:
        scattato = ex
    finally:
        riga["Prossimita"] = originale
    e.verifica(scattato is not None and scattato.diversi and riga["ID_Rischio"] in " ".join(scattato.diversi),
               f"cancello: con la Prossimita di {riga['ID_Rischio']} alterata nei dati l'HTML non esce, e il motivo nomina il rischio",
               getattr(scattato, "diversi", None))
    cella = reg.cella
    reg.cella = lambda f, r, c: (cella(f, r, c) + 0.5) if (f, c) == ("Delta", 7) and isinstance(cella(f, r, c), (int, float)) else cella(f, r, c)
    try:
        rh.genera(reg)
        scattato = None
    except rh.Cancello as ex:
        scattato = ex
    finally:
        reg.cella = cella
    e.verifica(scattato is not None and any("Delta" in d for d in scattato.diversi),
               "cancello: con un Delta di Excel diverso da quello calcolato l'HTML non esce", getattr(scattato, "diversi", None))


def test_indice_e_pubblicazione(e, testo, riga):
    with tempfile.TemporaryDirectory() as tmp:
        u = Path(tmp) / "Archivio"
        conf = {"cartella_uscita": u, "cartella_lavoro": Path(tmp) / "lavoro"}
        ciclo = riga["ciclo"]
        for n in (1, 2):
            f = Path(tmp) / f"r{n}.html"
            f.write_text(testo, encoding="utf-8")
            msg = campo.pubblica_html({"file": f, "riga": riga, "uguali": 118}, conf, ciclo)
            if n == 1:
                time.sleep(1.1)                       # nome della versione precedente con l'ora: secondi diversi
        cartella = u / "Cicli" / ciclo
        e.verifica((cartella / f"Report_comitato_{ciclo}.html").exists() and len(list(cartella.glob(f"Report_comitato_{ciclo}_*.html"))) == 1
                   and (cartella / f"Report_comitato_{ciclo}.json").exists() and "Versione precedente conservata" in msg,
                   "pubblicazione: Report_comitato_<ciclo>.html nell'archivio, la versione precedente con data e ora, il riassunto", msg)
        indice = u / "Cicli" / rh.INDICE
        altro = dict(riga, ciclo="2026Q3", file="2026Q3/Report_comitato_2026Q3.html")
        (u / "Cicli" / "2026Q3").mkdir(parents=True)
        (u / "Cicli" / "2026Q3" / "Report_comitato_2026Q3.json").write_text(json.dumps(altro), encoding="utf-8")
        rh.scrivi_indice(u / "Cicli")
        e.verifica(f'href="{ciclo}/Report_comitato_{ciclo}.html"' in indice.read_text(encoding="utf-8")
                   and "2026Q3/Report_comitato_2026Q3.html" not in indice.read_text(encoding="utf-8"),
                   "indice: una riga per report che c'e' (un riassunto senza il suo HTML non entra)")
        (u / "Cicli" / "2026Q3" / "Report_comitato_2026Q3.html").write_text("<html>", encoding="utf-8")
        rh.scrivi_indice(u / "Cicli")
        t = indice.read_text(encoding="utf-8")
        e.verifica(t.index(ciclo) < t.index("2026Q3/Report"), "indice: due cicli, dal piu' recente")
        msg = campo.pubblica_html({"motivo": "Avviso: report HTML del ciclo X NON uscito"}, conf, "2027Q1")
        e.verifica(msg.startswith("Avviso") and not (u / "Cicli" / "2027Q1" / "Report_comitato_2027Q1.html").exists(),
                   "cancello scattato: nessun file, solo l'avviso (il PDF esce lo stesso)", msg)


def main():
    e = Esito("Report al comitato in HTML (senza Excel)")
    if not DEMO.exists():
        e.verifica(False, f"registro della demo presente ({DEMO})")
        return 0 if e.stampa() else 1
    reg = rh.RegistroFile(DEMO)
    testo, riga = test_report(e, reg)
    test_cancello(e, reg)
    test_indice_e_pubblicazione(e, testo, riga)
    return 0 if e.stampa() else 1


if __name__ == "__main__":
    sys.exit(main())
