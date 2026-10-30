# Guida passo passo — per chi usa il sistema, senza conoscerne l'interno

Questa guida dice **cosa fare, in che ordine, cosa scrivere e cosa si deve
vedere**. Non serve capire come funziona dentro. Se un passo non da' il
risultato descritto, **fermarsi** e guardare la sezione 7 ("Se qualcosa va
storto"): il sistema e' fatto per fermarsi prima di sbagliare, non dopo.

Vale per la variante senza Copilot Studio: agenti in Microsoft 365 Copilot
(Agent Builder) e uno script sul PC. Contiene anche l'**avvio del progetto**
(decisioni, collaudo sul primo ciclo, cancelli e tempi: sezione "Avvio del
progetto", che dal 07/10/2026 sostituisce il vecchio piano di deploy) e la
configurazione iniziale del tenant (sezione 0); dettaglio tecnico in
`07_Senza_Studio/README_variante_locale.md`.

## Le parole che servono

| Parola | Significato |
|---|---|
| **Registro** | il file Excel `NFR_Registro.xlsx`: contiene tutto, cresce a ogni ciclo. |
| **Ciclo** | un trimestre, scritto cosi': `2026Q3` (anno, Q, numero del trimestre). |
| **Settimana** | indicata dal suo lunedi', scritto cosi': `2026-10-12`. |
| **Agente** | un assistente di Copilot: A1 (valuta i rischi ogni trimestre), A5 (controlla A1, facoltativo), A6 (scrive i testi delle schede dei rischi, dopo la validazione), A3 (legge le notizie ogni settimana), A4 (pareri su richiesta), A7 (risponde in chat sul perche' delle valutazioni, D-72). |
| **Schede** | il file `Schede_<ciclo>.xlsx`, a parte rispetto al registro: una scheda per rischio (contenuto nella sezione 4). |
| **Script** | il programma sul PC che scrive nel registro: `esegui_ciclo_locale.py` e `raccogli_notizie.py`. |
| **Baseline** | il file `Baseline_corrente.json` (e la sua copia `.txt`): la fotografia del registro che si da' agli agenti. |
| **Allegato** (D-84) | il file che si trascina nella chat di un agente; si chiama sempre `Input_<agente>`: `Input_A1_<ciclo>.txt` (A1: baseline, controlli, guida di scrittura), `Input_A8_<periodo>.txt` (A8, straordinario: lo stesso con il blocco dello straordinario), `Input_A3_A4.txt` (A3 e A4: la baseline), `Input_A5_<ciclo>.txt` (A5: l'output di A1 e la baseline, scritto dal precontrollo), `Input_A6_<ciclo>.json` (A6: i dati validati, in `Cicli\<ciclo>\`). Gli altri stanno nella cartella di uscita, accanto alla baseline. L'app li prepara da sola. |
| **Allegato di A1** | il file `Input_A1_<ciclo>.txt`, accanto alla baseline: baseline, controlli di A5 e guida di scrittura in un file solo. Lo scrive lo script ogni volta che aggiorna la baseline; si allega ad A1 (D-69). |
| **Validare** | accettare, correggere ("rettificare") o respingere le proposte degli agenti. Lo fa una persona. |

## Python: a cosa serve e cosa devi sapere

**Gli agenti non usano Python.** Vivono in Microsoft 365 Copilot: si aprono,
si scrive una richiesta, rispondono. Pero' non possono scrivere in Excel ne'
salvare file. Python fa questo lavoro: e' un programma sul tuo PC che prende
le risposte degli agenti, le **controlla**, le **scrive** nel registro Excel
e ne **archivia** una copia. Senza Python le risposte degli agenti restano
nella chat e andrebbero ricopiate a mano, senza nessun controllo.

### L'app NFR: il modo piu' semplice (dal 23/10/2026, D-83)

Dal 23/10/2026 i comandi Python si lanciano anche da una finestra: doppio clic su **`NFR.cmd`** nella cartella degli
script. L'app mostra a che punto e' il lavoro, propone il prossimo passo e guida ogni processo, agenti compresi:
**sezione "L'app NFR: uso passo per passo"**, qui sotto dopo "In breve". La configurazione che le serve (link degli
agenti, validatore, ecc.) e' nella sezione 0.3. I comandi scritti a mano, descritti nelle sezioni 1-3 e 9, restano
validi e fanno esattamente le stesse cose: l'app lancia gli stessi.

### Cosa lanci tu, e quando

Solo due programmi, sempre dal Prompt dei comandi, dalla cartella degli script:
`raccogli_notizie.py` (le notizie del lunedi') ed `esegui_ciclo_locale.py`
(tutto il resto, un comando per ogni azione: `baseline`, `trimestrale`,
`settimanale`, `valida`...). Quale passo usa quale comando: "In breve: i cicli
standard", qui sotto. Ogni comando con parametri, opzioni, file che scrive ed
errori tipici: **sezione 9**.

Nella stessa cartella ci sono altri file `.py` (`excel_com.py`,
`controlli_a5.py`, `valida_output.py`, `fonti.py`, `input_a1.py`, `precontrollo.py`,
`schede.py`, `spiegazioni.py`, `diagnosi.py`): **non si lanciano**, li usano i due programmi. Non spostarli e non rinominarli.

Nel pacchetto ci sono anche programmi che **tu non usi**: `componi_prompt.py`
(rigenera il testo dei prompt quando cambiano le regole), `genera_dashboard.py`
(rigenera il template Excel), la cartella `99_Collaudo` (verifica che una
modifica non abbia rotto niente). Li usa solo chi mantiene il pacchetto.

### Cosa fa sempre, prima di scrivere

Ogni volta che scrive nel registro, lo script:
1. controlla che la risposta dell'agente abbia il formato giusto e rispetti le
   regole (se no si ferma con **FERMATO** e il registro non viene toccato);
2. fa una copia di sicurezza del registro in `Archivio_Cicli\Backup\`;
3. scrive, ricalcola Excel e controlla che non ci siano errori;
4. salva e mette una copia con nome proprio nell'archivio.

Excel si apre e si chiude da solo, invisibile: non va aperto a mano. Anzi,
**il registro deve essere chiuso** mentre lo script lavora.

### Come si scrive un comando (per chi non l'ha mai fatto)

1. Menu Start, scrivere `cmd`, aprire **Prompt dei comandi**.
2. Andare nella cartella degli script: scrivere `cd` e il percorso fra
   virgolette, poi Invio. Esempio:
   `cd "C:\Users\nome\NFR\07_Senza_Studio"`. Suggerimento: in Esplora file
   si puo' copiare il percorso dalla barra degli indirizzi.
3. Scrivere il comando, per esempio `python esegui_ciclo_locale.py baseline`, e
   premere Invio. Aspettare che ricompaia la riga con il percorso: i comandi
   che scrivono nel registro impiegano uno-due minuti (Excel si apre e
   ricalcola tutto, invisibile).
4. I nomi di file con spazi vanno fra virgolette. I file degli agenti conviene
   salvarli nella cartella degli script, cosi' basta scriverne il nome.
5. Il tasto Freccia su richiama l'ultimo comando: utile per rilanciarlo.

Cosa fa ciascun agente e che cosa gli si puo' scrivere (messaggio base e variazioni): sezione 8.

Per sapere se il comando e' andato bene basta leggere l'ultima riga: il testo
atteso e' scritto nelle tabelle delle sezioni 1, 2 e 3. **FERMATO** vuol dire
che lo script ha trovato un problema e non ha toccato niente; **ERRORE
TECNICO** vuol dire un problema del PC (sezione 7).

### Raccolta notizie automatica ogni lunedi' (una volta sola)

Sul PC della raccolta la pianifica `installa.cmd` (sezione 0.3, punto 3), come attivita' **NFR raccolta notizie**.
A mano, se le regole del PC non lo permettono a `installa.cmd`:

1. Menu Start, aprire **Utilita' di pianificazione**, poi *Crea attivita' di base*.
2. Nome: `Raccolta notizie NFR`. Attivazione: *Settimanale*, lunedi', ore 7:00.
3. Azione: *Avvio programma*. Programma: `python`. Argomenti:
   `raccogli_notizie.py`. *Inizio in*: il percorso della cartella degli script
   (senza virgolette).
4. Il lunedi' successivo controllare che in `News_Inbox\<lunedi'>\` ci sia il
   file `Raccolta_<data>.txt`.

La raccolta normale scarica solo le fonti con `stato: approvata` in
`fonti.md` (al 24/09 tutte tranne FNT-19, esclusa: `04_Riferimenti/DECISIONI.md`).
Una fonte nuova, ancora "da validare", si prova con
`python raccogli_notizie.py --anche-da-validare`.

## In breve: i cicli standard

Un promemoria per chi conosce gia' il sistema: un passo per riga. I dettagli,
cio' che si deve vedere e cosa fare se qualcosa non torna sono nelle sezioni
indicate; per i messaggi d'errore la sezione 7, per cosa scrivere agli agenti la
sezione 8. Tutti i comandi si lanciano dalla cartella degli script, con il
registro chiuso.

**Ogni lunedi'** (sezione 1)

| # | Passo | In una riga |
|---|---|---|
| 1 | `python raccogli_notizie.py` (di solito automatico alle 7) | scarica le notizie delle fonti in `News_Inbox\<lunedi'>\` |
| 2 | file in `News_Inbox\<lunedi'>\Manuali\` | aggiungi a mano cio' che non arriva dai feed |
| 3 | A3: allega `Input_A3_A4.txt` (cartella di uscita), "Esegui l'aggiornamento settimanale" | valuta le notizie; salva la risposta come `A3_<lunedi'>.json` |
| 4 | `python esegui_ciclo_locale.py settimanale --payload A3_<lunedi'>.json` | scrive le notizie nel registro |
| 5 | facoltativo: griglia del foglio Validazione, poi `python esegui_ciclo_locale.py valida --periodo <lunedi'> --validatore "..."` | conferma o corregge le notizie (sezione 3) |

**Ogni trimestre** (sezione 2)

| # | Passo | In una riga |
|---|---|---|
| 1 | Registro, riga 4: "Ciclo validato" | il trimestre prima deve essere validato |
| 2 | `python esegui_ciclo_locale.py baseline` | prepara la baseline e gli allegati degli agenti: `Input_A1_<ciclo>.txt` per A1, `Input_A3_A4.txt` per A3 e A4 (dal 23/10/2026 non serve piu' copiare la baseline nella library Kernel) |
| 4 | A1: allega `Input_A1_<ciclo>.txt`, "Esegui il ciclo" | valuta i rischi; salva come `A1_<ciclo>.json` |
| 5 | **facoltativi, si possono saltare**: `python esegui_ciclo_locale.py precontrollo --payload A1_<ciclo>.json` e A5 | controllano A1 prima di scrivere (sezione 2, punti 5-bis e 6) |
| 6 | `python esegui_ciclo_locale.py trimestrale --payload A1_<ciclo>.json` (con `--challenger A5_<ciclo>.json` se hai usato A5) | scrive il ciclo; se FERMATO, dai ad A1 il messaggio `Correzione_A1_<ciclo>.txt` (sezione 2, punto 8) |
| 7 | griglia del foglio Validazione, poi `python esegui_ciclo_locale.py valida --periodo <ciclo> --validatore "..."` | il validatore decide le proposte (anche lo stato dei rischi: radar o osservazione) e motiva le segnalazioni ⚑ (sezione 3) |
| 8 | `python esegui_ciclo_locale.py schede-input`, A6 "Scrivi le schede", `python esegui_ciclo_locale.py schede --payload A6_<ciclo>.json` | schede dei rischi (sezione 2, punti 11-12) |
| 9 | `python esegui_ciclo_locale.py report` | PDF del report al comitato: lo fa gia' `valida` del passo 7; rilanciarlo dopo modifiche a mano (sezione 2, punto 13) |

**Quando serve**

| Passo | In una riga | Dettagli |
|---|---|---|
| A7: domande in chat | il perche' di valori, urgenza, livello, temi non censiti, rischi in osservazione; "sintesi per il Quadro" da incollare nelle Note dell'analista | sezioni 4 e 8 |
| A4: la notizia in chat | parere su una notizia, senza numeri nuovi | sezione 8 |
| Celle gialle del registro (presidio, anni di adeguamento, supervisore, stato delle azioni, Note dell'analista) | modifiche a mano ammesse; poi `python esegui_ciclo_locale.py report` per il PDF | sezione 6 |
| `python esegui_ciclo_locale.py riapri`, griglia del foglio Validazione, `valida` | cambia valori di un ciclo gia' validato (punteggi, decisione sullo stato, KRI, owner e orizzonte delle azioni), quante volte serve | sezione 3-ter |
| Testi delle tabelle dati (descrizioni, razionali, segnali di avvicinamento, nomi e note di KRI e azioni), poi `python esegui_ciclo_locale.py baseline` | correggerne la forma a mano | sezione 3-ter |
| Ciclo straordinario: `python esegui_ciclo_locale.py baseline --straordinario [--rischi NFR-nn] --motivo "..." --decisore "..."`, A8 "Esegui il ciclo straordinario" con i documenti dell'evento, `precontrollo` (facoltativo), `trimestrale`, `valida` | rivaluta subito i rischi toccati da un evento critico o censisce quelli nuovi che crea (proposto da A3 o A4, o di tua iniziativa) | sezione 2-bis |
| `python esegui_ciclo_locale.py dismetti --rischio NFR-nn --motivazione "..." --decisore "..."` | toglie un rischio dal registro, la storia resta | sezione 3-bis |
| `python esegui_ciclo_locale.py griglia` | ricostruisce il foglio Validazione rovinato a mano | sezione 3 |
| `python esegui_ciclo_locale.py diagnosi` | dopo la validazione, ogni tanto: i rischi nuovi entrano tutti bassi? il validatore alza (o abbassa) sempre le stesse dimensioni? ci sono rischi lontani con Impatto alto senza anni di adeguamento? Solo lettura | sezione 9 |
| `python esegui_ciclo_locale.py aggiorna-registro` | porta il registro su un template nuovo, dopo un aggiornamento del pacchetto | sezione 0-bis |

## L'app NFR: uso passo per passo

**A che cosa serve.** Fa da regista: sa a che punto e' il lavoro, prepara i file per gli agenti, raccoglie le loro
risposte, lancia i comandi nell'ordine giusto e mostra l'esito. **Non decide niente**: i controlli e la scrittura nel
registro restano allo script (gli stessi comandi della sezione 9), le decisioni al validatore.

**Avvio.** Doppio clic sul collegamento **NFR Horizon Scan** del Desktop (lo crea `installa.cmd`), o su `NFR.cmd` nella
cartella degli script, `07_Senza_Studio`. Prima volta: `installa.cmd` (sezione 0.3), che chiede cartelle e link degli
agenti. Se la finestra non si apre: sezione 7.

### La finestra, dall'alto in basso

| Parte | Che cosa dice o fa |
|---|---|
| **Stato** (due righe) | il ciclo corrente (scritto, DA VALIDARE, VALIDATO, RIAPERTO; report e schede pronti o da fare), il prossimo periodo, la settimana (raccolta, A3, scritta, validata), il registro (libero o in uso da chi). Si aggiorna da solo ogni mezzo minuto; e' lo stesso per tutti i colleghi, perche' si legge dall'archivio condiviso |
| **▶ Prossimo passo** | il passo che lo stato propone, con chi lo deve fare (analista o validatore) e perche'. Un clic e parte |
| **Pulsanti dei processi** | Settimana, Trimestre, Straordinario, Validazione, Schede, Report, Riapri un ciclo, Parere di A4, Chiedi ad A7, Diagnosi, Dismetti (i testi a mano sono in **Admin**) |
| **Con A5 Challenger** | casella: il trimestre e lo straordinario passano anche da A5 (facoltativo, D-71). Se non e' spuntata, l'app lo chiede comunque a precontrollo superato, prima di scrivere il ciclo (`chiedi_a5`, sezione 0.3) |
| **Agenti** | Agent Builder o Copilot Studio: da quale versione degli agenti vengono le risposte. Cambiano solo il link aperto e l'annotazione dell'origine; nomi dei file, cartelle e registro sono gli stessi |
| **Altro** | apri il registro (solo consultazione), apri l'archivio, aggiorna lo stato, **Verifica del PC**, togli il lucchetto rimasto, ricostruisci la griglia di validazione (sezione "Menu Altro") |
| **Passo in corso** | le istruzioni del passo, il **riquadro "Risposta dell'agente"** dove incollare (Ctrl+V; il testo resta visibile e un nuovo Ctrl+V lo sostituisce), sotto la **riga dell'esito** (in verde "Ricevuto: A1, … caratteri, salvato in In_arrivo\\A1_<ciclo>.json", in arancio una risposta tagliata, di un altro agente o fuori formato), e i pulsanti Usa il testo incollato, Leggi gli appunti adesso, Scegli file..., Ho chiuso Excel: controlla ora, Annulla il passo. Il passo in corso dice sempre che cosa sta facendo l'app: "Esecuzione del comando trimestrale in corso da 1:25 (Excel in background, di solito qualche minuto)", "In attesa della risposta di A1", "In attesa che tu chiuda il registro in Excel", "In attesa della tua risposta alla domanda: ..." |
| **Admin...** | pulsante accanto ad Altro: apre la finestra delle funzioni amministrative (nuovo registro, pulizia dell'archivio, ritorno a un ciclo validato, annullamento, ripartenza da zero, parcheggi, svuotamento), ognuna spiegata e con il suo pulsante (sezione "Pulsante Admin", D-85). Aprirla chiede conferma e lascia la traccia; finche' e' aperta il titolo della finestra dice ADMIN |
| **Aiuto (F1)** | una finestra con un argomento per pulsante dell'app (le sezioni "Pulsante ..." di questo capitolo), piu' leggere i risultati e dove sono i file, e il pulsante per aprire la guida completa. Passando con il mouse su un pulsante (anche Prossimo passo, la casella A5, Agenti, Altro) compare che cosa fa, con le righe della tabella "I processi" qui sotto. L'aiuto legge questa guida: non c'e' una copia da tenere allineata |
| **Divisore** | fra il passo in corso e l'uscita dei comandi: si trascina per dare piu' spazio all'una o all'altra |
| **Fascia dell'esito e uscita** | mentre un processo lavora, in blu il processo e la fase ("In corso: Trimestre - comando precontrollo in esecuzione"); poi l'esito dell'ultimo comando (verde OK, arancio FERMATO, rosso ERRORE TECNICO) e l'uscita dei comandi riga per riga. Ogni comando lascia un log in `Archivio_Cicli\Log\` |

Su uno schermo 1920x1080 (o piu' piccolo) la finestra si apre a tutto schermo, anche con la scala di Windows al 150%.

### Lavorare con un agente: i tuoi tre gesti

Per ogni agente l'app:
1. prepara i file da allegare in `%USERPROFILE%\NFR_Da_allegare\<agente>\` e apre la cartella;
2. apre l'agente, se in `configurazione.json` c'e' il suo link (sezione 0.2, punto 3-bis);
3. mette negli appunti il messaggio base (sezione 8), per esempio "Esegui il ciclo".

Poi tocca a te:
1. **chat nuova** con l'agente, **trascini** i file della cartella nella chat, **incolli** il messaggio (Ctrl+V) e invii;
2. quando l'agente ha finito **copi la risposta** (pulsante Copia sotto la risposta) e la **incolli nel riquadro
   "Risposta dell'agente"** dell'app (Ctrl+V). Appena incolli, l'app la prende; se no, "Usa il testo incollato".

In piu', se l'ascolto degli appunti e' acceso (`ascolta_appunti`, sezione 0.3), basta premere Copia: l'app se ne
accorge da sola. Una risposta salvata in un file si prende con "Scegli file...".

L'app estrae il JSON anche con frasi prima e dopo, i segni di codice ```json o i link alle fonti in coda, riconosce
l'agente dal formato, controlla il formato e salva il file con il nome giusto in `Archivio_Cicli\In_arrivo\`
(`A1_<ciclo>.json`, `A3_<lunedi'>.json`, `A5_<ciclo>.json`, `A6_<ciclo>.json`, `A8_<periodo>.json`; il parere di A4 in
`Archivio_Cicli\Pareri\`). Il testo incollato resta in `In_arrivo\Originali\` (con l'origine, Agent Builder o
Copilot Studio, nel nome); un file con lo stesso nome passa in `In_arrivo\Precedenti\`: niente si perde.

Casi particolari:
- **Risposta tagliata** (l'agente si ferma a meta'): l'app mette "continua" negli appunti; lo incolli nella **stessa
  chat** e incolli nell'app il resto della risposta. Le parti si uniscono da sole.
- **Correzione**: se il precontrollo o lo script trovano qualcosa da correggere, il messaggio di correzione e' gia'
  negli appunti. Lo incolli nella **stessa chat** dell'agente e incolli nell'app la risposta nuova.
- **Risposta di un altro agente** (per esempio A3 mentre il passo aspetta A1): l'app la salva ma il passo non avanza,
  e lo dice.

### I processi

Ogni pulsante fa un processo intero: l'app lancia da sola, nell'ordine giusto, quello che serve; tu fai solo i gesti
della colonna di destra. Passando con il mouse su un pulsante compare la sua riga di questa tabella.

| Pulsante | Che cosa fa l'app | Che cosa fai tu |
|---|---|---|
| **Settimana** | raccoglie le notizie se mancano (solo sul PC della raccolta); apre la cartella Manuali della settimana; prepara A3 con il suo allegato; scrive la settimana nel registro; se A3 va corretto mette il messaggio negli appunti; propone di validare le notizie | metti in Manuali i file a mano; i tre gesti con A3; decidi se validare |
| **Trimestre** | controlla che il ciclo prima sia validato; prepara l'allegato di A1; controlla la risposta di A1 (pochi secondi, senza Excel) e, se serve, prepara il messaggio di correzione per la stessa chat; propone A5 se la casella non e' spuntata; scrive il ciclo nel registro; propone la validazione | i tre gesti con A1 (e A5); se il controllo trova solo punti "da verificare", scegli se farli rivedere ad A1 o lasciarli al validatore; se trova testi troppo corti (C10), scegli se farli allungare ad A1 (consigliato) o proseguire |
| **Straordinario** | chiede rischi, motivo, chi decide e data; prepara l'allegato di A8; controlla la risposta; scrive il ciclo straordinario; propone la validazione | compili il modulo (decide la funzione di rischio); allega ad A8 anche i documenti dell'evento |
| **Validazione** | chiede chi valida; apre il registro in Excel sul foglio Validazione; quando lo chiudi applica le decisioni e rifa' il report al comitato (PDF e HTML). Se qualcosa non va, lo dice e propone di riaprire il registro; poi propone le schede | lavori nelle celle gialle del foglio Validazione, salvi e chiudi Excel |
| **Schede** | prepara i dati validati; chiede se usare A6 per i testi; fa le schede dei rischi (Excel e PDF) e il report se manca; apre la cartella del ciclo | i tre gesti con A6, se lo usi |
| **Report** | rifa' il report al comitato (PDF e, se i numeri tornano con Excel, HTML) e apre la cartella del ciclo | niente; serve dopo una correzione a mano delle celle gialle del registro |
| **Riapri un ciclo** | chiede quali rischi riaprire (vuoto = tutti); riapre la validazione del ciclo; poi la Validazione | come nella validazione |
| **Parere di A4** | prepara A4 con il suo allegato; archivia il parere; se A4 propone uno straordinario, lo dice | incolli la notizia dopo il messaggio base; copi e incolli il parere |
| **Chiedi ad A7** | apre A7 | fai le tue domande in chat |
| **Diagnosi** | misura se le valutazioni pendono da una parte (solo lettura) e scrive l'esito nell'uscita e nella cartella del ciclo | leggi le misure |
| **Dismetti** | chiede rischio, motivazione e chi decide; toglie il rischio dal registro attivo (la storia resta) | compili il modulo (decide la funzione di rischio) |

### I pulsanti del passo in corso

Mentre un processo aspetta una risposta di un agente o la chiusura di Excel, nel riquadro "Passo in corso" si accendono
questi pulsanti (gli altri restano grigi):

| Pulsante | Quando si usa |
|---|---|
| **Usa il testo incollato** | se dopo aver incollato la risposta nel riquadro (Ctrl+V) l'app non l'ha presa da sola |
| **Leggi gli appunti adesso** | se hai premuto Copia sotto la risposta dell'agente e l'app non se n'e' accorta |
| **Scegli file...** | se la risposta dell'agente e' salvata in un file (.json o .txt) |
| **Ho chiuso Excel: controlla ora** | quando hai chiuso il registro e l'app e' ancora "in attesa che tu chiuda Excel" |
| **Annulla il passo** | per fermare il processo senza danni; si riprende con Prossimo passo |

### Pulsante Prossimo passo

Il pulsante grande in alto dice che cosa c'e' da fare adesso, chi lo deve fare e perche' (per esempio "Validare il
ciclo 2026Q3", "Settimana del 26/10: A3", "Report al comitato del ciclo 2026Q3"). Premerlo fa partire quel processo,
come il pulsante del processo corrispondente. Se un collega sta scrivendo nel registro dice "Attendere".

### Pulsante Settimana

Ogni lunedi', per le notizie della settimana.

1. Premi **Settimana** (o **Prossimo passo**, se lo propone).
2. Sul PC della raccolta l'app raccoglie le notizie, se non l'ha gia' fatto l'attivita' del lunedi'. Poi apre la
   cartella **Manuali** della settimana: mettici i file che non arrivano dai feed (circolari, rapporti) e rispondi Si'.
   Si possono mettere anche durante la settimana: tasto destro sul file -> **Invia a -> NFR notizie manuali**.
3. I tre gesti con **A3**: chat nuova, trascini l'allegato, incolli il messaggio, poi copi la risposta nell'app.
4. L'app scrive la settimana. Se si ferma, il messaggio di correzione per A3 e' negli appunti: incollalo nella stessa
   chat e ricopia la risposta.
5. Alla domanda "Validare adesso le notizie?" puoi rispondere No: e' facoltativo (poi lo propone **Prossimo passo**).

### Pulsante Trimestre

Dopo la fine del trimestre, per il ciclo trimestrale.

1. Premi **Trimestre** (o **Prossimo passo**, che lo propone dopo la fine del trimestre). Il ciclo prima deve essere
   validato.
2. Se vuoi il parere di **A5**, spunta "Con A5 Challenger" prima di premere; se non la spunti, l'app te lo chiede dopo
   il controllo della risposta di A1.
3. I tre gesti con **A1**. L'app controlla la risposta in pochi secondi: se trova errori mette negli appunti il
   messaggio di correzione, che incolli nella **stessa chat** di A1; poi ricopi la risposta. Si ripete finche' il
   controllo e' superato. Se A1 e' stato **troppo sintetico** (testi sotto le lunghezze minime, controllo C10), l'app
   chiede se farglieli allungare: Si' (consigliato) mette negli appunti il messaggio per la stessa chat; No prosegue,
   e in validazione quei testi restano osservazioni.
4. Con A5: i tre gesti con A5, con il suo allegato.
5. L'app scrive il ciclo nel registro (Excel lavora in background per qualche minuto: il passo in corso dice da quanto).
6. Alla domanda "Passare alla validazione adesso?": Si' per validare subito (come il pulsante **Validazione**), No per
   farlo dopo.

### Pulsante Validazione

Per validare il ciclo scritto (il validatore).

1. Premi **Validazione** (o **Prossimo passo**). Scrivi chi valida e **Conferma**.
2. Si apre il registro sul foglio **Validazione**: una riga per rischio, KRI, azione e notizia. Lavora solo nelle
   **celle gialle**:
   - lasciare il valore proposto = accettare;
   - scrivere un valore diverso = rettificare, con la **Motivazione** (almeno 10 caratteri);
   - **Respingi** = Si' per una proposta da non applicare;
   - le righe con **⚑** hanno una segnalazione dei controlli: chiedono sempre la Motivazione, anche se accetti.
3. **Salva e chiudi Excel**. L'app se ne accorge da sola; se resta in attesa premi **Ho chiuso Excel: controlla ora**.
4. Se la validazione non passa, l'uscita dice quali righe sistemare e l'app propone di riaprire il registro.
5. A validazione riuscita il report al comitato (PDF e HTML) si rifa' da solo; poi l'app propone le schede (come il
   pulsante **Schede**).

I criteri per decidere sono nella sezione 3 di questa guida. La validazione delle notizie della settimana la propone
**Prossimo passo** dopo la settimana.

### Pulsante Straordinario

Solo su decisione della funzione di rischio, per un evento che non puo' aspettare il trimestre (per esempio quando A3
o A4 lo propongono).

1. Premi **Straordinario** e compila il modulo: i rischi da rivalutare (vuoto = solo rischi nuovi creati
   dall'evento), il motivo, chi decide, la data di riferimento (vuota = oggi).
2. I tre gesti con **A8**: oltre all'allegato, trascina nella chat anche i documenti dell'evento.
3. Come nel trimestre: controllo, correzioni nella stessa chat, A5 se vuoi, scrittura, poi la validazione.

### Pulsante Schede

Dopo la validazione (l'app le propone alla fine di **Validazione**). L'app chiede se usare **A6**: con A6 i testi delle
schede sono piu' estesi (i tre gesti con A6), senza l'app usa i testi di A1 dal registro. Se A6 e' stato **troppo
sintetico** (testi sotto le lunghezze minime), le schede sono gia' scritte e l'app chiede se farglieli allungare: Si'
(consigliato) mette negli appunti l'elenco per la stessa chat e rifa' le schede con la nuova risposta; No le tiene come
sono. Le schede (Excel e PDF) sono nella cartella del ciclo, che l'app apre; se il report al comitato manca, lo fa.

### Pulsante Report

Il report al comitato si rifa' da solo dopo ogni validazione: **Report** serve dopo una correzione a mano delle celle
gialle del registro (presidio, anni di adeguamento, attenzione del supervisore, stato delle azioni). Escono il PDF e
l'HTML, nella cartella del ciclo che l'app apre: l'HTML si apre con un doppio clic e ha le schede di tutti i rischi. Se
l'uscita dice che l'HTML non e' uscito, il PDF c'e' lo stesso e il messaggio va a chi mantiene il pacchetto.

### Pulsante Riapri un ciclo

Per cambiare un valore gia' validato (un punteggio, una soglia, l'owner di un'azione). Scrivi i rischi da riaprire
(vuoto = tutti) e **Conferma**; poi l'app passa alla validazione, come **Validazione**. Il ciclo dopo aspetta finche'
la riapertura non e' validata. Per correggere solo la forma di un testo, senza cambiare valori: **Admin** -> **Testi a
mano**, a riapertura validata.

### Pulsante Parere di A4

Per il parere su una notizia singola. I tre gesti con **A4**: dopo il messaggio base incolla la notizia (testo o
link). Il parere si archivia; se A4 propone un ciclo straordinario l'app lo dice (decide la funzione di rischio; poi
**Straordinario**).

### Pulsante Chiedi ad A7

Apre A7, che spiega in chat il perche' delle valutazioni (valori, urgenza, livello di allerta, decisioni del
validatore), in prima persona, come chi le ha proposte. Non scrive niente nel registro.

### Pulsante Diagnosi

Dopo una validazione, per vedere se le valutazioni pendono da una parte (con quali valori entrano i rischi nuovi, in
che verso il validatore corregge, i rischi lontani). Solo lettura: l'esito e' nell'uscita e nella cartella del ciclo.

### Pulsante Dismetti

Compila rischio (NFR-nn), motivazione e chi decide e **Conferma**: il rischio esce dal registro attivo e dai prossimi
cicli, i suoi KRI escono di vigore, le azioni aperte si annullano; la storia resta. Solo su decisione della funzione
di rischio. Non cancellare mai a mano una riga dell'anagrafica.

### Pulsante Admin

Apre la finestra delle **funzioni amministrative**. Aprirla chiede conferma e lascia la traccia di chi l'ha aperta e
quando; finche' e' aperta il titolo della finestra principale dice ADMIN; chiuderla spegne la modalita' Admin. Nella
finestra ogni operazione ha la sua spiegazione e il suo pulsante; il modulo che si apre propone le scelte possibili
(per esempio i cicli validati a cui si puo' tornare, i parcheggi da rimettere a posto).

| Operazione | A che cosa serve | Che cosa chiede |
|---|---|---|
| **Nuovo registro** | il primo registro, vuoto, quando non ce n'e' ancora uno (primo uso, o un ambiente di prova) | il trimestre prima del primo da valutare (per esempio 2025Q4 per cominciare dal 2026Q1) e il lunedi' della settimana corrente del registro |
| **Testi a mano** | corregge la forma dei testi di un ciclo validato (descrizioni, razionali, nomi e note dei KRI, descrizioni delle azioni), senza cambiare valori: prima una copia del registro va nel parcheggio con l'atto, poi si apre il registro; quando lo chiudi l'app rifa' l'allegato di A1, la knowledge di A7 e il report. Si annulla con **Annulla** finche' nessuno scrive nel registro. Con una riapertura aperta o un ciclo da validare non apre Excel: propone prima la Validazione | che cosa correggi e perche'; poi correggi in Excel SOLO le colonne di testo, salvi e chiudi |
| **Pulizia** | toglie dall'archivio cio' che non serve piu': tentativi e versioni vecchie dei report dei cicli validati, backup oltre gli ultimi 10, risposte incollate dei periodi chiusi, log vecchi | niente: mostra prima l'elenco e lo spazio, poi chiede se spostarli nel parcheggio |
| **Ritorno** | torna a un ciclo validato: il registro torna com'era alla sua validazione; i cicli dopo e le settimane scritte dopo vanno nel parcheggio, e l'app riparte da quel ciclo | il ciclo (fra quelli validati prima del corrente), il motivo, chi ha deciso e il ciclo riscritto per conferma |
| **Annulla** | rimette a posto un parcheggio; un ritorno, una ripartenza o dei testi a mano solo se nel frattempo nessuno ha scritto nel registro | il parcheggio (dall'elenco) e il motivo |
| **Ripartenza** | registro nuovo vuoto; il vecchio e tutto l'archivio dei cicli nel parcheggio (per esempio dopo i cicli di prova, per ricominciare da inizio anno) | il motivo, chi ha deciso, il trimestre prima del primo da valutare, il lunedi' della settimana corrente e il nome del registro riscritto per conferma |
| **Parcheggi** | l'elenco dei parcheggi: operazione, quando, chi, quanto spazio, stato | niente |
| **Svuota** | cancella per sempre i parcheggi piu' vecchi di 30 giorni | niente: mostra prima l'elenco, poi chiede conferma |

Niente si cancella subito, tranne con **Svuota**: tutto va nel parcheggio con l'atto e si puo' annullare. **Ritorno** e
**Ripartenza** cambiano la storia del registro: solo su decisione della funzione di rischio (sezione 3-quater).
Per provare piu' giri di cicli da inizio anno, in un ambiente di prova: **Ripartenza** (o **Nuovo registro**) con il
trimestre 2025Q4, i cicli con **Trimestre** e **Validazione**, poi di nuovo **Ripartenza**, oppure **Ritorno** a un
ciclo per rifare solo quelli dopo.

### Menu Altro

| Voce | A che cosa serve |
|---|---|
| **Apri il registro (sola consultazione)** | per guardare il registro; non cambia niente |
| **Apri l'archivio** | la cartella Archivio_Cicli |
| **Aggiorna lo stato** | rilegge subito a che punto e' il lavoro (lo fa da sola ogni mezzo minuto) |
| **Verifica del PC** | una riga per voce (Python, moduli, cartelle, registro ed Excel, collegamenti, attivita' della raccolta) con OK, ATTENZIONE o NO e che cosa fare; il file resta nell'archivio, da mandare a chi mantiene il pacchetto se qualcosa e' NO |
| **Togli il lucchetto rimasto (sblocca)** | solo se l'app dice "Il registro e' in uso" da parte di un collega che non sta lavorando (PC spento a meta' lavoro); sentirlo prima. Il lucchetto scade comunque dopo 2 ore |
| **Ricostruisci la griglia di validazione** | solo se il foglio Validazione e' stato rovinato a mano e la validazione non passa per questo |

### Pulsante Aiuto (F1)

Questa guida dentro l'app: a sinistra un argomento per pulsante, a destra il testo. **Apri la guida completa** apre
tutto il documento, anche le parti per chi mantiene il pacchetto. Passando con il mouse su un pulsante della finestra
principale compare che cosa fa.

### Interrompere, riprendere, se l'app si ferma

**Domande e moduli.** Quando l'app chiede qualcosa (per esempio "Ciclo ... scritto. Passare alla validazione adesso?" o
chi valida) la finestra viene in primo piano con un suono, e il passo in corso riporta la domanda: finche' non rispondi
i pulsanti dei processi restano grigi. **Registro aperto**: l'app si accorge da sola che hai chiuso Excel; se dopo la
chiusura e' ancora in attesa, premi "Ho chiuso Excel: controlla ora" (se il file risulta ancora aperto lo dice e
aspetta).

**Interrompere e riprendere.** "Annulla il passo" (o la chiusura della finestra) ferma il processo senza danni: il
registro si scrive solo alla fine dei controlli. Al riavvio, il "Prossimo passo" riparte dal punto giusto; se la
risposta di un agente e' gia' stata presa, l'app chiede se usarla invece di richiederla.

**Risposta tagliata** (l'agente si ferma a meta'): l'app mette "continua" negli appunti; incollalo nella stessa chat e
copia il resto della risposta: le parti si uniscono da sole.

**Piu' analisti.** Mentre un collega scrive nel registro, lo stato dice "Registro: in uso da ..." e il prossimo passo
e' "Attendere": riprova quando ha finito.

**La fascia dell'esito.** Verde OK; **arancio FERMATO**: il registro non e' stato toccato, il motivo e che cosa fare sono
nell'uscita (spesso un messaggio di correzione per l'agente e' gia' negli appunti); **rossa ERRORE TECNICO**: un problema
del PC o di Excel (per esempio Excel aperto): chiudere Excel e riprovare; se si ripete, mandare il log
(`Archivio_Cicli\Log\`) a chi mantiene il pacchetto. I messaggi piu' frequenti sono nella sezione 7.

## Avvio del progetto (responsabile, funzioni di controllo, manutentore — una volta)

Dal via al primo ciclo in esercizio: **dieci fasi** (0-9). Ogni fase ha i suoi
passi con chi li fa; le fasi 0, 1, 6, 7 e 8 si chiudono con un **cancello**: non
si passa alla fase dopo senza il si' della persona indicata, scritto in
`04_Riferimenti/DECISIONI.md`. I passi tecniche dell'installazione (fasi 2-6) sono
nella sezione 0. Riguarda la soluzione cosi' com'e' nel pacchetto (Agent Builder
e script locale, senza Copilot Studio ne' Power Automate); dal 05/10/2026 ci sono
anche due prove fuori dalle fasi: `04_Riferimenti/Prove/Prova_senza_Copilot_Studio.md` (la
versione corrente su un registro separato) e
`09_Copilot_Studio/Prova_con_Copilot_Studio.md` (D-70).

**Ruoli**

| Ruolo | Chi (da nominare) | Cosa fa |
|---|---|---|
| **Responsabile del progetto** | funzione di rischio | decide, presiede i cancelli, tiene `DECISIONI.md` |
| **Manutentore del pacchetto** | una persona con Python (IT o funzione di rischio) | adatta il kernel, rigenera prompt e template, lancia il collaudo |
| **Analista** | 1-2 persone della funzione di rischio | usa il sistema ogni settimana e ogni trimestre (sezioni 1-4) |
| **Validatore** | funzione di rischio o comitato | valida ogni ciclo (sezione 3) |
| **IT / postazioni** | informatica | Python e pywin32 sul PC, proxy, Utilita' di pianificazione |
| **Amministratore SharePoint / M365** | informatica | sito, library, permessi; verifica che Agent Builder sia attivo |
| **Compliance, model risk, DPO** | funzioni di controllo | qualificazione, trattamento dei dati in Agent Builder, licenze delle fonti |

**Fase 0 — Decisioni e autorizzazioni** (2-6 settimane, dipende dalle funzioni di controllo). Sapere se si puo' fare e con quali regole, prima di configurare qualunque cosa.

| # | Chi | Passo |
|---|---|---|
| 0.1 | Responsabile | Tenere `DECISIONI.md` (nel pacchetto in `04_Riferimenti/`; da caricare nella library `Kernel`): ogni decisione con data, chi l'ha presa, perche'. |
| 0.2 | Amministratore M365 | Agent Builder attivo per il tenant e per gli utenti del progetto; licenza Microsoft 365 Copilot ad analisti e validatore. |
| 0.3 | Compliance, DPO | Parere sul trattamento: dati interni (audit, incidenti) come knowledge di agenti Agent Builder, elaborati da servizi Copilot Studio, senza chiavi gestite dal cliente (`04_Riferimenti/controlli_e_model_risk.md`, sezione 6). |
| 0.4 | Model risk | Decidere se l'output e' un modello ai sensi della policy (`04_Riferimenti/controlli_e_model_risk.md`, sezione 1) e con quali requisiti di convalida. |
| 0.5 | Responsabile | Il registro **alimenta** o **affianca** il processo di rischio operativo esistente? |
| 0.6 | Responsabile | Nominare validatore, analisti, manutentore; decidere se la validazione delle notizie settimanali e' obbligatoria (oggi facoltativa). |
| 0.7 | IT | Python e pywin32 installabili sul PC dell'analista; il proxy lascia raggiungere i feed RSS (o si rinuncia alla raccolta automatica). |
| 0.8 | Responsabile | Fissare in `DECISIONI.md` i **criteri di accettazione del primo ciclo** (fase 7): riproducibilita' minima fra due run di A1, quota massima di rettifiche del validatore. **Non serve un trimestre gia' valutato a mano**: il registro parte vuoto. |

**Cancello G0** — Responsabile, con compliance e model risk: pareri positivi (anche con condizioni) in `DECISIONI.md`. Senza G0 non si configura niente nel tenant.

**Fase 1 — Kernel della Banca** (1-2 settimane, in parallelo alla fine della fase 0). Regole, scale e fonti della Banca, non i segnaposto del pacchetto. Come si cambia ogni file: sezione 6.

| # | Chi | Passo |
|---|---|---|
| 1.1 | Responsabile + manutentore | Rivedere `01_Kernel/tassonomia_nfr.md`: categorie (dal 07/10 le nove in perimetro della tassonomia interna, D-74) e driver. |
| 1.2 | Responsabile | Descrittori di `01_Kernel/rubrica_scoring.md` (Impatto, Probabilita, Prossimita, Velocity, rilevanza delle fonti) nel linguaggio della Banca (prima revisione: D-61); regole di variazione. Il presidio dei controlli e' un giudizio della Banca nell'anagrafica (D-49). |
| 1.3 | Responsabile | Pesi del composito (D-50: Impatto 0,35, Probabilita 0,25, Prossimita 0,20, Velocity 0,20), soglia di direzione (2), soglia del Delta (0,30, D-61), parametri dell'urgenza (X = 0,25 anni, Y di riserva 1 anno, anni per livello di Prossimita, D-59). Si scrivono poi nel foglio Parametri del registro (sezione 0.4). |
| 1.4 | Responsabile + compliance | Validare `01_Kernel/fonti.md`: `stato` approvata o esclusa, licenza d'uso, i **4 siti** con `sito_agente: si` (fatto il 24/09: D-15, D-16, D-27..D-29). |
| 1.5 | Manutentore | `python 02_Agenti/componi_prompt.py`: ogni prompt sotto 8.000 caratteri. |
| 1.6 | Manutentore | Se sono cambiati categorie o driver: `python 03_Excel/genera_dashboard.py`. |
| 1.7 | Manutentore | `python 99_Collaudo/esegui_collaudo.py`: **tutto OK** (circa 40 minuti con la catena in tre processi; serve Excel desktop; `--mirato` salta la catena se non e' cambiato niente che la riguardi). Un KO dice quale file allineare. |

**Cancello G1** — Responsabile: "rubrica, tassonomia e fonti sono quelle della Banca", collaudo tutto OK, in `DECISIONI.md`.

**Fasi 2-6 — Installazione** (3-4 giorni, piu' due settimane di rodaggio della raccolta notizie): i passi sono nella sezione 0.

| Fase | Cosa | Dove |
|---|---|---|
| 2 Postazione dell'analista | Python, pywin32, pypac, openpyxl, Excel; script in una cartella locale; prova di rete | sezione 0.3 |
| 3 SharePoint | sito, sette library, controllo versione, permessi; `Kernel` caricato; sottocartelle di `Analisi_Interne`; sincronizzazione e `configurazione.json` | sezioni 0.1, 0.2 (punto 2), 0.3 |
| 4 Registro vivo | `inizializza`, Parametri compilati, baseline (mai un registro creato a mano dal template) | sezione 0.4 |
| 5 Raccolta notizie | raccolta pianificata il lunedi'; `Manuali`; dopo due settimane le fonti "non raggiungibili" o senza notizie si correggono in `fonti.md` (e si ricarica A3) | "Raccolta notizie automatica ogni lunedi'", sezione 1 |
| 6 Agenti | creazione degli agenti (in Agent Builder o in Copilot Studio), capability spente, link degli agenti per l'app, istruzioni archiviate, prova di fumo | sezioni 0.2 e 0.2-bis |

**Cancello G2** — Manutentore: gli agenti rispondono nel formato atteso (prova di fumo della sezione 0.2).

**Fase 7 — Collaudo sul primo ciclo, da registro vuoto** (2-3 settimane). Misurare, **prima** di usarlo sul serio, se l'analisi di A1 e' stabile (due run danno lo stesso quadro) e accettabile per il validatore. Tutto su una **copia** del registro, mai su quello vivo; il metro sono il doppio run e la validazione umana.

| # | Chi | Passo |
|---|---|---|
| 7.1 | Manutentore | Copia di prova vuota: `python esegui_ciclo_locale.py --workbook <cartella_prova>\NFR_Prova.xlsx --cartella-uscita <cartella_prova>\Uscita inizializza --ciclo-precedente <trimestre prima del primo da valutare> --settimana <lunedi'>`. Tutti i comandi di questa fase usano le stesse due opzioni. |
| 7.2 | Analista | Mettere in `Analisi_Interne`, `Analisi_Esterne` e `News_Inbox` i documenti disponibili oggi. |
| 7.3 | Analista | Baseline della copia (senza rischi); A1 con `Input_A1_<ciclo>.txt` della cartella di uscita della copia: `A1_run1.json`; **rifare A1** sullo stesso input: `A1_run2.json`. |
| 7.4 | Manutentore | `python 99_Collaudo/confronta.py A1_run1.json A1_run2.json --primo-ciclo`: i rischi si abbinano per categoria e nome; quanti rischi in entrambi, quanti punteggi identici (controllare a occhio gli abbinamenti). |
| 7.5 | Responsabile + analista | Leggere `A1_run1.json`: i rischi coprono le aree che la funzione conosce? Motivazioni e fonti verificabili? Confronto con i **sette rischi di riferimento** (tabella sotto, D-37): trovati? se no, perche'? Annotare in `DECISIONI.md` (osservazione, non criterio). |
| 7.6 | Analista | `precontrollo --payload A1_run1.json` (facoltativo nell'uso normale; qui serve a contare i giri) e, se scrive il messaggio di correzione, darlo ad A1 finche' non resta niente che fermi (annotare i giri); A5 se lo si usa; `trimestrale` sulla copia. Obiettivo: un giro. |
| 7.7 | Validatore | Validare il ciclo di prova sulla copia (sezione 3); annotare il tempo, la quota di rettifiche e i rischi che non avrebbe voluto nel registro. |
| 7.8 | Analista | Una settimana di prova: A3 sulla raccolta reale, `settimanale` sulla copia, validazione delle notizie. |
| 7.9 | Responsabile | Se i criteri di 0.8 non sono raggiunti: rivedere descrittori o istruzioni (fase 1), ricomporre e ricaricare i prompt, ripetere 7.3-7.7. |

Sette rischi di riferimento (passo 7.5, D-37): da un Horizon Scanning fatto a mano con Copilot M365 e i report ORX (`Analisi_Architettura/Archivio/08`); **non si danno ad A1** (un'analisi a cui si dice cosa trovare lo conferma).

| Rischio dell'esempio | Categoria (D-74) | Driver | Nota |
|---|---|---|---|
| R1 AI agentica, identita' non umane | 9.7 Sicurezza informatica | DRV-AI, DRV-CYB | se il danno e' un'indisponibilita' dei sistemi: secondo rischio 9.6 |
| R2 Attacco ai modelli AI, data poisoning | 9.7 Sicurezza informatica | DRV-AI, DRV-CYB | il degrado non doloso (drift) e' un altro rischio, 9.13 o 9.6 |
| R3 Frodi con AI, deepfake | fuori perimetro (frode) | DRV-AI, DRV-CYB | la tassonomia interna mette la frode fuori dal perimetro dell'agente: fenomeno non censito |
| R4 Terze parti, concentrazione cloud | 9.9 Terze parti | DRV-TPR, DRV-CYB | |
| R5 Quantum / PQC | 9.7 Sicurezza informatica | DRV-CYB, DRV-TEC | caso tipico di anni di adeguamento (D-33) o di rischio in osservazione (D-79) |
| R6 Frammentazione normativa e sanzioni | 9.4 Legale | DRV-GEO, DRV-CON | serve un meccanismo di perdita legale; il financial crime e' fuori perimetro |
| R7 Competenze, eccessivo affidamento sull'AI | 9.11 Employer o 9.13 Processo | DRV-HUM, DRV-AI | |

Mancano 9.1, 9.5 e 9.8 e prevalgono i rischi tecnologici: e' il confronto atteso. A1 non deve coprire tutte le categorie (D-55); una categoria senza rischi resta visibile (sintesi di A1, "AREA NON PRESIDIATA"). Nel doppio run si guarda anche che meccanismi diversi restino rischi separati.

**Cancello G3** — Responsabile e model risk: criteri di 0.8 raggiunti, validatore d'accordo che la validazione e' praticabile. Esito in `DECISIONI.md`.

**Fase 8 — Primo ciclo reale, in parallelo al processo attuale** (un trimestre)

| # | Chi | Passo |
|---|---|---|
| 8.1 | Analisti | Ogni lunedi': sezione 1. |
| 8.2 | Analisti | A fine trimestre: sezione 2 (il primo ciclo propone tutti i rischi come "Nuovi"). |
| 8.3 | Validatore | Sezione 3. |
| 8.4 | Analista | Archiviare i prompt in uso; schede con A6 (sezione 2, punti 11-12); leggerle prima del comitato (nessun nome di persona, testi coerenti con i dati). |
| 8.5 | Responsabile | Confrontare registro e report con il processo attuale dello stesso trimestre; portare al comitato le differenze con il primo report (PDF da Quadro a Metodologia e file delle schede, con i limiti dichiarati di `04_Riferimenti/controlli_e_model_risk.md`, sezione 5). |

**Cancello G4 (finale)** — Responsabile, model risk, compliance: via all'esercizio (strumento ufficiale o affiancamento, come deciso in 0.5).

**Fase 9 — Esercizio e manutenzione** (continua)

| Cadenza | Chi | Cosa |
|---|---|---|
| Ogni lunedi' | analista | sezione 1; controllare le fonti non raggiungibili in testa alla raccolta |
| Ogni trimestre | analista, validatore | sezioni 2 e 3; archiviare i prompt in uso |
| A ogni "ATTENZIONE: l'anagrafica ha N posti liberi" | manutentore | template con `MAX_RISCHI` piu' alto (oggi 20) e le capacita' collegate, versione nuova della struttura, `aggiorna-registro` (sezione 0-bis); oltre i 20-25 rischi verificare la lunghezza delle risposte di A1, A5 e A6 |
| Quando un rischio non va piu' seguito | responsabile, analista | `dismetti` (sezione 3-bis) |
| Ogni modifica a rubrica, tassonomia, fonti | manutentore | sezione 6 e procedura "Se cambia il kernel" di `00_LEGGIMI.md` |
| Ogni anno | responsabile, compliance | revisione dell'elenco fonti e delle licenze, e della quota di rettifiche (validazione "di facciata"?) |
| A ogni aggiornamento di Agent Builder | manutentore | rileggere i limiti (8.000 caratteri, knowledge, tipi di file) in `07_Senza_Studio/README_variante_locale.md` |

**Cancelli e tempi**

| Cancello | Dopo la fase | Chi dice si' | Su cosa | Durata della fase |
|---|---|---|---|---|
| G0 | 0 | responsabile, compliance, model risk | si puo' fare, con quali regole | 2-6 settimane |
| G1 | 1 | responsabile | kernel e fonti della Banca, collaudo tutto OK | 1-2 settimane |
| G2 | 6 | manutentore | gli agenti rispondono nel formato atteso | 2-6: 3-4 giorni (5: due settimane in parallelo) |
| G3 | 7 | responsabile, model risk | primo ciclo riproducibile e accettabile; validazione praticabile | 2-3 settimane |
| G4 | 8 | responsabile, model risk, compliance | via all'esercizio | un trimestre |

Dal via (G0) al primo ciclo in parallelo: circa **6-10 settimane**; esercizio pieno dopo il trimestre in parallelo.

**Checklist prima del G4**: `DECISIONI.md` con G0-G3 firmati; kernel della Banca, `fonti.md` validato, prompt ricomposti, caricati e archiviati; collaudo tutto OK sull'ultima versione; registro creato con `inizializza`, Parametri compilati, baseline corretta; raccolta notizie pianificata e funzionante da due settimane; doppio run documentato; un ciclo di prova validato sulla copia con il tempo di validazione; backup verificati (un ripristino di prova da `Backup\`); guida consegnata ad analisti e validatore.

## 0. Prima installazione (una volta sola)

Percorso tecnico completo, dal tenant vuoto al primo ciclo pronto da
eseguire, **nell'ordine in cui va fatto**: prima l'amministratore (0.1), poi
chi mantiene il pacchetto (0.2), poi ogni analista sul proprio PC (0.3), poi
la creazione del registro (0.4). Chi segue solo la propria parte puo' andare
diretto alla sua sezione, ma i passi prima della propria vanno gia' fatti da
altri.

Questa e' la parte tecnica delle fasi 2-6 dell'avvio del progetto (sezione
precedente, con i pareri, il collaudo sul primo ciclo, i cancelli G0-G4 e i
tempi): qui i comandi e gli esiti attesi, una sola volta.

### 0.1 Amministratore SharePoint / M365 (prima di tutto il resto)

1. Verificare che **Agent Builder** sia attivo per il tenant e per gli utenti
   del progetto, e che la licenza Microsoft 365 Copilot sia assegnata ad
   analisti e validatore.
2. Creare il sito SharePoint (es. `NFR-Emerging-Risk`) con le **sette library**
   di `04_Riferimenti/struttura_e_liste.md`: `Kernel`, `Analisi_Interne`,
   `Analisi_Esterne`, `News_Inbox`, `Report_Trimestrali`, `Report_Settimanali`,
   `Archivio_Cicli` (`Report_Settimanali` in questa variante resta vuota e si
   puo' non creare: l'output della settimana va in `Archivio_Cicli\Settimane`,
   la sintesi di A3 nel foglio Sintesi_Settimane del registro).
   `Analisi_Interne` e `Analisi_Esterne` sono separate apposta
   (D-45): solo documenti della Banca su se stessa nella prima, solo materiale
   di terzi (report di settore, database di perdite di consorzio come ORX)
   nella seconda. A1 fa corrispondere `fonti[].tipo` alla cartella di
   provenienza ("Interna" per `Analisi_Interne`, "Esterna" per
   `Analisi_Esterne`): un documento di terzi finito per errore in
   `Analisi_Interne` verrebbe etichettato "Interna", quindi va spostato.
   (Le tre liste di quel documento non servono in questa variante senza
   Copilot Studio.)
3. Attivare il **controllo versione** su tutte le library. Permessi: `Kernel`
   e `Archivio_Cicli` in sola lettura per chi non e' manutentore o analista;
   il sito visibile solo al gruppo della funzione di rischio.

4. (analisti) Creare in `Analisi_Interne` le sottocartelle indicate dagli
   indirizzi delle fonti `share` di `01_Kernel/fonti.md` e caricarvi i documenti
   interni recenti (audit, incidenti, report di funzione); in `Analisi_Esterne`
   i report di settore e di consorzio.

**Verifica**: le sette library esistono nel sito, ciascuna con il controllo
versione attivo.

### 0.2 Manutentore del pacchetto (dopo 0.1, prima che un analista arrivi a 0.3)

1. Se non gia' fatto, adattare il kernel alla Banca: `01_Kernel/tassonomia_nfr.md`,
   `01_Kernel/rubrica_scoring.md`, `01_Kernel/fonti.md` (sezione 6 piu' sotto,
   "Cambiare le regole"). Poi `python 02_Agenti/componi_prompt.py` e, se e'
   cambiata la tassonomia, `python 03_Excel/genera_dashboard.py`.
2. Caricare nella library `Kernel`: i file di `01_Kernel/` e `DECISIONI.md`. Servono
   allo script, che li legge da li'; non si aggiungono come knowledge degli agenti
   (vedi sotto). La baseline non va nella library: gli agenti la ricevono come
   allegato (`Input_A1`, `Input_A3_A4`, `Input_A8`; AU7, D-84).
3. Creare gli **agenti** in Agent Builder (A1, A3, A4, A5 facoltativo, A6, A7) (rimando per il "perche'" — limiti di Agent Builder, fonti verificate su Microsoft Learn, capacita' che evolvono in fretta: `07_Senza_Studio/README_variante_locale.md`; qui solo i passi):
   Microsoft 365 Copilot ->
   Nuovo agente -> **"Passa a Configura"** (configurazione manuale, NON la
   descrizione in linguaggio naturale, che riscriverebbe le istruzioni). Per
   ciascuno, incollare **il file intero** delle istruzioni nel campo
   Istruzioni — mai i file di `02_Agenti/modelli/`, che contengono ancora i
   segnaposto `{{TASSONOMIA}}` / `{{RUBRICA:...}}` non risolti:

   | Agente | Istruzioni (file intero) | Modalita' | Capability | Condivisione |
   |---|---|---|---|---|
   | A1 Horizon Scanner | `02_Agenti/A1_Horizon_Scanner.md` | Think deeper | nessuna (spegnere entrambe) | analisti |
   | A3 Interim Update | `02_Agenti/A3_Interim_Update.md` | Auto | nessuna | analisti |
   | A4 News Assessor | `02_Agenti/A4_News_Assessor.md` | Auto | nessuna | gruppo della funzione di rischio |
   | A5 Challenger (facoltativo, D-71) | `02_Agenti/A5_Challenger.md` | Think deeper | nessuna | analisti |
   | A6 Schede dei rischi | `02_Agenti/A6_Schede.md` | Think deeper | nessuna | chi prepara il report al comitato |
   | A7 Assistente del registro | `02_Agenti/A7_Assistente_registro.md` | Think deeper | nessuna | gruppo della funzione di rischio |
   | A8 Evento critico (D-77) | `02_Agenti/A8_Evento_critico.md` | Think deeper | nessuna | analisti |

   **Perche' questa modalita'** (non e' una decisione registrata in
   `DECISIONI.md`: e' il ragionamento su cosa fa ciascun agente — se non
   convince, e' una modalita' che si cambia con un clic, senza toccare
   istruzioni o knowledge):
   - **A1 — Think deeper**: valuta TUTTI i rischi in anagrafica insieme, su
     quattro dimensioni e gli anni di adeguamento ciascuno, confrontando due cicli precedenti e
     rispettando regole di variazione rigide (max un punto, evidenza datata
     specifica). E' il compito con piu' vincoli incrociati da tenere insieme:
     quello dove un ragionamento superficiale produce piu' facilmente un
     errore che A5 poi deve fermare.
   - **A3 — Auto**: per ogni notizia della settimana, un compito
     classificatorio ripetuto (intensita' 0-3 su nove categorie fisse,
     direzione fra quattro valori). Un tempo di risposta prevedibile conta, e il
     compito non ha il ragionamento multi-vincolo di A1.
   - **A4 — Auto**: valuta UNA notizia alla volta, su richiesta, con una
     struttura di risposta fissa. Meno superficie di errore di A1: non tocca
     punteggi, non confronta cicli, non deve tenere coerenti piu' rischi
     insieme.
   - **A5 — Think deeper**: deve far passare l'output di A1 attraverso dieci
     controlli indipendenti (C1-C10), alcuni sottili (C4 plausibilita', C6
     deriva sistematica su piu' rischi), e puo' **fermare il ciclo**: un
     controllo superficiale vanificherebbe il suo scopo di contrappeso
     indipendente.
   - **A6 — Think deeper**: scrive testi estesi (1000-2000 caratteri la
     descrizione, 400-800 per ogni valore; D-88) dove ogni numero citato deve stare esattamente nei dati
     validati, senza liberta' creativa sui valori. Lo script comunque
     respinge un numero o una fonte alterati (`schede.controlla_a6`), ma un
     ragionamento piu' attento riduce i giri di correzione avanti e indietro.
   - **A8 — Think deeper**: legge per intero i documenti di un evento, ne
     ricostruisce la catena causale e rivaluta o censisce rischi con le stesse
     regole di A1: e' il compito piu' profondo, su pochi rischi.

   **Knowledge esatta per agente** — Configura -> Knowledge -> Add knowledge
   source. Per una cartella SharePoint: SharePoint/OneDrive -> selezionare
   la **cartella intera** (non i singoli file). Per un file: stesso percorso
   ma selezionare il **singolo file**. Per un sito: "Web site" e incollare
   l'URL (semplice, senza parametri, max due livelli).

   | Agente | Cartelle SharePoint (intere) | File singolo | Siti web esterni |
   |---|---|---|---|
   | A1 Horizon Scanner | `Analisi_Interne`, `Analisi_Esterne`, `News_Inbox` | — | i 4 sotto |
   | A3 Interim Update | `Analisi_Interne`, `Analisi_Esterne`, `News_Inbox` (la baseline arriva in chat: allegato `Input_A3_A4.txt`) | — | i 4 sotto |
   | A4 News Assessor | — (la baseline arriva in chat: allegato `Input_A3_A4.txt`) | — | nessuno |
   | A5 Challenger | **nessuna** (riceve solo l'allegato `Input_A5_<ciclo>.txt` in chat: output di A1 e baseline) | — | nessuno |
   | A6 Schede dei rischi | **nessuna** (riceve solo l'allegato `Input_A6_<ciclo>.json` in chat) | — | nessuno |
   | A7 Assistente del registro | `Kernel/Spiegazioni` (la cartella intera: la scrive lo script), `Analisi_Interne`, `Analisi_Esterne`, `News_Inbox` | — | nessuno |
   | A8 Evento critico | `Analisi_Interne`, `Analisi_Esterne`, `News_Inbox` (i documenti dell'evento si allegano in chat) | — | i 4 sotto |

   I **4 siti web** (gli unici con `sito_agente: si` in `01_Kernel/fonti.md`,
   uguali per A1, A3 e A8), da aggiungere uno per uno come "Web site":
   - FNT-20 Banca d'Italia, vigilanza — `https://www.bancaditalia.it/compiti/vigilanza`
   - FNT-21 CONSOB — `https://www.consob.it`
   - FNT-22 Garante per la protezione dei dati personali — `https://www.garanteprivacy.it`
   - FNT-23 Protezione Civile, rischi e allerte — `https://www.protezionecivile.gov.it/it`

   Lasciare **spento** "Search all websites": l'agente citerebbe fonti fuori
   elenco, che lo script poi rifiuta in scrittura.

   Il kernel (tassonomia, rubrica, elenco fonti) e' gia' dentro le
   Istruzioni di ogni agente: **non va aggiunto come knowledge**, ne' come
   cartella `Kernel` intera ne' come elenco fonti a parte. Nemmeno la
   baseline: dal 23/10/2026 (AU7, D-83) A3 e A4 la ricevono come allegato
   della chat (`Input_A3_A4.txt`), come A1. Se in un agente c'e'
   ancora `Kernel/Baseline_corrente.txt` fra le knowledge, toglierlo: sarebbe
   una baseline vecchia.

   Capability: il code interpreter ("Create documents, charts, and code") e'
   **acceso di default** su ogni agente nuovo — va **spento a mano**, insieme
   a "Create images" (Configura -> Capabilities): nessuno dei cinque ne ha
   bisogno, la scrittura resta sempre allo script. Nel tenant della Banca le
   capability **non sono abilitate** (verificato il 01/10/2026): non c'e'
   niente da spegnere, ed e' la configurazione voluta (D-11).
3-bis. **Link degli agenti per l'app** (D-83): per ogni agente, in Agent Builder,
   menu "..." dell'agente -> **Copia collegamento** (o, nella chat dell'agente, l'indirizzo
   della barra del browser), e incollarlo in `configurazione.json`, voce `link_agenti`
   (sezione 0.3). Con il link l'app apre da sola l'agente giusto; senza, lo si apre a
   mano e l'app funziona lo stesso.
4. A3: **niente prompt schedulato**. Dal 23/10/2026 (AU7) A3 legge la baseline solo
   dall'allegato `Input_A3_A4.txt`, che un prompt schedulato non puo' portare: risponderebbe
   "Baseline mancante". A3 si lancia dall'app (pulsante Settimana) o a mano (sezione 1).
   Se c'era un prompt schedulato, cancellarlo.
5. Archiviare in `Archivio_Cicli\Prompt\<data>\` il testo delle istruzioni
   appena incollate: si modificano nell'interfaccia di Agent Builder senza
   lasciare traccia.
6. Prova di fumo: dare a ogni agente un input minimo (es. una notizia
   qualsiasi ad A4) e controllare che risponda nel formato atteso — A3 e A4
   con un JSON, A5 con un esito, A6 con un JSON che il comando `schede`
   accetta.

**Verifica**: i cinque agenti rispondono nel formato atteso.

### 0.2-bis Agenti in Copilot Studio (alternativa ad Agent Builder, con l'app)

Gli stessi agenti si possono creare in **Copilot Studio** invece che in Agent Builder (anche solo alcuni, per esempio
A1) e usare con l'app allo stesso modo: chat nuova, allegati, messaggio, risposta copiata e incollata nell'app. L'app
salva le risposte con gli stessi nomi, nella stessa cartella e per lo stesso registro; annota solo da dove vengono
(casella "Agenti" della finestra). La versione tutta in Copilot Studio, con i flussi che leggono e scrivono i file da
soli, e' un'altra cosa: si progetta sul ramo `copilot-studio-pieno` (D-82).

Per ogni agente in Copilot Studio (esperienza standard; passi dettagliati della costruzione nella prova K0,
`09_Copilot_Studio/Prova_con_Copilot_Studio.md`, B1):
1. **Create** -> New agent -> **Configure**; nome come in Agent Builder (per esempio "A1 Horizon Scanner").
2. **Instructions**: lo stesso file intero di `02_Agenti/` della tabella del punto 3 (non i modelli, non le versioni
   `_CS` per le variabili globali, che servono solo alle prove K6).
3. **Knowledge**: le stesse cartelle SharePoint e gli stessi siti della tabella "Knowledge esatta per agente".
4. **Settings -> Generative AI**: "Use general knowledge" e "Web search" spenti; **File uploads** acceso (gli allegati
   in chat); **Code interpreter** spento (D-11). Modello: annotarlo (le prove K0 e K6 hanno usato GPT-5 reasoning).
5. **Authentication**: "Authenticate with Microsoft".
6. Il link per l'app: il riquadro di prova non ha un link; dopo **Publish**, il canale Teams o Microsoft 365 Copilot da'
   l'indirizzo della chat. In `link_agenti` si possono tenere i link delle due versioni (sezione 0.3).

Attenzione: in **Teams** un messaggio oltre circa 100 KB da' errore (prova K0): una risposta lunga di A1 si legge meglio
nella chat di Microsoft 365 Copilot o nel riquadro di prova. Copilot Studio puo' aggiungere in coda alla risposta i
link alle fonti: l'app li ignora.

### 0.3 Sul proprio PC (ogni analista, dopo 0.1 e 0.2)

1. Chiedere all'informatica **Python 3.10 o piu' recente** (python.org o Software Center, con l'opzione "Add
   python.exe to PATH" e tcl/tk, che python.org include di default). Serve anche Excel desktop. I moduli
   (`pywin32`, `openpyxl`, `pypac`) li installa `installa.cmd` al punto 3.
2. Sincronizzare con OneDrive (pulsante "Sincronizza" di SharePoint) le
   raccolte `Kernel`, `Report_Trimestrali`, `Archivio_Cicli`, `News_Inbox`.
3. **Doppio clic su `installa.cmd`** (cartella degli script, `07_Senza_Studio`; tappa M3). Si apre il Prompt dei
   comandi: in testa la versione del pacchetto e quella gia' installata su questo PC (D-89), poi i passi numerati,
   ognuno con il suo esito (OK, ATTENZIONE, NO):
   1. Python e tkinter;
   2. i moduli che mancano, installati con pip solo per il tuo utente (nessun diritto di amministratore). Se il
      proxy della Banca blocca pip, il messaggio lo dice: su un PC con la rete libera si scaricano i pacchetti con
      `python -m pip download pywin32 openpyxl pypac -d pacchetti` (stesso Python, 64 bit) e si copia la cartella
      `pacchetti` accanto a `07_Senza_Studio`; rilanciando `installa.cmd` si installano da li';
   3. i lanciatori arrivati per posta come `<nome>.cmd.txt` tornano `.cmd` (tranne `installa.cmd` se c'e' gia' ed
      e' diverso: e' il file in esecuzione, il riepilogo dice di rinominarlo a mano dopo);
   4. **la finestra della configurazione**: le quattro cartelle sincronizzate (pulsante Sfoglia), il tuo nome, chi
      valida di solito, se questo e' il PC della raccolta del lunedi', le opzioni dell'app e i link dei sette agenti
      per la versione scelta (Agent Builder o Copilot Studio). Con una configurazione che c'e' gia' i valori sono
      proposti; la precedente resta accanto (`configurazione_<data>.json.precedente`); le voci facoltative che
      mancano si scrivono con il valore predefinito;
   5. **i file dei pacchetti precedenti** che non servono piu' (elenco in `07_Senza_Studio\obsoleti.txt`, per esempio
      le cartelle `04_SharePoint`, `05_Workflow`, `06_Governance`, `08_Deploy`): dopo una conferma si spostano in
      `_obsoleti_<data>` accanto al pacchetto, da cui si possono riprendere o cancellare;
   6. **il kernel nella library `Kernel`**: l'elenco dei file nuovi e cambiati rispetto alla library e di quelli da
      togliere (`Baseline_corrente.txt`, `Tassonomia dei Rischi.csv`); dopo una conferma si copiano. La library e'
      condivisa: i file sostituiti e quelli tolti restano in `Kernel\_precedenti\<data>\`. Un pacchetto piu' vecchio
      di quello che ha copiato il kernel l'ultima volta (`Kernel\versione_kernel.txt`) non lo copia;
   7. i collegamenti: **NFR Horizon Scan** sul Desktop e **Invia a -> NFR notizie manuali** (tasto destro su un
      file: lo copia in `News_Inbox\<lunedi'>\Manuali`);
   8. solo sul PC della raccolta, l'attivita' pianificata **NFR raccolta notizie** ogni lunedi' alle 7 (se il PC
      e' spento, appena si accende; sezione "Raccolta notizie automatica");
   9. a richiesta, le cartelle sincronizzate "sempre su questo dispositivo" (consigliato);
   10. **gli agenti da reincollare** in Agent Builder, con il loro file di `02_Agenti`: quelli con le istruzioni
       cambiate rispetto a quelle segnate come reincollate (alla prima volta tutti). Quando li hai reincollati
       rispondi S; con N te li ricorda alla prossima installazione;
   11. la **Verifica del PC**: una riga per voce, salvata in `Archivio_Cicli\Verifiche_PC\`. Le righe NO vanno
       sistemate (il rimedio e' scritto sotto); se non e' chiaro, mandare il file a chi mantiene il pacchetto.

   In fondo il **riepilogo**: che cosa e' stato fatto e che cosa resta da fare a mano. Che cosa e' installato si
   scrive in `07_Senza_Studio\installato.json` (versione, kernel copiato, agenti reincollati), che lo zip non contiene.

   Rilanciare `installa.cmd` non fa danni (per esempio per cambiare un link): ogni passo controlla prima che cosa
   c'e'. Opzioni: `python installa.py --senza-finestra` (tiene la configurazione com'e'), `--senza-collegamenti`,
   `--senza-attivita`, `--senza-kernel`, `--senza-obsoleti`, `--solo-verifica`. La verifica si rifa' quando serve
   anche dall'app (Altro -> Verifica del PC) o con `python verifica_pc.py` (`--senza-excel` per non aprire il registro).

   **A mano, senza `installa.cmd`** (se le regole del PC non lo lasciano partire): da un Prompt dei comandi
   `pip install pywin32 pypac openpyxl` (`pypac` serve solo alla raccolta notizie, per trovare il proxy come fa il
   browser; `openpyxl` solo al file delle schede). Verifica: `python -c "import win32com.client, pythoncom;
   win32com.client.Dispatch('Excel.Application')"` non deve rispondere niente (non basta `import win32com`: non
   intercetta un pywin32 installato a meta', sezione 7). Poi nella cartella degli script copiare
   `configurazione_esempio.json` in `configurazione.json` e compilarlo con Blocco note (le barre dei percorsi vanno
   raddoppiate, `\\`, come nell'esempio). Le voci, che la finestra di `installa.cmd` scrive da sola:

   | Voce | Che cosa scrivere | Chi la usa |
   |---|---|---|
   | `workbook` | il registro `NFR_Registro.xlsx` nella cartella sincronizzata di `Report_Trimestrali` | script, app |
   | `kernel` | la cartella sincronizzata della library `Kernel` | script, app |
   | `cartella_uscita` | la cartella sincronizzata di `Archivio_Cicli` | script, app |
   | `news_inbox` | la cartella sincronizzata di `News_Inbox` | raccolta, app |
   | `utente` | il proprio nome e la funzione: e' il nome che i colleghi vedono quando stai scrivendo nel registro (lucchetto, D-83) | script, app |
   | `attesa_lucchetto` | secondi di attesa nella presa del lucchetto: 0 (nessuna attesa); un numero solo se due colleghi partissero spesso nello stesso istante | script |
   | `validatore_predefinito` | chi valida di solito (per esempio "Funzione Risk Management"): l'app lo propone, si puo' cambiare ogni volta | app |
   | `raccolta_su_questo_pc` | `true` solo sul PC che raccoglie le notizie il lunedi'; sugli altri `false` | app |
   | `agenti` | `Agent Builder` o `Copilot Studio`: la versione degli agenti proposta all'avvio (si cambia nella finestra) | app |
   | `ascolta_appunti` | `true`: basta premere Copia sotto la risposta; `false`: si incolla sempre nel riquadro | app |
   | `backup_da_tenere`, `giorni_log`, `giorni_parcheggio` | facoltative, per la pulizia e lo svuotamento (predefiniti 10, 90, 30; sezione 3-quater) | amministrazione |
   | `chiedi_a5` | `true` (predefinito): a precontrollo superato, se la casella A5 non e' spuntata, l'app chiede se passare anche da A5; `false`: nessuna domanda, A5 solo con la casella | app |
   | `link_agenti` | i link degli agenti (sezione 0.2, punto 3-bis): `{"A1": "https://...", "A3": "...", ...}`; con le due versioni, `{"Agent Builder": {"A1": ...}, "Copilot Studio": {"A1": ...}}`. Un link vuoto: l'agente si apre a mano | app |
   | `cartella_lavoro` | facoltativa: dove lo script tiene la copia di lavoro del registro (di solito non serve) | script |
4. Verificare che la cartella `03_Excel`, **fianco a fianco** con
   `07_Senza_Studio` (stesso livello, NON dentro la cartella sincronizzata da
   SharePoint), contenga il file `NFR_Dashboard_Template.xlsx`, non solo
   `genera_dashboard.py` (puo' mancare se l'allegato `.xlsx` e' stato filtrato
   dalla posta aziendale). Se manca, vedi la sezione 7, "Template non trovato".
5. Prova, dalla cartella degli script (come si apre: "Come si scrive un
   comando"):

   ```
   python esegui_ciclo_locale.py baseline
   ```
   Si deve vedere `Baseline scritta: ...Baseline_corrente.json`. Se il registro
   non c'e' ancora, il messaggio e' "Workbook non trovato" (sezione 7): il
   registro si crea al passo 0.4.

6. Prova di rete (dopo la sincronizzazione di `News_Inbox`): `python
   raccogli_notizie.py --anche-da-validare`. Si deve vedere `Raccolta scritta:
   ...` con delle notizie; se tutte le fonti sono "non raggiungibili", e' il
   proxy: chiedere all'informatica, oppure rinunciare al canale rss e proseguire
   con i siti dell'agente e i file in `Manuali`.

7. Prova dell'app: doppio clic sul collegamento **NFR Horizon Scan** del Desktop (o su `NFR.cmd`). Si apre la
   finestra con lo stato in alto; se il registro non c'e' ancora, il prossimo passo e' la baseline (0.4).

Da qui in avanti: ogni passo si fa dall'app (sezione "L'app NFR: uso passo per passo") o con i comandi nel Prompt dei
comandi, dalla cartella degli script; **il registro Excel deve essere chiuso** (anche per i colleghi) mentre lo script
lavora.

**Piu' analisti sullo stesso registro** (D-83). Ogni comando che scrive nel
registro prende un **lucchetto** (`Archivio_Cicli\_Lucchetto\registro.json`) e
lo lascia alla fine: se un collega sta scrivendo, il comando si ferma con
"Il registro e' in uso: <nome> ... dal ..." e non tocca niente; si riprova
quando ha finito. Lo script lavora poi su una **copia di lavoro** del registro
sul tuo PC e sostituisce il registro vero solo alla fine, dopo i controlli, e
solo se nel frattempo nessuno l'ha cambiato (altrimenti FERMATO "cambiato
mentre lo script lavorava": rilanciare). Il lucchetto e' un avviso per non
cominciare un lavoro che si fermerebbe; la protezione dei dati e' il controllo del
registro prima di sostituirlo. Per questo la presa non aspetta (`attesa_lucchetto`
0): due colleghi che partono nello stesso istante li ferma comunque il controllo.

### 0.4 Primo utilizzo reale (una volta, dopo 0.3)

Il template `03_Excel/NFR_Dashboard_Template.xlsx` contiene dati di ESEMPIO
(righe grigie). Il registro vero non si ricava a mano cancellandoli: lo crea
lo script.

1. In `configurazione.json` la voce `workbook` deve puntare al registro da
   creare (es. `...\Report_Trimestrali\NFR_Registro.xlsx`). Il file NON deve
   esistere.
2. Dalla cartella degli script (esempio per valutare per primo il 2026Q4, con
   la settimana del 28 settembre 2026):

   ```
   python esegui_ciclo_locale.py inizializza --ciclo-precedente 2026Q3 --settimana 2026-09-28
   ```
   `--ciclo-precedente` = il trimestre **prima** di quello da valutare;
   `--settimana` = il lunedi' della settimana in corso.
3. Si deve vedere `Registro creato: ...NFR_Registro.xlsx` e "Senza dati di
   esempio". Aprire il registro, foglio **Parametri**: scrivere nelle celle
   gialle i pesi, le soglie e i parametri dell'urgenza decisi nella fase 1
   dell'avvio (punto 1.3; la cella accanto alla somma dei pesi deve dire "OK"),
   salvare e chiudere. Poi `python esegui_ciclo_locale.py baseline`: la baseline
   dice il primo ciclo da valutare e non contiene rischi (gli allegati per A1,
   A3 e A4 sono accanto, nella cartella di uscita).
4. Non serve nessun trimestre gia' valutato: al primo ciclo A1 individua i
   rischi da zero, leggendo la documentazione disponibile (`Analisi_Interne`,
   `Analisi_Esterne`, `News_Inbox`, siti): un rischio per ogni meccanismo di
   perdita sostenuto da almeno una fonte specifica, anche piu' d'uno nella
   stessa categoria, e **nessuna categoria obbligatoria** (D-55): le categorie
   rimaste senza rischi le dichiara nella sintesi. Sono tutti nuovi
   (esito "Nuovo", lo calcola lo script). Tu li validi come ogni ciclo
   (sezione 3: foglio Validazione, una riga per rischio) e, nell'anagrafica,
   indichi quando lo sai il **presidio dei controlli** di ogni rischio
   (sezione 6).

Se il file esiste gia', lo script si ferma e non lo tocca: non sovrascrive mai
un registro.

### 0-bis. Aggiornare il pacchetto e il registro a un template nuovo (quando il registro e' di un template precedente)

**Non riguarda una prima installazione**: un registro creato con 0.4
(`inizializza`) nasce gia' con il template in vigore (versione `2026-10-09`) e
questa sezione non serve. Si applica a chi ha **gia'** un registro di un
template piu' vecchio e vuole portarlo avanti senza perdere i dati. Finche' non
e' aggiornato, **ogni comando si ferma** con "e' stato creato con un template
precedente al 25/09/2026" o "versione ..." e non tocca niente; lo stesso
comando vale per qualunque versione precedente.

Che cosa cambia per chi lavora, rispetto ai template dal 25/09 in poi (decisioni
e dettagli in `04_Riferimenti/DECISIONI.md`):
- **tassonomia interna della Banca** (D-74): i rischi si classificano nelle nove
  categorie in perimetro (9.1 Condotta ... 9.13 Processo) invece che negli event
  type di Basilea; il radar ha nove settori, le notizie nove intensita'. Dopo
  `aggiorna-registro` i rischi hanno ancora i codici di Basilea e **il radar non li
  mostra finche' A1 non li riclassifica**: al primo ciclo dopo l'aggiornamento A1
  assegna a ogni rischio una categoria (Osservazione nella colonna Segnalazioni) o
  lo segnala fuori perimetro (FP, da motivare: poi `dismetti`). Una categoria
  sbagliata si corregge a mano nell'anagrafica (Parametri, colonna J, elenco a
  discesa). Le intensita' delle notizie di prima (colonne Imp_L1_0x) restano solo
  nel registro vecchio;
- **ciclo straordinario** (D-75): un evento critico si valuta subito, solo per i
  rischi toccati, con un periodo `AAAAQn-Sk` (sezione 2-bis); A3 e A4 lo possono
  proporre; lo fa l'agente nuovo **A8 Evento critico** (D-77), che analizza a fondo
  l'evento e puo' anche solo censire un rischio nuovo;
- **registro unico** (D-79, dall'08/10, sostituisce la lista di osservazione
  della D-73): un solo registro di rischi `NFR-nn`, tutti con la stessa scala; i
  primi (regola di Parametri, righe 65-75) sono **nel radar** con KRI e azioni,
  gli altri **in osservazione**. `aggiorna-registro` trasforma le voci `OSS-nn`
  in rischi in osservazione con un codice nuovo (sezione 2, "Registro unico");
- **A7 Assistente del registro** risponde in chat sul perche' delle valutazioni,
  senza allegati: lo script scrive la sua knowledge nella cartella
  `Kernel\Spiegazioni`; nella prima pagina del Quadro la cella gialla **Note
  dell'analista** (D-72, sezione 4);
- A5 e' facoltativo e il ciclo si ferma solo per difetti di integrita'; le altre
  segnalazioni dei controlli e di A5 sono nella colonna **Segnalazioni dei
  controlli** del foglio Validazione, e quelle da motivare chiedono la
  Motivazione (D-71, sezione 3);
- il foglio **Validazione** ha una riga per rischio, KRI, azione e notizia, con le
  celle gialle gia' compilate con le proposte (D-67, sezione 3); il dettaglio
  campo per campo e' nel foglio dati **Storico_Validazioni**;
- la sintesi di A3 e i flag proposti di ogni settimana stanno in
  **Sintesi_Settimane** (D-66);
- **livello di allerta** calcolato dal foglio e mostrato nel radar (D-63) e
  colonna **Tipo** dei KRI, due per rischio (D-64);
- Severity si chiama **Impatto**; la Confidence non c'e' piu' e ogni fonte ha una
  **rilevanza** 1-3; gli **anni di adeguamento** li propone A1 e li decidi in
  validazione (D-57...D-60);
- lo scoring e' semplificato: il **presidio dei controlli** e' un giudizio della
  Banca nell'anagrafica, fuori dallo score; la Velocity e' facoltativa; i KRI
  possono non avere soglie (D-49...D-56);
- l'anagrafica arriva a 20 rischi.

0. **Prima di sostituire qualunque file**: se la Banca ha modificato il
   kernel sul PC (`01_Kernel\tassonomia_nfr.md`, `rubrica_scoring.md`,
   `fonti.md`) o `04_Riferimenti\DECISIONI.md`, quelle modifiche vanno date a chi
   mantiene il pacchetto **prima** dell'aggiornamento: il pacchetto nuovo
   contiene la sua versione di quei file e la sovrascrive, e i prompt degli
   agenti sono composti da quella versione. Se l'aggiornamento e' gia' stato
   estratto, la versione precedente si recupera dalla cronologia versioni di
   OneDrive o della library `Kernel`.
1. Estrarre il pacchetto (o lo zip di aggiornamento) **sopra la cartella del
   pacchetto** sul PC, sostituendo i file: `configurazione.json` non e' nello
   zip e resta com'e'. **Dal pacchetto del 30/10/2026 (D-89) poi basta un doppio
   clic su `installa.cmd`** (sezione 0.3, punto 3): rinomina i `.cmd.txt` arrivati
   per posta, aggiunge le voci nuove della configurazione, copia il kernel nella
   library (dopo una conferma, togliendo `Baseline_corrente.txt` e `Tassonomia dei
   Rischi.csv`), sposta i file e le cartelle dei pacchetti vecchi e dice quali
   agenti reincollare. Quello che segue in questo punto resta per chi lo fa a mano.
   Poi copiare **tutti i file di `01_Kernel`** e
   `04_Riferimenti\DECISIONI.md` nella library `Kernel`, cioe' nella cartella
   sincronizzata indicata alla voce `kernel` di `configurazione.json`: **lo
   script legge da li'** mappa dei campi, schemi, rubrica ed elenco fonti, non
   da `01_Kernel`. Senza `controlli_A5.md` e `guida_scrittura_A1.md` l'allegato
   di A1 ha solo la baseline (lo script lo dice). Il pacchetto del 05/10
   aggiunge `07_Senza_Studio\precontrollo.py` (senza, lo script non parte) e la
   cartella `09_Copilot_Studio`; la prova della versione, dall'installazione a un
   ciclo completo su un registro separato, e' in
   `04_Riferimenti\Prove\Prova_senza_Copilot_Studio.md`.
   Ricaricare in Agent Builder le istruzioni degli agenti cambiati rispetto alla
   tua installazione (file `.md` di `02_Agenti`, gia' pronti: **non** serve
   `componi_prompt.py`, che e' per chi mantiene il pacchetto). Rispetto al
   01/10 cambiano **A1, A5 e A6** (D-68, D-69); il pacchetto del 06/10 cambia
   di nuovo **A5** (D-71: i suoi rilievi vanno al validatore) e
   `controlli_A5.md` nel kernel; il pacchetto del 07/10 aggiunge l'agente **A7**
   (da creare: sezione 0.2) e cambia l'allegato di A1 (la guida di scrittura
   chiede i fenomeni non censiti e, dalla sera del 07/10, la lista di
   osservazione: basta copiare il kernel, A1 non si ricarica); con la lista di
   osservazione cambiano di poco le istruzioni di **A7** (se l'hai gia' creato,
   reincollale) e quelle di **A3**, che collega le notizie alle voci (reincollarle);
   con il ciclo straordinario cambiano **A3** e **A4** (proposta di ciclo
   straordinario: reincollarle); con la tassonomia interna (D-74) cambiano
   **A1, A3, A4 e A5** (le categorie sono nelle loro istruzioni: reincollarle
   tutte) e il kernel (copiarlo tutto); con il ciclo straordinario fatto da A8
   (D-77) si crea l'agente **A8** (sezione 0.2) e si copia il kernel (guida di
   scrittura e schema); A1 non cambia. Con il registro unico (D-79, pacchetto
   dell'08/10 sera) cambiano **A1, A3, A5, A7 e A8** (reincollarli tutti) e il
   kernel (rubrica, schemi, guida di scrittura, controlli, mappa: copiarlo tutto).
   Con il pacchetto del 23/10/2026 (app NFR, D-83; nomi degli allegati, D-84) cambiano **A3, A4, A5, A6 e A8**
   (reincollarli), il kernel no; in `07_Senza_Studio` ci sono file nuovi (`NFR.cmd`, `app_nfr.py`, `flussi.py`,
   `stato.py`, `ingresso.py`, `appunti.py`, `esecutore.py`, `lucchetto.py`); in `configurazione.json` vanno
   aggiunte le voci nuove (sezione 0.3: `utente`, `validatore_predefinito`, `raccolta_su_questo_pc`, `agenti`,
   `ascolta_appunti`, `link_agenti`); dalla knowledge di A3 e A4 e dalla library `Kernel` si toglie
   `Baseline_corrente.txt` e si cancella il prompt schedulato di A3 (sezione 0.2). Poi `baseline` riscrive gli
   allegati con i nomi nuovi. Nessun `aggiorna-registro`.
   In dubbio, ricaricarli tutti.
   Dal pacchetto dell'08/10 i documenti di riferimento stanno in una cartella sola,
   `04_Riferimenti` (DECISIONI, SharePoint, governance e, in `Prove`, i
   copioni di prova): nella copia del pacchetto sul PC cancellare le vecchie
   `04_SharePoint`, `05_Workflow`, `06_Governance` e `08_Deploy`; dal 09/10
   `Tassonomia dei Rischi.csv` sta in `04_Riferimenti`: se e' ancora nella library
   `Kernel`, toglierlo (non lo legge nessun componente). Le cartelle degli
   script (`07_Senza_Studio`) e del kit (`09_Copilot_Studio`) non cambiano nome:
   `configurazione.json` e le attivita' pianificate restano validi.
2. **Non serve validare prima**: le righe ancora da validare (per esempio le
   notizie di una settimana) passano nel foglio Validazione nuovo, con cio' che
   avevi gia' scritto nel vecchio foglio (Decisione Rettificato con il valore
   = cella gialla cambiata; Respinto = Respingi Sì; la Motivazione). Unica
   eccezione, per registri fino alla versione `2026-09-25c`: righe da decidere su
   campi tolti dal modello (Severity, Confidence, Gap_Controlli) vanno validate
   prima con il pacchetto con cui sono state scritte; lo script lo dice e non
   tocca niente.
3. **Chiudere** il registro (anche i colleghi), poi dalla cartella degli script:

   ```
   python esegui_ciclo_locale.py aggiorna-registro
   ```
4. Si deve vedere `Registro aggiornato alla versione 2026-10-09`, il numero di
   righe copiate per tabella e dove e' stato conservato il registro vecchio
   (`Archivio_Cicli\Backup\..._prima_di_aggiorna-registro_...`); se c'erano
   righe da validare, anche `Righe ancora da validare: N (periodi ...)`. Lo script
   elenca le colonne rinominate e quelle tolte dal modello, che restano solo nel
   registro vecchio. Il presidio dei controlli parte da "Non verificato" se non
   c'era; i KRI esistenti restano senza tipo finche' A1 non li ripropone (al primo
   ciclo ne ripropone due per rischio, il terzo esce di vigore). Da un registro con
   la lista di osservazione (fino alla `2026-10-08b`) compare anche `Lista di
   osservazione (D-73) convertita nel registro unico (D-79): OSS-01 -> NFR-13, ...`:
   le voci ancora in osservazione diventano rischi in osservazione con un codice
   libero e valori provvisori (Impatto = impatto potenziale, Probabilita dalla
   plausibilita', Prossimita dall'orizzonte), che A1 rivaluta al primo ciclo; le
   notizie collegate a una voce passano al rischio. Il file mantiene nome e
   percorso.
5. Prova: `python esegui_ciclo_locale.py baseline` deve rispondere come sempre
   (A3 e A4 ricevono la baseline dal'allegato `Input_A3_A4.txt`
   che il comando riscrive: niente da ricaricare nella library `Kernel`).

Prima di sostituire il file lo script verifica che le righe siano le stesse,
che non ci siano errori di formula e che la baseline sia identica a parte i
campi tolti; se una verifica fallisce si ferma con "Aggiornamento NON
applicato" e il registro resta com'era. Copia tutto per nome di colonna
(notizie, validazioni, cicli, anagrafica, ciclo e settimana correnti, parametri
dell'urgenza). **Pesi, soglie e anni per Prossimita (Z)** diventano quelli del
template nuovo (valori nella sezione 4): lo script stampa quelli che c'erano
prima, da reinserire a mano in Parametri solo se la Banca li aveva cambiati di
proposito.

## 1. Ogni lunedi' — aggiornamento settimanale (circa 20 minuti)

> **Dall'app**: pulsante **Settimana** (capitolo "L'app NFR", sezione "Pulsante Settimana"). Qui sotto il dettaglio: cio' che l'app fa per te e i comandi per chi lavora dal Prompt dei comandi.

| # | Chi | Cosa fare | Cosa si deve vedere |
|---|---|---|---|
| 1 | automatico o tu | `python raccogli_notizie.py` (di solito lo lancia da solo l'Utilita' di pianificazione di Windows alle 7) | `Raccolta scritta: ...News_Inbox\<lunedi'>\Raccolta_<oggi>.txt` e il numero di notizie. Se compare "ATTENZIONE: ... non raggiungibile", la raccolta e' incompleta per quella fonte: annotarlo, si puo' proseguire. |
| 2 | tu | Salvare nella cartella `News_Inbox\<lunedi'>\Manuali\` cio' che non arriva da solo: circolari CERTFin, rapporti di threat intelligence, newsletter, notizie viste sui siti senza feed. | I file sono nella cartella. |
| 3 | A3 | In Copilot, aprire l'agente **A3 Interim Update**, chat nuova: **allegare** `Input_A3_A4.txt` (cartella di uscita: la baseline, AU7) e scrivere `Esegui l'aggiornamento settimanale`. Il prompt schedulato non porta l'allegato: dal 23/10/2026 A3 senza allegato risponde "Baseline mancante". | Una risposta che e' **solo** un blocco JSON (comincia con `{` e finisce con `}`). Se risponde "Baseline mancante", l'allegato non e' arrivato. |
| 4 | tu | Copiare tutta la risposta, incollarla in Blocco note, *Salva con nome*: tipo "Tutti i file", codifica **UTF-8**, nome `A3_<lunedi'>.json` (es. `A3_2026-10-12.json`) nella cartella di lavoro. | Il file esiste. |
| 5 | tu | `python esegui_ciclo_locale.py settimanale --payload A3_2026-10-12.json` | `Settimana 2026-10-12: N notizie aggiunte`, i segnali netti oltre la soglia, le aree non presidiate, e `Excel di output: ...Settimane\2026-10-12\...`. |
| 6 | tu | Aprire l'Excel di output della settimana: Registro (colonna "Segnali netti"), Notizie (colonna Presidio e, a destra, la **sintesi di A3 e i flag proposti** della settimana). | Un ▲ o "AREA NON PRESIDIATA" sono segnali da riportare al prossimo trimestre: **nessuno score cambia di settimana in settimana**. |
| 7 | tu (consigliato) | Validare le notizie della settimana: sezione 3, con `--periodo 2026-10-12`. | `Validazione del periodo 2026-10-12 applicata: ...` |

## 2. Ogni trimestre — ciclo trimestrale (mezza giornata, piu' la validazione)

> **Dall'app**: pulsante **Trimestre** (capitolo "L'app NFR", sezione "Pulsante Trimestre"). Qui sotto il dettaglio: cio' che l'app fa per te e i comandi per chi lavora dal Prompt dei comandi.

Si fa nei primi giorni dopo la fine del trimestre. Esempio per il `2026Q3`.

| # | Chi | Cosa fare | Cosa si deve vedere |
|---|---|---|---|
| 1 | tu | Controllare che il trimestre PRECEDENTE sia validato: nel registro, foglio Registro riga 4 deve dire **"Ciclo validato"** (anche la fascia blu in cima a ogni foglio dice "validato" o "da validare"). Se dice "CICLO NON ANCORA VALIDATO", fare prima la sezione 3 per quel ciclo. | "Ciclo validato". |
| 2 | tu | `python esegui_ciclo_locale.py baseline` | `Baseline scritta: ...`, `Allegato per A1: ...Input_A1_2026Q3.txt` e `Allegato per A3 e A4 (AU7): ...Input_A3_A4.txt`. Se compare "ATTENZIONE: il ciclo ... ha ancora N righe da validare", tornare al passo 1. Se compare "Avviso: nel kernel ... mancano", copiare nella library `Kernel` tutti i file di `01_Kernel` (sezione 0-bis, punto 1). |
| 3 | — | Niente da fare (dal 23/10/2026, AU7): A3 e A4 ricevono la baseline dagli allegati scritti al passo 2, non piu' dalla raccolta `Kernel`. | — |
| 4 | A1 | In Copilot, agente **A1 Horizon Scanner**, chat nuova: **allegare al messaggio** `Input_A1_2026Q3.txt` (cartella di uscita) e scrivere `Esegui il ciclo`. L'allegato va nella chat: A1 non lo legge dalla library `Kernel`, che non e' tra le sue knowledge. | Solo JSON, con `"ciclo":"2026Q3"`. Se risponde "Baseline mancante", l'allegato non e' arrivato (per esempio e' solo nel `Kernel`): allegarlo al messaggio. |
| 5 | tu | Salvare la risposta come `A1_2026Q3.json` (Blocco note, UTF-8, come al punto 4 della sezione 1). | — |
| 5-bis | tu | **Precontrollo: FACOLTATIVO, si puo' saltare** se non usi A5 (pochi secondi, senza Excel, non tocca il registro): `python esegui_ciclo_locale.py precontrollo --payload A1_2026Q3.json`. Serve in due casi: **prima di A5, se lo usi** (scrive il suo allegato `Input_A5_2026Q3.txt`, D-84), o per far correggere ad A1 le segnalazioni prima di scrivere. Altrimenti si passa direttamente al punto 7, che fa gli stessi controlli e, se qualcosa ferma il ciclo, scrive lo stesso messaggio di correzione per A1. | `Precontrollo dell'output di A1 (2026Q3): nessun rilievo.` (la riga dopo, `Impronta dell'output di A1: ...`, serve solo alla prova di Copilot Studio). Altrimenti i punti da correggere (fermerebbero il ciclo), da verificare (finirebbero nella colonna Segnalazioni) e i rischi con testi troppo corti (C10, D-86: conviene farli allungare ad A1; se si prosegue restano Osservazioni), e il file `Cicli\2026Q3\Correzione_A1_2026Q3.txt`: aprirlo con Blocco note, copiarlo tutto, incollarlo nella chat di A1, salvare la nuova risposta (punto 5) e ripetere. |
| 6 | A5 | **Facoltativo** (D-71). Agente **A5 Challenger**: allegare SOLO `Input_A5_2026Q3.txt` (output di A1 e baseline, scritto dal precontrollo del punto 5-bis, che con A5 serve sempre), scrivere `Esegui i controlli`, salvare come `A5_2026Q3.json`. I suoi rilievi non fermano il ciclo: vanno nella colonna Segnalazioni del foglio Validazione (un suo Bloccante rende obbligatoria la Motivazione). Se lo usi, va rifatto ogni volta che A1 viene rifatto (vale solo per l'output esaminato); mai per le settimane, per A4 o dopo la validazione. | Solo JSON con `"ciclo":"2026Q3"` e `"esito":"Approvato"` o `"Da rivedere"`. |
| 7 | tu | `python esegui_ciclo_locale.py trimestrale --payload A1_2026Q3.json` e, se hai usato A5, `--challenger A5_2026Q3.json` | `Ciclo 2026Q3 scritto: 12/12 rischi, zero errori di formula.`, `A5: usato` o `non usato (facoltativo)`, se ce ne sono `SEGNALAZIONI DA MOTIVARE: N su M rischi` (punto 8-bis), `Registro unico (D-79): nel radar N rischi su 15 posti; in osservazione M; entrati nel radar ...; usciti ...` e `Excel di output: ...Cicli\2026Q3\NFR_Registro_2026Q3.xlsx`. Se compare "ATTENZIONE: l'anagrafica ha N posti liberi", avvisare chi mantiene il pacchetto. |
| 8 | tu | Se invece compare **FERMATO** con "Ciclo da rivedere": l'output di A1 ha un difetto che renderebbe incoerente il registro (C1 un rischio mancante o con un'altra categoria, C2 variazioni che non tornano, C7 o C9 un KRI con un identificativo sbagliato). Aprire il file `Cicli\2026Q3\Correzione_A1_2026Q3.txt` indicato, copiarlo tutto nella chat di A1, salvare la nuova risposta (punto 5) e ripetere il punto 7 (e A5, se lo usi, sul nuovo file). | Il registro non e' stato toccato: si puo' ripetere quante volte serve. |
| 8-bis | tu | **Segnalazioni da motivare**: non si rilancia niente. Sono le regole di metodo non rispettate (C3: evidenza fuori finestra o generica, salto di piu' di un punto; C5: fonte datata dopo la data di riferimento, oppure esposizione della Banca non nota alle fonti, con la Probabilita proposta e quella "se esposta" (D-81); C9: KRI senza la coppia Esposizione/Evoluzione o soglie invertite) e i rilievi Bloccanti di A5. Si decidono in validazione (sezione 3). I testi troppo corti (C10, D-86) restano Osservazioni anche quando A5 li dice Bloccanti: non chiedono la Motivazione. Se preferisci farle correggere ad A1 prima di scrivere, usa il precontrollo (punto 5-bis). | Nel foglio Validazione quei rischi hanno ⚑ davanti al nome e il testo nella colonna **Segnalazioni dei controlli**; il Quadro dice quante sono (riga "Segnalazioni da motivare"). |
| 9 | validatore | **Validare il ciclo**: sezione 3, con `--periodo 2026Q3`. Finche' non e' fatto, il trimestre dopo non parte. | Registro riga 4: "Ciclo validato". |
| 10 | — | Niente da fare: `trimestrale` (punto 7) ha gia' archiviato i prompt degli agenti del pacchetto in `Archivio_Cicli\Cicli\2026Q3\Prompt_in_uso\`. Se in Agent Builder ci sono istruzioni diverse da quelle del pacchetto, copiarle li'. | La riga `Prompt degli agenti del pacchetto archiviati: ...` nell'uscita di `trimestrale`. |
| 11 | tu | **Schede dei rischi**, dati per A6: `python esegui_ciclo_locale.py schede-input` | `Input delle schede del ciclo 2026Q3 (12 rischi): ...Cicli\2026Q3\Input_A6_2026Q3.json`. Se compare "righe da validare", il ciclo non e' ancora validato (punto 9). |
| 12 | A6, tu | Agente **A6 Schede dei rischi** (solo dopo la validazione, solo con l'allegato di `schede-input`; non valuta, spiega i valori validati): allegare SOLO `Input_A6_2026Q3.json`, scrivere `Scrivi le schede`. Salvare la risposta come `A6_2026Q3.json` (come al punto 5), poi `python esegui_ciclo_locale.py schede --payload A6_2026Q3.json` | `Schede del ciclo 2026Q3: 12 rischi, testi di A6 controllati. File: ...Schede_2026Q3.xlsx` e `PDF: ...Schede_2026Q3.pdf`. Se compare **FERMATO** (per esempio "numeri che non stanno nei dati del rischio" o "le fonti devono essere quelle dell'input"), chiedere ad A6 di correggere quei punti e rilanciare. Senza A6: `python esegui_ciclo_locale.py schede` produce le schede con i testi del registro. |
| 13 | tu | **Report al comitato**: lo produce gia' `valida` (punto 9) quando valida il ciclo corrente. `python esegui_ciclo_locale.py report` lo rigenera (con `--con-lavoro` aggiunge Registro e Parametri, in orizzontale su una pagina ciascuno). Il PDF si fa dal registro com'e' ora: se dopo la validazione cambi a mano il presidio, gli anni di adeguamento, l'attenzione del supervisore o lo stato di un'azione, **rilancia il comando** e il PDF segue le modifiche (la versione precedente resta con la data nel nome). Per un altro Excel: `--file <percorso>`. Allegare `Schede_2026Q3.xlsx` (o il suo PDF). | `Report al comitato del ciclo 2026Q3 rigenerato da ...` e il PDF in `Archivio_Cicli\Cicli\2026Q3\Report_comitato_2026Q3.pdf`, dal Quadro d'insieme alla Metodologia. Se la riga "Dopo il commento" del Quadro e' compilata (fondo giallo), il commento di A1 precede delle rettifiche: valgono i numeri. |

**Che cosa controlla lo script** (D-69, D-71): all'output di A1 applica la
parte dei controlli che si puo' verificare con una regola (lo schema, C1, C2,
C3, C7, C9, le date di C5, le osservazioni di C5, C6 e C8) e le parti del
razionale che servono alle schede. Ferma solo i difetti di integrita' (schema,
C1, C2, C7, identificativi dei KRI); C3, le date di C5, la coppia e le soglie
dei KRI diventano segnalazioni da motivare in validazione. Non giudica la
plausibilita' dei valori (C4): la giudica A5, se usato, e comunque il
validatore. Il precontrollo fa gli stessi controlli senza scrivere niente.

**Registro unico** (D-79): ogni fenomeno censito e' un rischio `NFR-nn`, valutato
con la stessa rubrica e lo stesso score. Lo script mette **nel radar di Mosca** i
rischi con **Prossimita almeno 2 e Probabilita almeno 2**, fino alla **capienza**
(15, fino a 20), i piu' alti per score; restano dentro anche oltre la capienza un
rischio AGIRE ORA, un tema del supervisore e uno che il validatore vuole nel radar.
Gli altri sono **in osservazione**: niente KRI ne' azioni, fuori da radar,
classifica e urgenza, con l'orizzonte stimato in anni e il **segnale di
avvicinamento** (il fatto che li porterebbe nel radar). Un rischio che scende sotto
la regola resta un ciclo **"Radar, in uscita"** ed esce al secondo (i suoi KRI escono
di vigore, la storia resta); uno che sale entra subito e A1 gli scrive KRI e azioni.
A ogni ciclo A1 rivaluta tutti i rischi del radar e quelli in osservazione per cui
ha evidenza nuova; gli altri lo script li riporta com'erano. Al massimo **20 rischi
in osservazione**. Stato, motivo e movimento (Entrato, Uscito) sono nel RiskRegister,
nel foglio Osservazione e nella pagina **Fenomeni** del report (sezione 4); la regola
e i suoi parametri nel foglio Parametri, righe 65-75. Le istruzioni per A1 sono
nell'allegato `Input_A1` e nel suo prompt (reincollarlo, sezione 0-bis).

**Avviso sulle schede** (D-68): i testi delle schede li scrive A1 nel
razionale, diviso in parti (RISCHIO:, IMPATTO:, PROBABILITA:, PROSSIMITA:,
VELOCITY:, ADEGUAMENTO:; per azioni e KRI EFFETTO:), quindi ci sono anche senza
A6; con A6 sono riscritti per chi non conosce il tema. Se `trimestrale` stampa "Avviso per le schede: il razionale di ... non e'
diviso in parti", in Agent Builder ci sono ancora le istruzioni vecchie di A1:
ricaricarle (sezione 0-bis); per quel ciclo la scheda mostra il razionale
intero, come prima.

**Messaggi per gli agenti**: il messaggio base di ogni agente, le sue variazioni (per esempio il messaggio rinforzato per A1, la richiesta di analizzare documenti precisi o di verificare un tema) e cosa un messaggio non puo' cambiare sono nella sezione 8.

## 2-bis. Ciclo straordinario — un evento critico non aspetta il trimestre (D-75)

> **Dall'app**: pulsante **Straordinario** (capitolo "L'app NFR", sezione "Pulsante Straordinario"). Qui sotto il dettaglio: cio' che l'app fa per te e i comandi per chi lavora dal Prompt dei comandi.

Si fa solo su decisione della funzione di rischio, quando un evento rende superata la
valutazione di uno o piu' rischi e non si puo' aspettare il trimestre. La proposta puo'
venire da A3 (comando `settimanale`: "PROPOSTA DI CICLO STRAORDINARIO di A3 per ...", e
in rosso nel riquadro del foglio Notizie) o da A4 (in testa al parere), con la regola del
segnale critico della rubrica: intensita' 3 su un rischio con Impatto 4-5, un evento in
corso presso la Banca, un fornitore o una controparte, una capacita' nuova di una
minaccia che rende superato un descrittore. Il periodo si chiama come il trimestre
appena chiuso con `-S1`, `-S2`... (per esempio `2026Q4-S1`): rivaluta **solo** i rischi
indicati e censisce i rischi nuovi che l'evento crea; gli altri restano come erano, gia'
validati. Senza `--rischi` lo straordinario e' di **solo censimento**: l'evento crea un
rischio nuovo e non cambia quelli esistenti. Lo fa l'agente **A8 Evento critico** (D-77):
legge per intero i documenti dell'evento e scrive, oltre ai rischi, l'**analisi
dell'evento** (fatto, catena causale, rischi toccati e non toccati, documenti, limiti),
che va nella colonna Straordinario di Sintesi_Cicli (il fatto) e nella knowledge di A7
(tutta). Stesso allegato e stesso formato di A1: i comandi sono quelli del trimestre.

| # | Chi | Cosa fare | Cosa si deve vedere |
|---|---|---|---|
| 1 | tu | Il ciclo corrente deve essere validato (Registro, riga 4: "Ciclo validato"). | "Ciclo validato". |
| 2 | funzione di rischio, tu | `python esegui_ciclo_locale.py baseline --straordinario --rischi NFR-01,NFR-07 --motivo "l'evento e perche' non puo' aspettare" --decisore "Comitato Rischi"` (facoltativo `--data AAAA-MM-GG`, data di riferimento: di norma oggi; senza `--rischi` = solo censimento di rischi nuovi) | `CICLO STRAORDINARIO 2026Q4-S1 deciso da ...`, la decisione archiviata in `Cicli\2026Q4-S1\Straordinario_2026Q4-S1.json` e l'allegato `Input_A8_2026Q4-S1.txt`. |
| 3 | A8 | Chat nuova, allegare `Input_A8_2026Q4-S1.txt` e i documenti sull'evento (o indicarli nella library) e scrivere `Esegui il ciclo straordinario`; salvare la risposta come `A8_2026Q4-S1.json`. | Solo JSON con `"ciclo":"2026Q4-S1"`, `analisi_evento` e i soli rischi indicati (piu' i rischi nuovi creati dall'evento; almeno uno se lo straordinario e' di solo censimento), con i valori riletti dei loro KRI in `ricalcolo_kri_ciclo_precedente`. Un KRI non riletto arriva al validatore come segnalazione da motivare: scriverne il valore nella griglia (riga del KRI, Valore_Corrente) o motivare. |
| 4 | tu | facoltativo, si puo' saltare: `python esegui_ciclo_locale.py precontrollo --payload A8_2026Q4-S1.json`; poi `trimestrale --payload A8_2026Q4-S1.json` (A5 facoltativo come nel trimestre) | `CICLO STRAORDINARIO 2026Q4-S1: rivalutati ...`. Se FERMATO con "non indicato per il ciclo straordinario", "assente dall'output" o "solo censimento", A8 ha scritto un rischio in piu' o in meno: dargli il messaggio di correzione ("Messaggio per A8", sezione 2, punto 8). Fra le segnalazioni, senza fermare: un rischio che secondo A8 l'evento tocca ma non e' stato indicato (valutare se rivalutarlo con un altro straordinario o al trimestre). |
| 5 | validatore | Validare con `--periodo 2026Q4-S1` (sezione 3): nella griglia ci sono solo i rischi rivalutati e quelli nuovi, i loro KRI e le azioni nuove. La regola del punto si misura sul periodo prima (il trimestre o lo straordinario precedente). L'analisi dell'evento non porta valori: si legge in Sintesi_Cicli o si chiede ad A7. | Registro riga 4: "Ciclo validato"; la fascia blu dice "Ciclo straordinario 2026Q4-S1". |
| 6 | tu | Report, schede, knowledge di A7: come nel trimestre (sezione 2, punti 11-13). | — |

Il trimestre dopo (per esempio il `2027Q1`) parte dai valori validati dello
straordinario: la baseline lo dice (`ciclo_precedente` = `2026Q4-S1`). Nel radar e nei
fogli lo straordinario e' il ciclo corrente; Delta e trend lo contano come un periodo.
Per un rischio non rivalutato, la Y dell'urgenza viene dalle azioni del ciclo in cui e'
stato valutato (colonna Periodo_Valutazione del RiskRegister).

## 3. Validare — accettare, correggere, respingere (validatore)

> **Dall'app**: pulsante **Validazione** (capitolo "L'app NFR", sezione "Pulsante Validazione"). Qui sotto il dettaglio: cio' che l'app fa per te e i comandi per chi lavora dal Prompt dei comandi.

La validazione e' il momento in cui la Banca fa proprie (o no) le proposte
degli agenti. Si fa nel foglio **Validazione**, **una riga per rischio (nel radar o
in osservazione), KRI, azione e notizia** (D-67, dal 02/10/2026; prima
era una riga per ogni singolo valore). Tutto resta tracciato: la proposta dell'agente non si cancella mai,
e il comando `valida` registra nel foglio dati **Storico_Validazioni**, campo
per campo, la decisione, il valore deciso, il motivo, chi e quando. Le righe
"Rettificato" (l'agente ha proposto X, la Banca ha deciso Y, per questo motivo)
sono la raccolta che servira' per insegnare agli agenti.

1. **Chiudere** l'Excel di output e aprire il registro vivo `NFR_Registro.xlsx`,
   foglio **Validazione**. La riga 3 dice che cosa c'e' da validare (per
   esempio "ciclo 2026Q3 (53 righe) · settimana del 12/10/2026 (5 notizie)"):
   il foglio mostra solo i periodi non ancora validati, in quattro sezioni
   (Rischi, KRI, Azioni, Notizie con la colonna Settimana). Dei rischi in
   osservazione ci sono solo quelli che A1 ha riscritto con evidenza nuova; gli
   altri non si rivalidano.
2. In ogni riga, accanto a ogni proposta dell'agente (colonna grigia, solo da
   leggere) c'e' una **cella gialla gia' compilata con la stessa proposta**.
   - **Se sei d'accordo non toccare niente**: la riga vale come accettata.
   - **Se non sei d'accordo** scrivi il valore giusto nella cella gialla (anche
     piu' d'uno nella stessa riga) e il perche' nella colonna **Motivazione**,
     almeno 10 caratteri con l'evidenza: la cella cambiata diventa arancio, la
     Motivazione resta rossa finche' manca.
   - **Per scartare** un KRI, un'azione o una notizia: **Respingi = Sì** e la
     Motivazione. Un rischio non si respinge: si rettifica, si mette in
     osservazione (sotto) o si toglie con `dismetti` (sezione 3-bis).
   - **Stato del rischio** (D-79, colonne a destra delle Segnalazioni): **Stato**
     dice dove lo mette la regola e perche' (Radar, Radar in uscita, Osservazione,
     con il motivo: quale soglia manca, l'eccezione, la capienza); la cella gialla
     **Decisione sullo stato** e' `Automatico` (vale la regola), `Radar` (resta o
     entra nel radar anche sotto le soglie) oppure `Osservazione` (resta o va fuori),
     con la Motivazione. La decisione resta da un ciclo all'altro finche' non la
     cambi; `valida` ricalcola lo stato sui valori validati (chi entra in validazione
     avra' KRI e azioni da A1 al ciclo dopo).
   - **Segnalazioni dei controlli** (ultima colonna dei rischi, D-71): cio' che lo
     script e A5 (se usato) hanno trovato su quel rischio, anche sui suoi KRI e
     sulle sue azioni; sopra la colonna, quelle che riguardano il ciclo intero.
     **⚑ davanti al nome** = almeno una segnalazione DA MOTIVARE: la Motivazione e'
     obbligatoria anche se non cambi nulla.
   - **Esposizione non nota** (segnalazione C5, D-81): A1 non sa se la Banca ha il
     prodotto, il processo o il fornitore colpito, e ha proposto la Probabilita senza
     l'esposizione; la segnalazione dice anche il valore "se esposta". Tu lo sai, o lo
     chiedi all'owner: se la Banca e' esposta scrivi quel valore nella cella gialla
     della Probabilita (per un rischio gia' nel registro al massimo un punto dal ciclo
     prima; oltre, dopo la validazione, con `riapri`), altrimenti lascia la proposta e
     scrivi perche' nella Motivazione.
   - In fondo alle righe dei rischi, **Score composito** e **Margine di Mosca**
     si ricalcolano mentre scrivi, con i valori gialli e le azioni non respinte
     (rosso AGIRE ORA, giallo entro l'anno, verde con margine; tra parentesi il
     valore con le sole proposte, se diverso): vedi l'effetto di una rettifica
     prima di lanciare il comando. Respingere un'azione puo' rendere un rischio
     piu' urgente.
   - **Non si toccano** ID, colonne grigie e righe (niente righe inserite o
     cancellate). Se succede, `python esegui_ciclo_locale.py griglia` ricostruisce
     il foglio dalle proposte e conserva cio' che hai gia' scritto.

   Regole che lo script controlla (se non sono rispettate non applica niente
   e dice cosa correggere, con il numero di riga):
   - per un rischio: intero da 1 a 5, e **non piu' di un punto** diverso dal
     trimestre precedente, anche se e' la proposta di A1 che lasci com'e' (in quel
     caso va corretta: lo segnala la colonna Segnalazioni). La **Velocity** puo' restare vuota ("non valutata",
     n.v.: nessuna fonte ne documenta i tempi) e, se prima era vuota, puo'
     prendere qualunque valore;
   - **anni di adeguamento** di un rischio: la stima di A1 (vuota = non serve);
     cambiarla con un numero da 0 a 30. Il valore deciso va nell'anagrafica
     (Parametri, colonna M) e allunga la Y dell'urgenza; una stima vuota non
     cancella il numero gia' presente;
   - per un KRI: un numero (vuoto = non rilevato). Le **soglie** le fissa la
     Banca quando A1 non le ha (celle vuote, stato "Soglie da definire"):
     scriverle **entrambe**; la soglia di allerta deve restare maggiore o
     uguale a quella di attenzione, anche quando le ha proposte A1 (soglie
     invertite o una sola: correggerle, oppure respingere il KRI);
   - per un'azione: owner = una funzione aziendale, mai il nome di una
     persona (un owner proposto che sembra una persona va cambiato: lasciato
     com'e' non si accetta); orizzonte `3 mesi`, `6 mesi` o `12 mesi`;
   - per una notizia: segnale fra Peggiorativo, Migliorativo, Neutro, Non
     rilevante; rischio fra quelli del registro (nel radar o in osservazione) o
     `NON PRESIDIATO`;
   - decisione sullo stato: `Automatico`, `Radar` o `Osservazione`;
   - una cella cambiata, un Respingi o un ⚑ vogliono la Motivazione (almeno
     10 caratteri); Respingi accetta solo `Sì` o vuoto.
3. **Salvare e chiudere** il registro.
4. Nel Prompt dei comandi:

   ```
   python esegui_ciclo_locale.py valida --periodo 2026Q3 --validatore "Comitato Rischi"
   ```
   (per le notizie: `--periodo` e' il lunedi' della settimana, es. `2026-10-12`).
5. Si deve vedere `Validazione del periodo 2026Q3 applicata: 53 righe — accettate
   N, rettificate N (N valori cambiati), respinte N`, e il file
   `NFR_Registro_2026Q3_validato.xlsx` nell'archivio del ciclo. Le righe del
   periodo escono dal foglio Validazione; nel Registro, riga 4: "Ciclo
   validato". Per il ciclo corrente `valida` rigenera anche il report al
   comitato (`Report al comitato del ciclo 2026Q3 rigenerato: ...pdf`; la
   versione precedente resta con la data nel nome); con `--senza-report` no.

Cosa succede ai dati: il valore rettificato sostituisce quello proposto nel
registro (colonna Validazione = "Rettificato"), e l'esito e le Variazioni del
rischio si riallineano ai valori validati (una rettifica che cambia un valore
compare come variazione con la tua motivazione; una rettifica che lo riporta
al trimestre prima toglie la variazione proposta dall'agente); un KRI respinto
esce di vigore; il valore di un KRI inserito da te riceve data e fonte della
rilevazione; un'azione accettata diventa "Approvata", una respinta "Respinta";
una notizia respinta non conta piu' nei segnali netti. La baseline per il trimestre
dopo e il file `Righe_liste_<ciclo>.json` si aggiornano da soli con i valori
validati.

## 3-bis. Dismettere un rischio (solo su decisione della funzione di rischio)

> **Dall'app**: pulsante **Dismetti** (capitolo "L'app NFR", sezione "Pulsante Dismetti"). Qui sotto il dettaglio: cio' che l'app fa per te e i comandi per chi lavora dal Prompt dei comandi.

Quando un rischio non va piu' seguito (per esempio e' venuta meno la causa), che sia
nel radar o in osservazione:

```
python esegui_ciclo_locale.py dismetti --rischio NFR-04 --motivazione "Sedi spostate fuori dalle aree a rischio" --decisore "Comitato Rischi"
```

Si deve vedere `Rischio NFR-04 dismesso: ...`. Il rischio esce dall'anagrafica
(e quindi dal report, dallo Storico e dai prossimi cicli), i suoi KRI escono di vigore, le
sue azioni aperte diventano "Annullata"; la sua storia resta nel registro e
l'atto (chi, quando, perche') e' in `Archivio_Cicli\Dismissioni\`.
**Non cancellare mai a mano una riga dell'anagrafica** in Parametri: una riga
vuota in mezzo fa sparire dalle viste l'ultimo rischio.

## 3-ter. Cambiare un ciclo gia' validato: riaprire la validazione, correggere i testi (D-76)

> **Dall'app**: pulsante **Riapri un ciclo**; per i testi **Admin** -> **Testi a mano** (capitolo "L'app NFR", sezioni "Pulsante Riapri un ciclo" e "Pulsante Admin"). Qui sotto il dettaglio: cio' che l'app fa per te e i comandi per chi lavora dal Prompt dei comandi.

Fra un ciclo e l'altro la funzione di rischio puo' dover cambiare qualcosa gia'
validato: un punteggio, una soglia, l'owner di un'azione, la decisione sullo stato
di un rischio. Si **riapre la validazione** del ciclo corrente e si valida di nuovo,
con la stessa griglia della sezione 3, **quante volte serve**.

1. Registro chiuso, poi:

   ```
   python esegui_ciclo_locale.py riapri
   ```
   Si deve vedere `Validazione del ciclo 2026Q4 RIAPERTA: rischi N, KRI N, azioni N`
   (i rischi sono quelli del radar e quelli in osservazione). Per riaprire solo alcuni
   rischi (con i loro KRI e le loro azioni): `riapri --rischi NFR-02,NFR-14`.
2. Nel foglio **Validazione** il grigio e' ora il **valore validato** (non una
   proposta) e la cella gialla contiene lo stesso valore; il titolo di ogni sezione
   dice RIAPERTURA. Si lavora come nella sezione 3:
   - una riga non toccata **resta com'e'** (nessun dato cambia);
   - un valore cambiato va motivato (almeno 10 caratteri, con l'evidenza); per i
     punteggi dei rischi **non c'e' il limite di un punto** (scelta dell'utente del
     07/10/2026): la motivazione e lo storico rendono conto del salto;
   - **Respingi = Sì** toglie un KRI (esce di vigore) o **annulla** un'azione; un'azione
     rettificata (owner, orizzonte) resta Approvata o In corso;
   - la **decisione sullo stato** porta un rischio in osservazione nel radar (`Radar`) o
     ne toglie uno (`Osservazione`): `valida` lo sposta subito (anagrafica, KRI fuori
     vigore per chi esce);
   - score e margine di Mosca si ricalcolano mentre scrivi.
3. Salvare, chiudere e lanciare `python esegui_ciclo_locale.py valida --periodo
   <ciclo> --validatore "<chi decide>"`. Nello storico (foglio
   Storico_Validazioni) le decisioni hanno il suffisso **(riapertura)**:
   Invariato, Rettificato o Respinto, con il valore di prima, quello deciso, la
   motivazione, chi e quando. Baseline, knowledge di A7 e report al comitato
   (PDF rigenerato da `valida`) seguono da soli. `riapri` lascia nella cartella
   del ciclo `Riapertura_<ciclo>.json` (chi ha riaperto, quando, che cosa);
   `valida` lo chiude con la data e chi ha validato.

Finche' la riapertura non e' validata il ciclo risulta "da validare": `trimestrale`,
`report` e `schede` aspettano. Per chiuderla senza cambiare niente basta lanciare
`valida` subito. Non serve per un rischio nuovo: lo censisce A1 al ciclo dopo (con un
messaggio della sezione 8 se serve); un rischio si toglie con `dismetti` (sezione
3-bis).

**Testi corretti a mano** (D-90: in modalita' Admin). Per correggere la forma di un testo di un ciclo validato, a
riapertura chiusa, si scrive direttamente nel foglio dati, nelle sole colonne di testo: RiskRegister **Descrizione** e
**Razionale** (lasciando le etichette RISCHIO:, IMPATTO:...); KRI **Nome**, **Unita**,
**Fonte_Dati**, **Razionale**, **Nota_Rilevazione**; Azioni **Descrizione** e
**Razionale**; RiskRegister **Segnale_Avvicinamento** dei rischi in osservazione. Mai
ID, numeri, date, Validazione, Stato o righe intere (i valori passano
dalla riapertura). Dall'app: **Admin** -> **Testi a mano**. Dal Prompt dei comandi, nella cartella degli script:

```
python amministrazione.py --admin testi --motivo "refuso nella descrizione di NFR-03"
```

che controlla il ciclo (validato, nessuna riapertura aperta) e mette una **copia** del registro nel parcheggio con
l'atto (chi, quando, perche'); poi si apre il registro, si corregge, si salva e si chiude, e:

```
python amministrazione.py --admin testi-fine
```

che scrive nell'atto l'impronta del registro corretto e rifa' baseline, allegato di A1, knowledge di A7 e report. Se il
registro non e' cambiato l'atto dice "senza modifiche". La correzione si annulla con **Annulla** (`annulla
--parcheggio <nome>`), finche' nessuno scrive nel registro: torna il registro di prima e baseline e report si rifanno.

## 3-quater. Amministrazione dell'archivio e del registro (modalita' Admin, tappa M5)

> **Dall'app**: pulsante **Admin** (capitolo "L'app NFR", sezione "Pulsante Admin"). Qui sotto il dettaglio: cio' che l'app fa per te e i comandi per chi lavora dal Prompt dei comandi.

Per ripulire l'archivio, tornare a un ciclo validato o ricominciare da zero dopo i cicli di prova. **Niente si
cancella subito**: cio' che un'operazione toglie va in un **parcheggio**, `Archivio_Cicli\_Parcheggio\<data_ora>_<operazione>\`,
con un atto (`atto.json`: chi, quando, perche', chi ha deciso, ogni file) e una traccia in `Archivio_Cicli\Amministrazione\`.
Ogni operazione **si annulla** rimettendo a posto il suo parcheggio. Le funzioni si usano solo in **modalita' Admin**
(D-85): nell'app il pulsante **Admin...** accanto ad Altro apre la finestra delle operazioni (sezione "Pulsante
Admin"), dopo una conferma che lascia la traccia di chi l'ha aperta e quando; chiuderla spegne la modalita' Admin.
Dal Prompt dei comandi, nella cartella degli script, l'opzione `--admin` va scritta prima del comando:

| Operazione | Comando | Che cosa fa |
|---|---|---|
| Nuovo registro (primo uso, ambiente di prova) | `python esegui_ciclo_locale.py inizializza --ciclo-precedente 2025Q4 --settimana 2026-01-05`, poi `python esegui_ciclo_locale.py baseline` | il primo registro, vuoto, se non c'e' ancora (guida, 0.4); il ciclo dopo `--ciclo-precedente` e' il primo da valutare |
| Parcheggi | `python amministrazione.py --admin parcheggi` | elenca i parcheggi: operazione, quando, chi, quanto spazio, stato (attivo, annullato) |
| Pulizia | `python amministrazione.py --admin pulizia` (anteprima), poi `python amministrazione.py --admin pulizia --esegui` | sposta nel parcheggio i tentativi dei cicli validati, i backup oltre gli ultimi `backup_da_tenere` (10), le versioni precedenti dei report, `In_arrivo\Originali` e `Precedenti` dei periodi chiusi, i log e le verifiche del PC piu' vecchi di `giorni_log` (90). L'anteprima dice cosa, perche' e quanto spazio |
| Ritorno a un ciclo validato | `python amministrazione.py --admin ritorno --ciclo 2026Q3 --motivo "..." --decisore "..." --conferma 2026Q3` | il registro torna quello di fine validazione del ciclo (`Cicli\2026Q3\<registro>_2026Q3_validato.xlsx`, l'ultima validazione anche dopo una riapertura). Nel parcheggio: il registro di adesso, le cartelle dei cicli e straordinari dopo, le settimane scritte o validate dopo la validazione del ciclo, la baseline, gli allegati, la knowledge di A7 e le risposte degli agenti di quei periodi; poi `baseline` li rigenera. Lo stato dell'app riparte da "Ciclo 2026Q3: VALIDATO". Le settimane uscite dal registro sono elencate con il comando per riscriverle (`settimanale --payload` dal loro `A3_<lunedi'>.json` nel parcheggio). Il ciclo deve essere validato, con il suo Excel validato e della stessa versione del template; motivo di almeno 20 caratteri e decisore obbligatori |
| Annulla | `python amministrazione.py --admin annulla --parcheggio <nome> --motivo "..."` | rimette a posto un parcheggio. Per un ritorno o una ripartenza **solo se nel frattempo nessuno ha scritto nel registro** (impronta uguale a quella lasciata dall'operazione): altrimenti si ferma senza toccare niente. Cio' che occupa i posti (il registro tornato, la baseline rigenerata) va in un parcheggio nuovo, "annullamento" |
| Testi a mano | `python amministrazione.py --admin testi --motivo "..."`, poi (corretto e chiuso il registro) `python amministrazione.py --admin testi-fine` | solo con il ciclo corrente validato e nessuna riapertura aperta: una copia del registro nel parcheggio con l'atto; dopo la correzione l'impronta del registro corretto nell'atto, poi baseline e report. Si annulla come un ritorno (sezione 3-ter) |
| Ripartenza da zero | `python amministrazione.py --admin ripartenza --motivo "..." --decisore "..." --ciclo-precedente 2026Q3 --conferma NFR_Registro.xlsx` | il vecchio registro e l'archivio dei cicli (cicli, settimane, backup, In_arrivo, baseline, allegati, knowledge di A7) nel parcheggio; poi un registro nuovo vuoto (`inizializza`, con la settimana di oggi o `--settimana`) e la baseline. Restano i log, le verifiche del PC, i parcheggi e la traccia. Le notizie di `News_Inbox` non si toccano |
| Svuota | `python amministrazione.py --admin svuota` (anteprima), poi `python amministrazione.py --admin svuota --esegui` | cancella **per sempre** i parcheggi piu' vecchi di `giorni_parcheggio` (30); l'elenco di cio' che si cancella resta nella traccia |

Ogni operazione che scrive prende il lucchetto del registro (sezione 0.3, "Piu' analisti"); il registro deve essere
chiuso. La `--conferma` va scritta uguale al ciclo (ritorno) o al nome del file del registro (ripartenza): un nome
diverso ferma prima di toccare qualcosa. Un ritorno cambia la storia del registro: va deciso dalla funzione di rischio
e motivato (governance: `04_Riferimenti/controlli_e_model_risk.md`, "Storia riscritta"). La modalita' Admin non e'
una protezione informatica (chiunque usi l'app puo' accenderla): la protezione e' che niente si cancella subito, che
ogni operazione lascia l'atto e che accendere l'Admin lascia la traccia.

## 4. Leggere i risultati

**Il report al comitato** esce in due forme, dallo stesso registro validato (D-83, tappa M4), nella cartella del ciclo
`Archivio_Cicli\Cicli\<ciclo>\`:
- `Report_comitato_<ciclo>.pdf`: i fogli da Quadro a Metodologia del registro;
- `Report_comitato_<ciclo>.html`: lo stesso report da aprire nel browser (doppio clic), un file unico che non scarica
  niente da internet. Ha il menu delle pagine (Quadro, Classifica, Radar di Mosca, Matrice, Delta, Rischi in
  osservazione, Metodologia), **le schede di tutti i rischi** (un clic sull'ID di un rischio, ovunque, apre la sua
  scheda) e una guida; passando sui grafici compaiono i numeri; il comando Stampa del browser mette ogni pagina su un
  foglio. In testa ciclo, data dei dati, data della validazione e validatore. A richiesta, chi mantiene il
  pacchetto lo fa anche con le viste di lavoro (Registro, Storico, Indicatori, Notizie, Piano azioni, Osservazione,
  Validazione, Parametri, Dizionario; sezione 9).

Prima di scrivere l'HTML lo script confronta i suoi numeri (X, Y, Z, margine, urgenza, livello di allerta, segnali
netti, ordine della classifica, Delta) con quelli calcolati da Excel nel registro (**cancello**): se anche uno non
torna l'HTML non esce, il PDF si', e l'uscita del comando dice quali numeri non tornano (da mandare a chi mantiene il
pacchetto). L'elenco dei report di tutti i cicli e' `Archivio_Cicli\Cicli\Indice_report.html`. Le pagine qui sotto
sono i fogli del registro; nell'HTML hanno lo stesso nome e lo stesso contenuto.

| Dove | Cosa guardare |
|---|---|
| **Quadro** | la prima pagina per il comitato: cinque numeri (rischi valutati, **livello di allerta** — quanti in attivazione e in attenzione —, variati e nuovi fra i rischi del radar, con sotto entrati, usciti e in osservazione, KRI in rosso, validazione), i primi cinque rischi, la matrice di gravita', il radar di Mosca; a pagina 2 il **commento di A1** (messaggio e decisioni), i controlli (con la sintesi di A5, se usato), quante **segnalazioni da motivare** sono andate in validazione e **i rischi segnalati con il perche'**, calcolato dal foglio. |
| **Classifica** | i rischi dal piu' alto per score composito; colore della barra = urgenza (rosso = agire ora). A destra, la **lente di Mosca**: per ogni rischio, dal piu' in ritardo, la colonna e' il tempo necessario (X + Y), il rombo il tempo disponibile (Z); la parte rossa sfora. |
| **Matrice** | ogni rischio nella cella della sua probabilita' e del suo impatto; verde, ambra, rosso secondo P x I. Dice la gravita', non l'urgenza. |
| **Delta** | cosa e' cambiato dal trimestre prima: una barra per rischio e, a fianco, il motivo con l'evidenza; sotto, quanto vale un punto di ogni dimensione (con e senza Velocity). |
| **Fenomeni** | i **rischi in osservazione** (D-79): in testa quanti nel radar e quanti fuori; poi dal piu' alto per score, con le quattro dimensioni, il **perche' sono fuori dal radar** (quale soglia manca, o la capienza), l'orizzonte e il segnale che li porterebbe nel radar; in fondo chi e' **entrato o uscito** dal radar nel ciclo. |
| **Metodologia** | pesi e parametri in vigore, scale della rubrica, come si leggono i grafici. |
| Schede (file a parte) | una scheda per rischio, nell'ordine della Classifica: il rischio e il razionale in termini di rischio, perche' di ogni punteggio con i documenti, urgenza, cosa e' cambiato, andamento negli ultimi trimestri, fonti e a cosa servono, azioni e KRI con perche' ed effetto atteso (D-68). |
| Registro, righe 4 e 5 | "Ciclo validato" o quante righe restano da validare; "Ciclo completo". Se dice CICLO INCOMPLETO, i numeri non sono affidabili. |
| Registro, tabella | un rischio per riga, dal piu' alto per score; il **fondo dell'ID** e' il colore del livello di allerta: le dimensioni (Vel "n.v." = non valutata), score, variazione sul trimestre prima e su 6 mesi, urgenza, ◆ (attenzione del supervisore), KRI rossi/ambra/verdi, segnali netti delle notizie, **presidio** dei controlli (giudizio della Banca), **rilievi** di A5 e dei controlli (⚑ = da motivare in validazione), owner. |
| **Radar_Mosca** | **quanto presto bisogna agire**: piu' il cerchio di un rischio e' vicino al centro, prima bisogna agire; dentro il cerchio rosso "Mosca" si e' gia' in ritardo (colonna Urgenza = "AGIRE ORA"); i cerchi grigi indicano 1, 2 e 3 anni di margine. **Area del cerchio del rischio** = probabilita' x impatto; **colore** = livello di allerta: **rosso Attivazione** (almeno due fra AGIRE ORA, un KRI in rosso, notizie in peggioramento: al comitato con un piano), **giallo Attenzione** (uno di questi, oppure margine sotto l'anno con P x I alta, presidio assente o KRI in ambra: l'owner verifica azioni e KRI), **verde Monitoraggio**; il motivo e' nelle colonne U-AB. **◆** accanto all'ID = tema all'attenzione del supervisore (BCE, EBA, Banca d'Italia). Il settore dice la **categoria di rischio** della tassonomia interna della Banca (nove, D-74); un rischio fuori perimetro (FP) o non ancora riclassificato non compare. |
| Storico | score di ogni rischio negli ultimi otto trimestri. |
| Indicatori | a sinistra gli indicatori in vigore, con il **tipo** (esposizione: quanto la Banca e' esposta; evoluzione: quanto cresce il fenomeno), lo stato (Verde/Ambra/Rosso, "Soglie da definire" finche' la Banca non le fissa) e tendenza; a destra la storia di un indicatore: sceglierlo in N4. |
| Notizie | pressione delle notizie per categoria di rischio; "AREA NON PRESIDIATA" (nessun rischio nel registro) o "In osservazione" (nessuno nel radar, almeno uno in osservazione); a destra la sintesi di A3 della settimana corrente, i flag proposti (anche sui rischi in osservazione) e quante notizie toccano i rischi in osservazione (la storia di tutte le settimane e' nel foglio Sintesi_Settimane). |
| Piano_azioni | tutte le azioni: prima quelle da decidere, poi approvate, in corso, completate, con la scadenza. |
| Osservazione | i rischi in osservazione con tutti i testi (dimensioni, score, perche' fuori dal radar, orizzonte, segnale, meccanismo, validazione), le notizie che A3 ha collegato a ognuno nelle ultime 4 settimane, chi e' entrato o uscito dal radar e, a destra, dove si concentrano: per driver e categoria accanto ai rischi del radar con lo stesso incrocio (una casella piena sopra e vuota sotto = tema che il radar non gestisce). La storia: foglio RiskRegister, colonne Stato e Movimento. |
| Dizionario | ogni dato del workbook: chi lo scrive, cosa significa, come si calcola, un esempio. |
| Validazione | le righe ancora da validare (vuoto = tutto validato). In testa al foglio: come si valida e i criteri per decidere. |
| Storico_Validazioni | cosa e' stato accettato, corretto, respinto, campo per campo, da chi, quando e perche'. |
| Riga 1 e 2 di ogni foglio | la **fascia blu** con ciclo, data, "validato" o "da validare"; la **guida**: chi aggiorna il foglio (azzurro = ciclo trimestrale, verde = settimanale, giallo = validatore, grigio = calcolo), cosa contiene, come si legge. Nelle tabelle dati le righe 3 e 4 dicono chi scrive e cosa significa ogni colonna. Il foglio Guida ha la tabella "chi aggiorna cosa". In fondo ai fogli del report, la legenda delle abbreviazioni. |

Come si calcola l'urgenza (disuguaglianza di Mosca): bisogna agire ora se
**X + Y > Z**, dove Z = anni prima che il rischio possa manifestarsi (dalla
Prossimita'), X = tempo per decidere e avviare (un trimestre), Y = tempo per
completare le azioni proposte (il loro orizzonte) oppure, se maggiori, gli
**anni di adeguamento** dell'anagrafica (stimati da A1 e decisi in validazione;
sezione 6). Z e' la meta' della fascia della Prossimita: 5 → 0 anni, 4 → 0,5,
3 → 1,5, 2 → 2,5, 1 → 3,5.
Dettagli e limiti: `01_Kernel/rubrica_scoring.md`, sezione 8.

Lo **score composito** e' la media pesata delle dimensioni valutate: 0,35 x
Impatto + 0,25 x Probabilita + 0,20 x Prossimita' + 0,20 x Velocity; se la
Velocity non e' valutata, lo stesso calcolo sulle altre tre con i pesi
ridistribuiti (decisione D-50; pesi nelle celle gialle di Parametri). Il
presidio dei controlli, gli anni di adeguamento e la rilevanza delle fonti non entrano nello score.

### Chiedere il perche' ad A7 (D-72)

Per capire una valutazione non serve aprire niente: si apre l'agente **A7
Assistente del registro** e si fanno domande, per esempio "perche' NFR-01 ha
Prossimita 5?", "perche' NFR-11 e' AGIRE ORA?", "perche' il tema X dei documenti
non e' un rischio?". Nessun file da allegare: A7 legge la cartella
`Kernel\Spiegazioni`, che `trimestrale`, `valida` e `dismetti` riscrivono da soli
(`Ciclo.txt` e un file per ogni posto dell'anagrafica, `Rischio_01.txt` ...
`Rischio_20.txt`, sempre gli stessi). Nelle risposte distingue cio' che e'
**registrato** (motivazioni di A1, decisioni del validatore), cio' che e'
**calcolato** (score, urgenza, livello) e la **sua lettura** dei documenti; non
propone valori nuovi. Per i temi non censiti usa il motivo che A1 ha registrato
(i "fenomeni considerati e non censiti") e i rischi in osservazione. Alla fine si puo' chiedere "sintesi per
il Quadro": un testo di al massimo 600 caratteri da incollare nella cella gialla
**Note dell'analista** della prima pagina del Quadro; il PDF del report la
mostra, e al ciclo dopo `trimestrale` la archivia nel foglio Sintesi_Cicli.
I nomi dei file non cambiano mai: un rischio appena censito entra in un
file che esiste gia', e A7 lo vede subito (solo alla prima installazione la cartella
puo' entrare nella knowledge il giorno dopo). A7 spiega soltanto: i valori si cambiano riaprendo la validazione e
i testi con Admin -> Testi a mano (sezione 3-ter). Copione di prova: `04_Riferimenti/Prove/Prova_A7.md`, con il confronto fra
A7 che legge i file di testo e una copia di prova che legge solo il registro Excel.

## 5. Dove sono i file

| Cosa | Dove |
|---|---|
| Registro vivo | `Report_Trimestrali\NFR_Registro.xlsx` |
| Excel di ogni trimestre (congelato) | `Archivio_Cicli\Cicli\<ciclo>\NFR_Registro_<ciclo>.xlsx` e `..._validato.xlsx` |
| Schede dei rischi del trimestre | `Archivio_Cicli\Cicli\<ciclo>\Schede_<ciclo>.xlsx` (con `Input_A6_<ciclo>.json` e `A6_<ciclo>.json`) |
| Excel di ogni settimana | `Archivio_Cicli\Settimane\<lunedi'>\NFR_Registro_<lunedi'>.xlsx` |
| Output degli agenti, esiti dei controlli, decisioni di validazione | nella stessa cartella del ciclo o della settimana |
| Ogni tentativo fermato | `Archivio_Cicli\Cicli\<ciclo>\tentativo_<data_ora>\` |
| Copia del registro prima di ogni scrittura | `Archivio_Cicli\Backup\` |
| Allegati per gli agenti (D-84) | `Archivio_Cicli\`: `Input_A1_<ciclo>.txt`, `Input_A8_<periodo>.txt`, `Input_A3_A4.txt`, `Input_A5_<ciclo>.txt`; `Input_A6_<ciclo>.json` nella cartella del ciclo. L'app li copia in `%USERPROFILE%\NFR_Da_allegare\<agente>\` |
| Risposte degli agenti prese dall'app | `Archivio_Cicli\In_arrivo\` (il testo incollato in `Originali\`, le versioni di prima in `Precedenti\`); pareri di A4 in `Archivio_Cicli\Pareri\` |
| Log dei comandi lanciati dall'app; chi sta scrivendo | `Archivio_Cicli\Log\`; `Archivio_Cicli\_Lucchetto\` (con `sblocchi.log`) |
| Prompt in uso nel ciclo; traccia di una riapertura | `Archivio_Cicli\Cicli\<ciclo>\Prompt_in_uso\`; `Riapertura_<ciclo>_<ora>.json` |
| Notizie raccolte | `News_Inbox\<lunedi'>\` |
| Report al comitato | `Archivio_Cicli\Cicli\<ciclo>\Report_comitato_<ciclo>.pdf` e `.html` (le versioni precedenti con data e ora nel nome); l'elenco di tutti: `Archivio_Cicli\Cicli\Indice_report.html` |
| Verifiche del PC | `Archivio_Cicli\Verifiche_PC\` |
| Parcheggi e traccia dell'amministrazione | `Archivio_Cicli\_Parcheggio\` (con `atto.json` in ognuno), `Archivio_Cicli\Amministrazione\` |

## 6. Cambiare le regole (solo su decisione della funzione di rischio)

Kernel e prompt sono una cosa sola: i file di `01_Kernel` sono copiati dentro le
istruzioni degli agenti da `componi_prompt.py`. Modificare un file del kernel
sul PC, da solo, **non cambia niente negli agenti**, e il prossimo
aggiornamento del pacchetto lo sovrascrive. Una modifica decisa dalla funzione
di rischio va quindi data a chi mantiene il pacchetto, che la riporta nella sua
copia, ricompone i prompt, rilancia il collaudo e consegna un pacchetto in cui
c'e' gia'.

| Cosa | Dove si cambia | Poi |
|---|---|---|
| Descrittori degli score, regole di variazione | `01_Kernel/rubrica_scoring.md` | chi mantiene il pacchetto rilancia `02_Agenti/componi_prompt.py` e il collaudo, poi ricarica i prompt negli agenti |
| Categorie di rischio, driver | `01_Kernel/tassonomia_nfr.md` (dal 07/10 le nove categorie in perimetro della tassonomia interna, `04_Riferimenti/Tassonomia dei Rischi.csv`, D-74) | come sopra, piu' `03_Excel/genera_dashboard.py`; se cambiano i **codici** (9.n, DRV-...) anche lo schema di A1, la mappa e i dati del collaudo, e poi `aggiorna-registro` |
| Elenco delle fonti | `01_Kernel/fonti.md` (una voce per fonte, stato "approvata" o "esclusa") | come sopra |
| Pesi, soglie, parametri dell'urgenza (X, Y di riserva, anni per Prossimita') | celle gialle del foglio Parametri del registro | niente: il registro si ricalcola da solo |
| Regola del radar (D-79): capienza (fino a 20), soglie di Prossimita e Probabilita, cicli prima di uscire | registro vivo, foglio Parametri, righe 66-69 (celle gialle; il massimo di 20 in osservazione e' fisso) | vale dalla scrittura del ciclo dopo o dalla prossima `valida`: lo stato si ricalcola li' |
| Anni di adeguamento di un rischio (es. una migrazione che richiede 3 anni) | di norma in validazione (cella gialla "Anni adeg." della riga del rischio, sezione 3: la stima di A1); a mano, se serve, nel registro vivo, foglio Parametri, colonna M dell'anagrafica | niente: la scrittura dei cicli lo conserva; per il PDF, rilanciare `report` |
| Tema all'attenzione del supervisore (BCE, EBA, Banca d'Italia) | registro vivo, foglio Parametri, colonna N dell'anagrafica: "Sì" o "No" | niente: compare ◆ accanto all'ID (sezione 4); la scrittura dei cicli lo conserva |
| Soglie del livello di allerta (P x I alta, quota di KRI in ambra o rosso, margine stretto, segnali forti per l'Attivazione) | registro vivo, foglio Parametri, righe 60-63 (celle gialle) | niente: radar, Registro e Quadro si ricalcolano |
| Presidio dei controlli di un rischio (giudizio della Banca) | registro vivo, foglio Parametri, colonna O dell'anagrafica: Non verificato, Adeguato, Parziale, Assente | niente: non entra nello score; la scrittura dei cicli lo conserva. Gli agenti non vedono i controlli interni: se non lo indichi resta "Non verificato" |
| Avanzamento di un'azione approvata | registro vivo, foglio Azioni, colonna Stato: "In corso" o "Completata" (unica colonna dei dati da toccare a mano) | niente: un'azione Completata non passa piu' ad A1 come aperta |
| Note dell'analista del ciclo (per esempio la sintesi delle spiegazioni di A7) | registro vivo, foglio Quadro, cella gialla in prima pagina (D-72) | niente; per il PDF rilanciare `report`. A un ciclo nuovo `trimestrale` la sposta nel foglio Sintesi_Cicli e la svuota |

## 7. Se qualcosa va storto

| Messaggio | Cosa vuol dire | Cosa fare |
|---|---|---|
| `'python' non e' riconosciuto come comando interno o esterno` | Python non e' installato, o non e' nel percorso di sistema | chiedere all'informatica; in alternativa provare `py` al posto di `python` |
| Il registro e' danneggiato o si vuole tornare indietro | ogni scrittura lascia la copia precedente in `Archivio_Cicli\Backup\`; in piu' c'e' la cronologia versioni di SharePoint | per tornare a un ciclo validato, il **ritorno** dell'Amministrazione, in modalita' Admin (sezione 3-quater), che parcheggia tutto e si annulla; per un danno dell'ultima scrittura, ripristinare la copia di `Backup`, poi rilanciare il comando |
| Agent Builder disattivato o cambiato | gli agenti non scrivono nulla: il registro resta integro | ricreare gli agenti (sezione 0.2) con le istruzioni archiviate |
| Il PC dell'analista non e' disponibile | lo script gira su qualunque PC con Python, pywin32, Excel e le cartelle sincronizzate | ripetere la sezione 0.3 su un altro PC |
| `can't open file ... esegui_ciclo_locale.py` | il Prompt dei comandi non e' nella cartella degli script | rifare il `cd` verso la cartella degli script |
| `No module named 'win32com'` | manca pywin32 | `installa.cmd` (sezione 0.3), oppure `pip install pywin32` |
| `installa.cmd`: `NO: mancano ancora ...` dopo pip | pip non ha potuto scaricare i pacchetti (proxy, certificati) o la cartella `pacchetti` e' di un altro Python | il messaggio dice la strada: cartella `pacchetti` scaricata su un PC con la rete libera con lo stesso Python, oppure l'IT |
| `installa.cmd`: `ATTENZIONE: attivita' non creata` o collegamento non creato | le regole del PC non lasciano creare attivita' pianificate o collegamenti all'utente | a mano: sezione "Raccolta notizie automatica" e tasto destro -> Invia a -> Desktop; oppure l'IT |
| `No module named 'openpyxl'` (comando `schede`) | manca openpyxl | `pip install openpyxl` |
| `No module named 'pythoncom'` (spesso dentro `ERRORE TECNICO`) | pywin32 installato a meta' | `python -m pip install --upgrade --force-reinstall pywin32`, poi verificare con il comando del punto 1 della sezione 0.3. Se compare anche "No module named 'pywin32_postinstall'" tentando `python -m pywin32_postinstall -install`, ignorarlo: nelle versioni recenti di pywin32 (visto: 312) quel modulo non esiste piu' e non serve, basta il reinstall. |
| `ATTENZIONE: ... non raggiungibile` solo su **alcune** fonti (spesso stesso dominio), ma i siti si aprono nel browser | `urllib` da solo non legge il file di autoconfigurazione del proxy (PAC) che il browser usa; quelle fonti vanno instradate sul proxy | verificare `pip show pypac` (deve essere installato: punto 1 della sezione 0.3); se manca, `pip install pypac` e rilanciare |
| `ATTENZIONE: ... non raggiungibile` su **tutte** le fonti, e i siti non si aprono nemmeno nel browser | proxy o firewall aziendale blocca davvero l'uscita | chiedere all'IT l'indirizzo del proxy (o un'eccezione per i siti dell'elenco fonti); non e' un problema che lo script possa risolvere da solo |
| `FERMATO` ... `file non trovato` | il nome del file dell'agente e' scritto male, o il file e' in un'altra cartella | controllare nome ed estensione (Blocco note a volte aggiunge `.txt`: salvare con tipo "Tutti i file") |
| `FERMATO` ... `non e' un JSON valido` | nel file c'e' anche testo dell'agente, o manca un pezzo | risalvare copiando solo da `{` a `}` (UTF-8, con o senza BOM va bene), oppure chiedere all'agente "Rispondi solo con il JSON" |
| `non conforme allo schema` subito dopo aver salvato un JSON | il JSON e' leggibile ma non ha i campi o i valori previsti | chiedere all'agente di rispondere rispettando lo schema, o rilanciarlo |
| `Precontrollo dell'output di A1 (...): N punti da correggere` | lo script ha trovato nell'output di A1 errori che fermerebbero il ciclo (C1-C9 o schema) | sezione 2, punto 5-bis; il registro non e' stato toccato |
| `Precontrollo dell'output di A1 (...): 0 punti da correggere, ..., N rischi con testi troppo corti (C10)` | A1 e' stato troppo sintetico: descrizioni, parti del razionale, azioni o KRI sotto le lunghezze minime della guida di scrittura (D-86) | conviene dare ad A1 il messaggio di correzione nella stessa chat perche' li allunghi (l'app lo propone); si puo' anche proseguire: in validazione restano Osservazioni |
| `Baseline non trovata: ...Baseline_corrente.json` (comando precontrollo) | non e' ancora stata scritta la baseline nella cartella di uscita | `python esegui_ciclo_locale.py baseline`, poi ripetere il precontrollo |
| `Avviso: nel kernel ... mancano controlli_A5.md ...` | nella library Kernel mancano i file nuovi del 02/10 | sezione 0-bis, punto 1, poi rilanciare `baseline` |
| `L'esito di A5 ... e' del ciclo ...` / `cita rischi che non sono nell'output di A1` | il file di A5 non e' quello di questo output di A1 (vecchio o di un altro run) | rifare A5 allegando l'output di A1 appena salvato |
| `id_notizia ripetuti` | A3 ha dato lo stesso id a due notizie | chiedere ad A3 di correggere |
| `ATTENZIONE: l'anagrafica ha N posti liberi` | ci si avvicina al numero massimo di rischi del template (20) | avvisare chi mantiene il pacchetto prima del prossimo rischio nuovo |
| `Nota: --procedi-con-rilievi ... non serve piu'` | l'opzione e' rimasta in un comando gia' in uso (D-56, superata da D-71) | niente: i rilievi di A5 vanno sempre in validazione; si puo' togliere con `--motivo` e `--decisore` |
| `Ciclo da rivedere (difetti che renderebbero incoerente il registro)` | l'output di A1 ha un difetto di integrita' (C1, C2, C7, identificativi dei KRI) | sezione 2, punto 8 |
| `il rischio ha segnalazioni da motivare` (comando valida) | quel rischio (⚑ davanti al nome) ha una segnalazione DA MOTIVARE nella colonna Segnalazioni | nel foglio Validazione scrivere la Motivazione nella sua riga, anche se i valori restano quelli proposti |
| `proposta di A1 non accettabile (... piu' di un punto dal ciclo precedente ...)` (comando valida) | A1 ha proposto un salto di due o piu' punti (segnalazione C3) e la riga e' rimasta com'era | scrivere nella cella gialla un valore a non piu' di un punto, con la Motivazione |
| `Owner ... sembra il nome di una persona` (comando valida) | l'azione ha come owner una persona | scrivere nella cella gialla Owner il nome della funzione aziendale, con la motivazione |
| `Il registro ha righe 'Da decidere' su campi che il modello non ha piu'` (comando aggiorna-registro) | registro molto vecchio con righe da validare su Severity, Confidence o Gap_Controlli; se il messaggio dice `(None, None)` e periodi `['None']`, sono invece righe **vuote** della tabella dello storico con Stato "Da decidere" (visto in Banca il 06/10) | campi vecchi: validarle con il pacchetto con cui sono state scritte. Righe vuote: con il registro chiuso farne una copia, poi nel foglio dello storico delle validazioni eliminarle (tasto destro → Elimina → Righe della tabella). Poi rilanciare aggiorna-registro |
| `Il foglio Validazione non corrisponde alle proposte del periodo` | nel foglio Validazione e' stata cancellata o inserita una riga, o cambiato un ID | `python esegui_ciclo_locale.py griglia` (ricostruisce il foglio, conserva cio' che e' gia' scritto nelle righe intatte), poi rilanciare valida |
| `Le notizie da validare (N...) superano le ... righe del foglio Validazione` (comando settimanale) | molte settimane di notizie non sono ancora state validate | validare le settimane piu' vecchie (`valida --periodo <lunedi'>`: una riga non toccata vale come accettata), poi rilanciare; niente e' stato scritto |
| `... superano le ... righe della vista` / `Anagrafica piena` | e' stata raggiunta una capacita' del template; niente e' stato salvato | chi mantiene il pacchetto rigenera il template con capacita' piu' alte |
| `Manca ...\Kernel\mappatura_campi.json` (o un altro file del kernel) | i file di `01_Kernel` non sono stati copiati nella cartella `kernel` di `configurazione.json` (la library Kernel sincronizzata) | copiarli tutti (sezione 0-bis, punto 1) e rilanciare; niente e' stato scritto |
| `FERMATO ... Il registro e' in uso: <nome> (PC ...), comando ..., dal ...` | un collega sta scrivendo nel registro (D-83) | aspettare che finisca e rilanciare; il registro non e' stato toccato |
| `FERMATO ... Un collega ha iniziato a scrivere nello stesso momento` | due analisti hanno lanciato un comando quasi insieme | riprovare fra qualche minuto |
| `Il registro e' in uso` con un nome che non sta lavorando | il lucchetto e' rimasto (PC spento o comando interrotto a meta'); scade da solo dopo 2 ore | dopo aver sentito il collega: `python esegui_ciclo_locale.py sblocca --motivo "..."` (resta scritto in `_Lucchetto\sblocchi.log`) |
| `FERMATO ... e' cambiato mentre lo script lavorava` | un collega ha salvato il registro, o la sincronizzazione ha portato una versione nuova, mentre il comando girava | rilanciare il comando: riparte dal registro aggiornato |
| `FERMATO ... Il registro e' aperto in un programma di questo PC` | il registro e' aperto in Excel sul tuo PC | chiuderlo e rilanciare |
| `Workbook non trovato: None` | manca `configurazione.json` (c'e' solo `configurazione_esempio.json`), oppure la voce `workbook` e' vuota o assente | copiare `configurazione_esempio.json` in `configurazione.json` e compilare `workbook` (sezione 0.3, punto 3) |
| `Workbook non trovato: <percorso>` | quel percorso in `configurazione.json` e' sbagliato, o il registro non e' ancora stato creato | correggere il percorso, oppure creare il registro (sezione 0.4, "Primo utilizzo reale") |
| `Template non trovato: <percorso>...03_Excel\NFR_Dashboard_Template.xlsx` | manca il file nella cartella `03_Excel` del pacchetto (non e' configurabile in `configurazione.json`: lo script lo cerca sempre fianco a fianco a `07_Senza_Studio`); capita se il pacchetto e' arrivato incompleto (es. l'allegato `.xlsx` filtrato dalla posta) | dalla cartella `03_Excel`: `python genera_dashboard.py` lo rigenera sul posto (serve `openpyxl`: `pip install openpyxl`); in alternativa richiedere di nuovo il pacchetto completo |
| `FERMATO — il workbook non e' stato modificato` + elenco | i controlli hanno trovato difetti nell'output degli agenti | vedi sezione 2, punto 8; il registro e' intatto |
| `Il ciclo precedente ... non e' ancora validato` | manca la validazione del trimestre prima | fare la sezione 3 per quel trimestre |
| `Validazione del periodo ... NON applicata (N problemi...)` | alcune righe non rispettano le regole | correggere nel foglio Validazione le righe elencate (il numero di riga e' nel messaggio), salvare, chiudere, rilanciare |
| `Nessuna riga da validare per il periodo` | quel periodo e' gia' validato (o il periodo e' scritto male: `2026Q3`, `2026-10-12`) | niente, o correggere il periodo |
| `Il periodo ... ha N righe nel foglio Storico_Validazioni con lo Stato vuoto o modificato a mano` | la colonna Stato dello storico e' stata cancellata o cambiata in Excel | rimettere `Da decidere` in quelle celle (selezionarle, scrivere, Ctrl+Invio), salvare, chiudere, lanciare `python esegui_ciclo_locale.py griglia`, poi validare |
| `Nota: --accetta-il-resto non serve piu'` | l'opzione e' rimasta in un comando gia' in uso | niente: una riga non toccata vale gia' come accettata; si puo' togliere |
| `Codici fonte non nell'elenco` | A3 ha citato una fonte che non e' in `fonti.md` | chiedere ad A3 di correggere, o usare `MAN` per un file caricato a mano |
| `ERRORE TECNICO — il workbook non e' stato salvato` | problema tecnico prima di scrivere (es. Excel bloccato; lo script ha gia' riprovato ad avviare Excel cinque volte) | chiudere Excel, riprovare; se persiste, riavviare il PC e poi chiamare chi mantiene il pacchetto |
| il comando non finisce da oltre 10 minuti | di solito un altro programma tiene aperto il registro e Excel non riesce a salvarlo | chiudere gli altri programmi; da Task Manager chiudere i processi "Microsoft Excel" in background; controllare in `Archivio_Cicli\Backup\` l'ultima copia e rilanciare il comando (se il registro non risulta cambiato) |
| `... e' stato creato con un template precedente al 25/09/2026` (o `con un template versione ...`) | il registro e' nato da un template con un'altra struttura: lo script non lo scrive | sezione 0-bis: `python esegui_ciclo_locale.py aggiorna-registro` |
| `Aggiornamento NON applicato` + elenco | una verifica dell'aggiornamento non e' passata; il registro e' rimasto com'era | inviare il messaggio a chi mantiene il pacchetto |
| `... e' aperto (in Excel o dalla sincronizzazione)` durante aggiorna-registro | il registro non si puo' sostituire | chiuderlo (e attendere la fine della sincronizzazione di OneDrive), rilanciare |
| `Avviso: impaginazione del report non aggiornata` | lo script non ha potuto adattare le altezze delle righe con testi calcolati | niente per i dati, che sono scritti; prima di salvare il PDF, nel Quadro (pagina 2), nel Delta e nella pagina Fenomeni allargare a mano le righe con testo tagliato |
| `Output di A6 non coerente con i dati validati` + elenco | A6 ha saltato un rischio, cambiato o omesso una fonte, o scritto un numero che non sta nei dati | incollare l'elenco nella chat di A6 chiedendo di correggere, salvare di nuovo, rilanciare `schede`; nessun file e' stato scritto |
| `ERRORE TECNICO DOPO IL SALVATAGGIO` | il registro E' scritto, ma un file dell'archivio non si e' potuto copiare (di solito perche' aperto) | **non rilanciare**: chiudere il file aperto e copiare a mano il registro nella cartella del ciclo con il nome indicato |

## 8. Gli agenti: mansioni e messaggi da usare

Gli agenti si usano scrivendo in chat. Ognuno ha un **messaggio base** (quello
dei passi delle sezioni 1, 2 e 4) e alcune **variazioni** utili. Regole che
valgono per tutti:
- il messaggio **aggiunge** indicazioni per quella volta, non cambia le regole
  dell'agente: le istruzioni incollate in Agent Builder (sezione 0.2) restano in
  vigore. Una richiesta che va contro una regola (per esempio "alza la Prossimita
  senza fonte" o "salta i controlli") viene ignorata o rifiutata, ed e' giusto
  cosi': quelle regole sono la garanzia del processo;
- per rifare una valutazione usa una **chat nuova**: una chat che ha gia'
  risposto piu' volte sullo stesso lavoro tende a ritoccare la risposta di prima
  invece di rifarla;
- gli agenti che rispondono in JSON (A1, A3, A5, A6) devono dare **solo** il
  JSON. Se aggiungono testo: "Rispondi solo con il JSON, senza testo attorno";
- tra parentesi quadre le parti da sostituire (`[ciclo]`, `[NFR-nn]`...).

| Agente | Mansione | Quando | Cosa gli dai | Cosa restituisce |
|---|---|---|---|---|
| A1 Horizon Scanner | valuta i rischi: valori, fonti, motivazioni, azioni, KRI (solo per quelli del radar); censisce i rischi nuovi; registra i temi esaminati e non censiti; rivaluta i rischi in osservazione quando trova evidenza nuova | ogni trimestre (sezione 2) | allegato `Input_A1_<ciclo>.txt` nella chat; legge da solo `Analisi_Interne`, `Analisi_Esterne`, `News_Inbox` e i siti | JSON da salvare come `A1_<ciclo>.json` |
| A3 Interim Update | legge le notizie della settimana e le collega ai rischi del registro, nel radar o in osservazione | ogni lunedi' (sezione 1) | niente: legge `News_Inbox`, i siti e la baseline in knowledge | JSON da salvare come `A3_<lunedi'>.json` |
| A4 News Assessor | parere su UNA notizia rispetto al registro, senza numeri nuovi | quando serve | la notizia (testo, link o file) | parere in sei sezioni, in chat; non scrive nel registro |
| A5 Challenger (facoltativo) | controlla l'output di A1 con i dieci controlli (C1-C10) | se lo usi, dopo A1 (sezione 2, punto 6) | `Input_A5_<ciclo>.txt` allegato (dal precontrollo) | JSON da salvare come `A5_<ciclo>.json` |
| A6 Schede dei rischi | scrive i testi delle schede sui dati validati | dopo la validazione (sezione 2, punto 12) | solo `Input_A6_<ciclo>.json` allegato | JSON da salvare come `A6_<ciclo>.json` |
| A7 Assistente del registro | spiega in chat il perche' delle valutazioni, come chi le ha proposte, senza cambiarle | quando serve (sezione 4, "Chiedere il perche' ad A7") | niente: legge la cartella `Kernel\Spiegazioni` e i documenti | risposte in chat; a richiesta la sintesi per le Note dell'analista |
| A8 Evento critico | analizza a fondo un evento critico, rivaluta i rischi indicati e censisce i nuovi | nel ciclo straordinario deciso dalla funzione di rischio (sezione 2-bis) | allegato `Input_A8_<AAAAQn-Sk>.txt` e i documenti dell'evento nella chat; legge anche `Analisi_Interne`, `Analisi_Esterne`, `News_Inbox` e i siti | JSON da salvare come `A8_<AAAAQn-Sk>.json` |

### A1 Horizon Scanner

Messaggio base, con l'allegato `Input_A1_<ciclo>.txt` (sempre allegato alla
chat: A1 non lo legge dalla library Kernel):

> Esegui il ciclo

Variazioni:
- **Rinforzato**, quando le fonti citate sono poche o le segnalazioni su C4 e C5
  (punteggi o fonti non sostenuti) sono tante. Visto la prima volta nel primo
  ciclo reale del 29/09/2026:

  > Esegui il ciclo per il [ciclo]. Prima di assegnare i punteggi, consulta tutti
  > i documenti disponibili in Analisi_Interne e in Analisi_Esterne — non
  > fermarti ai primi che trovi, verifica le intere cartelle — e tutte le notizie
  > recenti dei siti pubblici configurati. Il tipo di ogni fonte segue la
  > cartella: "Interna" solo per i documenti di Analisi_Interne, "Esterna" per
  > Analisi_Esterne, notizie e siti.

  Limite: rinforza le istruzioni per questa volta ma non obbliga Agent Builder a
  leggere tutta la knowledge. Se A1 cita ancora solo 2-3 fonti su molte, e' la
  ricerca della knowledge che ne recupera solo una parte, non il messaggio da
  correggere.
- **Documenti precisi**, per far pesare di piu' alcuni documenti:

  > Esegui il ciclo analizzando in particolare, in Analisi_Esterne, il file
  > "[nome del file]" e, in Analisi_Interne, il file "[nome del file]".

- **Tema da verificare**, per chiedere di valutare un rischio preciso:

  > Esegui il ciclo. Verifica in particolare se le fonti sostengono il rischio
  > "[descrizione del meccanismo di perdita]": se c'e' almeno una fonte specifica,
  > censiscilo come rischio nuovo con le regole abituali; se il meccanismo c'e' ma
  > e' lontano o solo teorico, censiscilo lo stesso: resta in osservazione con
  > l'orizzonte e il segnale; se non c'e', mettilo fra i fenomeni non censiti con il
  > motivo.

  La richiesta non resta tracciata (vive nella chat); A1 lo censisce solo se le
  fonti lo sostengono.
- **Fenomeno da osservare**, per chiedere un rischio che restera' in osservazione:

  > Esegui il ciclo. Valuta anche il fenomeno "[descrizione]": se ha un meccanismo di
  > perdita per la Banca e almeno una fonte, censiscilo come rischio nuovo, con
  > l'orizzonte e il segnale di avvicinamento.

  Per togliere un rischio in osservazione non serve A1: `dismetti` (sezione 3-bis).
- **Ciclo straordinario**: dal 07/10 (D-77) lo fa A8 (sotto). A1 lo sa ancora fare
  con lo stesso allegato e lo stesso messaggio, ma senza l'analisi dell'evento: il
  controllo lo segnala al validatore.
- **Simulazione di un ciclo passato** (registro di prova, per esempio un 2026Q2):

  > Esegui il ciclo. Considera solo documenti e notizie datati fino al
  > [data di riferimento, es. 30/06/2026].

  I controlli fermano comunque le fonti datate dopo la data di riferimento; il
  messaggio serve a non farsi influenzare da cio' che e' successo dopo.
- **Correzione**: dopo un fermo o un precontrollo, incollare tutto il contenuto di
  `Cicli\<ciclo>\Correzione_A1_<ciclo>.txt`, senza aggiungere altro; poi salvare la
  nuova risposta come `A1_<ciclo>.json`.

Cosa un messaggio non puo' cambiare: la regola del punto fra un ciclo e l'altro,
la fonte datata per ogni variazione, i due KRI per rischio, il formato del
razionale in parti.

### A3 Interim Update

Messaggio base, con l'allegato `Input_A3_A4.txt` (la baseline, dalla cartella di uscita;
AU7, 23/10/2026). Il prompt schedulato del lunedi' non porta l'allegato: A3 risponde
"Baseline mancante", quindi si lancia a mano.

> Esegui l'aggiornamento settimanale

Variazioni:
- **Correzione**: dopo un fermo di `settimanale` (per esempio "id_notizia ripetuti"
  o "Codici fonte non nell'elenco"), incollare il messaggio del fermo:

  > Correggi questi punti e restituisci di nuovo l'intero JSON: [messaggio]

- **Proposta di ciclo straordinario** (D-75): A3 la scrive da solo con la regola del
  segnale critico della rubrica (`proposta_straordinario`: rischi e motivo); non serve
  chiederla. E' una proposta: decide la funzione di rischio (sezione 2-bis).
- **Rischi in osservazione** (D-79): non serve chiederlo, A3 li legge nella
  baseline; collega una notizia a un rischio in osservazione come a uno del radar
  (`rischio_collegato`) e, se la notizia realizza il suo segnale di avvicinamento,
  propone un flag. Per insistere su un rischio: "Esegui l'aggiornamento settimanale;
  verifica in particolare le notizie su [NFR-nn]". Il flag e' una proposta: lo
  valuta A1 al ciclo dopo (o, per un evento critico, A8 nello straordinario).
- **Notizie portate a mano**: se hai messo file in `News_Inbox\<lunedi'>\Manuali\`,
  non serve dirlo, A3 li legge; per una fonte fuori elenco usa il codice `MAN`
  (sezione 1, punto 2).

A3 lavora sulla settimana in corso: per recuperare una settimana saltata il
prompt non prevede un'altra data; meglio aggiungere le notizie di quella
settimana nei `Manuali` della settimana in corso.

### A4 News Assessor

Messaggio base: la notizia, incollata o allegata, con l'allegato `Input_A3_A4.txt` (la
baseline, dalla cartella di uscita; AU7, 23/10/2026). Senza allegato A4 lo dice in testa
e da' solo l'analisi di impatto sulle nove categorie.

> Dammi il parere su questa notizia: [testo o link]

Variazioni:
- **Un rischio preciso**: "Dammi il parere su questa notizia, in particolare
  rispetto a [NFR-nn]: [testo o link]".
- **Una categoria**: "... valuta con attenzione l'impatto su [9.n, nome della categoria]".

A4 non propone numeri e non scrive nel registro: se il parere suggerisce di
rivedere un rischio, la via e' il ciclo trimestrale; se la notizia soddisfa la regola
del segnale critico, A4 scrive in testa alla sezione 5 "PROPOSTA DI CICLO
STRAORDINARIO" con i rischi e il motivo, e la funzione di rischio decide (sezione
2-bis; l'analisi approfondita dell'evento la fa poi A8 nello straordinario).

### A5 Challenger (facoltativo)

Messaggio base, con l'allegato `Input_A5_<ciclo>.txt` (output di A1 e baseline, scritto dal precontrollo):

> Esegui i controlli

Variazioni: nessuna utile. Dopo ogni nuovo output di A1, A5 va rifatto in una
chat nuova sul file nuovo (il vecchio esito vale solo per il vecchio output).

### A6 Schede dei rischi

Messaggio base, con il solo `Input_A6_<ciclo>.json` allegato:

> Scrivi le schede

Variazioni:
- **Correzione**: dopo un fermo di `schede`, incollare l'elenco del fermo:

  > Correggi questi punti e restituisci di nuovo l'intero JSON: [elenco]

### A7 Assistente del registro

Nessun allegato e nessun messaggio fisso: si fanno domande. Esempi:

> Perche' [NFR-nn] e' primo in classifica?
>
> Perche' [NFR-nn] ha Prossimita [valore]? Da quale documento viene?
>
> Perche' [NFR-nn] e' AGIRE ORA?
>
> Perche' il livello di [NFR-nn] e' Attenzione e non Attivazione?
>
> Il validatore ha cambiato qualcosa su [NFR-nn]? Perche'?
>
> Cosa e' cambiato per [NFR-nn] rispetto al ciclo prima?
>
> Perche' il tema "[tema]" che compare in [documento] non e' un rischio del registro?
>
> Quali rischi sono AGIRE ORA e che cosa li accomuna?
>
> Perche' [NFR-nn] e' in osservazione e non nel radar? Che cosa lo porterebbe nel radar?

Variazioni:
- **Per il comitato**: "Spiegamelo come a un membro del comitato, senza termini
  tecnici, in cinque righe".
- **Confronto**: "Perche' [NFR-nn] ha uno score piu' alto di [NFR-mm]?".
- **Sintesi per il Quadro**, alla fine della conversazione:

  > Fammi la sintesi per il Quadro

  Restituisce al massimo 600 caratteri da incollare nella cella gialla **Note
  dell'analista** della prima pagina del Quadro (sezione 6).

A7 risponde in prima persona, come chi ha proposto le valutazioni e le difende
("Ho dato Impatto 4 perche'..."; dopo una rettifica "Avevo proposto 3, il
validatore ha deciso 4 perche'..."), senza nominare gli altri agenti (D-87). Il
perche' e' quello scritto nel registro; segnala solo cio' che ricava ora dai
documenti ("lettura di oggi, non nel registro"). In chat non cambia valori: a
"dovrebbe essere piu' alto?" spiega perche' il valore e' quello e quale evidenza
lo farebbe salire. Copione di prova: `04_Riferimenti/Prove/Prova_A7.md`.

### A8 Evento critico

Solo nel ciclo straordinario (sezione 2-bis), in una chat nuova, con l'allegato
`Input_A8_<AAAAQn-Sk>.txt` e i documenti sull'evento allegati (o indicati per nome
nella library):

> Esegui il ciclo straordinario

L'allegato dice in testa quali rischi rivalutare (o che lo straordinario e' di solo
censimento) e perche'; A8 non riscrive gli altri rischi e aggiunge `analisi_evento`.

Variazioni:
- **Documenti precisi**: "Esegui il ciclo straordinario analizzando per intero
  [nome del file] in [Analisi_Interne o Analisi_Esterne] e il comunicato allegato".
- **Un rischio vicino da guardare**: "... e di' in analisi_evento se l'evento tocca anche
  [NFR-nn]". A8 non puo' riscriverlo se non e' indicato: lo mette fra i rischi toccati
  (segnalazione al validatore) e la funzione di rischio decide se rivalutarlo.
- **Correzione**: dopo un fermo o un precontrollo, incollare tutto
  `Cicli\<AAAAQn-Sk>\Correzione_A1_<AAAAQn-Sk>.txt` (lo script dice "Messaggio per A8");
  poi salvare la nuova risposta come `A8_<AAAAQn-Sk>.json`.

Cosa un messaggio non puo' cambiare: i rischi da rivalutare (li decide la funzione di
rischio con `baseline --straordinario`), la regola del punto rispetto al periodo prima,
le regole di A1 per fonti, KRI e azioni. L'analisi dell'evento spiega, non porta valori.

**Modifiche: non con A7** (decisione del 07/10/2026, D-76: niente modo manutenzione,
A7 spiega soltanto). Le strade:
- valori proposti da A1 (punteggi, anni di adeguamento, KRI, azioni) e lo stato di un
  rischio (radar o osservazione): nella griglia del foglio Validazione, prima di
  `valida` (sezione 3);
- gli stessi valori dopo la validazione: `riapri`, griglia, `valida`, quante volte
  serve (sezione 3-ter); anche per togliere un KRI, annullare un'azione o spostare un
  rischio fra radar e osservazione;
- testi (descrizioni, razionali, segnali di avvicinamento, nomi e note di KRI e
  azioni): a mano nei fogli dati, poi `baseline` (sezione 3-ter);
- presidio dei controlli, anni di adeguamento, attenzione del supervisore, stato di
  un'azione, Note dell'analista: celle gialle del registro (sezione 6);
- un rischio da togliere: `dismetti` (sezione 3-bis);
- un rischio nuovo, anche lontano (restera' in osservazione): al ciclo dopo (A1, con un
  messaggio della sezione 8 se serve).

## 9. I comandi Python: parametri, opzioni, errori

Riferimento completo dei due programmi. Si lanciano dal Prompt dei comandi, dalla
cartella degli script (`07_Senza_Studio`), con il **registro chiuso** (anche per i
colleghi). Come si scrive un comando: in testa alla guida. I testi da vedere
passo per passo sono nelle sezioni 1, 2 e 3; i messaggi d'errore con il rimedio
nella sezione 7.

**Codici di uscita** (uguali per tutti i comandi di `esegui_ciclo_locale.py`):
- 0 eseguito;
- 1 **FERMATO**: lo script ha trovato un problema nei dati o nei controlli e **non
  ha toccato il registro**: si corregge e si rilancia;
- 2 **ERRORE TECNICO**: un problema del PC o di Excel. Il messaggio dice se e'
  avvenuto prima del salvataggio (nulla scritto: si rilancia) o **dopo** (registro
  gia' scritto: **non rilanciare**, sezione 7).

**Opzioni comuni** di `esegui_ciclo_locale.py`, da scrivere **prima** del nome del
comando; senza, valgono i percorsi di `configurazione.json`:
- `--workbook <file>`: il registro su cui lavorare (per esempio un registro di prova);
- `--kernel <cartella>`: la cartella del kernel (la library Kernel sincronizzata);
- `--cartella-uscita <cartella>`: l'archivio (baseline, cicli, settimane, backup).

In `configurazione.json`, oltre ai percorsi (D-83): `utente` (il nome che i colleghi
vedono nel lucchetto; senza, l'utente di Windows), `attesa_lucchetto` (secondi della
presa in due tempi, 0: nessuna attesa) e, facoltativa, `cartella_lavoro` (la copia di lavoro del
registro; senza, `%LOCALAPPDATA%\NFR\lavoro`). I comandi che scrivono nel registro
(`trimestrale`, `settimanale`, `valida`, `griglia`, `riapri`, `dismetti`,
`inizializza`, `aggiorna-registro`) prendono il lucchetto; gli altri no.

Esempio: `python esegui_ciclo_locale.py --workbook "C:\NFR_Prova\Registro.xlsx" --cartella-uscita "C:\NFR_Prova\Archivio" baseline`.

### raccogli_notizie.py

`python raccogli_notizie.py [--giorni N] [--oggi AAAA-MM-GG] [--anche-da-validare] [--kernel <cartella>] [--news-inbox <cartella>]`

- Cosa fa: scarica i feed delle fonti `rss` approvate di `fonti.md` e scrive
  `News_Inbox\<lunedi'>\Raccolta_<data>.txt` (con la cartella `Manuali` vuota per i
  file a mano). Non tocca il registro.
- Opzioni: `--giorni` quanti giorni indietro (7); `--oggi` la data da usare come
  oggi (per recuperare una raccolta); `--anche-da-validare` prova anche le fonti
  non ancora approvate; `--kernel`, `--news-inbox` come in `configurazione.json`.
- Quando: ogni lunedi', di solito dall'Utilita' di pianificazione (in testa alla guida).
- Errori tipici: "non raggiungibile" su alcune o tutte le fonti (proxy: sezione 7).

### esegui_ciclo_locale.py baseline

`python esegui_ciclo_locale.py baseline [--uscita <file.json>]`
`python esegui_ciclo_locale.py baseline --straordinario [--rischi NFR-nn[,NFR-mm]] --motivo "..." --decisore "..." [--data AAAA-MM-GG]`

- Cosa fa: scrive `Baseline_corrente.json` (e la copia `.txt`), l'allegato di A1
  `Input_A1_<ciclo>.txt` e l'allegato di A3 e A4 `Input_A3_A4.txt`
  (AU7) nella cartella di uscita. Sola lettura del registro. Con
  `--straordinario` (D-75) la baseline e l'allegato sono per il periodo `AAAAQn-Sk`
  (l'allegato `Input_A8_<periodo>.txt` lo usa A8, D-77, D-84) e la decisione si archivia in
  `Cicli\<AAAAQn-Sk>\Straordinario_<AAAAQn-Sk>.json`.
- Opzioni: `--uscita` scrive la baseline in un altro file (prove, confronti);
  `--straordinario` con `--rischi` (separati da virgole; senza, lo straordinario e' di
  solo censimento di rischi nuovi, D-77), `--motivo` (almeno 20 caratteri), `--decisore`
  e, facoltativa, `--data` (di norma oggi; dopo la data del ciclo corrente).
- Quando: all'inizio del trimestre; la riscrivono anche `trimestrale`, `valida`, `dismetti`.
  Senza `--uscita` riscrive anche la knowledge di A7: la lancia `testi-fine` dopo
  aver corretto dei testi a mano (sezione 3-ter).
- Errori tipici: "il ciclo ... ha ancora N righe da validare" (avviso, sezione 3; per uno
  straordinario e' un fermo); "nel kernel ... mancano" (sezione 0-bis, punto 1); "Workbook
  non trovato" (sezione 7); con `--straordinario`: "--rischi: indicare i rischi ...",
  "--motivo ... e --decisore ... sono obbligatori", "--data ... deve venire dopo".

### esegui_ciclo_locale.py precontrollo

`python esegui_ciclo_locale.py precontrollo --payload A1_<ciclo>.json [--baseline <file.json>]`

- Cosa fa: controlla l'output di A1 (schema, controlli, parti del razionale) senza
  Excel e senza aprire il registro; se trova qualcosa scrive
  `Cicli\<ciclo>\Correzione_A1_<ciclo>.txt`, il messaggio da dare ad A1. Se nessun
  punto fermerebbe il ciclo scrive anche l'allegato di A5, `Input_A5_<ciclo>.txt`
  (output di A1 e baseline, D-84). Stampa l'impronta dell'output (serve solo alla
  prova di Copilot Studio).
- Obbligatorio: `--payload`. Opzione: `--baseline` (di default `Baseline_corrente.json`).
- Codice 1 se un punto fermerebbe il ciclo, 0 altrimenti.
- Quando: **FACOLTATIVO**, ma **necessario prima di A5** se lo usi (sezione 2, punto 5-bis). Se non serve, si puo' saltare: `trimestrale` fa gli stessi controlli prima di scrivere.
- Errori tipici: "Baseline non trovata" (lanciare `baseline`); "non e' un JSON
  valido" o "non conforme allo schema" (sezione 7).

### esegui_ciclo_locale.py trimestrale

`python esegui_ciclo_locale.py trimestrale --payload A1_<ciclo>.json [--challenger A5_<ciclo>.json]`

- Cosa fa: controlla l'output di A1 (e quello di A5, se c'e'), lo scrive nel
  registro (rischi, azioni, KRI, anagrafica, segnalazioni), ricalcola, verifica e
  salva (backup prima); archivia in `Cicli\<ciclo>\` l'Excel di output, gli output
  degli agenti e l'esito dei controlli; calcola lo stato di ogni rischio con la regola
  del radar (D-79: chi entra va in anagrafica, chi esce lascia l'anagrafica e i suoi
  KRI escono di vigore; i rischi in osservazione non toccati da A1 si riportano
  com'erano); riscrive baseline, allegato di A1 e knowledge di A7; archivia le Note
  dell'analista del ciclo prima.
- Obbligatorio: `--payload`. Opzione: `--challenger` (A5 facoltativo, D-71).
  `--procedi-con-rilievi`, `--motivo`, `--decisore`: superate, accettate ma inutili.
- Quando: ogni trimestre, dopo A1 (sezione 2, punto 7).
- Errori tipici: "Il ciclo precedente ... non e' ancora validato" (sezione 3);
  "Ciclo da rivedere (difetti che renderebbero incoerente il registro)" (sezione 2,
  punto 8: dare ad A1 `Correzione_A1_<ciclo>.txt`; vale anche per un rischio del radar
  senza KRI o azioni); "Rischi in osservazione N, oltre il massimo di 20" (A1 lascia
  fuori i meno rilevanti); "L'esito di A5 ... e' del ciclo
  ..." (rifare A5); "ATTENZIONE: l'anagrafica ha N posti liberi"; "Avviso per le
  schede: il razionale ... non e' diviso in parti" (ricaricare A1); per uno straordinario
  "non c'e' la decisione" (prima `baseline --straordinario`, sezione 2-bis).

### esegui_ciclo_locale.py settimanale

`python esegui_ciclo_locale.py settimanale --payload A3_<lunedi'>.json`

- Cosa fa: controlla l'output di A3 e i codici delle fonti, aggiunge le notizie
  senza duplicati, la sintesi della settimana, fa scorrere la settimana corrente,
  ricalcola e salva; archivia in `Settimane\<lunedi'>\`.
- Obbligatorio: `--payload`.
- Quando: ogni lunedi', dopo A3 (sezione 1, punto 5).
- Errori tipici: "id_notizia ripetuti", "Codici fonte non nell'elenco", una notizia collegata a
  un rischio che non e' nel registro (dare il messaggio ad A3), "settimana ...
  non e' un lunedi'", "Le notizie da validare ... superano le ... righe" (sezione 7).

### esegui_ciclo_locale.py valida

`python esegui_ciclo_locale.py valida --periodo <ciclo o lunedi'> --validatore "<funzione o comitato>" [--senza-report]`

- Cosa fa: legge la griglia del foglio Validazione per quel periodo (cella gialla
  uguale alla proposta = accettata, cambiata = rettificata, Respingi = Si' =
  respinta), controlla tutte le righe e solo se vanno tutte bene le applica ai dati,
  scrive lo storico, salva (backup prima), archivia l'Excel validato e
  `Validazione_<periodo>.json`; per il ciclo corrente riscrive baseline e knowledge di A7
  e rigenera il report al comitato (PDF, come `report`; D-83). Dopo una riapertura
  chiude `Riapertura_<ciclo>.json`.
- Obbligatori: `--periodo` (es. `2026Q3` o `2026-10-12`), `--validatore`.
  `--senza-report`: non rigenerare il report. `--accetta-il-resto`: superata, accettata
  ma inutile.
- Quando: dopo ogni trimestre (obbligatoria) e, se si vuole, dopo ogni settimana (sezione 3).
- Errori tipici: "Validazione del periodo ... NON applicata (N problemi)" con il
  numero di riga; "il rischio ha segnalazioni da motivare"; "proposta di A1 non
  accettabile"; "Il foglio Validazione non corrisponde alle proposte" (comando
  `griglia`); "Nessuna riga da validare"; "Stato vuoto o modificato a mano" (sezione 7).

### esegui_ciclo_locale.py griglia

`python esegui_ciclo_locale.py griglia`

- Cosa fa: ricostruisce il foglio Validazione dalle proposte ancora da decidere,
  conservando cio' che e' gia' scritto nelle righe intatte. Nessun parametro.
- Quando: solo se il foglio e' stato rovinato a mano (righe cancellate o inserite,
  ID cambiati).

### esegui_ciclo_locale.py riapri

`python esegui_ciclo_locale.py riapri [--rischi NFR-nn[,NFR-mm]]`

- Cosa fa (D-76): riapre la validazione del ciclo corrente, gia' validato: rischi (nel
  radar e in osservazione, D-79), KRI in vigore e azioni aperte tornano nella griglia
  del foglio Validazione con il valore validato. Poi `valida` come sempre; si puo'
  ripetere. Salva (backup prima); non cambia nessun dato. Lascia
  `Cicli\<ciclo>\Riapertura_<ciclo>.json` (chi, quando, che cosa), che `valida` chiude.
- Opzioni: `--rischi` solo quei rischi, con i loro KRI e azioni. Senza: tutto. (L'opzione
  per le voci della lista non c'e' piu' dall'08/10: le voci sono rischi in osservazione.)
- Quando: per cambiare un valore gia' validato (sezione 3-ter).
- Errori tipici: "ha gia' N righe da validare" (si cambia nella griglia gia' aperta,
  poi `valida`); "Da riaprire ma non nel ciclo" (codice sbagliato); "non ha ancora un
  ciclo validato".

### esegui_ciclo_locale.py schede-input e schede

`python esegui_ciclo_locale.py schede-input`
`python esegui_ciclo_locale.py schede [--payload A6_<ciclo>.json]`

- Cosa fanno: `schede-input` scrive `Cicli\<ciclo>\Input_A6_<ciclo>.json`, l'unico
  allegato di A6; `schede` controlla l'output di A6 e scrive `Schede_<ciclo>.xlsx` e il
  suo PDF (senza `--payload`, le schede con i testi del registro). Sola lettura del
  registro. Un errore nel PDF e' solo un avviso.
- Quando: dopo la validazione (sezione 2, punti 11-12).
- Errori tipici: "righe da validare" (validare prima); "Output di A6 non coerente
  con i dati validati" con l'elenco (correggere con A6, sezione 8); "No module named
  'openpyxl'" (sezione 7).

### esegui_ciclo_locale.py report

`python esegui_ciclo_locale.py report [--file <registro.xlsx>] [--con-lavoro]`

- Cosa fa: rigenera il PDF del report al comitato (Quadro..Metodologia) in
  `Cicli\<ciclo>\Report_comitato_<ciclo>.pdf` e lo stesso report in HTML,
  `Report_comitato_<ciclo>.html` (con le schede di tutti i rischi), solo se i suoi numeri
  tornano con quelli di Excel (cancello; altrimenti l'avviso con i numeri diversi, e il
  PDF esce lo stesso); ricompone `Cicli\Indice_report.html`. Le versioni precedenti
  restano con data e ora nel nome. Non modifica l'Excel.
- Opzioni: `--file` un altro Excel (per esempio l'Excel validato di un ciclo);
  `--con-lavoro` aggiunge Registro e Parametri al PDF, in orizzontale, e le viste di
  lavoro all'HTML.
- Quando: dopo ogni correzione a mano delle celle gialle (sezione 2, punto 13; sezione
  6); dopo la validazione lo fa gia' `valida`.
- Errori tipici: "righe da validare" (il ciclo deve essere validato); "Avviso: report
  HTML ... NON uscito, il cancello ha trovato N numeri diversi": esce solo il PDF; mandare
  il messaggio a chi mantiene il pacchetto.

### esegui_ciclo_locale.py sblocca

`python esegui_ciclo_locale.py sblocca --motivo "..."`

- Cosa fa (D-83): toglie il lucchetto del registro (`Archivio_Cicli\_Lucchetto\registro.json`)
  rimasto per errore, e scrive in `_Lucchetto\sblocchi.log` chi, quando, perche' e di chi
  era. Non tocca il registro.
- Obbligatorio: `--motivo`, almeno 10 caratteri.
- Quando: solo se un comando si ferma con "Il registro e' in uso" e chi e' indicato non
  sta lavorando (PC spento o comando interrotto a meta'); sentirlo prima. Un lucchetto
  scade comunque da solo dopo 2 ore.

### esegui_ciclo_locale.py diagnosi

`python esegui_ciclo_locale.py diagnosi`

- Cosa fa (D-80, analisi 17, 17.10): solo lettura, nessun dato cambia. Misura sul registro tre asimmetrie della
  valutazione e le scrive anche in `Cicli\<ciclo>\Diagnosi_valutazioni_<ciclo>.txt`:
  1. quanti rischi nuovi sono entrati con ogni valore, per dimensione (per esempio: nessuno con Probabilita 4 o 5);
  2. quante volte il validatore ha alzato o abbassato una dimensione proposta dall'agente, per i rischi nuovi, gli altri
     e in riapertura (molte rettifiche nello stesso verso = proposte sistematicamente basse o alte);
  3. i rischi lontani (Prossimita 1) con il margine di Mosca; quelli con Impatto 4-5 senza anni di adeguamento sono
     segnalati, perche' il margine usa la Y di riserva e non possono risultare AGIRE ORA.
- Quando: dopo la validazione di un ciclo, quando si vuole capire se le valutazioni pendono da una parte; utile da
  portare alla taratura di descrittori e soglie (A-12).
- Errori tipici: "Nessun ciclo nel registro" (prima del primo trimestrale).

### esegui_ciclo_locale.py dismetti

`python esegui_ciclo_locale.py dismetti --rischio NFR-nn --motivazione "..." --decisore "..."`

- Cosa fa: toglie il rischio dall'anagrafica senza lasciare righe vuote, fa uscire
  di vigore i suoi KRI, annulla le sue azioni aperte, archivia l'atto in
  `Dismissioni\`; la storia resta. Riscrive baseline e knowledge di A7.
- Obbligatori: `--rischio`, `--motivazione` (almeno 10 caratteri), `--decisore`.
- Quando: solo su decisione della funzione di rischio (sezione 3-bis).
- Errori tipici: "non e' nell'anagrafica dei rischi attivi"; motivazione troppo corta.

### esegui_ciclo_locale.py inizializza

`python esegui_ciclo_locale.py inizializza --ciclo-precedente AAAAQn --settimana AAAA-MM-GG [--template <file.xlsx>]`

- Cosa fa: crea il registro vuoto dal template (senza i dati di esempio), con il
  ciclo prima di quello da valutare e la settimana corrente. Non sovrascrive mai un
  file esistente.
- Obbligatori: `--ciclo-precedente` (il trimestre **prima** del primo da valutare),
  `--settimana` (un lunedi'). Opzione: `--template`.
- Quando: una volta sola, al primo uso (sezione 0.4), o per un registro di prova
  (con `--workbook` davanti al comando).
- Errori tipici: "esiste gia'"; "deve essere un lunedi'"; "Template non trovato" (sezione 7).

### esegui_ciclo_locale.py aggiorna-registro

`python esegui_ciclo_locale.py aggiorna-registro [--template <file.xlsx>]`

- Cosa fa: porta il registro su un template nuovo copiando tutto per nome di
  colonna (righe, anagrafica, parametri, Note dell'analista); verifica righe,
  errori e baseline prima di sostituire il file; il vecchio resta in `Backup\`.
  Pesi, soglie e Z diventano quelli del template nuovo (stampa quelli di prima).
- Opzione: `--template`.
- Quando: dopo un aggiornamento del pacchetto che cambia la struttura (ogni comando
  si ferma finche' non e' fatto); con il pacchetto dell'08/10/2026, alla versione
  2026-10-09 (sezione 0-bis).
- Errori tipici: "e' gia' sulla versione"; "righe vuote con lo Stato 'Da decidere'"
  e "campi che il modello non ha piu'" (sezione 7); "Aggiornamento NON applicato";
  "e' aperto" (chiudere il registro e attendere OneDrive).
