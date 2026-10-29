"""File a mano per la settimana (D-83, tappa M3): la voce "Invia a -> NFR notizie manuali" di Esplora file.

Tasto destro su uno o piu' file (una circolare, un rapporto, una pagina salvata) -> Invia a -> NFR notizie manuali: i
file si copiano in News_Inbox/<lunedi' di questa settimana>/Manuali, dove li prende A3 (guida, sezione 1). Un file con
lo stesso nome non si sovrascrive: si aggiunge un numero. Le cartelle (il primo livello) si copiano file per file.

Uso: python notizie_manuali.py FILE [FILE ...] [--news-inbox CARTELLA]
"""

import argparse
import datetime as dt
import shutil
import sys
from pathlib import Path


def cartella_manuali(news_inbox, oggi=None):
    oggi = oggi or dt.date.today()
    lunedi = oggi - dt.timedelta(days=oggi.weekday())
    return Path(news_inbox) / lunedi.isoformat() / "Manuali"


def libero(destinazione):
    """Il nome di destinazione senza toccare un file che c'e' gia': Circolare.pdf, Circolare (2).pdf, ..."""
    if not destinazione.exists():
        return destinazione
    n = 2
    while (destinazione.with_name(f"{destinazione.stem} ({n}){destinazione.suffix}")).exists():
        n += 1
    return destinazione.with_name(f"{destinazione.stem} ({n}){destinazione.suffix}")


def copia(file, news_inbox, oggi=None):
    """Copia i file; restituisce (copiati, saltati) come liste di (origine, destinazione o motivo)."""
    manuali = cartella_manuali(news_inbox, oggi)
    manuali.mkdir(parents=True, exist_ok=True)
    copiati, saltati = [], []
    for f in map(Path, file):
        elenco = sorted(p for p in f.iterdir() if p.is_file()) if f.is_dir() else [f]
        for p in elenco:
            if not p.is_file():
                saltati.append((p, "non trovato"))
                continue
            dest = libero(manuali / p.name)
            shutil.copy2(p, dest)
            copiati.append((p, dest))
    return copiati, saltati


def main(argv=None):
    p = argparse.ArgumentParser(description="Copia file in News_Inbox/<lunedi'>/Manuali")
    p.add_argument("file", nargs="*")
    p.add_argument("--news-inbox", dest="news_inbox")
    arg = p.parse_args(argv)
    from esegui_ciclo_locale import configurazione
    conf = configurazione(arg)
    if not arg.file:
        print("Nessun file: tasto destro sui file -> Invia a -> NFR notizie manuali.")
        return 1
    if not conf["news_inbox"] or not Path(conf["news_inbox"]).is_dir():
        print(f"Cartella News_Inbox non trovata ({conf['news_inbox']}): controllare news_inbox in configurazione.json "
              "(guida, sezione 0.3) e la sincronizzazione di OneDrive.")
        return 1
    copiati, saltati = copia(arg.file, conf["news_inbox"])
    for origine, dest in copiati:
        print(f"Copiato: {origine.name} -> {dest}")
    for origine, motivo in saltati:
        print(f"Saltato: {origine} ({motivo})")
    print(f"{len(copiati)} file in {cartella_manuali(conf['news_inbox'])}: A3 li leggera' con l'aggiornamento settimanale.")
    return 0 if copiati else 1


if __name__ == "__main__":
    sys.exit(main())
