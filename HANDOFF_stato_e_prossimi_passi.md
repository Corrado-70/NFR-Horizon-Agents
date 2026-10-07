# HANDOFF — Sistema di agenti NFR Emerging Risk

> Stato al 30/09/2026 (prima installazione reale in corso: sezione 2-quinquies;
> report al comitato, D-19 e aggiornamento del registro: sezione 2-sexies;
> guida nei fogli, P3, P6, P11, versione 2026-09-25b: sezione 2-septies;
> registro ridisegnato e agente A6 delle schede, versione 2026-09-25c:
> sezione 2-octies; piano di automazione: 2-decies; **primo ciclo reale e
> semplificazione dello scoring, versione 2026-09-30: sezione 2-undecies**;
> **revisione della rubrica del responsabile, versione 2026-09-30b: sezione
> 2-duodecies**; **livello di allerta, KRI per tipo, esposizione nella
> Probabilita, versione 2026-09-30c: sezione 2-terdecies**; installazione sul PC
> della Banca e sintesi settimanale di A3, versione 2026-10-01: sezione
> 2-quaterdecies; **validazione in una griglia, versione 2026-10-02: sezione
> 2-quindecies**; **schede con il perche' di ogni numero, D-68: sezione
> 2-sexdecies**; **allegato di A1 con i controlli di A5 e la guida di
> scrittura, precontrollo prima di A5, D-69: sezione 2-septdecies**; **prove
> sul PC della Banca e prova di Copilot Studio con il precontrollo dentro A1
> in due opzioni del codice, D-70, pacchetto del 05/10: sezione 2-octodecies**;
> **A5 facoltativo e segnalazioni in validazione, D-71, struttura 2026-10-06:
> sezione 2-novodecies**; **piano degli agenti nuovi e fase 1, A7 Assistente del registro, D-72,
> struttura 2026-10-07: sezione 2-vicies**).
> Pacchetto **rigenerato da zero** il 23/09 con
> `PROMPT_MASTER_rigenerazione.md` in `NFR_Emerging_Risk_Agents/`, collaudato
> a secco (la suite completa, catena compresa, su Excel desktop reale). Nel
> tenant della Banca gira la variante locale dal 24/09. La versione precedente di questo documento, che
> descriveva il pacchetto del 22/09 (zip in Downloads), e' in
> `HANDOFF_precedente_pacchetto_2026-09-22.md`.

## 1. Scelte dell'utente per questa rigenerazione

- Ambiente di destinazione: **solo Microsoft 365 Copilot**, senza Copilot
  Studio ne' Power Automate -> prodotta anche la variante `07_Senza_Studio/`.
- **Solo Python**, niente TypeScript/Office Script; meno dipendenze possibile
  oltre a M365 -> lo script di campo scrive tramite **Excel desktop via COM**
  (pywin32), non con openpyxl.
- **Da zero**, privilegiando la semplicita' di gestione e di modifica.

## 2. Cosa esiste

Indice completo e ordine di deploy: `NFR_Emerging_Risk_Agents/00_LEGGIMI.md`.
In breve: kernel (tassonomia, rubrica, tre schemi, mappa campi), quattro prompt
generati da modelli, generatore del workbook e template, SharePoint, workflow,
governance, variante locale (script di campo), suite di collaudo.

## 2-bis. Aggiunte del 23/09 pomeriggio (richieste dell'utente)

1. **12 rischi di esempio** (erano 6): il radar e' pieno. Il radar della
   Dashboard ha serie DINAMICHE (nomi `radarRischi`, `radarCorrente`...,
   OFFSET sul numero di rischi in anagrafica; nel file del grafico si scrivono
   `[0]!nome`, verificato su Excel): un raggio per rischio, mai raggi vuoti.
   `MAX_RISCHI` = 15. Il rischio nuovo della catena di prova e' ora NFR-13.
2. **Probabilita** (1-5, frequenza attesa): nuova valutazione di A1, fuori dal
   composito (la scala storica non cambia), con le regole di variazione.
   Prompt A1 a 7.884 caratteri (accorciate due frasi della rubrica).
3. **Urgenza con la disuguaglianza di Mosca** (X + Y > Z = agire ora),
   calcolata dal foglio **Radar_Mosca**: Z dalla Prossimita (tabella in
   Parametri), X = 0,25 anni, Y = orizzonte delle azioni non respinte.
   Grafico a dispersione polare: distanza dal centro = margine + 2, area del
   cerchio = P x I, settore = event type, cerchi a 0 (Mosca), 1, 2 e 3 anni.
   Metodo e limiti: rubrica, sezione 8. Adattamento del
   pacchetto, **da validare** dalla funzione di rischio.
4. **Validazione umana tracciata**: foglio/tabella Validazione (una riga per
   campo proposto), comando `valida`, blocco del trimestre successivo se il
   precedente non e' validato, proposta dell'agente sempre conservata (base
   dati per l'apprendimento). Sostituisce la compilazione manuale di
   `Approvato_Da`.
5. **Guida per l'utente** `00_GUIDA_PASSO_PASSO.md`; il collaudo verifica che
   comandi e opzioni citati esistano.

## 2-ter. Analisi dell'architettura (23/09 sera)

In `Analisi_Architettura/` (dieci documenti; il 07 e' il piano senza Python del
24/09, l'08 il confronto con un Horizon Scanning fatto con Copilot del 25/09,
il 09 la proposta grafica del report (approvata), il 10 il piano di
automazione per l'analista del 27/09, proposta non approvata, con dal 28/09
l'opzione separata Copilot Studio e i passi comuni alle due strade;
il 06 e' il focus su R2, agente
operativo in Copilot Studio, con piano R0-R9): stato attuale con misure e
debolezze; quattro alternative con gli stessi vincoli (Office Scripts, agenti
piccoli, piu' workbook + report di aggregazione, report generato); due con
Copilot Studio (pipeline orchestrata, agente operativo); confronto pesato;
piano di rigenerazione in otto fasi a partire dal report trimestrale.
Raccomandazione: con i vincoli attuali evolvere verso "dati separati dal
report + report trimestrale in PowerPoint"; **verificare subito con l'IT se
Copilot Studio e' abilitabile**: secondo Microsoft Learn (03/08/2026) la
licenza Microsoft 365 Copilot e' una delle configurazioni che danno accesso a
Copilot Studio. (28/09: Copilot Studio e' disponibile, D-44; se usarlo e'
A-15.)

## 2-quater. Revisione del software e correzioni (23/09 notte)

Revisione completa del codice e dei documenti; ogni correzione ha un test.
- **A5 del ciclo giusto**: la scrittura rifiutava nulla se l'esito di A5 era
  di un altro trimestre (provato: A1 2026Q3 + A5 2026Q4 scritto con codice 0).
  Ora si ferma, anche se A5 cita rischi assenti dall'output di A1.
- **Coerenza dopo la validazione**: le Variazioni restavano quelle dell'agente
  dopo una rettifica (NFR-06 della demo: "confidence da 2 a 3" con valore
  validato 2). Ora si riscrivono sui valori validati; il valore di un KRI
  rettificato riceve data e fonte; un valore scritto senza "Rettificato" ferma
  la validazione invece di essere ignorato.
- **`Righe_liste_<ciclo>.json`** conteneva i valori prima della validazione e
  non veniva aggiornato: ora `valida` lo riscrive; le liste si caricano dopo.
- **Testo in cella**: "=..." diventava formula (verificato con HYPERLINK),
  "5/6" una data, "0012" il numero 12. Ogni testo passa da `per_cella`.
- **Excel che non parte**: la catena falliva a caso 2 volte su 3 con
  "Esecuzione del server non riuscita"; `excel_com.py` ora riprova.
- **Primo uso e dismissione**: comandi nuovi `inizializza` (registro vuoto dal
  template, senza toccarlo a mano) e `dismetti` (anagrafica ricompattata, KRI
  fuori vigore, azioni "Annullata", atto archiviato). Svuotare a mano una riga
  dell'anagrafica toglieva dal radar l'ultimo rischio e lasciava i KRI in
  vigore per sempre. Il test del primo uso ha trovato un difetto grave:
  scrivendo in una tabella vuota i nomi definiti scivolavano (copertura 12/0);
  risolto con la riga segnaposto (trappola 16 del PROMPT_MASTER).
- Minori: JSON con BOM accettato; file non JSON = fermo, non errore tecnico;
  notizie duplicate nello stesso output e flag su rischi ignoti fermati;
  capacita' delle viste controllate e avviso a 2 posti liberi in anagrafica;
  `confronta.py` ora confronta anche la Probabilita (72 punteggi su 12 rischi);
  Delta con la Probabilita; cerchi del Radar_Mosca a 1, 2, 3 anni (il 4 era
  irraggiungibile); ID delle azioni corretti anche per azioni identiche;
  Periodo delle notizie coerente fra esempi e scrittura; documenti allineati.
- Limite residuo (visto nel collaudo): se un programma diverso da Excel tiene
  aperto il registro (nel test, openpyxl in sola lettura non chiuso), il
  salvataggio di Excel resta in attesa invece di fallire. Un utente con il
  file aperto in Excel e' invece rilevato e fermato. In esercizio: nessun altro
  programma deve tenere aperto il registro durante un comando; se un comando
  non termina dopo 10 minuti, chiudere Excel dal Task Manager (il registro non
  e' stato salvato: resta il backup).
- **Piano di deploy** della soluzione attuale: `NFR_Emerging_Risk_Agents/08_Deploy/Piano_deploy.md`
  (fasi 0-9, cancelli G0-G4). La mail riassuntiva `Mail_piano_deploy.md` e'
  stata tolta dall'utente il 24/09: se serve di nuovo, rigenerarla dal piano
  aggiornato.

## 2-quinquies. 24/09: prima installazione reale e decisioni

Installazione in corso sul PC dell'utente (OneDrive Intesa Sanpaolo, variante
senza Studio). Problemi incontrati e risolti, tutti documentati nella guida
(tabella degli errori):
- `Workbook non trovato: None` = manca `configurazione.json` (c'era solo
  l'esempio). La guida ora distingue `None` da un percorso sbagliato.
- `No module named 'pythoncom'`: pywin32 installato a meta'. Basta
  `pip install --upgrade --force-reinstall pywin32` (con pywin32 312
  `pywin32_postinstall` non esiste piu'). La verifica della guida ora prova
  `win32com.client` + `pythoncom` + Excel, non solo `import win32com`.
- Raccolta notizie: 8 fonti su 18 ok, i 9 domini `europa.eu` in timeout, e
  BleepingComputer con errore di certificato (ispezione TLS del proxy). I siti
  si aprono tutti nel browser, quindi il problema era il proxy PAC che urllib
  non legge. **Nuova dipendenza `pypac`** in `raccogli_notizie.py` (scopre il
  PAC una volta e instrada come il browser); documentata in guida, README,
  00_LEGGIMI e Piano_deploy. Resta da ritestare sul PC della Banca.
  BleepingComputer: serve il certificato radice aziendale dall'IT.
- `settimanale` si e' fermato con `RPC_E_DISCONNECTED` (Excel via COM
  disconnesso durante la scrittura): da ritestare. Sospetti: registro "solo
  online" in OneDrive, EDR aziendale che chiude Excel invisibile.
- Settimana corretta per A3: il lunedi' della settimana in corso (2026-09-21),
  non il 2026-09-28 usato come esempio per `inizializza`.

Modifiche e decisioni del 24/09:
- A1, A3, A4 (non A5): frase fissa "Usa sempre lo strumento di ricerca file o
  gli strumenti di ricerca aziendale: non rispondere a memoria". A5 escluso per
  indipendenza.
- **Partenza da registro vuoto, senza trimestre gia' valutato a mano**
  (decisione dell'utente): A1 ha la regola del primo ciclo (tutta l'evidenza
  disponibile; rischi individuati da zero su tutti e sette gli event type).
  Il metro del collaudo in ambiente (Piano_deploy, fase 7) diventa il doppio
  run + la validazione umana. `confronta.py --primo-ciclo` abbina i rischi per
  event type e nome. A1 e' a 7.972/8.000 caratteri.
- Guida: il sito SharePoint e gli agenti rimandano al Piano_deploy (niente
  doppioni). 00_LEGGIMI ha una mappa di "quale documento per quale domanda".
- Architettura: `Analisi_Architettura/Archivio/07_Piano_semplificazione_senza_Python.md`
  (proposta, **non approvata**). Fatti chiave: in Agent Builder il code
  interpreter e' **acceso di default** e i suoi file sono download temporanei,
  non salvati in SharePoint. "Modifica con Copilot" modifica in place, ma
  decide il modello quali celle cambiare. Power Query **abilitato**
  sull'Excel aziendale (confermato dall'utente il 25/09: V0 superata). In Copilot Studio l'uso interattivo, compresi gli
  agent flow chiamati dall'agente, e' gratuito con licenza M365 Copilot; le
  esecuzioni pianificate consumano crediti.
- L'utente vuole in futuro che gli agenti scrivano direttamente: va progettato
  mantenendo i controlli deterministici come gate.

## 2-sexies. 25/09: report al comitato, D-19, anni di adeguamento, aggiornamento del registro

Dal confronto con un Horizon Scanning fatto a mano con Copilot
(`Analisi_Architettura/Archivio/08`) sono state approvate e applicate le proposte di
priorita' A:
- **D-19 in vigore**: score composito 0,30 Sev + 0,20 Prob + 0,20 Gap + 0,15 Vel
  + 0,15 Pross. Pesi in Parametri B4:B8; tolti dai titoli della rubrica (non
  servono agli agenti); Probabilita come colonna G della Dashboard.
- **D-32 report al comitato**: sei fogli di seguito nel workbook, da salvare in
  PDF dall'Excel validato. Sintesi (stato, primi cinque, agire ora, nuovi e
  variati, commento di A1, avviso se dopo ci sono state rettifiche, sintesi di
  A5, limiti di 06_Governance sez. 5), Classifica (barre ordinate colorate per
  urgenza + lente di Mosca X + Y contro Z), Radar_Mosca, Delta, Schede (una per
  rischio), Metodologia. La `sintesi` di A1 ora ha una struttura fissata nel
  prompt e finisce nella tabella nuova Sintesi_Cicli (prima non arrivava in
  nessun output).
- **D-33 anni di adeguamento**: colonna M dell'anagrafica, input del
  validatore; Y di Mosca = max(azioni, anni di adeguamento). Esempio: NFR-11
  (legacy) con 3 anni diventa AGIRE ORA.
- **D-34 versione del template e `aggiorna-registro`**: il workbook dichiara
  `versioneTemplate` = 2026-09-25, la mappa `versione_template`; lo script si
  ferma su un registro o una mappa di un'altra versione. `aggiorna-registro`
  porta il registro in uso sul template nuovo (copia per nome di colonna,
  verifica righe, errori, copertura e baseline; vecchio in Backup).
- Corretto un difetto: nel Radar_Mosca "Agire entro l'anno" era rosso come
  "AGIRE ORA" (confronto di Excel senza maiuscole).
- Prompt: cambiano **A1** (riga della `sintesi`, passi 2, 5, 10 accorciati:
  7.959 caratteri) e **A5** (rubrica senza pesi: 7.647). A3 e A4 identici al 24/09.
- Collaudo del 25/09, tutto verde: catena con Excel 161/161 (nuovo passo 11
  sul registro del template del 23/09, `99_Collaudo/dati/registro_template_2026-09-23.xlsx`;
  report al comitato confrontato con calcoli indipendenti), controlli 168/168,
  riferimenti 28/28 (nuovo controllo 9: versione in generatore, script, mappa,
  template), mappa 108/108, fonti 21/21.

**Sul PC della Banca, in quest'ordine** (guida, sezione 0-bis):
1. sostituire la cartella del pacchetto (tranne `configurazione.json`) e
   caricare in `Kernel` `rubrica_scoring.md`, `mappatura_campi.json`,
   `DECISIONI.md`;
2. chiudere il registro e lanciare `python esegui_ciclo_locale.py aggiorna-registro`;
3. `python esegui_ciclo_locale.py baseline` di prova;
4. ricaricare in Agent Builder le istruzioni di **A1 e A5** (A3 e A4 solo se non
   gia' fatto dopo il 24/09), code interpreter spento, prova di fumo 6.4.

## 2-septies. 25/09 pomeriggio: il workbook si spiega da se', P3, P6, P11

Richieste dell'utente: spiegazioni in testa ai fogli, significato dei dati,
operazioni e criteri della validazione, chi agisce su ogni parte, quando si
lancia A5; poi P6 e P11, e P3 come bordo invece che colore.

- **Guida in ogni foglio (D-38).**
  - Riga 2 di ogni foglio: processo che lo aggiorna, con un colore per
    processo (azzurro trimestrale, verde settimanale, giallo validatore,
    grigio calcolo), poi cosa contiene, come si legge, cosa fare.
  - Tabelle dati: intestazione in **riga 4** (dati dalla 5); in riga 3 il
    significato di ogni colonna, dalla nuova chiave `significato` della mappa.
    L'intestazione e' colorata per chi scrive la colonna.
  - Validazione: operazioni e **criteri** per rischio, KRI, azione e notizia.
  - Leggimi: tabella "chi aggiorna cosa", quando si lancia A5, dove si scrive
    a mano.
  - Metodologia: fonti ed evidenze, analisi per dimensioni, KRI.
  - Dashboard e Sintesi: intestazioni colorate per processo.
- **Trovato nella revisione critica**: gli stati "In corso" e "Completata"
  delle azioni non li scriveva nessuno, e il Leggimi vietava di toccare i dati.
  Ora sono l'unica modifica a mano ammessa nei dati (guida, workflow, Leggimi).
- **P3 (D-35)**: colonna N dell'anagrafica `Attenzione_Supervisore` (Sì/No,
  input del validatore, conservata dalla scrittura). Nel radar il cerchio ha il
  **bordo giallo spesso**; il riempimento non cambia. Serie per P x I
  raddoppiate.
- **P6 (D-36)**: regola 7 della rubrica (un numero senza fonte e' una
  valutazione dichiarata), controllata da A5 in C4. I descrittori di
  plausibilita' della Probabilita sono rimandati ad A-12. A1 7.951 caratteri,
  A5 7.734.
- **P11 (D-37)**: i sette rischi dell'esempio in `Piano_deploy.md` 7.5, come
  osservazione del collaudo in ambiente. Mai dati ad A1.
- **Versione della struttura 2026-09-25b**: `aggiorna-registro` vale sia per il
  registro del 24/09 sia per uno gia' aggiornato alla 2026-09-25.
- **Proposta grafica** del report: `Analisi_Architettura/Archivio/09_Proposta_grafica_report.md`,
  **da approvare** prima di applicarla.
- Power Query **abilitato** sull'Excel aziendale (conferma dell'utente): A-05 a
  meta', V0 del documento 07 superata. (28/09: A-05 chiusa da D-44, anche
  Copilot Studio e' disponibile.)
- Collaudo del 25/09 sera: catena con Excel 162/162 (nuove verifiche: bordo
  rosso esattamente per i rischi segnalati, guida e significato conservati da
  `inizializza`), controlli 168/168, mappa 110/110 (ogni colonna ha un
  significato), riferimenti 28/28, fonti 21/21. Guide e radar controllati a
  occhio sul PDF esportato.

**Sul PC della Banca**: come in 2-sexies (sostituire il pacchetto, caricare in
`Kernel` `rubrica_scoring.md`, `mappatura_campi.json`, `DECISIONI.md`,
`aggiorna-registro`, `baseline`, reincollare **A1 e A5**). Poi, facoltativo,
colonna N dell'anagrafica.

## 2-octies. 25/09 sera: registro e report in un solo file ridisegnato, agente A6

Richiesta dell'utente dopo la valutazione della v3 ("valutato, procedi con
implementare la v3 e l'agente delle schede"; tutte le risposte "Sì", nessuna
nota), poi "aggiorna tutte le analisi passate e la documentazione per
riflettere il nuovo layout/processo".

- **D-39, file unico** (`03_Excel/genera_dashboard.py` riscritto nelle viste):
  20 fogli in quattro gruppi con linguette colorate. Guida; report **Quadro**
  (cinque riquadri, primi cinque, matrice e radar piccoli, commento di A1
  diviso in messaggio e decisioni, avviso, **rischi segnalati e perche'**
  calcolati dal foglio), Classifica (lente ordinata per margine, titoli che
  dicono il messaggio), Radar_Mosca (settori con i nomi, cerchio a 1 anno
  tratteggiato, legenda nel grafico, riempimento semitrasparente), **Matrice**,
  Delta (ordinato, motivi a fianco, scala spiegata), Metodologia; lavoro
  **Registro** (un rischio per riga ordinato per score, Δ sul ciclo prima e a
  6 mesi, controlli di validazione e copertura; blocco nascosto `pos*` che
  sostituisce la Dashboard), Storico, **Indicatori** (ex KRI_Correnti e
  Andamento_KRI), Notizie (ex Analisi_News), **Piano_azioni**, Validazione
  (Stato a elenco), Parametri (etichetta del ciclo), **Dizionario**; dati in
  fondo, con gruppi di colonne in riga 3 e intestazione in riga 5. Fascia del
  titolo con ciclo, data, validato/da validare e riservatezza. Legenda delle
  abbreviazioni in fondo ai report. Tolti Dashboard, Sintesi, Schede,
  Approfondimento, KRI_Correnti, Andamento_KRI, Trend, Leggimi (rinominati o
  assorbiti).
- **Commento di A1** nella forma "MESSAGGIO: ... DECISIONI: ..." (A1 7.966
  caratteri): il Quadro lo divide; senza marcatore tutto nel messaggio.
- **D-40, agente A6 e schede**: `02_Agenti/modelli/A6.md` (4.759 caratteri,
  rubrica 1-2), `01_Kernel/schema_output_A6.json`, `07_Senza_Studio/schede.py`
  (input dai dati validati, controlli: stessi rischi, sei dimensioni, fonti
  identiche, nessun numero fuori dai dati; file `Schede_<ciclo>.xlsx` con
  indice e una scheda per rischio: descrizione, valori e perche', urgenza,
  cosa e' cambiato, **andamento negli ultimi trimestri** con grafico, fonti e a
  cosa servono, azioni, KRI). Comandi nuovi `schede-input` e `schede
  [--payload]`, entrambi in sola lettura del registro; `schede-input` si
  ferma se il ciclo non e' validato.
- **Script**: legge solo nomi definiti (copertura, validazione, segnali,
  presidio), adatta le altezze delle righe con testi calcolati
  (`adatta_altezze`), scrive il JSON delle variazioni con le chiavi in ordine
  fisso (`ordina_chiavi`), controlla la capienza del Piano_azioni. Versione
  **2026-09-25c** in generatore, script e mappa.
- **Collaudo**: `run_catena.py` legge nomi; nuove verifiche sui rischi
  segnalati del Quadro contro una selezione indipendente, sul commento diviso
  (con e senza marcatori: il payload di prova del 2026Q3 ha ora i marcatori,
  quello del 2026Q4 no), sui motivi del Delta; passo **2c** sulle schede con
  A6 (input, quattro output difettosi fermati, file con e senza A6).
  `test_controlli.py`: 16 verifiche nuove su A6 e schede.
  `verifica_riferimenti.py`: il controllo di copertura sta nei nomi.
- **Trovato facendo** (trappole 42-46 del PROMPT_MASTER): un intervallo senza
  foglio dentro un nome definito fa rifiutare il file a Excel (trovato per
  bisezione, un foglio alla volta); formati condizionali senza colore di
  sfondo = celle bianche (anche le etichette di urgenza, testo bianco su
  bianco); etichette #N/D e 0,00 sulle barre per esito; #N/D riletto con INDEX
  scambiato per errore dal controllo dello script. Dal PDF della demo: con le
  righe dei motivi adattate al testo il grafico del Delta copriva la nota sulla
  scala; ora lo script allunga la riga sotto i motivi (trappola 46) e il
  collaudo lo verifica.
- **Documentazione allineata**: 00_LEGGIMI, guida passo passo (0-bis, sezione
  2 punti 11-13, lettura dei risultati, errori), README della variante locale
  (A6 in Agent Builder, openpyxl), Piano_deploy (cinque agenti, 8.4-8.5),
  workflow (passi 11-12), governance (controlli e rischi di A6 e dei
  segnalati), manuale di costruzione a mano (riscritto sulle formule nuove),
  TODO, COMMENTATI (sezione A6), schema documentato (A6 e input delle schede),
  LEGGIMI del collaudo, DECISIONI (D-39, D-40, A-14 chiusa), PROMPT_MASTER
  (sezione del workbook riscritta, A6, trappole 42-46). **Analisi**: in testa
  ai documenti 01-07 la corrispondenza fra i fogli di allora e quelli di oggi;
  08 e 09 aggiornati (09 con le differenze fra anteprima e realizzazione);
  indice delle analisi. **Demo** adeguata (grafici del nuovo layout, schede
  senza A6, PDF del report) e rilanciata.
- Collaudo del 25/09 sera: catena con Excel 182/182 (30-35 minuti), controlli 183/183, riferimenti 28/28, mappa 110/110, fonti 21/21; prompt A1 7.966, A5 7.734, A3 6.991, A4 4.873, A6 4.759 caratteri. Report controllato a occhio sul PDF del template e della demo (Quadro in due pagine, Classifica e Matrice in una, Delta in due)..

Consegna (su richiesta dell'utente): `NFR_Emerging_Risk_Agents_2026-09-25c.zip`, completo
(76 file, circa 630 KB: **solo sorgenti**; prompt composti, template Excel, output della demo e
anteprime si rigenerano: `componi_prompt.py`, `genera_dashboard.py`, `esegui_demo.py`), con
`LEGGIMI_installazione_2026-09-25c.md`: aggiornamento di un'installazione esistente,
reinstallazione completa da zero, dove sono le istruzioni complete, file cambiati.

**Sul PC della Banca**: sostituire il pacchetto (03_Excel, 07_Senza_Studio
tranne `configurazione.json`, 01_Kernel, 02_Agenti); caricare in `Kernel`
`mappatura_campi.json`, `rubrica_scoring.md` e `DECISIONI.md`; `pip install
openpyxl` se manca; chiudere il registro e lanciare `aggiorna-registro`
(risposta attesa: "Registro aggiornato alla versione 2026-09-25c", baseline
identica); `baseline` di prova. In Agent Builder: **reincollare A1**, **creare
A6** (istruzioni `A6_Schede.md`, nessuna knowledge, capability spente, Think
deeper). Al prossimo ciclo validato: `schede-input`, A6, `schede`, e PDF dei
fogli da Quadro a Metodologia.

## 2-nonies. 26/09: analisi dei processi, tracciata come TODO

L'utente ha descritto il processo che si aspetta (trimestrale fondante su
rapporti approfonditi; settimanale o mensile sulle notizie con notch, trend,
evento critico e variazioni sul radar; spot su una notizia con impatto per
dimensione). Il confronto con il pacchetto e le proposte sono in
`NFR_Emerging_Risk_Agents/TODO_possibili_sviluppi.md`: **AR1** (decidere e
avviare il piano 07 senza Python), **P1-P7** (gap dei processi, con tabella
"c'e' / in parte / manca") e **Q1** (quantificazione di probabilita' e impatto
per i rischi piu' rilevanti). Nessuna modifica a codice, prompt o template.
**AR1 condiziona l'ordine**: se il piano 07 si approva, le voci P e Q si fanno
dopo la migrazione o direttamente nella nuova architettura. (28/09: AR1 chiusa
da D-43; il nuovo ordine e' nel TODO, sezione 2-decies qui sotto.)

Decisioni dell'utente sull'analisi (stesso giorno): **D-41** restano "mai una
cifra nuova" e "solo il trimestre modifica uno score", con l'unica eccezione
del **ciclo straordinario su segnale critico** (es. l'annuncio di Mythos):
P1 ridotta a segnali qualitativi senza posizioni ipotetiche, P3 prima in
ordine. **D-42** un evento che tocca piu' rischi = righe separate e
**collegate** (P5 riscritta: campo `collegati` reciproco, niente categorie
secondarie). Entrambe da implementare; ordine consigliato P3, P1, P4, P5, P2,
P7, P6.

## 2-decies. 27-28/09: piano di automazione, opzione Copilot Studio, TODO unificato

Nessuna modifica a codice, prompt o template: analisi, decisioni e piano di
lavoro.

- **27/09**: `Analisi_Architettura/Archivio/10_Piano_automazione_processo.md`, la
  rianalisi orientata all'automazione. Scelte dell'utente: Python resta il
  motore, con sopra uno strato di automazione per l'analista (procedura guidata
  a menu, risposte degli agenti prese dagli appunti, lanciatori `.cmd`); il
  piano 07 passa in riserva. Rischio nuovo trovato: il Salvataggio automatico
  di OneDrive sul registro aperto via COM (fermo pulito non garantito).
- **28/09, parte seconda del documento 10**: l'opzione separata Copilot
  Studio.
  - Si automatizza molto di piu'.
  - Python si toglie dall'esercizio solo riscrivendo il motore, perche' il
    code interpreter di Copilot Studio genera il codice con il modello.
  - Variante descritta: **CS-1 ibrida**. Operatore in Teams; gli agenti
    consegnano solo in `In_arrivo`; il motore Python gira invariato in
    background su un PC esecutore; le richieste passano da una lista bianca.
  - Circa due terzi del piano 10 sono comuni alle due strade.
- **28/09, decisioni**:
  - **D-43**: Python motore, piano 07 in riserva, AR1 chiusa;
  - **D-44**: Copilot Studio e Power Query disponibili, chiude A-05;
  - **A-15** aperta: strada A o CS-1. Copilot Studio e' piu' complesso e
    l'utente non ha deciso; la proposta, senza decisione, e' la strada A.
- **28/09, TODO unificato** (`NFR_Emerging_Risk_Agents/TODO_possibili_sviluppi.md`):
  il piano unico del lavoro da fare. In testa l'ordine di lavoro:
  1. AU1-AU3, la parte comune, 6-7 giorni;
  2. in parallelo, facoltativi, la prova K0 in Copilot Studio e G1/G3/G2;
  3. AU4, cioe' la decisione A-15;
  4. AU5 (strada A, 3-4 giorni) oppure AU6 (CS-1, 13-15 giorni);
  5. P3, P1, P4, P5, P2, P7, P6 (dal 02/10 P8, lista di osservazione, dopo P4);
  6. Q1.

  Piano 07 e variante CS-2 sono nella sezione "in riserva".

## 2-undecies. 29-30/09: primo ciclo reale di prova e semplificazione dello scoring

- **29/09, primo ciclo di prova sul PC della Banca** (2026Q4): sette-otto giri
  A1 <-> A5 prima di convergere. Correzioni del giorno: D-45 (settima library
  `Analisi_Esterne`, il tipo di una fonte segue la cartella), D-46 (confidence
  4-5 senza fonte interna), D-47 (pavimento di Gap_Controlli), D-48
  (Prossimita 4-5 solo con un caso nominato); `PAROLE_FUNZIONE` ampliato;
  sezione 0 della guida riscritta come percorso unico; messaggio rinforzato per
  A1.
- **30/09, semplificazione** (`Analisi_Architettura/Archivio/11`, decisioni
  D-49..D-56, TODO S1): A1 valuta solo cio' che le fonti sostengono.
  - Gap_Controlli esce dal modello: resta il **presidio dei controlli**,
    giudizio della Banca nell'anagrafica (colonna O), fuori dallo score (D-49).
  - Velocity **facoltativa**; score = media pesata delle dimensioni valutate,
    pesi Severity 0,35, Probabilita 0,25, Prossimita 0,20, Velocity 0,20 (D-50).
  - Esito e "da/a" calcolati dallo script; la sola confidence non fa Variato
    (D-51).
  - Probabilita di plausibilita', Confidence su fonti indipendenti (D-52).
  - KRI da 1 a 3, soglie della Banca ("Soglie da definire"), rilettura solo
    dei valori trovati (D-53).
  - Azioni senza dimensione; C8 solo Osservazione; `valida` rifiuta un owner
    persona (D-54).
  - Un rischio per meccanismo di perdita, nessun event type obbligatorio,
    capienza 20 rischi (D-55).
  - `trimestrale --procedi-con-rilievi --motivo --decisore`: si superano solo i
    Bloccanti di A5; i rilievi restano sui rischi (colonna Rilievi), nel Quadro
    e in validazione (D-56).
  - Struttura del workbook **2026-09-30**; A1 a 7.496 caratteri (era 7.977).
  - Anteprima del template in `Anteprima_S1/` (fuori dal pacchetto), con i PDF
    dei fogli; il template del pacchetto e' gia' rigenerato.
  - Collaudo: dati di prova convertiti, baseline attese rigenerate, passi
    nuovi 11b (migrazione dal 2026-09-25c) e 12 (`--procedi-con-rilievi`).
  - PROMPT_MASTER con le trappole 51-58.
  - Collaudo completo del 30/09, tutto verde: catena con Excel 214/214 (circa
    40 minuti), controlli 204/204, mappa 112/112, riferimenti 28/28, fonti 21/21.
- **30/09, analisi di una proposta esterna di supporto NFR** (documento
  riservato, fuori dal pacchetto): coerente con il pacchetto; tre suggerimenti
  sui parametri (tipo di KRI, livello di allerta calcolato, esposizione nei
  descrittori della Probabilita) annotati nel TODO, sotto S1, da decidere.

## 2-duodecies. 30/09 sera: revisione della rubrica del responsabile (D-57..D-62)

Il responsabile ha riscritto i descrittori della rubrica; le scelte fatte con
lui:
- **Severity si chiama Impatto** ovunque, anche nei dati (campo `impatto`,
  colonna Impatto, `pesoImpatto`); il registro vecchio si migra con
  `colonne_rinominate` della mappa (D-57).
- **Niente Confidence**: ogni fonte ha una **rilevanza 1-3** per la
  previsione; Probabilita 5 o Prossimita 4-5 vogliono almeno una fonte di
  rilevanza 3, salvo deroga dichiarata; C5 diventa "Fonti" (D-58).
- **Z di Mosca = meta' della fascia** della Prossimita (5 → 0, 4 → 0,5,
  3 → 1,5, 2 → 2,5, 1 → 3,5), scritta accanto ai descrittori (D-59). Provato
  prima l'inizio della fascia: la Prossimita 4 valeva 0 e troppi rischi
  finivano in AGIRE ORA, un'urgenza che non informa; da tarare con A-12.
- **Anni di adeguamento stimati da A1** (`anni_adeguamento`, null se non
  serve), decisi in validazione e scritti da `valida` nell'anagrafica, che
  resta la fonte del Radar_Mosca (D-60).
- **Descrittori riscritti** (Impatto, Probabilita, Prossimita con la deroga per
  fenomeni ad altissimo impatto, Velocity), soglia di direzione 2, soglia del
  Delta 0,30 dalla tabella del responsabile (D-61).
- **Comando `report`** (`--file`, `--con-lavoro`): rigenera il PDF del report
  dopo correzioni manuali dei validatori, conservando la versione precedente;
  **Registro e Parametri** in A4 orizzontale, tutte le colonne in una pagina
  (D-62).
- Struttura del workbook **2026-09-30b**; A1 7.885 e A5 7.895 caratteri (margine
  stretto: sezione 4 della rubrica tolta da A5, testi accorciati).
- Anteprima: `Anteprima_S1/NFR_Dashboard_Template_S1b.xlsx` con i PDF dei
  fogli; il template del pacchetto e' rigenerato.
- Collaudo completo del 30/09 sera, tutto verde (anche dopo la Z a meta'
  fascia): catena con Excel 217/217, controlli 213/213, mappa 112/112,
  riferimenti 28/28, fonti 21/21.
- Demo rilanciata (`Demo_W1_W2/REPORT_demo.md`): 2 rischi AGIRE ORA su 13, 6
  entro l'anno, 5 con margine; report con il comando `report`, poi una
  correzione manuale del presidio e il PDF rigenerato con Registro e
  Parametri (13 pagine).
- PROMPT_MASTER con le trappole 59-62 (parametri conservati che coprono i
  nuovi, colonna rinominata, campo validato che non e' una dimensione,
  messaggio d'errore dopo la sostituzione del file, corretto).

Sul PC della Banca: reincollare A1, A3 (la sezione 6 della rubrica e' cambiata),
A4, A5, A6; `aggiorna-registro` prima su una copia, poi sul registro in uso
(pesi, soglie e Z diventano quelli del template; lo script stampa i vecchi);
`baseline` e ricarica in `Kernel`.

## 2-terdecies. 01/10: livello di allerta, KRI per tipo, esposizione (D-63..D-65)

Dai tre suggerimenti di una proposta esterna di supporto NFR (documento
riservato, fuori dal pacchetto), scelti dal responsabile:
- **Z di Mosca a meta' fascia** (D-59 rivista il 30/09 sera: l'inizio della
  fascia metteva troppi rischi in AGIRE ORA, "non danno nessuna
  informazione").
- **Livello di allerta** (D-63): Attivazione con due segnali forti (AGIRE ORA,
  KRI in rosso, notizie oltre la soglia), Attenzione con uno o con margine
  sotto l'anno e un aggravante (P x I da 12, presidio assente, meta' dei KRI in
  ambra o rosso), Monitoraggio altrimenti. **Nessuna colonna nuova** (richiesta
  del responsabile: "tenere il modello semplice"): lo calcola il Radar_Mosca
  (U-AB) e si vede come **colore dei cerchi del radar**, fondo dell'ID nel
  Registro, riquadro del Quadro e colonna dei rischi segnalati; il tema del
  supervisore passa dal bordo giallo al ◆. Soglie in Parametri B60:B63.
  Esempio del template: 1 Attivazione, 6 Attenzione, 5 Monitoraggio.
- **Due KRI per rischio**, Esposizione ed Evoluzione, con il `tipo` assegnato
  da A1 (D-64); A1 deve **ragionare analizzando nel dettaglio ogni fonte**
  (regola generale, nel ruolo). Colonna Tipo nel foglio KRI e negli
  Indicatori; C9 blocca un rischio senza la coppia.
- **Probabilita 4-5 solo se la Banca e' esposta** (D-65, opzione b).
- Struttura **2026-09-30c**; A1 7.917 e A5 7.895 caratteri (recuperati
  accorciando esempi ridondanti della rubrica). Trappole 63-66 nel
  PROMPT_MASTER.
- `prepara_report` adatta la scala del Quadro (fino al 60%) perche' resti in
  due pagine con molti rischi segnalati; il collaudo lo verifica.
- Collaudo completo del 01/10, tutto verde: catena con Excel 230/230,
  controlli 184/184, mappa 113/113, riferimenti 28/28, fonti 21/21. Demo
  rilanciata: 2 Attivazione (NFR-01, NFR-11), 5 Attenzione, 6 Monitoraggio;
  26 KRI in vigore, due per rischio con il tipo; report di 12 pagine.
- Da decidere con la funzione di rischio: le conseguenze dei tre livelli e la
  taratura delle soglie (A-12) dopo il ciclo 2026Q4 reale.
- Sul PC della Banca: reincollare A1, A3, A4, A5, A6; `aggiorna-registro` prima
  su una copia (i KRI esistenti restano senza tipo finche' A1 non li ripropone:
  al primo ciclo ne ripropone due per rischio, il terzo esce di vigore);
  `baseline` e ricarica in `Kernel`.

## 2-quaterdecies. 01/10 pomeriggio: installazione sul PC della Banca e sintesi settimanale

Durante l'installazione dell'aggiornamento sul PC della Banca sono emersi errori
della guida e del pacchetto, tutti corretti:
- lo zip con i soli file cambiati non bastava: sul PC mancavano i file mai
  cambiati (`fonti.py`, `excel_com.py`...). Si consegna il **pacchetto completo**,
  senza cartella in testa (`NFR_pacchetto_completo_2026-10-01.zip`);
- la guida (0-bis) non avvertiva che l'aggiornamento sovrascrive il kernel
  modificato dalla Banca (la tassonomia della Banca e' andata persa: riparte da
  quella del pacchetto), elencava solo quattro file da caricare in `Kernel` e
  quattro agenti da ricaricare, e mandava a lanciare `componi_prompt.py`
  (programma del manutentore). Trappola 67;
- lo script legge il kernel dalla cartella `kernel` di `configurazione.json`
  (library Kernel sincronizzata), non da `01_Kernel`: un file mancante ora
  ferma con "FERMATO" e il rimedio, non con "ERRORE TECNICO";
- la library `Report_Settimanali` non e' usata nella variante locale (lo dice
  ora la documentazione); il PDF del report e' in `Archivio_Cicli`, non in
  `Report_Trimestrali`;
- le capability di Agent Builder non sono abilitate nel tenant: coerente con
  D-11.
- primo ciclo 2026Q4 scritto in Banca (10 rischi, 20 KRI); in validazione la
  colonna Stato del foglio Validazione e' stata svuotata a mano: `valida` ora lo
  dice con il rimedio (trappola 69); diagnosi fatta confrontando il registro
  con la copia del ciclo in `Archivio_Cicli` (script `diagnosi_registro.py`,
  dato all'utente, fuori dal pacchetto).
- **01/10 sera: primo giro completo in Banca** sul ciclo 2026Q4 (struttura
  2026-09-30c): trimestrale, validazione (169 accettati, 1 rettificato),
  report, schede con A6. Restano: validare la settimana del 28/09 se non
  fatto, installare il pacchetto 2026-10-01 con `aggiorna-registro`, reincollare
  A4 (prompt corretto: baseline in knowledge come .txt).

**D-66**: sintesi di A3 e flag proposti di ogni settimana nel foglio dati
Sintesi_Settimane e nel foglio Notizie (struttura **2026-10-01**). Verificato
con il passo 3b del collaudo che le notizie validate entrino nelle viste
(respinta = esce da segnali netti, Notizie e livello di allerta; rettificata =
conta con il valore del validatore). Trappola 68. Collaudo completo verde: catena con
Excel 255/255, mappa 120/120, controlli 184/184, riferimenti 28/28, fonti
21/21; demo rilanciata.

## 2-quindecies. 01-02/10: validazione in una griglia, una riga per oggetto (D-67)

Richiesta dell'utente (01/10 pomeriggio): nel foglio di validazione due
colonne con il margine di Mosca colorato e lo score composito; domanda su dove
finisce la validazione e se non convenga validare direttamente nel Registro.
Risposta: il risultato vive gia' nel registro (RiskRegister, KRI, Azioni,
NewsLog con Validazione, Approvato_Da, Data_Validazione), ma validare li'
farebbe perdere la proposta e il "da cosa a cosa". Anteprima
`Anteprima_S1/Validazione_per_riga.xlsx` (fuori dal pacchetto), poi "prosegui
con la modifica ai fogli di validazione, non serve l'anteprima; prima un piano
dettagliato, poi esegui".

- **Foglio Validazione = griglia di lavoro** in quattro sezioni (Rischi 20,
  KRI 80, Azioni 100, Notizie 200 righe; le libere nascoste): una riga per
  oggetto dei periodi non ancora validati, proposta in grigio e **cella gialla
  gia' compilata con la proposta**. Non toccata = Accettato, cambiata =
  Rettificato (Motivazione obbligatoria), Respingi = Sì (KRI, azioni,
  notizie). Rischi con un bloccante di A5 superato: ⚑ e Motivazione
  obbligatoria. Per i rischi **Score composito e Margine di Mosca** con le
  formule del Registro e del Radar_Mosca sui valori gialli e sulle azioni non
  respinte, "(era …)" se cambiano. Formule dentro IFERROR.
- **Storico campo per campo** (`tblValidazione`, invariata) nel foglio dati
  nuovo **Storico_Validazioni**, scritto solo dallo script.
- Script: `valida` legge la griglia (stesse regole, messaggi con la riga del
  foglio, riepilogo per righe); comando nuovo **`griglia`** (ricostruisce il
  foglio conservando cio' che e' scritto); trimestrale, settimanale e valida
  riscrivono la griglia; **`aggiorna-registro` non si ferma piu' sulle righe
  da validare**: le porta nella griglia con le decisioni gia' scritte, anche
  dal vecchio foglio; `--accetta-il-resto` resta accettata ma non fa niente.
- Registro D4 e Quadro contano gli **oggetti** da validare, non i campi.
- Struttura **2026-10-02**. **Prompt degli agenti invariati**: niente da
  reincollare.
- Collaudo: validatore simulato (`comune.scrivi_decisioni`) che scrive nella
  griglia; passi 2b, 3, 3b, 11b, 12 adattati, con verifiche nuove (Score e
  Margine della griglia = registro dopo `valida`, riga cancellata riparata da
  `griglia`, settimanale con un valore sbagliato nella griglia, migrazione delle
  righe in sospeso). **Collaudo completo del 02/10 tutto verde**: catena con
  Excel 273/273 (circa 47 minuti), mappa 126/126, controlli 184/184,
  riferimenti 28/28, fonti 21/21.
- Documentazione allineata: guida (sezioni 0-bis, 3, tabella degli errori),
  00_LEGGIMI, README della variante locale, workflow, governance (controllo
  "Griglia di validazione", **validazione di facciata riscritta**: una riga non
  toccata vale come accettata, quindi accettare tutto non lascia una traccia
  diversa), Piano_deploy, struttura_e_liste, manuale del template (sezione
  della griglia), LEGGIMI del collaudo, TODO (AU5), DECISIONI (D-67, nota su
  D-06), PROMPT_MASTER (trappole 70-74), analisi 01, 06, 07, 10, 11 e indice.
  Demo rilanciata, con il PDF della griglia compilata del 2026Q3.

Sul PC della Banca: installare il pacchetto completo e lanciare
`aggiorna-registro` prima su una copia (le righe ancora da validare, per
esempio la settimana del 28/09, passano nella griglia); poi validare nella
griglia. Nessun agente da reincollare per questa modifica (resta A4 dal
01/10, se non fatto).

## 2-sexdecies. 02/10 pomeriggio: schede dei rischi con il perche' di ogni numero (D-68)

Richiesta dell'utente sulle schede: nelle righe di Impatto, Probabilita,
Prossimita e Velocity il razionale di ogni numero, con le informazioni e i
documenti da cui viene; il "Razionale" come spiegazione del fenomeno in
termini di rischio, senza i motivi dei numeri; azioni e KRI in vigore con il
razionale e l'effetto atteso.

- **Chi scrive cosa**: il perche' di un numero lo puo' dare solo A1, che legge
  i documenti; A6 riformula. A1 scrive quindi il razionale **in parti con
  etichette fisse** (`RISCHIO:`, `IMPATTO:`, `PROBABILITA:`, `PROSSIMITA:`,
  `VELOCITY:`, `ADEGUAMENTO:`), come gia' la sintesi con MESSAGGIO/DECISIONI;
  il razionale di azioni e KRI (che A1 scriveva gia' e il registro conservava,
  ma la scheda non mostrava) finisce con `EFFETTO:`. Il formato sta nello
  scheletro del prompt; lo schema non lo impone (un fermo per la forma
  costerebbe un giro di A1): `trimestrale` stampa un avviso se un razionale non
  e' diviso.
- **Scheda**: Il rischio → Razionale (il fenomeno; solo senza A6, perche' la
  descrizione estesa di A6 e' gia' il fenomeno) → tabella dei valori con
  "Perche' questo valore: informazioni e documenti" (spiegazione di A6 o
  motivazione di A1) → urgenza con il motivo degli anni di adeguamento → cosa e'
  cambiato → andamento → fonti → azioni e KRI in vigore, ciascuno con una riga
  "Perche'" / "Effetto atteso". Un razionale scritto prima resta intero nel
  "Razionale (registro)".
- **A6**: riceve dallo script le parti gia' divise (`razionale_rischio`,
  `motivazioni`, razionale ed effetto di azioni e KRI); la descrizione estesa e'
  il fenomeno senza i motivi dei punteggi; le spiegazioni partono dalle
  motivazioni di A1 e non attribuiscono a un documento cio' che A1 non gli
  attribuisce. Non scrive i testi di azioni e KRI (output piu' corto).
- Prompt: **A1 7.971** caratteri (formato pagato togliendo ripetizioni: "SOLO
  JSON" nel ruolo, codici di ricerca nel passo 10, rimando della regola 6,
  formato del ciclo, "id_rischio" nella sintesi), **A5 7.857** (regola 6 piu'
  corta), **A6 5.638**; A3 e A4 invariati. Schema A1: razionale fino a 2.500
  caratteri, quelli di azioni e KRI fino a 700; A6: spiegazioni fino a 600.
  **Struttura del workbook invariata** (cambiano solo i significati delle
  colonne Razionale nella mappa): nessun `aggiorna-registro`.
- Collaudo: dati di prova del 2026Q4 (`run3`) nel formato nuovo, quelli del
  2026Q3 nel vecchio (provano entrambe le letture); 10 verifiche nuove in
  `test_controlli.py` (194/194), una nel passo 2c della catena; catena con
  Excel 274/274.
- Documentazione: DECISIONI (D-68), guida (0-bis: reincollare A1, A5, A6;
  "Che cosa c'e' in una scheda", poi spostato nella sezione 4, riga Schede), 00_LEGGIMI, workflow, governance (scheda che
  inventa), schema documentato, COMMENTATI (A1 e A6), LEGGIMI del collaudo,
  PROMPT_MASTER (trappole 75-77), analisi 09 e indice; demo rilanciata.

Sul PC della Banca: installare il pacchetto completo; **reincollare A1, A5 e
A6** in Agent Builder; nessun `aggiorna-registro` per questa modifica (resta
quello della 2026-10-02, sezione 2-quindecies). Le schede dei cicli gia'
scritti mostrano il razionale intero, come prima.

## 2-septdecies. 02/10 sera: meno giri fra A1 e A5, testi di A1 piu' ragionati (D-69)

Domanda dell'utente: il giro A1 → A5 → A1 e' scomodo; A1 puo' tenere conto dei
controlli di A5 gia' nel primo output, magari ricevendone la definizione in un
file? E le descrizioni e le motivazioni di A1 sono carenti: si possono rendere
piu' ragionate? Proposta accettata ("procedi").

- **Controlli di A5 ad A1, con le stesse parole**: il testo dei nove controlli
  passa in `01_Kernel/controlli_A5.md`; `componi_prompt.py` lo mette nel prompt
  di A5 (`{{CONTROLLI}}`: prompt composto identico, salvo C8) e
  `07_Senza_Studio/input_a1.py` nell'**allegato di A1** `Input_A1_<ciclo>.txt`,
  che lo script scrive accanto alla baseline ogni volta che la aggiorna:
  baseline (JSON), controlli, **guida di scrittura** (`01_Kernel/guida_scrittura_A1.md`).
  Testo e non JSON: per il modello e' lo stesso, e la knowledge di Agent Builder
  i .json non li legge. A1 lo allega al posto della baseline (un solo gesto) e
  al passo 10 verifica ogni rischio con controlli e guida prima di rispondere.
- **Precontrollo dello script prima di A5**: comando `precontrollo --payload
  A1.json`, senza Excel e senza registro: schema, controlli meccanizzati (gli
  stessi di `trimestrale`), parti del razionale (D-68); scrive
  `Cicli/<ciclo>/Correzione_A1_<ciclo>.txt`, il messaggio da incollare nella
  chat di A1. E' la parte affidabile: un modello che rilegge il proprio output
  tende a confermarlo. A5 resta indipendente; `--procedi-con-rilievi` resta per
  i rilievi di giudizio.
- **Testi piu' ragionati**: la guida dice com'e' fatta una buona descrizione
  (meccanismo causa-evento-danno, dove tocca la Banca, perche' emergente), un
  razionale (per ogni valore descrittore, fatto con documento e data, perche'
  non il valore vicino), un'azione (risultato verificabile, anello interrotto,
  effetto osservabile) e un KRI; con un esempio completo di forma, fatti
  dichiarati inventati. L'esempio e' stato riletto contro i descrittori (la
  prima stesura aveva una Probabilita 4 che per la rubrica era 5: trappola 79).
- **Azioni nuove**: nei dati di prova A1 riproponeva ogni trimestre le azioni
  aperte (NFR-11 aveva tre volte la stessa azione nella scheda). Passo 7 "azioni
  nuove", guida "passo successivo", C8 (prompt e script) segnala come
  Osservazione la stessa descrizione di un'azione aperta dello stesso rischio.
  Dati di prova aggiornati: run1/run2 (7 azioni) e run3 (9) propongono il passo
  successivo; `baseline_2026Q4.json` con le descrizioni nuove (6 azioni aperte).
- Prompt: **A1 7.963** (allegato e passo 10 pagati togliendo "mai una persona",
  "mai il kri_id di un altro rischio" e "punteggi interi", gia' in C8, C9 e
  rubrica), **A5 7.902** (C8), A3, A4, A6 invariati.
- Collaudo: `test_controlli.py` 211/211 (17 verifiche nuove, `test_precontrollo`),
  `verifica_riferimenti.py` 30/30 (controlli dal kernel, modello di A5 senza
  copia), catena con Excel 277/277 (passo 1-bis precontrollo, allegato
  dopo il 2026Q3); mappa 126/126, fonti 21/21.
- Documentazione: DECISIONI (D-69), guida (glossario, comandi, 0-bis, passi
  2, 4, 5-bis, 8, "Che cosa fa il precontrollo", messaggio rinforzato),
  00_LEGGIMI (indice, sistema in una pagina, dove vive ogni regola), README
  della variante, workflow (W1 2-3-bis), governance (testo unico dei controlli,
  C8), Piano_deploy (7.3, 7.6, 8.2), SharePoint (Kernel, Archivio_Cicli), schema
  documentato, COMMENTATI (A1 input e passi 7, 8, 10; A5 controlli e C8), TODO
  (AU2: `messaggio_correzione` per A1 gia' fatto), LEGGIMI del collaudo,
  PROMPT_MASTER (trappole 78-80), analisi 10; demo rilanciata con il precontrollo.

Sul PC della Banca: installare il pacchetto completo e copiare **tutti i file
di `01_Kernel`** nella library Kernel (due file nuovi: senza, l'allegato ha solo
la baseline e lo script lo dice); **reincollare A1 e A5** (con D-68: A1, A5 e
A6); nessun `aggiorna-registro` per questa modifica. Da allora ad A1 si allega
`Input_A1_<ciclo>.txt` e, prima di A5, si lancia `precontrollo`.

## 2-octodecies. 05/10: prove sul PC della Banca e Copilot Studio in due opzioni del codice (D-70)

Richiesta dell'utente: i prossimi passi sono il test della versione senza Copilot Studio e
l'attivazione di quella con Copilot Studio, per vedere se funziona e con quali limiti ("mi hanno
detto che e' meglio attivare l'opzione code"); servono i pacchetti completi con istruzioni precise
per installarli e provarli. A meta' lavoro: "fai le 2 opzioni con le skill.md e vediamo". L'utente
stava anche verificando se il pacchetto del 02/10 e' gia' installato in Banca.

- **Verifiche su Microsoft Learn (05/10)**: Copilot Studio ha due motori.
  - **Esperienza standard**: il Code interpreter va abilitato dall'amministratore, poi acceso
    sull'agente; il codice lo scrive il modello; "No charge" per gli utenti Microsoft 365 Copilot.
  - **Nuova esperienza** (GitHub Copilot harness): sandbox Python e **skill** (SKILL.md e script in
    uno zip) che eseguono un nostro script sempre uguale; Copilot Credits dalla costruzione.

  Questo supera in parte la conclusione del 28/09 (piano 10, 10.10): sezione 10.20 nuova.
- **Codice**:
  - `07_Senza_Studio/precontrollo.py`: le regole del precontrollo tolte da `esegui_ciclo_locale.py`
    (stesso comportamento), piu' `conta`, `ciclo_di`, `riga_esito` e `impronta` (12 caratteri dello
    SHA-256 del JSON canonico); il comando la stampa;
  - `input_a1.leggi_baseline`;
  - `09_Copilot_Studio/prepara_kit.py` (manutentore) compone lo script unico
    `precontrollo_nfr.py`: i moduli del pacchetto copiati senza modifiche ed eseguiti in memoria,
    piu' lo schema di A1. Lo script e' nella skill `precontrollo-nfr/` (SKILL.md scritto a mano), nei
    due zip di `Da_caricare/` (cartella alla radice o SKILL.md alla radice) e come `.txt` da
    allegare. Output deterministico: stessi sorgenti, stessi byte.
- **Prove scritte per l'utente**:
  - `08_Deploy/Prova_senza_Copilot_Studio.md`: parte 1, installazione sul registro vero, con il
    controllo di cosa c'e' gia' (frasi da cercare nelle istruzioni degli agenti); parte 2, ciclo
    2026Q4 completo su un registro di prova nuovo in `C:\NFR_Prova`.
    **Trappola**: un ciclo 2027Q1 di prova oggi e' impossibile, perche' C3 vuole evidenze dopo il
    31/12/2026.
  - `09_Copilot_Studio/Prova_con_Copilot_Studio.md`:
    - B0, le domande all'IT: code interpreter, nuova esperienza, crediti, modelli, trascrizioni;
    - B1 e B2, costruzione e test T1.1-T1.4 e T2.0-T2.3;
    - B3, Teams e agent flow, facoltativi;
    - tabella dei risultati e come leggerli.

    I messaggi sono in `Da_caricare/Messaggi_da_incollare.txt`.
- **Collaudo**: `test_controlli.py` 224/224 (13 verifiche nuove: impronta nel comando,
  `leggi_baseline`, `test_kit_copilot_studio` con lo script eseguito come processo a parte e
  confrontato con il comando); `verifica_riferimenti.py` 30/30 (indice con i file nuovi); mappa
  126/126, fonti 21/21; catena con Excel 277/277 (refactoring senza cambi di comportamento).
- **Documentazione**:
  - DECISIONI: D-70, note su A-15 e D-11;
  - 00_LEGGIMI: indice, "Dove vive ogni regola", unica copia di codice verificata, stato nel tenant;
  - guida: 0-bis e 5-bis;
  - README della variante, governance (rischio del codice dentro l'agente), Piano_deploy, TODO (AU2,
    AU4, ordine), LEGGIMI del collaudo;
  - analisi 10 (10.10, 10.20) e 00 delle analisi;
  - PROMPT_MASTER.

  Demo rilanciata il 05/10: stessi risultati, piu' la riga dell'impronta del precontrollo nel report.
- **06/10, guida snellita** (richiesta dell'utente: ogni passo o opzione spiegato una sola volta): titoli e
  numerazione invariati, riferimenti incrociati 30/30. Tolte le ripetizioni (cartelle interne ed esterne
  solo in 0.1, comando e registro chiuso solo in "Come si scrive un comando", pesi e storia dei template
  in 0-bis una volta, contenuto delle schede solo nella sezione 4, "Quando si lancia A5/A6" dentro le righe
  della sezione 2, rimedi degli errori solo nella sezione 7). Esplicitato che l'allegato `Input_A1` va nella
  chat di A1, non nel `Kernel`: A1 non ha il `Kernel` tra le knowledge (segnalato dall'utente il 06/10, "Baseline mancante").
- **Sul PC della Banca**:
  1. estrarre `NFR_pacchetto_completo_2026-10-05.zip` (c'e' `precontrollo.py`, senza il quale lo
     script non parte); agenti e kernel uguali al 02/10;
  2. seguire le due prove;
  3. il kit di Copilot Studio e' anche in `NFR_kit_prova_Copilot_Studio_2026-10-05.zip`.

## 2-novodecies. 06/10: A5 facoltativo, segnalazioni dei controlli in validazione (D-71)

Richieste dell'utente: i passaggi di precontrollo e A5 "appesantiscono molto la procedura"; C3, C5 e C9
come "attributi di cui il validatore tiene conto"; poi "voglio che A5 sia facoltativo e che le sue
segnalazioni appaiano in una colonna aggiuntiva in fase di validazione, una sola colonna ma col
dettaglio/descrizione degli eventuali controlli non passati". Scelte confermate con due domande: un
Bloccante di A5 non ferma piu' (va in validazione); C3, date di C5 e C9 (coppia e soglie) diventano
segnalazioni.

- **Gravita'** (`controlli_a5.py`): Bloccante solo per l'integrita' (schema, C1, C2, C7, identificativi
  dei KRI di C9); "Da motivare" C3 (date, frasi generiche, salto di piu' di un punto), date delle fonti di
  C5, coppia e soglie dei KRI di C9, e ogni Bloccante di A5 (`combina`); Osservazione il resto.
- **`trimestrale`**: `--challenger` facoltativo; ferma solo per integrita' e allora scrive
  `Cicli/<ciclo>/Correzione_A1_<ciclo>.txt` (stesso messaggio del precontrollo); a video "A5: usato / non
  usato" e "SEGNALAZIONI DA MOTIVARE: n su m rischi"; `--procedi-con-rilievi` accettata ma inutile (lo
  dice). Colonna Rilievi: una riga per segnalazione, `⚑ DA MOTIVARE · C3 · controlli: ...`;
  Rilievi_Superati di Sintesi_Cicli = "Segnalazioni da motivare in validazione: n (controlli x, A5 y)".
- **Griglia**: colonna P **Segnalazioni dei controlli** nella sezione Rischi (testo della colonna Rilievi,
  anche per KRI e azioni del rischio; nella riga del titolo quelle sul ciclo), ⚑ e Motivazione
  obbligatoria per ogni rischio con una segnalazione da motivare.
- **`valida`**: non accetta un salto di piu' di un punto nemmeno sulla proposta accettata cosi' com'e', ne'
  soglie invertite o una sola (salvo sui KRI respinti).
- **Template** 2026-10-06 (`aggiorna-registro`): colonna P, Registro "⚑ da motivare", Quadro "Segnalazioni da
  motivare" e "Controlli (A5 se usato)", testi di guida dei fogli, Dizionario.
- **Prompt**: A5 7.962 caratteri (ruolo: "I tuoi rilievi vanno al validatore: un Bloccante lo obbliga a
  motivare la decisione"); A1 invariato, ma l'allegato `Input_A1` dice che solo i difetti di integrita'
  fermano. Kit di Copilot Studio rigenerato.
- **Collaudo**: `test_controlli.py` 225/225 (gravita' nuove, A5 facoltativo in `combina`); catena con Excel
  275/275: passo 1 con un kri_id di un altro rischio (fermo e messaggio per A1), passo 10 con il primo
  ciclo senza A5, **passo 12 riscritto** (C3, soglie di C9 e Bloccante di A5 in colonna, ⚑, `valida` che
  chiede le motivazioni e rifiuta salto e soglie); mappa 126/126, riferimenti 30/30, fonti 21/21.
- **Documentazione**: DECISIONI (D-71, D-56 superata), guida (parole, comandi, 0.2, 0-bis, sezione 2 punti
  5-bis..8-bis, "Che cosa controlla lo script", sezione 3, 4, errori), 00_LEGGIMI, README della variante,
  workflow, governance, Piano_deploy, SharePoint, manuale del template, schema documentato, COMMENTATI
  (A5), LEGGIMI del collaudo, `controlli_A5.md` (nota), protocollo di prova senza Copilot Studio, TODO
  (AU2; nuova P9 "temi da verificare indicati dall'analista"), PROMPT_MASTER (trappole 85-86), analisi 00,
  10 e 11. Demo rilanciata: A1 difettoso con un kri_id di un altro rischio (fermato dal precontrollo e da
  `trimestrale`, che scrive il messaggio per A1), 2026Q3 con A5, **2026Q4 senza A5**; `REPORT_demo.md`
  aggiornato. `aggiorna-registro` ora riconosce le righe vuote "Da decidere" dello storico e dice come
  toglierle (non coperto da un test con Excel).
- **Sul PC della Banca**: pacchetto completo; tutti i file di `01_Kernel` nella library Kernel;
  **reincollare A5** (se lo si usa); `aggiorna-registro` (struttura 2026-10-06; con il registro vero
  bloccato dalle righe "Da decidere" vuote del 06/10, prima vanno tolte: sezione 7 della guida).
- **Altro del 06/10**: guida snellita (ogni passo una volta); diagnosi della validazione
  (`diagnosi_validazione.py`, fuori dal pacchetto) dopo che `valida` aveva contato 0 rettifiche su modifiche
  probabilmente fatte su una copia o non salvate (recupero dal Backup); Copilot Studio in Banca: solo
  l'esperienza standard, knowledge SharePoint "Bloccata" (probabile data policy), Code interpreter da
  verificare con l'IT.

## 2-vicies. 07/10: piano degli agenti nuovi e fase 1, A7 Assistente del registro (D-72)

Richieste dell'utente: un agente che risponda in modo approfondito e motivato sul radar (perche' le valutazioni,
perche' temi dei documenti non sono rischi); uno per evento critico o rischio nuovo che analizzi documenti indicati
e censisca; uno di manutenzione (togliere priorita', lista di osservazione, modifiche puntuali). Vincoli: ridurre al
minimo le interazioni con Python; A7 completamente interattivo, senza allegati; manutenzione meglio in Excel o in
chat a testo libero, mai un JSON da gestire a mano; spiegazioni e manutenzione in un solo agente. Scelte con domande:
A1 registra i fenomeni scartati; A8 con ciclo straordinario e rivalutazione dei rischi indicati; manutenzione
applicata subito (eccezione a D-05); lista di osservazione nel piano.

- **Piano approvato** (TODO, sezione "Agenti nuovi"): 1 A7 spiegazioni (fatta); 2 lista di osservazione (P8);
  3 periodo straordinario `AAAAQn-Sk` (P3); 4 manutenzione in Excel con A7 in modo manutenzione; 5 A8 evento
  critico. Circa 14-15 giorni in tutto.
- **Fase 1 fatta**:
  - `07_Senza_Studio/spiegazioni.py`: knowledge di A7, un `.txt` per posto dell'anagrafica, `Rischio_01..20.txt`
    con nomi fissi (un rischio appena censito e' visibile subito; riuso di `schede.input_schede`,
    piu' decisioni del validatore e segnalazioni) e `Ciclo.txt` (stato, classifica, commento di A1, controlli,
    parametri del radar, fenomeni non censiti, dismessi, note), nella cartella `Spiegazioni` della library Kernel
    (con il kernel del pacchetto, in quella di uscita); la riscrivono `trimestrale`, `valida`, `dismetti`;
  - schema di A1: `fenomeni_non_censiti` facoltativo; guida di scrittura con il formato; prompt di A1 invariato;
  - Quadro: Note dell'analista in prima pagina (`quadroNote`), archiviate da `trimestrale` in
    `tblSintesi.Note_Analista`; conservate da `aggiorna-registro`, svuotate da `inizializza`; struttura 2026-10-07;
  - A7: `02_Agenti/modelli/A7.md` -> `A7_Assistente_registro.md` (6.575 caratteri); copione `08_Deploy/Prova_A7.md`.
- **Collaudo** (primo giro 278/280: note archiviate con un apostrofo in piu' e Quadro in 3 pagine dopo una settimana,
  corretti: aggiorna non riapplica per_cella, `scala_quadro` usa l'interruzione manuale, `settimanale` chiama
  `prepara_report`, scala del template al 74%; trappola 89): `test_controlli.py` 231/231; catena con Excel 280/280
  (knowledge dopo trimestrale, valida e dismetti; note archiviate; fenomeni di run3); mappa 127/127, riferimenti
  30/30, fonti 21/21. Dati di prova: `run3_A1_2026Q4.json` con due fenomeni non censiti.
- **Documentazione**: DECISIONI (D-72), guida (parole, 0.2, 0-bis, "Chiedere il perche' ad A7", sezione 6),
  00_LEGGIMI, README, Piano_deploy, workflow (W4), governance, SharePoint, manuale del template, schema
  documentato, COMMENTATI (A7), LEGGIMI del collaudo, TODO, PROMPT_MASTER (trappole 87-88), indice delle analisi.
- **Sul PC della Banca**: pacchetto completo; tutti i file di `01_Kernel` nella library Kernel; creare A7 (guida
  0.2: knowledge la cartella `Kernel/Spiegazioni` intera piu' `Analisi_*` e `News_Inbox`); `aggiorna-registro`
  alla 2026-10-07; dopo un `valida` o un `trimestrale` la cartella si riempie; prova con `Prova_A7.md`, che
  confronta A7 (file di testo) con una copia "A7 prova Excel" che legge solo il registro: decide se i file di testo
  servono davvero (domanda dell'utente del 07/10).
- **Guida riorganizzata** (richieste dell'utente del 07/10): in testa "In breve: i cicli standard" (settimana,
  trimestre, passi "quando serve", un passo per riga con il rimando alla sezione di dettaglio); sezione 8 "Gli
  agenti: mansioni e messaggi da usare" (tabella degli agenti e, per ciascuno, messaggio base e variazioni: il
  messaggio rinforzato di A1 si sposta qui dalla sezione 2); sezione 9 "I comandi Python" (codici di uscita,
  opzioni comuni, ogni comando con parametri, opzioni, file scritti, errori tipici); "Cosa lanci tu" rimanda
  alla sezione 9. `verifica_riferimenti.py` riconosce le opzioni comuni scritte prima del nome del comando.

## 2-unvicies. 07/10 sera e notte: lista di osservazione, A3, straordinario, tassonomia interna, documenti unificati

- **Fase 2, lista di osservazione (D-73)**, poi **A3 collega le notizie alle voci** (punto 6: `voce_osservazione`,
  `segnali_osservazione`, nella baseline `notizie_a3` e `segnali_a3`). Catena 288/288 (prima della fase 3).
- **Fase 3, ciclo straordinario `AAAAQn-Sk` (D-75)**, con la proposta di A3 (`proposta_straordinario`) e di A4.
  Scelte dell'utente: lo straordinario conta come ciclo per la regola del punto; proposta insieme al motore.
  Comando `baseline --straordinario`; `Periodo_Valutazione` nel RiskRegister; periodi delle viste scritti dallo
  script (`dataRiferimento`); dati `run4_A1_2026Q4-S1.json`; catena: passi 7b e 8s (271/272 prima della
  tassonomia; l'unico KO era la migrazione di un registro senza `tblSintesi`, corretta con `_righe_o_niente`).
- **Tassonomia interna della Banca (D-74)**: l'utente ha fornito `01_Kernel/Tassonomia dei Rischi.csv` e scelto:
  le nove categorie SI sostituiscono del tutto Basilea; radar a nove settori; A1 riclassifica o segna FP.
  Schemi (A1 con FP, A3 a nove impatti), mappa (`Imp_9_n`, `Imp_L1_0x` dismesse), generatore (Parametri, radar,
  Notizie, Osservazione), controlli (C1 riclassificazione = Osservazione, FP = da motivare), fonti.md (temi),
  prompt (A1 7.971, A3 7.899, A5 7.973), dati e test convertiti, avviso in `aggiorna-registro`. Radar: legende
  spostate sotto (con nove etichette un angolo e' sempre occupato); nel radar piccolo del Quadro nessuna legenda.
  `Revisione_tassonomia_L2.md` (bozza Basilea L2) superato.
- **Documenti**: il piano di deploy e' la sezione "Avvio del progetto" della guida (`08_Deploy/Piano_deploy.md`
  eliminato, riferimenti aggiornati); l'analisi architetturale ha due opzioni (`Analisi_Architettura/12_Due_opzioni.md`,
  il resto in `Archivio/`); `diagnosi_validazione.py` eliminato; TODO con la sezione "Pulizia e ottimizzazione"
  (M1 collaudo piu' corto, M2 regola della demo, M3 `Anteprima_S1` non attuale, M4 alberatura, M5 fatto).
- **Collaudo** a fine giornata: suite veloci verdi (mappa 158/158, controlli 267/267, fonti 21/21, riferimenti
  31/31); catena con Excel sullo stato finale lanciata su una copia del pacchetto (esito nella sezione 4 quando
  disponibile). Demo da rilanciare (struttura cambiata).
- **Regola della demo (M2)**: si rigenera solo quando cambia cio' che si vede (template e viste, report, schede,
  knowledge di A7, passi della guida, comandi) e prima di ogni consegna in Banca; non a ogni modifica interna.
  Scritta nel PROMPT_MASTER, sezione DEMO.
- **Sul PC della Banca**: pacchetto completo, kernel nella library Kernel, reincollare A1, A3, A4, A5 e A7,
  `aggiorna-registro` alla 2026-10-08b; al primo ciclo A1 riclassifica i rischi.
- **Restano** del piano agenti la fase 4 (manutenzione in Excel e A7 in modo manutenzione) e la fase 5 (A8).

## 3. Scostamenti dal PROMPT_MASTER precedente, e perche' (tutti recepiti nella versione del 23/09)

1. **Kernel "incollato per intero" non e' possibile.** Le istruzioni di un agente
   (Agent Builder e Copilot Studio) hanno un limite di 8.000 caratteri
   (Microsoft Learn, agg. 19/08/2026); kernel + schema superano i 20.000.
   Soluzione: `02_Agenti/componi_prompt.py` inserisce in ogni prompt le sole
   sezioni del kernel che servono a quell'agente, prese dai file del kernel
   (righe ">" escluse come note per chi legge), e verifica il limite. Il
   principio "kernel nelle istruzioni, non in knowledge" e' salvo; lo schema
   JSON intero non e' nel prompt (c'e' uno scheletro), perche' lo applica il
   validatore. (Recepito nel PROMPT_MASTER del 23/09.)
2. **Nessuna copia di codice.** Il master chiedeva di copiare il validatore in
   `07_Senza_Studio`. Qui il validatore e' generico (interpreta lo schema,
   non ricopia le regole) ed esiste una volta sola; la suite di collaudo
   importa il codice di campo invece di averne una propria versione. Tre punti
   da sincronizzare a mano sono diventati zero.
3. **Una sola implementazione della scrittura per entrambe le varianti.** Anche
   con Power Automate la scrittura e' lo stesso script, lanciato da un desktop
   flow (`05_Workflow`): "Analizza JSON" non applica pattern, enum, min/max ne' i
   controlli di A5.
4. **Mappa campi come dato** (`01_Kernel/mappatura_campi.json`): colonne delle
   tabelle e delle liste, sorgenti, formule. La leggono generatore, scrittura e
   collaudo.
5. **Stato storico nel workbook, liste come copia** (23/09, su richiesta
   dell'utente): la tabella KRI e' diventata storica (una riga per KRI per
   ciclo, solo in coda), con le viste `KRI_Correnti` e `Andamento_KRI`. Tutte
   le tabelle dati sono quindi storiche; le liste SharePoint sono una copia
   (`Righe_liste_<ciclo>.json`, caricate da Power Automate). Nella variante
   locale non si perde storia.
5-bis. **Elenco fonti** `01_Kernel/fonti.md` (23/09): 32 fonti commentate su
   tre canali (rss, sito, share), tutte "da validare"; feed verificati dal
   vivo il 23/09. Entra nel prompt di A3 (`{{FONTI}}`), alimenta
   `raccogli_notizie.py` (W0 locale) e il controllo `codice_fonte` (nuovo
   campo obbligatorio di A3, colonna `Codice_Fonte` in NewsLog).
6. **Approfondimento e Analisi_News sono automatici** (una sola cella di input
   in Approfondimento): chiude il punto aperto "i fogli manuali invecchiano male".
7. **Niente `OfficeScript_opzionale.ts`**, per scelta dell'utente (solo Python).
8. Dati di prova: 6 rischi (non 9), rischio nuovo NFR-07 su L1-03 al secondo
   ciclo. **Superato il 23/09 pomeriggio**: ora 12 rischi, rischio nuovo NFR-13.

## 4. Come e' stato verificato

**Aggiornamento 24/09 sera**: suite completa tutto OK sul pacchetto
aggiornato, template rigenerato compreso. Prompt A1 7.972, A3 6.991, A4
4.878, A5 7.729; 99 + 165 + 21 + 27 senza Excel; catena con Excel 105. Poi il
nuovo **passo 10 della catena** (registro di produzione: dal vuoto, per le
settimane, al primo ciclo, alla validazione e al secondo ciclo) e' passato sul
template attuale e su quello del 23/09 con cui e' stato creato il registro in
uso: 16 + 16 verifiche. Da ora la catena conta 121 verifiche (105 + 16); il
totale della suite e' 433.

Stato precedente, 23/09:
`python NFR_Emerging_Risk_Agents/99_Collaudo/esegui_collaudo.py` -> tutto OK
(23/09 notte, dopo la revisione): prompt aggiornati e sotto il limite (A1 7.884, A3 6.946, A5
7.729); mappa in entrambe le direzioni (99); validatore, controlli A5, dati di
esempio, regole delle rettifiche, Variazioni dopo una rettifica, scrittura come testo, consistenza (162); elenco fonti e raccolta
(21); riferimenti incrociati, comandi della guida compresi (27); catena con
Excel (105, circa 10 minuti: due cicli, validazioni, Radar_Mosca contro un calcolo indipendente,
radar dinamico, A5 di un altro ciclo, BOM, titoli con "=", primo uso con
`inizializza`, `dismetti`). Totale 414 verifiche. Prove di mutazione: codice fonte non controllato e
rettifiche dei rischi non applicate sono entrambe intercettate. I dati di
prova sono stati rigenerati per 12 rischi con lo strumento vero (baseline
estratte dal template e dopo la validazione del 2026Q3). Prova di
mutazione: tre modifiche deliberate (rubrica non ricomposta, colonna
rinominata, passo tolto dalla documentazione) sono state tutte intercettate.

Limiti del collaudo:
- I payload degli agenti sono stati scritti da Claude seguendo i prompt, **non
  sono output dell'agente Copilot reale**. Retrieval e riproducibilita' vere si
  misurano solo in tenant (doppio run + `confronta.py`).
- Outlook tolto su richiesta dell'utente (23/09): ogni run produce invece un
  Excel di output con nome proprio in `Archivio_Cicli/Cicli/<ciclo>/` o
  `Settimane/<lunedi'>/`, con gli output degli agenti; ogni tentativo, anche
  fermato, resta in una sottocartella. Demo completa in `../Demo_W1_W2/`.
- Excel usato: desktop, via COM. Excel per il web non testato.

## 5. Trappole trovate in questa sessione (non reintrodurle)

1. **Date via COM**: pywin32 converte un `datetime` come ora locale -> UTC e la
   data scritta slitta di un giorno. Si scrivono seriali di Excel.
2. **Upsert che cancella formule**: aggiornare una riga con tutti i campi della
   mappa sovrascriveva la formula Stato con un vuoto, senza errori. Ora le
   colonne formula non si scrivono mai come valori, e la verifica post-scrittura
   controlla che ogni colonna formula abbia la formula (`formule_mancanti`).
3. **Nome definito sbagliato** (`RR_ID` invece di `RR_ID_Rischio`): trovato solo
   dal ricalcolo in Excel (#NAME?). Il ricalcolo con motore vero e' indispensabile.
4. **Fonti "dal futuro" nei dati di esempio**: il generatore ripiegava su una
   fonte datata dopo il ciclo. Ora il collaudo sottopone i dati di esempio ai
   controlli C1-C5.
5. **Messaggio falso dopo il salvataggio** (trovato nella demo del 23/09): un
   Excel dell'archivio aperto faceva fallire la copia DOPO il salvataggio del
   registro, e lo script diceva "workbook non salvato" lasciando indietro la
   baseline. Ora baseline prima, Excel per ultimo, messaggio "E' STATO SCRITTO,
   non rilanciare"; test 8 della catena.
6. **Titolo e legenda sopra i grafici**: openpyxl non scrive `overlay`, ed Excel
   li sovrappone all'area. `fuori_dal_grafico()` in `genera_dashboard.py`.
7. **Knowledge di Agent Builder non legge .json ne' .md**: baseline scritta
   anche in `.txt`, raccolta notizie in `.txt`.
8. `shutil.copy2` verso una cartella copia DENTRO la cartella: per simulare un
   file bloccato nei test serve un file in sola lettura.
10. **Grafici con dati in colonne nascoste**: Excel non li disegna se non si
    imposta "mostra dati nascosti" (`visible_cells_only = False`).
11. **COM in italiano**: `Names.Add` interpreta la formula nella lingua di
    Excel (SCARTO, `;`); per i nomi definiti usare openpyxl in generazione.
12. **Periodo settimanale come testo** (`'2026-10-12`): scritto come data,
    Excel potrebbe restituirlo come numero e il confronto fallirebbe.
13. **"Nome Cognome" contro "Funzione Compliance"**: la regola dell'owner-persona
    e' una sola (`controlli_a5.sembra_persona`), usata da C8 e dalla validazione.
14. **Tabella vuota = nomi che scivolano**: `ListRows.Add` su una tabella senza
    righe inserisce in cima all'intervallo dei nomi definiti. Il registro
    inizializzato tiene una riga segnaposto.
15. **Testo che diventa formula o data** via COM: scrivere ogni testo con
    l'apostrofo (`per_cella`).
9. Le trappole del pacchetto precedente (upsert KRI, anagrafica per i rischi
   nuovi, append relativo alla tabella, SUMIFS assolute, assi fissi, note a lato,
   copertura in C10/E10 con COUNTIF "NFR-*", guardie dello Stato KRI,
   ricalcolo KRI a livello ciclo, kri_id non obbligatorio) sono tutte nel
   disegno e ciascuna ha un test.

## 6. Cosa manca, in ordine

Decisioni della Banca (non tecniche), prima di tutto:
- [ ] Adattare tassonomia, descrittori, pesi, soglie KRI (segnaposto, NON
      raccomandazioni). Poi la procedura "Se cambia il kernel" di 00_LEGGIMI.
- [x] Qualificazione model-risk: non rilevante, nessun requisito ulteriore (D-23, 24/09).
- [x] Rapporto col processo di rischio operativo esistente: affianca (D-14, 24/09).
- [x] **`08_Deploy/DECISIONI.md` creato e compilato il 24/09**, aggiornato il
      25/09: 38 decisioni prese (D-01..D-38) e 5 aperte (A-14: ridisegno del registro), con i responsabili. Le decisioni della
      Banca si leggono li'. In sintesi: Corrado copre tutti i ruoli, validatore
      compreso (limite di segregazione accettato nel pilota, D-30); il registro
      affianca il processo esistente; model risk non rilevante; parere DPO
      positivo; fonti tutte approvate tranne FNT-19 (esclusa); report al
      comitato in PDF dei sei fogli di report (D-32); notizie validate a discrezione; rubrica e parametri
      provvisori; primo ciclo 2026Q4; criteri di accettazione 80/80/30.
      **Cancelli G0, G1 (provvisorio) e G2 (con condizione) firmati il 24/09**;
      G3 senza data.
- [ ] Condizione di G2: ricaricare per intero le istruzioni di A1, A3 e A4
      (cambiate il 24/09; A3 anche per FNT-19 esclusa) e, dal 25/09, anche di
      A1 e A5 (sintesi, rubrica senza pesi; A1 di nuovo la sera: commento
      "MESSAGGIO: ... DECISIONI: ..."; A4 per il nome del foglio Notizie),
      **creare A6** (D-40), spegnere il code interpreter sui cinque agenti,
      ripetere la prova di fumo (Piano_deploy 6.4, anche per A6).
- [x] Aggiornare il registro in uso al template del 25/09 sera (versione
      2026-09-25c): fatto prima del ciclo di prova del 29/09.
- [ ] **Aggiornare il registro in uso alla versione 2026-09-30** (S1): validare
      o chiudere il ciclo di prova in corso, copiare pacchetto e kernel
      (rubrica, tassonomia, mappa, DECISIONI), `aggiorna-registro` **prima su
      una copia** del registro, poi sul registro; ricaricare le istruzioni di
      **A1, A5, A6 e A4**; ricaricare `Baseline_corrente.txt` in `Kernel`;
      rifare il ciclo 2026Q4 di prova (obiettivo: 1-2 giri A1-A5, oppure un giro
      e `--procedi-con-rilievi`). Guida, sezione 0-bis.
- [ ] Copiare nella library `Kernel` del tenant il nuovo `01_Kernel/fonti.md`
      (e `DECISIONI.md`): la raccolta notizie legge gli stati da li'.
      Il template e' stato rigenerato il 24/09 (notizie di esempio da FNT-19 a
      `MAN`). Il registro gia' creato con `inizializza` non contiene esempi,
      quindi non cambia. `Demo_W1_W2/` e' stata rilanciata il 25/09 sera sul
      layout nuovo (i payload di prova non citano FNT-19).
- [ ] Verifiche dell'utente su S1: bozza della rubrica e schemi, anteprima del
      template (`Anteprima_S1/`), dimensioni dei prompt; demo da rilanciare.
- [ ] Decidere sui tre suggerimenti della proposta esterna (TODO, S1, "fuori
      dal perimetro").
- [ ] P8 nel TODO (02/10): lista di osservazione dei fenomeni oltre
      l'orizzonte del registro, con valutazione preliminare (impatto
      potenziale, orizzonte in anni, plausibilita', segnale di avvicinamento)
      e collocazione per driver, event type e rischi collegati; nasce dalla
      domanda su come censire rischi a 10 anni o quasi impossibili senza
      allargare il registro (a 50 rischi non reggono risposte degli agenti,
      validazione e report). Da decidere: scala, revisione, criteri.
- [ ] **Due prove sul PC della Banca (05/10, pacchetto del 05/10)**:
      `08_Deploy/Prova_senza_Copilot_Studio.md` (installazione sul registro
      vero, poi un ciclo 2026Q4 completo su un registro di prova in
      `C:\NFR_Prova`) e `09_Copilot_Studio/Prova_con_Copilot_Studio.md` (A1 in
      Copilot Studio sullo stesso input, precontrollo dentro l'agente con il
      Code interpreter o con la skill; domande all'IT in B0). Attese: le due
      tabelle dei risultati. L'utente stava verificando se il pacchetto del
      02/10 e' gia' installato (la prova lo controlla al passo 1.1).
- [ ] Aperte in DECISIONI: A-15 (strada A o variante CS-1 con Copilot Studio,
      alla fine della parte comune del piano 10: TODO AU4; dal 05/10 con i
      risultati della prova K0 estesa, D-70), A-11 (con A-15),
      A-12 (dopo il primo ciclo), A-13 (ogni anno). A-05 chiusa il 28/09 da
      D-44: Copilot Studio e Power Query disponibili.
- [x] **D-19** in vigore dal 25/09 (template 2026-09-25, collaudo completo).
- [x] Validare `01_Kernel/fonti.md`: fatto il 24/09, tutte approvate tranne
      FNT-19, esclusa (D-15, D-16, D-27, D-28, D-29).
- [x] Compliance su Agent Builder: parere DPO positivo (D-24); Agent Builder attivo
      e licenze assegnate (D-25), 24/09.

Nel tenant (fuori dalla portata di Claude Code) — seguire `08_Deploy/Piano_deploy.md`:
- [x] Sito, library (`04_SharePoint`); registro creato con `inizializza` (24/09,
      ciclo precedente 2026Q3).
- [x] Agenti in Agent Builder, tutti e quattro provati (G2, 24/09; condizione: ricaricarli).
- [ ] Creare A6 Schede dei rischi in Agent Builder (D-40) e provarlo su un input
      prodotto da `schede-input` (Piano_deploy 6.4).
- [ ] Verificare dove arriva il risultato di un prompt schedulato (chat, mail?).
- [x] Script di campo sul PC dell'analista (D-26); verifiche tecniche aperte qui sotto.
- [ ] Raccolta notizie dal PC della Banca: verificare che il proxy lasci
      passare urllib (`raccogli_notizie.py --anche-da-validare`); pianificarla.
- [ ] Verificare in tenant che A3 legga davvero `Raccolta_*.txt` e i file in
      `Manuali` dalla knowledge SharePoint, e che citi i codici fonte.
- [x] Elenco fonti (bozza) e W0 locale — fatti il 23/09.
- [x] Storico KRI nel workbook, con viste dei KRI del ciclo e della storia di un KRI
      (dal 25/09 sera nel foglio Indicatori) — fatto il 23/09.
- [x] Demo rilanciata per intero il 23/09 (12 rischi, validazioni, Radar_Mosca).
- [ ] Validare il metodo dell'urgenza (Mosca): valori di Z per Prossimita, X,
      Y di riserva (la Probabilita nel composito e' decisa: D-19). Dal 25/09 il
      validatore puo' indicare per ogni rischio gli anni di adeguamento (D-33):
      decidere per quali rischi servono.
- [x] (24/09: validatore = Corrado, D-13; notizie facoltative, D-17) Decidere chi e' il validatore e se la validazione delle notizie
      settimanali e' obbligatoria (oggi facoltativa, non bloccante).
- [ ] Apprendimento dalle rettifiche (rimandato su richiesta): la base dati e'
      il foglio Validazione + `Validazione_<periodo>.json`; vedi 06_Governance 4-bis.
- [ ] Limite noto: la legenda dello Storico mostra voci vuote per le righe libere
      dell'anagrafica (serie per riga, non rese dinamiche).
- [ ] Collaudo in ambiente sul primo ciclo **da registro vuoto**: doppio run
      con `confronta.py --primo-ciclo`, lettura dell'analisi, validazione
      (Piano_deploy, fase 7). Non serve un trimestre gia' valutato a mano.
- [ ] Code interpreter: acceso di default in Agent Builder, mentre la guida dice
      "nessuna capability". Verificare/spegnere sui quattro agenti gia' creati e su A6.
- [ ] Ritestare sul PC della Banca: raccolta con `pypac`, comando `settimanale`
      (errore COM `RPC_E_DISCONNECTED`).
- [x] Piano `Analisi_Architettura/Archivio/07`: in riserva dal 27/09 (D-43, registrata
      il 28/09); si riprende solo se la Banca vietasse Python sul PC.
- [ ] Piano `Analisi_Architettura/Archivio/10` (27/09, esteso il 28/09), ora nel TODO
      come voci AU1-AU6 con l'ordine unico di lavoro. Prossimo passo proposto:
      AU1-AU3 (parte comune, 6-7 giorni), poi la decisione A-15 (AU4). Nessuna
      voce e' ancora approvata per la realizzazione.
- [x] Proposte di priorita' A di `Analisi_Architettura/Archivio/08`: approvate e
      applicate il 25/09 (D-19, D-32, D-33, D-34).
- [x] P3, P6, P11 di `Analisi_Architettura/Archivio/08` applicate il 25/09 (D-35..D-37).
- [ ] Decidere sulle proposte rimaste di `Analisi_Architettura/Archivio/08`: P7 azioni
      di approfondimento, P8 report di settore fra le fonti (licenza ORX), P10
      tracciabilita'. Descrittori di plausibilita' della Probabilita: A-12.
- [x] Anteprima v1 valutata dall'utente il 25/09 (`09_Anteprima_v1_valutata.xlsx`).
      Indicazioni: un solo file con report e registro senza doppioni; schede dei
      rischi in un file a parte, a tendere scritte da un agente dedicato; tutto il
      registro ridisegnato e molto piu' spiegato; "Horizon Scan NFR"; bordo giallo
      invece di rosso (gia' applicato al pacchetto, D-35).
- [x] Anteprima v2 valutata (`09_Anteprima_v2_valutata.xlsx`): struttura approvata; commento di
      A1 breve (messaggio e decisioni), il "perche'" lo calcola il foglio.
- [x] Anteprima v3 confermata (tutte "Sì") e realizzata il 25/09 sera: D-39 (file
      unico ridisegnato, versione 2026-09-25c) e D-40 (agente A6, file delle schede).
- [ ] Al primo PDF vero del report: controllare impaginazione e altezze delle
      righe su un PC con stampante (in collaudo: PDF esportato dal template e
      dalla demo; le altezze le stima lo script contando i caratteri).
- [ ] Al primo ciclo con A6: leggere le schede prima del comitato (nessun nome
      di persona; testi coerenti: lo script controlla numeri e fonti, non il senso).

Miglioramenti aperti (scelte, non difetti):
- [ ] Pesare i segnali per rilevanza (oggi ognuno conta uno).
- [ ] Mettere il pacchetto sotto git e agganciare `esegui_collaudo.py` a ogni
      modifica (la cartella non e' ancora un repository).
- [x] PROMPT_MASTER riscritto il 23/09 sera: incorpora scelte dell'utente, vincoli di Agent Builder,
      scostamenti, aggiunte (fonti, storico KRI, Probabilita, Mosca, validazione, guida) e trappole.
      La versione precedente e' in `PROMPT_MASTER_rigenerazione_precedente.md`.

## 7. Come riprendere

Ogni modifica: fonte unica (tabella "Dove vive ogni regola" in 00_LEGGIMI) ->
`componi_prompt.py` -> `genera_dashboard.py` se servono -> `esegui_collaudo.py`
tutto OK. Non modificare a mano i prompt in `02_Agenti/*.md`: sono generati.
**Regola dell'utente (24/09, ripetuta il 25/09)**: a ogni modifica aggiornare
subito anche `PROMPT_MASTER_rigenerazione.md` e tutta la documentazione toccata,
comprese le analisi in `Analisi_Architettura` (25/09 sera) e la demo.
Lo zip si crea **solo quando l'utente lo chiede** (25/09 sera).
Per una modifica grafica o di struttura del workbook: prima un'anteprima Excel
separata con i dati di esempio da far valutare all'utente, poi il generatore.
Se cambia la **struttura** del workbook: alzare `VERSIONE_TEMPLATE` in
generatore, script e mappa, e far lanciare `aggiorna-registro` sul registro in uso.
