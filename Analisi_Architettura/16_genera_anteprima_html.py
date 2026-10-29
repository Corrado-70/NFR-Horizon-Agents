"""Anteprima del report in HTML (analisi 16): Horizon Scan NFR con l'HTML al posto dei fogli di Excel.

Dal 29/10/2026 (tappa M4) il codice del report e' nel pacchetto, NFR_Emerging_Risk_Agents/07_Senza_Studio/report_html.py,
che lo produce come seconda uscita del comando report. Questo script ne fa l'anteprima dell'analisi 16 sui dati della
demo, con tutte le pagine (anche le tabelle dati) e un report per ogni ciclo, letti dal file con openpyxl.

Per il ciclo corrente confronta i numeri calcolati con quelli che Excel ha calcolato nel registro della demo (X, Y, Z,
margine, urgenza, livello di allerta e motivo, segnali netti, ordine della classifica, Delta): stampa l'esito.

Scrive, nella cartella 16_Anteprima_HTML:
  index.html                       archivio dei cicli, con il collegamento a ogni report
  Horizon_Scan_<ciclo>.html        un file per ciclo, autosufficiente: nessuna risorsa esterna, grafici in SVG,
                                   navigazione senza JavaScript (il JavaScript aggiunge solo comodita')
  dati_registro.json               le tabelle dati come file JSON: la "base" dello scenario

Uso:  python 16_genera_anteprima_html.py [--registro PERCORSO] [--uscita CARTELLA]
Dipendenze: openpyxl (per leggere il registro della demo).
"""

import argparse
import json
import sys
from pathlib import Path

QUI = Path(__file__).resolve().parent
RADICE = QUI.parent
sys.path.insert(0, str(RADICE / "NFR_Emerging_Risk_Agents" / "07_Senza_Studio"))
import report_html as rh  # noqa: E402

REGISTRO = RADICE / "Demo_W1_W2" / "NFR_Registro.xlsx"
USCITA = QUI / "16_Anteprima_HTML"


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--registro", type=Path, default=REGISTRO)
    ap.add_argument("--uscita", type=Path, default=USCITA)
    a = ap.parse_args()
    reg = rh.RegistroFile(a.registro)
    a.uscita.mkdir(parents=True, exist_ok=True)
    viste = [rh.Vista(reg, c) for c in rh.cicli_ordinati(reg)]
    corrente = viste[-1]
    uguali, diversi = rh.verifica(reg, corrente)
    print(f"Confronto con i valori calcolati da Excel ({corrente.ciclo}): {uguali} uguali, {len(diversi)} diversi")
    for d in diversi:
        print("  DIVERSO:", d)
    file_per_ciclo = {v.ciclo: f"Horizon_Scan_{v.ciclo}.html" for v in viste}
    for v in viste:
        p = a.uscita / file_per_ciclo[v.ciclo]
        p.write_text(rh.pagina(v, reg, p.name, anteprima=True), encoding="utf-8")
        print(f"  {p.name}: {p.stat().st_size // 1024} KB")
    righe = [rh.riassunto(v, file_per_ciclo[v.ciclo]) for v in viste]
    (a.uscita / "index.html").write_text(rh.pagina_indice(righe, anteprima=True), encoding="utf-8")
    dati = {n: reg.tab[n] for n in reg.tab}
    pj = a.uscita / "dati_registro.json"
    pj.write_text(json.dumps(dati, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"  index.html; dati_registro.json: {pj.stat().st_size // 1024} KB")
    return 0 if not diversi else 1


if __name__ == "__main__":
    sys.exit(main())
