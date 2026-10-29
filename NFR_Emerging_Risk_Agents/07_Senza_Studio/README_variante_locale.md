# Variante senza Copilot Studio — Agent Builder + script locale

Per un ambiente con licenza **Microsoft 365 Copilot** ma senza Copilot Studio
e senza Power Automate. Il principio del sistema non cambia; cambia dove vive
ciascuna meta':

| Meta' | Nel modulo principale | In questa variante |
|---|---|---|
| Giudizio (A1, A3, A4, A5, A6) | agenti Copilot Studio | agenti **Agent Builder** con le stesse istruzioni |
| Calcolo e scrittura (A2, controlli di A5) | Power Automate + desktop flow | **lo stesso script**, lanciato a mano da un analista |
| Orchestrazione | flow W0-W2 | prompt schedulati di Agent Builder (A3) e una procedura scritta |
| Raccolta notizie (W0) | flow | `raccogli_notizie.py`, pianificato con l'Utilita' di pianificazione di Windows |

Kernel, prompt, schemi e workbook sono identici al modulo principale.

## Cosa offre Agent Builder (verificato su Microsoft Learn, settembre 2026)

- Incluso nella licenza Microsoft 365 Copilot; nessun ruolo maker; un
  amministratore puo' disattivarlo per il tenant.
- Istruzioni fino a **8.000 caratteri** — per questo i prompt sono composti da
  `02_Agenti/componi_prompt.py`, che controlla il limite.
- Knowledge: fino a **4 siti web pubblici** (URL di al massimo due livelli,
  senza parametri; in alternativa l'interruttore "Search all websites"), fino
  a 100 file, cartelle o siti SharePoint, 1 lista SharePoint, 20 file caricati,
  connettori Copilot (la pagina "Build agents", agg. 19/08/2026, dice invece
  "fino a 20 knowledge source": la configurazione qui sotto ne usa al massimo
  7, quindi non cambia nulla). Tipi di file letti: .docx, .pdf, .pptx, .xlsx, .txt,
  .html (solo da SharePoint) — **non .json ne' .md**: per questo lo script
  scrive la baseline anche in `.txt` e la raccolta notizie in `.txt`.
  (Microsoft Learn, "Add knowledge sources to your declarative agent", agg.
  29/07/2026.)
- Capability: solo *code interpreter* ("Create documents, charts, and code") e
  *image generator* ("Create images"). **Il code interpreter e' ACCESO di
  default** (Microsoft Learn, "Code interpreter", agg. 29/07/2026): va spento a
  mano, vedi il setup qui sotto. I suoi file sono solo download temporanei della
  sessione, non salvati in SharePoint. **Nessuna azione, nessun flow, nessuna
  scrittura** in Excel o SharePoint: la scrittura resta allo script.
- Gli allegati caricati in chat vengono copiati nella cartella OneDrive
  "Microsoft Copilot Chat Files" di chi li carica (baseline, output di A1):
  copie persistenti da tenere presenti (`04_Riferimenti/controlli_e_model_risk.md`).
- Prompt schedulati (orari, giornalieri, settimanali, mensili), disponibili da
  maggio 2026: per singolo utente, girano solo per chi li ha creati e solo su
  agenti pubblicati.
- Gli agenti creati con Agent Builder non si usano nelle chat di Teams (si usano
  dall'app Microsoft 365 Copilot, anche dentro Teams).

Fonti: Microsoft Learn, "Agent Builder in Microsoft 365 Copilot" e "Build
agents with Agent Builder" (agg. agosto 2026); annuncio "Schedule prompts in
Agent Builder" (rollout maggio 2026). **Questa capacita' evolve in fretta:
ricontrollare prima del setup.**

## Setup degli agenti (una volta)

Percorso passo passo da seguire nell'ordine: `00_GUIDA_PASSO_PASSO.md`,
sezione 0.2. Questa tabella e le note sotto sono il riferimento tecnico e il
"perche'" (limiti verificati di Agent Builder); se le due divergono, la guida
e' quella da correggere per prima (e' quella in mano a chi installa).

Per ciascun agente: Microsoft 365 Copilot -> Nuovo agente -> "Passa a
Configura" (configurazione manuale, NON la descrizione in linguaggio naturale,
che riscriverebbe le istruzioni).

| Agente | Istruzioni (incollare il file intero) | Knowledge | Capability | Modalita' |
|---|---|---|---|---|
| A1 Horizon Scanner | `02_Agenti/A1_Horizon_Scanner.md` | `Analisi_Interne`, `Analisi_Esterne`, `News_Inbox`, i siti `sito_agente: si` di `fonti.md` | nessuna: **spegnere** "Create documents, charts, and code" e "Create images" | Think deeper |
| A3 Interim Update | `02_Agenti/A3_Interim_Update.md` | `News_Inbox`, `Analisi_Interne`, `Analisi_Esterne`, i siti `sito_agente: si` di `fonti.md` (la baseline arriva come allegato `Input_A3_A4.txt`, AU7) | nessuna (spegnere entrambi) | Auto |
| A4 News Assessor | `02_Agenti/A4_News_Assessor.md` | nessuna (la baseline arriva come allegato `Input_A3_A4.txt`, AU7) | nessuna (spegnere entrambi) | Auto |
| A5 Challenger (facoltativo) | `02_Agenti/A5_Challenger.md` | **nessuna** (riceve solo gli allegati) | nessuna (spegnere entrambi) | Think deeper |
| A6 Schede dei rischi | `02_Agenti/A6_Schede.md` | **nessuna** (riceve solo `Input_A6_<ciclo>.json`) | nessuna (spegnere entrambi) | Think deeper |
| A7 Assistente del registro | `02_Agenti/A7_Assistente_registro.md` | `Kernel/Spiegazioni` (scritta da `trimestrale`, `valida`, `dismetti`), `Analisi_Interne`, `Analisi_Esterne`, `News_Inbox` | nessuna (spegnere entrambi) | Think deeper |

**Capability**: il code interpreter e' acceso di default. Con la configurazione
"nessuna" va spento esplicitamente su ogni agente (Configura -> Capabilities).
Controllarlo anche sugli agenti gia' creati. Nel tenant della Banca le
capability non sono abilitate (01/10/2026): la configurazione "nessuna" e'
garantita dal tenant stesso.

Il kernel e' gia' dentro le istruzioni: non aggiungerlo come knowledge, ne'
lasciarlo solo li' (cio' che e' recuperabile e' ignorabile). Lo stesso vale
per l'elenco delle fonti: codici e nomi sono nelle istruzioni di A3
(`{{FONTI}}`); come knowledge web vanno solo i quattro siti marcati
`sito_agente: si`. Lasciare **spento** "Search all websites": l'agente
citerebbe fonti fuori elenco (che la scrittura poi rifiuta).

A3: niente prompt schedulato (dal 23/10/2026, AU7: la baseline arriva solo come
allegato `Input_A3_A4.txt`, che un prompt schedulato non porta); si lancia dall'app o a
mano. Per ogni agente copiare il link ("..." -> Copia collegamento) in
`configurazione.json`, `link_agenti`: l'app apre l'agente giusto. A4: condividere l'agente solo con il
gruppo della funzione di rischio. A6: condividerlo con chi prepara il report
al comitato; nessuna knowledge, perche' la scheda non deve introdurre fatti che
il ciclo non ha valutato.

## Setup dello script (una volta, sul PC dell'analista)

1. Python 3.10 o successivo (installazione per utente) e
   `pip install pywin32 pypac openpyxl`. Validatore e controlli usano solo la
   libreria standard; le dipendenze esterne servono per Excel (`pywin32`), per
   il file delle schede (`openpyxl`) e per
   la raccolta notizie (`pypac`, punto 5: legge il file di autoconfigurazione
   del proxy come fa il browser, invece del solo indirizzo statico che vede
   `urllib` da solo).
2. Sincronizzare con OneDrive le library `Kernel`, `Report_Trimestrali`,
   `Archivio_Cicli`, `News_Inbox` del sito.
3. Copiare `configurazione_esempio.json` in `configurazione.json` accanto allo
   script e compilarlo con i percorsi locali sincronizzati e con `utente` (il
   nome che i colleghi vedono nel lucchetto del registro, D-83).
4. Registro vivo (una volta sola, da chi fa il deploy):
   `python esegui_ciclo_locale.py inizializza --ciclo-precedente <AAAAQn> --settimana <lunedi'>`
   crea `NFR_Registro.xlsx` nel percorso di `configurazione.json` copiando il
   template SENZA i dati di esempio; `--ciclo-precedente` e' il trimestre prima
   del primo da valutare. Non sovrascrive mai un file esistente.
   Prova: `python esegui_ciclo_locale.py baseline` deve scrivere
   `Baseline_corrente.json` e `.txt` nella cartella di uscita, con
   `ciclo_da_valutare` = il primo trimestre da valutare e nessun rischio.
   Il registro parte vuoto, senza un trimestre gia' valutato a mano: nel primo
   ciclo A1 individua i rischi da zero dalla documentazione (tutti "Nuovo") e
   il validatore li valida nel foglio Validazione.
   **Registro gia' creato con un template precedente** (versione diversa da
   `VERSIONE_TEMPLATE`, ad esempio quello del 24/09 nato dal template del
   23/09): ogni comando si ferma finche' non si lancia
   `python esegui_ciclo_locale.py aggiorna-registro`, che lo porta sul template
   nuovo senza perdere dati (verifica righe, errori e baseline prima di
   sostituirlo; il vecchio resta in `Backup`). Anche `mappatura_campi.json`
   nella library `Kernel` deve essere della stessa versione: lo script lo
   controlla.
5. Prova della raccolta: `python raccogli_notizie.py --anche-da-validare`
   deve scrivere `News_Inbox/<lunedi'>/Raccolta_<oggi>.txt`. Se **tutte** le
   fonti risultano irraggiungibili, e' il proxy o il firewall aziendale (o
   pypac non trova il PAC di sistema: verificare che il sito si apra nel
   browser sullo stesso PC). Se irraggiungibili sono **solo alcune fonti**
   (tipicamente un gruppo con lo stesso dominio) mentre le altre funzionano,
   e i siti si aprono comunque nel browser, e' il caso che `pypac` risolve: il
   PAC del browser le instrada sul proxy, `urllib` da solo le tenta dirette e
   va in timeout.
6. Pianificare la raccolta: Utilita' di pianificazione di Windows, ogni
   lunedi' alle 7 (o ogni giorno), azione `python raccogli_notizie.py`.

File della cartella: `esegui_ciclo_locale.py` (comandi), `raccogli_notizie.py`
(W0), `fonti.py` (lettore dell'elenco fonti), `excel_com.py` (accesso a
Excel), `controlli_a5.py` (controlli meccanizzati), `valida_output.py`
(validatore generico), `schede.py` (input di A6, controlli sul suo output,
file delle schede), `input_a1.py` (allegato di A1 e lettore dei controlli di
A5, anche per `componi_prompt.py`), `precontrollo.py` (regole del precontrollo
dell'output di A1, senza Excel: dal 05/10/2026 le usa anche la skill della
prova di Copilot Studio, D-70). Lo script legge schemi, mappa ed elenco fonti dalla
library `Kernel`: le regole non sono copiate qui.

## Procedura trimestrale

1. `python esegui_ciclo_locale.py baseline`. Accanto alla baseline lo script
   scrive l'allegato `Input_A3_A4.txt` per A3 e A4 (AU7, D-83:
   non si copia piu' niente nella library `Kernel`) e `Input_A1_<ciclo>.txt` (D-69):
   baseline, controlli di A5 (`01_Kernel/controlli_A5.md`, lo stesso testo
   delle istruzioni di A5) e guida di scrittura (`01_Kernel/guida_scrittura_A1.md`).
   Lo riscrive ogni volta che aggiorna la baseline (`trimestrale`, `valida`,
   `dismetti`, `baseline`) e toglie quello del ciclo prima.
2. In A1: allegare `Input_A1_<ciclo>.txt`, scrivere "Esegui il ciclo". Salvare
   la risposta (solo il JSON) come `Archivio_Cicli/A1_<ciclo>.json`.
2-bis. Facoltativo: `python esegui_ciclo_locale.py precontrollo --payload A1_<ciclo>.json`
   (D-69, D-71): senza Excel e senza aprire il registro, verifica schema, controlli
   meccanizzati di `controlli_a5.py` e parti del razionale (D-68) rispetto a
   `Baseline_corrente.json` della cartella di uscita (o `--baseline <file>`).
   Se trova qualcosa scrive `Cicli/<ciclo>/Correzione_A1_<ciclo>.txt`, il
   messaggio da incollare nella chat di A1. Codice 1 se ci sono punti che
   fermerebbero il ciclo, 0 altrimenti (anche con soli punti da verificare).
   Stampa anche l'impronta dell'output controllato (D-70), la stessa che
   stampa la skill di Copilot Studio sullo stesso output.
3. Facoltativo (D-71), in A5: allegare `Input_A5_<ciclo>.txt` (output di A1 e baseline, scritto dal precontrollo),
   scrivere "Esegui i nove controlli". Salvare la risposta come `A5_<ciclo>.json`.
4. `python esegui_ciclo_locale.py trimestrale --payload A1_<ciclo>.json [--challenger A5_<ciclo>.json]`
   - codice 1: fermato, workbook intatto. Ferma solo un difetto di integrita'
     (schema, C1, C2, C7, identificativi dei KRI): dare ad A1 il messaggio
     `Cicli/<ciclo>/Correzione_A1_<ciclo>.txt` e ripetere (il rapporto resta in
     `Cicli/<ciclo>/tentativo_<ora>/`). Se si usa A5, dopo ogni nuovo run di A1
     serve un nuovo run di A5 sullo STESSO output: lo script rifiuta un esito
     di A5 di un altro ciclo o che cita rischi assenti dall'output di A1.
     C3, le date di C5, la coppia e le soglie dei KRI e i Bloccanti di A5 non
     fermano: sono "da motivare" (colonna Segnalazioni del foglio Validazione,
     ⚑, Motivazione obbligatoria). `--procedi-con-rilievi` (D-56) non serve piu'.
   - codice 2 "DOPO IL SALVATAGGIO": il registro e' gia' scritto e la baseline
     aggiornata; manca un pezzo dell'archivio (di solito perche' un Excel
     dell'archivio e' aperto). Non rilanciare: chiudere il file e copiare il
     registro in `Cicli/<ciclo>/NFR_Registro_<ciclo>.xlsx`.
   - codice 0: scritto. In `Cicli/<ciclo>/` c'e' l'**Excel di output**
     `NFR_Registro_<ciclo>.xlsx` con la nuova analisi, insieme agli output degli
     agenti e all'esito dei controlli; `Baseline_corrente.json` e' aggiornata.
     Lo **stato** di ogni rischio (registro unico, D-79: nel radar, in uscita o
     in osservazione) e' nel RiskRegister, calcolato con la regola di Parametri
     (`radar.py`); lo script stampa quanti sono nel radar e in osservazione, chi
     e' entrato e chi e' uscito. I prompt del pacchetto sono archiviati in
     `Cicli/<ciclo>/Prompt_in_uso/`.
5. **Validazione umana** (obbligatoria): nel foglio Validazione del registro,
   una riga per rischio (anche in osservazione, con la decisione sullo stato),
   KRI e azione proposti da A1, con le celle gialle gia' compilate con le
   proposte (D-67, D-79), il validatore
   cambia i valori con cui non e' d'accordo (con la Motivazione) o respinge un
   KRI, un'azione o una voce (Respingi = Sì), salva, chiude
   e lancia
   `python esegui_ciclo_locale.py valida --periodo <ciclo> --validatore "<chi>"`
   (rigenera anche il report al comitato, D-83).
   Una riga non toccata vale come accettata. Finche' non lo fa, il ciclo dopo
   non parte. Passo per passo: `00_GUIDA_PASSO_PASSO.md`, sezione 3. Il
   dettaglio campo per campo resta nel foglio Storico_Validazioni; la
   validazione riscrive `Cicli/<ciclo>/Righe_liste_<ciclo>.json` con i valori
   validati. Se il foglio Validazione viene modificato per errore (righe
   cancellate, ID cambiati): `python esegui_ciclo_locale.py griglia`. Per
   cambiare dopo un valore gia' validato (D-76): `python esegui_ciclo_locale.py
   riapri` (gli oggetti del ciclo tornano nella griglia con il valore validato),
   poi `valida`, quante volte serve; i testi si correggono a mano nei fogli dati,
   poi `baseline` (guida, sezione 3-ter).
6. Archiviare in `Archivio_Cicli` il testo dei prompt in uso.
7. **Schede dei rischi** (D-40): `python esegui_ciclo_locale.py schede-input`
   (si ferma se il ciclo non e' validato) scrive
   `Cicli/<ciclo>/Input_A6_<ciclo>.json`; in A6 allegarlo, da solo, e
   scrivere "Scrivi le schede"; salvare la risposta come `A6_<ciclo>.json`;
   `python esegui_ciclo_locale.py schede --payload A6_<ciclo>.json` controlla
   l'output (schema; stessi rischi, quattro dimensioni, fonti identiche, nessun
   numero fuori dai dati) e scrive `Cicli/<ciclo>/Schede_<ciclo>.xlsx`. Codice
   1 = fermato, nessun file: incollare i motivi nella chat di A6 e rifare. Senza
   `--payload`: schede con i testi del registro. Il registro non si tocca.
8. **Report al comitato** (D-32, D-39, D-62): `python esegui_ciclo_locale.py
   report` scrive `Cicli/<ciclo>/Report_comitato_<ciclo>.pdf` (con
   `--con-lavoro` anche Registro e Parametri); rilanciarlo dopo ogni modifica
   manuale dei validatori. Allegare il file delle schede.

## Ciclo straordinario (su decisione della funzione di rischio, D-75)

`python esegui_ciclo_locale.py baseline --straordinario [--rischi NFR-nn[,NFR-mm]] --motivo "..." --decisore "<chi>" [--data AAAA-MM-GG]`
archivia la decisione e scrive baseline e `Input_A8_<AAAAQn-Sk>.txt`; A8 Evento critico (D-77),
con l'allegato e i documenti dell'evento, "Esegui il ciclo straordinario" rivaluta solo quei rischi,
censisce i nuovi creati dall'evento (senza `--rischi`: solo censimento) e scrive `analisi_evento`;
poi `precontrollo` (facoltativo) e `trimestrale --payload A8_<AAAAQn-Sk>.json` (riporta gli altri rischi dal
ciclo prima, gia' validati) e `valida --periodo <AAAAQn-Sk>`. L'analisi va nella colonna
Straordinario di Sintesi_Cicli (il fatto) e nella knowledge di A7 (`Ciclo.txt`). La proposta puo'
venire da A3 (a video in `settimanale` e nel foglio Notizie) o da A4. Passo per passo: guida,
sezione 2-bis.

## Dismettere un rischio (su decisione della funzione di rischio)

`python esegui_ciclo_locale.py dismetti --rischio NFR-nn --motivazione "..." --decisore "<chi>"`.
Toglie il rischio dall'anagrafica senza buchi, fa uscire di vigore i suoi KRI
del ciclo corrente, annulla le sue azioni aperte, aggiorna la baseline e
archivia l'atto in `Archivio_Cicli/Dismissioni/`. La storia resta nel registro.
Mai svuotare a mano una riga dell'anagrafica: le viste perderebbero l'ultimo rischio.

## Procedura settimanale

0. La raccolta automatica (`raccogli_notizie.py`) ha scritto la
   `Raccolta_<data>.txt` della settimana; gli analisti salvano in `Manuali/`
   cio' che viene dai siti senza feed e dalle fonti a licenza.
1. A3, chat nuova, con l'allegato `Input_A3_A4.txt` (la baseline, AU7): "Esegui
   l'aggiornamento settimanale". Il prompt schedulato non porta l'allegato e
   risponde "Baseline mancante". Salvare il JSON della risposta come
   `A3_<AAAA-MM-GG>.json`.
2. `python esegui_ciclo_locale.py settimanale --payload A3_<AAAA-MM-GG>.json`:
   l'Excel di output della settimana e' in `Settimane/<AAAA-MM-GG>/`.
   Rilanciarlo sulla stessa settimana non duplica le notizie. Si ferma se una
   notizia cita un codice fonte che non e' in `fonti.md` (o e' escluso).
3. Consigliato: validare le notizie della settimana (foglio Validazione, una
   riga per notizia, poi `valida --periodo <AAAA-MM-GG> --validatore "<chi>"`).
   Le notizie non validate restano nel foglio; oltre 200, il settimanale si
   ferma e chiede di validare le settimane piu' vecchie.

## L'app NFR (D-83)

Installazione su un PC nuovo: doppio clic su `installa.cmd` (tappa M3: moduli, configurazione con una finestra, collegamenti, raccolta pianificata, Verifica del PC; guida, sezione 0.3). Poi doppio clic sul collegamento **NFR Horizon Scan** del Desktop, o su `NFR.cmd`: la finestra mostra lo stato del processo e il prossimo passo e guida ogni processo
(settimana, trimestre, straordinario, validazione, schede e report, riapertura, testi a mano, parere di A4). Per ogni
agente prepara gli allegati, apre l'agente (`link_agenti` in `configurazione.json`) e mette la richiesta negli
appunti; la risposta si incolla nel riquadro dell'app (o, con `ascolta_appunti`, basta premere Copia). Gli agenti
possono essere in Agent Builder o in Copilot Studio (casella "Agenti": stessi nomi e cartelle, origine annotata). I
comandi scritti a mano restano validi: l'app lancia gli stessi. Passo per passo: guida, sezione "L'app NFR: uso passo
per passo"; configurazione: guida, sezioni 0.2 (punto 3-bis), 0.2-bis e 0.3.

## Piu' analisti sullo stesso registro (D-83)

Ogni comando che scrive prende il lucchetto `Archivio_Cicli/_Lucchetto/registro.json`
(chi, PC, comando, da quando; scade dopo 2 ore) e lavora su una copia di lavoro
locale del registro: il registro vero si sostituisce alla fine, dopo i controlli, solo
se nessuno l'ha cambiato nel frattempo. Un collega che sta scrivendo ferma il comando
("Il registro e' in uso"); un lucchetto rimasto per errore si toglie con
`python esegui_ciclo_locale.py sblocca --motivo "..."`, registrato in `sblocchi.log`.

## Cosa copre lo script dei controlli di A5 — dichiarato, non sottinteso

| Controllo | Copertura meccanizzata |
|---|---|
| C1, C2, C7 | per intero; Bloccante (integrita', D-71) |
| C9 | per intero: identificativi dei KRI Bloccanti; coppia Esposizione/Evoluzione e soglie Da motivare (D-71) |
| C3 | date, frasi generiche, massimo un punto: Da motivare (D-71; il salto lo ferma `valida`) |
| C5 | date delle fonti Da motivare; rilevanza e fonti perse come Osservazione |
| C6, C8 | euristica a stringhe: solo Osservazione (un owner persona lo ferma il comando `valida`, D-54) |
| C4 | **nessuna**: plausibilita' rispetto ai descrittori, solo l'agente A5 |
| Registro unico (D-79) | solo lo script, con lo stato previsto dalla regola: oltre 20 rischi in osservazione e rischio del radar senza KRI o azioni come Bloccante; rischio che entra senza KRI o azioni come Da motivare; KRI o azioni su un rischio in osservazione, riscritto senza fonte nuova, senza orizzonte o segnale come Osservazione |

Lo script non giudica la plausibilita' (C4): senza `--challenger` (A5 facoltativo, D-71) quel giudizio resta al
validatore.

## Limiti (onesti)

- **Passaggio a mano del JSON** fra chat dell'agente e app: Agent Builder non ha API,
  quindi la risposta si copia e si incolla nell'app (o si preme Copia e l'app la prende
  dagli appunti). Gli agenti possono essere anche in Copilot Studio, con lo stesso
  passaggio (guida, sezione 0.2-bis).
- **Liste SharePoint non scritte.** Senza Power Automate e senza API nessuno
  carica le liste. Non si perde storia: le tabelle del workbook sono tutte
  storiche (anche KRI, una riga per KRI per ciclo), con la cronologia versioni
  di SharePoint, gli Excel di output congelati e i backup. Si perde solo la
  seconda copia interrogabile da SharePoint.
- **Raccolta dipendente dalla rete del PC**: se il proxy aziendale blocca
  urllib, la raccolta automatica non funziona e restano i canali `sito` e
  `share`. Da verificare al setup (passo 5).
- **Excel desktop necessario** sul PC che lancia lo script, e il workbook non
  deve essere aperto da altri: lo script lo rileva e si ferma. Ogni comando apre
  e ricalcola Excel: un trimestrale richiede circa due minuti. Se Excel non
  parte al primo colpo (errore COM transitorio) lo script riprova fino a
  cinque volte.
- **Capacita' fissate dal template**: 20 rischi in anagrafica (lo script
  avverte quando restano 2 posti), 60 KRI correnti, 150 KRI nella storia.
  Oltre, lo script si ferma prima di scrivere; serve un template rigenerato, e
  il registro vivo si porta sul template nuovo con `aggiorna-registro`.
- **Governance.** Che il trattamento avvenga dentro Agent Builder non e' una
  qualificazione gia' fatta: vedi `04_Riferimenti/controlli_e_model_risk.md`, sezione 6.
