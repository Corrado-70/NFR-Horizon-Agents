# 13. Scala unica per rischi e fenomeni in osservazione (TODO P10)

Data: 08/10/2026. Proposta dell'utente del 07/10: "un'unica scala per score in cui solo i primi N rischi entrano e
gli altri restano in osservazione. Un solo meccanismo uniforme, un solo criterio di valutazione e gestione".

Il documento confronta due opzioni e chiude con una raccomandazione e le scelte da fare. Non cambia niente nel
pacchetto: la decisione va poi in `04_Riferimenti/DECISIONI.md`.

## 13.1 Oggi: due meccanismi

| | Registro dei rischi | Lista di osservazione (D-73) |
|---|---|---|
| Codice | `NFR-nn`, fino a 20 (MAX_RISCHI) | `OSS-nn`, fino a 30 |
| Valutazione | Impatto, Probabilita, Prossimita, Velocity (rubrica, 1-5) e score composito | impatto potenziale 1-5 (descrittori della rubrica), orizzonte in anni, plausibilita' teorica / possibile / in crescita, segnale di avvicinamento |
| Gestione | due KRI, azioni, razionale in parti, radar, classifica, urgenza, schede, report | nessun KRI, nessuna azione; foglio Osservazione e pagina Fenomeni |
| Revisione di A1 | ogni rischio, ogni trimestre | solo le voci con evidenza nuova |
| Passaggio | — | A1 "promuove" una voce quando il suo segnale si verifica |
| Validazione | sezione Rischi della griglia | sezione Osservazione (impatto, orizzonte, plausibilita') |
| A3 | `rischio_collegato`, `flag_proposti` | `voce_osservazione`, `segnali_osservazione` |
| Peso nella risposta di A1 | circa 3,2 KB per rischio (misurato su `run3`) | circa 1 KB per voce |

I costi della separazione:
- due scale, quindi un rischio e un fenomeno non si confrontano;
- due codici;
- due sezioni della griglia, due sezioni dello schema di A1 e due canali di A3;
- un passaggio, la promozione, che dipende da un giudizio di A1 ("il segnale si e' verificato") e non da una
  regola.

## 13.2 Il nodo che decide: lo score da solo non separa il vicino dal lontano

Le quattro voci della demo, tradotte sulla scala della rubrica:
- Impatto = impatto potenziale;
- Probabilita da plausibilita': teorica = 1 (Remota), possibile = 2, in crescita = 3;
- Prossimita da orizzonte: oltre 3 anni = 1, 2-3 anni = 2;
- Velocity non valutata.

Score con i pesi D-50 (media pesata delle dimensioni valutate):

| Voce | Imp | Prob | Pross | Score | Confronto con il registro del 2026Q4 |
|---|---|---|---|---|---|
| OSS-01 Calcolo quantistico e crittografia dei pagamenti (teorica, 10 anni) | 5 | 1 | 1 | **2,75** | pari a NFR-08 (accessi impropri dei dipendenti, rischio di oggi) |
| OSS-02 Cavi sottomarini (possibile, 5 anni) | 4 | 2 | 1 | 2,63 | sotto l'ultimo rischio (2,75) |
| OSS-03 Agenti di IA autonomi (in crescita, 4 anni) | 3 | 3 | 1 | 2,50 | sotto |
| OSS-04 Vertenze nei ruoli IT (possibile, 3 anni) | 3 | 2 | 2 | 2,44 | sotto, ma e' la voce che poi diventa NFR-13 |

Cosa mostrano:
- **Il taglio ai "primi N" dipende tutto da N.** Con N = 20, la capienza di oggi, nel registro ci sono 13 rischi:
  entrerebbero tutte e quattro le voci, anche la "solo teorica a 10 anni". Con N = 13 non ne entrerebbe nessuna,
  nemmeno quella che il trimestre dopo e' diventata un rischio.
- **L'Impatto pesa 0,35**: un fenomeno remoto di Impatto 5 vale quanto un rischio presente di media gravita'.
  Ordinare solo per score mette insieme cio' che la lista era nata a separare (lontano o solo teorico contro
  valutabile oggi).
- **La posizione in classifica non e' stabile**: il rischio al posto N entra ed esce con un decimo di score. A ogni
  uscita perde la continuita' dei KRI e delle azioni.

Quindi la scala unica funziona se il criterio non e' solo "primi N per score", ma una **regola sulla stessa
scala** che dica quando un fenomeno e' abbastanza vicino e plausibile da essere gestito.

## 13.3 Opzione A — tenere la lista, sulla scala della rubrica

**Cosa cambia.** La lista resta un meccanismo a parte, ma parla la stessa lingua del registro:
- al posto della plausibilita', la **Probabilita** con i descrittori della rubrica;
- accanto all'orizzonte in anni, la **Prossimita** (1 oltre 3 anni);
- lo **score** della voce calcolato dal foglio con gli stessi pesi, mostrato nel foglio Osservazione e nella
  pagina Fenomeni, accanto all'ultimo rischio del registro;
- la promozione resta un giudizio di A1 ("il segnale si e' verificato"), con un'indicazione in piu': una voce con
  Prossimita >= 2 e Probabilita >= 2 va promossa o motivata.

Restano due codici, due sezioni della griglia, due canali di A3.

| Pro | Contro |
|---|---|
| un rischio e un fenomeno si confrontano sulla stessa scala | restano due meccanismi: l'obiettivo dell'utente non e' raggiunto |
| cambio piccolo (campi della voce, foglio, guida di scrittura) | la promozione resta un giudizio, non una regola |
| nessuna migrazione dei codici | |

Impegno: circa 1 giorno; struttura nuova del registro (colonne della tabella delle voci) e `aggiorna-registro`.

## 13.4 Opzione B — scala unica: un registro con due stati

**L'idea.** Un solo elenco di rischi `NFR-nn`, tutti valutati con la rubrica (quattro dimensioni, score). Ogni
rischio ha uno **stato**: **Nel registro** (gestione completa) oppure **In osservazione** (gestione leggera). Lo
stato **lo calcola lo script** con una regola sulla scala, dopo la validazione; non lo decide A1.

**Regola dello stato** (proposta):
1. **Entra nel registro** un rischio con **Prossimita >= 2** (si puo' manifestare entro 3 anni) **e Probabilita
   >= 2** (non solo teorico).
2. Se i rischi che soddisfano la regola sono piu' di N (la capienza, oggi 20), entrano i **primi N per score**.
   Gli altri restano in osservazione, segnalati come "sopra la soglia, fuori per capienza".
3. **Eccezioni, sempre nel registro**:
   - un rischio AGIRE ORA;
   - un tema all'attenzione del supervisore;
   - una decisione del validatore, con la motivazione.
4. **Margine contro l'altalena**: un rischio esce dal registro solo se e' sotto la regola per **due cicli di
   fila**, oppure per decisione del validatore. Entra subito.

Con la regola 1 nessuna delle quattro voci della demo entra nel 2026Q3: sono tutte a Prossimita 1, oppure (OSS-04)
a Probabilita 2 e Prossimita 2. In quel caso OSS-04 entra, che e' cio' che e' successo davvero un trimestre dopo.
La "solo teorica a 10 anni" resta fuori per regola, non per un giudizio.

**Gestione per stato**:

| | Nel registro | In osservazione |
|---|---|---|
| Valutazione | quattro dimensioni, razionale in parti, fonti | quattro dimensioni (Velocity facoltativa), razionale breve, fonti, orizzonte in anni come nota, segnale di avvicinamento come nota |
| Revisione di A1 | ogni trimestre | solo con evidenza nuova; lo script riporta le altre invariate (come oggi la lista) |
| KRI e azioni | due KRI, azioni | nessuno |
| Viste | radar, classifica, urgenza, Registro, schede, report | foglio e pagina Fenomeni: stesse colonne della rubrica, con lo score e la distanza dalla regola |
| Validazione | sezione Rischi della griglia | **la stessa sezione**, con la colonna Stato |
| A3 | `rischio_collegato` e `flag_proposti` | gli stessi campi: un codice solo |

**Passaggi di stato**:
- *Ingresso*: il rischio entra subito nel registro con "KRI da definire" e nessuna azione; nell'urgenza vale la Y
  di riserva. Al ciclo dopo A1 gli deve due KRI e le azioni, come per un rischio nuovo. In alternativa A1 applica
  la regola gia' nella risposta e lo script la verifica (piu' veloce, ma A1 deve fare un calcolo).
- *Uscita*: i KRI escono di vigore con la storia conservata; le azioni aperte restano fino alla chiusura.

| Pro | Contro |
|---|---|
| un solo codice, una sola scala, una sola sezione della griglia, un solo canale di A3 | il registro cresce: anagrafica da 20 a circa 50 righe (registro piu' osservazione), viste filtrate sullo stato |
| il passaggio e' una regola calcolata e motivabile, non un giudizio di A1 | **migrazione**: le voci OSS diventano rischi in osservazione; Probabilita e Prossimita convertite in via provvisoria, poi rivalutate da A1 al primo ciclo |
| nello schema di A1 sparisce la sezione `osservazione`, in A3 `voce_osservazione` e `segnali_osservazione` | lavoro su generatore, script, schemi, controlli, griglia, report, knowledge di A7, prompt di A1 (al limite) e di A3 |
| la pagina Fenomeni mostra quanto ogni fenomeno e' lontano dall'entrare | la regola (soglie e N) e' un parametro nuovo da tarare con la funzione di rischio |

Peso nella risposta di A1: invariato rispetto a oggi, perche' le voci in osservazione si riscrivono solo con
evidenza nuova. Una voce sulla rubrica pesa circa come oggi, 1 KB.

Impegno: **4-5 giorni**:
- struttura del registro nuova e migrazione in `aggiorna-registro` (2);
- script, controlli e griglia (1-1,5);
- schemi e prompt (0,5);
- collaudo, demo e documenti (1).

## 13.5 Confronto

| Criterio | A: lista sulla scala della rubrica | B: scala unica a due stati |
|---|---|---|
| Un solo meccanismo (obiettivo dell'utente) | no | **si'** |
| Rischi e fenomeni confrontabili | si' | si' |
| Passaggio fra i due mondi | giudizio di A1, con un'indicazione | **regola calcolata** con eccezioni e margine |
| Codici, sezioni della griglia, canali di A3 | due | **uno** |
| Migrazione del registro in Banca | colonne nuove della lista | voci OSS convertite in rischi in osservazione |
| Impegno | ~1 giorno | 4-5 giorni |
| Rischio di realizzazione | basso | medio: anagrafica piu' grande e viste filtrate |

## 13.6 Raccomandazione

**Opzione B**, con la regola della sezione 13.4 (soglia sulla scala piu' capienza, eccezioni, due cicli per
uscire) e non con il solo "primi N per score". E' l'unica che raggiunge l'obiettivo di un solo meccanismo. Il
caso OSS-04 mostra che la regola sposta un fenomeno nel momento giusto senza un giudizio in piu'.

Il momento e' adesso, prima del primo ciclo vero (2026Q4, inizio 2027):
- secondo l'HANDOFF, in Banca il registro non e' ancora alla struttura con la lista (2026-10-07b): la lista non e'
  in uso e la migrazione delle voci sarebbe vuota;
- tutte le voci P successive (P1, P5, P6) partono da un modello piu' semplice.

## 13.7 Scelte da fare prima di costruire B

1. **Soglia di ingresso**: Prossimita >= 2 e Probabilita >= 2 (proposta), oppure solo Prossimita >= 2.
2. **Capienza N** del registro: 20 come oggi (proposta), oppure un numero piu' basso per un report piu' corto.
3. **Eccezioni**: AGIRE ORA, supervisore, validatore (proposta); se aggiungerne o toglierne.
4. **Uscita**: dopo due cicli sotto la regola (proposta), oppure subito.
5. **Ingresso**: KRI e azioni al ciclo dopo (proposta, nessun calcolo per A1), oppure A1 applica gia' la regola.
6. **Massimo di rischi in osservazione**: 30 come la lista di oggi (proposta).

Dopo le scelte: un'anteprima Excel del Registro e della pagina Fenomeni con i dati della demo, poi la
costruzione (TODO P10).

**Risposte dell'utente (08/10)**: opzione B. 1 si', da documentare nel foglio. 2: 15 rischi nel registro (radar di
Mosca) per ora, fino a 20. 6: al massimo 20 rischi in osservazione. 3, 4 e 5 spiegati nella 13.8.1, con una
proposta per ciascuno.

## 13.8 Piano di realizzazione dell'opzione B

**Parole (chiarite con l'utente l'08/10).**
- Il **registro** e' **unico**: tutti i rischi, fino a 40.
- I primi secondo la regola sono **nel radar** di Mosca: 15, fino a 20. Hanno gestione completa: KRI, azioni,
  urgenza, report e schede.
- Gli altri, fino a 20, sono **in osservazione**: stessa scala e stesso score, niente KRI ne' azioni.

Dove sotto si legge "nel registro" come stato, si intenda **"nel radar"**. L'anagrafica di Parametri sara' l'elenco
dei rischi nel radar. Valori della colonna Stato: **Radar**, **Radar, in uscita**, **Osservazione**.

**Scelte confermate dall'utente (08/10)**:
- eccezioni: tutte e tre (AGIRE ORA, supervisore, validatore);
- uscita dopo due cicli;
- ingresso con KRI e azioni scritti subito da A1;
- 15 nel radar (parametro fino a 20), al massimo 20 in osservazione.

### 13.8.1 I punti 3, 4 e 5, spiegati con un esempio

**3. Eccezioni: chi resta nel registro anche se non rispetta la regola.** La regola guarda solo Prossimita e
Probabilita, quindi non vede due casi.
- *Urgenza.* La crittografia dei pagamenti e il calcolo quantistico hanno Prossimita 1 (oltre 3 anni). Ma se la
  migrazione agli algoritmi nuovi dura 5 anni, il radar di Mosca dice AGIRE ORA: bisogna partire prima che il
  rischio arrivi. Senza eccezione il rischio finirebbe in osservazione proprio quando serve un'azione.
- *Decisione umana.* Un tema chiesto dalla vigilanza (◆), o un rischio che la funzione di rischio vuole seguire
  comunque, con la motivazione.

Proposta:
- resta (o entra) nel registro un rischio **AGIRE ORA**;
- resta nel registro un rischio **◆ supervisore**;
- resta nel registro, o ne resta fuori, un rischio con la **decisione del validatore**: una colonna nella griglia,
  con la Motivazione.

**4. Uscita: subito o dopo due trimestri.** Esempio: NFR-09 (sanzioni) ha Probabilita 2 e Prossimita 2, giusto sulla
soglia. Se un trimestre la Probabilita scende a 1 e quello dopo torna a 2:
- con l'**uscita subito**, esce, perde i KRI in vigore e le azioni, e il trimestre dopo rientra da capo;
- con l'**uscita dopo due cicli**, il primo trimestre resta nel registro con l'etichetta "in uscita"; esce solo se
  anche il trimestre dopo e' sotto la soglia.

Proposta: due cicli. Un rischio che sale invece entra subito.

**5. Ingresso: chi scrive KRI e azioni di un rischio che entra.** Un rischio in osservazione non ha KRI ne' azioni;
quando sale sopra la soglia ne servono due e almeno un'azione.
- (a) A1 conosce la regola (sta nell'allegato) e li scrive nella stessa risposta in cui alza il valore.
- (b) Il rischio entra con "KRI da definire" e A1 li propone al trimestre dopo.

Proposta: **(a)**, che non lascia un trimestre senza KRI. Se e' la validazione a portare un rischio sopra la soglia,
vale (b) per quel trimestre: entra con "KRI da definire" e la segnalazione al validatore.

**Capienza (punto 2).** Leggo "15 / 20" cosi':
- la **capienza del registro** e' un parametro in Parametri (cella gialla), oggi **15**;
- lo si puo' alzare fino a **20**, il massimo delle viste (anagrafica, radar, classifica), senza rigenerare niente.

Rischi in osservazione: al massimo **20**.

### 13.8.2 Il modello dei dati

| Oggi | Con l'opzione B |
|---|---|
| Anagrafica in Parametri = i rischi attivi (fino a 20) | **anagrafica = il registro**: solo i rischi "nel registro", al massimo la capienza (15, fino a 20). Tutte le viste che partono dall'anagrafica (Registro, Radar_Mosca, Classifica, Matrice, Delta, Storico, Quadro, Indicatori) **non cambiano** |
| Tabella dei rischi (RiskRegister): una riga per rischio per ciclo | stessa tabella per **tutti** i rischi, con tre colonne nuove: **Stato** (Registro / Registro, in uscita / Osservazione), **Orizzonte_Anni** e **Segnale_Avvicinamento** (note, solo per l'osservazione, fuori dallo score) |
| Lista di osservazione: tabella a parte `tblOsservazione`, codici `OSS-nn` | **non c'e' piu'**: un rischio in osservazione e' una riga della tabella dei rischi con Stato Osservazione e codice `NFR-nn`, senza KRI ne' azioni |
| Promozione decisa da A1 | **regola calcolata dallo script**, uguale per tutti |

Parametri nuovi (celle gialle, con la spiegazione accanto):
- capienza del registro, 15;
- soglia di Prossimita, 2;
- soglia di Probabilita, 2;
- cicli prima dell'uscita, 2.

Restano fissi nella struttura il massimo di 20 nel registro e di 20 in osservazione.

### 13.8.3 La regola, in un punto solo del codice

Una sola funzione dello script decide lo stato di ogni rischio. La usano `trimestrale` (sui valori proposti, cosi'
le viste sono gia' giuste durante la validazione), `valida` e la riapertura (sui valori validati), lo straordinario
e la migrazione.
1. Candidato al registro: Prossimita >= soglia e Probabilita >= soglia.
2. Sempre nel registro: AGIRE ORA, ◆ supervisore, decisione "Registro" del validatore. Mai: decisione
   "Osservazione" del validatore.
3. Se i candidati superano la capienza: prima le eccezioni, poi i piu' alti per score. Gli altri vanno in osservazione
   con il motivo "fuori per capienza".
4. Un rischio del registro sotto la regola diventa "in uscita"; se lo e' gia' dal ciclo prima, passa in osservazione.
5. Passaggi:
   - in **ingresso** il rischio entra nell'anagrafica (come un rischio nuovo);
   - in **uscita** lascia l'anagrafica, compattata come con `dismetti`: i KRI escono di vigore, la storia resta; le
     azioni aperte restano nel Piano_azioni fino alla chiusura.

Il motivo dello stato e' scritto per ogni rischio, per esempio "Prossimita 1 sotto la soglia 2" o "fuori per
capienza: score 2,60, ultimo del registro 2,75". Lo leggono il foglio Osservazione, il report e A7.

### 13.8.4 Cosa cambia, per componente

| Componente | Modifica |
|---|---|
| **Rubrica** (kernel) | sezione nuova "Registro e osservazione": regola, eccezioni, uscita, ingresso; letta da Metodologia, guida dei fogli e prompt |
| **Schema di A1** | sparisce `osservazione`; nei rischi `orizzonte_anni` e `segnale_avvicinamento` facoltativi; KRI e azioni obbligatori solo per chi sta nel registro (controllo dello script, non dello schema) |
| **Schema di A3** | spariscono `voce_osservazione` e `segnali_osservazione`: una notizia si collega a qualunque `NFR-nn` (`rischio_collegato`) e i segnali diventano `flag_proposti` |
| **Baseline e allegato** | `rischi` (registro) e `rischi_in_osservazione` (con le notizie di A3 dopo il ciclo); guida di scrittura: la lista diventa "Rischi in osservazione" (rivaluta solo con evidenza nuova; KRI e azioni per chi entra) |
| **Controlli** | completezza (C1) solo per il registro; KRI e azioni (C8, C9) solo per il registro; un rischio che entra senza KRI e' da motivare; al massimo 20 in osservazione (fermo); `controlla_osservazione` sostituita da questi |
| **Script** | funzione della regola; `trimestrale` scrive tutte le righe (le osservazioni non toccate si riportano invariate, come oggi le voci); anagrafica aggiornata con ingressi e uscite; `valida` e `riapri` ricalcolano gli stati (`riapri --voci` sparisce, vale `--rischi`); `dismetti` vale anche per un rischio in osservazione (archiviarlo) |
| **Griglia di validazione** | una sola sezione Rischi; colonna **Stato** (calcolato, con il motivo) e colonna **Decisione sullo stato** (Automatico / Registro / Osservazione, con Motivazione); sparisce la sezione Osservazione |
| **Viste** | Registro, radar e le altre invariate; Quadro: "variati · nuovi" contano solo il registro; riga nuova "entrati · usciti"; foglio **Osservazione** e pagina **Fenomeni** rifatti sulla stessa scala (le quattro dimensioni, lo score, il motivo dello stato, orizzonte e segnale come note) |
| **Parametri, Metodologia, Guida dei fogli, Dizionario** | la regola documentata nel foglio (richiesta dell'utente): celle dei parametri con la spiegazione, paragrafo nella Metodologia, voce nella Guida |
| **Knowledge di A7, schede** | `Ciclo.txt`: rischi in osservazione con il motivo dello stato e gli ingressi e uscite del ciclo; schede solo per il registro |
| **Migrazione** (`aggiorna-registro`) | voci OSS in osservazione -> rischi in osservazione con codice `NFR-nn` nuovo: Impatto = impatto potenziale, Probabilita da plausibilita' (teorica 1, possibile 2, in crescita 3), Prossimita da orizzonte (oltre 3 anni 1, 2-3 anni 2), Velocity vuota; da rivalutare da A1 al primo ciclo; la tabella vecchia resta nel backup |
| **Prompt** | A1 (al limite: procedura riscritta piu' corta, dettagli nella guida di scrittura), A3, A5 (C1), A7, A8 |
| **Collaudo** | test dei controlli e della regola (casi: sulla soglia, capienza, eccezioni, uscita in due cicli, ingresso senza KRI); passi della catena con la lista riscritti; dati di prova convertiti; migrazione da un registro con la lista |
| **Demo e documenti** | demo con un ingresso (OSS-04 di oggi) e un'uscita "in uscita"; DECISIONI (D-79), guida, LEGGIMI, workflow, governance, SharePoint (colonne nuove della lista RiskRegister_Storico), TODO, HANDOFF, PROMPT_MASTER |

Struttura nuova del registro (versione 2026-10-09) e `aggiorna-registro` in Banca.

### 13.8.5 Fasi, con i punti in cui decidi

| Fase | Cosa | Verifica |
|---|---|---|
| 0 | Le scelte 3, 4, 5 e la capienza (questa sezione) | **conferma dell'utente** |
| 1 | **Anteprima Excel** (fuori dal pacchetto): Parametri con la regola documentata, foglio Osservazione e pagina Fenomeni sulla stessa scala, Registro e Quadro con "entrati · usciti", griglia con Stato e Decisione sullo stato; dati della demo | **valutazione dell'utente** |
| 2 | Kernel: rubrica, schemi A1 e A3, guida di scrittura, mappa | test della mappa e dei controlli |
| 3 | Script: regola, scrittura, validazione, riapertura, baseline, migrazione | test dei controlli e della regola |
| 4 | Generatore e template | apertura in Excel, zero errori, PDF guardato |
| 5 | Prompt A1, A3, A5, A7, A8 | sotto gli 8.000 caratteri |
| 6 | Dati di prova e catena | collaudo completo verde |
| 7 | Demo e documentazione | demo rilanciata, `REPORT_demo.md` |

**Stato (08/10)**: fase 0 fatta (scelte confermate). Fase 1 pronta: `Anteprima_Scala_unica/` (cancellata l'08/10 sera dopo la realizzazione; fuori dal
pacchetto), con `genera_anteprima.py` (contiene il prototipo della regola, funzione `stati`),
`Anteprima_scala_unica.xlsx` e il PDF. Sui dati della demo NFR-15 (ex OSS-02) entra nel radar, 14 su 15 posti;
NFR-14 e NFR-16 restano in osservazione. Attesa la valutazione dell'utente.

**Stato (08/10 sera)**: anteprima approvata dall'utente ("mi piace procedi"); fasi 2-7 fatte, **D-79**, struttura
2026-10-09. Scostamenti dal piano, decisi strada facendo:
- valori della colonna Stato: **Radar**, **Radar, in uscita**, **Osservazione** (piu' Dismesso dopo `dismetti`);
  decisione sullo stato **Automatico / Radar / Osservazione**;
- nei dati di esempio i tre rischi in osservazione sono NFR-13, 14, 15 (le tre voci della vecchia lista); la
  vertenza dei dati di prova e' NFR-16 (nasce in osservazione nel 2026Q3, entra nel radar nel 2026Q4) e A8 censisce
  NFR-17;
- Movimento "Entrato" solo per chi era in osservazione nel ciclo prima: un rischio nuovo che va subito nel radar e'
  Nuovo, senza Movimento;
- nel foglio Notizie una categoria con soli rischi in osservazione e' "In osservazione", non "AREA NON PRESIDIATA";
- `aggiorna-registro` confronta la baseline senza la regola del radar (pesi e soglie del template nuovo).
Dettaglio in HANDOFF, sezione 2-quattuorvicies.

Impegno: fasi 2-7 circa 5 giorni (piu' della stima della 13.4, perche' la lista e' gia' in 40 file fra codice, dati
e documenti).
