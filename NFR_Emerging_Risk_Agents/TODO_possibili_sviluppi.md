# TODO — lavoro da fare

Il piano unico del lavoro ancora aperto. Ogni voce dice perche' serve, cosa fare e come capire che e' fatta. Quando
una voce e' realizzata esce dalla sua sezione e diventa una riga di **"Fatto"** (sezione 9), con la decisione e il
documento dove vive; il dettaglio di come e' stata fatta sta in `04_Riferimenti/DECISIONI.md` e nell'HANDOFF.

Riordinato l'08/10/2026 sera: prima le voci aperte, in ordine; il fatto in fondo, una riga per voce. I codici delle
voci (P, AU, Q, G, M) non cambiano, perche' DECISIONI, HANDOFF e analisi li citano.

Sezioni:
1. ordine di lavoro;
2. passi sul PC della Banca (non sviluppo: installare e provare cio' che c'e' gia');
3. processi (P1, P2, P4, P5, P6, P7, P9, P12, P13, P14, P15);
4. automazione del processo: l'app di orchestrazione (tappe M1-M4; AU1, AU2, AU3, AU5);
5. quantificazione (Q1);
6. grafici e report (G1, G2, G3, G5, G6);
7. pulizia residua (M1, M4);
8. questioni aperte emerse dal lavoro (compresa la revisione della procedura);
9. fatto;
10. in riserva.

## 1. Ordine di lavoro

Il primo ciclo vero e' il **2026Q4**, con il primo run di A1 a inizio gennaio 2027 (D-22). L'ordine mette prima cio'
che migliora quel ciclo.

| Passo | Voci | Perche' qui | Giorni |
|---|---|---|---|
| 0 | **Passi sul PC della Banca** (sezione 2): pacchetto dell'08/10 sera, `aggiorna-registro`, agenti reincollati (B1-B4); poi le **prove della CS-1** (B5) | tutto il resto si appoggia su un'installazione allineata al pacchetto; le prove decidono la A-15 | 1-2 per B1-B4; 1-2 per le prove, piu' le attese (in Banca) |
| 1 | **P4** rapporti di scenario, **P9** temi da verificare e **P14** il "so what" nei testi di A1 (AU7 fatta il 23/10, D-83; lunghezze dei testi fatte il 29/10, D-86) | piccole, migliorano subito la qualita' del trimestrale: A1 legge i rapporti di analisti e regolatori, le richieste dell'analista restano tracciate, le schede dicono che cosa significa ogni rischio per la Banca | circa 1,5 |
| 3 | **P1** segnali qualitativi per dimensione e pressione sul radar | e' il pezzo che manca di piu' al settimanale (quale rischio e quale dimensione sono sotto pressione) | 2-3 |
| 4 | **P5** rischi collegati | un evento che tocca piu' rischi resta leggibile come un insieme; con il registro unico capitera' piu' spesso | 2-3 |
| 5 | **App NFR, tappe M2-M4** (sezione 4: AU2, AU3, AU5 e report HTML; la tappa M1 e' fatta) | la strada A su `main` e' decisa (D-83): finestra che guida ogni processo, risposte dagli appunti, piu' analisti, report HTML al comitato | 13-15 |
| 7 | **P2**, **P7**, **P6** | presentazione: scia sul radar, riepilogo mensile, scheda per tema | 2-3 |
| in parallelo | **Q1** nota di metodo (il prototipo dopo il passo 4) | e' soprattutto lavoro della Banca (stime degli esperti) | nota 1-2, prototipo 3-5 |
| in parallelo | **G1, G3, G2**; **G6** quando servira' leggere A1 accanto ai controlli prima della scrittura | toccano solo il generatore o sono strumenti di lettura | circa 2 |
| sempre | **G5** difetti estetici, **sezione 8** questioni aperte | quando capitano | |

**Perche' i processi prima dell'automazione** (cambia la regola del 28/09, "P dopo AU3"). Quella regola valeva per P3,
che aggiungeva un comando alla coda delle richieste e una voce al menu: P3 e' fatta (D-75, D-77). Le voci P rimaste
cambiano schemi, prompt e viste, che valgono in tutte le strade dell'automazione: farle prima non costringe a rifare
niente. Fra le P, P4 e P9 sono piccole e servono subito al trimestrale; P1 e' la piu' utile per il settimanale; P2, P6
e P7 sono di presentazione e possono aspettare.

## 2. Passi sul PC della Banca

Non sono sviluppo: si installa e si prova cio' che il pacchetto ha gia'. Istruzioni nella guida, sezione 0-bis.

| # | Passo | Per quali decisioni | Stato |
|---|---|---|---|
| B1 | Pacchetto completo dell'08/10 sera; cancellare le vecchie `04_SharePoint`, `05_Workflow`, `06_Governance`, `08_Deploy` | D-78 | da fare |
| B2 | Copiare tutto `01_Kernel` e `04_Riferimenti\DECISIONI.md` nella library Kernel; togliere dalla library `Tassonomia dei Rischi.csv` (dal 09/10 in `04_Riferimenti`, non lo legge nessun componente) | D-74, D-77, D-79 | da fare |
| B3 | Reincollare in Agent Builder A1, A3, A4, A5, A6, A7; creare A8 (guida, 0.2) | D-68...D-79 | da fare |
| B4 | `aggiorna-registro`, prima su una copia e poi sul registro in uso (struttura 2026-10-09: le voci della lista di osservazione diventano rischi in osservazione; i codici di Basilea vanno riclassificati da A1 al primo ciclo) | D-74, D-79 | da fare |
| B5 | **Prove di fattibilita' della CS-1**, dopo B1-B4, nell'ordine sotto. Protocollo unico: `09_Copilot_Studio/Prove_CS1.md`, con i tempi, i testi da mandare, i comandi e la tabella dei risultati | A-15 fra le tre strade (`Analisi_Architettura/14_Tre_strade.md`, 14.9) | pronte dal 09/10 |
| B5.1 | **D1 e D2**: domande all'IT (PC esecutore, avvio automatico, connessione di servizio dei flussi, Office Scripts) e alla compliance (trascrizioni di Copilot Studio, etichette di riservatezza). Si possono mandare subito, anche prima di B1 | un no ferma la CS-1 | da fare |
| B5.2 | Preparazione: registro di prova rifatto con la parte 2 di `04_Riferimenti/Prove/Prova_senza_Copilot_Studio.md`, configurazione **senza la riga `kernel`**; due run di A1 in Agent Builder (`A1_AB_run1.json`, `A1_AB_run2.json`); cartelle `Archivio_Cicli\Prova_K0\In_arrivo`, `Esiti`, `Spiegazioni` | base di confronto di K4 | da fare |
| B5.3 | **K6** Operatore a passi fissi, compreso K6.5 in Teams (`09_Copilot_Studio/Prova_K6_Operatore.md`) | il cuore della CS-1 | da fare |
| B5.4 | **K4** qualita' di A1 in Copilot Studio: `confronta.py` AB/AB, CS/CS, AB/CS; precontrollo al primo giro; modello | D-21 | da fare |
| B5.5 | **K11** piu' utenti, con un collega: identita' nel flusso, connessione dei flussi, lancio simultaneo, trascrizioni | multiutenza (14.5-bis) | da fare |
| B5.6 | **K12** A7 come sotto-agente: risposte dai file di `Spiegazioni`, tempo di aggiornamento dopo una riscrittura | consultazione da altri utenti | da fare |
| B5.7 | **K7a** sincronizzazione SharePoint <-> PC (`99_Collaudo/osserva_cartella.py`), con e senza "Mantieni sempre su questo dispositivo"; conflitto con il registro aperto sul web | tempi e sicurezza della scrittura | da fare |
| B5.8 | **K7b** Excel senza nessuno davanti: schermo bloccato, avvio automatico, senza accesso, Excel gia' aperto | PC esecutore | da fare |
| B5.9 | Facoltativo, per la CS-2: prova K0 ripetuta con file allineati (`09_Copilot_Studio/Prova_con_Copilot_Studio.md`: T1.2 con l'impronta, T1.3). Prima tornata del 09/10: opzione 1 funziona (T1.1, T1.2, T1.4 rifiutata), T1.3 una volta in errore, opzione 2 non disponibile in Banca, salvataggio in SharePoint riuscito con impronta uguale | D-70; CS-2 | parziale |
| B5.10 | Facoltativo, per A-16: **K14** report HTML (`Analisi_Architettura/16_Report_HTML.md`, 16.9): apertura da SharePoint in Edge, "Convert file" su HTML, zip dal code interpreter, report nella knowledge di A7. Si usano i file di `Analisi_Architettura/16_Anteprima_HTML/` | A-16 | da fare |
| B9 | **Copilot Studio pieno** (D-82, ramo `copilot-studio-pieno`): costruzione e prove T0-T8 di `09_Copilot_Studio/Copilot_Studio_pieno.md`, nell'ordine. Prima T0 (Office Scripts, code interpreter nei prompt, domande all'IT), poi T1-T3 (agente, flussi, A1 e A8, correzione dai file), poi **T4 (K9)** e **T5 (K8)**, che decidono la strada del motore (V2, F2, V1 o A-15). Sostituisce per questo ramo B5.3 (K6), B5.9 e la parte K8/K9 della CS-2. **23/10**: T0.1 e T0.2 si', T4.1 (K9) negativo, T5.1, T5.2 e K8-bis riusciti: strada **V1** (motore in TypeScript con Office Scripts); prossimo passo il precontrollo in TypeScript con collaudo sotto Node contro il Python (HANDOFF 2-tretricesies) | versione senza Python sul PC | in corso |
| B5-bis | Tappe M1 e M2 dell'app (23/10): copiare `07_Senza_Studio` (file nuovi `lucchetto.py`, `NFR.cmd`, `app_nfr.py`, `flussi.py`, `stato.py`, `ingresso.py`, `appunti.py`, `esecutore.py`); in `configurazione.json` le voci della guida, sezione 0.3 (`utente`, `validatore_predefinito`, `raccolta_su_questo_pc`, `agenti`, `ascolta_appunti`, `link_agenti`); cancellare il prompt schedulato di A3; un trimestre di prova dall'app (doppio clic su `NFR.cmd`): copia dagli appunti di una risposta lunga di A1, giro di correzione, validazione; reincollare A3, A4, A5, A6 e A8 (D-84, nomi degli allegati); togliere `Baseline_corrente.txt` dalla knowledge di A3 e A4 e dalla library Kernel; prova del lucchetto con un collega (V-F e lucchetto fra due PC, `Analisi_Architettura/Archivio/10`, 10.5). Le prove CS-1 di B5 restano utili solo al ramo `copilot-studio-pieno` | D-83 | da fare |
| B6 | Prova di A7 (`04_Riferimenti/Prove/Prova_A7.md`) | D-72 | da fare |
| B7 | Ciclo 2026Q4 di prova (prima del ciclo vero): converge in 1-2 giri A1, senza A5 o con A5 | S1 (D-49...D-56), D-69, D-71 | da fare |
| B8 | Facoltativo, per A-17: **K15** contraddittorio senza codice sul ciclo 2026Q4 (`Analisi_Architettura/17_Decimo_uomo.md`, 17.8): A9 in Agent Builder dopo A1, piu' la variante 2b nella chat di A1; il validatore giudica ogni tesi utile, gia' nota o rumore | A-17 | da fare |
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
- **Tocca**: `fonti.md` (e `fonti.py`), guida di scrittura di A1 (il prompt e' a 7.989 caratteri: l'istruzione va
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
- **Cosa fare**, uno per volta su richiesta dell'utente (19.11): scale a 6 livelli e registro nuovo (A-19); prova K15
  con il mandato esteso (A-17); pavimento di evidenza con la prova C (A-20); driver per prevalenza, SOV e NOR, "agisce
  su", casi reali nella scheda (A-24); fonti di orizzonte e natura della fonte (A-22); residuo (A-21); STOP morbidi
  (A-23).
- **Impegno**: circa 4-6 giorni per le scale, poi da mezza giornata a 4 giorni per voce (19.11).

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
  Registro e Radar_Mosca, prompt A3 (7.599 caratteri) e A4, controlli e collaudo. Nessun principio da cambiare.
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
  Registro, schede (A6 e `schede.py`), collaudo. Prompt A1 a 7.989 caratteri: le istruzioni vanno nella guida di
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

## 4. Automazione del processo (piano `Analisi_Architettura/Archivio/10`)

Oggi un trimestre chiede circa 13 passi manuali (9 comandi da scrivere, 3 salvataggi in Blocco note, copie a mano);
una settimana circa 7 (piano 10, 10.1). Obiettivo: niente copia-incolla, gli agenti fanno il piu' possibile, ogni
azione rimasta si lancia con un doppio clic o un messaggio.

Punti fermi:
- **Python resta il motore** (D-43); il piano 07 e' in riserva (sezione 10).
- **Copilot Studio e Power Query sono disponibili** nel tenant (D-44); **usare Copilot Studio non e' deciso**: e' la
  decisione aperta A-15, da prendere con AU4. Dal 09/10 l'analisi ha **tre strade**
  (`Analisi_Architettura/14_Tre_strade.md`): A, app Python sul PC (AU1-AU5); CS-1, ibrida con un PC esecutore (AU6);
  CS-2, tutto in Copilot Studio senza Python sul PC, che e' l'obiettivo dichiarato dall'utente il 09/10. Si
  decide dopo le prove K6, K8 (Office Scripts) e K9 (code interpreter su compiti lunghi). Dall'11/10 la CS-2 e'
  approfondita in `Analisi_Architettura/15_CS2_approfondita.md`: raccomandata la variante V2 ("Python decide, Excel
  esegue"), a tappe dopo la CS-1. Le tappe sono: adattatore del registro nel motore, esecutore in Office Script
  (prova K8), motore nel prompt con code interpreter (K9) e PDF (K10). Dal 14/10 c'e' la variante **V4**
  (`Analisi_Architettura/16_Report_HTML.md`, decisione aperta A-16): report HTML generato da Python al posto delle viste
  di Excel e registro come file di dati senza formule; vale in tutte le strade e nella CS-2 sostituirebbe la V2 (niente
  Office Scripts). Si decide dopo la prova K14 (B5.10) e la tappa T2.
- **Dal 23/10, sul ramo `copilot-studio-pieno`**, c'e' il progetto della versione tutta in Copilot Studio (D-82): agente con un argomento per comando, comunicazione via file in SharePoint e variabili globali, flusso `NFR_Motore` come interfaccia unica del motore, V2 con le riserve F2 (senza Office Scripts) e F1. Prove T0-T8 in `09_Copilot_Studio/Copilot_Studio_pieno.md` (voce B9).
- **Separare chi chiede da chi esegue**: nella strada A la richiesta la scrive il menu, nella CS-1 un flusso di
  Copilot Studio; tutto cio' che sta dietro la richiesta e' identico.
- Qualunque strada: nel registro scrive solo il motore, dopo i controlli (D-10); kernel, schemi, controlli,
  validazione e collaudo non cambiano.

**Dal 23/10/2026 (D-83) la strada e' decisa**: su `main` la strada A, cioe' agenti in Agent Builder e un'app Python
di orchestrazione sul PC; la versione tutta in Copilot Studio vive sul ramo `copilot-studio-pieno` (D-82). Le voci AU4 e
AU6 non servono piu' su `main`. Il piano dell'app, approvato dall'utente, e' a quattro tappe, piu' la M5 aggiunta il 23/10. **L'avanzamento voce per voce, con le spunte (fatto, da verificare, da fare), e' in `Analisi_Architettura/18_App_orchestrazione.md`**; qui solo il riassunto:

| Tappa | Cosa | Moduli | Stato |
|---|---|---|---|
| M1 | motore: lucchetto per piu' analisti, copia di lavoro del registro, Salvataggio automatico spento; AU7; automatismi di AU1 (report da `valida`, prompt archiviati, PDF delle schede, traccia della riapertura) | `lucchetto.py`, `esegui_ciclo_locale.py`, `input_a1.py`, `excel_com.py` | **fatta il 23/10** |
| M2 | l'app: ingresso unico delle risposte (appunti e file), stato del processo, esecutore del motore, flussi di ogni processo, finestra tkinter (AU2, AU5) | `ingresso.py`, `appunti.py`, `stato.py`, `esecutore.py`, `flussi.py`, `app_nfr.py`, `NFR.cmd` | **fatta il 23/10** (collaudata senza Excel con un Ambiente finto; resta la prova a mano con gli agenti veri, B5-bis, e la demo attraverso i flussi) |
| M3 | installazione con un doppio clic e Verifica del PC (AU3) | `installa.cmd`, `installa.py`, `installazione.py`, `verifica_pc.py`, `notizie_manuali.py` | **fatta il 29/10** (collaudata senza Windows: `test_installazione.py`; restano le prove sul PC della Banca: pip dietro il proxy, schtasks, collegamenti, Excel via COM); il 30/10 anche l'aggiornamento sopra un pacchetto installato (D-89: versione, `.cmd.txt`, kernel nella library, obsoleti, agenti da reincollare), da provare in Banca su una copia sopra il pacchetto del 23/10 |
| M4 | report HTML al comitato come seconda uscita di `report`: viste, grafici e schede di tutti i rischi dal prototipo dell'analisi 16, numeri controllati contro Excel | `report_html.py` | **fatta il 29/10** (collaudata senza Excel sul registro della demo: `test_report_html.py`; la lettura via COM e il cancello con Excel sono nella catena, da lanciare sul PC) |
| M5 | funzioni amministrative (richiesta del 23/10): pulizia dell'archivio dei cicli, ritorno indietro di N trimestri (registro dall'Excel validato del ciclo scelto), ripartenza da zero; niente si cancella subito, tutto nel parcheggio con l'atto; da decidere chi puo' farlo | `amministrazione.py`, voce Amministrazione dell'app | **fatta il 29/10** (collaudata senza Excel: `test_amministrazione.py`; ritorno e annullamento con Excel nella catena, da lanciare sul PC; chi puo' farlo: modalita' Admin, D-85) |

Scelte dell'utente: finestra tkinter; risposte dagli appunti piu' il file; piu' analisti sullo stesso registro; niente
coda delle richieste (serviva alla CS-1). Le voci AU1, AU2, AU3 e AU5 qui sotto restano come dettaglio di cio' che le
tappe realizzano.

### AU1. Motore: automatismi e scrittura robusta (piano 10: C2 e C3)

- **Perche'**: spariscono passi a mano del trimestre (baseline copiata in `Kernel`, prompt copiati nell'archivio), e
  la scrittura resta pulita anche con il registro in una cartella OneDrive: il Salvataggio automatico potrebbe salvare
  righe scritte prima di un fermo (rischio trovato il 27/09, forse la causa di `RPC_E_DISCONNECTED`).
- **Cosa fare**:
  - *fatto il 23/10 (D-83, tappa M1): scrittura robusta, prompt archiviati, report da `valida`, PDF delle schede; la
    copia della baseline in `kernel` non serve piu' (AU7)*;
  - **scrittura robusta (passo 2 dell'ordine)**: `wb.AutoSaveOn = False` subito dopo l'apertura;
    `registro_in_lavoro(conf)` per `trimestrale`, `settimanale`, `valida`, `riapri` e `dismetti`: copia di lavoro
    locale, scrittura e controlli sulla copia, sostituzione solo se l'originale non e' cambiato nel frattempo;
  - `_scrivi_baseline` copia anche `Baseline_corrente.txt` nella cartella `kernel` configurata (non quando `kernel`
    e' la `01_Kernel` del pacchetto: collaudo e demo);
  - `trimestrale` archivia i prompt generati in `Cicli/<ciclo>/Prompt_in_uso/`;
  - `valida` lancia `report` per i trimestrali (il comando `report` c'e' dal 30/09, D-62); `schede` esporta anche
    `Schede_<ciclo>.pdf`. Un errore nel PDF e' solo un avviso.
- **Tocca**: `esegui_ciclo_locale.py`, `excel_com.py`, `schede.py`, `Demo_W1_W2/esegui_demo.py`, `run_catena.py`,
  guida, `04_Riferimenti/controlli_e_model_risk.md`.
- **Fatto quando**: la catena di collaudo prova il caso "registro cambiato nel frattempo", produce i due PDF, trova la
  baseline in `kernel` e i prompt archiviati; la demo e' rilanciata.
- **Impegno**: circa 2 giorni (la scrittura robusta circa 1).

### AU2. Ingresso unico, stato del processo e coda delle richieste (piano 10: C4-C7)

- **Perche'**: tutte le risposte degli agenti entrano da un solo posto, `Archivio_Cicli\In_arrivo\`, che vengano dagli
  appunti (strada A) o da un flusso (CS-1). Ogni azione del motore diventa una richiesta controllata. Serve in
  entrambe le strade.
- **Cosa fare**:
  - `07_Senza_Studio/ingresso.py`: `estrai_json` (toglie BOM e recinti ```json, trova il JSON in mezzo al testo, se e'
    troncato unisce le parti successive); `riconosci_agente` dai campi `required` degli schemi; nomi dei file e
    controllo di schema subito; `messaggio_correzione` esteso agli altri agenti e ai fermi di `settimanale` e `schede`
    (per A1 c'e' dal 02/10, D-69, in `precontrollo.py` dal 05/10, D-70; per `trimestrale` dal 06/10, D-71); conserva
    il testo originale;
  - `stato(conf)`: stato del processo e prossimo passo, senza Excel, anche in `Esiti/Stato_processo.json`;
  - esecutore del motore in un sottoprocesso: fasce OK / FERMATO / ERRORE TECNICO, `Esiti/Esito_<id>.json`, log in
    `Archivio_Cicli/Log`;
  - coda delle richieste: `01_Kernel/schema_richiesta.json`; lista bianca `baseline`, `precontrollo`, `trimestrale`,
    `settimanale`, `valida`, `riapri`, `schede-input`, `schede`, `report`; validatori ammessi in
    `configurazione.json`; `inizializza`, `dismetti` e `aggiorna-registro` solo da riga di comando;
  - `02_Agenti/modelli/A3.md`: una riga ("le notizie possono arrivare anche come allegati o nel testo della
    richiesta"), poi `componi_prompt.py` e ricaricare A3.
- **Fatto quando**: i test senza Excel sono verdi (estrazione da testi reali, riconoscimento e nomi, stato calcolato
  da archivi finti, richieste fuori lista o con un validatore non ammesso rifiutate); A3 resta sotto gli 8.000
  caratteri.
- **Impegno**: circa 3 giorni.

### AU3. Installazione con un doppio clic e Verifica del PC (piano 10: C8)

- **Perche'**: i blocchi della prima installazione del 24/09 erano di questo tipo (`.json.txt`, `Workbook non trovato:
  None`, pythoncom a meta', proxy). Il PC che esegue il motore si installa allo stesso modo in entrambe le strade.
- **Cosa fare**: `installa.cmd` + `installa.py`, ripetibili: controllo di Python e dei moduli, `pip install --user`
  solo di cio' che manca (messaggio chiaro se il proxy blocca); `configurazione.json` compilato con finestre di
  dialogo; `attrib +P` sulle cartelle sincronizzate; Verifica del PC (moduli, Excel via COM, `AutoSaveOn` e
  `FullName` del registro) riga per riga in verde o rosso, con un file da mandare al manutentore. Con l'installatore
  si uniscono anche le cartelle del codice (M4).
- **Fatto quando**: `installa.cmd` su una cartella di prova produce una configurazione valida e la Verifica e' tutta
  verde; la guida, sezione 0, e' riscritta.
- **Impegno**: circa 1 giorno.

### AU4. Scegliere la strada: A (procedura guidata) o CS-1 (Copilot Studio) — decisione A-15

| | Strada A | Variante CS-1 |
|---|---|---|
| Cosa fa l'analista | menu al PC; per ogni agente trascina i file, incolla la richiesta, preme Copia | un messaggio in Teams e dei pulsanti; nessun gesto per agente |
| Raccolta notizie | sul PC (proxy, `pypac`, attivita' pianificata) | flusso nel cloud |
| Python | sul PC dell'analista | su un solo PC esecutore, in background |
| Lavoro dopo la parte comune | 3-4 giorni | 13-15 giorni |
| Cosa si aggiunge da mantenere | niente | Operatore, argomenti, flussi e sotto-agenti in Copilot Studio, piu' la soluzione esportata |
| Nuove verifiche e pareri | V-A..V-G (piano 10, 10.5) | V-H..V-Q (10.18): DLP, modello, trascrizioni (parere DPO), sincronizzazione |
| Agenti | quelli di oggi, in Agent Builder | da ricreare; la qualita' si rimisura con il doppio run |

- **Come scegliere**: **CS-1** se piu' analisti useranno il sistema, se si vuole lavorare da Teams senza stare al PC
  o se i gesti per agente e la raccolta sul PC si rivelano un peso; in piu' devono riuscire la prova K0 e il parere
  sulle trascrizioni. **Strada A** se il pilota resta a una persona al proprio PC (D-13), se si vuole la minima
  complessita' prima del primo ciclo vero, o se K0 o il parere non arrivano in tempo.
- **Prova K0** (passo B5.9, pronta dal 05/10, D-70): A1 in Copilot Studio sullo stesso input della prova senza Copilot
  Studio; il precontrollo dentro l'agente in due modi (Code interpreter dell'esperienza standard con lo script
  allegato, oppure skill `precontrollo-nfr` nella nuova esperienza, a consumo di crediti). Criteri nuovi: se il
  precontrollo gira dentro A1 con l'impronta verificata, il giro A1 -> PC si riduce in tutte e due le strade; i
  crediti della nuova esperienza sono un costo che la strada A non ha.

  Prima tornata del 09/10:
  - in Banca c'e' solo l'opzione 1: funziona nel riquadro di prova;
  - in Teams risponde spesso con errori, probabilmente per il limite di circa 100 KB dei messaggi;
  - il salvataggio in SharePoint dall'agente funziona: all'inizio il file finiva nel OneDrive, risolto il 09/10; il JSON arriva intero (impronta uguale a quella del file scaricato).

  Per la CS-1 questi sono i punti critici, perche' la CS-1 vive in Teams. Il 09/10 l'utente ha scelto di proseguire
  con la prova K6 (passo B5.3; tutte le prove della CS-1 nel passo B5, `09_Copilot_Studio/Prove_CS1.md`): un argomento a passi fissi, con il JSON che passa solo per i flussi.
- **Proposta, se alla fine del passo 5 la decisione non c'e'**: strada A. La CS-1 resta aggiungibile dopo, perche'
  cambia solo chi scrive le richieste.
- **Fatto quando**: A-15 e' chiusa in `04_Riferimenti/DECISIONI.md`.

### AU5. Strada A: procedura guidata a menu (solo se A-15 sceglie la strada A)

- **Cosa fare**: `07_Senza_Studio/appunti.py` (ascolto degli appunti con `win32clipboard`; cio' che si copia passa da
  `ingresso.py`); `procedura.py` + `NFR.cmd`: menu con lo stato e il prossimo passo (Invio = procedi), che scrive le
  richieste nella coda di AU2; per ogni agente prepara `%USERPROFILE%\NFR_Da_allegare\`, apre il link dell'agente,
  mette la richiesta negli appunti, aspetta la copia; per la validazione apre Excel sulla griglia del foglio
  Validazione; link degli agenti in `configurazione.json`; `NFR_incolla.cmd` con il tasto di scelta rapida (niente
  Ctrl+Alt: sulla tastiera italiana e' AltGr); "Invia a -> NFR notizie manuali"; attivita' pianificata della raccolta
  con `schtasks /create /xml`; guida riscritta attorno al menu; demo con appunti simulati.
- **Verifiche nel tenant**: V-A..V-G (piano 10, 10.5).
- **Fatto quando**: la demo passa dalla procedura con appunti simulati e la prova a mano sul PC riesce (10.6).
- **Impegno**: 3-4 giorni.

### AU6. Variante CS-1: Copilot Studio con il motore in background (solo se A-15 sceglie la CS-1)

- **Cosa fare** (piano 10, 10.12 e fasi K1-K6 di 10.15): `07_Senza_Studio/motore_in_ascolto.py` sul PC esecutore
  (parte all'accesso a Windows, esegue la coda di AU2, aggiorna `motore_attivo.json`); agent flow
  `Deposita_Risposta`, `Scrivi_Richiesta`, `Leggi_Stato`, `Leggi_File`, `Salva_Allegato`, `Archivia_Parere`, con le
  schede di costruzione in `09_Copilot_Studio/`; A1, A3, A4 e A8 come sotto-agenti, A5 e A6 come strumenti prompt con
  uscita JSON, istruzioni sempre da `componi_prompt.py`; Operatore NFR con argomenti guidati, Adaptive Card e copioni
  di collaudo con i casi ostili; cloud flow della raccolta del lunedi' (2-4 settimane in ombra con
  `raccogli_notizie.py`); regole di governo 1-6 del piano 10 in `04_Riferimenti/controlli_e_model_risk.md`; A-11
  chiusa (`04_Riferimenti/workflow.md` archiviata, sostituita da `09_Copilot_Studio`).
- **Verifiche nel tenant**: V-H..V-Q (piano 10, 10.18).
- **Fatto quando**: i copioni di conversazione sono superati due volte di fila; la demo con richieste simulate e'
  rilanciata; il primo ciclo vero passa dal doppio run e dalla validazione.
- **Impegno**: 13-15 giorni, piu' l'ombra della raccolta.

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
| M4 (resto) | Cartelle del codice (`07_Senza_Studio`, `09_Copilot_Studio`) unite con l'installatore AU3, che rifa' i percorsi in `configurazione.json` e nelle attivita' pianificate | con AU3 |

## 8. Questioni aperte emerse dal lavoro

Piccole, da decidere quando capita l'occasione:
- conseguenze dei tre livelli di allerta (D-63: chi fa cosa, entro quando), da decidere con la funzione di rischio;
- taratura delle soglie del livello di allerta, dei descrittori e dei parametri del radar (capienza, soglie, D-79)
  con A-12, dopo il ciclo 2026Q4 reale;
- la Y di Mosca conta le azioni del periodo di valutazione del rischio (D-75), non quelle ancora aperte dei cicli
  prima;
- `sogliaDelta` colora solo il Delta; il nome `rmPxI` non e' usato;
- i flag di A3 citano "il descrittore", che A3 non ha nel prompt (si risolve con P1).

### Revisione dell'intera procedura per ridurne la complessita' (richiesta del 13/10/2026) — IMPORTANTE, dopo aver risolto l'installazione

- **Perche'**: il 13/10 l'allineamento al pacchetto ha richiesto molti giri a vuoto: script e kernel di versioni diverse
  (messaggi "e' della versione ..."), `configurazione.json` perso alla sostituzione della cartella, registro che risultava
  vuoto e poi con i dati di esempio del template, baseline lette da posti diversi (`trimestrale` la ricostruisce dal registro,
  `precontrollo` la legge da un file), baseline da ricopiare nella knowledge (AU7), raccolta notizie scritta fuori da
  `News_Inbox`, errori tecnici senza indicazione del punto. Ogni passo manuale e' una possibile deriva fra file.
- **Cosa fare** (analisi, non ancora sviluppo): a) elencare ogni passo manuale e ogni file che deve coincidere fra PC,
  SharePoint e Agent Builder, e togliere quelli eliminabili; b) un solo comando di verifica (`verifica`) che controlli
  versione dello script, kernel, template, registro (ciclo, numero di rischi, assenza dei dati di esempio), percorsi di
  `configurazione.json`, esistenza dei file di input, e dica cosa correggere; c) un solo pacchetto con manifest e
  impronte, e un installatore che non tocchi `configurazione.json`; d) un controllo che rifiuti un registro con gli id di
  esempio; e) mostrare nei messaggi di `baseline` e `trimestrale` quale registro e quale ciclo stanno usando; f) valutare
  se il giro A1 → precontrollo → A5 → trimestrale → validazione possa avere meno passaggi a mano (si collega ad AU2, AU4,
  AU7).
- **Fatto quando**: una persona che parte da un PC pulito arriva al primo `trimestrale` senza consultare piu' di una
  pagina di istruzioni e senza passaggi manuali di allineamento fra file.
- **Impegno**: analisi circa 1 giorno, poi le voci che ne escono.

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

## 10. In riserva (non pianificate)

Non sono voci di lavoro. Si riprendono solo se cambia la condizione indicata.

| Voce | Cosa e' | Quando riprenderla |
|---|---|---|
| Piano 07, Power Query senza Python (`Analisi_Architettura/Archivio/07`) | controlli e consolidamento in Excel con Power Query; Python solo al manutentore. Era la voce AR1, chiusa da D-43 | se la Banca vietasse Python sul PC |
| Variante CS-2, tutto nel cloud (piano 10, 10.11; `Analisi_Architettura/Archivio/06`) | motore in Office Scripts, stato in Liste SharePoint, report con Power Query: nessun PC in esercizio | solo dopo la CS-1 (AU6), se la Banca vuole un esercizio senza PC |
| Foglio Manutenzione (anteprima del 07/10 cancellata l'08/10; disegno in D-76 e nell'HANDOFF, sezione 2-unvicies) | una riga per campo da cambiare fra un ciclo e l'altro, al posto della riapertura | se le modifiche fra un ciclo e l'altro diventano frequenti |
