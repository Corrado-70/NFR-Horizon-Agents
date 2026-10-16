# 16. Report e grafici in HTML al posto dei fogli di Excel (variante V4)

Data: 14/10/2026. Richieste dell'utente:

> e se invece di usare excel come base per tutto, si passasse direttamente a report e grafici HTML? sarebbe fattibile e
> più facile da gestire

> credo che in questo modo l'output sarebbe anche pubblicabile su un server http facilmente

> prepara anteprima HTML e analisi di dettaglio dello scenario ricordati di inserire oltre ai vari tab dell'excel le
> singole schede di tutti i rischi

L'analisi si appoggia a `14_Tre_strade.md`, che resta il quadro delle strade A, CS-1 e CS-2, e a
`15_CS2_approfondita.md`, che descrive le varianti V1, V2 e V3 della CS-2. Lo scenario HTML ne diventa una quarta, la
**V4**. A differenza delle altre, vale per **tutte e tre le strade**, non solo per la CS-2.

L'anteprima e' in `16_Anteprima_HTML/` (da aprire con `index.html`); la produce `16_genera_anteprima_html.py`.

## 16.0 In breve

1. **Si puo' fare, e l'anteprima lo mostra con i dati della demo.**
   - Sei report, uno per ciclo dal 2025Q4 al 2026Q4-S1, piu' l'indice dell'archivio.
   - In ogni report ci sono tutte le 17 viste del registro e le **16 schede dei rischi**: i 13 del radar e i 3 in
     osservazione.
   - Per il ciclo corrente **118 numeri su 118** coincidono con quelli calcolati dalle formule di Excel: X, Y, Z,
     margine, urgenza, livello di allerta e motivo, segnali netti, ordine della classifica, Delta.
2. **Excel oggi fa tre lavori. L'HTML ne sostituisce uno solo, il piu' costoso.**
   - **Vista** (report, grafici, PDF): passa all'HTML.
   - **Archivio dei dati**: passa a un file di dati semplice, senza formule ne' grafici. E' un `.xlsx` "muto" scritto
     con openpyxl, oppure JSON (16.2).
   - **Posto dove le persone scrivono** (griglia di validazione, parametri): resta Excel, ma generato e riletto da
     Python, senza Excel via COM ne' Office Scripts.
3. **Si toglie molto.**
   - `genera_dashboard.py` (4.083 righe) e il template.
   - Excel via COM: `excel_com.py` e le circa 1.400 righe del motore che lo usano.
   - Circa un terzo delle 110 trappole del PROMPT_MASTER.
   - Nella CS-2: l'Office Script esecutore della V2 e la prova K8.

   Il prototipo che fa tutte le viste, le schede e i grafici e' di circa 2.000 righe, e la meta' sono pagine HTML e CSS.
4. **La V4 e' la V3 dell'analisi 15 resa semplice.** La V3 era sconsigliata per due motivi:
   - riscrivere un `.xlsx` pieno di formule e grafici senza Excel (XML, nessun ricalcolo);
   - sostituire un file che le persone modificano.

   Nella V4 il file dei dati non ha formule, perche' le viste le calcola Python, e nessuno lo modifica a mano: si
   scrive con openpyxl senza rischi.
5. **I vincoli sono di consegna, non di calcolo** (16.5, 16.6).
   - SharePoint Online **scarica** i file `.html` invece di mostrarli, e non c'e' un'impostazione del tenant che lo
     cambi.
   - Il PDF per il comitato si fa con "Convert file", che accetta l'HTML fino a **2 MB**: e' da provare.
   - Pubblicare su un server HTTP e' facile solo tecnicamente: i dati sono riservati, quindi serve un server interno
     con accesso autenticato, deciso con l'IT.
6. **Raccomandazione** (16.10):
   - adottare la V4 come direzione per le viste, **al posto della V2** se la prova K14 va bene;
   - partire dalla strada A, dove la V4 toglie Excel desktop dal PC senza aspettare Copilot Studio;
   - la decisione e' nuova: la propongo come **A-16**.

## 16.1 Che cosa fa Excel oggi: tre lavori

| Lavoro | Dove sta oggi | Chi lo tocca | Codice che lo regge |
|---|---|---|---|
| **Archivio dei dati** | 7 tabelle dati (RiskRegister, Azioni, KRI, NewsLog, Sintesi_Cicli, Sintesi_Settimane, Storico_Validazioni), anagrafica e parametri (foglio Parametri) | solo lo script (D-10); a mano i testi (D-76), lo Stato delle azioni, le celle gialle dei parametri | `Scrittore` e `excel_com.py`: nomi definiti, riga segnaposto, capienza delle tabelle, formule scritte riga per riga |
| **Posto dove le persone scrivono** | foglio Validazione (una riga per oggetto, D-67), celle gialle di Parametri, colonna Stato di Azioni | validatore, funzione di rischio | griglia con formule e convalide, letta via COM dal comando `valida` |
| **Vista** | 17 fogli: Quadro, Classifica, Radar_Mosca, Matrice, Delta, Fenomeni, Metodologia, Registro, Storico, Indicatori, Notizie, Piano_azioni, Osservazione, Validazione, Parametri, Dizionario, Guida; il PDF di 7 fogli; le schede in `Schede_<ciclo>.xlsx` | nessuno: sono formule | `genera_dashboard.py` (4.083 righe): formule con OFFSET e AGGREGATE, colonne di appoggio nascoste, nomi dinamici per i grafici, formattazioni condizionali; impaginazione via COM |

La vista e' la parte piu' grande e piu' fragile. Gran parte delle trappole viene da qui, per esempio:
- i nomi definiti che scivolano;
- le serie dinamiche del radar;
- i valori in cache vecchi;
- l'Excel che non parte;
- il salvataggio in attesa.

Anche il costo della CS-2 viene da qui: la V2 esiste per far scrivere e ricalcolare un file pieno di formule dentro il
vero Excel.

## 16.2 Lo scenario V4: "i dati in un file semplice, Python calcola, l'HTML mostra"

```
Agenti (A1, A3, A5, A6, A8) ─> JSON ─> motore Python ─┬─> NFR_Dati.xlsx       tabelle dati, parametri, anagrafica:
                                     (controlli D-10,  │                       solo valori, nessuna formula
                                      regola del radar,├─> Horizon_Scan_<ciclo>.html   report, grafici, schede
                                      viste)           ├─> Validazione_<ciclo>.xlsx    griglia da compilare
                                                       └─> archivio, testi per A7, PDF
Validatore ─> Validazione_<ciclo>.xlsx ─> motore (valida) ─> NFR_Dati.xlsx + report rigenerato
```

### Il file dei dati

Si scrivono le stesse tabelle di oggi, con le stesse colonne della mappa dei campi (`01_Kernel/mappatura_campi.json`).
Le colonne con `sorgente: formula:` diventano valori calcolati dal motore, e le viste spariscono dal file.

| Forma | Quando | Perche' |
|---|---|---|
| **`.xlsx` senza formule** (consigliata) | in tutte e tre le strade | nella CS-2 il prompt con code interpreter accetta un solo file in ingresso, Office ma non `.json` ne' `.txt` (15.2). openpyxl lo legge e lo scrive per intero: senza grafici ne' formule non perde niente. Si apre in Excel per controllare o filtrare. Lo storico delle versioni di SharePoint lo conserva |
| JSON (`dati_registro.json`, come nell'anteprima) | in piu', come copia di pubblicazione o di archivio | nativo per i flussi e per il JavaScript della pagina; diff leggibili; non entra nel code interpreter |
| Liste SharePoint | no | multiutenza nativa, ma 7 liste da tenere coerenti, limiti di vista, e un terzo modo di accedere ai dati |

Nessuno modifica a mano il file dei dati. I testi (D-76) e lo Stato delle azioni si correggono con un comando o
passano per la griglia. Cosi' sostituire il file intero non perde modifiche, e cade il secondo motivo per cui la V3 era
sconsigliata.

### La vista

- Un **file HTML per ciclo**, autosufficiente:
  - nessuna risorsa esterna;
  - grafici in SVG scritti da Python;
  - navigazione senza JavaScript (CSS `:target`);
  - il poco JavaScript aggiunge solo i tooltip, il filtro e lo scaricamento in CSV delle tabelle dati.
- Un **indice** che elenca i cicli: e' l'archivio, consultabile.
- Le **schede dei rischi** sono pagine dello stesso file, non un `Schede_<ciclo>.xlsx` a parte. A6 resta com'e':
  scrive testi e i controlli di `schede.controlla_a6` restano.
- Il **PDF** si fa dallo stesso HTML (16.5).

### La validazione

La griglia di oggi (foglio Validazione, D-67) diventa un file a parte, `Validazione_<ciclo>.xlsx`:
- la genera il motore con openpyxl: una riga per oggetto, celle gialle, convalide a elenco, segnalazioni in colonna P;
- il validatore la compila in Excel desktop o in Excel per il web;
- il comando `valida` la rilegge con openpyxl.

Restano le regole di oggi:
- blocco del ciclo dopo se il precedente non e' validato;
- proposta dell'agente sempre conservata;
- riapertura ripetibile (D-76).

### Che cosa cambia nelle tre strade

| Strada | Oggi | Con la V4 |
|---|---|---|
| **A**, tutto sul PC | Python + Excel desktop via COM: trappole, Excel che non parte, registro aperto da qualcuno | Python + openpyxl: **niente Excel desktop nel motore**. Il PC esegue solo Python; Excel serve a chi compila la griglia |
| **CS-1**, ibrida | il PC esecutore deve tenere un utente collegato, perche' Excel via COM non gira come servizio (14.4) | il motore non apre Excel: il PC esecutore puo' essere un **servizio** o un'attivita' pianificata. Cade il contro piu' pesante della CS-1 |
| **CS-2**, tutto in Copilot Studio | V2: Python nel code interpreter decide, un Office Script esecutore scrive dentro Excel per il web | V4: Python nel code interpreter decide **e scrive** il file dei dati e il report; il flusso controlla l'impronta (come nella V2), estrae i file e li salva. **Niente Office Scripts** |

Nella CS-2 restano due punti da provare (K14, 16.9):
- **un solo file in uscita dal prompt.** Il code interpreter produce uno zip con dati, report e griglia, e il flusso lo
  estrae con "Extract archive to folder" (50 MB, 100 file). Da provare: che il prompt restituisca uno zip;
- **un solo file in ingresso.** L'output di A1 e il codice del motore entrano nel file dei dati in una tabella
  `_Scambio`, come nella V2, scritta dal flusso con il connettore Excel Online ("Add a row"). Il blocco fino a 6
  minuti del connettore (15.2) si evita scrivendo su una **copia di lavoro** del file: il prompt legge la copia, il
  flusso aggiorna l'originale con il file restituito.

## 16.3 L'anteprima

### Dove e come si rigenera

```
cd Analisi_Architettura
python 16_genera_anteprima_html.py            # legge Demo_W1_W2/NFR_Registro.xlsx, scrive 16_Anteprima_HTML/
```

| File | Dimensione | Contenuto |
|---|---|---|
| `index.html` | circa 25 KB | archivio: un ciclo per riga, con tipo, data, validazione, rischi nel radar e in osservazione, in attivazione, KRI in rosso, messaggio di A1 |
| `Horizon_Scan_2025Q4.html` ... `Horizon_Scan_2026Q4-S1.html` | da 330 KB a 1,3 MB | un report per ciclo. Per il 2026Q4-S1 la pagina "Tabelle dati" pesa il 61% (770 KB); senza, il report e' di circa 500 KB |
| `dati_registro.json` | 580 KB | le tabelle dati in JSON, cioe' la "base" dello scenario |

Lo script legge **solo** le tabelle dati, i parametri e l'anagrafica del registro della demo: cioe' quello che nello
scenario sta nel file dei dati. Le viste le ricalcola tutte. Le viste di Excel le legge solo per il confronto finale.

### Pagine e fogli

| Gruppo | Pagina dell'HTML | Foglio di oggi | Note |
|---|---|---|---|
| Report al comitato | Quadro d'insieme | Quadro | cinque riquadri, priorita', matrice piccola, radar piccolo, commento di A1, rischi segnalati con il perche' |
| | Classifica | Classifica | barre per score colorate per urgenza, lente di Mosca (X, Y entro Z, Y oltre Z, Z) |
| | Radar di Mosca | Radar_Mosca | radar a nove settori; tabella con X, Y, Z, margine, livello e motivo |
| | Matrice | Matrice | 5 x 5 con i nomi delle probabilita' e degli impatti |
| | Delta | Delta | barre divergenti, motivi con l'evidenza, dettaglio per dimensione |
| | Rischi in osservazione | Fenomeni | registro unico (D-79), entrati e usciti |
| | Metodologia | Metodologia | testo del foglio |
| Lavoro | Registro | Registro | un rischio per riga, con il livello sul bordo dell'ID |
| | Storico | Storico | andamento su scala fissa 1-5 per rischio |
| | Indicatori (KRI) | Indicatori | tabella dei KRI e **la storia di tutti i KRI** a piccoli multipli (nell'Excel uno alla volta, cella N4) |
| | Notizie | Notizie | intensita' per categoria, presidio, pressione di 12 settimane, sintesi di A3, proposta di straordinario |
| | Piano azioni | Piano_azioni | con la scadenza calcolata |
| | Osservazione | Osservazione | incroci driver x categoria |
| | Validazione | Validazione | **l'esito**, non la griglia: decisioni per oggetto, rettifiche e respingimenti con il motivo, notizie in attesa |
| | Parametri | Parametri | pesi, Mosca, livello di allerta, registro unico, regola, tassonomia, driver, anagrafica |
| | Dizionario | Dizionario | testo del foglio |
| Schede | Indice e 16 schede | `Schede_<ciclo>.xlsx` | il radar in ordine di classifica, poi l'osservazione; navigazione precedente e successiva |
| Dati | Tabelle dati | RiskRegister ... Storico_Validazioni | fino al ciclo del report; filtro e CSV |
| Aiuto | Guida | Guida | come si usa il report; pagine e fogli di oggi |

### Che cosa dimostra

1. **Le formule del registro si portano in Python senza perdere un numero.**
   - Per il 2026Q4-S1 l'anteprima confronta 118 valori con quelli calcolati da Excel e coincidono tutti.
   - Per 13 rischi: Z, X, Y, margine, testo dell'urgenza, livello, motivo del livello e segnali netti; poi l'ordine
     della classifica e i 13 Delta.
   - Il confronto ha trovato una trappola: `round()` di Python porta 1,25 a 1,2, mentre `ROUND` di Excel lo porta a
     1,3. "Margine 1,2 anni" contro "Margine 1,3 anni" per NFR-09. Si risolve con `Decimal` e `ROUND_HALF_UP`. Vale per
     ogni riscrittura in Python di una formula di Excel, compreso l'adattatore della V2 (trappola 111 del
     PROMPT_MASTER).
2. **La logica del pacchetto e' gia' separabile da Excel.**
   - `schede.input_schede` gira **invariata** con un lettore di 40 righe che le passa i dati e le viste calcolate in
     Python al posto della sessione COM.
   - E' la stessa interfaccia che la V2 chiama "adattatore del registro".
3. **Il report si legge senza installare niente e si stampa.**
   - La navigazione non usa JavaScript, quindi funziona anche se una policy del browser lo blocca.
   - La stampa da Chrome produce un PDF A4 di 59 pagine per il 2026Q4-S1: report al comitato (12 pagine), lavoro
     (21, di cui 8 di Dizionario), 16 schede (25), guida. Le tabelle dati non si stampano.
   - Tema chiaro e scuro, larghezza da telefono.
4. **Un archivio per ciclo viene gratis.** Ogni file e' la fotografia del ciclo, con le tabelle dati fino a quel
   ciclo.

### Limiti dell'anteprima

- I dati si leggono dal `.xlsx` della demo, che ha anche le viste: il file dei dati senza formule (16.2) non e' ancora
  scritto.
- **Attenzione del supervisore e presidio dei controlli non sono storicizzati**: il registro li tiene solo
  nell'anagrafica di oggi. Per i cicli passati l'anteprima usa quelli di oggi, quindi il livello di allerta di un
  ciclo passato puo' differire da quello che Excel mostrava allora.
  - Nella V4 vanno storicizzati: due colonne nel RiskRegister, scritte alla validazione.
  - E' una lacuna gia' presente oggi, che il report per ciclo rende visibile.
- Il confronto con Excel copre solo il ciclo corrente: i valori dei cicli passati Excel non li conserva.
- I testi di A6 non ci sono, perche' la demo genera le schede senza A6: si vedono i testi di A1 dal registro.
- La griglia di validazione in file a parte non e' fatta.
- Non e' provato in Banca: apertura da SharePoint, policy di Edge, "Convert file" (K14).
- La pagina Validazione conta le "rettifiche applicate" come la formula di oggi, cioe' solo `Rettificato` e non
  `Rettificato (riapertura)`. E' una scelta del registro, riprodotta tale e quale.

## 16.4 Che cosa si toglie e che cosa si aggiunge

| Si toglie | Righe o volume | Nota |
|---|---|---|
| `03_Excel/genera_dashboard.py` e `NFR_Dashboard_Template.xlsx` | 4.083 | piu' `costruzione_manuale_template.md` |
| `excel_com.py` e l'accesso a Excel nel motore (`Scrittore`, impaginazione, controllo errori e formule, PDF via COM) | circa 1.400 + 132 | sostituiti da un lettore e scrittore openpyxl |
| Comando `aggiorna-registro` (migrazione del template) | parte del motore | lo schema dei dati si migra aggiungendo colonne: niente template da ricostruire |
| Trappole del PROMPT_MASTER legate a Excel | circa 35 su 110, a una prima conta per parole chiave | la sezione WORKBOOK (circa 370 righe) diventa la sezione REPORT |
| CS-2: Office Script esecutore e prova K8 | 250-350 righe di TypeScript | e D-02 ("niente Office Scripts") non va rivista |

| Si aggiunge | Righe (dal prototipo) | Nota |
|---|---|---|
| Motore delle viste (Mosca, livello, classifica, Delta, notizie, piano, osservazione, validazione) | circa 300 | Python puro; nel prototipo classe `Vista` |
| Grafici SVG (radar, classifica, lente, Delta, notizie, pressione, sparkline, KRI) | circa 320 | |
| Pagine HTML e schede | circa 830 | testi e legende riusati dal registro |
| CSS e JavaScript | circa 220 | una volta sola |
| Lettore e scrittore del file dei dati (openpyxl) | 150-250 | il prototipo ha solo il lettore |
| Griglia di validazione in file a parte | 250-350 | oggi e' nel generatore (formule) e nel motore (lettura COM) |

Il saldo e' di circa 2.300 righe in piu' contro circa 5.600 in meno. Il codice aggiunto e' Python puro e si collauda
senza Excel, quindi in secondi.

## 16.5 Pubblicare: SharePoint, server HTTP, Teams

| Dove | Come si vede | Pro | Contro |
|---|---|---|---|
| **Library SharePoint** (archivio) | il file `.html` **si scarica** e si apre nel browser: SharePoint Online non mostra mai gli HTML, e nessuna impostazione del tenant lo cambia | e' gia' l'archivio; versioni; permessi | un passaggio in piu' per chi legge; il trucco di rinominare in `.aspx` richiede script personalizzati sul sito: **escluso** in una banca |
| **PDF in SharePoint** | si apre nel browser | e' quello che il comitato riceve gia' | statico: niente tooltip ne' collegamenti |
| **Cartella sincronizzata** (OneDrive) | doppio clic sul file | semplice per il gruppo di lavoro | serve la sincronizzazione sul PC |
| **Server web interno** (intranet) | un indirizzo, con l'accesso dell'intranet | la via piu' semplice se l'IT concede uno spazio; i file sono statici | decisione dell'IT; la copia sul server la fa un processo dell'IT o una persona |
| **Azure Static Web Apps o storage con login Entra ID** | un indirizzo con accesso aziendale | e' il servizio fatto apposta per file statici | sottoscrizione Azure gestita dall'IT; pubblicazione da un flusso con il connettore HTTP, che e' **premium** |
| **Scheda di Teams** | il sito dentro Teams | dove gli utenti gia' lavorano | serve uno dei due precedenti |

Altri due punti:
- **A7 legge l'HTML.** La knowledge degli agenti accetta `.html` (PROMPT_MASTER, vincoli della piattaforma). Il
  report del ciclo puo' affiancare o sostituire i testi di `Kernel\Spiegazioni`: e' da valutare con K12.
- **Riservatezza.** Il report e' "Uso interno". Qualunque server deve avere accesso autenticato; gli hosting pubblici
  sono esclusi. Il file e' autosufficiente proprio per non dipendere da CDN esterne, che il proxy della Banca
  potrebbe comunque bloccare.

**Il PDF del comitato.**
- Nella strada A: stampa del browser oppure Chrome o Edge senza interfaccia (`--print-to-pdf`), come nell'anteprima.
- Nella CS-2: "Convert file" del connettore OneDrive, che accetta `htm` e `html` come sorgente per il PDF, con un
  **limite di 2 MB** e "problemi noti" documentati sulla conversione da HTML.

Per stare sotto i 2 MB, il PDF si fa da un HTML ridotto: senza tabelle dati e, se serve, senza Dizionario. Va provato
che "Convert file" capisca il CSS di stampa e gli SVG (K14).

Se "Convert file" non e' fedele, il PDF lo fa a mano chi apre il report e lo stampa: un gesto, non un blocco, come per
K10 nella V2.

## 16.6 Vincoli, rischi, contromisure

| # | Vincolo o rischio | Effetto | Contromisura | Da verificare |
|---|---|---|---|---|
| 1 | SharePoint scarica gli HTML | chi legge da SharePoint deve scaricare e aprire | PDF accanto all'HTML; cartella sincronizzata; server interno | gia' noto (Learn, community Microsoft) |
| 2 | Policy di Edge sui file locali o sul JavaScript | tooltip e filtri non funzionano | la navigazione e' senza JavaScript; ogni grafico ha la sua tabella | K14 |
| 3 | "Convert file": 2 MB e fedelta' dell'HTML | PDF incompleto o diverso | HTML ridotto per il PDF; stampa a mano come riserva | K14 |
| 4 | Code interpreter: un file in ingresso, uno in uscita, 100 secondi | nella CS-2, dati, report e griglia escono insieme | zip estratto dal flusso; sul PC lettura dei dati, viste e sei report richiedono meno di un secondo | K14 (e K9) |
| 5 | Excel per il web cambia i tipi quando una persona scrive nella griglia ("5/6" diventa una data) | valori sbagliati in validazione | convalide a elenco e celle di testo; `valida` rilegge e controlla, come oggi (trappola dei testi in cella) | collaudo |
| 6 | Il file dei dati viene sostituito per intero | modifiche concorrenti perse | nessuno lo modifica a mano; un solo scrittore, il motore (D-10); lucchetto nel flusso o sul PC | K13 |
| 7 | Gli utenti sono abituati a Excel (filtri, copia per le slide) | resistenza, richieste di "rimettere l'Excel" | CSV per tabella; il file dei dati si apre in Excel in sola lettura; grafici con tabella accanto | utenti |
| 8 | Evidenza e integrita' del report archiviato | un HTML si puo' modificare dopo | storico delle versioni e conservazione in SharePoint; **impronta SHA-256 del file dei dati nel piede del report** e nell'archivio | proposta |
| 9 | Il file del ciclo cresce con le tabelle dati | dopo qualche anno, file di molti MB | tabelle dati solo del ciclo, o il collegamento al file dei dati dell'archivio | quando servira' |
| 10 | Due implementazioni delle viste durante il passaggio (Excel e Python) | divergenze | il collaudo di oggi su Excel fa da **oracolo**: le catene di prova si confrontano sui due lati finche' Excel resta | T2 |

## 16.7 Confronto con la V2 e con oggi

| Criterio | Oggi (strada A) | V2 (CS-2) | **V4** |
|---|---|---|---|
| Dove si calcolano le viste | formule di Excel (4.083 righe di generatore) | formule di Excel | **Python**, come le regole |
| Chi scrive il registro | Python via COM su Excel desktop | Office Script dentro Excel per il web | **Python con openpyxl** (sul PC o nel code interpreter) |
| Linguaggi | Python, formule di Excel | Python, TypeScript, formule | **Python** (piu' HTML e CSS generati) |
| Componenti in esercizio nella CS-2 | — | Copilot Studio, flussi, code interpreter, Office Scripts, SharePoint | Copilot Studio, flussi, code interpreter, SharePoint |
| Excel desktop sul PC del motore | si' | no | **no**, in tutte le strade |
| Collaudo delle viste | catene su Excel reale, lente | come oggi, piu' le prove nel tenant | **Python puro, in secondi**; Excel solo come oracolo nel passaggio |
| PDF | Excel via COM | "Convert file" su una copia del registro (K10) | stampa del browser (A) o "Convert file" su HTML (CS-2, K14) |
| Grafici | grafici di Excel con serie dinamiche; il radar e' un dispersione con trucchi | come oggi | SVG: radar, lente e piccoli multipli liberi; tooltip e collegamenti alle schede |
| Pubblicazione | file Excel e PDF | come oggi | HTML statico pubblicabile su qualunque server interno, PDF, CSV |
| Migrazione dello schema | `aggiorna-registro` ricostruisce dal template | come oggi | colonne aggiunte al file dei dati; le viste nuove non toccano i dati |
| Manutenzione grafica | generatore di fogli, celle, merge, altezze | come oggi | HTML e CSS: piu' semplice da cambiare e da provare (anteprima in un browser) |
| Rischio tecnico | noto (trappole) | Office Scripts nel tenant (K8), motore nel prompt (K9) | motore nel prompt (K9, come la V2), zip in uscita e "Convert file" (K14) |
| Impegno, strada A | — | — | **15-20 giorni** |
| Impegno, CS-2 | — | 30-42 giorni (15.4) | **circa 28-38 giorni**: niente Office Script e adattatore Excel, in piu' viste e report |

La V4 non costa meno della V2 la prima volta. Costa meno **dopo**:
- un solo linguaggio;
- un collaudo che non apre Excel;
- grafiche che si cambiano in un browser;
- niente template da migrare.

E serve anche alla strada A e alla CS-1 da subito.

## 16.8 Effetti su agenti, kernel, decisioni, collaudo e documenti

- **Agenti**: invariati. A1, A3, A5, A8 scrivono JSON; l'allegato di A1 e il precontrollo li costruisce gia' Python.
  A6 riceve lo stesso input (`schede.input_schede`). A7 puo' leggere il report HTML come knowledge (16.5).
- **Kernel**:
  - `mappatura_campi.json` resta la fonte delle colonne;
  - le colonne `formula:` diventano funzioni del motore delle viste;
  - la rubrica (sezione 8, Mosca e livello) resta la fonte dei parametri.
- **Decisioni**:
  - **D-10** resta: nel registro scrive solo il motore, dopo i controlli. Nella CS-2 vale la formulazione della V2,
    "esito accettato solo con l'impronta del motore vero";
  - **D-02** e **D-11** come nella V2 per il code interpreter; D-02 non va toccata per gli Office Scripts;
  - **D-39** (file unico con report e registro) va rivista: dati, report e griglia diventano tre file;
  - **D-40** (schede in un file a parte): le schede entrano nel report;
  - **D-67** (validazione in griglia): invariata nella sostanza, in un file a parte;
  - nuova **A-16** (16.10).
- **Trappola 110 del PROMPT_MASTER**: la terza regola ("il registro lo scrive solo codice deterministico dentro Excel,
  che ricalcola") vale per un registro con formule. Nella V4 il file dei dati non ne ha e la premessa cade. Le altre
  due regole restano.
- **Collaudo**:
  - le 800 e piu' verifiche delle regole restano;
  - le verifiche delle viste si riscrivono su Python;
  - durante il passaggio, le catene di prova girano anche su Excel e si confrontano le viste (oracolo), come il
    confronto dell'anteprima.
- **Documenti** da riscrivere quando si decide: guida (parte sull'uso del registro), PROMPT_MASTER (sezioni WORKBOOK,
  SCRIPT DI CAMPO, COLLAUDO, TRAPPOLE), `00_LEGGIMI`, `struttura_e_liste.md`, demo.

## 16.9 Percorso a tappe, prova K14 e stima

| Tappa | Che cosa | Giorni | Serve anche se ci si ferma qui |
|---|---|---|---|
| T0 | **Anteprima** (fatta il 14/10) | — | per decidere |
| T1 | **Prova K14** nel tenant, con i file dell'anteprima (sotto) | 0,5-1 | si' |
| T2 | **Motore delle viste nel pacchetto** (`viste.py`), con il confronto contro Excel su tutte le catene del collaudo | 3-4 | si': report HTML accanto all'Excel di oggi, senza togliere niente |
| T3 | **Report HTML e schede nel pacchetto** (comando `report-html`), PDF dalla stampa del browser | 2-3 | si': il comitato puo' ricevere il report nuovo |
| T4 | **File dei dati senza formule** (scrittore openpyxl), migrazione una tantum dal registro di oggi, storicizzazione di supervisore e presidio | 3-4 | si': il motore non apre piu' Excel (strada A) |
| T5 | **Griglia di validazione in file a parte** (genera e rileggi con openpyxl) | 2-3 | con T4, niente Excel via COM |
| T6 | Togliere COM, generatore e template; collaudo, guida, PROMPT_MASTER, demo | 3-4 | fine della strada A con la V4 |
| T7 | CS-2 con la V4: flussi, `_Scambio`, zip, PDF con "Convert file" (oltre alla parte comune della CS-1) | 12-18 | obiettivo dell'utente |

Strada A con la V4: T1-T6, circa **15-20 giorni**. CS-2 con la V4: T1-T7, circa **28-38 giorni** compresa la parte
della CS-1 che serve.

### Prova K14: report HTML e file dei dati nel tenant

| Passo | Che cosa | Come | Superata se |
|---|---|---|---|
| K14.1 | Apertura | caricare `16_Anteprima_HTML/` in una library; aprire un report da SharePoint (download) e dalla cartella sincronizzata, in Edge | si apre; menu, collegamenti alle schede, tooltip e filtro funzionano; nessun avviso bloccante |
| K14.2 | PDF | "Convert file" sul report ridotto (senza tabelle dati), da un flusso | PDF prodotto sotto i 2 MB; grafici SVG presenti; una pagina per vista e per scheda |
| K14.3 | Code interpreter | prompt con un `.xlsx` senza formule in ingresso (le tabelle della demo); il codice genera il report e uno zip con report e dati | zip restituito; tempo sotto i 100 secondi; il flusso lo estrae con "Extract archive to folder" |
| K14.4 | Knowledge | aggiungere un report alla knowledge di A7 | A7 risponde citando il report |

Se K14.2 fallisce, il PDF si fa a mano. Se K14.3 fallisce, la V4 resta per la strada A e la CS-1, e nella CS-2 il report
esce come unico file mentre i dati restano alla V2.

## 16.10 Raccomandazione e decisione da prendere

**Raccomandazione.**
- Adottare la V4 come direzione per le viste e per il file dei dati.
- Partire dalle tappe T2-T3, che non tolgono niente: il report HTML nasce accanto all'Excel di oggi, si confronta con
  lui e si fa vedere al comitato.
- Poi T4-T6, che tolgono Excel desktop dal motore gia' nella strada A.
- La CS-2 si fa con la V4 al posto della V2, se K14 e K9 vanno bene.

Le ragioni:
- toglie la parte piu' grande e fragile del pacchetto, invece di spostarla dentro Excel per il web;
- lascia un solo linguaggio per regole e viste;
- da' un report pubblicabile e un archivio per ciclo;
- e' utile in tutte e tre le strade, quindi non dipende dalla decisione A-15.

**Decisione proposta, A-16**: "Report in HTML generato da Python al posto delle viste di Excel; registro come file di
dati senza formule; Excel solo per la griglia di validazione". Si chiude dopo la prova K14 e la tappa T2.

Non cambia:
- nel registro scrive solo il motore (D-10);
- validazione umana obbligatoria, con lo storico delle proposte;
- kernel, prompt e controlli.

## Fonti (consultate il 14/10/2026)

- [Connettore OneDrive for Business](https://learn.microsoft.com/en-us/connectors/onedriveforbusiness/): "Convert file"
  e "Extract archive to folder" (50 MB, 100 file); rimando ai problemi noti della conversione da HTML a PDF.
- [Microsoft Graph, Convert to other formats](https://learn.microsoft.com/en-us/graph/api/driveitem-get-content-format?view=graph-rest-1.0):
  formati sorgente per il PDF (compresi `htm` e `html`); limite di 2 MB per la conversione.
- [Microsoft Q&A, file HTML in SharePoint Online](https://learn.microsoft.com/en-us/answers/questions/321942/issue-in-loading-html-files-in-sharepoint-online(m)) e
  [Tech Community, aprire gli HTML nel browser](https://techcommunity.microsoft.com/discussions/sharepoint_general/open-html-files-in-browser---sharepoint-online/130620/replies/718132):
  SharePoint Online scarica gli HTML e non ha un'impostazione del tenant per mostrarli.
- Analisi 15 (15.2 e fonti dell'11/10) per i limiti del code interpreter, degli Office Scripts e del connettore Excel
  Online.
