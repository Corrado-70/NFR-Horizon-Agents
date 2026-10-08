"""Kit della prova di Copilot Studio: lo script della skill e i file da caricare (D-70).

Per chi mantiene il pacchetto, come componi_prompt.py: la Banca riceve i file gia' pronti e non lo lancia.
Rilanciarlo dopo ogni modifica a 07_Senza_Studio/precontrollo.py, controlli_a5.py, valida_output.py, schede.py,
input_a1.py o a 01_Kernel/schema_output_A1.json: il collaudo (test_controlli.py, test_kit_copilot_studio) si ferma
se il kit non contiene esattamente quei file.

Scrive:
  precontrollo-nfr/scripts/precontrollo_nfr.py    script unico: i moduli del pacchetto copiati senza modifiche,
                                                  caricati in memoria all'avvio, e lo schema di A1
  Da_caricare/precontrollo-nfr.zip                la skill (SKILL.md + scripts/) per la nuova esperienza, opzione 2
  Da_caricare/precontrollo-nfr_senza_cartella.zip la stessa, con SKILL.md alla radice dello zip (se la prima e' rifiutata)
  Da_caricare/precontrollo_nfr.txt                lo stesso script, da allegare in chat con il code interpreter
                                                  dell'esperienza standard, opzione 1 (.txt: i .py non si allegano)

Uso:  python 09_Copilot_Studio/prepara_kit.py
Solo libreria standard. Il risultato non dipende dal giorno: rilanciato senza modifiche ai sorgenti, scrive gli
stessi byte.
"""

import hashlib
import shutil
import sys
import zipfile
from pathlib import Path

QUI = Path(__file__).resolve().parent
PACCHETTO = QUI.parent
CAMPO = PACCHETTO / "07_Senza_Studio"
# Ordine di caricamento: ogni modulo importa solo quelli prima di lui.
MODULI = ["valida_output", "radar", "controlli_a5", "schede", "input_a1", "precontrollo"]
SCHEMA = PACCHETTO / "01_Kernel" / "schema_output_A1.json"
NOME_SKILL = "precontrollo-nfr"
SKILL = QUI / NOME_SKILL
SCRIPT = SKILL / "scripts" / "precontrollo_nfr.py"
DA_CARICARE = QUI / "Da_caricare"
ZIP_CARTELLA = DA_CARICARE / f"{NOME_SKILL}.zip"
ZIP_PIATTO = DA_CARICARE / f"{NOME_SKILL}_senza_cartella.zip"
ALLEGATO = DA_CARICARE / "precontrollo_nfr.txt"
DATA_ZIP = (2026, 10, 5, 0, 0, 0)                   # data fissa nello zip: stessi sorgenti, stessi byte

TESTA = '''"""Precontrollo NFR dell'output di A1 per Copilot Studio (skill precontrollo-nfr o code interpreter).

GENERATO da 09_Copilot_Studio/prepara_kit.py: non modificarlo a mano (il collaudo lo confronta con il pacchetto).
Contiene, copiati senza modifiche, i moduli {elenco} di 07_Senza_Studio e lo schema
01_Kernel/schema_output_A1.json: e' lo stesso codice del comando "python esegui_ciclo_locale.py precontrollo"
che la Banca lancia sul PC (D-69, D-70).

Uso:
    python precontrollo_nfr.py <output di A1, A1_<ciclo>.json> <Input_A1_<ciclo>.txt oppure Baseline_corrente.json>
    python precontrollo_nfr.py --verifica      versione e impronta di ogni modulo contenuto
Stampa l'esito (prima riga) e l'impronta dell'output di A1 (seconda riga, la stessa del comando sul PC); se trova
qualcosa scrive accanto all'output Correzione_A1_<ciclo>.txt, il messaggio di correzione per A1. Codice di uscita:
0 nessun punto da correggere, 1 punti da correggere, 2 file illeggibili. Solo libreria standard: niente rete,
niente Excel, non scrive nel registro.
"""

import hashlib
import json
import sys
import types
from pathlib import Path

VERSIONE = "{versione}"
'''

CORPO = '''

def _carica():
    """I moduli del pacchetto, eseguiti in memoria nell'ordine di MODULI, come se fossero file accanto allo script."""
    for nome, sorgente in MODULI.items():
        modulo = types.ModuleType(nome)
        modulo.__file__ = f"precontrollo_nfr/{nome}.py"
        sys.modules[nome] = modulo
        exec(compile(sorgente, modulo.__file__, "exec"), modulo.__dict__)
    return sys.modules["precontrollo"], sys.modules["input_a1"]


def _leggi_json(percorso):
    """JSON da un file; se c'e' testo attorno (recinti ```json di una risposta in chat), dalla prima { all'ultima }."""
    testo = Path(percorso).read_text(encoding="utf-8-sig")
    try:
        return json.loads(testo)
    except json.JSONDecodeError:
        inizio, fine = testo.find("{"), testo.rfind("}")
        if inizio < 0 or fine < inizio:
            raise
        return json.loads(testo[inizio:fine + 1])


def main(argv):
    if argv[1:] == ["--verifica"]:
        print(f"precontrollo_nfr {VERSIONE}")
        for nome, sorgente in {**MODULI, "schema_output_A1.json": SCHEMA_A1}.items():
            print(f"  {nome}: {hashlib.sha256(sorgente.encode('utf-8')).hexdigest()[:12]}")
        return 0
    if len(argv) != 3:
        print(__doc__)
        return 2
    precontrollo, input_a1 = _carica()
    try:
        payload = _leggi_json(argv[1])
    except (OSError, ValueError) as ex:              # JSONDecodeError e' un ValueError
        print(f"File illeggibile: l'output di A1 {argv[1]} non e' un JSON ({ex}).")
        return 2
    try:
        testo = Path(argv[2]).read_text(encoding="utf-8-sig")
        baseline = input_a1.leggi_baseline(testo) if input_a1.INIZIO_BASELINE in testo else _leggi_json(argv[2])
    except (OSError, ValueError) as ex:
        print(f"File illeggibile: {argv[2]} non e' un allegato Input_A1 (manca la parte \\"{input_a1.INIZIO_BASELINE}\\") "
              f"ne' una baseline JSON ({ex}).")
        return 2
    if not isinstance(baseline, dict):
        print("File illeggibile: la baseline deve essere un oggetto JSON (Input_A1_<ciclo>.txt o Baseline_corrente.json).")
        return 2
    esito = precontrollo.precontrolla(payload, baseline, json.loads(SCHEMA_A1))
    ciclo = precontrollo.ciclo_di(payload, baseline)
    da_correggere, da_verificare = precontrollo.conta(esito)
    print(precontrollo.riga_esito(ciclo, esito))
    print(f"Impronta dell'output di A1: {precontrollo.impronta(payload)} · script precontrollo_nfr {VERSIONE}")
    if da_correggere or da_verificare:
        messaggio = precontrollo.messaggio_correzione(ciclo, esito)
        file = Path(argv[1]).with_name(f"Correzione_A1_{ciclo}.txt")
        file.write_text(messaggio, encoding="utf-8")
        print(f"Messaggio di correzione: {file}\\n\\n{messaggio}")
    return 1 if da_correggere else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
'''


def sorgenti():
    """{nome: testo} dei moduli e dello schema, letti dal pacchetto (a capo normalizzati)."""
    testi = {nome: (CAMPO / f"{nome}.py").read_text(encoding="utf-8").replace("\r\n", "\n") for nome in MODULI}
    testi["schema_output_A1.json"] = SCHEMA.read_text(encoding="utf-8").replace("\r\n", "\n")
    return testi


def _letterale(nome, testo):
    """Stringa grezza a tre apici: il testo resta leggibile e identico, barre rovesciate comprese."""
    if "'''" in testo or testo.endswith("\\"):
        raise SystemExit(f"{nome} contiene ''' o finisce con una barra rovesciata: non si puo' copiare cosi' com'e'.")
    return "r'''" + testo + "'''"


def componi():
    """Il testo dello script unico."""
    testi = sorgenti()
    versione = hashlib.sha256("".join(testi[k] for k in sorted(testi)).encode("utf-8")).hexdigest()[:12]
    righe = [TESTA.replace("{elenco}", ", ".join(f"{n}.py" for n in MODULI)).replace("{versione}", versione),
             "SCHEMA_A1 = " + _letterale("schema_output_A1.json", testi["schema_output_A1.json"]), "",
             "MODULI = {"]
    righe += [f'    "{nome}": {_letterale(nome, testi[nome])},' for nome in MODULI]
    righe.append("}")
    return "\n".join(righe) + CORPO


def contenuto_script(percorso):
    """{nome: testo} dei moduli e dello schema dentro uno script generato, senza eseguirne il main: per il collaudo e
    per la verifica qui sotto."""
    spazio = {"__name__": "precontrollo_nfr_verifica"}
    exec(compile(Path(percorso).read_text(encoding="utf-8"), str(percorso), "exec"), spazio)
    return {**spazio["MODULI"], "schema_output_A1.json": spazio["SCHEMA_A1"]}


def _zip(destinazione, prefisso):
    with zipfile.ZipFile(destinazione, "w", zipfile.ZIP_DEFLATED) as z:
        for sorgente, nome in ((SKILL / "SKILL.md", "SKILL.md"), (SCRIPT, "scripts/precontrollo_nfr.py")):
            info = zipfile.ZipInfo(prefisso + nome, date_time=DATA_ZIP)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            z.writestr(info, sorgente.read_bytes())


def main():
    if not (SKILL / "SKILL.md").exists():
        raise SystemExit(f"Manca {SKILL / 'SKILL.md'}: e' scritto a mano, non lo genera questo programma.")
    SCRIPT.parent.mkdir(parents=True, exist_ok=True)
    DA_CARICARE.mkdir(exist_ok=True)
    SCRIPT.write_bytes(componi().encode("utf-8"))
    if contenuto_script(SCRIPT) != sorgenti():
        raise SystemExit("Lo script generato non contiene esattamente i sorgenti del pacchetto: non usarlo.")
    shutil.copyfile(SCRIPT, ALLEGATO)
    _zip(ZIP_CARTELLA, NOME_SKILL + "/")
    _zip(ZIP_PIATTO, "")
    print(f"Kit della prova di Copilot Studio scritto ({len(SCRIPT.read_bytes()):,} byte di script):")
    for f in (SCRIPT, ZIP_CARTELLA, ZIP_PIATTO, ALLEGATO):
        print(f"  {f.relative_to(PACCHETTO)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
