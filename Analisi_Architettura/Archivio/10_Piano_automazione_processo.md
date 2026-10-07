# 10. Piano: automazione del processo per l'analista (procedura guidata)

Data: 27/09/2026. Stato: **proposta, non ancora approvata** per la
realizzazione. Oggetto: il pacchetto `NFR_Emerging_Risk_Agents/` alla versione
della struttura 2026-09-25c.

Richiesta dell'utente: rianalizzare software e architettura, cercare
miglioramenti o ristrutturazioni restando nei vincoli (Microsoft 365 Copilot,
Python se serve, comandi shell di Windows) e valutare in dettaglio quanto si
puo' automatizzare il processo. Obiettivi: niente copia-incolla; gli agenti
fanno il piu' possibile; ogni azione manuale rimasta si lancia con una "macro"
o uno script semplicissimo, perche' chi usa il sistema e' un analista, non un
programmatore.

**Scelte dell'utente del 27/09:**
- **Python resta il motore**, con sopra uno strato di automazione. Il piano 07
  (senza Python) passa **in riserva**: si riprende solo se la Banca vietasse
  Python sul PC. La voce AR1 del TODO si chiude con questa motivazione
  (registrata come **D-43** il 28/09).
- L'interfaccia e' un **menu in una finestra di testo**, con lo stato del
  processo e il prossimo passo proposto: Invio = procedi.

**Estensione del 28/09** (parte seconda, sezioni 10.9-10.19), su richiesta
dell'utente: l'opzione separata **Copilot Studio**. Risponde a tre domande:
quanto si automatizza in piu'; se e quanto Python si puo' togliere; quali passi
di questo piano sono **comuni alle due strade** e si possono fare subito. Non
cambia le scelte del 27/09.

**Aggiornamento del 28/09, dopo l'estensione:**
- **Copilot Studio e Power Query sono disponibili** nel tenant (D-44). Usare
  Copilot Studio **non e' deciso**: l'utente lo trova piu' complesso. La
  scelta fra strada A e variante CS-1 e' la decisione aperta **A-15**.
- **Le voci di lavoro di questo piano sono nel TODO del pacchetto**
  (`NFR_Emerging_Risk_Agents/TODO_possibili_sviluppi.md`, voci AU1-AU6), con
  un ordine unico insieme alle voci P, Q e G. Qui resta il dettaglio tecnico.
  Corrispondenza:
  - AU1 = C2 + C3;
  - AU2 = C4-C7;
  - AU3 = C8;
  - AU4 = scelta della strada (A-15), con la prova K0 facoltativa;
  - AU5 = parte della sola strada A;
  - AU6 = K1-K6.

  C9 (collaudo e documentazione) e' distribuita nelle voci.

**Aggiornamento del 06/10 (D-71, struttura 2026-10-06):** A5 e' facoltativo e
nessun suo rilievo ferma il ciclo; `trimestrale` ferma solo i difetti di
integrita' e scrive da se' il messaggio per A1 (`Correzione_A1_<ciclo>.txt`,
una parte di `messaggio_correzione` di AU2). Il trimestre conta un passo con
l'agente in meno, e precontrollo e A5 diventano voci facoltative del menu di
AU5. In Banca Copilot Studio ha solo l'esperienza standard; la knowledge
SharePoint risulta "Bloccata" (probabile data policy) e il Code interpreter e'
da verificare: se il codice nell'agente non e' possibile, la strada resta la A.

**Aggiornamento del 02/10 (D-67, struttura 2026-10-02):** la validazione si fa
in una **griglia**, una riga per rischio, KRI, azione e notizia, con le celle
gialle gia' compilate con le proposte; una riga non toccata vale come
accettata e `--accetta-il-resto` non serve piu'. Per la procedura guidata
(10.4, il menu): la validazione apre la griglia senza filtri da mettere e non chiede piu'
"accetti le righe lasciate vuote?"; nel settimanale "accetto le notizie?"
lancia `valida` senza opzioni. Per la tabella 10.1: "filtrare" sparisce dai
passi della validazione. I punti interessati sono corretti nel testo.

---

## 10.1 Il problema: quanti passi manuali ci sono oggi

Il pacchetto funziona ed e' collaudato: cinque agenti in Agent Builder, lo
script `07_Senza_Studio/esegui_ciclo_locale.py` che controlla e scrive nel
registro Excel via COM, validazione umana tracciata. Usarlo ogni giorno pero'
e' faticoso.

| Processo | Passi manuali oggi (`00_GUIDA_PASSO_PASSO.md`) |
|---|---|
| Trimestre | circa **13**, fra cui 9 comandi da scrivere nel Prompt dei comandi (con `cd`, nomi di file, `--periodo`, `--validatore`), 3 salvataggi in Blocco note (UTF-8, tipo "Tutti i file", nome esatto), la copia a mano di `Baseline_corrente.txt` in `Kernel`, la copia dei prompt nell'archivio, il PDF del report fatto a mano (fogli selezionati con Maiusc, opzioni di stampa) |
| Settimana | circa **7**, fra cui un salvataggio in Blocco note e un comando |
| Validazione | aprire il registro, filtrare (dal 02/10 non serve: griglia, D-67), decidere, salvare, chiudere, scrivere il comando `valida` con periodo e validatore |

I blocchi della prima installazione del 24/09 erano tutti di questo tipo: file
salvato come `.json.txt`, `Workbook non trovato: None`, pythoncom installato a
meta', proxy.

## 10.2 Esito della rianalisi

### Cosa resta com'e'

E' il valore del progetto, e nessuna delle modifiche proposte lo tocca:
- il kernel come fonte unica;
- gli schemi JSON come contratto fra agenti e scrittura;
- i controlli deterministici prima della scrittura, con fermo pulito;
- la validazione umana "tutto o niente", con blocco del ciclo successivo;
- le decisioni D-41 e D-42;
- il workbook 2026-09-25c e le sue oltre 414 verifiche.

Il motore **non si riscrive**: cambia solo nei punti mirati delle fasi F1 e F5.

### Cosa si puo' automatizzare, e cosa no

Agent Builder non ha API, non ha azioni e non scrive file: per questo resta
manuale un'interazione con ogni agente. Si riduce pero' a tre gesti:
1. trascinare nella chat i file che la procedura ha gia' preparato;
2. incollare il testo della richiesta, che la procedura ha gia' messo negli
   appunti, e inviare;
3. premere **Copia** sotto la risposta.

Da li' la procedura se ne accorge da sola, perche' ascolta gli appunti: estrae
il JSON, riconosce l'agente, controlla lo schema, da' il nome al file e passa
al passo dopo.

Restano umani **per scelta**, non per limiti tecnici:
- le decisioni di validazione;
- i file da salvare in `Manuali`;
- ricaricare le istruzioni in Agent Builder quando cambiano.

| Processo | Oggi | Con la procedura guidata |
|---|---|---|
| Trimestre | circa 13 passi, 9 comandi scritti, 3 Blocco note | Invio; per A1, A5 e A6 i tre gesti di sopra; validazione in Excel; nessun comando, nessun nome di file |
| Settimana | circa 7 passi, 1 Blocco note | Invio; eventuali file in `Manuali`; per A3 i tre gesti; "accetto le notizie? S/N" |
| Report al comitato | PDF a mano | automatico dopo la validazione e le schede |
| Correzione dopo un FERMATO | leggere i motivi e riscriverli all'agente | messaggio di correzione gia' negli appunti: incollarlo nella chat dell'agente |

### Rischio nuovo trovato nella rianalisi: il Salvataggio automatico

Excel apre i file di una cartella sincronizzata con OneDrive come documenti
cloud, con il **Salvataggio automatico** attivo. Via COM, le righe gia'
scritte prima di un fermo per i controlli dopo la scrittura (formule, errori,
copertura) potrebbero essere gia' salvate. Il fermo pulito non sarebbe piu'
garantito, e questo potrebbe spiegare anche l'errore `RPC_E_DISCONNECTED` del
24/09. Collaudo e demo non lo vedono, perche' girano su cartelle locali. La
mitigazione e' nella fase F5; la verifica e' la V-F (sezione 10.5).

### Opzioni scartate

| Opzione | Perche' no |
|---|---|
| Automazione del browser (guidare la chat di Copilot con uno script) | fragile a ogni cambio di interfaccia, contraria alle politiche della Banca |
| Macro VBA nel registro | le macro dei file su SharePoint e OneDrive sono di norma bloccate; la logica dei controlli andrebbe duplicata fuori da Python |
| Script PowerShell `.ps1` | di solito bloccati dall'execution policy: si usano solo lanciatori `.cmd` |
| Copilot Studio, API di Microsoft 365 Copilot | fuori dai vincoli del 27/09; restano l'evoluzione possibile. Copilot Studio e' valutato come opzione separata nella parte seconda (10.9-10.19); dal 28/09 risulta disponibile (D-44) e l'uso e' da decidere (A-15) |
| File scaricabile dal code interpreter | spento per D-11; resta comunque accettato come ingresso alternativo, trascinando il file |
| Piano 07 (Power Query, niente Python) | in riserva, per scelta dell'utente: toglie l'installazione ma non i passi manuali (lo dice lo stesso piano 07, sezione 7.2) |

## 10.3 L'architettura proposta

```
Analista ──doppio clic──> NFR.cmd ──> procedura.py (menu, stato, flussi)
                                        │  appunti.py: ascolto degli appunti, estrazione JSON,
                                        │              riconoscimento dell'agente dagli schemi, nome file
                                        │  apre link dell'agente, cartella "Da allegare", Excel
                                        ▼
                         esegui_ciclo_locale.py (motore, invariato nei controlli; in sottoprocesso come la demo)
                                        ▼
                         Registro Excel (copia di lavoro locale -> sostituzione verificata), Archivio, PDF
```

Tutte le risposte degli agenti passano da un solo ingresso,
`Archivio_Cicli\In_arrivo\`: gli appunti, un file trascinato e, in futuro, un
file scritto dall'agente stesso. Il gate resta identico, quindi l'architettura
e' gia' pronta per il giorno in cui gli agenti potranno scrivere da soli
(direzione futura dell'utente, D-10).

## 10.4 Fasi di lavoro

### F1 — Automatismi nel motore (poche righe, basso rischio)

- `_scrivi_baseline` copia anche `Baseline_corrente.txt` nella cartella
  `kernel` configurata: sparisce il passo 3 del trimestre. **Trappola**: non
  farlo quando `kernel` e' la cartella `01_Kernel` del pacchetto (collaudo e
  demo).
- `comando_trimestrale` archivia i prompt generati (`02_Agenti/*.md`) in
  `Cicli/<ciclo>/Prompt_in_uso/`: sparisce il passo 10.
- (Realizzato il 30/09 sera come comando `report`, D-62, con il PDF in
  `Cicli/<ciclo>/Report_comitato_<ciclo>.pdf` e la demo che lo usa; restano
  l'avvio da `valida` e il PDF delle schede.) Comando nuovo `report [--ciclo]`: esporta in PDF i fogli da Quadro a
  Metodologia dell'Excel validato, in
  `Cicli/<ciclo>/Comitato/Report_comitato_<ciclo>.pdf`. Riusa `report_pdf()`
  di `Demo_W1_W2/esegui_demo.py`, che da quel momento chiamera' il motore.
  - `valida` lo lancia da solo alla fine, per i cicli trimestrali.
  - `schede` esporta anche `Schede_<ciclo>.pdf` (se mancano, impostazioni di
    stampa nel file delle schede, in `schede.scrivi_file_schede`).
  - Un errore nel PDF e' solo un avviso: i dati sono gia' salvati.

### F2 — `07_Senza_Studio/appunti.py`: niente piu' Blocco note

- **Lettura degli appunti** con `win32clipboard` (pywin32, gia' installato).
  `GetClipboardSequenceNumber` riconosce una copia nuova e ignora quelle fatte
  dalla procedura stessa.
- **`estrai_json(testo)`**:
  - toglie BOM e recinti ```json;
  - prova `json.JSONDecoder().raw_decode` da ogni `{` e tiene l'oggetto piu'
    grande che rispetta uno schema noto;
  - se le graffe non si chiudono, dice "risposta troncata" e unisce le parti
    successive ("chiedi ad A1: continua").
- **`riconosci_agente(payload)`**: usa i campi `required` di
  `01_Kernel/schema_output_A1/A3/A5/A6.json`, senza regole ricopiate. Un testo
  che non e' JSON e' un parere di A4.
- **`nome_file`**: `A1_<ciclo>.json`, `A5_<ciclo>.json`,
  `A3_<settimana>.json`, `A6_<ciclo>.json`, in UTF-8 dentro `In_arrivo`.
  Conserva anche il testo copiato cosi' com'era, per traccia.
- **Controllo di schema immediato** con `valida_output.valida`: un A1
  malformato si scopre prima di lanciare A5.
- **`messaggio_correzione(motivi, agente)`**: trasforma l'elenco di un FERMATO
  nel testo per l'agente ("correggi solo questi punti, restituisci l'intero
  JSON, nessun testo attorno") e lo mette negli appunti. Nessun carattere in
  piu' nei prompt: A1 e' a 7.966 su 8.000.
  > **Aggiornamento 02/10/2026 (D-69)**: per A1 c'e' gia'.
  > `esegui_ciclo_locale.messaggio_correzione(ciclo, esito)` e' usato dal
  > comando `precontrollo`, che prima di A5 verifica schema, controlli
  > meccanizzati e parti del razionale e scrive
  > `Cicli/<ciclo>/Correzione_A1_<ciclo>.txt` (non ancora negli appunti). Anche
  > il "controllo di schema immediato" del punto sopra, per A1, e' il
  > precontrollo. Qui restano gli altri agenti, i fermi di `trimestrale`,
  > `settimanale` e `schede` e gli appunti. Inoltre A1 riceve i controlli di A5
  > nell'allegato `Input_A1_<ciclo>.txt` e li applica prima di rispondere.

### F3 — `07_Senza_Studio/procedura.py` + `NFR.cmd`: il menu

- **`stato(conf)`**, veloce e senza Excel. Legge:
  - `Baseline_corrente.json` (ultimo ciclo scritto, ciclo da valutare, data di
    riferimento);
  - l'archivio (`Validazione_<c>.json` = validato; `Schede_<c>.xlsx`;
    `Comitato/*.pdf`; `Settimane/<lunedi'>/`);
  - `News_Inbox/<lunedi'>/Raccolta_*.txt`.

  Da questi calcola il **prossimo passo proposto**.
- **Menu**:

  | Voce | Cosa fa |
  |---|---|
  | 1 | Aggiornamento settimanale |
  | 2 | Ciclo trimestrale |
  | 3 | Validazione |
  | 4 | Schede e report al comitato |
  | 5 | Parere su una notizia (A4) |
  | 6 | Incolla una risposta di un agente |
  | 7 | Dismetti un rischio |
  | 8 | Apri registro o archivio |
  | 9 | Verifica del PC |
  | 0 | Esci |

  Invio sceglie il prossimo passo proposto. Esempio di schermata:

  ```
  NFR Horizon Scan — stato al 12/10/2026
   Trimestre 2026Q3: scritto, VALIDATO, schede e report pronti
   Settimana 12/10: raccolta fatta (48 notizie), A3 da fare

   1  Aggiornamento settimanale   <- prossimo passo
   2  Ciclo trimestrale
   ...
  Scelta [1]: _
  ```

- **Ogni passo con un agente**:
  - la procedura prepara `%USERPROFILE%\NFR_Da_allegare\` con i soli file da
    allegare e apre Esplora file li';
  - apre il link dell'agente (da `configurazione.json`) e mette negli appunti il
    testo della richiesta;
  - poi aspetta, controllando insieme gli appunti e il tasto Invio (`msvcrt`).
- **Settimanale**:
  1. raccolta, se non e' gia' fatta questa settimana;
  2. apre `Manuali` ("aggiungi i file, poi Invio");
  3. A3, con allegati raccolta + manuali + baseline `.txt`;
  4. `settimanale`;
  5. apre l'Excel della settimana;
  6. facoltativo: "accetto le notizie? S/N", che lancia `valida` (dal 02/10
     senza opzioni: nella griglia una riga non toccata vale come accettata,
     D-67).
- **Trimestrale**:
  1. si ferma se il ciclo prima non e' validato, e propone la validazione;
  2. `baseline`;
  3. A1;
  4. A5 (allegati A1 + baseline);
  5. `trimestrale`;
  6. se FERMATO: messaggio di correzione negli appunti ("torna nella chat di A1
     e incolla"), poi di nuovo A1 -> A5 obbligatorio -> `trimestrale`.
- **Validazione**:
  1. riepilogo delle righe da decidere;
  2. apre il registro in Excel **visibile**, sulla griglia del foglio
     Validazione (dal 02/10 mostra solo i periodi da validare: niente filtri,
     D-67). Lo script non salva nulla; se l'apertura non riesce, ripiega su
     `os.startfile`;
  3. aspetta che il file sia chiuso (prova di apertura esclusiva);
  4. (tolto il 02/10: una riga non toccata vale gia' come accettata);
  5. `valida`, con il periodo preso dallo stato e il validatore dalla
     configurazione;
  6. poi propone subito le schede.
- **Schede e report**: `schede-input` -> A6 -> `schede` (con il PDF) -> apre
  `Cicli/<ciclo>/Comitato/`.
- **Parere di A4**: archivia il testo in
  `Archivio_Cicli/Pareri/<data>_<titolo>.txt`.
- **Esecuzione del motore**: gira in un sottoprocesso, come fa
  `esegui_demo.py`.
  - L'uscita scorre a video ed e' catturata.
  - Il codice 0/1/2 diventa una fascia OK / FERMATO / ERRORE TECNICO, con
    "cosa fare".
  - Il **log** di ogni esecuzione va in `Archivio_Cicli/Log/`.
- **Collaudo**: gli ingressi (appunti, tastiera, apertura di link e cartelle)
  si possono iniettare, cosi' la procedura si collauda senza una persona.
- **Lanciatori `NFR.cmd` e `NFR_incolla.cmd`**:
  - usano `%~dp0`, `chcp 65001`, `PYTHONIOENCODING=utf-8`;
  - cercano `py -3`, poi `python`;
  - contengono solo testo ASCII.

  `NFR_incolla.cmd` fa la voce 6 da sola: riconosce l'agente e continua il
  flusso giusto.

### F4 — `07_Senza_Studio/installa.cmd` + `installa.py`: setup con un doppio clic, ripetibile

- **Controllo dell'ambiente**:
  - controlla Python e i moduli: `win32com.client`, `pythoncom`, `openpyxl`,
    `pypac`, Excel via COM;
  - lancia `pip install --user` solo per cio' che manca, con un messaggio
    chiaro se il proxy blocca.
- **`configurazione.json`**:
  - cartelle scelte con finestre di dialogo (`tkinter.filedialog`, gia' in
    Python), proposte cercando le library sincronizzate in `%USERPROFILE%`;
  - i cinque link degli agenti ("Copia collegamento" in Agent Builder);
  - il nome del validatore.

  L'analista non apre piu' il JSON in Blocco note.
- **Collegamenti**:
  - sul Desktop, "NFR Horizon Scan" e "NFR Incolla risposta";
  - il secondo con un tasto di scelta rapida facoltativo. **Trappola**: niente
    Ctrl+Alt, che sulla tastiera italiana e' AltGr; il tasto funziona solo per
    collegamenti sul Desktop o nel menu Start.
- **Voce "Invia a -> NFR notizie manuali"**: copia i file selezionati in
  `News_Inbox\<lunedi'>\Manuali\`.
- **Attivita' pianificata della raccolta** con `schtasks /create /xml`
  (lunedi' alle 7, "esegui appena possibile" se il PC era spento): sostituisce
  i passi a mano nell'Utilita' di pianificazione.
- **Cartelle e verifica**:
  - `attrib +P` sulle cartelle sincronizzate (sempre disponibili su questo
    dispositivo);
  - al termine, la **Verifica del PC** (voce 9). Controlla anche
    `wb.AutoSaveOn` e `wb.FullName` del registro, riga per riga in verde o
    rosso, e salva un file da mandare a chi mantiene il pacchetto.

### F5 — Robustezza della scrittura

- In `excel_com.SessioneExcel`, subito dopo l'apertura: `wb.AutoSaveOn = False`
  (in try/except).
- Context manager `registro_in_lavoro(conf)` in `esegui_ciclo_locale.py`, per
  `trimestrale`, `settimanale`, `valida` e `dismetti`. E' lo stesso schema che
  `aggiorna-registro` usa gia' con `os.replace`:
  1. copia il registro in `%LOCALAPPDATA%\NFR\lavoro\` e ne registra
     l'impronta;
  2. scrive e controlla sulla copia locale;
  3. se l'originale non e' cambiato: backup, poi `os.replace`; altrimenti
     FERMATO "registro cambiato nel frattempo".

  `SALVATO` vuol dire "sostituito". Codici e messaggi restano uguali.

### F6 — Agenti: il minimo indispensabile

- `02_Agenti/modelli/A3.md`: una riga, "le notizie possono arrivare anche come
  allegati (raccolta, manuali)". Si smette di dipendere dall'indicizzazione
  della knowledge di SharePoint; il prompt schedulato resta possibile. Poi
  `componi_prompt.py` e il ricaricamento di A3 in Agent Builder.
- A1, A5 e A6 non cambiano: le correzioni passano nel messaggio preparato
  dalla procedura.

### F7 — Documentazione, decisioni, analisi, demo, collaudo

Regola dell'utente: tutto allineato, niente zip.

- **Collaudo**:
  - `99_Collaudo/test_procedura.py` (senza Excel), aggiunto a
    `esegui_collaudo.py`. Copre:
    - estrazione del JSON da testi reali: recinti, testo attorno, BOM, JSON
      troncato e unito in piu' parti;
    - riconoscimento dell'agente e nomi dei file;
    - stato calcolato da archivi finti, prossimo passo, messaggio di
      correzione;
    - flusso completo con appunti e tastiera simulati;
    - controlli sui file `.cmd`.
  - `run_catena.py`:
    - PDF del report e delle schede;
    - copia di lavoro locale, compreso il caso "registro cambiato nel
      frattempo";
    - baseline copiata in `kernel`;
    - prompt archiviati.
  - `verifica_riferimenti.py`: i lanciatori e le voci di menu citati nella
    guida esistono. La guida tiene un'appendice "Comandi diretti", cosi' il
    controllo 8 resta valido.
- **Documenti**:
  - `00_GUIDA_PASSO_PASSO.md` riscritta attorno al menu: sezione 0 =
    `installa.cmd`; sezioni 1-4 con passi "cosa premi, cosa vedi"; tabella
    degli errori aggiornata; appendice dei comandi diretti.
  - `00_LEGGIMI.md`: indice, requisiti, "Dove vive ogni regola"
    (riconoscimento degli agenti = schemi).
  - `07_Senza_Studio/README_variante_locale.md`.
  - `08_Deploy/Piano_deploy.md`: fase 2 = installa, fase 5 = schtasks, fase 6 =
    link degli agenti in configurazione.
  - `06_Governance/controlli_e_model_risk.md`: rischi di Salvataggio
    automatico, copia di lavoro e appunti; il gate non cambia.
  - `02_Agenti/COMMENTATI/*` (la riga di A3), `99_Collaudo/LEGGIMI_collaudo.md`.
- **Decisioni**:
  - `08_Deploy/DECISIONI.md`: **D-43**. Python resta il motore; strato di
    automazione; piano 07 in riserva; chiude AR1. *Fatto il 28/09*: D-43
    registrata; A-05 chiusa da D-44; la scelta della strada e' A-15.
  - `TODO_possibili_sviluppi.md`: AR1 chiusa (riserva). Le voci P e Q si fanno
    sull'architettura Python, dopo questo intervento; P3 aggiunge la sua voce
    al menu. *Fatto il 28/09*: il TODO contiene le voci AU1-AU6 e l'ordine
    unico di lavoro.
- **Fuori dal pacchetto**:
  - `HANDOFF_stato_e_prossimi_passi.md`: sezione 2-decies.
  - `PROMPT_MASTER_rigenerazione.md`: SCELTE, VINCOLI (link, appunti,
    Salvataggio automatico, execution policy), PROMPT (A3), SCRIPT DI CAMPO,
    DOCUMENTAZIONE, COLLAUDO, **TRAPPOLE** nuove numerate, STRUTTURA DEI FILE.
  - Questa cartella: nota in testa a `07` ("in riserva, D-43") e a `04`; in
    questo documento, l'esito della realizzazione.
  - `Demo_W1_W2/esegui_demo.py`: passa dalla procedura con appunti simulati (A1
    copiato con i recinti, un A1 troncato in due parti, correzione dopo un
    FERMATO), poi viene rilanciata. Aggiornare anche `REPORT_demo.md`.

## 10.5 Da verificare sul PC e nel tenant della Banca

La Verifica del PC (voce 9) ne copre una parte.

| # | Cosa verificare | Se non va |
|---|---|---|
| V-A | Il link "Copia collegamento" di un agente di Agent Builder apre la chat dell'agente | aprire l'agente a mano |
| V-B | Il pulsante Copia porta negli appunti il JSON intero, anche per un A1 da 40 KB | selezionare il testo e copiarlo con Ctrl+C |
| V-C | La risposta lunga di A1 (12-15 rischi) arriva intera | unione in piu' parti, gia' prevista |
| V-D | A3 legge per intero gli allegati `.txt` | tenere la knowledge `News_Inbox` come oggi |
| V-E | Tasto di scelta rapida, "Invia a" e `schtasks` sono permessi all'utente | menu e Utilita' di pianificazione a mano |
| V-F | `AutoSaveOn` e `FullName` del registro aperto via COM | se il registro e' aperto come documento cloud, F5 diventa urgente |
| V-G | `attrib +P` funziona sulle library sincronizzate | "Mantieni sempre su questo dispositivo" a mano |

## 10.6 Come si verifica il risultato

1. Rigenerare e collaudare:
   - `python 02_Agenti/componi_prompt.py`: A3 sotto gli 8.000 caratteri;
   - `python 99_Collaudo/esegui_collaudo.py`: tutto OK, catena con Excel
     compresa, con i nuovi test della procedura, del PDF e della copia di
     lavoro.
2. `python Demo_W1_W2/esegui_demo.py`: due cicli e due settimane attraverso la
   procedura con appunti simulati, compresi un FERMATO con il messaggio di
   correzione e un A1 in due parti. Il `Report_comitato_2026Q4.pdf` e lo
   `Schede_2026Q4.pdf` si controllano a occhio.
3. Prova a mano sul PC:
   - `installa.cmd` su una cartella di prova;
   - doppio clic su "NFR Horizon Scan": stato e prossimo passo corretti;
   - voce 6 con un JSON copiato da un editor (con recinti e testo attorno):
     file nominato e passo avviato;
   - Verifica del PC con tutte le righe verdi.

## 10.7 Impegno indicativo

| Fase | Giorni |
|---|---|
| F1 | 0,5 |
| F2 | 1 |
| F3 | 2-3 |
| F4 | 1-1,5 |
| F5 | 1 |
| F6 | 0,5 |
| F7 | 2 |

Totale circa 8-10 giorni. F1 e F2 danno subito il guadagno maggiore: niente
Blocco note e niente copie a mano.

## 10.8 Fuori da questo piano

- Voci P1-P7, Q1 e G1-G5 del TODO: dopo questo intervento, sulla stessa
  architettura.
- Copilot Studio: opzione separata, nella parte seconda qui sotto (disponibile,
  D-44; uso da decidere, A-15). Le API di Copilot restano fuori.
- Il pacchetto sotto git.
- Lo zip, solo su richiesta.

---
---

# Parte seconda — Opzione separata: Copilot Studio (28/09/2026)

Richiesta dell'utente (28/09): valutare, come opzione separata, se Copilot
Studio permette di automatizzare di piu'; se a quel punto si puo' eliminare
Python, o ridurlo al minimo; quali passi si possono fare subito perche' comuni
alle due strade.

Stato: **proposta, non approvata**. Copilot Studio e' disponibile nel tenant
(D-44, 28/09; prima era la decisione aperta A-05). Se usarlo non e' deciso: e'
la decisione aperta **A-15**. Le scelte del 27/09 restano valide, e la
variante descritta qui (CS-1) le rispetta: Python resta il motore.

Nomi usati in questa parte:
- **strada A**: la procedura guidata delle sezioni 10.1-10.8 (Agent Builder,
  menu, appunti);
- **strada B**: Copilot Studio, nelle varianti CS-1, CS-2 e CS-3 (10.11).

## 10.9 Le risposte in breve

1. **Si automatizza di piu'? Si', molto.** In Copilot Studio un agente puo'
   chiamare dei flussi. A1 e A5 si concatenano da soli e le risposte arrivano
   in un file senza passare dagli appunti. Spariscono:
   - i tre gesti per agente della strada A;
   - la raccolta notizie sul PC, con proxy, `pypac` e attivita' pianificata;
   - il bisogno di stare al PC con il menu.

   Il trimestre diventa un messaggio in Teams, due o tre pulsanti e la
   validazione.
2. **Si elimina Python? Dal PC dell'analista si', del tutto no.** Copilot
   Studio non esegue il nostro codice Python: il suo code interpreter scrive
   codice nuovo a ogni richiesta, quindi non puo' fare da gate. Per togliere
   Python dall'esercizio bisogna **riscrivere il motore** in Office Scripts o
   in Power Query (varianti CS-2 e CS-3). Costa circa 4 settimane in piu' e fa
   perdere la regola D-02: stesso codice in collaudo e in esercizio. Python
   resta comunque al manutentore, per prompt, template e collaudo.
3. **Ridurlo al minimo senza riscrivere si puo': variante CS-1 (ibrida).** Il
   motore Python resta com'e'. Gira da solo, in background, su **un solo PC**
   (l'esecutore), quando arriva una richiesta. L'analista lavora in Teams e non
   vede mai Python. Dal PC spariscono raccolta, appunti, menu, `pypac` e
   attivita' pianificata.
4. **I passi comuni sono circa due terzi del piano 10** (10.14, 6-7 giorni).
   Si fanno subito; la strada si sceglie alla fine, con la decisione A-15.
   I passi della sola strada A (3-4 giorni) si rimandano fino ad allora.

## 10.10 Cosa porta Copilot Studio (verificato su Microsoft Learn il 28/09/2026)

| Fatto | Conseguenza |
|---|---|
| Un agente puo' chiamare **agent flow** con i connettori standard (SharePoint, Teams). Per un utente con licenza Microsoft 365 Copilot, azioni dell'agente, strumenti AI e azioni degli agent flow sono **"No charge"**. Per gli agent flow vale solo con il trigger "When an agent calls the flow" (Billing rates, agg. 14/09/2026) | Tutto cio' che l'analista avvia in chat non consuma crediti: trimestrale, settimanale e validazione si avviano in chat |
| Gli agent flow con **altri trigger** (pianificati, a evento) consumano Copilot Credits. Senza crediti, i nuovi run sono bloccati, non fatturati. I **cloud flow di Power Automate** usano invece la licenza di Power Automate | La raccolta del lunedi' si fa con un cloud flow di Power Automate: RSS e SharePoint sono connettori Standard. A3 pianificato consumerebbe crediti, quindi lo avvia l'analista |
| **Orchestratore con sotto-agenti, argomenti guidati (topic) e Adaptive Card**. Nei flussi ci sono azioni "human in the loop": richiesta di informazioni e approvazioni | A1 -> A5 in sequenza senza una persona in mezzo. Le conferme ("scrivo?", "accetti il resto?") diventano pulsanti in Teams. La correzione dopo un FERMATO passa da agente ad agente |
| **Code interpreter** di Copilot Studio: il codice lo scrive il modello a ogni richiesta; e' spento di default nell'ambiente; non si carica codice proprio (pagine del code interpreter, agg. 17/09/2026 e 04/02/2026) | Non e' un posto per il motore dei controlli. E' la stessa conclusione del 7.1 per Agent Builder. **Superata in parte il 05/10/2026** (10.20): nella nuova esperienza una skill esegue un nostro script sempre uguale |
| **Office Scripts** lanciati da un flusso: 120 secondi per chiamata, 1.600 chiamate al giorno per utente, 5 MB verso il workbook, nessuna chiamata esterna; l'amministratore puo' spegnerli (Office Scripts, platform limits) | E' l'unico motore deterministico tutto nel cloud (CS-2), ma va scritto in TypeScript |
| Un flusso chiamato dall'agente risponde entro il limite delle operazioni sincrone di Power Automate, **120 secondi**. Payload dei connettori: 5 MB. Istruzioni di un agente per Microsoft 365 Copilot: 8.000 caratteri (Quotas and limits, agg. 04/08/2026) | Il motore si chiama in modo **asincrono**: l'agente consegna, il risultato arriva dopo. Un A1 da 45 KB ci sta. Con i sotto-agenti A1 si puo' dividere senza passi in piu'. Il limite per sotto-agenti e prompt e' da verificare (V-K) |
| **Modelli**: in Copilot Studio i modelli Anthropic sono fuori dall'EU Data Boundary e **spenti di default nella UE** | Si useranno i modelli disponibili nel tenant. Cambiare piattaforma puo' cambiare il modello: la qualita' di A1 va **rimisurata** con il doppio run e `confronta.py`, come per il primo ciclo |
| Knowledge: fino a 500 fonti. Con alcune modalita' i file con etichetta di riservatezza *Confidential* o *Highly confidential* non vengono indicizzati | Controllare le etichette di `Kernel` e `Analisi_Interne` (V-O) |
| Lanciare da un cloud flow un desktop flow sul PC (Power Automate Desktop) richiede la licenza **Power Automate Premium** | Non si usa per avviare il motore: basta un programma in ascolto su una cartella sincronizzata (10.12) |

## 10.11 Tre modi di usare Copilot Studio: conta dove gira il motore

Copilot Studio risolve l'orchestrazione, non il gate. Le varianti si
distinguono per dove girano i controlli e la scrittura.

| | **CS-1 Ibrida** (consigliata) | CS-2 Tutto nel cloud | CS-3 Power Query |
|---|---|---|---|
| Da dove viene | questo documento | R2 del documento 06 | piano 07 piu' i flussi |
| Chi orchestra | Operatore NFR in Teams con gli agent flow | uguale | uguale |
| Motore dei controlli | `esegui_ciclo_locale.py` **invariato**, sul PC esecutore | Office Scripts (TypeScript) | query M nel report |
| Dove sta lo stato | il registro Excel di oggi | Liste SharePoint e report con Power Query | file in `Validati` e report |
| Gate | identico a oggi: prima della scrittura | prima della scrittura, se si scrive solo con lo strumento "controlla e scrivi" | in parte dopo: un flusso non aggiorna le query, legge il Gate salvato nel file |
| Python in esercizio | solo sul PC esecutore, in background | no | no |
| Riscrittura | nessuna | tutto il motore, con collaudo differenziale | tutto il motore, in M |
| Collaudo automatico (oltre 414 verifiche) | intatto | resta per i contratti; il resto si prova nell'ambiente di test | come CS-2 |
| Impegno | parte comune piu' 13-15 giorni | 6-7 settimane, circa 4 in piu' partendo da CS-1 | 5-7 settimane |

Opzioni scartate:

| Opzione | Perche' no |
|---|---|
| Code interpreter con il nostro codice incollato nelle istruzioni ("esegui esattamente questo") | il codice lo riscrive comunque il modello; quello eseguito si legge solo dall'API di Dataverse; non e' ripetibile per costruzione |
| Power Automate Desktop per lanciare il motore dal cloud | licenza Premium per utente, e un altro strumento da governare per fare cio' che fa un programma in ascolto |
| Computer use: l'agente usa Excel al posto della persona | escluso dalla licenza Microsoft 365 Copilot (Billing rates, nota 4); fragile come l'automazione del browser |
| Scrittura diretta nel registro con il connettore Excel Online | file bloccato dopo l'uso, niente scritture concorrenti, nessun controllo prima (documento 03) |

## 10.12 La variante CS-1 nel dettaglio

### Come funziona

```
Analista / validatore in Teams ──> Operatore NFR (Copilot Studio)
   argomenti guidati: Prepara il ciclo, Analizza la settimana, Applica la validazione,
                      Schede e report, Stato, Valuta una notizia
      ├─> A1, A3, A4: sotto-agenti con knowledge (ricerca file, D-09)
      ├─> A5, A6: strumenti "prompt" con uscita JSON (senza ricerca, come oggi)
      └─> agent flow: Deposita_Risposta, Scrivi_Richiesta, Leggi_Stato, Leggi_File,
                      Salva_Allegato, Archivia_Parere
                         │
                         ▼
        SharePoint  Archivio_Cicli\In_arrivo\  (risposte degli agenti + Richiesta_<id>.json)
                         │  sincronizzazione OneDrive
                         ▼
PC esecutore ── motore_in_ascolto.py ──> esegui_ciclo_locale.py (invariato)
                         │                   └─> Registro, Archivio, baseline in Kernel, PDF
                         └─> Archivio_Cicli\Esiti\  (Esito_<id>.json, Stato_processo.json,
                                                     motore_attivo.json)

Cloud flow del lunedi' (Power Automate) ──> News_Inbox\<lunedi'>\Raccolta_<data>.txt
```

Il punto di giunzione e' `In_arrivo`, gia' previsto in 10.3 come ingresso
unico, "in futuro anche per un file scritto dall'agente stesso". La CS-1 e'
quel futuro. A5 e A6 sono strumenti "prompt" perche' non cercano nella
knowledge (D-09 per A5; A6 usa solo l'input preparato dal motore): la loro
uscita JSON passa al flusso senza che l'orchestratore la ricopi.

### Come lo vive l'analista

| Processo | Strada A (10.2) | CS-1 |
|---|---|---|
| Trimestre | Invio nel menu; i tre gesti per A1, A5 e A6; validazione in Excel | "Prepara il ciclo 2026Q4" in Teams. L'Operatore legge stato e baseline, lancia A1 e poi A5, mostra il riepilogo; pulsante **Scrivi**; consegna al motore; l'esito arriva da solo |
| Correzione dopo un FERMATO | incollare il messaggio preparato nella chat di A1 | pulsante **Correggi**: l'Operatore passa i motivi ad A1, rilancia A5 e riconsegna |
| Settimana | Invio; file in `Manuali`; i tre gesti per A3; S/N | la raccolta l'ha gia' fatta il flusso del lunedi'; i file manuali si trascinano nella chat; "Analizza la settimana"; pulsante **Accetto le notizie** |
| Validazione | Excel aperto dalla procedura; S/N; `valida` | Excel dal link dell'Operatore; "Applica la validazione"; pulsante "accetti le righe lasciate vuote?" |
| Schede e report | procedura: `schede-input` -> A6 -> `schede` | dopo la validazione l'Operatore propone le schede: prende l'input di A6 preparato dal motore, lancia A6, consegna; i PDF finiscono in `Comitato` |
| Parere su una notizia | voce 5 del menu, A4 in chat | "Valuta questa notizia", con testo o link; un pulsante per archiviare il parere |
| Dove si lavora | al PC, con il menu | in Teams, da qualunque posto; il PC esecutore deve essere acceso |

### Il PC esecutore e `motore_in_ascolto.py`

- Un solo PC con Python ed Excel: nel pilota quello dell'utente (D-13), poi
  quello del manutentore. **Gli altri analisti non hanno bisogno di Python.**
- Il programma parte all'accesso a Windows, da un collegamento nella cartella
  Esecuzione automatica creato da `installa.cmd`: niente `schtasks`.
- Ogni 15-30 secondi guarda `In_arrivo`:
  - prende una richiesta solo quando il file e' completo (JSON leggibile,
    dimensione stabile);
  - una richiesta alla volta, in ordine di arrivo;
  - la controlla con `01_Kernel/schema_richiesta.json` e con le regole qui
    sotto.
- Lancia il motore con l'esecutore della parte comune (C5): sottoprocesso,
  codici 0/1/2, log.
- Alla fine:
  - scrive `Esiti/Esito_<id>.json`: fascia OK / FERMATO / ERRORE TECNICO,
    motivi, messaggio di correzione, file prodotti;
  - aggiorna `Stato_processo.json`;
  - sposta la richiesta in `Richieste_evase`;
  - mostra un avviso sul PC. Facoltativo: un messaggio in Teams, con un cloud
    flow sulla cartella `Esiti` (V-M).
- Ogni minuto aggiorna `motore_attivo.json` con l'ora e il nome del PC. Cosi'
  l'Operatore puo' dire "il motore non e' attivo da 40 minuti: accendi il PC
  esecutore". Il programma non parte se un altro PC ha aggiornato lo stesso
  file da poco.

### Le regole di governo

1. **Agenti e flussi non scrivono mai nel registro.** Scrivono solo in
   `In_arrivo`, che e' una cartella di consegna. Nel registro scrive solo il
   motore, dopo i controlli: la garanzia di D-10 non cambia. E' anche la
   risposta alla direzione futura dell'utente (agenti che scrivono), senza
   aggirare il gate.
2. **Richieste in lista bianca.** Il motore accetta solo `baseline`,
   `trimestrale`, `settimanale`, `valida`, `schede-input`, `schede` e `report`,
   con i parametri controllati dallo schema. `inizializza`, `dismetti` e
   `aggiorna-registro` si lanciano solo dal PC. Nessuna riga di comando viene
   mai composta con il testo di una richiesta.
3. **Chi valida lo dice Teams, non il testo.** La richiesta `valida` porta
   l'identita' dell'utente, presa dal flusso. Il motore la accetta solo se e'
   fra i validatori di `configurazione.json` (oggi una persona, D-13).
4. **Consegna integra.** Il flusso scrive nella richiesta:
   - la lunghezza del testo consegnato: una risposta troncata si ferma prima
     ancora dello schema;
   - la data di modifica del registro letta in SharePoint: il motore aspetta
     che la copia sincronizzata sia almeno di quella data. Evita di applicare
     una validazione salvata sul web ma non ancora arrivata al PC.
5. **Conferma non e' validazione.** Il pulsante Scrivi autorizza la scrittura
   "da validare". La validazione resta sul foglio Validazione (dal 02/10 la
   griglia, una riga per oggetto, D-67), con le regole di oggi (documento 06,
   regola 5).
6. **Traccia.** Ogni richiesta ha un identificativo, che si ritrova nella
   risposta archiviata, nell'esito e nel log. Il testo originale di ogni agente
   si conserva come oggi.

### Rischi e contromisure

| Rischio | Contromisura |
|---|---|
| PC esecutore spento o senza Excel: niente esecuzioni | le richieste restano in coda e non si perdono; l'Operatore segnala il motore non attivo; la riga di comando resta come riserva |
| Ritardi o conflitti della sincronizzazione OneDrive | richieste con nome unico; il motore aspetta il registro aggiornato (regola 4); dopo la scrittura controlla che non siano nate copie in conflitto; misura in V-P |
| Registro aperto sul web dal validatore mentre il motore scrive | copia di lavoro locale con sostituzione verificata (C3); l'Operatore chiede di chiudere il registro prima di "Applica la validazione" |
| `In_arrivo` diventa una porta d'ingresso | permessi della cartella (analisti e identita' dei flussi); lista bianca; schema; validatori in configurazione |
| Modello diverso da quello di oggi | doppio run e validazione del primo ciclo sulla nuova piattaforma, con i criteri di D-21 |
| Due piattaforme da mantenere (Copilot Studio e Python) | istruzioni sempre generate da `componi_prompt.py`; soluzione esportata e conservata in `09_Copilot_Studio/`; schede di costruzione scritte da Claude Code |
| Trascrizioni delle conversazioni conservate da Copilot Studio | parere DPO che estende D-24 (V-N) |

## 10.13 Si puo' eliminare Python? Pezzo per pezzo

| Pezzo in Python oggi | Strada A | CS-1 | CS-2 / CS-3 |
|---|---|---|---|
| `raccogli_notizie.py`, `pypac`, attivita' pianificata | PC dell'analista | **tolti**: cloud flow del lunedi' | tolti |
| ascolto degli appunti (`appunti.py`) | PC | **non serve**; l'estrazione del JSON resta nel motore (C4) | non serve |
| menu (`procedura.py`, `NFR.cmd`) | PC | **sostituito da Teams**; restano `motore_in_ascolto.py` e la riga di comando di riserva | non serve |
| motore: `esegui_ciclo_locale.py`, `excel_com.py`, `valida_output.py`, `controlli_a5.py`, `schede.py` | PC | PC esecutore, **invariato** | riscritto in TypeScript o M; il Python diventa l'oracolo del collaudo |
| PDF del report e delle schede (via COM) | PC | PC esecutore | da rifare, con la conversione in PDF di un flusso (da provare con le aree di stampa) |
| `componi_prompt.py`, `genera_dashboard.py`, collaudo | manutentore | manutentore | manutentore |

In sintesi:
- **CS-1** porta Python da "ogni analista, con comandi e menu" a "un PC, in
  background, invisibile". E' la riduzione massima **senza riscrivere nulla** e
  senza toccare il collaudo.
- **CS-2 e CS-3** lo tolgono dall'esercizio, ma bisogna riscrivere il motore e
  tenere due copie delle regole durante la migrazione. Conviene solo se la
  Banca vuole togliere del tutto il PC dall'esercizio.
- **Eliminarlo del tutto** vorrebbe dire rinunciare al collaudo automatico e
  alla composizione dei prompt dal kernel: non e' consigliato in nessuna strada.

## 10.14 I passi comuni alle due strade (da fare subito)

Il principio che li rende comuni: **separare chi chiede da chi esegue**. Nella
strada A il menu scrive una richiesta e l'esecutore la esegue. Nella CS-1 la
stessa richiesta la scrive un flusso. Tutto cio' che sta dietro la richiesta e'
identico.

| # | Passo | Da dove viene | Perche' serve anche con Copilot Studio | Giorni |
|---|---|---|---|---|
| C1 | Domande di dettaglio all'IT e alla compliance (testo qui sotto). Dal 28/09 la domanda 1 ha risposta (D-44); le altre servono solo se si considera la CS-1, e non bloccano C2-C9 | documento 06, fase R0 | servono a decidere A-15 | 0,5 + attesa |
| C2 | Automatismi del motore: baseline `.txt` in `Kernel`, prompt archiviati, comando `report` con PDF, PDF delle schede | F1 | nella CS-1 l'Operatore legge la baseline da `Kernel`, e i PDF li fa comunque il motore | 0,5 |
| C3 | Robustezza della scrittura: `AutoSaveOn` spento, copia di lavoro locale, sostituzione verificata | F5 | nella CS-1 il registro puo' essere aperto sul web mentre il motore scrive: serve ancora di piu' | 1 |
| C4 | Ingresso unico `In_arrivo` (`ingresso.py`): `estrai_json`, `riconosci_agente` dagli schemi, nomi dei file, controllo di schema immediato, `messaggio_correzione`, testo originale conservato | F2, senza l'ascolto degli appunti | i file del flusso si puliscono, si riconoscono e si nominano allo stesso modo; il messaggio di correzione lo usa l'Operatore | 0,75 |
| C5 | Stato e prossimo passo (`stato(conf)`), anche in JSON; esecutore del motore in sottoprocesso, con le fasce OK / FERMATO / ERRORE TECNICO; esito in `Esiti/`, log in `Archivio_Cicli/Log` | F3, la parte senza interfaccia | e' cio' che l'Operatore legge per "Stato" e per rispondere | 1 |
| C6 | Coda delle richieste: `01_Kernel/schema_richiesta.json`, lista bianca, validatori in configurazione | nuovo | nella strada A il menu diventa un produttore di richieste; nella CS-1 lo diventa il flusso | 0,5 |
| C7 | La riga di A3: notizie anche in allegato o nel testo della richiesta | F6 | nella CS-1 il flusso passa la raccolta ad A3 come ingresso | 0,25 |
| C8 | Installazione di base: controllo di Python e dei moduli, `configurazione.json` con finestre di dialogo, `attrib +P`, Verifica del PC (`AutoSaveOn`, `FullName`) | F4, la parte comune | il PC esecutore si installa allo stesso modo | 0,75 |
| C9 | Collaudo e documentazione della parte comune: test di ingresso, stato, coda, PDF, copia di lavoro; DECISIONI, guida, PROMPT_MASTER | F7, la parte comune | e' la base di entrambe | 1,5 |
| | **Totale** | | | **circa 6-7** |

**Testo per C1.** Completa la domanda del documento 03 (3.0):
1. Possiamo avere un ambiente Power Platform con il ruolo di autore di Copilot
   Studio per 1-2 persone, e pubblicare un agente in Teams per un gruppo di
   sicurezza? *Risposta del 28/09: Copilot Studio e' disponibile (D-44); la
   pubblicazione in Teams per un gruppo resta da provare in K0.*
2. I criteri DLP mettono SharePoint, Teams e RSS nello stesso gruppo?
   (Approvals e' facoltativo.)
3. Un cloud flow pianificato con connettori standard e' coperto dalle nostre
   licenze? Finora Power Automate era escluso (D-01).
4. Quali modelli di linguaggio sono attivi per gli agenti? Si puo' fissarne
   uno?
5. Dove e per quanto si conservano le trascrizioni delle conversazioni? Per la
   compliance: estensione del parere D-24.
6. Il code interpreter e' spento a livello di ambiente? Deve restarlo (D-11).
7. Solo per la variante CS-2: gli Office Scripts sono attivi e si possono
   lanciare da un flusso?

**Da non anticipare** (solo strada A, 3-4 giorni):
- l'ascolto degli appunti;
- il menu testuale, con l'apertura dei link degli agenti e la cartella "Da
  allegare";
- i link degli agenti in `configurazione.json`;
- `NFR_incolla.cmd` e il tasto di scelta rapida;
- "Invia a -> NFR notizie manuali";
- l'attivita' pianificata della raccolta;
- guida e demo costruite attorno al menu.

Se la strada B parte, non servono. Se non parte, si fanno subito dopo la parte
comune.

## 10.15 Fasi della variante CS-1 (dopo la parte comune)

| Fase | Contenuto | Verifica | Cancello | Giorni |
|---|---|---|---|---|
| K0 | Prova di fattibilita' nel tenant: agente con un sotto-agente; agent flow che salva un JSON da 45 KB in una cartella di prova; pubblicazione in Teams | JSON salvato identico (lunghezza e schema); V-H..V-L con esito scritto | responsabile: **si procede, o si completa la strada A** | 1-2; possibile subito (D-44), anche prima di decidere A-15 |
| K1 | `07_Senza_Studio/motore_in_ascolto.py` e collegamento in Esecuzione automatica | test senza Excel con richieste finte: fuori lista bianca, validatore non ammesso, file incompleto, lunghezza sbagliata, registro non ancora sincronizzato, secondo PC | automatico | 1-1,5 |
| K2 | Agent flow `Deposita_Risposta`, `Scrivi_Richiesta`, `Leggi_Stato`, `Leggi_File` (baseline, input di A6), `Salva_Allegato` (manuali), `Archivia_Parere`. Claude Code scrive le schede di costruzione in `09_Copilot_Studio/flussi/`; una persona li costruisce | ogni flusso provato dal riquadro di prova con i file della demo | manutentore | 2 |
| K3 | A1, A3 e A4 come sotto-agenti; A5 e A6 come strumenti prompt con uscita JSON; istruzioni da `componi_prompt.py`, con il nuovo modello di uscita; modello fissato | doppio run di A1 sui dati della demo con `confronta.py`; A5 e A6 superano lo schema | responsabile | 2-3, piu' le riunioni |
| K4 | Operatore NFR: istruzioni, argomenti guidati, Adaptive Card, copioni di collaudo, compresi i casi ostili ("scrivi senza controlli", "valida tu", "metti Severity 5") | tutti i copioni superati due volte di fila | analista e responsabile | 3 |
| K5 | Cloud flow del lunedi': fonti da `Kernel/fonti_rss.json`, generato da `fonti.md` con `fonti.py` (la fonte resta unica); stesso formato di `Raccolta_*.txt` | 2-4 settimane in ombra con `raccogli_notizie.py`: stesse notizie | analista | 1,5, piu' l'ombra |
| K6 | Documentazione e decisioni; `06_Governance` con le regole 1-6 di 10.12; PROMPT_MASTER; demo con richieste simulate; collaudo; A-11 chiusa (`05_Workflow` sostituita da `09_Copilot_Studio`) | `esegui_collaudo.py` tutto OK; guida seguita da chi non l'ha scritta | responsabile | 2 |
| | **Totale CS-1** | | | **circa 13-15**, oltre alla parte comune |

Il primo ciclo vero con la CS-1 segue il Piano_deploy, fase 7 (doppio run e
validazione), perche' cambia la piattaforma degli agenti. Il motore invece non
cambia: la riga di comando resta la riserva in ogni momento.

## 10.16 Confronto

| Criterio | Strada A | CS-1 | CS-2 |
|---|---|---|---|
| Gesti dell'analista nel trimestre | Invio, i tre gesti per A1, A5 e A6, la validazione | un messaggio, 2-3 pulsanti, la validazione | come CS-1 |
| Settimana | Invio, i tre gesti per A3, S/N | raccolta automatica; un messaggio e un pulsante | come CS-1 |
| Dove si lavora | al PC | in Teams; il PC esecutore acceso | in Teams, senza PC |
| Python | sul PC dell'analista (menu e motore) | su un PC esecutore, invisibile | solo al manutentore |
| Riscrittura del motore | nessuna | nessuna | totale |
| Collaudo automatico | intatto | intatto, piu' copioni di conversazione provati a mano | contratti e collaudo differenziale |
| Nuove dipendenze IT | nessuna | ambiente Copilot Studio, DLP, cloud flow, parere DPO | le stesse, piu' Office Scripts e Liste |
| Costi | nessuno | nessuno per l'uso in chat; crediti solo se si pianifica un agente | come CS-1 |
| Tempo | 8-10 giorni | 6-7 comuni, piu' 13-15 | circa 4 settimane piu' di CS-1 |
| Rischi nuovi | pulsante Copia e appunti (V-B) | PC esecutore, sincronizzazione, modello diverso, due piattaforme | divergenza del porting, nessuna transazione sulle Liste |
| Tornare indietro | — | facile: motore e riga di comando restano; si completano i passi della strada A | difficile |

## 10.17 Raccomandazione

*Riscritta il 28/09 dopo D-44: Copilot Studio e' disponibile, quindi la
strada non dipende piu' dall'IT ma dalla scelta dell'utente (A-15).*

1. **Subito**: la parte comune (10.14, circa 6-7 giorni; TODO AU1-AU3).
   Qualunque strada si scelga, nessun lavoro va perso.
2. **Facoltativo, in parallelo**: la prova K0 (1-2 giorni). Mostra quanto e'
   complesso davvero Copilot Studio nel tenant, prima di impegnarsi.
3. **Alla fine della parte comune, decisione A-15** (criteri nel TODO, AU4):
   - **CS-1** se il sistema servira' a piu' analisti, se si vuole lavorare da
     Teams senza stare al PC, o se i tre gesti per agente e la raccolta sul
     PC si rivelano un peso. In piu' devono riuscire K0 e il parere sulle
     trascrizioni. Da' la massima automazione con Python ridotto al solo
     motore in background, senza riscrivere nulla, con gate e collaudo
     identici;
   - **strada A** se il pilota resta a una persona al proprio PC (D-13) e si
     vuole la minima complessita' prima del primo ciclo vero. E' la
     **proposta** se la decisione non c'e': 3-4 giorni, nessuna dipendenza
     nuova. La CS-1 resta aggiungibile dopo, perche' cambia solo chi scrive le
     richieste.
4. **Togliere Python anche dal PC esecutore** (CS-2) e' una decisione a parte,
   da prendere dopo, e solo se la Banca vuole un esercizio senza PC. Riusa
   Operatore, sotto-agenti e flussi della CS-1; costa il porting del motore.

Registrate il 28/09 in `DECISIONI.md`: D-43 (Python resta il motore, piano 07
in riserva), D-44 (Copilot Studio e Power Query disponibili, chiude A-05),
A-15 aperta (scelta della strada).

## 10.18 Da verificare nel tenant (oltre a V-A..V-G)

| # | Cosa verificare | Se non va |
|---|---|---|
| V-H | Copilot Studio abilitato: ambiente e ruolo di autore (**superata il 28/09**, D-44); pubblicazione in Teams per un gruppo, da provare in K0 | strada A |
| V-I | DLP: SharePoint, Teams e RSS nello stesso gruppo | raccolta sul PC come oggi; il resto della CS-1 regge |
| V-J | Un sotto-agente chiama un proprio strumento, e un JSON da 45 KB arriva intero in SharePoint | la risposta la consegna l'Operatore; la lunghezza la controlla comunque il motore |
| V-K | A1 riceve per intero la baseline (circa 40 KB) e risponde con 12-15 rischi senza troncare; A6 riceve il suo input (circa 70 KB); limite di caratteri delle istruzioni di sotto-agenti e prompt | A1 diviso in due sotto-agenti (Evidenze, Punteggi); baseline ridotta |
| V-L | Modello degli agenti: quale e' attivo e se si puo' fissare; qualita' al doppio run | criteri di D-21 soddisfatti prima di andare avanti |
| V-M | Cloud flow pianificato con connettori standard coperto dalle licenze | raccolta sul PC come oggi; solo l'avviso locale |
| V-N | Trascrizioni: dove e per quanto; parere DPO | strada A |
| V-O | Etichette di riservatezza su `Kernel` e `Analisi_Interne` | i file come allegati invece che come knowledge |
| V-P | Latenza della sincronizzazione di `In_arrivo` ed `Esiti` fra SharePoint e PC esecutore (obiettivo: sotto i 2 minuti) | "Mantieni sempre su questo dispositivo" (V-G); se resta lenta, l'Operatore dichiara attese piu' lunghe |
| V-Q | Solo CS-2: Office Scripts attivi e lanciabili da un flusso | la CS-2 non si fa |

## 10.19 Fonti (consultate il 28/09/2026)

- Microsoft Learn, [Billing rates and management — Copilot Studio](https://learn.microsoft.com/en-us/microsoft-copilot-studio/requirements-messages-management), agg. 14/09/2026: "No charge" per gli utenti Microsoft 365 Copilot; agent flow gratuiti solo con il trigger "When an agent calls the flow"; run bloccati quando i crediti finiscono; computer use escluso.
- Microsoft Learn, [Use code interpreter in a prompt](https://learn.microsoft.com/en-us/microsoft-copilot-studio/code-interpreter-for-prompts), agg. 17/09/2026, e [FAQ for code interpreter](https://learn.microsoft.com/en-us/microsoft-copilot-studio/faq-code-interpreter), agg. 04/02/2026: codice generato dal modello, spento di default nell'ambiente.
- Microsoft Learn, [Code interpreter for developers](https://learn.microsoft.com/en-us/power-apps/developer/data-platform/code-interpreter), agg. 23/09/2025: il codice eseguito si legge nella risposta dell'API Predict di Dataverse.
- Microsoft Learn, [Quotas and limits — Copilot Studio](https://learn.microsoft.com/en-us/microsoft-copilot-studio/requirements-quotas), agg. 04/08/2026: 500 fonti di knowledge, 8.000 caratteri, payload dei connettori 5 MB, etichette di riservatezza.
- Microsoft Learn, [Office Scripts: platform limits](https://learn.microsoft.com/en-us/office/dev/scripts/testing/platform-limits), agg. 29/10/2025: 120 secondi per le operazioni sincrone, 1.600 chiamate al giorno, 5 MB, niente chiamate esterne.
- Microsoft Learn, [Request information from human review in agent flows](https://learn.microsoft.com/en-us/microsoft-copilot-studio/flows-request-for-information) e [Agent flows overview](https://learn.microsoft.com/en-us/microsoft-copilot-studio/flows-overview).
- Microsoft Learn, [Anthropic models in Microsoft Online Services](https://learn.microsoft.com/en-us/microsoft-365/copilot/connect-to-ai-subprocessor): esclusi dall'EU Data Boundary, spenti di default nella UE.
- Microsoft Learn, [RSS connector](https://learn.microsoft.com/en-us/connectors/rss/): connettore Standard.
- Microsoft Learn, [Trigger desktop flows from cloud flows](https://learn.microsoft.com/en-us/power-automate/desktop-flows/trigger-desktop-flows) e [Types of Power Automate licenses](https://learn.microsoft.com/en-us/power-platform/admin/power-automate-licensing/types): Power Automate Premium per i desktop flow avviati dal cloud.
- Documenti 03, 06 e 07 di questa cartella.

## 10.20 Aggiornamento del 05/10/2026: due motori in Copilot Studio, skill, prova K0 estesa (D-70)

Richiesta dell'utente (05/10): provare la versione senza Copilot Studio e attivare quella con Copilot
Studio, per vedere se funziona e con quali limiti; gli e' stato consigliato di attivare l'opzione del
codice. Poi: "fai le 2 opzioni con le skill.md e vediamo".

**Cosa e' cambiato su Microsoft Learn dal 28/09** (pagine consultate il 05/10):

| Fatto | Conseguenza |
|---|---|
| Copilot Studio ha due motori ("harness"): l'**esperienza standard** (agenti classici) e la **nuova esperienza** (GitHub Copilot harness, interruttore New experience). Un agente nasce in una delle due e non si sposta | la CS-1 si puo' costruire su entrambe; va scelto il motore |
| Nella nuova esperienza c'e' un **sandbox** (Python 3.12, circa 99 librerie, niente rete, niente pacchetti da installare) e le **skill**: SKILL.md con script e file, caricate come .zip. Gli script delle skill sono "pre-written": girano sempre uguali | **cade in parte la conclusione di 10.10**: un nostro script puo' girare dentro l'agente. Il precontrollo (D-69) puo' stare dentro A1 |
| La nuova esperienza consuma **Copilot Credits dal primo minuto** (costruzione, prove nel riquadro, uso); serve capacita' assegnata all'ambiente | costo nuovo, assente nella strada A e nell'esperienza standard |
| Esperienza standard: per gli utenti con licenza Microsoft 365 Copilot, uso interno autenticato, **"No charge"** anche per gli strumenti premium (code interpreter, modelli di ragionamento) | l'opzione 1 non costa |
| Il **code interpreter** dell'esperienza standard va abilitato dall'amministratore (spento di default) e poi acceso sull'agente (Settings -> Generative AI -> File processing capabilities). Il codice lo scrive il modello | il nostro script gira solo se allegato e se il modello lo esegue cosi' com'e': va misurato (ripetibilita', impronta) |
| File creati dall'agente fino a 10 MB, allegati fino a 16 MiB, conservati 28 giorni; allegati .txt, .md, .csv, non .json ne' .py | lo script si allega come `.txt`; l'output di A1 (40-60 KB) ci sta |
| I modelli di ragionamento sono soprattutto nella nuova esperienza | per A1 (oggi "Think deeper" in Agent Builder) la qualita' va rimisurata su entrambe |

**Cosa si e' fatto** (D-70):
- le regole del precontrollo in un modulo senza Excel, `07_Senza_Studio/precontrollo.py`, con
  l'**impronta** dell'output;
- `09_Copilot_Studio/prepara_kit.py` compone dai moduli del pacchetto uno **script unico**: lo stesso
  file e' nella skill `precontrollo-nfr` (opzione 2) ed e' l'allegato `.txt` dell'opzione 1. Il
  collaudo verifica che sia identico al pacchetto e che dia lo stesso esito, la stessa impronta e lo
  stesso messaggio del comando;
- protocollo della prova K0 estesa, `09_Copilot_Studio/Prova_con_Copilot_Studio.md`:
  - A1 senza codice, cioe' quanto regge la risposta (V-K);
  - A1 con il precontrollo nelle due opzioni;
  - ripetibilita' e una richiesta da rifiutare;
  - crediti;
  - facoltativi, Teams (V-H) e un agent flow che salva il JSON in SharePoint (V-J).

  Usa lo stesso input della prova della versione senza Copilot Studio
  (`08_Deploy/Prova_senza_Copilot_Studio.md`, registro di prova 2026Q4).

**Cosa cambia nella decisione A-15.** Se l'opzione 2 funziona, il precontrollo dentro A1 riduce il
giro A1 -> PC in qualunque strada. La variante CS-1 diventa piu' interessante, perche' anche la
correzione dopo un fermo resterebbe dentro l'agente. Il costo pero' passa a consumo. Se funziona solo
l'opzione 1, il vantaggio c'e' senza costi, a patto che il modello esegua il file cosi' com'e'. In
tutti i casi il gate resta in `trimestrale` sul PC (D-10), e D-11 resta in vigore per gli agenti in
esercizio finche' non si decide.

Fonti aggiunte: Harnesses in Copilot Studio e Compare Copilot Studio agent harnesses (30/09/2026);
Skills overview e Add an existing skill; Files the agent creates; Attach files to a conversation;
Overview of usage-based billing (10/09/2026); Billing rates and management; Use code interpreter to
analyze structured data (04/08/2026); Code interpreter in a prompt (30/09/2026); FAQ for code
interpreter; blog del CAT Microsoft "Copilot Studio agent sandbox" (20/07/2026). Link nel protocollo
della prova.
