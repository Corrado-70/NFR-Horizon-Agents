# TODO — registro vivo del lavoro

**Da qui si parte.** Questo file dice a che punto e' il lavoro su `main` e che cosa viene dopo: per riprendere basta la
sezione 0. Ogni voce aperta dice perche' serve, cosa fare e come capire che e' fatta.

**Aggiornato al 07/11/2026.**

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
6. ogni voce aperta ha lo stato in testa (fatto, in corso, da fare, in attesa, superata) e il suo numero nella lista
   della sezione 1; la sezione 1 comprende **tutto** cio' che resta, grafici e pulizia compresi: una voce che non
   e' li' non e' in programma.

La versione tutta in Copilot Studio ha il suo registro, sul ramo `copilot-studio-pieno`:
`09_Copilot_Studio/TODO_Copilot_Studio.md`. Qui restano le voci di `main` e quelle comuni ai due rami.

Sezioni:
0. da dove si riparte;
1. ordine di lavoro: **tutto cio' che resta, in un'unica lista numerata con lo stato**;
2. passi sul PC della Banca (non sviluppo: installare e provare cio' che c'e' gia');
3. processi (P1, P12, P13, P15);
4. automazione del processo: l'app di orchestrazione, fatta (finestra per processo dal 04/11, AU8); restano la demo (AU5),
   A1 a lotti (AU9) e il canale Claude su Vertex (AU10, analisi 20);
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
| Ultimo commit | 07/11: analisi 20, sezioni 20.15-20.17 (solo documenti; A-30...A-32). 06/11: PC della Banca agganciato a GitHub (clone di `main`; credenziali e impostazioni locali di Claude Code escluse); pacchetto alleggerito con `export-ignore` in `.gitattributes`; zip tolti dal repository. Ultimo commit di sviluppo 04/11: testi ereditati (P17, D-93), passo 3 (D-94...D-98), Quadro in due pagine, passo 7 (P2, P7, P6: D-99...D-101), G5 in parte e finestra dell'app per processo (AU8, D-102); su GitHub |
| Collaudo | 04/11, con Excel: catena 407/407; collaudo veloce verde (test_controlli 340, test_app 86, test_report_html 23) |
| Ultimo pacchetto preparato | zip **`NFR-Horizon-Agents_2026-11-06_<commit>.zip`** (06/11, il commit e' quello che aggiorna questa sezione; 178 file, 3,5 MB, i `.cmd` con il nome vero): stesso software dello zip per la posta `..._2026-11-04_ed63ea0_posta.zip` del 04/11, con le istruzioni del pacchetto del 04/11 in testa ad `AGGIORNAMENTO_IN_BANCA.md` (template `2026-11-04`, `aggiorna-registro`, A1, A5 e A8 da reincollare, cartella `Rapporti_Scenario`). Fuori dallo zip (`.gitattributes`): la presentazione `.pptx`, `Analisi_Architettura`, i file di git, `.claude/`, `CLAUDE.md`, HANDOFF, PROMPT_MASTER e `Revisione_*.md`. Gli zip non stanno nel repository: `git archive --format=zip -o NFR-Horizon-Agents_<data>_<commit>.zip HEAD` |
| In Banca | il 29/10 prima prova dell'app, con un pacchetto precedente; il 05/11 il progetto copiato sul PC della Banca, collaudo veloce verde (`--senza-excel`, con `py -3`); il 06/11 la copia e' diventata un clone di GitHub. L'installazione in uso e' su OneDrive (`NFR Horizon Scan OneDrive`): la versione installata si legge in `07_Senza_Studio\installato.json`, non ancora annotata (B1) |
| Ramo `copilot-studio-pieno` | allineato a `main` il 04/11 (merge, `genera_CS.py`, `prepara_kit.py`); la finestra dei temi, il riepilogo mensile e la finestra per processo vanno rifatti li' come argomenti e flussi quando si decide la strada del motore (D-91) |
| Analisi aperta piu' recente | 06/11: **analisi 20**, `Analisi_Architettura/20_Agenti_Claude_Vertex.md`. Agenti Claude su Vertex come terza origine della strada A, con analisi critica in 20.14; decisioni A-25...A-29, prove K16-K25, tappe CL0-CL7 (AU10). **07/11: sezione 20.15**, Claude Code con skill, sotto-agenti e hook: variante O3 guidata (ordine da `stato.leggi()`, shell con un elenco chiuso) e assistente di validazione in sola lettura; A-30, DB9, K26, K27. **07/11: sezione 20.16**, l'interfaccia, con una ricerca sul mercato: chat con i soli strumenti del progetto (server MCP, senza shell; supera la variante O3 guidata), cruscotto HTML e validazione nel browser con i testi interi correggibili; A-31, A-32, DB9 f-h, K28, K29. **07/11: sezione 20.17**, la soluzione proposta (O4 come motore degli agenti; chat, cruscotto e pagina di validazione come interfaccia) e il percorso in cinque fasi (sezione 1, nota sull'ordine delle voci 17-22). Nessun codice: il pacchetto non cambia |

**In sospeso**: nessun lavoro di sviluppo a meta'; primo ritocco: la nota sotto i primi cinque del Quadro su due righe (G5). In Banca: leggere la versione installata su OneDrive e, se precede `ed63ea0`, installare lo zip del 06/11 (B1-B4). Dall'analisi 20: le domande DB3-DB9 da portare in Banca, perche' DB1 e DB2 hanno avuto risposta il 06/11, e la prova K16 (n. 17, B10). DB9 (07/11) chiede all'IT se shell, hook, skill, sotto-agenti e un server MCP del progetto sono ammessi in Claude Code, se c'e' VS Code e se Edge lascia salvare una pagina locale: decide l'assistente di validazione (n. 20) e la chat con gli strumenti del progetto (n. 21). **07/11: VS Code con l'estensione di Claude Code e' ammesso (DB9 g).** Le verifiche in ordine, con la strada che ognuna apre, sono in 20.17.5: decidono DB4 (b) e DB9 (f), quest'ultima con la nuova prova K28b (server MCP minimo in VS Code).

**Prossimo passo**: le prove in Banca (numeri 2-4 della sezione 1) con lo zip del 06/11 (stesso software del 04/11):
installazione con `aggiorna-registro`, poi il ciclo 2026Q4 di prova (B7, B9) con le verifiche elencate in `AGGIORNAMENTO_IN_BANCA.md`,
passo 6. La nota del Quadro su due righe (n. 1) si fa quando si torna allo sviluppo; dopo,
le scale a 6 livelli (5). **Insieme alle prove in Banca**: le domande DB3-DB9 dell'analisi 20 e, se Claude Code e' sul
PC, la prova K16 senza codice (n. 17). Se DB9 lo consente, l'assistente di validazione (n. 20) si prepara in mezza
giornata o una e si prova in Banca (K26), anche con A1 su Agent Builder. Dopo vengono la chat con gli strumenti del
progetto (n. 21) e la validazione nel browser (n. 22), se l'utente decide A-31 e A-32. L'elenco completo, con lo stato
di ogni voce, e' la sezione 1.

**Decisioni che aspettano** (il testo e' in DECISIONI):

| Decisione | Quando |
|---|---|
| **A-19** scale a 6 livelli e registro nuovo: indirizzo dell'utente del 30/10, si avvia su sua richiesta | **prima del primo ciclo vero**: 4-6 giorni piu' un ciclo di prova (P15) |
| A-24 driver | con A-19 |
| A-17 contraddittorio | dopo la prova K15 (B8) |
| A-20, A-21, A-22, A-23 spunti della proposta esterna | su richiesta dell'utente (P15) |
| A-25...A-29 canale Claude su Vertex (analisi 20): canale, corpus, prompt, conformita', rami | A-28 e il trasporto dopo le risposte DB1-DB8; A-25 dopo K19 e K25 (AU10) |
| A-30 assistente di validazione (analisi 20, 20.15; la variante O3 guidata e' superata da A-31) | dopo DB9 e K26 (AU10) |
| A-31 interfaccia agentica: chat con gli strumenti del progetto e cruscotto; A-32 validazione nel browser con i testi (analisi 20, 20.16) | A-31 dopo DB9 (f, g) e K28; A-32 dopo K29 e A-19 (AU10) |
| A-12 taratura | dopo il ciclo 2026Q4 reale |

## 1. Ordine di lavoro: le cose ancora aperte, in un'unica lista

Solo le voci **ancora aperte**, nell'ordine in cui farle; cio' che e' fatto passa nella sezione 9 (e nella 9-bis le voci
superate). La colonna **Stato** usa sempre le stesse parole: **da fare**, **in corso**, **in attesa** (di un passo
prima, della Banca o di una decisione), **da decidere**. Ogni voce ha il suo dettaglio nella sezione indicata, dove la
stessa parola di stato sta in testa. La colonna "Era" dice il numero che la voce aveva nell'ordine prima del piano del 04/11.

**Chiuso il 04/11** (sezione 9): passo 3 (P4, P9, P14, P16, rischi collegati al posto di P5, D-94...D-98), Quadro in
due pagine, passo 7 (P2, P7, P6, D-99...D-101), G5 in parte, AU8 (D-102), demo e presentazione, documenti e ramo
`copilot-studio-pieno` allineati; collaudo con Excel 407/407.

**Aggiunte il 06/11** (analisi 20): le voci 17-19 stanno in coda per non cambiare i numeri citati nelle altre sezioni.
La 17 si fa insieme alle prove in Banca (n. 2-3); la 18 dopo; la 19 aspetta le risposte della 17, la decisione
dell'utente e A-19 (n. 5).

**Aggiunte il 07/11** (analisi 20, 20.15 e 20.16): le voci 20-22, in coda per la stessa ragione. La 20 aspetta la
risposta a DB9 (con la 17). La 21 era la variante O3 guidata; lo stesso giorno e' diventata la chat con gli strumenti
del progetto, senza shell (la variante e' tra le superate, 9-bis). La 21 e la 22 aspettano DB9 e la decisione
dell'utente su A-31 e A-32; la 22 anche A-19 (n. 5).

**Ordine delle voci 17-22** (analisi 20, 20.17, percorso in cinque fasi; i numeri non cambiano):
1. fase 0, novembre: la 17, insieme alle prove in Banca (n. 2-3);
2. fase 1, dicembre: la 18, la 5 (A-19) e la 20;
3. fase 2, gennaio: il ciclo vero 2026Q4 su Agent Builder; intanto la 19 nella variante minima (CL2) e A1 in ombra;
4. fase 3, febbraio-marzo: la 21 e la 22;
5. fase 4, da aprile: il resto della 19 (CL3, CL4, CL6, CL7).

La finestra di chat di A7 nell'app, prevista nella 19 (CL4), non si fa: la sostituisce la chat della 21.

| # | Voce | Che cosa | Era | Giorni | Stato | Dettaglio |
|---|---|---|---|---|---|---|
| 1 | **G5** nota del Quadro | la nota sotto i primi cinque su due righe, con il dettaglio tolto il 04/11 ("l'ultimo ciclo del trimestre, straordinario compreso"); circa 11 punti in piu' in pagina 1, poi la catena | in parallelo | 0,25 | da fare, subito (proposta accettata dall'utente il 04/11) | sezione 6 |
| 2 | **B1-B4, B5-bis** in Banca | installazione del pacchetto unico e verifiche dell'app | 1 | 1-2 | zip del 06/11 pronto (stesso software del 04/11); versione installata su OneDrive da leggere; prima prova il 29/10 | sezione 2 |
| 3 | **B7, B9, B6** in Banca; **B8** se c'e' tempo | ciclo 2026Q4 di prova, qualita' di A1 e A8, prova di A7; K15 contraddittorio | 4 | in Banca | in attesa del n. 2 | sezione 2 |
| 4 | **AU9** A1 a lotti | solo se nel ciclo di prova la risposta di A1 si taglia ancora | dopo 1 | 1-1,5 | in attesa dell'esito del n. 3 | sezione 4 |
| 5 | **P15.1 / A-19** scale a 6 livelli | rubrica, schemi e registro nuovo (riparte da zero), con i driver (A-24); prima del ciclo vero | 2 | 4-6 piu' un ciclo di prova | in attesa: dopo le prove in Banca, su richiesta dell'utente | sezione 3 |
| 6 | **P1** segnali per dimensione | dimensione e descrittore nei segnali di A3 e A4, freccia di pressione sul radar | 5 | 2-3 | da fare, solo se finisce prima di gennaio | sezione 3 |
| 7 | **AU5** demo dai flussi | la demo passa dai flussi dell'app con appunti simulati | in parallelo | 1 | da fare | sezione 4 |
| 8 | **G1, G3, G2** manutenzione dei grafici | parametri dei grafici in una tabella, script di anteprima, documento su come modificarli | in parallelo | 2 | da fare | sezione 6 |
| 9 | **G6** report intermedio | rischi di A1 accanto ai rilievi, prima della scrittura | in parallelo | 0,5 | da fare quando servira' | sezione 6 |
| 10 | **Q1** quantificazione | nota di metodo da far approvare, poi prototipo su 1-2 rischi | in parallelo | nota 1-2, prototipo 3-5 | da fare (stime degli esperti: lavoro della Banca) | sezione 5 |
| 11 | **M1 (c), M4** pulizia | collaudo piu' corto; cartelle del codice da unire | sempre | — | da fare, bassa priorita' | sezione 7 |
| 12 | **P13** punti 3b, 4, 6 | esposizione nell'anagrafica, salto con evidenza forte, taratura dei descrittori | dopo il ciclo vero | 1-3 | in attesa del ciclo 2026Q4 vero | sezione 3 |
| 13 | **P12** contraddittorio | agente A9 dopo A1 | dopo il ciclo vero | 3-4 | in attesa della prova K15 (n. 3) | sezione 3 |
| 14 | **P15.3** altri spunti esterni | A-20...A-23 e la scheda di A-24 | dopo il ciclo vero | 0,5-4 per voce | in attesa di una richiesta dell'utente | sezione 3 |
| 15 | Revisione della procedura | meno passi manuali e file da allineare | dopo la prova in Banca | 0,5 piu' le voci che ne escono | da fare | sezione 8 |
| 16 | Questioni aperte | conseguenze dei livelli di allerta, taratura, QUINDI per A3... | quando capitano | — | da decidere | sezione 8 |
| 17 | **AU10, tappa CL0** domande alla Banca e prova senza codice | domande DB1-DB8 dell'analisi 20 (autorizzazione, accesso a Vertex, rete, Claude Code, modelli e quote, DPO, Legale, model risk); K16 se Claude Code e' sul PC, K17 con lo script di prova | nuova (06/11) | 0,5-1 piu' le attese | da fare, insieme alle prove in Banca (n. 2-3) | sezione 2 (B10), sezione 4 |
| 18 | **AU10, tappa CL1** anelli e canale su `main` | i tre anelli che ripartono da uno stato vecchio (20.5.3), il livello "canale", il contatore dei tentativi; utili anche con Agent Builder | nuova (06/11) | 2-3 | da fare, dopo le prove in Banca e prima di CL2 | sezione 4 |
| 19 | **AU10, tappe CL2-CL7** canale Claude | prototipo sul ramo `canale-claude` (A-29), corpus, pilota in ombra limitato, passaggio | nuova (06/11) | 18-25 piu' un ciclo | in attesa delle risposte di CL0 e della decisione dell'utente; dopo A-19 (n. 5) | sezione 4 |
| 20 | **AU10, assistente di validazione** (A-30, parte 1) | Claude Code interattivo in sola lettura sui file del ciclo e sulle spiegazioni, dietro il bottone "Apri chat (A7)"; skill `/validazione` e impostazioni che negano shell e scrittura; vale anche con A1 su Agent Builder; poi K26 in Banca | nuova (07/11) | 0,5-1 piu' K26 | in attesa della risposta a DB9 (n. 17) | sezione 4, sezione 2 (B10) |
| 21 | **AU10, chat con gli strumenti del progetto e cruscotto** (A-31) | server MCP locale `nfr` sopra `stato`, `flussi`, `ingresso` e il motore (terzo `Ambiente`, flusso sospeso e ripreso, otto strumenti), Claude Code con i soli strumenti del progetto (nessuna shell; nel pannello di VS Code con i divieti di `.claude/settings.json`), cruscotto HTML in sola lettura; prova K28 sulla demo, K28b in Banca | nuova (07/11) | 5-7 | in attesa di DB9 (f) con K28b e della decisione dell'utente; VS Code ammesso (DB9 g, 07/11) | sezione 4 |
| 22 | **AU10, validazione nel browser con i testi** (A-32) | pagina per rischio con valori vincolati alla rubrica, testi interi correggibili con le modifiche in vista e l'origine, riscrittura di una parte fatta da A1; `valida --decisioni`; collaudo sulle due superfici; prova K29 in Banca | nuova (07/11) | 5-7 | in attesa della decisione dell'utente; dopo A-19 (n. 5), o con la rubrica letta dal kernel | sezione 4 |

## 2. Passi sul PC della Banca

Non sono sviluppo: si installa e si prova cio' che il pacchetto ha gia'. I passi del pacchetto corrente sono in
`AGGIORNAMENTO_IN_BANCA.md`, quelli generali nella guida, sezione 0-bis. Le prove di Copilot Studio sono nel registro del
ramo (9-bis).

| # | Passo | Per quali decisioni | Stato |
|---|---|---|---|
| B1 | Pacchetto corrente (zip del 06/11, stesso software di `ed63ea0` del 04/11) estratto nella cartella del pacchetto su OneDrive e `installa.cmd` lanciato da li' (lavora sulla cartella in cui si trova). Prima leggere la versione installata (`07_Senza_Studio\installato.json`, o la prima riga di `installa.cmd`): se e' gia' `ed63ea0`, non c'e' niente da installare. Sposta da solo in `_obsoleti_<data>` i file elencati in `obsoleti.txt` | D-78, D-89 | da fare: versione installata da leggere |
| B2 | Kernel nella library: lo copia `installa.cmd` dopo una conferma (i file sostituiti in `Kernel\_precedenti\<data>`); rispetto al pacchetto del 30/10 cambiano `guida_scrittura_A1.md`, `schema_output_A1.json`, `controlli_A5.md`, `fonti.md` e `mappatura_campi.json` | D-74, D-89, D-92...D-98 | da fare |
| B3 | Reincollare gli agenti che `installa.cmd` elenca: sopra il pacchetto del 30/10 o del 03/11 A1, A5 e A8; sopra quello del 23/10 anche A4, A6 e A7 | D-86...D-88, D-92, D-93 | da fare |
| B4 | `aggiorna-registro` al template `2026-11-04`: serve con questo pacchetto, prima su una copia e poi sul registro vero (`AGGIORNAMENTO_IN_BANCA.md`, passo 4; guida, 0-bis) | D-74, D-79, D-99 | da fare |
| B5-bis | **Verifiche dell'app, tappe M1-M5**: elenco in `AGGIORNAMENTO_IN_BANCA.md` ("Verifiche da fare" e, per il pacchetto del 04/11, passo 6 dell'aggiornamento rapido), esiti in `Analisi_Architettura/18_App_orchestrazione.md`, 18.6 (nel clone git: dal 06/11 `Analisi_Architettura` non e' nel pacchetto installato). **29/10**: prima prova, un trimestre dall'app fino a `trimestrale` e validazione (A1, precontrollo, una correzione, precontrollo superato); i problemi trovati sono corretti. Restano, sul pacchetto corrente: risposta lunga di A1 dagli appunti, link degli agenti, lucchetto con un collega, installazione completa (pip, collegamenti, attivita' della raccolta, Verifica del PC con Excel), report HTML, Admin | D-83, D-85...D-90 | in corso |
| B6 | Prova di A7 (`04_Riferimenti/Prove/Prova_A7.md`), anche per la prima persona | D-72, D-87 | da fare |
| B7 | Ciclo 2026Q4 di prova (prima del ciclo vero): converge in 1-2 giri A1, senza A5 o con A5. **29/10**: un giro di correzione, senza le lunghezze di C10; da rifare sulla versione dei passi 2 e 3 dell'ordine | S1 (D-49...D-56), D-69, D-71 | in corso |
| B8 | Facoltativo, per A-17: **K15** contraddittorio senza codice sul ciclo 2026Q4 (`Analisi_Architettura/17_Decimo_uomo.md`, 17.8): A9 in Agent Builder dopo A1, piu' la variante 2b nella chat di A1; il validatore giudica ogni tesi utile, gia' nota o rumore. Dal 30/10 con il mandato esteso (A-17, analisi 19) | A-17 | da fare |
| B9 | **Prova di qualita' di A1 e A8 su documenti pubblici** (proposta del 24/10): una libreria di documenti pubblici (EBA, BCE, ENISA, rassegne stampa; niente di interno alla Banca) sul PC di sviluppo e la stessa in Banca. (a) Sul PC di sviluppo Claude fa A1 o A8 con le istruzioni, l'allegato `Input_A1`/`Input_A8` e i documenti, poi precontrollo e `trimestrale` sul registro di prova: dice se istruzioni e documenti bastano, non che cosa fara' l'agente (Claude legge i documenti per intero, Agent Builder ne pesca dei pezzi). (b) Prova piu' utile: l'agente vero in Banca sugli stessi documenti, il JSON (senza dati della Banca) riportato e controllato da Claude affermazione per affermazione (fatti e date nel documento citato, descrittori della rubrica, fenomeni mancati o scartati a torto) | qualita' di A1 (D-21), P14 | da fare |
| B10 | **Canale Claude, tappa CL0** (`Analisi_Architettura/20_Agenti_Claude_Vertex.md`, 20.1.2 e 20.12). (a) Le domande DB1-DB8 a IT, cloud team, DPO, Legale e model risk: autorizzazione per un'app propria o solo per Claude Code, autenticazione a Vertex e gcloud, uscita di rete verso `aiplatform.eu.rep.googleapis.com`, Claude Code e pip, progetto, regione `eu`, modelli e quote, registro delle richieste, parere scritto sui dati, testo completo delle fonti, riesame di D-23. **06/11: risposte a DB1** (l'autorizzazione vale per lo strumento Claude Code sul PC, quindi trasporto `claude-p`) **e a DB2** (ADC dell'utente con gcloud). Ora decisiva **DB4**: Claude Code su ogni PC degli analisti, uso non interattivo da uno script compreso nell'autorizzazione, nessun blocco dell'EDR. (b) **K16** (manuale: `04_Riferimenti/Prove/Prova_K16_Claude_Code.md`, con `Prove/K16/`), se Claude Code e' sul PC: A1 con il prompt per Claude e `Input_A1` del ciclo di prova, JSON in un file, poi "Scegli file" e precontrollo nell'app. (c) **K17** con lo script di prova (proxy, token, host `eu`, quota). (d) **07/11: DB9** all'IT (20.1.2): nelle impostazioni gestite di Claude Code, shell (Bash, PowerShell), hook e regole del progetto, skill e sotto-agenti sono ammessi? Per quanti giorni restano le sessioni sul PC? Un server MCP del progetto e' ammesso? C'e' VS Code con l'estensione di Claude Code (**si', 07/11**)? In Edge una pagina HTML locale puo' salvare un file con la File System Access API? Con la sola estensione `claude` non e' nel PATH: K16 usa la sua copia di `claude.exe` (manuale, passo 2). **K28b**: un server MCP minimo in VS Code, senza dati (20.12). Ordine delle verifiche in 20.17.5. (e) Se DB9 lo consente, **K26**: l'assistente di validazione su un ciclo di prova (n. 20). (f) Dopo la voce 22, **K29**: lo stesso ciclo validato con la griglia e con la pagina nel browser | A-25, A-28, A-30, A-31, A-32 | da fare (n. 17; K26 con il n. 20, K29 con il n. 22) |

## 3. Processi: cosa manca rispetto al disegno atteso

Dall'analisi del 26/09/2026: il processo desiderato e' **trimestrale come processo fondante** (su documentazione
approfondita: regolatori, analisti di settore, siti specialistici, analisi interne), **settimanale o mensile** sulle
notizie (trend dei rischi esistenti, evento critico che chiede di rigenerare il trimestre, variazioni visibili sul
radar) e **spot** su una sola notizia (analisi a fondo, impatto per dimensione, posizione sul radar).

Decisioni dell'utente che fanno da cornice:
- **D-41**: "mai una cifra nuova" fuori dal trimestre e "solo un ciclo di valutazione modifica uno score"; l'unica
  eccezione e' il ciclo straordinario (fatto: D-75, D-77). Niente notch numerici ne' posizioni ipotetiche sul radar.
- **D-42**: un evento che tocca piu' rischi genera righe di rischio separate, collegate fra loro: dal 04/11 nella parte
  COLLEGATI: del rischio primario (D-97, al posto di P5).
- **D-79**: un registro unico, nel radar i primi e gli altri in osservazione, con la stessa scala.

| Attesa | Stato oggi | Voce e stato |
|---|---|---|
| Trimestrale come unico processo che cambia gli score | c'e' (principio 3, W1) | fatto |
| Trimestrale su rapporti approfonditi di analisti e regolatori | c'e': cartella `Analisi_Esterne/Rapporti_Scenario`, tipo Rapporto, A1 li legge per primi (D-95); da verificare nel ciclo di prova | P4: **fatto** il 04/11 |
| Temi che l'analista chiede di verificare | c'e': finestra dell'app, temi nella baseline, risposta controllata (D-98) | P9: **fatto** il 04/11 |
| Report aggiornato, non rifatto, e ciclo straordinario | c'e' (Confermato/Variato/Nuovo, al piu' un punto; straordinario D-75, A8 D-77) | fatto |
| Fenomeni lontani o quasi impossibili oggi | c'e': rischi in osservazione del registro unico (D-79); meccanismi anche solo potenziali e segnali deboli nella guida di A1 (D-94) | P16: **fatto** il 04/11 |
| Settimanale: analisi su tutti i rischi toccati | in parte: nove intensita' per notizia, un solo rischio collegato | **P1**: da fare (n. 6) |
| Settimanale: trend dei rischi esistenti e pressione visibile sul radar | in parte: segnali netti, flag, soglia 3 in 4 settimane; il radar non mostra la pressione | **P1**: da fare (n. 6) |
| Spot: impatto per dimensione | in parte: A4 indica il descrittore messo in discussione | **P1**: da fare (n. 6) |
| Evento con piu' meccanismi di perdita | c'e': COLLEGATI: nel rischio primario, "Collegato a" nelle schede (D-97); schede per tema (D-101) | P5: **superata** (D-97); P6: **fatto** il 04/11 |
| Spostamento nel tempo dei rischi | c'e': scia sul radar e traiettoria nel Quadro (D-99) | P2: **fatto** il 04/11 |
| Cadenza mensile | c'e': riepilogo mensile in Excel e HTML (D-100) | P7: **fatto** il 04/11 |
| Contraddittorio sulla valutazione ("decimo uomo"): letture opposte, rischi mancanti, ipotesi, combinazioni | manca: A5 controlla la coerenza dell'output di A1, non la sua completezza ne' le letture alternative | **P12**: in attesa (n. 13) |
| Testi del registro e delle schede chiari e diretti, ma completi e approfonditi, con il "so what" per la Banca | in parte: guida di scrittura (descrizione in 3-5 frasi, razionale in parti con descrittore, fatto e "perche' non il valore vicino"), lunghezze minime e consigliate con il controllo C10 (D-86, D-88), parte QUINDI: e sezione "Stile" (D-96); resta da decidere l'estensione ad A3 (sezione 8) | P14: **fatto** il 04/11 |
| Valutazioni senza asimmetrie: rischi nuovi non tutti bassi, rischi lontani a mitigazione lunga visibili all'urgenza | in parte: diagnosi e anni di adeguamento dei rischi in osservazione (D-80), esposizione non nota (D-81) fatti; restano salto con evidenza forte, taratura | **P13**: in parte fatto (n. 12) |

### P12. Contraddittorio sulla valutazione trimestrale, "decimo uomo" (proposta del 19/10/2026, A-17)

**Stato: in attesa** della prova K15 (B8) · n. 13 dell'ordine di lavoro.

- **Perche'**: le regole (conferma di default, un punto per ciclo) proteggono dall'inflazione ma favoriscono lo status
  quo; A5 non usa la knowledge (D-09) e non cerca cio' che A1 non ha visto. Manca chi sostenga la tesi opposta.
- **Cosa fare**: analisi `Analisi_Architettura/17_Decimo_uomo.md`. Opzione 1 raccomandata: agente A9 Contraddittore
  dopo A1, con la knowledge di A1 e una ricerca propria; JSON senza numeri (tesi in entrambi i versi sui rischi
  principali, rischi mancanti, ipotesi critiche, combinazioni); `trimestrale --contraddittore`: tesi nella colonna
  Segnalazioni come Osservazioni, sintesi in Sintesi_Cicli e nel Quadro, rischi mancanti come temi da verificare (P9, fatta: D-98).
  Prima la prova K15 senza codice (B8).
- **Tocca**: schema nuovo, modello del prompt, script, template (versione nuova), collaudo, guida,
  `controlli_e_model_risk.md` (rischio "ancoraggio alla valutazione precedente").
- **Fatto quando**: K15 dice che le tesi servono e la catena del collaudo porta un A9 di prova fino al Quadro.
- **Impegno**: prova mezza giornata; integrazione circa 3-4 giorni.

### P13. Ancoraggio e asimmetrie della valutazione (proposta del 19/10/2026)

**Stato: in parte fatto** (punti 1, 2 e 3a, D-80 e D-81); i punti 3b, 4, 5 e 6 **in attesa** del ciclo 2026Q4 vero · n. 12 dell'ordine di lavoro.

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

### P15. Spunti dalla proposta esterna di osservatorio (analisi 19, 30/10/2026)

**Stato: da fare, su richiesta dell'utente**: punto 1 (scale a 6 livelli) n. 5 dell'ordine, dopo le prove in Banca; punto 2 e' la prova B8 (n. 3); punto 3 n. 14, dopo il ciclo vero.

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

**Stato: da fare** · n. 6 dell'ordine di lavoro (solo se finisce prima di gennaio).

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

**Stato: da fare** · n. 7 dell'ordine di lavoro.

- **Perche'**: i flussi dell'app sono collaudati con un Ambiente finto; straordinario, schede, report, riapertura,
  dismissione, parere di A4, A7, diagnosi e sblocca sono scritti ma non coperti dalla demo (18.2, F5).
- **Cosa fare**: `Demo_W1_W2/esegui_demo.py` attraverso i flussi con appunti simulati: A1 con i recinti, A1 in due
  parti, correzione dopo un fermo.
- **Fatto quando**: la demo passa dai flussi e le voci `[~]` e `[ ]` di F5 in 18 diventano `[x]`.
- **Impegno**: circa 1 giorno.

### AU9. A1 a lotti, al posto del "continua" (segnalazione dell'utente del 03/11/2026)

**Stato: in attesa** dell'esito del ciclo di prova in Banca · n. 4 dell'ordine di lavoro.

- **Perche'**: in Agent Builder il "continua" nella stessa chat non funziona: A1 a volte ricomincia da capo, a volte
  dice che non ha altro da aggiungere. Con la D-92 l'output di A1 scende di circa il 40% (sulla demo da circa 4.900 a
  circa 3.000 caratteri per rischio), ma un ciclo di 15-20 rischi resta di 45-60.000 caratteri. Se la risposta si
  taglia ancora, il ciclo di prova non si chiude.
- **Cosa fare**:
  1. A1 consegna il ciclo in piu' risposte, ognuna un JSON completo: per esempio rischi del radar a gruppi di 5, poi
     rischi nuovi e in osservazione, fenomeni non censiti e ricalcolo dei KRI. Da decidere con l'utente se il lotto lo
     chiede l'app (messaggio "Lotto 2: rischi NFR-06...NFR-10" negli appunti) o se A1 si ferma da se' a fine lotto;
  2. l'ingresso dell'app riconosce i lotti dello stesso ciclo, li unisce e passa al precontrollo solo il ciclo intero;
  3. la regola sta nella guida di scrittura (il prompt di A1 e' al limite degli 8.000 caratteri); lo schema di A1 non
     cambia se l'unione la fa l'app.
- **Tocca**: `ingresso.py`, `flussi.py`, guida di scrittura di A1, `test_app.py`, guida passo passo; A8 se servira'
  anche a lui. Da valutare la stessa cosa sul ramo `copilot-studio-pieno` (nella prova K6-ter A1 in Copilot Studio ha
  scritto 27.500 caratteri in una risposta).
- **Fatto quando**: un ciclo di 15 rischi arriva intero in Banca senza "continua", e il precontrollo lo legge come un
  output solo.
- **Impegno**: circa 1-1,5 giorni.
- **Con il canale Claude (AU10)**: AU9 non serve. A1 sta in una chiamata sola (fino a 128K token in uscita), e
  spezzarla per rischio romperebbe la coerenza tra rischi (analisi 20, 20.6). AU9 resta solo per Agent Builder.

### AU10. Canale Claude su Vertex, terza origine degli agenti (analisi 20, 06/11/2026)

**Stato: da fare** la tappa CL0 (n. 17) · **da fare** la CL1 (n. 18) · **in attesa** le CL2-CL7 (n. 19) · **in
attesa** di DB9 l'assistente di validazione (n. 20) · **in attesa** di DB9 e della decisione dell'utente la chat con
gli strumenti del progetto (n. 21) e la validazione nel browser (n. 22).

- **Perche'**: la Banca fornisce Claude (Opus) su Google Cloud Vertex. Chiamato dall'app, senza chat, toglie:
  - i tre gesti per agente;
  - le risposte tagliate;
  - il limite degli 8.000 caratteri;
  - la lettura parziale dei documenti;
  - il limite dei 4 siti.

  Restano il registro, il motore unico che scrive (D-10), i controlli e la validazione umana.
- **Cosa fare**: le tappe CL0-CL7 di 20.12:
  - CL0: domande DB1-DB8, K16 e K17 (B10);
  - CL1 su `main`: i tre anelli con stato vecchio di `flussi.py`, il livello "canale" e il contatore;
  - CL2-CL4 sul ramo `canale-claude` (A-29), da creare quando l'utente lo dice: `agenti_claude.py` con il trasporto
    `claude-p` (Claude Code autorizzato, DB1) e `api` come riserva, schema di decodifica, corpus con manifest e lettori,
    anteprima G6 (dal 07/11 dentro il cruscotto; la finestra di chat di A7 non si fa, 20.17);
  - CL5: A-19 su `main`;
  - CL6: pilota in ombra limitato;
  - CL7: passaggio dietro la scelta "Agenti".
- **Aggiunta del 07/11** (20.15): Claude Code con skill, sotto-agenti e hook.
  - **Assistente di validazione** (n. 20): Claude Code in sola lettura sui file del ciclo, dietro il bottone di A7;
    indipendente dal canale, quindi utile anche con Agent Builder. Fatto quando K26 e' superata.
  - **Variante O3 guidata**: superata lo stesso giorno (9-bis). I dieci problemi, con il loro perche', restano in
    20.15.3 e valgono come lista di controllo.
- **Aggiunta del 07/11** (20.16): l'interfaccia, dopo una ricerca sulle applicazioni agentiche del mercato.
  - **Chat con gli strumenti del progetto e cruscotto** (n. 21, A-31): Claude Code con i soli strumenti di un server
    MCP locale sopra il codice di oggi; nessuna shell; le domande del flusso arrivano in chat. Vale con qualunque
    origine degli agenti. Fatto quando K28 e' superata.
  - **Validazione nel browser con i testi** (n. 22, A-32): testi interi correggibili in validazione, con le modifiche
    in vista e l'origine; un file di decisioni che `valida` applica come la griglia. Fatto quando K29 e' superata.
- **Percorso** (20.17): O4 come motore degli agenti, chat, cruscotto e pagina di validazione come interfaccia, in
  cinque fasi additive; l'ordine delle voci 17-22 e' nella sezione 1.
- **Decisioni**: A-25...A-32 (DECISIONI, sezione 2).
- **Fatto quando**: K19 e K25 superate e A-25 decisa.
- **Impegno**: 20-28 giorni (variante minima senza corpus 9-12), A-19 esclusa.

## 5. Quantificazione per i rischi piu' rilevanti

### Q1. Nota di metodo e prototipo di probabilita' e impatto quantitativi

**Stato: da fare** · n. 10 dell'ordine di lavoro.

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

**Stato: da fare** · n. 8 dell'ordine di lavoro.

- **Cosa fare**: una tabella `GRAFICI` all'inizio di `genera_dashboard.py`, una voce per grafico (foglio, ancoraggio,
  dimensioni, titolo, legenda, colori delle serie, scala degli assi, scala delle bolle, testi degli anelli); le
  funzioni dei fogli leggono da li'.
- **Fatto quando**: il template rigenerato e' identico a prima e ogni parametro visivo e' nella tabella.
- **Impegno**: circa mezza giornata.

### G3. Script di anteprima dei grafici

**Stato: da fare** · n. 8 dell'ordine di lavoro.

- **Cosa fare**: `03_Excel/anteprima_grafici.py [file.xlsx]` che apre il file in sola lettura, ricalcola ed esporta in
  PNG tutti i grafici, compresa la storia di un KRI a scelta. Default: il template appena generato.
- **Fatto quando**: un comando produce una cartella di immagini, una per grafico, senza modificare il file.
- **Impegno**: basso.

### G2. Documentare come modificare ed estendere i grafici

**Stato: da fare** · n. 8 dell'ordine di lavoro (dopo G1).

- **Cosa fare**: `03_Excel/grafici_come_modificarli.md`: i tre livelli (cosa mostra, quali dati entrano, come
  appare); ricette (colori e dimensioni, scala di un asse, una serie in piu', un grafico nuovo, un intervallo dinamico
  con un nome OFFSET); le trappole gia' incontrate (overlay di titolo e legenda, assi eliminati da openpyxl,
  `varyColors`, linee smussate, colonne nascoste e `visible_cells_only`, #N/D invece di zero, anagrafica senza righe
  vuote); come verificare (rigenerare, G3, collaudo). Dopo G1.
- **Fatto quando**: un manutentore che non ha scritto il generatore cambia il colore di una serie e aggiunge un
  grafico seguendo solo il documento.
- **Impegno**: basso.

### G5. Difetti estetici noti

**Stato: in parte fatto** (04/11: le due matrici) · la nota del Quadro e' il n. 1 dell'ordine di lavoro, il resto il n. 8.

| Dove | Difetto | Idea di soluzione |
|---|---|---|
| Storico | voci vuote in legenda per le righe libere dell'anagrafica | nascondere la legenda ed etichettare l'ultimo punto di ogni linea, o serie dinamiche |
| Radar di Mosca | con molti rischi nello stesso settore e margine simile i cerchi possono toccarsi (piu' probabile con un rischio per meccanismo, D-55) | spostamento radiale alternato per i rischi adiacenti |
| Quadro, matrice piccola | con sei o piu' rischi nella stessa cella l'ultima riga di numeri puo' essere tagliata | **fatto il 04/11**: "n rischi" da sei in su, l'elenco nella Matrice |
| Quadro, nota sotto i primi cinque | a una riga, era tagliata in stampa: il 04/11 accorciata, togliendo "(l'ultimo ciclo del trimestre, straordinario compreso)"; la nota sotto la matrice piccola solo riformulata | **primo ritocco dopo il commit del 04/11** (proposta accettata dall'utente): nota su due righe con il dettaglio, circa 11 punti in piu' in pagina 1, poi la catena |
| Quadro e Delta | l'altezza delle righe con testi calcolati e' stimata contando i caratteri | misurare in Excel con una cella di appoggio non unita |
| Report HTML, matrice Probabilita x Impatto (vista Matrice e matrice piccola del Quadro) | con molti rischi nella stessa cella quella cella diventava molto piu' grande delle altre (segnalazione dell'utente del 04/11) | **fatto il 04/11**: celle di misura fissa (`table-layout: fixed`), al massimo 5 ID nella grande e 3 nella piccola, poi "+n"; l'elenco intero nel suggerimento della cella |

### G6. Report intermedio leggibile: rischi di A1 accanto ai rilievi dei controlli

**Stato: da fare quando servira'** · n. 9 dell'ordine di lavoro.

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
| M1 (c) | Collaudo piu' corto: meno letture complete del registro nel gruppo `catena` (oggi circa 40-60 minuti in parallelo; il gruppo `catena` resta in sequenza e da solo dura quasi tutto) | da fare (n. 11) |
| M4 (resto) | Cartelle del codice (`07_Senza_Studio`, `09_Copilot_Studio`) da unire: doveva farlo l'installatore, che non l'ha fatto; `installa.cmd`, la guida e `AGGIORNAMENTO_IN_BANCA.md` puntano a `07_Senza_Studio`. Conviene solo insieme a un pacchetto che cambia comunque i percorsi | da fare, bassa priorita' (n. 11) |

## 8. Questioni aperte emerse dal lavoro

Piccole, da decidere quando capita l'occasione:
- conseguenze dei tre livelli di allerta (D-63: chi fa cosa, entro quando), da decidere con la funzione di rischio;
- taratura delle soglie del livello di allerta, dei descrittori e dei parametri del radar (capienza, soglie, D-79)
  con A-12, dopo il ciclo 2026Q4 reale;
- la Y di Mosca conta le azioni del periodo di valutazione del rischio (D-75), non quelle ancora aperte dei cicli
  prima;
- `sogliaDelta` colora solo il Delta; il nome `rmPxI` non e' usato;
- i flag di A3 citano "il descrittore", che A3 non ha nel prompt (si risolve con P1).
- il "so what" (QUINDI:, D-96) anche nelle motivazioni delle notizie di A3: da decidere (TODO P14, punto 4).

### Revisione dell'intera procedura per ridurne la complessita' (richiesta del 13/10/2026) — IMPORTANTE, dopo la prova in Banca

**Stato: da fare** dopo la prova in Banca · n. 15 dell'ordine di lavoro.

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
| Lunghezze di A1 ridotte | Fascia intermedia delle lunghezze dei testi dei rischi (circa il 40% in meno), perche' l'output di A1 stesse nelle risposte di Copilot | 03/11 | D-92 | guida di scrittura di A1, `controlli_a5.py` |
| P17 | Testi dei rischi esistenti aggiornati, non riscritti: descrizione una sola che racconta l'evoluzione, solo le parti del razionale che cambiano, KRI in vigore che restano; lo script riprende il resto dalla baseline; A8 con le stesse regole; dopo una riapertura l'elenco dei testi da rileggere e Testi a mano | 03/11 | D-93 | `controlli_a5.eredita_testi`, guida di scrittura ("Rischi esistenti"), `valida` e Testi a mano |
| P16 | Horizon scan: meccanismi di perdita anche solo potenziali, fonte anche precedente alla finestra per un rischio nuovo in osservazione, segnali deboli | 04/11 | D-94 | guida di scrittura di A1 ("Fenomeni considerati", "Radar e osservazione") |
| P4 | Rapporti di scenario: cartella `Analisi_Esterne/Rapporti_Scenario/<anno>`, tipo di fonte Rapporto, letti per primi da A1 | 04/11 | D-95 | `fonti.md` (FNT-35), schema di A1, guida di scrittura |
| P14 (so what) | Parte QUINDI: del razionale (C10, schede "Che cosa significa per la Banca") e sezione "Stile" della guida | 04/11 | D-96 | guida di scrittura, `controlli_a5.py`, `schede.py` |
| P5 alleggerita | Rischi collegati citati nella parte COLLEGATI: del rischio primario, "Collegato a" ricavato dallo script nelle schede e nel report HTML, controllo come Osservazione di C1 | 04/11 | D-97 | guida di scrittura ("Rischi collegati"), `schede.legami_collegati` |
| P2 e commento in pagina 1 | Scia sul radar (solo di posizione, dal trimestre prima), traiettoria dei primi cinque, commento di A1 in prima pagina del Quadro; template 2026-11-04 | 04/11 | D-99 | `genera_dashboard.py` (Radar_Mosca, Quadro), `report_html.py` |
| P7 | Riepilogo mensile delle notizie, Excel e HTML, comando `mensile` | 04/11 | D-100 | `riepilogo_mensile.py`; guida, sezione 9 |
| P6 | Schede per tema, un foglio per driver con almeno due rischi | 04/11 | D-101 | `schede.py` |
| Quadro in due pagine | Gli ultimi rischi segnalati si nascondono, elencati nella nota, se la seconda pagina non sta al 60% | 04/11 | — | `esegui_ciclo_locale.rischi_fuori_dal_quadro` |
| AU8 | Finestra per processo: riquadri per cadenza, "Approvazioni e report" unico con il periodo nel nome, nomi nuovi con l'agente fra parentesi, Aggiungi un rischio (A8), Diagnosi in Admin; l'approvazione delle notizie rigenera il report (e il mensile a fine mese) | 04/11 | D-102 | `app_nfr.py`, `flussi.py`; guida, "I processi" |
| G5 (parte) | Matrice P x I del report HTML a spaziatura fissa; matrice piccola del Quadro con "n rischi" | 04/11 | — | `report_html.py`, `genera_dashboard.py` |
| Demo e presentazione | Demo rilanciata con testi lunghi, QUINDI, COLLEGATI, un tema, scia, commento in pagina 1, schede per tema e riepilogo mensile; presentazione di 70 slide | 04/11 | — | `Demo_W1_W2/REPORT_demo.md`, `Presentazione/` |
| Allineamento del 04/11 | Documenti, istruzioni del pacchetto in `AGGIORNAMENTO_IN_BANCA.md`, commit e push di `main`, merge nel ramo `copilot-studio-pieno` con `genera_CS.py` e `prepara_kit.py`; zip per la posta `..._2026-11-04_ed63ea0_posta.zip` | 04/11 | — | sezione 0 |
| PC della Banca su GitHub, pacchetto piu' leggero | La copia del 05/11 agganciata a GitHub (credenziali GCP e impostazioni locali escluse); dal pacchetto fuori presentazione, analisi, file di git e documenti di sviluppo (da 12 a 3,5 MB); zip tolti dal repository | 06/11 | — | sezione 0; `.gitattributes`, `.gitignore` |
| P9 | Temi da verificare: finestra dell'app (menu Altro, proposta prima di A1), temi aperti nella baseline, risposta controllata in validazione | 04/11 | D-98 | `temi.py`, `flussi.py`, guida passo passo ("Menu Altro") |
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
| P5: campo `collegati`, colonna "Collegati" nel registro, linee fra i cerchi del radar | scelta dell'utente del 04/11: basta citare i collegati nel rischio primario (D-97) | DECISIONI D-42 e D-97 |
| Variante CS-2 in riserva | sostituita dal ramo `copilot-studio-pieno` (D-82) | `Analisi_Architettura/15_CS2_approfondita.md` |
| Variante O3 guidata (skill, sotto-agenti, hook, shell con un elenco chiuso; prova K27), voce 21 per poche ore del 07/11 | superata lo stesso giorno dalla chat con i soli strumenti del progetto, che ottiene lo stesso senza shell (A-31, nuova voce 21) | `Analisi_Architettura/20_Agenti_Claude_Vertex.md`, 20.15 (i dieci problemi in 20.15.3 restano validi) |

## 10. In riserva (non pianificate)

Non sono voci di lavoro. Si riprendono solo se cambia la condizione indicata.

| Voce | Cosa e' | Quando riprenderla |
|---|---|---|
| Piano 07, Power Query senza Python (`Analisi_Architettura/Archivio/07`) | controlli e consolidamento in Excel con Power Query; Python solo al manutentore. Era la voce AR1, chiusa da D-43 | se la Banca vietasse Python sul PC |
| Foglio Manutenzione (anteprima del 07/10 cancellata l'08/10; disegno in D-76 e nell'HANDOFF, sezione 2-unvicies) | una riga per campo da cambiare fra un ciclo e l'altro, al posto della riapertura | se le modifiche fra un ciclo e l'altro diventano frequenti |
