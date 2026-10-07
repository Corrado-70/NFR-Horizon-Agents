# 09 — Proposta grafica per il report al comitato

Data: 25/09/2026. Stato: **approvata (anteprima v3, senza note) e applicata la
sera del 25/09** — decisioni D-39 (file unico ridisegnato, template 2026-09-25c)
e D-40 (agente A6 e file delle schede). Le anteprime v1 e v2 con le valutazioni
dell'utente sono archiviate nello zip del pacchetto 2026-09-25b; in questa
cartella restano la v3 (`09_Anteprima_v3_registro.xlsx`, `_schede.xlsx`) e i
generatori delle tre anteprime.

**Realizzazione nel pacchetto (differenze rispetto alla v3):**
- nomi dei fogli senza spazi e apostrofi (Excel li vuole fra apici nei
  riferimenti dei grafici): **Quadro** (il titolo resta "Quadro d'insieme"),
  **Piano_azioni**, **Indicatori** (la v3 lo chiamava KRI, ma KRI e' il foglio
  dei dati); Radar_Mosca conserva il nome, che lo script e il collaudo usano;
- tutto e' formula sui dati: rischi segnalati e loro perche', motivi del Delta,
  mini matrice e mini radar del Quadro si ricalcolano a ogni ciclo; lo script
  adatta le altezze delle righe con testi calcolati (`adatta_altezze`);
- commento di A1 nella forma "MESSAGGIO: ... DECISIONI: ...", diviso dal Quadro;
- il Piano_azioni mostra proposte, azioni aperte e chiuse degli ultimi due
  cicli (la storia intera resta nel foglio Azioni), per restare di dimensione
  limitata (150 righe, nome `capienzaPianoAzioni`);
- le schede: comando `schede-input` (dati validati per A6), agente A6, comando
  `schede` che controlla l'output (stessi rischi, sei dimensioni, fonti
  identiche, nessun numero fuori dai dati) e scrive `Schede_<ciclo>.xlsx`;
  senza A6, schede con i testi del registro. **Dal 02/10 (D-68)**, su richiesta
  dell'utente, la scheda ha dopo "Il rischio" il **Razionale** (il fenomeno in
  termini di rischio), nella tabella dei valori **il perche' di ogni valore con
  i documenti**, nell'urgenza il motivo degli anni di adeguamento e, sotto ogni
  azione e KRI in vigore, "Perche'" ed "Effetto atteso": li scrive A1 nel
  razionale diviso in parti, A6 li riformula;
- trovati facendo: un intervallo senza nome del foglio dentro un nome definito
  impedisce a Excel di aprire il file; nei formati condizionali il
  riempimento va dato come colore di sfondo; un'etichetta di un punto #N/D si
  vede, quindi le serie "per esito" usano zero con un formato che lo nasconde
  (trappole 42-45 del PROMPT_MASTER); dal PDF della demo: con le righe dei motivi
  adattate al testo il grafico del Delta copriva la nota sulla scala (trappola 46).

Il testo qui sotto e' la proposta com'era prima dell'approvazione.

**Anteprima v2 (25/09, dopo la valutazione della v1)**: `09_Anteprima_v2_registro.xlsx` e
`09_Anteprima_v2_schede.xlsx`, generate da `09_genera_anteprima_v2.py`. La valutazione della v1
fatta dall'utente e' conservata in `09_Anteprima_v1_valutata.xlsx`. Indicazioni dell'utente
recepite nella v2:
- **un solo file** con report e registro, senza doppioni: struttura proposta nel foglio omonimo
  (Guida; report: Sintesi in due fogli, "il quadro" e "il perche'", Classifica, Radar, Matrice,
  Delta, Metodologia; lavoro: Registro al posto di Dashboard e Approfondimento, Storico, KRI,
  Notizie, Validazione, Parametri, Dizionario; dati in fondo, linguetta grigia);
- **schede dei rischi in un file a parte**, a tendere prodotto da un **agente dedicato** (testi
  estesi: descrizione lunga, razionale per dimensione con l'evidenza, fonti e cosa sostengono);
- **tutto il registro ridisegnato e spiegato**: vista Registro, tabella dati con gruppi di colonne
  e riga "chi · cosa", Dizionario dei dati con il calcolo di ogni valore, Validazione con
  operazioni e criteri;
- nome dell'analisi **Horizon Scan NFR** nelle intestazioni;
- mini radar e legenda dei rischi nella Sintesi; sezione "Rischi segnalati e perche'",
  calcolabile dal registro; commento di A1 in quattro parti;
- elenco dei rischi anche nella matrice grande;
- **bordo giallo** per l'attenzione del supervisore (il rosso si confondeva con la linea di
  Mosca), spiegato dentro il grafico. Applicato subito anche al pacchetto (D-35).

**Anteprima v3 (25/09, dopo la valutazione della v2)**: `09_Anteprima_v3_registro.xlsx` e
`09_Anteprima_v3_schede.xlsx` (da `09_genera_anteprima_v3.py`); la v2 valutata e' in
`09_Anteprima_v2_valutata.xlsx`. Decisioni dell'utente sulla v2: struttura approvata; commento di
A1 breve (messaggio e decisioni) con il "perche'" calcolato dal foglio. Affinamenti:
- **Quadro d'insieme** (nuovo titolo della Sintesi) in un solo foglio, due pagine: numeri,
  priorita', matrice, radar con i dati nel foglio stesso e legenda dei rischi; poi commento di
  A1, A5 e avviso; poi "Rischi segnalati e perche'" con una colonna Urgenza (niente colori non
  spiegati);
- radar: in basso a sinistra il campione giallo e, sotto, la linea rossa "AGIRE ORA";
- Delta: la scala spiegata (quanto vale un punto di ogni dimensione, quando si ha ±1) e, a
  fianco, il motivo di ogni variazione o non variazione;
- Registro: "il ciclo corrente", gruppo "Notizie · 4 settimane", colonna Δ 6 mesi;
  l'andamento dei rischi negli ultimi trimestri va nelle schede;
- Dizionario completo (ogni colonna di ogni tabella, valori calcolati, parametri); legenda delle
  abbreviazioni in fondo a ogni report;
- Validazione: Stato a elenco; nuovo foglio **Piano azioni** (proposte da decidere, approvate,
  in corso, completate, con scadenza).

Da decidere dopo la v2 (DECISIONI, A-14, aggiornata): la struttura del file unico, l'agente delle schede e il
suo posto nel ciclo, il commento esteso di A1 (costa caratteri nel prompt, oggi a 7.951 su 8.000:
la parte "perche'" e' gia' calcolabile dal registro e puo' restare fuori dal prompt).

**Anteprima v1**: `09_Anteprima_stile_report.xlsx`, generata da
`09_genera_anteprima.py` con i dati di esempio del pacchetto. E' un Excel a
parte, non collegato al registro, con grafici nativi. Fogli: Come valutare
(con una colonna "Ti piace?" per ogni elemento), Sintesi, Matrice,
Classifica, Radar, Delta, Scheda. Non ancora nell'anteprima: le soglie del
Delta come linee e il salto pagina delle Schede.

Oggetto: aspetto dei sei fogli del report (Sintesi, Classifica, Radar_Mosca,
Delta, Schede, Metodologia) e dei grafici del workbook.

## 1. Vincoli (non cambiano)

- **Tutto nativo in Excel**, generato da `genera_dashboard.py` e legato alle
  formule. Il report esce dall'Excel validato con "Salva come PDF": niente
  immagini incollate, niente strumenti in piu' (D-31, D-32).
- **Scale fisse** (0-5 per gli score, -1/+1 per il Delta): un ciclo si
  confronta con l'altro a colpo d'occhio.
- **Nessun numero ritoccato per il grafico.** E' l'errore dell'esempio fatto
  con Copilot (documento 08, sezione 4).
- **Leggibile in bianco e nero e da chi non distingue rosso e verde.** Il
  colore conferma, non e' l'unico segnale: etichette, simboli e posizione.

## 2. Diagnosi: cosa non funziona oggi

| Dove | Problema | Effetto per chi legge |
|---|---|---|
| Sintesi | Solo testo, in due colonne | Il messaggio non si coglie in 10 secondi: servono numeri grandi e una figura |
| Classifica | Barre senza valore scritto | Per leggere lo score si deve stimare la lunghezza della barra |
| Lente di Mosca | Colonne in ordine di score, non di ritardo; nessuna etichetta del margine | Non si vede subito chi e' piu' in ritardo e di quanto |
| Radar_Mosca | Settori con il solo codice (L1-02); nessuna legenda delle aree; riempimento pieno | Un lettore non sa cosa sia L1-02; cerchi vicini si coprono; la dimensione non ha una scala di riferimento |
| Delta | Barre di un solo colore, senza valore | Aumenti e diminuzioni si distinguono solo dal verso |
| Manca | Matrice Probabilita x Severity | E' la figura che un comitato rischi si aspetta, e oggi non c'e' |
| Stile | Colori, caratteri e titoli dei grafici diversi da foglio a foglio | Il report sembra assemblato, non progettato |

## 3. Proposta

### 3.1 Stile unico (base per tutto il resto)

- **Tavolozza**:
  - blu notte `1F3864` per titoli e testo principale;
  - urgenza: rosso `C00000`, ambra `FFC000`, grigio `A6A6A6`;
  - aumento e diminuzione: rosso `C00000`, blu `2E75B6`, al posto del verde,
    cosi' si distinguono anche per chi confonde rosso e verde;
  - fondi dei processi della guida gia' in uso.
- **Caratteri**: Calibri; titolo del foglio 16 pt, titoli di sezione 12 pt
  bianchi su fascia blu notte, testo 10 pt.
- **Grafici**:
  - niente bordo esterno;
  - griglia grigio chiaro, solo dove serve;
  - titolo corto che dice il messaggio (es. "3 rischi da affrontare subito"),
    non il tipo di grafico: si ottiene con un titolo collegato a una cella con
    formula;
  - legenda in basso o assente se le etichette bastano.
- **Pagina**: una fascia di intestazione su ogni foglio del report con ciclo,
  data di riferimento e stato della validazione. E' una formula, cosi' anche
  una pagina stampata da sola dice di che ciclo e' e se e' validata.

### 3.2 Sintesi: una pagina executive

1. **Riga di cinque riquadri con numeri grandi**, celle unite con formule:
   - rischi valutati;
   - agire ora;
   - nuovi e variati;
   - KRI rossi;
   - stato della validazione.

   Ogni riquadro ha un fondo colorato solo se richiede attenzione (es. agire
   ora > 0 in rosso chiaro).
2. **A sinistra, i primi cinque**: tabella compatta con score, barra di dati
   nella cella (formattazione condizionale, scala fissa 0-5), urgenza come
   etichetta colorata, freccia di variazione (▲▼●).
3. **A destra, la matrice Probabilita x Severity** (3.3), in piccolo.
4. **Sotto, il commento di A1** e il controllo indipendente, come oggi, con i
   limiti in corpo piccolo.

La pagina resta una sola, in orizzontale.

### 3.3 Nuovo: matrice Probabilita x Severity (5 x 5)

- Una griglia di celle, non un grafico:
  - Probabilita in verticale, Severity in orizzontale;
  - in ogni cella gli ID dei rischi (TEXTJOIN su colonne di appoggio, come
    gia' negli elenchi della Sintesi);
  - fondo con formattazione condizionale in tre fasce sul prodotto P x I:
    fino a 6, da 8 a 12, da 15 in su.
- Si stampa nitida, si legge in bianco e nero e non ha sovrapposizioni.
- Il radar di Mosca resta per l'urgenza, la matrice mostra la gravita': le due
  cose si leggono separate.
- Posto: Classifica (in grande) e Sintesi (in piccolo).

### 3.4 Classifica e lente di Mosca

- **Barre**:
  - valore dello score scritto in fondo alla barra (2 decimali);
  - freccia della variazione nell'etichetta del rischio ("NFR-01 ▲ Frodi su
    pagamenti...").
- **Lente**, riordinata per **margine**, dal piu' in ritardo:
  - etichetta con il margine in anni sopra ogni colonna;
  - Y rosso se X + Y > Z, altrimenti arancio. Il colore dice subito chi
    sfora.
- Le due figure affiancate in orizzontale invece che una sotto l'altra, se la
  pagina lo consente. Da provare in stampa.

### 3.5 Radar di Mosca

- **Settori con il nome**, su due righe ("L1-02 / Frode esterna").
- **Legenda delle aree** in un angolo: tre cerchi di riferimento (P x I = 4,
  12, 25) con il valore.
- **Riempimento semitrasparente** (circa 40%), cosi' due cerchi vicini restano
  leggibili. Il bordo dell'attenzione del supervisore resta, in giallo (v2). Richiede un
  piccolo intervento sull'XML del grafico: openpyxl non scrive la trasparenza
  da solo.
- **Zona "AGIRE ORA" segnata**:
  - la scritta "AGIRE ORA" dentro il cerchio rosso;
  - l'anello fra 0 e 1 anno tratteggiato ambra, al posto del grigio.

  Non si puo' colorare l'area: un grafico a dispersione disegna linee e punti,
  non superfici.

### 3.6 Delta

- Due serie: aumento in rosso, diminuzione in blu, con il valore scritto.
- Righe ordinate dal maggiore aumento alla maggiore diminuzione.
- Soglia di Parametri come due linee verticali tratteggiate.

### 3.7 Schede

- Intestazione di ogni scheda su una fascia blu notte con posizione, ID,
  nome, score e urgenza.
- Punteggi in una **mini-tabella** di sei celle colorate da 1 a 5, invece
  della riga di testo "Severity 4 · Probabilita 4 ...".
- Salto pagina ogni due schede: una scheda non si spezza fra due pagine.

### 3.8 Viste di lavoro (non stampate)

Priorita' bassa:
- **Trend**: legenda dinamica (difetto G5).
- **Dashboard**: al posto del radar a tre cicli, poco leggibile, un grafico a
  punti "ciclo prima → ciclo corrente" per rischio.

## 4. Impegno e ordine consigliato

| # | Intervento | Impegno | Valore per il comitato |
|---|---|---|---|
| 1 | Stile unico + fascia di intestazione (3.1) | basso | alto: tutto il report sembra progettato |
| 2 | Matrice P x I (3.3) | basso-medio | alto: la figura attesa, oggi assente |
| 3 | Sintesi executive con riquadri (3.2) | medio | alto: messaggio in 10 secondi |
| 4 | Etichette e riordino di Classifica, lente, Delta (3.4, 3.6) | basso | medio-alto |
| 5 | Radar: nomi, legenda, trasparenza (3.5) | medio (XML) | medio |
| 6 | Schede con fascia e salti pagina (3.7) | medio | medio |
| 7 | Viste di lavoro (3.8) | medio | basso |

Ogni intervento passa dal collaudo (catena con Excel, confronto del report
con calcoli indipendenti) e da un controllo a occhio del PDF.

## 5. Claude Design: serve?

**Per costruire il report, no. Per decidere l'aspetto, puo' aiutare.**

Claude Design produce disegni e prototipi visivi (pagine HTML, tavole), non
grafici Excel collegati alle formule del registro. Il report deve:
- uscire dall'Excel validato del ciclo, con numeri che nessuno ricopia a mano;
- essere rigenerabile sul PC della Banca;
- passare dal collaudo automatico.

Un disegno fatto altrove andrebbe comunque ricostruito in
`genera_dashboard.py`, e ogni ciclo richiederebbe un passaggio manuale in
piu'.

Dove puo' essere utile: fare **una o due tavole di riferimento** della pagina
Sintesi e della matrice, **solo con i dati di esempio** (mai dati veri della
Banca fuori dal tenant). Si approvano quelle e poi si riproducono in Excel. Lo
stesso risultato si ottiene con un'anteprima HTML fatta qui, senza strumenti
in piu'.

Diventerebbe la scelta giusta solo se il comitato volesse un report in un
altro formato, per esempio slide. E' una decisione diversa, gia' esclusa per
ora (D-31, D-32).

## 6. Decisioni richieste

1. Approvare lo stile (3.1) e l'ordine del paragrafo 4, oppure sceglierne
   una parte.
2. Matrice P x I: soglie delle tre fasce (proposta: fino a 6, da 8 a 12, da
   15 in su).
3. Delta e aumenti: blu al posto del verde per le diminuzioni (sicuro per chi
   confonde rosso e verde).
4. Anteprima prima di applicare: tavola HTML con i dati di esempio, oppure
   direttamente il template di prova.
