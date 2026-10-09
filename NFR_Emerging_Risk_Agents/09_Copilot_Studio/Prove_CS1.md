# Prove di fattibilita' della CS-1 (Operatore in Copilot Studio, motore Python su un PC esecutore)

Le prove dicono se la variante ibrida CS-1 si puo' fare in Banca (`Analisi_Architettura/14_Tre_strade.md`, 14.9).
Le prime (K6, K4, K11, K12) valgono anche per la CS-2.

Si fanno **dopo l'allineamento al pacchetto corrente** (TODO, passi B1-B4). Nessuna prova tocca il registro vero:
- si lavora sul registro di prova in `C:\NFR_Prova`;
- in SharePoint si lavora nella cartella `Archivio_Cicli\Prova_K0`.

## Ordine e tempi

| # | Prova | Dove | Tempo | Che cosa decide |
|---|---|---|---|---|
| 0 | Preparazione: registro di prova e due run di A1 in Agent Builder | PC, Agent Builder | 1-2 ore | base di confronto per K4 |
| D1, D2 | Domande all'IT e alla compliance | posta | 10 minuti, poi l'attesa | **un no ferma la CS-1**: mandarle subito, anche prima del punto 0 |
| 1 | **K6** Operatore a passi fissi, compreso K6.5 in Teams (`Prova_K6_Operatore.md`) | tenant | 2-3 ore | il cuore della CS-1 |
| 2 | **K4** qualita' di A1 in Copilot Studio | tenant e PC | 2 ore | che spostare A1 non peggiori le valutazioni |
| 3 | **K11** piu' utenti | tenant, con un collega | 1 ora | multiutenza e ruoli |
| 4 | **K12** A7 e aggiornamento delle spiegazioni | tenant | 1 ora, piu' l'attesa dell'indicizzazione | consultazione da parte di altri utenti |
| 5 | **K7a** sincronizzazione fra SharePoint e PC | PC e tenant | 1 ora | tempi e sicurezza della scrittura |
| 6 | **K7b** Excel senza nessuno davanti | PC | 1 ora, con un riavvio | che il PC possa fare da esecutore |

Alla fine si compila la tabella dei risultati in fondo e la si manda a chi mantiene il pacchetto.

## 0. Preparazione (dopo i passi B1-B4)

1. Rifare il registro di prova con il pacchetto corrente: `04_Riferimenti/Prove/Prova_senza_Copilot_Studio.md`,
   parte 2, dal passo 2.1 al 2.7 (A1, precontrollo, `trimestrale`, `valida`).
   - Al passo 2.1 la configurazione di prova va scritta **senza la riga `kernel`** (corretto il 09/10). Cosi'
     le spiegazioni per A7 finiscono in `C:\NFR_Prova\Archivio\Spiegazioni` e non nella library Kernel vera.
   - Il primo output di A1 del passo 2.3 si conserva come `A1_AB_run1.json`.
2. **Secondo run in Agent Builder**: in una chat **nuova** di A1, stesso allegato
   `C:\NFR_Prova\Archivio\Input_A1_2026Q4.txt`, messaggio `Esegui il ciclo`. Salvare la risposta (solo il JSON)
   come `C:\NFR_Prova\A1_AB_run2.json`. Non correggerla: serve a misurare quanto A1 cambia da solo.
3. Copiare `A1_AB_run1.json` in `C:\NFR_Prova\` accanto al secondo.
4. In SharePoint creare:
   - `Archivio_Cicli\Prova_K0\In_arrivo`;
   - `Archivio_Cicli\Prova_K0\Esiti`;
   - `Archivio_Cicli\Prova_K0\Spiegazioni`.
5. Copiare `C:\NFR_Prova\Archivio\Input_A1_2026Q4.txt` in `Archivio_Cicli\Prova_K0\`.

## D1 e D2. Domande all'IT e alla compliance (testi pronti)

**D1, all'IT** (oggetto: "Copilot Studio e un PC che esegue uno script: e' ammesso?"):

> Stiamo valutando di usare Copilot Studio per il registro dei rischi emergenti NFR. Gli agenti consegnano file
> JSON in una cartella SharePoint del nostro sito, con agent flow e connettore SharePoint. Un PC della funzione,
> sempre acceso e con un utente collegato, li vede attraverso la sincronizzazione di OneDrive. Su quel PC un
> programma Python lancia Excel desktop e aggiorna il registro: oggi lo facciamo a mano con gli stessi script. Vi
> chiediamo:
> 1. un PC usato cosi', acceso anche di notte e senza nessuno davanti, e' ammesso? Ci sono regole sul blocco
>    dello schermo, sugli aggiornamenti automatici e sullo spegnimento?
> 2. un programma che parte da solo all'accesso a Windows (collegamento nella cartella Esecuzione automatica) e'
>    ammesso, o va registrato?
> 3. un agent flow puo' usare una connessione unica di servizio, invece di quella di ogni utente? E' il caso
>    dell'errore "FlowMakerConnectionBlocked".
> 4. gli Office Scripts lanciati da un flusso ("Run script" del connettore Excel Online) sono attivi nel tenant?
>    Serve a una variante senza PC.

**D2, alla compliance / DPO** (oggetto: "Copilot Studio: trascrizioni ed etichette"):

> Per il registro NFR valutiamo un agente Copilot Studio usato da piu' persone della funzione rischi. Legge
> documenti delle cartelle SharePoint `Analisi_Interne`, `Analisi_Esterne` e `News_Inbox`, e conserva le
> conversazioni come trascrizioni nell'ambiente Power Platform. Vi chiediamo:
> 1. le trascrizioni delle conversazioni conservate da Copilot Studio sono ammesse? Per quanto tempo e dove?
>    E' l'estensione del parere sulle conversazioni di Agent Builder (D-24).
> 2. ci sono etichette di riservatezza sulle library `Kernel` e `Analisi_Interne`? Con alcune etichette la
>    knowledge non indicizza i file.

Annotare la risposta e la data nella tabella dei risultati.

## 1. K6 — Operatore a passi fissi

Protocollo intero in `Prova_K6_Operatore.md`: costruzione, test da K6.1 a K6.5, tabella. In piu', per questa serie
di prove:
- dopo K6.1 copiare dalla cartella sincronizzata `Archivio_Cicli\Prova_K0\In_arrivo\A1_2026Q4.json` in
  **`C:\NFR_Prova\A1_CS_run1.json`**;
- dopo K6.4, una seconda esecuzione in una conversazione nuova che riscrive lo stesso file, copiarlo in
  **`C:\NFR_Prova\A1_CS_run2.json`**;
- in K6.5 (Teams) annotare anche **quanto dura il turno** dal comando al messaggio finale.

## 2. K4 — Qualita' di A1 in Copilot Studio

Si confrontano quattro output di A1 sullo stesso allegato: due da Agent Builder (punto 0) e due dall'Operatore (K6).

1. Controllare che in `C:\NFR_Prova\` ci siano i quattro file: `A1_AB_run1.json`, `A1_AB_run2.json`,
   `A1_CS_run1.json` e `A1_CS_run2.json`.
2. Prompt dei comandi:

   ```
   cd C:\NFR_Prova\pacchetto\99_Collaudo
   python confronta.py C:\NFR_Prova\A1_AB_run1.json C:\NFR_Prova\A1_AB_run2.json --primo-ciclo
   python confronta.py C:\NFR_Prova\A1_CS_run1.json C:\NFR_Prova\A1_CS_run2.json --primo-ciclo
   python confronta.py C:\NFR_Prova\A1_AB_run1.json C:\NFR_Prova\A1_CS_run1.json --primo-ciclo
   ```

   Per ogni confronto annotare due numeri: quota di rischi presenti in tutti e due i run, e quota di punteggi
   identici sui rischi abbinati. Controllare a occhio gli abbinamenti stampati.
3. Precontrollo di ognuno dei quattro file, da `C:\NFR_Prova\pacchetto\07_Senza_Studio`:

   ```
   python esegui_ciclo_locale.py precontrollo --payload C:\NFR_Prova\A1_CS_run1.json
   ```

   e cosi' per gli altri tre. Annotare quanti punti da correggere e quanti da verificare. E' la qualita' al primo
   giro, senza correzioni.
4. Annotare il **modello** dell'Operatore (Settings -> Generative AI) e se si puo' fissare.

**Superata** se:
- il confronto Copilot Studio contro Copilot Studio rispetta D-21: almeno l'80% dei rischi in tutti e due i run e
  l'80% dei punteggi identici;
- non e' peggiore del confronto Agent Builder contro Agent Builder;
- i punti da correggere al primo giro non sono di piu' di quelli di Agent Builder.

Il confronto incrociato (terzo comando) dice quanto cambia cambiando piattaforma: non ha soglia, si legge con il
responsabile.

## 3. K11 — Piu' utenti

Serve un collega con licenza Microsoft 365 Copilot, chiamato qui B. Deve poter leggere `Analisi_Interne`,
`Analisi_Esterne` e `News_Inbox`, e scrivere in `Archivio_Cicli\Prova_K0`.

**Modifiche all'agente** (15 minuti):
1. Nel flusso `Salva_JSON`:
   - aggiungere un input di testo `utente`;
   - dopo Create file, aggiungere un secondo **Create file** nella stessa cartella. File Name = espressione
     `concat(<variabile nome_file>, '.chi.txt')`; File Content = espressione
     `concat(<variabile utente>, ' ', utcNow())`, con le variabili scelte dal contenuto dinamico;
   - salvare e pubblicare.
2. Nell'argomento `Esegui ciclo`, passo 6, assegnare a `utente` la variabile di sistema con l'indirizzo
   dell'utente (`System.User.Email` o `System.User.PrincipalName`: annotare quale c'e'). Save.
3. Pubblicare l'agente. Nel canale **Teams and Microsoft 365 Copilot** renderlo disponibile a B, singolarmente o
   con un gruppo: annotare l'opzione usata.

**Test**

| Test | Chi | Cosa | Cosa annotare |
|---|---|---|---|
| K11.1 | B, in Teams | `Esegui_ciclo`, `2026Q4` | Trova l'agente? Gli serve qualche licenza o ruolo in piu'? La sequenza va? Il file `A1_2026Q4.json.chi.txt` contiene l'indirizzo di B? |
| K11.2 | tu | cronologia delle esecuzioni di `Salva_JSON` in Power Automate | Con quale connessione e' girata l'esecuzione di B: la sua o la tua? |
| K11.3 | tu e B, insieme | `Esegui_ciclo`, `2026Q4`, lanciati entro un minuto | Due file o uno solo? Se uno solo, di chi? Nella CS-1 vera i nomi devono contenere chi chiede o l'ora: e' la misura |
| K11.4 | tu | la conversazione di B | Tu non la vedi, e la vede solo la scheda Activity (Analytics) di Copilot Studio? Annotare chi vede le trascrizioni: serve alla risposta della DPO |

**Superata** se:
- B usa l'Operatore senza licenze o ruoli in piu';
- l'identita' di chi lancia arriva nel flusso;
- si sa con quale connessione girano i flussi.

## 4. K12 — A7 e aggiornamento delle spiegazioni

A7 legge le spiegazioni dalla knowledge. La domanda e': dopo che il motore le ha riscritte, quanto tempo passa
prima che A7 risponda con i dati nuovi?

**Preparazione** (20 minuti):
1. Caricare in `Archivio_Cicli\Prova_K0\Spiegazioni` tutti i file di `C:\NFR_Prova\Archivio\Spiegazioni`:
   `Ciclo.txt` e `Rischio_01.txt` ... `Rischio_20.txt`. Attendere un'ora, poi cominciare.
2. Nell'Operatore, **Agents** -> **Add** -> **New child agent**:
   - Name: `A7 Assistente del registro`;
   - **When will this be used?**: **The agent chooses** (A7 legge soltanto, puo' sceglierlo il modello);
   - descrizione: `Spiega il perche' delle valutazioni del registro NFR (valori, motivazioni, decisioni, segnalazioni, temi non censiti). Non valuta e non scrive.`;
   - Instructions: il file intero `02_Agenti\A7_Assistente_registro.md`;
   - Knowledge: la cartella `Archivio_Cicli\Prova_K0\Spiegazioni`.
3. Sostituire le istruzioni dell'Operatore con:

   `Sei l'Operatore NFR di prova. Esegui solo cio' che dicono gli argomenti. Le domande sul perche' delle valutazioni del registro le passi ad A7 Assistente del registro. Non valutare rischi, non scrivere JSON, non chiamare strumenti di tua iniziativa. Per il resto rispondi che i comandi disponibili sono Esegui_ciclo e le domande ad A7.`
4. Ripubblicare.

**Test**

| Test | Cosa | Cosa annotare |
|---|---|---|
| K12.1 | Chiedere `Perche' il rischio del primo posto ha questa Prossimita'?` | Risponde dal file `Rischio_01.txt` (valori e motivazione uguali)? La knowledge funziona nel sotto-agente? |
| K12.2 | **File esistente modificato**. Aprire `C:\NFR_Prova\Archivio\Spiegazioni\Rischio_01.txt` con Blocco note e aggiungere in cima `Codice di verifica della prova K12: ALFA`. Salvare e caricarlo in SharePoint sostituendo quello di prima: annotare l'ora T0. Poi ogni 5 minuti, in una conversazione nuova: `Qual e' il codice di verifica della prova K12 nel file del primo rischio?` | Ora T1 della prima risposta giusta (ALFA). **T1-T0 e' il tempo di aggiornamento**. Smettere dopo 24 ore |
| K12.3 | Come K12.2 con `BETA` al posto di `ALFA` | Secondo tempo: conferma |
| K12.4 | Facoltativo: un **file nuovo** `Prova_K12.txt` con `Codice di verifica del file nuovo: GAMMA` | Tempo per un file nuovo. Il motore usa nomi fissi apposta: se un file nuovo e' molto piu' lento, la scelta e' confermata |

**Superata** se A7 risponde dai file e il tempo di aggiornamento sta sotto l'ora. Fra un'ora e un giorno si puo'
usare, ma il validatore deve aspettare; oltre un giorno A7 resta in Agent Builder.

## 5. K7a — Sincronizzazione fra SharePoint e PC

Si misura sul PC che farebbe da esecutore, con la library `Archivio_Cicli` sincronizzata. Nei comandi, `<sync>` e'
la cartella sincronizzata di `Archivio_Cicli`, per esempio `C:\Users\NOME\Banca\NFR-Emerging-Risk -
Archivio_Cicli`.

**Dal cloud al PC**:
1. Prompt dei comandi:

   ```
   cd C:\NFR_Prova\pacchetto\99_Collaudo
   python osserva_cartella.py "<sync>\Prova_K0\In_arrivo" --minuti 60
   ```

2. In Power Automate aprire `Salva_JSON` e **provarlo da solo** (Test, manualmente):
   - `nome_file` = `Sync_1.json`, `contenuto` = `{"prova": 1}`;
   - dalla cronologia annotare l'ora di fine dell'esecuzione, T0.
3. Nella finestra di `osserva_cartella` leggere l'ora di `compare` e di `completo` (T1).
4. Ripetere tre volte, poi tre volte dall'Operatore con `Esegui_ciclo` (il JSON di A1, 40-60 KB).
5. Ripetere tutto dopo aver scelto, con il tasto destro sulla cartella `Prova_K0`, **Mantieni sempre su questo
   dispositivo**.

**Dal PC al cloud**:
1. `python osserva_cartella.py --scrivi "<sync>\Prova_K0\Esiti"`: stampa l'ora di scrittura T0.
2. Nel browser aprire `Archivio_Cicli\Prova_K0\Esiti` e aggiornare la pagina ogni 15 secondi finche' compare il
   file: ora T1.
3. Ripetere tre volte.

**Conflitto con il registro aperto sul web**:
1. Copiare `C:\NFR_Prova\NFR_Registro_prova.xlsx` in `<sync>\Prova_K0\NFR_Registro_sync.xlsx` e aspettare che
   in SharePoint compaia.
2. Aprirlo nel browser (Excel per il web) e scrivere `prova web` nella cella **Z200** del foglio Quadro, che il
   motore non usa. Lasciare aperta la scheda.
3. Sul PC, da `C:\NFR_Prova\pacchetto\07_Senza_Studio`:

   ```
   python esegui_ciclo_locale.py --workbook "<sync>\Prova_K0\NFR_Registro_sync.xlsx" griglia
   ```

   Il comando ricostruisce il foglio Validazione e salva.
4. Dopo 5 minuti annotare:
   - l'esito del comando;
   - se in `Prova_K0` e' comparsa una copia con il nome del PC (copia in conflitto);
   - nella cronologia versioni del file in SharePoint, quante versioni nuove e di chi;
   - riaprendo il file nel browser, se `prova web` c'e' ancora.

**Superata** se, con "Mantieni sempre su questo dispositivo", i tempi stanno sotto i 2 minuti in tutte e due le
direzioni e il conflitto non perde dati in silenzio. Se nasce una copia in conflitto o `prova web` sparisce,
nella CS-1 il registro va chiuso sul web prima di ogni scrittura: e' la regola della CS-1, ora misurata.

## 6. K7b — Excel senza nessuno davanti

1. Creare `C:\NFR_Prova\prova_k7b.cmd` con Blocco note:

   ```
   @echo off
   cd /d C:\NFR_Prova\pacchetto\07_Senza_Studio
   echo %date% %time% attesa di 2 minuti >> C:\NFR_Prova\prova_k7b.log
   timeout /t 120 /nobreak > nul
   echo %date% %time% inizio griglia >> C:\NFR_Prova\prova_k7b.log
   python esegui_ciclo_locale.py griglia >> C:\NFR_Prova\prova_k7b.log 2>&1
   echo %date% %time% fine griglia, codice %errorlevel% >> C:\NFR_Prova\prova_k7b.log
   python esegui_ciclo_locale.py report >> C:\NFR_Prova\prova_k7b.log 2>&1
   echo %date% %time% fine report, codice %errorlevel% >> C:\NFR_Prova\prova_k7b.log
   ```

   `griglia` scrive nel registro di prova; `report` usa Excel per il PDF. Sono le due cose che l'esecutore fa.

| Test | Cosa | Cosa annotare dal log |
|---|---|---|
| K7b.1 schermo bloccato | doppio clic su `prova_k7b.cmd`, poi subito **Win+L**. Sbloccare dopo 6 minuti | i due codici sono 0? Il PDF in `C:\NFR_Prova\Archivio\Cicli\2026Q4\` ha l'ora giusta? |
| K7b.2 avvio automatico | **Win+R**, `shell:startup`, incollare un collegamento a `prova_k7b.cmd`. Riavviare il PC, accedere e bloccare subito lo schermo; sbloccare dopo 6 minuti | come K7b.1. Poi **togliere il collegamento** |
| K7b.3 dopo il riavvio, senza accesso | con il collegamento ancora presente, riavviare e **non** accedere per 5 minuti, poi accedere | dalle ore nel log: il comando e' partito solo dopo l'accesso? Atteso si': l'esecutore ha bisogno di un utente collegato. Poi togliere il collegamento |
| K7b.4 Excel gia' aperto | aprire in Excel un altro file qualsiasi, poi doppio clic su `prova_k7b.cmd` senza bloccare | il motore scrive anche con Excel aperto dall'utente? Il file dell'utente resta intatto? |

Annotare anche le impostazioni di risparmio energia del PC: con la sospensione non gira niente.

**Superata** se K7b.1, K7b.2 e K7b.4 riescono. K7b.3 dice di che cosa ha bisogno l'esecutore; va confrontato con la
risposta dell'IT (D1).

## Tabella dei risultati

| Prova | Esito | Data |
|---|---|---|
| D1 IT: PC esecutore ammesso; avvio automatico; connessione di servizio; Office Scripts | | |
| D2 DPO: trascrizioni; etichette di riservatezza | | |
| 0 Preparazione: registro di prova rifatto senza la riga `kernel`; due run in Agent Builder | | |
| K6 (dalla tabella di `Prova_K6_Operatore.md`), durata del turno in Teams | | |
| K4 AB/AB: rischi in tutti e due, punteggi identici | | |
| K4 CS/CS: rischi in tutti e due, punteggi identici | | |
| K4 AB/CS: rischi in tutti e due, punteggi identici | | |
| K4 precontrollo al primo giro: punti da correggere / da verificare per AB1, AB2, CS1, CS2; modello | | |
| K11 piu' utenti: B senza licenze in piu'; identita' nel flusso; connessione dei flussi; lancio simultaneo; chi vede le trascrizioni | | |
| K12 A7: risposta dai file; tempo di aggiornamento ALFA e BETA; file nuovo | | |
| K7a dal cloud al PC: tre tempi senza e tre con "Mantieni sempre"; con il JSON di A1 | | |
| K7a dal PC al cloud: tre tempi | | |
| K7a conflitto: esito, copia in conflitto, versioni, `prova web` | | |
| K7b: schermo bloccato; avvio automatico; senza accesso; Excel aperto; risparmio energia | | |

## Come si legge

**La CS-1 si puo' fare** se:
- D1 e D2 dicono si';
- K6 e K4 sono superate;
- K7a sta nei tempi;
- K7b.1, K7b.2 e K7b.4 riescono.

K11 e K12 dicono se ha senso: la CS-1 conviene soprattutto con piu' utenti. Con gli esiti si decide la A-15
(TODO, AU4) fra le tre strade di `14_Tre_strade.md`. K6, K4, K11 e K12 valgono anche per la CS-2, che aggiunge
K8 (Office Scripts) e K9 (code interpreter su compiti lunghi).

Dopo le prove, in SharePoint, si puo' cancellare `Archivio_Cicli\Prova_K0`; in Copilot Studio si scollegano i canali
dell'Operatore, se non si prosegue.
