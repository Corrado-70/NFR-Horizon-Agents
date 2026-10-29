"""Installazione dell'app NFR su un PC (D-83, tappa M3): le parti che non toccano il sistema.

Le usa installa.py (che le esegue sul PC) e le prova il collaudo (test_installazione.py) anche senza Windows:
  - quali moduli Python mancano e il comando pip per installarli (dalla rete o da una cartella di pacchetti);
  - la configurazione: valori proposti, unione con quella esistente, controllo delle voci;
  - l'attivita' pianificata della raccolta del lunedi' (XML per schtasks);
  - i collegamenti sul Desktop e in "Invia a" (script PowerShell, nessun pacchetto in piu').

Solo libreria standard.
"""

import datetime as dt
import json
import subprocess
import sys
from pathlib import Path

QUI = Path(__file__).resolve().parent
VERSIONE_MINIMA = (3, 10)
# (prova di import, pacchetto pip, a che cosa serve). La prova di pywin32 importa anche pythoncom: un pywin32
# installato a meta' passa "import win32com" e si ferma alla prima apertura di Excel (guida, sezione 7).
MODULI = [("import win32com.client, pythoncom", "pywin32", "Excel via COM e appunti"),
          ("import openpyxl", "openpyxl", "file delle schede"),
          ("import pypac", "pypac", "proxy della raccolta notizie")]
CARTELLE_PACCHETTI = [QUI / "pacchetti", QUI.parent / "pacchetti"]
NOME_ATTIVITA = "NFR raccolta notizie"
NOME_COLLEGAMENTO = "NFR Horizon Scan"
NOME_INVIA_A = "NFR notizie manuali"
AGENTI = ["A1", "A3", "A4", "A5", "A6", "A7", "A8"]
ORIGINI = ["Agent Builder", "Copilot Studio"]
SEGNAPOSTO = "incollare il link"            # il testo di configurazione_esempio.json


# ------------------------------------------------------------ Python e moduli
def python_adatto(versione=None):
    versione = tuple(versione or sys.version_info[:2])
    return versione >= VERSIONE_MINIMA


def prova_import(istruzione, eseguibile=None):
    """True se l'import riesce in un processo nuovo: vede anche i pacchetti appena installati con pip."""
    try:
        r = subprocess.run([eseguibile or sys.executable, "-c", istruzione], capture_output=True, text=True, timeout=120,
                           creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
        return r.returncode == 0
    except (OSError, subprocess.SubprocessError):
        return False


def moduli_mancanti(prova=prova_import):
    return [(pacchetto, uso) for istruzione, pacchetto, uso in MODULI if not prova(istruzione)]


def cartella_pacchetti(cartelle=None):
    """La cartella dei pacchetti scaricati altrove (pip download ... -d pacchetti), se c'e' e non e' vuota."""
    for c in cartelle or CARTELLE_PACCHETTI:
        if Path(c).is_dir() and any(Path(c).iterdir()):
            return Path(c)
    return None


def comando_pip(pacchetti, cartella=None, eseguibile=None):
    """pip install --user: nessun diritto di amministratore. Con una cartella di pacchetti, solo da li' (--no-index)."""
    cmd = [eseguibile or sys.executable, "-m", "pip", "install", "--user", "--disable-pip-version-check"]
    if cartella:
        cmd += ["--no-index", "--find-links", str(cartella)]
    return cmd + sorted(set(pacchetti))


def spiega_pip(uscita):
    """Il motivo piu' probabile di un pip non riuscito, in parole semplici."""
    testo = (uscita or "").lower()
    if any(p in testo for p in ("proxy", "connection", "timed out", "certificate", "ssl", "getaddrinfo", "network")):
        return ("la rete del PC non lascia scaricare i pacchetti (proxy o certificati). Due strade: chiedere all'IT di "
                "installarli, oppure su un PC con la rete libera lanciare  python -m pip download pywin32 openpyxl pypac "
                "-d pacchetti  e copiare la cartella 'pacchetti' accanto a 07_Senza_Studio; poi rilanciare installa.cmd.")
    if "no matching distribution" in testo or "could not find a version" in testo:
        return ("nella cartella dei pacchetti manca la versione giusta per questo Python: scaricarli con lo stesso Python "
                "(stessa versione e 64 bit) che c'e' su questo PC.")
    if "no module named pip" in testo:
        return "questo Python non ha pip: chiedere all'IT un Python 3.10+ completo (python.org o Software Center)."
    return "vedere il messaggio di pip qui sopra; se non e' chiaro, mandarlo a chi mantiene il pacchetto."


# ------------------------------------------------------------ configurazione
def carica_configurazione(percorso):
    percorso = Path(percorso)
    if not percorso.exists():
        return {}
    return json.loads(percorso.read_text(encoding="utf-8-sig"))


def link_della_versione(conf, origine):
    """I link degli agenti di una versione, da link_agenti piatto o per versione (come flussi.Flussi.link)."""
    link = conf.get("link_agenti") or {}
    if any(isinstance(v, dict) for v in link.values()):
        link = link.get(origine) or {}
    return {a: str(link.get(a) or "") for a in AGENTI}


def unisci(vecchia, nuova, origine=None):
    """La configurazione da salvare: le voci della finestra sopra quelle che c'erano; le voci che la finestra non
    conosce (cartella_lavoro, attesa_lucchetto...) restano. I link si scrivono nella versione degli agenti scelta, e
    quelli dell'altra versione restano."""
    risultato = dict(vecchia)
    link_nuovi = nuova.get("link_agenti")
    risultato.update({k: v for k, v in nuova.items() if k != "link_agenti"})
    if link_nuovi is not None:
        vecchi = vecchia.get("link_agenti") or {}
        per_versione = any(isinstance(v, dict) for v in vecchi.values())
        origine = origine or nuova.get("agenti") or ORIGINI[0]
        if per_versione:
            risultato["link_agenti"] = {**vecchi, origine: {**(vecchi.get(origine) or {}), **link_nuovi}}
        elif origine != ORIGINI[0] and any(v and SEGNAPOSTO not in v for v in vecchi.values()):
            # c'erano i link di Agent Builder e si scrivono quelli di Copilot Studio: si passa al formato per versione
            risultato["link_agenti"] = {ORIGINI[0]: vecchi, origine: link_nuovi}
        else:
            risultato["link_agenti"] = {**vecchi, **link_nuovi}
    return risultato


def problemi(conf):
    """(gravi, avvisi) della configurazione: i gravi impediscono di lavorare, gli avvisi no."""
    gravi, avvisi = [], []
    for voce, cosa, file in (("workbook", "il registro", True), ("kernel", "la cartella Kernel", False),
                             ("cartella_uscita", "la cartella Archivio_Cicli", False), ("news_inbox", "la cartella News_Inbox", False)):
        valore = conf.get(voce)
        if not valore:
            gravi.append(f"{voce}: manca ({cosa})")
        elif not file and not Path(valore).is_dir():
            gravi.append(f"{voce}: la cartella {valore} non esiste (e' sincronizzata con OneDrive?)")
        elif file and not Path(valore).parent.is_dir():
            gravi.append(f"{voce}: la cartella del registro {Path(valore).parent} non esiste")
        elif file and not Path(valore).exists():
            avvisi.append(f"{voce}: {valore} non c'e' ancora (si crea con inizializza, guida 0.4)")
    if not str(conf.get("utente") or "").strip():
        gravi.append("utente: manca il nome (lo vedono i colleghi quando scrivi nel registro)")
    origine = conf.get("agenti") or ORIGINI[0]
    if origine not in ORIGINI:
        gravi.append(f"agenti: {origine!r} non e' fra {ORIGINI}")
    link = link_della_versione(conf, origine if origine in ORIGINI else ORIGINI[0])
    vuoti = [a for a, v in link.items() if not v.startswith("http")]
    if vuoti:
        avvisi.append(f"link_agenti ({origine}): senza link {', '.join(vuoti)}: quegli agenti si aprono a mano")
    return gravi, avvisi


def salva_configurazione(percorso, conf):
    """Scrive configurazione.json; la versione precedente resta accanto, con data e ora nel nome."""
    percorso = Path(percorso)
    if percorso.exists():
        copia = percorso.with_name(f"configurazione_{dt.datetime.now():%Y%m%d_%H%M%S}.json.precedente")
        copia.write_bytes(percorso.read_bytes())
    percorso.write_text(json.dumps(conf, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return percorso


# ------------------------------------------------------------ attivita' pianificata della raccolta
def xml_attivita(eseguibile, script, cartella, inizio=None):
    """Attivita' di Windows: ogni lunedi' alle 7, per l'utente collegato, senza privilegi; se il PC era spento parte
    appena possibile; solo con la rete. Da salvare in UTF-16 per schtasks /xml."""
    inizio = inizio or dt.date.today()
    lunedi = inizio + dt.timedelta(days=(7 - inizio.weekday()) % 7)
    x = lambda t: (str(t).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;"))
    return f"""<?xml version="1.0" encoding="UTF-16"?>
<Task version="1.2" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
  <RegistrationInfo>
    <Description>NFR Horizon Scan: raccolta delle notizie del lunedi' (raccogli_notizie.py, guida sezione 1).</Description>
  </RegistrationInfo>
  <Triggers>
    <CalendarTrigger>
      <StartBoundary>{lunedi.isoformat()}T07:00:00</StartBoundary>
      <Enabled>true</Enabled>
      <ScheduleByWeek>
        <DaysOfWeek><Monday /></DaysOfWeek>
        <WeeksInterval>1</WeeksInterval>
      </ScheduleByWeek>
    </CalendarTrigger>
  </Triggers>
  <Principals>
    <Principal id="Autore">
      <LogonType>InteractiveToken</LogonType>
      <RunLevel>LeastPrivilege</RunLevel>
    </Principal>
  </Principals>
  <Settings>
    <MultipleInstancesPolicy>IgnoreNew</MultipleInstancesPolicy>
    <DisallowStartIfOnBatteries>false</DisallowStartIfOnBatteries>
    <StopIfGoingOnBatteries>false</StopIfGoingOnBatteries>
    <StartWhenAvailable>true</StartWhenAvailable>
    <RunOnlyIfNetworkAvailable>true</RunOnlyIfNetworkAvailable>
    <ExecutionTimeLimit>PT1H</ExecutionTimeLimit>
    <Enabled>true</Enabled>
  </Settings>
  <Actions Context="Autore">
    <Exec>
      <Command>{x(eseguibile)}</Command>
      <Arguments>"{x(script)}"</Arguments>
      <WorkingDirectory>{x(cartella)}</WorkingDirectory>
    </Exec>
  </Actions>
</Task>
"""


def comando_attivita(file_xml):
    return ["schtasks", "/create", "/tn", NOME_ATTIVITA, "/xml", str(file_xml), "/f"]


def eseguibile_senza_finestra(eseguibile=None):
    """pythonw.exe accanto a python.exe: la raccolta e l'app partono senza la finestra nera del Prompt dei comandi."""
    e = Path(eseguibile or sys.executable)
    w = e.with_name("pythonw.exe")
    return w if e.name.lower() == "python.exe" and w.exists() else e


# ------------------------------------------------------------ collegamenti
def _ps(testo):
    return "'" + str(testo).replace("'", "''") + "'"


def script_collegamento(cartella_speciale, nome, destinazione, argomenti="", cartella_lavoro="", descrizione=""):
    """Script PowerShell che crea <cartella speciale>\\<nome>.lnk (Desktop, SendTo) con WScript.Shell, presente in ogni
    Windows: nessun pacchetto in piu'. La cartella speciale si chiede a Windows (un Desktop spostato in OneDrive va bene)."""
    return ("$ErrorActionPreference = 'Stop'; "
            f"$c = [Environment]::GetFolderPath({_ps(cartella_speciale)}); "
            f"$l = (New-Object -ComObject WScript.Shell).CreateShortcut((Join-Path $c {_ps(nome + '.lnk')})); "
            f"$l.TargetPath = {_ps(destinazione)}; $l.Arguments = {_ps(argomenti)}; "
            f"$l.WorkingDirectory = {_ps(cartella_lavoro)}; $l.Description = {_ps(descrizione)}; $l.Save(); "
            "Write-Output (Join-Path $c " + _ps(nome + ".lnk") + ")")


def comando_powershell(script):
    return ["powershell", "-NoProfile", "-NonInteractive", "-ExecutionPolicy", "Bypass", "-Command", script]


def collegamenti(eseguibile=None, cartella=None):
    """I due collegamenti: l'app sul Desktop, i file a mano in "Invia a"."""
    cartella = Path(cartella or QUI)
    app = eseguibile_senza_finestra(eseguibile)
    return [
        ("Desktop", NOME_COLLEGAMENTO, str(app), f'"{cartella / "app_nfr.py"}"', str(cartella),
         "Apre l'app NFR Horizon Scan"),
        ("SendTo", NOME_INVIA_A, str(cartella / "NFR_notizie_manuali.cmd"), "", str(cartella),
         "Copia i file scelti in News_Inbox\\<lunedi'>\\Manuali"),
    ]


def comandi_mantieni_sul_pc(cartella):
    """attrib +P: OneDrive tiene la cartella sempre sul PC ("Mantieni sempre su questo dispositivo"), cosi' Excel e lo
    script non aspettano un download a meta' lavoro. La cartella (i file nuovi ereditano) e cio' che contiene gia'."""
    c = Path(cartella)
    return [["attrib", "+P", str(c)], ["attrib", "+P", str(c / "*"), "/S", "/D"]]
