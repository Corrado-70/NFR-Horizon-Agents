"""Test senza Excel dell'orchestrazione per piu' analisti (D-83, 23/10/2026).

  1. lucchetto.py: presa e rilascio, lucchetto di un collega (fermo), scaduto (si prende), proprio rimasto da un comando
     interrotto (si riprende), copia in conflitto di OneDrive (ritiro), sblocca registrato;
  2. sostituzione del registro dalla copia di lavoro (esegui_ciclo_locale._sostituisci): con l'originale cambiato nel
     frattempo si ferma e non tocca niente; altrimenti sostituisce senza lasciare file temporanei;
  3. aperto_qui: un file tenuto aperto in esclusiva da un programma di questo PC.

Uso: python test_app.py [-v]
"""

import copy
import datetime as dt
import json
import sys
import tempfile
from pathlib import Path

from comune import CAMPO, DATI, KERNEL, Esito, carica
import esegui_ciclo_locale as campo
import lucchetto


def _scrivi_lucchetto(cartella, **campi):
    adesso = dt.datetime.now().replace(microsecond=0)
    dati = {"id": "collega", "utente": "Collega", "pc": "ALTRO-PC", "comando": "valida", "inizio": adesso.isoformat(),
            "scadenza": (adesso + dt.timedelta(hours=1)).isoformat(), **campi}
    (cartella / lucchetto.CARTELLA).mkdir(parents=True, exist_ok=True)
    (cartella / lucchetto.CARTELLA / lucchetto.FILE).write_text(json.dumps(dati), encoding="utf-8")
    return dati


def test_lucchetto(e):
    with tempfile.TemporaryDirectory() as tmp:
        c = Path(tmp)
        file = c / lucchetto.CARTELLA / lucchetto.FILE
        with lucchetto.preso(c, "griglia", "Analista", attesa=0) as mio:
            dentro = json.loads(file.read_text(encoding="utf-8"))
            e.verifica(dentro["id"] == mio["id"] and dentro["utente"] == "Analista" and lucchetto.stato(c)["comando"] == "griglia",
                       "lucchetto: preso, con utente, comando e scadenza; stato() lo vede", dentro)
        e.verifica(not file.exists() and lucchetto.stato(c) is None, "lucchetto: lasciato alla fine")
        try:
            with lucchetto.preso(c, "valida", "Analista", attesa=0):
                raise ValueError("errore nel comando")
        except ValueError:
            pass
        e.verifica(not file.exists(), "lucchetto: lasciato anche dopo un errore del comando")

        _scrivi_lucchetto(c)
        try:
            lucchetto.prendi(c, "griglia", "Analista", attesa=0)
            fermato = None
        except lucchetto.Occupato as ex:
            fermato = str(ex)
        e.verifica(fermato and "Collega" in fermato and "sblocca" in fermato
                   and json.loads(file.read_text(encoding="utf-8"))["id"] == "collega",
                   "lucchetto di un collega: Occupato con chi e da quando, e il suo lucchetto resta", fermato)

        _scrivi_lucchetto(c, scadenza=(dt.datetime.now() - dt.timedelta(minutes=1)).replace(microsecond=0).isoformat())
        mio = lucchetto.prendi(c, "griglia", "Analista", attesa=0)
        e.verifica(json.loads(file.read_text(encoding="utf-8"))["id"] == mio["id"], "lucchetto scaduto di un collega: si prende")
        lucchetto.lascia(c, mio)

        io = lucchetto.chi_sono("Analista")
        _scrivi_lucchetto(c, id="vecchio", utente="Analista", pc=io["pc"])
        mio = lucchetto.prendi(c, "griglia", "Analista", attesa=0)
        e.verifica(mio["id"] != "vecchio", "lucchetto proprio rimasto da un comando interrotto (stesso utente e PC): si riprende")
        lucchetto.lascia(c, mio)

        # OneDrive ha creato una copia in conflitto del collega mentre si attendeva: ci si ritira.
        conflitto = c / lucchetto.CARTELLA / "registro-ALTRO-PC.json"
        conflitto.write_text(json.dumps(_scrivi_lucchetto(c) | {"id": "altro"}), encoding="utf-8")
        file.unlink()
        try:
            lucchetto.prendi(c, "griglia", "Analista", attesa=0)
            fermato = None
        except lucchetto.Occupato as ex:
            fermato = str(ex)
        e.verifica(fermato and "nello stesso momento" in fermato and not file.exists(),
                   "lucchetto: copia in conflitto di un collega arrivata durante la presa: ritiro, nessun lucchetto lasciato",
                   fermato)
        conflitto.unlink()

        _scrivi_lucchetto(c)
        tolto = lucchetto.sblocca(c, "PC del collega spento", "Analista")
        log = (c / lucchetto.CARTELLA / lucchetto.REGISTRO_SBLOCCHI).read_text(encoding="utf-8")
        e.verifica(tolto["utente"] == "Collega" and not file.exists() and "Analista" in log and "spento" in log
                   and "Collega" in log, "sblocca: toglie il lucchetto e registra chi, perche' e di chi era", log)


def test_sostituzione(e):
    with tempfile.TemporaryDirectory() as tmp:
        c = Path(tmp)
        originale, copia = c / "NFR_Registro.xlsx", c / "lavoro.xlsx"
        originale.write_bytes(b"registro di prima")
        copia.write_bytes(b"registro scritto dallo script")
        prima = campo.impronta_file(originale)
        originale.write_bytes(b"registro salvato da un collega")
        campo.SALVATO.update(registro=None, backup=None)
        try:
            campo._sostituisci(copia, originale, prima)
            fermato = None
        except campo.Fermo as ex:
            fermato = str(ex)
        e.verifica(fermato and "cambiato" in fermato and originale.read_bytes() == b"registro salvato da un collega"
                   and campo.SALVATO["registro"] is None,
                   "copia di lavoro: registro cambiato nel frattempo -> FERMATO, il registro del collega resta, niente "
                   "segnato come salvato", fermato)
        prima = campo.impronta_file(originale)
        campo._sostituisci(copia, originale, prima)
        e.verifica(originale.read_bytes() == b"registro scritto dallo script" and campo.SALVATO["registro"] == originale
                   and not [f for f in c.iterdir() if f.name.startswith("~$")],
                   "copia di lavoro: registro invariato -> sostituito, segnato come salvato, nessun file temporaneo")
        campo.SALVATO.update(registro=None, backup=None)


def test_aperto_qui(e):
    import win32con
    import win32file
    with tempfile.TemporaryDirectory() as tmp:
        f = Path(tmp) / "NFR_Registro.xlsx"
        f.write_bytes(b"x")
        e.verifica(not campo.aperto_qui(f), "aperto_qui: un file chiuso non e' aperto")
        h = win32file.CreateFile(str(f), win32con.GENERIC_READ, 0, None, win32con.OPEN_EXISTING, 0, None)
        try:
            e.verifica(campo.aperto_qui(f), "aperto_qui: un file tenuto aperto in esclusiva (come fa Excel) e' aperto")
        finally:
            h.Close()


def test_ingresso(e):
    """Ingresso unico delle risposte (tappa M2): estrazione, riconoscimento, nome, salvataggio."""
    import ingresso
    schemi = ingresso.carica_schemi(KERNEL)
    a1 = carica(DATI / "run1_A1_2026Q3.json")
    a3 = carica(DATI / "run_A3_2026-10-12.json")
    a5 = carica(DATI / "run_A5_2026Q3.json")
    a8 = carica(DATI / "run4_A1_2026Q4-S1.json")
    testo_a1 = json.dumps(a1, ensure_ascii=False, indent=2)
    copiato = f"﻿Ecco l'output del ciclo:\n```json\n{testo_a1}\n```\nFammi sapere se serve altro."
    payload, stato = ingresso.estrai_json(copiato, schemi)
    e.verifica(stato == ingresso.OK and payload == a1, "ingresso: JSON di A1 estratto da BOM, frase prima, recinti e frase dopo")
    e.verifica([ingresso.riconosci_agente(p, schemi) for p in (a1, a3, a5, a8)] == ["A1", "A3", "A5", "A8"],
               "ingresso: agente riconosciuto dagli schemi (A8 dal periodo straordinario)")
    e.verifica([ingresso.nome_file(ag, p) for ag, p in (("A1", a1), ("A3", a3), ("A5", a5), ("A8", a8))]
               == ["A1_2026Q3.json", "A3_2026-10-12.json", "A5_2026Q3.json", "A8_2026Q4-S1.json"], "ingresso: nomi dei file")
    meta = len(testo_a1) // 2
    parte1, parte2 = "```json\n" + testo_a1[:meta], testo_a1[meta:] + "\n```"
    _, stato = ingresso.estrai_json(parte1, schemi)
    payload, stato2 = ingresso.estrai_json(ingresso.unisci([parte1, parte2]), schemi)
    e.verifica(stato == ingresso.TRONCATA and stato2 == ingresso.OK and payload == a1,
               "ingresso: risposta tagliata riconosciuta (anche con rischi interi dentro), poi unita nelle due parti")
    with tempfile.TemporaryDirectory() as tmp:
        r = ingresso.ricevi(copiato, schemi, tmp, atteso="A1")
        cartella = Path(tmp) / ingresso.CARTELLA
        e.verifica(r["stato"] == ingresso.OK and r["agente"] == "A1" and not r["errori"] and not r["avviso"]
                   and json.loads((cartella / "A1_2026Q3.json").read_text(encoding="utf-8")) == a1
                   and not (cartella / "A1_2026Q3.json").read_bytes().startswith(b"\xef\xbb\xbf")
                   and len(list((cartella / "Originali").iterdir())) == 1,
                   "ricevi: A1 salvato in In_arrivo con il suo nome, UTF-8 senza BOM, testo originale conservato", r)
        rotto = copy.deepcopy(a1)
        rotto["rischi"][0]["impatto"] = 9
        r2 = ingresso.ricevi(json.dumps(rotto), schemi, tmp, atteso="A1")
        e.verifica(r2["agente"] == "A1" and r2["errori"] and len(list((cartella / "Precedenti").iterdir())) == 1,
                   "ricevi: schema violato salvato lo stesso, con gli errori; il file di prima passa in Precedenti", r2["errori"])
        r3 = ingresso.ricevi(json.dumps(a3), schemi, tmp, atteso="A1")
        e.verifica(r3["agente"] == "A3" and "aspetta A1" in (r3["avviso"] or ""),
                   "ricevi: la risposta di un altro agente si salva ma il passo non avanza (avviso)", r3)
        parere = "## 1. Il fatto\nPROPOSTA DI CICLO STRAORDINARIO: NFR-01...\nUn fornitore cloud..."
        r4 = ingresso.ricevi(parere, schemi, tmp)
        e.verifica(r4["agente"] == "A4" and r4["file"].parent.name == "Pareri" and ingresso.proposta_straordinario(parere),
                   "ricevi: un testo senza JSON e' un parere di A4, archiviato in Pareri; proposta di straordinario vista", r4)
        r5 = ingresso.ricevi("Non ho trovato la baseline.", schemi, tmp, atteso="A3")
        e.verifica(r5["agente"] is None and "non contiene un JSON" in r5["avviso"],
                   "ricevi: un testo senza JSON quando si aspetta A3 non si archivia come parere", r5)
    record = json.dumps({"finishReason": "stop", "text": json.dumps(a1, ensure_ascii=False)}) + "\n\n[1] fonte.pdf"
    payload, stato = ingresso.estrai_json(record, schemi)
    e.verifica(stato == ingresso.OK and payload == a1,
               "ingresso: JSON dentro il campo text di un record di Copilot Studio, con i link alle fonti in coda")
    with tempfile.TemporaryDirectory() as tmp:
        r = ingresso.ricevi(json.dumps(a1), schemi, tmp, atteso="A1", origine="Copilot Studio")
        originali = [f.name for f in (Path(tmp) / ingresso.CARTELLA / "Originali").iterdir()]
        e.verifica(r["origine"] == "Copilot Studio" and r["file"].name == "A1_2026Q3.json"
                   and originali and originali[0].endswith("_CopilotStudio.txt"),
                   "ricevi: con gli agenti di Copilot Studio stesso nome e cartella, origine annotata nell'originale", originali)
    m = ingresso.messaggio_correzione("A3", ["id_notizia ripetuti: N-20261012-01"])
    e.verifica("intero JSON" in m and "- id_notizia ripetuti" in m, "messaggio di correzione per A3, A5, A6", m)


def test_stato(e):
    """Stato del processo e prossimo passo da un archivio finto (tappa M2), senza Excel."""
    import os
    import time
    import stato
    with tempfile.TemporaryDirectory() as tmp:
        u, news = Path(tmp) / "uscita", Path(tmp) / "news"
        u.mkdir()
        conf = {"cartella_uscita": u, "news_inbox": news, "utente": "Analista"}
        oggi = dt.date(2026, 10, 23)                 # venerdi': lunedi' 2026-10-19
        prossimo = lambda g=oggi: stato.leggi(conf, g)["prossimo"]
        scrivi = lambda p, testo="{}": (p.parent.mkdir(parents=True, exist_ok=True), p.write_text(testo, encoding="utf-8"))
        e.verifica(prossimo()["chiave"] == "baseline", "stato: archivio vuoto -> baseline", prossimo())
        scrivi(u / "Baseline_corrente.json", json.dumps({"ciclo_precedente": "2026Q3", "ciclo_da_valutare": "2026Q4"}))
        p = prossimo()
        e.verifica(p["chiave"] == "validazione" and p["chi"] == "validatore" and "2026Q3" in p["titolo"],
                   "stato: ciclo scritto e non validato -> validazione, del validatore", p)
        q3 = u / "Cicli" / "2026Q3"
        scrivi(q3 / "Validazione_2026Q3.json")
        e.verifica(prossimo()["chiave"] == "report", "stato: validato senza report -> report", prossimo())
        time.sleep(0.05)
        scrivi(q3 / "Report_comitato_2026Q3.pdf", "pdf")
        e.verifica(prossimo()["chiave"] == "schede", "stato: report fatto -> schede", prossimo())
        scrivi(q3 / "Schede_2026Q3.xlsx", "x")
        p = prossimo()
        e.verifica(p["chiave"] == "settimanale" and "raccolta" in p["titolo"], "stato: niente sul ciclo -> settimana, raccolta da fare", p)
        scrivi(news / "2026-10-19" / "Raccolta_2026-10-19.txt", "notizie")
        e.verifica(prossimo()["titolo"].endswith(": A3"), "stato: raccolta fatta -> A3", prossimo())
        scrivi(u / "In_arrivo" / "A3_2026-10-19.json")
        e.verifica("scrivere l'output di A3" in prossimo()["titolo"], "stato: A3 copiato -> settimanale", prossimo())
        scrivi(u / "Settimane" / "2026-10-19" / "A3_2026-10-19.json")
        e.verifica(prossimo()["chiave"] == "valida_settimana", "stato: settimana scritta -> validazione facoltativa", prossimo())
        scrivi(u / "Settimane" / "2026-10-19" / "Validazione_2026-10-19.json")
        e.verifica(prossimo()["chiave"] == "niente", "stato: tutto fatto -> niente da fare", prossimo())
        p = prossimo(dt.date(2027, 1, 5))
        e.verifica(p["chiave"] == "trimestrale" and p["titolo"].endswith(": A1"), "stato: trimestre 2026Q4 chiuso -> A1", p)
        scrivi(u / "In_arrivo" / "A1_2026Q4.json")
        e.verifica("scrivere l'output di A1" in prossimo(dt.date(2027, 1, 5))["titolo"], "stato: A1 copiato -> trimestrale")
        scrivi(q3 / "Riapertura_2026Q3.json", json.dumps({"ciclo": "2026Q3", "riaperta_da": "Collega"}))
        s = stato.leggi(conf, dt.date(2027, 1, 5))
        e.verifica(s["prossimo"]["chiave"] == "validazione" and "riapertura" in s["prossimo"]["titolo"]
                   and not any(a["chiave"] == "trimestrale" for a in s["attivita"]) and "RIAPERTO" in s["righe"][0],
                   "stato: riapertura aperta -> validarla prima; il trimestre aspetta", s["attivita"])
        (q3 / "Riapertura_2026Q3.json").unlink()
        os.utime(q3 / "Report_comitato_2026Q3.pdf", (time.time() - 3600, time.time() - 3600))
        e.verifica(not stato.leggi(conf, oggi)["report"], "stato: report piu' vecchio della validazione -> da rifare")
        scrivi(u / "Baseline_corrente.json", json.dumps({"ciclo_precedente": "2026Q3", "ciclo_da_valutare": "2026Q3-S1",
                                                         "straordinario": {"decisore": "Comitato Rischi"}}))
        p = prossimo()
        e.verifica(p["chiave"] == "straordinario" and "A8" in p["titolo"], "stato: straordinario deciso -> A8", p)
        _scrivi_lucchetto(u)
        s = stato.leggi(conf, oggi)
        e.verifica(s["prossimo"]["chiave"] == "attesa" and "Collega" in s["prossimo"]["titolo"] and "in uso" in s["righe"][-1],
                   "stato: un collega scrive -> attendere, e la riga del registro lo dice", s["righe"])
        stato.segna(u, "2026Q4", "A1 richiesto", "Analista")
        e.verifica(stato.passi_segnati(u, "2026Q4")["A1 richiesto"]["da"] == "Analista", "stato: passo segnato con chi e quando")


class AmbienteFinto:
    """L'Ambiente dei flussi senza persona ne' Excel: risposte degli agenti, conferme e moduli da code preparate; il
    motore simulato scrive nell'archivio i file che scriverebbe quello vero (baseline, correzione, validazione)."""

    def __init__(self, uscita, risposte=(), conferme=(), moduli=(), esiti=None):
        self.uscita = Path(uscita)
        self.risposte, self.conferme, self.moduli = list(risposte), list(conferme), list(moduli)
        self.esiti = esiti or {}                     # comando -> lista di (codice, uscita), consumata in ordine
        self.comandi, self.appunti, self.aperti, self.messaggi, self.chiusure = [], [], [], [], []

    def esegui(self, argomenti, script=None):
        comando = argomenti[0] if not script else Path(script).stem
        self.comandi.append(argomenti if not script else [comando, *argomenti])
        coda = self.esiti.get(comando) or [(0, "")]
        codice, uscita = coda.pop(0) if len(coda) > 1 else coda[0]
        if callable(uscita):
            uscita = uscita(self, argomenti)
        fascia = {0: "OK", 1: "FERMATO"}.get(codice, "ERRORE TECNICO")
        return {"codice": codice, "fascia": fascia, "uscita": uscita, "log": None, "dopo_salvataggio": False, "cosa_fare": ""}

    def apri(self, cosa):
        self.aperti.append(str(cosa))

    def copia(self, testo):
        self.appunti.append(testo)

    def risposta(self, agente, istruzioni):
        return self.risposte.pop(0) if self.risposte else None

    def attendi_chiusura(self, file):
        self.chiusure.append(str(file))

    def chiedi(self, titolo, campi):
        return self.moduli.pop(0) if self.moduli else None

    def conferma(self, domanda):
        return self.conferme.pop(0) if self.conferme else False

    def mostra(self, testo, tipo="info"):
        self.messaggi.append((tipo, testo))


def _scrivi(p, dati):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(dati if isinstance(dati, str) else json.dumps(dati), encoding="utf-8")


def test_flussi(e):
    """I processi dell'app (tappa M2) con l'Ambiente finto: ordine dei comandi, allegati, richieste negli appunti,
    giri di correzione."""
    import flussi
    import ingresso
    with tempfile.TemporaryDirectory() as tmp:
        u = Path(tmp) / "uscita"
        conf = {"cartella_uscita": u, "kernel": KERNEL, "news_inbox": Path(tmp) / "news", "workbook": Path(tmp) / "R.xlsx",
                "utente": "Analista", "link_agenti": {"A1": "https://a1", "A3": "https://a3"}, "validatore_predefinito": ""}
        _scrivi(u / "Baseline_corrente.json", {"ciclo_precedente": "2026Q3", "ciclo_da_valutare": "2026Q4"})
        _scrivi(u / "Cicli" / "2026Q3" / "Validazione_2026Q3.json", {})
        a1 = carica(DATI / "run3_A1_2026Q4.json")

        def baseline(amb, arg):
            _scrivi(u / "Input_A1_2026Q4.txt", "allegato di A1")
            return "Baseline scritta"

        def precontrollo_ko(amb, arg):
            _scrivi(u / "Cicli" / "2026Q4" / "Correzione_A1_2026Q4.txt", "Il precontrollo dello script ha trovato...")
            return "Precontrollo dell'output di A1 (2026Q4): 1 punti da correggere, 0 da verificare."

        def trimestrale(amb, arg):
            _scrivi(u / "Baseline_corrente.json", {"ciclo_precedente": "2026Q4", "ciclo_da_valutare": "2027Q1"})
            return "Ciclo 2026Q4 scritto"
        amb = AmbienteFinto(u, risposte=["```json\n" + json.dumps(a1) + "\n```", json.dumps(a1)], conferme=[False],
                            esiti={"baseline": [(0, baseline)], "precontrollo": [(1, precontrollo_ko),
                                   (0, "Precontrollo dell'output di A1 (2026Q4): nessun rilievo.")],
                                   "trimestrale": [(0, trimestrale)]})
        f = flussi.Flussi(amb, conf, cartella_allegati=Path(tmp) / "allegati")
        es = f.trimestrale()
        e.verifica([c[0] for c in amb.comandi] == ["baseline", "precontrollo", "precontrollo", "trimestrale"] and es["fascia"] == "OK",
                   "flusso trimestrale: baseline, A1, precontrollo con un giro di correzione, trimestrale", amb.comandi)
        e.verifica(amb.appunti[0] == "Esegui il ciclo" and amb.appunti[1].startswith("Il precontrollo dello script")
                   and "https://a1" in amb.aperti and (Path(tmp) / "allegati" / "A1" / "Input_A1_2026Q4.txt").exists(),
                   "flusso trimestrale: allegato pronto nella cartella, link di A1 aperto, richiesta e poi correzione negli appunti",
                   amb.appunti)
        e.verifica(amb.comandi[3][2].endswith("A1_2026Q4.json") and (u / ingresso.CARTELLA / "A1_2026Q4.json").exists(),
                   "flusso trimestrale: trimestrale sul file salvato da ingresso", amb.comandi[3])

        # ripresa: la risposta di A1 e' gia' in In_arrivo (processo interrotto), si usa senza richiederla
        _scrivi(u / "Cicli" / "2026Q4" / "Validazione_2026Q4.json", {})
        _scrivi(u / "In_arrivo" / "A1_2027Q1.json", {"ciclo": "2027Q1"})
        amb = AmbienteFinto(u, conferme=[True, False],
                            esiti={"baseline": [(0, "Baseline scritta")],
                                   "precontrollo": [(0, "Precontrollo dell'output di A1 (2027Q1): nessun rilievo.")],
                                   "trimestrale": [(0, "Ciclo 2027Q1 scritto")]})
        flussi.Flussi(amb, conf, cartella_allegati=Path(tmp) / "allegati").trimestrale()
        e.verifica([c[0] for c in amb.comandi] == ["baseline", "precontrollo", "trimestrale"] and not amb.appunti
                   and amb.comandi[1][2].endswith("A1_2027Q1.json"),
                   "flusso ripreso: la risposta gia' copiata si usa (nessuna richiesta ad A1), poi precontrollo e trimestrale",
                   f"{amb.comandi}\n{amb.appunti}")

        # risposta tagliata in due parti
        testo = json.dumps(a1, indent=1)
        amb = AmbienteFinto(u, risposte=[testo[:len(testo) // 2], testo[len(testo) // 2:]])
        r = flussi.Flussi(amb, conf, cartella_allegati=Path(tmp) / "allegati").chiedi_ad_agente("A1", [], "Esegui il ciclo", "2027Q1")
        e.verifica(r["agente"] == "A1" and "continua" in amb.appunti, "flusso: risposta tagliata, 'continua' negli appunti, parti unite", amb.appunti)

        # validazione: registro aperto, chiusura attesa, valida con il validatore del modulo
        amb = AmbienteFinto(u, moduli=[{"validatore": "Comitato Rischi"}], conferme=[False])
        flussi.Flussi(amb, conf).validazione()
        e.verifica(amb.chiusure == [str(conf["workbook"])] and amb.comandi == [["valida", "--periodo", "2026Q4", "--validatore", "Comitato Rischi"]],
                   "flusso validazione: registro aperto e atteso chiuso, valida del ciclo corrente con chi valida", amb.comandi)

        # settimanale: fermo, correzione per A3, poi scritta
        a3 = carica(DATI / "run_A3_2026-10-12.json")
        _scrivi(u / "Input_A3_A4.txt", "allegato di A3 e A4")
        amb = AmbienteFinto(u, risposte=[json.dumps(a3), json.dumps(a3)], conferme=[True, False],
                            esiti={"raccogli_notizie": [(0, "Raccolta scritta")],
                                   "settimanale": [(1, "FERMATO — il workbook non e' stato modificato.\nid_notizia ripetuti: ['N-1']"),
                                                   (0, "Settimana scritta")]})
        flussi.Flussi(amb, dict(conf, raccolta_su_questo_pc=True), cartella_allegati=Path(tmp) / "allegati").settimanale()
        e.verifica([c[0] for c in amb.comandi] == ["raccogli_notizie", "settimanale", "settimanale"]
                   and any("id_notizia ripetuti" in a for a in amb.appunti) and amb.appunti[0] == "Esegui l'aggiornamento settimanale"
                   and (Path(tmp) / "allegati" / "A3" / "Input_A3_A4.txt").exists(),
                   "flusso settimanale: raccolta, A3 con l'allegato, fermo con la correzione per A3, poi scritta",
                   f"{amb.comandi}\n{amb.appunti}")

        # annullato: nessuna risposta
        amb = AmbienteFinto(u)
        try:
            flussi.Flussi(amb, conf).chiedi_ad_agente("A5", [], "Esegui i nove controlli", "2026Q4")
            annullato = False
        except flussi.Annullato:
            annullato = True
        e.verifica(annullato, "flusso: senza risposta il processo si interrompe (Annullato), niente di scritto")


def test_cmd(e):
    """I lanciatori .cmd: solo ASCII, cartella dello script, UTF-8 (trappola dei .cmd con accenti)."""
    for nome in ("NFR.cmd",):
        p = CAMPO / nome
        if not p.exists():
            e.verifica(False, f"{nome} presente in 07_Senza_Studio")
            continue
        b = p.read_bytes()
        testo = b.decode("ascii", errors="replace")
        e.verifica(all(c < 128 for c in b) and "%~dp0" in testo and "chcp 65001" in testo and "app_nfr.py" in testo,
                   f"{nome}: solo ASCII, parte dalla sua cartella, UTF-8, lancia app_nfr.py")


def main():
    e = Esito("Orchestrazione per piu' analisti: lucchetto, copia di lavoro, ingresso, stato, flussi (senza Excel)")
    test_lucchetto(e)
    test_sostituzione(e)
    test_aperto_qui(e)
    test_ingresso(e)
    test_stato(e)
    test_flussi(e)
    test_cmd(e)
    return 0 if e.stampa() else 1


if __name__ == "__main__":
    sys.exit(main())
