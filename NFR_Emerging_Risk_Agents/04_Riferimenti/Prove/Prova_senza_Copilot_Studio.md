# Prova della versione senza Copilot Studio (Agent Builder e script sul PC)

Pacchetto del 06/10/2026. Si prova sul PC della Banca tutto cio' che e' cambiato dopo il giro del 01/10:
- la **griglia di validazione**, una riga per rischio, KRI, azione e notizia (D-67);
- le **schede con il perche' di ogni numero**, dal razionale di A1 diviso in parti (D-68);
- l'**allegato di A1** con i controlli di A5 e la guida di scrittura, e il **precontrollo** prima di A5 (D-69);
- l'**impronta** dell'output di A1 nel precontrollo, che serve anche alla prova di Copilot Studio (D-70);
- **A5 facoltativo** e la colonna **Segnalazioni dei controlli** nella griglia: il ciclo si ferma solo per
  difetti di integrita', il resto si decide in validazione (D-71).

Due parti:

| Parte | Dove | Tempo | Cosa tocca |
|---|---|---|---|
| 1. Installazione | il pacchetto e il registro veri | 20-30 minuti | aggiorna il registro vero alla struttura 2026-10-06 |
| 2. Ciclo di prova completo | una cartella a parte, `C:\NFR_Prova`, con un registro di prova nuovo | mezza giornata | **niente** del registro vero |

**Perche' un registro di prova, e perche' il 2026Q4.** Sul registro vero il 2026Q4 e' validato, quindi
il prossimo ciclo sarebbe il 2027Q1. Oggi pero' un ciclo 2027Q1 non si puo' fare davvero: ogni
variazione di punteggio vuole un'evidenza datata dopo il 31/12/2026 (controllo C3). Il registro di
prova riparte da zero con il 2026Q4, come il primo giro del 29/09, e si confronta direttamente con
quel giro: allora servirono 7-8 giri fra A1 e A5.

Il risultato di ogni passo va nella tabella in fondo. Gli stessi file della parte 2
(`Input_A1_2026Q4.txt` e l'output di A1) servono poi alla prova di Copilot Studio
(`09_Copilot_Studio/Prova_con_Copilot_Studio.md`).

## Parte 1. Installazione sul pacchetto e sul registro veri

### 1.1 Che cosa e' gia' installato (2 minuti)

| Cosa guardare | Come | Che cosa vuol dire |
|---|---|---|
| Registro | lo dice il passo 1.4 | "e' gia' sulla versione 2026-10-06" = gia' aggiornato |
| A1 in Agent Builder | Configura -> Istruzioni, cercare (Ctrl+F) `Allegato Input_A1` | trovato = istruzioni del 02/10 |
| A5 | cercare `I tuoi rilievi vanno al validatore` | trovato = istruzioni del 06/10 |
| A6 | cercare `il fenomeno in termini di rischio` | trovato = istruzioni del 02/10 |
| A4 | cercare `Baseline_corrente.txt in knowledge` | trovato = istruzioni del 01/10 |

Il pacchetto del 06/10 va estratto comunque: cambia lo script (D-71) e contiene
`07_Senza_Studio\precontrollo.py`, senza il quale lo script non parte.

### 1.2 Prima di estrarre

Se dal 01/10 in Banca avete modificato `tassonomia_nfr.md`, `rubrica_scoring.md`, `fonti.md` o
`DECISIONI.md`, mandate le modifiche a chi mantiene il pacchetto **prima** di estrarre: il pacchetto
le sovrascrive.

### 1.3 Estrarre e copiare il kernel

1. Estrarre `NFR_pacchetto_completo_2026-10-05.zip` **sopra la cartella del pacchetto** sul PC,
   sostituendo i file. `configurazione.json` non e' nello zip e resta com'e'.
2. Copiare **tutti gli 11 file di `01_Kernel`** e `04_Riferimenti\DECISIONI.md` nella cartella della
   library Kernel (la voce `kernel` di `configurazione.json`): lo script legge da li'.

### 1.4 Registro

**Chiudere** il registro (anche i colleghi), poi dalla cartella degli script:

```
python esegui_ciclo_locale.py aggiorna-registro
```

| Si vede | Vuol dire |
|---|---|
| `FERMATO ... e' gia' sulla versione 2026-10-06: niente da aggiornare.` | gia' fatto: il registro non e' stato toccato, si va avanti |
| `Registro aggiornato alla versione 2026-10-06 (era: ...)`, le righe copiate per tabella e `Registro vecchio conservato in: ...Backup\...` | fatto ora. Se c'erano righe da validare (per esempio le settimane del 28/09 e del 05/10), passano nella griglia nuova. Lo script stampa pesi e soglie di prima: reinserirli in Parametri solo se la Banca li aveva cambiati di proposito |

### 1.5 Agenti

Reincollare in Agent Builder le istruzioni degli agenti che al passo 1.1 **non** avevano la frase:
file interi di `02_Agenti` (`A1_Horizon_Scanner.md`, `A5_Challenger.md`, `A6_Schede.md`,
`A4_News_Assessor.md`), gia' pronti. Non serve `componi_prompt.py`. A3 non cambia. Archiviare il
testo incollato in `Archivio_Cicli\Prompt\<data>\`.

### 1.6 Baseline

```
python esegui_ciclo_locale.py baseline
```

Si deve vedere `Baseline scritta: ...Baseline_corrente.json` e `Allegato per A1:
...Input_A1_2027Q1.txt (baseline, controlli di A5 e guida di scrittura)`. Se compare "Avviso: nel
kernel ... mancano", il punto 2 del passo 1.3 e' incompleto. Poi copiare `Baseline_corrente.txt`
nella library Kernel (A3 e A4 la leggono).

### 1.7 Validare nella griglia nuova (lavoro vero, non prova)

Se il foglio Validazione del registro ha righe (per esempio le notizie delle settimane passate),
validarle come dice la guida, sezione 3:
- se si e' d'accordo, non toccare niente;
- per correggere, cambiare la cella gialla e scrivere la Motivazione;
- per scartare, Respingi = Si' e la Motivazione.

Poi, per ogni settimana:

```
python esegui_ciclo_locale.py valida --periodo 2026-09-28 --validatore "Comitato Rischi"
```

Si deve vedere `Validazione del periodo 2026-09-28 applicata: N righe — accettate ..., rettificate
..., respinte ...`.

## Parte 2. Ciclo di prova completo su un registro separato

Tutti i comandi di questa parte si lanciano **da `C:\NFR_Prova\pacchetto\07_Senza_Studio`**. Prima
di andare avanti, controllare che ogni percorso stampato dallo script cominci con `C:\NFR_Prova`. Se
compare il percorso del registro vero, ci si trova nella cartella sbagliata: fermarsi.

### 2.1 Preparare la cartella di prova (10 minuti)

1. Creare la cartella `C:\NFR_Prova` ed estrarre **lo stesso zip** in `C:\NFR_Prova\pacchetto`.
2. In `C:\NFR_Prova\pacchetto\07_Senza_Studio` copiare `configurazione_esempio.json` in
   `configurazione.json` e scriverci, con Blocco note:

   ```
   {
     "workbook": "C:\\NFR_Prova\\NFR_Registro_prova.xlsx",
     "kernel": "QUI LA RIGA kernel DEL configurazione.json VERO",
     "cartella_uscita": "C:\\NFR_Prova\\Archivio",
     "news_inbox": "C:\\NFR_Prova\\News_Inbox"
   }
   ```

   Per `kernel`, copiare il valore dal `configurazione.json` vero, con le barre doppie: la prova
   legge la stessa library Kernel e non ci scrive niente.
3. Aprire un **nuovo** Prompt dei comandi e scrivere `cd C:\NFR_Prova\pacchetto\07_Senza_Studio`.

### 2.2 Registro di prova e baseline

```
python esegui_ciclo_locale.py inizializza --ciclo-precedente 2026Q3 --settimana 2026-10-05
python esegui_ciclo_locale.py baseline
```

`--settimana` e' il lunedi' della settimana in corso: 2026-10-05, oppure 2026-10-12 se la prova si fa
la settimana dopo.

Si deve vedere:
- `Registro creato: C:\NFR_Prova\NFR_Registro_prova.xlsx` e "Senza dati di esempio";
- `Baseline scritta: C:\NFR_Prova\Archivio\Baseline_corrente.json`;
- `Allegato per A1: C:\NFR_Prova\Archivio\Input_A1_2026Q4.txt`, senza "Avviso".

La baseline di prova **non** va copiata nella library Kernel.

### 2.3 A1

1. In Agent Builder, agente **A1 Horizon Scanner**, **chat nuova**: allegare
   `C:\NFR_Prova\Archivio\Input_A1_2026Q4.txt` e scrivere `Esegui il ciclo`. Annotare l'ora di
   invio e quella della risposta.
2. Salvare la risposta (Blocco note, UTF-8) come `A1_2026Q4.json` in
   `C:\NFR_Prova\pacchetto\07_Senza_Studio`, e una copia come `A1_2026Q4_giro1.json`.

### 2.4 Precontrollo (facoltativo nell'uso normale, da fare in questa prova; pochi secondi, senza Excel)

```
python esegui_ciclo_locale.py precontrollo --payload A1_2026Q4.json
```

- La prima riga dice `nessun rilievo` oppure `N punti da correggere, M da verificare`.
- La seconda riga dice `Impronta dell'output di A1: ...`, 12 caratteri da annotare: servono alla
  prova di Copilot Studio.

Con punti da correggere:
1. aprire con Blocco note `C:\NFR_Prova\Archivio\Cicli\2026Q4\Correzione_A1_2026Q4.txt`;
2. copiarlo tutto nella chat di A1;
3. salvare la nuova risposta come `A1_2026Q4.json`;
4. ripetere il precontrollo.

Annotare quanti giri servono e i punti al primo giro. Con soli punti "da verificare" si puo' andare
avanti: in validazione diventano le segnalazioni della colonna Segnalazioni (D-71).

### 2.5 A5 (facoltativo dal 06/10, D-71; in questa prova farlo, per vedere i suoi rilievi in validazione)

Agente **A5 Challenger**:
1. allegare `A1_2026Q4.json` e `C:\NFR_Prova\Archivio\Baseline_corrente.json`;
2. scrivere `Esegui i nove controlli`;
3. salvare la risposta come `A5_2026Q4.json` nella stessa cartella.

### 2.6 Scrittura nel registro di prova

```
python esegui_ciclo_locale.py trimestrale --payload A1_2026Q4.json --challenger A5_2026Q4.json
```

Senza A5, lo stesso comando senza `--challenger A5_2026Q4.json`.

Si deve vedere `Ciclo 2026Q4 scritto: N/N rischi, zero errori di formula.`, `A5: usato` (o `non usato`), se
ce ne sono `SEGNALAZIONI DA MOTIVARE: N su M rischi`, e l'Excel di output in
`C:\NFR_Prova\Archivio\Cicli\2026Q4\`. Non deve comparire "Avviso per le schede: il razionale di ...
non e' diviso in parti"; se compare, in Agent Builder ci sono ancora le istruzioni vecchie di A1.

Se compare **FERMATO**, e' un difetto di integrita': seguire la guida, sezione 2, punto 8 (dare ad A1 il
messaggio `Correzione_A1_2026Q4.txt`, di nuovo `trimestrale`, e A5 se lo si usa), e contare i giri.

### 2.7 Validazione nella griglia

1. Aprire `C:\NFR_Prova\NFR_Registro_prova.xlsx`, foglio **Validazione**: una riga per rischio, KRI,
   azione.
2. Per provare la griglia:
   - leggere la colonna **Segnalazioni dei controlli** (ultima a destra dei rischi): per ogni rischio con
     ⚑ davanti al nome scrivere la Motivazione (anche se non si cambia nulla); un salto di piu' di un punto
     o soglie invertite proposte da A1 vanno corretti nella cella gialla;
   - cambiare **un** valore giallo di un rischio (per esempio l'Impatto) con la Motivazione, e
     guardare Score composito e Margine di Mosca ricalcolarsi in fondo alla riga;
   - mettere **Respingi = Si'** su un KRI, con la Motivazione;
   - lasciare tutto il resto com'e'.
3. Salvare e chiudere, poi:

   ```
   python esegui_ciclo_locale.py valida --periodo 2026Q4 --validatore "Prova"
   ```

   Si deve vedere `Validazione del periodo 2026Q4 applicata: N righe — accettate ..., rettificate ...,
   respinte 1.` (le rettifiche sono almeno una, piu' quelle chieste dalle segnalazioni). Se dice "NON
   applicata", l'elenco dice quale riga correggere.

### 2.8 Schede con A6 e report

```
python esegui_ciclo_locale.py schede-input
```

1. Agente **A6**: allegare SOLO `C:\NFR_Prova\Archivio\Cicli\2026Q4\Schede_input_2026Q4.json`,
   scrivere `Scrivi le schede`, salvare la risposta come `A6_2026Q4.json`.
2. Generare le schede:

   ```
   python esegui_ciclo_locale.py schede --payload A6_2026Q4.json
   python esegui_ciclo_locale.py report
   ```

3. Aprire `Schede_2026Q4.xlsx`. Ogni scheda deve avere:
   - il Razionale (causa, evento, danno per la Banca);
   - accanto a Impatto, Probabilita, Prossimita e Velocity, il perche' del valore con i documenti;
   - per azioni e KRI, "Perche'" ed "Effetto atteso".
4. Il PDF del report e' in `C:\NFR_Prova\Archivio\Cicli\2026Q4\Report_comitato_2026Q4.pdf`.

### 2.9 Alla fine

- Tenere `C:\NFR_Prova` fino alla fine della prova di Copilot Studio, che usa
  `Archivio\Input_A1_2026Q4.txt`, `A1_2026Q4.json` e l'impronta annotata al passo 2.4.
- Da mandare a chi mantiene il pacchetto: la tabella qui sotto compilata. Se le regole della Banca
  lo consentono, anche:
  - `A1_2026Q4_giro1.json` e `A1_2026Q4.json`;
  - i file `Correzione_A1_2026Q4.txt`;
  - `A5_2026Q4.json` e `Schede_2026Q4.xlsx`.
- Dopo, `C:\NFR_Prova` si puo' cancellare: il registro vero non ne dipende.

## Tabella dei risultati

| Passo | Verifica | Atteso | Esito e note |
|---|---|---|---|
| 1.4 | aggiorna-registro | "gia' sulla versione 2026-10-06" oppure "Registro aggiornato ..." | |
| 1.5 | agenti reincollati | quali | |
| 1.6 | baseline e allegato | `Input_A1_2027Q1.txt`, nessun avviso | |
| 1.7 | validazione delle settimane nella griglia | "Validazione del periodo ... applicata" | |
| 2.2 | registro di prova e allegato | `Input_A1_2026Q4.txt` in `C:\NFR_Prova\Archivio` | |
| 2.3 | A1: tempo di risposta, numero di rischi, solo JSON | | |
| 2.4 | precontrollo: punti al primo giro (da correggere / da verificare), giri fino a zero punti da correggere, impronta finale | meno dei 7-8 giri del 29/09 | |
| 2.5 | A5 (facoltativo): esito e numero di rilievi bloccanti | i suoi rilievi non fermano: vanno in validazione | |
| 2.6 | trimestrale: scritto al primo colpo? giri A1 totali; quante segnalazioni da motivare | un giro | |
| 2.7 | griglia: una riga per oggetto, colonna Segnalazioni leggibile e utile per decidere, ⚑ sui rischi giusti, Score e Margine che cambiano, valida con le rettifiche e 1 respinto | | |
| 2.8 | schede: le parti del razionale e l'effetto atteso ci sono; report PDF | | |
| — | testi di A1: descrizioni e motivazioni piu' ragionate di quelle del 29/09? | giudizio dell'analista | |
