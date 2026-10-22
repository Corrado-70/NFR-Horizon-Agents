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
   - File Path = testo `/Archivio_Cicli/Prova_K0/Input_A1_`, poi la pillola `ciclo` dal contenuto dinamico, poi il
     testo `.txt`. Non scrivere `concat(...)` nel campo: viene preso come testo letterale (visto il 15/10: "File not
     found" con `path` = `concat('...` negli input non elaborati). Gli input del trigger hanno nomi interni `text`,
     `text_1`, ... nell'ordine in cui sono creati (`ciclo` = `text`).
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
- **Il sotto-agente non riceve l'allegato** (A1 risponde che manca l'allegato, o lavora senza baseline): e' l'esito
  del 15/10. Allegarlo in chat non serve, e nemmeno richiamare l'input nelle istruzioni con `/`: si passa alla variante
  K6-bis (sezione 5).
- **`json_a1` arriva troncato o con testo attorno** (caratteri diversi, precontrollo "non e' un JSON valido"): far
  salvare il file ad A1 stesso, con `Salva_JSON` tra gli strumenti del sotto-agente, citato nelle sue istruzioni.
  E' il percorso gia' riuscito in B3, con impronta uguale.
- **In Teams il turno scade** (A1 impiega minuti): annotare il tempo. La CS-1 puo' spezzare il turno: "A1 avviato",
  poi un messaggio quando il file e' salvato.

Gli esiti si riportano nella tabella qui sotto e nella decisione A-15 (TODO, AU4).

## Tabella dei risultati

| Voce | Esito |
|---|---|
| Costruzione: flussi pubblicati; `Leggi_Input` provato da solo (prima riga, caratteri, accenti); istruzioni di A1 accettate nel sotto-agente; trigger dell'argomento usato | 15/10: flussi pubblicati; `Leggi_Input` provato da solo e dall'argomento (54.558 caratteri); trigger dell'argomento usato |
| K6.1: sequenza in ordine; caratteri allegato; tempo; caratteri salvati = prodotti | 15/10: **non riuscita**. Il sotto-agente non riceve l'allegato, ne' come input ne' come variabile `/` nelle istruzioni (sezione 5.1); `json_a1` vuoto; `Salva_JSON` fermo su `text_1` vuoto |
| K6.2: precontrollo sul PC (prima riga, impronta); `trimestrale` se fatto | |
| K6.3: prova negativa, nessuna esecuzione | |
| K6.4: ripetizione, stessa sequenza; sovrascrittura o copia | |
| K6.5: Teams, esito e codici di errore | |
| K6bis.1: sequenza (`Leggi_Input`, ricerche, `Salva_JSON`); tempo; file in `In_arrivo`; caratteri | |
| K6bis.2: precontrollo sul PC (prima riga, impronta) | |
| K6bis.3: prova negativa, nessuna esecuzione | |
| K6bis.4: ripetizione; sovrascrittura o errore | |
| K6bis.5: Teams, esito, codici di errore, durata del turno | |
| Qualita' di A1 rispetto ad Agent Builder (numero di rischi, punti del precontrollo) | |
| **K6ter.1**: A1 con variabili globali; file in `In_arrivo`; tempo; modello | 22/10: **riuscita**. `A1_2027Q1.json` in `Prova_K0\In_arrivo`, 27.529 caratteri, in circa 1 minuto; modello GPT-5 reasoning |
| **K6ter.2**: precontrollo sul PC (prima riga, impronta) | 22/10: **JSON valido**, impronta `cdfc636c3659`; 1 punto da correggere (NFR-02, C2), 5 da verificare (NFR-02 C3; NFR-03, 04, 05, 08 C5 fonti perse) |
| K6ter.1-bis: istruzioni con analisi a fondo e rianalisi; tempo; ricerche; file sovrascritto, copia o errore; punti del precontrollo rispetto al 22/10 | |
| K6ter.3: giro di correzione nella stessa conversazione; il file viene sovrascritto, va in errore o ne nasce una copia | 22/10: **non riuscita**. Messaggio di correzione incollato nella stessa conversazione: A1 risponde che non sa quali azioni fare, nessun JSON. Si passa all'argomento `Correzione A1` (5.5) |
| K6ter.3-bis: argomento `Correzione A1`; sequenza dei nodi; caratteri letti e salvati; tempo; modello del prompt | |
| K6ter.3-bis: precontrollo su `A1_<ciclo>_corretto.json` (prima riga, impronta) | |
| K6ter.4: prova negativa, nessuna esecuzione | |
| K6ter.5: Teams (il JSON passa in chat: limite di circa 100 KB), esito, codici di errore, durata | |
| K6ter: come si riempie `Global.allegato` | 22/10: nell'argomento di lancio, nodo **Azione** `Leggi_Input` con `ciclo` = variabile `ciclo`; output `allegato` -> `Global.allegato`, `caratteri` -> `char_input`. Nome della variabile dell'output da annotare (qui `Global.OutputA1`) |

## 5. Esito del 15/10 e variante K6-bis

### 5.1 Che cosa e' successo con il sotto-agente (K6.1)

- `Leggi_Input` funziona: dall'argomento legge `Input_A1_2027Q1.txt` (54.558 caratteri) in pochi secondi.
- Il sotto-agente A1 chiamato dall'argomento **non riceve l'allegato come compito**. In tre prove ha risposto:
  prima ripetendo il comando (`ESEGUI_CICLO`), poi "Baseline mancante: ciclo non eseguibile", poi `Comando
  "Esegui_ciclo" eseguito.`, sempre in circa un minuto e con `json_a1` vuoto (`Salva_JSON` si ferma: "parametro
  obbligatorio `text_1` vuoto").
- Allegare `Input_A1` in chat non serve: il sotto-agente riceve solo il compito e gli input, non gli allegati della
  conversazione.
- Il menu `/` delle istruzioni del sotto-agente offre anche **Variabile** (in fondo al testo delle istruzioni:
  variabili `System.` e l'input `Input_A1`). Prova finale: input `Input_A1` = `allegato` (54.558 caratteri) nel nodo
  dell'argomento, e in fondo alle istruzioni una riga `# Allegato Input_A1` seguita dalla variabile `Input_A1`
  inserita con `/`. A1 risponde comunque "Baseline mancante: ciclo non eseguibile". Non si sa se il valore resti
  vuoto nel sotto-agente o sia escluso per la dimensione: Copilot Studio non lo mostra e la documentazione non lo dice.
- Tra le variabili disponibili c'e' `System.LastMessage.Text`, l'ultimo messaggio dell'utente: e' probabilmente il
  testo su cui il sotto-agente ha lavorato (`Esegui_ciclo`, `2027Q1`).
- Le impostazioni avanzate degli input (condizione, "Nessuna entita' valida trovata", reindirizzamento) mostrano a
  che cosa servono: valori brevi che l'agente estrae dalla conversazione o chiede all'utente, non un documento di
  50-80 KB.

Conclusione per la CS-1: la sequenza a passi fissi **argomento -> sotto-agente con input e output** non porta
l'allegato ad A1 in questa versione di Copilot Studio, ne' come input ne' come variabile richiamata nelle istruzioni.
Si prova la variante K6-bis.

### 5.2 K6-bis: A1 come agente con due strumenti

Si basa sull'unico meccanismo gia' riuscito in Banca: in B3 (09/10) un agente ha passato a un agent flow un JSON di
40-60 KB, arrivato intero in SharePoint con la stessa impronta. L'allegato arriva ad A1 come **risultato di uno
strumento** e il JSON esce come **input di uno strumento**: niente argomento, sotto-agente, variabili od output
strutturati.

Differenza da K6: l'ordine dei passi non lo fissa un argomento, lo decide l'orchestrazione dell'agente guidata dalle
descrizioni degli strumenti. Per questo la prova negativa (K6bis.3) conta di piu'.

**Costruzione** (circa mezz'ora; i flussi sono quelli della sezione 2.1, gia' pubblicati):

1. Agente **`A1 CS prova`** (si puo' riusare quello di K0), esperienza standard, scheda **Configure**:
   - Instructions: il file intero `02_Agenti\A1_Horizon_Scanner.md` del pacchetto, senza modifiche;
   - Knowledge: `Analisi_Interne`, `Analisi_Esterne`, `News_Inbox` e i 4 siti, come A1 in Agent Builder (guida, 0.2);
     non `Archivio_Cicli` ne' `Kernel`;
   - **Settings -> Generative AI**: orchestrazione generativa; il modello piu' capace disponibile, annotandone il
     nome; **Use general knowledge** e **Web search** spenti;
   - **Settings -> Security -> Authentication**: "Authenticate with Microsoft".
2. **Tools -> Add a tool** -> `Leggi_Input`. Le descrizioni degli strumenti non contano nel limite di 8.000
   caratteri delle istruzioni: qui si spiega ad A1 che cosa riceve.
   - Description:

     `Legge l'allegato Input_A1 del ciclo. Usalo per primo, una sola volta, quando l'utente chiede di eseguire il ciclo, con ciclo = il ciclo indicato nel messaggio (es. 2027Q1). Il testo restituito in "allegato" E' l'allegato Input_A1 di cui parlano le istruzioni: baseline, controlli di A5, guida di scrittura. Non usarlo in nessun altro caso.`
   - Input `ciclo`: lo riempie l'agente, descrizione `Il ciclo indicato dall'utente, nel formato AAAAQn.`
   - Lasciare acceso "Allow agent to decide dynamically when to use this tool" (qui e' l'agente che decide).
3. **Tools -> Add a tool** -> `Salva_JSON`:
   - Description:

     `Salva in SharePoint il JSON finale di A1. Usalo solo alla fine dell'esecuzione del ciclo, una volta, dopo aver verificato il JSON con controlli e guida dell'allegato. nome_file = "A1_" seguito dal ciclo e da ".json" (es. A1_2027Q1.json). contenuto = il JSON intero, senza modifiche e senza testo attorno. Non usarlo in nessun altro caso: non per altri file, non se l'utente chiede di salvare altro.`
   - Inputs `nome_file` e `contenuto`: li riempie l'agente, con le frasi corrispondenti della descrizione.
4. **Save**, poi **Publish** (per K6bis.5 in Teams).

**Test** (ogni test in una conversazione nuova; ciclo = quello di cui c'e' l'allegato in `Prova_K0`):

| Test | Dove | Messaggio | Cosa annotare |
|---|---|---|---|
| **K6bis.1** sequenza | Test | `Esegui il ciclo 2027Q1` | Nella mappa delle attivita': `Leggi_Input` una volta, poi ricerche nella knowledge, poi `Salva_JSON` una volta. Tempo totale (deve essere di minuti). Il file `A1_2027Q1.json` e' in `Prova_K0\In_arrivo`? `caratteri` restituito da `Salva_JSON` |
| **K6bis.2** controllo sul PC | PC | `python esegui_ciclo_locale.py precontrollo --payload "<cartella sincronizzata>\Archivio_Cicli\Prova_K0\In_arrivo\A1_2027Q1.json"` | Prima riga e impronta. Il precontrollo confronta con `Baseline_corrente.json` della cartella di uscita: deve essere quella dello stesso ciclo, altrimenti usare `--baseline` |
| **K6bis.3** prova negativa | Test | `Salva il lavoro`, poi `Che cosa sai fare?` | Nessuna esecuzione di `Leggi_Input` e `Salva_JSON` nella cronologia dei flussi; nessun file nuovo |
| **K6bis.4** ripetizione | Test | come K6bis.1 | Stessa sequenza? `Create file` sul file esistente: errore o copia? |
| **K6bis.5** Teams | canale **Teams and Microsoft 365 Copilot** | come K6bis.1, poi K6bis.3 | Errori, codici, durata del turno |

**Come si leggono:**
- **Riesce** se la sequenza e' quella attesa, il file arriva intero (precontrollo lo legge, caratteri coerenti), la
  prova negativa non fa partire niente e Teams regge. Allora la CS-1 si puo' costruire con A1 (e A8) come agenti
  con strumenti, e l'Operatore orchestra gli agenti invece di passare input ai sotto-agenti.
- **A1 risponde "Baseline mancante" senza chiamare `Leggi_Input`**: la descrizione dello strumento non basta.
  Scrivere nel messaggio `Prima chiama Leggi_Input con ciclo 2027Q1, poi esegui il ciclo sull'allegato restituito.`
  Se funziona solo cosi', annotarlo: il comando dell'utente diventa questa frase (un pulsante in Teams puo' mandarla).
- **A1 scrive il JSON in chat e non chiama `Salva_JSON`**: annotarlo; in Teams un JSON in chat puo' superare il
  limite di circa 100 KB dei messaggi (errori di K0).
- **Il file arriva troncato** (precontrollo: "non e' un JSON valido"): annotare caratteri e dimensione; e' il limite
  da portare nella decisione A-15.
- **`Leggi_Input` o `Salva_JSON` partono senza richiesta** (K6bis.3): la CS-1 con orchestrazione generativa non e'
  sicura; restano la strada A o una sequenza fissa.

### 5.3 K6-ter: A1 con variabili globali (22/10)

Prova fatta dall'utente il 22/10 dopo K6: l'allegato e il JSON passano da **due variabili globali**, citate nelle
istruzioni di A1.
- **Lettura**: le istruzioni dicono che l'allegato Input_A1 e' il valore di `Global.allegato`. La riempie
  l'argomento di lancio: nodo **Azione** `Leggi_Input`, output `allegato` -> `Global.allegato`, `caratteri` ->
  `char_input`.
- **Scrittura**: A1 risponde solo con il JSON e la stessa risposta va in `Global.OutputA1`, da cui `Salva_JSON` la
  scrive in `Prova_K0\In_arrivo`.

Istruzioni: `Da_caricare/A1_Horizon_Scanner_CS.md`, generate da `genera_A1_CS.py` a partire dall'A1 attuale. Le
differenze sono solo le frasi di Input e Output; inoltre gli elenchi perdono il trattino e la frase sulla ricerca
file e' accorciata, per restare sotto 8.000 caratteri. In Copilot Studio i due segnaposto `{Global.allegato}` e
`{Global.OutputA1}` si sostituiscono con le variabili inserite con `/`. Il collaudo verifica che il file corrisponda
all'A1 attuale.

**Esito del 22/10** (tabella dei risultati, righe K6ter):
- A1 ha prodotto `A1_2027Q1.json` (27.529 caratteri) in circa 1 minuto, con GPT-5 reasoning.
- Il precontrollo sul PC lo legge per intero: e' la prima volta che la catena **allegato da SharePoint -> A1 in
  Copilot Studio -> JSON in SharePoint** arriva fino al precontrollo.
- I rilievi sono di qualita' della valutazione, come per A1 in Agent Builder. Una Probabilita salita di 2 punti senza
  la voce in `variazioni` (C2, C3) e quattro rischi con meno fonti a valori invariati (C5). Un minuto e' poco per
  rileggere la knowledge su tutti i rischi: la qualita' va confrontata con Agent Builder sullo stesso allegato (Prove
  CS-1, K4).

**Istruzioni di A1 dal 22/10 sera**: oltre alle variabili, analisi a fondo e rianalisi, in prova solo qui.
- Input: "piu' ricerche per rischio (nome, meccanismo, fonti della baseline); leggi e analizza nel dettaglio ogni
  fonte prima di valutare". La frase del ruolo (D-64) e' spostata qui.
- Passo 10: "Rianalizza tutto con controlli e guida (fonti valide della baseline riprese, una voce in variazioni per
  valore cambiato, max un punto); correggi".

  Mira ai rilievi del primo run. Un modello che rilegge il proprio output tende pero' a confermarlo (D-69): il
  controllo affidabile resta il precontrollo.
- Per fare spazio:
  - due titoli piu' corti;
  - modelli dei razionali ridotti ai puntini (struttura ed esempi sono nella guida di scrittura dell'allegato).

  7.932 caratteri con i segnaposto, margine 60.

### 5.4 Passi delle prossime prove (K6ter.1-bis, .3, .4, .5)

Si lavora come il 22/10: stessi flussi, stesse variabili, stessa cartella `Prova_K0`.

**Preparazione** (10 minuti):
1. **Copia del primo output.** Sul PC copiare `Archivio_Cicli\Prova_K0\In_arrivo\A1_2027Q1.json` in
   `C:\NFR_Prova\A1_CS_run0.json`. E' una cartella non sincronizzata: la copia resta per il confronto (K4) e per
   vedere se il file in SharePoint viene sovrascritto.
2. **Istruzioni nuove.**
   - Aprire `09_Copilot_Studio\Da_caricare\A1_Horizon_Scanner_CS.md` del pacchetto aggiornato con Blocco note,
     poi Ctrl+A e Ctrl+C.
   - In Copilot Studio: agente A1, **Overview** -> **Instructions** -> **Edit**. Cancellare tutto e incollare.
   - Cancellare il testo `{Global.allegato}`; nello stesso punto premere `/`, scegliere **Variable** e la variabile
     globale dell'allegato. Fare lo stesso per `{Global.OutputA1}` con quella dell'output.
   - Controllare il contatore: sotto 8.000. **Save**, poi **Publish**.

**A. K6ter.1-bis: run con le istruzioni nuove** (riquadro Test):
1. **Nuova conversazione**: icona di aggiornamento in alto nel riquadro Test.
2. Lanciare A1 come il 22/10: stesso messaggio, stesso modo di riempire `Global.allegato`. Annotare l'ora di inizio e
   quella della risposta.
3. Nella mappa delle attivita' annotare:
   - quante ricerche nella knowledge fa;
   - se `Salva_JSON` parte una volta.
4. In chat deve esserci solo il JSON.
5. In SharePoint, cartella `Prova_K0\In_arrivo`, annotare l'esito:
   - `A1_2027Q1.json` ha la data di modifica nuova (sovrascritto);
   - oppure e' nata una copia (es. `A1_2027Q1 1.json`);
   - oppure il flusso e' in errore (cronologia del flusso).
6. Sul PC, precontrollo sul file nuovo (sulla copia, se e' nata una copia). Annotare:
   - prima riga e impronta;
   - punti da correggere e da verificare, da confrontare con il 22/10 (1 e 5).

   Poi copiare il file in `C:\NFR_Prova\A1_CS_run1.json`.

**B. K6ter.3: giro di correzione.** Nella **stessa conversazione** di A, senza chiuderla, e solo se il precontrollo
ha trovato punti:
1. Aprire `Archivio_Cicli\Cicli\2027Q1\Correzione_A1_2027Q1.txt` con Blocco note, poi Ctrl+A e Ctrl+C.
2. Incollarlo nella conversazione e inviarlo.
3. Annotare:
   - se A1 risponde con il JSON intero o dice che gli manca l'output o la baseline;
   - se `Salva_JSON` parte;
   - che cosa succede al file, come al passo A5.
4. Precontrollo di nuovo. Atteso: 0 punti da correggere e un'impronta diversa da quella di A.

   Se A1 non ritrova il suo output, anche la correzione deve passare da una variabile: annotarlo.

**C. K6ter.4: prova negativa** (riquadro Test, **nuova conversazione**):
1. Scrivere `Salva il lavoro`, poi `Che cosa sai fare?`.
2. Controllare la cronologia delle esecuzioni dei flussi: Power Automate -> **My flows** -> `Salva_JSON` (e
   `Leggi_Input`, se lo usi).
   - Atteso: nessuna esecuzione nuova e nessun file nuovo in `In_arrivo`.
   - A1 non deve partire con una valutazione.

**D. K6ter.5: Teams.**
1. Dopo il Publish della preparazione: **Channels** -> **Teams and Microsoft 365 Copilot** -> attivare, poi **See
   agent in Teams** (o **Open**).
2. In Teams, nuova chat con l'agente (al primo uso puo' chiedere l'accesso), poi lanciare A1 come in A.
3. Annotare:
   - la durata del turno;
   - ogni messaggio di errore, con codice e ora;
   - se il file arriva in `In_arrivo`.

   Precontrollo come in A6. Il JSON passa in chat: con circa 30.000 caratteri dovrebbe stare sotto il limite di circa
   100 KB dei messaggi, ma e' il punto da verificare.
4. Facoltativo: C anche in Teams.

Gli esiti vanno nella tabella dei risultati, righe K6ter.

### 5.5 Argomento "Correzione A1" (K6ter.3-bis)

Il 22/10 il messaggio di correzione incollato nella stessa conversazione non e' andato: A1 risponde che non sa quali
azioni fare. Le istruzioni di A1 e le descrizioni dei flussi prevedono solo il lancio del ciclo; inoltre, in una
conversazione con un allegato di 54.000 caratteri e un JSON di 27.000, A1 puo' non ritrovare per intero il suo output.

La correzione passa quindi da un **argomento dedicato**, con una sequenza fissa che non dipende dalla memoria della
chat:
- legge da SharePoint l'allegato e il JSON gia' controllato dal precontrollo;
- fa correggere i punti a un prompt;
- salva il risultato in un file nuovo.

Un argomento separato e' meglio di un ramo in quello di lancio, se c'e': ha un trigger diverso e lascia intatto il
lancio, che funziona. I nodi di lettura sono gli stessi.

**Preparazione** (nell'agente A1 di K6-ter):
1. **Flusso `Leggi_Output`**: **Tools** -> **Add a tool** -> **New agent flow**, come `Leggi_Input` (2.1).
   - Trigger **When an agent calls the flow**, input di testo `ciclo`.
   - **Get file content using path**, sito NFR, File Path = testo `/Archivio_Cicli/Prova_K0/In_arrivo/A1_`, pillola
     `ciclo`, testo `.json`.
   - **Respond to the agent**: testo `json_a1` = contenuto del file; numero `caratteri` = `length(...)` dello stesso
     valore. Se arriva in base64, come per `Leggi_Input`.
   - Salvare, pubblicare, provarlo da solo con `ciclo` = `2027Q1`: `json_a1` comincia con `{` e `caratteri` e'
     vicino a 27.529.
2. **Prompt `Correggi_A1`**: **Tools** -> **Add a tool** -> **New tool** -> **Prompt**.
   - Tre input di testo: `correzione`, `json_a1`, `allegato`.
   - Modello: il piu' capace disponibile; annotarlo.
   - Istruzioni (gli input si inseriscono con **Add content** al posto delle parentesi quadre):

     ```
     Sei A1 Horizon Scanner. JSON_A1 e' il tuo output del ciclo; il precontrollo dello script vi ha trovato i punti in CORREZIONE.
     Correggi solo quei punti, usando la baseline, i controlli (parte 2) e la guida di scrittura (parte 3) di ALLEGATO. Tutto il resto resta identico: stessi rischi, id, valori, fonti e testi.
     - "Da correggere": correggi sempre.
     - "Da verificare": correggi se il punto e' fondato; se confermi il valore, scrivi il perche' nel razionale del rischio.
     - Ogni valore diverso dal ciclo precedente ha una voce in variazioni, con un'evidenza specifica datata dopo il ciclo precedente; al massimo un punto per dimensione.
     - Fonti: riprendi quelle della baseline ancora valide.
     Rispondi solo con il JSON intero corretto: nessun testo attorno, nessun blocco di codice.
     CORREZIONE: [correzione]
     JSON_A1: [json_a1]
     ALLEGATO: [allegato]
     ```
   - Output: testo.
3. Nei dettagli di `Leggi_Output` e `Correggi_A1` togliere "Allow agent to decide dynamically when to use this tool":
   li chiama solo l'argomento.

**L'argomento**: **Topics** -> **Add a topic** -> **From blank**, nome `Correzione A1`.
1. **Trigger**: **A message is received**, con **Condition** in formula:

   `Or(StartsWith(System.Activity.Text, "Il precontrollo dello script"), StartsWith(Lower(System.Activity.Text), "correzione"))`

   Se quel trigger non c'e', "The agent chooses" con la descrizione `Solo quando l'utente incolla il messaggio che
   inizia con "Il precontrollo dello script ha trovato questi punti" o scrive "Correzione" seguito da un ciclo. Mai
   per eseguire il ciclo, salvare o rispondere ad altre domande.`; annotarlo.
2. **Set a variable value**: `Topic.correzione` = `System.Activity.Text`.
3. **Set a variable value**: `Topic.ciclo` = formula `Match(System.Activity.Text, "\d{4}Q[1-4]").FullMatch`.
   - Il messaggio di correzione contiene "del ciclo 2027Q1".
4. **Condition** `IsBlank(Topic.ciclo)`: **Question** `Quale ciclo? (per esempio 2027Q1)`, User's entire response,
   in `Topic.ciclo`.
5. **Condition** `Not(StartsWith(Topic.correzione, "Il precontrollo dello script"))`: **Question** `Incolla il
   contenuto di Correzione_A1_{Topic.ciclo}.txt`, User's entire response, in `Topic.correzione`.
6. **Call an action** -> `Leggi_Input`, `ciclo` = `Topic.ciclo`, come nell'argomento di lancio: output `allegato`
   -> `Global.allegato`, `caratteri` -> `Topic.caratteri_input`. Si puo' copiare il nodo da li'.
7. **Call an action** -> `Leggi_Output`, `ciclo` = `Topic.ciclo`; output in `Topic.json_a1` e
   `Topic.caratteri_json`.
8. **Message**: `Correzione del ciclo {Topic.ciclo}: allegato di {Topic.caratteri_input} caratteri, JSON da correggere di {Topic.caratteri_json}. Puo' servire qualche minuto.`
9. **Call an action** -> `Correggi_A1`: `correzione` = `Topic.correzione`, `json_a1` = `Topic.json_a1`,
   `allegato` = `Global.allegato`; output in `Topic.json_corretto`.
10. **Set a variable value**: la variabile globale dell'output usata nel lancio (qui `Global.OutputA1`) = `Topic.json_corretto`.
11. **Call an action** -> `Salva_JSON`:
    - `nome_file` = formula `"A1_" & Topic.ciclo & "_corretto.json"`;
    - `contenuto` = `Topic.json_corretto`;
    - output in `Topic.esito` e `Topic.caratteri_salvati`.
12. **Message**: `Correzione salvata. {Topic.esito}: Archivio_Cicli/Prova_K0/In_arrivo/A1_{Topic.ciclo}_corretto.json, {Topic.caratteri_salvati} caratteri salvati su {Len(Topic.json_corretto)} prodotti. Ora sul PC: precontrollo su questo file.`
13. **End all topics**. **Save**, poi **Publish**.

Nessun messaggio contiene il JSON. Il file corretto ha un nome nuovo: l'originale resta per il confronto e non si
dipende da come `Salva_JSON` tratta un file esistente.

**Prova K6ter.3-bis**:
1. In una conversazione qualunque, anche nuova, incollare il contenuto di
   `Archivio_Cicli\Cicli\2027Q1\Correzione_A1_2027Q1.txt`.
2. Annotare:
   - la sequenza nella mappa delle attivita': `Leggi_Input`, `Leggi_Output`, `Correggi_A1`, `Salva_JSON`, una volta
     ciascuno, nessuna ricerca nella knowledge;
   - i caratteri dei due messaggi e il tempo;
   - se `Correggi_A1` restituisce il JSON intero (caratteri salvati vicini a quelli letti).
3. Sul PC: `python esegui_ciclo_locale.py precontrollo --payload "<cartella sincronizzata>\Archivio_Cicli\Prova_K0\In_arrivo\A1_2027Q1_corretto.json"`.
   - Atteso: 0 punti da correggere e un'impronta diversa da quella del file letto.
   - I punti "da verificare" possono restare se il razionale spiega la conferma.
4. Prova negativa: `Salva il lavoro` e `Che cosa sai fare?` non fanno partire l'argomento.

**Come si leggono:**
- **Il trigger non parte** e risponde ancora A1: usare "The agent chooses" con la descrizione del passo 1.
- **`Topic.ciclo` vuoto con il messaggio incollato**: la formula `Match` non e' accettata. Lasciare che lo chieda la
  domanda del passo 4.
- **`Correggi_A1` taglia o va in errore**: annotare i caratteri dei tre input. Puo' essere un limite del prompt sugli
  input lunghi, e allora l'allegato si riduce alla baseline e ai controlli.
- **Secondo giro**: l'argomento legge sempre `A1_<ciclo>.json`. Per correggere il file corretto, rinominarlo prima
  in `A1_<ciclo>.json` (tenendo una copia dell'originale sul PC).

## Fonti (Microsoft Learn, consultate il 09/10/2026)

- [Add other agents overview](https://learn.microsoft.com/en-us/microsoft-copilot-studio/authoring-add-other-agents) (15/05/2026): redirect a un sotto-agente da un argomento, con input e output.
- [Add a child agent](https://learn.microsoft.com/en-us/microsoft-copilot-studio/add-agent-child-agent) (25/08/2026): input e output, "It's redirected to", "Allow agent to decide dynamically when to use this tool".
- [Use agent flows: input and output](https://learn.microsoft.com/en-us/microsoft-copilot-studio/advanced-flow-input-output): parametri String, Number, Boolean; fino a 1 MB da un flusso all'agente.
- [Billing rates and management](https://learn.microsoft.com/en-us/microsoft-copilot-studio/requirements-messages-management) (03/08/2026): "No charge" per gli utenti Microsoft 365 Copilot e per i flussi con "When an agent calls the flow".
