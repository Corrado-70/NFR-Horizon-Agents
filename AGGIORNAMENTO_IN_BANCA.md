# Aggiornamento sul PC della Banca — pacchetto del 29/10/2026

Per chi installa il pacchetto in Banca. Il commit esatto e' nel nome dello zip
(`NFR-Horizon-Agents_2026-10-29_<commit>.zip`). I riferimenti fra parentesi sono le sezioni di
`NFR_Emerging_Risk_Agents/00_GUIDA_PASSO_PASSO.md`. Questo pacchetto si mette **sopra quello del 23/10** gia'
installato; se il PC non ha ancora il pacchetto del 23/10, prima i passi dell'appendice in fondo.

## Che cosa porta questo pacchetto

- **Aiuto nell'app** (pulsante Aiuto o F1): un argomento per pulsante, preso dalla guida; passando con il mouse su un
  pulsante compare che cosa fa.
- **App piu' esplicita**: la fascia blu dice processo e fase, il passo in corso il comando in esecuzione con il tempo
  trascorso; domande e moduli vengono in primo piano con un suono; "Ho chiuso Excel: controlla ora". Dopo il
  precontrollo superato l'app chiede se passare anche da **A5** (`chiedi_a5`).
- **Installazione con un doppio clic** (tappa M3): `07_Senza_Studio\installa.cmd` controlla Python e i moduli
  (installa con pip quelli che mancano), apre la **finestra della configurazione**, crea i collegamenti (**NFR Horizon
  Scan** sul Desktop, **Invia a -> NFR notizie manuali**), sul PC della raccolta pianifica la **raccolta del lunedi'**
  e alla fine fa la **Verifica del PC** (anche dall'app: Altro -> Verifica del PC) (0.3).
- **Report al comitato anche in HTML** (tappa M4): `valida` e `report` scrivono accanto al PDF
  `Report_comitato_<ciclo>.html`, da aprire nel browser, con le schede di tutti i rischi; esce solo se i suoi numeri
  tornano con quelli di Excel; l'elenco di tutti i report e' `Cicli\Indice_report.html` (4).
- **Amministrazione** (tappa M5, pulsante **Admin...** della finestra, D-85): pulizia dell'archivio,
  ritorno a un ciclo validato, ripartenza da zero, annullamento; niente si cancella subito, tutto va nel parcheggio
  con l'atto (3-quater).
- **Testi di A1 piu' lunghi e controllo C10** (D-86): la guida di scrittura fissa per ogni testo un minimo e un
  consigliato (descrizione 500-900 caratteri, ogni parte del razionale 300-400, azioni e KRI 300-600...); un testo
  piu' corto e' il rilievo **C10**: per A5 un Bloccante, nel precontrollo l'app chiede se farlo allungare ad A1 nella
  stessa chat (si puo' dire di no), in validazione un'Osservazione. Le risposte di A1 diventano circa il doppio: piu'
  spesso servira' "continua".
- **A7 risponde in prima persona** (D-87), come chi ha proposto le valutazioni e le difende, senza nominare gli
  altri agenti e senza cautele di rito; dopo una rettifica: "avevo proposto..., il validatore ha deciso...".
- **Schede di A6, analisi dell'evento di A8 e pareri di A4 piu' estesi** (D-88): A6 ha lunghezze minime (descrizione
  1000-2000 caratteri, 400-800 per ogni valore) e l'app propone di fargli allungare i testi corti; l'analisi dell'evento
  di A8 entra nelle lunghezze di C10; A4 scrive un parere piu' disteso.
- **Da reincollare: A4, A5, A6 e A7**; nella library Kernel quattro file aggiornati (passo 3-bis). Struttura del registro invariata
  (versione `2026-10-09`): nessun `aggiorna-registro`.

## Passi

**0. Prima di estrarre**: chiudere l'app, Excel e il registro. Copiare per sicurezza la cartella del pacchetto
com'e' adesso (per tornare indietro).

**1. Estrarre lo zip nella cartella del pacchetto**, sostituendo i file. Lo zip non contiene `configurazione.json`,
che resta com'e'.

**Zip arrivato per posta** (nome che finisce con `_posta.zip`): la posta blocca i file `.cmd`, quindi nello zip i
tre lanciatori finiscono con `.txt`: `07_Senza_Studio\NFR.cmd.txt`, `07_Senza_Studio\installa.cmd.txt`,
`07_Senza_Studio\NFR_notizie_manuali.cmd.txt`. Dopo l'estrazione **rinominarli togliendo `.txt`** (Esplora file:
Visualizza -> Mostra -> Estensioni nomi file, poi tasto destro -> Rinomina); se c'e' gia' un `NFR.cmd`, sostituirlo.

**2. Doppio clic su `07_Senza_Studio\installa.cmd`** (0.3, punto 3). Si apre la finestra della configurazione con i
valori di adesso: controllare le cartelle e i link degli agenti e premere **Salva** (la configurazione di prima resta
accanto, `configurazione_<data>.json.precedente`). Alla fine la Verifica del PC: le righe NO vanno sistemate (il
rimedio e' scritto sotto); il file e' in `Archivio_Cicli\Verifiche_PC\`.
- Se pip non riesce (proxy): il messaggio dice la strada (cartella `pacchetti` o l'IT); i moduli che servono ci sono
  gia', dal pacchetto del 23/10, quindi si puo' proseguire.
- Se l'attivita' pianificata o i collegamenti non si possono creare: a mano (sezione 1, "Raccolta notizie
  automatica"; tasto destro su `NFR.cmd` -> Invia a -> Desktop).

**3. Amministrazione**: niente da configurare. Il pulsante **Admin...** apre, dopo una conferma che lascia la traccia,
la finestra delle operazioni, ognuna spiegata e con il suo pulsante (Aiuto -> "Pulsante Admin", D-85).

**3-bis. Kernel, A4, A5, A6 e A7** (D-86, D-87, D-88)
- Copiare nella library **Kernel** (la cartella della voce `kernel` di `configurazione.json`), sostituendoli, i quattro
  file di `NFR_Emerging_Risk_Agents\01_Kernel`: `controlli_A5.md`, `guida_scrittura_A1.md`, `schema_output_A5.json`,
  `schema_output_A6.json`.
  Lo script li mette negli allegati di A1 e di A5: senza la copia A1 non vede le lunghezze.
- Agent Builder: **reincollare le istruzioni di A4, A5, A6 e A7** (`NFR_Emerging_Risk_Agents\02_Agenti\A4_News_Assessor.md`,
  `A5_Challenger.md`, `A6_Schede.md`, `A7_Assistente_registro.md`). A1, A3 e A8 non cambiano.

**4. L'app.** Doppio clic sul collegamento **NFR Horizon Scan** del Desktop (o su `NFR.cmd`).

## Verifiche da fare (TODO B5-bis; esiti da annotare in `Analisi_Architettura/18_App_orchestrazione.md`, 18.6)

Del pacchetto del 23/10 (se non ancora fatte):
- un trimestre di prova dall'app sul **registro di prova** (`04_Riferimenti\Prove\Prova_senza_Copilot_Studio.md`):
  A1 con la risposta incollata nella finestra, il giro di correzione, la validazione, il report;
- il pulsante Copia di Agent Builder porta negli appunti una risposta lunga di A1 intera (V-B, V-C);
- il link "Copia collegamento" apre la chat dell'agente (V-A);
- con un collega: lanciando un comando mentre l'altro scrive, compare "Il registro e' in uso".

Nuove:
- **app**: durante il trimestre la fascia e il passo in corso dicono sempre che cosa succede; la domanda "Passare alla
  validazione adesso?" viene in primo piano; "Ho chiuso Excel: controlla ora" prosegue dopo aver chiuso Excel; dopo il
  precontrollo superato compare la domanda su A5;
- **lunghezze dei testi (C10)**: nel trimestre di prova `Input_A1_<ciclo>.txt` ha nella parte 3 la tabella "Lunghezze
  dei testi"; se A1 risponde corto, l'app dice quanti rischi hanno testi troppo corti e propone il messaggio per
  allungarli; dopo la correzione il precontrollo non li segnala piu'; A5 (reincollato) segnala C10 come Bloccante e in
  validazione compare come osservazione; annotare se le risposte di A1 si tagliano piu' spesso (V-B);
- **A7 in prima persona**: le domande 2, 5 e 9 del copione `04_Riferimenti\Prove\Prova_A7.md`; A7 risponde "ho dato...",
  dopo una rettifica "avevo proposto..., il validatore ha deciso...", senza nominare A1 o A5 e senza cautele di rito;
- **schede di A6 (D-88)**: dopo la validazione di prova, Schede con A6: se A6 scrive corto, l'app lo dice e propone
  l'elenco per la stessa chat; con la risposta nuova le schede si rifanno; annotare quanto sono lunghe le schede;
- **A4 (D-88)**: un parere su una notizia di prova e' piu' disteso nelle sei sezioni;
- **installazione (M3)**: `installa.cmd` arriva in fondo; la Verifica del PC ha `Excel via COM` OK e le righe
  `FullName` e `AutoSaveOn` (V-F: annotare cosa dicono); sul Desktop c'e' il collegamento, in Invia a la voce "NFR
  notizie manuali" (provarla su un file: finisce in `News_Inbox\<lunedi'>\Manuali`); sul PC della raccolta, in
  Utilita' di pianificazione, l'attivita' "NFR raccolta notizie" (V-E);
- **report HTML (M4)**: dopo la validazione del ciclo di prova c'e' `Report_comitato_<ciclo>.html` accanto al PDF; si
  apre con un doppio clic, il clic su un ID apre la scheda del rischio, i numeri sono quelli del PDF; l'uscita di
  `valida` dice "Cancello: N numeri uguali";
- **amministrazione (M5), sul registro di prova** (configurazione della prova): pulsante Admin (conferma, titolo con
  ADMIN, traccia in `Archivio_Cicli\Amministrazione`), poi nella finestra Admin ->
  pulizia (anteprima e poi spostamento), parcheggi, annulla della pulizia; poi un ritorno al ciclo validato prima
  di quello corrente e il suo annullamento (lo stato dell'app torna com'era).
- **collaudo completo sul PC** (chi mantiene il pacchetto): `python NFR_Emerging_Risk_Agents\99_Collaudo\esegui_collaudo.py`
  (catena con Excel compresa: report HTML via COM, cancello, ritorno e annullamento); poi la presentazione con
  `python Presentazione\genera_presentazione.py`.

## Se qualcosa non va

- I messaggi e i rimedi sono nella sezione 7 della guida; ogni comando lanciato dall'app lascia un log in
  `Archivio_Cicli\Log\`.
- Per tornare indietro: rimettere la copia della cartella del pacchetto fatta al passo 0 e la configurazione
  precedente (`configurazione_<data>.json.precedente` rinominato `configurazione.json`). Il registro non cambia
  struttura con questo pacchetto.

---

## Appendice — pacchetto del 23/10/2026 (solo se il PC non lo ha ancora)

Per chi installa il pacchetto in Banca. Il commit esatto e' nel nome dello zip
(`NFR-Horizon-Agents_2026-10-23_<commit>.zip`). I riferimenti fra parentesi sono le sezioni di
`NFR_Emerging_Risk_Agents/00_GUIDA_PASSO_PASSO.md`, che ha il dettaglio di ogni passo.

### Che cosa porta questo pacchetto

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

### Passi

**0. Prima di estrarre** (0-bis, punto 0)
- Se in Banca sono stati modificati `01_Kernel\tassonomia_nfr.md`, `rubrica_scoring.md`, `fonti.md` o
  `04_Riferimenti\DECISIONI.md`, mandare le modifiche a chi mantiene il pacchetto **prima**: lo zip li sovrascrive.
- Chiudere Excel e il registro. Copiare per sicurezza la cartella del pacchetto com'e' adesso (per tornare indietro).

**1. Estrarre lo zip nella cartella del pacchetto**, sostituendo i file. Lo zip non ha una cartella in testa e non
contiene `configurazione.json`, che resta com'e'. Se ci sono ancora le cartelle vecchie `04_SharePoint`,
`05_Workflow`, `06_Governance`, `08_Deploy`, cancellarle.

**Zip arrivato per posta** (nome che finisce con `_posta.zip`): la posta blocca gli allegati con file `.cmd`, quindi il
lanciatore dell'app e' nello zip come `07_Senza_Studio\NFR.cmd.txt`. Dopo l'estrazione **rinominarlo `NFR.cmd`**:
in Esplora file, Visualizza -> Mostra -> Estensioni nomi file (per vedere il `.txt` finale), poi tasto destro ->
Rinomina e togliere `.txt`. Se c'e' gia' un `NFR.cmd` di un pacchetto precedente, sostituirlo.

**2. Library `Kernel`** (la cartella sincronizzata della voce `kernel` di `configurazione.json`)
- copiare **tutti** i file di `NFR_Emerging_Risk_Agents\01_Kernel` e `04_Riferimenti\DECISIONI.md`: lo script legge
  il kernel da li';
- **togliere `Baseline_corrente.txt`**, se c'e': nessun agente la legge piu' dalla library;
- **togliere `Tassonomia dei Rischi.csv`**, se c'e': dal 09/10 sta in `04_Riferimenti` e nessun componente la legge
  dalla library.

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

### Se qualcosa non va

- I messaggi e i rimedi sono nella sezione 7 della guida; ogni comando lanciato dall'app lascia un log in
  `Archivio_Cicli\Log\`.
- Un lucchetto rimasto per errore (PC spento a meta' comando) scade dopo 2 ore; prima, sentito il collega:
  `python esegui_ciclo_locale.py sblocca --motivo "..."`.
- Per tornare indietro: rimettere la copia della cartella del pacchetto fatta al passo 0 e reincollare le istruzioni
  degli agenti di prima. Il registro non cambia struttura con questo pacchetto.
