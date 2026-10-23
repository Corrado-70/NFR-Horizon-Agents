# PROMPT MASTER — Sistema di agenti NFR Emerging Risk (rigenerazione completa)

> Da incollare come richiesta iniziale a Claude Code, in una cartella vuota.
> Rigenera l'intero pacchetto in un colpo, con i controlli di coerenza
> incorporati dal disegno invece che aggiunti dopo.
>
> **Versione del 23/09/2026, aggiornata il 24, 25, 29, 30/09, 01, 02, 05, 06 e 07/10**
> (ultimo aggiornamento, 08/10 sera: **registro unico** (D-79, sostituisce la lista di osservazione della D-73):
> un solo registro di rischi `NFR-nn` con la stessa rubrica; colonna **Stato** del RiskRegister (Radar, Radar, in
> uscita, Osservazione, Dismesso) con Motivo_Stato, Movimento (Entrato / Uscito), Decisione_Stato del validatore,
> Orizzonte_Anni e Segnale_Avvicinamento di A1, formula Ordine_Osservazione; regola in un solo modulo
> `07_Senza_Studio/radar.py` (Prossimita >= 2 e Probabilita >= 2, capienza 15 fino a 20 per score, eccezioni AGIRE
> ORA, supervisore, decisione Radar; decisione Osservazione esclude; uscita dopo due cicli "in uscita"; massimo 20
> in osservazione); anagrafica = il radar; KRI e azioni solo per il radar, A1 li scrive subito per chi entra;
> `tblOsservazione`, `OSS-nn`, `voce_osservazione` e `segnali_osservazione` spariscono; `riapri` senza `--voci`;
> `aggiorna-registro` converte le voci in rischi in osservazione; struttura **2026-10-09**; trappole 103-107.
> Prima, 08/10: **documenti di riferimento in `04_Riferimenti`** (DECISIONI,
> SharePoint, workflow, governance, `Prove/`; D-78) e **collaudo in parallelo** (dieci gruppi in tre processi,
> `--mirato`); A8 rilegge i KRI dei rischi che riscrive (D-77, punto 4); analisi della scala unica in
> `Analisi_Architettura/13_Scala_unica.md` (TODO P10); trappola 102. Prima, 07/10 notte: **A8 Evento critico** (D-77): agente del ciclo
> straordinario, stesso allegato, formato e comandi di A1; legge per intero i
> documenti dell'evento, rivaluta i rischi indicati, censisce i nuovi e scrive il
> campo facoltativo `analisi_evento` (evento, catena causale, rischi toccati e non
> toccati, documenti, limiti: nella colonna Straordinario di Sintesi_Cicli il fatto,
> in `Ciclo.txt` di A7 tutto; controlli solo Osservazioni); `baseline --straordinario`
> senza `--rischi` = solo censimento (C1 Bloccante se nessun rischio nuovo); demo con
> riapertura e straordinario; trappola 101. Prima, 07/10 notte: **tassonomia interna della Banca** (D-74): le
> nove categorie in perimetro (9.1 Condotta, 9.4 Legale, 9.5 Fiscale, 9.6 Tecnologico,
> 9.7 Sicurezza informatica, 9.8 Sicurezza fisica, 9.9 Terze parti, 9.11 Employer,
> 9.13 Processo, da `Tassonomia dei Rischi.csv`, dal 09/10 in `04_Riferimenti`) sostituiscono i sette
> event type di Basilea ovunque (radar a nove settori, nove intensita' delle notizie,
> colonne `Imp_9_n`); A1 riclassifica i codici di Basilea della baseline
> (Osservazione C1) o segna FP i rischi fuori perimetro (da motivare, poi
> `dismetti`); struttura **2026-10-08b**. **Ciclo straordinario** `AAAAQn-Sk`
> (D-75): `baseline --straordinario` con decisore e motivo, A1 rivaluta solo i
> rischi indicati, `trimestrale` riporta gli altri gia' validati
> (`Periodo_Valutazione`, da cui la Y di Mosca), lo straordinario conta come ciclo
> per la regola del punto, periodi delle viste scritti dallo script
> (`dataRiferimento` nuova), proposta di A3 (`proposta_straordinario`) e di A4.
> **A3 collega le notizie alle voci in osservazione** (D-73, punto 6:
> `voce_osservazione`, `segnali_osservazione`, nella baseline come `notizie_a3` e
> `segnali_a3`). **Un documento solo per uso e avvio**: il piano di deploy e' la
> sezione "Avvio del progetto" della guida (`Piano_deploy.md` non c'e' piu').
> **Analisi architetturale a due opzioni** (`Analisi_Architettura/12_Due_opzioni.md`:
> app Python unica, Copilot Studio nei vincoli; **dal 09/10 tre strade**,
> `14_Tre_strade.md`: A, CS-1, CS-2 senza Python sul PC, obiettivo dell'utente; **l'11/10 la CS-2
> approfondita**, `15_CS2_approfondita.md`: variante V2 "Python decide, Excel esegue", trappola 110; **il 14/10 la variante V4**, `16_Report_HTML.md`: report HTML generato da Python al posto delle viste di Excel, anteprima in `Analisi_Architettura/16_Anteprima_HTML/`, decisione aperta A-16, trappola 111; il pacchetto non cambia finche' A-16 non e' decisa; **il 19/10 il contraddittorio "decimo uomo"**, `17_Decimo_uomo.md`: agente separato A9 proposto, decisione aperta A-17, prova K15; il pacchetto non cambia finche' A-17 non e' decisa; nella stessa analisi, 17.10, **ancoraggio e asimmetrie**: fatti il comando `diagnosi` e gli anni di adeguamento dei rischi in osservazione con Impatto 4-5, D-80, trappola 112, e l'esposizione "non nota" decisa dal validatore, D-81; **il 23/10 due rami e la strada A su `main`** (D-83, chiude A-15 e A-16): su `main` agenti in Agent Builder e un'app Python di orchestrazione, per piu' analisti, a tappe M1-M4; tappa M1 fatta: lucchetto, copia di lavoro del registro, Salvataggio automatico spento, `sblocca`, AU7 (baseline ad A3 e A4 come allegato), report rigenerato da `valida`, prompt archiviati, PDF delle schede, traccia della riapertura; poi la tappa M2, l'app: `NFR.cmd`, `app_nfr.py` (tkinter), `flussi.py`, `stato.py`, `ingresso.py`, `appunti.py`, `esecutore.py`; trappole 122-129 (le 113-121 sono del ramo `copilot-studio-pieno`, D-82); niente V4: il report HTML sara' una seconda uscita di `report`). Trappole 93-98. Prima, 07/10 sera:
> **lista di osservazione** (D-73, **sostituita l'08/10 dal registro unico, D-79**: il testo resta come storia): i fenomeni
> con un meccanismo di perdita ma lontani o solo teorici diventano voci `OSS-nn`
> della tabella storica `tblOsservazione` (foglio dati Lista_Osservazione), con
> impatto potenziale 1-5, orizzonte in anni, plausibilita' teorica / possibile / in
> crescita e segnale di avvicinamento, senza KRI, azioni ne' score; A1 le propone
> nel campo facoltativo `osservazione` (solo voci nuove e con evidenza nuova,
> istruzioni nella guida di scrittura), lo script riporta le altre invariate, le
> controlla (`controlla_osservazione`), le mette nella sezione nuova della griglia
> di validazione, nella baseline, nel foglio di lavoro Osservazione, nella pagina
> del report **Fenomeni** (prima della Metodologia) e in `Ciclo.txt` di A7; al
> massimo 30 voci; struttura **2026-10-07b**; trappole 90-92. Prima, 07/10:
> **A7 Assistente del registro** (D-72), agente
> solo interattivo che spiega in chat il perche' delle valutazioni distinguendo
> registrato, calcolato e sua lettura; knowledge nella cartella
> `Kernel/Spiegazioni` (`Ciclo.txt` e `Rischio_01..20.txt`, uno per posto
> dell'anagrafica, nomi fissi),
> scritta da `07_Senza_Studio/spiegazioni.py` alla fine di `trimestrale`,
> `valida`, `dismetti`; campo facoltativo `fenomeni_non_censiti` nello schema di
> A1 (istruzioni nella guida di scrittura); **Note dell'analista** nel Quadro
> (`quadroNote`, archiviate in `tblSintesi.Note_Analista` al ciclo dopo);
> struttura **2026-10-07**; trappole 87-89. E' la fase 1 del piano degli agenti
> nuovi (TODO, "Agenti nuovi"). Prima, 06/10: **A5 facoltativo e segnalazioni in validazione**
> (D-71): lo script ferma solo i difetti di integrita' (schema, C1, C2, C7,
> identificativi dei KRI) e scrive il messaggio per A1; C3, le date di C5, la
> coppia e le soglie dei KRI e i Bloccanti di A5 diventano "Da motivare":
> colonna Rilievi del RiskRegister e nuova colonna **Segnalazioni dei
> controlli** della griglia (P), ⚑ e Motivazione obbligatoria; `valida` non
> accetta salti di piu' di un punto ne' soglie invertite anche sulle proposte
> accettate; `--procedi-con-rilievi` inutile; struttura **2026-10-06**;
> trappole 85-86. Prima, 05/10: **prove sul PC della Banca e prova di Copilot
> Studio** (D-70): le regole del precontrollo in un modulo senza Excel
> (`07_Senza_Studio/precontrollo.py`) con l'**impronta** dell'output di A1;
> cartella `09_Copilot_Studio` con lo **script unico** composto da
> `prepara_kit.py` dai moduli del pacchetto, la **skill** `precontrollo-nfr`
> (SKILL.md) e il protocollo della prova in due opzioni del codice (Code
> interpreter dell'esperienza standard, skill nel sandbox della nuova
> esperienza); `04_Riferimenti/Prove/Prova_senza_Copilot_Studio.md` (installazione e ciclo
> su un registro di prova); trappole 81-84. Prima, 02/10 sera: **meno giri fra A1 e A5** (D-69): i nove
> controlli in un solo file del kernel (`controlli_A5.md`) da cui si compongono
> le istruzioni di A5 e l'**allegato di A1** `Input_A1_<ciclo>.txt` (baseline,
> controlli, **guida di scrittura** con un esempio di forma), scritto dallo script
> con la baseline; comando **`precontrollo`** prima di A5, senza Excel, con il
> messaggio di correzione per A1; azioni nuove (C8 segnala un'azione uguale a
> un'azione aperta); trappole 78-80. Prima, 02/10 pomeriggio: **schede dei rischi con il perche'
> di ogni numero** (D-68): A1 scrive il razionale in parti (RISCHIO, IMPATTO,
> PROBABILITA, PROSSIMITA, VELOCITY, ADEGUAMENTO) e l'EFFETTO di azioni e KRI;
> la scheda mette il Razionale (il fenomeno) dopo il rischio, il perche' accanto
> a ogni valore e "Perche'" / "Effetto atteso" sotto azioni e KRI; struttura del
> workbook invariata; trappole 75-77. Prima, 02/10 mattina: **validazione in una griglia, una riga per
> rischio, KRI, azione e notizia** (D-67): celle gialle gia' compilate con le
> proposte, Score e Margine di Mosca calcolati mentre si scrive, storico campo
> per campo nel foglio dati Storico_Validazioni, comando `griglia`,
> `--accetta-il-resto` superato, `aggiorna-registro` che porta le righe in
> sospeso nella griglia; versione **2026-10-02**; trappole 70-74. Prima, 01/10:
> **livello di allerta, KRI per tipo, esposizione nella
> Probabilita**, D-63...D-65, dai suggerimenti di una proposta esterna:
> livello Attivazione/Attenzione/Monitoraggio calcolato dal Radar_Mosca e
> mostrato come colore dei cerchi, senza colonne nuove; due KRI per rischio,
> uno di Esposizione e uno di Evoluzione (campo `tipo`); Probabilita 4-5 solo
> se la Banca e' esposta; A1 ragiona analizzando nel dettaglio ogni fonte;
> Z a meta' fascia (D-59 rivista); versione 2026-09-30c; trappole 63-67. Poi,
> sempre il 01/10: **sintesi settimanale di A3 nel registro** (D-66, foglio dati
> Sintesi_Settimane e riquadro nel foglio Notizie; versione 2026-10-01) e
> collaudo delle notizie validate nelle viste (passo 3b); trappole 68-69.
> Prima, 30/09 sera: **revisione della rubrica del responsabile**,
> D-57...D-62: Severity si chiama Impatto; la Confidence del rischio e'
> sostituita dalla rilevanza 1-3 di ogni fonte; Z di Mosca = inizio della
> fascia della Prossimita; anni di adeguamento stimati da A1 e validati;
> descrittori riscritti, deroga della Prossimita per fenomeni ad altissimo
> impatto, soglie 2 e 0,30; comando `report`; Registro e Parametri stampabili
> in orizzontale; versione 2026-09-30b; trappole 59-62. Prima, 30/09 mattina:
> **semplificazione dello scoring di A1** dopo il primo
> ciclo reale, D-49...D-56, `Analisi_Architettura/Archivio/11`: Gap_Controlli fuori dal
> modello e presidio dei controlli come giudizio della Banca, Velocity
> facoltativa con pesi ridistribuiti, esito e "da/a" calcolati dallo script,
> Probabilita di plausibilita', KRI da 1 a 3 con soglie facoltative, azioni
> senza dimensione, un rischio per meccanismo di perdita senza event type
> obbligatori, opzione `--procedi-con-rilievi`, colonna Rilievi, 20 rischi,
> versione 2026-09-30; trappole 51-58. Prima, 29/09: errore "Template non trovato" con rimedio esplicito,
> sezione 0 della guida riscritta come percorso unico di prima installazione
> (amministratore, manutentore/agenti, PC analista, primo registro), elenco
> `PAROLE_FUNZIONE` di C8 ampliato (owner reali fermati da un falso
> positivo); Input di A1 corretto su `fonti[].tipo` (Interna seguiva la
> cartella, non il contenuto) e FNT-35 rinominata `Fonti_Esterne`, scope
> allargato; trappole 47-50. Prima, 25/09 sera: **registro e report in un solo file ridisegnato**
> (D-39: Quadro, Registro, Matrice, Piano_azioni, Dizionario, fascia del titolo,
> tabelle dati dalla riga 5), **agente A6 e file delle schede** (D-40),
> commento di A1 "MESSAGGIO: ... DECISIONI: ...", versione 2026-09-25c;
> trappole 42-46. Prima, 25/09 pomeriggio: guida in testa a ogni foglio,
> attenzione del supervisore (bordo giallo), regola dei numeri nel razionale,
> sette rischi di riferimento, versione 2026-09-25b, trappole 34-41; e: report
> al comitato, D-19 in vigore, anni di adeguamento, `aggiorna-registro`;
> trappole 25-33). Riscritta dopo la rigenerazione del 23/09 e le
> richieste successive dell'utente: incorpora le scelte gia' fatte, gli
> scostamenti motivati dalla versione precedente (conservata in
> `PROMPT_MASTER_rigenerazione_precedente.md`) e le trappole trovate
> collaudando con Excel vero. Il pacchetto di riferimento prodotto con questo
> prompt e' `NFR_Emerging_Risk_Agents/`; lo stato e le decisioni aperte sono in
> `HANDOFF_stato_e_prossimi_passi.md`.
>
> Cosa questo prompt PUO' far produrre: tutti gli artefatti (kernel, elenco
> fonti, prompt, schemi, generatore Excel, script di campo, struttura
> SharePoint, workflow, governance, guida per l'utente), una suite di collaudo
> che esegue la catena con lo strumento vero ed Excel desktop, una demo. Cosa
> NON puo': creare, pubblicare o eseguire gli agenti nel tenant della Banca.
> Il collaudo verifica gli artefatti prima del deploy; non lo sostituisce.

---

## RUOLO E OBIETTIVO

Sei un ingegnere che progetta un sistema di agenti Microsoft 365 Copilot per il
monitoraggio dei rischi non finanziari (NFR) emergenti di una banca
significativa dell'area euro. Produci un pacchetto di deploy completo,
internamente coerente e collaudato. Il pacchetto viene consegnato a chi lo
configurera' nel tenant. Il tuo output sono file, una suite di collaudo che li
verifica eseguendoli, e una guida che un utente non esperto sappia seguire.

Lavora in italiano. Ogni documento destinato agli utenti e' in italiano.

## SCELTE GIA' FATTE DALL'UTENTE (non richiederle)

- **Ambiente**: solo Microsoft 365 Copilot, **senza Copilot Studio ne' Power
  Automate**. Gli agenti vanno in **Agent Builder**; la parte deterministica e'
  uno script Python sul PC dell'analista. La documentazione del modulo con
  Power Automate resta (workflow W0-W3), ma riusa lo stesso script.
  Dal 28/09 Copilot Studio e' **disponibile** nel tenant (D-44), ma **usarlo
  non e' deciso** (A-15, TODO AU4). Finche' A-15 e' aperta vale questa
  scelta. **Python resta il motore** in ogni caso (D-43).
- **Solo Python**, niente TypeScript/Office Script. Lo script scrive nel
  workbook tramite **Excel desktop via COM** (`pywin32`), non con openpyxl:
  solo il motore vero di Excel ricalcola le formule e trova gli errori.
  openpyxl serve solo a generare il template e nei test di lettura.
- **Semplicita' di gestione e di modifica** prima di tutto: una regola vive in
  un solo posto; nessuna copia di codice da tenere sincronizzata.
- **Nessuna notifica Outlook**: ogni esecuzione produce un **Excel di output**
  con nome proprio, archiviato.
- **Tassonomia**: dal 07/10/2026 (D-74) la **tassonomia interna della Banca**, solo
  le nove categorie marcate SI nel file della Banca; sostituisce del tutto i sette
  event type di Basilea (prima classificazione principale, D-04).
- Lo storico dei KRI vive nel workbook; le fonti delle notizie arrivano da tre
  canali insieme (feed, siti pubblici, file sulla share); le valutazioni degli
  agenti sono **validate da una persona** con traccia di ogni rettifica.
- **Si parte dal registro vuoto** (24/09): nessun trimestre gia' valutato a mano
  e' richiesto, ne' per l'avvio ne' per il collaudo in ambiente. Il primo ciclo
  di A1 individua i rischi da zero dalla documentazione e li propone tutti come
  "Nuovo"; il metro di qualita' e' il doppio run piu' la validazione umana.
- **Documentazione sempre allineata** (24/09): ogni modifica aggiorna nello
  stesso momento questo PROMPT_MASTER e tutti i documenti che la citano.
  Lo **zip** del pacchetto si crea **solo su richiesta dell'utente** (25/09
  sera), non a ogni modifica.
- **Registro delle decisioni** `04_Riferimenti/DECISIONI.md` (24/09, aggiornato il
  25/09, 26/09, 28/09, 29/09, 30/09 e 01/10): 66 decisioni prese (D-01..D-66; D-41 e D-42 del 26/09:
  principi confermati con l'eccezione del ciclo straordinario su segnale
  critico, e rischi separati ma collegati, entrambe da implementare; D-43
  Python resta il motore e il piano 07 va in riserva; D-44 Copilot Studio e
  Power Query disponibili, chiude A-05; D-45..D-48 dal primo ciclo reale del
  29/09: settima library `Analisi_Esterne`, confidence 4-5 senza fonte interna,
  pavimento di Gap_Controlli (sostituito da D-49), Prossimita 4-5 solo con un
  caso nominato; **D-49..D-56 del 30/09**, la semplificazione dello scoring,
  elencate sotto) e 4 aperte (A-15 strada A o variante
  CS-1 con Copilot Studio, TODO AU4; A-11 variante 04_Riferimenti/workflow.md, con A-15; A-12
  revisione dopo il primo ciclo; A-13 revisione annuale delle fonti; A-14
  ridisegno del registro chiusa da D-39 e D-40), con data, chi, perche' e stato; cancelli G0, G1
  (provvisorio) e G2 (con condizione) firmati il 24/09. E' la
  fonte delle scelte della Banca: una rigenerazione lo **conserva cosi' com'e'**
  (non lo riscrive) e applica le decisioni "In vigore", "Provvisoria" e "Da
  implementare". Quelle che toccano il pacchetto:
  - D-07 partenza da registro vuoto; D-08 un rischio non si respinge (si
    rettifica o si dismette); D-09 ricerca file in A1/A3/A4, non in A5; D-11
    capability spente; D-12 `pypac`;
  - D-13 **una sola persona** e' responsabile, manutentore, analista e
    validatore; D-30 il limite (validazione non indipendente) e' **accettato
    nel pilota** e va dichiarato nel report e in `04_Riferimenti/controlli_e_model_risk.md`;
  - D-14 il registro **affianca** il processo di rischio operativo (pilota);
  - D-23 model risk: **non rilevante**, nessun requisito di convalida
    ulteriore; D-24 parere compliance/DPO positivo (Agent Builder e copie in
    "Microsoft Copilot Chat Files"; non copre gli agenti Office, che non si
    usano); D-25 Agent Builder attivo e licenze assegnate; D-26 Python,
    pywin32 e pypac ammessi sul PC;
  - D-15/D-16/D-27/D-28/D-29 fonti: **tutte approvate tranne FNT-19**,
    esclusa perche' fuori perimetro (vedi "Elenco fonti");
  - D-31 (sostituita da D-32) e **D-32 report al comitato**: PDF dei sei fogli
    di report dell'Excel validato, di seguito nel workbook; dal 25/09 sera
    (**D-39**) sono Quadro (con il commento di A1, cioe' la `sintesi`, e i
    rischi segnalati), Classifica con la lente di Mosca, Radar_Mosca, Matrice,
    Delta, Metodologia (vedi "Il workbook"), piu' il file delle schede (**D-40**,
    agente A6);
  - **D-33 anni di adeguamento** per rischio, nell'anagrafica, Y minima di
    Mosca (vedi "Rubrica", sezione 8); dal 30/09 sera (**D-60**) li stima A1 e
    li decide il validatore;
  - **D-34 versione della struttura del workbook** e comando
    `aggiorna-registro` (vedi "Lo script di campo");
  - D-17 validazione delle notizie settimanali facoltativa;
  - D-18/D-20 tassonomia, descrittori e parametri **provvisori** (quelli del
    pacchetto), da rivedere dopo il primo ciclo;
  - D-19 **Probabilita nel composito** (in vigore dal 25/09); i **pesi** sono
    quelli di **D-50** (30/09): Impatto 0,35, Probabilita 0,25, Prossimita
    0,20, Velocity 0,20, media pesata delle dimensioni valutate (vedi
    "Rubrica");
  - **D-49** Gap_Controlli fuori dal modello; resta il **presidio dei
    controlli** (Non verificato, Adeguato, Parziale, Assente), input del
    validatore nell'anagrafica, fuori dallo score; **D-50** Velocity
    facoltativa (null = non valutata) e pesi ridistribuiti; **D-51** esito e
    "da/a" delle variazioni calcolati dallo script ("Variato" = cambia
    Impatto, Probabilita, Prossimita o Velocity);
    **D-52** Probabilita con descrittori di plausibilita', Confidence solo su
    numero, indipendenza e data delle fonti; **D-53** KRI da 1 a 3 (dal 01/10 due, D-64), soglie
    entrambe o nessuna (le fissa la Banca: "Soglie da definire"), rilettura
    solo dei valori trovati; **D-54** azioni senza `dimensione`, C8 solo
    Osservazioni, `valida` rifiuta un owner persona anche se Accettato;
    **D-55** un rischio per meccanismo di perdita, nessun event type
    obbligatorio, 20 rischi; **D-56** `trimestrale --procedi-con-rilievi
    --motivo --decisore`: i soli Bloccanti di A5 (l'agente) si superano, i
    rilievi restano sui rischi e la validazione chiede la motivazione;
  - **D-57..D-62** (30/09 sera, revisione del responsabile): **D-57** Severity
    si chiama **Impatto** ovunque (campo `impatto`, colonna Impatto,
    pesoImpatto; `colonne_rinominate` per la migrazione); **D-58** Confidence
    tolta, **rilevanza 1-3 per fonte** (Probabilita 5 o Prossimita 4-5 con una
    fonte di rilevanza 3, salvo deroga), C5 "Fonti"; **D-59** Z = meta' della
    fascia (5 → 0, 4 → 0,5, 3 → 1,5, 2 → 2,5, 1 → 3,5; l'inizio della fascia,
    provato, metteva quasi tutto in AGIRE ORA); **D-60** anni di adeguamento
    stimati da A1 (campo `anni_adeguamento`), validati, scritti
    nell'anagrafica da `valida`; **D-61** descrittori riscritti (Impatto 1 "perdita
    entro 100.000 euro", Probabilita su casi in altri settori, aziende
    strutturate, istituzioni finanziarie; Prossimita 5 anche aziende ampie e
    complesse e deroga dichiarata per fenomeni ad altissimo impatto; Velocity
    3 da 3 a 6 mesi, 4 da 1 a 3 mesi, 5 entro 1 mese), soglia di direzione 2,
    soglia del Delta 0,30; **D-62** comando `report` e stampa orizzontale di
    Registro e Parametri;
  - **D-63..D-65** (01/10, suggerimenti di una proposta esterna di supporto
    NFR, documento riservato fuori dal pacchetto): **D-63** livello di allerta
    calcolato (segnali forti F1 AGIRE ORA, F2 KRI in rosso, F3 segnali netti
    oltre la soglia; aggravanti, solo con margine sotto 1 anno, A1 P x I da
    12, A2 presidio Assente, A3 meta' dei KRI in ambra o rosso; Attivazione
    con 2 forti, Attenzione con 1 o margine stretto e un aggravante,
    Monitoraggio altrimenti), senza colonne nuove nei dati: colore dei cerchi
    del radar, fondo dell'ID nel Registro, numero del Quadro, livello dei
    rischi segnalati; il tema del supervisore passa dal bordo giallo al ◆
    accanto all'ID; **D-64** due KRI per rischio, Esposizione ed Evoluzione,
    con il `tipo` assegnato da A1 (sostituisce "da 1 a 3" di D-53) e A1 che
    ragiona analizzando nel dettaglio ogni fonte; **D-65** Probabilita 4-5 solo
    se la Banca e' esposta (nessuna dimensione "Esposizione");
  - **D-66** (01/10): sintesi di A3 e flag proposti di ogni settimana nel
    foglio dati Sintesi_Settimane (scritti da `settimanale`; rilanciare la
    stessa settimana aggiorna la riga) e nel foglio Notizie per la settimana
    corrente; la library Report_Settimanali resta vuota nella variante locale;
  - D-21 criteri di accettazione del primo ciclo: 80% dei rischi in entrambi i
    run, 80% dei punteggi identici, rettifiche al massimo 30%;
  - D-22 primo ciclo da valutare **2026Q4** (registro inizializzato con ciclo
    precedente 2026Q3).
- Direzione futura dichiarata: dare agli agenti il permesso di scrivere,
  eliminando il copia-incolla. Va progettata **mantenendo i controlli
  deterministici come gate**. Analisi in
  `Analisi_Architettura/Archivio/07_Piano_semplificazione_senza_Python.md` (in riserva,
  D-43) e in `Analisi_Architettura/Archivio/10_Piano_automazione_processo.md` (27/09:
  Python resta il motore, procedura guidata per l'analista; dal 28/09 anche
  l'opzione Copilot Studio, dove gli agenti consegnano solo in `In_arrivo` e
  nel registro scrive sempre e solo il motore). Le voci di lavoro del piano 10
  sono nel TODO (AU1-AU6); la scelta della strada e' A-15. Niente e' ancora
  approvato per la realizzazione: fino ad allora vale l'architettura
  descritta qui.
- Confronto con un Horizon Scanning fatto a mano con Copilot M365
  (`Analisi_Architettura/Archivio/08_Confronto_Horizon_Scanning_Copilot.md`, 25/09).
  Le proposte di **priorita' A sono approvate e applicate** il 25/09: P1 pagina
  di sintesi executive, P2 classifica e lente di Mosca, P9 schede e
  metodologia nel report (D-32), P4 anni di adeguamento (D-33), P5 D-19 in
  vigore; per portarle sul registro in uso, D-34. Poi, lo stesso giorno:
  **P3** come bordo giallo spesso del cerchio (non un colore diverso: scelta
  dell'utente; il rosso della prima versione si confondeva con la linea di Mosca) per i temi all'attenzione del supervisore, input del validatore
  (D-35); **P6** regola 7 della rubrica (numero con fonte o dichiarato come
  valutazione) verificata da A5 in C4 (D-36; descrittori di plausibilita' della
  Probabilita rimandati ad A-12); **P11** i sette rischi dell'esempio come
  osservazione nel collaudo in ambiente (guida, Avvio del progetto, 7.5), mai dati ad A1
  (D-37). P7 azioni di approfondimento, P8 report di settore fra le fonti,
  P10 tracciabilita' restano **proposte non approvate**: non implementarle
  finche' non sono in DECISIONI.md.
- **Il workbook si spiega da se'** (richiesta dell'utente del 25/09, D-38):
  guida in testa a ogni foglio con il processo che lo aggiorna, significato di
  ogni colonna, operazioni e criteri della validazione, tabella "chi aggiorna
  cosa", quando si lanciano A5 e A6. Vedi IL WORKBOOK.
- **Ridisegno del registro e del report** (`Analisi_Architettura/Archivio/09`, anteprime
  v1, v2 e v3 valutate dall'utente il 25/09; v3 approvata senza note; **D-39**
  e **D-40**): **un solo file** con report e registro senza doppioni, tutto
  ridisegnato e spiegato (Dizionario dei dati, guida e fascia del titolo,
  legenda delle abbreviazioni); nome dell'analisi "**Horizon Scan NFR**";
  **commento di A1 breve** (messaggio chiave e decisioni richieste) e il
  "perche'" di ogni rischio segnalato **calcolato dal foglio**; Delta con la
  scala spiegata e i motivi a fianco; Registro con Δ 6 mesi; Piano_azioni;
  **schede dei rischi in un file a parte**, con l'andamento negli ultimi
  trimestri e i testi estesi di un **agente dedicato, A6**, dopo la
  validazione. Per valutare una modifica grafica o di struttura: prima
  un'anteprima Excel separata con i dati di esempio, poi il generatore.
  Claude Design solo per tavole di riferimento; il report resta nativo in Excel.
- **Power Query e' abilitato** sull'Excel aziendale (confermato il 25/09): non
  e' piu' un'ipotesi da verificare (V0 del documento 07); anche Copilot Studio
  e' disponibile (28/09, D-44). Dall'esempio NON si prende: lista dei rischi
  imposta nel prompt, punteggi ritoccati per la grafica, urgenza stimata a
  giudizio, autocontrollo affidato al modello.
- **Prova di Copilot Studio in due opzioni del codice** (richiesta dell'utente
  del 05/10: "fai le 2 opzioni con le skill.md e vediamo"; D-70). Il
  precontrollo gira dentro A1 con lo **stesso codice** del comando sul PC:
  script unico composto dai moduli del pacchetto, eseguito dal Code interpreter
  dell'esperienza standard (allegato .txt) o dalla skill `precontrollo-nfr`
  nella nuova esperienza. In parallelo, la prova della versione senza Copilot
  Studio su un registro di prova separato. Adottare un'opzione e' una decisione
  da prendere con A-15; D-11 resta per gli agenti in esercizio.

Fermati e chiedi solo per decisioni che spettano alla funzione di rischio della
Banca (soglie, pesi, tassonomia, fonti, validatore) o se l'ambiente Microsoft
risulta diverso da quanto sopra.

## VINCOLI DELLA PIATTAFORMA — verificali con una ricerca prima di scrivere

Agent Builder evolve in fretta: rileggi Microsoft Learn e riporta nel README
la data della pagina. Alla stesura valgono (Learn, agg. luglio-agosto 2026):
- istruzioni di un agente **fino a 8.000 caratteri** (anche in Copilot Studio);
- knowledge: **al massimo 4 siti web pubblici** (URL di al massimo due livelli,
  senza parametri; oppure l'interruttore "Search all websites"); la pagina
  "Build agents" (agg. 19/08/2026) dice "fino a 20 knowledge source" in tutto
  (prima si leggeva 100 file/cartelle/siti SharePoint): verificare;
- tipi di file letti dalla knowledge: .docx, .pdf, .pptx, .xlsx, .txt, .html
  (solo da SharePoint) — **non .json ne' .md**;
- capability: code interpreter ("Create documents, charts, and code") e image
  generator. Il **code interpreter e' ACCESO di default** (Learn, agg.
  29/07/2026): la configurazione deve dire esplicitamente di spegnerlo o di
  usarlo. I suoi file sono **download temporanei della sessione**, non salvati
  in SharePoint; il codice lo scrive il modello, quindi non e' un controllo
  deterministico. **Nessuna scrittura** in Excel o SharePoint da parte
  dell'agente, nessun flow;
- "Modifica con Copilot" (Copilot dentro Excel, GA 22/04/2026) modifica in place
  un workbook su OneDrive/SharePoint, ma decide il modello quali celle cambiare:
  non sostituisce la scrittura controllata;
- gli allegati caricati in chat finiscono nella cartella OneDrive "Microsoft
  Copilot Chat Files" (copie persistenti: tema di governance);
- gli agenti Word/Excel/PowerPoint di Microsoft usano modelli Anthropic,
  **fuori dall'EU Data Boundary**: non usarli sui dati del registro senza un
  parere del DPO;
- prompt schedulati nativi, per singolo utente;
- le funzioni di Agent Builder sono elaborate da Copilot Studio; niente chiavi
  gestite dal cliente; un amministratore puo' disattivarlo;
- **Copilot Studio** (Learn, 05/10/2026) ha due motori:
  - **esperienza standard**: agenti classici; Code interpreter in Settings ->
    Generative AI -> File processing capabilities, da abilitare prima
    nell'ambiente (spento di default); richiede l'autenticazione Microsoft; il
    codice lo scrive il modello; "No charge" per gli utenti Microsoft 365
    Copilot in uso interno;
  - **nuova esperienza** (GitHub Copilot harness): sandbox Python senza rete
    (circa 99 librerie, niente pacchetti da installare); **skill** caricate
    come SKILL.md o .zip con script, che girano sempre uguali; file creati fino
    a 10 MB; allegati .txt, .md, .csv (non .json ne' .py), fino a 16 MiB;
    Copilot Credits dalla costruzione.

  Un agente non passa da un motore all'altro. Le pagine cambiano spesso:
  ricontrollarle prima di scrivere passi per Copilot Studio.

Conseguenze di progetto, obbligatorie:
- il kernel non si puo' incollare per intero: i prompt si **compongono** con le
  sole sezioni che servono a ciascun agente (vedi "Prompt");
- tutto cio' che un agente deve leggere come knowledge o allegato si scrive **anche in
  .txt** (la raccolta notizie; la baseline arriva come allegato: `Input_A1_<ciclo>.txt` ad
  A1, `Input_A8_<periodo>.txt` ad A8, `Input_A3_A4.txt` ad A3 e A4 (AU7), `Input_A5_<ciclo>.txt` ad A5, `Input_A6_<ciclo>.json` ad A6 (D-84): mai dalla knowledge,
  che si indicizza in ritardo o salta un file singolo);
- l'elenco delle fonti va **nelle istruzioni** di A3; come knowledge web solo i
  quattro siti marcati; "Search all websites" spento;
- setup degli agenti: capability "nessuna" vuol dire **spegnere esplicitamente**
  il code interpreter ("Create documents, charts, and code", acceso di default)
  e "Create images" su ogni agente; il README e la guida (sezione 0.2) lo dicono.

## PRINCIPI ARCHITETTURALI — non negoziabili

1. **Separazione giudizio / calcolo.** L'LLM valuta e argomenta; il codice
   calcola, versiona e disegna. Gli agenti danno le dimensioni del rischio, MAI
   lo score composito, MAI l'urgenza: li calcola il foglio.
2. **Lo stato e' storico e non si riscrive.** Tutte le tabelle dati del workbook
   (RiskRegister, Azioni, KRI, NewsLog, Storico_Validazioni) sono storiche: una riga per
   soggetto per ciclo o per notizia, **solo in coda**. Le liste SharePoint, dove
   c'e' Power Automate, ne sono una copia. Ogni ciclo e ogni settimana lasciano
   un Excel congelato con nome proprio.
3. **Solo il ciclo trimestrale modifica uno score.** Settimanale e su richiesta
   leggono, commentano, propongono un flag, senza mai una cifra nuova.
   Confermato dall'utente il 26/09 (D-41) con una sola eccezione, da
   implementare (TODO P3): un segnale critico puo' portare a un ciclo
   straordinario, con la stessa catena di controlli e validazione (fatto: D-75,
   con A8 dal D-77). Un evento
   che tocca piu' rischi = righe di rischio separate, collegate fra loro
   (D-42, collegamento da implementare: TODO P5).
4. **Ogni controllo di giudizio ha una controparte deterministica** dove il
   vincolo e' esprimibile, e ogni controllo e' a sua volta collaudato (un caso
   che passa, uno che viene fermato).
5. **Coerenza fra componenti verificata dal codice.** Una sola fonte per ogni
   regola; la mappa sorgente->destinazione e' un DATO letto da generatore,
   scrittura e collaudo; i riferimenti incrociati sono testati.
6. **Un prompt non contiene commenti.** Il perche' sta nei file _DOCUMENTATO.
   Nei file del kernel le righe `>` sono note per chi legge e non entrano nei
   prompt.
7. **Nessuna valutazione vale senza una persona che la valida**, e ogni
   rettifica conserva proposta dell'agente, valore deciso, motivo, autore,
   data: e' la base dati per insegnare agli agenti in futuro.
8. **Il sistema si ferma prima di sbagliare, non dopo.** Ogni scrittura: valida,
   controlla, scrive, ricalcola in Excel, verifica, e SOLO ALLORA salva (backup
   prima). Un fermo lascia il registro intatto e lo dice.

## LA FAMIGLIA DI AGENTI

- **A1 Horizon Scanner** (trimestrale): valuta tutti i rischi in anagrafica
  rispetto ai due cicli precedenti e ne individua di nuovi (un rischio per
  meccanismo di perdita, D-55); "ragiona con cura: prima di valutare analizza nel dettaglio ogni fonte" (D-64, nel ruolo); propone da 1 a 5 azioni e due KRI (Esposizione, Evoluzione) per
  rischio; rilegge i KRI in vigore di cui trova un valore. Valuta solo cio' che
  le fonti sostengono (D-49...D-53): niente controlli della Banca, niente
  esito, Velocity null se nessuna fonte ne documenta i tempi. Il razionale e'
  in parti (D-68): RISCHIO (il fenomeno in termini di rischio), IMPATTO,
  PROBABILITA, PROSSIMITA, VELOCITY (perche' quel valore, con fatto e
  documento), ADEGUAMENTO; azioni e KRI con EFFETTO. Registra i fenomeni
  esaminati e non censiti (D-72). **Registro unico** (D-79): rivaluta tutti i rischi
  del radar e, di quelli in osservazione, solo quelli con evidenza nuova (con
  orizzonte_anni e segnale_avvicinamento, senza KRI ne' azioni); a chi entra nel
  radar scrive subito KRI e azioni. Output JSON.
- **A2 Scrittura** (NON un agente): lo script deterministico, uguale in
  entrambe le varianti (con Power Automate lo lancia un desktop flow).
- **A3 Interim Update** (settimanale): integra le notizie dei tre canali; per
  ogni notizia l'impatto su tutti e sette gli event type, il rischio collegato,
  il segnale, il **codice fonte**; propone flag; non modifica score. Baseline solo
  dall'allegato `Input_A3_A4.txt` (AU7, D-83).
- **A4 News Assessor** (su richiesta): parere su una notizia, ancorato alla
  valutazione deliberata; mai una cifra, mai una persona, non scrive. Baseline solo
  dall'allegato `Input_A3_A4.txt` (AU7, D-83).
- **A5 Challenger** (trimestrale, dopo A1, **facoltativo** dal 06/10, D-71):
  nove controlli C1-C9 su input ristretto (output di A1 + baseline, mai le
  notizie); i suoi rilievi non fermano il ciclo: vanno nella colonna
  Segnalazioni della griglia e un suo Bloccante chiede la Motivazione. Ferma
  solo lo script, per l'integrita' del registro.
- **A6 Schede dei rischi** (trimestrale, DOPO la validazione, D-40): un solo
  allegato, `Input_A6_<ciclo>.json` (dati validati preparati dallo
  script), nessuna knowledge; scrive per ogni rischio descrizione estesa (il
  fenomeno in termini di rischio), spiegazione di ognuna delle quattro
  dimensioni (Impatto, Probabilita, Prossimita, Velocity) a partire dalle
  motivazioni di A1, con i documenti (D-68), a cosa serve ogni fonte e perche'
  ha la sua rilevanza; non
  valuta e non cambia valori. Lo script controlla l'output e produce
  `Schede_<ciclo>.xlsx`; senza A6 le schede escono con i testi del registro
  (Razionale, perche' di ogni valore, perche' ed effetto di azioni e KRI: di A1).
- **A7 Assistente del registro** (su richiesta, D-72): spiega in chat il perche'
  delle valutazioni (anche dei fenomeni non censiti e dei rischi in
  osservazione) distinguendo registrato, calcolato e sua lettura; knowledge
  scritta dallo script (cartella `Spiegazioni`); non propone valori e non scrive.
- **A8 Evento critico** (nel ciclo straordinario deciso dalla funzione di rischio,
  D-75, D-77): stesso allegato `Input_A8_<AAAAQn-Sk>.txt` e stesso schema di A1, piu'
  i documenti dell'evento; analizza a fondo l'evento (campo `analisi_evento`),
  rivaluta TUTTI e SOLO i rischi indicati e censisce i nuovi che l'evento crea
  (almeno uno se lo straordinario e' di solo censimento); rilegge ogni KRI in
  vigore dei rischi che riscrive (C7 da motivare se no: un KRI Non rilevato
  toglierebbe l'aggravante al livello di allerta proprio quando il rischio sale). Nessun comando proprio:
  `precontrollo`, `trimestrale`, `valida` come per A1. Prompt al limite: il dettaglio
  di `analisi_evento` sta nella guida di scrittura dell'allegato.
- **Validazione umana** (dopo ogni trimestre; facoltativa ogni settimana): un
  validatore accetta, rettifica o respinge ogni proposta nella **griglia del
  foglio Validazione**, una riga per rischio (con la decisione sullo stato:
  Automatico, Radar, Osservazione; D-79), KRI, azione e notizia (D-67):
  riga non toccata = accettata, cella gialla cambiata = rettifica con
  Motivazione, Respingi = Sì (non per i rischi); il trimestre dopo non parte
  finche' il precedente non e' validato.

## IL KERNEL (01_Kernel) — da scrivere per primo

### Rubrica (`rubrica_scoring.md`), sezioni numerate

1. **Dimensioni**, interi 1-5 ancorati a descrittori osservabili, 5 = peggiore:
   **Impatto** (era Severity, D-57; 1 "Limitato: nessun cliente toccato,
   perdita entro 100.000 euro" ... 5 "Critico: effetto sulla continuita', sui
   prodotti o sulla solvibilita' della Banca"), **Probabilita** (plausibilita'
   per la Banca, D-52 e D-61: 1 Remota "solo teorica, nessun caso noto" ... 3
   "casi in altri settori anche non finanziari; Banca esposta", 4 "casi
   ripetuti in aziende strutturate o banche, o crescita del fenomeno
   documentata", 5 "gia' osservato presso istituzioni finanziarie o la loro
   filiera, anche di fornitori, o fenomeno in rapida accelerazione"; riga
   "4-5 solo se la Banca e' esposta", D-65),
   Prossimita (QUANDO puo' manifestarsi, solo tempo; 5 anche "aziende ampie e
   complesse"; "4-5 solo con casi documentati (banca comparabile, fornitore,
   quasi-incidente in aziende complesse) o un evento certo; deroga, dichiarata
   nel razionale, per fenomeni ad altissimo impatto (es. nuovo Mythos, GenAI
   imprevista, superintelligenza)"; nota `>` con la tabella di Z per livello,
   D-59), Velocity (1 oltre 12 mesi, 2 da 6 a 12, 3 da 3 a 6, 4 da 1 a 3, 5
   entro 1 mese; **facoltativa**, D-50: "null se nessuna fonte ne documenta i
   tempi"), tutte con le stesse regole di variazione; e **Anni di
   adeguamento** (D-60: "Facoltativo (null se non serve): anni di un
   adeguamento strutturale della Banca ... stima motivata nel razionale").
   La frase "Non calcolare lo score composito" e' tolta il 30/09 sera per
   spazio (lo schema non ha il campo). **Gap_Controlli non c'e'
   piu'** (D-49, 30/09): A1 non vede i controlli della Banca, con poche fonti
   esterne era un pavimento costante (4 su 7 rischi su 7 il 29/09) che fermava
   A5; resta il **presidio dei controlli**, giudizio qualitativo della Banca
   nell'anagrafica, fuori dallo score (riga `>` della sezione 7).
   Score_Composito solo formula del foglio: **decisione D-50**, media pesata
   delle dimensioni valutate, 0,35 Impatto + 0,25 Probabilita + 0,20
   Prossimita + 0,20 Velocity, divisa per la somma dei pesi presenti (senza
   Velocity i pesi si ridistribuiscono sulle altre tre); vuoto se manca una
   delle tre obbligatorie. Pesi provvisori, in Parametri B4:B7. **I pesi NON
   stanno nei titoli delle dimensioni** (quindi nemmeno nei prompt): sono nelle
   righe `>` delle sezioni 1 e 7. Gli agenti non calcolano il composito, e i
   caratteri servono ad A1.
2. **Rilevanza delle fonti** (D-58, 30/09 sera): "Rilevanza 1-3 di ogni fonte
   per la previsione; stesso ente o stesso fatto = una fonte"; 1 Bassa (stampa
   generalista, opinioni), 2 Media (fonte specializzata con dati o casi), 3
   Alta (regolatore o autorita', consorzio di dati come ORX; caso documentato
   presso la Banca, una banca comparabile o un fornitore); "Probabilita 5 o
   Prossimita 4-5: almeno una fonte di rilevanza 3 (salvo deroga)". La
   Confidence del rischio non c'e' piu'. Storia: prima era la **Confidence** 1-5, fuori dal composito (solidita' dell'evidenza; confidence
   4 richiede almeno 2 fonti, 5 almeno 3; "Stesso ente o stesso fatto = una
   fonte"; 3 = "Due fonti indipendenti, o una primaria degli ultimi 12 mesi",
   D-52). **D-46 (29/09)**: il 4 e il 5 non
   richiedono piu' una fonte INTERNA, ma "primaria/indipendente" (regolatore,
   consorzio dati, caso di banca comparabile contano quanto un audit interno)
   — un rischio davvero emergente non ha ancora una traccia interna, quindi
   richiederla impediva per costruzione la confidence alta sui casi per cui
   l'Horizon Scan esiste. "Indipendenti" resta il freno contro l'inflazione
   (regola 6, sezione 3).
3. **Regole di variazione**: conferma di default senza evidenza nuova; massimo
   un punto fra cicli consecutivi ("una Velocity prima null entra con
   qualunque valore"); ogni valore cambiato cita un'evidenza specifica datata
   dopo il ciclo precedente (frasi generiche non sono evidenza); le riduzioni
   hanno lo stesso onere degli aumenti ("l'Impatto scende solo se cambia il
   danno possibile"); confermare significa riprendere le fonti ("se non
   valgono piu', il valore va rivisto"); la copertura
   mediatica non e' evidenza; **(7, D-36)** il razionale cita un dato numerico
   con la sua fonte, se esiste, e un numero senza fonte e' una valutazione da
   dichiarare. A5 lo controlla in C4 (Osservazione).
4. **KRI** (D-53, D-64): due per rischio, "Esposizione (quanto la Banca e' esposta) ed Evoluzione (quanto cresce il fenomeno)"; valore crescente = peggio; fonte dati
   interna identificabile; "Soglie solo se una fonte le sostiene, entrambe,
   allerta >= attenzione; altrimenti null (le fissa la Banca)".
5. **Intensita' di una notizia** 0-3 per event type, separata dalla direzione.
6. **Segnali**: quattro valori letterali (Peggiorativo, Migliorativo, Neutro,
   Non rilevante); soglia di direzione 2 segnali netti in 4 settimane (D-61;
   era 3), in una cella di input.
7. **Parametri numerici e dove vivono** (solo righe `>`).
8. **Urgenza: disuguaglianza di Mosca** (solo righe `>`, la calcola il foglio):
   origine (Mosca 2015, crittografia post-quantistica: X + Y > Z = agire ora) e
   adattamento DA VALIDARE: Z = anni prima della manifestazione, da una tabella
   per Prossimita = **meta' della fascia** del descrittore (D-59: 5..1 -> 0 /
   0,5 / 1,5 / 2,5 / 3,5; prima 0 / 0,5 / 1,5 / 2,5 / 4, senza corrispondenza
   scritta); X = anni per decidere e
   avviare (0,25, un ciclo); Y = il maggiore fra l'orizzonte piu' lungo delle
   azioni del ciclo non respinte (3/6/12 mesi; 1 anno di riserva se non ce ne
   sono) e gli **anni di adeguamento** del rischio (colonna Anni_Adeguamento
   dell'anagrafica, stimati da A1 e validati, D-33 e D-60: senza, Y non supera un anno e i
   rischi con adeguamento pluriennale, es. migrazione post-quantistica, sono
   sottostimati — proprio il caso per cui Mosca ha scritto la disuguaglianza).
   Margine = Z - (X + Y); < 0 = "AGIRE ORA". Limiti dichiarati: graduatoria
   ancorata, non previsione. Sottosezione **Livello di allerta** (D-63): le
   tre tabelle dei segnali forti F1-F3, degli aggravanti A1-A3 e dei livelli
   con le conseguenze da decidere con la funzione di rischio; non e' uno score
   (cambia anche con i segnali settimanali, senza contraddire D-41); il tema del
   supervisore non alza il livello. Nella sezione 7 le quattro soglie del
   livello (livelloPxI, livelloQuotaKRI, livelloMargine, livelloForti).

**Descrittori brevi**: il limite di 8.000 caratteri vale per il prompt composto.
Dopo ogni modifica si ricompone e si misura.

### Tassonomia (`tassonomia_nfr.md`)

Nove categorie della tassonomia interna della Banca (D-74, codici `9.1`, `9.4`,
`9.5`, `9.6`, `9.7`, `9.8`, `9.9`, `9.11`, `9.13`, descrizioni riassunte dal file
`04_Riferimenti/Tassonomia dei Rischi.csv` (fonte documentale, non la legge nessun componente) per stare nei prompt; i nomi interni restano
`event_type`, `Event_Type`, `codiciL1`) + otto driver emergenti DRV-CYB, TPR, AI,
CLI, CON, GEO, TEC, HUM (PERCHE' e' emergente). Un rischio: UNA categoria, UNO O
PIU' driver; `FP` solo per un rischio esistente fuori perimetro; regola di
classificazione: "anche due meccanismi di perdita diversi nella stessa categoria
sono due rischi" (D-55; nota `>`: nessun event type obbligatorio,
la prevalenza la danno le fonti, niente lista di ambiti attesi, D-37). Sezione
"Fuori perimetro". Nota: da adattare alla tassonomia della Banca prima del
deploy; il collaudo elenca ogni disallineamento se cambia un codice.

### Elenco fonti (`fonti.md`) — validato

Stato al 24/09 (D-15, D-16, D-27, D-28, D-29): **tutte approvate tranne
FNT-19**. FNT-19 (pagine di stato dei fornitori ICT critici) e' **esclusa**:
il monitoraggio si fa gia' in altre sedi; resta nell'elenco come traccia della
scelta. Licenze di stampa e abbonamenti verificate da Legal. I quattro siti
della knowledge web sono FNT-20 Banca d'Italia vigilanza, FNT-21 CONSOB,
FNT-22 Garante privacy, FNT-23 Protezione Civile. Una rigenerazione conserva
stati, licenze e note.

Una voce per fonte, formato fisso leggibile da codice: titolo `### FNT-nn Nome`,
poi righe `- chiave: valore` (canale rss/sito/share, indirizzo, temi = codici
di tassonomia, stato da validare/approvata/esclusa, licenza; facoltative
sito_agente si/no, max_voci, escludi con parole separate da `;`, verificato),
commenti in righe `>`. Tre canali usati insieme:
- `rss`: feed raccolti da script (W0);
- `sito`: siti senza feed; **al massimo quattro** con `sito_agente: si`
  (knowledge web dell'agente), URL validi per Agent Builder;
- `share`: documenti interni o a licenza in SharePoint.
Contenuto di partenza: vigilanza e regolazione (BCE Vigilanza comunicati e
pubblicazioni, EBA, ESMA, Banca d'Italia, Commissione, FSB, BIS), cyber e frodi
(ACN/CSIRT, CERT-EU, NCSC, Europol, stampa specializzata), clima, stampa
generalista (con licenza da verificare), stato dei fornitori ICT critici,
siti senza feed (Banca d'Italia vigilanza, CONSOB, Garante privacy, Protezione
Civile), documenti interni (incidenti, antifrode, audit, DORA/BCM, threat
intelligence a pagamento, perdite esterne, newsletter). **Prova ogni feed dal
vivo** prima di scriverlo (molti indirizzi "classici" non funzionano piu') e
annota data e numero di voci; annota i feed senza date e quelli da filtrare.
Codice `MAN` = file caricato a mano da una fonte fuori elenco.

### Schemi e mappa

- `schema_output_A1.json` (dal 07/10 anche il campo facoltativo
  `fenomeni_non_censiti`, D-72; dall'08/10, D-79, nel rischio i campi facoltativi
  `orizzonte_anni` intero 1-30 o null e `segnale_avvicinamento` 10-300 caratteri o
  null, `kri_proposti` al massimo 2 e `azioni_mitigazione` al massimo 5, senza
  minimo: un rischio in osservazione non ne ha; niente campo `osservazione`):
  `additionalProperties: false` ovunque; ciclo
  `^[0-9]{4}Q[1-4]$`; **impatto**, prossimita, **probabilita** interi 1-5;
  **velocity `["integer","null"]` obbligatoria** (null = non valutata);
  **anni_adeguamento `["number","null"]` 0-30 obbligatorio** (D-60); niente
  confidence (D-58);
  NESSUN score composito, **nessun gap_controlli ne' esito**; variazioni
  (dimensione fra impatto, velocity, prossimita, probabilita;
  evidenza >= 20 caratteri; data_evidenza; **niente da/a**: li aggiunge lo
  script); fonti (tipo Interna/Esterna, **rilevanza** intero 1-3 obbligatorio,
  D-58); azioni 1-5 (owner funzione, orizzonte
  3/6/12 mesi, **niente dimensione**); kri_proposti **esattamente 2** (D-64),
  ciascuno con **`tipo` obbligatorio "Esposizione" o "Evoluzione"**, soglie
  `["number","null"]` obbligatorie, `kri_id` `["string","null"]` NON
  obbligatorio (null per un KRI nuovo: l'id lo assegna la scrittura);
  `ricalcolo_kri_ciclo_precedente` a livello CICLO, `valore` numero o null.
  Documenta che "entrambe o nessuna" e soglia_allerta >= soglia_attenzione non
  sono esprimibili nello schema: li presidiano C9 e la formula Stato del
  foglio.
- `schema_output_A3.json`: settimana (lunedi'); notizie con id
  `^N-[0-9]{8}-[0-9]{2}$`, fonte per esteso, **codice_fonte
  `^(FNT-[0-9]{2}|MAN)$`**, rischio_collegato o null, segnale, impatti
  ESATTAMENTE 7; flag_proposti.
- `schema_output_A5.json`: esito Approvato/Da rivedere, rilievi C1-C9 con
  gravita' Bloccante/Osservazione. Lo stesso formato lo producono i controlli
  meccanizzati: i due esiti si combinano (si procede solo se entrambi approvano).
- `mappatura_campi.json`: la mappa UNICA campo -> colonna, con
  `versione_template` (= la struttura del workbook che descrive; lo script si
  ferma se non coincide con la sua). Sezione `tabelle`
  (tblRegister, tblAzioni, tblKRI, **tblSintesi** — una riga per ciclo con
  `righe_da` vuoto: Ciclo, Data_Riferimento, Sintesi_A1 = `payload:sintesi`
  (significato: "nella forma MESSAGGIO: ... DECISIONI: ..."),
  Sintesi_A5, Osservazioni_Controlli, Data_Scrittura —, **tblSettimane** (D-66:
  foglio Sintesi_Settimane, payload A3, `righe_da` vuoto: Settimana,
  Notizie = `derivato:numero_notizie`, Sintesi_A3 = `payload:sintesi`,
  Flag_Proposti = `derivato:flag_proposti` "NFR-nn · direzione: motivazione"
  uno per riga o "Nessun flag proposto", Data_Scrittura; prefisso SE_) e tblNews: foglio, payload, righe_da, modo,
  colonne con sorgente `payload:percorso[|trasformazione]`, `derivato:nome` o
  `formula:modello` con `{Colonna}`; Esito = `derivato:esito`; colonna
  **Rilievi** di tblRegister = `derivato:rilievi_rischio`; in tblSintesi
  Rilievi_Ciclo e Rilievi_Superati; Score_Composito con la media pesata delle
  dimensioni presenti, `IF(ISNUMBER({Velocity}),...)`; Stato del KRI che
  controlla PRIMA le soglie vuote: "Soglie da definire"); `colonne_dismesse`
  (D-49, D-54, D-58: Gap_Controlli e Confidence in tblRegister, Dimensione in
  tblAzioni: colonne che `aggiorna-registro` lascia nel backup invece di
  fermarsi); `colonne_rinominate` (D-57: Severity -> Impatto in tblRegister,
  copiata nella colonna nuova); colonna **Anni_Adeguamento** di tblRegister
  dal payload (D-60); `validazione` (tabella tblValidazione nel foglio dati
  **Storico_Validazioni**, D-67; la nota descrive griglia e storico),
  colonne, decisioni, oggetti Rischio/KRI/Azione/Notizia con tabella, id,
  periodo, nome, campi validabili — per il Rischio **cinque**: Impatto,
  Velocity, Prossimita, Probabilita, Anni_Adeguamento —, respingibile); `anagrafica`
  (ID, Nome, Event_Type, Driver dal payload; Owner, **Anni_Adeguamento**,
  Attenzione_Supervisore e **Presidio_Controlli** input umani conservati:
  derivati `owner_esistente_o_da_assegnare`, `anni_adeguamento_esistente`,
  `attenzione_supervisore_esistente`, `presidio_esistente_o_non_verificato`); `parametri`;
  `non_nel_workbook` (ogni campo degli schemi senza colonna, con la sua
  destinazione); `liste_sharepoint` (copie delle tabelle senza colonne formula).
- `schema_output_A6.json`: ciclo; schede (id_rischio, descrizione_estesa
  300-1800, dimensioni ESATTAMENTE 4 con dimensione fra impatto,
  probabilita, prossimita, velocity e spiegazione 40-500, fonti con
  riferimento e a_sostegno_di). Cio' che lo schema non vede (stessi rischi
  dell'input, cinque valori diversi, fonti identiche, nessun numero fuori dai
  dati) lo controlla `schede.controlla_a6`.
- `schema_output_A1_DOCUMENTATO.md`: i quattro schemi campo per campo, la
  baseline e l'input delle schede.
- `controlli_A5.md` (D-69): il **testo unico dei nove controlli** C1-C9, un
  punto elenco ciascuno ("- C1 Completezza: ..."), righe `>` di nota. C8 dice
  anche "non ripete un'azione aperta della baseline". Lo leggono
  `componi_prompt.py` (`{{CONTROLLI}}` nel modello di A5) e `input_a1.py`
  (allegato di A1), tramite `input_a1.testo_controlli`.
- `guida_scrittura_A1.md` (D-69; dal 07/10 anche le sezioni "Fenomeni
  considerati e non censiti", D-72, e "Radar e osservazione", D-79: la regola dalla
  baseline, `rischi` contro `rischi_in_osservazione`, riscrivere un rischio in
  osservazione solo con evidenza nuova, orizzonte e segnale, notizie e flag di A3,
  KRI e azioni per chi entra; dal 19/10, D-80, gli anni di adeguamento anche dei rischi in osservazione con
  Impatto 4-5, riscrivendo senza evidenza nuova chi non li ha, perche' con X + Y > Z entrino nel radar; dal 19/10, D-81,
  la frase "ESPOSIZIONE NON NOTA: con l'esposizione documentata sarebbe N" nella parte PROBABILITA quando le fonti
  non dicono se la Banca e' esposta): come A1 scrive la descrizione (3-5 frasi:
  meccanismo causa-evento-danno, dove tocca la Banca, perche' emergente; niente
  punteggi), il razionale in parti (per ogni valore: descrittore, fatto con
  documento e data, **perche' non il valore vicino**, da/a o fonti ancora
  valide; "Attribuisci a un documento solo cio' che il documento dice"), le
  azioni (verbo, oggetto, risultato verificabile; quale anello interrompe;
  EFFETTO osservabile; **un'azione aperta non si ripropone**: passo successivo)
  e i KRI; poi un **esempio completo di forma** (frode con voce clonata sui
  bonifici corporate) con fatti e documenti dichiarati inventati ("Documento
  A/B/C"). Esempio coerente con la rubrica: Probabilita 5 perche' gia'
  osservato presso banche, Prossimita 4 e "non 5" perche' nessun tentativo
  presso la Banca (trappola 79).

## PROMPT (02_Agenti)

- Modelli in `02_Agenti/modelli/A1.md, A3.md, A4.md, A5.md, A6.md` con segnaposto
  `{{TASSONOMIA}}`, `{{RUBRICA:1,3}}` (sezioni numerate), `{{FONTI}}` (elenco
  compatto codice/nome/canale, fonti escluse omesse), `{{CONTROLLI}}` (i nove
  controlli di `controlli_A5.md`, D-69: il modello di A5 tiene il titolo
  "# I nove controlli", la frase "Esegui tutti e nove..." e, dopo, la riga
  sull'esito; non ha piu' una copia dei controlli).
- `componi_prompt.py` genera i prompt operativi (`A1_Horizon_Scanner.md` ...),
  esclude le righe `>`, e con `--verifica` esce con errore se un prompt e' fuori
  data o supera 8.000 caratteri. I prompt generati non si modificano a mano.
- Lo schema JSON intero non sta nel prompt: basta uno scheletro dell'output; lo
  schema lo applica il validatore.
- **A1, A3, A4, A7, A8** (non A5) hanno nell'Input la frase fissa "Utilizza
  **sempre** lo strumento di ricerca file o altri strumenti di ricerca aziendale
  per accedere ai file della knowledge." (dal 13/10; prima "Usa sempre la ricerca
  nei file o quella aziendale: non rispondere a memoria") — forza l'uso dello strumento di ricerca invece di
  rispondere dal solo contesto della chat. **A5 ne e' escluso deliberatamente**:
  il suo Input dice l'opposto ("Non usare notizie, knowledge o altre fonti e non
  cercarle") perche' deve giudicare se l'output di A1 si sostiene da se',
  non cercare conferme esterne — le due istruzioni sono in conflitto voluto,
  non un'incoerenza da correggere in una rigenerazione futura.
- A1 riceve: rubrica 1-4, tassonomia, procedura in 10 passi numerati (il 10 e'
  l'autocontrollo), input = allegato `Input_A1` (dal 02/10, D-69: "Allegato
  Input_A1: baseline, controlli di A5, guida di scrittura."; la frase "Senza
  baseline rispondi solo ..." resta), fonti interne, News_Inbox (con
  codice FNT nel riferimento), siti configurati. Dal 02/10 sera (D-69) passo 7
  "Da 1 a 5 azioni nuove per rischio; owner = una funzione.", passo 8 senza "mai
  il kri_id di un altro rischio" (C9 nell'allegato), passo 10 "Prima di
  rispondere verifica ogni rischio con controlli e guida dell'allegato e
  correggi.", Output "Solo JSON, nessun testo attorno. Date AAAA-MM-GG." (senza
  "punteggi interi": la rubrica dice "Interi 1-5"). Nell'Output una riga fissa la
  struttura della **`sintesi`** (commento per il comitato, D-32, D-39):
  `sintesi: "MESSAGGIO: " messaggio chiave, 3 priorita' (id_rischio, perche'), nuovi e variati, event type senza rischi; poi "DECISIONI: " decisioni richieste. Solo fatti delle fonti.`
  Il Quadro la divide sul marcatore; senza marcatore tutto va nel messaggio.
  Il commento resta BREVE per scelta dell'utente: il perche' di ogni rischio
  segnalato lo calcola il foglio. Dal 02/10 (**D-68**) lo scheletro chiede
  anche il **razionale in parti**:
  `"razionale":"RISCHIO: causa, evento, danno. IMPATTO: fatto e documento. PROBABILITA: ... PROSSIMITA: ... VELOCITY: ... ADEGUAMENTO: se serve"`,
  e per azioni e KRI `"razionale":"perche'. EFFETTO: cosa cambia"` /
  `"razionale":"cosa misura. EFFETTO: andamento atteso"` (le schede mettono
  il perche' accanto a ogni valore e sotto ogni azione e KRI). Per farlo stare
  (circa 170 caratteri) sono tolte ripetizioni: "e restituisci SOLO un oggetto
  JSON" dal ruolo (lo dice l'Output), "riferimenti senza codici di ricerca
  (turn...)" dal passo 10 (li toglie `pulisci_riferimento`), "(sezione 2:
  stesso fatto = una fonte)" dalla regola 6 della rubrica, "ciclo AAAAQn"
  dall'Output e "id_rischio" dalla riga della sintesi ("(id e perche')");
  schema: razionale fino a 2.500 caratteri, quelli di azioni e KRI fino a 700.
  Tieni un margine sotto
  il limite: **almeno 500 caratteri per A1** quando si puo' (02/10 sera, D-69:
  A1 **7.963**, A5 7.902, A6 5.638; 02/10 pomeriggio: A1
  **7.971**, A5 7.857, A6 5.638; 01/10: A1
  **7.917** e A5 **7.895**, sotto l'obiettivo di margine; A3 7.082, A4 5.080 (dal 01/10 sera: "Baseline_corrente.txt
  in knowledge", prima diceva .json mentre la knowledge e' la copia .txt),
  A6 5.111; il 30/09 sera A1 7.885, al mattino 7.496; prima della
  semplificazione 7.977). Per farli stare: tolta la sezione 4 della rubrica
  (KRI) da A5 (`{{RUBRICA:1,2,3}}`: C9 la ripete), accorciati i passi 3, 4, 10
  di A1, la deroga, le regole 3, 6 e 7, la riga sugli strumenti di ricerca
  ("Usa sempre la ricerca nei file o quella aziendale: non rispondere a
  memoria."), il descrittore 1 della rilevanza e la riga degli anni di
  adeguamento. Il 01/10 il ruolo di A1 aggiunge "Ragiona con cura: prima di
  valutare analizza nel dettaglio ogni fonte." (richiesta del responsabile,
  vale in generale), il passo 8 "riusa kri_id, tipo e soglie", lo scheletro
  `"tipo":"Esposizione|Evoluzione"`; A5 C9 "due per rischio, uno di
  Esposizione e uno di Evoluzione, coerenti con cio' che misurano" e C4
  "(Probabilita 4-5 con la Banca esposta)"; A6 riceve tipo dei KRI e livello
  di allerta.
  Il 30/09 i passi di A1 restano dieci: 3 "Valuta TUTTI i rischi in anagrafica
  dai valori precedenti, con le regole di variazione; stesso id ed event
  type."; 4 "Rischi nuovi (al primo ciclo tutti): uno per meccanismo di
  perdita non coperto, con almeno una fonte specifica; nessun event type
  obbligatorio, parti dai driver sotto pressione nelle fonti. id_rischio =
  primo NFR-nn libero."; 5 una voce di variazione per ogni valore cambiato,
  nessuna per un rischio nuovo; 8 KRI "riusa kri_id e soglie di un KRI in
  vigore valido"; 9 rilettura "solo KRI in vigore con un valore di questo
  ciclo nelle fonti, mai ricopiato"; 10 autocontrollo con "nessun campo in
  piu'" (fino al 02/10 anche "riferimenti senza codici di ricerca"). Scheletro con
  `"velocity":null` e soglie null. Storia della lunghezza: al 25/09 sera A1
  era a 7.966 caratteri; la regola
  7 e' stata pagata accorciando la rubrica — "Non calcolare lo score
  composito: lo calcola il foglio.", regole 3, 4 e 5, confidence — e il passo 9
  "o null: mai ricopiato"): per farci
  stare la riga sono stati tolti i pesi dai titoli della rubrica e accorciati
  il passo 2 ("Evidenza nuova = datata dopo data_riferimento_precedente (se
  manca: tutta) e non dopo data_riferimento"), il passo 5, il passo 10 e due
  frasi della rubrica. **Non accorciare la tassonomia** per fare spazio ad A1:
  entra anche in A3 e A4, che andrebbero ricaricati senza motivo.
- **Primo ciclo da registro vuoto** (passi 2 e 4 di A1): se
  `data_riferimento_precedente` manca vale tutta l'evidenza disponibile non
  datata dopo `data_riferimento`; se la baseline non ha rischi, A1 li individua
  da zero, un rischio per meccanismo di perdita, **senza** passare in rassegna
  obbligata i sette event type (D-55: il 29/09 A1 l'aveva letto come "uno per
  tipo", accorpando meccanismi e riempiendo tipi deboli); lo script li scrive
  tutti "Nuovo". Il perche' e' in `COMMENTATI/A1_Horizon_Scanner_DOCUMENTATO.md`.
- A3: tre canali, codice_fonte, sette impatti, elenco fonti `{{FONTI}}`,
  rubrica 5-6. A5: C1-C9 con gravita', stessa numerazione ma contenuto del
  30/09: C1 stesso event type; C2 una variazione per ogni valore cambiato; C3
  data, specificita', un punto (Velocity da null libera); C4 un rischio = un
  meccanismo, Velocity solo con i tempi documentati, "un numero senza fonte
  non dichiarato come valutazione e' un'Osservazione"; C5 fonti indipendenti;
  C6 stesso fatto o copertura mediatica, aumenti senza fonti nuove; C7 solo KRI
  sconosciuti o ripetuti; C8 "sempre Osservazione"; C9 due KRI, uno per tipo (D-64), soglie
  entrambe o nessuna. A4 (la riga dei nomi delle dimensioni, senza Gap): sezioni fisse del
  parere (e non promette che la notizia compaia nel foglio Notizie).
- **A6**: ruolo (spiega, non valuta), input = solo `Input_A6_<ciclo>.json`
  (niente notizie, knowledge o ricerche: come A5, la frase "usa sempre lo
  strumento di ricerca" NON c'e'), sette regole (una scheda per rischio; valori
  intoccabili; **ogni numero deve stare nei dati del rischio o nella
  rubrica**; descrizione estesa 400-1500 caratteri = il fenomeno in termini di
  rischio (causa, evento, danno), senza i motivi dei punteggi; quattro
  spiegazioni di 80-500 caratteri (per una Velocity null: "non valutata" e
  perche') con le informazioni e i documenti, **partendo dalle `motivazioni`
  di A1 e senza attribuire a un documento cio' che A1 non gli attribuisce**
  (D-68), e, per un valore rettificato, il motivo del validatore; fonti
  copiate identiche con "a sostegno di"; niente nomi di persone), rubrica 1-2,
  scheletro dell'output. L'input porta `razionale_rischio`, `motivazioni`
  (divise dallo script) e, per azioni e KRI, razionale ed effetto atteso; A6
  non riscrive azioni e KRI (output piu' corto, nessun rischio di troncamento).
- `COMMENTATI/` spiega il perche' di ogni passo, con la stessa numerazione (il
  collaudo la confronta).

## IL WORKBOOK (03_Excel/genera_dashboard.py -> NFR_Dashboard_Template.xlsx)

**Colonne dalla mappa, mai elencate nel generatore.** Un solo file, 24 fogli
senza viste doppie (D-39), in quattro gruppi con linguette colorate, in
quest'ordine: **Guida** (ocra); report al comitato, di seguito per il PDF
(D-32), blu notte: **Quadro, Classifica, Radar_Mosca, Matrice, Delta,
Fenomeni** (D-79: i rischi in osservazione), **Metodologia**; lavoro, blu: **Registro, Storico, Indicatori,
Notizie, Piano_azioni, Osservazione** (D-79), **Validazione, Parametri,
Dizionario**; dati, grigio: RiskRegister, Azioni, KRI, NewsLog, Sintesi_Cicli,
**Sintesi_Settimane** (D-66), **Storico_Validazioni** (D-67). Nomi dei fogli senza spazi ne' apostrofi
(i riferimenti dei grafici li vorrebbero fra apici). Griglia nascosta tranne
nei dati; foglio attivo all'apertura: Quadro. Le **schede dei rischi** non
stanno nel registro: sono un file a parte (D-40, vedi "Lo script di campo").
**Versione della struttura**: nome definito `versioneTemplate` (="2026-10-09"),
uguale a `VERSIONE_TEMPLATE` del generatore e dello script e a
`versione_template` della mappa (il collaudo lo verifica). Va alzata a ogni
cambio di struttura (fogli, colonne, nomi), non per i soli dati di esempio.

**Dati** (unico posto in cui scrive lo script): tblRegister (con Probabilita,
Score_Composito e Chiave formula, **Rilievi** dopo Fonti, senza Gap_Controlli,
Approvato_Da, Validazione, Data_Validazione), tblAzioni (con Mesi_Orizzonte
formula, Stato, Validazione, senza Dimensione), **tblKRI STORICA**
(una riga per KRI per ciclo, colonne Ciclo e Chiave `Ciclo|KRI_ID`, **Tipo**
dopo Nome — payload `kri_proposti[].tipo`, D-64, vuoto nei KRI di prima —, Stato
formula, Validazione), tblNews (con Codice_Fonte, Settimana formula,
Imp_L1_01..07, Validazione), **tblValidazione** nel foglio dati
Storico_Validazioni (D-67; Periodo, Oggetto, ID, Nome, Campo, Proposta_Agente,
Decisione, Valore_Validato, Motivazione, Validato_Da, Data_Validazione, Stato:
una riga per oggetto e campo, la scrive solo lo script, niente elenchi a
discesa), **tblSintesi** nel foglio
Sintesi_Cicli (una riga per ciclo: commento di A1, sintesi di A5,
osservazioni, **Rilievi_Ciclo** e **Rilievi_Superati**; prefisso SI_),
**tblSettimane** nel foglio Sintesi_Settimane (una riga per settimana: sintesi
di A3 e flag proposti; prefisso SE_; D-66). **Registro unico (D-79)**: in fondo a
tblRegister le colonne **Stato**, **Motivo_Stato**, **Movimento**,
**Decisione_Stato** (derivate dallo script), **Orizzonte_Anni**,
**Segnale_Avvicinamento** (di A1) e la formula **Ordine_Osservazione** = score x
100000 + 1 - ROW()/10^6 per le sole righe "Osservazione" del ciclo corrente,
chiave unica delle viste ordinate; convalide a elenco su Stato e Decisione_Stato.

**Rischi in osservazione (D-79).** Foglio di lavoro **Osservazione**: righe 6-25 i
rischi in osservazione per Ordine_Osservazione (AGGREGATE(14) + MATCH) con
dimensioni, score, motivo, orizzonte, segnale, descrizione, validazione e notizie
di A3 (colonna O, `NW_Rischio_ID`); righe 27-38 entrati e usciti dal radar
(`RR_Movimento`); a destra da P4 due matrici driver x categoria (rischi in
osservazione con `COUNTIFS(RR_Ciclo,cicloCorrente,RR_Stato,"Osservazione",...)`;
rischi del radar con `COUNTIFS(ANA_Event_Type,...,ANA_Driver,"*"&codice&"*")`).
Pagina **Fenomeni** del report: riepilogo in A4 (nel radar con la capienza, in
osservazione, entrati, usciti, in uscita), rischi compatti in 7-26 (nome
`fenomeniLista`, altezze adattate da `prepara_report`) con "Imp · Prob · Pross ·
Vel", score, perche' fuori dal radar, orizzonte, segnale, driver, notizie; entrati
e usciti in 30-35 (`fenomeniUscite`). Nella griglia, sezione Rischi, colonne W
(stato con il motivo), X/Y (decisione sullo stato in vigore e gialla). Parametri
righe 65-75: `capienzaRadar` (15, da 1 a MAX_RISCHI), `sogliaProssimitaRadar`,
`sogliaProbabilitaRadar`, `cicliUscitaRadar` (gialli), `capienzaOsservazione` = 20
fisso, il testo della regola. Quadro: "Variati · nuovi (radar)" con sotto
entrati, usciti e in osservazione; Notizie: presidio "In osservazione" per una
categoria con soli rischi in osservazione. I dati di esempio hanno NFR-13, 14, 15
in osservazione (stato calcolato con `radar.py` dal generatore).

**Testata e guida (D-38, D-39).** Riga 1 = **fascia del titolo**: celle unite,
blu notte, testo bianco, formula `="Horizon Scan NFR — <titolo>   ·   "&etichettaCiclo`;
`etichettaCiclo` (Parametri!B57) = ciclo, data di riferimento (fine trimestre
con DATE/DAY/MONTH/YEAR, mai TEXT), "validato" o "da validare"
(`decisioniDaPrendere`), riservatezza (`ETICHETTA_RISERVATEZZA`). Riga 2 = la
**guida**: cella unita in rich text (`CellRichText`), prima riga in grassetto
con il **processo che aggiorna il foglio**, poi cosa contiene, come si legge,
cosa fare (dizionario `GUIDE`; per i fogli del report e' scritta per il
comitato). Colori per processo (`PROCESSI`): azzurro DDEBF7 trimestrale (A1,
A5), verde E2EFDA settimanale (A3), giallo FFF2CC validatore (= input), grigio
EDEDED calcolo. Altezze stimate dal testo (Excel non adatta celle unite).
**Tabelle dati dall'intestazione in riga 5** (dati dalla 6,
`PRIMA_RIGA_DATI`): riga 3 = **gruppi di colonne** consecutive dello stesso
autore ("A1 · ciclo trimestrale, poi validato", "Script · alla scrittura",
"Validazione · comando valida"...; `GRUPPO_CHI`); riga 4 = **significato** di
ogni colonna (chiave `significato` della mappa, obbligatoria); intestazione
colorata per chi scrive (`chi_colonna`); niente riquadri bloccati. In fondo ai
fogli del report la **legenda delle abbreviazioni** per esteso (`legenda()`).
Stile comune: costanti di colore (BLU_NOTTE 1F3864, ROSSO C00000, AMBRA FFC000,
scala delle dimensioni da F2F2F2 a C55A11),
`stile_grafico()`, `etichette_valore()`, `titolo_da_cella()` (titolo del
grafico = cella con il messaggio), `chip_urgenza()` (rosso AGIRE ORA, ambra
entro l'anno, grigio margine), `sezione()`.

**Regole di robustezza, tutte da errori reali:**
- Un **nome definito ASSOLUTO per ogni colonna** (prefissi RR_, AZ_, KRI_, NW_,
  VAL_, SI_; dalla prima riga dati, la 6, alla 20000; `MAX_RIGHE`), mai
  riferimenti strutturati nelle viste. Una formula che passa da riga del foglio
  a posizione nel nome sottrae `PRIMA_RIGA_DATI - 1` (elenco dei KRI:
  `ROW(KRI_KRI_ID)-5`). Anagrafica: `MAX_RISCHI` = **20** righe (D-55), nomi
  ANA_; nessun intervallo scritto per 15 o 20 righe a mano: tutto da
  `MAX_RISCHI`.
- **In un nome definito ogni intervallo ha il nome del foglio**
  (`COUNT(Delta!$AJ$5:$AJ$24)`): senza, Excel rifiuta di aprire il file.
- **Un testo fra virgolette dentro una formula e' al massimo 255 caratteri**:
  oltre, Excel non apre il file ("Errore nel metodo Open"). Testi lunghi
  calcolati (nota della scala del Delta) si spezzano con `"..."&"..."`.
- **Lo script e il collaudo leggono NOMI, mai celle**: `decisioniDaPrendere`,
  `statoValidazione`, `coperturaAnagrafica`, `coperturaValutati`,
  `statoCopertura` (Registro righe 4-5); `posID`...`posBadge`; `rmID`, `rmX`,
  `rmY`, `rmZ`, `rmMargine`, `rmUrgenza`, `rmPxI`, `rmLivello`,
  `rmMotivoLivello` (Radar_Mosca); `posLivello` (Registro, blocco);
  `presidioCodici`, `presidioStato` (Notizie); `quadroCommento`,
  `quadroSegnalati`, `deltaMotivi` (righe con testi calcolati); `valStato` e
  `VG_<oggetto>_<colonna>` (griglia del foglio Validazione, D-67).
- Criterio delle SUMIFS = esattamente l'ID corto.
- **#N/D (NA()), non zero**, per un valore mancante; e una formula che puo'
  restituire #N/D lo fa con **NA() esplicito** (`IF(ISNUMBER(INDEX(...)),INDEX(...),NA())`):
  il controllo degli errori dello script ammette solo il #N/D di una formula
  che contiene NA().
- Score_Composito (D-50) = media pesata delle dimensioni valutate, con
  guardia `IF(COUNT({Impatto},{Prossimita},{Probabilita})<3,"")` e ROUND a 2:
  numeratore e denominatore con `IF(ISNUMBER({Velocity}),pesoVelocity...,0)`;
  pesi da Parametri (B4:B7, somma controllata in B8/C8). Stato KRI con tre
  guardie, in quest'ordine: **"Soglie da definire"** se una soglia e' vuota
  (una cella vuota vale 0 e darebbe un falso Rosso), SOGLIE INVERTITE, poi
  "Non rilevato" se manca il valore.
- **Un valore facoltativo vuoto non e' zero**: nelle viste per rischio il
  COUNTIFS che precede SUMIFS ha anche `{campo},"<>"` (Registro, Delta,
  storia delle soglie negli Indicatori); la Velocity vuota si mostra "n.v.",
  la soglia vuota e' #N/D nel grafico.
- **Note SOPRA le tabelle** (righe 1-4), mai sotto.
- **Niente funzione TEXT** (dipende dalla lingua di Excel): numeri nei testi con
  `FIXED`; **niente formule matriciali**: elenchi ordinati con
  `MATCH(AGGREGATE(14|15,6,chiave,k),chiave,0)` su una chiave = valore meno (o
  piu') k/100000 per lo spareggio; filtri con `AGGREGATE(15,6,ROW(...)/(cond),k)`;
  `TEXTJOIN` su colonne di appoggio nascoste.
- **Formati condizionali con il colore di SFONDO** (`PatternFill(fgColor=c,
  bgColor=c)`): con il solo fgColor Excel lascia la cella bianca.
- Grafici: assi a **scala fissa** dove il confronto conta (0-5 score, -1/+1
  delta); **titolo e legenda con overlay=False**; `x_axis.delete=False`;
  `varyColors=False`; linee NON smussate con marcatori; **dati in colonne
  nascoste solo con `visible_cells_only=False`**; serie dinamiche su nomi
  `OFFSET(...)` scritte `[0]!nome`; **barre negative con
  `invertIfNegative=False`**; serie "per esito" (una barra per rischio in
  una sola serie) con **zero, non NA()**, dove il rischio non ha quell'esito e
  formato della cella `0.00;-0.00;;` (l'etichetta di un punto #N/D si vede;
  openpyxl non scrive sourceLinked="0", quindi il formato va sulle celle).
- **Blocco per posizione nel Registro** (colonne nascoste AA-AN, righe 9-28):
  per ogni posizione dell'anagrafica ID, nome, Impatto, Probabilita,
  Prossimita, Velocity, score corrente, del ciclo prima e di due cicli prima,
  segnali netti, etichetta dei segnali (`▲ +n`, `▼ n`, `● n` oltre
  `sogliaDirezione`), chiave d'ordine e posizione del k-esimo per score. Le
  colonne del blocco e della tabella visibile si calcolano da **elenchi di
  nomi** (`blocco`, `COLONNE_REGISTRO`), mai lettere scritte a mano: togliere
  Gap ha spostato tutte le colonne. Nomi `pos*`: tutte le viste li riusano.
- **Registro** ("il ciclo corrente"): righe 4-5 controlli (righe da validare
  = **oggetti** del ciclo, non campi: si conta il primo campo di ogni oggetto,
  D-67; rettifiche applicate, "CICLO NON ANCORA VALIDATO"/"Ciclo validato";
  rischi in anagrafica `COUNTIF(ANA_ID,"NFR-*")`, valutati nel ciclo, "CICLO
  INCOMPLETO"/"Ciclo completo"); riga 7 gruppi (Rischio, Dimensioni, Calcolati,
  Sup., KRI del ciclo, Notizie · 4 settimane, Banca, A5 e controlli,
  Anagrafica); riga 8 intestazioni; righe 9-28 un rischio per riga **ordinato
  per score**: ID (fondo = **livello di allerta**, formattazione condizionale
  dal blocco nascosto, colonna "Livello" = `posLivello`; nessuna colonna in
  piu', D-63), nome, event type, Imp, Prob, Pross, Vel ("n.v." se non
  valutata; colorate), score (barra dei dati 0-5), Δ sul ciclo prima e
  **Δ 6 mesi**, urgenza (chip), margine, ◆, KRI R/A/V, segnali netti (colonna
  R), **Presidio** (dall'anagrafica, colorato), **Rilievi** ("⚑ superato" o
  "n oss.", dalla colonna Rilievi del RiskRegister), owner; legenda.
- **Storico**: score degli ultimi otto cicli per rischio, linee, asse 0-5.
- **Indicatori**: a sinistra i KRI in vigore nel ciclo (AGGREGATE sulla
  colonna nascosta Z, conteggi per cinque stati compreso "Soglie da definire",
  valore del ciclo prima, tendenza; colonna L = **Tipo** del KRI, D-64); a
  destra la storia di un KRI scelto in **N4** (elenco `elencoKRI` = OFFSET sulla
  colonna nascosta AB con tutti i KRI mai definiti, presi dalla riga in cui
  Ciclo = Ciclo_Definizione; il nome in N5 riporta il tipo), valori e soglie sugli 8 cicli, grafico con soglie
  tratteggiate. Capacita': nomi costanti `capienzaKRICorrenti` (60) e
  `capienzaElencoKRI` (150), letti dallo script.
- **Notizie**: per event type intensita' massima, notizie >= 2, rischi in
  anagrafica, Presidio ("AREA NON PRESIDIATA"), conteggi per intensita';
  barre orizzontali **impilate** (mai un radar dell'intensita'); pressione su 12
  settimane; grafici **sotto** le tabelle; a destra (L4:S13) un **riquadro
  con la sintesi di A3 e i flag proposti della settimana corrente** (INDEX/MATCH
  di `settimanaCorrente` su `SE_Settimana`; D-66).
- **Piano_azioni**: prima le proposte da decidere, poi le azioni aperte di
  ogni ciclo, poi le chiuse (completate, respinte, annullate) del ciclo e del
  precedente, con UNA AGGREGATE su chiave `ROW + 1.000.000 x gruppo` e MOD;
  scadenza = EDATE(decisione, mesi) per le approvate o in corso; Stato colorato;
  colonne Ciclo, Rischio, ID azione, Azione, Owner, Orizzonte, Stato, Decisa
  il, Scadenza, Validazione (nessuna "Riduce", D-54);
  **capienzaPianoAzioni** = 150, controllata dallo script. La storia intera
  resta nel foglio Azioni.
- **Validazione** (D-67; anteprima `Anteprima_S1/Validazione_per_riga.xlsx`
  del 01/10, approvata dall'utente): la **griglia di lavoro** del
  validatore, quattro sezioni una sotto l'altra a capienza fissa (`GRIGLIA`:
  Rischi 20 = `MAX_RISCHI`, KRI 80, Azioni 100, Notizie 200), righe libere
  **nascoste**; riga 3 `valStato` = i periodi da validare. Una riga per
  oggetto: accanto a ogni proposta (fondo F2F2F2, testo grigio; "n.v." o "—"
  se vuota) la **cella gialla gia' compilata con la proposta**; owner e
  rischio su due colonne unite (C:D proposta, E:F valore); una Motivazione per
  riga (M); Respingi per KRI, azioni e notizie; Tipo del KRI, Settimana della
  notizia. Per i rischi **N Score composito e O Margine di Mosca** con le
  stesse formule del Registro e del Radar_Mosca applicate ai valori gialli e
  alle azioni non respinte della griglia (Y dalle colonne nascoste delle
  azioni, anni di adeguamento gialli o, se vuoti, quelli dell'anagrafica),
  testo "3,40 (era 3,10)" e urgenza colorata; colonne nascoste Q periodo, R
  appoggio (rischio: 1 = segnalazione da motivare, ⚑ davanti al nome; azione:
  il suo rischio), S-V calcoli. **P Segnalazioni dei controlli** (D-71, solo
  Rischi, larga 60, a capo, fondo FCE4D6 se contiene DA MOTIVARE): il testo
  della colonna Rilievi del RiskRegister del rischio, scritto dallo script in
  `ricostruisci_griglia`; P della riga del titolo dei Rischi
  (`VG_Rischio_SegnalazioniCiclo`) le segnalazioni sul ciclo (Rilievi_Ciclo). **Tutte le formule dentro IFERROR** (trappola
  71). Formati condizionali: cella gialla diversa dalla proposta arancio
  F8CBAD; Motivazione F4B183 se serve e ha meno di 10 caratteri; convalide
  (interi 1-5, decimale 0-30, elenchi). Nomi `VG_<oggetto>_<colonna>` per ogni
  colonna (`_P` per la proposta), `_righe`, `_titolo`: le lettere stanno solo
  in `GRIGLIA`, che deve avere gli stessi oggetti e campi della mappa (il
  generatore si ferma altrimenti). Nel template tutto e' validato: griglia
  vuota. "Dopo il commento" del Quadro conta i valori rettificati piu' gli
  oggetti respinti (un'azione respinta una volta, non per campo).
- **Dizionario** (pesi e soglie dell'esempio come formula `FIXED(pesoImpatto,2)&...`,
  mai scritti nel testo): una riga per ogni colonna di ogni tabella (dalla mappa: chi
  la scrive colorato per processo, significato, come si calcola da `COME`,
  valori da `VALORI`, esempio dai dati di esempio), piu' i valori calcolati
  nelle viste (`CALCOLATI`) e parametri e anagrafica (`PARAMETRI_DIZ`).
- **Radar_Mosca**: tabella per rischio (Impatto, Probabilita, P x I,
  Prossimita, Z, X, Y, Margine, Urgenza, settore, angolo, raggio =
  MAX(0,6; MIN(6; margine + 2)), x, y, attenzione del supervisore; **U-AB
  livello di allerta**, D-63: U F1 AGIRE ORA, V F2 KRI in rosso, W F3 segnali
  netti >= `sogliaDirezione` (da `posNetti`), X A1 P x I >= `livelloPxI`, Y A2
  presidio Assente, Z A3 KRI in ambra o rosso >= `livelloQuotaKRI` dei KRI in
  vigore, 1/0; **AA livello** = Attivazione se F1+F2+F3 >= `livelloForti`,
  Attenzione se almeno uno o se margine < `livelloMargine` con un aggravante,
  Monitoraggio altrimenti, vuoto se il rischio non e' valutato; **AB motivo**
  con TEXTJOIN, senza numeri; nomi `rmLivello`, `rmMotivoLivello`) e grafico a
  **DISPERSIONE** costruito da `grafico_radar(ws, base, piccolo)`, che scrive
  l'appoggio nel foglio stesso (colonne nascoste da `base`: 30 nel
  Radar_Mosca, dopo le colonne del livello; 60 nel Quadro) e
  legge i valori da Radar_Mosca: quattro cerchi (Mosca rosso, 1 anno grigio
  **tratteggiato**, 2 e 3 anni grigio chiaro), raggi dei settori, etichette
  dei settori su due righe (codice e nome della categoria, `NOMI_SETTORI` =
  TASSONOMIA, nove settori, D-74; legende sotto il radar in una fascia aggiunta,
  `SOTTO_RADAR`, altezza del grafico in proporzione; nel radar piccolo del Quadro
  nessuna legenda, i colori nella legenda del Quadro); **una serie
  per ogni valore di P x I** (14) **per ciascun livello di allerta** (42; riga
  3 dell'appoggio = livello; dal 01/10, D-63: prima la serie era raddoppiata per
  l'attenzione del supervisore con il bordo giallo, D-35); marcatore di lato 10
  x radice del valore (AREA proporzionale a P x I), riempimento del colore del
  livello (`LIVELLI`: E06666 rosso, F6C342 giallo, 93C47D verde, colori usati
  solo li') **semitrasparente** (openpyxl non scrive l'alpha: la funzione
  `trasparenza` lo aggiunge nell'XML dei grafici, una volta per colore, con
  tentativi ripetuti se l'antivirus trattiene il file), bordo sottile grigio; una
  serie per rischio per l'etichetta con l'ID e **◆ se il tema e' all'attenzione
  del supervisore**; legenda nel grafico (tre cerchi dei livelli, sotto la
  linea rossa "AGIRE ORA: X + Y > Z", aree di riferimento 4, 12, 25). Assi +-7,6
  nascosti.
- **Classifica** (righe 5-24): T chiave, U posizione; visibili pos., ID, nome,
  score, score del ciclo prima, Δ, esito, urgenza (chip), margine, owner,
  etichetta "ID ▲/▼/●/○ nome". Titolo del grafico dalla cella AL2 ("2 da
  affrontare subito: NFR-01, NFR-11"). A sinistra **barre orizzontali**
  ordinate (tre serie sovrapposte per esito, etichetta del valore), a destra
  la **lente di Mosca ordinata per margine** (colonne impilate X grigio, Y
  entro Z arancio, Y oltre Z rosso, rombo Z; etichette "ID (±margine)";
  `colonne += rombi`). Una pagina di stampa.
- **Matrice**: 5 x 5 Probabilita (righe) x Impatto (colonne, da "Limitato" a "Critico"), fondo per fascia
  di P x I (verde fino a 6, ambra 8-12, rosso da 15), in ogni cella gli ID con
  `TEXTJOIN` su 25 colonne nascoste (codice cella P*10+S); sotto i rischi dal
  piu' grave; descrittori delle scale ai margini (Probabilita da "Remota" a
  "Quasi certa", D-52).
- **Delta**: appoggio nascosto (delta di Impatto, Probabilita, Prossimita,
  Velocity, Score per posizione, solo se il valore c'e' in
  entrambi i cicli; indici del blocco con nomi, non numeri; ordine dal
  maggiore aumento); barre orizzontali **ordinate** in tre serie (in aumento
  rosso, in diminuzione blu, invariato grigio; asse **-1,5/+1,5 passo 0,5**:
  quando la Velocity entra o esce i pesi si ridistribuiscono; titolo
  "n in aumento, n in diminuzione, n invariati"); **a fianco, nello stesso
  ordine, il motivo** (JSON delle Variazioni reso leggibile con SUBSTITUTE
  annidati: "• Impatto 3 → 4: evidenza (data)", anche "• severity" dei cicli
  scritti prima del 30/09 sera; "Invariato: nessuna evidenza
  nuova..."; "Rischio nuovo nel ciclo."; " null → " diventa " n.v. → ");
  righe dei motivi senza esempio alte 3 punti nel template (20 righe da 30
  punti non stanno in pagina con il grafico); sotto la **scala spiegata** con
  una **formula** che calcola dai pesi di Parametri quanto vale un punto di
  ogni dimensione, con e senza Velocity (`FIXED`; mai pesi scritti nel testo)
  e il dettaglio per dimensione con la nota (AGGREGATE che ignora i #N/D:
  "viola la rubrica", "Velocity non valutata in uno dei due cicli");
  interruzione di pagina fra le due parti.
- **Quadro** (quadro d'insieme, prima pagina del report; colonne A-O larghe
  10,5): cinque riquadri (rischi valutati su anagrafica, **livello di allerta
  "n · m"** = in attivazione · in attenzione, con gli ID in attivazione e il
  numero in monitoraggio (T4 nascosta = in attivazione; D-63), variati · nuovi,
  KRI in rosso, validazione ✓ o decisioni mancanti); primi cinque della Classifica (score con barra, Δ, urgenza chip,
  ◆); **matrice piccola** con i soli numeri; **radar di Mosca piccolo** (8,5
  cm, appoggio nel foglio stesso) con l'elenco dei rischi a fianco (righe da
  12 punti: 20 rischi nella prima pagina); interruzione di pagina. Pagina 2:
  **commento di A1** diviso in "Messaggio
  chiave" e "Decisioni richieste" (SEARCH del marcatore "DECISIONI:"; senza
  marcatore tutto nel messaggio), controllo indipendente (A5 e osservazioni),
  "Dopo il commento" (avviso se sono state applicate rettifiche o
  respingimenti, fondo ambra), **"Rilievi di A5 superati"** (da
  `SI_Rilievi_Superati`: chi, quando, perche', fondo ambra; D-56);
  `quadroCommento` = cinque righe; **"Rischi segnalati e perche'"**: primi tre per
  score, **in attivazione o in attenzione**, variati, nuovi, in ordine di
  classifica, con il **livello** (chip dei colori del radar), il **perche'
  calcolato dal foglio** (posizione e score, X + Y contro Z con gli anni di
  adeguamento, margine sotto l'anno, variato e verso, attenzione del
  supervisore, presidio assente, KRI rossi, notizie oltre la soglia) e cosa e'
  cambiato; bordi
  solo sulle righe piene (formattazione condizionale); limiti letti in
  generazione da `04_Riferimenti/controlli_e_model_risk.md`, sezione 5; legenda. Stampa a scala 78%,
  margini ridotti: pagina 1 il quadro, pagina 2 commento e segnalati; con
  molti rischi segnalati la scala la riduce `prepara_report` (fino al 60%)
  perche' resti in due pagine.
- **Metodologia**, in sezioni colorate per processo: chi produce i numeri
  (anche A6 e le schede), fonti ed evidenze, analisi per dimensioni, score
  composito con i pesi come riferimenti a Parametri (quattro, Velocity "se
  valutata"; somma da B8), presidio dei controlli spiegato come giudizio della
  Banca fuori dallo score, un rischio per meccanismo di perdita, scale e regole di
  variazione lette dalla rubrica, Mosca, **livello di allerta** (regole con i
  parametri letti da Parametri), KRI (due, Esposizione ed Evoluzione), **come si leggono i grafici**
  (Classifica, lente, radar, Matrice, Delta), validazione.
- **Guida**: a cosa serve, tabella "chi aggiorna cosa e quando" (`CHI_AGGIORNA`:
  report, lavoro, dati, file a parte; colonne settimanale / trimestrale /
  validatore / a cosa serve), **quando si lanciano A5 e A6**, dove si scrive a
  mano (Validazione, celle gialle di Parametri, Stato delle Azioni, N4 degli
  Indicatori), regole, primo uso.
- **Stampa** dei sette fogli del report: A4 orizzontale (Radar_Mosca
  verticale), 1 pagina in larghezza, intestazione con foglio, "Uso interno" e
  "Horizon Scan NFR", piede con file e pagina.
- **Parametri**: quattro pesi in B4:B7 (Impatto, Probabilita, Prossimita,
  Velocity; somma in B8), soglie (direzione 2, Delta 0,30: D-61), Z per
  Prossimita in B51:B55 (3,5, 2,5, 1,5, 0,5, 0: D-59), ciclo corrente e precedenti, 8 cicli
  del trend, settimana corrente e finestra, 12 settimane, urgenza (moscaX,
  moscaYDefault, anniProssimita), etichetta del ciclo (B57), **livello di
  allerta** in B60:B63 (`livelloPxI` 12, `livelloQuotaKRI` 0,5,
  `livelloMargine` 1, `livelloForti` 2: D-63), tassonomia,
  driver, anagrafica **H..O** (ID, Nome, Event_Type, Driver azzurre; Owner,
  **Anni_Adeguamento** con convalida decimale 0-30, **Attenzione_Supervisore**
  Sì/No e **Presidio_Controlli** a elenco Non verificato/Adeguato/Parziale/
  Assente, gialle: input del validatore conservati dalla scrittura; M lo
  scrive anche `valida` dalla stima di A1, D-60). Radar_Mosca
  J = `MAX(y delle azioni o riserva, N(Parametri!M))`. **Stampa di Registro
  e Parametri** (D-62): A4 orizzontale, tutte le colonne in una pagina di
  larghezza (Registro A-T con le righe 7-8 ripetute; Parametri A-O).
- Stati delle azioni: Proposta — da valutare, Approvata, Respinta, In corso,
  Completata, **Annullata** (rischio dismesso).

**Dati di ESEMPIO** (fondo grigio): una riga di Sintesi_Cicli per ciclo (il
commento del 2026Q2 nella forma "MESSAGGIO: ... DECISIONI: ..."); **NFR-11
con 3 anni di adeguamento** (AGIRE ORA nell'esempio); **NFR-01, 02, 07, 09
all'attenzione del supervisore**; **12 rischi** su tre cicli (2025Q4-2026Q2),
nessuno su L1-03 (l'area che la catena di prova scopre e copre), tre entrati a
meta' storia; storico KRI su tre cicli, **due KRI per rischio, uno di
Esposizione e uno di Evoluzione** (D-64; NFR-02: K1 esposizione, K2
evoluzione, che la catena di prova sostituisce nel 2026Q3 con NFR-02-K3);
12 azioni validate (una Respinta); con le soglie del template il livello di
allerta d'esempio e' 1 Attivazione, 6 Attenzione, 5 Monitoraggio;
notizie con codici fonte, **mai una fonte esclusa** (le notizie dal comunicato
di un fornitore cloud usano `MAN`, D-28). Validazione del 2026Q2 gia'
applicata con una rettifica di rischio, una di KRI e un'azione respinta
(Periodo di una notizia = lunedi' in cui A3 l'ha valutata). Il registro vero
NON si ricava a mano da questi esempi: comando `inizializza`. Rispettano la
rubrica (il collaudo li sottopone a C1-C5 e confronta l'esito con quello che
calcola lo script) ed esercitano i casi limite: delta sopra soglia nei due
versi, i tre stati dei segnali netti, KRI Verde/Ambra/Rosso/Non rilevato e
**Soglie da definire** (NFR-10-K1), **Velocity non valutata** (NFR-10), una
variazione della Velocity (NFR-01 da 4 a 5 nel 2026Q2), **fonti con la
rilevanza** (almeno una di rilevanza 3 per ogni rischio con Prossimita 4),
**anni di adeguamento** nella colonna del RiskRegister (NFR-11: 3), **presidi** Adeguato, Parziale,
Assente e Non verificato, un **rilievo di A5 superato** (NFR-12 nel 2026Q2,
con motivazione del validatore), fonti mai datate dopo il ciclo. Tuple della
storia (impatto, vel, pross, esito, var); azioni senza dimensione.

`costruzione_manuale_template.md`: come rifare il template a mano; ogni formula
citata deve esistere identica nel template (il collaudo lo verifica).

## LO SCRIPT DI CAMPO (07_Senza_Studio)

Nessuna API Graph, nessuna registrazione app, nessun ruolo admin: file in
cartelle SharePoint sincronizzate con OneDrive. Requisiti: Windows, Excel
desktop, Python 3.10+, pywin32, pypac (solo per la raccolta notizie),
openpyxl (solo per il file delle schede). Moduli:
- `excel_com.py`: sessione Excel dedicata e invisibile (DispatchEx), apertura
  in sola lettura o scrittura (in scrittura `AutoSaveOn = False`, D-83), ricalcolo
  completo, ricerca degli errori di formula (#N/D voluto ammesso), rilevazione del
  file aperto da altri;
  **nuovi tentativi** (fino a 5, attesa crescente) sugli errori COM transitori
  di avvio (CO_E_SERVER_EXEC_FAILURE, RPC_E_CALL_REJECTED): senza, la catena
  falliva a caso 2 volte su 3.
- `valida_output.py`: validatore JSON Schema **generico** (interpreta lo
  schema, non ne ricopia le regole), solo libreria standard; UNO solo. Legge i
  file in `utf-8-sig` (il Blocco note puo' salvare "UTF-8 con BOM").
- **Ogni testo scritto in cella passa da `per_cella`** (apostrofo iniziale):
  via COM un testo "=..." diventa formula (un titolo da un feed esterno), "5/6"
  una data, "0012" il numero 12. Verificato su Excel.
- Un file dell'agente mancante o che non e' JSON e' un **fermo** (codice 1),
  non un errore tecnico.
- **Registro unico** in `esegui_ciclo_locale.py` (D-79): in `scrivi_trimestrale`,
  prima di tutto, `radar.stati` sui rischi di A1 e su quelli che si riportano (in
  osservazione non toccati; nello straordinario quelli del radar non rivalutati),
  con `stato_prima_di` e `ingresso_radar`; fermo oltre `max_osservazione`; KRI e
  azioni solo per `payload_radar`; i KRI di chi esce In_Vigore "No"; anagrafica
  compattata per chi esce e `upsert_anagrafica` con owner e anni dalla sua ultima
  riga per chi entra; i riportati ricopiati con il loro Periodo_Valutazione.
  `applica_validazione` ricalcola con `stati_del_ciclo` e `applica_stati` sui
  valori validati (anche dopo `riapri`); `controlla_valore` accetta Decisione_Stato
  Automatico / Radar / Osservazione; `estrai_baseline` aggiunge
  `rischi_in_osservazione` (con notizie_a3 e flag_a3), lo stato dei rischi e
  `regola_radar`; `dismetti` vale anche per un rischio in osservazione (riga
  Dismesso). `aggiorna-registro` converte le voci "In osservazione" di
  `tblOsservazione` in rischi in osservazione con un codice NFR libero (valori
  provvisori) e confronta la baseline senza `rischi_in_osservazione` e
  `regola_radar`. Storia (fino al 2026-10-08b), **lista di osservazione** (D-73): `voci_osservazione`
  (voci di A1 con codice nuovo = primo OSS-nn libero mai usato, Esito, Stato,
  Prima_Osservazione, Validazione "Da validare"; poi le voci "In osservazione" del
  ciclo prima non toccate, riportate con Esito Invariata e Validazione vuota),
  scritte in `scrivi_trimestrale` dopo tblSintesi; in validazione solo le voci
  con Esito diverso da Invariata; `controlla_valore` (impatto 1-5, orizzonte 1-20,
  plausibilita' nell'elenco); Respingi = Si': voce nuova -> Stato Respinta, voce
  esistente -> valori, segnale e stato del ciclo prima; `estrai_baseline` aggiunge
  `osservazione` (voci "In osservazione" del ciclo corrente; [] per un registro
  senza la tabella); `spiegazioni.raccogli` la mette in `Ciclo.txt` con le
  decisioni del validatore.
- `controlli_a5.py` (dall'08/10, D-79, `stati_previsti` con la regola della baseline:
  KRI o azioni su un rischio in osservazione, riscritto senza fonte nuova, senza
  orizzonte o segnale = Osservazione; rischio che entra senza KRI o azioni = Da
  motivare; rischio del radar senza = Bloccante; piu' di 20 in osservazione = C1
  Bloccante; `controlla_osservazione` non c'e' piu'. Storia, dal 07/10 `controlla_osservazione`, dentro `controlla`:
  oss_id coerenti con la baseline e con l'esito, codici ripetuti, promosso_a solo
  con esito promossa e solo verso un rischio nuovo del ciclo, al massimo 30 voci
  dopo il ciclo = **C1 Bloccante**; rischi toccati inesistenti, voce nuova entro 2
  anni e in crescita = C1 Osservazione; fonte dopo la data di riferimento, voce
  aggiornata senza una fonte nuova = C5 Osservazione): C1, C2, C3, C5, C7, C9 per intero; C6 e C8 euristici,
  **solo Osservazione** (D-54; l'owner persona lo ferma `valida`, con la regola
  unica `sembra_persona` e l'elenco `PAROLE_FUNZIONE`, ampliato il 30/09 con
  procurement, acquisti, immobili, infrastrutture, tecnologia, organizzazione,
  operativa/o, controlli, business); lavorano sul payload COSI' COME L'HA
  SCRITTO A1 (senza esito ne' da/a): `DIMENSIONI` = impatto, probabilita,
  prossimita, velocity; C5 "Fonti" (D-58: data dopo il ciclo = Bloccante;
  Probabilita 5 o Prossimita 4-5 senza una fonte di rilevanza 3 e fonti perse
  con i valori invariati = Osservazioni); C2 = una variazione per ogni valore cambiato
  (`_diversi`: None contro 3 e' un cambio); C3 "una Velocity prima null entra
  con qualunque valore"; C6 aumenti su piu' di meta' dei rischi senza fonti
  nuove; C7 solo KRI sconosciuti o ripetuti; C8 anche un'azione con la stessa
  descrizione (`_stesso_testo`: minuscole, spazi compressi, senza punto finale)
  di un'azione aperta dello stesso rischio nella baseline = Osservazione che
  cita l'id dell'azione aperta (D-69); C9 **due KRI, uno per tipo**
  (`TIPI_KRI`, Bloccante), tipo diverso da quello della baseline per un KRI in
  vigore = Osservazione, soglie entrambe o nessuna, KRI in vigore non
  riproposto = Osservazione. **C4 dichiarato non
  coperto**. `combina(meccanico, agente, supera_agente=False)` restituisce
  esito, rilievi (con `origine` script o A5) e `superati`: con
  `supera_agente` (D-56) i Bloccanti di A5 non fermano, quelli dello script
  si'. Lo script NON sostituisce A5: senza l'esito dell'agente si ferma.
- `fonti.py`: unico lettore di `fonti.md` (script, prompt, collaudo).
- `input_a1.py` (D-69, solo libreria standard): `testo_kernel` (file senza
  righe `>` e senza titolo `# `), `testo_controlli(kernel)` (unico lettore di
  `controlli_A5.md`, usato anche da `componi_prompt.py`), `nome_file`
  (`Input_A1_<ciclo_da_valutare>.txt`), `componi(baseline, kernel, oggi)` ->
  (testo, file mancanti): intestazione, "=== 1. BASELINE ===" con il JSON
  (indent 2), "=== 2. CONTROLLI ===" con una frase ("Prima di rispondere
  verifica ogni rischio con questi controlli e correggi...") e i controlli,
  "=== 3. GUIDA DI SCRITTURA ==="; un file del kernel mancante toglie la sua
  parte e non ferma niente. `scrivi(cartella, ...)` scrive il file e toglie gli
  `Input_A1_<AAAAQn>.txt` e `Input_A8_<AAAAQn-Sk>.txt` degli altri periodi (solo quelli con quel nome; un file
  aperto resta). **Nomi degli allegati (D-84)**: sempre `Input_<agente>`; `Input_A8_<periodo>.txt` per lo
  straordinario (intestazione "INPUT DI A8"); `Input_A3_A4.txt` unico per A3 e A4 (`scrivi_allegato_a3_a4`, toglie
  i vecchi `Input_A3.txt` e `Input_A4.txt`); `Input_A5_<ciclo>.txt` (`componi_a5`, `leggi_a5`: "=== 1. OUTPUT DI A1
  ===" e "=== 2. BASELINE ===") scritto da `precontrollo` quando nessun punto e' da correggere e tolto quando ce ne
  sono; `Input_A6_<ciclo>.json` in `Cicli/<ciclo>/` (`NOME_A6`, prima `Schede_input_`). `_scrivi_baseline` lo chiama a ogni baseline scritta
  (`baseline`, `trimestrale`, `valida`, `dismetti`) e avvisa se mancano file
  del kernel; con `baseline --uscita` no.
- `input_a1.leggi_baseline(testo)` (D-70): il JSON della parte 1
  dell'allegato (`raw_decode` dalla prima `{` dopo "=== 1. BASELINE ==="),
  ValueError se la parte manca; la usa lo script della skill, che riceve solo
  l'allegato.
- `precontrollo.py` (D-69; modulo a parte dal 05/10, D-70, solo libreria
  standard e moduli senza Excel, importato da `esegui_ciclo_locale.py`):
  `precontrolla(payload, baseline, schema)`, `messaggio_correzione(ciclo, esito)`,
  `conta(esito)` (da correggere, da verificare), `ciclo_di(payload, baseline)`,
  `riga_esito(ciclo, esito)` (prima riga, uguale nel comando e nella skill) e
  `impronta(payload)` (primi 12 caratteri dello SHA-256 del JSON con chiavi
  ordinate, senza spazi: indipendente da a capo e ordine dei campi; il comando
  la stampa nella seconda riga). `precontrolla`: schema (se fallisce, niente controlli:
  lavorano su campi garantiti), `controlli_a5.controlla`, forma (parti del
  razionale attese, ADEGUAMENTO solo con anni_adeguamento; EFFETTO in ogni
  azione e KRI), **una riga per rischio** ("razionale senza le parti ...;
  EFFETTO: mancante nel razionale di azioni 1, 2; KRI di Evoluzione e di
  Esposizione"): una riga per azione o KRI dava 51 righe con un A1 nel formato
  di prima, un messaggio che nessuno incolla. Messaggio: richiesta di restituire l'intero JSON, poi blocchi
  "Schema", "Da correggere (fermerebbero il ciclo)", "Da verificare (correggi se
  fondati; se confermi, spiega il perche' nel razionale)", "Forma dei testi",
  righe "NFR-01 · C9: ...". Comando `precontrollo --payload [--baseline]`:
  baseline di default `Baseline_corrente.json` della cartella di uscita (senza:
  fermo con "Lanciare prima: ... baseline"); non apre Excel e non richiede il
  workbook (`main` lo esenta dal controllo "Workbook non trovato"); scrive
  `Cicli/<ciclo>/Correzione_A1_<ciclo>.txt` se c'e' qualcosa, lo cancella se
  l'output e' pulito; restituisce 1 con punti da correggere, 0 altrimenti
  (`main` restituisce il codice del comando, `codice or 0`).
- `schede.py` (D-40): `input_schede` (dal registro validato, via COM: per ogni
  rischio valutato, in ordine di classifica, valori, score e score del ciclo
  prima, urgenza da `rm*`, segnali netti da `posNetti`, variazioni, fonti,
  azioni del ciclo o aperte, KRI in vigore con valore del ciclo prima, storia
  degli ultimi otto cicli; numeri arrotondati; dal 02/10, D-68,
  `razionale_rischio` e `motivazioni` da `parti_razionale` e, per azioni e KRI,
  `razionale` ed `effetto_atteso` da `parti_effetto`); `parti_razionale`
  (etichette RISCHIO, IMPATTO, PROBABILITA, PROSSIMITA, VELOCITY, ADEGUAMENTO,
  con o senza accento o apostrofo: valgono all'inizio del testo o dopo un
  punto, un punto e virgola o un a capo, in maiuscolo anche ovunque dopo uno
  spazio; "Impatto resta 4:" a meta' frase NON e' un'etichetta; testo prima
  della prima etichetta = "altro"; nessuna etichetta = {} e il razionale resta
  intero) e `parti_effetto` (EFFETTO: o EFFETTO ATTESO:); `controlla_a6` (ciclo, stessi
  rischi senza ripetizioni, quattro dimensioni (`DIMENSIONI` = impatto,
  probabilita, prossimita, velocity), fonti identiche, **numeri**: ogni
  numero dei testi, estratto con `\d+([.,]\d+)?` e confrontato per valore
  — 10/06/2026 e 2026-06-10 coincidono, 4,2 = 4.2 — deve stare nei dati del
  rischio, nella rubrica, nel ciclo o essere 1-5); `scrivi_file_schede`
  (openpyxl, Python puro: indice con collegamenti e una scheda per rischio con
  intestazione, etichette, poi in quest'ordine (D-68): "Il rischio"
  (descrizione estesa di A6 o descrizione di A1); senza A6 il **"Razionale: il
  fenomeno in termini di rischio"** (parte RISCHIO; "Razionale (registro)" con
  il testo intero se non e' diviso); tabella dei valori con, nella colonna C
  unita fino a H, **"Perche' questo valore: informazioni e documenti"**
  (spiegazione di A6 o motivazione di A1; senza nessuna delle due, una nota che
  rimanda al Razionale) — "n.v." per la Velocity non valutata —, presidio dei
  controlli, formula dello score con i pesi ridistribuiti; urgenza con il motivo
  degli anni di adeguamento (parte ADEGUAMENTO); cosa e' cambiato; andamento
  con tabella di sette colonne e grafico; fonti con "a sostegno di"; **azioni**
  (riga dell'azione: descrizione A:E, owner F:G, orizzonte · stato H) e **KRI
  in vigore** con semaforo e "Soglie da definire", ciascuno seguito da una riga
  "Perche'" (A:D) / "Effetto atteso" (E:H) su fondo F7F9FC ("non indicato nel
  razionale di A1" se manca EFFETTO); legenda; stampa verticale).
- `raccogli_notizie.py` (W0 locale): legge i feed rss delle fonti `approvata`
  (`--anche-da-validare` per le prove), finestra di 7 giorni, parole
  `escludi`, `max_voci`, doppioni via `News_Inbox/_visti.json`, voci senza data
  con la data di prima raccolta dichiarata; scrive
  `News_Inbox/<lunedi'>/Raccolta_<data>.txt` (ogni voce con il codice fonte) e
  crea `Manuali/`; una fonte irraggiungibile e' dichiarata in testa al file e
  non ferma le altre. Scarica con urllib, ma **il proxy lo sceglie `pypac`**:
  nelle reti aziendali il proxy e' spesso un file di autoconfigurazione (PAC)
  che il browser legge e urllib no. Visto sul PC della Banca: i domini
  `europa.eu`, instradati dal PAC sul proxy, andavano in timeout dallo script
  pur aprendosi nel browser. Il PAC si scopre **una volta sola** (cache) e con
  `pac_context_for_url` si instrada ogni fonte; senza PAC il comportamento e'
  quello di prima. L'import e' in testa al modulo, la scoperta avviene solo alla
  prima richiesta vera: i test che iniettano feed finti non toccano la rete.
- `esegui_ciclo_locale.py`: **controllo di versione** all'apertura di ogni
  comando (`controlla_versione`: nome `versioneTemplate` del workbook =
  `VERSIONE_TEMPLATE`, altrimenti fermo con l'indicazione di
  `aggiorna-registro`) e della mappa (`carica_mappa`: `versione_template`);
  anagrafica scritta **dalla mappa** (`upsert_anagrafica` risolve le sorgenti:
  payload o derivati che conservano Owner, Anni_Adeguamento,
  Attenzione_Supervisore e Presidio_Controlli: `attenzione_supervisore_esistente`,
  D-35; `presidio_esistente_o_non_verificato`, D-49);
  `svuota_registro` lascia gialle (input) le colonne Owner, Anni_Adeguamento,
  Attenzione_Supervisore e Presidio_Controlli dell'anagrafica;
  **`completa_payload(payload, baseline)`** (D-51), chiamata all'inizio di
  `scrivi_trimestrale` (dopo i controlli, che vedono il payload com'e'): toglie
  dai riferimenti delle fonti i codici dello strumento di ricerca
  (`CODICE_RICERCA`, `turn1search17` e simili; `pulisci_riferimento` non
  lascia un riferimento vuoto), calcola `_esito` (Nuovo se l'id non e' nella
  baseline; Variato se cambia una delle `DIMENSIONI_ESITO` — Impatto,
  Probabilita, Prossimita, Velocity —, da vuota a un valore compreso;
  altrimenti Confermato) e aggiunge `da`/`a` alle variazioni; idempotente;
  **`testo_rilievi(stato, id_rischio)`**: i rilievi di A5 e dei controlli di un
  rischio (o del ciclo, id None), uno per riga `[controllo · gravita' ·
  origine] testo`, con BLOCCANTE SUPERATO per i Bloccanti superati;
  `prepara_report` prima di ogni salvataggio: `adatta_altezze` sulle righe
  di `quadroCommento`, `quadroSegnalati` e `deltaMotivi` (per ogni cella con
  testo, unita o no: righe stimate dalla larghezza dell'area unita e dalla
  dimensione del carattere; riga senza testo quasi nascosta) e
  `spazio_per_il_grafico` (la riga sotto i motivi del Delta si allunga finche'
  il grafico accanto non copre la nota sulla scala) e `scala_quadro` (01/10:
  scala di stampa del Quadro fra 60% e 78%, calcolata dall'altezza delle due
  pagine e dall'altezza utile dell'A4 orizzontale, perche' Limiti e legenda
  non finiscano soli su una terza pagina); se fallisce
  avvisa e non ferma. Letture dal workbook **solo per nome**
  (`copertura_foglio`, `segnali_sopra_soglia`, `aree_non_presidiate`,
  `colonna_nome`). JSON delle liste (variazioni, fonti) scritto con le chiavi in
  ordine fisso (`ordina_chiavi`: dimensione, da, a, evidenza, data_evidenza;
  riferimento, data, tipo): le formule del Quadro e del Delta ci contano.
  Capacita' del Piano_azioni controllata prima della scrittura
  (`capienzaPianoAzioni`). Comandi:
  - `precontrollo --payload A1.json [--baseline file]` (D-69): vedi
    `precontrolla` sopra; prima di A5, senza Excel. **Facoltativo, si puo'
    saltare**: `trimestrale` fa gli stessi controlli e, se ferma, scrive lo
    stesso messaggio per A1. Guida, LEGGIMI, workflow, help del comando e
    messaggio dello straordinario lo dicono (09/10, richiesta dell'utente).
  - `baseline`: esporta `Baseline_corrente.json` **e .txt** e l'allegato di A1
    `Input_A1_<ciclo>.txt` (D-69; stampa "Allegato per A1: ...") (input di A1, A3,
    A4, A5: rischi con impatto, velocity — null se non valutata —, prossimita,
    probabilita, **presidio_controlli**, **anni_adeguamento** (dall'anagrafica),
    esito_precedente, fonti (con la rilevanza),
    storico di due cicli; niente gap_controlli; KRI in vigore nel ciclo
    corrente; azioni aperte); avvisa se il ciclo non e' validato.
  - `trimestrale --payload A1.json [--challenger A5.json]` (A5 **facoltativo**,
    D-71): si ferma se il ciclo precedente ha decisioni "Da decidere"; valida lo
    schema; controlli meccanizzati con **tre gravita'** (`controlli_a5.py`):
    **Bloccante** solo per l'integrita' (C1, C2, C7, identificativi dei KRI di
    C9) -> fermo e `Cicli/<ciclo>/Correzione_A1_<ciclo>.txt` (lo stesso
    `messaggio_correzione` del precontrollo); **Da motivare** C3 (date, frasi
    generiche, salto di piu' di un punto), date delle fonti di C5, coppia e
    soglie dei KRI di C9; **Osservazione** il resto. L'esito di A5, se c'e',
    deve essere **dello stesso ciclo** e citare solo rischi dell'output di A1;
    `combina` trasforma i suoi Bloccanti in "Da motivare" e non ferma mai per
    A5. `Esito_controlli_<ciclo>.json` ha `da_motivare` e `a5_usato`; a video
    "A5: usato / non usato (facoltativo)" e "SEGNALAZIONI DA MOTIVARE: n su m
    rischi". `--procedi-con-rilievi`, `--motivo`, `--decisore` restano accettate
    (nascoste nell'help) e stampano che non servono. Senza A5 la Sintesi_A5 dice
    "A5 non usato in questo ciclo". Colonna Rilievi: una riga per segnalazione,
    `⚑ DA MOTIVARE · C3 · controlli: testo` o `Osservazione · C8 · A5: testo`,
    prima le da motivare; `da_motivare(testo)` riconosce anche il vecchio
    BLOCCANTE SUPERATO; Rilievi_Superati = "Segnalazioni da motivare in
    validazione: n (controlli x, A5 y)." Avvisa quando
    l'anagrafica ha 2 posti liberi o meno e, dopo la scrittura, quando un
    razionale non e' diviso in parti ("Avviso per le schede", D-68: istruzioni
    di A1 non aggiornate; non ferma); si ferma prima di superare le
    capacita' delle viste; scrive: **fotografia dei KRI in coda allo
    storico** (KRI in vigore ripresi con il valore riletto ORA, mai ricopiato;
    non riproposti -> In_Vigore No nella riga del ciclo; nuovi col primo
    progressivo libero del rischio, mai per posizione, mai riusati), anagrafica
    (rischi nuovi con Owner "Da assegnare" e presidio "Non verificato") PRIMA
    del registro, append di RiskRegister (con **Rilievi** per rischio), Azioni e
    **Sintesi_Cicli** (sintesi di A1, sintesi di A5, osservazioni,
    Rilievi_Ciclo, Rilievi_Superati "Rilievi bloccanti di A5 superati: n, da
    <decisore> il <data>. Motivo: ...") relativo alla TABELLA (ListRows.Add);
    un KRI riproposto **senza soglie** conserva quelle in vigore (D-53); righe "Da
    decidere" nello storico (tblValidazione), ciclo corrente, e griglia del
    foglio Validazione ricostruita (`ricostruisci_griglia`, conserva cio' che il
    validatore ha gia' scritto); ricalcola; verifica formule
    integre, zero errori, copertura calcolata in Python = foglio, ciclo
    completo; SOLO ALLORA backup e salvataggio; archivio.
  - `settimanale --payload A3.json`: valida, sette impatti per notizia, lunedi',
    id non ripetuti nell'output, codici fonte nell'elenco e non esclusi, rischi
    collegati e dei flag esistenti; append
    senza duplicati; **riga di Sintesi_Settimane** (sintesi e flag di A3,
    aggiornata se la settimana esiste gia', D-66); righe di validazione delle
    notizie e griglia ricostruita (oltre la capienza di 200 notizie da
    validare: fermo, validare prima le settimane vecchie); scorre la settimana;
    ricalcola, verifica, salva; archivio; a video segnali netti oltre la
    soglia e aree non presidiate.
  - `valida --periodo <ciclo|lunedi'> --validatore "<chi>"`: legge la
    **griglia** del foglio Validazione (D-67) e la trasforma nelle decisioni
    campo per campo: cella gialla uguale alla proposta (anche "3" contro 3) =
    Accettato, diversa = Rettificato, Respingi = Sì = Respinto per tutti i campi
    dell'oggetto, con la Motivazione della riga. Si ferma se la griglia non
    corrisponde alle proposte "Da decidere" del periodo (righe mancanti o ID
    estranei: indica il comando `griglia`) o se lo storico ha righe del periodo
    con lo Stato cambiato a mano (trappola 69). Controlla TUTTE le righe con le
    stesse regole degli agenti (rischio: intero 1-5 a non piu' di un punto dal
    ciclo precedente, non respingibile; **Velocity anche vuota** e, da vuota,
    qualunque valore; **Anni_Adeguamento** numero 0-30 o vuoto, senza il
    limite di un punto, D-60; KRI: numeri, soglie **entrambe o nessuna** e coerenti
    dopo le rettifiche; azione: owner funzione, orizzonte ammesso, e un owner
    proposto che sembra una persona **si rifiuta anche se la riga non e' toccata**
    (D-54); notizia: vocabolari; una cella gialla svuotata dove il vuoto non e'
    ammesso e' un errore; Motivazione >= 10 caratteri se la riga cambia o si
    respinge; **un rischio con un rilievo di A5 superato** — BLOCCANTE SUPERATO
    nella colonna Rilievi, ⚑ nella griglia — chiede la Motivazione anche se non
    cambia nulla, D-56) — se una non va non applica niente e le elenca tutte,
    con la riga del foglio; `--accetta-il-resto` resta accettata ma non fa niente
    (lo dice a video: una riga non toccata vale gia' come accettata); poi applica
    (valori validati nei dati, esito ricalcolato con la stessa regola della
    scrittura — le quattro dimensioni — **e Variazioni
    riscritte**: la variazione dell'agente sul campo rettificato si toglie e,
    se il valore validato differisce dal ciclo precedente (anche da vuoto: "da
    n.v."), se ne aggiunge una con evidenza "Rettifica del validatore:
    <motivazione>"; KRI respinto fuori vigore;
    valore di un KRI rettificato con data (fine trimestre) e fonte della
    rilevazione, o data vuota se il valore e' vuoto; azione Approvata/Respinta con
    chi e quando, notizia respinta "Non rilevante" con impatti 0), compila lo
    storico (Decisione, Valore_Validato, Motivazione, chi, quando) e lo marca
    "Applicata", toglie il periodo dalla griglia, salva con backup, archivia
    `Validazione_<periodo>.json` e
    `NFR_Registro_<periodo>_validato.xlsx`, **riscrive `Righe_liste_<ciclo>.json`
    con i valori validati** (le liste si caricano dopo la validazione),
    aggiorna la baseline. Riepilogo per righe della griglia: "N righe —
    accettate N, rettificate N (N valori cambiati), respinte N". Gli **anni di adeguamento validati** si scrivono
    nell'anagrafica (`ANA_Anni_Adeguamento`, colonna M di Parametri) — un valore
    vuoto non cancella quello presente — e non producono variazioni (non sono
    una dimensione, D-60).
  - `griglia` (D-67): ricostruisce la griglia del foglio Validazione dalle
    proposte "Da decidere" dello storico, conservando valori gialli,
    Motivazione e Respingi delle righe intatte (chiave: oggetto, periodo, ID).
    Serve dopo una modifica a mano del foglio; la stessa ricostruzione la fanno
    trimestrale, settimanale, valida e aggiorna-registro. Prima le altezze delle
    righe, poi si nascondono le libere (trappola 70).
  - `inizializza --ciclo-precedente <AAAAQn> --settimana <lunedi'> [--template]`:
    crea il registro vivo dal template SENZA dati di esempio (svuota le cinque
    tabelle lasciando la riga segnaposto della trappola 16, l'anagrafica e il suo fondo grigio, imposta ciclo e settimana,
    ricalcola, zero errori); lavora su un file temporaneo e non sovrascrive mai
    un registro esistente.
  - `aggiorna-registro [--template]` (D-34): registro vivo -> template nuovo.
    Legge il vecchio in sola lettura (righe di ogni tabella per nome di
    colonna, anagrafica, parametri di input, baseline, copertura); le righe
    "Da decidere" passano nel registro nuovo e nella sua griglia con cio' che il
    validatore aveva gia' scritto (nella griglia o, nei registri fino al
    2026-10-01, nel vecchio foglio Validazione una riga per campo:
    `modifiche_vecchio_formato`), e si ferma solo se riguardano campi tolti dal
    modello (trappola 74); si ferma se una colonna del vecchio
    non esiste nel nuovo **e non e' fra le `colonne_dismesse` della mappa**
    (Gap_Controlli, Confidence, Dimensione: restano solo nel backup) **o fra le
    `colonne_rinominate`** (Severity -> Impatto: il valore si copia nella
    colonna nuova, D-57); il presidio dei
    controlli assente nel vecchio diventa "Non verificato"; crea il nuovo accanto,
    svuotato come `inizializza` (`svuota_registro`, comune), scrive tutto
    (date ISO -> seriale), ricalcola e verifica: zero errori, formule presenti,
    stesse righe, stessa copertura, **baseline identica** (a parte i campi
    dismessi); solo allora copia il
    vecchio in `Backup/..._prima_di_aggiorna-registro_<ora>` e lo sostituisce
    (stesso nome e percorso). Pesi, soglie e Z NON si copiano (D-50, D-61:
    `PARAMETRI_DA_CONSERVARE` = cicloCorrente, settimanaCorrente, moscaX,
    moscaYDefault): lo script stampa quelli vecchi, compreso `pesoGap` o
    `pesoSeverity` se c'erano, e le colonne rinominate e tolte. Rilanciato su un
    registro gia' aggiornato: fermo "niente da aggiornare".
  - `schede-input` (D-40): sola lettura; si ferma se il ciclo corrente ha
    decisioni "Da decidere"; scrive `Cicli/<ciclo>/Input_A6_<ciclo>.json`
    e dice come proseguire con A6.
  - `schede [--payload A6_<ciclo>.json]`: sola lettura del registro; con
    `--payload` valida lo schema e `controlla_a6` (un problema = fermo, nessun
    file); archivia input e output di A6 e scrive
    `Cicli/<ciclo>/Schede_<ciclo>.xlsx`; senza `--payload` le schede con i testi
    del registro.
  - `report [--file <xlsx>] [--con-lavoro]` (D-62): PDF del report al
    comitato dal registro com'e' ora, anche dopo correzioni manuali dei
    validatori. Sola lettura (apre il registro vivo o il file indicato, non
    salva); si ferma se la versione del template non e' quella dello script, se
    il ciclo corrente ha decisioni "Da decidere" o se il ricalcolo trova errori
    di formula; `prepara_report` come nel trimestrale; esporta i fogli
    `FOGLI_REPORT` (Quadro ... Metodologia; con `--con-lavoro` anche Registro e
    Parametri) in `Cicli/<ciclo>/Report_comitato_<ciclo>.pdf`; un PDF gia'
    presente diventa `Report_comitato_<ciclo>_<data di modifica>.pdf`.
  - `dismetti --rischio --motivazione --decisore`: toglie il rischio
    dall'anagrafica **ricompattandola**, `In_Vigore = No` ai suoi KRI del ciclo
    corrente, azioni aperte "Annullata", baseline aggiornata, atto in
    `Archivio_Cicli/Dismissioni/`. Baseline e fotografia dei KRI considerano
    solo i rischi in anagrafica.
  - `riapri [--rischi]` (D-76; `--voci` tolto dalla D-79): il ciclo corrente, gia' validato,
    torna nella griglia (rischi del radar e in osservazione, KRI in vigore, azioni
    aperte non proposte) con `aggiungi_da_validare`, cioe' con il valore
    attuale come "proposta"; si ferma se il ciclo ha gia' righe da decidere.
    Un oggetto e' **riaperto** se il suo dato ha gia' una Validazione diversa
    da "Da validare" (`oggetti_riaperti`); `valida` lo tratta cosi': riga non
    toccata = il dato non si tocca; rettifica senza il limite di un punto;
    Respingi = KRI fuori vigore, azione Annullata, voce Archiviata; un'azione
    rettificata tiene il suo Stato; gli anni di adeguamento vanno
    nell'anagrafica solo se cambiati; niente obbligo del ⚑. Nello storico
    "Invariato / Rettificato / Respinto (riapertura)". Un'azione riaperta di
    un ciclo prima si trova per ID (`riga_dato`). `baseline` senza `--uscita`
    riscrive anche la knowledge di A7 (dopo i testi corretti a mano).
  - `diagnosi` (D-80, analisi 17, 17.10): sola lettura del registro; `diagnosi.py` (solo libreria standard, collaudato
    su righe finte) misura i valori all'ingresso dei rischi nuovi (Esito "Nuovo" di qualunque ciclo), il verso delle
    rettifiche sulle quattro dimensioni nello storico (proposta contro valore validato; rischi nuovi, altri, riapertura;
    da o verso n.v. nessun verso) e i rischi con Prossimita 1 con il margine di `radar.margine`; segnala quelli con
    Impatto 4-5 senza anni di adeguamento; conta le note di esposizione non nota (D-81) con la Probabilita validata.
    Stampa e scrive `Cicli/<ciclo>/Diagnosi_valutazioni_<ciclo>.txt`.
  - Esposizione non nota (D-81), in `controlli_a5.py` (C5): `esposizione_non_nota(razionale)` restituisce (dichiarata,
    N); con N maggiore della Probabilita proposta un rilievo "Da motivare" con i due valori e, per un rischio della
    baseline, il massimo ammesso in validazione (un punto); frase senza valore maggiore = Osservazione. Nessun campo
    nuovo: la frase sta nel razionale.
- **Piu' analisti** (D-83): `lucchetto.py` (solo libreria standard). I comandi di `SCRIVONO` (trimestrale,
  settimanale, valida, griglia, riapri, dismetti, inizializza, aggiorna-registro) prendono in `main()` il lucchetto
  `Archivio_Cicli/_Lucchetto/registro.json` (id, utente da `configurazione.json` o Windows, PC, comando, inizio,
  scadenza 2 ore): un lucchetto valido di un altro utente o PC ferma (codice 1, "Il registro e' in uso"); uno scaduto,
  o il proprio rimasto da un comando interrotto, si prende. **Presa in due tempi** solo se configurata: scrive, attende
  `attesa_lucchetto` secondi (0 di default dal 23/10, scelta dell'utente: in quattro due avvii nello stesso istante
  sono rarissimi e li ferma l'impronta; `NFR_ATTESA_LUCCHETTO` la sostituisce), rilegge; un id diverso o una copia in conflitto di OneDrive
  (`registro-*.json`) di un altro = ritiro ("nello stesso momento"). Rilascio in `finally`, solo se e' ancora il
  proprio. `sblocca --motivo` lo toglie e scrive `sblocchi.log`.
- **Copia di lavoro** (D-83): le sessioni in scrittura passano da `sessione_registro(conf)`: fermo se il registro e'
  aperto in un programma di questo PC (`aperto_qui`: `open(r+b)` -> PermissionError); copia in `cartella_lavoro`
  (`%LOCALAPPDATA%/NFR/lavoro/<ora>_<pid>/`, stesso nome del file) con l'impronta SHA-256; Excel lavora sulla copia;
  `_salva_con_backup` fa il backup dell'originale e salva la copia (`LAVORO["salvata"]`); chiusa la sessione,
  `_sostituisci` controlla che l'impronta dell'originale non sia cambiata (altrimenti FERMATO "cambiato mentre lo
  script lavorava"), copia in `~$NFR_nuovo_<pid>.xlsx` accanto all'originale (OneDrive non sincronizza i `~$`) e fa
  `os.replace`; solo allora `SALVATO["registro"]`. La cartella di lavoro si cancella sempre.
- **Automatismi** (AU1, D-83): `valida` del ciclo corrente (trimestre o straordinario) rigenera il PDF del report
  dalla stessa sessione con `esporta_pdf` in una cartella temporanea e lo pubblica nell'archivio con `pubblica_report` (gli stessi di `report`) solo dopo la sostituzione del registro e dopo `Validazione_<ciclo>.json`, con l'ora della pubblicazione (avviso, mai fermo; `--senza-report`); `trimestrale`
  copia `02_Agenti/A*.md` in `Cicli/<ciclo>/Prompt_in_uso/` (`archivia_prompt`); `schede` esporta anche
  `Schede_<ciclo>.pdf` (avviso se non riesce); `riapri` scrive `Cicli/<ciclo>/Riapertura_<ciclo>.json`, `valida` la
  chiude rinominandola con data e ora e chi ha validato (`chiudi_riapertura`). AU7: `_scrivi_baseline` scrive anche
  `Input_A3_A4.txt` (`input_a1.scrivi_allegato_a3_a4`: intestazione con ciclo e data, poi la baseline
  dopo `=== 1. BASELINE ===`, leggibile con `leggi_baseline`).
- **L'app NFR** (D-83, tappa M2; strada A dell'analisi 14): `NFR.cmd` (ASCII, `%~dp0`, `chcp 65001`; `pyw -3`,
  poi `pythonw`, poi `python`) apre `app_nfr.py`, finestra tkinter: stato in testa (ogni 30 secondi), pulsante del
  prossimo passo, un pulsante per processo, passo in corso con le istruzioni e i pulsanti "Leggi gli appunti adesso",
  "Scegli file...", "Ho chiuso il registro", "Annulla il passo", log con l'esito colorato. **L'app non contiene
  regole**: i processi sono in `flussi.py`, scritti contro un `Ambiente` (esegui, apri, copia, risposta,
  attendi_chiusura, chiedi, conferma, mostra) che la finestra realizza e il collaudo simula (`AmbienteFinto` di
  `test_app.py`). Ogni processo gira in un thread; le chiamate alla finestra passano da una coda al thread di tkinter.
  - `stato.py`: stato e prossimo passo **senza Excel**, dall'archivio condiviso (Baseline_corrente: `ciclo_precedente`
    = ciclo corrente, `ciclo_da_valutare`; `Validazione_<c>.json` = validato; `Riapertura_<c>.json` aperta; report
    piu' recente della validazione; schede; settimana dal lunedi' di oggi: Raccolta, A3 in In_arrivo, Settimane;
    lucchetto). Priorita': attesa del collega, baseline, validazione (anche riapertura), straordinario deciso,
    trimestre chiuso (oggi dopo la fine del trimestre da valutare), report, schede, settimana, validazione della
    settimana. `segna` annota in `Archivio_Cicli/Stato/<periodo>.json` i passi senza file (chi, quando).
  - `ingresso.py`: `estrai_json` (BOM e recinti via, `raw_decode` da ogni `{`, il piu' grande che e' di un agente;
    graffe non chiuse = TRONCATA anche se dentro ci sono oggetti interi), `unisci` le parti, `riconosci_agente` dai
    `required` degli schemi (il piu' specifico; A8 = schema di A1 con periodo `-Sk` o `analisi_evento`), `nome_file`,
    `salva` in `Archivio_Cicli/In_arrivo/` (UTF-8 senza BOM; originale in `Originali/`, il file di prima in
    `Precedenti/`, con i millisecondi), `ricevi` (un testo senza JSON e' un parere di A4 solo se atteso A4 o nessuno:
    `Pareri/`), `messaggio_correzione` per A3, A5, A6.
  - `appunti.py`: pywin32, `GetClipboardSequenceNumber`; le copie dell'app si ignorano; senza pywin32 solo i file.
  - `esecutore.py`: motore in un processo a parte con `python.exe` anche sotto `pythonw`, `CREATE_NO_WINDOW`, uscita
    riga per riga, fascia OK / FERMATO / ERRORE TECNICO ("DOPO IL SALVATAGGIO": non rilanciare), log in
    `Archivio_Cicli/Log/`; `esito_precontrollo` legge la prima riga del precontrollo.
  - `flussi.py`: per un agente prepara `%USERPROFILE%/NFR_Da_allegare/<agente>/`, apre la cartella e il link (solo se
    comincia con http), copia il messaggio base (guida, sezione 8), aspetta la risposta; "continua" per una risposta
    tagliata; giro di correzione nella **stessa chat** (A1/A8: `Correzione_A1_<periodo>.txt` del precontrollo o di
    `trimestrale`; A3, A6: dal fermo); una risposta gia' in `In_arrivo` si riusa se l'analista conferma (ripresa).
    Validazione: registro aperto con `os.startfile`, attesa che Excel lo apra e poi lo chiuda (`aperto_qui` e file
    `~$`), poi `valida`. Configurazione dell'app in `configurazione.json`: `link_agenti` (piatto o per versione:
    `{"Agent Builder": {...}, "Copilot Studio": {...}}`), `validatore_predefinito`, `raccolta_su_questo_pc`, `agenti`
    (versione proposta all'avvio), `ascolta_appunti`.
  - **Risposte incollate** (richiesta dell'utente, 23/10): riquadro "Risposta dell'agente" nella finestra; incollando
    (evento `<<Paste>>`) la risposta passa al processo, o con "Usa il testo incollato"; l'ascolto degli appunti resta
    in piu' (`ascolta_appunti`, acceso di default), e "Scegli file...". Casella **"Agenti"**: Agent Builder o Copilot
    Studio; stessi nomi, cartella `In_arrivo` e registro, l'origine si annota (`ingresso.ORIGINI`; nome del testo
    originale `<nome>_<ora>_<origine>.txt`; nota in `Stato/<periodo>.json`; nome del parere di A4) e sceglie il link.
    `estrai_json` legge anche il JSON dentro un campo di testo (record di un prompt di Copilot Studio, campo `text`) e
    ignora i link alle fonti in coda.
  - **Divisore trascinabile** (ttk.PanedWindow, 60% passo in corso e 40% uscita all'avvio) fra il passo in corso e
    l'uscita dei comandi; il riquadro della risposta e' alto e resta visibile dopo l'incolla (un nuovo Ctrl+V lo
    sostituisce); sotto, la riga dell'esito scritta da `flussi.esito` (`esito_risposta` dell'Ambiente, se c'e'):
    ricevuto con agente, caratteri e file, oppure risposta tagliata, di un altro agente, fuori schema.
  - **Schermi 1920x1080**: con un'altezza dello schermo fino a 1200 pixel la finestra si apre ingrandita (`zoomed`);
    stato su due righe, riquadro per incollare di tre righe; provata con la scala al 100, 125 e 150%.
  - **Documentazione dell'uso**: guida, sezione "L'app NFR: uso passo per passo" (finestra, i tre gesti con un agente,
    risposta tagliata, correzione, ogni processo con cio' che fa l'app e cio' che fa l'analista, ripresa, piu'
    analisti); configurazione degli agenti nella 0.2 (3-bis, link) e 0.2-bis (Copilot Studio), voci di
    `configurazione.json` in una tabella nella 0.3.
- Codici di uscita: 0 eseguito; 1 fermato (registro intatto); 2 errore tecnico,
  distinguendo **prima** del salvataggio (nulla scritto) da **dopo** (registro
  scritto, baseline gia' aggiornata: "NON rilanciare").
- **Archivio** (`Archivio_Cicli`): `Baseline_corrente.json/.txt`;
  `Cicli/<ciclo>/` (Excel di output `NFR_Registro_<ciclo>.xlsx`, versione
  `_validato`, output di A1 e A5, baseline usata, esito dei controlli,
  `Righe_liste_<ciclo>.json`, validazione, `Input_A6_<ciclo>.json`,
  `A6_<ciclo>.json`, `Schede_<ciclo>.xlsx` e `.pdf`, `Report_comitato_<ciclo>.pdf`,
  `Prompt_in_uso/`, `Riapertura_<ciclo>.json` finche' la riapertura e' aperta);
  `Cicli/<ciclo>/tentativo_<ora>/` per OGNI tentativo, anche fermato;
  `Settimane/<lunedi'>/`; `Backup/`; `_Lucchetto/` (registro.json, sblocchi.log; D-83);
  accanto alla baseline `Input_A1_<ciclo>.txt`, `Input_A3_A4.txt`.
- Dopo il salvataggio: prima la baseline, per ultima la copia dell'Excel (e'
  quella che fallisce se qualcuno ha aperto un file dell'archivio).
- `configurazione_esempio.json`: workbook, kernel, cartella_uscita, news_inbox, utente, attesa_lucchetto (0),
  validatore_predefinito, raccolta_su_questo_pc, agenti, ascolta_appunti, link_agenti
  (facoltativa `cartella_lavoro`).
- `README_variante_locale.md`: vincoli di Agent Builder con data della fonte,
  setup dei cinque agenti (istruzioni, knowledge, capability, modalita'), setup
  dello script e pianificazione della raccolta, procedure, copertura dei
  controlli di A5, limiti onesti.

## SHAREPOINT, WORKFLOW, GOVERNANCE

- `04_Riferimenti/struttura_e_liste.md` (colonna Rilievi in RiskRegister_Storico,
  niente Gap_Controlli ne' Dimensione; Velocity e soglie possono essere vuote): sette library (Kernel con la baseline
  .txt e fonti.md; Analisi_Interne con sottocartelle come negli indirizzi delle
  fonti share, SOLO documenti della Banca su se stessa; **Analisi_Esterne**
  (D-45, 29/09) per report di settore, dati di consorzio e analisi di terzi,
  separata apposta perche' il tipo di una fonte segue la cartella; News_Inbox per settimana con Manuali/; Report_Trimestrali con il
  registro vivo (il PDF del report lo scrive `report` in Archivio_Cicli/Cicli/<ciclo>/); Report_Settimanali,
  **non usata nella variante locale** (l'output della settimana va in Archivio_Cicli/Settimane; serviva al
  disegno con Copilot Studio): la documentazione lo dice, perche' una library elencata senza uso confonde;
  Archivio_Cicli) e tre liste storiche che
  copiano le tabelle (RiskRegister_Storico, Azioni_Storico, KRI_Storico: ogni
  colonna documentata, il collaudo lo verifica); nessuna lista per le
  validazioni (base dati nel workbook + json per periodo). Nella variante
  senza Power Automate le liste si possono non creare: la storia e' nel
  workbook.
- `04_Riferimenti/workflow.md`: W0 raccolta (tre canali; lo stesso script anche con
  Power Automate); W1 trimestrale con i passi dello script numerati, passo 8
  validazione umana e passo 9 comando valida, mai auto-approvazione per
  decorrenza dei termini; passo 11 schede dei rischi (`schede-input`, A6,
  `schede`); passo 12 report al comitato (PDF dei fogli da Quadro a
  Metodologia dell'Excel validato, piu' il file delle schede); eventi fuori
  ciclo: primo uso (un rischio per meccanismo di perdita, nessun event type
  obbligatorio),
  dismissione, anni di adeguamento, **attenzione del supervisore**,
  **presidio dei controlli** (D-49),
  **avanzamento delle azioni** (Stato In corso/Completata, unica colonna dei
  dati modificabile a mano), **aggiornamento del template** (colonne
  dismesse; righe da validare portate nella griglia, fermo solo su campi tolti
  dal modello), **griglia di validazione rovinata a mano** (comando
  `griglia`); nel passo 4
  **A5 facoltativo** (D-71); nel passo 5 il fermo solo per l'integrita' e le
  segnalazioni da motivare e, prima dell'append, pulizia dei riferimenti, esito e "da/a"
  calcolati dallo script (D-51); nel passo 8 Velocity vuota, soglie entrambe o
  nessuna, rischi con segnalazioni da motivare (colonna Segnalazioni); W2
  settimanale con validazione facoltativa; W3 A4;
  tabella dei campi derivati (tutti quelli della mappa, il collaudo li
  confronta col codice: dal 30/09 anche `esito`,
  `presidio_esistente_o_non_verificato`, `rilievi_rischio`, `rilievi_ciclo`,
  `rilievi_superati`); test in ambiente **da registro vuoto** (nessun
  trimestre gia' valutato a mano) con doppio run e `confronta.py --primo-ciclo`,
  poi lettura dell'analisi e validazione.
- `04_Riferimenti/controlli_e_model_risk.md`: qualificazione model-risk prima del
  deploy; tabella dei controlli con controparte deterministica (schema, esito
  e "da/a" calcolati, C1-C9 nella versione del 30/09, soglie invertite o vuote,
  **rilievi di A5 superati** (D-56), colonne tolte dal modello, codici dello
  strumento di ricerca, copertura, formule integre, composito, direzione,
  approvazione/validazione, rettifiche umane, urgenza calcolata, fonti delle
  notizie, storico KRI); evidenze per ciclo (incluso il testo dei prompt e
  fonti.md); rischi del sistema (inflazione progressiva, deriva mediatica,
  affidamento su A4, validazione di facciata, urgenza fraintesa, fonti non
  validate o fuori licenza, fonte silenziosa, e dal 24/09: **validazione non
  indipendente** (una sola persona, limite accettato nel pilota, D-30),
  **copie fuori dall'archivio** (allegati in "Microsoft Copilot Chat Files",
  parere DPO positivo, D-24), **capability accese per default** (code
  interpreter da spegnere), e dal 25/09: **urgenza sottostimata** (rimedio:
  anni di adeguamento, D-33), **commento superato dalla validazione** (rimedio:
  avviso nel Quadro), **scheda che inventa** (rimedio: input solo dai dati
  validati, controllo dei numeri e delle fonti, D-40), **attenzione del supervisore scambiata per gravita'**
  (rimedio: input separato, fuori da score e urgenza, D-35); C4 comprende i
  numeri del razionale (D-36); dal 30/09 **superamento dei rilievi come
  scorciatoia**, **presidio non aggiornato**, **Velocity sempre non
  valutata**); tra gli elementi della qualificazione, che cio' che richiede
  conoscenza interna (presidio, soglie) lo mette la Banca e la contabilita'
  (esito, da/a) lo script; dal 02/10 (D-67) il controllo "Griglia di
  validazione" e la **validazione di facciata** riscritta (una riga non
  toccata vale come accettata: nessun gesto e nessuna traccia diversa da
  un'accettazione ragionata; presidi: quota di rettifiche, ⚑ che chiede la
  Motivazione, effetto di ogni valore visibile nella griglia); la base dati
  delle rettifiche (foglio Storico_Validazioni) e le cautele per usarla; limiti da riportare nel memo (sezione 5: il generatore li copia nel
  foglio Quadro, righe `>`); nota Agent Builder. Nella tabella dei controlli
  anche "Schede dei rischi (A6)" e "Perche' un rischio e' segnalato". In sezione 1
  l'**esito della qualificazione** (D-23: non rilevante, nessun requisito
  ulteriore; da rivalutare se il registro passa da affiancamento a input del
  processo ufficiale) e, per il primo ciclo, i criteri di accettazione al posto
  di un trimestre di riferimento.

## DOCUMENTAZIONE PER CHI USA E CHI MANTIENE

- **Nessun contenuto ripetuto fra documenti, con un'eccezione deliberata**:
  ogni documento ha un pubblico e rimanda agli altri invece di copiarli.
  la guida passo passo contiene anche l'avvio del progetto (fasi 0-9, ruoli,
  cancelli G0-G4, tempi, checklist: sezione "Avvio del progetto"; dal 07/10/2026,
  richiesta dell'utente, al posto di `08_Deploy/Piano_deploy.md`); `README_variante_locale.md` = i campi
  esatti di Agent Builder e il "perche'" (limiti verificati su Microsoft
  Learn); 00_LEGGIMI = orientamento e regole. **La guida (sezione 0) fa
  eccezione** (trappola 48, 29/09): contiene per intero, in un solo percorso
  ordinato, anche i passi che altrove sono descritti a parte (creazione sito
  SharePoint, creazione dei cinque agenti con knowledge/capability/modalita'),
  perche' un primo installatore reale, seguendo solo il rimando, doveva
  ricostruirsi da solo l'ordine saltando fra file — fonte di errori. La
  tabella agenti resta anche in `README_variante_locale.md` (per il
  "perche'"): le due copie si tengono allineate a mano, con una nota in ciascuna su quale correggere
  per prima (la guida). Non esprimibile come mappa dati unica: sono prosa con
  pubblici diversi, non righe di una tabella.
- `00_LEGGIMI.md` (per chi installa e mantiene): in testa la mappa "quale
  documento per quale domanda"; il sistema in una pagina, principi, **indice
  con una riga per file** (il collaudo lo confronta coi file presenti, nei due
  versi), dove vive ogni regola, ordine di deploy **solo in sintesi con rimando
  alla guida, sezione "Avvio del progetto"** (non una seconda lista da allineare), procedura "Se cambia
  il kernel", requisiti.
- `00_GUIDA_PASSO_PASSO.md` (per chi usa, anche senza esperienza): le parole
  che servono; **a cosa serve Python** (gli agenti non lo usano; cosa lancia
  l'utente e quando; cosa fa lo script prima di scrivere; come si scrive un
  comando; pianificazione della raccolta); **sezione 0, prima installazione,
  un solo percorso ordinato** (trappola 48, 29/09): **0.1** amministratore
  SharePoint/M365 (sito, sette library, controllo versione, permessi); **0.2**
  manutentore del pacchetto (kernel gia' adattato, caricare `Kernel`, creare i
  cinque agenti in Agent Builder con la tabella istruzioni/modalita'/
  capability/condivisione, **il perche' di ciascuna modalita'** (Think
  deeper per A1/A5/A6, Auto per A3/A4: ragionamento su cosa fa ciascun
  agente, non una decisione in `DECISIONI.md` — dichiarato come tale), una
  seconda tabella con la **knowledge esatta** per agente (cartelle intere,
  file singolo, nessuna) e i **4 siti pubblici con URL esatto** (FNT-20..23,
  da `01_Kernel/fonti.md`), spegnere le capability, link degli agenti per l'app
  (3-bis), niente prompt schedulato di A3 (AU7), prova di fumo; **0.2-bis** gli stessi
  agenti in Copilot Studio, usati dall'app con copia e incolla); **0.3** sul
  PC di ogni analista (Python e dipendenze con verifica che apre Excel,
  sincronizzare OneDrive, `configurazione.json`, **verificare che
  `03_Excel/NFR_Dashboard_Template.xlsx` esista davvero** — trappola 47 — non
  solo la cartella, prova con `baseline`); **0.4** primo utilizzo reale da
  registro vuoto (`inizializza`, mai a mano dal template). Poi **0-bis
  aggiornare il registro a un template nuovo** (`aggiorna-registro`), che apre
  dicendo esplicitamente a chi NON serve (chi ha appena fatto 0.4 non la
  legge); ogni lunedi'; ogni trimestre (punti 11-12: schede con A6; punto 13:
  PDF del report al comitato); validare; leggere i risultati (Quadro con le segnalazioni da motivare,
  Classifica e lente, Matrice, Delta, Metodologia, file delle schede per
  primi, poi Registro con Presidio e Rilievi e fogli di lavoro, fascia del
  titolo e guida di ogni foglio); nel ciclo trimestrale precontrollo e A5
  **facoltativi**, il **punto 8** (fermo solo per integrita', messaggio per A1)
  e il **punto 8-bis** (segnalazioni da motivare: si decidono in validazione);
  nella validazione la colonna Segnalazioni, le regole su Velocity vuota, soglie
  fissate dalla Banca (entrambe, anche quelle invertite proposte da A1), salto
  di piu' di un punto non accettabile nemmeno se proposto, rischi con ⚑ e owner
  persona; 0.4 senza copertura
  obbligata degli event type; 0-bis sull'aggiornamento alla versione
  2026-09-30 (ciclo validato prima, ricaricare A1, A5, A6 e A4, colonne
  dismesse, presidio "Non verificato", baseline in `Kernel`); **quando si lanciano A5 e A6** (riquadro dopo il ciclo
  trimestrale); in testa **"In breve: i cicli standard"** (07/10: settimana,
  trimestre e passi "quando serve", un passo per riga con il rimando alla
  sezione di dettaglio); subito dopo, dal 23/10 (D-83), **"L'app NFR: uso passo per passo"** (la finestra parte per
  parte, i tre gesti con un agente e il riquadro per incollare, risposta tagliata e correzione nella stessa chat,
  una tabella con ogni processo: che cosa fa l'app e che cosa fa l'analista; ripresa, piu' analisti); in fondo la **sezione 8 "Gli agenti: mansioni e
  messaggi da usare"** (07/10: tabella di mansione, momento, input e output di
  ogni agente; messaggio base e variazioni per ciascuno, compreso il
  **messaggio rinforzato per A1** del 29/09 con i suoi due limiti — rinforza
  le Istruzioni, non le sostituisce; non forza il retrieval di Agent Builder —,
  documenti precisi, tema da verificare, simulazione di un ciclo passato,
  correzione; cosa un messaggio non puo' cambiare); la **sezione 9 "I comandi
  Python"** (07/10: codici di uscita, opzioni comuni da scrivere prima del
  comando, e per ogni comando sintassi, parametri obbligatori, opzioni, cosa fa e
  scrive, quando, errori tipici con il rimando alla sezione 7; "Cosa lanci tu"
  in testa rimanda li', senza ripetere la tabella); dove sono i file; cambiare le regole (anche anni di
  adeguamento, attenzione del supervisore, **presidio dei controlli**,
  avanzamento delle azioni); "se
  qualcosa va storto" (messaggio -> cosa fare, errori di Python compresi,
  incluso "Template non trovato" con il rimedio `genera_dashboard.py`). Ogni
  passo: chi, cosa fare, cosa si deve vedere. Il collaudo verifica che ogni
  comando e opzione citati esistano (le opzioni di python e pip, come
  `--version`, `--upgrade`, `--force-reinstall`, sono escluse dal controllo).
- Errori di installazione da mettere nella tabella della guida (visti sul PC
  della Banca il 24/09 e il 29/09): `Workbook non trovato: None` (manca
  `configurazione.json`) distinto da un percorso sbagliato; `No module named
  'pythoncom'` (pywin32 a meta': reinstall forzato; `pywin32_postinstall` non
  esiste piu' dalla 312); fonti irraggiungibili solo in parte (PAC: `pypac`)
  distinte da tutte irraggiungibili (blocco vero: IT); **`Template non
  trovato: ...03_Excel\NFR_Dashboard_Template.xlsx`** (trappola 47: pacchetto
  arrivato senza il file binario, es. allegato filtrato dalla posta —
  rimedio: `python genera_dashboard.py` in `03_Excel`, o `--template`). La
  verifica di pywin32 nella guida deve aprire Excel (`win32com.client` +
  `pythoncom` + `Dispatch`), non solo `import win32com`.
- `TODO_possibili_sviluppi.md`: **il piano unico** del lavoro da fare (dal
  28/09), proposte non fatte, ciascuna con perche', cosa fare, quando e'
  fatta, impegno.
  - Dall'08/10 sera il file e' riordinato: voci aperte in sezioni (ordine di
    lavoro; passi sul PC della Banca B1-B7; processi; automazione; Q1; grafici;
    pulizia; questioni aperte), il fatto in fondo, una riga per voce. In testa
    l'**ordine di lavoro** unico:
    0. passi sul PC della Banca (pacchetto, `aggiorna-registro`, agenti, prove);
    1. P4 e P9, piccole e utili subito al trimestrale;
    2. AU1, solo la scrittura robusta (registro protetto prima del primo ciclo);
    3. P1; 4. P5;
    5. AU1-AU3, la parte comune; 6. AU4 (A-15), poi AU5 oppure AU6;
    7. P2, P7, P6; in parallelo Q1, G1/G3/G2, G6.

    I processi vengono prima dell'automazione: la regola del 28/09 ("P dopo
    AU3") valeva per P3, che toccava la coda delle richieste, ed e' fatta
    (D-75, D-77); le P rimaste cambiano schemi, prompt e viste, validi in
    tutte le strade.
  - Sezione **automazione del processo**, dal piano
    `Analisi_Architettura/Archivio/10`, al posto di AR1 chiusa da D-43:
    - AU1 automatismi del motore (baseline in kernel, prompt archiviati,
      comando `report` con PDF, PDF delle schede) e scrittura robusta
      (`AutoSaveOn` spento, copia di lavoro locale con sostituzione
      verificata);
    - AU2 ingresso unico `In_arrivo` (`estrai_json`, `riconosci_agente` dagli
      schemi, nomi, `messaggio_correzione`), `stato(conf)`, esecutore con esiti
      in `Esiti/`, coda delle richieste con `schema_richiesta.json` e lista
      bianca, riga di A3;
    - AU3 `installa.cmd` e Verifica del PC;
    - AU4 scelta della strada, con tabella di confronto, criteri, prova K0 e
      proposta "strada A se non si decide";
    - AU5 procedura guidata a menu con gli appunti (strada A);
    - AU6 variante CS-1 (Copilot Studio con il motore in background).
  - Sezione finale **in riserva**: piano 07 e variante CS-2.
  - Poi le voci che seguono. Almeno: G1 parametri dei grafici in una
  tabella unica; G2 guida alla modifica/estensione dei grafici; G3 script di
  anteprima PNG; G4 migrazione del registro vivo su un template rigenerato
  (**fatta il 25/09**: `aggiorna-registro`, resta come traccia); G5 difetti
  estetici noti (corretto il colore "Agire entro l'anno"; tolto il radar della
  Dashboard; matrice piccola del Quadro affollata; stima delle altezze).
  Dal 26/09 anche (AR1, piano 07, chiusa il 28/09 da D-43 e spostata fra le
  voci in riserva): una tabella "c'e' / in parte / manca" dei processi
  trimestrale, settimanale e spot, con in testa le decisioni D-41 e D-42; P1
  segnali qualitativi (direzione, dimensione, descrittore) per ogni rischio
  toccato da A3 e A4, freccia sul cerchio deliberato del Radar_Mosca e nel
  Registro, **senza numeri ne' posizioni ipotetiche** (D-41); P2 scia sul
  radar; P3 campo `critico` e ciclo straordinario, unica eccezione al
  "solo il trimestre modifica uno score" (D-41, es. l'annuncio di Mythos); P4
  fonti di tipo `rapporto` per A1 (ORX, EBA RAR, priorita' BCE, ENISA, WEF);
  P5 rischi collegati (un evento che tocca piu' rischi = righe separate con
  campo `collegati` reciproco, nessuna media ne' score dell'evento: D-42); P6
  scheda per driver o gruppo di collegati; P7 riepilogo mensile; Q1 metodologia
  quantitativa per i 3-5 rischi piu' rilevanti (scenari con Monte Carlo, dati
  esterni riscalati, frequenze dei peer, FAIR e reti bayesiane, ancoraggio al
  CET1; numeri dagli esperti, calcolo dal codice, divergenza oltre una fascia
  decisa dal validatore).

## LA SUITE DI COLLAUDO (99_Collaudo) — scrivila ed eseguila

Nessuna copia del codice di campo: importa `07_Senza_Studio/` e lancia
`esegui_ciclo_locale.py` come un analista. `esegui_collaudo.py` lancia tutto
(`--senza-excel` salta la catena; `-v` mostra anche i successi; di default
stampa solo i fallimenti). Dall'08/10 (M1, D-78):
- la catena e' in **dieci gruppi indipendenti**, ognuno su copie proprie;
- `esegui_collaudo.py` li lancia con `run_catena.py --parallelo 3`, un'istanza di Excel per processo (`DispatchEx`);
- `--passo <nome>` lancia un gruppo solo;
- `--mirato` salta la catena se nessun file che la riguarda e' cambiato dalle impronte dell'ultimo collaudo
  completo e verde (in `%LOCALAPPDATA%\NFR_collaudo`, fuori dal pacchetto).
1. `componi_prompt.py --verifica`.
2. `test_mappatura.py`: ogni campo degli schemi ha una destinazione, ogni
   colonna una sorgente valida (payload esistente, derivato implementato,
   formula) e un **significato** (almeno 10 caratteri); tabelle del template
   = mappa (anche tblValidazione nel foglio Storico_Validazioni); campi
   validabili esistenti; **nomi `VG_<oggetto>_*` della griglia** nel foglio
   Validazione per ogni campo validabile (senza Respingi per il Rischio) e
   `valStato`; colonne delle liste documentate.
3. `test_controlli.py`: validatore su payload conformi e un difetto per regola
   (incluso cio' che lo schema non vede, e i campi tolti il 30/09:
   gap_controlli, esito, da/a, dimensione, KRI 0 o 4); controlli A5 su ciclo
   pulito e un difetto per controllo, piu' cio' che NON deve fermare (Velocity
   da null a un valore con la sua variazione, KRI in vigore non riletto);
   `combina` con `supera_agente` (supera A5, non lo script); dati di esempio
   conformi a C1-C5 **con l'esito calcolato da `completa_payload` uguale a
   quello scritto nel template**, KRI in cinque stati; regole delle
   rettifiche umane (`controlla_valore`: Velocity vuota, da vuota qualunque
   valore; variazione "da n.v."); consistenza fra due run (`confronta.py`),
   anche **primo ciclo** (stessi rischi con id diversi: abbinati per event type e
   nome; un rischio in un solo run e' segnalato); una mappa delle colonne senza
   versione o di un'altra versione ferma lo script; **schede**: output di A6
   conforme allo schema e senza problemi, poi un difetto per controllo (ciclo,
   rischio mancante o in piu', scheda ripetuta, valore doppio (servono i
   cinque, Velocity null spiegata come "non valutata"), fonte
   riscritta o omessa, numero o data inventati), numeri in date italiane e ISO,
   ordine fisso delle chiavi del JSON, file delle schede con e senza A6;
   **razionale in parti** (D-68): `parti_razionale` legge le etichette (accento,
   apostrofo, minuscole dopo un punto) e lascia intero un razionale scritto
   prima ("Impatto resta 4:"), `parti_effetto` divide perche' ed EFFETTO; nel
   file il perche' di ogni valore sta accanto al valore (spiegazione di A6 o
   motivazione di A1), il Razionale con il fenomeno c'e' solo senza A6, azioni e
   KRI hanno "Perche'" ed "Effetto atteso"; un rischio con il razionale vecchio
   ha "Razionale (registro)", la nota nella tabella e "non indicato".
   **Precontrollo e allegato di A1** (D-69, `test_precontrollo`): nei cicli di
   prova nessuna azione ripete un'azione aperta; una ripetuta (maiuscole, spazi,
   punto a parte) e' un'Osservazione di C8 con l'id dell'azione aperta;
   `precontrolla`: run3 pulito, run1 solo punti di forma (razionale senza parti),
   difettoso (soglie invertite, evidenza generica) con il messaggio "Da
   correggere" e righe "NFR-01 · C9: ...", campo in piu' = errore di schema col
   nome del campo; comando senza registro (codice 1 e file, 0 con soli punti da
   verificare, 0 senza file con output pulito, messaggio vecchio cancellato,
   fermo senza baseline); allegato: nove controlli senza note, stesso testo nel
   prompt composto di A5, baseline identica, guida senza righe `>`, file del
   ciclo prima sostituito (non gli altri), kernel senza i file nuovi = sola baseline;
   `leggi_baseline` restituisce la baseline scritta e rifiuta un testo senza la
   parte 1; il comando stampa l'impronta.
   **Kit di Copilot Studio** (D-70, `test_kit_copilot_studio`):
   - lo script della skill contiene esattamente i moduli e lo schema del
     pacchetto (`prepara_kit.contenuto_script` == `sorgenti()`);
   - il `.txt` e gli zip hanno lo stesso script e `SKILL.md` attuali, con
     `name` uguale alla cartella e `description` di al massimo 1024 caratteri;
   - lo script, lanciato come **processo a parte**, da' lo stesso esito del
     comando: output pulito con codice 0 e impronta; difettoso con codice 1,
     stessa prima riga e stesso messaggio;
   - legge una risposta con i recinti e `Baseline_corrente.json`;
   - su file illeggibili esce con codice 2 e il motivo; `--verifica` elenca le
     impronte dei moduli.
4. `test_fonti.py`: formato di fonti.md, codici unici e conformi allo schema,
   limiti dei siti per Agent Builder, temi = codici di tassonomia, codici dei
   dati di esempio nell'elenco, elenco nel prompt di A3; raccolta con **feed
   finti** (RSS, Atom, senza data, finestra, esclusioni, max_voci, doppioni fra
   due giorni, fonte giu'), senza rete.
5. `verifica_riferimenti.py`: prompt aggiornati; codici di tassonomia identici
   ovunque; C1-C9 in schema, kernel (`controlli_A5.md`), prompt composto di A5,
   documentazione, governance, codice (C4 assente dal codice); il modello di A5
   ha `{{CONTROLLI}}` e nessuna riga "- Cn " (D-69); numeri di passo documentati = modelli; campi derivati
   documentati = implementati; formule e nomi del manuale = template; indice di
   00_LEGGIMI = file presenti; comandi e opzioni della guida e dei README =
   parser degli script (`esegui_ciclo_locale.py`, `raccogli_notizie.py` e
   `confronta.py`, che per questo usa argparse; le opzioni di python e pip
   citate nella guida sono escluse; i nomi di comando con trattino, come
   `aggiorna-registro`, si leggono con `[\w-]+`); nomi definiti citati nel
   manuale (anche SI_, classifica*, lente*, pos*, rm*, delta*, quadro*,
   presidio*, copertura*, stato*, capienza*, etichettaCiclo, versioneTemplate);
   il controllo di copertura sta davvero nei nomi coperturaAnagrafica e
   coperturaValutati;
   **versione della struttura** uguale in generatore, script, mappa e template.
6. `run_catena.py` (Excel desktop), su una copia del template: payload
   difettosi fermati senza scrivere un byte (checksum, nessun backup);
   **precontrollo** dal comando vero (D-69, passo 1-bis: soglie invertite =
   codice 1 e `Correzione_A1_2026Q3.txt`, registro intatto; run1 = codice 0); ciclo
   N scritto (copertura, storico KRI in coda con le righe passate identiche,
   rilettura per id, KRI nuovo senza valore ereditato, KRI del ciclo negli
   Indicatori = in vigore, baseline anche .txt, **allegato di A1
   `Input_A1_2026Q4.txt`** con la stessa baseline, controlli e guida, archivio,
   tentativi, righe per le liste);
   validazione **nella griglia** (D-67: una riga per oggetto, celle gialle
   uguali alle proposte, Score e Margine della griglia = Registro e
   Radar_Mosca; il ciclo dopo non parte prima; righe non valide rifiutate
   tutte insieme con la riga del foglio; il margine si ricalcola mentre si
   scrive; Score e Margine della griglia PRIMA di `valida` = quelli del registro
   DOPO; rettifiche e respinta applicate, Respingi per tutti i campi
   dell'oggetto; il periodo esce dalla griglia; proposta conservata; baseline
   aggiornata; `schede-input` fermo prima della validazione);
   **schede (2c)**: input di A6 in ordine di classifica con valori, urgenza,
   storia, KRI; razionale del 2026Q3 (senza parti) intero, `motivazioni` null,
   azioni e KRI con il loro razionale (D-68); output di A6 costruito dal test con i soli dati dell'input,
   fermato con un rischio mancante, una fonte cambiata, un numero inventato,
   una dimensione ripetuta; file con indice e una scheda per rischio; senza A6
   con i testi del registro; registro mai toccato; settimana (codice fonte fuori elenco fermato; segnali netti;
   area non presidiata; rilancio senza duplicati; una riga cancellata a mano
   dalla griglia ferma `valida`, il comando `griglia` la ripara conservando le
   altre; validazione delle notizie);
   baseline N+1 identica a quella usata per i dati di prova; ciclo N+1 (rischio
   nuovo su L1-03 che chiude l'area scoperta; storia di un KRI negli
   Indicatori = storico, anche per un KRI uscito; elenco dei KRI; **Radar_Mosca
   = calcolo indipendente in Python**; Registro con esattamente una riga per
   rischio;
   **◆ nell'etichetta esattamente per i rischi all'attenzione del supervisore**,
   conservata dalla scrittura, un solo cerchio per rischio, nella serie del
   colore del suo livello di allerta); gate
   di copertura; scorrimento della finestra; **errore dopo il salvataggio**
   (file dell'archivio bloccato: messaggio veritiero, baseline aggiornata);
   **primo uso** (`inizializza`, con guida in testa e significato delle
   colonne conservati; primo ciclo con tutti i rischi nuovi) e
   **dismissione** (anagrafica senza buchi, Registro con una riga in meno, KRI e
   azioni chiusi, baseline senza il rischio); **registro di produzione dal
   vuoto al secondo ciclo**: settimane su un registro senza rischi (notizie
   tutte NON PRESIDIATO, zero errori di formula, notizia collegata a un rischio
   inesistente fermata), primo ciclo tutto "Nuovo", secondo ciclo bloccato fino
   alla validazione, baseline del secondo ciclo. E' il percorso reale fino al
   primo ciclo (D-07, D-22); `produzione(e, template=...)` lo rifa' anche sul
   template della stessa versione. **Report al comitato** ai passi 2, 2b, 5 e
   11: score composito = formula D-50 calcolata a parte (media pesata delle
   dimensioni presenti, arrotondamento a meta' in su come ROUND di Excel,
   `Decimal`); Classifica = ordinamento
   indipendente; grafici della Classifica con un punto per rischio; **Quadro:
   rischi segnalati = selezione indipendente** (primi tre, AGIRE ORA, variati,
   nuovi) e **commento di A1 diviso in messaggio e decisioni** (con e senza
   marcatori); Delta con un motivo per rischio e grafico che non copre la nota
   dopo l'adattamento delle altezze; avviso dopo le rettifiche;
   Radar_Mosca con gli anni di adeguamento. **Passo 11,
   aggiornamento del registro in produzione** su
   `dati/registro_template_2026-09-23.xlsx` (costruito una volta con lo script
   del 24/09 e il template del 23/09: una settimana e il primo ciclo validati;
   NON si rigenera): comandi fermati finche' non e' aggiornato; aggiornamento con
   stesse righe, vecchio in Backup e baseline identica a
   `dati/baseline_registro_template_2026-09-23.json`; secondo aggiornamento
   fermato; poi un ciclo intero sul registro aggiornato con un anno di
   adeguamento scritto a mano. **Passo 11b** (30/09) su
   `dati/registro_template_2026-09-25c.xlsx` (un ciclo validato con
   Gap_Controlli e Dimensione; NON si rigenera): fermo con righe "Da decidere"
   su campi tolti dal modello; righe "Da decidere" su campi attuali portate
   nella griglia con la decisione scritta nel vecchio foglio, poi validate;
   colonne dismesse non copiate, colonna Rilievi presente,
   presidio "Non verificato", baseline uguale a
   `dati/baseline_registro_template_2026-09-25c.json`. **Passo 12** (A5
   facoltativo e segnalazioni in validazione, D-71), con un Bloccante di A5 su
   NFR-12, un salto di due punti su NFR-03 e soglie invertite su NFR-01-K1: un
   rischio mancante ferma comunque, con il messaggio per A1; il resto si scrive,
   segnalazioni DA MOTIVARE sui tre rischi (l'osservazione di A5 resta tale),
   Rilievi_Superati e Quadro "3 (controlli 2, A5 1)", `Esito_controlli` con
   `da_motivare` e `a5_usato`; ⚑ sui soli tre rischi e colonna Segnalazioni
   uguale al registro; `--procedi-con-rilievi` accettata ma inutile; `valida` su
   righe non toccate chiede le motivazioni e rifiuta salto e soglie; un
   settimanale scritto durante la validazione conserva cio' che e' gia' scritto
   nella griglia e non si ferma per un valore sbagliato scritto li' (trappola
   71), che `valida` poi segnala; poi la validazione si applica con Prossimita e
   soglie corrette nel registro. Il primo ciclo del passo 10 si scrive senza
   A5. Passo 1: il fermo C9 e' un kri_id di un altro rischio (le soglie
   invertite non fermano piu') e `trimestrale` scrive il messaggio per A1. Nella catena del 2026Q3: esito dallo script, Velocity
   di NFR-10 vuota, NFR-10-K1
   "Soglie da definire", NFR-03-K1 riproposto senza soglie che conserva quelle
   del 2026Q2; in validazione la Velocity di NFR-10 da vuota a 3 ("da n.v.",
   Variato), le soglie di NFR-10-K1 fissate e gli anni di adeguamento di
   NFR-06 rettificati a 1 e scritti nell'anagrafica (D-60); comando `report`
   fermo prima della validazione, poi PDF e versione precedente conservata
   (D-62); in 11b Severity diventa Impatto e Confidence resta nel backup. Un test per ciascuna trappola 15.
   Esito al 25/09 sera (struttura 2026-09-25c): catena con Excel 182/182
   (30-35 minuti), controlli 183/183, riferimenti 28/28, mappa 110/110, fonti
   21/21; al 30/09 (struttura 2026-09-30): controlli 204/204, riferimenti
   28/28, mappa 112/112, fonti 21/21, catena con Excel 214/214 (circa 40 minuti); prompt A1
   7.496, A5 7.563, A3 7.082, A4 5.031, A6 4.624 caratteri; al 30/09 sera
   (struttura 2026-09-30b): controlli 213/213, mappa 112/112, riferimenti 28/28,
   fonti 21/21, catena con Excel 217/217; prompt A1 7.885, A5 7.895, A3 7.082,
   A4 5.050, A6 5.108 caratteri; al 01/10 (struttura 2026-09-30c): controlli 184/184 (meno righe KRI
   d'esempio da controllare), mappa 113/113, riferimenti 28/28, fonti 21/21,
   catena con Excel 230/230; prompt A1 7.917, A5 7.895, A3 7.082, A4 5.050,
   A6 5.111 caratteri.
   Al 01/10 pomeriggio (struttura 2026-10-01): mappa 120/120, controlli 184/184,
   riferimenti 28/28, fonti 21/21, catena con Excel 255/255 (con il passo 3b).
   Al 02/10 (struttura 2026-10-02, griglia di validazione): mappa 126/126,
   controlli 184/184, riferimenti 28/28, fonti 21/21, catena con Excel
   273/273 (circa 45 minuti); prompt invariati. Al 02/10 pomeriggio (D-68,
   razionale in parti nelle schede): mappa 126/126, controlli 194/194,
   riferimenti 28/28, fonti 21/21, catena con Excel 274/274; prompt A1 7.971,
   A5 7.857, A6 5.638. Al 02/10 sera (D-69, allegato di A1 e precontrollo):
   mappa 126/126, controlli 211/211, riferimenti 30/30, fonti 21/21, catena con
   Excel 277/277; prompt A1 7.963, A5 7.902, A3 7.082, A4 5.080, A6 5.638.
   Al 05/10 (D-70, precontrollo in un modulo e kit di Copilot Studio): mappa
   126/126, controlli 224/224, riferimenti 30/30, fonti 21/21, catena con Excel
   277/277; prompt invariati. Al 06/10 (D-71, A5 facoltativo, segnalazioni in
   validazione, struttura 2026-10-06): mappa 126/126, controlli 225/225,
   riferimenti 30/30, fonti 21/21, catena con Excel 275/275; prompt A5 7.962
   (ruolo: i rilievi vanno al validatore), gli altri invariati. Al 07/10 (D-72,
   A7 e Note dell'analista, struttura 2026-10-07): mappa 127/127, controlli
   231/231, riferimenti 30/30, fonti 21/21, catena con Excel 280/280; prompt A7
   6.575, gli altri invariati.
   Una eccezione diventa un KO, non nasconde i KO gia' trovati.
7. **Dati di prova rigenerati con lo strumento vero**: baseline estratte dal
   template e dopo la validazione; payload di A1/A3/A5 scritti SU quelle
   baseline e sottoposti a schema e controlli; decisioni del validatore come
   file JSON che il collaudo scrive nella griglia del foglio Validazione
   (`comune.scrivi_decisioni`, come una persona: cambia la cella gialla,
   scrive Respingi e la Motivazione).
   Dichiara che i payload sono simulati, non output dell'agente reale. Quando
   cambia il modello (es. 30/09), si convertono i payload con uno script usa e
   getta e **si rigenerano le baseline attese ripetendo i passi della catena**,
   poi si confrontano con le vecchie campo per campo: devono cambiare solo i
   campi previsti.
8. **Prove di mutazione**: rompi deliberatamente almeno un controllo per area
   (codice fonte non verificato, rettifiche non applicate, prompt non
   ricomposto, colonna rinominata) e verifica che la suite se ne accorga.
9. **Guarda i grafici**: esporta le immagini ed esaminale; il collaudo verifica
   i dati, non l'aspetto.

Il collaudo a componenti isolati NON basta: le incoerenze stanno nelle cuciture.

## DEMO (fuori dal pacchetto, cartella `Demo_W1_W2/`)

`esegui_demo.py`: controlla prima che nessun file della demo precedente sia
aperto; raccolta W0 **reale**; W1 con un A1 difettoso (fermato) e corretto;
tentativo del ciclo dopo prima della validazione (fermato); validazione;
settimana con validazione; ciclo dopo con validazione e **riapertura della
validazione** di un rischio (`riapri --rischi`, poi `valida`: D-76); schede del ciclo
(`schede-input` e `schede` senza A6: gli output di A6 non si simulano nella
demo) e PDF del report al comitato (fogli da Quadro a Metodologia dell'Excel
validato); esporta le immagini dei grafici (Quadro, Classifica, lente,
Radar_Mosca, Delta, Storico, Notizie anche nella settimana con l'area
scoperta, storia di due KRI); poi una settimana in cui A3 propone un **ciclo
straordinario**, la decisione (`baseline --straordinario`), lo straordinario
`AAAAQn-S1` su un rischio, scritto e validato (D-75), con Radar_Mosca e Storico
esportati di nuovo.
`Demo_W1_W2/Archivio_Cicli/` (registri congelati, backup, PDF, baseline) non si versiona
(`.gitignore`, richiesta dell'utente del 13/10: era l'84% dello zip): lo ricrea la demo.
`REPORT_demo.md`: cosa produce ogni agente e cosa decide il validatore, con
tabelle e immagini, dichiarando cosa e' simulato e cosa e' eseguito davvero.

**Quando rigenerare la demo** (regola del 07/10/2026, voce M2 del TODO): solo
quando cambia cio' che si vede (template e viste, report, schede, knowledge di
A7, passi della guida, comandi e loro messaggi) e sempre prima di consegnare un
pacchetto in Banca; non a ogni modifica interna (prompt, testi del kernel,
controlli gia' coperti dal collaudo). Dopo la demo, `REPORT_demo.md` si
riallinea ai numeri nuovi (righe, livelli, segnalazioni).

## TRAPPOLE GIA' INCONTRATE — non reintrodurle

1. Date passate a COM come `datetime`: pywin32 le converte in UTC e slittano di
   un giorno. Scrivere **seriali di Excel**.
2. Una colonna formula aggiornata con un valore si svuota in silenzio: le
   colonne formula non si scrivono mai; dopo ogni scrittura si verifica che
   ogni riga abbia la formula.
3. Un nome definito sbagliato si vede solo ricalcolando (#NAME?): ricalcolo con
   il motore vero sempre.
4. Dati di esempio che citano fonti "dal futuro": il collaudo li controlla.
5. Messaggio "non salvato" dopo il salvataggio: vedi codici di uscita.
6. Titolo e legenda sopra i grafici (overlay); assi nascosti; varyColors;
   linee smussate; dati in colonne nascoste non disegnati.
7. La knowledge di Agent Builder non legge .json ne' .md.
8. `shutil.copy2` verso una cartella copia DENTRO la cartella: per simulare un
   file bloccato serve un file in sola lettura.
9. COM in italiano: `Names.Add` interpreta la formula nella lingua di Excel;
   i nomi definiti si creano con openpyxl in generazione.
10. Il periodo settimanale va scritto come **testo** (`'2026-10-12`): come data
    tornerebbe numero e il confronto fallirebbe.
11. "Nome Cognome" contro "Funzione Compliance": una sola regola dell'owner,
    usata da C8 e dalla validazione.
12. Heredoc con backslash (`\b`, `\n`) negli script di modifica: usa file o lo
    strumento di modifica diretta.
13. Feed RSS "noti" non piu' validi (BIS/BCBS, ENISA, CSIRT, EBA vecchio):
    prova ogni indirizzo dal vivo.
14. Un file dell'archivio aperto in Excel dall'utente blocca demo e archivio:
    controllalo prima di iniziare.
15. (Revisione del 23/09 sera, tutte con un test.) Esito di A5 di un altro
    ciclo accettato; Variazioni che contraddicono i valori validati;
    `Righe_liste` prodotte prima della validazione e mai aggiornate; testo "="
    scritto come formula e "5/6" come data; JSON con BOM rifiutato; notizie
    duplicate nello stesso output; valore del validatore ignorato senza
    "Rettificato"; KRI rettificato senza data; un rischio tolto a mano che
    lascia un buco (radar senza l'ultimo rischio) e KRI in vigore per sempre;
    capacita' delle viste superate in silenzio; `confronta.py` che ignorava la
    Probabilita; errori COM transitori all'avvio di Excel.
16. **Mai una tabella del registro senza righe.** `ListRows.Add` su una tabella
    vuota inserisce la riga in cima all'intervallo dei nomi definiti (riga 2):
    i nomi assoluti scivolano in basso a ogni aggiunta (RR_ID_Rischio da $C$2 a
    $C$14 dopo 12 righe) e le viste non vedono piu' i dati (copertura 12/0).
    `inizializza` lascia quindi una riga **segnaposto** (valori vuoti, formule
    presenti, senza fondo grigio) che la prima scrittura riempie; `righe()` non
    la conta. Trovato dal test del primo uso: senza quel test il registro vero
    sarebbe nato rotto.
17. (Prima installazione reale, 24/09.) **`import win32com` non basta come
    verifica**: con pywin32 installato a meta' passa, poi lo script fallisce su
    `pythoncom`. La guida verifica `win32com.client` + `pythoncom` + avvio di
    Excel. `pywin32_postinstall` non esiste piu' dalla versione 312: basta il
    reinstall forzato.
18. **urllib non legge il PAC del proxy aziendale**: le fonti che il PAC
    instrada sul proxy (i domini `europa.eu`) vanno in timeout dallo script,
    anche se si aprono nel browser. `pypac`, con la scoperta del PAC fatta una
    sola volta. Diagnosi: se si apre nel browser ma non dallo script, e' il
    PAC; se non si apre nemmeno nel browser, e' un blocco vero (IT).
19. **`Workbook non trovato: None`** vuol dire che manca `configurazione.json`,
    non che il percorso e' sbagliato: la guida distingue i due casi.
20. **Primo ciclo da registro vuoto: A1 numera da se' i rischi nuovi.** Due run
    danno numeri diversi allo stesso rischio, e il confronto per id segnalerebbe
    differenze che non esistono. `confronta.py --primo-ciclo` abbina per event
    type e nome e stampa gli abbinamenti da controllare.
21. **Dati di esempio che citano una fonte esclusa** vengono rifiutati dalla
    scrittura settimanale: quando si esclude una fonte (FNT-19), le notizie di
    esempio e di prova passano a `MAN` e il template si rigenera. Lo intercetta
    `test_fonti.py`.
22. **Code interpreter acceso di default in Agent Builder**: "capability
    nessuna" va scritto come azione (spegnere il toggle), non come assenza.
23. **Controllo delle opzioni citate nella guida**: le opzioni di pip
    (`--upgrade`, `--force-reinstall`) non sono opzioni degli script ed erano
    segnalate a torto. Vanno escluse, come `--version`.
24. **Il registro vuoto riceve settimane prima del primo ciclo**: A3 deve
    lasciare `rischio_collegato` a null (una notizia collegata a un rischio
    inesistente e' fermata) e le viste devono reggere notizie senza rischi.
    Lo verifica il passo 10 della catena.
25. (25/09) **Serie su colonne nascoste scartate**: con "solo celle visibili"
    (il default) Excel toglie da `SeriesCollection` le serie i cui dati sono
    tutti nascosti; il grafico esce vuoto senza errori. Ogni grafico che legge
    colonne di appoggio nascoste vuole `visible_cells_only = False` (Classifica,
    lente, Radar_Mosca). Il collaudo conta i punti delle serie.
26. **Il confronto "=" di Excel ignora le maiuscole**: `LEFT(L5,5)="AGIRE"` vale
    anche per "Agire entro l'anno", che veniva colorato di rosso come "AGIRE
    ORA". Distinguere con prefissi diversi (`LEFT(L5,9)="AGIRE ORA"`,
    `LEFT(L5,11)="Agire entro"`) o con EXACT.
27. **Funzione TEXT e lingua di Excel**: il formato ("0.00") si interpreta nella
    lingua dell'utente; nei testi dei fogli di report i numeri passano da
    `FIXED`, che usa i separatori locali senza codici di formato.
28. **Combinare due grafici in openpyxl**: `colonne += rombi`, non `colonne +
    rombi` (quest'ultimo solleva "Cannot combine instances of different
    types"). Gli assi sono condivisi se hanno gli stessi id (10 e 100, il
    default).
29. **Cambio di struttura del workbook con un registro gia' in uso**: il
    registro nato dal template vecchio non ha le colonne e i nomi nuovi; una
    scrittura con la mappa nuova scriverebbe fuori dall'anagrafica o in
    colonne sbagliate. Da qui `versioneTemplate` (lo script si ferma) e
    `aggiorna-registro` (copia per nome di colonna e verifica la baseline). Il
    collaudo usa un registro vero del template precedente, non uno simulato.
30. **Mappa vecchia nella library Kernel**: lo script legge la mappa da
    `Kernel`, che il PC sincronizza; una mappa non aggiornata con script e
    template nuovi darebbe una scrittura incoerente. La mappa porta
    `versione_template` e lo script la controlla.
31. **Spazio nel prompt di A1**: aggiungere una riga costa caratteri che vanno
    tolti dallo stesso prompt; tagliare la tassonomia cambia anche A3 e A4 (da
    ricaricare senza motivo). Si taglia nel modello di A1 o nelle sezioni della
    rubrica che entrano solo in A1 e A5, poi si confronta A3/A4 con la versione
    gia' incollata.
32. **Regex dei comandi citati**: `esegui_ciclo_locale\.py (\w+)` legge
    `aggiorna` da `aggiorna-registro` e segnala un comando inesistente: `[\w-]+`.
33. **Il commento dell'agente precede la validazione**: la `sintesi` di A1 e'
    scritta nel ciclo, le rettifiche arrivano dopo. Il Quadro (prima la Sintesi) non la
    corregge (e' testo dell'agente, conservato): avvisa quante rettifiche e
    respingimenti sono stati applicati dopo, e numeri e grafici restano quelli
    validati.
34. (25/09 sera) **Excel non adatta l'altezza di una cella unita**: la guida
    in riga 2 (cella unita, testo a capo) resterebbe tagliata a una riga. Il
    generatore stima le righe dal testo e dalla larghezza delle colonne unite
    e fissa l'altezza; va rifatta la stima se cambiano testo o larghezze.
35. **Spostare le tabelle dati sotto una guida**: i nomi definiti partono
    dalla prima riga dati (5), e ogni formula che converte la riga del foglio
    in posizione nel nome (`INDEX(nome, ROW(...)-k)`) deve sottrarre
    `PRIMA_RIGA_DATI - 1`, non 1. Le formule `INDEX(Foglio!$X:$X, ROW(...))`
    su colonna intera non cambiano. Lo script scrive per tabella
    (`ListRows`), quindi non se ne accorge; `aggiorna-registro` porta i
    registri con le tabelle in A1 sul layout nuovo.
36. **Rich text in openpyxl**: `CellRichText` di `TextBlock(InlineFont(...))`;
    rileggendo con `load_workbook` senza `rich_text=True` il valore e' una
    stringa semplice (i controlli che cercano stringhe continuano a
    funzionare).
37. **Heredoc con backslash, di nuovo** (trappola 12): una regex con `\\` in
    uno script passato con heredoc si rompe ("unterminated character set").
    Script di modifica sempre in un file.
38. **Stati senza processo**: "In corso" e "Completata" delle azioni erano
    ammessi dalla convalida ma nessun passo li scriveva, e la guida vietava
    di toccare i dati. Deciso: si scrivono a mano nella sola colonna Stato
    (guida passo passo, foglio Guida, workflow). Ogni valore ammesso deve avere chi lo scrive.
39. **Un testo che inizia con "=" diventa una formula** in openpyxl ("= 0,00"
    per una variazione nulla): Excel non apre il file ("Errore nel metodo
    Open"). Nessun testo scritto dal generatore deve iniziare con "=" (qui:
    "● 0,00"); lo script di campo ha gia' la stessa protezione per i testi
    degli agenti.
40. **Barre negative bianche**: in un grafico a barre openpyxl lascia
    `invertIfNegative` attivo, ed Excel disegna senza colore le barre sotto
    zero. Per il Delta: `invertIfNegative = False`.
41. **Grafico vuoto su colonne nascoste** (di nuovo la trappola 25): vale per
    ogni grafico, anche nelle anteprime.
42. (25/09 sera) **Intervallo senza foglio in un nome definito**:
    `OFFSET(Delta!$AN$5,0,0,MAX(1,COUNT($AK$5:$AK$19)),1)` fa rifiutare il file
    a Excel ("Errore nel metodo Open"), senza dire dove. In un nome definito
    ogni intervallo porta il foglio. Per trovare un file che non si apre:
    generarlo con un foglio di vista alla volta e aprirlo in Excel (bisezione).
43. **Formattazione condizionale senza colore**: un `PatternFill` con il solo
    `fgColor` in un formato condizionale lascia la cella bianca (Excel usa il
    colore di sfondo nei formati differenziali): dare `fgColor` e `bgColor`.
    Da una cella bianca con testo bianco (etichetta "AGIRE ORA") non si vede
    niente: controllare il PDF.
44. **Etichette "#N/D" e "0,00" sulle barre**: le serie "una per esito"
    hanno #N/D (o zero) dove il rischio non ha quell'esito; Excel scrive
    l'etichetta anche per quei punti. Zero invece di NA() e formato
    `0.00;-0.00;;` sulle celle di origine (un `numFmt` sulle etichette non
    basta: openpyxl non scrive `sourceLinked="0"`).
45. **Il controllo degli errori ammette solo #N/D con NA() nella formula**:
    una vista che rilegge un #N/D con INDEX (senza NA()) diventa un "errore di
    formula" e ferma la scrittura. Ogni formula che puo' dare #N/D lo scrive
    esplicitamente. E: in un patch passato con heredoc Bash, `\n` dentro una
    f-string Python diventa un a capo vero e rompe il codice (trappola 12,
    ancora): script di modifica in un file, controllati con `pyflakes`.
46. **Righe adattate piu' basse del grafico accanto**: nel Delta il grafico sta
    accanto ai motivi; quando lo script riduce le righe dei motivi al loro
    testo, il grafico passa sulla nota della scala e oltre il salto pagina (visto
    solo nel PDF della demo, dopo `prepara_report`, non nel template).
    `spazio_per_il_grafico` allunga la riga vuota sotto i motivi; il collaudo
    confronta fondo del grafico e inizio della nota. Guardare sempre il PDF di un
    registro scritto dallo script, non solo quello del template.
47. **Pacchetto arrivato senza `03_Excel/NFR_Dashboard_Template.xlsx`** (visto
    su un PC reale, 29/09): la cartella `03_Excel` esisteva con
    `genera_dashboard.py` e `costruzione_manuale_template.md` ma senza il
    file binario, filtrato dal gateway di posta aziendale nel trasferimento
    dello zip. Il messaggio "Template non trovato: ..." dello script (in
    `inizializza` e `aggiorna-registro`) ora dice esplicitamente il rimedio
    (`python genera_dashboard.py` nella cartella `03_Excel`, o `--template`
    per un percorso alternativo) invece di limitarsi al percorso: chi installa
    non deve capirlo da solo. Il percorso del template NON e' in
    `configurazione.json`: e' sempre `03_Excel/` fianco a fianco con
    `07_Senza_Studio/` (`TEMPLATE_PREDEFINITO = QUI.parent / "03_Excel" / ...`).
48. **Guida di prima installazione spezzata fra due file**: chi installava per
    la prima volta (PC reale, 29/09) doveva seguire `00_GUIDA_PASSO_PASSO.md`
    per Python/PC ma saltare a `07_Senza_Studio/README_variante_locale.md` per
    la creazione degli agenti (knowledge, capability, modalita'), senza che
    nessuno dei due file dicesse esplicitamente di fare l'altro salto — e senza
    un controllo esplicito che `03_Excel` contenesse davvero l'xlsx (trappola
    47), ne' un chiarimento che la sezione "aggiornare il registro a un
    template nuovo" (0-bis) non riguarda affatto chi non ha ancora un
    registro. La sezione 0 della guida ora e' il percorso unico e ordinato
    (0.1 amministratore SharePoint, 0.2 manutentore/agenti, 0.3 PC
    dell'analista con il controllo di 03_Excel, 0.4 primo registro), con
    `README_variante_locale.md` richiamato per il "perche'" (limiti di Agent
    Builder) invece che per i passi stessi; 0-bis apre dicendo a chi non serve.
    Chi rigenera il pacchetto: se cambia la tabella agenti, aggiornarla in
    entrambi i file (la guida e' quella da correggere per prima) o farla
    scrivere da un'unica fonte, non a mano in due posti.
49. **`PAROLE_FUNZIONE` (C8, `controlli_a5.py`) troppo corta ferma owner
    validi** (PC reale, 29/09): l'euristica "sembra una persona" (owner con
    forma "Parola Parola" e nessuna parola di funzione) e' Bloccante apposta
    (D-13), ma l'elenco delle parole di funzione era troppo corto e in
    prevalenza italiano: owner reali della Banca come "Cyber Security",
    "Information Security", "Operational Resilience", "Data Governance",
    "Data Management", "Comunicazione Istituzionale" **non contenevano
    nessuna** delle parole allora in elenco (mancavano security, cyber,
    information, resilience, governance, management, comunicazione,
    istituzionale, operational) e fermavano il ciclo trimestrale con **il
    registro intatto** ma nessun dato scritto, pur essendo owner legittimi.
    L'elenco e' pensato per essere esteso quando emergono nomi di funzione
    reali (stesso principio di `FRASI_GENERICHE`, riga 20): aggiungere la
    parola mancante, non riscrivere l'euristica. `sembra_persona` e' condivisa
    fra il controllo di A5 e la validazione umana (riga 741 di
    `esegui_ciclo_locale.py`): una correzione qui vale per entrambe. **Dal
    30/09 (D-54) C8 e' solo Osservazione**: il 29/09 fermava anche
    "Immobili, Infrastrutture e Procurement"; la regola vera sta in `valida`,
    che rifiuta un owner persona anche se Accettato. L'elenco resta, ampliato
    (procurement, acquisti, immobili, infrastrutture, tecnologia,
    organizzazione, operativa/o, controlli, business).
50. **`fonti[].tipo` di A1 seguiva la cartella, non il contenuto** (primo ciclo
    reale, 29/09): A1 taggava "Interna" qualunque documento letto da
    `Analisi_Interne`, inclusi report di terzi (es. ORX) semplicemente perche'
    erano salvati li' dentro — A5 bloccava poi il ciclo su C5 (confidence non
    sostenuta da fonte interna qualificata) senza che il vero problema
    (l'etichetta sbagliata) fosse mai nominato. Aggiunta una riga all'Input di
    A1 (modello, non rubrica: costava budget solo ad A1, non anche ad A5):
    "'Interna' solo se della Banca, mai un fornitore/consorzio". A1 e' quasi
    sempre al limite di 8.000 caratteri: prima di aggiungere, misurare con
    `componi_prompt.py --verifica` e cercare uno sconto altrove (qui: una
    ridondanza in un passo della procedura) piuttosto che sforare.
    Conseguenza collegata: FNT-35 rinominata da "Database di perdite operative
    esterne" (`Analisi_Interne/Perdite_Esterne`) a "Fonti esterne di
    orizzonte", scope allargato da sole
    perdite di consorzio a qualunque fonte esterna di orizzonte — su richiesta
    dell'utente: per l'Horizon Scanning le fonti esterne sono spesso le PIU'
    rilevanti (un rischio davvero emergente non ha ancora una traccia interna),
    non una categoria minore. Poi (D-45, 29/09) la causa e' tolta alla radice:
    una **settima library `Analisi_Esterne`** (indirizzo di FNT-35), separata da
    `Analisi_Interne`, e nell'Input di A1 la regola "tipo segue la cartella"
    (Interna solo per `Analisi_Interne`). Un documento di terzi finito in
    `Analisi_Interne` si sposta, non si rietichetta. La domanda sui descrittori
    di Confidence e' stata chiusa da D-46 (29/09) e completata da D-52 (30/09):
    nessun livello richiede una fonte interna.
51. **Colonne tolte dal modello fermano la migrazione** (30/09):
    `aggiorna-registro` si fermava se una colonna del registro vecchio non
    esiste nel template nuovo — giusto per un errore, sbagliato per una colonna
    tolta apposta (Gap_Controlli, Dimensione delle azioni). Rimedio: sezione
    `colonne_dismesse` della mappa, che il comando salta (restano nel backup);
    ogni altra colonna mancante continua a fermarlo. E prima di copiare, fermo
    se ci sono decisioni "Da decidere": una decisione aperta su un campo tolto
    non si potrebbe piu' applicare.
52. **Pesi scritti nei testi** (30/09): Metodologia, nota della scala del
    Delta, Dizionario, guida e documenti riportavano "0,30 Severity + 0,20 ..."
    e i nomi `pesoGap`: cambiando i pesi restavano veri solo in Parametri. Nel
    workbook i pesi si leggono dai nomi (`=pesoSeverity`, `FIXED(pesoSeverity/
    (somma dei pesi presenti),2)`), mai scritti; nei documenti si citano con la
    decisione (D-50) e vanno aggiornati con lei. Cercare `0,30`, `0,15`,
    `pesoGap`, `B9` dopo ogni cambio di pesi.
53. **Campi che A1 ricopia dalla baseline o che lo script sovrascrive**
    (30/09): (a) dopo aver tolto un campo dallo schema, A1 tende a riscriverlo
    se la baseline o gli esempi lo contengono ancora (esito, gap_controlli): lo
    schema lo rifiuta (`additionalProperties: false`), il passo 10 dice
    "nessun campo in piu'", e la baseline va ricaricata in `Kernel` dopo
    `aggiorna-registro`; (b) un KRI riproposto con soglie null NON deve
    cancellare le soglie validate: la scrittura conserva quelle in vigore
    (D-53); (c) esito e "da/a" si calcolano DOPO i controlli
    (`completa_payload` all'inizio di `scrivi_trimestrale`), perche' A5 e i
    controlli devono vedere il payload come l'ha scritto A1.
54. **Codici dello strumento di ricerca nelle fonti** (primo ciclo reale,
    29/09): tutti i 26 riferimenti di A1 iniziavano con `turn1search17 - ...`,
    un marcatore interno della chat di Copilot, irrintracciabile e destinato a
    finire nelle schede. Rimedio doppio: riga nel passo 10 di A1 e
    `pulisci_riferimento` (regex `CODICE_RICERCA`) nello script, che non
    lascia mai un riferimento vuoto o sotto i 5 caratteri.
55. **Un valore facoltativo vuoto letto come zero** (30/09): una soglia KRI
    vuota vale 0 nei confronti e dava un falso **Rosso**; una Velocity vuota
    letta con SUMIFS vale 0 e produceva nel Delta un falso "Aumento > 1 punto".
    Rimedi: lo Stato del KRI controlla le soglie vuote PER PRIMO ("Soglie da
    definire"); ogni COUNTIFS che precede un SUMIFS su un campo facoltativo ha
    anche `campo,"<>"`; nelle viste la Velocity vuota e' "n.v." e la soglia
    vuota #N/D; la nota del Delta usa AGGREGATE(4|5,6,...), che ignora i #N/D.
56. **Un testo fra virgolette di oltre 255 caratteri dentro una formula**
    (30/09): openpyxl lo scrive senza errori, ma Excel rifiuta di aprire il
    file ("Errore nel metodo Open per la classe Workbooks", anche da COM). Era
    la nota della scala del Delta diventata formula. Spezzare i testi lunghi
    con `"..."&"..."`; dopo ogni modifica al generatore aprire il template con
    Excel (non basta openpyxl) e cercare letterali > 255.
57. **Alzare `MAX_RISCHI` rompe l'impaginazione** (30/09, da 15 a 20): le righe
    per rischio con altezza fissa (motivi del Delta 30 punti, elenco dei
    rischi nel Quadro 16 punti, rischi segnalati 52 punti) spingevano oltre la
    pagina il grafico o i limiti, e il report usciva con pagine vuote. Nel
    template le righe senza esempio nascono basse (lo script le adatta con
    `prepara_report`), l'elenco del Quadro passa a 12 punti; controllare il
    numero di pagine del PDF di Quadro e Delta (2 e 2) dopo ogni cambio di
    capacita'.
58. **Arrotondamento del composito nel collaudo** (30/09): con i pesi divisi
    per 0,8 (Velocity mancante) lo score puo' finire in ...,125; `round()` di
    Python arrotonda al pari (3,12), il ROUND di Excel a meta' in su (3,13). Il
    calcolo indipendente del collaudo usa `Decimal` con `ROUND_HALF_UP`.
59. **Parametri conservati che coprono i valori nuovi** (30/09 sera): la
    migrazione copiava nel template nuovo tutti i parametri di input del
    registro vecchio; cambiando soglie e Z (D-59, D-61) il registro aggiornato
    avrebbe tenuto 3, 0,40 e 0/0,5/1,5/2,5/4. Si conservano solo ciclo,
    settimana e i parametri di Mosca che la Banca imposta
    (`PARAMETRI_DA_CONSERVARE`); pesi, soglie e Z vengono dal template, e lo
    script stampa quelli vecchi.
60. **Una colonna rinominata e' una colonna "tolta" piu' una "nuova"**
    (Severity -> Impatto): senza `colonne_rinominate` la migrazione si ferma
    (colonna del vecchio che non esiste nel nuovo) o, se la si mette fra le
    dismesse, perde i valori. Anche il codice che legge le righe per nome
    (`colonna()`) deve accettare il nome vecchio. Le variazioni scritte prima
    restano con la dimensione "severity": Delta e schede la mostrano cosi' com'e',
    `variazioni_dopo_rettifica` ignora i campi che non sono dimensioni.
61. **Un campo validato che non e' una dimensione** (Anni_Adeguamento): la
    riscrittura delle variazioni dopo la validazione non deve crearne una, e il
    valore va dove la formula lo legge (l'anagrafica, non la riga del ciclo:
    Radar_Mosca legge `Parametri!M`).
62. **Messaggio di errore dopo la sostituzione del file** (30/09 sera): un
    errore di concatenazione nella stampa finale di `aggiorna-registro`,
    avvenuto dopo che il registro era gia' stato sostituito, faceva dire allo
    script "il workbook non e' stato salvato". Dopo `os.replace` lo script
    registra il salvataggio (`SALVATO`), come dopo `salva_con_backup`, cosi'
    l'errore tecnico dice "DOPO IL SALVATAGGIO ... NON rilanciare"; e le stampe
    dopo il salvataggio si provano nel collaudo (passo 11b) come il resto.
63. **Il codice di un KRI nuovo e' il primo progressivo LIBERO** (01/10): nei
    dati d'esempio ridotti a due KRI per rischio (D-64), togliere NFR-02-K1
    avrebbe fatto prendere K1 al KRI nuovo del 2026Q3 invece di K4, e i test che
    citano i codici sarebbero falliti senza che il codice fosse sbagliato. Chi
    cambia i KRI d'esempio controlla i codici attesi nel collaudo (passi 2, 5,
    9) e nei dati di prova.
64. **Un indicatore in piu' che scatta per tutti non informa** (01/10): il
    livello di allerta richiede due segnali forti per l'Attivazione e, per
    l'Attenzione, un motivo di merito oltre al margine stretto; con i KRI a due
    per rischio, "meta' dei KRI in ambra o rosso" vuol dire basta uno. Dopo
    ogni cambio di regole o soglie, contare i livelli sulla demo prima di
    consegnare (come per la Z, D-59). Piu' rischi segnalati allungano la
    pagina 2 del Quadro: nella demo del 01/10 Limiti e legenda erano finiti su
    una terza pagina; ora `scala_quadro` adatta la scala e il collaudo verifica
    "Quadro in due pagine" a ogni report.
65. **Colore del cerchio e colore del tema di vigilanza** (01/10): con il
    riempimento per livello (giallo = Attenzione) il bordo giallo dei temi del
    supervisore (D-35) diventava ambiguo: il supervisore passa al ◆
    nell'etichetta. La trasparenza si aggiunge per colore esatto nell'XML: i
    colori dei livelli non vanno usati altrove nei grafici, e il file si
    riscrive una volta per colore (tentativi ripetuti se l'antivirus lo
    trattiene, `PermissionError` su `os.replace`).
66. **Il limite di 8.000 caratteri decide cosa entra in A1** (01/10): ogni
    regola nuova (due KRI, esposizione, "ragiona con cura") costa caratteri; si
    recuperano accorciando esempi ridondanti della rubrica, non togliendo
    regole. Dopo ogni modifica `componi_prompt.py`, e il margine si annota qui.
67. **Un aggiornamento del pacchetto sovrascrive il kernel della Banca** (01/10,
    sul PC della Banca): la Banca aveva modificato `tassonomia_nfr.md` sul suo
    PC; lo zip di aggiornamento conteneva la versione del manutentore e l'ha
    sostituita, e i prompt erano composti da quella. La guida (0-bis, punto 0;
    sezione 6) dice ora che le modifiche al kernel si danno al manutentore
    PRIMA dell'aggiornamento, che modificare il kernel da solo non cambia gli
    agenti, e come recuperare la versione precedente (cronologia di OneDrive o
    della library). E i passi per chi aggiorna non devono mai rimandare a
    programmi del manutentore (`componi_prompt.py`): i prompt arrivano gia'
    composti.
68. **Le viste vanno provate dopo la validazione, non solo il dato** (01/10):
    il collaudo verificava che la rettifica del segnale di una notizia
    cambiasse la riga del NewsLog, ma non che badge, foglio Notizie e livello
    di allerta seguissero rettifiche e respingimenti. Il passo 3b scrive una
    settimana sul template, controlla le viste, valida (un respingimento, una
    rettifica) e le ricontrolla. E un output dell'agente scritto solo
    nell'archivio JSON (sintesi e flag di A3) non lo legge nessuno: ogni testo
    per le persone deve arrivare in un foglio (D-66).
69. **Lo Stato del foglio Validazione cancellato a mano** (01/10, in Banca):
    compilando le decisioni in Excel e' stata svuotata l'intera colonna Stato;
    `valida` diceva "Nessuna decisione da prendere", che non aiuta. Ora, se le
    righe del periodo hanno uno Stato diverso da "Da decidere" e "Applicata",
    `valida` si ferma con il numero di righe e il rimedio (rimettere "Da
    decidere": le Decisioni restano); la guida (sezione 3) dice che si scrivono
    solo Decisione, Valore_Validato e Motivazione; il passo 3b lo prova. Per
    capire cosa c'e' davvero nel registro: confrontarlo con la copia salvata dal
    comando nel `Archivio_Cicli` (e' il registro come l'ha lasciato lo script).
    Dal 02/10 (D-67) il validatore non scrive piu' nello storico: lavora nella
    griglia e lo storico (foglio Storico_Validazioni) lo scrive solo lo script;
    il controllo resta, il rimedio aggiunge il comando `griglia`.
70. **Un'altezza di riga impostata rende visibile una riga nascosta** (01/10,
    griglia di validazione): la griglia nasconde le righe libere e adatta
    l'altezza delle righe scritte ai testi (Excel non lo fa con le celle
    unite). Impostando `RowHeight` dopo `Hidden` le righe nascoste
    ricomparivano. Ordine: prima le altezze, poi si nascondono le righe libere.
    Verificato anche che una colonna di celle unite (owner e rischio, C:D ed
    E:F) si scrive in un colpo solo con un vettore sul nome della colonna.
71. **Una cella dove scrive una persona non deve poter rompere il registro**
    (02/10): nella griglia il validatore scrive valori liberi; un 9 nella
    Prossimita darebbe #RIF! nel Margine (INDEX oltre la tabella di Z), e il
    controllo "zero errori di formula" di ogni scrittura fermerebbe anche un
    settimanale. Tutte le formule della griglia stanno dentro IFERROR; il
    valore sbagliato lo segnala `valida`, con la riga, quando si valida. Il
    passo 12 lo prova (settimanale scritto con un 9 nella griglia).
72. **Righe e campi sono due unita' diverse** (02/10): lo storico ha una riga
    per campo (12 rischi x 5 + 25 KRI x 3 + 15 azioni x 2 = 165), la griglia una
    per oggetto (52). "Righe da validare" del Registro e del Quadro contavano i
    campi e non tornavano con la griglia: ora contano gli oggetti (il primo
    campo di ognuno); l'avviso "Dopo il commento" conta i valori rettificati
    piu' gli oggetti respinti (un'azione respinta una volta, non per campo); il
    riepilogo di `valida` e' per righe della griglia, con i valori cambiati fra
    parentesi.
73. **Una riga non toccata vale come accettata** (02/10): e' la comodita'
    voluta, ma una validazione "di facciata" non lascia piu' una traccia
    diversa ("Accettato in blocco" spariva con `--accetta-il-resto`). Presidi:
    quota di rettifiche visibile (Registro G4, riepilogo di `valida`), ⚑ che
    chiede la Motivazione anche senza cambi per un rischio con un bloccante di
    A5 superato, governance riscritta. Un owner proposto che sembra una persona
    si ferma anche se la riga non e' toccata. `--accetta-il-resto` resta
    accettata senza effetto, con un avviso, per non rompere comandi gia' in uso.
74. **La migrazione non deve fermarsi su cio' che il validatore sta facendo**
    (02/10): `aggiorna-registro` si fermava se c'erano righe "Da decidere";
    in Banca bastava una settimana non validata per bloccare l'aggiornamento.
    Ora le righe in sospeso passano nella griglia del registro nuovo con le
    decisioni gia' scritte, anche nel vecchio formato a una riga per campo
    (`modifiche_vecchio_formato`); si ferma solo se riguardano campi tolti dal
    modello, perche' nella griglia non c'e' piu' una cella dove deciderle.
    Passo 11b.
75. **Il perche' di un numero lo sa chi ha letto il documento** (02/10,
    schede): l'utente voleva accanto a ogni valore il motivo e i documenti da
    cui viene. A6 non ha letto i documenti (vede solo i riferimenti): una sua
    attribuzione "questo documento sostiene l'Impatto" sarebbe plausibile ma
    non verificabile. Il perche' lo scrive A1 nel razionale, diviso in parti;
    lo script lo divide (non A6) e lo mette accanto al valore; A6 lo riformula
    e non attribuisce a un documento cio' che A1 non gli attribuisce.
76. **Un'etichetta a meta' frase non e' un'etichetta** (02/10): i razionali
    scritti prima contengono "Prossimita' sale a 5:" e "Impatto resta 4:", che
    una ricerca ingenua di "IMPATTO:" senza maiuscole spezzerebbe a caso.
    `parti_razionale` accetta un'etichetta solo all'inizio del testo o dopo un
    punto, un punto e virgola o un a capo, oppure scritta tutta in maiuscolo; il
    collaudo prova entrambi i formati sui dati di prova (`run1`/`run2` vecchi,
    `run3` nuovo).
77. **Il formato si chiede nello scheletro, non si impone con un fermo**
    (02/10): un pattern nello schema avrebbe fermato ogni output di A1 senza
    etichette, cioe' un altro giro di A1 per una questione di forma (il primo
    ciclo reale ne aveva richiesti sette-otto). Il razionale senza parti passa:
    `trimestrale` stampa un avviso (di solito vuol dire istruzioni di A1 non
    reincollate) e la scheda lo mostra intero, come prima. Lo scheletro costa
    pochi caratteri e mostra dove va il testo; l'avviso fa da controparte
    deterministica senza bloccare.
78. **Le regole che A1 deve rispettare gli si danno con le stesse parole di
    chi lo controlla, ma il controllo resta fuori da A1** (02/10, D-69): i
    controlli di A5 stanno in un solo file del kernel e finiscono sia nel prompt
    di A5 sia nell'allegato di A1; una copia a mano divergerebbe al primo
    ritocco. Pero' un modello che rilegge il proprio output tende a confermarlo:
    l'autocontrollo del passo 10 riduce i giri, non li elimina. La verifica
    affidabile prima di A5 e' quella dello script (`precontrollo`), con gli
    stessi controlli meccanizzati di `trimestrale` e il messaggio di correzione
    gia' scritto. Il precontrollo non apre Excel ne' il registro: si lancia in
    pochi secondi tutte le volte che serve. Nessun fermo nuovo: le regole sono
    quelle di prima.
79. **Un esempio guida la forma piu' di una regola, e quindi deve essere
    giusto** (02/10, D-69): nella guida di scrittura l'esempio completo vale piu'
    di altre istruzioni, ma A1 ne copia anche gli errori. La prima stesura dava
    Probabilita 4 a un fenomeno "gia' osservato presso banche europee", che per
    la rubrica e' 5, e "non 5: non in corso presso la Banca" a una Prossimita
    con un tentativo fermato presso la Banca, che e' "imminente": corretti
    rileggendo ogni valore contro il descrittore. I fatti dell'esempio sono
    dichiarati inventati ("Documento A/B/C") perche' A1 non li citi come fonti.
    Le istruzioni senza spazio (A1 a 7.963 caratteri) si allungano con
    l'allegato, non con il prompt.
80. **Un'azione aperta non si ripropone** (02/10, D-69): nei dati di prova A1
    riproponeva ogni trimestre le stesse azioni approvate (nella scheda di
    NFR-11 tre volte "Piano di sostituzione..."), e ogni copia diventava una riga
    nuova in Azioni e una riga in piu' da validare. La guida chiede il passo
    successivo e C8 segnala come Osservazione la stessa descrizione di
    un'azione aperta dello stesso rischio. Cambiare i dati di prova vuol dire
    cambiare anche la baseline attesa dopo il primo ciclo
    (`baseline_2026Q4.json`, le azioni 2026Q3-...-A1), che la catena confronta
    al carattere con quella estratta dal registro.
81. **In Copilot Studio il motore decide che cosa si puo' fare e quanto costa**
    (05/10, D-70). Da settembre 2026 ci sono l'esperienza standard e la nuova
    esperienza (GitHub Copilot harness), e un agente non passa dall'una
    all'altra.
    - Standard: il Code interpreter va abilitato dall'amministratore (spento di
      default) e il codice lo scrive il modello; per gli utenti Microsoft 365
      Copilot e' "No charge".
    - Nuova esperienza: le skill eseguono un nostro script sempre uguale, ma i
      Copilot Credits si consumano dalla costruzione, anche nel riquadro di
      prova.

    La conclusione del 28/09 ("il code interpreter non puo' fare da gate")
    resta vera per il code interpreter, non per le skill. Prima di scrivere
    passi per Copilot Studio: ricontrollare Learn, poi chiedere all'IT
    ambiente, abilitazione del code interpreter, crediti e modelli.
82. **Il codice che gira altrove deve essere lo stesso codice** (05/10, D-70).
    Lo script della skill non si scrive a mano: `prepara_kit.py` lo compone dai
    moduli del pacchetto, copiati in stringhe grezze a tre apici ed eseguiti in
    memoria all'avvio. Il generatore rifiuta un sorgente con `'''` o che finisce
    con una barra rovesciata, normalizza gli a capo e verifica che lo script
    contenga esattamente i sorgenti. Una data fissa negli zip fa si' che a
    sorgenti uguali corrispondano byte uguali. Il collaudo lo lancia come
    processo a parte e confronta prima riga, impronta e messaggio con il
    comando. Le regole del precontrollo sono state spostate in un modulo senza
    Excel proprio per questo: dentro `esegui_ciclo_locale.py` avrebbero
    trascinato COM e configurazione.
83. **L'esito riferito da un agente si verifica, non si crede** (05/10, D-70).
    Un agente puo':
    - saltare lo script, o eseguirlo su un'altra versione del JSON;
    - riscriverlo;
    - riferire un esito che lo script non ha stampato.

    Per questo il precontrollo stampa l'impronta dell'output. Si calcola sul
    JSON canonico (chiavi ordinate, senza spazi): un file salvato dalla chat e
    lo stesso contenuto riformattato hanno la stessa impronta. L'impronta
    dell'agente si confronta con quella del PC sul file consegnato. Il gate
    resta comunque `trimestrale`.
84. **Una prova di ciclo non si fa sul registro vero, e non su un ciclo futuro**
    (05/10). Sul registro della Banca il prossimo ciclo e' il 2027Q1, ma oggi C3
    fermerebbe ogni variazione: l'evidenza deve essere datata dopo la data di
    riferimento del ciclo prima, il 31/12/2026.
    - La prova si fa su un registro nuovo (`inizializza`, primo ciclo 2026Q4),
      in una cartella a parte con il suo `configurazione.json`. I comandi
      restano quelli della guida; si controlla che ogni percorso stampato sia
      quello di prova.
    - Negli allegati della nuova esperienza i `.py` e i `.json` non passano: lo
      script viaggia come `.txt` (Python lo esegue lo stesso) e l'allegato di A1
      e' gia' `.txt`.

85. **Un controllo che ferma deve proteggere il registro, non il metodo**
    (06/10, D-71). Fino al 05/10 C3, le date di C5 e le soglie di C9 fermavano
    la scrittura come un rischio mancante: ogni rilievo di metodo costava un giro
    A1 -> A5 -> `trimestrale` (7-8 il 29/09). Ferma solo cio' che renderebbe
    incoerente il registro (C1, C2, C7, identificativi dei KRI); il resto e'
    "Da motivare" e arriva al validatore con il testo accanto alla riga. Ma una
    regola che la rubrica dichiara assoluta (un punto per ciclo, soglie
    ordinate) non si puo' "motivare": `valida` la applica anche alla proposta
    accettata cosi' com'e', altrimenti l'ammorbidimento la cancellerebbe.
86. **Una formula che conta i separatori dipende dal formato del testo**
    (06/10). La colonna Rilievi del Registro contava le segnalazioni come
    numero di "[" nel testo del RiskRegister; il formato nuovo
    (`⚑ DA MOTIVARE · C3 · controlli: ...`) non ha parentesi e avrebbe
    contato zero. Si contano le righe (CHAR(10)), che valgono per il formato
    vecchio e per il nuovo, e si cerca sia DA MOTIVARE sia BLOCCANTE SUPERATO:
    un registro migrato porta con se' testi del formato di prima.
87. **Un agente che spiega deve dire da dove viene ogni frase** (07/10, D-72).
    Una spiegazione plausibile e' facile da scrivere anche senza il motivo vero:
    A7 deve separare REGISTRATO (motivazioni di A1, decisioni del validatore),
    CALCOLATO (score, urgenza, livello rifatti con i numeri) e LETTURA MIA. Per
    "perche' questo tema non e' un rischio" serve un motivo registrato nel ciclo:
    per questo A1 scrive `fenomeni_non_censiti`; senza, ogni risposta sarebbe una
    ricostruzione.
88. **La knowledge di Agent Builder si scrive a file piccoli e con nomi fissi**
    (07/10). Un file aggiornato si reindicizza subito, uno nuovo puo' aspettare
    l'indicizzazione giornaliera; un file unico di decine di KB viene letto a
    pezzi. Quindi un `.txt` per **posto dell'anagrafica** (`Rischio_01..20.txt`,
    con il codice del rischio in testa; i posti liberi lo dicono) piu' `Ciclo.txt`:
    un rischio appena censito entra in un file che esiste gia'. Sempre con lo stesso
    nome, scritti dallo script (nessuna copia a mano), e i file dei rischi che non
    ci sono piu' tolti. Quando il kernel e' la `01_Kernel` del pacchetto
    (collaudo, demo) la cartella va in quella di uscita: lo script non deve mai
    scrivere nel pacchetto.

89. **La scala di una pagina si misura sull'interruzione manuale, e la ricalcola
    ogni comando che cambia cio' che si stampa** (07/10). Con la riga delle Note
    il Quadro e' diventato piu' alto: `scala_quadro` prendeva la prima
    interruzione di pagina, che poteva essere una automatica di Excel (dipende
    dalla scala attuale), e `settimanale` non chiamava `prepara_report` anche se
    le notizie cambiano livelli e rischi segnalati. Ora: solo interruzioni
    manuali (`Type == -4135`), `prepara_report` anche in `settimanale`, scala di
    partenza del template al 74%.

90. **Una lista che l'agente aggiorna "solo con evidenza nuova" la completa lo
    script** (07/10, D-73). A1 scrive solo le voci nuove o cambiate per non
    allungare la risposta; se il registro tenesse solo quelle, le viste filtrate
    sul ciclo corrente e la baseline perderebbero le voci non toccate. Quindi
    `voci_osservazione` riporta nel ciclo nuovo ogni voce "In osservazione" del
    ciclo prima (Esito Invariata, non da rivalidare): ogni ciclo ha la lista
    intera. Una voce respinta o promossa non si riporta; una voce esistente
    respinta in validazione torna ai valori del ciclo prima.
91. **Un controllo nuovo va dove c'e' spazio, senza codici nuovi** (07/10, D-73).
    Il prompt di A5 e' a 7.962 caratteri e include `controlli_A5.md`: le regole
    della lista stanno nella guida di scrittura dell'allegato di A1 e i controlli
    solo nello script, con i codici esistenti (C1 per codici e promozioni, C5 per
    le date). Un "C10" romperebbe l'elenco C1-C9 controllato in cinque documenti
    e lo schema di A5, con cui il collaudo valida anche l'esito dei controlli; un
    controllo con codice C4 romperebbe la regola "C4 solo ad A5".
92. **Un elenco ordinato con AGGREGATE vuole chiavi uniche** (07/10). La vista
    trova la k-esima voce con `MATCH(AGGREGATE(14,6,chiave,k),chiave,0)`: due voci
    con la stessa chiave (stesso impatto e orizzonte) darebbero due volte la
    prima. La colonna Ordine aggiunge `1-ROW()/1000000` (unica, a parita' prima la
    riga scritta prima) e vale "" fuori dal ciclo corrente o fuori osservazione,
    che AGGREGATE ignora.

93. **I periodi si confrontano come testo, e li scrive lo script** (07/10, D-75).
    `2026Q4` < `2026Q4-S1` < `2026Q4-S2` < `2027Q1` in ordine alfabetico: basta
    `sorted()` per la sequenza. Le formule di Parametri che ricavavano il ciclo
    precedente con `LEFT`/`RIGHT` sui trimestri non reggono uno straordinario: il
    precedente, il trend e la data di riferimento li scrive `imposta_ciclo` ogni
    volta che cambia il ciclo corrente (trimestrale, inizializza,
    aggiorna-registro). Un rischio non rivalutato nello straordinario si riporta
    con `Periodo_Valutazione` d'origine, e la Y di Mosca prende le azioni di quel
    periodo: senza, il margine dei rischi non toccati cambierebbe da solo.
94. **Una funzione nuova che legge il registro deve reggere i registri vecchi**
    (07/10). `aggiorna-registro` estrae la baseline dal registro vecchio con le
    stesse funzioni: `periodi_registro` leggeva `tblSintesi`, che un registro del
    23/09 non ha, e la migrazione si fermava con KeyError. Le letture passano da
    `_righe_o_niente`.
95. **Nove etichette equidistanti cadono sempre vicino a un angolo** (07/10, D-74).
    Con passi di 40 gradi, qualunque rotazione lascia un'etichetta a meno di 5
    gradi da una diagonale: le legende negli angoli del radar si sovrappongono. Si
    mettono sotto il radar, allungando il grafico in proporzione (cerchi rotondi);
    nel radar piccolo del Quadro la legenda si toglie, perche' allungarlo lo
    portava oltre il salto di pagina (verificato con la posizione del grafico).
96. **Un prompt al limite si accorcia prima di aggiungere** (07/10). A3 era a 7.702
    caratteri e la proposta di ciclo straordinario lo portava a 8.338: si e'
    riscritto il testo senza togliere regole (7.899-7.914). La regola del segnale
    critico sta nella sezione 6 della rubrica, che entra sia in A3 sia in A4: una
    regola, due agenti.
97. **Cambiare tassonomia senza cambiare i nomi interni** (07/10, D-74). I valori
    passano da `L1-0n` a `9.n`, ma campo `event_type`, colonna `Event_Type` e nome
    `codiciL1` restano: rinominarli toccava decine di formule, la mappa, gli schemi
    e i dati di collaudo senza dare niente a chi usa il registro (le etichette
    visibili dicono "Categoria"). La riclassificazione di un codice di Basilea e'
    un'Osservazione, non un fermo; `FP` resta fuori dal radar finche' non si
    dismette; fino alla riclassificazione il radar di un registro aggiornato e'
    vuoto, e `aggiorna-registro` lo dice.
98. **Un passo si descrive una volta sola** (07/10). Guida e piano di deploy
    descrivevano le stesse installazioni con due liste da allineare a mano; il
    piano era gia' rimasto indietro ("5 agenti", collaudo "15 minuti"). Ora la
    guida ha l'avvio del progetto (decisioni, collaudo sul primo ciclo, cancelli)
    e rimanda alla sezione 0 per ogni passo tecnico.
99. **Un valore atteso su una finestra mobile si ricalcola sulla stessa finestra**
    (07/10). Il collaudo confrontava l'intensita' di una categoria del foglio
    Notizie dopo la validazione con quella di prima della settimana; ma la finestra
    di 4 settimane finisce con la settimana corrente, che la scrittura di A3 sposta:
    notizie vecchie escono e il "prima" non e' piu' un riferimento. L'atteso si
    calcola dal NewsLog con le stesse date del foglio (`massimo_finestra` in
    `run_catena.py`). Stesso giorno: un payload di prova costruito da un registro
    vecchio deve fare cio' che farebbe A1, cioe' riclassificare i codici di
    Basilea (D-74), non ricopiarli.
100. **Prima di un meccanismo nuovo, chiedersi se uno esistente basta** (07/10,
    D-76). Per le modifiche fra un ciclo e l'altro era pronto un foglio
    Manutenzione con il suo comando e un modo manutenzione di A7 (circa 600
    righe fra script e mappa); l'utente ha proposto di riusare la validazione,
    rieseguibile quante volte serve. La riapertura copre quasi tutto con circa
    150 righe, nessuna struttura nuova e un solo gesto gia' noto. Nel riuso
    attenzione a cio' che la validazione dava per scontato: "proposta" =
    valore validato, "accettata" = non toccare il dato (altrimenti Validazione
    e Stato delle azioni tornano a "Accettato"/"Approvata"), limite di un
    punto, ⚑ obbligatorio, decisioni nello storico da distinguere da quelle
    sulle proposte degli agenti. Stesso giorno: nello straordinario la
    Data_Rilevazione di un KRI riportato tornava da COM come testo ISO e veniva
    riscritta come testo: le date copiate da una riga letta vanno riconvertite
    con `a_data`.
101. **Un agente nuovo non e' per forza un formato nuovo** (07/10, D-77). Il piano
    prevedeva per A8 un comando `straordinario --payload A8.json`; scrivendo A8
    nello schema di A1 (con un solo campo facoltativo in piu') valgono gia'
    allegato, precontrollo, controlli, scrittura e validazione. Il prompt di un
    agente "come A1 ma diverso" sfora subito gli 8.000 caratteri (prima stesura
    8.284): le istruzioni di dettaglio vanno nella guida di scrittura
    dell'allegato, nel prompt solo procedura e scheletro. Un campo nuovo dello
    schema va anche in `mappatura_campi.json` (`non_nel_workbook`, altrimenti
    `test_mappatura` e' KO), nel kit di Copilot Studio (`prepara_kit.py`) e nei dati
    di prova: un controllo nuovo puo' far fallire un test vecchio che chiedeva
    "nessun rilievo" (ora "nessun Bloccante").
102. **Il parallelo accorcia solo cio' che e' indipendente** (08/10, M1). Dividere la catena in dieci gruppi e
    lanciarli in tre processi, un Excel ciascuno, porta il collaudo da circa 50 a 40 minuti, non a 20-25 come
    stimato: il gruppo `catena` (passi 0-5, 7, 8s, 8a) e' una sequenza di stati e da solo dura quasi tutto. Per
    scendere ancora servono meno aperture di Excel dentro quel gruppo (`leggi()` apre e ricalcola a ogni
    chiamata). Altre due cose:
    - uno stato del PC (le impronte di `--mirato`) va fuori dal pacchetto, altrimenti finisce nello zip e
      l'indice del 00_LEGGIMI lo segnala;
    - spostare una cartella di documenti e' una sostituzione di testo; spostare una cartella di codice installata
      in Banca e' una reinstallazione: si fa con l'installatore (AU3).

103. **Un rischio nuovo non "entra" nel radar** (08/10, D-79). Movimento confronta lo stato con il ciclo prima:
    Entrato solo per chi era in osservazione, Uscito solo per chi era nel radar. Un rischio nuovo che va subito nel
    radar e' Nuovo, senza Movimento (lo dice anche il riepilogo di `valida`, che elenca chi entra nell'anagrafica):
    un test che si aspetta "Entrato" per un rischio nato nel ciclo sbaglia. Per provare l'ingresso dall'osservazione
    serve un rischio che c'era gia' (nei dati di esempio NFR-13 e NFR-14 dal 2026Q1).
104. **Un rischio fuori dal radar sta ancora nel registro** (08/10, D-79). Ogni vista o verifica che contava le
    righe del ciclo nel RiskRegister ora conta anche quelle in osservazione: il report e il Radar_Mosca leggono
    l'anagrafica (= il radar), le liste e lo score tutte le righe. Nel collaudo `verifica_report` e
    `mosca_attesa` filtrano sull'anagrafica; nel foglio Notizie una categoria senza rischi del radar ma con uno in
    osservazione e' "In osservazione", non "AREA NON PRESIDIATA". Nell'aggiornamento di un registro la baseline
    di prima e di dopo si confronta senza `regola_radar`: pesi e soglie sono del template nuovo.
105. **ROUND di Excel non e' Decimal(repr(x))** (08/10). Lo score 1,7/0,8 = 2,125 in Python e' 2,12499999...: un
    arrotondamento a meta' in su sul repr da' 2,12, Excel (15 cifre significative) da' 2,13. Il calcolo
    indipendente del collaudo arrotonda prima a 10 decimali. Il caso e' nato con un rischio in osservazione dei dati
    di esempio (Impatto 3, Probabilita 1, Prossimita 2, Velocity non valutata).

106. **Chi non ha uno stato non esce dal radar** (08/10, D-79, trovata dal gate di copertura). La scrittura
    toglieva dall'anagrafica ogni rischio "non nel radar", compreso uno del radar che A1 aveva dimenticato: il
    rischio spariva in silenzio e il ciclo risultava completo (11 su 11). Escono solo i rischi a cui la regola ha
    dato uno stato fuori dal radar (`fuori`); uno assente resta in anagrafica e il controllo di copertura ferma il
    ciclo (C1 lo ferma gia' prima: il gate e' la seconda difesa). Ogni insieme calcolato per complemento ("tutti
    tranne quelli dentro") va riletto cosi'.

107. **Una vista giusta puo' essere invisibile** (08/10, demo D-79). La sezione "Entrati e usciti dal radar" della
    pagina Fenomeni aveva il dato giusto (NFR-16, Entrato) ma righe alte 3 punti, come nel template, e nel PDF non si
    vedeva niente; il collaudo leggeva il valore delle celle e passava. Ogni intervallo con testi calcolati che il
    template crea basso va passato da `adatta_altezze` in `prepara_report` (ora anche `fenomeniUscite`); il controllo
    vero e' guardare il foglio esportato.

108. **Il riquadro di prova di Copilot Studio non e' Teams** (09/10, prova K0, D-70). Nel riquadro di prova A1 con il
    code interpreter funzionava; pubblicato in Teams rispondeva spesso con errori. Il flusso di salvataggio funzionava
    lanciato da solo, ma dall'agente in Teams il file finiva nel OneDrive personale (risolto dall'utente lo stesso giorno; poi impronta uguale: il JSON passa intero per il flusso). Teams ha limiti suoi:
    - messaggi fino a circa 100 KB contati in UTF-16, quindi un JSON di A1 di 40-60 KB nel messaggio non passa;
    - consenso alle connessioni;
    - solo la versione pubblicata;
    - file della chat conservati nel OneDrive di chi chatta.

    La causa del OneDrive era il protocollo: in Create file vanno scelte le variabili del flusso, cioe' gli
    input del trigger, non nomi scritti come testo. Inoltre la descrizione dello strumento deve limitarlo a
    un comando esplicito (`Scrivi_JSON`): l'orchestrazione generativa chiama uno strumento ogni volta che la
    descrizione sembra adatta, quindi un'azione che scrive va legata a un comando e provata anche al
    negativo. Ogni passo per Copilot Studio va provato nel canale vero. In un protocollo si chiedono il codice dell'errore, la
    cronologia delle esecuzioni del flusso e la scheda Activity, non solo "funziona / non funziona". Nella prova in
    Banca l'opzione 2, cioe' la nuova esperienza, non c'e'.

109. **Una prova che legge il kernel vero ci puo' anche scrivere** (09/10, trovata scrivendo le prove della CS-1).
    La prova senza Copilot Studio faceva copiare nella configurazione di `C:\NFR_Prova` la riga `kernel` di quella
    vera, "la prova legge la stessa library Kernel e non ci scrive niente". Dal 07/10 (D-72) pero' `trimestrale`,
    `valida` e `dismetti` scrivono `Kernel\Spiegazioni`, la knowledge di A7: la prova avrebbe sostituito le
    spiegazioni del registro vero con quelle del registro di prova. Ora la configurazione di prova e' senza
    `kernel`: si usa `01_Kernel` del pacchetto e le spiegazioni vanno nella cartella di uscita
    (`cartella_spiegazioni`). Ogni volta che un comando comincia a scrivere in una cartella nuova, vanno riletti i
    protocolli di prova che puntano a quella cartella.

110. **Nel cloud il problema non sono le librerie, ma chi esegue il codice** (11/10, analisi 15). Quasi tutte le regole
    del pacchetto sono gia' libreria standard e girano nel sandbox di Copilot Studio. In Copilot Studio pero' gira
    codice nostro solo in due modi:
    - il code interpreter, perche' il modello decide di eseguirlo;
    - gli Office Scripts, deterministici, dentro Excel.

    Ne seguono tre regole:
    - prima di scegliere una libreria va chiarito chi esegue il codice e che cosa succede se non lo fa;
    - un esito prodotto da un modello si accetta solo se porta l'impronta del motore vero, che il flusso confronta con
      quella attesa: a prova di guasto, senza esito verificato non si scrive;
    - il registro lo scrive solo codice deterministico dentro Excel, che ricalcola e cerca gli errori. Un `.xlsx`
      riscritto fuori da Excel ha i valori delle formule vecchi.

    Limiti che hanno deciso il disegno:
    - i prompt accettano un solo file Office in ingresso e restituiscono un solo file;
    - i prompt hanno 100 secondi;
    - i flussi estraggono uno zip ma non lo creano;
    - il connettore Excel Online puo' bloccare il file per 6 minuti;
    - gli Office Scripts lanciati da un flusso non aggiornano Power Query.

    Nella variante V4 (analisi 16) il file dei dati non ha formule: la terza regola non si applica, perche' manca la
    premessa (niente da ricalcolare); le prime due restano.

111. **`round()` di Python non e' `ROUND` di Excel** (14/10, anteprima dell'analisi 16). Python arrotonda la meta' al
    pari e lavora in binario: `round(1.25, 1)` da' 1,2, Excel da' 1,3. Ricalcolando in Python le viste del registro
    della demo, "Margine 1,3 anni" di NFR-09 diventava "Margine 1,2 anni": l'unico valore diverso su 118. Ogni formula di
    Excel riscritta in Python (viste della V4, adattatore della V2, testi con `FIXED`) arrotonda con
    `Decimal(str(x)).quantize(..., ROUND_HALF_UP)`, e il collaudo confronta i testi, non solo i numeri.
112. **Mosca non vede un rischio lontano di cui nessuno stima la mitigazione** (19/10, analisi 17, 17.10). La regola
    del radar vuole Prossimita almeno 2, ma un rischio AGIRE ORA entra comunque: per un rischio in osservazione il
    margine usa gli anni di adeguamento della sua riga, e senza quelli la Y di riserva (1 anno). NFR-13 della demo
    (crittografia post-quantistica, Impatto 5, Prossimita 1) aveva margine 2,25 e restava fuori: proprio il caso per
    cui Mosca ha scritto la disuguaglianza. La guida di A1 chiede gli anni anche per i rischi in osservazione con
    Impatto 4-5 (D-80); il comando `diagnosi` segnala chi non li ha. Non mettere gli anni di adeguamento solo
    nell'anagrafica: per i rischi in osservazione vivono nella riga del RiskRegister.

(Le trappole 113-121 e 130 sono sul ramo `copilot-studio-pieno`, versione tutta in Copilot Studio, D-82: arrivano qui
solo se l'utente decide di unire il ramo. Regola dei numeri: una trappola nuova prende il primo numero libero dopo
l'ultimo usato in tutti e due i rami.)

122. **Con piu' analisti il lucchetto da solo non basta** (23/10, D-83). OneDrive porta il file del lucchetto sugli
    altri PC con secondi o minuti di ritardo: due analisti possono prenderlo insieme, e un collega puo' salvare il
    registro da Excel per il web senza passare dallo script. La garanzia e' la copia di lavoro con l'impronta: il
    registro vero si sostituisce solo se e' ancora quello copiato all'inizio. Il lucchetto resta come avviso cortese,
    con la copia in conflitto di OneDrive (`registro-PCNOME.json`) letta come un collega; la presa in due tempi c'e' ma
    con attesa 0 di default: l'avviso serve a non cominciare un lavoro che si fermerebbe, non a proteggere i dati.
123. **Mai sostituire un file aperto da Excel, e mai attraverso volumi diversi** (23/10). La copia di lavoro sta in
    `%LOCALAPPDATA%`: la sostituzione si fa solo dopo aver chiuso la sessione di Excel (il file della copia e' bloccato
    finche' e' aperto), copiando prima accanto all'originale e poi con `os.replace` (atomico solo nella stessa
    cartella). Il nome temporaneo comincia con `~$`, che OneDrive non sincronizza. Un registro aperto in Excel sul PC
    si scopre prima con `open(r+b)`: dopo, l'errore arriverebbe a lavoro fatto.
124. **`SALVATO` vuol dire "registro sostituito", non "copia salvata"** (23/10). Con la copia di lavoro un errore
    dopo `_salva_con_backup` ma prima della sostituzione lascia il registro com'era: il messaggio deve dire "non
    salvato". `SALVATO["registro"]` si imposta solo in `_sostituisci`; la knowledge di A7 scritta dentro la sessione si
    riallinea al comando dopo, se la sostituzione non riesce.
125. **Il report rigenerato da `valida` aggiunge una versione** (23/10). Il collaudo che contava le versioni
    precedenti del PDF dopo due `report` deve contarne una in piu'; nella riapertura si prova anche `--senza-report`.
    Il report si esporta dalla sessione di `valida` gia' ricalcolata, prima di chiuderla (riaprire Excel costerebbe un
    minuto a ogni validazione), ma in una cartella temporanea: entra nell'archivio solo dopo la sostituzione del
    registro, altrimenti un fermo "registro cambiato" lascerebbe un report di dati mai salvati.
126. **Un prompt schedulato non porta allegati** (23/10, AU7). Dal momento in cui A3 legge la baseline solo
    dall'allegato `Input_A3_A4.txt`, il prompt schedulato del lunedi' risponde "Baseline mancante": A3 si lancia a mano
    (o dall'app). Togliere `Baseline_corrente.txt` dalla knowledge di A3 e A4 e dalla library Kernel, altrimenti un
    agente potrebbe ancora leggerne una vecchia.
127. **tkinter si tocca solo dal suo thread** (23/10, app). Il motore impiega minuti: i processi girano in un thread,
    e ogni richiesta alla finestra (messaggio, domanda, modulo, attesa della risposta) passa da una coda svuotata con
    `after` nel thread principale, con un Event per il risultato. Chiamare un widget dal thread del processo blocca o
    chiude la finestra senza errori leggibili.
128. **Senza `SetProcessDpiAwareness(1)` la finestra e' sfocata e le coordinate sono sbagliate** (23/10). Con la
    scala di Windows al 125-150% tkinter disegna a 96 dpi e Windows ingrandisce l'immagine; anche una cattura dello
    schermo prende il rettangolo sbagliato. La finestra si dimensiona in proporzione allo schermo, non in pixel fissi;
    su 1920x1080 con la scala al 150% una finestra al 82% dell'altezza lasciava due righe all'uscita del motore: fino
    a 1200 pixel di altezza si apre ingrandita. Provarla simulando lo schermo (geometria e `tk scaling`), non solo sul
    monitor di chi sviluppa.
129. **Una risposta tagliata contiene oggetti JSON interi** (23/10). Dentro un A1 interrotto a meta' ci sono rischi
    completi: "c'e' un oggetto JSON" non basta a dire che la risposta e' intera. Si cerca prima l'oggetto di un agente
    (campi obbligatori dello schema); solo se manca e le graffe dalla prima `{` non si chiudono la risposta e'
    TRONCATA. Un segnaposto nei link degli agenti non si apre (solo link che cominciano con http).

131. **La posta blocca gli zip con file eseguibili** (23/10). Gmail ha rifiutato lo zip del pacchetto per `07_Senza_Studio/NFR.cmd`:
    gli allegati con .cmd, .bat, .ps1, .vbs, .js, .exe (anche dentro uno zip) non passano. Per la posta si consegna
    `<nome>_posta.zip`: lo stesso contenuto di git archive, con quei file rinominati `.txt` in coda, e in
    `AGGIORNAMENTO_IN_BANCA.md` il passo per rinominarli dopo l'estrazione. Prima di consegnare si controllano anche
    gli zip annidati del kit.

## STRUTTURA DEI FILE DA PRODURRE

```
00_LEGGIMI.md  00_GUIDA_PASSO_PASSO.md  TODO_possibili_sviluppi.md
01_Kernel/  tassonomia_nfr.md  fonti.md  rubrica_scoring.md  schema_output_A1.json
            schema_output_A3.json  schema_output_A5.json  schema_output_A6.json
            schema_output_A1_DOCUMENTATO.md  controlli_A5.md  guida_scrittura_A1.md
            mappatura_campi.json
02_Agenti/  A1_Horizon_Scanner.md  A3_Interim_Update.md  A4_News_Assessor.md  A5_Challenger.md
            A6_Schede.md  A7_Assistente_registro.md  A8_Evento_critico.md (generati)  componi_prompt.py
            modelli/A1.md A3.md A4.md A5.md A6.md A7.md A8.md
            COMMENTATI/A1_Horizon_Scanner_DOCUMENTATO.md  COMMENTATI/A3_A4_A5_DOCUMENTATO.md
03_Excel/   genera_dashboard.py  NFR_Dashboard_Template.xlsx  costruzione_manuale_template.md
04_Riferimenti/  DECISIONI.md (registro delle decisioni della Banca: si conserva, non si rigenera)
                struttura_e_liste.md  workflow.md  controlli_e_model_risk.md
                Prove/ Prova_senza_Copilot_Studio.md (installazione e ciclo su un registro di prova)
                       Prova_A7.md (copione di prova di A7)
07_Senza_Studio/  README_variante_locale.md  esegui_ciclo_locale.py  raccogli_notizie.py  fonti.py
                  excel_com.py  controlli_a5.py  valida_output.py  schede.py  input_a1.py
                  precontrollo.py  radar.py  spiegazioni.py  diagnosi.py  lucchetto.py  configurazione_esempio.json
                  NFR.cmd  app_nfr.py  flussi.py  stato.py  ingresso.py  appunti.py  esecutore.py
09_Copilot_Studio/  Prova_con_Copilot_Studio.md  Prova_K6_Operatore.md  Prove_CS1.md  prepara_kit.py  precontrollo-nfr/SKILL.md
                    precontrollo-nfr/scripts/precontrollo_nfr.py (generato)
                    Da_caricare/ precontrollo-nfr.zip  precontrollo-nfr_senza_cartella.zip
                                 precontrollo_nfr.txt (generati)  Messaggi_da_incollare.txt
99_Collaudo/  LEGGIMI_collaudo.md  esegui_collaudo.py  comune.py  test_mappatura.py  test_controlli.py
              test_fonti.py  test_app.py  verifica_riferimenti.py  run_catena.py  confronta.py  osserva_cartella.py
              dati/ baseline_2026Q3.json  run1_A1_2026Q3.json  run2_A1_2026Q3.json  run_A5_2026Q3.json
                    run_A3_2026-10-12.json  baseline_2026Q4.json  run3_A1_2026Q4.json  run_A5_2026Q4.json
                    decisioni_validatore_2026Q3.json  decisioni_validatore_2026-10-12.json
                    registro_template_2026-09-23.xlsx  baseline_registro_template_2026-09-23.json
                    (registro di un template precedente, per il passo 11: si conserva, non si rigenera)
```
Fuori dal pacchetto: `Demo_W1_W2/`, `HANDOFF_stato_e_prossimi_passi.md`,
`Analisi_Architettura/` (analisi e anteprime), lo zip del pacchetto con la data.

## ORDINE DI LAVORO

1. Verifica i vincoli della piattaforma (ricerca, con date).
2. Kernel: tassonomia, rubrica (sezioni numerate, descrittori brevi).
3. Schemi e SUBITO il validatore generico, provato su un payload finto.
4. Mappa campi come dato; controllala in entrambe le direzioni prima dei prompt.
5. Modelli dei prompt e `componi_prompt.py`; misura il limite.
6. Generatore del workbook e template; apertura e ricalcolo in Excel: zero
   errori; esporta in PDF i fogli del report e **guarda** pagine e grafici.
7. Script di campo (COM), controlli di A5, precontrollo (`precontrollo.py`) e
   schede (`schede.py`); poi `fonti.md` provando i feed dal vivo, `fonti.py`,
   `raccogli_notizie.py`; poi il kit di Copilot Studio (`prepara_kit.py`, dopo
   il precontrollo, perche' ne copia i moduli).
8. Dati di prova generati con lo strumento vero; suite di collaudo; catena con
   Excel; prove di mutazione.
9. Correggi ogni incoerenza NEL FILE GIUSTO (fonte unica), non a valle.
10. SharePoint, workflow, governance, README, _DOCUMENTATO, guida passo passo,
    TODO, 00_LEGGIMI.
11. Demo con report; verifica finale della suite completa; HANDOFF con
    stato, scostamenti, trappole, decisioni aperte della Banca.

Procedi. Fermati e chiedi solo per decisioni che spettano alla funzione di
rischio della Banca o se l'ambiente Microsoft e' diverso da quanto dichiarato.
