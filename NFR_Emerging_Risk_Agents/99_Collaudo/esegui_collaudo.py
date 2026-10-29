"""Esegue l'intera suite di collaudo, nell'ordine, e riassume l'esito.

Uso:  python esegui_collaudo.py [--senza-excel | --mirato] [--in-sequenza]
  --senza-excel  salta run_catena.py (per un PC senza Excel, o per un check
                 rapido dopo una modifica ai soli testi)
  --mirato       lancia la catena con Excel solo se dall'ultimo collaudo
                 completo e verde e' cambiato un file che la riguarda (script,
                 generatore, template, kernel, dati di prova, collaudo): per
                 prompt, guida e documenti bastano le suite veloci (M1, 08/10/2026)
  --in-sequenza  la catena con i gruppi uno dopo l'altro (circa 50 minuti),
                 invece che in tre processi con un Excel ciascuno (default)

Da lanciare dopo OGNI modifica a kernel, schemi, mappa, prompt, generatore o
script di campo. Codice di uscita 0 solo se tutto passa.
"""

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

QUI = Path(__file__).resolve().parent
PACCHETTO = QUI.parent
CATENA = "Catena a due cicli (Excel)"
PASSI = [
    ("Prompt aggiornati", [sys.executable, str(PACCHETTO / "02_Agenti" / "componi_prompt.py"), "--verifica"]),
    ("Mappa sorgente -> destinazione", [sys.executable, str(QUI / "test_mappatura.py")]),
    ("Validatore, controlli A5, esempi, consistenza", [sys.executable, str(QUI / "test_controlli.py")]),
    ("Elenco fonti e raccolta notizie", [sys.executable, str(QUI / "test_fonti.py")]),
    ("Piu' analisti: lucchetto e copia di lavoro", [sys.executable, str(QUI / "test_app.py")]),
    ("Installazione e Verifica del PC", [sys.executable, str(QUI / "test_installazione.py")]),
    ("Report al comitato in HTML", [sys.executable, str(QUI / "test_report_html.py")]),
    ("Funzioni amministrative", [sys.executable, str(QUI / "test_amministrazione.py")]),
    ("Riferimenti incrociati", [sys.executable, str(QUI / "verifica_riferimenti.py")]),
    (CATENA, [sys.executable, str(QUI / "run_catena.py")]),
]
# File che la catena con Excel mette alla prova: se nessuno cambia, --mirato la salta.
DELLA_CATENA = ["07_Senza_Studio/*.py", "03_Excel/*.py", "03_Excel/*.xlsx", "01_Kernel/*", "99_Collaudo/*.py",
                "99_Collaudo/dati/*"]
# Scritto solo dopo un collaudo completo e verde; fuori dal pacchetto (e' uno stato di questo PC, non va nello zip).
IMPRONTE = Path(os.environ.get("LOCALAPPDATA") or Path.home()) / "NFR_collaudo" / "ultimo_collaudo_completo.json"


def impronte():
    """{percorso relativo: sha256} dei file che la catena mette alla prova."""
    out = {}
    for schema in DELLA_CATENA:
        for f in sorted(PACCHETTO.glob(schema)):
            if f.is_file() and not f.name.startswith("~$"):
                out[f.relative_to(PACCHETTO).as_posix()] = hashlib.sha256(f.read_bytes()).hexdigest()
    return out


def cambiati_dall_ultimo():
    """File della catena cambiati dall'ultimo collaudo completo e verde (tutti, se non ce n'e' uno)."""
    attuali = impronte()
    try:
        prima = json.loads(IMPRONTE.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return sorted(attuali)
    return sorted(f for f in set(attuali) | set(prima) if attuali.get(f) != prima.get(f))


def main(argv):
    ambiente = {**os.environ, "PYTHONIOENCODING": "utf-8"}
    salta_catena = "--senza-excel" in argv
    if "--mirato" in argv and not salta_catena:
        cambiati = cambiati_dall_ultimo()
        if cambiati:
            print(f"Collaudo mirato: la catena serve, sono cambiati {len(cambiati)} file che la riguardano: "
                  + ", ".join(cambiati[:8]) + (" ..." if len(cambiati) > 8 else ""))
        else:
            print("Collaudo mirato: nessun file della catena e' cambiato dall'ultimo collaudo completo; bastano le "
                  "suite veloci.")
            salta_catena = True
    esiti = []
    for nome, comando in PASSI:
        if nome == CATENA:
            if salta_catena:
                esiti.append((nome, None))
                continue
            if "--in-sequenza" not in argv:
                comando = comando + ["--parallelo", "3"]
        r = subprocess.run(comando, capture_output=True, text=True, encoding="utf-8", errors="replace", env=ambiente)
        print(r.stdout.rstrip())
        if r.returncode != 0 and r.stderr:
            print(r.stderr.rstrip())
        esiti.append((nome, r.returncode == 0))
    print("\n=== RIEPILOGO ===")
    for nome, ok in esiti:
        print(f"  {'SALTATO' if ok is None else 'OK     ' if ok else 'FALLITO'}  {nome}")
    tutto_ok = all(ok is not False for _, ok in esiti)
    if tutto_ok and all(ok for _, ok in esiti):      # completo (catena compresa) e verde: punto di partenza di --mirato
        IMPRONTE.parent.mkdir(parents=True, exist_ok=True)
        IMPRONTE.write_text(json.dumps(impronte(), indent=1), encoding="utf-8")
    return 0 if tutto_ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
