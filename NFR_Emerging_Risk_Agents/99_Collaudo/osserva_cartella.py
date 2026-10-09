"""Misura i tempi della sincronizzazione fra SharePoint e il PC (prova K7a della CS-1, 09_Copilot_Studio/Prove_CS1.md).

Strumento di prova, come confronta.py: non fa parte del processo e non tocca registro ne' archivio.

Uso:
  python osserva_cartella.py <cartella sincronizzata> [--minuti 30]
      guarda la cartella ogni 2 secondi e stampa l'ora in cui ogni file nuovo compare sul PC, la sua data di
      modifica e la dimensione, e quando la dimensione smette di cambiare (file completo). Le stesse righe vanno
      in osserva_cartella_<data_ora>.log nella cartella da cui lo si lancia. Si ferma dopo i minuti indicati o
      con Ctrl+C.
  python osserva_cartella.py --scrivi <cartella sincronizzata>
      scrive Prova_sync_<ora>.txt con dentro l'ora di scrittura sul PC, e la stampa: e' il segnale da cercare in
      SharePoint, nel browser, per misurare il tempo di caricamento.
Solo libreria standard.
"""

import argparse
import datetime as dt
import sys
import time
from pathlib import Path


def ora():
    return dt.datetime.now().strftime("%H:%M:%S")


def scrivi(cartella):
    cartella = Path(cartella)
    if not cartella.is_dir():
        sys.exit(f"Cartella non trovata: {cartella}")
    adesso = dt.datetime.now()
    nome = cartella / f"Prova_sync_{adesso:%H%M%S}.txt"
    nome.write_text(f"Scritto sul PC alle {adesso:%Y-%m-%d %H:%M:%S}\n", encoding="utf-8")
    print(f"{ora()}  scritto {nome.name}: cercarlo in SharePoint e annotare l'ora in cui compare.")


def osserva(cartella, minuti, intervallo=2.0):
    cartella = Path(cartella)
    if not cartella.is_dir():
        sys.exit(f"Cartella non trovata: {cartella}")
    registro = Path.cwd() / f"osserva_cartella_{dt.datetime.now():%Y%m%d_%H%M%S}.log"

    def annota(riga):
        print(riga)
        with registro.open("a", encoding="utf-8") as f:
            f.write(riga + "\n")

    def stato():
        visti = {}
        for p in cartella.iterdir():
            if p.is_file():
                try:
                    st = p.stat()
                except OSError:
                    continue
                visti[p.name] = (st.st_size, st.st_mtime)
        return visti

    prima = stato()
    in_crescita = {}
    annota(f"{ora()}  osservo {cartella} ({len(prima)} file gia' presenti, ignorati); registro in {registro}")
    fine = time.monotonic() + minuti * 60
    try:
        while time.monotonic() < fine:
            time.sleep(intervallo)
            adesso = stato()
            for nome, (dim, mtime) in adesso.items():
                modifica = dt.datetime.fromtimestamp(mtime).strftime("%H:%M:%S")
                if nome not in prima:
                    annota(f"{ora()}  compare   {nome}  {dim} byte  data di modifica {modifica}")
                    in_crescita[nome] = dim
                elif prima[nome] != (dim, mtime):
                    annota(f"{ora()}  cambia    {nome}  {dim} byte  data di modifica {modifica}")
                    in_crescita[nome] = dim
                elif nome in in_crescita and in_crescita[nome] == dim:
                    annota(f"{ora()}  completo  {nome}  {dim} byte")
                    del in_crescita[nome]
            for nome in set(prima) - set(adesso):
                annota(f"{ora()}  sparisce  {nome}")
            prima = adesso
    except KeyboardInterrupt:
        pass
    annota(f"{ora()}  fine dell'osservazione")


def main(argv=None):
    p = argparse.ArgumentParser(description="Tempi della sincronizzazione fra SharePoint e il PC (prova K7a).")
    p.add_argument("cartella", nargs="?")
    p.add_argument("--minuti", type=float, default=30)
    p.add_argument("--scrivi", metavar="CARTELLA")
    a = p.parse_args(argv)
    if a.scrivi:
        scrivi(a.scrivi)
    elif a.cartella:
        osserva(a.cartella, a.minuti)
    else:
        p.error("indicare la cartella da osservare oppure --scrivi <cartella>")


if __name__ == "__main__":
    main()
