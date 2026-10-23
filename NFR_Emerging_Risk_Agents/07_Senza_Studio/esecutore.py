"""Esecuzione del motore per l'app NFR (D-83, tappa M2; TODO AU2).

L'app non importa il motore: lo lancia in un processo a parte, come fa l'analista dal Prompt dei comandi e come fanno
collaudo e demo. Cosi' un errore di Excel non chiude la finestra, e il motore resta lo stesso programma, con gli stessi
codici di uscita, sia da riga di comando sia dall'app.

  - L'uscita arriva riga per riga (su_riga), per mostrarla mentre il comando lavora.
  - Il codice diventa una fascia: 0 OK, 1 FERMATO (registro intatto), 2 ERRORE TECNICO; con "DOPO IL SALVATAGGIO"
    l'app non propone di rilanciare.
  - Ogni esecuzione lascia un log in Archivio_Cicli/Log/<data_ora>_<utente>_<comando>.txt: chi, quando, che cosa,
    con quale esito.

Solo libreria standard.
"""

import datetime as dt
import os
import re
import subprocess
import sys
from pathlib import Path

QUI = Path(__file__).resolve().parent
MOTORE = QUI / "esegui_ciclo_locale.py"
RACCOLTA = QUI / "raccogli_notizie.py"
FASCE = {0: "OK", 1: "FERMATO", 2: "ERRORE TECNICO"}
COSA_FARE = {
    "OK": "Fatto.",
    "FERMATO": "Il registro non e' stato toccato: leggere il motivo qui sopra, correggere e rilanciare.",
    "ERRORE TECNICO": "Un problema del PC o di Excel, prima del salvataggio: niente e' stato scritto. Rimuovere la causa "
                      "(per esempio chiudere Excel) e rilanciare; se si ripete, mandare il log a chi mantiene il pacchetto.",
    "DOPO IL SALVATAGGIO": "Il registro E' STATO SCRITTO: NON rilanciare lo stesso comando. Completare l'archivio come dice il "
                           "messaggio e avvisare chi mantiene il pacchetto.",
}


def interprete():
    """python.exe anche quando l'app gira con pythonw.exe (senza console): l'uscita del motore si legge dal tubo."""
    eseguibile = Path(sys.executable)
    if eseguibile.name.lower() == "pythonw.exe" and (eseguibile.parent / "python.exe").exists():
        return str(eseguibile.parent / "python.exe")
    return str(eseguibile)


def _nome_log(argomenti, utente):
    comando = next((a for a in argomenti if not str(a).startswith("-")), "comando")
    pulito = lambda t: re.sub(r"[^A-Za-z0-9_-]+", "_", str(t))[:30]
    return f"{dt.datetime.now():%Y%m%d_%H%M%S}_{pulito(utente)}_{pulito(comando)}.txt"


def esegui(argomenti, cartella_uscita, utente="", su_riga=None, script=MOTORE, opzioni=()):
    """Lancia il motore (o un altro script del pacchetto) con 'argomenti'; 'opzioni' vanno prima del comando
    (--workbook, --cartella-uscita...). Restituisce {codice, fascia, uscita, log, dopo_salvataggio, cosa_fare}."""
    cmd = [interprete(), str(script), *map(str, opzioni), *map(str, argomenti)]
    righe = []
    env = {**os.environ, "PYTHONIOENCODING": "utf-8"}
    nascosto = getattr(subprocess, "CREATE_NO_WINDOW", 0)
    try:
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding="utf-8",
                                errors="replace", env=env, cwd=str(QUI), creationflags=nascosto)
        for riga in proc.stdout:
            righe.append(riga)
            if su_riga:
                su_riga(riga.rstrip("\n"))
        codice = proc.wait()
    except OSError as ex:                            # Python non trovato o simili
        righe.append(f"ERRORE TECNICO — il motore non parte: {ex}\n")
        codice = 2
    uscita = "".join(righe)
    dopo = "DOPO IL SALVATAGGIO" in uscita
    fascia = FASCE.get(codice, "ERRORE TECNICO")
    log = None
    try:
        cartella = Path(cartella_uscita) / "Log"
        cartella.mkdir(parents=True, exist_ok=True)
        log = cartella / _nome_log(argomenti, utente)
        log.write_text(f"Comando: {' '.join(cmd[1:])}\nUtente: {utente}\nCodice: {codice} ({fascia})\n\n{uscita}",
                       encoding="utf-8")
    except OSError:
        pass                                         # il log non e' essenziale: l'uscita resta nella finestra
    return {"codice": codice, "fascia": fascia, "uscita": uscita, "log": log, "dopo_salvataggio": dopo,
            "cosa_fare": COSA_FARE["DOPO IL SALVATAGGIO" if dopo else fascia]}


PRECONTROLLO = re.compile(r"Precontrollo dell'output di A[18] \(([^)]+)\): (?:nessun rilievo|(\d+) punti da correggere, (\d+) da verificare)")


def esito_precontrollo(uscita):
    """(punti da correggere, punti da verificare) dalla prima riga del comando precontrollo; None se non c'e'."""
    m = PRECONTROLLO.search(uscita)
    if not m:
        return None
    return (int(m.group(2) or 0), int(m.group(3) or 0))
