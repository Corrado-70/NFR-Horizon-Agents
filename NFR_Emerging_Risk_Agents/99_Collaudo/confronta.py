"""Confronta due output di A1 sullo stesso input: misura la riproducibilita'.

Uso:  python confronta.py run1.json run2.json [--primo-ciclo]
Codice di uscita 0 se i giudizi coincidono, 1 altrimenti.

Cosa DEVE coincidere fra due run (e' giudizio ancorato alla rubrica): le
quattro dimensioni del composito (Impatto, Probabilita, Prossimita, Velocity,
anche quando e' null), l'event type, le dimensioni variate, i kri_id riusati,
gli id dei rischi (D-50: dimensioni del confronto di D-21; l'esito non e' piu'
di A1, lo calcola lo script, D-51; la Confidence non c'e' piu', D-58). Gli anni
di adeguamento sono una stima (D-60): non entrano nel confronto.
Cosa PUO' variare: la prosa (razionale, sintesi, descrizioni). Lo strumento
serve soprattutto in tenant, per il doppio run del collaudo in ambiente
(04_Riferimenti/workflow.md, test in ambiente; guida, Avvio del progetto, fase 7).

--primo-ciclo: da registro vuoto A1 numera da se' i rischi nuovi, quindi lo
stesso rischio puo' avere id diversi nei due run. Con questa opzione i rischi
si abbinano per event type e somiglianza del nome (non per id); gli abbinamenti
sono stampati per un controllo a occhio. Un rischio senza abbinamento e'
"presente in un solo run": per il primo ciclo e' la misura piu' importante.
"""

import argparse
import copy
import difflib
import sys

from comune import carica

PUNTEGGI = ["impatto", "probabilita", "prossimita", "velocity"]
CAMPI = PUNTEGGI + ["event_type"]
SOGLIA_NOME = 0.5                 # somiglianza minima fra i nomi per abbinare due rischi


def abbina(a, b):
    """Rinumera i rischi di b con gli id dei rischi di a che descrivono lo
    stesso rischio (stesso event type, nome piu' simile). Abbinamento globale:
    prima le coppie piu' simili. Restituisce (b rinumerato, coppie)."""
    punteggi = sorted(((difflib.SequenceMatcher(None, x["nome"].lower(), y["nome"].lower()).ratio(), i, j)
                       for i, x in enumerate(a["rischi"]) for j, y in enumerate(b["rischi"])
                       if x["event_type"] == y["event_type"]), reverse=True)
    presi_a, presi_b, coppie = set(), set(), []
    for s, i, j in punteggi:
        if s >= SOGLIA_NOME and i not in presi_a and j not in presi_b:
            presi_a.add(i)
            presi_b.add(j)
            coppie.append((a["rischi"][i]["id_rischio"], b["rischi"][j]["id_rischio"], round(s, 2)))
    nuovo = copy.deepcopy(b)
    verso = {id_b: id_a for id_a, id_b, _ in coppie}
    for r in nuovo["rischi"]:
        r["id_rischio"] = verso.get(r["id_rischio"], "solo run2: " + r["id_rischio"])
    return nuovo, sorted(coppie)


def confronta(a, b):
    differenze = []
    ra = {r["id_rischio"]: r for r in a["rischi"]}
    rb = {r["id_rischio"]: r for r in b["rischi"]}
    for rid in sorted(set(ra) ^ set(rb)):
        differenze.append(f"{rid}: presente in un solo run")
    for rid in sorted(set(ra) & set(rb)):
        x, y = ra[rid], rb[rid]
        for c in CAMPI:
            if x.get(c) != y.get(c):
                differenze.append(f"{rid}.{c}: {x.get(c)} contro {y.get(c)}")
        dx = sorted(v["dimensione"] for v in x["variazioni"])
        dy = sorted(v["dimensione"] for v in y["variazioni"])
        if dx != dy:
            differenze.append(f"{rid}.variazioni: {dx} contro {dy}")
        kx = sorted(k.get("kri_id") or "nuovo" for k in x["kri_proposti"])
        ky = sorted(k.get("kri_id") or "nuovo" for k in y["kri_proposti"])
        if kx != ky:
            differenze.append(f"{rid}.kri_id: {kx} contro {ky}")
    va = {z["kri_id"]: z["valore"] for z in a["ricalcolo_kri_ciclo_precedente"]}
    vb = {z["kri_id"]: z["valore"] for z in b["ricalcolo_kri_ciclo_precedente"]}
    if va != vb:
        differenze.append("ricalcolo_kri_ciclo_precedente: valori diversi")
    punteggi = sum(1 for rid in set(ra) & set(rb) for c in PUNTEGGI if ra[rid].get(c) == rb[rid].get(c))
    return differenze, punteggi, len(PUNTEGGI) * len(set(ra) & set(rb))


def main(argv):
    p = argparse.ArgumentParser(description="Confronta due output di A1 sullo stesso input (riproducibilita').")
    p.add_argument("run1")
    p.add_argument("run2")
    p.add_argument("--primo-ciclo", action="store_true",
                   help="abbina i rischi per event type e nome (primo ciclo da registro vuoto)")
    arg = p.parse_args(argv[1:])
    a, b = carica(arg.run1), carica(arg.run2)
    if arg.primo_ciclo:
        b, coppie = abbina(a, b)
        print("Abbinamenti (run1 <- run2, somiglianza dei nomi): controllarli a occhio")
        for id_a, id_b, s in coppie:
            print(f"  {id_a} <- {id_b} ({s})")
    diff, uguali, totali = confronta(a, b)
    print(f"Punteggi identici: {uguali}/{totali}")
    for d in diff:
        print("  -", d)
    return 1 if diff else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
