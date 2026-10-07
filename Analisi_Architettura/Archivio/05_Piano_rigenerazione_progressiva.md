# 5. Rigenerare il progetto per fasi, validando man mano — a partire dal report trimestrale

> **Aggiornamento del 25/09/2026 sera (struttura del workbook 2026-09-25c,
> DECISIONI D-39 e D-40).** Il registro e il report sono ora un solo file
> ridisegnato; le schede dei rischi sono un file a parte, `Schede_<ciclo>.xlsx`,
> con i testi dell'agente **A6**, che si lancia dopo la validazione con un solo
> allegato preparato dallo script (che ne controlla l'output). I nomi dei fogli
> citati qui si leggono cosi': Dashboard -> **Registro** (tabella per rischio,
> controlli di validazione e copertura) e **Quadro** (report); Sintesi ->
> **Quadro**; Trend -> **Storico**; KRI_Correnti e Andamento_KRI ->
> **Indicatori**; Analisi_News -> **Notizie**; Approfondimento e Schede -> file
> delle schede; Leggimi -> **Guida**; il radar a tre cicli della Dashboard non
> c'e' piu' (lo sostituiscono Matrice e Radar_Mosca). Fogli nuovi: **Matrice**,
> **Piano_azioni**, **Dizionario**. Qualunque alternativa architetturale deve
> riprodurre questa struttura del report e il passo delle schede; il resto del
> documento e' l'analisi com'era alla sua data.

## 5.1 Perche' partire dal report

La rigenerazione "tutto in un colpo" (il PROMPT_MASTER) produce un pacchetto
coerente, ma la prima volta che una persona della funzione di rischio vede un
risultato e' alla fine, e la cosa piu' importante resta non misurata: **l'agente
valuta come la Banca?** Qui si fa il contrario:

1. si parte da **cio' che il comitato deve leggere** (il report trimestrale) e
   lo si fa approvare con dati **inseriti a mano** da un trimestre gia'
   valutato;
2. poi si costruisce, un pezzo alla volta, chi riempie quel report: prima la
   scrittura, poi l'agente, poi i controlli, poi il resto;
3. ogni fase finisce con un **cancello**: verifiche automatiche verdi **e** un
   si' esplicito di una persona. Non si passa alla fase dopo senza.

Ogni fase aggiunge verifiche a `esegui_collaudo.py`; quelle delle fasi prima
devono restare verdi (regressione).

## 5.2 Regole valide per tutte le fasi

- **Specifica unica**: `PROMPT_MASTER_rigenerazione.md` resta il riferimento
  per ogni dettaglio (scelte, vincoli, trappole). Ogni prompt di fase dice
  quali sezioni applicare e quali **non** ancora.
- **Trimestre di riferimento**: prima della fase 1 la funzione di rischio
  sceglie un trimestre gia' valutato a mano (rischi, punteggi, motivazioni,
  fonti). E' il metro di tutte le validazioni.
- **Una cartella sotto controllo di versione** (git): un commit a fine fase,
  con il nome della fase. Si torna indietro senza paura.
- **`DECISIONI.md`**: ogni scelta della Banca (descrittori, pesi, soglie, fonti,
  validatore) con data e chi l'ha presa. I prompt di fase la leggono.
- **Architettura**: il piano segue la raccomandazione con i vincoli attuali
  (documento 4: attuale evoluta verso C + D). Se si sceglie R2 (Copilot Studio),
  la tabella 5.5 dice cosa cambia fase per fase.
- **Guardare, non solo testare**: ogni fase con viste o grafici esporta le
  immagini e le fa vedere a chi le usera'.

## 5.3 Le fasi

### Fase 0 — Preparazione (mezza giornata)

- **Obiettivo**: avere il metro e le regole prima di scrivere codice.
- **Da produrre**: `DECISIONI.md` con le decisioni gia' prese (ambiente,
  tassonomia di Basilea, niente Outlook, validazione umana) e quelle aperte;
  il trimestre di riferimento in un foglio semplice (un rischio per riga:
  ID, nome, event type, driver, Severity, Velocity, Prossimita, Gap_Controlli,
  Probabilita, Confidence, motivazione, fonti).
- **Cancello**: la funzione di rischio conferma che quel foglio e' "la
  valutazione vera" di quel trimestre.

### Fase 1 — Il report trimestrale, con dati inseriti a mano

- **Obiettivo**: un report che il comitato accetterebbe, prima di qualunque
  agente.
- **Da produrre**:
  - il file dati minimo (`NFR_Rischi.xlsx`: tabella RiskRegister storica,
    anagrafica, Parametri con pesi e soglie) generato da script, con i nomi
    definiti assoluti;
  - il report (`NFR_Report.xlsx`) alimentato da Power Query: Dashboard con
    controllo di copertura, radar dinamico, Trend, Delta, Approfondimento;
  - il **generatore del report per il comitato** (PowerPoint via COM):
    sintesi, tabella dei rischi con variazioni e motivazioni, radar, rischi
    principali, limiti dichiarati;
  - uno script `carica_manuale.py` che porta il trimestre di riferimento (e,
    se c'e', il precedente) nel file dati.
- **Prompt per Claude Code**:
  ```text
  Leggi PROMPT_MASTER_rigenerazione.md (specifica) e
  Analisi_Architettura/05_Piano_rigenerazione_progressiva.md, fase 1.
  Applica SOLO: principi 1, 2, 5, 8; sezione "IL WORKBOOK" limitatamente a
  RiskRegister, anagrafica, Parametri, Dashboard, Trend, Delta,
  Approfondimento; architettura C+D del documento 4 (dati in NFR_Rischi.xlsx,
  viste in NFR_Report.xlsx con Power Query, report per il comitato in
  PowerPoint via COM). Niente agenti, niente KRI, notizie, validazione, Mosca.
  Carica i trimestri di riferimento da riferimento/*.xlsx con carica_manuale.py.
  Collaudo: ricalcolo in Excel senza errori, copertura, radar con un raggio per
  rischio, report PowerPoint generato. Esporta le immagini dei grafici e del
  report e fermati mostrandomele.
  ```
- **Verifiche automatiche**: zero errori di formula; controllo di copertura
  che vede un rischio mancante; il report si rigenera identico due volte di
  fila; Power Query si aggiorna senza errori.
- **Validazione umana**: la funzione di rischio confronta report e PowerPoint
  con la propria valutazione del trimestre di riferimento: numeri, ordinamento,
  leggibilita' dei grafici. Si correggono le viste, non i dati.
- **Cancello**: "questo e' il report che porteremmo in comitato" (per iscritto
  in `DECISIONI.md`).

### Fase 2 — Il contratto e la scrittura (senza agente)

- **Obiettivo**: poter riempire il report da un JSON, con controlli e fermo.
- **Da produrre**: kernel minimo (tassonomia, rubrica sezioni 1-3 in bozza),
  `schema_output_A1.json` ridotto ai rischi (dimensioni, probabilita,
  confidence, esito, variazioni, fonti, razionale), validatore generico,
  `mappatura_campi.json`, comandi `baseline` e `trimestrale` (senza KRI e
  azioni), controlli C1, C2, C3, C5, archivio per ciclo con tentativi, backup,
  codici di uscita veritieri.
- **Prompt**: "Fase 2: applica le sezioni Schemi e mappa (solo A1 ridotto),
  LO SCRIPT DI CAMPO (solo baseline e trimestrale, controlli C1-C3 e C5), le
  trappole 1-5. Scrivi a mano il JSON del trimestre di riferimento partendo
  dal foglio della fase 0 e verifica che il report prodotto sia identico a
  quello della fase 1."
- **Verifiche automatiche**: un difetto per regola dello schema e per
  controllo; checksum identico dopo un fermo; catena con Excel su due cicli.
- **Validazione umana**: nessuna nuova (il report deve essere uguale a quello
  gia' approvato).
- **Cancello**: il report prodotto dal JSON coincide con quello della fase 1.

### Fase 3 — L'agente A1 contro il metro

- **Obiettivo**: misurare quanto l'agente valuta come la Banca, e migliorarlo.
- **Da produrre**: rubrica completa con i descrittori della Banca, prompt A1
  composto (`componi_prompt.py`, limite 8.000), agente in Agent Builder con
  la knowledge del trimestre di riferimento (fonti interne di quel periodo),
  `confronta.py` esteso al confronto **agente contro valutazione umana**.
- **Prompt**: "Fase 3: applica PROMPT (solo A1), rubrica completa da
  DECISIONI.md. Prepara il pacchetto di configurazione di A1 in Agent Builder
  e un protocollo di prova: due run sullo stesso input, confronto fra i run e
  con la valutazione di riferimento, report delle differenze per rischio e
  dimensione."
- **Verifiche**: prompt sotto il limite; i due run dell'agente reale passano lo
  schema e i controlli della fase 2.
- **Validazione umana**: la funzione di rischio legge le differenze. Soglia
  suggerita (da fissare in `DECISIONI.md`): nessuna dimensione lontana piu' di
  un punto dalla valutazione umana, almeno l'80% identiche, motivazioni
  riconosciute come corrette. Se non basta: si cambiano i descrittori o si
  separa A1 in "Evidenze" + "Punteggi" (alternativa B parziale) e si ripete.
- **Cancello**: soglia raggiunta su **due** trimestri di riferimento (per non
  adattare la rubrica a un solo caso).

### Fase 4 — A5, controlli completi e validazione umana

- **Obiettivo**: il ciclo trimestrale completo e governato.
- **Da produrre**: A5 (C1-C9) e controlli meccanizzati completi; foglio o
  file di Validazione, comando `valida` con le regole delle rettifiche, blocco
  del ciclo successivo, Excel validato; il PowerPoint della fase 1 include
  ora le rettifiche del validatore.
- **Prompt**: "Fase 4: applica A5, controlli_a5 completi, la parte
  validazione della mappa e del comando valida, principio 7. Aggiungi al
  collaudo i difetti per controllo, le decisioni non valide rifiutate in
  blocco e le prove di mutazione."
- **Verifiche**: tutte le precedenti + mutazioni intercettate.
- **Validazione umana**: il validatore designato valida **davvero** il
  trimestre di riferimento prodotto dall'agente. Le sue rettifiche sono il
  **primo nucleo della base dati per l'apprendimento**: si guardano insieme per
  capire dove l'agente sbaglia.
- **Cancello**: il validatore dice che il foglio di validazione e' usabile
  (tempo impiegato annotato; se troppo, si rivede il formato).

### Fase 5 — Azioni e KRI

- **Obiettivo**: il ciclo completo come oggi (azioni, tre KRI per rischio,
  rilettura, storico e viste dei KRI).
- **Prompt**: "Fase 5: estendi schema, mappa, scrittura e report con azioni e
  KRI come da specifica (KRI storico in coda, KRI_Correnti, Andamento_KRI,
  rilettura per id, KRI nuovi per progressivo)."
- **Validazione umana**: le funzioni proprietarie dei dati (antifrode, ICT,
  compliance...) confermano che i KRI proposti sono misurabili e dove stanno
  i dati; si fissano le soglie in `DECISIONI.md`.
- **Cancello**: due cicli di prova consecutivi con rilettura corretta.

### Fase 6 — Il ciclo settimanale

- **Obiettivo**: notizie, badge e aree non presidiate.
- **Da produrre**: `fonti.md` validato dalla funzione di rischio (feed provati
  dal vivo), raccolta W0, A3 con codice fonte, NewsLog, badge, Analisi_News a
  barre, validazione delle notizie.
- **Prova in ombra**: 4 settimane in parallelo al lavoro attuale; l'analista
  annota le notizie che avrebbe segnalato lui.
- **Validazione umana**: confronto fra le notizie di A3 e quelle
  dell'analista; utilita' dei badge per la funzione di rischio.
- **Cancello**: nessuna notizia importante persa nelle 4 settimane, rumore
  accettabile.

### Fase 7 — Urgenza (Mosca) e magnitudo

- **Obiettivo**: il Radar_Mosca, con i parametri decisi dalla Banca.
- **Da produrre**: sezione 8 della rubrica, parametri in Parametri, vista e
  grafico, pagina del report per il comitato.
- **Validazione umana**: la funzione di rischio verifica che l'ordinamento per
  urgenza sul trimestre di riferimento abbia senso ("chi e' dentro la linea di
  Mosca e' davvero il piu' urgente?"); fissa Z per Prossimita, X, Y di riserva.
- **Cancello**: parametri approvati in `DECISIONI.md`.

### Fase 8 — Completamento ed esercizio in parallelo

- **Da produrre**: A4, guida passo passo, governance, SharePoint e workflow,
  demo, HANDOFF, TODO.
- **Esercizio in parallelo**: un trimestre intero con il sistema accanto al
  processo attuale.
- **Cancello finale**: model risk e compliance danno il via; il comitato
  riceve il primo report prodotto dal sistema.

## 5.4 Riepilogo dei cancelli

| Fase | Chi dice si' | Su cosa |
|---|---|---|
| 0 | funzione di rischio | il trimestre di riferimento e' la valutazione vera |
| 1 | funzione di rischio (e un membro del comitato) | forma e contenuto del report |
| 2 | automatico | il JSON riproduce il report approvato |
| 3 | funzione di rischio | l'agente valuta come la Banca, su due trimestri |
| 4 | validatore | la validazione e' praticabile; prime rettifiche analizzate |
| 5 | funzioni proprietarie dei dati | KRI misurabili, soglie decise |
| 6 | analista e funzione di rischio | 4 settimane in ombra senza perdite importanti |
| 7 | funzione di rischio | parametri dell'urgenza |
| 8 | model risk, compliance, comitato | via all'esercizio |

## 5.5 Se si sceglie R2 (Copilot Studio)

| Fase | Cosa cambia |
|---|---|
| 1 | dati in Liste SharePoint invece che in `NFR_Rischi.xlsx`; report Excel con Power Query (o Power BI) collegato alle liste; il PowerPoint lo genera un'azione di flusso o resta lo script |
| 2 | la scrittura e' uno strumento "controlla e scrivi" dell'agente operativo (flusso + Office Script per i controlli); lo schema e i controlli restano collaudati in Python come contratto |
| 3 | A1 diventa un sotto-agente; si puo' separare subito in "Evidenze" + "Punteggi" senza passi manuali in piu' |
| 4 | la validazione sta nelle liste (stato, motivazione, cronologia); le approvazioni in Teams |
| 6 | la raccolta W0 e' un flusso pianificato |
| 8 | ambienti di sviluppo e produzione, soluzioni, DLP e stima dei crediti fanno parte del cancello finale |

## 5.6 Stima dei tempi (una persona con Claude Code, piu' il tempo delle persone della Banca)

| Fase | Costruzione | Attesa per le validazioni umane |
|---|---|---|
| 0 | 0,5 giorni | dipende dalla disponibilita' del trimestre di riferimento |
| 1 | 2-3 giorni | 1 riunione |
| 2 | 2 giorni | — |
| 3 | 2-3 giorni + configurazione dell'agente | 1-2 riunioni, possibili iterazioni sulla rubrica |
| 4 | 2 giorni | 1 validazione reale |
| 5 | 2 giorni | 1 giro con le funzioni proprietarie |
| 6 | 3 giorni | 4 settimane in ombra |
| 7 | 1 giorno | 1 riunione |
| 8 | 3 giorni | un trimestre in parallelo |
