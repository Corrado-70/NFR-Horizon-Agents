"""I processi dell'app NFR come sequenze di passi (D-83, tappa M2; TODO AU5).

Ogni processo (settimana, trimestre, straordinario, validazione, schede e report, riapertura, testi a mano,
dismissione, parere di A4...) e' una funzione che parla con il mondo solo attraverso un Ambiente:
  - esegui(argomenti, script=None)  lancia il motore (esecutore.py) e restituisce l'esito;
  - apri(cosa)                      apre un file, una cartella o il link di un agente;
  - copia(testo)                    mette un testo negli appunti (la richiesta per l'agente, una correzione);
  - risposta(agente, istruzioni)    aspetta la risposta copiata dall'agente (appunti o file); None = annullato;
  - attendi_chiusura(file)          aspetta che il registro aperto in Excel sia chiuso;
  - chiedi(titolo, campi)           un modulo da compilare (dict) o None;
  - conferma(domanda)               si' o no;
  - mostra(testo, tipo)             un messaggio (info, avviso, errore, ok).
La finestra (app_nfr.py) realizza l'Ambiente con tkinter; il collaudo con un Ambiente finto, senza persona ne' Excel.
Le regole restano nel motore: qui c'e' solo l'ordine dei passi, i nomi dei file e i testi da dare agli agenti.

Gli agenti restano in Agent Builder: per ognuno l'app prepara i file da allegare in una cartella
(%USERPROFILE%/NFR_Da_allegare/<agente>), apre la cartella e il link dell'agente, mette la richiesta negli appunti e
aspetta la risposta. Tre gesti per l'analista: trascinare i file, incollare la richiesta, premere Copia.
"""

import argparse
import datetime as dt
import json
import os
import shutil
from pathlib import Path

import esecutore
import ingresso
import stato

QUI = Path(__file__).resolve().parent

# Messaggi base degli agenti (guida, sezione 8).
MESSAGGI = {"A1": "Esegui il ciclo", "A8": "Esegui il ciclo straordinario", "A3": "Esegui l'aggiornamento settimanale",
            "A5": "Esegui i nove controlli", "A6": "Scrivi le schede", "A4": "Dammi il parere su questa notizia: "}
NOMI = {"A1": "A1 Horizon Scanner", "A3": "A3 Interim Update", "A4": "A4 News Assessor", "A5": "A5 Challenger",
        "A6": "A6 Schede dei rischi", "A7": "A7 Assistente del registro", "A8": "A8 Evento critico"}


class Annullato(Exception):
    """L'analista ha interrotto il processo: niente di male, si riprende dal passo giusto."""


def configurazione():
    """Le chiavi del motore (esegui_ciclo_locale.configurazione) piu' quelle dell'app da configurazione.json:
    link_agenti (piatto o per versione degli agenti), validatore_predefinito, raccolta_su_questo_pc, agenti (Agent Builder
    o Copilot Studio: la versione in uso all'avvio), ascolta_appunti."""
    import esegui_ciclo_locale
    conf = esegui_ciclo_locale.configurazione(argparse.Namespace())
    grezza = {}
    if (QUI / "configurazione.json").exists():
        grezza = json.loads((QUI / "configurazione.json").read_text(encoding="utf-8-sig"))
    conf.update(link_agenti=grezza.get("link_agenti") or {}, validatore_predefinito=grezza.get("validatore_predefinito") or "",
                raccolta_su_questo_pc=bool(grezza.get("raccolta_su_questo_pc", True)),
                agenti=grezza.get("agenti") if grezza.get("agenti") in ingresso.ORIGINI else ingresso.ORIGINI[0],
                ascolta_appunti=bool(grezza.get("ascolta_appunti", True)))
    return conf


class Flussi:
    def __init__(self, amb, conf, schemi=None, cartella_allegati=None):
        self.amb, self.conf = amb, conf
        self.origine = conf.get("agenti") or ingresso.ORIGINI[0]      # Agent Builder o Copilot Studio (si annota)
        self.uscita = Path(conf["cartella_uscita"])
        self.schemi = schemi or ingresso.carica_schemi(conf["kernel"])
        self.allegati = Path(cartella_allegati or Path(os.environ.get("USERPROFILE") or Path.home()) / "NFR_Da_allegare")

    # ------------------------------------------------------------ mattoni
    def esito(self, testo, tipo):
        """La riga sotto il riquadro della risposta (se l'Ambiente la ha: la finestra si', il collaudo no)."""
        funzione = getattr(self.amb, "esito_risposta", None)
        if funzione:
            funzione(testo, tipo)

    def motore(self, *argomenti, script=None):
        """Lancia un comando; mostra l'esito; restituisce il dict dell'esecutore."""
        esito = self.amb.esegui([str(a) for a in argomenti], script)
        tipo = {"OK": "ok", "FERMATO": "avviso"}.get(esito["fascia"], "errore")
        nome = Path(script).stem if script else next((str(a) for a in argomenti if not str(a).startswith("-")), "")
        self.amb.mostra(f"{nome}: {esito['fascia']}. {esito['cosa_fare']}", tipo)
        return esito

    def link(self, agente):
        """Il link dell'agente nella versione in uso: link_agenti piatto ({"A1": ...}) oppure per versione
        ({"Agent Builder": {...}, "Copilot Studio": {...}})."""
        link = self.conf.get("link_agenti") or {}
        if self.origine in link and isinstance(link[self.origine], dict):
            link = link[self.origine]
        return str(link.get(agente) or "")

    def prepara_allegati(self, agente, file):
        cartella = self.allegati / agente
        if cartella.exists():
            shutil.rmtree(cartella, ignore_errors=True)
        cartella.mkdir(parents=True, exist_ok=True)
        for f in file:
            shutil.copy2(f, cartella / Path(f).name)
        return cartella

    def chiedi_ad_agente(self, agente, file, messaggio, periodo, nuova_chat=True, atteso=None):
        """Prepara gli allegati, apre la cartella e l'agente, mette la richiesta negli appunti, aspetta la risposta.
        Unisce le parti di una risposta tagliata. Restituisce l'esito di ingresso.ricevi (agente atteso, file salvato)."""
        atteso = atteso or agente
        if nuova_chat:
            cartella = self.prepara_allegati(agente, file)
            if file:
                self.amb.apri(cartella)
            link = self.link(agente)
            if link.startswith("http"):                # un segnaposto non compilato non si apre
                self.amb.apri(link)
            self.amb.copia(messaggio)
            stato.segna(self.uscita, periodo, f"{agente} richiesto", self.conf.get("utente"))
            istruzioni = (f"{NOMI.get(agente, agente)} ({self.origine}): chat nuova" + (f", trascina i file della cartella {cartella}" if file else "")
                          + ", incolla la richiesta (e' negli appunti) e invia. Poi copia la risposta e incollala qui sotto "
                          "(Ctrl+V), oppure premi Copia sotto la risposta: l'app la prende da sola.")
        else:
            istruzioni = (f"Nella stessa chat di {NOMI.get(agente, agente)}: incolla il messaggio (e' negli appunti) e invia. "
                          "Poi copia la risposta e incollala qui sotto (o premi Copia).")
        parti = []
        while True:
            testo = self.amb.risposta(atteso, istruzioni)
            if testo is None:
                raise Annullato(f"risposta di {atteso} non arrivata")
            parti.append(testo)
            r = ingresso.ricevi(ingresso.unisci(parti) if len(parti) > 1 else testo, self.schemi, self.uscita, atteso,
                                self.origine)
            if r["stato"] == ingresso.TRONCATA:
                self.esito(f"Risposta tagliata ({sum(len(p) for p in parti):,} caratteri finora): nella stessa chat scrivi "
                           "\"continua\" (e' negli appunti) e incolla qui il resto.".replace(",", "."), "avviso")
                self.amb.copia("continua")
                istruzioni = (f"La risposta di {atteso} e' tagliata: scrivi \"continua\" nella stessa chat (e' negli appunti), "
                              "poi premi Copia sotto il resto della risposta.")
                continue
            if r["agente"] != atteso:
                self.esito(r["avviso"] or f"Non e' la risposta di {atteso}.", "avviso")
                self.amb.mostra(r["avviso"] or f"Non e' la risposta di {atteso}.", "avviso")
                parti = []
                continue
            if r["errori"] and atteso not in ("A1", "A8"):     # A1 e A8: lo schema lo guarda il precontrollo
                self.amb.copia(ingresso.messaggio_correzione(atteso, r["errori"]))
                self.esito(f"Risposta di {atteso} salvata ma non rispetta lo schema ({len(r['errori'])} punti): il "
                           "messaggio di correzione e' negli appunti.", "avviso")
                self.amb.mostra(f"La risposta di {atteso} non rispetta lo schema ({len(r['errori'])} punti): il messaggio "
                                "di correzione e' negli appunti.", "avviso")
                parti = []
                istruzioni = (f"Nella stessa chat di {NOMI.get(atteso, atteso)}: incolla il messaggio di correzione e invia. "
                              "Poi premi Copia sotto la risposta.")
                continue
            stato.segna(self.uscita, periodo, f"{atteso} ricevuto", self.conf.get("utente"), f"{r['file']} ({self.origine})")
            lunghezza = len(ingresso.unisci(parti) if len(parti) > 1 else testo)
            self.esito(f"Ricevuto: {atteso} ({self.origine}), {lunghezza:,} caratteri, salvato in ".replace(",", ".")
                       + (f"{Path(r['file']).parent.name}\\{Path(r['file']).name}" if r.get("file") else "In_arrivo"), "ok")
            return r

    def gia_copiata(self, agente, nome):
        """Una risposta gia' in In_arrivo (processo interrotto e ripreso): si usa se l'analista conferma."""
        file = self.uscita / ingresso.CARTELLA / nome
        if file.exists() and self.amb.conferma(f"In In_arrivo c'e' gia' la risposta di {agente} ({nome}). Usarla senza "
                                               f"richiederla ad {agente}?"):
            return {"stato": ingresso.OK, "agente": agente, "file": file, "errori": [], "avviso": None}
        return None

    def correzione_a1(self, ciclo):
        return self.uscita / "Cicli" / ciclo / f"Correzione_A1_{ciclo}.txt"

    def registro_in_excel(self):
        """Apre il registro visibile (per la griglia o i testi) e aspetta che l'analista lo chiuda."""
        self.amb.apri(self.conf["workbook"])
        self.amb.attendi_chiusura(self.conf["workbook"])

    # ------------------------------------------------------------ processi
    def valutazione(self, periodo, agente, file_agente, con_a5=False):
        """A1 (o A8) -> precontrollo con il giro di correzione -> A5 facoltativo -> trimestrale (con il suo giro)."""
        r = (self.gia_copiata(agente, f"{agente}_{periodo}.json")
             or self.chiedi_ad_agente(agente, file_agente, MESSAGGI[agente], periodo))
        while True:
            pre = self.motore("precontrollo", "--payload", r["file"])
            conti = esecutore.esito_precontrollo(pre["uscita"])
            if pre["fascia"] == "ERRORE TECNICO" or conti is None:
                raise Annullato("precontrollo non riuscito")
            da_correggere, da_verificare = conti
            if not da_correggere and not (da_verificare and self.amb.conferma(
                    f"Il precontrollo ha {da_verificare} punti da verificare (andrebbero in validazione come segnalazioni). "
                    f"Farli rivedere prima ad {agente}?")):
                break
            self.amb.copia(self.correzione_a1(periodo).read_text(encoding="utf-8"))
            r = self.chiedi_ad_agente(agente, [], "", periodo, nuova_chat=False)
        a5 = None
        if con_a5:
            a5 = self.chiedi_ad_agente("A5", [self.uscita / f"Input_A5_{periodo}.txt"], MESSAGGI["A5"], periodo)
        while True:
            argomenti = ["trimestrale", "--payload", r["file"]] + (["--challenger", a5["file"]] if a5 else [])
            es = self.motore(*argomenti)
            if es["fascia"] != "FERMATO" or not self.correzione_a1(periodo).exists():
                return es
            self.amb.copia(self.correzione_a1(periodo).read_text(encoding="utf-8"))
            r = self.chiedi_ad_agente(agente, [], "", periodo, nuova_chat=False)
            if a5:
                a5 = self.chiedi_ad_agente("A5", [self.uscita / f"Input_A5_{periodo}.txt"], MESSAGGI["A5"], periodo)

    def trimestrale(self, con_a5=False):
        s = stato.leggi(self.conf)
        if s["ciclo_corrente"] and (not s["validato"] or s["riapertura"]):
            self.amb.mostra(f"Il ciclo {s['ciclo_corrente']} non e' validato: prima la validazione.", "avviso")
            return None
        if self.motore("baseline")["fascia"] != "OK":
            return None
        ciclo = stato.leggi(self.conf)["da_valutare"]
        es = self.valutazione(ciclo, "A1", [self.uscita / f"Input_A1_{ciclo}.txt"], con_a5)   # nomi: input_a1, D-84
        if es["fascia"] == "OK" and self.amb.conferma(f"Ciclo {ciclo} scritto. Passare alla validazione adesso?"):
            return self.validazione()
        return es

    def straordinario(self, con_a5=False):
        dati = self.amb.chiedi("Ciclo straordinario (decide la funzione di rischio)", [
            ("rischi", "Rischi da rivalutare, separati da virgole (vuoto = solo censimento di rischi nuovi)", ""),
            ("motivo", "L'evento e perche' non puo' aspettare il trimestre (almeno 20 caratteri)", ""),
            ("decisore", "Chi decide (funzione o comitato)", self.conf.get("validatore_predefinito") or ""),
            ("data", "Data di riferimento AAAA-MM-GG (vuoto = oggi)", "")])
        if not dati:
            return None
        argomenti = ["baseline", "--straordinario", "--motivo", dati["motivo"], "--decisore", dati["decisore"]]
        argomenti += (["--rischi", dati["rischi"]] if dati.get("rischi") else []) + (["--data", dati["data"]] if dati.get("data") else [])
        if self.motore(*argomenti)["fascia"] != "OK":
            return None
        periodo = stato.leggi(self.conf)["da_valutare"]
        self.amb.mostra(f"Per A8 servono anche i documenti dell'evento: trascinali nella chat insieme a Input_A8_{periodo}.txt.", "info")
        es = self.valutazione(periodo, "A8", [self.uscita / f"Input_A8_{periodo}.txt"], con_a5)
        if es["fascia"] == "OK" and self.amb.conferma(f"Straordinario {periodo} scritto. Passare alla validazione adesso?"):
            return self.validazione()
        return es

    def validazione(self, periodo=None):
        s = stato.leggi(self.conf)
        periodo = periodo or s["ciclo_corrente"]
        if not periodo:
            self.amb.mostra("Niente da validare.", "info")
            return None
        validatore = self.conf.get("validatore_predefinito")
        dati = self.amb.chiedi(f"Validazione del periodo {periodo}", [("validatore", "Chi valida (funzione o comitato)", validatore or "")])
        if not dati or not dati.get("validatore"):
            return None
        self.amb.mostra("Si apre il registro sul foglio Validazione: cambia solo le celle gialle, la Motivazione e Respingi; "
                        "poi salva e chiudi Excel.", "info")
        while True:
            self.registro_in_excel()
            es = self.motore("valida", "--periodo", periodo, "--validatore", dati["validatore"])
            if es["fascia"] != "FERMATO" or not self.amb.conferma("La validazione non e' applicata (motivi qui sopra). "
                                                                   "Riaprire il registro per correggere la griglia?"):
                break
        if es["fascia"] == "OK" and "Q" in periodo and self.amb.conferma("Validato. Fare adesso le schede dei rischi?"):
            self.schede()
        return es

    def schede(self):
        if self.motore("schede-input")["fascia"] != "OK":
            return None
        ciclo = stato.leggi(self.conf)["ciclo_corrente"]
        if self.amb.conferma("Usare A6 per i testi delle schede? (No = schede con i testi di A1 dal registro)"):
            r = (self.gia_copiata("A6", f"A6_{ciclo}.json")
                 or self.chiedi_ad_agente("A6", [self.uscita / "Cicli" / ciclo / f"Input_A6_{ciclo}.json"], MESSAGGI["A6"], ciclo))
            while True:
                es = self.motore("schede", "--payload", r["file"])
                if es["fascia"] != "FERMATO":
                    break
                self.amb.copia(ingresso.messaggio_correzione("A6", [x.strip(" -") for x in es["uscita"].splitlines()
                                                                     if x.strip().startswith("- ")]))
                r = self.chiedi_ad_agente("A6", [], "", ciclo, nuova_chat=False)
        else:
            es = self.motore("schede")
        if not stato.leggi(self.conf)["report"]:
            self.motore("report")
        self.amb.apri(self.uscita / "Cicli" / ciclo)
        return es

    def report(self):
        es = self.motore("report")
        ciclo = stato.leggi(self.conf)["ciclo_corrente"]
        if es["fascia"] == "OK" and ciclo:
            self.amb.apri(self.uscita / "Cicli" / ciclo)
        return es

    def settimanale(self):
        s = stato.leggi(self.conf)
        lun = s["settimana"]["lunedi"]
        news = Path(self.conf.get("news_inbox"))
        if not s["settimana"]["raccolta"]:
            if self.conf.get("raccolta_su_questo_pc", True):
                self.motore("--news-inbox", news, script=esecutore.RACCOLTA)
            else:
                self.amb.mostra("La raccolta delle notizie non e' ancora arrivata (gira su un altro PC): si puo' "
                                "proseguire con i soli file manuali e i siti di A3.", "avviso")
        manuali = news / lun / "Manuali"
        manuali.mkdir(parents=True, exist_ok=True)
        self.amb.apri(manuali)
        if not self.amb.conferma("Aggiunti in Manuali i file che non arrivano dai feed (circolari, rapporti)? "
                                 "Si' per proseguire con A3."):
            return None
        r = (self.gia_copiata("A3", f"A3_{lun}.json")
             or self.chiedi_ad_agente("A3", [self.uscita / "Input_A3_A4.txt"], MESSAGGI["A3"], lun))
        while True:
            es = self.motore("settimanale", "--payload", r["file"])
            if es["fascia"] != "FERMATO":
                break
            motivo = es["uscita"].split("FERMATO", 1)[-1].strip().splitlines()
            self.amb.copia(ingresso.messaggio_correzione("A3", [m for m in motivo[1:] if m.strip()] or motivo))
            r = self.chiedi_ad_agente("A3", [], "", lun, nuova_chat=False)
        if es["fascia"] == "OK" and self.amb.conferma("Settimana scritta. Validare adesso le notizie (facoltativo)?"):
            return self.validazione(lun)
        return es

    def riapertura(self):
        dati = self.amb.chiedi("Riaprire la validazione del ciclo corrente",
                               [("rischi", "Solo questi rischi, separati da virgole (vuoto = tutto)", "")])
        if dati is None:
            return None
        es = self.motore("riapri", *(["--rischi", dati["rischi"]] if dati.get("rischi") else []))
        return self.validazione() if es["fascia"] == "OK" else es

    def testi_a_mano(self):
        self.amb.mostra("Si apre il registro: correggi solo le colonne di testo (guida, sezione 3-ter), poi salva e chiudi.", "info")
        self.registro_in_excel()
        es = self.motore("baseline")
        return self.motore("report") if es["fascia"] == "OK" else es

    def dismetti(self):
        dati = self.amb.chiedi("Dismettere un rischio (decide la funzione di rischio)", [
            ("rischio", "ID del rischio (NFR-nn)", ""), ("motivazione", "Perche' (almeno 10 caratteri)", ""),
            ("decisore", "Chi ha deciso", self.conf.get("validatore_predefinito") or "")])
        if not dati:
            return None
        return self.motore("dismetti", "--rischio", dati["rischio"], "--motivazione", dati["motivazione"],
                           "--decisore", dati["decisore"])

    def parere_a4(self):
        r = self.chiedi_ad_agente("A4", [self.uscita / "Input_A3_A4.txt"], MESSAGGI["A4"], f"A4_{dt.date.today():%Y%m%d}")
        self.amb.mostra(f"Parere archiviato: {r['file']}", "ok")
        if ingresso.proposta_straordinario(Path(r["file"]).read_text(encoding="utf-8")):
            self.amb.mostra("A4 propone un CICLO STRAORDINARIO: decide la funzione di rischio (pulsante Straordinario).", "avviso")
        return r

    def assistente_a7(self):
        link = self.link("A7")
        if link.startswith("http"):
            self.amb.apri(link)
        else:
            self.amb.mostra("Link di A7 non configurato (configurazione.json, link_agenti).", "avviso")

    def diagnosi(self):
        return self.motore("diagnosi")

    def sblocca(self):
        dati = self.amb.chiedi("Togliere il lucchetto del registro (solo se e' rimasto per errore)",
                               [("motivo", "Perche' (almeno 10 caratteri; resta registrato)", "")])
        return self.motore("sblocca", "--motivo", dati["motivo"]) if dati else None

    def prossimo(self):
        """Il passo che lo stato propone (pulsante grande della finestra)."""
        s = stato.leggi(self.conf)
        chiave = s["prossimo"]["chiave"]
        azioni = {"baseline": lambda: self.motore("baseline"), "validazione": self.validazione, "trimestrale": self.trimestrale,
                  "straordinario": self._riprendi_straordinario, "report": self.report, "schede": self.schede,
                  "settimanale": self.settimanale, "valida_settimana": lambda: self.validazione(s["settimana"]["lunedi"])}
        if chiave in azioni:
            return azioni[chiave]()
        self.amb.mostra(s["prossimo"]["titolo"], "info")
        return None

    def _riprendi_straordinario(self):
        """Uno straordinario gia' deciso (baseline --straordinario fatto): da A8 in poi."""
        periodo = stato.leggi(self.conf)["da_valutare"]
        es = self.valutazione(periodo, "A8", [self.uscita / f"Input_A8_{periodo}.txt"])
        if es["fascia"] == "OK" and self.amb.conferma(f"Straordinario {periodo} scritto. Passare alla validazione adesso?"):
            return self.validazione()
        return es
