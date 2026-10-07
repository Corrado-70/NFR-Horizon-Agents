"""Validatore JSON Schema minimo e severo, solo libreria standard.

Unica implementazione del pacchetto: la usano lo script di campo
(esegui_ciclo_locale.py) e la suite di collaudo (99_Collaudo), che la importa
da qui invece di tenerne una copia. Le regole NON sono scritte qui: stanno
negli schemi di 01_Kernel/, che questo modulo interpreta. Se cambia una regola
si cambia solo lo schema.

Costrutti supportati: type (anche lista, con "null"), required, properties,
additionalProperties (solo false), items, minItems, maxItems, uniqueItems,
enum, pattern, minLength, maxLength, minimum, maximum, $ref locale (#/$defs/..).
Un costrutto non supportato presente nello schema e' un ERRORE, non viene
ignorato: un validatore che salta in silenzio una regola la rende finta.

Uso da riga di comando:
    python valida_output.py <schema.json> <payload.json>
Codice di uscita 0 se conforme, 1 se non conforme, 2 se lo schema e' illeggibile.
"""

import json
import re
import sys

# Parole chiave che il validatore sa applicare, piu' quelle solo descrittive.
SUPPORTATE = {
    "type", "required", "properties", "additionalProperties", "items",
    "minItems", "maxItems", "uniqueItems", "enum", "pattern",
    "minLength", "maxLength", "minimum", "maximum", "$ref",
}
DESCRITTIVE = {"$schema", "$id", "title", "description", "$defs"}


def _tipo_ok(valore, tipo):
    # bool e' sottoclasse di int in Python: va escluso esplicitamente,
    # altrimenti true passerebbe come punteggio 1.
    if tipo == "null":
        return valore is None
    if tipo == "boolean":
        return isinstance(valore, bool)
    if tipo == "integer":
        return isinstance(valore, int) and not isinstance(valore, bool)
    if tipo == "number":
        return isinstance(valore, (int, float)) and not isinstance(valore, bool)
    if tipo == "string":
        return isinstance(valore, str)
    if tipo == "array":
        return isinstance(valore, list)
    if tipo == "object":
        return isinstance(valore, dict)
    raise ValueError(f"tipo non supportato nello schema: {tipo}")


def _risolvi(radice, ref):
    if not ref.startswith("#/"):
        raise ValueError(f"$ref non locale non supportato: {ref}")
    nodo = radice
    for parte in ref[2:].split("/"):
        nodo = nodo[parte]
    return nodo


def _valida(valore, schema, radice, percorso, errori):
    sconosciute = set(schema) - SUPPORTATE - DESCRITTIVE
    if sconosciute:
        raise ValueError(f"{percorso}: costrutti non supportati {sorted(sconosciute)}")

    if "$ref" in schema:
        _valida(valore, _risolvi(radice, schema["$ref"]), radice, percorso, errori)
        return

    if "type" in schema:
        tipi = schema["type"] if isinstance(schema["type"], list) else [schema["type"]]
        if not any(_tipo_ok(valore, t) for t in tipi):
            errori.append(f"{percorso}: tipo {type(valore).__name__}, atteso {tipi}")
            return  # i controlli successivi non hanno senso su un tipo sbagliato

    if "enum" in schema and valore not in schema["enum"]:
        errori.append(f"{percorso}: valore {valore!r} fuori da {schema['enum']}")

    if isinstance(valore, str):
        if "minLength" in schema and len(valore) < schema["minLength"]:
            errori.append(f"{percorso}: lunghezza {len(valore)} < {schema['minLength']}")
        if "maxLength" in schema and len(valore) > schema["maxLength"]:
            errori.append(f"{percorso}: lunghezza {len(valore)} > {schema['maxLength']}")
        if "pattern" in schema and not re.search(schema["pattern"], valore):
            errori.append(f"{percorso}: {valore!r} non rispetta {schema['pattern']}")

    if isinstance(valore, (int, float)) and not isinstance(valore, bool):
        if "minimum" in schema and valore < schema["minimum"]:
            errori.append(f"{percorso}: {valore} < minimo {schema['minimum']}")
        if "maximum" in schema and valore > schema["maximum"]:
            errori.append(f"{percorso}: {valore} > massimo {schema['maximum']}")

    if isinstance(valore, list):
        if "minItems" in schema and len(valore) < schema["minItems"]:
            errori.append(f"{percorso}: {len(valore)} elementi < {schema['minItems']}")
        if "maxItems" in schema and len(valore) > schema["maxItems"]:
            errori.append(f"{percorso}: {len(valore)} elementi > {schema['maxItems']}")
        if schema.get("uniqueItems"):
            visti = [json.dumps(v, sort_keys=True) for v in valore]
            if len(visti) != len(set(visti)):
                errori.append(f"{percorso}: elementi duplicati")
        if "items" in schema:
            for i, elemento in enumerate(valore):
                _valida(elemento, schema["items"], radice, f"{percorso}[{i}]", errori)

    if isinstance(valore, dict):
        for campo in schema.get("required", []):
            if campo not in valore:
                errori.append(f"{percorso}: manca il campo obbligatorio '{campo}'")
        proprieta = schema.get("properties", {})
        if "additionalProperties" in schema:
            if schema["additionalProperties"] is not False:
                raise ValueError(f"{percorso}: additionalProperties supportato solo come false")
            for campo in valore:
                if campo not in proprieta:
                    errori.append(f"{percorso}: campo non previsto '{campo}'")
        for campo, sotto in proprieta.items():
            if campo in valore:
                _valida(valore[campo], sotto, radice, f"{percorso}.{campo}", errori)


def valida(payload, schema):
    """Restituisce la lista degli errori (vuota = conforme)."""
    errori = []
    _valida(payload, schema, schema, "$", errori)
    return errori


def carica_json(percorso):
    # utf-8-sig: accetta anche "UTF-8 con BOM", una delle due codifiche UTF-8
    # che il Blocco note propone; senza, il file sarebbe rifiutato come illeggibile.
    with open(percorso, encoding="utf-8-sig") as f:
        return json.load(f)


def main(argv):
    if len(argv) != 3:
        print(__doc__)
        return 2
    try:
        schema = carica_json(argv[1])
    except (OSError, json.JSONDecodeError) as e:
        print(f"Schema illeggibile: {e}")
        return 2
    try:
        payload = carica_json(argv[2])
    except (OSError, json.JSONDecodeError) as e:
        print(f"NON CONFORME: payload illeggibile ({e})")
        return 1
    errori = valida(payload, schema)
    if errori:
        print(f"NON CONFORME: {len(errori)} errori")
        for e in errori:
            print("  -", e)
        return 1
    print("CONFORME")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
