# Prova K16: A1 con Claude Code sul PC della Banca

Prova dell'analisi 20 (`Analisi_Architettura/20_Agenti_Claude_Vertex.md`, 20.12), preparata il 06/11/2026.

**Che cosa si prova.** Claude Code, lo strumento autorizzato dalla Banca (DB1), fa il lavoro di A1 senza chat e senza
strumenti, come lo farebbe il canale Claude dell'app:
- riceve l'allegato `Input_A1` del ciclo di prova;
- risponde con il JSON di A1;
- il JSON passa dal precontrollo, come oggi la risposta di Agent Builder.

Si misura se **il trasporto** funziona: risposta intera, schema giusto, punti del precontrollo, tempi, costi. Non si
misura ancora la qualita' delle valutazioni. Senza i documenti della knowledge, A1 lavora sulla baseline e, nella prova
C, sulle raccolte delle notizie. La qualita' e' la prova K19.

**Che cosa non tocca.** Il registro, l'archivio (`Archivio_Cicli`), le library e gli agenti di Agent Builder restano
come sono. Tutto si scrive in una cartella di prova, `%USERPROFILE%\NFR_K16`.

**Tempo e costo.**
- Una prova dura da qualche minuto a mezz'ora.
- Ogni chiamata ha un tetto di spesa di 5 dollari (`--budget`). L'ordine atteso e' 1-3 dollari per prova.

**Dati.** `Input_A1` contiene il registro: secondo la risposta del 06/11 tutti i dati sono ammessi su Vertex. Il parere
scritto del DPO e' la decisione A-28. **Fuori dalla Banca si riporta solo la tabella dei risultati** (passo 7), mai i
file della cartella di prova.

## File della prova

Nel clone del progetto, cartella `NFR_Emerging_Risk_Agents\04_Riferimenti\Prove\K16\`:

| File | Che cosa e' |
|---|---|
| `A1_per_Claude.md` | il prompt di A1 per Claude: identico a `02_Agenti\A1_Horizon_Scanner.md` tranne la sezione Input (tutto e' nel messaggio, niente strumenti ne' internet, citare solo cio' che c'e') e la prima riga di Output (niente recinti di codice) |
| `prova_k16.py` | lancia `claude -p` come lo lancerebbe l'app e salva la risposta come JSON per il precontrollo; solo libreria standard |

Nei comandi sotto:
- `<CLONE>` e' la cartella del clone di GitHub;
- `<PACCHETTO>` e' la cartella del pacchetto installato su OneDrive (quella con `07_Senza_Studio\configurazione.json`);
- `<ARCHIVIO>` e' la cartella di uscita dell'archivio, cioe' la chiave `cartella_uscita` di `configurazione.json`.

Tutti i comandi vanno dati nel **prompt dei comandi** (`cmd`), non in PowerShell.

## Passo 1. Aggiornare il clone

```
cd /d <CLONE>
git pull
```

Controllare che esista `NFR_Emerging_Risk_Agents\04_Riferimenti\Prove\K16\prova_k16.py`.

## Passo 2. Verifiche di Claude Code

1. **Dov'e' Claude Code, e quale versione.**
   ```
   where claude
   claude --version
   ```
   - Annotare la versione.
   - Se `where` mostra solo un file `.cmd` e nessun `.exe`, annotarlo: lo script vuole `claude.exe`, da indicare con
     `--claude <percorso>`.
   - Se `where` non trova niente ma Claude Code si usa da **VS Code** (ammesso in Banca, DB9 g, 07/11): l'estensione
     porta con se' una propria copia di Claude Code e non la mette nel PATH (documentazione dell'estensione, 07/11).
     Cercarla nella cartella delle estensioni:
     ```
     dir /s /b "%USERPROFILE%\.vscode\extensions\claude.exe"
     ```
     Annotare il percorso e la versione (`"<percorso>" --version`), poi passarlo allo script con `--claude "<percorso>"`.
     Se non c'e' nemmeno li', annotarlo: per il canale Claude (O4) serve l'installazione autonoma di Claude Code, da
     chiedere all'IT (DB4 a).
2. **Dove sta la configurazione verso Vertex.** Basta vedere se c'e', senza copiare i valori:
   ```
   set | findstr /i "VERTEX CLOUD_ML CLAUDE_CODE"
   findstr /i "VERTEX CLOUD_ML" "%USERPROFILE%\.claude\settings.json"
   ```
   Annotare dove compare, se nelle variabili d'ambiente o nel file `settings.json`, e il valore di `CLOUD_ML_REGION`
   (`eu`, `global` o una regione).
3. **Accesso a Google valido** (DB2):
   ```
   gcloud auth application-default print-access-token >nul && echo ACCESSO OK
   ```
   Se non scrive `ACCESSO OK`, dare `gcloud auth application-default login` (si apre il browser) e ripetere.
4. **Modello e fornitore.** Aprire Claude Code interattivo (`claude`), scrivere `/status` e annotare:
   - `API provider`, che deve essere Google Vertex AI;
   - `Default region`;
   - `Model`.

   Uscire con `/exit`. Se il modello non e' `claude-opus-5-5`, nei passi 4 e 6 aggiungere `--modello <quello mostrato>`.
5. **Chiamata minima senza strumenti**, come la fara' lo script:
   ```
   echo Rispondi solo con la parola OK| claude --bare -p --tools "" --no-session-persistence --settings "%USERPROFILE%\.claude\settings.json" --model claude-opus-5-5 --output-format json --max-budget-usd 0.10
   ```
   Atteso: un JSON con `"result":"OK"` e, in `modelUsage`, il nome del modello.
   - Se chiede di fare il login, o di una chiave API, con `--bare` Claude Code non trova la configurazione verso Vertex.
     Ripetere il comando senza `--bare`; se cosi' funziona, nei passi 4 e 6 aggiungere `--senza-bare`.
   - Se il file `settings.json` non esiste, togliere `--settings ...` dal comando.
   - Gli altri errori sono in fondo, "Se qualcosa va storto".

## Passo 3. La cartella di prova

```
mkdir "%USERPROFILE%\NFR_K16"
copy "<ARCHIVIO>\Input_A1_*.txt" "%USERPROFILE%\NFR_K16\"
copy "<ARCHIVIO>\Baseline_corrente.json" "%USERPROFILE%\NFR_K16\"
cd /d "%USERPROFILE%\NFR_K16"
dir
```

- Ci deve essere **un solo** `Input_A1_<ciclo>.txt`, quello del ciclo da valutare (lo stesso ciclo di
  `ciclo_da_valutare` nella baseline). Se ce ne sono piu' d'uno, tenere solo quello giusto.
- Nei comandi sotto il ciclo e' `2026Q4`: sostituirlo se e' un altro.
- La cartella e' sul disco locale, non su OneDrive, di proposito.

## Passo 4. Le prove di A1

Sempre da `%USERPROFILE%\NFR_K16`.

**Prova A, senza schema.** Claude scrive il JSON nel testo, e lo script lo estrae:
```
py -3 "<CLONE>\NFR_Emerging_Risk_Agents\04_Riferimenti\Prove\K16\prova_k16.py" --input Input_A1_2026Q4.txt --run A
```

**Prova B, con lo schema di decodifica.** E' lo schema del kernel senza i vincoli di lunghezza, che restano al
precontrollo:
```
py -3 "<CLONE>\NFR_Emerging_Risk_Agents\04_Riferimenti\Prove\K16\prova_k16.py" --input Input_A1_2026Q4.txt --run B --con-schema
```

**Prova C, facoltativa: con le raccolte delle notizie del trimestre in coda.** Indicare la cartella `News_Inbox`, cioe'
la chiave `news_inbox` di `configurazione.json`:
```
py -3 "<CLONE>\NFR_Emerging_Risk_Agents\04_Riferimenti\Prove\K16\prova_k16.py" --input Input_A1_2026Q4.txt --run C --aggiungi "<NEWS_INBOX>\2026-1*\Raccolta_*.txt"
```
Lo script scrive quanti documenti ha aggiunto. L'asterisco `2026-1*` prende le settimane di ottobre, novembre e
dicembre: va adattato al trimestre.

**Che cosa si vede.** Lo script dice "puo' durare decine di minuti", poi stampa un riepilogo:
- esito;
- durata;
- costo stimato;
- token in ingresso e in uscita;
- modelli usati;
- numero di rischi e caratteri;
- nome del file salvato, `A1_2026Q4_claude_<prova>.json`.

Nella cartella restano anche la richiesta inviata, lo schema e la risposta completa di Claude Code
(`K16_<prova>_<ora>_*`).

Codici di uscita: 0 risposta salvata; 1 risposta arrivata ma non usabile (il riepilogo dice perche'); 2 errore tecnico.

## Passo 5. Il precontrollo

Per ogni file `A1_2026Q4_claude_<prova>.json`:
```
cd /d "<PACCHETTO>\07_Senza_Studio"
py -3 esegui_ciclo_locale.py --cartella-uscita "%USERPROFILE%\NFR_K16" precontrollo --payload "%USERPROFILE%\NFR_K16\A1_2026Q4_claude_A.json" --baseline "%USERPROFILE%\NFR_K16\Baseline_corrente.json"
```

- La prima riga dice l'esito: "nessun rilievo", oppure i punti **da correggere**, **da verificare** e i **testi corti
  (C10)**. Annotarli.
- Con `--cartella-uscita` il messaggio di correzione e l'allegato di A5 si scrivono solo in `NFR_K16`. Il registro non
  si apre.

**Confronto con Agent Builder.**
- Se per lo **stesso** `Input_A1` c'e' gia' una risposta di Agent Builder (in `<ARCHIVIO>\In_arrivo\A1_2026Q4.json`),
  copiarla in `NFR_K16` con un altro nome, per esempio `A1_2026Q4_AB.json`, e lanciare lo stesso precontrollo.
- Se `Input_A1` e' cambiato da allora, si puo' chiedere ad A1 in Agent Builder una risposta nuova sullo stesso file e
  salvarla.

## Passo 6, facoltativo. Un giro di correzione senza memoria di chat

Se il precontrollo della prova A ha punti da correggere, si prova la correzione come la farebbe il canale Claude
(20.5.5): una richiesta nuova, con l'output precedente e il messaggio di correzione come documenti.
```
cd /d "%USERPROFILE%\NFR_K16"
py -3 "<CLONE>\NFR_Emerging_Risk_Agents\04_Riferimenti\Prove\K16\prova_k16.py" --input Input_A1_2026Q4.txt --run D --aggiungi A1_2026Q4_claude_A.json Cicli\2026Q4\Correzione_A1_2026Q4.txt --richiesta "Correggi il tuo output precedente (documento A1_2026Q4_claude_A.json) secondo il messaggio di correzione (documento Correzione_A1_2026Q4.txt): cambia solo i punti indicati e restituisci l'intero JSON."
```
Poi il precontrollo del passo 5 su `A1_2026Q4_claude_D.json`.

## Passo 7. Risultati da annotare

Questa tabella, con i soli numeri, si puo' riportare fuori dalla Banca.

| Voce | Valore |
|---|---|
| Data, PC | |
| Versione di Claude Code (passo 2.1) | |
| Configurazione verso Vertex: variabili d'ambiente o `settings.json`; `CLOUD_ML_REGION` | |
| `/status`: fornitore, regione, modello | |
| Chiamata minima: riuscita con `--bare`? Senza? | |
| Antivirus o blocchi quando Python lancia Claude Code? | |

| Prova | Esito script | Durata (min) | Costo (USD) | Token in / out | Rischi | Caratteri | Precontrollo: da correggere / da verificare / testi corti |
|---|---|---|---|---|---|---|---|
| A senza schema | | | | | | | |
| B con schema | | | | | | | |
| C con raccolte (facoltativa) | | | | | | | |
| D correzione (facoltativa) | | | | | | | |
| Agent Builder, stesso Input_A1 | — | — | — | — | | | |

**K16 e' superata se:**
- fornitore Vertex, e regione quella attesa;
- in almeno una tra A e B: risposta intera, senza tagli;
- JSON valido per lo schema;
- punti del precontrollo non piu' di Agent Builder sullo stesso ingresso;
- C10 rispettato;
- meno di 30 minuti.

Se la prova B fallisce con `error_max_structured_output_retries`, la via e' la prova A (20.5.2, R21).

## Se qualcosa va storto

| Che cosa si vede | Perche' | Che cosa fare |
|---|---|---|
| Chiede il login o una chiave API | con `--bare` non arriva la configurazione verso Vertex | `--senza-bare` nello script, e annotarlo (R19) |
| "Could not load the default credentials", oppure un errore 401 o 403 | accesso Google scaduto | `gcloud auth application-default login`, poi ripetere |
| "model not found" (404) | modello non abilitato nel progetto o nella regione | il modello di `/status`, con `--modello` (DB5) |
| Errore 429 | quota del progetto | aspettare qualche minuto; annotare (DB5, K17) |
| Errori di rete o di proxy, ma Claude Code interattivo funziona | il prompt dei comandi non ha le stesse variabili | lanciare dallo stesso prompt dove `claude` funziona; confrontare `set` |
| `error_max_budget_usd` | tetto di spesa raggiunto | `--budget 10` |
| `error_max_structured_output_retries` (prova B) | lo schema e' stato rifiutato piu' volte | annotare; vale la prova A (R21) |
| "Risposta non utilizzabile": testo senza JSON o tagliato | risposta tagliata o rifiutata | guardare `K16_<prova>_*_uscita_claude.json` (campo `result`, eventuale `stop_reason`); annotare (R20) |
| "Claude Code non si avvia" | antivirus o AppLocker | annotare: e' DB4, parte c |
| "'claude' non trovato" | non e' nel PATH | `--claude "<percorso di claude.exe>"` |

A prova finita, la cartella `%USERPROFILE%\NFR_K16` si puo' tenere per il confronto o cancellare. Contiene dati del
registro: vale la stessa cura degli altri file del progetto.
