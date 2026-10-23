"""Lucchetto del registro: un solo analista alla volta scrive (D-83, 23/10/2026).

Piu' analisti usano lo stesso registro, in una library SharePoint sincronizzata con OneDrive. Il lucchetto e' un file
nell'archivio condiviso, Archivio_Cicli/_Lucchetto/registro.json, con chi scrive, da quale PC, con quale comando e da
quando. Lo prende esegui_ciclo_locale.py prima di ogni comando che scrive nel registro e lo lascia alla fine, anche
dopo un fermo o un errore.

E' un avviso cortese, non una garanzia: OneDrive sincronizza con qualche secondo (o minuto) di ritardo, quindi due
analisti possono prenderlo quasi insieme. Per questo:
  - la presa e' in due tempi: si scrive il file, si attende, lo si rilegge; se nel frattempo e' arrivato il lucchetto
    di un collega (o una copia in conflitto creata da OneDrive), ci si ritira;
  - la garanzia vera e' la copia di lavoro del motore (registro_in_lavoro in esegui_ciclo_locale.py): il registro si
    sostituisce solo se nessuno l'ha cambiato nel frattempo.

Un lucchetto scaduto (SCADENZA_ORE, per esempio un PC spento a meta' comando) si puo' prendere; uno incastrato si
toglie con il comando sblocca, che lo registra in sblocchi.log. Solo libreria standard.
"""

import datetime as dt
import json
import os
import socket
import time
import uuid
from contextlib import contextmanager
from pathlib import Path

CARTELLA = "_Lucchetto"
FILE = "registro.json"
REGISTRO_SBLOCCHI = "sblocchi.log"
SCADENZA_ORE = 2
ATTESA_SECONDI = 5          # presa in due tempi: il tempo per far arrivare il lucchetto di un collega


class Occupato(Exception):
    """Il registro e' in uso da un altro analista (il comando si ferma senza scrivere)."""


def chi_sono(utente=None):
    return {"utente": utente or os.environ.get("USERNAME") or os.environ.get("USER") or "sconosciuto",
            "pc": os.environ.get("COMPUTERNAME") or socket.gethostname()}


def _ora():
    return dt.datetime.now().replace(microsecond=0)


def _leggi(percorso):
    try:
        return json.loads(Path(percorso).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def scaduto(dati, adesso=None):
    try:
        return dt.datetime.fromisoformat(dati["scadenza"]) <= (adesso or _ora())
    except (KeyError, TypeError, ValueError):
        return True                                  # illeggibile: non protegge nessuno


def descrivi(dati):
    return (f"{dati.get('utente', '?')} (PC {dati.get('pc', '?')}), comando {dati.get('comando', '?')}, "
            f"dal {str(dati.get('inizio', '?')).replace('T', ' ')}")


def stato(cartella_uscita):
    """Il lucchetto in vigore (dict) o None se il registro e' libero. Senza scritture: lo usa anche l'app."""
    dati = _leggi(Path(cartella_uscita) / CARTELLA / FILE)
    return None if not dati or scaduto(dati) else dati


def _conflitti(cartella, mio_id):
    """Copie in conflitto create da OneDrive (registro-PCNOME.json e simili) di un altro analista, non scadute."""
    out = []
    for f in cartella.glob("registro*.json"):
        if f.name == FILE:
            continue
        dati = _leggi(f)
        if dati and dati.get("id") != mio_id and not scaduto(dati):
            out.append(dati)
    return out


def prendi(cartella_uscita, comando, utente=None, attesa=ATTESA_SECONDI, ore=SCADENZA_ORE):
    """Prende il lucchetto o solleva Occupato. Restituisce i dati scritti (servono per lasciarlo)."""
    cartella = Path(cartella_uscita) / CARTELLA
    cartella.mkdir(parents=True, exist_ok=True)
    percorso = cartella / FILE
    io = chi_sono(utente)
    attuale = _leggi(percorso)
    if attuale and not scaduto(attuale) and (attuale.get("utente"), attuale.get("pc")) != (io["utente"], io["pc"]):
        raise Occupato(f"Il registro e' in uso: {descrivi(attuale)}. Riprova quando ha finito. Se il lucchetto e' "
                       "rimasto per errore (PC spento a meta' comando): python esegui_ciclo_locale.py sblocca --motivo \"...\"")
    inizio = _ora()
    mio = {"id": uuid.uuid4().hex, **io, "comando": comando, "inizio": inizio.isoformat(),
           "scadenza": (inizio + dt.timedelta(hours=ore)).isoformat()}
    percorso.write_text(json.dumps(mio, ensure_ascii=False, indent=2), encoding="utf-8")
    if attesa:
        time.sleep(attesa)
    riletto = _leggi(percorso)
    altri = _conflitti(cartella, mio["id"])
    if not riletto or riletto.get("id") != mio["id"] or altri:
        if riletto and riletto.get("id") == mio["id"]:
            lascia(cartella_uscita, mio)
        chi = descrivi(altri[0] if altri else riletto) if (altri or riletto) else "un collega"
        raise Occupato(f"Un collega ha iniziato a scrivere nello stesso momento: {chi}. Riprova fra qualche minuto.")
    return mio


def lascia(cartella_uscita, mio):
    """Toglie il lucchetto solo se e' ancora il proprio (mai quello di un collega)."""
    percorso = Path(cartella_uscita) / CARTELLA / FILE
    attuale = _leggi(percorso)
    if attuale and attuale.get("id") == mio.get("id"):
        try:
            percorso.unlink()
        except OSError:
            pass                                     # resta: scade da solo


@contextmanager
def preso(cartella_uscita, comando, utente=None, attesa=ATTESA_SECONDI):
    mio = prendi(cartella_uscita, comando, utente, attesa)
    try:
        yield mio
    finally:
        lascia(cartella_uscita, mio)


def sblocca(cartella_uscita, motivo, utente=None):
    """Toglie qualunque lucchetto e lo registra (chi, quando, perche', di chi era). Restituisce il lucchetto tolto."""
    cartella = Path(cartella_uscita) / CARTELLA
    percorso = cartella / FILE
    attuale = _leggi(percorso)
    if percorso.exists():
        percorso.unlink()
    cartella.mkdir(parents=True, exist_ok=True)
    io = chi_sono(utente)
    riga = (f"{_ora().isoformat()} sbloccato da {io['utente']} (PC {io['pc']}): {motivo} | lucchetto tolto: "
            f"{descrivi(attuale) if attuale else 'nessuno'}\n")
    with open(cartella / REGISTRO_SBLOCCHI, "a", encoding="utf-8") as f:
        f.write(riga)
    return attuale
