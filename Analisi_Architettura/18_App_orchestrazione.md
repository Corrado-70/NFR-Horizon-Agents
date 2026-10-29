# 18. App Python di orchestrazione: piano e avanzamento (strada A, ramo `main`)

Data: 23/10/2026. Decisione D-83 (chiude A-15 e A-16). Piano approvato dall'utente il 23/10, a tappe M1-M4.

Questo documento e' il **registro di avanzamento** dell'app: a ogni passo si aggiornano le spunte. Il TODO (sezione 4)
ne tiene solo la tabella riassuntiva; il racconto di cio' che e' stato fatto e' nell'HANDOFF.

**Legenda**
- `[x]` fatto e collaudato;
- `[~]` fatto, da verificare (catena con Excel, demo, prova in Banca): la colonna "Dove si verifica" dice come;
- `[ ]` da fare.

## 18.0 Il quadro

| Tappa | Cosa | Stato |
|---|---|---|
| M1 | motore: piu' analisti (lucchetto, copia di lavoro), AU7, automatismi | fatta e collaudata (catena 375/375, gruppi rilanciati verdi); restano le prove in Banca |
| M2 | l'app: finestra, flussi, stato, ingresso delle risposte | fatta; da provare con gli agenti veri e nella demo |
| M3 | installazione con un doppio clic e Verifica del PC | da fare |
| M4 | report HTML al comitato, seconda uscita di `report` | da fare |
| M5 | funzioni amministrative: pulizia dell'archivio, ritorno indietro di N trimestri, ripartenza da zero, tutto nel parcheggio | da fare (richiesta del 23/10) |

Scelte dell'utente (23/10):
- finestra tkinter;
- risposte dagli appunti piu' il file;
- piu' analisti sullo stesso registro;
- report HTML dentro il piano, generato solo su ciclo validato, "un secondo tipo di report al comitato".

Fuori dal piano: la coda delle richieste della CS-1 e la variante V4.

```
NFR.cmd ──> app_nfr.py  (tkinter: stato, prossimo passo, pulsanti dei processi, passo in corso, log, esito)
              │  flussi.py      sequenze dei processi su un Ambiente (finestra, o finto nel collaudo)
              │  stato.py       stato e prossimo passo, senza Excel, dall'archivio condiviso
              │  ingresso.py    risposte degli agenti: JSON dal testo copiato, agente dallo schema, In_arrivo
              │  appunti.py     ascolto degli appunti
              │  esecutore.py   motore in un processo a parte, fascia dell'esito, log
              ▼
esegui_ciclo_locale.py  (motore: lucchetto + copia di lavoro + report)  ──> registro Excel, archivio, knowledge di A7
```

L'app non contiene regole di metodo; nel registro scrive solo il motore (D-10).

## 18.1 Tappa M1: il motore

### F0. Decisioni e configurazione

| Stato | Voce | Dove si verifica |
|---|---|---|
| [x] | D-83 in DECISIONI; A-15 e A-16 chiuse; D-82 riportata dal ramo | `04_Riferimenti/DECISIONI.md` |
| [x] | Regola dei due rami in `CLAUDE.md` (commit 98ce507 e f52d105) | `CLAUDE.md` |
| [x] | `configurazione()` legge `utente`, `cartella_lavoro`, `attesa_lucchetto` (con `NFR_ATTESA_LUCCHETTO` e `NFR_CARTELLA_LAVORO`) | `test_app.py`, catena `piu_analisti` |
| [x] | `configurazione_esempio.json` con le chiavi del motore e dell'app (`link_agenti`, `validatore_predefinito`, `raccolta_su_questo_pc`) | — |

### F1. Automatismi e AU7

| Stato | Voce | Dove si verifica |
|---|---|---|
| [x] | AU7: `baseline` scrive l'allegato di A3 e A4 (`input_a1.scrivi_allegato_a3_a4`; dal 23/10 sera un file solo, `Input_A3_A4.txt`, D-84) | catena `piu_analisti` (7/7) |
| [x] | Prompt di A3 e A4: baseline solo dall'allegato (A3 7.691 caratteri, A4 5.711) | `componi_prompt.py --verifica` |
| [x] | Nomi degli allegati unificati (D-84): `Input_A1_<ciclo>`, `Input_A8_<periodo>`, `Input_A3_A4`, `Input_A5_<ciclo>` (dal precontrollo), `Input_A6_<ciclo>`; prompt di A3, A4, A5 (7.994 caratteri), A6, A8 | `test_controlli.py`, `test_app.py`; catena 375/375 e demo rigenerata (23/10 sera) |
| [x] | Il ramo `copilot-studio-pieno` con i nomi nuovi: merge di `main` (4aea653), `genera_CS.py` (A3, A5, A6, A8), argomenti YAML, test del ramo (290/293: restano i 3 KO noti dei fine riga CRLF di quella cartella) | merge del 23/10 sera |
| [~] | A3, A4, A5, A6 e A8 reincollati in Agent Builder (D-84); `Baseline_corrente.txt` tolto dalla knowledge e dalla library Kernel | in Banca, B5-bis |
| [x] | `trimestrale` archivia i prompt in `Cicli/<ciclo>/Prompt_in_uso/` | catena `piu_analisti` |
| [x] | `valida` del ciclo corrente rigenera il report; `--senza-report` | catena `catena` 178/178 e `riapertura` 28/28 (rilanciate il 23/10) |
| [x] | Il PDF di `valida` entra nell'archivio solo dopo la sostituzione del registro e dopo `Validazione_<ciclo>.json` (`esporta_pdf`, `pubblica_report`) | catena `catena`, `riapertura` |
| [x] | `schede` produce anche `Schede_<ciclo>.pdf` | demo rigenerata il 23/10 (`Schede_2026Q4.pdf`) |
| [x] | `riapri` lascia `Riapertura_<ciclo>.json`, `valida` la chiude | catena `riapertura` |
| [x] | La copia della baseline nel Kernel non serve piu' (sostituita da AU7) | — |

### F2. Scrittura robusta e piu' analisti

| Stato | Voce | Dove si verifica |
|---|---|---|
| [x] | `lucchetto.py`: presa (in due tempi solo se configurata: attesa 0 di default dalla sera del 23/10, scelta dell'utente), scadenza, ripresa del proprio lucchetto, copia in conflitto di OneDrive, rilascio anche dopo un errore | `test_app.py` |
| [x] | Comando `sblocca` registrato in `sblocchi.log` | `test_app.py`, catena `piu_analisti` |
| [x] | I comandi che scrivono prendono il lucchetto; quelli che leggono no | catena `piu_analisti` |
| [x] | Copia di lavoro (`sessione_registro`): sostituzione solo con l'impronta invariata, nessun file temporaneo rimasto | `test_app.py`, catena `piu_analisti` |
| [x] | Registro aperto in un programma del PC: fermo prima di scrivere | `test_app.py`, catena `piu_analisti` |
| [x] | `AutoSaveOn` spento nelle sessioni in scrittura | catena (tutti i gruppi) |
| [x] | Tutti i gruppi della catena con la copia di lavoro (`SALVATO` = sostituito; errore dopo il salvataggio, gate) | catena completa 375/375 (23/10, 61 minuti) |
| [~] | Lucchetto fra due PC con OneDrive; `AutoSaveOn` e `FullName` del registro vero (V-F) | in Banca, B5-bis |

## 18.2 Tappa M2: l'app

### F3. Ingresso delle risposte

| Stato | Voce | Dove si verifica |
|---|---|---|
| [x] | `ingresso.py`: BOM, recinti, testo attorno, l'oggetto di un agente fra piu' oggetti | `test_app.py` |
| [x] | Risposta tagliata riconosciuta anche con oggetti interi dentro; unione delle parti | `test_app.py` |
| [x] | Agente dagli schemi (A1, A3, A5, A6; A8 dal periodo straordinario); un testo senza JSON e' un parere di A4 | `test_app.py` |
| [x] | Salvataggio in `In_arrivo` (UTF-8 senza BOM), originale in `Originali/`, file di prima in `Precedenti/` | `test_app.py` |
| [x] | Messaggio di correzione per A3, A5, A6 | `test_app.py` |
| [x] | Riquadro "Risposta dell'agente": la risposta si incolla nell'app (richiesta dell'utente del 23/10); ascolto degli appunti in piu' (`ascolta_appunti`) | prova della finestra |
| [x] | Agenti in Agent Builder o in Copilot Studio: stessi nomi e cartelle, origine annotata; JSON dentro il campo `text` di Copilot Studio | `test_app.py` |
| [~] | Copia e incolla di una risposta vera di Agent Builder, anche per un A1 di 40 KB (V-B, V-C); lo stesso con un agente di Copilot Studio | in Banca, B5-bis |

### F4. Stato del processo ed esecutore

| Stato | Voce | Dove si verifica |
|---|---|---|
| [x] | `stato.py`: prossimo passo per ogni situazione (baseline, validazione, riapertura, straordinario, trimestre chiuso, report, schede, settimana, lucchetto) | `test_app.py` |
| [x] | Passi annotati in `Archivio_Cicli/Stato/<periodo>.json` | `test_app.py` |
| [x] | `esecutore.py`: motore in un processo a parte, fascia, log in `Archivio_Cicli/Log/`, lettura del precontrollo | `test_app.py` (lettura), prova della finestra |
| [~] | Esecutore con il motore vero dalla finestra (Excel, tempi, log) | demo attraverso i flussi; in Banca |

### F5. Flussi

| Stato | Voce | Dove si verifica |
|---|---|---|
| [x] | Trimestrale: baseline, A1, precontrollo con il giro di correzione nella stessa chat, A5 facoltativo, trimestrale con il suo giro | `test_app.py` (Ambiente finto) |
| [x] | Ripresa di un processo interrotto dalla risposta gia' in `In_arrivo` | `test_app.py` |
| [x] | Validazione: registro aperto, attesa della chiusura, `valida` | `test_app.py` |
| [x] | Settimanale: raccolta, Manuali, A3 con l'allegato, fermo e correzione | `test_app.py` |
| [~] | Straordinario, schede (con e senza A6), report, riapertura, testi a mano, dismissione, parere di A4, A7, diagnosi, sblocca | scritti; da coprire nel collaudo e nella demo |
| [ ] | Demo (`Demo_W1_W2/esegui_demo.py`) attraverso i flussi, con appunti simulati: A1 con i recinti, A1 in due parti, correzione dopo un fermo | — |

### F6. Finestra

| Stato | Voce | Dove si verifica |
|---|---|---|
| [x] | `app_nfr.py`: stato, prossimo passo, pulsanti, passo in corso, log colorato; processi in un thread, chiamate alla finestra da una coda | prova di avvio con un archivio finto (immagine controllata) |
| [x] | Nitida con la scala di Windows oltre il 100%; finestra in proporzione allo schermo | prova di avvio |
| [x] | Schermi 1920x1080 con la scala al 100, 125 e 150%: si apre ingrandita, uscita del motore leggibile | simulazione dello schermo |
| [x] | Divisore trascinabile fra passo in corso e uscita; riquadro della risposta alto e visibile dopo l'incolla; riga dell'esito sotto il riquadro (richiesta dell'utente del 23/10) | simulazione a 100% e 150% |
| [x] | `NFR.cmd`: ASCII, cartella dello script, UTF-8, `pyw`/`pythonw`/`python` | `test_app.py` |
| [x] | Aiuto nell'app dalla guida (richiesta dell'utente del 29/10): pulsante "Aiuto (F1)" con gli argomenti principali e "Apri la guida completa"; suggerimenti sui pulsanti dalla tabella "I processi"; nessuna copia dei testi (`aiuto.py`) | `test_app.py` (test_aiuto); prova della finestra con Xvfb |
| [x] | Che cosa sta facendo l'app, sempre detto (richiesta dell'utente del 29/10, dopo la prima prova in Banca): nella fascia il processo e la fase; nel passo in corso il comando in esecuzione con il tempo trascorso e la durata attesa, la domanda o il modulo in attesa, l'attesa della chiusura di Excel; domande e moduli in primo piano con un suono; "Ho chiuso Excel: controlla ora" controlla davvero il file; a fine processo quale processo e' finito e quando | prova della finestra con Xvfb (testi di ogni fase); in Banca |
| [~] | Uso vero: un trimestre di prova dall'app, con gli agenti in Agent Builder e il registro di prova | in Banca, B5-bis |
| [~] | Link degli agenti da "Copia collegamento" che aprono la chat (V-A) | in Banca, B5-bis |

### Documenti delle tappe M1 e M2

| Stato | Voce |
|---|---|
| [x] | Guida: sezione "L'app NFR: uso passo per passo" (finestra, tre gesti, ogni processo, ripresa); 0.2 con i link degli agenti e senza prompt schedulato; 0.2-bis agenti in Copilot Studio; 0.3 con la tabella di `configurazione.json`; 0-bis, 1, 2, 3, 3-ter, 7, 8, 9 |
| [x] | 00_LEGGIMI (moduli e regola del lucchetto), README della variante locale, LEGGIMI del collaudo |
| [x] | controlli_e_model_risk (due analisti, salvataggio a meta', evidenze), documentazione di A3 e A4 |
| [x] | PROMPT_MASTER (motore, app, archivio, struttura; trappole 122-129) |
| [x] | TODO (tabella delle tappe, AU7 e AU4 fatte, B5-bis), HANDOFF (2-tertricesies), analisi 12, 14 e 16 (esito) |
| [x] | Presentazione: slide dei comandi, del trimestre, di A3 e A4 |
| [x] | Presentazione: slide "L'app NFR" con l'immagine della finestra (69 slide; immagine `Presentazione/app_finestra.png`) |
| [x] | Demo rigenerata (23/10) e `REPORT_demo.md` riallineato (report da `valida`, PDF delle schede, prompt archiviati, riapertura, allegati di A3 e A4) |
| [x] | Commit e push: 68b891f su `main` (23/10) |

## 18.3 Tappa M3: installazione e Verifica del PC (fatta il 29/10/2026; prove sul PC in Banca)

| Stato | Voce | Dove si verifica |
|---|---|---|
| [x] | `installa.cmd` + `installa.py`: Python 3.10+, tkinter, pywin32 (con pythoncom), openpyxl, pypac provati in un processo nuovo; `pip install --user` di cio' che manca, dalla rete o dalla cartella `pacchetti` (`--no-index`); messaggio chiaro se il proxy blocca, con la strada della cartella | `test_installazione.py` |
| [~] | pip dietro il proxy della Banca, oppure la cartella `pacchetti` | in Banca |
| [x] | `configurazione.json` da una finestra: quattro cartelle con Sfoglia, utente, validatore, PC della raccolta, opzioni dell'app (appunti, `chiedi_a5`), versione e link dei 7 agenti; valori proposti da quella che c'e', voci sconosciute conservate, precedente accanto | `test_installazione.py`; prova della finestra con Xvfb (ha trovato la trappola 134) |
| [x] | Collegamento sul Desktop "NFR Horizon Scan" (pythonw, senza console); "Invia a -> NFR notizie manuali" (`notizie_manuali.py`: cartella Manuali del lunedi', mai sovrascrivere) | `test_installazione.py` (script e copia) |
| [~] | Collegamenti creati davvero su Windows (V-E) | in Banca |
| [x] | Attivita' pianificata della raccolta (`schtasks /create /xml`, UTF-16, lunedi' 7:00, senza privilegi, appena possibile se il PC era spento) solo sul PC della raccolta; `attrib +P` a richiesta | `test_installazione.py` (XML) |
| [~] | schtasks permesso all'utente (V-E) | in Banca |
| [x] | Verifica del PC (`verifica_pc.py`, Altro -> Verifica del PC): Python, moduli, configurazione, cartelle scrivibili, kernel e template, registro chiuso, Excel via COM con versione, `AutoSaveOn` e `FullName` (V-F), lucchetto, appunti, link, collegamenti, attivita'; file in `Archivio_Cicli/Verifiche_PC/` | `test_installazione.py` (senza Excel) |
| [~] | Verifica del PC con Excel vero (V-F) | in Banca |
| [x] | Guida, sezione 0.3 riscritta attorno a `installa.cmd` (a mano come alternativa), raccolta, Altro, sezione 7; 00_LEGGIMI, README, PROMPT_MASTER (trappole 132-134), TODO | `verifica_riferimenti.py` (comandi e opzioni citati) |
| [x] | Domanda su A5 a precontrollo superato (richiesta del 29/10; `chiedi_a5`) | `test_app.py` |

## 18.4 Tappa M4: report HTML al comitato (fatta il 29/10/2026; catena con Excel sul PC)

| Stato | Voce | Dove si verifica |
|---|---|---|
| [x] | `report_html.py` dal prototipo `16_genera_anteprima_html.py` (che ne e' diventato un involucro: un solo codice): viste da Quadro a Metodologia, grafici SVG, schede di tutti i rischi collegate, guida | `test_report_html.py` sulla demo; anteprima rigenerata, differenze solo nei testi dello "scenario" |
| [x] | Dati letti dalla stessa sessione COM di `report` e `valida` (`RegistroExcel`: tabelle, nomi definiti, celle), non da openpyxl; `RegistroFile` (openpyxl) per collaudo, demo e anteprima | codice; catena: HTML via COM = HTML dal file |
| [~] | Lettura via COM provata con Excel | catena (`verifica_html_excel`), sul PC |
| [x] | Cancello: X, Y, Z, margine, urgenza, livello e motivo, segnali netti, ordine della classifica, Delta contro le viste di Excel; se uno non torna l'HTML non esce, il PDF si', con l'avviso | `test_report_html.py` (dato alterato e cella alterata: trappola 135) |
| [~] | Cancello con Excel vero (dato alterato nella sessione) | catena, sul PC |
| [x] | File unico autosufficiente; ciclo, dati al, data della validazione e validatore in testa; versione precedente conservata; riassunto accanto; `Cicli/Indice_report.html` | `test_report_html.py` |
| [x] | `--con-lavoro`: Registro, Storico, Indicatori, Notizie, Piano azioni, Osservazione, Validazione, Parametri, Dizionario | `test_report_html.py`; catena (`report --con-lavoro`) |
| [x] | `valida` pubblica PDF e HTML insieme; lo stato dell'app guarda anche l'HTML ("pronto, PDF e HTML" / "solo PDF") | `test_app.py`; catena (2b) |
| [x] | Guida (sezioni 4, 5, 9, app), README, 00_LEGGIMI, PROMPT_MASTER (trappole 135-136), TODO, analisi 16; testi della presentazione nel generatore | `verifica_riferimenti.py`; la presentazione (.pptx) si rigenera sul PC con Excel |

## 18.5 Tappa M5: funzioni amministrative (fatta il 29/10/2026; richiesta dell'utente del 23/10/2026)

Pulizia dell'archivio e "ritorno indietro nel tempo". Regola di fondo: **niente si cancella subito**. Tutto cio' che si
toglie va in un **parcheggio** (`Archivio_Cicli/_Parcheggio/<data_ora>_<operazione>/`) con un atto che dice chi, quando,
perche' e che cosa. Si svuota solo con un comando a parte e dopo un tempo minimo. Ogni operazione prende il lucchetto,
chiede la conferma scritta (ritorno e ripartenza), lascia la traccia in `Archivio_Cicli/Amministrazione/` e si annulla
rimettendo a posto il parcheggio. In `amministrazione.py` e nella finestra del pulsante Admin dell'app.

| Stato | Voce | Dove si verifica |
|---|---|---|
| [x] | **Pulizia dell'archivio** con anteprima e spazio: tentativi dei cicli validati, backup oltre gli ultimi N, versioni precedenti dei report, In_arrivo (Originali, Precedenti) dei periodi chiusi, log e verifiche vecchi; tutto nel parcheggio | `test_amministrazione.py`; catena (9) |
| [x] | **Ritorno al ciclo validato C**: registro dall'Excel validato di C; nel parcheggio registro attuale, cicli e straordinari dopo C, settimane scritte o validate dopo, baseline, allegati, knowledge di A7, risposte di quei periodi; poi `baseline`; lo stato riparte da "Ciclo C: VALIDATO" | `test_amministrazione.py` (senza Excel); catena (9, baseline vera) |
| [x] | Controlli del ritorno: C validato con il suo Excel validato, prima del corrente, stessa versione del template; motivo (almeno 20 caratteri) e decisore; conferma scritta | `test_amministrazione.py` |
| [x] | **Annulla**: rimette il parcheggio, se nel frattempo non si e' scritto nel registro (impronta); cio' che occupa i posti in un parcheggio "annullamento"; un parcheggio annullato non si annulla due volte | `test_amministrazione.py`; catena (9) |
| [x] | **Ripartenza da zero**: registro nuovo con `inizializza` e baseline; il vecchio registro e l'archivio dei cicli nel parcheggio; restano log, verifiche, parcheggi e traccia | `test_amministrazione.py` (senza Excel) |
| [~] | Ripartenza con Excel vero | sul registro di prova in Banca |
| [x] | **Svuota il parcheggio**: solo i parcheggi piu' vecchi di `giorni_parcheggio`, anteprima e poi `--esegui`; l'elenco nella traccia | `test_amministrazione.py` |
| [x] | Settimane dopo C: elencate dopo il ritorno con il comando `settimanale --payload` dal loro `A3_<lunedi'>.json` parcheggiato | `test_amministrazione.py` |
| [x] | Chi puo' farlo: modalita' Admin (D-85, decisione dell'utente del 29/10): pulsante Admin dell'app che apre, dopo una conferma tracciata, la finestra delle operazioni (con Nuovo registro e i moduli con le scelte); `--admin` da riga di comando; governance: "Storia riscritta" in `controlli_e_model_risk.md` | `test_app.py`, `test_amministrazione.py`; prova della finestra |
| [x] | Guida 3-quater, 0.3 (tempi), Admin, Altro, 5, 7; README, 00_LEGGIMI, PROMPT_MASTER (trappole 137-138), TODO, HANDOFF; `AGGIORNAMENTO_IN_BANCA.md` del 29/10 | `verifica_riferimenti.py` |

## 18.6 Verifiche in Banca (TODO B5-bis)

| Stato | Voce |
|---|---|
| [ ] | Estrarre il pacchetto (zip del 23/10, istruzioni in `AGGIORNAMENTO_IN_BANCA.md`); copiare `01_Kernel` e `DECISIONI.md` nella library Kernel; in `configurazione.json` le voci della guida 0.3 (`utente`, `validatore_predefinito`, `raccolta_su_questo_pc`, `agenti`, `ascolta_appunti`, `link_agenti`) |
| [ ] | Reincollare A3, A4, A5, A6 e A8 (D-84); togliere `Baseline_corrente.txt` dalla knowledge di A3 e A4 e dalla library Kernel; cancellare il prompt schedulato di A3; `baseline` per gli allegati con i nomi nuovi |
| [ ] | V-A: il link "Copia collegamento" apre la chat dell'agente |
| [ ] | V-B, V-C: il pulsante Copia porta negli appunti un A1 intero di 40 KB |
| [ ] | V-F: `AutoSaveOn` e `FullName` del registro aperto via COM |
| [ ] | Lucchetto fra due PC con OneDrive: il collega vede "Il registro e' in uso" |
| [ ] | Un trimestre di prova dall'app sul registro di prova: giro di correzione, validazione, report |
| [ ] | App piu' esplicita (29/10): fascia e passo in corso, domande in primo piano, "Ho chiuso Excel: controlla ora", domanda su A5 dopo il precontrollo |
| [ ] | M3: `installa.cmd` fino in fondo (pip o cartella `pacchetti`), finestra della configurazione, collegamenti e Invia a, attivita' della raccolta (V-E), Verifica del PC con Excel (V-F) |
| [ ] | M4: `Report_comitato_<ciclo>.html` dopo `valida` sul registro di prova, schede collegate, "Cancello: N numeri uguali" |
| [ ] | M5 sul registro di prova: pulizia e annullamento, ritorno e annullamento; ripartenza da zero |
| [ ] | Collaudo completo sul PC con Excel (`esegui_collaudo.py`, catena compresa) e presentazione rigenerata |
