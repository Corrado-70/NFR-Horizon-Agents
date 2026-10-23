# Aggiornamento sul PC della Banca — pacchetto del 23/10/2026

Per chi installa il pacchetto in Banca. Il commit esatto e' nel nome dello zip
(`NFR-Horizon-Agents_2026-10-23_<commit>.zip`). I riferimenti fra parentesi sono le sezioni di
`NFR_Emerging_Risk_Agents/00_GUIDA_PASSO_PASSO.md`, che ha il dettaglio di ogni passo.

## Che cosa porta questo pacchetto

- **App NFR** (D-83): un doppio clic su `07_Senza_Studio\NFR.cmd` apre una finestra che dice a che punto e' il lavoro,
  propone il prossimo passo e guida ogni processo. Le risposte degli agenti si incollano nella finestra (sezione
  "L'app NFR: uso passo per passo"). I comandi scritti a mano restano validi.
- **Piu' analisti sullo stesso registro** (D-83): ogni comando che scrive prende un lucchetto e lavora su una copia
  del registro; il registro vero si sostituisce solo se nessuno l'ha cambiato nel frattempo.
- **Allegati degli agenti con un nome solo, `Input_<agente>`** (D-84): `Input_A1_<ciclo>.txt`,
  `Input_A8_<periodo>.txt` per lo straordinario, `Input_A3_A4.txt` per A3 e A4, `Input_A5_<ciclo>.txt` scritto dal
  precontrollo, `Input_A6_<ciclo>.json`. A3 e A4 non leggono piu' la baseline dalla knowledge (AU7).
- `valida` rigenera da solo il report al comitato; `trimestrale` archivia i prompt; `schede` fa anche il PDF.
- **Struttura del registro invariata** (versione `2026-10-09`): nessun `aggiorna-registro`, se il registro e' gia'
  su questa versione.

## Passi

**0. Prima di estrarre** (0-bis, punto 0)
- Se in Banca sono stati modificati `01_Kernel\tassonomia_nfr.md`, `rubrica_scoring.md`, `fonti.md` o
  `04_Riferimenti\DECISIONI.md`, mandare le modifiche a chi mantiene il pacchetto **prima**: lo zip li sovrascrive.
- Chiudere Excel e il registro. Copiare per sicurezza la cartella del pacchetto com'e' adesso (per tornare indietro).

**1. Estrarre lo zip nella cartella del pacchetto**, sostituendo i file. Lo zip non ha una cartella in testa e non
contiene `configurazione.json`, che resta com'e'. Se ci sono ancora le cartelle vecchie `04_SharePoint`,
`05_Workflow`, `06_Governance`, `08_Deploy`, cancellarle.

**2. Library `Kernel`** (la cartella sincronizzata della voce `kernel` di `configurazione.json`)
- copiare **tutti** i file di `NFR_Emerging_Risk_Agents\01_Kernel` e `04_Riferimenti\DECISIONI.md`: lo script legge
  il kernel da li';
- **togliere `Baseline_corrente.txt`**, se c'e': nessun agente la legge piu' dalla library.

**3. `configurazione.json`** (cartella `07_Senza_Studio`; tabella completa nella sezione 0.3). Aprirlo con Blocco note,
lasciare i percorsi come sono e aggiungere le voci nuove, come in `configurazione_esempio.json`:

| Voce | Che cosa scrivere |
|---|---|
| `utente` | il proprio nome e la funzione: lo vedono i colleghi quando stai scrivendo nel registro |
| `attesa_lucchetto` | `0` |
| `validatore_predefinito` | chi valida di solito, per esempio `"Funzione Risk Management"` |
| `raccolta_su_questo_pc` | `true` solo sul PC che raccoglie le notizie il lunedi', `false` sugli altri |
| `agenti` | `"Agent Builder"` |
| `ascolta_appunti` | `true` (basta premere Copia sotto la risposta) o `false` (si incolla sempre nella finestra) |
| `link_agenti` | i link degli agenti: in Agent Builder, menu "..." dell'agente -> **Copia collegamento**, uno per agente (`"A1": "https://..."`, ...). Senza link l'app funziona lo stesso: l'agente si apre a mano |

**4. Agent Builder** (0.2, 0.2-bis)
- **Reincollare le istruzioni di A3, A4, A5, A6 e A8** (i file `.md` di `NFR_Emerging_Risk_Agents\02_Agenti`, gia'
  pronti; non serve `componi_prompt.py`). Se l'installazione in Banca e' precedente al pacchetto dell'08/10 sera,
  **reincollare tutti gli agenti** (A1, A3, A4, A5, A6, A7, A8) e creare quelli che mancano (0.2).
- A3 e A4: togliere `Kernel/Baseline_corrente.txt` dalla knowledge.
- A3: **cancellare il prompt schedulato** del lunedi', se c'e': non porta l'allegato e A3 risponderebbe "Baseline
  mancante".

**5. Primo comando** (Prompt dei comandi, cartella `07_Senza_Studio`, registro chiuso):

```
python esegui_ciclo_locale.py baseline
```

Si deve vedere `Baseline scritta: ...`, `Allegato per A1: ...Input_A1_<ciclo>.txt` e `Allegato per A3 e A4 (AU7):
...Input_A3_A4.txt`; i vecchi `Input_A3.txt` e `Input_A4.txt` spariscono da soli. Se invece il comando si ferma con
"versione ..." o "template precedente", il registro e' di una struttura vecchia: prima `aggiorna-registro`,
seguendo la sezione 0-bis (su una copia, poi sul registro in uso).

**6. L'app.** Doppio clic su `07_Senza_Studio\NFR.cmd` (conviene un collegamento sul Desktop: tasto destro ->
Mostra altre opzioni -> Invia a -> Desktop). In alto lo stato, poi il pulsante del prossimo passo. Se la finestra
non si apre, `python app_nfr.py` dalla cartella degli script mostra l'errore.

**7. Prove** (TODO B5-bis; risultati da annotare in `Analisi_Architettura/18_App_orchestrazione.md`, 18.6)
- un trimestre di prova dall'app sul **registro di prova** (`04_Riferimenti\Prove\Prova_senza_Copilot_Studio.md`):
  A1 con la risposta incollata nella finestra, il giro di correzione, la validazione, il report;
- il pulsante Copia di Agent Builder porta negli appunti una risposta lunga di A1 intera;
- il link "Copia collegamento" apre la chat dell'agente;
- con un collega: lanciando un comando mentre l'altro scrive, compare "Il registro e' in uso".

## Se qualcosa non va

- I messaggi e i rimedi sono nella sezione 7 della guida; ogni comando lanciato dall'app lascia un log in
  `Archivio_Cicli\Log\`.
- Un lucchetto rimasto per errore (PC spento a meta' comando) scade dopo 2 ore; prima, sentito il collega:
  `python esegui_ciclo_locale.py sblocca --motivo "..."`.
- Per tornare indietro: rimettere la copia della cartella del pacchetto fatta al passo 0 e reincollare le istruzioni
  degli agenti di prima. Il registro non cambia struttura con questo pacchetto.
