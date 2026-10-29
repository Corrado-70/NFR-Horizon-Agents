"""Verifica del PC (D-83, tappa M3): che cosa serve all'app su questo PC, riga per riga, e che cosa manca.

Una riga per voce, con l'esito OK, ATTENZIONE (si lavora, ma qualcosa va sistemato) o NO (cosi' non si lavora) e che
cosa fare. Le voci: Python e moduli; configurazione.json; cartelle sincronizzate e scrivibili; kernel e template;
registro (chiuso, versione del template) ed Excel via COM con AutoSaveOn e FullName (verifica V-F); lucchetto;
appunti; link degli agenti; collegamenti e, sul PC della raccolta, l'attivita' del lunedi'.

Solo lettura: non scrive nel registro; nell'archivio solo il file della verifica (Verifiche_PC/), da mandare a chi
mantiene il pacchetto se qualcosa non va. Codice di uscita: 0 tutto OK o solo attenzioni, 1 almeno un NO.

Uso: python verifica_pc.py [--senza-excel]
"""

import argparse
import datetime as dt
import os
import platform
import subprocess
import sys
import tempfile
from pathlib import Path

import installazione

QUI = Path(__file__).resolve().parent
OK, ATTENZIONE, NO = "OK", "ATTENZIONE", "NO"
FILE_KERNEL = ["mappatura_campi.json", "schema_output_A1.json", "schema_output_A3.json", "schema_output_A5.json",
               "schema_output_A6.json", "fonti.md", "controlli_A5.md", "guida_scrittura_A1.md", "rubrica_scoring.md",
               "tassonomia_nfr.md"]
TEMPLATE = QUI.parent / "03_Excel" / "NFR_Dashboard_Template.xlsx"
CARTELLA_VERIFICHE = "Verifiche_PC"


def riga(esito, voce, dettaglio="", rimedio=""):
    return {"esito": esito, "voce": voce, "dettaglio": dettaglio, "rimedio": rimedio}


# ------------------------------------------------------------ le voci
def voce_python():
    v = ".".join(map(str, sys.version_info[:3]))
    if not installazione.python_adatto():
        return [riga(NO, "Python", f"{v} ({sys.executable})", "serve Python 3.10 o piu' recente: chiederlo all'IT")]
    righe = [riga(OK, "Python", f"{v}, {platform.architecture()[0]} ({sys.executable})")]
    try:
        import tkinter  # noqa: F401
        righe.append(riga(OK, "tkinter (la finestra dell'app)"))
    except ImportError:
        righe.append(riga(NO, "tkinter (la finestra dell'app)", "non installato",
                          "reinstallare Python con l'opzione tcl/tk (python.org la include di default)"))
    return righe


def voce_moduli(prova=installazione.prova_import):
    righe = []
    for istruzione, pacchetto, uso in installazione.MODULI:
        if prova(istruzione):
            righe.append(riga(OK, f"modulo {pacchetto}", uso))
        else:
            grave = pacchetto == "pywin32"
            righe.append(riga(NO if grave else ATTENZIONE, f"modulo {pacchetto}", f"manca ({uso})",
                              "lanciare installa.cmd" + ("" if grave else "; senza, " + ("niente file delle schede in Excel"
                                                                                        if pacchetto == "openpyxl" else
                                                                                        "la raccolta usa il proxy di sistema"))))
    return righe


def voce_configurazione(conf_grezza, file_conf):
    if not conf_grezza:
        return [riga(NO, "configurazione.json", f"non trovato in {file_conf.parent}", "lanciare installa.cmd (configurazione guidata)")]
    gravi, avvisi = installazione.problemi(conf_grezza)
    righe = [riga(NO, "configurazione", g, "installa.cmd o configurazione.json (guida, sezione 0.3)") for g in gravi]
    righe += [riga(ATTENZIONE, "configurazione", a, "installa.cmd o configurazione.json (guida, sezione 0.3)") for a in avvisi]
    return righe or [riga(OK, "configurazione", f"{file_conf}")]


def scrivibile(cartella):
    try:
        with tempfile.NamedTemporaryFile(dir=cartella, prefix="~$verifica_", delete=True) as f:
            f.write(b"x")
        return True
    except OSError:
        return False


def voce_cartelle(conf):
    righe = []
    for voce, nome in (("cartella_uscita", "Archivio_Cicli"), ("news_inbox", "News_Inbox"), ("kernel", "Kernel")):
        c = conf.get(voce)
        if not c or not Path(c).is_dir():
            righe.append(riga(NO, f"cartella {nome}", f"{c} non trovata", "sincronizzarla con OneDrive (guida, 0.3) e "
                              "correggere configurazione.json"))
        elif voce != "kernel" and not scrivibile(c):
            righe.append(riga(NO, f"cartella {nome}", f"{c}: non si puo' scrivere", "permessi della library SharePoint (guida, 0.1)"))
        else:
            righe.append(riga(OK, f"cartella {nome}", str(c)))
    w = conf.get("workbook")
    if w and Path(w).parent.is_dir() and not scrivibile(Path(w).parent):
        righe.append(riga(NO, "cartella del registro", f"{Path(w).parent}: non si puo' scrivere", "permessi della library"))
    return righe


def voce_kernel(conf):
    k = Path(conf.get("kernel") or "")
    if not k.is_dir():
        return []
    mancanti = [f for f in FILE_KERNEL if not (k / f).exists()]
    righe = [riga(ATTENZIONE if mancanti else OK, "file del kernel",
                  f"mancano {', '.join(mancanti)}" if mancanti else f"{len(FILE_KERNEL)} file in {k}",
                  "copiare nella library Kernel tutti i file di 01_Kernel del pacchetto" if mancanti else "")]
    righe.append(riga(OK if TEMPLATE.exists() else ATTENZIONE, "template del registro",
                      str(TEMPLATE) if TEMPLATE.exists() else f"manca {TEMPLATE}",
                      "" if TEMPLATE.exists() else "serve a inizializza e aggiorna-registro (guida, sezione 7, \"Template non trovato\")"))
    return righe


def voce_registro(conf, con_excel=True):
    """Registro chiuso, poi Excel via COM in sola lettura: versione del template, FullName e AutoSaveOn (V-F)."""
    from esegui_ciclo_locale import VERSIONE_TEMPLATE, aperto_qui, versione_workbook
    w = Path(conf.get("workbook") or "")
    if not w.name or not w.exists():
        return [riga(ATTENZIONE, "registro", f"{w} non c'e' ancora", "si crea con inizializza (guida, 0.4)")]
    if aperto_qui(w):
        return [riga(ATTENZIONE, "registro", f"{w.name} e' aperto in Excel su questo PC", "chiuderlo e rilanciare la verifica")]
    if not con_excel:
        return [riga(OK, "registro", f"{w} (Excel non provato: --senza-excel)")]
    try:
        from excel_com import SessioneExcel
        with SessioneExcel(w, sola_lettura=True) as s:
            versione = versione_workbook(s)
            nome = str(s.wb.FullName)
            try:
                autosave = bool(s.wb.AutoSaveOn)
            except Exception:                        # noqa: BLE001 - Excel senza la proprieta'
                autosave = None
    except ImportError as ex:
        return [riga(NO, "Excel via COM", f"pywin32 non utilizzabile ({ex})", "lanciare installa.cmd")]
    except Exception as ex:                          # noqa: BLE001 - qualunque errore di Excel va riportato, non nascosto
        return [riga(NO, "Excel via COM", f"{type(ex).__name__}: {ex}", "Excel desktop installato e attivato? Chiudere "
                     "ogni Excel e riprovare; se si ripete, mandare questo file a chi mantiene il pacchetto")]
    righe = [riga(OK, "Excel via COM", "il registro si apre in un Excel invisibile e si richiude")]
    righe.append(riga(OK if versione == VERSIONE_TEMPLATE else NO, "versione del registro",
                      f"{versione or 'precedente al 25/09/2026'} (lo script vuole {VERSIONE_TEMPLATE})",
                      "" if versione == VERSIONE_TEMPLATE else "aggiorna-registro (guida, 0-bis)"))
    cloud = nome.lower().startswith("http")
    righe.append(riga(ATTENZIONE if cloud else OK, "FullName del registro (V-F)", nome,
                      "Excel lo apre come documento cloud: la copia di lavoro protegge comunque la scrittura; avvisare chi "
                      "mantiene il pacchetto" if cloud else ""))
    righe.append(riga(OK, "AutoSaveOn del registro (V-F)", "non disponibile in questo Excel" if autosave is None else
                      f"{'acceso' if autosave else 'spento'} all'apertura (lo script lo spegne sulla sua copia)"))
    return righe


def voce_lucchetto(conf):
    import lucchetto
    c = conf.get("cartella_uscita")
    if not c or not Path(c).is_dir():
        return []
    altrui = lucchetto.stato(c)
    if altrui:
        return [riga(ATTENZIONE, "lucchetto del registro", lucchetto.descrivi(altrui),
                     "se chi e' indicato non sta lavorando: Altro -> Togli il lucchetto rimasto (sblocca)")]
    try:
        with lucchetto.preso(c, "verifica_pc", conf.get("utente"), attesa=0):
            pass
    except Exception as ex:                          # noqa: BLE001 - Occupato o cartella non scrivibile
        return [riga(NO, "lucchetto del registro", f"{type(ex).__name__}: {ex}", "permessi di Archivio_Cicli")]
    return [riga(OK, "lucchetto del registro", "libero; presa e rilascio riusciti")]


def voce_appunti():
    try:
        import appunti
        if appunti.disponibili():
            return [riga(OK, "appunti", "l'app puo' leggere il pulsante Copia degli agenti")]
    except Exception:                                # noqa: BLE001
        pass
    return [riga(ATTENZIONE, "appunti", "ascolto non disponibile", "le risposte si incollano nel riquadro (Ctrl+V)")]


def voce_link(conf_grezza):
    origine = conf_grezza.get("agenti") or installazione.ORIGINI[0]
    link = installazione.link_della_versione(conf_grezza, origine)
    buoni = [a for a, v in link.items() if v.startswith("https://")]
    vuoti = [a for a in installazione.AGENTI if a not in buoni]
    if not vuoti:
        return [riga(OK, f"link degli agenti ({origine})", "tutti e 7; che aprano la chat si vede dall'app (V-A)")]
    return [riga(ATTENZIONE, f"link degli agenti ({origine})", f"senza link: {', '.join(vuoti)}",
                 "Copia collegamento dall'agente (guida, 0.2 punto 3-bis) e installa.cmd")]


def _schtasks_presente(nome):
    try:
        r = subprocess.run(["schtasks", "/query", "/tn", nome], capture_output=True, text=True, timeout=60,
                           creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
        return r.returncode == 0
    except (OSError, subprocess.SubprocessError):
        return False


def _collegamento_presente(cartella_speciale, nome):
    try:
        r = subprocess.run(installazione.comando_powershell(
            f"Test-Path (Join-Path ([Environment]::GetFolderPath('{cartella_speciale}')) '{nome}.lnk')"),
            capture_output=True, text=True, timeout=60, creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
        return r.stdout.strip().lower() == "true"
    except (OSError, subprocess.SubprocessError):
        return False


def voce_collegamenti(conf_grezza, attivita=_schtasks_presente, collegamento=_collegamento_presente):
    if os.name != "nt":
        return []
    righe = [riga(OK if collegamento("Desktop", installazione.NOME_COLLEGAMENTO) else ATTENZIONE,
                  "collegamento sul Desktop", installazione.NOME_COLLEGAMENTO, "installa.cmd"),
             riga(OK if collegamento("SendTo", installazione.NOME_INVIA_A) else ATTENZIONE,
                  "Invia a -> NFR notizie manuali", "", "installa.cmd")]
    for r in righe:
        if r["esito"] == OK:
            r["rimedio"] = ""
    if conf_grezza.get("raccolta_su_questo_pc", True):
        presente = attivita(installazione.NOME_ATTIVITA)
        righe.append(riga(OK if presente else ATTENZIONE, "raccolta del lunedi' (attivita' pianificata)",
                          installazione.NOME_ATTIVITA if presente else "non pianificata su questo PC della raccolta",
                          "" if presente else "installa.cmd, oppure Utilita' di pianificazione a mano (guida, sezione 1)"))
    return righe


# ------------------------------------------------------------ insieme
def verifica(con_excel=True, file_conf=None):
    file_conf = Path(file_conf or QUI / "configurazione.json")
    conf_grezza = installazione.carica_configurazione(file_conf) if file_conf.exists() else {}
    righe = voce_python() + voce_moduli() + voce_configurazione(conf_grezza, file_conf)
    if conf_grezza:
        conf = {k: (Path(v) if k in ("workbook", "kernel", "cartella_uscita", "news_inbox") and v else v)
                for k, v in conf_grezza.items()}
        righe += voce_cartelle(conf) + voce_kernel(conf) + voce_registro(conf, con_excel) + voce_lucchetto(conf)
        righe += voce_link(conf_grezza) + voce_collegamenti(conf_grezza)
    righe += voce_appunti()
    return righe, conf_grezza


def testo(righe, conf):
    adesso = dt.datetime.now()
    intestazione = [f"Verifica del PC per l'app NFR - {adesso:%d/%m/%Y %H:%M}",
                    f"PC: {platform.node()}   utente Windows: {os.environ.get('USERNAME', '?')}   utente NFR: {conf.get('utente', '?')}",
                    f"Windows: {platform.platform()}", ""]
    corpo = []
    for r in righe:
        corpo.append(f"[{r['esito']:<10}] {r['voce']}" + (f": {r['dettaglio']}" if r["dettaglio"] else ""))
        if r["rimedio"] and r["esito"] != OK:
            corpo.append(f"             -> {r['rimedio']}")
    n = {e: sum(1 for r in righe if r["esito"] == e) for e in (OK, ATTENZIONE, NO)}
    finale = ["", f"Esito: {n[OK]} OK, {n[ATTENZIONE]} da sistemare, {n[NO]} che impediscono di lavorare."]
    return "\n".join(intestazione + corpo + finale) + "\n"


def salva(contenuto, conf):
    """Il file della verifica nell'archivio (Verifiche_PC/), o accanto agli script se l'archivio non c'e'."""
    nome = f"Verifica_{platform.node() or 'PC'}_{dt.datetime.now():%Y%m%d_%H%M}.txt"
    for base in (conf.get("cartella_uscita"), QUI):
        try:
            if base and Path(base).is_dir():
                c = Path(base) / CARTELLA_VERIFICHE
                c.mkdir(exist_ok=True)
                (c / nome).write_text(contenuto, encoding="utf-8")
                return c / nome
        except OSError:
            continue
    return None


def main(argv=None):
    p = argparse.ArgumentParser(description="Verifica del PC per l'app NFR")
    p.add_argument("--senza-excel", action="store_true", help="non apre il registro con Excel")
    arg = p.parse_args(argv)
    righe, conf = verifica(con_excel=not arg.senza_excel)
    contenuto = testo(righe, conf)
    print(contenuto)
    file = salva(contenuto, conf)
    if file:
        print(f"Verifica salvata in {file}: se qualcosa e' NO o da sistemare, mandarla a chi mantiene il pacchetto.")
    return 1 if any(r["esito"] == NO for r in righe) else 0


if __name__ == "__main__":
    sys.exit(main())
