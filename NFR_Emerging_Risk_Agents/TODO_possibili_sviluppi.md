# TODO — registro vivo del lavoro

**Da qui si parte.** Questo file dice a che punto e' il lavoro su `main` e che cosa viene dopo: per riprendere basta la
sezione 0. Ogni voce aperta dice perche' serve, cosa fare e come capire che e' fatta.

**Aggiornato al 30/10/2026.**

Come si tiene vivo, a ogni intervento:
1. all'inizio si legge la sezione 0; alla fine si aggiornano la data, il quadro, gli impegni in sospeso e il prossimo
   passo;
2. una voce finita esce dalla sua sezione e diventa una riga di **"Fatto"** (sezione 9); una voce che non serve piu'
   diventa una riga di **"Superate"** (9-bis), con il motivo; una voce nuova entra nella sua sezione e, se cambia le
   priorita', nell'ordine di lavoro (sezione 1);
3. un passo provato in Banca cambia stato nella sezione 2 lo stesso giorno, con la data e cio' che si e' visto;
4. qui non si copia cio' che ha gia' un posto: decisioni in `04_Riferimenti/DECISIONI.md`, racconto nell'HANDOFF, spunte
   dell'app in `Analisi_Architettura/18_App_orchestrazione.md`, passi in Banca in `AGGIORNAMENTO_IN_BANCA.md`; niente
   numeri che invecchiano, come i caratteri dei prompt o i conteggi dei test;
5. i codici delle voci (P, AU, B, Q, G, M) non cambiano, perche' DECISIONI, HANDOFF e analisi li citano.

La versione tutta in Copilot Studio ha il suo registro, sul ramo `copilot-studio-pieno`:
`09_Copilot_Studio/TODO_Copilot_Studio.md`. Qui restano le voci di `main` e quelle comuni ai due rami.

Sezioni:
0. da dove si riparte;
1. ordine di lavoro;
2. passi sul PC della Banca (non sviluppo: installare e provare cio' che c'e' gia');
3. processi (P1, P2, P4, P5, P6, P7, P9, P12, P13, P14, P15);
4. automazione del processo: l'app di orchestrazione, fatta; resta la demo (AU5);
5. quantificazione (Q1);
6. grafici e report (G1, G2, G3, G5, G6);
7. pulizia residua (M1, M4);
8. questioni aperte emerse dal lavoro (compresa la revisione della procedura);
9. fatto, e 9-bis superate;
10. in riserva.

## 0. Da dove si riparte

| Quadro | |
|---|---|
| Obiettivo | primo ciclo vero **2026Q4**, primo run di A1 a inizio gennaio 2027 (D-22) |
| Versione in uso | `main`: agenti in Agent Builder, app Python sul PC (D-83); tappe M1-M5 fatte |
| Ultimo commit | 30/10: D-90, D-91 e il riordino di questa TODO, non ancora su GitHub |
| Ultimo pacchetto preparato | 30/10, commit `aa7aea9`, zip per la posta; non contiene D-90 e D-91 |
| In Banca | il 29/10 prima prova dell'app, con un pacchetto precedente; l'installazione del pacchetto del 30/10 non e' ancora annotata (B1) |
| Ramo `copilot-studio-pieno` | allineato a `aa7aea9` (merge `11520a3`); strada del motore da capire (D-91); ha il suo registro |

**In sospeso** (da chiudere prima di ogni altra cosa):

| # | Cosa | Stato |
|---|---|---|
| 1 | `AGGIORNAMENTO_IN_BANCA.md`, per il prossimo pacchetto: D-90 (il pulsante Testi a mano passa in Admin) e D-91 (`mappatura_campi.json` cambia nel kernel, `workflow.md` fra gli obsoleti) | da fare |
| 2 | Collaudo completo sul PC con Excel (`esegui_collaudo.py`, catena compresa): non rilanciato dopo M4, M5, D-86 e D-90 | da fare |
| 3 | `esegui_demo.py` con `REPORT_demo.md` sui testi lunghi (D-86), poi la presentazione | da fare |
| 4 | Ramo `copilot-studio-pieno`: `git merge main` e `genera_CS.py`, per ricevere D-90 e D-91. Nel merge di questa TODO si tiene la versione di `main`: le due righe proprie del ramo sono nel suo registro | da fare |

**Prossimo passo**: i punti 1-3 qui sopra, poi il pacchetto in Banca e le sue verifiche (B1-B4, B5-bis).

**Decisioni che aspettano** (il testo e' in DECISIONI):

| Decisione | Quando |
|---|---|
| **A-19** scale a 6 livelli e registro nuovo: indirizzo dell'utente del 30/10, si avvia su sua richiesta | **prima del primo ciclo vero**: 4-6 giorni piu' un ciclo di prova (P15) |
| A-24 driver | con A-19 |
| A-17 contraddittorio | dopo la prova K15 (B8) |
| A-20, A-21, A-22, A-23 spunti della proposta esterna | su richiesta dell'utente (P15) |
| A-12 taratura | dopo il ciclo 2026Q4 reale |

## 1. Ordine di lavoro

L'ordine mette prima cio' che migliora il primo ciclo vero. L'app e' fatta: da qui in poi il lavoro e' provarla e
migliorare la qualita' dei contenuti.

| Passo | Voci | Perche' qui | Giorni | Stato |
|---|---|---|---|---|
| 0 | **In sospeso** (sezione 0) | pacchetto, demo e documenti devono essere allineati prima di andare in Banca | circa 0,5 | in corso |
| 1 | **B1-B4, B5-bis**: pacchetto in Banca e verifiche dell'app | tutto il resto si appoggia su un'installazione allineata | 1-2 | in corso (prima prova il 29/10) |
| 2 | **P15, punto 1**: scale a 6 livelli e registro nuovo (A-19), con i driver (A-24) | A-19 va fatta prima del ciclo vero: cambia rubrica, schemi e registro, che riparte da zero. Viene prima delle voci piccole, che toccano gli stessi testi | 4-6 | su richiesta dell'utente |
| 3 | **P4** rapporti di scenario, **P9** temi da verificare, **P14** il "so what" nei testi di A1 | piccole, migliorano subito la qualita' del trimestrale: A1 legge i rapporti di analisti e regolatori, le richieste dell'analista restano tracciate, le schede dicono che cosa significa ogni rischio per la Banca | circa 1,5 | da fare |
| 4 | **B7** ciclo di prova, **B9** qualita' di A1 e A8, **B6** prova di A7; **B8** (K15) se c'e' tempo | il collaudo di qualita' prima del ciclo vero, sulla versione con le voci dei passi 2 e 3 | in Banca, con le attese | da fare |
| 5 | **P1** segnali qualitativi per dimensione e pressione sul radar | e' il pezzo che manca di piu' al settimanale, ma non cambia il primo trimestrale: si comincia solo se finisce prima di gennaio | 2-3 | da fare |
| 6 | **P5** rischi collegati | un evento che tocca piu' rischi resta leggibile come un insieme; con il registro unico capitera' piu' spesso | 2-3 | da fare |
| 7 | **P2**, **P7**, **P6** | presentazione: scia sul radar, riepilogo mensile, scheda per tema | 2-3 | da fare |
| dopo il ciclo vero | **P13** (diagnosi con la funzione di rischio), **P12** se K15 dice che serve, gli altri punti di **P15**, **revisione della procedura** (sezione 8) | servono i dati e l'esperienza di un ciclo vero | | |
| in parallelo | **AU5** demo attraverso i flussi (sezione 4) | copre i flussi oggi provati solo con l'Ambiente finto | circa 1 | da fare |
| in parallelo | **Q1** nota di metodo (il prototipo dopo il passo 6) | e' soprattutto lavoro della Banca (stime degli esperti) | nota 1-2, prototipo 3-5 | da fare |
| in parallelo | **G1, G3, G2**; **G6** quando servira' leggere A1 accanto ai controlli prima della scrittura | toccano solo il generatore o sono strumenti di lettura | circa 2 | da fare |
| sempre | **G5** difetti estetici, **sezione 8** questioni aperte | quando capitano | | |

## 2. Passi sul PC della Banca

Non sono sviluppo: si installa e si prova cio' che il pacchetto ha gia'. I passi del pacchetto corrente sono in
`AGGIORNAMENTO_IN_BANCA.md`, quelli generali nella guida, sezione 0-bis. Le prove di Copilot Studio sono nel registro del
ramo (9-bis).

| # | Passo | Per quali decisioni | Stato |
|---|---|---|---|
| B1 | Pacchetto corrente con `installa.cmd`, sopra quello del 23/10; sposta da solo in `_obsoleti_<data>` le cartelle dei pacchetti vecchi (`04_SharePoint`, `05_Workflow`, `06_Governance`, `08_Deploy`) | D-78, D-89 | da fare |
| B2 | Kernel nella library: lo copia `installa.cmd` dopo una conferma (i file sostituiti in `Kernel\_precedenti\<data>`) e toglie `Baseline_corrente.txt` e `Tassonomia dei Rischi.csv` | D-74, D-89 | da fare |
| B3 | Reincollare gli agenti che `installa.cmd` elenca: sopra il pacchetto del 23/10 bastano A4, A5, A6 e A7 | D-86...D-88 | da fare |
| B4 | `aggiorna-registro`: non serve con questo pacchetto, la struttura resta `2026-10-09`. Solo per un registro in una struttura precedente, prima su una copia | D-74, D-79 | non serve con il pacchetto corrente |
| B5-bis | **Verifiche dell'app, tappe M1-M5**: elenco in `AGGIORNAMENTO_IN_BANCA.md` ("Verifiche da fare"), esiti in `Analisi_Architettura/18_App_orchestrazione.md`, 18.6. **29/10**: prima prova, un trimestre dall'app fino a `trimestrale` e validazione (A1, precontrollo, una correzione, precontrollo superato); i problemi trovati sono corretti. Restano, sul pacchetto corrente: risposta lunga di A1 dagli appunti, link degli agenti, lucchetto con un collega, installazione completa (pip, collegamenti, attivita' della raccolta, Verifica del PC con Excel), report HTML, Admin | D-83, D-85...D-90 | in corso |
| B6 | Prova di A7 (`04_Riferimenti/Prove/Prova_A7.md`), anche per la prima persona | D-72, D-87 | da fare |
| B7 | Ciclo 2026Q4 di prova (prima del ciclo vero): converge in 1-2 giri A1, senza A5 o con A5. **29/10**: un giro di correzione, senza le lunghezze di C10; da rifare sulla versione dei passi 2 e 3 dell'ordine | S1 (D-49...D-56), D-69, D-71 | in corso |
| B8 | Facoltativo, per A-17: **K15** contraddittorio senza codice sul ciclo 2026Q4 (`Analisi_Architettura/17_Decimo_uomo.md`, 17.8): A9 in Agent Builder dopo A1, piu' la variante 2b nella chat di A1; il validatore giudica ogni tesi utile, gia' nota o rumore. Dal 30/10 con il mandato esteso (A-17, analisi 19) | A-17 | da fare |
| B9 | **Prova di qualita' di A1 e A8 su documenti pubblici** (proposta del 24/10): una libreria di documenti pubblici (EBA, BCE, ENISA, rassegne stampa; niente di interno alla Banca) sul PC di sviluppo e la stessa in Banca. (a) Sul PC di sviluppo Claude fa A1 o A8 con le istruzioni, l'allegato `Input_A1`/`Input_A8` e i documenti, poi precontrollo e `trimestrale` sul registro di prova: dice se istruzioni e documenti bastano, non che cosa fara' l'agente (Claude legge i documenti per intero, Agent Builder ne pesca dei pezzi). (b) Prova piu' utile: l'agente vero in Banca sugli stessi documenti, il JSON (senza dati della Banca) riportato e controllato da Claude affermazione per affermazione (fatti e date nel documento citato, descrittori della rubrica, fenomeni mancati o scartati a torto) | qualita' di A1 (D-21), P14 | da fare |

## 3. Processi: cosa manca rispetto al disegno atteso

Dall'analisi del 26/09/2026: il processo desiderato e' **trimestrale come processo fondante** (su documentazione
approfondita: regolatori, analisti di settore, siti specialistici, analisi interne), **settimanale o mensile** sulle
notizie (trend dei rischi esistenti, evento critico che chiede di rigenerare il trimestre, variazioni visibili sul
radar) e **spot** su una sola notizia (analisi a fondo, impatto per dimensione, posizione sul radar).

Decisioni dell'utente che fanno da cornice:
- **D-41**: "mai una cifra nuova" fuori dal trimestre e "solo un ciclo di valutazione modifica uno score"; l'unica
  eccezione e' il ciclo straordinario (fatto: D-75, D-77). Niente notch numerici ne' posizioni ipotetiche sul radar.
- **D-42**: un evento che tocca piu' rischi genera righe di rischio separate, collegate fra loro (P5).
- **D-79**: un registro unico, nel radar i primi e gli altri in osservazione, con la stessa scala.

| Attesa | Stato oggi | Voce |
|---|---|---|
| Trimestrale come unico processo che cambia gli score | c'e' (principio 3, W1) | — |
| Trimestrale su rapporti approfonditi di analisti e regolatori | in parte: vigilanza e cyber arrivano come notizie; nessun canale per i rapporti da leggere per intero | **P4** |
| Temi che l'analista chiede di verificare | in parte: si scrivono nel messaggio ad A1, non restano tracciati | **P9** |
| Report aggiornato, non rifatto, e ciclo straordinario | c'e' (Confermato/Variato/Nuovo, al piu' un punto; straordinario D-75, A8 D-77) | — |
| Fenomeni lontani o quasi impossibili oggi | c'e': rischi in osservazione del registro unico (D-79) | — |
| Settimanale: analisi su tutti i rischi toccati | in parte: nove intensita' per notizia, un solo rischio collegato | **P1** |
| Settimanale: trend dei rischi esistenti e pressione visibile sul radar | in parte: segnali netti, flag, soglia 3 in 4 settimane; il radar non mostra la pressione | **P1** |
| Spot: impatto per dimensione | in parte: A4 indica il descrittore messo in discussione | **P1** |
| Evento con piu' meccanismi di perdita | c'e' la regola (D-42); manca il collegamento fra le righe | **P5**, P6 |
| Spostamento nel tempo dei rischi | in parte: Storico, Delta, schede; il radar e' una fotografia | **P2** |
| Cadenza mensile | in parte: la finestra di 4 settimane lo e' di fatto | **P7** |
| Contraddittorio sulla valutazione ("decimo uomo"): letture opposte, rischi mancanti, ipotesi, combinazioni | manca: A5 controlla la coerenza dell'output di A1, non la sua completezza ne' le letture alternative | **P12** |
| Testi del registro e delle schede chiari e diretti, ma completi e approfonditi, con il "so what" per la Banca | in parte: guida di scrittura (descrizione in 3-5 frasi, razionale in parti con descrittore, fatto e "perche' non il valore vicino"), lunghezze minime e consigliate con il controllo C10 (D-86, D-88); manca il "so what" esplicito | **P14** |
| Valutazioni senza asimmetrie: rischi nuovi non tutti bassi, rischi lontani a mitigazione lunga visibili all'urgenza | in parte: diagnosi e anni di adeguamento dei rischi in osservazione (D-80), esposizione non nota (D-81) fatti; restano salto con evidenza forte, taratura | **P13** |

### P4. Canale "rapporti di scenario" per A1

- **Perche'**: il trimestre deve poggiare su analisi approfondite, non solo su notizie. Oggi A1 li usa solo se
  qualcuno li mette in `Analisi_Interne`, senza distinguerli. Sono anche la fonte naturale dei fenomeni lontani, che
  dal 08/10 entrano come rischi in osservazione (D-79).
- **Cosa fare**: in `fonti.md` un tipo di fonte `rapporto` (canale `share`), con una cartella dedicata (es.
  `Rapporti_Scenario/<anno>`); A1 li legge per primi e li cita nel razionale; le schede di A6 dicono quale rapporto
  sostiene quale dimensione. Esempi: ORX Emerging Risks e Horizon, EBA Risk Assessment Report, priorita' di vigilanza
  BCE, ENISA Threat Landscape, WEF Global Risks, Allianz Risk Barometer, rapporti delle societa' di consulenza.
- **Tocca**: `fonti.md` (e `fonti.py`), guida di scrittura di A1 (il prompt e' al limite degli 8.000 caratteri: l'istruzione va
  nell'allegato), struttura SharePoint, licenze d'uso (governance).
- **Fatto quando**: il ciclo di prova cita almeno un rapporto per ogni rischio variato.
- **Impegno**: basso, circa mezza giornata.

### P9. Temi da verificare indicati dall'analista (proposta del 06/10/2026)

- **Perche'**: oggi l'unico modo di chiedere ad A1 di verificare un rischio preciso e' scriverlo nel messaggio della
  chat: la richiesta non resta tracciata, nessuno controlla che A1 l'abbia esaminata e va riscritta a ogni ciclo. Con
  il registro unico (D-79) un tema con una fonte diventa comunque un rischio, anche lontano (in osservazione): P9
  serve a tracciare la richiesta e la risposta.
- **Cosa fare**: un file `temi_da_verificare.md` nella library Kernel (un tema per riga, con chi lo chiede e
  perche'); `input_a1.py` lo aggiunge all'allegato `Input_A1` come quarta parte, con l'istruzione: per ogni tema,
  rischio (nel radar o in osservazione) se c'e' almeno una fonte specifica, altrimenti fenomeno non censito con il
  motivo. Il prompt di A1 non cambia. Un controllo dello script (Osservazione) segnala un tema che non compare ne' fra
  i rischi ne' fra i fenomeni non censiti.
- **Fatto quando**: allegato con la parte 4, controllo nel collaudo, guida (sezione 2, punto 4).
- **Impegno**: circa mezza giornata.

### P12. Contraddittorio sulla valutazione trimestrale, "decimo uomo" (proposta del 19/10/2026, A-17)

- **Perche'**: le regole (conferma di default, un punto per ciclo) proteggono dall'inflazione ma favoriscono lo status
  quo; A5 non usa la knowledge (D-09) e non cerca cio' che A1 non ha visto. Manca chi sostenga la tesi opposta.
- **Cosa fare**: analisi `Analisi_Architettura/17_Decimo_uomo.md`. Opzione 1 raccomandata: agente A9 Contraddittore
  dopo A1, con la knowledge di A1 e una ricerca propria; JSON senza numeri (tesi in entrambi i versi sui rischi
  principali, rischi mancanti, ipotesi critiche, combinazioni); `trimestrale --contraddittore`: tesi nella colonna
  Segnalazioni come Osservazioni, sintesi in Sintesi_Cicli e nel Quadro, rischi mancanti come temi da verificare (P9).
  Prima la prova K15 senza codice (B8).
- **Tocca**: schema nuovo, modello del prompt, script, template (versione nuova), collaudo, guida,
  `controlli_e_model_risk.md` (rischio "ancoraggio alla valutazione precedente").
- **Fatto quando**: K15 dice che le tesi servono e la catena del collaudo porta un A9 di prova fino al Quadro.
- **Impegno**: prova mezza giornata; integrazione circa 3-4 giorni. Dopo P9.

### P13. Ancoraggio e asimmetrie della valutazione (proposta del 19/10/2026)

- **Perche'**: analisi `Analisi_Architettura/17_Decimo_uomo.md`, 17.10. Le regole che frenano l'inflazione (conferma di
  default, un punto per ciclo, valori di prima nella baseline, accettazione senza gesti) fanno anche restare basso un
  rischio entrato basso; i descrittori di Probabilita 4-5 chiedono casi gia' osservati e l'esposizione della Banca, che A1
  non conosce: nella demo 7 rischi nuovi su 7 sono entrati con Probabilita 3 o meno. I rischi oltre i 3 anni restano in
  osservazione e, senza anni di adeguamento, Mosca non li vede mai urgenti.
- **Cosa fare**, in ordine:
  1. **fatto (D-80)**: comando `diagnosi` (valori all'ingresso, verso delle rettifiche, rischi lontani); da lanciare sul
     ciclo 2026Q4 vero dopo la validazione;
  2. **fatto (D-80)**: anni di adeguamento anche per i rischi in osservazione con Impatto 4-5 (guida di scrittura di A1);
  3. **fatto (D-81), variante leggera 3a**: esposizione "non nota" scritta da A1 nel razionale con il valore "se
     esposta", segnalazione da motivare in validazione, decide il validatore. Resta la variante 3b (esposizione
     registrata nell'anagrafica, circa 3 giorni, template nuovo), da fare se la nota torna sugli stessi rischi;
  4. un salto di piu' di un punto in validazione con evidenza di rilevanza alta datata nel ciclo (tocca la regola 2 della
     rubrica: decisione della funzione di rischio);
  5. contraddittorio, tesi "sottovalutato" (P12, A-17);
  6. taratura dei descrittori di Probabilita con la Banca (A-12).
- **Fatto quando**: la diagnosi del 2026Q4 e' letta con la funzione di rischio e i punti 3-6 sono decisi (fatti o
  scartati).
- **Impegno**: variante 3b circa 3 giorni (esposizione nell'anagrafica, template nuovo), 17.10; punto 4 circa 1 giorno dopo la decisione.

### P14. Il "so what" per la Banca nei testi di A1 (proposta del 24/10/2026; lunghezze fatte con D-86 e D-88)

- **Perche'**: descrizioni e motivazioni finiscono nel registro e nelle schede per il comitato e devono dire che cosa
  significa il rischio per la Banca e che cosa chiede al comitato. Le lunghezze minime e consigliate e il controllo C10
  ci sono dal 29/10 (D-86 per A1 e A8, D-88 per A6 e A4); il "so what" non e' ancora chiesto in modo esplicito.
- **Cosa fare**:
  1. il **"so what"** come ultima parte del razionale di A1, con un'etichetta nuova (per esempio `QUINDI:`: che cosa
     significa per la Banca, che cosa va deciso o osservato), nella guida di scrittura (il prompt e' al limite degli
     8.000 caratteri); `schede.py` la riconosce e la mostra come voce a se' della scheda. Nessun campo nuovo nel JSON,
     nessuna versione nuova del template;
  2. un razionale senza `QUINDI:` diventa un rilievo di C10 (stessi livelli: Bloccante per A5, proposta di correzione
     nel precontrollo, Osservazione in validazione);
  3. nella guida di scrittura una breve sezione **"Stile"**: frasi brevi e dirette, niente gergo, ogni affermazione
     completa (chi, cosa, quando, fonte);
  4. da decidere se estendere ad A3 (motivazioni delle notizie).
- **Tocca**: `01_Kernel/guida_scrittura_A1.md`, `controlli_A5.md`, `precontrollo.py`, `schede.py`, collaudo, demo, guida
  passo passo, PROMPT_MASTER. Modifica comune: nasce su `main`, poi merge nel ramo `copilot-studio-pieno`.
- **Fatto quando**: un ciclo di prova (B9) ha il suo `QUINDI:` in ogni scheda, il precontrollo segnala il razionale che
  non ce l'ha e il collaudo e' verde.
- **Impegno**: circa mezza giornata.

### P15. Spunti dalla proposta esterna di osservatorio (analisi 19, 30/10/2026)

- **Perche'**: una proposta esterna per la stessa attivita' (`Analisi_Architettura/19_Confronto_proposta_esterna.md`)
  porta scale a 6 livelli, alberi decisionali, rischio residuo, agente avversariale, fonti per scopo.
- **Cosa fare**, uno per volta su richiesta dell'utente (19.11):
  1. **scale a 6 livelli e registro nuovo (A-19), prima del primo ciclo vero**: indirizzo dell'utente del 30/10, si
     riparte da zero senza convertire lo storico; con i driver per prevalenza, SOV e NOR (A-24);
  2. prova K15 con il mandato esteso (A-17, passo B8);
  3. dopo il primo ciclo: pavimento di evidenza con la prova C (A-20); "agisce su" e casi reali nella scheda (A-24);
     fonti di orizzonte e natura della fonte (A-22); residuo (A-21); STOP morbidi (A-23).
- **Tocca**, per le scale (19.5): kernel, prompt, `radar.py` e soglie, template (versione nuova), collaudo, demo.
  **Modifica comune, non ancora iniziata**: nasce su `main` e passa al ramo `copilot-studio-pieno` con il merge e
  `genera_CS.py`.
- **Impegno**: circa 4-6 giorni per le scale, piu' un ciclo di prova; poi da mezza giornata a 4 giorni per voce (19.11).

### P1. Segnali qualitativi per dimensione e pressione sul radar (settimanale e spot)

- **Perche'**: oggi fra un trimestre e l'altro il radar non dice quali rischi sono sotto pressione, e il settimanale
  dice "peggiorativo" ma non "su quale dimensione". Per D-41 senza numeri: nessun notch, nessuna posizione ipotetica.
- **Cosa fare**: A3 indica, per **ogni** rischio toccato da una notizia (non solo il piu' diretto, anche quelli in
  osservazione), direzione, **dimensione** e **descrittore** messi in discussione; A4 fa lo stesso nella sezione 3 del
  parere (gia' quasi cosi'). Il foglio conta i segnali per rischio e dimensione nelle ultime 4 settimane e segna il
  cerchio **deliberato** nel Radar_Mosca e la riga del Registro con una freccia (in peggioramento, in miglioramento,
  contrastato) quando la soglia di direzione e' superata. Il cerchio non si sposta. I segnali arrivano ad A1 come
  flag del trimestre, con la dimensione. Un segnale sulla Velocity di un rischio "non valutato" e' un buon motivo per
  valutarla al trimestre; uno su Prossimita o Probabilita di un rischio in osservazione dice che puo' entrare nel
  radar.
- **Tocca**: schema A3 (dimensione nei flag, piu' rischi per notizia), `mappatura_campi.json`, fogli Notizie,
  Registro e Radar_Mosca, prompt A3 e A4, controlli e collaudo. Nessun principio da cambiare.
- **Fatto quando**: in demo tre settimane di notizie peggiorative sulla Probabilita di un rischio mettono la freccia
  sul suo cerchio e nel Registro, il cerchio resta fermo e il trimestre dopo A1 riceve il flag con la dimensione.
- **Impegno**: medio, circa 2-3 giorni con collaudo e documentazione.

### P5. Rischi collegati (un evento, piu' righe di rischio)

- **Perche'**: un evento (es. "LLM sempre piu' capaci") tocca piu' meccanismi di perdita. Per D-42 diventa piu' righe
  di rischio separate, ciascuna con i suoi score; va conservata la vista d'insieme dell'evento. La regola "un rischio
  per meccanismo di perdita" (D-55) e il registro unico (D-79, anche i lontani sono rischi) rendono i collegamenti
  piu' frequenti.
- **Cosa fare**: nel rischio un campo `collegati` (elenco di `id_rischio`, con una riga di motivo: "stesso evento",
  "stessa causa") proposto da A1 e validato come gli altri campi; il collegamento e' reciproco (lo script controlla
  che i rischi esistano e completa il verso opposto). Nel Registro una colonna "Collegati"; nelle schede un riquadro
  "Rischi collegati" con i loro score; nel Radar_Mosca, facoltativo, una linea sottile fra i cerchi collegati. Nessuna
  media e nessuno score dell'evento.
- **Tocca**: `tassonomia_nfr.md`, schema A1, mappa, controlli (collegati esistenti, niente autocollegamento),
  Registro, schede (A6 e `schede.py`), collaudo. Prompt A1 al limite degli 8.000 caratteri: le istruzioni vanno nella guida di
  scrittura.
- **Fatto quando**: nella demo due rischi nati dallo stesso evento si citano a vicenda nel Registro e nelle schede.
- **Impegno**: medio, circa 2-3 giorni.

### P2. Scia sul radar e nel report trimestrale

- **Perche'**: il comitato vede dove sta un rischio oggi, non da dove viene.
- **Cosa fare**: nel Radar_Mosca un punto piccolo nella posizione del trimestre prima e una freccia verso quella
  attuale (solo per i rischi variati, per non affollare); nel Quadro, per i primi cinque, la traiettoria su quattro
  trimestri. Un rischio appena entrato nel radar (D-79) ha la scia solo se era gia' nel radar prima.
- **Fatto quando**: nella demo il rischio variato fra 2026Q3 e 2026Q4 mostra la scia; gli altri no.
- **Impegno**: basso-medio (serie in piu' nel grafico, dati da Storico).

### P7. Riepilogo mensile

- **Perche'**: la cadenza mensile e' utile per la funzione di rischio senza un agente in piu'.
- **Cosa fare**: una vista (o un file) che aggrega le ultime quattro settimane: segnali netti per rischio, pressione
  per categoria, aree non presidiate, flag e (con P1) segnali per dimensione; notizie critiche, proposte di ciclo
  straordinario e cicli straordinari del mese.
- **Fatto quando**: un comando o un foglio produce il riepilogo del mese dai dati settimanali gia' registrati.
- **Impegno**: basso.

### P6. Scheda "tema" per driver (facoltativa)

- **Perche'**: un fenomeno ampio (es. l'intelligenza artificiale, DRV-AI) oggi si vede solo sparso nei rischi figli
  (frodi con deepfake, errori di modelli interni, condotta).
- **Cosa fare**: nel file delle schede una scheda per driver (o per gruppo di rischi collegati, P5), con i rischi
  figli, i loro score e l'andamento, anche quelli in osservazione; nessuno score proprio del tema (D-42).
- **Fatto quando**: `Schede_<ciclo>.xlsx` ha una scheda per ogni driver con almeno due rischi.
- **Impegno**: basso.

## 4. Automazione del processo: l'app di orchestrazione

Obiettivo: niente copia-incolla, gli agenti fanno il piu' possibile, ogni azione rimasta si fa da una finestra. **Su
`main` e' realizzato** (D-83): agenti in Agent Builder e app Python sul PC, con il motore Python (D-43, D-91); nel registro
scrive solo il motore, dopo i controlli (D-10). Scelte dell'utente: finestra tkinter; risposte dagli appunti piu' il
file; piu' analisti sullo stesso registro; niente coda delle richieste.

**L'avanzamento voce per voce, con le spunte (fatto, da verificare, da fare), e' in
`Analisi_Architettura/18_App_orchestrazione.md`**; qui solo il riassunto:

| Tappa | Cosa | Moduli | Stato |
|---|---|---|---|
| M1 | motore: lucchetto per piu' analisti, copia di lavoro del registro, Salvataggio automatico spento; AU7; automatismi (report da `valida`, prompt archiviati, PDF delle schede, traccia della riapertura) | `lucchetto.py`, `esegui_ciclo_locale.py`, `input_a1.py`, `excel_com.py` | **fatta il 23/10** |
| M2 | l'app: ingresso unico delle risposte (appunti e file), stato del processo, esecutore del motore, flussi di ogni processo, finestra tkinter | `ingresso.py`, `appunti.py`, `stato.py`, `esecutore.py`, `flussi.py`, `app_nfr.py`, `NFR.cmd` | **fatta il 23/10**, prima prova in Banca il 29/10 |
| M3 | installazione con un doppio clic e Verifica del PC; dal 30/10 anche l'aggiornamento sopra un pacchetto installato (D-89) | `installa.cmd`, `installa.py`, `installazione.py`, `verifica_pc.py`, `notizie_manuali.py` | **fatta il 29-30/10**, da provare in Banca (B5-bis) |
| M4 | report HTML al comitato come seconda uscita di `report`, con i numeri controllati contro Excel | `report_html.py` | **fatta il 29/10**, cancello con Excel da lanciare sul PC (sezione 0) |
| M5 | funzioni amministrative in modalita' Admin (D-85): pulizia, ritorno a un ciclo validato, ripartenza, annullamento; niente si cancella subito; Testi a mano in Admin dal 30/10 (D-90) | `amministrazione.py`, finestra Admin dell'app | **fatta il 29-30/10**, ritorno e annullamento con Excel da lanciare sul PC (sezione 0) |

### AU5 (resto). La demo attraverso i flussi

- **Perche'**: i flussi dell'app sono collaudati con un Ambiente finto; straordinario, schede, report, riapertura,
  dismissione, parere di A4, A7, diagnosi e sblocca sono scritti ma non coperti dalla demo (18.2, F5).
- **Cosa fare**: `Demo_W1_W2/esegui_demo.py` attraverso i flussi con appunti simulati: A1 con i recinti, A1 in due
  parti, correzione dopo un fermo.
- **Fatto quando**: la demo passa dai flussi e le voci `[~]` e `[ ]` di F5 in 18 diventano `[x]`.
- **Impegno**: circa 1 giorno.

## 5. Quantificazione per i rischi piu' rilevanti

### Q1. Nota di metodo e prototipo di probabilita' e impatto quantitativi

- **Perche'**: per i 3-5 rischi piu' rilevanti (AGIRE ORA o primi per score) una stima in euro e in frequenza annua da'
  un ancoraggio alla scala 1-5 e un confronto per il comitato. Serve a **calibrare e sfidare** gli score, non a
  sostituirli; e' collegata alla regola 7 della rubrica (fatti e stime separati, D-36) e alla decisione aperta A-12.
  La Probabilita ha descrittori di plausibilita' (D-52): una frequenza stimata servira' a tararli.
- **Basi possibili**:
  - A. **analisi di scenario** (ICAAP e Pillar 2): 2-3 scenari per rischio, esperti tarati con Delphi e un
    challenger, frequenza Poisson, severita' lognormale dai percentili "1 in 10" e "1 in 40 anni", Monte Carlo;
  - B. **dati esterni riscalati** sulla Banca: ORX, sanzioni pubbliche, IMF GFSR aprile 2024 (cyber), IBM Cost of a
    Data Breach, ECB Cyber Resilience Stress Test 2024, incidenti gravi DORA, stress test EBA;
  - C. **frequenze di base dai peer**; per i rischi senza storia analoghi di altri settori e quasi-incidenti;
  - D. **modelli per cause**: FAIR per cyber, AI e terze parti; reti bayesiane aggiornate nel ciclo di valutazione,
    non fra un ciclo e l'altro (D-41);
  - E. **ancoraggio** in % del CET1 o dell'utile operativo e giorni di interruzione; uso per Pillar 2 e ICAAP, non per
    Pillar 1; reverse stress test.
- **Principio**: i numeri li danno gli esperti; A1 porta evidenze e analoghi, non cifre; il calcolo lo fa il codice.
  Se il valore quantitativo e lo score 1-5 divergono di piu' di una fascia, decide il validatore.
- **Cosa fare**: una nota di metodo di una pagina da far approvare alla funzione di rischio; poi un prototipo su 1-2
  rischi della demo (cyber, terze parti) con Monte Carlo nello script, risultato nelle schede accanto agli score.
- **Fatto quando**: la nota e' approvata e il prototipo produce perdita attesa, P99 e P99,9 con la fascia di Impatto
  corrispondente.
- **Impegno**: nota 1-2 giorni; prototipo 3-5 giorni; la raccolta delle stime degli esperti e' lavoro della Banca.

## 6. Grafici e report

Tutti i grafici del registro nascono in `03_Excel/genera_dashboard.py`, ciascuno nella funzione del suo foglio
(Storico, Delta, Notizie, Radar di Mosca con `grafico_radar`, storia di un KRI negli Indicatori, Classifica e lente di
Mosca); quelli delle schede in `07_Senza_Studio/schede.py`. C'e' uno stile comune (costanti dei colori,
`stile_grafico()`, `etichette_valore()`, `titolo_da_cella()`, `chip_urgenza()`, `legenda()`); dimensioni e posizioni
restano dentro ogni funzione. Il collaudo verifica i **dati** dei grafici, non l'aspetto. Ordine consigliato: G1, G3,
G2, poi i difetti di G5.

### G1. Isolare i parametri dei grafici

- **Cosa fare**: una tabella `GRAFICI` all'inizio di `genera_dashboard.py`, una voce per grafico (foglio, ancoraggio,
  dimensioni, titolo, legenda, colori delle serie, scala degli assi, scala delle bolle, testi degli anelli); le
  funzioni dei fogli leggono da li'.
- **Fatto quando**: il template rigenerato e' identico a prima e ogni parametro visivo e' nella tabella.
- **Impegno**: circa mezza giornata.

### G3. Script di anteprima dei grafici

- **Cosa fare**: `03_Excel/anteprima_grafici.py [file.xlsx]` che apre il file in sola lettura, ricalcola ed esporta in
  PNG tutti i grafici, compresa la storia di un KRI a scelta. Default: il template appena generato.
- **Fatto quando**: un comando produce una cartella di immagini, una per grafico, senza modificare il file.
- **Impegno**: basso.

### G2. Documentare come modificare ed estendere i grafici

- **Cosa fare**: `03_Excel/grafici_come_modificarli.md`: i tre livelli (cosa mostra, quali dati entrano, come
  appare); ricette (colori e dimensioni, scala di un asse, una serie in piu', un grafico nuovo, un intervallo dinamico
  con un nome OFFSET); le trappole gia' incontrate (overlay di titolo e legenda, assi eliminati da openpyxl,
  `varyColors`, linee smussate, colonne nascoste e `visible_cells_only`, #N/D invece di zero, anagrafica senza righe
  vuote); come verificare (rigenerare, G3, collaudo). Dopo G1.
- **Fatto quando**: un manutentore che non ha scritto il generatore cambia il colore di una serie e aggiunge un
  grafico seguendo solo il documento.
- **Impegno**: basso.

### G5. Difetti estetici noti

| Dove | Difetto | Idea di soluzione |
|---|---|---|
| Storico | voci vuote in legenda per le righe libere dell'anagrafica | nascondere la legenda ed etichettare l'ultimo punto di ogni linea, o serie dinamiche |
| Radar di Mosca | con molti rischi nello stesso settore e margine simile i cerchi possono toccarsi (piu' probabile con un rischio per meccanismo, D-55) | spostamento radiale alternato per i rischi adiacenti |
| Quadro, matrice piccola | con sei o piu' rischi nella stessa cella l'ultima riga di numeri puo' essere tagliata | "n rischi" oltre una soglia, con rimando alla Matrice |
| Quadro e Delta | l'altezza delle righe con testi calcolati e' stimata contando i caratteri | misurare in Excel con una cella di appoggio non unita |

### G6. Report intermedio leggibile: rischi di A1 accanto ai rilievi dei controlli

- **Perche'**: nato dal collaudo del primo ciclo (29/09). Ridimensionato: dal 06/10 (D-71) le segnalazioni stanno sui
  rischi nella griglia di validazione e il precontrollo (D-69) scrive il messaggio per A1. Resta utile per leggere A1
  e i rilievi affiancati PRIMA della scrittura, senza aprire due JSON.
- **Cosa fare**: un comando (es. `report-intermedio --payload A1_<ciclo>.json`) che produce un Excel con un blocco per
  rischio: cio' che A1 propone accanto ai rilievi dei controlli e di A5, se usato; i rilievi sul ciclo a parte.
  Nessuna scrittura nel registro. Da decidere: se il validatore puo' correggere li' i valori, e con quale traccia.
- **Fatto quando**: il report si genera con un comando solo e mostra ogni rischio con i suoi rilievi a fianco.
- **Impegno**: basso.

## 7. Pulizia residua

| # | Voce | Stato |
|---|---|---|
| M1 (c) | Collaudo piu' corto: meno letture complete del registro nel gruppo `catena` (oggi circa 40-60 minuti in parallelo; il gruppo `catena` resta in sequenza e da solo dura quasi tutto) | aperta |
| M4 (resto) | Cartelle del codice (`07_Senza_Studio`, `09_Copilot_Studio`) da unire: doveva farlo l'installatore, che non l'ha fatto; `installa.cmd`, la guida e `AGGIORNAMENTO_IN_BANCA.md` puntano a `07_Senza_Studio`. Conviene solo insieme a un pacchetto che cambia comunque i percorsi | aperta, bassa priorita' |

## 8. Questioni aperte emerse dal lavoro

Piccole, da decidere quando capita l'occasione:
- conseguenze dei tre livelli di allerta (D-63: chi fa cosa, entro quando), da decidere con la funzione di rischio;
- taratura delle soglie del livello di allerta, dei descrittori e dei parametri del radar (capienza, soglie, D-79)
  con A-12, dopo il ciclo 2026Q4 reale;
- la Y di Mosca conta le azioni del periodo di valutazione del rischio (D-75), non quelle ancora aperte dei cicli
  prima;
- `sogliaDelta` colora solo il Delta; il nome `rmPxI` non e' usato;
- i flag di A3 citano "il descrittore", che A3 non ha nel prompt (si risolve con P1).

### Revisione dell'intera procedura per ridurne la complessita' (richiesta del 13/10/2026) — IMPORTANTE, dopo la prova in Banca

- **Perche'**: il 13/10 l'allineamento al pacchetto ha richiesto molti giri a vuoto: script e kernel di versioni diverse
  (messaggi "e' della versione ..."), `configurazione.json` perso alla sostituzione della cartella, registro che risultava
  vuoto e poi con i dati di esempio del template, baseline lette da posti diversi (`trimestrale` la ricostruisce dal registro,
  `precontrollo` la legge da un file), raccolta notizie scritta fuori da `News_Inbox`, errori tecnici senza indicazione del
  punto. Ogni passo manuale e' una possibile deriva fra file.
- **Gia' fatto**: installatore che aggiorna senza perdere `configurazione.json`, con versione del pacchetto e impronte di
  kernel e agenti (D-89); Verifica del PC (M3) su ambiente, configurazione, kernel, template e registro chiuso; app che
  guida il giro A1 -> precontrollo -> A5 -> trimestrale -> validazione (D-83); baseline non piu' nella knowledge (AU7).
- **Cosa resta** (analisi, non ancora sviluppo): a) elencare i passi manuali e i file che devono coincidere fra PC,
  SharePoint e Agent Builder rimasti dopo l'app, e togliere quelli eliminabili; b) estendere la Verifica del PC al
  contenuto del registro (ciclo, numero di rischi, assenza dei dati di esempio); c) un controllo che rifiuti un registro
  con gli id di esempio; d) mostrare nei messaggi di `baseline` e `trimestrale` quale registro e quale ciclo stanno usando.
- **Fatto quando**: una persona che parte da un PC pulito arriva al primo `trimestrale` senza consultare piu' di una
  pagina di istruzioni e senza passaggi manuali di allineamento fra file.
- **Impegno**: analisi circa mezza giornata, poi le voci che ne escono.

## 9. Fatto

Una riga per voce realizzata; il dettaglio e' nella decisione e nell'HANDOFF.

| Voce | Cosa | Quando | Decisioni | Dove vive |
|---|---|---|---|---|
| S1 | Semplificazione dello scoring di A1: niente controlli della Banca ne' esito in A1, Velocity facoltativa, KRI senza soglie, Impatto, rilevanza delle fonti, livello di allerta, due KRI per tipo | 30/09-01/10 | D-49...D-65 | rubrica, schemi, guida; analisi `Archivio/11` (restano i passi B in Banca) |
| G4 | Migrazione del registro su un template nuovo: comando `aggiorna-registro` con il controllo di versione | 25/09 | D-34 | guida, sezione 0-bis |
| AU1 (parte) | Comando `report`: PDF del report al comitato, rilanciabile | 30/09 | D-62 | guida, sezione 9 |
| AU2 (parte) | Messaggio di correzione per A1 dal precontrollo e da `trimestrale` | 02/10-06/10 | D-69, D-70, D-71 | `precontrollo.py` |
| Agenti nuovi, fase 1 | A7 Assistente del registro, fenomeni non censiti, Note dell'analista | 07/10 | D-72 | guida, sezioni 4 e 8 |
| P8 / fase 2 | Lista di osservazione | 07/10 | D-73 | **sostituita** dal registro unico (D-79) |
| P3 / fase 3 | Ciclo straordinario `AAAAQn-Sk`, con la proposta di A3 e A4 | 07/10 | D-75 | guida, sezione 2-bis |
| Fase 4 | Modifiche fra un ciclo e l'altro: riapertura della validazione e testi a mano (al posto del foglio Manutenzione, la cui anteprima e' stata cancellata l'08/10) | 07/10 | D-76 | guida, sezione 3-ter |
| Fase 5 | A8 Evento critico, analisi dell'evento, straordinario di solo censimento | 07/10 | D-77 | guida, sezione 2-bis |
| M1 (a, b) | Collaudo in gruppi paralleli e `--mirato` | 08/10 | D-78 | `99_Collaudo/LEGGIMI_collaudo.md` |
| M2 | Regola su quando rigenerare la demo | 07/10 | — | PROMPT_MASTER, sezione DEMO |
| M3, M5 | Cartella `Anteprima_S1`, zip superati e script temporanei eliminati | 07/10 | — | — |
| M4 (documenti) | Documenti di riferimento in `04_Riferimenti` | 08/10 | D-78 | 00_LEGGIMI |
| P13 (1, 2) | Comando `diagnosi`; anni di adeguamento dei rischi in osservazione con Impatto 4-5 | 19/10 | D-80 | guida, sezione 9; guida di scrittura di A1; analisi 17, 17.10 |
| P13 (3a) | Esposizione della Banca "non nota": nota di A1 nel razionale, segnalazione C5 da motivare, decide il validatore | 19/10 | D-81 | guida, sezione 3; guida di scrittura di A1; analisi 17, 17.10 |
| AU7 | Baseline in input ad A3 e A4 come allegato della chat (`Input_A3_A4.txt`), non piu' dalla knowledge: niente copia di `Baseline_corrente.txt` nella library Kernel | 23/10 | D-83 | guida, sezioni 0.2, 1, 2 e 8; `input_a1.py` |
| AU1 (scrittura robusta e automatismi) e lucchetto | Piu' analisti: lucchetto nell'archivio condiviso, copia di lavoro del registro con l'impronta, Salvataggio automatico spento, `sblocca`; report da `valida`, prompt archiviati, PDF delle schede, traccia della riapertura | 23/10 | D-83 | guida, sezioni 0.3, 3, 7 e 9; `lucchetto.py` |
| AU4 | Scelta della strada: A su `main`, tutto in Copilot Studio sul ramo `copilot-studio-pieno` | 23/10 | D-83 (chiude A-15 e A-16) | `CLAUDE.md`, DECISIONI |
| P10 | Registro unico: nel radar i primi (Prossimita e Probabilita almeno 2, capienza 15 fino a 20, eccezioni), gli altri in osservazione; un solo modulo per la regola | 08/10 | D-79 | rubrica sezione 9, Parametri righe 65-75, guida; analisi `13_Scala_unica.md` |
| AU2 | Ingresso unico delle risposte (appunti e file), stato del processo, esecutore del motore, messaggi di correzione per A3, A5, A6 (tappa M2) | 23/10 | D-83 | `ingresso.py`, `stato.py`, `esecutore.py`; analisi 18.2 |
| AU5 (parte) | La finestra dell'app al posto della procedura a menu: flussi di ogni processo, appunti, link degli agenti, riquadro "Risposta dell'agente" (al posto di `NFR_incolla.cmd`); resta la demo (sezione 4) | 23/10 | D-83 | `app_nfr.py`, `flussi.py`, `appunti.py`; guida, "L'app NFR" |
| AU3 | Installazione con un doppio clic e Verifica del PC (tappa M3); aggiornamento sopra un pacchetto installato | 29-30/10 | D-89 | `installa.cmd`, `verifica_pc.py`; guida, sezione 0.3 |
| Tappa M4 | Report al comitato in HTML, seconda uscita di `report` e `valida`, con il cancello su Excel | 29/10 | D-83 | `report_html.py`; guida, sezione 4 |
| Tappa M5 | Funzioni amministrative in modalita' Admin: pulizia, ritorno a un ciclo validato, ripartenza, annullamento | 29/10 | D-85 | `amministrazione.py`; guida, 3-quater |
| Aiuto nell'app | Pulsante Aiuto (F1) e suggerimenti sui pulsanti, letti dalla guida | 29/10 | — | `aiuto.py` |
| P14 (lunghezze) | Lunghezze minime dei testi e controllo C10 per A1 e A8; testi piu' lunghi per A6 e A4 | 29/10 | D-86, D-88 | guida di scrittura di A1, `controlli_a5.py`, `schede.py` |
| A7 in prima persona | A7 risponde come autore delle valutazioni | 29/10 | D-87 | modello di A7 |
| Testi a mano in Admin | Con copia del registro e atto; il report si rifa' a fine correzione | 30/10 | D-90 | `amministrazione.py`; guida, 3-ter |
| A-11 e PROMPT_MASTER | Variante Power Automate archiviata, parti vive spostate; PROMPT_MASTER allineato a D-83 | 30/10 | D-91 | `struttura_e_liste.md`, `controlli_e_model_risk.md` sezione 7, `Analisi_Architettura/Archivio` |

### 9-bis. Superate

Voci chiuse senza farle, perche' una decisione le ha rese inutili. Il contenuto resta dove dice l'ultima colonna.

| Voce | Perche' | Dove resta |
|---|---|---|
| B5, B5.1-B5.9: prove della CS-1 | su `main` non decidono piu' nulla: A-15 e' chiusa (D-83) | ramo `copilot-studio-pieno`, `09_Copilot_Studio/TODO_Copilot_Studio.md`; protocollo in `09_Copilot_Studio/Prove_CS1.md`, esiti di K0 in `Prova_con_Copilot_Studio.md` |
| B5.10: prova K14 del report HTML | A-16 chiusa da D-83: niente variante V4; il report HTML e' fatto (M4) e si prova con B5-bis | `Analisi_Architettura/16_Report_HTML.md`, 16.9 |
| AU6: variante CS-1 con il motore in background | D-83 | `Analisi_Architettura/Archivio/10`, 10.12 e 10.15 |
| AU1: copia della baseline nella cartella `kernel` | sostituita da AU7 | D-83 |
| AU2: coda delle richieste | serviva alla CS-1; scelta dell'utente del 23/10 | `Analisi_Architettura/Archivio/10` |
| Variante CS-2 in riserva | sostituita dal ramo `copilot-studio-pieno` (D-82) | `Analisi_Architettura/15_CS2_approfondita.md` |

## 10. In riserva (non pianificate)

Non sono voci di lavoro. Si riprendono solo se cambia la condizione indicata.

| Voce | Cosa e' | Quando riprenderla |
|---|---|---|
| Piano 07, Power Query senza Python (`Analisi_Architettura/Archivio/07`) | controlli e consolidamento in Excel con Power Query; Python solo al manutentore. Era la voce AR1, chiusa da D-43 | se la Banca vietasse Python sul PC |
| Foglio Manutenzione (anteprima del 07/10 cancellata l'08/10; disegno in D-76 e nell'HANDOFF, sezione 2-unvicies) | una riga per campo da cambiare fra un ciclo e l'altro, al posto della riapertura | se le modifiche fra un ciclo e l'altro diventano frequenti |
