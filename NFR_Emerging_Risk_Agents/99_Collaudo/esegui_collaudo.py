"""Esegue l'intera suite di collaudo, nell'ordine, e riassume l'esito.

Uso:  python esegui_collaudo.py [--senza-excel]
  --senza-excel  salta run_catena.py (per un PC senza Excel, o per un check
                 rapido dopo una modifica ai soli testi)

Da lanciare dopo OGNI modifica a kernel, schemi, mappa, prompt, generatore o
script di campo. Codice di uscita 0 solo se tutto passa.
"""

import os
import subprocess
import sys
from pathlib import Path

QUI = Path(__file__).resolve().parent
PASSI = [
    ("Prompt aggiornati", [sys.executable, str(QUI.parent / "02_Agenti" / "componi_prompt.py"), "--verifica"]),
    ("Mappa sorgente -> destinazione", [sys.executable, str(QUI / "test_mappatura.py")]),
    ("Validatore, controlli A5, esempi, consistenza", [sys.executable, str(QUI / "test_controlli.py")]),
    ("Elenco fonti e raccolta notizie", [sys.executable, str(QUI / "test_fonti.py")]),
    ("Riferimenti incrociati", [sys.executable, str(QUI / "verifica_riferimenti.py")]),
    ("Catena a due cicli (Excel)", [sys.executable, str(QUI / "run_catena.py")]),
]


def main(argv):
    ambiente = {**os.environ, "PYTHONIOENCODING": "utf-8"}
    esiti = []
    for nome, comando in PASSI:
        if "--senza-excel" in argv and "Excel" in nome:
            esiti.append((nome, None))
            continue
        r = subprocess.run(comando, capture_output=True, text=True, encoding="utf-8", errors="replace", env=ambiente)
        print(r.stdout.rstrip())
        if r.returncode != 0 and r.stderr:
            print(r.stderr.rstrip())
        esiti.append((nome, r.returncode == 0))
    print("\n=== RIEPILOGO ===")
    for nome, ok in esiti:
        print(f"  {'SALTATO' if ok is None else 'OK     ' if ok else 'FALLITO'}  {nome}")
    return 0 if all(ok is not False for _, ok in esiti) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
