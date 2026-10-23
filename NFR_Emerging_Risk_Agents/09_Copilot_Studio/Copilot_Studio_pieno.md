# Copilot Studio pieno: progetto, costruzione e prove (D-82)

Versione del processo tutta nel tenant: nessun Python sul PC. Gli analisti danno comandi a un agente, l'agente fa
lavorare gli agenti di valutazione, un flusso registra. Questo documento vale per il ramo `copilot-studio-pieno`.
Contiene il progetto (sezioni 1-6), la sequenza di creazione con le prove (7), le strade alternative (8) e la
tabella dei risultati (9).

Le prove fatte finora (K0, K6, K6-bis, K6-ter: 09-22/10/2026) sono in `Prova_K6_Operatore.md` e
`Prova_con_Copilot_Studio.md`. Qui si riprendono solo le conclusioni.

| Funziona | Non funziona |
|---|---|
| Argomento con trigger "A message is received" e una condizione sul testo | L'input passato al sotto-agente nel nodo (K6.1: arriva vuoto) |
| Agent flow che legge un file da SharePoint e uno che salva il JSON (40-60 KB, impronta identica, B3) | La correzione incollata nella chat di A1 (K6ter.3) |
| Sotto-agente A1 che legge l'allegato da una variabile globale e restituisce il JSON in un'altra (K6ter.1) | Le variabili globali dopo una conversazione nuova o un Save: si azzerano |
| Prompt con tre ingressi di testo; l'uscita e' un record con il testo nel campo `text` | Teams con messaggi oltre circa 100 KB |

Le etichette dell'interfaccia sono quelle di Microsoft Learn in inglese, come negli altri protocolli. Se una voce
non c'e' o si chiama diversamente, va annotata: e' un risultato della prova.

## 1. Il disegno in breve

```text
 Analista (riquadro Test, poi Teams)
   |  "Esegui_ciclo 2027Q1"
   v
 Agente NFR Operatore ---- argomento del comando (trigger fisso sul testo, YAML)
   |   1. Leggi_File: Input_A1 da SharePoint  -> Global.ingresso
   |   2. sotto-agente A1 (o A8, A3) con la knowledge -> Global.uscita
   |   3. Salva_JSON: A1_<periodo>.json in Archivio_Cicli/In_arrivo
   |   4. NFR_Motore("registra_ciclo"): risponde subito "avviato"
   v
 Flusso NFR_Motore (continua da solo)
   [A5 se chiesto] -> controlli del motore -> giro di correzione automatico (al massimo 2)
   -> scrittura del registro -> Esiti/Ultimo_esito.txt -> avviso in Teams
```

Componenti:

| Componente | Che cos'e' | Dove si costruisce |
|---|---|---|
| NFR Operatore | agente con i comandi: uno per argomento, nessuna decisione del modello | Copilot Studio, esperienza standard |
| A1, A8, A3 | sotto-agenti: valutano e devono leggere la knowledge | Agents -> New child agent |
| A5, A6, Correggi | prompt: ingresso e uscita fissi, niente knowledge | Tools -> Prompt (o AI Hub), chiamati dal flusso |
| Motore | prompt con code interpreter che esegue il codice del pacchetto contenuto in una busta Excel (prova K9) | Tools -> Prompt, Settings -> Enable code interpreter |
| Leggi_File, Salva_JSON | agent flow: leggono e scrivono file in cartelle fisse | Tools -> New agent flow |
| NFR_Motore | agent flow: esegue i comandi del registro, li orchestra e li verifica | Tools -> New agent flow |
| Raccolta_notizie | flusso cloud pianificato: i feed nel News_Inbox, al posto di `raccogli_notizie.py` | Power Automate |
| A4, A7 | restano in Agent Builder: non scrivono nulla, leggono solo la knowledge | invariati |

Principi:
1. **Ogni comando e' un argomento con un trigger deterministico**: `A message is received` con la condizione
   `StartsWith(System.Activity.Text, "<comando>")`. L'orchestrazione generativa non sceglie mai uno strumento o un
   sotto-agente: i flussi hanno "Allow agent to decide dynamically" spento, i sotto-agenti sono "It's redirected to".
2. **Ogni argomento e' autosufficiente.** All'inizio rilegge da SharePoint i file che gli servono, quindi funziona in
   qualunque conversazione, anche dopo un Save o il giorno dopo. Non si dipende piu' dalla conversazione del lancio.
3. **I file in SharePoint sono la fonte di verita'; le variabili globali solo il mezzo di trasporto** verso e dai
   sotto-agenti, durante l'esecuzione di un argomento (sezione 2).
4. **Il lavoro deterministico lo fa il flusso, non l'argomento.** L'argomento fa solo cio' che richiede l'agente:
   chiamare un sotto-agente con la knowledge. Il resto (A5, controlli, correzioni, registro) e' nel flusso
   `NFR_Motore`, che non ha limiti di tempo dopo aver risposto.
5. **Un'interfaccia unica del motore**: `NFR_Motore(comando, periodo, parametri, utente)`. Come e' fatto dentro (V2,
   F2, sezione 6) non cambia gli argomenti.
6. **Niente passi inutili**:
   - il precontrollo non e' un passo separato: gli stessi controlli girano nel motore prima di scrivere, e un
     Bloccante fa partire da solo il giro di correzione;
   - A5 si chiede solo quando serve (`Esegui_ciclo 2027Q1 A5`);
   - A4 e A7 non si spostano;
   - nessun file si copia a mano: `Baseline_corrente.txt` in Kernel e la knowledge di A7 le scrive il motore.
7. **Chi valida e decide e' l'utente collegato** (`System.User.DisplayName` e `PrincipalName`), non un nome scritto a
   mano.

A9 Contraddittore (A-17, aperta) non e' costruito. Se verra' deciso, sara' un prompt in piu', chiamato dal flusso
come A5.

## 2. Comunicazione: file in SharePoint e variabili globali

**Cartelle.** Durante le prove la radice e' `Archivio_Cicli/Prova_K0`, in esercizio `Archivio_Cicli`. Ogni flusso
la tiene in una sola azione **Compose** `radice`: si cambia li'.

| Codice area | Cartella | Chi scrive | Chi legge |
|---|---|---|---|
| `BASE` | `<radice>` | il motore: `Input_A1_<periodo>.txt`, `Baseline_corrente.json` | Esegui_ciclo, Esegui_settimana |
| `LAVORO` | `<radice>/In_arrivo` | Salva_JSON e il motore: output degli agenti, correzioni | il motore |
| `ESITI` | `<radice>/Esiti` | il motore: `Ultimo_esito.txt`, un JSON per esecuzione, le buste | Stato |
| (motore) | `<radice>/Cicli`, `Settimane`, `Dismissioni`, `Backup` | il motore, come oggi lo script | A7, chi consulta l'archivio |

Il motore legge il proprio codice da `Kernel/Motore` (durante le prove da `<radice>/Motore`): busta vuota e impronta
attesa. La libreria Kernel e' in sola lettura per tutti tranne il manutentore.

**File di lavoro** (in `In_arrivo`, nomi fissi composti dall'argomento o dal flusso, mai dal modello):

| File | Scritto da | Contenuto |
|---|---|---|
| `A1_<periodo>.json` | Esegui_ciclo (A1 o A8), poi il giro di correzione | output della valutazione; per uno straordinario lo scrive A8, con lo stesso nome con cui lo archivia lo script |
| `A1_<periodo>_giro_<n>.json` | NFR_Motore | la versione prima di ogni correzione, per il confronto |
| `Correzione_A1_<periodo>.txt` | NFR_Motore | i punti trovati dai controlli, nel testo di oggi (`messaggio_correzione`) |
| `A5_<periodo>.json` | NFR_Motore, se chiesto | rilievi di A5 |
| `A3_<lunedi'>.json` | Esegui_settimana | notizie della settimana |
| `A6_<ciclo>.json` | NFR_Motore | testi delle schede |

**Variabili globali.** Sono tre e vengono azzerate all'inizio di ogni argomento che le usa:

| Variabile | Contenuto | Letta da |
|---|---|---|
| `Global.periodo` | il ciclo (`2027Q1`, `2027Q1-S1`) o il lunedi' (`2026-10-19`) del comando | A3 (settimana), argomenti |
| `Global.ingresso` | il testo dato al sotto-agente: `Input_A1_<periodo>.txt`, o `Baseline_corrente.json` per A3 | A1, A8, A3, citata nelle istruzioni |
| `Global.uscita` | la risposta del sotto-agente (output di Completamento) | l'argomento, che la passa a Salva_JSON |

Perche' cosi':
- l'input del nodo sotto-agente non arriva (K6.1), le variabili globali si' (K6ter.1);
- le globali pero' si perdono con la conversazione, quindi non possono essere la memoria del processo: lo sono i file;
- ogni passaggio lascia un file con un nome fisso, che si apre e si confronta.

**Pulizia del JSON.** `Salva_JSON` salva solo il testo dalla prima `{` all'ultima `}`. I link alle fonti che Copilot
Studio aggiunge in fondo alla risposta (K6-ter) spariscono in modo deterministico, senza dipendere dalla descrizione
dell'output. I segni di citazione dentro i testi (`[1]`) non si tolgono: li segnalano i controlli.

## 3. Gli agenti

| Agente | Forma | Istruzioni (da `Da_caricare/`) | Ingresso | Uscita | Knowledge |
|---|---|---|---|---|---|
| NFR Operatore | agente | testo in T1.1 | i comandi | messaggi brevi, mai JSON | nessuna |
| A1 Horizon Scanner | sotto-agente | `agenti/A1_CS.md` (7.931 caratteri) | `{Global.ingresso}` = Input_A1 | `{Global.uscita}` = JSON | Analisi_Interne, Analisi_Esterne, News_Inbox, i 4 siti |
| A8 Evento critico | sotto-agente | `agenti/A8_CS.md` (7.846) | `{Global.ingresso}` = Input_A1 dello straordinario; documenti dell'evento in `Analisi_Esterne/Eventi/<periodo>` | `{Global.uscita}` | come A1 |
| A3 Interim Update | sotto-agente | `agenti/A3_CS.md` (7.597) | `{Global.ingresso}` = Baseline_corrente.json; `{Global.periodo}` = lunedi' | `{Global.uscita}` | Analisi_Interne, Analisi_Esterne, News_Inbox, i 4 siti |
| A5 Challenger | prompt | `prompt/A5.txt` | `json_a1`, `baseline` | JSON (record, campo `text`) | nessuna (D-09) |
| A6 Schede | prompt | `prompt/A6.txt` | `schede_input` | JSON | nessuna |
| Correggi | prompt | `prompt/Correggi.txt` | `correzione`, `json_a1`, `allegato` | JSON corretto | nessuna |
| Motore | prompt con code interpreter | `prompt/Motore.txt` | `comando` (testo), `busta` (file) | una riga JSON | nessuna |
| A4, A7 | Agent Builder, invariati | `02_Agenti/` | come oggi | come oggi | come oggi; i file li aggiorna il motore |

Le istruzioni dei sotto-agenti e i testi dei prompt li genera `genera_CS.py` dagli A*.md attuali. Le differenze sono
solo le frasi di ingresso e uscita, piu' qualche accorciamento per stare sotto gli 8.000 caratteri; scale, regole e
schemi restano identici.
- Nei sotto-agenti, i segnaposto `{Global.ingresso}`, `{Global.uscita}`, `{Global.periodo}` si cancellano e si
  reinseriscono con `/` -> **Variable**: il testo scritto a mano non diventa una variabile.
- Nei prompt, ogni `[nome]` dell'ultima riga si sostituisce con un ingresso creato con **Add content** -> **Text**
  (per `busta`: **Image or document**) con lo stesso nome.

Il modello e' lo stesso per tutti: il piu' capace disponibile, GPT-5 reasoning nelle prove del 22/10, da annotare.
A1 in particolare: "piu' ricerche per rischio" e "rianalizza tutto" restano come nella prova K6-ter.

**Completamento dei sotto-agenti** (A1, A8, A3): un output `output`, tipo testo, con la descrizione:

`Il JSON prodotto dall'agente, identico carattere per carattere, dalla prima { all'ultima }. Escludi tutto cio' che sta fuori: link e citazioni delle fonti, note, testo aggiunto in fondo alla chat.`

## 4. I flussi

### 4.1 Leggi_File (nuovo, sostituisce Leggi_Input)

1. **Tools** -> **Add a tool** -> **New agent flow**. Trigger **When an agent calls the flow** con due ingressi di
   testo, in quest'ordine: `area`, `nome`. I nomi interni sono `text` e `text_1`: gli argomenti li usano cosi'.
2. **Compose** `radice`: `/Archivio_Cicli/Prova_K0` (in esercizio `/Archivio_Cicli`).
3. **Initialize variable** `cartella`, tipo String, vuota.
4. **Condition**, nell'editor delle espressioni (fx):
   `or(contains(triggerBody()?['text_1'], '/'), contains(triggerBody()?['text_1'], '\'), contains(triggerBody()?['text_1'], '..'))`.
   Ramo vero: **Respond to the agent** con `testo` vuoto, `caratteri` 0, `esito` = `nome non ammesso`.
5. **Switch** su `area`:
   - `BASE` -> **Set variable** `cartella` = pillola `radice`;
   - `LAVORO` -> pillola `radice` + testo `/In_arrivo`;
   - `ESITI` -> pillola `radice` + testo `/Esiti`;
   - **Default** -> **Respond to the agent** con `esito` = `area non ammessa`.
6. SharePoint **Get file content using path**: sito NFR. File Path = pillola `cartella`, testo `/`, pillola `nome`.
   Pillole dal contenuto dinamico, mai `concat(...)` scritto nel campo (K6: viene preso alla lettera).
7. **Respond to the agent**:
   - testo `testo` = il contenuto del file. Se arriva in base64 (comincia con `{"$content-type"`), usare
     `base64ToString(body('Get_file_content_using_path')?['$content'])`, con il nome dell'azione come appare nel
     flusso. Controllare le lettere accentate;
   - numero `caratteri` = `length(...)` dello stesso valore;
   - testo `esito` = `ok`.
8. Una seconda **Respond to the agent** in parallelo al punto 7, con **Configure run after** -> **has failed** su
   Get file content: `testo` vuoto, `caratteri` 0, `esito` = `non trovato`.
9. **Save**, **Publish**. Nell'agente: **Tools**, aggiungere `Leggi_File`; in **Additional details** togliere
   "Allow agent to decide dynamically when to use this tool".

### 4.2 Salva_JSON (quello delle prove, modificato)

Stessi ingressi di oggi, `nome_file` (`text`) e `contenuto` (`text_1`): gli ID delle prove restano validi.
1. **Compose** `radice`, come in 4.1; Folder Path = pillola `radice` + testo `/In_arrivo`.
2. **Compose** `pulito`, nell'editor delle espressioni:
   `if(and(endsWith(triggerBody()?['text'], '.json'), greater(indexOf(triggerBody()?['text_1'], '{'), -1)), substring(triggerBody()?['text_1'], indexOf(triggerBody()?['text_1'], '{'), add(sub(lastIndexOf(triggerBody()?['text_1'], '}'), indexOf(triggerBody()?['text_1'], '{')), 1)), triggerBody()?['text_1'])`
3. SharePoint **Get file metadata using path** sullo stesso percorso, poi una **Condition** con **Configure run
   after** -> "is successful" e "has failed":
   - il file esiste -> **Update file** (File Identifier = l'Id del metadata) con contenuto `pulito`;
   - non esiste -> **Create file** con nome e contenuto `pulito`.

   La versione precedente resta nella cronologia delle versioni della libreria. Cosi' non si dipende da cosa fa
   Create file su un file che esiste gia' (mai verificato).
4. **Respond to the agent**: `esito` = `salvato`, `caratteri` = `length(outputs('pulito'))`.

### 4.3 NFR_Motore

Ingressi di testo, in quest'ordine: `comando` (`text`), `periodo` (`text_1`), `parametri` (`text_2`), `utente`
(`text_3`). Uscite: `esito`, `messaggio`.

`parametri` sono righe `chiave=valore`: per esempio `rischio=NFR-07` e `motivazione=...`, oppure `rischi=NFR-01,NFR-07`
e `motivo=...`, oppure `A5`. `utente` e' "Nome Cognome <email>".

**Forma provvisoria** (T1.4), finche' il motore non c'e':
- solo **Respond to the agent**: `esito` = `non attivo`, `messaggio` =
  `concat('Motore non ancora attivo (', triggerBody()?['text'], ' ', triggerBody()?['text_1'], '): i file sono in Archivio_Cicli/In_arrivo.')`;
- gli argomenti funzionano gia' cosi' e non cambiano quando arriva il motore.

**Forma completa.** Uno **Switch** su `comando`; ogni ramo comincia con **Respond to the agent** (`esito` = `avviato`,
`messaggio` = "... avviato: ti scrivo in Teams alla fine, intanto puoi usare Stato") e poi continua senza il limite
dei 100 secondi.

| Comando | Cosa fa il flusso dopo la risposta |
|---|---|
| `registra_ciclo` | [se `A5`: prompt A5 su A1 e Baseline -> `A5_<p>.json`] -> **giro**: controlli del motore; se ci sono Bloccanti e giro < 2: prompt Correggi -> nuova `A1_<p>.json` -> di nuovo i controlli -> scrittura del registro (`trimestrale`) -> archivio, baseline, Input_A1 successivo, knowledge di A7 |
| `correggi_ciclo` | un giro di Correggi dai file `Correzione_A1_<p>.txt`, `A1_<p>.json`, `Input_A1_<p>.txt`, poi come `registra_ciclo` senza A5 |
| `settimanale` | motore `settimanale` su `A3_<lunedi'>.json` |
| `valida` | motore `valida` (griglia -> registro); per un ciclo anche baseline, Input_A1, knowledge di A7, `Kernel/Baseline_corrente.txt` per A4 |
| `riapri`, `dismetti`, `straordinario` | motore con i `parametri`; `straordinario` restituisce il periodo `AAAAQn-Sk` e scrive il suo Input_A1 |
| `schede` | motore `schede-input` -> prompt A6 -> motore `schede` -> `Schede_<c>.xlsx` |
| `report`, `diagnosi` | motore; PDF o testo in `Cicli/<c>/` |

Alla fine di ogni ramo:
- **Esiti/Ultimo_esito.txt**: una riga con data e ora, comando, periodo, utente, esito e messaggio;
- un JSON per esecuzione in `Esiti/`;
- in Teams, **Post message in a chat or channel** (Flow bot, chat con l'utente) con la stessa riga.

Due esecuzioni insieme non devono scrivere il registro:
- **Settings** del trigger -> **Concurrency control** -> 1;
- se non c'e' per questo trigger, un file `Esiti/In_corso.txt`: se esiste, il ramo risponde "in uso da ... dalle
  ..." e si ferma.

**Il motore dentro il flusso** (V2, sezione 6):
1. Copia della busta vuota da `Kernel/Motore` (in prova `<radice>/Motore`) in
   `Esiti/Busta_<comando>_<periodo>_<ora>.xlsx`.
2. Ingressi nella tabella `tblIngresso`, con l'azione Excel Online (Business) **Add a row into a table**: Nome, Parte,
   Testo. Un testo lungo va a blocchi di 30.000 caratteri, con un **Do until** su
   `substring(testo, mul(variables('parte'), 30000), min(30000, sub(length(testo), mul(variables('parte'), 30000))))`.
3. **Run a prompt** `Motore`: `comando`, e `busta` = il contenuto della copia (**Get file content**).
4. **Parse JSON** dell'uscita. Fermarsi se:
   - `impronta_codice` o `impronta_busta` diversa da `Kernel/Motore/Impronta.txt`: "motore non verificato";
   - c'e' il campo `errore`.

   Nel primo caso si archiviano il codice e il log del prompt.
5. Esito: `codice_uscita` 1 -> `Correzione_A1_<p>.txt` = `correzione` e nuovo giro; 0 -> si prosegue.

Con V2 il motore restituisce anche le operazioni sul registro, che applica l'Office Script "applica" (sezione 6).

### 4.4 Raccolta_notizie (flusso cloud pianificato)

1. Power Automate -> **Create** -> **Scheduled cloud flow**: ogni lunedi' alle 7:00, fuso di Roma.
2. **Compose** `fonti`: incollare il contenuto di `Da_caricare/flussi/Fonti_rss.json`, cioe' i feed approvati di
   `fonti.md`, generati.
3. **Compose** `lunedi`:
   `formatDateTime(addDays(utcNow(), sub(1, if(equals(dayOfWeek(utcNow()), 0), 7, dayOfWeek(utcNow())))), 'yyyy-MM-dd')`.
4. **Initialize variable** `testo` con le righe di testa del file di oggi:
   - `RACCOLTA NOTIZIE — settimana del <lunedi>`;
   - la finestra;
   - "Ogni notizia porta il codice della fonte: usalo come codice_fonte".
5. **Apply to each** su `fonti`:
   - **RSS** -> **List all RSS feed items**, Feed URL = `item()?['indirizzo']`, Since = `addDays(utcNow(), -7)`;
   - poi **Append to string variable**: `== <codice> <nome> ==` e, per ogni voce,
     `- [<codice>] <data> | <titolo>`, il link e l'estratto (al massimo `max_voci` voci).
   - Su un feed in errore (**Configure run after** -> has failed) la riga va sotto "FONTI NON RAGGIUNGIBILI".
6. SharePoint **Create file** in `News_Inbox/<lunedi>/`, nome `Raccolta_<oggi>.txt`; la cartella `Manuali` la creano
   gli analisti.

Differenze dallo script:
- niente `_visti.json`: un doppione fra due raccolte lo riconosce A3, che unisce gli articoli sullo stesso fatto;
- le parole `escludi` delle fonti non si applicano. Se servono: **Filter array** sul titolo.

## 5. I comandi (argomenti YAML)

Un file per comando in `Da_caricare/argomenti/`. Tutti hanno il trigger `OnActivity` (`A message is received`) con
la condizione sul testo, e finiscono con **End all topics**.

| Comando | File | Che cosa fa |
|---|---|---|
| `Esegui_ciclo 2027Q1` (`2027Q1-S1` per A8; ` A5` in fondo per il Challenger) | `Esegui_ciclo.yaml` | Leggi_File Input_A1 -> A1 o A8 -> controllo che il JSON ci sia -> Salva_JSON -> NFR_Motore `registra_ciclo` |
| `Correggi_ciclo 2027Q1` | `Correggi_ciclo.yaml` | NFR_Motore `correggi_ciclo` |
| `Esegui_settimana 2026-10-19` | `Esegui_settimana.yaml` | Leggi_File Baseline -> A3 -> Salva_JSON -> NFR_Motore `settimanale` |
| `Valida 2027Q1` (o un lunedi') | `Valida.yaml` | conferma -> NFR_Motore `valida` |
| `Riapri [NFR-03 NFR-07]` | `Riapri.yaml` | conferma -> NFR_Motore `riapri` |
| `Dismetti NFR-07` | `Dismetti.yaml` | motivazione (almeno 10 caratteri) -> conferma -> NFR_Motore `dismetti` |
| `Straordinario [NFR-01 NFR-07]` | `Straordinario.yaml` | motivo (almeno 20) -> conferma -> NFR_Motore `straordinario` |
| `Schede 2027Q1` | `Schede.yaml` | NFR_Motore `schede` |
| `Report 2027Q1 [completo]` | `Report.yaml` | NFR_Motore `report` |
| `Diagnosi 2027Q1` | `Diagnosi.yaml` | NFR_Motore `diagnosi` |
| `Stato` | `Stato.yaml` | Leggi_File `Esiti/Ultimo_esito.txt` |
| `Aiuto` | `Aiuto.yaml` | elenco dei comandi |

**Come si incolla un argomento:**
1. Aprire il file `.yaml` con Blocco note.
2. Con **Modifica** -> **Sostituisci** (Ctrl+H) sostituire ogni segnaposto `<<...>>` con il valore scritto in
   `ID_tenant.txt` ("Sostituisci tutto").
3. In Copilot Studio: **Topics** -> **Add a topic** -> **From blank**, nome = il nome del file. Menu **...** in alto a
   destra -> **Open code editor**. Ctrl+A, incollare tutto il file, **Save**.
4. Se l'editor segnala un errore: copiare il messaggio e la riga e mandarli a Claude, senza correggere a mano.

Il nodo del sotto-agente (`kind: BeginDialog`, riga `dialog:`) e' la sola forma non ancora vista nel tenant: la
conferma T2.3. Le altre (flusso, condizioni, variabili) sono quelle del YAML dell'argomento Correzione A1 del 23/10;
il trigger e le domande seguono i modelli YAML di Microsoft (fonti in fondo).

## 6. Il motore: V2, e se Office Scripts non c'e'

Il motore e' il codice Python del pacchetto (controlli, radar, validatore, schede: libreria standard, l'87% del codice
di oggi, analisi 15). Va eseguito senza il PC. Le strade:

**V2, scelta per questo ramo: "Python decide, Excel esegue" (analisi 15).**
1. L'Office Script generico **prepara** scrive nel foglio nascosto `_Scambio` del registro i dati che servono,
   ricalcolati.
2. Il prompt **Motore** (code interpreter) riceve la busta, esegue il codice e restituisce l'esito e la lista delle
   operazioni.
3. Il flusso confronta l'impronta del codice con quella attesa.
4. L'Office Script **applica** esegue le operazioni solo sulle tabelle e sui nomi ammessi, ricalcola, cerca errori di
   formula e confronta i valori di controllo con quelli attesi dal Python. Se qualcosa non torna, il flusso rimette
   la copia di backup.

Il registro resta quello di oggi, con grafici e formattazione. Serve rivedere D-02 ("niente Office Scripts").

**F2, se Office Scripts non c'e' (T0.1 negativo).** Senza Office Scripts nessuno puo' scrivere dentro il registro con i
grafici: il Python del code interpreter scrive con openpyxl, che i grafici esistenti li perde. Quindi si separano i
dati dalla presentazione:
- `NFR_Dati.xlsx` contiene le tabelle di oggi, la griglia di validazione e il foglio nascosto `_Motore` con il
  codice. Nessun grafico.
- Il prompt Motore lo riceve come unico file in ingresso e restituisce il nuovo `NFR_Dati.xlsx` come unico file in
  uscita (il limite di Learn: un file in, un file out). Il flusso fa la copia di backup, verifica l'impronta e salva.
- Gli ingressi (JSON degli agenti) entrano nella tabella `tblIngresso` con il connettore standard Excel Online, come
  in 4.3. Nessun Office Script.
- La presentazione (Quadro, radar, classifica, grafici) diventa `NFR_Registro.xlsx`, che legge `NFR_Dati.xlsx` con
  **Power Query** (abilitato in Banca dal 25/09). Si aggiorna con "Aggiorna tutto"; oppure il report HTML della
  proposta A-16.
- Il validatore lavora nella griglia di `NFR_Dati.xlsx`, come oggi nel registro.

Costo: si cambia il modo in cui si legge il registro (un passo di aggiornamento) e si riscrive la scrittura del
motore per openpyxl (al posto di COM).

**F1, terza scelta, solo connettore Excel Online.**
- Le operazioni del Python si applicano riga per riga con **Add a row into a table** e **Update a row**.
- Le celle con nome di Parametri diventano una tabella `tblCiclo` e la griglia diventa una tabella.
- E' lento (una chiamata per riga, limite di 1.600 al giorno, blocco del file fino a 6 minuti, righe doppie sui
  tentativi ripetuti): si usa solo se F2 non va.

**Se K9 fallisce** (il code interpreter non esegue fedelmente il nostro codice, o non e' ripetibile):
- con Office Scripts: V1, le regole riscritte in TypeScript (8-11 settimane, analisi 15);
- senza: non c'e' modo di eseguire il motore nel tenant. Restano un esecutore PC (CS-1b, contro la direzione data)
  oppure la strada A (A-15).

Il documento lo dice qui perche' la decisione si prende sui fatti di T0, T4 e T5, prima di scrivere il codice.

| T0.1 Office Scripts | T4 K9 | Strada |
|---|---|---|
| si' | riesce | **V2** |
| no | riesce | **F2** |
| si' | fallisce | V1 |
| no | fallisce | versione piena non fattibile: A-15 |

## 7. Sequenza di creazione e prove

Ogni passo dice cosa fare, cosa deve succedere e cosa annotare nella tabella della sezione 9. Se fallisce, la
riserva e' nella sezione 8. Si lavora con la radice `Archivio_Cicli/Prova_K0`, mai sul registro vero.

### T0. Prerequisiti (15 minuti, niente da costruire)

- **T0.1 Office Scripts.** Aprire un qualunque file Excel di SharePoint in Excel per il web: c'e' la scheda
  **Automatizza** (Automate)?
  - Si' -> V2 possibile.
  - No -> domanda all'IT: interfaccia di amministrazione di Microsoft 365 -> Impostazioni -> Impostazioni
    dell'organizzazione -> Office Scripts. Se resta no, F2.
- **T0.2 Code interpreter nei prompt.** Nell'agente di prova: **Tools** -> **Add a tool** -> **Prompt** -> menu
  **...** -> **Settings**. Annotare se **Enable code interpreter** c'e' e si attiva. Chiudere senza salvare.
- **T0.3 Domande all'IT** (insieme a D1):
  - i prompt eseguiti dentro un agent flow (**Run a prompt**) e il code interpreter ("text and generative AI tools
    (premium)") hanno costo per chi ha Microsoft 365 Copilot?
  - i connettori Microsoft Teams, RSS ed Excel Online (Business) sono ammessi dalla data policy nei flussi?
- **T0.4 Cartelle e file di prova** in `Archivio_Cicli/Prova_K0`:
  - creare `Esiti` e `Motore`;
  - in `In_arrivo` ci sono gia' `A1_2027Q1.json` e la correzione del 22/10 (`Correzione_A1_2027Q1.txt`, dal PC);
  - nella radice: `Input_A1_2027Q1.txt` (c'e'), `Baseline_corrente.json` dal PC, `Input_A1_2026Q4-S1.txt` dalla
    demo (`Demo_W1_W2/1_Input_agenti`);
  - in `Motore`: `K9_Busta_vuota.xlsx` e un file `Impronta.txt` con la sola impronta di `K9_atteso.txt`;
  - in `Analisi_Esterne` una cartella `Eventi`.

### T1. Fondamenta: agente, variabili, flussi

- **T1.1 Agente.** Home di Copilot Studio, New experience spenta -> **Create** -> **New agent** -> **Configure**.
  - Name: `NFR Operatore`;
  - Description: `Comandi del processo NFR: lancia gli agenti di valutazione e il motore del registro.`;
  - Instructions:

    `Sei l'Operatore NFR. Esegui solo cio' che dicono gli argomenti. Non valutare rischi, non scrivere JSON, non chiamare strumenti o agenti di tua iniziativa. Se l'utente chiede altro, rispondi che i comandi disponibili si vedono scrivendo Aiuto.`

  Poi:
  - **Settings** -> **Generative AI**: orchestrazione generativa; il modello piu' capace (annotarlo); **Use general
    knowledge** e **Web search** spenti; **Save**;
  - **Settings** -> **Security** -> **Authentication**: "Authenticate with Microsoft".
- **T1.2 Variabili globali.** **Topics** -> **Add a topic** -> **From blank**, nome `Variabili NFR`. Tre nodi **Set a
  variable value** -> **Create a new variable**, rinominate `periodo`, `ingresso`, `uscita`, valore vuoto. Per
  ciascuna: clic sulla variabile -> **Variable properties** -> **Usage**: **Global (any topic can access)**. **Save**.
  - Controllo: in un altro argomento, inserendo una variabile con `/`, compaiono `Global.periodo`,
    `Global.ingresso` e `Global.uscita`.
  - L'argomento `Variabili NFR` resta, senza trigger utile: tiene le definizioni.
- **T1.3 Leggi_File** (4.1). Provarlo dal flusso (**Test** -> **Manually**):
  - `BASE` + `Input_A1_2027Q1.txt`: `esito` ok e circa 54.558 caratteri; il testo comincia con `INPUT DI A1 PER IL
    CICLO`; accenti giusti;
  - `BASE` + `non_esiste.txt`: `non trovato`;
  - `BASE` + `../x.txt`: `nome non ammesso`;
  - `ALTRO` + `x`: `area non ammessa`.
- **T1.4 Salva_JSON** (4.2). Dal flusso:
  - `prova.json` con `{"a": 1}` due volte di seguito: un solo file, con due versioni nella cronologia;
  - poi `prova.json` con `{"a": 2}` seguito da `\n\n[1]: https://esempio`: il file contiene solo `{"a": 2}`.
- **T1.5 NFR_Motore provvisorio** (4.3, forma provvisoria). Per la prova della risposta anticipata, dopo **Respond to
  the agent** aggiungere **Delay** di 3 minuti e **Create file** `Esiti/Prova_continua.txt` con il testo `ok`.
- **T1.6 Strumenti nell'agente e ID.**
  - **Tools**: aggiungere `Leggi_File`, `Salva_JSON`, `NFR_Motore`, tutti con "Allow agent to decide dynamically"
    spento.
  - Poi un argomento temporaneo `Rilievo` (From blank): aggiungere dall'interfaccia un nodo per ciascuno dei tre
    flussi (**Add node** -> **Add a tool**). Menu **...** -> **Open code editor**: copiare le tre righe `flowId:` in
    `ID_tenant.txt`. Non salvare l'argomento.
- **T1.7 Primi argomenti.** Incollare `Aiuto.yaml`, `Stato.yaml`, `Correggi_ciclo.yaml` (sezione 5). Nel riquadro
  **Test**, conversazione nuova:
  - `Aiuto`: l'elenco dei comandi;
  - `Stato`: "Nessun esito del motore registrato finora";
  - `Correggi_ciclo 2027Q1`: subito "Motore non ancora attivo (correggi_ciclo 2027Q1) ..."; dopo 3 minuti in `Esiti`
    c'e' `Prova_continua.txt`. E' la prova che il flusso continua dopo la risposta. Poi togliere **Delay** e
    **Create file** dal flusso.
  - `Che cosa sai fare?` e `Salva il lavoro`: nessun argomento parte (mappa delle attivita'), nessun flusso nella
    cronologia di Power Automate.

### T2. A1 e A8 come sotto-agenti

- **T2.1 A1.** **Agents** -> **Add** -> **New child agent**.
  1. Name: `A1 Horizon Scanner`; **When will this be used?**: **It's redirected to**.
  2. Instructions: tutto `agenti/A1_CS.md`. Cancellare `{Global.ingresso}` e, nello stesso punto, `/` -> **Variable**
     -> `Global.ingresso`; lo stesso per `{Global.uscita}`. Il contatore deve restare sotto 8.000.
  3. Knowledge: `Analisi_Interne`, `Analisi_Esterne`, `News_Inbox` e i 4 siti (guida, 0.2). Non `Archivio_Cicli` ne'
     `Kernel`.
  4. **Completamento**: output `output`, testo, con la descrizione della sezione 3.
  5. Modello: lo stesso dell'agente, se si sceglie. **Save**.
- **T2.2 A8.** Come A1, con `agenti/A8_CS.md` e nome `A8 Evento critico`.
- **T2.3 Nodo del sotto-agente.** Nell'argomento temporaneo `Rilievo`: **Add node** -> sotto-agente A1, poi A8.
  **Open code editor**:
  - se il nodo e' `kind: BeginDialog` con una riga `dialog:`, copiare i due valori in `ID_tenant.txt`;
  - se la forma e' diversa (altro `kind`, output con altro nome), incollare il YAML del nodo nella chat con Claude:
    si adeguano gli argomenti.

  Non salvare l'argomento.
- **T2.4 Esegui_ciclo.** Incollare `Esegui_ciclo.yaml`. Conversazione nuova: `Esegui_ciclo 2027Q1`.
  - Attesi:
    1. "Allegato letto: ... caratteri. Avvio di A1";
    2. dopo qualche minuto "salvato: In_arrivo/A1_2027Q1.json, N caratteri salvati su M prodotti";
    3. "Motore non ancora attivo".
  - Annotare: tempo; M ed N, dove N <= M e la differenza sono i link tolti; il file finisce con `}`; una nuova
    versione di `A1_2027Q1.json` nella cronologia.
  - In chat non deve comparire il JSON. Se compare, provare T2.8.
- **T2.5 Indipendenza dalla conversazione.** Senza aprire una conversazione nuova, fare **Save** su un argomento
  qualsiasi e ripetere `Esegui_ciclo 2027Q1`: deve funzionare come prima. Poi in una conversazione nuova, lo stesso.
- **T2.6 Ingresso grande.** `Esegui_ciclo 2026Q4-S1`, con l'Input dello straordinario della demo (76.878 caratteri):
  - parte A8;
  - il JSON ha `analisi_evento`;
  - A8 non risponde "Allegato del ciclo straordinario mancante".

  Questa prova dice se una globale di quasi 80 KB arriva intera al sotto-agente.
- **T2.7 Prove negative.** `Esegui il ciclo` (senza trattino basso), `Lancia A1`, `Salva il lavoro`: nessun
  argomento, nessun sotto-agente, nessun flusso.
- **T2.8 JSON fuori dalla chat.** In A1 e A8, **Completamento** -> "Don't respond". Ripetere T2.4: `Global.uscita`
  deve riempirsi lo stesso, cioe' file salvato e caratteri uguali. Se resta vuota, rimettere la risposta e annotarlo:
  per Teams vale la riserva della sezione 8.

### T3. Correzione dai file (prompt Correggi nel flusso)

- **T3.1 Prompt Correggi.** Si puo' riusare `Correggi_A1` delle prove: stessi ingressi `correzione`, `json_a1`,
  `allegato`. Istruzioni = `prompt/Correggi.txt`; uscita testo; modello come A1. "Allow agent to decide
  dynamically" spento.
- **T3.2 Ramo `correggi_ciclo` di NFR_Motore**:
  1. **Respond to the agent** (`avviato`);
  2. **Get file content using path** di `In_arrivo/Correzione_A1_<p>.txt`, `In_arrivo/A1_<p>.json` e
     `<radice>/Input_A1_<p>.txt`;
  3. **Run a prompt** `Correggi_A1` con i tre testi;
  4. **Compose** `pulito` sul campo `text` dell'uscita, come in 4.2;
  5. **Copy file** di `A1_<p>.json` in `A1_<p>_giro_<ora>.json`;
  6. **Update file** `A1_<p>.json` con `pulito`;
  7. **Create file** o **Update file** di `Esiti/Ultimo_esito.txt`:
     `correggi_ciclo <p>: JSON corretto, <caratteri> caratteri (prima <caratteri>).`

  Prova: `Correggi_ciclo 2027Q1`, poi dopo qualche minuto `Stato`. Annotare il tempo e i caratteri.
  - Se il prompt va in errore o taglia: annotare il messaggio e le dimensioni (circa 54.000 + 27.000 caratteri in
    ingresso). E' la prova dei prompt con ingressi grandi.
  - Sul PC, finche' c'e', precontrollo sul file corretto: atteso 0 punti da correggere.

### T4. K9: il motore eseguito dal code interpreter

Il punto critico: decide se il motore puo' stare nel tenant. Si fa prima di costruire altro.

- **T4.1 Prompt Motore.** **Tools** -> **Add a tool** -> **Prompt**, nome `Motore`.
  1. Menu **...** -> **Settings** -> **Enable code interpreter**.
  2. Istruzioni = `prompt/Motore.txt`: `[comando]` diventa un ingresso **Text**, `[busta]` un ingresso **Image or
     document**.
  3. Nel test del prompt: busta = `K9_Busta_prova.xlsx`, comando = `precontrollo` -> **Test**.
  4. La risposta deve essere la riga di `K9_atteso.txt`: stesse impronte (`impronta_codice` = `impronta_busta` =
     quella attesa), stesso `esito`, stessa `impronta_output`.
  5. Ripetere 5 volte. Annotare: quante uguali, il tempo, se il codice mostrato nella risposta e' solo il caricamento
     dei blocchi o altro.
- **T4.2 Busta riempita dal flusso.** Nel flusso NFR_Motore, ramo `controlla`, provato dal designer con **Test** ->
  **Manually** (comando `controlla`, periodo `2027Q1`):
  1. copia di `Motore/K9_Busta_vuota.xlsx` in `Esiti/`;
  2. `A1_2027Q1.json` e `Input_A1_2027Q1.txt` nella tabella `tblIngresso` a blocchi (4.3, punto 2), con Nome `A1` e
     `Input_A1`;
  3. **Run a prompt** `Motore`;
  4. **Parse JSON** e confronto delle impronte con `Motore/Impronta.txt`.

  Atteso: stessa `impronta_output` e stesso esito del precontrollo sul PC sullo stesso file. Ripetere fino a 10 volte
  in giorni diversi.
- **T4.3 Giro automatico.** Collegare il ramo `controlla` a `registra_ciclo`:
  - controlli; se `codice_uscita` 1 e giro < 2: Correggi (T3.2) e di nuovo controlli;
  - alla fine `Ultimo_esito.txt`: "A1 controllato: 0 punti da correggere, N da verificare", oppure "fermato dopo 2
    giri: vedi Correzione_A1_<p>.txt".

  Prova completa: `Esegui_ciclo 2027Q1`, poi `Stato`.

### T5. K8: Office Scripts sul registro (se T0.1 e' positivo, altrimenti si passa a F2)

- **T5.1** Copia del registro con dati: `NFR_Registro_prova_K8.xlsx`, fuori da `Report_Trimestrali`.
  1. Excel per il web -> **Automatizza** -> **Nuovo script**: incollare `prove/K8_prova.ts`, salvare come
     `K8_prova`, **Esegui**.
  2. Atteso: `errori_formula` 0; `grafici_prima` = `grafici_dopo`; `righe_dopo` = `righe_prima` + 50.
  3. Annotare `millisecondi`. Aprire la copia nel desktop: grafici, formattazione condizionale e formule della tabella
     intatti.
- **T5.2** Lo stesso script da un flusso: Excel Online (Business) **Run script**, sulla stessa copia. Atteso: stessa
  riga JSON, sotto i 120 secondi, nessun errore di blocco del file.
- **T5.3 (K13)** Copia aperta in Excel per il web in un'altra scheda mentre il flusso esegue lo script: nessun dato
  perso. Due esecuzioni insieme: la seconda aspetta o fallisce, non scrive a meta'.
- **T5.4 Esito.** V2 o F2 secondo la tabella della sezione 6. Il codice del motore (adattatore del registro, script
  "prepara" e "applica" o la scrittura F2, caricatore) e' la consegna successiva, scritta sui risultati di T4 e T5.

### T6. Gli altri agenti

- **T6.1 A5 a richiesta.**
  1. Prompt `A5` con `prompt/A5.txt` (ingressi `json_a1`, `baseline`).
  2. Nel ramo `registra_ciclo`, se `parametri` = `A5`: **Run a prompt** `A5` -> `pulito` -> `In_arrivo/A5_<p>.json`.
  3. Prova: `Esegui_ciclo 2027Q1 A5`. Annotare se il JSON rispetta lo schema (lo verifica il motore) e confrontarlo
     con A5 di Agent Builder sullo stesso output.
- **T6.2 A3 e notizie.**
  1. Sotto-agente `A3 Interim Update` con `agenti/A3_CS.md`: tre variabili da inserire con `/`; knowledge come A1.
     ID in `ID_tenant.txt` come T2.3.
  2. Incollare `Esegui_settimana.yaml`.
  3. Flusso `Raccolta_notizie` (4.4), eseguito a mano una volta.
  4. Prova: `Esegui_settimana <lunedi' corrente>` -> `In_arrivo/A3_<lunedi'>.json`.
  5. Annotare: notizie, codici fonte, confronto con la raccolta dello script dello stesso giorno, se disponibile.
- **T6.3 A6.** Prompt `A6` con `prompt/A6.txt`. Prova nel test del prompt con un `Schede_input_<ciclo>.json`
  dell'archivio. Si collega al motore con T5.4.

### T7. Teams

- **T7.1** Se T2.8 e' riuscito, "Don't respond" in A1, A8 e A3. **Publish**. **Channels** -> **Teams and Microsoft 365
  Copilot** -> **Add channel** -> **See agent in Teams**.
- **T7.2** In Teams: `Aiuto`, `Esegui_ciclo 2027Q1`, `Stato`. Annotare errori con codice e ora.
  - Se un comando non fa partire il suo argomento: cambiare il trigger in "The agent chooses" con la descrizione
    `Solo quando il messaggio comincia con <comando>. Mai in altri casi.`
- **T7.3** Avviso di fine di NFR_Motore in Teams (4.3): arriva una volta per comando, con la riga di
  `Ultimo_esito.txt`.

### T8. A4 e A7

Restano in Agent Builder. Quando il motore scrive (dopo T5.4) si verifica solo che la loro knowledge si aggiorni da
sola:
- `Kernel/Baseline_corrente.txt` per A4;
- `Kernel/Spiegazioni` per A7.

Prova: dopo un `Valida`, una domanda ad A7 su un valore cambiato.

## 8. Strade alternative

| Ipotesi | Prova che la decide | Se non regge |
|---|---|---|
| Il sotto-agente legge `Global.ingresso` anche a 77.000 caratteri | T2.6 | Libreria `Ingresso` con il solo Input del periodo come knowledge di A1/A8 (copiata dal flusso); oppure A1 come agente connesso (**Add an agent** -> agente esistente, input di testo) |
| L'output di Completamento contiene il JSON intero | T2.4 (N vicino a M, file valido) | Argomento con trigger `OnGeneratedResponse` che copia `System.Response.FormattedText` in `Global.uscita`; oppure A1 che chiama `Salva_JSON` come strumento, con descrizione legata al comando (B3, 09/10) |
| `Global.uscita` si riempie con "Don't respond" | T2.8 | Risposta in chat solo nel riquadro Test; in Teams un messaggio breve generato da A1 al posto del JSON |
| Un prompt accetta 80.000 caratteri di ingresso | T3.2 | Correggi come sotto-agente con le globali (lo schema di A1); per A5, la baseline senza la parte KRI |
| Il flusso continua dopo "Respond to the agent" | T1.7 | Flusso cloud con trigger "When a file is created" in `In_arrivo/Richieste/`: l'argomento scrive la richiesta con Salva_JSON (lista bianca CS-1). Senza limite di tempo; costo da chiarire con l'IT |
| Il code interpreter esegue il nostro codice tale e quale | T4.1, T4.2 | Sezione 6: V1 con Office Scripts, altrimenti A-15 |
| Office Scripts disponibile | T0.1, T5 | F2 (sezione 6) |
| Il trigger sul testo parte anche in Teams | T7.2 | "The agent chooses" con la descrizione del comando |
| `Run a prompt` nei flussi e' gratuito per chi ha Copilot | T0.3 | Prompt chiamati dagli argomenti (nodo prompt, come Correzione A1 del 23/10): niente giro automatico, ma `Correggi_ciclo` a mano dopo `Stato` |

## 9. Tabella dei risultati

| Passo | Esito e note (data, tempo, caratteri, messaggi) |
|---|---|
| T0.1 Office Scripts (scheda Automatizza) | |
| T0.2 Enable code interpreter nei prompt | |
| T0.3 Risposte dell'IT (costi, connettori) | |
| T1.3 Leggi_File: 4 casi | |
| T1.4 Salva_JSON: versioni, link tolti | |
| T1.7 Aiuto, Stato, risposta anticipata, prove negative | |
| T2.3 Forma del nodo sotto-agente | |
| T2.4 Esegui_ciclo 2027Q1: tempo, M, N | |
| T2.5 Dopo un Save e in conversazione nuova | |
| T2.6 Straordinario a 77.000 caratteri | |
| T2.7 Prove negative | |
| T2.8 Don't respond | |
| T3.2 Correggi nel flusso: tempo, caratteri, errori | |
| T4.1 Motore nel test del prompt: 5 esecuzioni | |
| T4.2 Busta dal flusso: 10 esecuzioni | |
| T4.3 Giro automatico | |
| T5.1 K8 in Excel per il web | |
| T5.2 K8 da flusso | |
| T5.3 K13 concorrenza | |
| T6.1 A5 a richiesta | |
| T6.2 A3 e Raccolta_notizie | |
| T6.3 A6 | |
| T7.2 Teams | |
| T7.3 Avviso in Teams | |

## 10. Cosa resta da decidere

- **D-02** (niente Office Scripts) va rivista se si va con V2. **D-01** (niente Copilot Studio e Power Automate),
  **D-10** (JSON portato a mano allo script) e **D-11** (niente capability) cambiano per questa versione. Si
  formalizzano con la decisione A-15, sui risultati di T4 e T5.
- **Governance** (`04_Riferimenti/controlli_e_model_risk.md`): il motore eseguito da un modello e verificato con
  l'impronta, e il rischio residuo di un modello che inventa un'uscita con l'impronta giusta (analisi 15).
- **Trascrizioni** e dati nelle conversazioni: parere della DPO (D2).

## Fonti (Microsoft Learn, consultate il 23/10/2026)

- [Use code interpreter in a prompt](https://learn.microsoft.com/en-us/microsoft-copilot-studio/code-interpreter-for-prompts) (30/09/2026): un solo file in ingresso e uno in uscita, codice generato dal modello, autenticazione utente, costo "premium".
- [Using topic triggers](https://learn.microsoft.com/en-us/microsoft-copilot-studio/authoring-triggers): trigger "A message is received".
- [Edit your agent in Visual Studio Code](https://learn.microsoft.com/microsoft-copilot-studio/visual-studio-code-extension-edit-agent-components): YAML degli argomenti.
- Modelli YAML di Microsoft ([skills-for-copilot-studio](https://github.com/microsoft/skills-for-copilot-studio)): `OnActivity` con `type: Message` e `condition`, `Question`, `ConditionGroup`, `init:` per le variabili nuove, `OnGeneratedResponse`.
- Le fonti delle prove precedenti sono in `Prova_K6_Operatore.md`.
