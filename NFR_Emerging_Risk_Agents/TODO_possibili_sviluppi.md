# TODO — possibili sviluppi

Il piano unico del lavoro ancora da fare: proposte non ancora fatte, da
decidere. Ognuna dice perche' serve, cosa fare, come capire che e' fatta.
Quando una voce viene realizzata si toglie da qui e si documenta dove vive
(00_LEGGIMI, guida, manuali).

Dal 28/09/2026 comprende anche il piano di automazione del processo
(`Analisi_Architettura/Archivio/10_Piano_automazione_processo.md`): qui stanno le voci
e l'ordine; nel documento 10 il dettaglio tecnico, le verifiche nel tenant e
le fonti.

Dal 07/10/2026 l'analisi architetturale ha **due sole opzioni**
(`Analisi_Architettura/12_Due_opzioni.md`): 1) app Python unica sul PC, che
corrisponde alle voci AU1-AU6 qui sotto, allargate a manutenzione,
straordinario, lucchetto del registro e ripresa dopo stop e riavvii; 2) Copilot
Studio nei vincoli della Banca (variante CS-1), da esplorare con le prove K1-K7
prima di decidere la A-15.

Sezioni:
- **ordine di lavoro**, unico per tutte le voci;
- **agenti nuovi** (piano del 07/10: A7 Assistente del registro, lista di osservazione, periodo straordinario,
  manutenzione in Excel, A8 evento critico; fase 1 fatta, D-72; fase 2 fatta, D-73; fase 3 fatta, D-75);
- **semplificazione dello scoring di A1** (S1, in corso dal 30/09);
- **automazione del processo** (AU1-AU6, dal piano 10; prende il posto di
  AR1);
- **processi** (P1-P9: cio' che manca rispetto al disegno atteso dei processi
  trimestrale, settimanale e spot; P8, dal 02/10, la lista di osservazione dei
  fenomeni oltre l'orizzonte del registro, fatta il 07/10, D-73);
- **quantificazione** (Q1);
- **grafici del registro** (G1-G6);
- **in riserva** (piano 07 e variante CS-2: non pianificati).

## Ordine di lavoro

| Passo | Voci | Quando | Giorni |
|---|---|---|---|
| 0 | S1: semplificazione dello scoring di A1 (D-49..D-56) | nel pacchetto dal 30/09; restano le verifiche dell'utente e il passo sul PC della Banca | circa 6 |
| 1 | AU1, AU2, AU3: la parte comune del piano 10, utile qualunque strada si scelga | dopo S1 | 6-7 |
| in parallelo, facoltativo | prova K0 in Copilot Studio (AU4), con il precontrollo dentro A1 nelle due opzioni del codice (D-70): **pronta dal 05/10**, `09_Copilot_Studio/Prova_con_Copilot_Studio.md`; insieme, la prova della versione senza Copilot Studio (`08_Deploy/Prova_senza_Copilot_Studio.md`) | ora, sul PC della Banca | 1-2 |
| in parallelo | G1, G3, G2 (toccano solo il generatore del template) | quando c'e' tempo | circa 2 |
| in parallelo | G6, report intermedio A1+A5 (nato dal collaudo del primo ciclo, 29/09; ridimensionato da S1: i rilievi stanno gia' sui rischi) | quando servira' leggere A1 e A5 prima della scrittura | basso |
| 2 | AU4: scelta della strada (decisione aperta A-15) | alla fine del passo 1 | — |
| 3 | AU5 (strada A) **oppure** AU6 (variante CS-1) | dopo A-15 | 3-4 oppure 13-15 |
| 4 | P3, P1, P4, P8, poi P5, P2, P7, P6 | dopo il passo 3 | circa 3 settimane e mezza |
| 5 | Q1: la nota di metodo in qualunque momento, il prototipo dopo il passo 4 | | nota 1-2, prototipo 3-5 |
| sempre | G5, difetti estetici | quando capitano | |

**Calendario.** Il primo ciclo vero e' il 2026Q4, con il primo run di A1 a
inizio gennaio 2027 (D-22). I passi 1-3 stanno prima di quella data anche con
la variante CS-1: il primo ciclo si farebbe gia' con l'automazione.

**Regola d'ordine per le voci P e Q** (prende il posto di quella di AR1): si
fanno sull'architettura Python, **dopo il passo 3**. P3 aggiunge un'azione alla
coda delle richieste (AU2) e una voce al menu (AU5) o un argomento
all'Operatore (AU6): farla dopo evita di farla due volte. Le modifiche agli
schemi JSON (P1, P3, P5) si possono anticipare, perche' il contratto vale in
tutte le strade.

## Agenti nuovi (piano del 07/10/2026)

Piano approvato dall'utente il 07/10 (file di piano di Claude Code, riportato qui). Principio: **ridurre al
minimo scambi e interazioni con Python** (nessun comando per preparare gli input degli agenti, nessun JSON da
gestire a mano per spiegazioni e manutenzione, un solo comando per applicare cio' che cambia il registro).

| Fase | Contenuto | Stato | Impegno |
|---|---|---|---|
| 1 | **A7 Assistente del registro**, modo spiegazioni (in chat, knowledge `Kernel/Spiegazioni` scritta dallo script), fenomeni scartati da A1, Note dell'analista nel Quadro | **fatta il 07/10 (D-72)**; in Banca il copione `Prova_A7.md` confronta la knowledge di testo con il registro Excel letto direttamente | ~2 giorni |
| 2 | **Lista di osservazione** (voce P8 qui sotto): tabella e foglio, sezione nella griglia, A1 e A8 propongono, la manutenzione applica | **fatta il 07/10 sera (D-73)**: tabella storica, foglio Osservazione, pagina Fenomeni del report, sezione della griglia, A1 propone (guida di scrittura), controlli dello script, baseline, knowledge di A7; A3 collega notizie e segnali alle voci (struttura 2026-10-07c); restano le voci di A8 (fase 5) e le voci aggiunte o archiviate a mano (fase 4) | ~3 giorni |
| 3 | **Periodo straordinario** `AAAAQn-Sk` (motore della voce P3): sequenza dei periodi letta dal registro, periodo completo con i rischi non toccati gia' validati, `cicloPrecedente` e cicli del trend scritti dallo script, Y di Mosca dalle azioni aperte di qualunque periodo, C1 in modalita' straordinaria | **fatta il 07/10 (D-75)**: lo straordinario conta come ciclo per la regola del punto; Y di Mosca dalle azioni del periodo di valutazione del rischio (colonna Periodo_Valutazione), non di qualunque periodo; con la proposta di A3 e A4 (regola del segnale critico) | ~5 giorni |
| 4 | **Manutenzione in Excel** (foglio Manutenzione con elenchi a discesa e cella Decisore, comando `manutenzione` senza argomenti, applica subito: eccezione a D-05 con decisore e motivo) e **A7 in modo manutenzione** (righe da incollare nel foglio, testo separato da tabulazioni; non propone valori di sua iniziativa) | da fare (dopo 1, 2, 3) | ~2-3 giorni |
| 5 | **A8 Evento critico / rischio nuovo**: stesso allegato di A1 piu' documenti indicati, analisi approfondita, rivaluta i rischi indicati e censisce i nuovi; comando `straordinario --payload A8.json`, poi `valida` | da fare (dopo 3) | ~2 giorni |

Operazioni della manutenzione (fase 4): modifica valutazione, modifica KRI, porta in osservazione (riuso di
`dismetti`), nuova e archivia osservazione, presidio, attenzione del supervisore, stato di un'azione (oggi a mano
in Excel). Le modifiche di valutazione creano un periodo `-Sk` gia' validato per i soli rischi toccati.

## Pulizia e ottimizzazione del progetto (richieste dell'utente del 07/10/2026)

Si spunta qui, nella colonna Stato, come per gli agenti nuovi.

| # | Voce | Proposta | Stato |
|---|---|---|---|
| M1 | **Collaudo piu' corto** (la catena con Excel dura circa 50 minuti) | (a) dividere `run_catena.py` in gruppi indipendenti (catena principale, gate, errore dopo il salvataggio, primo uso, produzione, aggiornamento dei registri vecchi, segnalazioni), che gia' lavorano su copie separate, e lanciarli **in parallelo** con un'istanza di Excel ciascuno: stimato 20-25 minuti; (b) **collaudo mirato**: `esegui_collaudo.py --mirato` sceglie le suite dai file cambiati (testi e prompt: niente catena; script e template: la catena); (c) meno letture complete del registro (`leggi()` apre Excel e ricalcola a ogni chiamata) | da fare |
| M2 | **Quando rigenerare la demo** | solo quando cambia cio' che si vede (template, report, schede, guida dei passi, comandi) e prima di consegnare un pacchetto in Banca; non a ogni modifica interna. Regola scritta nel PROMPT_MASTER (sezione DEMO) e nell'HANDOFF | **fatto** il 07/10 (regola scritta) |
| M3 | Cartella `Anteprima_S1` (fuori dal pacchetto) | non e' piu' attuale: anteprime del 30/09-01/10 dello scoring S1 e della griglia di validazione, gia' nel pacchetto. Proposta: eliminarla (o spostarla in `Analisi_Architettura/Archivio`), insieme agli zip del 05/10 superati | **fatto** il 07/10 (cartella e zip eliminati, con l'ok dell'utente) |
| M4 | **Alberatura del pacchetto** | `05_Workflow` (un file, riferimento tecnico dei flussi, in parte ripete la guida), `06_Governance` (un file, controlli e model risk, serve alle funzioni di controllo), `04_SharePoint` (un file) e `08_Deploy` (DECISIONI e due copioni di prova) in **una cartella di documenti di riferimento**, con `DECISIONI.md` in evidenza e le prove in una sottocartella; `07_Senza_Studio` e `09_Copilot_Studio` in **una cartella con due sottocartelle** (locale, copilot_studio): il kit di Copilot Studio e' gia' generato dai moduli dello script (`prepara_kit.py`), quindi non ci sono file da unificare oltre al generatore. Attenzione: in Banca la cartella degli script e' gia' installata con il nome `07_Senza_Studio` e i percorsi sono in `configurazione.json` e nelle attivita' pianificate: lo spostamento chiede una reinstallazione guidata | da decidere con l'utente |
| M5 | Script temporanei non piu' attuali | eliminato `diagnosi_validazione.py` (fuori dal pacchetto) e le cache `__pycache__` il 07/10 | **fatto** |

## Semplificazione dello scoring di A1 (documento `Analisi_Architettura/Archivio/11`)

### S1. Semplificare scoring e selezione dei rischi di A1 — nel pacchetto dal 30/09/2026

**Stato al 30/09**: kernel, prompt (A1 7.885 caratteri dopo la revisione della sera), controlli, script,
schede, workbook (struttura 2026-09-30, 20 rischi), collaudo (passi 11b e 12
nuovi, dati di prova convertiti e baseline rigenerate) e documentazione sono
fatti. Restano: le verifiche dell'utente (bozza della rubrica e schemi,
anteprima del template in `Anteprima_S1/`, dimensioni dei prompt), la demo
rilanciata e, sul PC della Banca, `aggiorna-registro` prima su una copia e poi
sul registro in uso, il ricaricamento di A1, A5, A6, A4 e il ciclo 2026Q4 di
prova.

- **Perche'**: il collaudo del primo ciclo (29/09) ha richiesto 7-8 giri
  A1 <-> A5; A1 doveva sostenere con poche fonti esterne giudizi che non puo'
  sostenere (controlli della Banca, KRI con dati interni, frequenze per
  rischi senza storia) e fare contabilita' che lo script sa fare (esito,
  da/a). Decisioni D-49..D-56.
- **Perche' prima di AU1**: lo schema di A1 e' il contratto su cui poggiano
  AU2 (riconoscimento degli agenti dai campi `required`) e le voci P1, P3,
  P5; la semplificazione libera anche lo spazio che P5 chiede nel prompt di
  A1 (7.977 caratteri su 8.000 il 29/09).
- **Cosa fare** (dettaglio nel documento 11, sezioni 5-6): kernel (rubrica,
  tassonomia, schemi, mappa); codice (controlli, script di campo, schede,
  confronto); workbook (versione nuova della struttura, capienza 20 rischi);
  collaudo (catena, nuovo passo 11b sul registro 2026-09-25c); prompt A1, A5,
  A6, A4; documentazione, PROMPT_MASTER e demo.
- **Momenti di verifica dell'utente**: bozza della rubrica e schemi;
  anteprima del template; dimensioni dei prompt; `aggiorna-registro` su una
  copia del registro in uso.
- **Fatto quando**: collaudo completo verde con i casi nuovi (Velocity vuota,
  KRI senza soglie, esito calcolato, `--procedi-con-rilievi`, migrazione dai
  template 2026-09-23 e 2026-09-25c); demo rilanciata; sul PC della Banca il
  ciclo di prova converge in 1-2 giri, oppure in un giro piu' l'opzione.
- **Impegno**: circa 6 giorni.
- **Fuori dal perimetro di S1** (visti durante il lavoro, da decidere):
  - la Y di Mosca conta solo le azioni del ciclo corrente, non quelle ancora
    aperte dei cicli prima (`genera_dashboard.py`, foglio Radar_Mosca);
  - `sogliaDelta` colora solo il Delta; il nome `rmPxI` non e' usato;
  - i flag di A3 citano "il descrittore", che A3 non ha nel prompt (tema di P1);
  - da una proposta esterna di supporto NFR esaminata il 30/09 (documento riservato, fuori dal pacchetto):
    tipo di KRI (evoluzione del fenomeno o esposizione della Banca), livello
    di allerta calcolato (monitoraggio, attenzione, attivazione), esposizione
    nei descrittori della Probabilita: **fatti il 01/10** (D-63 livello di
    allerta calcolato, colore del radar, senza colonne nuove; D-64 due KRI per
    rischio, Esposizione ed Evoluzione; D-65 Probabilita 4-5 solo con la Banca
    esposta). Restano: le conseguenze dei tre livelli (chi fa cosa, entro
    quando) da decidere con la funzione di rischio; la taratura delle soglie
    del livello con A-12 dopo il ciclo 2026Q4 reale.

## Automazione del processo (piano `Analisi_Architettura/Archivio/10`)

Oggi un trimestre chiede circa 13 passi manuali: 9 comandi da scrivere, 3
salvataggi in Blocco note, copie a mano, il PDF fatto a mano. Una settimana ne
chiede circa 7 (piano 10, 10.1). Obiettivo: niente copia-incolla, gli agenti
fanno il piu' possibile, ogni azione rimasta si lancia con un doppio clic o un
messaggio.

Punti fermi:
- **Python resta il motore** e il piano 07 passa in riserva: D-43 (scelta
  dell'utente del 27/09). La voce AR1 e' chiusa.
- **Copilot Studio e Power Query sono disponibili** nel tenant: D-44 (28/09).
  **Usare Copilot Studio non e' deciso**: e' la decisione aperta A-15, da
  prendere con la voce AU4.
- Principio che rende utile la parte comune: **separare chi chiede da chi
  esegue**. Nella strada A la richiesta la scrive il menu; nella variante CS-1
  la scrive un flusso di Copilot Studio. Tutto cio' che sta dietro la
  richiesta e' identico.
- Qualunque strada: nel registro scrive solo il motore, dopo i controlli (D-10);
  kernel, schemi, controlli, validazione e collaudo non cambiano.

### AU1. Motore: automatismi e scrittura robusta (piano 10: C2 e C3, cioe' F1 e F5)

- **Perche'**: spariscono tre passi a mano del trimestre (baseline copiata in
  `Kernel`, prompt copiati nell'archivio, PDF del report). La scrittura resta
  pulita anche con il registro in una cartella OneDrive: il Salvataggio
  automatico potrebbe salvare righe scritte prima di un fermo (rischio trovato
  il 27/09, forse la causa di `RPC_E_DISCONNECTED`).
- **Cosa fare**:
  - `_scrivi_baseline` copia anche `Baseline_corrente.txt` nella cartella
    `kernel` configurata. **Trappola**: non quando `kernel` e' la `01_Kernel`
    del pacchetto (collaudo e demo);
  - `trimestrale` archivia i prompt generati in `Cicli/<ciclo>/Prompt_in_uso/`;
  - comando `report`: **fatto il 30/09 sera (D-62)**, PDF in
    `Cicli/<ciclo>/Report_comitato_<ciclo>.pdf`, rilanciabile dopo correzioni
    manuali. Resta: lanciarlo da `valida` per i trimestrali; `schede` esporta
    anche `Schede_<ciclo>.pdf`.
    Un errore nel PDF e' solo un avviso: i dati sono gia' salvati;
  - `wb.AutoSaveOn = False` subito dopo l'apertura;
  - `registro_in_lavoro(conf)` per `trimestrale`, `settimanale`, `valida` e
    `dismetti`: copia di lavoro locale, scrittura e controlli sulla copia,
    sostituzione solo se l'originale non e' cambiato nel frattempo.
- **Tocca**: `esegui_ciclo_locale.py`, `excel_com.py`, `schede.py`,
  `Demo_W1_W2/esegui_demo.py`, `run_catena.py`, guida, `06_Governance`.
- **Fatto quando**: la catena di collaudo produce i due PDF, prova il caso
  "registro cambiato nel frattempo", trova la baseline in `kernel` e i prompt
  archiviati; la demo e' rilanciata.
- **Impegno**: circa 2 giorni, collaudo e documentazione compresi.

### AU2. Ingresso unico, stato del processo e coda delle richieste (piano 10: C4-C7)

- **Perche'**: tutte le risposte degli agenti entrano da un solo posto,
  `Archivio_Cicli\In_arrivo\`, che vengano dagli appunti (strada A) o da un
  flusso (CS-1). Ogni azione del motore diventa una richiesta controllata.
  Questo lavoro serve in entrambe le strade.
- **Cosa fare**:
  - `07_Senza_Studio/ingresso.py`:
    - `estrai_json`: toglie BOM e recinti ```json; trova il JSON in mezzo al
      testo; se e' troncato unisce le parti successive;
    - `riconosci_agente`: usa i campi `required` degli schemi, senza regole
      ricopiate;
    - nomi dei file (`A1_<ciclo>.json`, `A3_<settimana>.json`...) e controllo
      di schema subito;
    - `messaggio_correzione`: dai motivi di un FERMATO, il testo per l'agente.
      **Per A1 c'e' dal 02/10/2026** (D-69): `messaggio_correzione`, dal 05/10
      in `07_Senza_Studio/precontrollo.py` (D-70), usato dal comando
      `precontrollo` e dalla skill di Copilot Studio (schema, controlli
      meccanizzati, parti del razionale); qui resta da estenderlo agli altri
      agenti e ai fermi di `settimanale` e `schede` (per `trimestrale` fatto il
      06/10, D-71: su un fermo di integrita' scrive `Correzione_A1_<ciclo>.txt`);
    - conserva il testo originale;
  - `stato(conf)`: stato del processo e prossimo passo, senza Excel, scritto
    anche in `Esiti/Stato_processo.json`;
  - esecutore del motore in un sottoprocesso: fasce OK / FERMATO / ERRORE
    TECNICO, `Esiti/Esito_<id>.json`, log in `Archivio_Cicli/Log`;
  - coda delle richieste:
    - `01_Kernel/schema_richiesta.json`;
    - lista bianca: `baseline`, `precontrollo`, `trimestrale`, `settimanale`, `valida`,
      `schede-input`, `schede`, `report`;
    - validatori ammessi in `configurazione.json`;
    - `inizializza`, `dismetti` e `aggiorna-registro` solo da riga di comando;
  - `02_Agenti/modelli/A3.md`: una riga ("le notizie possono arrivare anche
    come allegati o nel testo della richiesta"), poi `componi_prompt.py` e
    ricaricare A3.
- **Tocca**: file nuovi in `07_Senza_Studio` e nel kernel, modello di A3,
  collaudo (test nuovo senza Excel in `esegui_collaudo.py`), 00_LEGGIMI ("Dove
  vive ogni regola").
- **Fatto quando**:
  - i test senza Excel sono verdi: estrazione da testi reali (recinti, testo
    attorno, BOM, JSON in due parti), riconoscimento e nomi, stato calcolato
    da archivi finti, richieste fuori lista o con un validatore non ammesso
    rifiutate;
  - A3 resta sotto gli 8.000 caratteri.
- **Impegno**: circa 3 giorni.

### AU3. Installazione con un doppio clic e Verifica del PC (piano 10: C8, parte comune di F4)

- **Perche'**: i blocchi della prima installazione del 24/09 erano di questo
  tipo (`.json.txt`, `Workbook non trovato: None`, pythoncom a meta', proxy).
  Il PC che esegue il motore si installa allo stesso modo in entrambe le
  strade: quello dell'analista nella strada A, il PC esecutore nella CS-1.
- **Cosa fare**: `installa.cmd` + `installa.py`, ripetibili:
  - controllo di Python e dei moduli; `pip install --user` solo di cio' che
    manca, con un messaggio chiaro se il proxy blocca;
  - `configurazione.json` compilato con finestre di dialogo (cartelle,
    validatore): niente JSON in Blocco note;
  - `attrib +P` sulle cartelle sincronizzate;
  - Verifica del PC: moduli, Excel via COM, `AutoSaveOn` e `FullName` del
    registro, riga per riga in verde o rosso, con un file da mandare al
    manutentore.
- **Fatto quando**: `installa.cmd` su una cartella di prova produce una
  configurazione valida e la Verifica e' tutta verde; la guida, sezione 0, e'
  riscritta.
- **Impegno**: circa 1 giorno.

### AU4. Scegliere la strada: A (procedura guidata) o CS-1 (Copilot Studio) — decisione A-15

- **Perche'**: Copilot Studio e' disponibile (D-44) e automatizza di piu', ma
  e' piu' complesso. Sintesi del piano 10 (10.16):

  | | Strada A | Variante CS-1 |
  |---|---|---|
  | Cosa fa l'analista | menu al PC; per ogni agente trascina i file, incolla la richiesta, preme Copia | un messaggio in Teams e dei pulsanti; nessun gesto per agente |
  | Raccolta notizie | sul PC (proxy, `pypac`, attivita' pianificata) | flusso nel cloud |
  | Python | sul PC dell'analista | su un solo PC esecutore, in background |
  | Lavoro dopo la parte comune | 3-4 giorni | 13-15 giorni |
  | Cosa si aggiunge da mantenere | niente | Operatore, argomenti, flussi e sotto-agenti in Copilot Studio, piu' la soluzione esportata |
  | Nuove verifiche e pareri | V-A..V-G (piano 10, 10.5) | V-H..V-Q (10.18): DLP, modello, trascrizioni (parere DPO), sincronizzazione |
  | Agenti | quelli di oggi, in Agent Builder | da ricreare; la qualita' si rimisura con il doppio run |

- **Come scegliere**:
  - **CS-1** se vale almeno una di queste: piu' analisti useranno il sistema
    (a loro Python non servirebbe); si vuole lavorare da Teams senza stare al
    PC; i tre gesti per agente o la raccolta sul PC si rivelano un peso. In
    piu' devono riuscire la prova K0 e il parere sulle trascrizioni.
  - **Strada A** se il pilota resta a una persona al proprio PC (D-13), se si
    vuole la minima complessita' prima del primo ciclo vero, o se K0 o il
    parere non arrivano in tempo.
- **Facoltativo, prima di decidere: prova K0** (1-2 giorni). Si puo' fare
  subito, perche' Copilot Studio c'e': un agente con un sotto-agente, un agent
  flow che salva in SharePoint un JSON da 45 KB, la pubblicazione in Teams.
  Mostra la complessita' reale senza impegno.
  **Pronta dal 05/10/2026 (D-70)**, in `09_Copilot_Studio`. La prova misura:
  - A1 in Copilot Studio, sullo stesso input della prova senza Copilot Studio;
  - il precontrollo eseguito dentro l'agente in due modi: Code interpreter
    dell'esperienza standard con lo script allegato, oppure skill
    `precontrollo-nfr` nel sandbox della nuova esperienza (GitHub Copilot
    harness, a consumo di crediti);
  - facoltativi, Teams e l'agent flow.

  Il sotto-agente resta per la K3. Nuovi criteri di scelta dai risultati:
  - se il precontrollo gira dentro A1 con l'impronta verificata, il giro
    A1 -> PC si riduce in tutte e due le strade;
  - i crediti della nuova esperienza sono un costo che la strada A non ha.
- **Proposta, se alla fine del passo 1 la decisione non c'e'**: strada A. La
  CS-1 resta aggiungibile anche dopo, perche' cambia solo chi scrive le
  richieste. Del lavoro della strada A si perderebbe una parte dei 3-4 giorni;
  menu e appunti resterebbero come riserva.
- **Fatto quando**: A-15 e' chiusa in `08_Deploy/DECISIONI.md` con la strada
  scelta.

### AU5. Strada A: procedura guidata a menu (solo se A-15 sceglie la strada A)

- **Cosa fare** (piano 10: ascolto degli appunti di F2, menu di F3, parte
  specifica di F4, guida e demo di F7):
  - `07_Senza_Studio/appunti.py`: ascolto degli appunti con `win32clipboard`
    (`GetClipboardSequenceNumber`); cio' che si copia passa da `ingresso.py`
    (AU2);
  - `procedura.py` + `NFR.cmd`: menu con lo stato e il prossimo passo (Invio =
    procedi). Il menu scrive le richieste nella coda di AU2. Per ogni agente:
    prepara `%USERPROFILE%\NFR_Da_allegare\`, apre il link dell'agente, mette
    la richiesta negli appunti, aspetta la copia. Per la validazione apre
    Excel sulla griglia del foglio Validazione (una riga per oggetto dal
    02/10, D-67: niente filtri da mettere);
  - link degli agenti in `configurazione.json`;
  - `NFR_incolla.cmd` con il tasto di scelta rapida (niente Ctrl+Alt: sulla
    tastiera italiana e' AltGr);
  - "Invia a -> NFR notizie manuali";
  - attivita' pianificata della raccolta con `schtasks /create /xml`;
  - guida riscritta attorno al menu, con l'appendice "Comandi diretti"; demo
    con appunti simulati.
- **Verifiche nel tenant**: V-A..V-G (piano 10, 10.5).
- **Fatto quando**: la demo passa dalla procedura con appunti simulati (A1 con
  i recinti, A1 in due parti, correzione dopo un FERMATO) e la prova a mano sul
  PC riesce (piano 10, 10.6).
- **Impegno**: 3-4 giorni.

### AU6. Variante CS-1: Copilot Studio con il motore in background (solo se A-15 sceglie la CS-1)

- **Cosa fare** (piano 10, 10.12 e fasi K1-K6 di 10.15; la K0 e' in AU4):
  - `07_Senza_Studio/motore_in_ascolto.py` sul PC esecutore: parte
    all'accesso a Windows, esegue la coda di AU2, aggiorna
    `motore_attivo.json`, mostra un avviso sul PC;
  - agent flow `Deposita_Risposta`, `Scrivi_Richiesta`, `Leggi_Stato`,
    `Leggi_File`, `Salva_Allegato`, `Archivia_Parere`, con le schede di
    costruzione in `09_Copilot_Studio/`;
  - A1, A3 e A4 come sotto-agenti; A5 e A6 come strumenti prompt con uscita
    JSON; istruzioni sempre da `componi_prompt.py`;
  - Operatore NFR: argomenti guidati, Adaptive Card, copioni di collaudo con i
    casi ostili;
  - cloud flow della raccolta del lunedi', con le fonti da
    `Kernel/fonti_rss.json` generato da `fonti.md`; 2-4 settimane in ombra con
    `raccogli_notizie.py`;
  - le regole di governo 1-6 del piano 10 (10.12) in `06_Governance`; A-11
    chiusa (`05_Workflow` archiviata, sostituita da `09_Copilot_Studio`).
- **Verifiche nel tenant**: V-H..V-Q (piano 10, 10.18).
- **Fatto quando**:
  - i copioni di conversazione sono superati due volte di fila;
  - la demo con richieste simulate e' rilanciata;
  - il primo ciclo vero passa dal doppio run e dalla validazione
    (guida, Avvio del progetto, fase 7), perche' cambia la piattaforma degli agenti.
- **Impegno**: 13-15 giorni, piu' l'ombra della raccolta.

## Processi: cosa manca rispetto al disegno atteso

Dall'analisi del 26/09/2026: il processo desiderato e' **trimestrale come
processo fondante** (su documentazione approfondita: regolatori, analisti di
settore, siti specialistici, analisi interne), **settimanale o mensile** sulle
notizie (nuove schede, trend e notch dei rischi esistenti, evento critico che
chiede di rigenerare il trimestre, variazioni visibili sul radar) e **spot**
su una sola notizia (analisi a fondo su tutti i rischi, impatto per
dimensione, posizione sul radar).

**Decisioni dell'utente sull'analisi (26/09, `08_Deploy/DECISIONI.md`)**:
- **D-41**: restano "mai una cifra nuova" fuori dal trimestre e "solo il ciclo
  trimestrale modifica uno score". Unica eccezione: un **segnale critico**
  (es. l'annuncio di un modello di AI con capacita' offensive nuove, come
  Mythos) puo' portare a un **ciclo straordinario** con la stessa catena del
  trimestre. Quindi niente notch numerici ne' posizioni ipotetiche sul radar
  (P1 ridotta a segnali qualitativi), e P3 diventa la via per muovere uno
  score fra due trimestri.
- **D-42**: un evento che tocca piu' rischi genera **righe di rischio
  separate**, collegate fra loro; niente categorie secondarie con score
  propri (P5 riscritta).

| Attesa | Stato oggi | Dove |
|---|---|---|
| Trimestrale come unico processo che cambia gli score | c'e' | principio 3, W1 |
| Trimestrale su rapporti approfonditi di analisti e regolatori | in parte: vigilanza e cyber arrivano come feed di notizie; nessun canale per i rapporti da leggere per intero | P4 |
| Report aggiornato, non rifatto | in parte: A1 parte dagli score precedenti (Confermato/Variato/Nuovo, al piu' un punto); manca il ciclo straordinario | P3 |
| Spostamento nel tempo degli eventi | in parte: Storico, Delta, Registro (3 e 6 mesi), schede; il radar e' una fotografia | P2 |
| Evento con piu' categorie | c'e' come regola (D-42): righe separate, un event type ciascuna, piu' driver; manca il collegamento fra le righe | P5, P6 |
| Settimanale: analisi su tutti i rischi | c'e': sette impatti per notizia; un solo rischio collegato | P1 (tutti i rischi toccati) |
| Settimanale: nuova scheda se il rischio non c'era | in parte: "AREA NON PRESIDIATA"; il rischio nasce al trimestre (o nel ciclo straordinario) | P3 |
| Settimanale: trend dei rischi esistenti | in parte: segnali netti, pressione, flag, soglia 3 in 4 settimane; per D-41 nessun notch numerico | P1 (qualitativo) |
| Settimanale: evento critico, proposta di rigenerare il trimestre | manca (deciso: D-41) | P3 |
| Settimanale e spot: pressione visibile sul radar | manca; per D-41 senza spostare il cerchio | P1 |
| Cadenza mensile | in parte: la finestra di 4 settimane lo e' di fatto | P7 |
| Spot: analisi a fondo della notizia | c'e': A4, sei sezioni | P3 (segnale critico) |
| Spot: impatto per dimensione | in parte: A4 indica il descrittore messo in discussione; per D-41 nessuna cifra | P1 |
| Fenomeni oltre l'orizzonte del registro (lontani o quasi impossibili oggi) | c'e' dal 07/10: lista di osservazione (D-73), fino a 30 voci fuori dal registro | P8 (fatto) |

Ordine consigliato: P3, P1, P4, P8, poi P5, P2, P7, P6 (P8 dopo P4, che porta
i rapporti di scenario da cui nascono i fenomeni lontani).

### P1. Segnali qualitativi per dimensione e pressione sul radar (settimanale e spot)

- **Perche'**: oggi fra un trimestre e l'altro il radar non dice quali rischi
  sono sotto pressione, e il settimanale dice "peggiorativo" ma non "su quale
  dimensione". Per D-41 senza numeri: nessun notch, nessuna posizione
  ipotetica.
- **Cosa fare**: A3 indica, per **ogni** rischio toccato da una notizia (non
  solo il piu' diretto), direzione, **dimensione** e **descrittore** messi in
  discussione; A4 fa lo stesso nella sezione 3 del parere (gia' quasi cosi').
  Il foglio conta i segnali per rischio e dimensione nelle ultime 4 settimane e
  segna il cerchio **deliberato** nel Radar_Mosca e la riga del Registro con
  una freccia (in peggioramento, in miglioramento, contrastato) quando la
  soglia di direzione e' superata. Il cerchio non si sposta. I segnali
  arrivano ad A1 come flag del trimestre, con la dimensione.
- **Tocca**: schema A3 (dimensione nei flag, piu' rischi per notizia),
  `mappatura_campi.json`, fogli Notizie, Registro e Radar_Mosca, prompt A3 e
  A4, controlli e collaudo. Nessun principio da cambiare. Dopo S1 (30/09) le
  dimensioni sono Impatto, Probabilita, Prossimita e Velocity (facoltativa);
  un segnale sulla Velocity di un rischio "non valutato" e' un buon motivo per
  valutarla al trimestre.
- **Fatto quando**: in demo tre settimane di notizie peggiorative sulla
  Probabilita di un rischio mettono la freccia sul suo cerchio e nel Registro,
  il cerchio resta fermo e il trimestre dopo A1 riceve il flag con la
  dimensione.
- **Impegno**: medio (circa 2-3 giorni con collaudo e documentazione).

### P2. Scia sul radar e nel report trimestrale

- **Perche'**: il comitato vede dove sta un rischio oggi, non da dove viene.
- **Cosa fare**: nel Radar_Mosca un punto piccolo nella posizione del
  trimestre prima e una freccia verso quella attuale (solo per i rischi
  variati, per non affollare); nel Quadro, per i primi cinque, la traiettoria
  su quattro trimestri.
- **Fatto quando**: nella demo il rischio variato fra 2026Q3 e 2026Q4 mostra
  la scia; gli altri no.
- **Impegno**: basso-medio (serie in piu' nel grafico, dati da Storico).

### P3. Evento critico e ciclo straordinario

**Stato al 07/10/2026: fatta (D-75, struttura 2026-10-08)**, compresa la proposta di A3 e A4. Resta l'agente
A8 (fase 5 del piano degli agenti nuovi) per l'analisi approfondita dell'evento. Il testo qui sotto e' la proposta del 26/09.

- **Perche'**: oggi un evento grave a meta' trimestre aspetta la fine del
  trimestre; nessun meccanismo lo segnala come tale. E' l'unica eccezione
  decisa al principio "solo il trimestre modifica uno score" (D-41; esempio
  dell'utente: l'annuncio di un modello di AI con capacita' offensive nuove,
  come Mythos). E' anche la via per un rischio nuovo che non puo' aspettare.
- **Cosa fare**: campo `critico` (si/no, con motivo) nell'output di A3 e di
  A4, con una regola esplicita nella rubrica (es. intensita' 3 su un rischio
  con Impatto >= 4, un cambio di capacita' di una minaccia che rende superato
  un descrittore, o evento in corso presso controparti della Banca); lo
  script lo mette in evidenza a video e nel foglio Notizie con "PROPOSTA DI
  CICLO STRAORDINARIO". La funzione di rischio decide; il ciclo straordinario
  e' un comando (es. `trimestrale --straordinario`) che rivaluta solo i rischi
  indicati (e puo' aggiungerne di nuovi), con la stessa catena (A1, A5,
  controlli, validazione) e un periodo proprio (es. `2026Q4-S1`). Il
  trimestre ordinario dopo parte dai valori validati dello straordinario;
  regole di variazione invariate (al piu' un punto per ciclo, straordinario
  compreso: da decidere se lo straordinario conta come ciclo per questa
  regola). Il principio 3 di `00_LEGGIMI.md` si riformula: "solo un ciclo di
  valutazione (trimestrale o straordinario) modifica uno score".
- **Tocca**: rubrica (regola del critico), schemi A3/A4, script, formato del
  periodo in mappa e fogli, guida, workflow. Dopo il passo 3 dell'ordine di
  lavoro anche la coda delle richieste (AU2: `trimestrale` con
  `--straordinario` nella lista bianca) e una voce del menu (AU5) o un
  argomento dell'Operatore (AU6).
- **Fatto quando**: nella catena di collaudo una settimana con una notizia
  critica propone il ciclo straordinario e il ciclo straordinario validato
  aggiorna solo i rischi indicati.
- **Impegno**: alto (circa una settimana).

### P4. Canale "rapporti di scenario" per A1

- **Perche'**: il trimestre deve poggiare su analisi approfondite, non solo su
  notizie. Oggi A1 li usa solo se qualcuno li mette in `Analisi_Interne`,
  senza distinguerli.
- **Cosa fare**: in `fonti.md` un tipo di fonte `rapporto` (canale `share`),
  con una cartella dedicata (es. `Rapporti_Scenario/<anno>`); A1 li legge per
  primi e li cita nel razionale; le schede di A6 dicono quale rapporto sostiene
  quale dimensione. Esempi: ORX Emerging Risks e Horizon, EBA Risk Assessment
  Report, priorita' di vigilanza BCE, ENISA Threat Landscape, WEF Global
  Risks, Allianz Risk Barometer, rapporti delle societa' di consulenza.
- **Tocca**: `fonti.md` (e `fonti.py`), prompt A1, struttura SharePoint,
  licenze d'uso (governance).
- **Fatto quando**: il ciclo di prova cita almeno un rapporto per ogni rischio
  variato.
- **Impegno**: basso.

### P5. Rischi collegati (un evento, piu' righe di rischio)

- **Perche'**: un evento (es. "LLM sempre piu' capaci") tocca piu'
  meccanismi di perdita. Per D-42 diventa piu' righe di rischio separate, una
  per event type, ciascuna con i suoi score; va conservata la vista
  d'insieme dell'evento.
- **Cosa fare**: nel rischio un campo `collegati` (elenco di `id_rischio`,
  con una riga di motivo: "stesso evento", "stessa causa") proposto da A1 e
  validato come gli altri campi; il collegamento e' reciproco (lo script
  controlla che i rischi esistano e completa il verso opposto). Nel Registro
  una colonna "Collegati"; nelle schede un riquadro "Rischi collegati" con i
  loro score; nel Radar_Mosca, facoltativo, una linea sottile fra i cerchi
  collegati. Nessuna media e nessun score dell'evento.
- **Tocca**: `tassonomia_nfr.md` (la regola "due event type = due rischi"
  resta; si aggiunge il collegamento), schema A1, mappa, controlli (C-nuovo:
  collegati esistenti, niente autocollegamento), Registro, schede (A6 e
  `schede.py`), collaudo. Prompt A1: dopo la revisione del 30/09 sera e' a
  7.885 caratteri, con poco margine: serve spazio. La regola del 30/09 (un rischio per meccanismo di
  perdita, D-55) rende i collegamenti piu' frequenti: meccanismi prima
  accorpati diventano rischi separati dello stesso evento.
- **Fatto quando**: nella demo due rischi nati dallo stesso evento si citano a
  vicenda nel Registro e nelle schede.
- **Impegno**: medio.

### P6. Scheda "tema" per driver (facoltativa)

- **Perche'**: un fenomeno ampio (es. l'intelligenza artificiale, DRV-AI) oggi
  si vede solo sparso nei rischi figli (frodi con deepfake, errori di modelli
  interni, condotta).
- **Cosa fare**: nel file delle schede una scheda per driver (o per gruppo di
  rischi collegati, P5), con i rischi figli, i loro score e l'andamento;
  nessun score proprio del tema (D-42).
- **Fatto quando**: `Schede_<ciclo>.xlsx` ha una scheda per ogni driver con
  almeno due rischi.
- **Impegno**: basso.

### P7. Riepilogo mensile

- **Perche'**: la cadenza mensile e' utile per la funzione di rischio senza
  un agente in piu'.
- **Cosa fare**: una vista (o un file) che aggrega le ultime quattro settimane:
  segnali netti per rischio, pressione per event type, aree non presidiate,
  flag e (con P1) segnali per dimensione; notizie critiche e cicli
  straordinari del mese (P3).
- **Fatto quando**: un comando o un foglio produce il riepilogo del mese dai
  dati settimanali gia' registrati.
- **Impegno**: basso.

### P8. Lista di osservazione: fenomeni con una valutazione preliminare, collocati nella gerarchia dei rischi

**Stato al 07/10/2026 sera: fatta (D-73), struttura 2026-10-07b.** Decisioni prese
dall'utente: impatto potenziale 1-5 con i descrittori + orizzonte in anni +
plausibilita' (teorica, possibile, in crescita) + segnale di avvicinamento; al
massimo 30 voci, A1 riscrive solo quelle con evidenza nuova; foglio di lavoro
nel registro **e** pagina "Fenomeni" nel report, prima della Metodologia.
Criteri di ingresso: un meccanismo di perdita per la Banca e almeno una fonte;
archiviazione con motivo; A5 non la controlla (solo lo script, perche' il prompt di
A5 e' al limite). **Fatto poi, su richiesta dell'utente**: A3 collega le notizie
alle voci e propone segnali (Avvicina, Segnale verificato, Allontana), che A1
trova nella baseline (D-73 punto 6, struttura 2026-10-07c). **Non fatto**: voci
aggiunte o archiviate a mano senza passare da A1 (fase 4, manutenzione); voci
proposte da A8 (fase 5). Il testo qui sotto e' la proposta del 02/10.

Richiesta dell'utente del 02/10/2026.

- **Perche'**: il registro tiene i rischi con un meccanismo di perdita
  valutabile oggi. I fenomeni lontani (oltre 3 anni, anche a 10) o con
  plausibilita' quasi nulla possono entrare solo come rischi con Prossimita 1.
  Cosi' occupano uno dei 20 posti dell'anagrafica e chiedono ogni trimestre due
  KRI, almeno un'azione e un razionale di circa 4 KB; altrimenti restano fuori
  e nessuno li segue. Allargare il registro non e' la strada: a 50 rischi non
  reggono la lunghezza delle risposte di A1, A5 e A6, la validazione (200-250
  righe per trimestre) e la leggibilita' del report. Serve un posto piu'
  leggero, dove un fenomeno si osserva prima di diventare un rischio.
- **Cosa fare** (proposta, da decidere nel dettaglio):
  - una **lista separata dal registro**, con una riga per fenomeno: `OSS-nn`,
    nome, descrizione breve, fonti, data della prima osservazione, stato (in
    osservazione, promosso a rischio NFR-nn, archiviato con motivo);
  - **collocazione nella gerarchia dei rischi**: driver della tassonomia
    (perche' emerge), event type L1 in cui si manifesterebbe in perdita, rischi
    del registro che toccherebbe se si avvicina. Nessun codice nuovo nella
    tassonomia;
  - **valutazione preliminare**, senza score composito:
    - impatto potenziale con i descrittori della rubrica, se si manifestasse;
    - orizzonte stimato in anni (5, 10...), che la Prossimita non distingue
      oltre i 3 anni;
    - plausibilita' qualitativa: teorica, possibile, in crescita;
    - **segnale di avvicinamento**: il fatto osservabile che lo farebbe
      promuovere a rischio;
  - nessun KRI, nessuna azione; fuori da radar, classifica e urgenza: e' una
    lista da osservare, non un rischio (principio 1 e D-42 invariati);
  - chi la alimenta:
    - A1 nel trimestrale propone voci nuove e aggiorna quelle esistenti, con
      l'esito di ciascuna (confermata, avvicinata, promossa, archiviata);
    - A3 nel settimanale segnala le notizie che toccano un fenomeno in
      osservazione;
    - la funzione di rischio ne propone una con un documento in
      `Analisi_Interne`, come per un rischio aggiunto a mano;
  - **promozione**: quando il segnale di avvicinamento si verifica, A1 propone
    il rischio nuovo, valutato con la rubrica, e la voce passa a "promosso";
  - validazione nella griglia (sezione Osservazione: accetta, rettifica,
    respingi), leggera;
  - una vista per driver ed event type (dove si concentrano i fenomeni,
    accanto alla copertura del registro) e, facoltativa, una pagina
    "Fenomeni in osservazione" nel report al comitato;
  - peso nella risposta di A1: circa 0,5 KB per voce contro circa 4 KB per
    rischio, quindi 30 fenomeni pesano come 4 rischi. Le istruzioni per A1
    vanno nella guida di scrittura dell'allegato `Input_A1` (A1 e' a 7.963
    caratteri), nel prompt solo lo scheletro.
- **Da decidere**: la scala della valutazione preliminare (descrittori della
  rubrica o tre livelli qualitativi); se A1 rivede ogni trimestre tutte le voci
  o solo quelle con evidenza nuova; un numero massimo di voci; i criteri di
  ingresso (serve comunque un meccanismo di perdita per la Banca, anche
  lontano) e di archiviazione; se la lista entra nel report al comitato; se A5
  la controlla (probabilmente solo i controlli dello script: id, collocazione,
  promozione coerente).
- **Tocca**: rubrica (sezione nuova: ingresso, valutazione preliminare,
  promozione, archiviazione), schema A1 (elenco `osservazione` accanto a
  `rischi`), schema A3 (riferimento a `OSS-nn` nei flag), mappa, generatore
  (foglio e tabella nuovi: versione nuova della struttura e `aggiorna-registro`),
  script (scrittura, controlli, griglia di validazione, precontrollo), guida di
  scrittura di A1, prompt A1 e A3, baseline (le voci in osservazione per A1),
  collaudo, guida, demo.
- **Collegamenti**: P4 (i rapporti di scenario sono la fonte naturale dei
  fenomeni lontani), P5 e P6 (vista per tema e driver), capienza
  dell'anagrafica (`MAX_RISCHI`).
- **Fatto quando**: nella catena di collaudo A1 propone due fenomeni in
  osservazione collocati per driver ed event type; al ciclo dopo uno viene
  promosso a rischio quando il suo segnale si verifica; la validazione ne
  accetta e ne respinge; registro, classifica e radar non cambiano per le voci
  in osservazione.
- **Impegno**: medio, circa 2-3 giorni con collaudo e documentazione
  (struttura del workbook nuova).

### P9. Temi da verificare indicati dall'analista (proposta del 06/10/2026)

- **Perche'**: oggi l'unico modo di chiedere ad A1 di verificare un rischio
  preciso ("verifica nei documenti questo rischio e, se le fonti lo
  sostengono, censiscilo") e' scriverlo nel messaggio della chat: la richiesta
  non resta tracciata, nessuno controlla che A1 l'abbia esaminata e va
  riscritta a ogni ciclo.
- **Cosa fare**: un file `temi_da_verificare.md` nella library Kernel (un tema
  per riga, con chi lo chiede e perche'); `input_a1.py` lo aggiunge
  all'allegato `Input_A1` come quarta parte, con l'istruzione: per ogni tema,
  rischio nuovo se c'e' almeno una fonte specifica, altrimenti riga nella
  sintesi "verificato senza evidenza". Il prompt di A1 non cambia (37
  caratteri liberi): l'istruzione sta nell'allegato. Un controllo dello script
  (Osservazione) segnala un tema che non compare ne' fra i rischi ne' nella
  sintesi.
- **Legami**: vicina a P8 (lista di osservazione); si puo' fare prima, perche'
  non tocca il registro.
- **Fatto quando**: allegato con la parte 4, controllo nel collaudo, guida
  (sezione 2, punto 4).
- **Impegno**: circa mezza giornata.

## Quantificazione per i rischi piu' rilevanti

### Q1. Nota di metodo e prototipo di probabilita' e impatto quantitativi

- **Perche'**: per i 3-5 rischi piu' rilevanti (AGIRE ORA o primi del
  composito) una stima in euro e in frequenza annua per una grande banca
  sistemica europea da' un ancoraggio alla scala 1-5 e un confronto per il
  comitato. Serve a **calibrare e sfidare** gli score, non a sostituirli. E'
  collegata alla regola 7 della rubrica (fatti e stime separati, D-36) e alla
  decisione aperta A-12. Dopo S1 (30/09) la Probabilita ha descrittori di
  plausibilita' (D-52), non di frequenza: una frequenza stimata in Q1 servira'
  a tarare quei descrittori, non a sostituirli.
- **Basi possibili**:
  - A. **Analisi di scenario** (standard del rischio operativo, oggi ICAAP e
    Pillar 2): 2-3 scenari per rischio (tipico, severo, estremo); esperti
    tarati, con Delphi e un challenger, stimano frequenza annua e perdita
    "1 volta in 10 anni" e "1 volta in 40 anni"; frequenza Poisson, severita'
    lognormale dai due percentili, Monte Carlo: perdita attesa, P99, P99,9.
  - B. **Dati esterni riscalati sulla Banca**: ORX (loss data, scenario
    library); scalatura per dimensione (esponente di circa 0,2-0,3 su reddito
    o Business Indicator); sanzioni pubbliche (BCE, FCA, SEC, GDPR fino al 4%
    del fatturato); IMF GFSR aprile 2024, capitolo cyber (code estreme); IBM
    Cost of a Data Breach, settore finanziario; ECB Cyber Resilience Stress
    Test 2024; incidenti gravi DORA aggregati dalle ESA; metodologia dello
    stress test EBA per condotta e altro rischio operativo.
  - C. **Frequenze di base dai peer**: eventi fra G-SIB e banche significative
    / anni-banca osservati, corretti per il Gap_Controlli; per i rischi senza
    storia (AI, post-quantum) analoghi di altri settori e quasi-incidenti.
  - D. **Modelli per cause**: FAIR per cyber, AI e terze parti (frequenza
    della minaccia x vulnerabilita' x perdita primaria e secondaria); reti
    bayesiane che collegano driver, controlli e perdita, dove le notizie
    aggiornano la probabilita' (nel ciclo di valutazione, non fra un ciclo e
    l'altro: D-41).
  - E. **Ancoraggio**: impatto in % del CET1 o dell'utile operativo e giorni
    di interruzione di una funzione essenziale; mappatura sulle fasce di
    Impatto e Probabilita' (i descrittori della Probabilita' sono gia' di
    frequenza); uso per Pillar 2 e ICAAP, non per Pillar 1 (SMA con CRR3,
    ILM = 1 in UE: le perdite interne non muovono il requisito); reverse
    stress test ("quale scenario costa l'X% del CET1?").
- **Principio**: i numeri li danno gli esperti; A1 porta evidenze e analoghi,
  non cifre; il calcolo lo fa il codice (principio 1). Se il valore
  quantitativo e lo score 1-5 divergono di piu' di una fascia, decide il
  validatore.
- **Cosa fare**: una nota di metodo di una pagina da far approvare alla
  funzione di rischio; poi un prototipo su 1-2 rischi della demo (cyber, terze
  parti) con Monte Carlo nello script, risultato nelle schede accanto agli
  score.
- **Fatto quando**: la nota e' approvata e il prototipo produce perdita
  attesa, P99 e P99,9 con la fascia di Impatto corrispondente per i rischi di
  prova.
- **Impegno**: nota 1-2 giorni; prototipo 3-5 giorni; la raccolta delle stime
  degli esperti e' lavoro della Banca.

## Grafici del registro

### Stato attuale (25/09/2026, struttura 2026-09-25c)

Tutti i grafici del registro nascono in `03_Excel/genera_dashboard.py`,
ciascuno dentro la funzione che costruisce il suo foglio; quelli delle schede
in `07_Senza_Studio/schede.py`:

| Grafico | Funzione |
|---|---|
| Storico, linee su 8 cicli | `foglio_storico` |
| Delta, barre ordinate con serie dinamiche (in aumento, in diminuzione, invariato) | `foglio_delta` |
| Barre delle notizie per event type e barre settimanali | `foglio_notizie` |
| Radar di Mosca, dispersione con cerchi (grande nel Radar_Mosca, piccolo nel Quadro) | `grafico_radar` (con `_punti`, `_etichetta_serie`, `ANELLI`, `PUNTI_ANELLO`, `VALORI_PXI`, `NOMI_SETTORI`) e `trasparenza` |
| Storia di un KRI | `foglio_indicatori` |
| Classifica (barre ordinate, colore = urgenza) e lente di Mosca (colonne X + Y e rombo Z, ordinata per margine) | `foglio_classifica` (con `_serie_dinamica`) |
| Andamento di un rischio negli ultimi trimestri | `schede.scrivi_file_schede` |

Dal 25/09 c'e' uno stile comune: colori in costanti (`BLU_NOTTE`, `ROSSO`,
`AMBRA`, `SCALA_DIM`...), `stile_grafico()`, `etichette_valore()`,
`titolo_da_cella()` (titoli che dicono il messaggio), `chip_urgenza()`,
`legenda()`. Dimensioni e posizioni restano dentro ogni funzione.

Cosa e' documentato: il **cosa** e il **perche'** (manuale del template;
rubrica, sezione 8, per il radar di Mosca). Non il **come ritoccare**.

Cosa e' collaudato: i **dati** dei grafici (numero di raggi del radar,
margine di Mosca contro un calcolo indipendente). Non l'**aspetto**, che si
controlla a occhio esportando le immagini.

### G1. Isolare i parametri dei grafici

- **Perche'**: oggi per cambiare un colore o una dimensione bisogna trovare il
  punto giusto dentro una funzione lunga, fra formule che non vanno toccate.
- **Cosa fare**: una tabella `GRAFICI` all'inizio di `genera_dashboard.py`,
  una voce per grafico: foglio, ancoraggio, larghezza e altezza, titolo,
  posizione della legenda, colori delle serie, scala degli assi, scala delle
  bolle, testi degli anelli. Le funzioni dei fogli leggono da li'. Nessun
  cambiamento visibile nel template generato.
- **Fatto quando**: il template rigenerato e' identico a prima (stessi
  grafici, stesse immagini esportate) e ogni parametro visivo e' nella tabella.
- **Impegno**: basso, circa mezza giornata compreso il collaudo.

### G2. Documentare come modificare ed estendere i grafici

- **Perche'**: chi mantiene il pacchetto deve poter ritoccare un grafico senza
  conoscerne la storia, ed evitare le trappole gia' trovate.
- **Cosa fare**: un documento `03_Excel/grafici_come_modificarli.md` con:
  - i tre livelli su cui si agisce: **cosa mostra** (formule nelle celle e
    celle gialle di Parametri, senza codice), **quali dati entrano** (serie e
    intervalli, nel generatore), **come appare** (colori, dimensioni,
    etichette, nel generatore o a mano in Excel);
  - ricette: cambiare colori e dimensioni; cambiare la scala di un asse;
    aggiungere una serie; aggiungere un grafico nuovo a un foglio esistente;
    rendere dinamico un intervallo con un nome OFFSET (`[0]!nome` nel file del
    grafico);
  - le trappole gia' incontrate: `overlay` di titolo e legenda, assi marcati
    come eliminati da openpyxl, `varyColors` sui radar a una serie, linee
    smussate che inventano valori, dati in colonne nascoste non disegnati
    senza `visible_cells_only = False`, #N/D invece di zero per i valori
    mancanti, anagrafica senza righe vuote in mezzo per il radar dinamico;
  - come verificare: rigenerare, esportare le immagini (G3), lanciare il
    collaudo.
- **Fatto quando**: un manutentore che non ha scritto il generatore cambia
  il colore di una serie e aggiunge un grafico seguendo solo il documento.
- **Impegno**: basso. Conviene farlo dopo G1, cosi' le ricette puntano alla
  tabella dei parametri.

### G3. Script di anteprima dei grafici

- **Perche'**: oggi per vedere l'effetto di una modifica bisogna lanciare la
  demo intera o uno script improvvisato.
- **Cosa fare**: `03_Excel/anteprima_grafici.py [file.xlsx]` che apre il file
  in Excel (sola lettura), ricalcola ed esporta in PNG tutti i grafici in una
  cartella, compresa la storia di un KRI (Indicatori) a scelta. Default: il template appena generato.
- **Fatto quando**: un comando produce una cartella di immagini, una per
  grafico, senza modificare il file.
- **Impegno**: basso.

### G4. Migrazione del registro vivo su un template nuovo — FATTA il 25/09/2026

Realizzata come comando `aggiorna-registro` di `esegui_ciclo_locale.py`
(decisione D-34), con il controllo di versione `versioneTemplate` e il passo 11
della catena di collaudo sul registro del template del 23/09. Differenze
rispetto alla proposta qui sotto: il registro nuovo prende il posto del
vecchio (stesso nome e percorso, vecchio in `Backup`); i pesi non si copiano
(quelli nuovi vengono da una decisione); la verifica confronta anche la
baseline. Per alzare una capacita' (MAX_RISCHI...) basta ora rigenerare il
template, alzare la versione e lanciare `aggiorna-registro`. Testo originale
della proposta, per memoria:

- **Perche'**: e' il punto debole vero. Rigenerare il template cambia i
  grafici (e le formule) **solo nei registri nuovi**: il registro in uso
  conserva quelli con cui e' nato. Oggi le alternative sono ritoccare a mano
  il registro vivo (la modifica non torna nel generatore e si perde al
  prossimo template) o ricopiare i dati a mano. Serve anche per le
  **capacita'** del template (15 rischi, 60 KRI correnti, 150 KRI nella
  storia): lo script avverte quando restano 2 posti in anagrafica e si ferma
  prima di superare una capacita', ma per alzarla oggi c'e' solo la via
  manuale. La demo e' gia' a 13 rischi su 15.
- **Cosa fare**: `07_Senza_Studio/migra_registro.py --da vecchio.xlsx --a
  template_nuovo.xlsx --uscita nuovo_registro.xlsx`, che copia:
  - le righe di tutte le tabelle dati e di Validazione, per nome di colonna
    (non per posizione), lasciando alle colonne formula le formule nuove;
  - le celle di input di Parametri (pesi, soglie, parametri dell'urgenza,
    ciclo e settimana correnti) e l'anagrafica.

  Poi verifica: stesso numero di righe per tabella, zero errori di formula,
  copertura del ciclo uguale, stesse viste (score, segnali, KRI correnti,
  margini di Mosca) prima e dopo. Si ferma se una colonna del vecchio registro
  non esiste nel nuovo template.
- **Fatto quando**: il collaudo migra il registro alla fine della catena di
  prova su un template rigenerato e trova le stesse viste; la guida passo
  passo ha una sezione "Aggiornare il registro a un template nuovo".
- **Impegno**: medio, circa una giornata compreso il collaudo.

### G5. Difetti estetici noti

| Dove | Difetto | Idea di soluzione |
|---|---|---|
| Storico | voci vuote in legenda per le righe libere dell'anagrafica (una serie per riga) | nascondere la legenda ed etichettare l'ultimo punto di ogni linea con l'ID, oppure serie dinamiche con nome definito per riga |
| ~~Radar della Dashboard~~ | tolto il 25/09 (D-39): il Registro e la Matrice lo sostituiscono | — |
| Radar di Mosca | con molti rischi nello stesso settore e margine simile i cerchi possono ancora toccarsi (oggi: raggio = margine + 2, spaziatura uniforme nel settore, riempimento semitrasparente dal 25/09). Dal 30/09 (D-55: un rischio per meccanismo, 20 rischi) e' piu' probabile, soprattutto su L1-02 e L1-06 | spostamento radiale alternato per i rischi adiacenti |
| Quadro, matrice piccola | con sei o piu' rischi nella stessa cella i numeri vanno su tre righe e l'ultima puo' essere tagliata | mostrare "n rischi" oltre una soglia, con rimando alla Matrice |
| Quadro e Delta | l'altezza delle righe con testi calcolati la stima lo script (`adatta_altezze`) contando i caratteri: con testi molto lunghi una riga puo' restare un po' alta o bassa | misurare in Excel (AutoFit su una cella di appoggio non unita della stessa larghezza) |
| Radar di Mosca | ~~colore dell'urgenza: "Agire entro l'anno" in rosso invece che ambra~~ corretto il 25/09 (la regola `LEFT(L5,5)="AGIRE"` valeva anche per "Agire": il confronto di Excel ignora le maiuscole) | — |
| Radar di Mosca | ~~un solo colore per tutti i rischi~~ risolto il 25/09 (D-35, bordo giallo per i temi del supervisore) e il 01/10 (D-63): colore = livello di allerta, ◆ per i temi del supervisore | — |

Ordine consigliato: G1, G3, G2 (la documentazione si scrive meglio quando i
parametri sono isolati e l'anteprima esiste), poi G4, poi i difetti di G5.

### G6. Report intermedio leggibile: rischi di A1 accanto alle osservazioni di A5

- **Ridimensionata da S1 (30/09)**: tutti i rilievi di A5 e dei controlli
  finiscono ora sui rischi nel registro (colonna Rilievi, D-56) e un rilievo di
  giudizio di A5 si puo' superare e decidere in validazione. Resta utile per
  leggere A1 e A5 affiancati PRIMA della scrittura.
- **Perche'**: nato dal collaudo del primo ciclo (29/09/2026). Fra A1 e
  `trimestrale` oggi l'unico modo di leggere cosa non va e' aprire due JSON
  (l'output di A1 e `Esito_controlli_<ciclo>.json`) e abbinare a mano ogni
  `id_rischio` fra i due — lento, ed espone a errori di trascrizione se si
  riassume a voce o si incolla solo un pezzo nella chat di correzione con A1
  (si rischia di perdere fedelta' rispetto a quello che A5 ha scritto
  davvero). Nel primo ciclo reale sono serviti 7 giri A1<->A5 prima di
  convergere: un report leggibile fin dal primo giro avrebbe reso ogni giro
  piu' veloce da capire, e avrebbe permesso al validatore di intervenire lui
  stesso sui punti piu' semplici (es. abbassare un punteggio palesemente
  troppo alto) invece di rimandare tutto ad A1.
- **Cosa fare**: un comando (es. `esegui_ciclo_locale.py report-intermedio
  --payload A1_<ciclo>.json --challenger Esito_controlli_<ciclo>.json`) che
  produce un Excel (o foglio dentro il workbook di prova) con una riga o un
  blocco per rischio: i dati che A1 ha proposto (event type, driver, le
  quattro dimensioni, anni di adeguamento, razionale, fonti con rilevanza, azioni, KRI) **accanto** ai
  rilievi di A5 che lo riguardano (controllo, gravita', descrizione),
  raggruppati per `id_rischio`; i rilievi con `id_rischio: null` (sul ciclo)
  a parte. Nessuna scrittura nel registro: e' un allegato di lavoro, non
  sostituisce la validazione ne' il comando `trimestrale`. Punto aperto da
  decidere insieme, non tecnico: se il validatore puo' **modificare i valori
  in questo report** e farli rientrare come correzione (e con quale traccia,
  per restare coerenti col principio "nessuna valutazione vale senza una
  persona che la valida, con motivo e autore conservati"), o se resta solo
  uno strumento di lettura per capire cosa scrivere nel messaggio di
  correzione ad A1.
- **Fatto quando**: dopo un ciclo con FERMATO, il report si genera con un
  comando solo e mostra ogni rischio con le osservazioni di A5 a fianco,
  senza dover aprire i due JSON.
- **Impegno**: basso (formattazione, non giudizio: i dati esistono gia' in
  entrambi i file).

## In riserva (non pianificate)

Non sono voci di lavoro. Si riprendono solo se cambia la condizione indicata.

| Voce | Cosa e' | Quando riprenderla |
|---|---|---|
| Piano 07, Power Query senza Python (`Analisi_Architettura/Archivio/07`) | controlli e consolidamento in Excel con Power Query; la "scrittura" diventa lo spostamento dei file in `Dati/Validati/`; Python solo al manutentore. Era la voce AR1, chiusa da D-43 | se la Banca vietasse Python sul PC |
| Variante CS-2, tutto nel cloud (piano 10, 10.11; `Analisi_Architettura/Archivio/06`) | motore riscritto in Office Scripts, stato in Liste SharePoint, report con Power Query: nessun PC in esercizio | solo dopo la CS-1 (AU6), se la Banca vuole un esercizio senza PC; circa 4 settimane in piu' |
