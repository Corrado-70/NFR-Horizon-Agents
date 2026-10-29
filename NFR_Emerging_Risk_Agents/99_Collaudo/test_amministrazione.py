"""Test senza Excel delle funzioni amministrative (D-83, tappa M5, 29/10/2026) su un archivio finto.

  1. solo il manutentore ("ruolo": "manutentore");
  2. pulizia: anteprima di cio' che si sposta (tentativi e versioni dei report dei cicli validati, backup oltre gli
     ultimi N, In_arrivo dei periodi chiusi, log vecchi), parcheggio con l'atto e la traccia, annullamento;
  3. ritorno indietro: controlli (ciclo validato, Excel validato, prima del corrente, motivo e decisore), registro
     tornato quello validato, nel parcheggio cio' che viene dopo (cicli, settimane scritte dopo la validazione,
     baseline, allegati, knowledge di A7, risposte in In_arrivo); lo stato dell'app riparte dal ciclo validato;
  4. annullamento del ritorno: rifiutato se nel frattempo si e' scritto nel registro; altrimenti tutto torna com'era e
     cio' che occupava i posti va in un parcheggio nuovo; un parcheggio annullato non si annulla due volte;
  5. ripartenza da zero: registro e archivio dei cicli nel parcheggio (log, parcheggi, traccia e lucchetto restano);
  6. svuota: solo i parcheggi piu' vecchi del minimo, con l'elenco nella traccia;
  7. conferma scritta: un nome diverso ferma prima di toccare qualcosa.
Ritorno e ripartenza con Excel (baseline e inizializza veri) sono nella catena (run_catena.py, gruppo amministrazione).

Uso: python test_amministrazione.py [-v]
"""

import argparse
import datetime as dt
import json
import os
import sys
import tempfile
import time
from pathlib import Path

from comune import Esito
import amministrazione as amm
import stato

ORA = time.time()


def scrivi(p, testo="x", eta_giorni=0):
    p = Path(p)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(testo if isinstance(testo, str) else json.dumps(testo), encoding="utf-8")
    if eta_giorni:
        os.utime(p, (ORA - eta_giorni * 86400, ORA - eta_giorni * 86400))
    return p


def archivio(t):
    """Un archivio finto: 2026Q2 e 2026Q3 validati, 2026Q4 scritto e da validare, due settimane, backup, log."""
    u, k = t / "Archivio_Cicli", t / "Kernel"
    reg = t / "Report" / "NFR_Registro.xlsx"
    conf = {"cartella_uscita": u, "workbook": reg, "kernel": k, "news_inbox": t / "News", "utente": "Manutentore"}
    grezza = {"ruolo": "manutentore", "utente": "Manutentore", "backup_da_tenere": 3, "giorni_log": 90, "giorni_parcheggio": 30}
    scrivi(reg, "registro di adesso (2026Q4 scritto)")
    for c, eta in (("2026Q2", 120), ("2026Q3", 30)):
        scrivi(u / "Cicli" / c / f"Validazione_{c}.json", {"periodo": c}, eta)
        scrivi(u / "Cicli" / c / f"NFR_Registro_{c}_validato.xlsx", f"registro validato {c}", eta)
        scrivi(u / "Cicli" / c / f"tentativo_2026{eta}" / f"A1_{c}.json", "{}", eta)
        scrivi(u / "Cicli" / c / f"Report_comitato_{c}.pdf", "pdf", eta)
        scrivi(u / "Cicli" / c / f"Report_comitato_{c}_20261001_120000.pdf", "pdf vecchio", eta)
    scrivi(u / "Cicli" / "2026Q4" / "NFR_Registro_2026Q4.xlsx", "registro 2026Q4", 5)
    scrivi(u / "Cicli" / "2026Q4" / "tentativo_x" / "A1.json", "{}", 5)      # ciclo non validato: il tentativo resta
    scrivi(u / "Settimane" / "2026-09-21" / "A3_2026-09-21.json", "{}", 40)   # prima della validazione del 2026Q3
    scrivi(u / "Settimane" / "2026-10-19" / "A3_2026-10-19.json", "{}", 10)   # dopo
    for i in range(5):
        scrivi(u / "Backup" / f"NFR_Registro_{i}.xlsx", f"backup {i}", 10 + i)
    scrivi(u / "In_arrivo" / "A1_2026Q4.json", "{}", 6)
    scrivi(u / "In_arrivo" / "Originali" / "A1_2026Q2_Agent_Builder.txt", "testo", 121)
    scrivi(u / "In_arrivo" / "Originali" / "A1_2026Q4_Agent_Builder.txt", "testo", 6)
    scrivi(u / "In_arrivo" / "Originali" / "senza_periodo.txt", "testo", 200)
    scrivi(u / "Log" / "vecchio.txt", "log", 100)
    scrivi(u / "Log" / "nuovo.txt", "log", 1)
    scrivi(u / "Baseline_corrente.json", {"ciclo_precedente": "2026Q4", "ciclo_da_valutare": "2027Q1"})
    scrivi(u / "Input_A1_2027Q1.txt", "allegato")
    scrivi(k / "Spiegazioni" / "Ciclo.txt", "knowledge del 2026Q4")
    return conf, grezza


def test_ruolo(e):
    try:
        amm.controlla_ruolo({"ruolo": "analista"})
        fermo = False
    except amm.Fermo:
        fermo = True
    e.verifica(fermo and amm.autorizzato({"ruolo": "Manutentore"}), "solo il manutentore (ruolo in configurazione.json)")


def test_pulizia(e, conf, grezza):
    u = conf["cartella_uscita"]
    scelti = amm.da_pulire(conf, grezza)
    nomi = sorted(p.relative_to(u).as_posix() for p, _ in scelti)
    attesi = sorted(["Cicli/2026Q2/tentativo_2026120", "Cicli/2026Q3/tentativo_202630",
                     "Cicli/2026Q2/Report_comitato_2026Q2_20261001_120000.pdf",
                     "Cicli/2026Q3/Report_comitato_2026Q3_20261001_120000.pdf",
                     "Backup/NFR_Registro_3.xlsx", "Backup/NFR_Registro_4.xlsx",
                     "In_arrivo/Originali/A1_2026Q2_Agent_Builder.txt", "In_arrivo/Originali/senza_periodo.txt",
                     "Log/vecchio.txt"])
    e.verifica(nomi == attesi, "pulizia: tentativi e report vecchi dei cicli validati, backup oltre gli ultimi 3, In_arrivo "
               "dei periodi chiusi (o vecchio senza periodo), log oltre 90 giorni; il ciclo da validare non si tocca",
               f"{nomi}\n{attesi}")
    anteprima = amm.testo_anteprima(scelti, "Pulizia")
    e.verifica("9 elementi" in anteprima and "backup oltre gli ultimi 3: 2" in anteprima,
               "pulizia: anteprima con quanti elementi, lo spazio e il perche'", anteprima)
    cartella, atto = amm.parcheggia(conf, grezza, "pulizia", [p for p, _ in scelti], "pulizia dell'archivio")
    e.verifica(not any((u / n).exists() for n in attesi) and all((cartella / "archivio" / n).exists() for n in attesi)
               and (cartella / "atto.json").exists() and list((u / amm.TRACCIA).glob("*_pulizia.json"))
               and atto["utente"] == "Manutentore" and len(atto["elementi"]) == 9,
               "pulizia: tutto nel parcheggio con i percorsi di prima, l'atto (chi, ogni file) e la traccia")
    atto, _ = amm.annulla(conf, grezza, cartella.name, "rimessi per la prova")
    e.verifica(all((u / n).exists() for n in attesi) and atto["stato"] == "annullato",
               "pulizia annullata: ogni file al suo posto, l'atto dice annullato")


def test_ritorno(e, conf, grezza):
    u, reg = conf["cartella_uscita"], conf["workbook"]

    def fermo(**k):
        try:
            amm.ritorno(conf, grezza, **{"ciclo": "2026Q3", "motivo": "ritorno di prova, cicli di collaudo", "decisore": "Comitato",
                                          "corrente": "2026Q4", **k})
            return None
        except amm.Fermo as ex:
            return str(ex)
    e.verifica(all([fermo(ciclo="2026Q4"), fermo(ciclo="2026Q1"), fermo(ciclo="2026Q4", corrente="2026Q4"),
                    fermo(motivo="corto"), fermo(decisore=" ")]) and reg.read_text(encoding="utf-8").startswith("registro di adesso"),
               "ritorno: fermo per un ciclo non validato, senza il suo Excel, non prima del corrente, motivo corto, senza "
               "decisore; niente toccato")
    rigenerati = []

    def rigenera(c):
        rigenerati.append(True)
        scrivi(u / "Baseline_corrente.json", {"ciclo_precedente": "2026Q3", "ciclo_da_valutare": "2026Q4"})
        scrivi(Path(c["kernel"]) / "Spiegazioni" / "Ciclo.txt", "knowledge del 2026Q3")
    cartella, atto, settimane = amm.ritorno(conf, grezza, "2026Q3", "ritorno di prova, cicli di collaudo", "Comitato",
                                            "2026Q4", rigenera)
    dentro = lambda *p: (cartella.joinpath(*p)).exists()
    e.verifica(reg.read_text(encoding="utf-8") == "registro validato 2026Q3" and rigenerati
               and atto["impronta_registro_dopo"] == amm.impronta(reg),
               "ritorno: il registro e' l'Excel validato del 2026Q3; baseline e knowledge rigenerate; impronta nell'atto")
    e.verifica(dentro("registro", "NFR_Registro.xlsx") and dentro("archivio", "Cicli", "2026Q4")
               and dentro("archivio", "Settimane", "2026-10-19") and not dentro("archivio", "Settimane", "2026-09-21")
               and dentro("archivio", "Baseline_corrente.json") and dentro("archivio", "Input_A1_2027Q1.txt")
               and dentro("spiegazioni", "Spiegazioni", "Ciclo.txt") and dentro("archivio", "In_arrivo", "A1_2026Q4.json")
               and (u / "Cicli" / "2026Q3").exists() and (u / "Settimane" / "2026-09-21").exists(),
               "ritorno: nel parcheggio il registro di prima, il 2026Q4, la settimana scritta dopo la validazione, baseline, "
               "allegati, knowledge di A7, la risposta di A1 del 2026Q4; restano il 2026Q3 e la settimana prima",
               "\n".join(sorted(str(p.relative_to(cartella)) for p in cartella.rglob("*"))))
    e.verifica([s.name for s in settimane] == ["2026-10-19"] and atto["settimane"] == ["2026-10-19"],
               "ritorno: le settimane uscite dal registro sono elencate (per riscriverle con settimanale)")
    s = stato.leggi({**conf, "news_inbox": conf["news_inbox"]})
    e.verifica(s["ciclo_corrente"] == "2026Q3" and s["validato"], "ritorno: lo stato dell'app riparte da 'Ciclo 2026Q3: VALIDATO'",
               s["righe"])
    return cartella


def test_annulla_ritorno(e, conf, grezza, cartella):
    u, reg = conf["cartella_uscita"], conf["workbook"]
    reg.write_text("qualcuno ha scritto", encoding="utf-8")
    try:
        amm.annulla(conf, grezza, cartella.name, "annullo il ritorno di prova")
        fermo = None
    except amm.Fermo as ex:
        fermo = str(ex)
    e.verifica(fermo and "scritto nel registro" in fermo and (cartella / "registro" / "NFR_Registro.xlsx").exists(),
               "annulla: rifiutato se dopo il ritorno qualcuno ha scritto nel registro; niente toccato", fermo)
    reg.write_text("registro validato 2026Q3", encoding="utf-8")
    atto, nuovo = amm.annulla(conf, grezza, cartella.name, "annullo il ritorno di prova")
    e.verifica(reg.read_text(encoding="utf-8").startswith("registro di adesso") and (u / "Cicli" / "2026Q4").exists()
               and json.loads((u / "Baseline_corrente.json").read_text(encoding="utf-8"))["ciclo_precedente"] == "2026Q4"
               and (Path(conf["kernel"]) / "Spiegazioni" / "Ciclo.txt").read_text(encoding="utf-8") == "knowledge del 2026Q4"
               and (u / "Settimane" / "2026-10-19").exists() and (u / "In_arrivo" / "A1_2026Q4.json").exists(),
               "annulla: registro, 2026Q4, settimana, baseline, knowledge e risposte tornano com'erano")
    e.verifica(nuovo and (nuovo / "registro" / "NFR_Registro.xlsx").read_text(encoding="utf-8") == "registro validato 2026Q3"
               and (nuovo / "archivio" / "Baseline_corrente.json").exists(),
               "annulla: il registro tornato e la baseline rigenerata vanno in un parcheggio nuovo (nemmeno l'annullamento "
               "cancella)")
    try:
        amm.annulla(conf, grezza, cartella.name, "di nuovo, per prova")
        due = False
    except amm.Fermo:
        due = True
    e.verifica(due and stato.leggi(conf)["ciclo_corrente"] == "2026Q4", "annulla: un parcheggio annullato non si annulla due "
               "volte; lo stato e' di nuovo al 2026Q4")


def test_ripartenza(e, conf, grezza):
    u, reg = conf["cartella_uscita"], conf["workbook"]

    def crea(c):
        scrivi(reg, "registro nuovo vuoto")
        scrivi(u / "Baseline_corrente.json", {"ciclo_precedente": "2026Q4", "ciclo_da_valutare": "2027Q1"})
    cartella, atto = amm.ripartenza(conf, grezza, "ripartenza dopo i cicli di prova", "Responsabile", crea)
    restano = sorted(p.name for p in u.iterdir())
    e.verifica(reg.read_text(encoding="utf-8") == "registro nuovo vuoto" and (cartella / "registro" / "NFR_Registro.xlsx").exists()
               and (cartella / "archivio" / "Cicli" / "2026Q3").exists() and (cartella / "archivio" / "Backup").exists()
               and set(restano) == {"Log", amm.PARCHEGGIO, amm.TRACCIA, "Baseline_corrente.json"}
               and (cartella / "spiegazioni" / "Spiegazioni").exists(),
               "ripartenza: registro nuovo; il vecchio, i cicli, le settimane, i backup, In_arrivo e la knowledge nel "
               "parcheggio; restano log, parcheggi e traccia", restano)
    atto, nuovo = amm.annulla(conf, grezza, cartella.name, "annullo la ripartenza di prova")
    e.verifica(reg.read_text(encoding="utf-8").startswith("registro di adesso") and (u / "Cicli" / "2026Q3").exists()
               and (nuovo / "registro" / "NFR_Registro.xlsx").read_text(encoding="utf-8") == "registro nuovo vuoto",
               "ripartenza annullata: il vecchio registro e l'archivio tornano; il registro nuovo nel parcheggio")


def test_svuota(e, conf, grezza):
    tutti = amm.elenco_parcheggi(conf)
    e.verifica(not amm.da_svuotare(conf, grezza), "svuota: nessun parcheggio piu' giovane di 30 giorni si cancella")
    fra_un_mese = dt.datetime.now() + dt.timedelta(days=31)
    atto = amm.svuota(conf, grezza, "svuota di prova", adesso=fra_un_mese)
    tracce = sorted((conf["cartella_uscita"] / amm.TRACCIA).glob("*_svuota.json"))
    e.verifica(len(atto["cancellati"]) == len(tutti) > 0 and not amm.elenco_parcheggi(conf) and tracce
               and len(json.loads(tracce[-1].read_text(encoding="utf-8"))["cancellati"]) == len(tutti),
               f"svuota: dopo 30 giorni i {len(tutti)} parcheggi si cancellano; l'elenco resta nella traccia")


def test_conferma(e, conf, grezza):
    arg = argparse.Namespace(comando="ritorno", ciclo="2026Q3", conferma="2026Q2", motivo="x" * 30, decisore="Comitato")
    try:
        amm.esegui(arg, conf, grezza)
        fermo = None
    except amm.Fermo as ex:
        fermo = str(ex)
    arg = argparse.Namespace(comando="ripartenza", conferma="altro.xlsx", motivo="x" * 30, decisore="R",
                             ciclo_precedente="2026Q3", settimana=None)
    try:
        amm.esegui(arg, conf, grezza)
        fermo2 = None
    except amm.Fermo as ex:
        fermo2 = str(ex)
    e.verifica(fermo and "riscriverlo uguale" in fermo and fermo2 and "nome del registro" in fermo2
               and conf["workbook"].read_text(encoding="utf-8").startswith("registro di adesso"),
               "conferma scritta: un ciclo o un nome del registro diverso ferma prima di toccare qualcosa")


def main():
    e = Esito("Funzioni amministrative: parcheggio, pulizia, ritorno, annulla, ripartenza, svuota (senza Excel)")
    test_ruolo(e)
    with tempfile.TemporaryDirectory() as tmp:
        conf, grezza = archivio(Path(tmp))
        test_pulizia(e, conf, grezza)
        cartella = test_ritorno(e, conf, grezza)
        test_annulla_ritorno(e, conf, grezza, cartella)
        test_ripartenza(e, conf, grezza)
        test_conferma(e, conf, grezza)
        test_svuota(e, conf, grezza)
    return 0 if e.stampa() else 1


if __name__ == "__main__":
    sys.exit(main())
