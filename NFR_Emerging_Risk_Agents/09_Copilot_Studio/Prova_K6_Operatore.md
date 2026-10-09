# Prova K6: l'Operatore NFR esegue A1 e salva in SharePoint (CS-1, argomento a passi fissi)

Prova K6 dell'opzione 2 (`Analisi_Architettura/12_Due_opzioni.md`, 12.4; piano 10, 10.12), decisa il 09/10 dopo la
prima tornata della prova K0 (`Prova_con_Copilot_Studio.md`).

Con un solo comando in chat, un agente "Operatore" esegue una sequenza fissa:
1. legge l'allegato di A1 da SharePoint;
2. lo passa ad A1;
3. salva il JSON di A1 in una cartella SharePoint;
4. risponde con nome del file e numero di caratteri.

Nessun passo lo decide il modello: li decide un **argomento** (topic). Il JSON non passa mai nei messaggi della
chat, quindi non c'e' il limite di circa 100 KB dei messaggi di Teams che ha dato errori in K0.

Cosa resta sul PC, come oggi:
- il precontrollo, facoltativo;
- `trimestrale`, che fa i controlli e scrive nel registro (D-10).

**Obiettivo dell'utente (09/10): a regime nessun Python sul PC, tutto via agenti Copilot Studio.** In questa prova
il PC serve solo a controllare il risultato. Come portare nel cloud controlli e scrittura e' oggetto di un'analisi
a parte; questa prova vale per tutte le varianti, perche' orchestrazione, sotto-agenti e flussi sono comuni.

Si lavora solo nell'**esperienza standard**: nessun credito per chi ha la licenza Microsoft 365 Copilot. I flussi
hanno il trigger "When an agent calls the flow" e si usano in modo interattivo.

## 1. Le cartelle: dove legge e dove scrive

Non serve una library nuova "Work": la cartella di lavoro e' **`Archivio_Cicli\In_arrivo`**, gia' prevista dalla
CS-1. E' l'**unica** cartella in cui Copilot Studio scrive.

| Cartella | Chi legge | Chi scrive | Nella prova |
|---|---|---|---|
| `Analisi_Interne`, `Analisi_Esterne`, `News_Inbox` | A1 (knowledge del sotto-agente) | le persone | come oggi |
| `Archivio_Cicli` (radice): `Input_A1_<ciclo>.txt` | il flusso `Leggi_Input` | lo script (`baseline`) | `Archivio_Cicli\Prova_K0\Input_A1_2026Q4.txt`, copiato a mano da `C:\NFR_Prova\Archivio` |
| `Archivio_Cicli\In_arrivo` | lo script (`precontrollo`, `trimestrale`) | **solo** il flusso `Salva_JSON` | `Archivio_Cicli\Prova_K0\In_arrivo` |
| registro, `Kernel`, il resto di `Archivio_Cicli` | — | solo lo script | non si toccano |

Tre regole valgono anche dopo la prova:
- **L'agente non sceglie dove scrivere.** La cartella e' fissa nel flusso; il nome del file lo compone l'argomento
  (`A1_<ciclo>.json`). Un errore del modello non puo' scrivere altrove ne' toccare il registro.
- **Le cartelle di lettura e quella di scrittura sono separate.** `Archivio_Cicli` e `Kernel` non vanno nella
  knowledge di A1, che altrimenti leggerebbe i propri output e la baseline come se fossero evidenze.
- **Gli strumenti che scrivono non partono da soli.** Il flusso lo chiama l'argomento, non il modello: nello
  strumento si toglie "Allow agent to decide dynamically when to use this tool". Il comando `Scrivi_JSON` di B3
  serviva quando era il modello a decidere; qui non serve.

Preparazione in SharePoint (5 minuti):
1. creare `Archivio_Cicli\Prova_K0\In_arrivo`;
2. copiare `C:\NFR_Prova\Archivio\Input_A1_2026Q4.txt` in `Archivio_Cicli\Prova_K0\`.

Va bene il file della prova senza Copilot Studio, rifatto con il pacchetto dell'08/10 ("Prima di ripetere" in
`Prova_con_Copilot_Studio.md`).

## 2. Costruzione (circa un'ora)

Le etichette sono quelle di Microsoft Learn in inglese. Se una voce non c'e' o si chiama diversamente, annotarlo:
e' un risultato della prova.

### 2.1 I due agent flow

Si creano dall'agente: **Tools** -> **Add a tool** -> **New agent flow**. In tutti e due i campi si riempiono con
le **variabili del flusso**, scelte dal contenuto dinamico (icona del fulmine, oppure `/`), mai scrivendo il nome a
mano: e' la causa del salvataggio nel OneDrive in B3.

**`Leggi_Input`** (nuovo):
1. Trigger **When an agent calls the flow** con un input di testo `ciclo`.
2. Azione SharePoint **Get file content using path**:
   - sito NFR;
   - File Path = espressione `concat('/Archivio_Cicli/Prova_K0/Input_A1_', triggerBody()?['text'], '.txt')`;
   - se l'input ha un altro nome interno, si sceglie `ciclo` dal contenuto dinamico dentro `concat`.
3. Azione **Respond to the agent** con due output:
   - testo `allegato` = il contenuto del file;
   - numero `caratteri` = `length(...)` dello stesso valore.
4. Salvare, pubblicare, poi **provare il flusso da solo** con `ciclo` = `2026Q4`.
   - `allegato` deve cominciare con `INPUT DI A1 PER IL CICLO 2026Q4`.
   - `caratteri` deve essere vicino alla dimensione del file: 50-80 mila.
   - Se `allegato` comincia con `{"$content-type"` o e' illeggibile, il contenuto e' arrivato in base64. Allora
     l'output si scrive con l'espressione `base64ToString(body('Get_file_content_using_path')?['$content'])`: il
     nome dell'azione e' quello che compare nel flusso. Controllare anche che le lettere accentate siano giuste.

**`Salva_JSON`** (quello di B3, modificato):
1. Folder Path: `/Archivio_Cicli/Prova_K0/In_arrivo`.
2. In **Respond to the agent**, oltre a `esito`, un output numero `caratteri` = `length(contenuto)`, con
   `contenuto` dal contenuto dinamico.
3. Salvare e pubblicare.

### 2.2 L'agente "NFR Operatore prova"

1. Home di Copilot Studio, **New experience spenta** -> **Create** -> **New agent** -> scheda **Configure**.
2. Compilare:
   - Name: `NFR Operatore prova`;
   - Description: `Prova K6: esegue A1 e salva il JSON in SharePoint con un comando`;
   - Instructions:

     `Sei l'Operatore NFR di prova. Esegui solo cio' che dicono gli argomenti. Non valutare rischi, non scrivere JSON, non chiamare strumenti o agenti di tua iniziativa. Se l'utente chiede altro, rispondi che l'unico comando disponibile e' Esegui_ciclo.`
3. **Settings -> Generative AI**:
   - orchestrazione generativa;
   - il modello piu' capace disponibile, lo stesso di K0, annotandone il nome;
   - **Use general knowledge** e **Web search** spenti;
   - Code interpreter non serve;
   - **Save**.
4. **Settings -> Security -> Authentication**: "Authenticate with Microsoft".
5. **Tools**: aggiungere `Leggi_Input` e `Salva_JSON`. In ciascuno, sotto **Additional details**, **togliere**
   "Allow agent to decide dynamically when to use this tool". Cosi' li chiama solo l'argomento.

### 2.3 Il sotto-agente A1

**Agents** -> **Add** -> **New child agent**:
1. Name: `A1 Horizon Scanner`.
2. **When will this be used?**: **It's redirected to**. Lo chiama solo l'argomento, mai l'orchestrazione.
3. Instructions: il file intero `02_Agenti\A1_Horizon_Scanner.md` del pacchetto (7.963 caratteri). Se il campo ha
   un limite diverso da quello dell'agente, annotarlo.
4. **Knowledge**:
   - `Analisi_Interne`, `Analisi_Esterne`, `News_Inbox`;
   - i 4 siti, come A1 in Agent Builder (guida, 0.2).

   Non `Archivio_Cicli` ne' `Kernel`.
5. **Inputs** -> **Add Input**:
   - Display name `allegato`, tipo String, obbligatorio;
   - Description: `Il testo intero dell'allegato Input_A1 del ciclo (baseline, controlli, guida di scrittura): e' l'allegato di cui parlano le istruzioni.`
6. **Outputs** -> **Add output**:
   - Display name `json_a1`, tipo String;
   - Description: `L'output JSON completo di A1, come nella sezione Output delle istruzioni: solo il JSON, intero, senza testo attorno.`
7. **After running**: **Don't respond**.
8. **Save**.

### 2.4 L'argomento "Esegui ciclo"

**Topics** -> **Add a topic** -> **From blank**, nome `Esegui ciclo`.

1. **Trigger**:
   - **A message is received**, con **Condition** in formula: `StartsWith(System.Activity.Text, "Esegui_ciclo")`;
   - se quel trigger non c'e', usare quello predefinito ("The agent chooses") con la descrizione `Solo quando
     l'utente scrive il comando Esegui_ciclo. Mai in altri casi.`, e annotarlo.
2. **Question**:
   - testo: `Quale ciclo? (per esempio 2026Q4)`;
   - identify: User's entire response;
   - salvare in `Topic.ciclo`.
3. **Call an action** -> `Leggi_Input`:
   - `ciclo` = `Topic.ciclo`;
   - output in `Topic.allegato` e `Topic.caratteri_input`.
4. **Message**: `Allegato letto: {Topic.caratteri_input} caratteri. Avvio A1: possono servire alcuni minuti.`
5. **Add an agent** -> `A1 Horizon Scanner`:
   - input `allegato` = `Topic.allegato`;
   - output in `Topic.json_a1`.
6. **Call an action** -> `Salva_JSON`:
   - `nome_file` = formula `"A1_" & Topic.ciclo & ".json"`;
   - `contenuto` = `Topic.json_a1`;
   - output in `Topic.esito` e `Topic.caratteri_salvati`.
7. **Message**: `A1 finito. {Topic.esito}: Archivio_Cicli/Prova_K0/In_arrivo/A1_{Topic.ciclo}.json, {Topic.caratteri_salvati} caratteri salvati su {Len(Topic.json_a1)} prodotti da A1. Ora sul PC: precontrollo (facoltativo) e trimestrale.`
8. **End all topics**.

Nessun messaggio contiene il JSON. **Save**.

## 3. Test

Prima nel riquadro **Test**, poi in Teams. Ogni test in una conversazione nuova.

| Test | Dove | Messaggio | Cosa annotare |
|---|---|---|---|
| **K6.1** sequenza | Test | `Esegui_ciclo`, poi `2026Q4` | I passi in ordine nella mappa delle attivita' (Activity)? Caratteri dell'allegato. Tempo totale. Il file e' in `Prova_K0\In_arrivo`? Caratteri salvati = caratteri prodotti? |
| **K6.2** controllo sul PC | PC, cartella `C:\NFR_Prova\pacchetto\07_Senza_Studio` | `python esegui_ciclo_locale.py precontrollo --payload "<cartella sincronizzata>\Archivio_Cicli\Prova_K0\In_arrivo\A1_2026Q4.json"` | Prima riga e impronta. "non e' un JSON valido" = A1 ha messo testo attorno o il JSON e' troncato. Facoltativo: `trimestrale` con lo stesso `--payload` sul registro di prova |
| **K6.3** prova negativa | Test | `Salva il lavoro`, poi `Che cosa sai fare?` | Nessuna esecuzione di `Leggi_Input` e `Salva_JSON` nella cronologia dei flussi; nessun file nuovo; A1 non parte |
| **K6.4** ripetizione | Test | come K6.1 | Stessa sequenza? Il file viene sovrascritto o ne nasce una copia? Annotare. Il contenuto puo' cambiare: A1 e' un modello |
| **K6.5** Teams | Publish, poi canale **Teams and Microsoft 365 Copilot** | come K6.1, poi K6.3 | Come K6.1. Errori? Annotare **codice dell'errore** e ora. Il turno dura minuti: un timeout del canale e' un risultato |

## 4. Come si leggono i risultati

- **K6 riesce** se:
  - la sequenza e' sempre la stessa;
  - il file arriva con i caratteri uguali e il precontrollo lo legge;
  - la prova negativa non fa partire niente;
  - Teams regge.

  Poi, in quest'ordine:
  1. K6b: il pulsante **Correggi**. Dopo un precontrollo, il messaggio di correzione torna ad A1 nella stessa
     sequenza.
  2. A5 come strumento "prompt" dopo A1.
  3. Controlli e scrittura senza il PC, secondo l'analisi decisa (code interpreter, Office Scripts).
- **Il sotto-agente non riceve l'allegato** (A1 risponde che manca l'allegato, o lavora senza baseline): provare a
  passarlo anche nel compito in linguaggio naturale. In alternativa l'utente allega `Input_A1` in chat prima di
  `Esegui_ciclo`.
- **`json_a1` arriva troncato o con testo attorno** (caratteri diversi, precontrollo "non e' un JSON valido"): far
  salvare il file ad A1 stesso, con `Salva_JSON` tra gli strumenti del sotto-agente, citato nelle sue istruzioni.
  E' il percorso gia' riuscito in B3, con impronta uguale.
- **In Teams il turno scade** (A1 impiega minuti): annotare il tempo. La CS-1 puo' spezzare il turno: "A1 avviato",
  poi un messaggio quando il file e' salvato.

Gli esiti si riportano nella tabella qui sotto e nella decisione A-15 (TODO, AU4).

## Tabella dei risultati

| Voce | Esito |
|---|---|
| Costruzione: flussi pubblicati; `Leggi_Input` provato da solo (prima riga, caratteri, accenti); istruzioni di A1 accettate nel sotto-agente; trigger dell'argomento usato | |
| K6.1: sequenza in ordine; caratteri allegato; tempo; caratteri salvati = prodotti | |
| K6.2: precontrollo sul PC (prima riga, impronta); `trimestrale` se fatto | |
| K6.3: prova negativa, nessuna esecuzione | |
| K6.4: ripetizione, stessa sequenza; sovrascrittura o copia | |
| K6.5: Teams, esito e codici di errore | |
| Qualita' di A1 rispetto ad Agent Builder (numero di rischi, punti del precontrollo) | |

## Fonti (Microsoft Learn, consultate il 09/10/2026)

- [Add other agents overview](https://learn.microsoft.com/en-us/microsoft-copilot-studio/authoring-add-other-agents) (15/05/2026): redirect a un sotto-agente da un argomento, con input e output.
- [Add a child agent](https://learn.microsoft.com/en-us/microsoft-copilot-studio/add-agent-child-agent) (25/08/2026): input e output, "It's redirected to", "Allow agent to decide dynamically when to use this tool".
- [Use agent flows: input and output](https://learn.microsoft.com/en-us/microsoft-copilot-studio/advanced-flow-input-output): parametri String, Number, Boolean; fino a 1 MB da un flusso all'agente.
- [Billing rates and management](https://learn.microsoft.com/en-us/microsoft-copilot-studio/requirements-messages-management) (03/08/2026): "No charge" per gli utenti Microsoft 365 Copilot e per i flussi con "When an agent calls the flow".
