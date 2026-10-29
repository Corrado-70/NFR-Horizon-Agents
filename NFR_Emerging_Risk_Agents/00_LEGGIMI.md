# Sistema di agenti NFR Emerging Risk — pacchetto di deploy

Famiglia di agenti Microsoft 365 Copilot per il monitoraggio dei rischi non
finanziari (NFR) emergenti di una banca significativa dell'area euro.
Pacchetto completo e collaudato a secco; nel tenant della Banca gira la
variante locale (Agent Builder e script sul PC, dal 24/09/2026). Copilot
Studio e' in prova (D-70, `09_Copilot_Studio`): la strada e' la decisione
aperta A-15.

> **Chi usa il sistema** (analista, validatore) legge solo
> `00_GUIDA_PASSO_PASSO.md`: cosa fare ogni settimana e ogni trimestre, come
> validare, cosa fare se qualcosa si ferma — setup del proprio PC compreso.
> Questo file e' per chi installa e mantiene il pacchetto. Per non ripetere lo
> stesso contenuto in piu' posti:
> - **"Si puo' fare, e come si fa una volta sola?"** -> `00_GUIDA_PASSO_PASSO.md`,
>   sezione "Avvio del progetto" (fasi, responsabili, verifiche, cancelli) e
>   sezione 0 (installazione). Fino al 07/10/2026 era `08_Deploy/Piano_deploy.md`.
> - **"Cosa faccio ogni settimana/trimestre, e come uso lo script?"** ->
>   `00_GUIDA_PASSO_PASSO.md`: in testa "In breve: i cicli standard" (un passo
>   per riga), poi le sezioni di dettaglio; sezione 8 per le mansioni degli agenti
>   e i messaggi da usare con le loro variazioni; sezione 9 per ogni comando
>   Python con parametri, opzioni, file scritti ed errori tipici.
> - **"Che campo scrivo in Agent Builder, esattamente?"** ->
>   `07_Senza_Studio/README_variante_locale.md`.
> - **"Che colonne ha questa tabella/lista, che regola segue questo campo?"**
>   -> la tabella "Dove vive ogni regola" qui sotto.

## Il sistema in una pagina

| Componente | Cadenza | Cosa fa | Scrive score? |
|---|---|---|---|
| A1 Horizon Scanner | trimestrale | valuta il registro rispetto ai due cicli precedenti analizzando nel dettaglio ogni fonte, propone azioni nuove e due KRI per rischio (esposizione ed evoluzione), rilegge i KRI del ciclo prima; riceve in un allegato baseline, controlli di A5 e guida di scrittura e li applica prima di rispondere (D-69); output JSON | propone |
| Precontrollo | **facoltativo, si puo' saltare**: trimestrale, dopo A1 e prima di A5 | **non e' un agente**: schema, controlli meccanizzati e parti del razionale sull'output di A1, con il messaggio di correzione per A1 (D-69); senza Excel | no |
| A5 Challenger | trimestrale, dopo A1, **facoltativo** (D-71) | nove controlli (C1-C9) su input ristretto; i suoi rilievi vanno in validazione (colonna Segnalazioni), un Bloccante chiede la Motivazione | no |
| A2 Scrittura | dopo A5 | **non e' un agente**: codice che valida, controlla, scrive e verifica | scrive cio' che A1 propone e A5 approva |
| A3 Interim Update | settimanale | integra le notizie, impatto sulle nove categorie di rischio, flag proposti (anche sui rischi in osservazione), proposta di ciclo straordinario | no |
| A4 News Assessor | su richiesta | parere su una notizia, ancorato alla valutazione deliberata | no |
| Registro unico: radar e osservazione | a ogni scrittura e validazione | un solo registro di rischi con la stessa scala; lo script mette nel radar di Mosca quelli con Prossimita e Probabilita alle soglie, fino alla capienza (15, fino a 20), piu' AGIRE ORA, temi del supervisore e decisioni del validatore; gli altri sono in osservazione (niente KRI ne' azioni, con orizzonte e segnale di avvicinamento); chi scende resta un ciclo "in uscita" (D-79, `07_Senza_Studio/radar.py`) | no: calcola |
| Validazione umana | dopo ogni trimestre (e, se si vuole, ogni settimana) | nel foglio Validazione, una riga per rischio (con la decisione sullo stato, D-79), KRI, azione e notizia (D-67): accetta (non tocca), rettifica (cambia la cella gialla) o respinge; il comando `valida` la applica e la registra campo per campo nel foglio Storico_Validazioni; senza, il trimestre dopo non parte | decide |
| A6 Schede dei rischi | trimestrale, dopo la validazione | testi estesi delle schede (il fenomeno in termini di rischio, perche' di ogni punteggio con i documenti, a cosa serve ogni fonte) sui dati validati, a partire dal razionale in parti di A1 (D-68); lo script li controlla (stessi rischi, stesse fonti, nessun numero nuovo) e produce `Schede_<ciclo>.xlsx` (D-40), con azioni e KRI accompagnati da perche' ed effetto atteso scritti da A1 | no: spiega |
| A7 Assistente del registro | su richiesta, in chat | risponde sul perche' delle valutazioni del registro e del radar (valori, urgenza, livello, cosa e' cambiato, fenomeni non censiti, rischi in osservazione), distinguendo registrato, calcolato e sua lettura; legge la cartella `Spiegazioni` della library Kernel, riscritta dallo script; su richiesta una sintesi per le Note dell'analista del Quadro (D-72) | no: spiega |
| A8 Evento critico | nel ciclo straordinario, deciso dalla funzione di rischio | analisi approfondita dell'evento sui documenti indicati (fatto, catena causale, rischi toccati e non toccati, documenti, limiti: campo `analisi_evento`), rivaluta i rischi indicati e censisce i nuovi che l'evento crea; stesso allegato e stesso formato di A1, quindi stessi `precontrollo` (facoltativo), `trimestrale` e validazione (D-77) | propone |
| Radar_Mosca | automatico | urgenza (disuguaglianza di Mosca X + Y > Z) e magnitudo (Probabilita x Impatto) di ogni rischio | no: calcola |
| Report al comitato | ogni trimestre, dopo la validazione | PDF dei fogli Quadro (il quadro d'insieme, con il commento di A1 e i rischi segnalati), Classifica e lente di Mosca, Radar_Mosca, Matrice, Delta, Fenomeni (i rischi in osservazione, D-79), Metodologia dell'Excel validato (D-32, D-39), piu' il file delle schede | no: legge |

Principi, non negoziabili:
1. **LLM per il giudizio, codice per calcolo, versioning e disegno.** Gli agenti
   danno le quattro dimensioni (la Velocity solo se le fonti ne documentano i
   tempi) e gli anni di adeguamento, con la rilevanza di ogni fonte; mai lo
   score composito ne' l'esito: lo
   calcola il foglio con i pesi di Parametri (D-50: media pesata delle dimensioni valutate).
2. **Lo stato e' storico e non si riscrive**: RiskRegister, Azioni, KRI e
   NewsLog sono tabelle storiche (una riga per soggetto per ciclo o per
   notizia, solo in coda); con Power Automate sono copiate anche nelle liste
   SharePoint. Ogni ciclo e ogni settimana lasciano inoltre un Excel congelato.
3. **Solo un ciclo di valutazione modifica uno score**: il trimestrale o, per
   un evento critico, il ciclo straordinario `AAAAQn-Sk` (D-41, D-75), deciso
   dalla funzione di rischio, che rivaluta solo i rischi indicati (o censisce
   solo rischi nuovi) con A8 e la stessa catena di controlli e validazione
   (D-77). A3 e A4 possono proporlo, non deciderlo.
4. **Ogni controllo di giudizio ha una controparte deterministica** dove il
   vincolo e' esprimibile, e ogni controllo e' a sua volta collaudato.
5. **Coerenza fra componenti come requisito di progetto**: la mappa
   sorgente->destinazione e i riferimenti incrociati sono verificati dal codice.
6. **Un prompt non contiene commenti**: il perche' sta nei file _DOCUMENTATO.
7. **Nessuna valutazione vale senza una persona che la valida**, e ogni
   rettifica conserva la proposta dell'agente, il valore deciso e il motivo:
   e' la base dati per insegnare agli agenti.

## Indice dei file

```text
00_LEGGIMI.md                                          questo file
00_GUIDA_PASSO_PASSO.md                                la guida per chi usa il sistema: cicli standard in breve, settimana, trimestre, validazione, errori, agenti e messaggi (sez. 8), comandi Python (sez. 9)
TODO_possibili_sviluppi.md                             piano unico del lavoro da fare, con l'ordine di lavoro in testa: passi sul PC della Banca (B1-B7), processi (P1, P2, P4-P7, P9: segnali qualitativi per dimensione sul radar, scia, rapporti di scenario, rischi collegati, schede per driver, riepilogo mensile, temi da verificare), automazione del processo (AU1-AU6; scelta fra strada A e Copilot Studio: A-15), quantificazione (Q1), grafici (G1-G6), pulizia, questioni aperte; in fondo il fatto, una riga per voce, e le voci in riserva
01_Kernel/tassonomia_nfr.md                            9 categorie di rischio in perimetro della tassonomia interna (D-74) + 8 driver emergenti
01_Kernel/fonti.md                                     elenco commentato delle fonti (rss, siti, share), DA VALIDARE
01_Kernel/rubrica_scoring.md                           4 dimensioni del composito (Impatto, Probabilita, Prossimita, Velocity facoltativa; pesi D-50 nelle note), anni di adeguamento, rilevanza delle fonti, regole di variazione, KRI (1-3, soglie facoltative), notizie, urgenza (Mosca, anni di adeguamento); presidio dei controlli della Banca (D-49)
01_Kernel/controlli_A5.md                              testo unico dei nove controlli C1-C9: istruzioni di A5 e allegato di A1 (D-69)
01_Kernel/guida_scrittura_A1.md                        come A1 scrive descrizione, razionale in parti, azioni e KRI, con un esempio di forma (allegato di A1, D-69)
01_Kernel/schema_output_A1.json                        contratto dell'output di A1
01_Kernel/schema_output_A3.json                        contratto dell'output di A3
01_Kernel/schema_output_A5.json                        contratto dell'esito di A5 (e dei controlli meccanizzati)
01_Kernel/schema_output_A6.json                        contratto dell'output di A6 (testi delle schede)
01_Kernel/schema_output_A1_DOCUMENTATO.md              i quattro schemi campo per campo, la baseline e l'input delle schede
01_Kernel/mappatura_campi.json                         UNICA mappa campo -> colonna; la leggono generatore, scrittura e collaudo
02_Agenti/A1_Horizon_Scanner.md                        prompt operativo (generato: non modificare a mano)
02_Agenti/A3_Interim_Update.md                         prompt operativo (generato)
02_Agenti/A4_News_Assessor.md                          prompt operativo (generato)
02_Agenti/A5_Challenger.md                             prompt operativo (generato)
02_Agenti/A6_Schede.md                                 prompt operativo (generato)
02_Agenti/A7_Assistente_registro.md                    prompt operativo (generato)
02_Agenti/A8_Evento_critico.md                         prompt operativo (generato)
02_Agenti/componi_prompt.py                            compone i prompt da modelli + kernel, controlla il limite di 8.000 caratteri
02_Agenti/modelli/A1.md                                modello del prompt A1 (qui si modificano le istruzioni)
02_Agenti/modelli/A3.md                                modello del prompt A3
02_Agenti/modelli/A4.md                                modello del prompt A4
02_Agenti/modelli/A5.md                                modello del prompt A5
02_Agenti/modelli/A6.md                                modello del prompt A6
02_Agenti/modelli/A7.md                                modello del prompt A7 Assistente del registro (spiegazioni in chat, D-72)
02_Agenti/modelli/A8.md                                modello del prompt A8 Evento critico (ciclo straordinario: analisi dell'evento, rivalutazione e censimento, D-77)
02_Agenti/COMMENTATI/A1_Horizon_Scanner_DOCUMENTATO.md  il perche' di ogni passo di A1
02_Agenti/COMMENTATI/A3_A4_A5_DOCUMENTATO.md           il perche' di ogni passo di A3, A4, A5, A6, A7, A8
03_Excel/genera_dashboard.py                           genera il template (colonne dalla mappa, scale e limiti dal kernel e dalla governance, dati di esempio); VERSIONE_TEMPLATE
03_Excel/NFR_Dashboard_Template.xlsx                   versione 2026-10-07 (Note dell'analista nel Quadro; validazione una riga per oggetto con la colonna Segnalazioni dei controlli, livello di allerta nel radar, tipo dei KRI, sintesi settimanale di A3): 22 fogli in quattro gruppi (Guida; report Quadro..Metodologia; lavoro Registro..Dizionario, con la griglia Validazione; dati, con Storico_Validazioni), ognuno con fascia del titolo e guida in testa; 7 tabelle dall'intestazione in riga 5 (sopra, gruppi e significato delle colonne); 9 grafici; 12 rischi di esempio grigi, capienza 20
03_Excel/costruzione_manuale_template.md               come rifare il template a mano, senza Python
04_Riferimenti/DECISIONI.md                            registro delle decisioni: prese (con data, chi, perche', stato), aperte (con responsabile), cancelli G0-G4
04_Riferimenti/struttura_e_liste.md                    SharePoint: 7 library, 3 liste storiche
04_Riferimenti/workflow.md                             W0-W3, passi [Piattaforma]/[Umano], campi derivati, test in ambiente
04_Riferimenti/controlli_e_model_risk.md               governance: controlli e controparti, evidenze per ciclo, model risk, limiti
04_Riferimenti/Prove/Prova_A7.md                       copione di prova di A7 Assistente del registro: undici domande con i fatti attesi, confronto con e senza il registro Excel come knowledge, tabella dei risultati (D-72)
04_Riferimenti/Prove/Prova_senza_Copilot_Studio.md     prova sul PC della Banca della versione del 05/10: installazione sul registro vero, poi un ciclo completo su un registro di prova separato, con la tabella dei risultati
04_Riferimenti/Tassonomia dei Rischi.csv               tassonomia interna dei rischi della Banca (famiglie e categorie; SI = in perimetro dell'agente NFR), fornita dall'utente il 07/10: fonte delle nove categorie di tassonomia_nfr.md (D-74); non la legge nessun componente
07_Senza_Studio/README_variante_locale.md              variante Agent Builder + script locale
07_Senza_Studio/esegui_ciclo_locale.py                 A2 e controlli di A5: trimestrale, settimanale, baseline (con l'allegato di A1), precontrollo (facoltativo: output di A1 controllato senza scrivere, messaggio di correzione), valida (dalla griglia del foglio Validazione), griglia (la ricostruisce), riapri (riapre la validazione di un ciclo gia' validato per cambiare valori, D-76), inizializza (registro vuoto), dismetti, aggiorna-registro (template nuovo), schede-input e schede (file delle schede con A6), report (PDF del report al comitato, rigenerabile dopo modifiche manuali; lo rigenera anche valida, D-83), diagnosi (sola lettura: asimmetrie delle valutazioni, D-80), sblocca (lucchetto rimasto per errore, D-83); archivio con Excel di output; ogni comando che scrive prende il lucchetto e lavora su una copia di lavoro del registro (D-83)
07_Senza_Studio/schede.py                              schede dei rischi: input di A6 dal registro validato, controlli sull'output di A6, file Schede_<ciclo>.xlsx
07_Senza_Studio/spiegazioni.py                         knowledge di A7: Ciclo.txt e un file per posto dell'anagrafica (Rischio_01..20.txt, nomi fissi) nella cartella Spiegazioni della library Kernel, riscritti da trimestrale, valida e dismetti (D-72)
07_Senza_Studio/raccogli_notizie.py                    W0 locale: scarica i feed dell'elenco fonti e scrive la raccolta settimanale in News_Inbox
07_Senza_Studio/fonti.py                               unico lettore di 01_Kernel/fonti.md (script, prompt, collaudo)
07_Senza_Studio/input_a1.py                            allegato di A1 Input_A1_<ciclo>.txt (baseline, controlli, guida) e unico lettore di controlli_A5.md (D-69); legge la baseline dall'allegato (skill, D-70); allegati di A3 e A4 Input_A3_A4.txt (AU7)
07_Senza_Studio/lucchetto.py                           lucchetto del registro per piu' analisti (D-83): Archivio_Cicli/_Lucchetto/registro.json, avviso per non cominciare un lavoro che si fermerebbe (presa senza attesa di default), scadenza, sblocca registrato
07_Senza_Studio/NFR.cmd                                l'app NFR Horizon Scan con un doppio clic (D-83): lancia app_nfr.py senza console
07_Senza_Studio/installa.cmd                           installazione su un PC con un doppio clic (tappa M3): lancia installa.py
07_Senza_Studio/installa.py                            installazione (tappa M3): Python e tkinter, moduli con pip --user (o dalla cartella pacchetti), configurazione.json con una finestra, collegamenti, attivita' della raccolta del lunedi', cartelle sempre sul PC, Verifica del PC
07_Senza_Studio/installazione.py                       le parti dell'installazione senza effetti sul sistema (moduli, comando pip, unione e controllo della configurazione, XML di schtasks, collegamenti): le prova il collaudo
07_Senza_Studio/verifica_pc.py                         Verifica del PC (tappa M3): una riga per voce (Python, moduli, configurazione, cartelle, kernel, registro ed Excel con AutoSaveOn e FullName, lucchetto, appunti, link, collegamenti, attivita'), file in Archivio_Cicli/Verifiche_PC; anche dal menu Altro dell'app
07_Senza_Studio/report_html.py                         report al comitato in HTML (tappa M4), seconda uscita di report e valida: viste da Quadro a Metodologia, grafici SVG, schede di tutti i rischi, guida (con --con-lavoro le viste di lavoro); dati letti via COM dalla sessione del report o con openpyxl dal file; cancello: numeri confrontati con le viste di Excel, se uno non torna l'HTML non esce; Cicli/Indice_report.html
07_Senza_Studio/notizie_manuali.py                     "Invia a -> NFR notizie manuali": copia i file scelti in News_Inbox/<lunedi'>/Manuali senza sovrascrivere
07_Senza_Studio/NFR_notizie_manuali.cmd                destinazione del collegamento in Invia a: lancia notizie_manuali.py
07_Senza_Studio/app_nfr.py                             la finestra dell'app (tkinter): stato, prossimo passo, un pulsante per processo, passo in corso con le istruzioni per l'agente, uscita del motore
07_Senza_Studio/flussi.py                              i processi dell'app come sequenze di passi (settimana, trimestre con il giro di correzione, straordinario, validazione, schede e report, riapertura, testi a mano, dismissione, parere di A4), su un Ambiente che la finestra realizza e il collaudo simula
07_Senza_Studio/stato.py                               stato del processo e prossimo passo, senza Excel, dall'archivio condiviso (baseline, cicli, settimane, In_arrivo, lucchetto)
07_Senza_Studio/ingresso.py                            ingresso unico delle risposte degli agenti: JSON estratto dal testo copiato (recinti, testo attorno, risposta tagliata), agente riconosciuto dagli schemi, file in Archivio_Cicli/In_arrivo; pareri di A4 in Pareri
07_Senza_Studio/appunti.py                             appunti di Windows per l'app: copia nuova riconosciuta dal numero di sequenza, le copie dell'app ignorate
07_Senza_Studio/esecutore.py                           il motore lanciato dall'app in un processo a parte: uscita riga per riga, fascia OK / FERMATO / ERRORE TECNICO, log in Archivio_Cicli/Log
07_Senza_Studio/precontrollo.py                        regole del precontrollo dell'output di A1 (schema, controlli meccanizzati, parti del razionale, messaggio di correzione, impronta), senza Excel: le usano il comando precontrollo e la skill di Copilot Studio (D-69, D-70)
07_Senza_Studio/radar.py                               regola del registro unico (D-79): chi sta nel radar di Mosca e chi in osservazione (soglie, eccezioni, capienza, uscita in due cicli); la usano script, controlli, precontrollo e kit di Copilot Studio
07_Senza_Studio/diagnosi.py                            misure del comando diagnosi (D-80): valori all'ingresso dei rischi nuovi, verso delle rettifiche del validatore, rischi lontani senza anni di adeguamento
07_Senza_Studio/excel_com.py                           accesso al workbook tramite Excel desktop (COM)
07_Senza_Studio/controlli_a5.py                        controlli meccanizzati C1-C9 (C4 escluso, per disegno)
07_Senza_Studio/valida_output.py                       validatore JSON Schema generico, solo libreria standard
07_Senza_Studio/configurazione_esempio.json            percorsi da copiare in configurazione.json; utente, attesa del lucchetto (D-83); per l'app validatore_predefinito, raccolta_su_questo_pc, agenti, ascolta_appunti, link_agenti (guida, 0.3)
09_Copilot_Studio/Prova_con_Copilot_Studio.md          prova K0 di Copilot Studio (D-70): A1 e il precontrollo con il Code interpreter dell'esperienza standard (opzione 1) e con una skill nel sandbox della nuova esperienza (opzione 2); Teams e agent flow facoltativi; tabella dei risultati
09_Copilot_Studio/Prova_K6_Operatore.md                prova K6 (CS-1, 09/10): un Operatore con un argomento a passi fissi legge l'allegato di A1 da SharePoint, lo passa al sotto-agente A1 e salva il JSON in Archivio_Cicli\In_arrivo con un agent flow; cartelle di lettura e scrittura; tabella dei risultati
09_Copilot_Studio/Prove_CS1.md                         prove di fattibilita' della CS-1 dopo l'allineamento (TODO B5): domande all'IT e alla DPO, K6, K4 qualita' di A1, K11 piu' utenti, K12 A7, K7a sincronizzazione, K7b Excel senza nessuno davanti; tabella dei risultati
09_Copilot_Studio/prepara_kit.py                       per chi mantiene il pacchetto: compone lo script della skill dai moduli del pacchetto e i file da caricare
09_Copilot_Studio/genera_A1_CS.py                      per chi mantiene il pacchetto: compone l'A1 per Copilot Studio con variabili globali (K6-ter) dall'A1 attuale
09_Copilot_Studio/precontrollo-nfr/SKILL.md            istruzioni della skill precontrollo-nfr (scritte a mano)
09_Copilot_Studio/precontrollo-nfr/scripts/precontrollo_nfr.py  script unico della skill (generato da prepara_kit.py: precontrollo, controlli, validatore, parti del razionale, schema di A1)
09_Copilot_Studio/Da_caricare/precontrollo-nfr.zip     la skill da caricare nella nuova esperienza (opzione 2), cartella precontrollo-nfr alla radice (generato)
09_Copilot_Studio/Da_caricare/precontrollo-nfr_senza_cartella.zip  la stessa skill con SKILL.md alla radice dello zip, se la prima e' rifiutata (generato)
09_Copilot_Studio/Da_caricare/precontrollo_nfr.txt     lo script della skill in .txt, da allegare in chat con il Code interpreter (opzione 1; generato)
09_Copilot_Studio/Da_caricare/Messaggi_da_incollare.txt  i messaggi di ogni test della prova di Copilot Studio
09_Copilot_Studio/Da_caricare/A1_Horizon_Scanner_CS.md  istruzioni di A1 per Copilot Studio: allegato letto da {Global.allegato}, JSON anche in {Global.json_a1} (K6-ter, 22/10; generato)
99_Collaudo/LEGGIMI_collaudo.md                        cosa verifica la suite e con quali dati
99_Collaudo/esegui_collaudo.py                         lancia tutta la suite (catena in tre processi; --mirato la salta se non e' cambiato niente che la riguardi)
99_Collaudo/comune.py                                  percorsi e utilita' della suite
99_Collaudo/test_mappatura.py                          mappa in entrambe le direzioni
99_Collaudo/test_controlli.py                          validatore, controlli A5, dati di esempio, consistenza, precontrollo e kit di Copilot Studio, controlli sull'output di A6 e file delle schede
99_Collaudo/test_fonti.py                              elenco fonti, limiti di Agent Builder, raccolta con feed finti
99_Collaudo/test_report_html.py                        il report HTML senza Excel (tappa M4), sul registro della demo: cancello superato, pagine e schede, file autosufficiente, collegamenti interni, cancello che scatta con un numero alterato, indice, pubblicazione con la versione precedente
99_Collaudo/test_installazione.py                      l'installazione senza Excel (tappa M3): moduli e pip, configurazione (unione, link per versione, problemi), XML dell'attivita', collegamenti, Invia a, Verifica del PC su una configurazione di prova, lanciatori .cmd
99_Collaudo/test_app.py                                l'app e i piu' analisti, senza Excel (D-83): lucchetto (collega, scaduto, conflitto di OneDrive, sblocca), sostituzione dalla copia di lavoro, registro aperto; ingresso delle risposte, stato e prossimo passo su archivi finti, flussi con un Ambiente finto (giri di correzione, risposta tagliata), lanciatore NFR.cmd
99_Collaudo/verifica_riferimenti.py                    riferimenti incrociati fra file
99_Collaudo/run_catena.py                              tredici gruppi indipendenti (--parallelo, --passo): due cicli e due settimane con lo strumento vero ed Excel; primo uso e dismissione; piu' analisti (lucchetto, copia di lavoro, allegati di A3 e A4, prompt archiviati, D-83); registro di produzione dal vuoto al secondo ciclo; aggiornamento di un registro del template del 23/09 e del 2026-09-25c; A5 facoltativo e segnalazioni in validazione (D-71); comando report; report al comitato contro calcoli indipendenti; schede dei rischi con A6
99_Collaudo/confronta.py                               confronto fra due run di A1 (anche per il doppio run in tenant)
99_Collaudo/osserva_cartella.py                        strumento della prova K7a della CS-1: tempi della sincronizzazione fra SharePoint e PC
99_Collaudo/dati/baseline_2026Q3.json                  baseline estratta dal template
99_Collaudo/dati/run1_A1_2026Q3.json                   output A1 di prova, ciclo 2026Q3
99_Collaudo/dati/run2_A1_2026Q3.json                   secondo run sullo stesso input
99_Collaudo/dati/run_A5_2026Q3.json                    esito A5 di prova, 2026Q3
99_Collaudo/dati/run_A3_2026-10-12.json                output A3 di prova, con una notizia e un flag sul rischio in osservazione NFR-16 (il suo segnale si verifica)
99_Collaudo/dati/baseline_2026Q4.json                  baseline dopo il 2026Q3
99_Collaudo/dati/run3_A1_2026Q4.json                   output A1 di prova, ciclo 2026Q4, rischio nuovo
99_Collaudo/dati/run_A5_2026Q4.json                    esito A5 di prova, 2026Q4
99_Collaudo/dati/run4_A1_2026Q4-S1.json                output A1 di prova, ciclo straordinario 2026Q4-S1: solo NFR-01, Probabilita da 4 a 5 (D-75)
99_Collaudo/dati/decisioni_validatore_2026Q3.json      decisioni di prova del validatore sul 2026Q3 (cinque rettifiche, fra cui una Velocity da non valutata e le soglie di un KRI; un'azione respinta)
99_Collaudo/dati/decisioni_validatore_2026-10-12.json  decisioni di prova del validatore su una settimana
99_Collaudo/dati/registro_template_2026-09-23.xlsx     registro nato dal template del 23/09 (una settimana e il primo ciclo, validati): prova di aggiorna-registro
99_Collaudo/dati/baseline_registro_template_2026-09-23.json  baseline di quel registro: deve restare identica dopo l'aggiornamento
99_Collaudo/dati/registro_template_2026-09-25c.xlsx    registro nato dal template 2026-09-25c (un ciclo validato, con Gap_Controlli e Dimensione): prova delle colonne dismesse
99_Collaudo/dati/registro_template_2026-10-08b.xlsx    template di esempio del 07/10 con la lista di osservazione (D-73): prova della conversione al registro unico (D-79)
99_Collaudo/dati/baseline_registro_template_2026-09-25c.json  baseline attesa di quel registro dopo aggiorna-registro (senza Gap_Controlli, presidio "Non verificato")
```

## Dove vive ogni regola (una sola volta)

| Regola | Unica fonte | Chi la usa |
|---|---|---|
| Codici delle categorie e dei driver | `tassonomia_nfr.md` | prompt (composti), schemi, generatore, mappa — allineamento verificato dal collaudo |
| Descrittori, rilevanza delle fonti, regole di variazione | `rubrica_scoring.md` | prompt (composti), controlli di A5 |
| Elenco delle fonti (codici, canali, indirizzi) | `fonti.md` | prompt di A3 (composto), raccolta notizie, controllo dei codici fonte, collaudo |
| Pesi e soglie numeriche, parametri dell'urgenza (X, Y di riserva, anni per Prossimita) | celle di input di `Parametri` (valori iniziali nel generatore; pesi: D-50) | formule del workbook, foglio Metodologia |
| Anni di adeguamento di un rischio (Y minima di Mosca) | anagrafica in `Parametri`, colonna M, input del validatore (D-33) | Radar_Mosca, lente di Mosca |
| Attenzione del supervisore su un rischio | anagrafica in `Parametri`, colonna N, input del validatore (D-35) | ◆ nel Radar_Mosca, in Registro, Matrice, Quadro, schede |
| Significato di ogni colonna delle tabelle dati | `mappatura_campi.json`, chiave `significato` | riga 4 dei fogli dati e foglio Dizionario (generatore) |
| Guida in testa ai fogli, chi aggiorna cosa, dizionario dei dati | dizionari `GUIDE`, `CHI_AGGIORNA`, `COME`, `CALCOLATI` di `genera_dashboard.py` (D-38, D-39) | riga 2 di ogni foglio, Guida, Dizionario |
| Limiti della valutazione da dichiarare al comitato | `04_Riferimenti/controlli_e_model_risk.md`, sezione 5 | foglio Quadro (letto dal generatore) |
| Cosa A6 puo' scrivere nelle schede | `02_Agenti/modelli/A6.md` (regole) e `07_Senza_Studio/schede.py` (`controlla_a6`: stessi rischi, quattro dimensioni, stesse fonti, nessun numero fuori dai dati) | comando schede, collaudo |
| Parti del razionale di A1 (RISCHIO, IMPATTO, PROBABILITA, PROSSIMITA, VELOCITY, ADEGUAMENTO; EFFETTO per azioni e KRI) | scheletro di `02_Agenti/modelli/A1.md` (formato chiesto) e `schede.py` (`parti_razionale`, `parti_effetto`: come si leggono) (D-68) | input di A6, file delle schede, avviso di `trimestrale` |
| Versione della struttura del workbook | `VERSIONE_TEMPLATE` in `genera_dashboard.py` = in `esegui_ciclo_locale.py` = `versione_template` della mappa (verificato dal collaudo) | script di campo: si ferma su un registro o una mappa di un'altra versione |
| Metodo dell'urgenza (Mosca) | `rubrica_scoring.md`, sezione 8 (spiegazione) + foglio Radar_Mosca (calcolo) | Radar_Mosca |
| Cosa si valida e con quali regole | `mappatura_campi.json`, sezione `validazione` (oggetti e campi); regole in `esegui_ciclo_locale.py` (`controlla_valore`, `applica_validazione`); colonne della griglia del foglio Validazione in `genera_dashboard.py` (`GRIGLIA`, nomi `VG_...`) | scrittura, comando `valida`, generatore, collaudo |
| Formato dei payload | `schema_output_*.json` | validatore generico (lo interpreta, non lo ricopia) |
| Colonne delle tabelle e delle liste | `mappatura_campi.json` | generatore, scrittura, collaudo, documento SharePoint |
| Testo dei controlli C1-C9 | `01_Kernel/controlli_A5.md` (D-69) | prompt di A5 (`{{CONTROLLI}}`), allegato di A1 (`input_a1.py`) |
| Come A1 scrive i testi (descrizione, razionale, azioni, KRI) | `01_Kernel/guida_scrittura_A1.md` (D-69) | allegato di A1 (`input_a1.py`) |
| Controlli C1-C9 meccanizzabili | `controlli_a5.py` | script di campo (`precontrollo`, `trimestrale`), skill di Copilot Studio, collaudo |
| Precontrollo dell'output di A1 (cosa si controlla, messaggio di correzione, impronta) | `07_Senza_Studio/precontrollo.py` (D-69, D-70) | comando `precontrollo`, skill `precontrollo-nfr` (script composto da `prepara_kit.py`), collaudo |
| Istruzioni degli agenti | `02_Agenti/modelli/*.md` | `componi_prompt.py` |
| Chi scrive nel registro in questo momento (piu' analisti) | `07_Senza_Studio/lucchetto.py`, file `Archivio_Cicli/_Lucchetto/registro.json` (D-83) | ogni comando che scrive (`SCRIVONO` in `esegui_ciclo_locale.py`), `sblocca` |

Non ci sono copie di codice da tenere sincronizzate a mano: il validatore
e' uno, i controlli sono uno, la scrittura e' una (la usano entrambe le
varianti), la suite importa il codice vero. L'unica copia, lo script della
skill di Copilot Studio, la compone `09_Copilot_Studio/prepara_kit.py` dai
moduli del pacchetto, e il collaudo si ferma se non e' identica.

## Ordine di deploy

Il piano vero — dieci fasi, responsabili, verifiche, cancelli — e' **solo** nella
guida passo passo, sezione "Avvio del progetto": non e' ripetuto qui per non tenere due versioni
allineate a mano. In sintesi (per orientarsi, non per eseguire): **decisioni
della Banca prima di tutto** (tassonomia/rubrica/soglie da adattare —
segnaposto oggi, NON raccomandazioni; qualificazione model-risk; rapporto con
il processo di rischio operativo esistente; validazione di `fonti.md`), poi
adattamento del kernel, SharePoint, raccolta notizie, agenti, collaudo in
ambiente sul primo ciclo **da registro vuoto** (doppio run e validazione umana:
non serve un trimestre gia' valutato a mano), primo ciclo in parallelo al
processo attuale.
Dopo ogni adattamento del kernel: procedura "Se cambia il kernel" qui sotto.

## Se cambia il kernel (o uno schema, la mappa, un prompt)

1. Modificare la fonte unica (tabella qui sopra). Per le istruzioni degli
   agenti: il modello in `02_Agenti/modelli/`, mai il prompt generato.
2. `python 02_Agenti/componi_prompt.py` — rigenera i prompt e segnala se uno
   supera 8.000 caratteri.
3. `python 03_Excel/genera_dashboard.py` — se sono cambiate colonne, codici,
   scale della rubrica, testo dei limiti o dati di esempio. Se cambia la
   **struttura** del workbook (fogli, colonne, nomi definiti) alzare anche
   `VERSIONE_TEMPLATE` nel generatore, nello script di campo e nella mappa, e
   aggiornare il registro in uso con `aggiorna-registro`.
4. Se cambiano campi o codici, allineare anche documentazione e dati di prova:
   il collaudo dice cosa manca.
5. `python 99_Collaudo/esegui_collaudo.py` — deve finire con tutto OK.
6. Ricaricare i prompt negli agenti e archiviarne il testo (`04_Riferimenti/controlli_e_model_risk.md`).

## Requisiti

Per generare e collaudare: Python 3.10+, `openpyxl`, `pywin32`, `pypac`, Excel
desktop. In esercizio: nessun Python per chi legge il workbook; lo script di
campo richiede Python, `pywin32` ed Excel desktop sul PC che lo lancia, e
`openpyxl` per il comando `schede` (file delle schede);
`pypac` serve solo a `raccogli_notizie.py`, per instradare il traffico come
fa il browser quando il proxy e' configurato con un file di autoconfigurazione
(PAC) invece di un indirizzo fisso.
