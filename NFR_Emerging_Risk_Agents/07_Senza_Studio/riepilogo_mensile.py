"""Riepilogo mensile (P7, D-100, 04/11/2026): le settimane di un mese in un file Excel e in una pagina HTML.

La cadenza mensile serve alla funzione di rischio senza un agente in piu': il comando `mensile` legge dal registro cio'
che le settimane hanno gia' scritto (tblNews, tblSettimane, tblSintesi, tblRegister) e lo aggrega per il mese:
  - le notizie del mese per segnale e i segnali netti per rischio (peggiorative meno migliorative), anche per i rischi
    in osservazione;
  - la pressione per categoria (notizie, intensita' massima, notizie di intensita' 2 o piu') con il presidio (rischi
    del radar, solo in osservazione, AREA NON PRESIDIATA);
  - le notizie senza rischio collegato (NON PRESIDIATO);
  - i flag proposti da A3 e le proposte di ciclo straordinario delle settimane del mese;
  - le notizie forti su rischi gravi: intensita' 3 su un rischio con Impatto 4 o 5 (la parte (a) della regola del
    segnale critico di A3; le altre due sono giudizio);
  - i cicli straordinari con la data di riferimento nel mese.
Un mese = le settimane (lunedi') che cadono nel mese. Nessun numero nuovo: niente score, niente stime (D-41).
I due file escono dagli stessi dati (calcola), quindi dicono le stesse cose; il collaudo lo verifica.
"""

import datetime as dt
import html
import re
from pathlib import Path

SEGNALI = ("Peggiorativo", "Migliorativo", "Neutro")
NON_PRESIDIATO = "NON PRESIDIATO"
MESI = ["gennaio", "febbraio", "marzo", "aprile", "maggio", "giugno", "luglio", "agosto", "settembre", "ottobre",
        "novembre", "dicembre"]
VUOTI = (None, "", "—", "-")


def nome_mese(mese):
    return f"{MESI[int(mese[5:7]) - 1]} {mese[:4]}"


def _testo(v):
    return "" if v in VUOTI else str(v).strip()


def _data(v):
    return str(v or "")[:10]


def mesi_disponibili(reg):
    """I mesi con almeno una settimana di notizie o di sintesi, dal piu' vecchio."""
    settimane = {_data(n.get("Settimana")) for n in reg.tab.get("tblNews", [])} | \
                {_data(s.get("Settimana")) for s in reg.tab.get("tblSettimane", [])}
    return sorted({s[:7] for s in settimane if re.match(r"\d{4}-\d{2}-\d{2}", s)})


def ultimo_mese_completo(reg):
    """L'ultimo mese con settimane nel registro gia' finito alla settimana corrente (Parametri, settimanaCorrente); se
    nessuno e' finito, l'ultimo con settimane."""
    mesi = mesi_disponibili(reg)
    corrente = _data(reg.nome("settimanaCorrente"))[:7]
    finiti = [m for m in mesi if m < corrente] if corrente else []
    return (finiti or mesi or [None])[-1]


def calcola(reg, mese):
    """I dati del riepilogo del mese AAAA-MM dal registro (un lettore di report_html: tab e nome)."""
    if not re.fullmatch(r"\d{4}-(0[1-9]|1[0-2])", str(mese or "")):
        raise ValueError(f"Mese '{mese}' non valido: AAAA-MM.")
    news = [n for n in reg.tab.get("tblNews", []) if _data(n.get("Settimana"))[:7] == mese]
    sett = sorted((s for s in reg.tab.get("tblSettimane", []) if _data(s.get("Settimana"))[:7] == mese),
                  key=lambda s: _data(s.get("Settimana")))
    settimane = sorted({_data(n.get("Settimana")) for n in news} | {_data(s.get("Settimana")) for s in sett})
    # L'ultima riga di ogni rischio (radar o osservazione): nome, stato, categoria e Impatto di oggi.
    ultime = {}
    for r in sorted(reg.tab.get("tblRegister", []), key=lambda r: str(r.get("Ciclo"))):
        ultime[r["ID_Rischio"]] = r
    codici = list(reg.nome("codiciL1") or [])
    nomi_cat = dict(zip(codici, reg.nome("nomiL1") or []))

    per_rischio = {}
    for n in news:
        rid = _testo(n.get("Rischio_ID")) or NON_PRESIDIATO
        if rid == NON_PRESIDIATO:
            continue
        x = per_rischio.setdefault(rid, {"id": rid, "notizie": 0, **{s: 0 for s in SEGNALI}})
        x["notizie"] += 1
        if n.get("Segnale") in SEGNALI:
            x[n["Segnale"]] += 1
    rischi = []
    for rid, x in per_rischio.items():
        r = ultime.get(rid) or {}
        stato = _testo(r.get("Stato")) or ("Radar" if r else "non nel registro")
        rischi.append({**x, "nome": _testo(r.get("Nome")), "stato": stato, "impatto": r.get("Impatto"),
                       "netti": x["Peggiorativo"] - x["Migliorativo"]})
    rischi.sort(key=lambda x: (-x["netti"], -x["notizie"], x["id"]))

    attivi = [r for r in ultime.values() if _testo(r.get("Stato")) != "Dismesso"]
    categorie = []
    for cod in codici:
        valori = [n.get("Imp_" + cod.replace(".", "_")) or 0 for n in news]
        nel_radar = sum(1 for r in attivi if r.get("Event_Type") == cod and _testo(r.get("Stato")).startswith("Radar"))
        in_oss = sum(1 for r in attivi if r.get("Event_Type") == cod and _testo(r.get("Stato")) == "Osservazione")
        forti = sum(1 for v in valori if v >= 2)
        presidio = ("Presidiata" if nel_radar else "In osservazione" if in_oss else
                    "AREA NON PRESIDIATA" if forti else "Nessun rischio censito")
        categorie.append({"cod": cod, "nome": nomi_cat.get(cod, ""), "notizie": sum(1 for v in valori if v >= 1),
                          "max": max(valori, default=0), "forti": forti, "radar": nel_radar, "osservazione": in_oss,
                          "presidio": presidio})

    def imp_max(n):
        return max((n.get("Imp_" + c.replace(".", "_")) or 0 for c in codici), default=0)
    critiche = [{"data": _data(n.get("Data")), "id": n.get("ID_Notizia"), "titolo": _testo(n.get("Titolo")),
                 "rischio": n.get("Rischio_ID"), "nome": _testo((ultime.get(n.get("Rischio_ID")) or {}).get("Nome")),
                 "segnale": n.get("Segnale"), "sintesi": _testo(n.get("Sintesi"))}
                for n in news if imp_max(n) >= 3 and ((ultime.get(n.get("Rischio_ID")) or {}).get("Impatto") or 0) >= 4]
    non_presidiate = [{"data": _data(n.get("Data")), "id": n.get("ID_Notizia"), "titolo": _testo(n.get("Titolo")),
                       "categorie": ", ".join(c for c in codici if (n.get("Imp_" + c.replace(".", "_")) or 0) >= 2)}
                      for n in news if (_testo(n.get("Rischio_ID")) or NON_PRESIDIATO) == NON_PRESIDIATO]
    flag = [{"settimana": _data(s["Settimana"]), "flag": riga.strip()} for s in sett
            for riga in _testo(s.get("Flag_Proposti")).splitlines() if riga.strip() and riga.strip() not in VUOTI]
    proposte = [{"settimana": _data(s["Settimana"]), "proposta": _testo(s.get("Proposta_Straordinario"))} for s in sett
                if _testo(s.get("Proposta_Straordinario"))]
    straordinari = [{"ciclo": s["Ciclo"], "data": _data(s.get("Data_Riferimento")), "decisione": _testo(s.get("Straordinario"))}
                    for s in reg.tab.get("tblSintesi", []) if "-S" in str(s.get("Ciclo"))
                    and _data(s.get("Data_Riferimento"))[:7] == mese]
    conta = {s: sum(1 for n in news if n.get("Segnale") == s) for s in SEGNALI}
    return {"mese": mese, "nome_mese": nome_mese(mese), "settimane": settimane,
            "settimane_sintesi": [{"settimana": _data(s["Settimana"]), "notizie": s.get("Notizie"),
                                   "sintesi": _testo(s.get("Sintesi_A3"))} for s in sett],
            "notizie": len(news), "segnali": conta, "da_validare": sum(1 for n in news if n.get("Validazione") == "Da validare"),
            "rischi": rischi, "categorie": categorie, "non_presidiate": non_presidiate, "critiche": critiche,
            "flag": flag, "proposte": proposte, "straordinari": straordinari,
            "aree_non_presidiate": [c["cod"] for c in categorie if c["presidio"] == "AREA NON PRESIDIATA"]}


def numeri_chiave(d):
    """I numeri in testa al riepilogo, nello stesso ordine nei due file."""
    return [("Settimane", len(d["settimane"])), ("Notizie", d["notizie"]),
            ("Peggiorative", d["segnali"]["Peggiorativo"]), ("Migliorative", d["segnali"]["Migliorativo"]),
            ("Notizie forti su rischi gravi", len(d["critiche"])), ("Notizie senza rischio", len(d["non_presidiate"])),
            ("Aree non presidiate", len(d["aree_non_presidiate"])), ("Flag di A3", len(d["flag"])),
            ("Proposte di straordinario", len(d["proposte"])), ("Cicli straordinari", len(d["straordinari"]))]


# Le tabelle dei due file: (titolo, intestazioni, righe)
def tabelle(d):
    return [
        ("Segnali per rischio (netti = peggiorative - migliorative)",
         ["ID", "Rischio", "Stato", "Notizie", "Peggiorative", "Migliorative", "Neutre", "Netti"],
         [[x["id"], x["nome"], x["stato"], x["notizie"], x["Peggiorativo"], x["Migliorativo"], x["Neutro"], x["netti"]]
          for x in d["rischi"]]),
        ("Pressione per categoria",
         ["Categoria", "Nome", "Notizie", "Intensita' massima", "Intensita' 2 o piu'", "Rischi nel radar",
          "Rischi in osservazione", "Presidio"],
         [[c["cod"], c["nome"], c["notizie"], c["max"], c["forti"], c["radar"], c["osservazione"], c["presidio"]]
          for c in d["categorie"]]),
        ("Notizie forti su rischi gravi (intensita' 3 su un rischio con Impatto 4-5)",
         ["Data", "Notizia", "Titolo", "Rischio", "Segnale"],
         [[x["data"], x["id"], x["titolo"], f"{x['rischio']} {x['nome']}".strip(), x["segnale"]] for x in d["critiche"]]),
        ("Notizie senza rischio collegato (NON PRESIDIATO)", ["Data", "Notizia", "Titolo", "Categorie (intensita' 2 o piu')"],
         [[x["data"], x["id"], x["titolo"], x["categorie"]] for x in d["non_presidiate"]]),
        ("Flag proposti da A3", ["Settimana", "Flag"], [[x["settimana"], x["flag"]] for x in d["flag"]]),
        ("Proposte di ciclo straordinario (A3)", ["Settimana", "Proposta"], [[x["settimana"], x["proposta"]] for x in d["proposte"]]),
        ("Cicli straordinari del mese", ["Ciclo", "Data di riferimento", "Decisione"],
         [[x["ciclo"], x["data"], x["decisione"]] for x in d["straordinari"]]),
        ("Settimane del mese: sintesi di A3", ["Settimana", "Notizie", "Sintesi"],
         [[x["settimana"], x["notizie"], x["sintesi"]] for x in d["settimane_sintesi"]]),
    ]


NOTA = ("Dalle settimane gia' scritte nel registro: nessun numero nuovo, nessuno score (D-41). I segnali dicono dove "
        "guardare al prossimo trimestre; un evento critico si porta alla funzione di rischio come ciclo straordinario.")


def scrivi_xlsx(d, percorso, intestazione=""):
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Font, PatternFill
    fill = lambda c: PatternFill("solid", fgColor=c, bgColor=c)
    wb = Workbook()
    ws = wb.active
    ws.title = "Riepilogo"
    ws.sheet_view.showGridLines = False
    for col, w in zip("ABCDEFGH", [14, 40, 16, 12, 14, 14, 14, 22]):
        ws.column_dimensions[col].width = w
    ws.merge_cells("A1:H1")
    c = ws.cell(row=1, column=1, value=f"Riepilogo mensile · {d['nome_mese']}" + (f" · {intestazione}" if intestazione else ""))
    c.font, c.fill = Font(size=14, bold=True, color="FFFFFF"), fill("1F3864")
    ws.row_dimensions[1].height = 30
    ws.merge_cells("A2:H2")
    ws.cell(row=2, column=1, value=f"Settimane: {', '.join(d['settimane']) or 'nessuna'}. {NOTA}").alignment = \
        Alignment(wrap_text=True, vertical="top")
    ws.row_dimensions[2].height = 45
    riga = 4
    for etichetta, valore in numeri_chiave(d):
        ws.cell(row=riga, column=1, value=etichetta).font = Font(bold=True)
        ws.cell(row=riga, column=3, value=valore)
        riga += 1
    for titolo, intest, righe in tabelle(d):
        riga += 1
        ws.merge_cells(start_row=riga, start_column=1, end_row=riga, end_column=8)
        ws.cell(row=riga, column=1, value=titolo).font = Font(size=12, bold=True, color="1F3864")
        riga += 1
        for j, t in enumerate(intest, start=1):
            c = ws.cell(row=riga, column=j, value=t)
            c.font, c.fill = Font(bold=True, color="FFFFFF"), fill("2F5597")
            c.alignment = Alignment(wrap_text=True)
        riga += 1
        if not righe:
            ws.cell(row=riga, column=1, value="Nessuna voce nel mese.").font = Font(italic=True, color="595959")
            riga += 1
        for r in righe:
            for j, v in enumerate(r, start=1):
                c = ws.cell(row=riga, column=j, value=v)
                c.alignment = Alignment(wrap_text=True, vertical="top")
                if v == "AREA NON PRESIDIATA":
                    c.font, c.fill = Font(bold=True, color="C00000"), fill("FBE5E5")
            riga += 1
    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToWidth, ws.page_setup.fitToHeight = 1, 0
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    Path(percorso).parent.mkdir(parents=True, exist_ok=True)
    wb.save(percorso)
    return Path(percorso)


CSS = """body{font-family:Segoe UI,Arial,sans-serif;color:#262626;margin:24px auto;max-width:1100px;padding:0 16px}
h1{background:#1F3864;color:#fff;padding:12px 16px;font-size:20px;margin:0 0 8px}h2{color:#1F3864;font-size:16px;
margin:22px 0 6px}p.nota{color:#595959;font-size:13px}.numeri{display:flex;flex-wrap:wrap;gap:8px}.numero{border:1px
solid #BFBFBF;border-radius:6px;padding:8px 12px;min-width:120px}.numero b{display:block;font-size:22px;color:#1F3864}
table{border-collapse:collapse;width:100%;font-size:13px}th{background:#2F5597;color:#fff;text-align:left;padding:5px}
td{border-bottom:1px solid #D9D9D9;padding:5px;vertical-align:top}td.allarme{color:#C00000;font-weight:bold;
background:#FBE5E5}.vuoto{color:#595959;font-style:italic}@media print{body{margin:0}}"""


def scrivi_html(d, percorso, intestazione=""):
    e = lambda v: html.escape("" if v is None else str(v))
    parti = [f"<!doctype html><html lang='it'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,"
             f"initial-scale=1'><title>Riepilogo mensile {e(d['nome_mese'])}</title><style>{CSS}</style></head><body>",
             f"<h1>Riepilogo mensile · {e(d['nome_mese'])}" + (f" · {e(intestazione)}" if intestazione else "") + "</h1>",
             f"<p class='nota'>Settimane: {e(', '.join(d['settimane']) or 'nessuna')}. {e(NOTA)}</p><div class='numeri'>"]
    parti += [f"<div class='numero'><b>{e(v)}</b>{e(k)}</div>" for k, v in numeri_chiave(d)]
    parti.append("</div>")
    for titolo, intest, righe in tabelle(d):
        parti.append(f"<h2>{e(titolo)}</h2>")
        if not righe:
            parti.append("<p class='vuoto'>Nessuna voce nel mese.</p>")
            continue
        parti.append("<table><tr>" + "".join(f"<th>{e(t)}</th>" for t in intest) + "</tr>")
        parti += ["<tr>" + "".join(f"<td class='allarme'>{e(v)}</td>" if v == "AREA NON PRESIDIATA" else f"<td>{e(v)}</td>"
                                   for v in r) + "</tr>" for r in righe]
        parti.append("</table>")
    parti.append(f"<p class='nota'>Prodotto il {dt.date.today().strftime('%d/%m/%Y')} dal comando "
                 "python esegui_ciclo_locale.py mensile.</p></body></html>")
    Path(percorso).parent.mkdir(parents=True, exist_ok=True)
    Path(percorso).write_text("".join(parti), encoding="utf-8")
    return Path(percorso)
