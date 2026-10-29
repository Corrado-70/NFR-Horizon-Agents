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

## 18.3 Tappa M3: installazione e Verifica del PC (da fare, circa 1,5 giorni)

| Stato | Voce |
|---|---|
| [ ] | `installa.cmd` + `installa.py`: Python 3.10+, tkinter, pywin32, openpyxl, pypac; `pip install --user` di cio' che manca, con un messaggio chiaro se il proxy blocca |
| [ ] | `configurazione.json` con dialoghi: cartelle sincronizzate, link dei 7 agenti, utente, validatore, PC della raccolta |
| [ ] | Collegamento sul Desktop "NFR Horizon Scan"; "Invia a -> NFR notizie manuali" |
| [ ] | Attivita' pianificata della raccolta (`schtasks /create /xml`) solo sul PC della raccolta; `attrib +P` |
| [ ] | Verifica del PC dall'app, riga per riga: moduli, Excel via COM, `AutoSaveOn` e `FullName`, cartelle scrivibili, lucchetto, link; file da mandare al manutentore |
| [ ] | Guida, sezione 0 riscritta attorno a `installa.cmd`; collaudo dell'installatore su una cartella di prova |

## 18.4 Tappa M4: report HTML al comitato (da fare, 3-4 giorni)

| Stato | Voce |
|---|---|
| [ ] | `report_html.py` dal prototipo `16_genera_anteprima_html.py`: viste da Quadro a Metodologia, grafici SVG, schede di tutti i rischi collegate |
| [ ] | Dati letti dalla stessa sessione COM di `report` (righe dello `Scrittore`, celle con nome), non da openpyxl |
| [ ] | Cancello: numeri dell'HTML confrontati con le celle delle viste di Excel; se uno non torna l'HTML non esce, il PDF si' |
| [ ] | File unico autosufficiente; ciclo, data della validazione e validatore in testa; versione precedente conservata; `Cicli/Indice_report.html` |
| [ ] | `--con-lavoro`: Registro, Storico, Indicatori, Notizie, Piano azioni, Parametri |
| [ ] | `valida` pubblica PDF e HTML insieme; lo stato dell'app guarda anche l'HTML |
| [ ] | Catena: numeri uguali a Excel e cancello che scatta con un numero alterato; guida, presentazione, PROMPT_MASTER |

## 18.5 Tappa M5: funzioni amministrative (da fare; richiesta dell'utente del 23/10/2026)

Pulizia dell'archivio e "ritorno indietro nel tempo" di N trimestri. Regola di fondo: **niente si cancella subito**.
Tutto cio' che si toglie va in un **parcheggio** (`Archivio_Cicli/_Parcheggio/<data_ora>_<operazione>/`) con un atto
che dice chi, quando, perche' e che cosa. Si svuota solo con un comando a parte e dopo un tempo minimo. Ogni operazione:
- prende il lucchetto;
- chiede conferma scrivendo il nome del ciclo;
- lascia la traccia in `Archivio_Cicli/Amministrazione/`;
- si annulla rimettendo a posto il parcheggio.

In una voce "Amministrazione" dell'app, protetta da una conferma; anche da riga di comando.

| Stato | Voce |
|---|---|
| [ ] | **Pulizia dell'archivio**: i tentativi fermati (`Cicli/<c>/tentativo_<ora>/`) dei cicli validati; i `Backup` oltre gli ultimi N (o piu' vecchi di N giorni); le versioni precedenti dei report; `In_arrivo` (Originali, Precedenti) dei periodi chiusi; i `Log` vecchi. Anteprima di cio' che si sposta e dello spazio liberato, poi tutto nel parcheggio |
| [ ] | **Ritorno indietro di N trimestri** (al ciclo validato C): il registro torna quello di fine validazione di C (`Cicli/C/NFR_Registro_C_validato.xlsx`, che dopo una riapertura e' l'ultima validazione). Nel parcheggio vanno il registro attuale, le cartelle dei periodi dopo C (cicli, straordinari, settimane), `Baseline_corrente`, gli allegati e la knowledge di A7. Poi si rigenerano baseline, allegati, knowledge di A7 e griglia. Lo stato dell'app riparte da "Ciclo C: VALIDATO" |
| [ ] | Controlli del ritorno: C deve avere l'Excel validato nell'archivio e la stessa versione del template (altrimenti prima `aggiorna-registro` sulla copia); motivo (almeno 20 caratteri) e decisore obbligatori; avviso sulle settimane dopo C, le cui notizie escono dal registro ma restano nel parcheggio |
| [ ] | **Annulla il ritorno**: rimette il registro e le cartelle dal parcheggio, se nel frattempo non si e' scritto niente (impronta del registro uguale a quella del ritorno) |
| [ ] | **Ripartenza da zero** (per esempio dopo i cicli di prova): registro nuovo con `inizializza`; il vecchio registro e tutto l'archivio dei cicli vanno nel parcheggio |
| [ ] | **Svuota il parcheggio**: solo i parcheggi piu' vecchi di N giorni (in configurazione), con conferma; l'elenco di cio' che si cancella resta nella traccia |
| [ ] | Settimane dopo C dal parcheggio: proposta di riscriverle con `settimanale` dai loro `A3_<lunedi'>.json` parcheggiati (le notizie tornano nel registro) |
| [ ] | Chi puo' farlo: decisione della funzione di rischio (DECISIONI), per esempio solo il manutentore o con un `ruolo` in `configurazione.json`; governance (controlli_e_model_risk: rischio "storia riscritta" e presidio) |
| [ ] | Collaudo (catena: ritorno di un trimestre e annullamento, pulizia con anteprima, parcheggio intatto; senza Excel: selezione di cio' che si sposta); guida, PROMPT_MASTER, HANDOFF, presentazione |

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
