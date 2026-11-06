"""Prova K16 (Analisi_Architettura/20_Agenti_Claude_Vertex.md, 20.12): A1 con Claude Code sul PC della Banca.

Lancia `claude -p` senza strumenti, come lo lancerebbe il canale Claude dell'app (20.5.2), su una copia
dell'allegato Input_A1, e salva la risposta come JSON pronto per il precontrollo. Non tocca il registro ne' la
cartella dell'archivio: scrive solo nella cartella di prova indicata con --cartella.

Uso (dal prompt dei comandi, nella cartella di prova):
  py -3 prova_k16.py --input Input_A1_2026Q4.txt --run A                 (senza schema: il JSON nel testo)
  py -3 prova_k16.py --input Input_A1_2026Q4.txt --run B --con-schema    (con lo schema di decodifica)
  py -3 prova_k16.py --input ... --solo-comando                          (mostra il comando, non lancia nulla)
Opzioni: --modello, --effort, --budget, --aggiungi <file o percorso con *> (documenti in coda all'allegato),
--richiesta "<testo>" (per il giro di correzione), --senza-bare, --impostazioni <settings.json>,
--claude <percorso di claude.exe>. Il manuale e' 04_Riferimenti/Prove/Prova_K16_Claude_Code.md.

Uscite: 0 risposta salvata come JSON; 1 risposta arrivata ma non utilizzabile (vedi il riepilogo); 2 errore tecnico.
Solo libreria standard.
"""
import argparse
import datetime as dt
import glob
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

QUI = Path(__file__).resolve().parent
PACCHETTO = QUI.parents[2]                                   # .../NFR_Emerging_Risk_Agents
SCHEMA_A1 = PACCHETTO / "01_Kernel" / "schema_output_A1.json"
PROMPT = QUI / "A1_per_Claude.md"
RICHIESTA = "Esegui il ciclo. L'allegato Input_A1 e gli eventuali documenti sono qui sotto."

# Parole chiave che l'uscita strutturata non accetta, o che farebbero rifiutare e rigenerare tutta la risposta per una
# lunghezza (20.6): le lunghezze le controllano il precontrollo (C10) e valida_output.py, sullo schema intero.
TOGLI = {"$schema", "$id", "title", "minLength", "maxLength", "minimum", "maximum", "exclusiveMinimum",
         "exclusiveMaximum", "multipleOf", "maxItems", "uniqueItems", "minProperties", "maxProperties"}
CONTENITORI = {"properties", "$defs", "definitions", "patternProperties"}   # le chiavi qui dentro sono nomi, non parole chiave


def schema_decodifica(nodo, dentro_contenitore=False):
    """Schema del kernel (draft 2020-12) -> schema per --json-schema (draft-07, senza vincoli di lunghezza)."""
    if isinstance(nodo, list):
        return [schema_decodifica(x) for x in nodo]
    if not isinstance(nodo, dict):
        return nodo
    if dentro_contenitore:
        return {nome: schema_decodifica(v) for nome, v in nodo.items()}
    nuovo = {}
    for chiave, valore in nodo.items():
        if chiave in TOGLI or (chiave == "minItems" and valore not in (0, 1)):
            continue
        nome = "definitions" if chiave == "$defs" else chiave
        nuovo[nome] = schema_decodifica(valore, dentro_contenitore=chiave in CONTENITORI)
    if isinstance(nuovo.get("$ref"), str):
        nuovo["$ref"] = nuovo["$ref"].replace("#/$defs/", "#/definitions/")
    return nuovo


def espandi(percorsi):
    """I percorsi con * o ? (il prompt dei comandi non li espande): i file trovati, in ordine di nome."""
    file = []
    for p in percorsi:
        trovati = sorted(glob.glob(p, recursive=True)) if any(c in p for c in "*?") else [p]
        if not trovati:
            raise SystemExit(f"ERRORE TECNICO: nessun file per {p}")
        file += trovati
    return file


def testo_richiesta(input_a1, aggiunti, richiesta=RICHIESTA):
    parti = [richiesta, "", "=== ALLEGATO Input_A1 ===", Path(input_a1).read_text(encoding="utf-8-sig")]
    for f in aggiunti:
        parti += ["", f"=== DOCUMENTO: {Path(f).name} ===", Path(f).read_text(encoding="utf-8-sig", errors="replace")]
    return "\n".join(parti)


def trova_claude(indicato=None):
    percorso = indicato or shutil.which("claude")
    if not percorso:
        raise SystemExit("ERRORE TECNICO: 'claude' non trovato. Controllare con: where claude")
    if Path(percorso).suffix.lower() in (".cmd", ".bat"):
        raise SystemExit(f"ERRORE TECNICO: {percorso} e' un file .cmd: serve claude.exe (installazione nativa). "
                         "Indicarlo con --claude <percorso di claude.exe>.")
    return percorso


def comando(arg, claude, schema=None):
    c = [claude] + ([] if arg.senza_bare else ["--bare"]) + [
        "-p", "--tools", "", "--no-session-persistence",
        "--model", arg.modello, "--effort", arg.effort,
        "--system-prompt-file", str(arg.prompt),
        "--output-format", "json", "--max-budget-usd", str(arg.budget)]
    if not arg.senza_bare and arg.impostazioni and Path(arg.impostazioni).exists():
        c += ["--settings", str(arg.impostazioni)]
    if schema is not None:
        c += ["--json-schema", json.dumps(schema, ensure_ascii=False, separators=(",", ":"))]
    return c


def ambiente():
    env = dict(os.environ)
    env.setdefault("CLAUDE_CODE_MAX_OUTPUT_TOKENS", "128000")     # R20: il valore predefinito potrebbe tagliare A1
    env["CLAUDE_CODE_DISABLE_MODEL_ACCESS_FALLBACK"] = "1"         # nessun cambio di modello in silenzio
    env["CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC"] = "1"          # niente aggiornamenti automatici e telemetria
    return env


def estrai_json(testo):
    """Il JSON di A1 dal testo della risposta: toglie i recinti e prende da '{' all'ultima '}'."""
    t = testo.strip()
    if t.startswith("```"):
        t = t.split("\n", 1)[1] if "\n" in t else ""
        t = t.rsplit("```", 1)[0]
    inizio, fine = t.find("{"), t.rfind("}")
    if inizio < 0 or fine <= inizio:
        return None
    try:
        return json.loads(t[inizio:fine + 1])
    except json.JSONDecodeError:
        return None


def riepilogo(busta, payload, durata):
    uso = busta.get("usage") or {}
    modelli = list((busta.get("modelUsage") or {}).keys())
    righe = [
        f"Esito di Claude Code: {busta.get('subtype')} (is_error={busta.get('is_error')}), turni {busta.get('num_turns')}",
        f"Durata: {durata/60:.1f} minuti; costo stimato da Claude Code: {busta.get('total_cost_usd')} USD",
        "Token: in {} (+ cache letta {}, cache scritta {}), out {}".format(
            uso.get("input_tokens"), uso.get("cache_read_input_tokens"), uso.get("cache_creation_input_tokens"),
            uso.get("output_tokens")),
        f"Modelli usati: {', '.join(modelli) or 'non indicati'}",
    ]
    if payload is not None:
        rischi = payload.get("rischi") or []
        caratteri = f"{len(json.dumps(payload, ensure_ascii=False)):,}".replace(",", ".")
        righe.append(f"Risposta: JSON del ciclo {payload.get('ciclo')}, {len(rischi)} rischi, {caratteri} caratteri")
    return "\n".join(righe)


def main(argv=None):
    p = argparse.ArgumentParser(description="Prova K16: A1 con Claude Code senza strumenti.")
    p.add_argument("--input", required=True, help="copia di Input_A1_<ciclo>.txt")
    p.add_argument("--run", default="A", help="etichetta della prova (A, B, ...)")
    p.add_argument("--con-schema", action="store_true", help="passa lo schema di decodifica con --json-schema")
    p.add_argument("--aggiungi", nargs="*", default=[], help="documenti da mettere in coda all'allegato (anche con *)")
    p.add_argument("--richiesta", default=RICHIESTA, help="testo della richiesta (per il giro di correzione)")
    p.add_argument("--modello", default="claude-opus-5-5")
    p.add_argument("--effort", default="high")
    p.add_argument("--budget", type=float, default=5.0, help="tetto di spesa della chiamata, in USD")
    p.add_argument("--prompt", default=str(PROMPT))
    p.add_argument("--schema", default=str(SCHEMA_A1))
    p.add_argument("--impostazioni", default=str(Path(os.environ.get("USERPROFILE", "~")) / ".claude" / "settings.json"))
    p.add_argument("--senza-bare", action="store_true", help="ripiego se con --bare Claude Code non trova Vertex")
    p.add_argument("--claude", help="percorso di claude.exe, se non e' nel PATH")
    p.add_argument("--cartella", default=".", help="cartella di prova dove salvare (default: quella corrente)")
    p.add_argument("--timeout", type=int, default=45, help="minuti")
    p.add_argument("--solo-comando", action="store_true", help="mostra il comando e non lancia nulla")
    arg = p.parse_args(argv)

    cartella = Path(arg.cartella).resolve()
    cartella.mkdir(parents=True, exist_ok=True)
    schema = schema_decodifica(json.loads(Path(arg.schema).read_text(encoding="utf-8"))) if arg.con_schema else None
    claude = "claude" if arg.solo_comando else trova_claude(arg.claude)
    cmd = comando(arg, claude, schema)
    aggiunti = espandi(arg.aggiungi)
    richiesta = testo_richiesta(arg.input, aggiunti, arg.richiesta)
    if aggiunti:
        print(f"Documenti in coda all'allegato: {len(aggiunti)}")
    riga = subprocess.list2cmdline(cmd)
    if len(riga) > 30000:
        print(f"ERRORE TECNICO: riga di comando di {len(riga)} caratteri, oltre il limite di Windows.")
        return 2
    if arg.solo_comando:
        mostrato = [("<schema di decodifica: %d caratteri>" % len(cmd[-1])) if schema is not None and i == len(cmd) - 1
                    else x for i, x in enumerate(cmd)]
        print(subprocess.list2cmdline(mostrato))
        print(f"Richiesta su stdin: {len(richiesta):,} caratteri".replace(",", "."))
        return 0

    ora = dt.datetime.now().strftime("%Y%m%d_%H%M")
    base = cartella / f"K16_{arg.run}_{ora}"
    (base.parent / f"{base.name}_richiesta.txt").write_text(richiesta, encoding="utf-8")
    if schema is not None:
        (base.parent / f"{base.name}_schema.json").write_text(json.dumps(schema, ensure_ascii=False, indent=1),
                                                               encoding="utf-8")
    print(f"Lancio di Claude Code (prova {arg.run}, {'con' if schema is not None else 'senza'} schema): "
          f"puo' durare decine di minuti...", flush=True)
    inizio = time.time()
    try:
        r = subprocess.run(cmd, input=richiesta.encode("utf-8"), capture_output=True, cwd=str(cartella),
                           env=ambiente(), timeout=arg.timeout * 60)
    except subprocess.TimeoutExpired:
        print(f"ERRORE TECNICO: nessuna risposta in {arg.timeout} minuti.")
        return 2
    except OSError as ex:
        print(f"ERRORE TECNICO: Claude Code non si avvia ({ex}). Un blocco dell'antivirus? (DB4, parte c)")
        return 2
    durata = time.time() - inizio
    uscita = r.stdout.decode("utf-8", errors="replace")
    (base.parent / f"{base.name}_uscita_claude.json").write_text(uscita, encoding="utf-8")
    if r.stderr:
        (base.parent / f"{base.name}_errori.txt").write_bytes(r.stderr)
    try:
        busta = json.loads(uscita)
    except json.JSONDecodeError:
        print(f"ERRORE TECNICO: Claude Code non ha restituito JSON (codice {r.returncode}). Prime righe:\n{uscita[:800]}\n"
              f"{r.stderr.decode('utf-8', errors='replace')[:800]}")
        return 2
    payload = busta.get("structured_output") if schema is not None else None
    if payload is None:
        payload = estrai_json(busta.get("result") or "")
    print(riepilogo(busta, payload, durata))
    if busta.get("is_error") or payload is None:
        print(f"Risposta non utilizzabile. Testo di Claude Code (primi 800 caratteri):\n{(busta.get('result') or '')[:800]}")
        return 1
    ciclo = payload.get("ciclo") or "ciclo"
    file_a1 = cartella / f"A1_{ciclo}_claude_{arg.run}.json"
    file_a1.write_text(json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\nRisposta salvata: {file_a1}\nOra il precontrollo (passo 5 del manuale).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
