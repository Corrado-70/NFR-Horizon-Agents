# 17. Il "decimo uomo": un contraddittorio sulla valutazione di A1

Data: 19/10/2026. Richieste dell'utente:

> ho notato che i controlli di A5 sono molto relativi alla solità dei numeri dati. Avrebbe senso che spianga anche a
> fare da "10 uomo" e valutare altri rischi o prospettive diverse sui dati che fanno emergere (o ridurre) i vari rischi
> identificati?

> fai un'analisi con le 2 opzioni

Le due opzioni sono:
1. **un agente nuovo e separato**, A9 Contraddittore;
2. **il contraddittorio fatto da A1 stesso**, nella stessa valutazione o con un secondo messaggio nella stessa chat.

L'idea di metterlo dentro A5 e' scartata in 17.1: cambierebbe la natura di A5 e le sue istruzioni sono gia' al limite.

## 17.0 In breve

1. **La domanda e' giusta.** Oggi nessun componente chiede "e se A1 avesse torto?". Le regole spingono tutte nella
   stessa direzione: niente cambia senza evidenza nuova, al massimo un punto per ciclo, conferma di default.
   - Questo protegge dall'inflazione dei punteggi, ma favorisce lo status quo e la conferma di cio' che si e' gia'
     scritto.
   - A5 controlla la coerenza dell'output di A1, non la sua completezza ne' le letture alternative (17.1).
2. **Il "decimo uomo"** e' la regola per cui, quando tutti concordano, qualcuno ha il compito di sostenere la tesi
   opposta. Qui avrebbe quattro compiti (17.2):
   - la tesi opposta sui rischi principali, sia "sopravvalutato" sia "sottovalutato";
   - i rischi mancanti;
   - le ipotesi da cui dipende la valutazione;
   - i rischi che si combinano.

   Non propone numeri, e ogni tesi cita una fonte o si dichiara ipotesi.
3. **Opzione 1, agente separato A9** (17.3).
   - Pro:
     - fa una ricerca sua nei documenti, diversa da quella di A1;
     - non e' legato alla risposta che ha appena dato;
     - non tocca A1 ne' A5.
   - Contro: un agente in piu' da configurare e da lanciare, e una versione nuova del template.
4. **Opzione 2, contraddittorio dentro A1** (17.4).
   - Pro: costa meno e non serve un agente nuovo.
   - Contro:
     - un modello che rilegge la propria valutazione tende a confermarla (lo abbiamo gia' visto, D-69);
     - cerca negli stessi documenti con la stessa ricerca, quindi ha gli stessi punti ciechi;
     - allunga una risposta di A1 che e' gia' la piu' lunga del sistema.
5. **Raccomandazione** (17.9): opzione 1, a due tappe.
   - Prima una **prova senza codice** sul primo ciclo vero 2026Q4 (prova K15): A9 in Agent Builder, il validatore
     giudica l'utilita' di ogni tesi.
   - Poi, se la prova e' utile, l'integrazione nello script.
   - Decisione proposta: **A-17**.
6. **Ancoraggio e asimmetrie** (17.10, aggiunta del 19/10): perche' i rischi nuovi entrano con Probabilita 3 o meno e
   perche' i rischi oltre i 3 anni non risultano mai urgenti; sei rimedi. Fatti i primi due (**D-80**): il comando
   `diagnosi` e gli anni di adeguamento dei rischi in osservazione con Impatto 4-5. Poi il terzo (**D-81**), nella
   variante leggera: l'esposizione "non nota" scritta da A1 va in validazione e decide il validatore.

## 17.1 Che cosa fa oggi A5, e che cosa manca

A5 risponde a una domanda sola: **l'output di A1 e' fondato su cio' che A1 stesso cita?**
- Nove controlli (C1-C9): completezza, variazioni, evidenza, plausibilita', fonti, deriva, KRI, azioni.
- Per scelta **non usa la knowledge** (D-09): giudica solo cio' che A1 cita, e per questo e' indipendente da A1.

Restano scoperte tre domande:

| Domanda | Chi la copre oggi | Limite |
|---|---|---|
| A1 ha **mancato** un rischio? | A1 stesso, con i "fenomeni considerati e non censiti"; il validatore; A3 con le aree non presidiate | A1 si giudica da solo; il validatore vede solo cio' che A1 ha scritto; A3 guarda una settimana di notizie |
| Gli stessi documenti si possono **leggere in un altro modo**? | nessuno | C4 (A5) chiede se il punteggio corrisponde al descrittore, dato il razionale di A1, non se il razionale e' l'unica lettura |
| La valutazione regge se cambia un'**ipotesi**, o se due rischi si attivano insieme? | nessuno; P5 (rischi collegati, TODO) registrerebbe i collegamenti, non li mette in discussione | nessuno scenario avverso e' chiesto a nessun agente |

**Perche' non dentro A5.**
- A5 dovrebbe leggere la knowledge, quindi D-09 cadrebbe e A5 non sarebbe piu' indipendente da cio' che cerca.
- Il suo prompt e' a 7.990 caratteri su 8.000: per fare spazio andrebbero tagliati i controlli.
- Mescolare "i numeri sono fondati?" e "e se fosse il contrario?" renderebbe meno chiaro al validatore da dove viene
  ogni rilievo.

**Un rischio del sistema che oggi non e' scritto.** In `controlli_e_model_risk.md` (sezione 4) ci sono l'inflazione
progressiva e la deriva mediatica, cioe' le spinte verso l'alto. Manca la spinta opposta:
- **ancoraggio alla valutazione precedente**: la regola di conferma di default, il limite di un punto e A1 che si
  rilegge favoriscono la continuita';
- **visione unica**: un solo agente cerca e un solo agente controlla cio' che il primo ha trovato.

Il decimo uomo e' il presidio di questo rischio. Va aggiunto alla tabella in ogni caso.

## 17.2 Che cosa vuol dire "decimo uomo" in questo sistema

Il contraddittorio ha quattro compiti, gli stessi nelle due opzioni:

1. **La tesi opposta sui rischi principali.** Per i rischi che contano (i primi N per score, quelli AGIRE ORA e quelli
   in Attivazione) costruisce:
   - l'argomento piu' forte per cui il rischio e' **sopravvalutato**;
   - l'argomento piu' forte per cui e' **sottovalutato**.

   Per ognuno indica la dimensione e il descrittore della rubrica messi in discussione e il documento su cui si basa.
   Tenere entrambi i versi e' cio' che lo distingue da un generatore di allarmi.
2. **I rischi mancanti.** Al massimo tre fenomeni che A1 non ha censito o ha scartato, ciascuno con:
   - il meccanismo di perdita per la Banca;
   - la categoria;
   - la fonte;
   - il motivo per cui la valutazione di A1 non l'ha visto.

   Li confronta con i "fenomeni considerati e non censiti" di A1. Uno scarto gia' motivato si discute, non si ripete.
3. **Le ipotesi da cui dipende la valutazione.** Per i rischi principali, che cosa deve restare vero perche' i valori
   reggano e quale segnale osservabile lo smentirebbe. Esempi:
   - "il fornitore resta sostituibile in 12 mesi";
   - "nessuna banca italiana ha ancora subito il caso".
4. **I rischi che si combinano.** Un evento che attiva piu' rischi insieme (cascata, concentrazione, causa comune):
   quali rischi e con quale effetto.

Le regole che lo tengono utile:
- **nessun numero**: non propone score, probabilita' o perdite; mette in discussione un descrittore;
- **ogni tesi ha una fonte datata** entro la data di riferimento, **oppure si dichiara "ipotesi senza evidenza"**;
- **un tetto**: al massimo due tesi per rischio e un totale per ciclo (proposta: 12 tesi, 3 rischi mancanti, 3
  combinazioni). Oltre, il validatore non le legge;
- **non decide nulla**: le tesi sono materiale per il validatore e, per i rischi mancanti, per A1 al ciclo dopo.

## 17.3 Opzione 1: un agente separato, A9 Contraddittore

**Quando.**
- Dopo A1 (e dopo il precontrollo, se si usa), prima di `trimestrale`, accanto ad A5 e indipendente da lui.
  Facoltativo come A5 (D-71).
- Si puo' usare anche nello straordinario, sull'output di A8.

**Che cosa riceve.**
- In chat: `A1_<ciclo>.json` e `Input_A1_<ciclo>.txt`, che contiene gia' la baseline.
- **La knowledge di A1**: Analisi_Interne, Analisi_Esterne, News_Inbox, i siti. E' la differenza con A5.
- Il prompt gli chiede di **cercare prima per conto suo** (quali temi e quali documenti ci sono per ogni categoria) e
  solo dopo di confrontare con l'output di A1. L'ordine serve a non farsi ancorare alla risposta di A1.

**Che cosa restituisce.** Un JSON con lo schema nuovo `schema_output_A9.json`:

| Campo | Contenuto |
|---|---|
| `tesi[]` | `id_rischio`, verso (Sopravvalutato / Sottovalutato), dimensione, argomento (fino a 600 caratteri), fonti (riferimento, data, tipo) oppure `ipotesi_senza_evidenza: true`, segnale che permetterebbe di verificarla |
| `ipotesi_critiche[]` | `id_rischio`, ipotesi, segnale che la smentirebbe |
| `rischi_mancanti[]` | nome, categoria, meccanismo di perdita, fonti, perche' non e' nella valutazione |
| `combinazioni[]` | rischi coinvolti, evento comune, effetto |
| `sintesi` | fino a 600 caratteri, per il Quadro |

Lo schema **non ha campi numerici** per i punteggi.

**Che cosa fa lo script.** Comando `trimestrale --contraddittore A9_<ciclo>.json`, come `--challenger` per A5:
- **controlla**:
  - lo schema;
  - che i rischi citati siano nella baseline o nell'output di A1;
  - le date delle fonti;
  - i tetti;
  - che nel testo non ci sia un valore proposto (es. "Probabilita 5"), con lo stesso tipo di regola che ferma i
    numeri di A6.

  Un difetto **non ferma il ciclo**: le tesi difettose sono scartate e la scelta e' annunciata a video;
- **scrive**:
  - le tesi e le ipotesi critiche nella **colonna Segnalazioni** della griglia, sul rischio a cui si riferiscono, come
    `Osservazione · DU · A9: ...`. Il validatore le legge, ma la Motivazione resta obbligatoria solo per le ⚑ di oggi;
  - rischi mancanti, combinazioni e sintesi in una colonna nuova di **Sintesi_Cicli** ("Contraddittorio") e in una
    riga nuova di pagina 2 del **Quadro**, "Prospettive alternative (A9)", sotto i controlli. Il comitato vede che c'e'
    stato un contraddittorio e su che cosa;
  - lo stesso testo nella knowledge di A7 (`Ciclo.txt`), cosi' A7 puo' rispondere a "che cosa ha obiettato il
    contraddittore?";
- **chiude il giro.** I rischi mancanti diventano **temi da verificare** per A1 al ciclo dopo. E' la voce P9 del TODO:
  A1 deve rispondere su ognuno, censendolo come rischio (anche in osservazione) oppure motivando come fenomeno non
  censito, e lo script segnala un tema senza risposta. Senza P9, restano in Sintesi_Cicli e l'analista li passa ad A1
  con il messaggio "tema da verificare" (guida, sezione 8).

**Istruzioni dell'agente.**
- Il modello e' `02_Agenti/modelli/A9.md`, composto con le sezioni 1-2 della rubrica (descrittori e rilevanza delle
  fonti) e con la tassonomia.
- La dimensione e' quella di A5, entro il limite di 8.000 caratteri. Se non basta, le regole di dettaglio vanno in un
  allegato, come per A1 (D-69).

**Nelle strade di automazione (A-15).** E' un agente in piu' in tutte e tre:
- **strada A**: un passo in piu' nella procedura;
- **CS-1 e CS-2**: un sotto-agente in piu' dell'Operatore.

Lo schema e i controlli stanno nel codice comune, quindi valgono ovunque.

## 17.4 Opzione 2: il contraddittorio dentro A1

Due varianti.

**2a. Nella stessa risposta.**
- Il JSON di A1 ha un campo nuovo `contraddittorio`, con la stessa struttura della tabella in 17.3.
- Le istruzioni vanno nella **guida di scrittura dell'allegato** (`guida_scrittura_A1.md`), non nel prompt: il prompt
  di A1 e' a 7.980 caratteri, e l'allegato non ha limite (D-69).
- Lo script scrive il campo come nell'opzione 1.

**2b. Con un secondo messaggio nella stessa chat.**
- Dopo il JSON, l'analista scrive "Ora fai da decimo uomo sulla valutazione che hai appena dato" e salva la risposta
  in un file a parte.
- Nessuna modifica allo schema di A1.
- Lo script legge il file come il JSON di A9 dell'opzione 1, oppure il validatore lo legge e basta.

**Pro.**
- Nessun agente nuovo da configurare, caricare e mantenere.
- Nessun passo in piu' per l'analista (2a), o un solo messaggio in piu' (2b).
- A1 ha appena letto i documenti: non serve una seconda ricerca.

**Contro.**
- **Si conferma da solo.** Lo abbiamo osservato con D-69: un modello che rilegge il proprio output tende a
  confermarlo. Per questo la verifica affidabile e' rimasta allo script e ad A5. Un contraddittorio scritto da chi ha
  appena deciso parte dalle stesse conclusioni.
- **Stessi punti ciechi.** La ricerca di Agent Builder recupera solo una parte della knowledge (rischio "retrieval
  incompleto" in `controlli_e_model_risk.md`). Se A1 non ha trovato un documento, la sua seconda passata non lo
  trovera'. Il valore principale del decimo uomo, cercare altrove, si perde.
- **Risposta piu' lunga.** L'output di A1 e' gia' il piu' lungo del sistema: tutti i rischi del radar, razionale in
  parti, azioni, KRI. Aggiungere il contraddittorio nella stessa risposta (2a) aumenta il rischio di risposte tagliate
  o meno curate proprio sulla valutazione principale.
- **Lo schema di A1 cambia (2a)**, e con lui il precontrollo, il kit di Copilot Studio (script della skill
  rigenerato) e il collaudo.
- **Traccia debole (2b)**: se l'analista non salva il secondo messaggio, il contraddittorio resta solo nella chat.

## 17.5 Confronto

| Criterio | Opzione 1: A9 separato | Opzione 2: dentro A1 |
|---|---|---|
| Indipendenza dalla valutazione | alta: non l'ha scritta lui e cerca prima per conto suo | bassa: e' l'autore che si contesta |
| Ricerca nei documenti | una seconda ricerca, con domande diverse | la stessa ricerca, gli stessi punti ciechi |
| Rischio di contraddittorio di maniera | medio (tesi forzate per dovere) | alto (obiezioni deboli, gia' "risolte" dalla risposta) |
| Effetto su A1 | nessuno | risposta piu' lunga (2a) o un messaggio in piu' (2b) |
| Lavoro per ciclo | un agente in piu' da lanciare (10-15 minuti) e piu' righe da leggere in validazione | un messaggio in piu' (2b) o nessuno (2a), stesse righe da leggere |
| Modifiche al pacchetto | prompt e schema nuovi, opzione di `trimestrale`, colonna in Sintesi_Cicli, riga del Quadro, versione del template, collaudo | campo nuovo nello schema di A1 (2a), precontrollo e kit, stesse modifiche a registro e Quadro |
| Limite di 8.000 caratteri | prompt nuovo, nei limiti come A5 | istruzioni nell'allegato, nessun problema |
| Tracciabilita' | alta: file A9 archiviato con il ciclo | alta in 2a, debole in 2b |
| Strade di automazione | un sotto-agente in piu' | nessun sotto-agente in piu' |
| Stima | circa 3-4 giorni (17.8) | circa 1,5-2 giorni |

## 17.6 Rischi e contromisure

| Rischio | Meccanismo | Contromisura |
|---|---|---|
| Contraddittorio di maniera | il contraddittore produce tesi deboli perche' deve produrne | tetto di tesi; ogni tesi con fonte o etichetta "ipotesi"; giudizio di utilita' nella prova K15; se dopo due cicli le tesi utili sono poche, si spegne (e' facoltativo) |
| Rumore per il validatore | troppe righe nella colonna Segnalazioni | Osservazione, non ⚑: nessuna Motivazione obbligatoria; tetto per ciclo; tesi solo sui rischi principali |
| Pressione verso l'alto | si leggono solo le tesi "sottovalutato" | ogni rischio scelto ha entrambi i versi; il Quadro dice quante tesi per verso |
| Ancoraggio all'output di A1 (opzione 1) | A9 legge A1 e ne segue la cornice | prima la ricerca autonoma, poi il confronto (ordine nel prompt); i rischi mancanti obbligano a uscire dalla cornice |
| Numeri dalla porta di servizio | una tesi suggerisce un valore ("dovrebbe essere 5") | schema senza campi numerici; lo script scarta le tesi con un valore proposto |
| Nuova fonte di errore | una tesi cita un documento che non dice cio' che afferma | il validatore verifica prima di rettificare; le tesi non cambiano nulla da sole |
| Validazione non indipendente (D-13) | chi lancia gli agenti valida anche le proposte | il contraddittorio non risolve D-13, ma da' al validatore una lettura avversa strutturata: un aiuto, non un secondo validatore |

## 17.7 Effetti su kernel, script, registro, collaudo e documenti

| Dove | Opzione 1 | Opzione 2 |
|---|---|---|
| Kernel | `schema_output_A9.json`; nessun cambio di rubrica o tassonomia | campo `contraddittorio` in `schema_output_A1.json` (2a); istruzioni in `guida_scrittura_A1.md` |
| Agenti | `modelli/A9.md`, `componi_prompt.py` (un agente in piu'), `COMMENTATI` | nessun prompt nuovo; allegato di A1 piu' lungo |
| Script | `--contraddittore` di `trimestrale` (e dello straordinario); controlli; scrittura in Segnalazioni, Sintesi_Cicli, Quadro, knowledge di A7; con P9, i rischi mancanti nei temi da verificare | lettura del campo dall'output di A1 (2a) o del file a parte (2b); il resto uguale |
| Registro | una colonna in Sintesi_Cicli, una riga nel Quadro: **versione nuova del template** e `aggiorna-registro` | uguale |
| Copilot Studio | un sotto-agente in piu' nella prova K6 e successive | il kit della skill (schema di A1) va rigenerato |
| Collaudo | dati di prova `run_A9_<ciclo>.json`; test dello schema, dei tetti, delle tesi con numeri; catena con `--contraddittore` | test del campo nuovo in precontrollo e catena |
| Documenti | guida (sezioni 2 e 8), README di Agent Builder, `00_LEGGIMI`, `controlli_e_model_risk.md` (controllo nuovo e rischio dell'ancoraggio), DECISIONI, PROMPT_MASTER, demo, presentazione | uguale, senza l'agente |

## 17.8 Percorso a tappe, prova K15 e stima

**Tappa 1: prova K15, senza codice** (consigliata in ogni caso, circa mezza giornata di preparazione).
- Si crea A9 in Agent Builder con le istruzioni in bozza e la stessa knowledge di A1.
- Sul primo ciclo vero (2026Q4) si lancia A9 dopo A1 e si salva la risposta.
- Il validatore segna, tesi per tesi:
  - **utile**: ha portato a una rettifica, a un tema per il ciclo dopo o a una domanda all'owner;
  - **gia' nota**;
  - **rumore**.
- Per confronto si fa anche la variante 2b nella chat di A1: e' un messaggio in piu' e mostra sul caso reale se
  l'autocontraddittorio aggiunge qualcosa.
- Criterio proposto per proseguire: almeno un terzo delle tesi utili e almeno un rischio mancante o una rettifica che
  il ciclo non avrebbe avuto.

**Tappa 2: integrazione**, solo se K15 va bene.

| Lavoro | Opzione 1 | Opzione 2 |
|---|---|---|
| Prompt o istruzioni, schema | 1 giorno | 0,5 |
| Script (opzione, controlli, scrittura) | 1 | 0,5-1 |
| Template (Sintesi_Cicli, Quadro), aggiorna-registro | 0,5 | 0,5 |
| Collaudo, demo, documenti | 1-1,5 | 0,5 |
| **Totale** | **circa 3-4 giorni** | **circa 1,5-2,5 giorni** |

Nel piano del TODO si collocherebbe dopo P4 e P9: P9 serve a chiudere il giro dei rischi mancanti, quindi conviene
farla prima o insieme.

## 17.9 Raccomandazione e decisione da prendere

**Raccomandazione: opzione 1, agente separato A9, a due tappe.**
- Prima la prova K15 sul ciclo 2026Q4, senza codice.
- Poi l'integrazione, se la prova dice che le tesi servono.
- A5 resta com'e'.

Le ragioni:
- il valore del decimo uomo sta nel **guardare altrove e da un altro punto di vista**: un agente separato con una sua
  ricerca lo da', A1 che si rilegge no (D-69);
- non tocca la valutazione principale di A1, che resta il pezzo piu' delicato del ciclo;
- e' facoltativo e si spegne senza conseguenze se non rende;
- la prova costa poco e si fa sul ciclo vero, dove il valore si misura sui documenti reali e non su dati di demo.

L'opzione 2 resta valida se si vuole il minimo costo: in quel caso **2b** come prova (un messaggio in piu', nessuna
modifica) e **2a** solo se la prova mostra obiezioni non banali.

**Decisione proposta, A-17**: "Contraddittorio facoltativo sulla valutazione trimestrale (decimo uomo): agente separato
A9, senza numeri, con tesi in entrambi i versi, rischi mancanti, ipotesi critiche e combinazioni. Le tesi vanno in
validazione come Osservazioni, i rischi mancanti diventano temi da verificare per A1". Si chiude dopo la prova K15.

In ogni caso, subito e senza costi: aggiungere a `controlli_e_model_risk.md` (sezione 4) il rischio **"Ancoraggio alla
valutazione precedente"**, con il presidio che si decidera'.

Non cambia:
- nessun agente modifica score: il contraddittorio e' materiale per il validatore (D-10, D-41);
- A5 e i suoi nove controlli;
- la regola del punto, la conferma di default, la validazione umana obbligatoria.

## 17.10 Ancoraggio e asimmetrie della valutazione (19/10/2026)

Richieste dell'utente, dopo la spiegazione del rischio "ancoraggio":

> Ho anche notato che le valutazioni nuove tendono a essere massimo a 3 di probabilità e  forse taglia i rischi oltre 3
> anni anche se esistenti

> metti nell'analisi, nella todo e procedi con 1 e 2. Poi dimmi cosa costa il punto 3

### L'ancoraggio, meccanismo per meccanismo

Il primo numero diventa il riferimento e le correzioni successive restano piccole. Qui non e' solo una tendenza
dell'agente: lo incorporano regole nate, con buone ragioni, contro l'inflazione dei punteggi.

| Meccanismo | Regola | Effetto collaterale |
|---|---|---|
| Il valore resta senza evidenza nuova | rubrica, regola 1 | un valore sbagliato all'ingresso resta finche' non arriva un documento nuovo |
| Al massimo un punto per ciclo | regola 2, C3 | un rischio entrato a 2 che merita 5 ci mette tre trimestri; anche lo straordinario sale di un punto |
| A1 parte dai valori di prima | baseline con numeri e razionale | A1 vede il numero prima delle fonti e tende a confermarlo |
| Rischi in osservazione rivalutati solo con evidenza nuova | guida di scrittura | se A1 non trova la notizia giusta, il rischio resta fermo per cicli |
| Accettare non costa niente | griglia di validazione | la proposta diventa il valore validato per inerzia |

### Perche' i rischi nuovi entrano con Probabilita 3 o meno

- I descrittori di 4 e 5 chiedono un fenomeno gia' osservato ("casi ripetuti in aziende strutturate o banche", "gia'
  osservato presso istituzioni finanziarie"). Un rischio emergente non ha ancora una storia: 3 ("casi in altri settori")
  e' il tetto naturale.
- 4 e 5 valgono solo "se la Banca e' esposta" (D-65), ma A1 non conosce l'esposizione interna (D-49): nel dubbio non la
  afferma.
- Per 5 serve una fonte di rilevanza alta (C5); per un rischio nuovo spesso c'e' solo un report di settore (media).
- Dopo il primo ciclo reale del 29/09 le regole sono state strette contro i 4-5 su evidenza generica (D-48).

Con l'ancoraggio, un rischio emergente entra a 3 e sale di un punto al trimestre: in ritardo proprio dove lo Horizon
Scan dovrebbe anticipare. Nella demo (output di A1 simulati seguendo le regole) i 7 rischi nuovi sono entrati tutti con
Probabilita da 1 a 3.

### Perche' i rischi oltre i 3 anni restano fuori

- La Prossimita si ferma a "oltre 3 anni": 3 anni e 30 anni valgono 1, con Z = 3,5.
- La regola del radar vuole Prossimita almeno 2: un rischio lontano e' in osservazione anche con Impatto 5.
- Un rischio AGIRE ORA entra sempre nel radar, ma per i rischi in osservazione la guida di A1 non chiedeva gli anni di
  adeguamento: il margine usava la Y di riserva (1 anno). NFR-13 (crittografia post-quantistica, Impatto 5,
  Prossimita 1) ha margine 2,25 e resta fuori: e' proprio il caso per cui Mosca ha scritto la disuguaglianza.
- I rischi lontani non sono scartati: entrano in osservazione, e sono scartati solo oltre i 20.

### Rimedi

| # | Rimedio | Costo | Stato |
|---|---|---|---|
| 1 | **Misurare**: comando `diagnosi` (valori all'ingresso dei rischi nuovi, verso delle rettifiche del validatore, rischi lontani con il margine) | mezza giornata | **fatto, D-80** |
| 2 | **Anni di adeguamento dei rischi in osservazione con Impatto 4-5** (guida di scrittura di A1): con X + Y > Z il rischio e' AGIRE ORA ed entra nel radar | poche ore: il codice li usava gia' | **fatto, D-80** |
| 3 | **Esposizione "non nota"** al posto di un 3 per prudenza: decide il validatore | sotto | **fatta la variante 3a, D-81**; la 3b resta |
| 4 | **Salto di piu' di un punto** in validazione con evidenza di rilevanza alta datata nel ciclo | circa 1 giorno | da decidere: tocca la regola 2 della rubrica |
| 5 | **Contraddittorio**, tesi "sottovalutato" (17.3) | 17.8 | A-17 |
| 6 | **Taratura** dei descrittori di Probabilita con la Banca | lavoro della Banca | A-12 |

**Che cosa e' stato fatto (D-80).**
- `07_Senza_Studio/diagnosi.py` e il comando `python esegui_ciclo_locale.py diagnosi`, solo lettura, con il rapporto in
  `Cicli/<ciclo>/Diagnosi_valutazioni_<ciclo>.txt`. Sul registro della demo: 7 rischi nuovi su 7 con Probabilita 3 o
  meno; rettifiche della Probabilita 1 in su (in riapertura) e 1 in giu'; NFR-13 e NFR-14 lontani senza anni di
  adeguamento, margine 2,25.
- Guida di scrittura di A1 (allegato `Input_A1`, nessun prompt da reincollare): per i rischi in osservazione con
  Impatto 4-5, gli anni di adeguamento quando la difesa richiede un adeguamento strutturale pluriennale, anche
  riscrivendo un rischio della baseline che non li ha; se X + Y > Z, anche KRI e azioni, perche' il rischio entra nel
  radar. Il codice li usava gia' (margine della regola, baseline, ingresso nel radar).
- `controlli_e_model_risk.md`: rischi "Ancoraggio alla valutazione precedente" e "Rischio lontano mai urgente".
- Collaudo: verifiche della diagnosi su righe finte e dell'istruzione nell'allegato.
- La demo non e' rigenerata: i suoi output di A1 sono dell'08/10, prima della regola nuova. Il primo ciclo che la usa e'
  il 2026Q4 in Banca; dopo la sua validazione conviene lanciare `diagnosi`.

### Il punto 3: esposizione "non nota", due varianti e costo

Oggi A1 deve scegliere fra "esposta" e "poco esposta" senza sapere com'e' fatta la Banca, e sceglie prudente. L'idea e'
che lo dica ("non nota") e che decida il validatore, che l'esposizione la conosce o la puo' chiedere all'owner.

**3a. Leggera: una nota nel razionale e una segnalazione in validazione.**
- Quando l'esposizione della Banca non e' documentata nelle fonti, A1 scrive nella parte PROBABILITA del razionale
  "ESPOSIZIONE NON NOTA: con l'esposizione documentata sarebbe N", dove N e' il valore che darebbe senza il freno.
- Un controllo meccanizzato legge la nota, come gia' legge le parti del razionale, e la porta nella colonna Segnalazioni
  della griglia come "Da motivare": il validatore vede i due valori e sceglie. Per un rischio nuovo puo' dare qualunque
  valore; per uno esistente vale il limite di un punto, salvo `riapri`.
- Tocca: guida di scrittura, `controlli_a5.py` e precontrollo (con il kit di Copilot Studio da rigenerare), collaudo,
  guida e documenti. Nessuno schema, nessun prompt, nessuna versione nuova del template.
- **Costo: circa 1-1,5 giorni.**
- Limite: l'esposizione decisa non resta registrata; al ciclo dopo A1 non la conosce e la nota si ripete.

**3b. Completa: l'esposizione come dato dell'anagrafica.**
- Campo `esposizione` (Documentata, Non nota) nell'output di A1 e di A8, con la Probabilita "se esposta".
- Colonna Esposizione nell'anagrafica di Parametri, decisa dal validatore come il presidio dei controlli (D-49): resta da
  un ciclo all'altro, arriva ad A1 nella baseline, si vede nel Registro, nelle schede e nella knowledge di A7.
- Regola della rubrica: Probabilita 4-5 con esposizione documentata nelle fonti o decisa dal validatore.
- Tocca: schema di A1 e documentazione dei campi, mappa, generatore (anagrafica, Registro, Dizionario, Metodologia),
  **versione nuova del template** e `aggiorna-registro`, scrittura, baseline, griglia di validazione, controlli e
  precontrollo (kit), schede, spiegazioni di A7, rubrica, collaudo con dati di prova, demo rigenerata, guida,
  presentazione. I prompt di A1 (7.980 caratteri), A5 (7.990) e A8 (7.993) sono al limite: le istruzioni vanno
  nell'allegato e nei controlli, non nei prompt.
- **Costo: circa 3 giorni**, piu' `aggiorna-registro` in Banca (i prompt non cambiano).

**Raccomandazione.** Prima la diagnosi sul ciclo 2026Q4 vero. Se mostra rettifiche della Probabilita in su sui rischi
nuovi, fare la **3a**: costa poco e misura subito quante volte A1 si frena per mancanza di dati interni. Passare alla
**3b** solo se la nota si ripete ciclo dopo ciclo sugli stessi rischi, cioe' se serve davvero registrare l'esposizione.
Il rischio da tenere d'occhio e' l'inverso: un A1 che scrive sempre "non nota" con un valore alternativo alto. La
diagnosi lo vede (verso delle rettifiche) e la decisione resta comunque al validatore.

**Fatto il 19/10 (D-81), variante 3a.** L'utente: "procedi con il punto 3 [...] so gia' che il validatore ha alzato
spesso in Q4".
- Guida di scrittura di A1: se le fonti non dicono se la Banca e' esposta, il valore senza esposizione e la frase
  "ESPOSIZIONE NON NOTA: con l'esposizione documentata sarebbe N" nella parte PROBABILITA.
- `controlli_a5.py` (parte meccanizzata di C5; quindi anche precontrollo e skill di Copilot Studio, rigenerata): con
  N maggiore della proposta, segnalazione "Da motivare" con i due valori e, per un rischio gia' nel registro, il valore
  massimo ammesso in validazione; senza un valore leggibile, Osservazione sulla forma.
- `diagnosi`: sezione 4, le note del ciclo con la Probabilita validata e il valore "se esposta"; la lettura dice
  quante volte il validatore ha scelto il valore "se esposta".
- Nessuno schema, prompt o template cambiato; collaudo senza Excel con le verifiche nuove.
