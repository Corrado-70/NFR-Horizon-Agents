"""Test senza Excel dell'installazione (D-83, tappa M3, 29/10/2026).

  1. moduli mancanti e comando pip (dalla rete, dalla cartella dei pacchetti); spiegazione di un pip non riuscito;
  2. configurazione: unione con quella che c'e' (voci sconosciute conservate, link per versione), problemi gravi e
     avvisi, salvataggio con la copia precedente;
  3. attivita' pianificata: XML valido in UTF-16, lunedi' alle 7, senza privilegi, comando e cartella giusti;
  4. collegamenti: script PowerShell con gli apici raddoppiati, Desktop e Invia a;
  5. "Invia a -> NFR notizie manuali": copia nella cartella del lunedi', nomi gia' presenti non sovrascritti;
  6. Verifica del PC su una configurazione di prova (senza Excel): righe e file salvato nell'archivio;
  7. i lanciatori nuovi (.cmd): solo ASCII, a capo di Windows, cartella dello script;
  8. l'aggiornamento sopra un pacchetto installato (D-89): versione, lanciatori .cmd.txt, voci facoltative, kernel
     nella library con i precedenti messi da parte, file obsoleti, agenti da reincollare, installato.json.
Le prove sul PC vero (pip, schtasks, collegamenti, Excel) sono nella guida, sezione 0.3, e in 18.3 dell'analisi.

Uso: python test_installazione.py [-v]
"""

import contextlib
import datetime as dt
import io
import json
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

from comune import CAMPO, Esito, KERNEL
import installazione as ins


def test_moduli(e):
    tutti = lambda istruzione: True
    nessuno = lambda istruzione: False
    e.verifica(ins.moduli_mancanti(tutti) == [], "moduli: niente da installare se gli import riescono")
    mancanti = ins.moduli_mancanti(lambda istruzione: "openpyxl" in istruzione)
    e.verifica([p for p, _ in mancanti] == ["pywin32", "pypac"], "moduli: si elencano solo quelli che mancano", mancanti)
    e.verifica(any("pythoncom" in i for i, p, _ in ins.MODULI if p == "pywin32"),
               "moduli: pywin32 si prova anche con pythoncom (un pywin32 a meta' non passa)")
    cmd = ins.comando_pip(["pypac", "pywin32", "pypac"], eseguibile="python")
    e.verifica(cmd[:5] == ["python", "-m", "pip", "install", "--user"] and cmd[-2:] == ["pypac", "pywin32"]
               and "--no-index" not in cmd, "pip: --user, pacchetti senza doppioni, dalla rete", cmd)
    with tempfile.TemporaryDirectory() as tmp:
        vuota, piena = Path(tmp) / "vuota", Path(tmp) / "pacchetti"
        vuota.mkdir()
        piena.mkdir()
        (piena / "pywin32-311-cp312-cp312-win_amd64.whl").write_bytes(b"x")
        e.verifica(ins.cartella_pacchetti([vuota, Path(tmp) / "manca"]) is None, "pacchetti: una cartella vuota non conta")
        trovata = ins.cartella_pacchetti([vuota, piena])
        cmd = ins.comando_pip(["pywin32"], trovata, eseguibile="python")
        e.verifica(trovata == piena and cmd[cmd.index("--find-links") + 1] == str(piena) and "--no-index" in cmd,
                   "pip: con la cartella dei pacchetti si installa solo da li' (--no-index)", cmd)
    e.verifica("pip download" in ins.spiega_pip("ProxyError: Cannot connect to proxy") and
               "stessa versione" in ins.spiega_pip("ERROR: No matching distribution found for pywin32"),
               "pip non riuscito: proxy -> cartella dei pacchetti; versione sbagliata -> stesso Python")
    e.verifica(ins.python_adatto((3, 10)) and not ins.python_adatto((3, 9)), "Python: 3.10 si', 3.9 no")


def test_configurazione(e):
    vecchia = {"workbook": "C:\\vecchio.xlsx", "cartella_lavoro": "D:\\lavoro", "attesa_lucchetto": 0,
               "link_agenti": {"A1": "https://ab/a1", "A3": "incollare il link dell'agente"}}
    nuova = {"workbook": "C:\\nuovo.xlsx", "utente": "Analista", "agenti": "Agent Builder",
             "link_agenti": {"A3": "https://ab/a3"}}
    u = ins.unisci(vecchia, nuova)
    e.verifica(u["workbook"] == "C:\\nuovo.xlsx" and u["cartella_lavoro"] == "D:\\lavoro" and u["attesa_lucchetto"] == 0
               and u["link_agenti"] == {"A1": "https://ab/a1", "A3": "https://ab/a3"},
               "configurazione: la finestra vince, le voci che non conosce restano, i link si uniscono", u)
    cs = ins.unisci(u, {"agenti": "Copilot Studio", "link_agenti": {"A1": "https://cs/a1"}})
    e.verifica(cs["link_agenti"] == {"Agent Builder": {"A1": "https://ab/a1", "A3": "https://ab/a3"},
                                     "Copilot Studio": {"A1": "https://cs/a1"}},
               "configurazione: i link di Copilot Studio accanto a quelli di Agent Builder (formato per versione)", cs)
    di_nuovo = ins.unisci(cs, {"link_agenti": {"A7": "https://ab/a7"}}, "Agent Builder")
    e.verifica(di_nuovo["link_agenti"]["Agent Builder"]["A7"] == "https://ab/a7"
               and di_nuovo["link_agenti"]["Copilot Studio"] == {"A1": "https://cs/a1"},
               "configurazione: per versione, si cambia solo la versione scelta", di_nuovo["link_agenti"])
    e.verifica(ins.link_della_versione(di_nuovo, "Copilot Studio")["A1"] == "https://cs/a1"
               and ins.link_della_versione(vecchia, "Copilot Studio")["A1"] == "https://ab/a1",
               "configurazione: link letti dal formato per versione e da quello piatto")
    with tempfile.TemporaryDirectory() as tmp:
        t = Path(tmp)
        for c in ("Kernel", "Archivio", "News", "Report"):
            (t / c).mkdir()
        conf = {"workbook": str(t / "Report" / "NFR_Registro.xlsx"), "kernel": str(t / "Kernel"),
                "cartella_uscita": str(t / "Archivio"), "news_inbox": str(t / "News"), "utente": "Analista",
                "agenti": "Agent Builder", "link_agenti": {a: f"https://ab/{a}" for a in ins.AGENTI}}
        gravi, avvisi = ins.problemi(conf)
        e.verifica(not gravi and len(avvisi) == 1 and "inizializza" in avvisi[0],
                   "configurazione completa: solo l'avviso del registro che non c'e' ancora", f"{gravi}\n{avvisi}")
        gravi, avvisi = ins.problemi({**conf, "kernel": str(t / "manca"), "utente": " ", "link_agenti": {"A1": "x"}})
        e.verifica(len(gravi) == 2 and any("kernel" in g for g in gravi) and any("utente" in g for g in gravi)
                   and any("A3" in a for a in avvisi), "configurazione: cartella che non c'e' e utente vuoto sono gravi; "
                   "link mancanti un avviso", f"{gravi}\n{avvisi}")
        f = t / "configurazione.json"
        ins.salva_configurazione(f, {"utente": "uno"})
        ins.salva_configurazione(f, {"utente": "due"})
        copie = list(t.glob("configurazione_*.json.precedente"))
        e.verifica(json.loads(f.read_text(encoding="utf-8"))["utente"] == "due" and len(copie) == 1
                   and json.loads(copie[0].read_text(encoding="utf-8"))["utente"] == "uno",
                   "configurazione: salvata, la precedente resta accanto con data e ora")


def test_attivita(e):
    testo = ins.xml_attivita(r"C:\Python312\pythonw.exe", r"C:\NFR & co\raccogli_notizie.py", r"C:\NFR & co",
                             inizio=dt.date(2026, 10, 29))
    radice = ET.fromstring(testo.encode("utf-16"))
    ns = {"t": "http://schemas.microsoft.com/windows/2004/02/mit/task"}
    e.verifica(radice.find(".//t:StartBoundary", ns).text == "2026-11-02T07:00:00"
               and radice.find(".//t:DaysOfWeek/t:Monday", ns) is not None
               and radice.find(".//t:RunLevel", ns).text == "LeastPrivilege"
               and radice.find(".//t:StartWhenAvailable", ns).text == "true",
               "attivita': XML valido in UTF-16, il prossimo lunedi' alle 7, senza privilegi, recupera se il PC era spento")
    e.verifica(radice.find(".//t:Command", ns).text == r"C:\Python312\pythonw.exe"
               and radice.find(".//t:Arguments", ns).text == r'"C:\NFR & co\raccogli_notizie.py"'
               and radice.find(".//t:WorkingDirectory", ns).text == r"C:\NFR & co",
               "attivita': programma, script tra virgolette e cartella giusti, anche con '&' nel percorso")
    e.verifica(ins.comando_attivita("a.xml") == ["schtasks", "/create", "/tn", ins.NOME_ATTIVITA, "/xml", "a.xml", "/f"],
               "attivita': schtasks /create /xml, sostituisce quella che c'e' (/f)")


def test_collegamenti(e):
    s = ins.script_collegamento("Desktop", "NFR Horizon Scan", r"C:\Users\d'Amico\pythonw.exe", '"app_nfr.py"')
    e.verifica("GetFolderPath('Desktop')" in s and r"'C:\Users\d''Amico\pythonw.exe'" in s and "$l.Save()" in s,
               "collegamenti: cartella del Desktop chiesta a Windows, apici raddoppiati nei percorsi", s)
    nomi = [(c[0], c[1]) for c in ins.collegamenti(eseguibile="python.exe", cartella=CAMPO)]
    e.verifica(nomi == [("Desktop", ins.NOME_COLLEGAMENTO), ("SendTo", ins.NOME_INVIA_A)]
               and ins.collegamenti(cartella=CAMPO)[1][2].endswith("NFR_notizie_manuali.cmd"),
               "collegamenti: l'app sul Desktop, i file a mano in Invia a", nomi)
    k = Path(r"C:\K")
    e.verifica(ins.comandi_mantieni_sul_pc(k) == [["attrib", "+P", str(k)], ["attrib", "+P", str(k / "*"), "/S", "/D"]],
               "OneDrive: attrib +P sulla cartella e su cio' che contiene")


def test_notizie_manuali(e):
    import notizie_manuali as nm
    with tempfile.TemporaryDirectory() as tmp:
        t = Path(tmp)
        news = t / "News_Inbox"
        news.mkdir()
        a, b = t / "Circolare.pdf", t / "rapporto"
        a.write_bytes(b"pdf")
        b.mkdir()
        (b / "Rapporto.txt").write_text("r", encoding="utf-8")
        giovedi = dt.date(2026, 10, 29)
        copiati, saltati = nm.copia([a, b, t / "manca.pdf"], news, giovedi)
        manuali = news / "2026-10-26" / "Manuali"
        e.verifica(sorted(p.name for p in manuali.iterdir()) == ["Circolare.pdf", "Rapporto.txt"] and len(saltati) == 1,
                   "Invia a: i file (anche quelli di una cartella) nella cartella Manuali del lunedi'; uno che non c'e' saltato",
                   f"{copiati}\n{saltati}")
        nm.copia([a], news, giovedi)
        e.verifica((manuali / "Circolare (2).pdf").exists() and (manuali / "Circolare.pdf").read_bytes() == b"pdf",
                   "Invia a: un file con lo stesso nome non si sovrascrive (Circolare (2).pdf)")


def test_verifica_pc(e):
    import verifica_pc
    with tempfile.TemporaryDirectory() as tmp:
        t = Path(tmp)
        for c in ("Archivio", "News", "Report"):
            (t / c).mkdir()
        conf = {"workbook": str(t / "Report" / "NFR_Registro.xlsx"), "kernel": str(KERNEL),
                "cartella_uscita": str(t / "Archivio"), "news_inbox": str(t / "News"), "utente": "Analista",
                "agenti": "Agent Builder", "raccolta_su_questo_pc": False,
                "link_agenti": {"A1": "https://ab/a1"}}
        f = t / "configurazione.json"
        f.write_text(json.dumps(conf), encoding="utf-8")
        righe, letta = verifica_pc.verifica(con_excel=False, file_conf=f)
        per_voce = {r["voce"]: r for r in righe}
        e.verifica(per_voce["cartella Archivio_Cicli"]["esito"] == "OK" and per_voce["file del kernel"]["esito"] == "OK"
                   and per_voce["lucchetto del registro"]["esito"] == "OK"
                   and per_voce["registro"]["esito"] == "ATTENZIONE"
                   and per_voce["link degli agenti (Agent Builder)"]["esito"] == "ATTENZIONE",
                   "verifica del PC: cartelle, kernel e lucchetto OK; registro che non c'e' e link mancanti da sistemare",
                   "\n".join(f"{r['esito']} {r['voce']}: {r['dettaglio']}" for r in righe))
        e.verifica(not (t / "Archivio" / "_Lucchetto" / "registro.json").exists(),
                   "verifica del PC: il lucchetto di prova e' stato lasciato")
        contenuto = verifica_pc.testo(righe, letta)
        salvato = verifica_pc.salva(contenuto, conf)
        e.verifica(salvato and salvato.parent == t / "Archivio" / verifica_pc.CARTELLA_VERIFICHE
                   and "Esito:" in salvato.read_text(encoding="utf-8"),
                   "verifica del PC: il file nell'archivio, in Verifiche_PC, con l'esito in fondo", salvato)
        righe, _ = verifica_pc.verifica(con_excel=False, file_conf=t / "manca.json")
        e.verifica(any(r["voce"] == "configurazione.json" and r["esito"] == "NO" for r in righe),
                   "verifica del PC: senza configurazione.json un NO con il rimedio (installa.cmd)")


def test_lanciatori(e):
    for nome, script in (("installa.cmd", "installa.py"), ("NFR_notizie_manuali.cmd", "notizie_manuali.py")):
        p = CAMPO / nome
        if not p.exists():
            e.verifica(False, f"{nome} presente in 07_Senza_Studio")
            continue
        b = p.read_bytes()
        righe = b.split(b"\n")
        e.verifica(all(c < 128 for c in b) and all(r.endswith(b"\r") for r in righe[:-1]) and b"%~dp0" in b
                   and script.encode() in b and b"chcp 65001" in b,
                   f"{nome}: solo ASCII, a capo di Windows (le etichette goto), cartella dello script, lancia {script}")


def test_versione_e_lanciatori(e):
    with tempfile.TemporaryDirectory() as tmp:
        t = Path(tmp)
        f = t / "VERSIONE.txt"
        e.verifica(ins.leggi_versione(f) == "sconosciuta", "versione: senza VERSIONE.txt 'sconosciuta'")
        f.write_text("$Format:%h %cs$\n", encoding="utf-8")
        e.verifica(ins.leggi_versione(f) == "sviluppo", "versione: il segnaposto di git (copia di sviluppo) e' 'sviluppo'")
        f.write_text("da119c9 2026-10-30\n", encoding="utf-8")
        e.verifica(ins.leggi_versione(f) == "da119c9 2026-10-30" and ins.data_versione("da119c9 2026-10-30") == "2026-10-30",
                   "versione: commit e data scritti da git archive")
        (t / "NFR.cmd.txt").write_bytes(b"nuovo")
        (t / "NFR_notizie_manuali.cmd.txt").write_bytes(b"nuovo")
        (t / "NFR_notizie_manuali.cmd").write_bytes(b"vecchio")
        (t / "installa.cmd.txt").write_bytes(b"nuovo")
        (t / "installa.cmd").write_bytes(b"vecchio")
        fatti, lasciati = ins.rinomina_lanciatori(t)
        e.verifica(sorted(fatti) == ["NFR.cmd", "NFR_notizie_manuali.cmd"] and lasciati == ["installa.cmd.txt"]
                   and (t / "NFR_notizie_manuali.cmd").read_bytes() == b"nuovo" and not (t / "NFR.cmd.txt").exists()
                   and (t / "installa.cmd").read_bytes() == b"vecchio",
                   "lanciatori: .cmd.txt -> .cmd, anche sopra quello di prima; installa.cmd in esecuzione resta", f"{fatti} {lasciati}")
        (t / "installa.cmd").write_bytes(b"nuovo")
        fatti, lasciati = ins.rinomina_lanciatori(t)
        e.verifica(fatti == ["installa.cmd"] and not lasciati and not (t / "installa.cmd.txt").exists(),
                   "lanciatori: installa.cmd.txt uguale a installa.cmd si toglie e basta", f"{fatti} {lasciati}")
        e.verifica(ins.rinomina_lanciatori(t) == ([], []), "lanciatori: rilanciato, niente da fare")
    mancanti = ins.predefiniti_mancanti({"utente": "x", "chiedi_a5": False, "giorni_log": 7})
    e.verifica(mancanti == {"attesa_lucchetto": 0, "ascolta_appunti": True, "backup_da_tenere": 10, "giorni_parcheggio": 30},
               "configurazione: le voci facoltative che mancano con il predefinito, quelle scritte restano", mancanti)


def test_kernel(e):
    with tempfile.TemporaryDirectory() as tmp:
        t = Path(tmp)
        sorg, lib = t / "01_Kernel", t / "Kernel"
        sorg.mkdir()
        (lib / "Spiegazioni").mkdir(parents=True)
        (sorg / "rubrica.md").write_bytes(b"riga 1\nriga 2\n")
        (sorg / "schema.json").write_bytes(b'{"nuovo": 1}\n')
        (sorg / "guida.md").write_bytes(b"nuova\n")
        (sorg / "Tassonomia dei Rischi.csv").write_bytes(b"csv")         # rimasta in 01_Kernel da un pacchetto vecchio
        decisioni = t / "DECISIONI.md"
        decisioni.write_bytes(b"D-89\n")
        (lib / "rubrica.md").write_bytes(b"riga 1\r\nriga 2\r\n")          # solo a capo diversi: non e' cambiato
        (lib / "schema.json").write_bytes(b'{"vecchio": 1}\n')
        (lib / "Baseline_corrente.txt").write_bytes(b"baseline")
        (lib / "Tassonomia dei Rischi.csv").write_bytes(b"csv")
        (lib / "Spiegazioni" / "Ciclo.txt").write_bytes(b"spiegazioni")
        sorgenti = ins.sorgenti_kernel(sorg, decisioni)
        nuovi, cambiati, togliere = ins.differenze_kernel(lib, sorgenti)
        e.verifica([s.name for s in nuovi] == ["guida.md", "DECISIONI.md"] and [s.name for s in cambiati] == ["schema.json"]
                   and togliere == ["Baseline_corrente.txt", "Tassonomia dei Rischi.csv"],
                   "kernel: nuovi, cambiati (non per gli a capo) e i file da togliere dalla library; la tassonomia "
                   "rimasta in 01_Kernel non si copia",
                   f"{nuovi}\n{cambiati}\n{togliere}")
        e.verifica(ins.differenze_kernel(sorg, sorgenti) == ([], [], []), "kernel: library = 01_Kernel (sviluppo), niente")
        parcheggio = ins.copia_kernel(lib, nuovi, cambiati, togliere, "da119c9 2026-10-30", quando="20261030_120000")
        e.verifica(parcheggio == lib / "_precedenti" / "20261030_120000"
                   and sorted(p.name for p in parcheggio.iterdir()) == ["Baseline_corrente.txt", "Tassonomia dei Rischi.csv", "schema.json"]
                   and (parcheggio / "schema.json").read_bytes() == b'{"vecchio": 1}\n'
                   and (lib / "schema.json").read_bytes() == b'{"nuovo": 1}\n' and (lib / "DECISIONI.md").exists()
                   and not (lib / "Baseline_corrente.txt").exists() and (lib / "Spiegazioni" / "Ciclo.txt").exists()
                   and (lib / "rubrica.md").read_bytes() == b"riga 1\r\nriga 2\r\n",
                   "kernel: copiati i nuovi e i cambiati, i sostituiti e i tolti in _precedenti, Spiegazioni non toccata")
        e.verifica(ins.differenze_kernel(lib, sorgenti) == ([], [], []), "kernel: rilanciato, niente da copiare")
        e.verifica(ins.kernel_piu_recente(lib, "abc1234 2026-10-28") == "da119c9 2026-10-30"
                   and ins.kernel_piu_recente(lib, "fff0000 2026-11-05") is None
                   and ins.kernel_piu_recente(lib, "sviluppo") is None,
                   "kernel: un pacchetto piu' vecchio di quello nella library non la riporta indietro")


def test_obsoleti(e):
    with tempfile.TemporaryDirectory() as tmp:
        t = Path(tmp)
        elenco = t / "obsoleti.txt"
        elenco.write_text("# commento\n\nNFR/04_SharePoint\nNFR\\01_Kernel\\vecchio.csv\nDemo/manca.txt\n"
                          "C:/Windows\n../fuori\n/assoluto\n", encoding="utf-8")
        letti = ins.leggi_obsoleti(elenco)
        e.verifica(letti == ["NFR/04_SharePoint", "NFR/01_Kernel/vecchio.csv", "Demo/manca.txt"],
                   "obsoleti: commenti, righe vuote, percorsi assoluti e '..' scartati; barre rovesciate accettate", letti)
        (t / "NFR" / "04_SharePoint").mkdir(parents=True)
        (t / "NFR" / "04_SharePoint" / "struttura.md").write_text("x", encoding="utf-8")
        (t / "NFR" / "01_Kernel").mkdir()
        (t / "NFR" / "01_Kernel" / "vecchio.csv").write_text("x", encoding="utf-8")
        presenti = ins.obsoleti_presenti(t, letti)
        e.verifica(presenti == ["NFR/04_SharePoint", "NFR/01_Kernel/vecchio.csv"], "obsoleti: solo quelli che ci sono", presenti)
        parcheggio = ins.parcheggia_obsoleti(t, presenti, quando="20261030_120000")
        e.verifica(parcheggio == t / "_obsoleti_20261030_120000"
                   and (parcheggio / "NFR" / "04_SharePoint" / "struttura.md").exists()
                   and (parcheggio / "NFR" / "01_Kernel" / "vecchio.csv").exists()
                   and not (t / "NFR" / "04_SharePoint").exists() and (t / "NFR" / "01_Kernel").exists(),
                   "obsoleti: spostati in _obsoleti_<data> con lo stesso percorso, le cartelle in uso restano")
        e.verifica(ins.obsoleti_presenti(t, letti) == [], "obsoleti: rilanciato, niente da spostare")
        (t / "NFR" / "__pycache__").mkdir()
        (t / "NFR" / "01_Kernel" / "__pycache__").mkdir()
        (parcheggio / "NFR" / "__pycache__").mkdir()
        e.verifica(ins.togli_pycache(t) == 2 and not (t / "NFR" / "__pycache__").exists()
                   and (parcheggio / "NFR" / "__pycache__").exists(), "obsoleti: __pycache__ tolte, non nel parcheggio")
    pacchetto = ins.leggi_obsoleti()
    e.verifica(pacchetto and ins.obsoleti_presenti(ins.RADICE, pacchetto) == [],
               "obsoleti.txt del pacchetto: nessun percorso elencato esiste nel pacchetto di adesso",
               ins.obsoleti_presenti(ins.RADICE, pacchetto))


def test_agenti(e):
    import installa
    with tempfile.TemporaryDirectory() as tmp:
        t = Path(tmp)
        (t / "COMMENTATI").mkdir()
        (t / "A1_Horizon_Scanner.md").write_text("A1 v1", encoding="utf-8")
        (t / "A3_Interim_Update.md").write_text("A3 v1", encoding="utf-8")
        (t / "componi_prompt.py").write_text("", encoding="utf-8")
        e.verifica([a for a, _ in ins.agenti_cambiati({}, t)] == ["A1", "A3"],
                   "agenti: senza installato.json si elencano tutti")
        imp = {a: i for a, (_, i) in ins.impronte_agenti(t).items()}
        f = t / "installato.json"
        ins.scrivi_installato(f, "da119c9 2026-10-30", {"rubrica.md": "abc"}, {"A1": imp["A1"], "A3": imp["A3"]}, "Analista")
        letto = ins.leggi_installato(f)
        e.verifica(letto["versione"] == "da119c9 2026-10-30" and letto["utente"] == "Analista"
                   and ins.agenti_cambiati(letto, t) == [], "agenti: installato.json scritto e riletto, niente da reincollare")
        (t / "A3_Interim_Update.md").write_text("A3 v2", encoding="utf-8")
        e.verifica([a for a, _ in ins.agenti_cambiati(letto, t)] == ["A3"], "agenti: si elenca solo quello cambiato")
        f.write_text("{rotto", encoding="utf-8")
        e.verifica(ins.leggi_installato(f) == {} and ins.leggi_installato(t / "manca.json") == {},
                   "agenti: installato.json illeggibile o assente vale come prima installazione")
    riep = {"fatto": [], "a_mano": []}
    tutti = {a: i for a, (_, i) in ins.impronte_agenti().items()}
    with contextlib.redirect_stdout(io.StringIO()):
        segnati = installa.passo_agenti({}, riep, chiedi=lambda _: "n")
    e.verifica(segnati == {} and riep["a_mano"] and set(tutti) >= {"A1", "A3", "A4", "A5", "A6", "A7", "A8"},
               "agenti: risposta N, restano da reincollare (nel riepilogo)", riep)
    with contextlib.redirect_stdout(io.StringIO()):
        segnati = installa.passo_agenti({"agenti": {"A1": tutti["A1"]}}, riep, chiedi=lambda _: "s")
    e.verifica(segnati == tutti and ins.agenti_cambiati({"agenti": segnati}) == [],
               "agenti: risposta S, segnati come reincollati quelli elencati e quelli di prima", segnati)


def main():
    e = Esito("Installazione e Verifica del PC (senza Excel)")
    test_moduli(e)
    test_configurazione(e)
    test_attivita(e)
    test_collegamenti(e)
    test_notizie_manuali(e)
    test_verifica_pc(e)
    test_lanciatori(e)
    test_versione_e_lanciatori(e)
    test_kernel(e)
    test_obsoleti(e)
    test_agenti(e)
    return 0 if e.stampa() else 1


if __name__ == "__main__":
    sys.exit(main())
