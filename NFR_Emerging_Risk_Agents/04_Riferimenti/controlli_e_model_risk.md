# Governance — controlli, evidenze, model risk

## 1. Qualificazione model-risk (da decidere PRIMA del deploy)

Il sistema produce valutazioni che un comitato usa per decidere priorita' e
azioni. La funzione di rischio e la funzione di convalida devono decidere, prima
del primo ciclo reale, se l'output e' un **modello** ai fini della policy di
model risk della Banca. Retrofittare i requisiti su un sistema in esercizio
costa molto piu' che partire qualificati.

**Esito (24/09/2026, `04_Riferimenti/DECISIONI.md` D-23)**: non rilevante secondo la
policy; approvato, senza requisiti di convalida ulteriori. Parere di
compliance/DPO positivo (D-24). Si rivaluta se cambia l'uso: per esempio se il
registro, da affiancamento (D-14), diventa l'input del processo ufficiale.

Elementi per la decisione:
- Il giudizio (quattro dimensioni, di cui la Velocity facoltativa, e la
  gli anni di adeguamento, con la rilevanza di ogni fonte) e' prodotto da un LLM
  ancorato a una rubrica; il calcolo (score composito, segnali netti, stato KRI, urgenza) e'
  deterministico e verificabile nel foglio.
- Il sistema non produce cifre di perdita ne' probabilita'.
- Cio' che richiede conoscenza interna non lo stima l'agente (30/09/2026,
  D-49...D-56): il presidio dei controlli e le soglie dei KRI li mette la
  Banca; esito e "da/a" delle variazioni li calcola lo script.
- Ogni ciclo e' approvato da una persona (`Approvato_Da`); nessuna
  auto-approvazione.
- La riproducibilita' si misura con un doppio run (04_Riferimenti/workflow.md, "Test in
  ambiente"); il collaudo a secco la misura solo sugli artefatti.
- Non esiste un trimestre gia' valutato a mano con cui confrontare l'agente:
  il registro parte vuoto. Il primo ciclo si accetta con criteri fissati prima
  in `DECISIONI.md`: riproducibilita' del doppio run (`confronta.py
  --primo-ciclo`), lettura dell'analisi da parte della funzione di rischio,
  quota di rettifiche del validatore (guida, Avvio del progetto, fasi 0.8 e 7).

## 2. Controlli incorporati

Ogni controllo di giudizio ha, dove il vincolo e' esprimibile, una controparte
deterministica. La colonna "Dove" indica il file che lo implementa.

Il testo dei nove controlli C1-C9 sta in un solo file, `01_Kernel/controlli_A5.md`
(D-69): da li' si compongono le istruzioni di A5 e l'allegato di A1
(`Input_A1_<ciclo>.txt`), cosi' A1 conosce le regole con cui sara' controllato
e le applica prima di rispondere. Questa autoverifica non e' un controllo: un
modello che rilegge il proprio output tende a confermarlo. I controlli restano
la controparte deterministica, che `trimestrale` applica prima di scrivere (e il
comando `precontrollo` prima, se lo si usa), e A5, **facoltativo dal 06/10/2026**
(D-71; indipendente: non vede la knowledge ne' la chat di A1). Dal D-71 lo
script ferma solo i difetti di integrita' (schema, C1, C2, C7, identificativi
dei KRI); C3, le date di C5, la coppia e le soglie dei KRI e i Bloccanti di A5
sono **da motivare**: colonna Segnalazioni del foglio Validazione, Motivazione
obbligatoria; `valida` non accetta un salto di piu' di un punto ne' soglie
invertite.

| Controllo | Cosa verifica | Giudizio (agente) | Controparte deterministica | Dove |
|---|---|---|---|---|
| Schema | campi, tipi, pattern, interi 1-5 (Velocity anche null), due KRI con il tipo (Esposizione, Evoluzione), soglie numero o null, nessun campo in piu' (anche gap_controlli, esito, da/a, dimensione delle azioni) | — | validatore generico sullo schema | `07_Senza_Studio/valida_output.py` + `01_Kernel/schema_output_A1.json` |
| Esito e "da/a" | calcolati, non dichiarati (D-51) | — | lo script li ricava dalla baseline dopo i controlli; Variato = cambia Impatto, Probabilita, Prossimita o Velocity; ricalcolati dopo la validazione | `esegui_ciclo_locale.py` (`completa_payload`), `test_controlli.py`, `run_catena.py` |
| C1 Completezza | ogni rischio in anagrafica valutato, con la stessa categoria (D-74: un codice di Basilea riclassificato = Osservazione; FP = da motivare); id unici | A5 | per intero | `controlli_a5.py` |
| C2 Variazioni | una variazione per ogni valore cambiato e solo per quelli (anche una Velocity che diventa non valutata) | A5 | per intero | `controlli_a5.py` |
| C3 Evidenza | evidenza datata nella finestra del ciclo, non generica; max un punto | A5 | date, frasi generiche, max un punto | `controlli_a5.py` |
| C4 Plausibilita' | score coerenti con i descrittori; un rischio = un meccanismo di perdita (D-55); Velocity solo con i tempi documentati (D-50); simmetria aumenti/riduzioni; numeri del razionale con la fonte o dichiarati come valutazione (D-36) | A5 | **nessuna**: solo giudizio | `02_Agenti/A5_Challenger.md` |
| C5 Fonti | rilevanza 1-3 coerente con i descrittori; Probabilita 5 o Prossimita 4-5 con una fonte di rilevanza 3 (salvo deroga dichiarata); fonti non future; fonti perse con valori invariati (D-58); esposizione della Banca non nota alle fonti (D-81) | A5 | date per intero (Bloccante); rilevanza alta e fonti perse come Osservazioni; la frase "ESPOSIZIONE NON NOTA" del razionale porta la Probabilita proposta e quella "se esposta" in validazione (Da motivare) | `controlli_a5.py` |
| C6 Deriva | aumenti solo su fonti esterne; inflazione progressiva | A5 | euristica (Osservazione) | `controlli_a5.py` |
| C7 Rilettura KRI | solo KRI in vigore, ciascuno una volta; un KRI non riletto resta "Non rilevato" (D-53) | A5 | per intero | `controlli_a5.py` |
| C8 Azioni | owner funzione e non persona; azione pertinente; non ripete un'azione aperta della baseline (D-69) | A5 | euristica, solo Osservazione (D-54); la regola sull'owner la applica `valida`, che rifiuta un owner persona anche se Accettato; azione con la stessa descrizione di un'azione aperta dello stesso rischio = Osservazione | `controlli_a5.py`, `esegui_ciclo_locale.py` |
| C9 KRI | due per rischio, uno di Esposizione e uno di Evoluzione (D-64; tipo cambiato su un KRI in vigore = Osservazione); fonte; soglie entrambe o nessuna, soglia_allerta >= soglia_attenzione; kri_id coerenti; KRI non riproposto = Osservazione | A5 | per intero | `controlli_a5.py` |
| Soglie invertite o vuote | vincoli fra due campi, non esprimibili in JSON Schema; una soglia vuota non deve valere 0 | — | C9 + formula Stato del foglio ("SOGLIE INVERTITE", "Soglie da definire" prima di ogni confronto); un KRI riproposto senza soglie conserva quelle validate | `controlli_a5.py`, tabella `tblKRI`, `esegui_ciclo_locale.py` |
| Segnalazioni da motivare (D-71; prima, D-56, rilievi di A5 superati) | una regola di metodo o un rilievo di A5 non ferma il ciclo, ma nemmeno sparisce | il validatore | le segnalazioni stanno sui rischi (colonna Rilievi), nella colonna Segnalazioni della griglia (⚑) e in Sintesi_Cicli; il Quadro dice quante sono; `valida` chiede la Motivazione sul rischio e non accetta salti di piu' di un punto ne' soglie invertite; i difetti di integrita' restano cancelli | `esegui_ciclo_locale.py`, `controlli_a5.py` (`combina`), `run_catena.py` passo 12 |
| Registro unico (D-79) | lo stato di ogni rischio (radar, in uscita, osservazione) segue la regola di Parametri, sui valori proposti alla scrittura e sui validati dopo `valida`; KRI e azioni solo per il radar; al massimo 20 rischi in osservazione; i rischi in osservazione non toccati da A1 restano com'erano | lo script, con un solo modulo (`radar.py`) per script, controlli, precontrollo e kit | oltre 20 in osservazione e rischio del radar senza KRI o azioni come Bloccante; rischio che entra senza KRI o azioni come Da motivare; KRI o azioni su un rischio in osservazione, riscritto senza fonte nuova, senza orizzonte o segnale come Osservazione; la decisione del validatore sullo stato (Radar, Osservazione) con la Motivazione | `radar.py`, `controlli_a5.py` (`stati_previsti`), `esegui_ciclo_locale.py` (`applica_stati`), `test_controlli.py`, `run_catena.py` passi 2, 5, 13, 14 |
| Ciclo straordinario (D-75) | si rivalutano solo i rischi decisi dalla funzione di rischio, con la stessa catena; un numero fuori dal trimestre passa comunque da controlli e validazione | lo script, il validatore | decisione con decisore e motivo archiviata (`Straordinario_<periodo>.json`), C1 in modo straordinario (rischio indicato assente o rischio esistente in piu' = Bloccante), rischi non rivalutati riportati con la validazione d'origine, regola del punto sul periodo validato prima, colonna Straordinario in Sintesi_Cicli | `esegui_ciclo_locale.py` (`baseline --straordinario`, `scrivi_trimestrale`), `controlli_a5.py`, `run_catena.py` passi 7b e 8s |
| Copertura del ciclo | tutti i rischi in anagrafica scritti nel ciclo | — | Registro righe 4-5 (nomi coperturaAnagrafica, coperturaValutati) + stessa logica in Python; gate prima del salvataggio | `genera_dashboard.py`, `esegui_ciclo_locale.py` |
| Integrita' formule | nessuna formula sovrascritta con un valore | — | verifica dopo ogni scrittura | `esegui_ciclo_locale.py` |
| Composito | calcolato solo dal foglio | — | formula Score_Composito; lo schema non ha il campo | `mappatura_campi.json` |
| Direzione | 2 segnali netti in 4 settimane (D-61) | A3 propone flag | segnali netti calcolati dal foglio | Registro, colonna Q |
| Schede dei rischi (A6) | i testi estesi spiegano i dati validati senza cambiarli | A6 | stessi rischi, quattro dimensioni, fonti identiche all'input, nessun numero fuori dai dati del rischio e dalla rubrica; niente file se un controllo fallisce; il registro non si tocca (D-40) | `07_Senza_Studio/schede.py`, `test_controlli.py`, `run_catena.py` |
| Perche' un rischio e' segnalato | il comitato legge un motivo che i dati sostengono | — (A1 scrive solo messaggio e decisioni) | il Quadro calcola dai dati validati i rischi segnalati (primi tre, AGIRE ORA, variati, nuovi) e il loro perche'; il collaudo li confronta con una selezione indipendente (D-39) | `genera_dashboard.py`, `run_catena.py` |
| Approvazione | nessun ciclo valido senza validatore | — | griglia del foglio Validazione, una riga per rischio, KRI, azione e notizia (D-67): ogni proposta accettata (riga non toccata), rettificata (cella gialla cambiata) o respinta; comando `valida` che controlla le decisioni e le applica; il trimestre dopo non parte se il precedente ha decisioni aperte | W1 passi 8-9, `esegui_ciclo_locale.py` |
| Griglia di validazione | il foglio di lavoro corrisponde alle proposte da decidere (D-67) | — | `valida` si ferma se nella griglia mancano righe o ci sono ID che non sono da validare, con la riga del foglio; il comando `griglia` la ricostruisce dalle proposte conservando cio' che e' scritto nelle righe intatte; trimestrale e settimanale la riscrivono senza perdere le decisioni gia' scritte e senza fermarsi per un valore sbagliato scritto li' | `esegui_ciclo_locale.py`, `run_catena.py` passi 2b, 3, 12 |
| Rettifiche umane | una rettifica rispetta le stesse regole della proposta | — | `controlla_valore`: interi 1-5, massimo un punto dal ciclo precedente (Velocity anche vuota; da vuota qualunque valore), soglie numeriche, entrambe o nessuna, coerenti, owner funzione, vocabolari; o tutte valide o nessuna applicata | `esegui_ciclo_locale.py`, `test_controlli.py`, `run_catena.py` |
| Urgenza | calcolata, non stimata | — | Radar_Mosca: X + Y > Z con parametri in Parametri; il collaudo la confronta con un calcolo indipendente | `genera_dashboard.py`, `run_catena.py` |
| Fonti delle notizie | ogni notizia cita una fonte dell'elenco, o MAN | prompt di A3 (elenco nelle istruzioni) | `codice_fonte` obbligatorio nello schema; la scrittura settimanale ferma un codice fuori elenco o escluso | `01_Kernel/fonti.md`, `esegui_ciclo_locale.py` |
| Storico KRI | un valore rilevato non si riscrive | — | tabella KRI solo in coda, una riga per KRI per ciclo; il collaudo verifica che le righe dei cicli prima restino identiche | `esegui_ciclo_locale.py`, `run_catena.py` |
| Esito di A5 del ciclo giusto | un'approvazione vale solo per l'output di A1 esaminato | — | la scrittura si ferma se l'esito di A5 e' di un altro ciclo o cita rischi assenti dall'output di A1 | `esegui_ciclo_locale.py`, `run_catena.py` |
| Coerenza dopo la validazione | il registro validato non si contraddice | — | Esito e Variazioni ricalcolati sui valori validati (la rettifica diventa una variazione con la motivazione come evidenza, anche "da n.v."; la sola Confidence non fa Variato); valore di un KRI rettificato con data e fonte; `Righe_liste` riscritte con i valori validati; una cella cambiata o un Respingi senza Motivazione fermano la validazione | `esegui_ciclo_locale.py`, `run_catena.py` |
| Testo esterno innocuo | un titolo di notizia o un testo di un agente non diventa formula ne' data | — | ogni testo scritto in cella come testo (apostrofo iniziale) | `esegui_ciclo_locale.py` (`per_cella`), `run_catena.py` |
| Anni di adeguamento | una stima dell'agente non diventa urgenza senza una decisione umana (D-60) | A1 stima | colonna degli anni di adeguamento nella riga del rischio della griglia di Validazione; `valida` scrive nell'anagrafica solo il valore validato (numero 0-30); una stima vuota non cancella un valore gia' presente; nessuna variazione | `esegui_ciclo_locale.py`, `test_controlli.py`, `run_catena.py` passo 2b |
| Report al comitato | il PDF segue i dati validati e le correzioni manuali successive (D-62) | — | comando `report`: sola lettura, fermo con decisioni da prendere o errori di formula, la versione precedente del PDF resta | `esegui_ciclo_locale.py`, `run_catena.py` passo 2b |
| Dismissione di un rischio | un rischio esce solo per decisione tracciata, senza buchi nelle viste | — | comando `dismetti`: motivazione obbligatoria, anagrafica ricompattata, KRI fuori vigore, azioni annullate, atto in `Dismissioni/` | `esegui_ciclo_locale.py`, `run_catena.py` |
| Modifica di un valore gia' validato (D-76) | un valore cambia fuori dal ciclo solo con decisione motivata e tracciata | rischio: la riapertura diventa un modo di cambiare gli score senza il limite di un punto | comando `riapri`, poi `valida`: stesse regole della validazione tranne il limite di un punto, Motivazione obbligatoria per ogni valore cambiato, storico con "(riapertura)", valore di prima conservato; il report presentato resta nell'Excel archiviato del ciclo. Controllo di secondo livello: le righe "(riapertura)" di Storico_Validazioni | `esegui_ciclo_locale.py`, `run_catena.py` (passo 13) |
| Testi corretti a mano (D-76) | descrizioni e razionali leggibili senza rifare il ciclo | limite accettato: **nessuna traccia automatica** di chi e quando (solo il Backup e l'Excel archiviato prima); un numero scritto in un testo non passa dai controlli | ammessi solo nelle colonne di testo elencate nel foglio Guida; mai ID, numeri, date o righe; `baseline` riallinea A1 e A7 | guida, sezione 3-ter |
| Colonne tolte dal modello | un registro vecchio si aggiorna senza perdere dati | — | `aggiorna-registro`: le `colonne_dismesse` della mappa (Gap_Controlli, Dimensione delle azioni) restano solo nel backup; le righe ancora da validare passano nella griglia con le decisioni gia' scritte (D-67), fermo solo se riguardano campi tolti dal modello; presidio "Non verificato" | `esegui_ciclo_locale.py`, `run_catena.py` passo 11b |
| Codici dello strumento di ricerca | nessun riferimento irrintracciabile nelle fonti | prompt di A1, passo 10 | la scrittura toglie i codici `turn…` dai riferimenti prima di scrivere il ciclo | `esegui_ciclo_locale.py` (`pulisci_riferimento`) |

Ogni controllo deterministico e' a sua volta collaudato: `99_Collaudo`
contiene, per ciascuno, un caso che deve passare e uno che deve essere
fermato. Un controllo che conta la cosa sbagliata, o che nessuno vede,
protegge quanto nessun controllo.

## 3. Evidenze da conservare per ciclo (in `Archivio_Cicli/Cicli/<ciclo>/`)

Lo script le archivia da solo, tranne il testo dei prompt:
- Output di A1 e di A5, esito dei controlli meccanizzati (`Esito_controlli_<ciclo>.json`).
- Baseline usata come input (`Baseline_usata_<ciclo>.json`).
- `Righe_liste_<ciclo>.json` (riscritto dalla validazione con i valori
  validati) e l'Excel di output del ciclo (`NFR_Registro_<ciclo>.xlsx`, stato
  prima della validazione).
- Fuori ciclo: l'atto di ogni rischio dismesso (`Archivio_Cicli/Dismissioni/<rischio>_<data>.json`:
  chi, quando, perche', KRI e azioni toccati).
- **Il testo dei prompt in uso** (i quattro file di `02_Agenti` e la versione del
  kernel, `fonti.md` compreso): si modificano nell'interfaccia di Agent Builder o Copilot Studio
  senza traccia, quindi vanno fotografati a ogni ciclo.
- Chi ha validato e quando, e ogni decisione (`Validazione_<ciclo>.json`,
  `NFR_Registro_<ciclo>_validato.xlsx`; nel registro: foglio dati
  Storico_Validazioni, una riga per campo, e colonne `Approvato_Da`,
  `Data_Validazione`, `Validazione` delle tabelle dati).
- In caso di arresto: il rapporto, la correzione fatta e chi l'ha fatta.

## 4. Rischi del sistema stesso

| Rischio | Meccanismo | Presidio |
|---|---|---|
| Ancoraggio alla valutazione precedente (analisi 17, 17.10) | la spinta opposta all'inflazione: conferma di default, un punto per ciclo, baseline con i valori di prima e accettazione senza gesti in validazione fanno restare basso un rischio entrato basso; i descrittori di Probabilita 4-5 chiedono casi gia' osservati e l'esposizione della Banca, che A1 non conosce, quindi i rischi nuovi entrano di solito a 3 o meno | comando `diagnosi` (D-80): valori all'ingresso dei rischi nuovi e verso delle rettifiche del validatore; `riapri` senza il limite di un punto; esposizione "non nota" dichiarata da A1 e decisa dal validatore (D-81), contata da `diagnosi`; proposte aperte: salto con evidenza forte, contraddittorio (A-17), taratura (A-12) |
| Rischio lontano mai urgente | la Prossimita si ferma a "oltre 3 anni" (Z = 3,5) e la regola del radar vuole Prossimita almeno 2: un rischio a mitigazione lunga (crittografia post-quantistica) resta in osservazione se nessuno ne stima gli anni di adeguamento, perche' il margine usa la Y di riserva | dal 19/10 (D-80) A1 stima gli anni di adeguamento anche dei rischi in osservazione con Impatto 4-5: con X + Y > Z il rischio e' AGIRE ORA ed entra nel radar; il comando `diagnosi` segnala quelli che ne sono privi |
| Inflazione progressiva | ogni ciclo aggiunge un po' di preoccupazione, nessuno toglie | regola di conferma di default; simmetria delle riduzioni; C6 a livello ciclo; confronto nel foglio Storico su otto cicli |
| Deriva mediatica | la copertura sostituisce l'evidenza | soglia di 3 segnali netti; A3 non modifica score; C6 |
| Affidamento su A4 | il parere su richiesta diventa una valutazione di fatto | A4 non scrive, non propone numeri, rimanda al ciclo trimestrale |
| Ciclo scritto a meta' | rischi mancanti letti come rischio nullo | controllo di copertura, gate prima del salvataggio, #N/A invece di zero |
| Prompt modificati senza traccia | il comportamento cambia fra cicli | fotografia dei prompt per ciclo; `componi_prompt.py --verifica` |
| Retrieval incompleto | il planner salta una knowledge source | kernel nelle istruzioni; baseline allegata esplicitamente |
| Kernel generico | descrittori e soglie non della Banca | adattamento obbligatorio prima del deploy (00_LEGGIMI) |
| Validazione non indipendente | nel pilota una sola persona lancia gli agenti e ne valida le proposte (`04_Riferimenti/DECISIONI.md`, D-13) | **limite accettato per il pilota** (D-30): dichiararlo nel report al comitato; la quota di rettifiche resta visibile per ciclo; da riconsiderare prima dell'esercizio pieno (G4) |
| Validazione di facciata | il validatore lancia `valida` senza guardare: con la griglia (D-67) una riga non toccata vale come accettata, quindi accettare tutto non chiede nessun gesto e nello storico non si distingue da un'accettazione ragionata | la quota di rettifiche per ciclo e' nel Registro (G4, "Rettifiche applicate"), nel riepilogo di `valida` e nel foglio Storico_Validazioni: una quota sempre a zero e' un segnale da portare al comitato; i rischi scritti superando un bloccante di A5 (⚑) chiedono la Motivazione anche se non cambia nulla; Score e Margine di Mosca della griglia mostrano l'effetto di ogni valore prima di confermarlo |
| Livello di allerta come automatismo | il colore del radar letto come decisione gia' presa, o soglie che mettono quasi tutto in Attivazione | e' un calcolo del foglio su dati validati (D-63), non uno score: le conseguenze dei tre livelli le decide la funzione di rischio; le soglie stanno in Parametri (righe 60-63) e la distribuzione si controlla a ogni cambio (demo, collaudo); il motivo di ogni livello e' scritto (colonna AB) |
| Tipo del KRI sbagliato | A1 classifica come evoluzione un dato che misura l'esposizione, o viceversa | A5 ne giudica la coerenza (C9); il tipo di un KRI in vigore non cambia senza un'Osservazione; il tipo non e' un campo di validazione: si corregge con il ciclo successivo |
| Urgenza fraintesa | il Radar_Mosca letto come previsione | e' una graduatoria ancorata (Z ha cinque valori, la meta' della fascia della Prossimita, D-59; Y viene dagli orizzonti delle azioni, al massimo un anno, o dagli anni di adeguamento decisi dal validatore, D-33): rubrica sezione 8, limiti dichiarati; la lente di Mosca della Classifica mostra X, Y e Z di ogni rischio |
| Urgenza sottostimata | un rischio con adeguamento pluriennale (migrazione crittografica, legacy, uscita da un fornitore) risulta "con margine" perche' le azioni durano al massimo 12 mesi | colonna Anni_Adeguamento dell'anagrafica (D-33): input del validatore, conservato dalla scrittura, usato come Y minima |
| Segnalazioni accettate per abitudine (D-71) | il validatore scrive una motivazione di rito su ogni ⚑ invece di correggere, e senza A5 nessuno giudica la plausibilita' dei valori (C4) | la Motivazione e' obbligatoria e resta nello storico accanto alla proposta; il Quadro dice quante segnalazioni erano da motivare; salti e soglie invertite non si accettano; A5 si puo' sempre usare, per esempio al primo ciclo o su un campione; il numero di segnalazioni per ciclo va portato al comitato |
| Presidio non aggiornato | il Presidio_Controlli resta "Non verificato" per sempre: il comitato non sa se i controlli ci sono | e' un input del validatore visibile nel Registro e nelle schede; un "Non verificato" su un rischio AGIRE ORA e' un punto da portare al comitato; non entra nello score, quindi non lo abbassa ne' lo alza (D-49) |
| Velocity sempre non valutata | lo score si calcola su tre dimensioni per molti rischi e non e' confrontabile fra rischi | i pesi si ridistribuiscono in modo dichiarato (Metodologia, nota del Delta); la Velocity entra quando una fonte documenta i tempi; da rivedere nella taratura A-12 |
| Attenzione del supervisore scambiata per gravita' | il ◆ del radar (D-35, D-63) spinge a trattare come prioritario un rischio solo perche' e' un tema di vigilanza | e' un input del validatore, separato dagli score: non entra ne' nello score ne' nell'urgenza ne' nel livello di allerta; la Metodologia lo dice; la decisione e' tracciata in anagrafica |
| Commento superato dalla validazione | il comitato legge nel Quadro il commento di A1, scritto prima delle rettifiche | il Quadro avvisa ("Dopo il commento") quante rettifiche o respingimenti sono stati applicati dopo il commento; numeri, grafici e rischi segnalati del report sono sempre quelli validati |
| Spiegazione che inventa (A7, D-72) | A7 risponde in modo convincente con un motivo che il registro non contiene, o presenta come motivo di A1 una sua ricostruzione | legge solo la cartella Spiegazioni scritta dallo script e i documenti; il prompt lo obbliga a distinguere registrato, calcolato e sua lettura e a dire cio' che non sa; non scrive nulla e non propone valori; copione di prova `04_Riferimenti/Prove/Prova_A7.md` |
| Osservazione come parcheggio (D-79) | un rischio vicino resta in osservazione, quindi fuori da radar, urgenza e azioni | lo stato non lo sceglie A1: lo calcola la regola sulle soglie di Prossimita e Probabilita, e un rischio AGIRE ORA o del supervisore e' sempre nel radar; la capienza tiene fuori solo i piu' bassi per score, con il motivo scritto; la pagina Fenomeni porta al comitato i rischi in osservazione con il perche'; il validatore puo' mettere un rischio nel radar con la decisione sullo stato |
| Straordinari per abitudine (D-75) | ogni notizia forte diventa un ciclo straordinario, con piu' lavoro di validazione e meno confrontabilita' fra trimestri | A3 e A4 propongono solo con la regola del segnale critico; decide la funzione di rischio con decisore e motivo agli atti; lo straordinario rivaluta solo i rischi indicati e conta come ciclo per la regola del punto; il numero di straordinari del periodo va portato al comitato |
| Scheda che inventa | un testo esteso ben scritto introduce un dato che il ciclo non ha valutato, o attribuisce a un documento un fatto che non contiene | A6 lavora solo sull'input dei dati validati, senza altre fonti; lo script ferma ogni numero che non sta nei dati del rischio e ogni fonte non identica; dal 02/10 (D-68) il perche' di ogni valore, con i documenti, lo scrive A1 che li ha letti (razionale in parti) e A6 lo riformula senza attribuire a un documento cio' che A1 non gli attribuisce; senza A6 la scheda mostra il testo di A1; nomi di persone e corrispondenza fra testi e fonti: controllo di chi legge le schede prima del comitato |
| Fonti non validate o fuori licenza | una notizia entra nel registro da una fonte che la Banca non ha scelto, o il cui contenuto non puo' essere dato a un'AI | nessuna fonte usata finche' la funzione di rischio non la approva (al 24/09 tutte approvate tranne FNT-19, esclusa, con licenze verificate da Legal: DECISIONI D-15, D-27..D-29); licenza per voce; raccolta di default solo dalle fonti "approvata"; revisione almeno annuale dell'elenco |
| Fonte silenziosa | un feed cambia indirizzo e smette di dare notizie senza errori | la raccolta dichiara in testa al file le fonti irraggiungibili; da controllare anche le fonti con zero notizie per piu' settimane |
| Copie fuori dall'archivio | gli allegati caricati in chat (baseline, output di A1) sono copiati nella cartella OneDrive personale "Microsoft Copilot Chat Files" e ci restano | l'archivio ufficiale resta `Archivio_Cicli`; applicare la retention della Banca anche a quella cartella; non condividerla. Parere DPO positivo (DECISIONI D-24) |
| Capability accese per default | il code interpreter di Agent Builder e' acceso di default: l'agente potrebbe produrre file o eseguire codice non previsti dalla configurazione | spegnerlo su ogni agente (README, setup; guida, sezione 0.2) e ricontrollarlo quando si ricaricano le istruzioni |
| Codice eseguito dentro l'agente (prova di Copilot Studio, D-70) | il precontrollo gira dentro A1, con lo script allegato al Code interpreter o con la skill `precontrollo-nfr` nel sandbox. L'agente decide se eseguirlo e riferisce lui l'esito: potrebbe saltarlo, eseguirlo su un'altra versione del JSON, riscriverlo o dichiarare un esito mai stampato. Nella nuova esperienza ogni prova consuma Copilot Credits | lo script e' quello del pacchetto, composto da `prepara_kit.py` e verificato identico dal collaudo; stampa l'impronta dell'output, che il precontrollo sul PC ricalcola sul file consegnato; `trimestrale` rifa' comunque tutti i controlli prima di scrivere (D-10). Solo agenti di prova: D-11 resta in vigore. Tetto di crediti per l'agente di prova (Power Platform admin center) |

## 4-bis. La base dati delle rettifiche (per l'apprendimento futuro)

La proposta originale resta nel foglio dati Storico_Validazioni
(`Proposta_Agente`, una riga per campo, scritta da `valida` dalla griglia del
foglio Validazione, D-67) e nell'output di A1 archiviato; nel registro restano
i valori validati, con Variazioni coerenti. Ogni riga dello storico con
Decisione "Rettificato" o "Respinto" e'
una coppia **proposta dell'agente -> decisione della Banca**, con motivo,
autore, data e contesto (periodo, oggetto, campo). Le righe "Accettato"
sono gli esempi confermati. Insieme sono il materiale per:
- misurare la qualita' degli agenti per campo (quota di rettifiche su
  Impatto, Probabilita, anni di adeguamento, soglie dei KRI...) e per ciclo;
- in futuro, costruire esempi per i prompt o un insieme di addestramento e
  valutazione. Prima di usarle a questo scopo: verifica con la compliance
  (dati interni in un modello) e selezione delle sole righe con motivazione
  esplicita: un "Accettato" senza motivazione e' una riga della griglia non
  toccata, che puo' essere anche una riga non letta.

## 5. Limiti da riportare in ogni memo

Testo da includere, adattato, in ogni memo trimestrale. Dal 25/09 compare da
solo nel foglio Quadro del report al comitato (D-32, D-39): il generatore del
template lo legge da qui (le righe che iniziano con ">"), quindi si cambia in
questo file e poi si rigenera il template.

> Le valutazioni sono prodotte con il supporto di un modello linguistico
> ancorato alla rubrica della Banca e verificate da controlli deterministici e
> da un challenger indipendente. Non sono stime di perdita ne' probabilita'.
> Gli score cambiano solo nel ciclo trimestrale, su evidenza datata; le notizie
> settimanali producono segnali, non variazioni. Il controllo C4 (plausibilita'
> rispetto ai descrittori) e' solo di giudizio. La valutazione e' valida dopo
> l'approvazione indicata in Approvato_Da.

## 6. Nota sulla variante senza Copilot Studio (Agent Builder)

Che il trattamento avvenga dentro Agent Builder di Microsoft 365 Copilot **non
e' un'autocertificazione** che soddisfi i requisiti specifici della Banca
(residenza dei dati, DORA, esternalizzazione). La documentazione Microsoft
indica che le funzionalita' di Agent Builder sono elaborate da Copilot Studio,
con flussi di dati fra Microsoft 365 e Copilot Studio, e che le chiavi gestite
dal cliente non sono supportate per questi agenti (Microsoft Learn, "Agent
Builder in Microsoft 365 Copilot", agg. agosto 2026). Va verificato con la
compliance con la stessa cura riservata a Copilot Studio. Un amministratore puo'
disattivare Agent Builder per policy di tenant: verificarlo prima di investire
tempo nel setup.
