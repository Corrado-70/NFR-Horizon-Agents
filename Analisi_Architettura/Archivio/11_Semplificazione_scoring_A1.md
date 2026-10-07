# 11. Semplificazione dello scoring e della selezione dei rischi di A1

> **06/10 (D-71)**: dopo la semplificazione e il precontrollo (D-69), anche i controlli di metodo
> (C3, date di C5, coppia e soglie dei KRI) e i Bloccanti di A5 non fermano piu' il ciclo: vanno
> nella colonna Segnalazioni della griglia di validazione, con la Motivazione obbligatoria. A5 e'
> facoltativo. Lo script ferma solo i difetti di integrita' del registro.

Data: 30/09/2026. Stato: **approvata dall'utente il 30/09** (decisioni D-49..D-56
in `08_Deploy/DECISIONI.md`) e **realizzata nel pacchetto il 30/09** (voce
**S1** del TODO; struttura 2026-09-30): restano le verifiche dell'utente e il
passo sul PC della Banca (sezione 8). Oggetto: il pacchetto
`NFR_Emerging_Risk_Agents/` alla versione della struttura 2026-09-25c.

Richiesta dell'utente (29-30/09): il collaudo del primo ciclo ha mostrato che
il modello di scoring e selezione dei rischi e' troppo articolato per valutare
rischi nuovi da poche fonti, spesso senza riscontri interni. Semplificare;
prima, rivedere tutte le informazioni che A1 produce, dove sono usate, come e
se servono davvero, e l'effetto a cascata sugli altri agenti.

## 1. Perche'

Il primo ciclo di prova sul PC della Banca (29/09) ha richiesto 7-8 giri
A1 <-> A5. I blocchi avevano una radice comune:
- **C4 Gap_Controlli**: 7 rischi su 7 (A1 non vede i controlli della Banca);
- **C4 Prossimita 4-5** senza caso nominato: 6 rischi su 7;
- **C5**: fonti etichettate "Interne" che erano esterne (ORX);
- **C8**: owner validi scambiati per persone.

Le correzioni D-45..D-48 hanno fatto passare il ciclo aggiungendo regole, e A1
era a 7.977 caratteri su 8.000. Il modello chiedeva ad A1 due tipi di cose che
non dovrebbe fare:
- **giudizi che con poche fonti esterne non puo' sostenere**: lo stato dei
  controlli della Banca, i dati interni dei KRI (fonte, soglie, valori), le
  frequenze per rischi senza storia;
- **contabilita' che lo script sa fare da se'**: l'esito (Confermato,
  Variato, Nuovo) e i "da/a" delle variazioni.

E' un cambio di **struttura** (chi valuta cosa), non una taratura dei
descrittori: la taratura resta A-12, dopo il primo ciclo validato.

## 2. Perche' modifiche mirate e non una rigenerazione

- La modifica tocca il contratto dello scoring (rubrica, schemi, prompt
  A1/A5/A6/A4, controlli, mappa, alcune formule, schede, dati di collaudo); il
  resto (layout v3 approvato, installazione, correzioni fatte sul PC reale,
  piano AU) non cambia. Una rigenerazione rifarebbe anche quello, e non e'
  deterministica.
- C'e' un'installazione viva: agenti in Agent Builder, registro, library. Le
  modifiche arrivano con gli strumenti che esistono (`aggiorna-registro`,
  prompt da reincollare, decisioni nuove).
- Il PROMPT_MASTER del 29/09 non riprodurrebbe nemmeno il pacchetto del
  29/09 (mancavano D-45 e D-48): si riallinea e si aggiorna alla fine, come
  sempre.

## 3. Revisione dei campi di A1

Fatto strutturale: **Matrice, radar e Mosca usano solo Severity, Probabilita
e Prossimita** (P x S per la matrice e l'area dei cerchi; Prossimita -> Z per
l'urgenza). **Velocity e Gap_Controlli entravano solo nello score composito**
(Classifica, Delta, primi tre del Quadro).

| Campo di A1 | Dove finisce, a cosa serve | Decisione |
|---|---|---|
| `ciclo`, `data_riferimento`, `sintesi`, `id_rischio`, `nome`, `descrizione`, `event_type`, `driver[]`, `razionale` | chiavi, anagrafica, settore del radar, Quadro, schede, A6 (driver solo testo) | restano |
| `severity` | composito; asse della Matrice; area del radar | resta |
| `probabilita` | composito; asse della Matrice; area del radar | resta, con **descrittori di plausibilita'** |
| `prossimita` | composito; Z di Mosca (urgenza, AGIRE ORA, distanza nel radar) | resta; il "caso nominato" (D-48) sta nel descrittore |
| `velocity` | solo composito | resta, **facoltativa**: valutata solo se una fonte documenta i tempi (D-50) |
| `gap_controlli` | solo composito | **esce dal modello**; resta un dato qualitativo della Banca, `Presidio_Controlli` in anagrafica (D-49) |
| `confidence` | fuori dal composito; Registro, Delta, schede; C5 | resta 1-5, descrittori solo su numero, indipendenza e data delle fonti (D-52) |
| `esito` | Quadro (conteggi, rischi segnalati), Classifica, Delta | **lo calcola lo script** (D-51) |
| `variazioni[]` | Registro, Quadro "cosa e' cambiato", Delta, schede, A6 | A1 scrive `{dimensione, evidenza, data_evidenza}`; **da/a li calcola lo script** (D-51) |
| `fonti[]` | Registro, schede, A6; C5 e C6 | restano; `tipo` = library d'origine (D-45); lo script toglie i codici dello strumento di ricerca (`turn1search17 - ...`) |
| `azioni_mitigazione[]` | Azioni, Piano_azioni; **orizzonte = Y di Mosca** | restano, **senza `dimensione`**; C8 solo Osservazioni (D-54) |
| `kri_proposti` | tabella KRI storica, Indicatori, semaforo, "KRI in rosso" | **da 1 a 3, soglie facoltative**: le fissa il validatore (D-53) |
| `ricalcolo_kri_ciclo_precedente` | valore corrente dei KRI; C7 | **solo i KRI per cui A1 trova un valore** (D-53) |

**Selezione dei rischi (D-55).** Nel codice non c'e' mai stato un vincolo di
un rischio per event type; veniva dal testo ("individuali da zero su tutti e
sette gli event type", "copertura obbligata" nel piano di deploy). A1 l'aveva
letto come "uno per tipo" e per starci aveva accorpato piu' meccanismi in un
rischio. Regola nuova: un rischio per ogni meccanismo di perdita distinto
sostenuto da almeno una fonte specifica, anche piu' d'uno nello stesso event
type; nessun event type obbligatorio; la rassegna parte dai driver su cui le
fonti mostrano pressione; gli event type senza rischi si elencano nella
`sintesi`. Nessuna lista di ambiti "attesi" nel prompt (D-37): la prevalenza
cyber, se c'e', la danno le fonti. Capienza del template: da 15 a 20 rischi.

**A cascata.**
- A5 (stesse sezioni 1-4 della rubrica): controlli piu' semplici, prompt piu'
  corto; stessa numerazione C1-C9.
- A6: cinque valori spiegati (severity, probabilita, prossimita, velocity,
  confidence); il presidio della Banca e' un dato del rischio.
- A4: la riga con i nomi delle dimensioni.
- A3: nessuna modifica obbligata (non riceve i descrittori).
- Baseline: senza gap_controlli, cosi' A1 non ricopia un campo che il suo
  schema rifiuterebbe.

## 4. Il ciclo di prova del 29/09 (output di A1 del primo giro)

Verificato leggendo il codice dei controlli (`controlli_a5.py`):
- **i controlli meccanici passano**, con una sola Osservazione (owner
  "Immobili, Infrastrutture e Procurement"): tutti i blocchi venivano dal
  giudizio di A5;
- **Gap_Controlli = 4 su 7 rischi su 7**: con il pavimento D-47 e' una
  costante (0,80 uguale per tutti nel composito);
- **un rischio per ciascun event type** ("censiti sette rischi, uno per
  ciascun event type"); NFR-06 accorpa cloud e compromissione di terze parti,
  NFR-02 deepfake, identita' sintetiche e social engineering; NFR-03 e NFR-05
  sono i piu' deboli come rischi emergenti;
- **26 fonti, tutte esterne** (ORX e report di settore), tutte con un codice
  dello strumento di ricerca in testa (`turn1search17 - ...`), che non si
  rintraccia;
- **21 KRI, tutti con soglie senza base interna**;
- **Velocity** motivata con i tempi in NFR-02, 05, 06; in NFR-01, 03, 04, 07 no;
- **Prossimita 4 su cinque rischi**, tre dei quali (NFR-01, 04, 07) senza caso
  nominato: A5 li ferma per D-48; con l'opzione nuova il ciclo si scrive e
  decide il validatore.

## 5. Come funziona dopo

- **Composito**: media pesata delle dimensioni valutate. Pesi provvisori in
  Parametri: Severity 0,35, Probabilita 0,25, Prossimita 0,20, Velocity 0,20;
  se la Velocity manca, i pesi si ridistribuiscono sulle altre tre. Vuoto se
  manca una delle tre obbligatorie.
- **Esito** calcolato: "Nuovo" = id non in baseline; "Variato" = cambia
  Severity, Probabilita, Prossimita o Velocity (da vuota a un valore conta);
  la sola confidence non basta. Stessa regola dopo la validazione.
- **Variazioni**: da/a aggiunti dallo script; una Velocity che entra da vuota
  produce una variazione "da n.v.".
- **Opzione `trimestrale --procedi-con-rilievi --motivo "..."`** (D-56):
  - supera solo i rilievi Bloccanti di A5 (l'agente); i Bloccanti dei
    controlli meccanici e i fermi di integrita' restano cancelli (D-10);
  - tutti i rilievi finiscono sui rischi, colonna `Rilievi` del registro, anche
    senza l'opzione; quelli di ciclo in `Sintesi_Cicli`;
  - chi, quando, perche' e quanti bloccanti superati: `Sintesi_Cicli` ed
    `Esito_controlli_<ciclo>.json`; il Quadro lo dice;
  - in validazione un rischio con un bloccante superato chiede la motivazione
    anche se "Accettato", e `--accetta-il-resto` non lo copre. (Dal 02/10,
    D-67: nella griglia del foglio Validazione il rischio ha ⚑ davanti al nome
    e la sua riga vuole la Motivazione anche se non cambia nulla;
    `--accetta-il-resto` non serve piu'.)
- **KRI**: soglie entrambe o nessuna; stato "Soglie da definire"; soglie
  validate conservate se A1 ripropone il KRI senza soglie; un KRI in vigore non
  riproposto esce di vigore e C9 lo segnala come Osservazione.
- **Controlli C1-C9**: stessa numerazione; C2 = un'evidenza per ogni valore
  cambiato; C7 = nessun KRI sconosciuto o ripetuto; C8 solo Osservazioni (e
  `valida` rifiuta un owner che sembra una persona anche se Accettato); C9 =
  da 1 a 3 KRI, soglie coerenti.
- **Migrazione**: `colonne_dismesse` nella mappa (Gap_Controlli del registro,
  Dimensione delle azioni): `aggiorna-registro` le lascia nel backup invece di
  fermarsi; si ferma se ci sono decisioni "Da decidere".

## 6. Ordine di lavoro

Voce S1 del TODO, prima di AU1: lo schema di A1 e' il contratto su cui
poggiano AU2 (riconoscimento degli agenti) e P1/P3/P5, e la semplificazione
libera lo spazio che P5 chiede nel prompt di A1. Passi, con quattro momenti di
verifica dell'utente: collaudo di partenza e riallineamento dei documenti;
decisioni; kernel (checkpoint 1: rubrica e schemi); dati di prova; codice;
workbook (checkpoint 2: anteprima del template); collaudo con Excel; prompt
(checkpoint 3: dimensioni); documentazione e demo; PC della Banca (checkpoint
4: `aggiorna-registro` su una copia).

## 7. Fuori perimetro (nel TODO)

- La Y di Mosca conta solo le azioni del ciclo corrente: le azioni aperte dei
  cicli prima sono ignorate.
- `sogliaDelta` colora solo il Delta; il nome `rmPxI` non e' usato.
- I flag di A3 citano "il descrittore", che A3 non ha, e non arrivano ad A1
  (tema di P1).

## 8. Stato della realizzazione (30/09/2026)

Fatto nel pacchetto:
- **Kernel**: rubrica (Probabilita di plausibilita', Prossimita con il caso
  nominato nel descrittore, Velocity facoltativa, Confidence su fonti
  indipendenti, KRI da 1 a 3 con soglie facoltative, pesi D-50), tassonomia
  (un meccanismo di perdita = un rischio), schemi A1 e A6, mappa (versione
  2026-09-30, `colonne_dismesse`, Rilievi, presidio, formule di score e stato
  dei KRI).
- **Prompt**: A1 7.496 caratteri (era 7.977), A5 7.563, A6 4.624, A4 5.031;
  A1 con la riga sui codici `turn…`.
- **Codice**: `controlli_a5.py` (C1-C9 ridotti, `combina` con il superamento),
  `esegui_ciclo_locale.py` (`completa_payload`, `--procedi-con-rilievi`,
  colonna Rilievi, validazione dei rischi con rilievi superati, owner persona,
  soglie conservate, "da n.v.", migrazione), `schede.py`, `confronta.py`.
- **Workbook**: struttura 2026-09-30, 20 rischi, Registro con Presidio e
  Rilievi e colonne calcolate da elenchi, Delta con asse ±1,5 e nota della
  scala dai pesi di Parametri, Quadro con i rilievi superati, Indicatori con
  "Soglie da definire", Piano_azioni senza "Riduce"; anteprima in
  `Anteprima_S1/` (fuori dal pacchetto) con i PDF dei fogli.
- **Collaudo**: dati di prova convertiti, baseline attese rigenerate, casi
  nuovi in `test_controlli.py` e nei passi 2, 2b, 11b e 12 di `run_catena.py`.
- **Documentazione**: guida, workflow, governance, liste SharePoint, manuale
  del template, schemi e prompt commentati, README, Piano_deploy,
  LEGGIMI del collaudo, PROMPT_MASTER (trappole 51-58), TODO.

Restano:
- le verifiche dell'utente (bozza della rubrica e schemi, anteprima del
  template, dimensioni dei prompt);
- la demo rilanciata;
- sul PC della Banca: `aggiorna-registro` su una copia del registro in uso,
  poi sul registro; ricaricare A1, A5, A6, A4 e la baseline in `Kernel`;
  rifare il ciclo 2026Q4 di prova. Obiettivo: 1-2 giri A1-A5, oppure un giro
  e `--procedi-con-rilievi`; meccanismi prima accorpati (cloud e terze parti,
  deepfake e identita' sintetiche) come rischi separati; distribuzione per
  driver che segue le fonti.

## 9. Revisione della rubrica del responsabile (30/09 sera, D-57..D-62)

Dopo la semplificazione il responsabile ha riletto la rubrica e ne ha
riscritto i descrittori. Cosa cambia rispetto alle sezioni 3 e 5:
- **Severity → Impatto** (D-57), nome usato nei descrittori del responsabile e
  nella Matrice; rinominata anche nei dati, con una migrazione dichiarata
  nella mappa (`colonne_rinominate`).
- **La Confidence esce** (D-58). La sezione 3 la teneva fuori dallo score come
  giudizio sulla solidita' dell'evidenza; il responsabile preferisce vedere la
  rilevanza di ciascuna fonte (1-3) invece di un numero unico del rischio. Il
  requisito che la sostituisce: Probabilita 5 o Prossimita 4-5 con almeno una
  fonte di rilevanza 3 (salvo deroga dichiarata); C5 lo segnala come
  Osservazione.
- **Z di Mosca** (D-59): la tabella 0 / 0,5 / 1,5 / 2,5 / 4 non era scritta
  accanto ai descrittori. Provato l'inizio della fascia (0 / 0 / 1 / 2 / 3):
  la Prossimita 4 valeva 0 come la 5 e nella demo nessun rischio aveva piu'
  un anno di margine; "troppi rischi in AGIRE ORA non danno nessuna
  informazione" (responsabile). Scelta la meta' della fascia (0 / 0,5 / 1,5 /
  2,5 / 3,5), scritta nella rubrica; la taratura resta in A-12.
- **Anni di adeguamento** (D-60): li stima A1, li decide il validatore, e
  restano nell'anagrafica. E' l'unico campo nuovo per A1 dopo la
  semplificazione: e' una stima di conoscenza generale (quanto dura una
  migrazione, un adeguamento normativo), che la validazione umana corregge.
- **Soglie** di direzione (2) e del Delta (0,30) e descrittori (D-61), dalla
  tabella del responsabile.
- **Report** rigenerabile con il comando `report` dopo correzioni manuali, e
  fogli di lavoro stampabili (D-62).

Il margine di A1 torna stretto (7.885 caratteri): un'altra aggiunta al prompt
richiedera' di spostare testo dalla rubrica ai COMMENTATI o di accorciare i
descrittori.

## 10. Livello di allerta, KRI per tipo, esposizione (01/10, D-63..D-65)

Tre suggerimenti di una proposta esterna, adottati dal responsabile dopo la
revisione della Z (meta' fascia):
- **Livello di allerta** calcolato dal foglio, senza campi nuovi: risponde a
  "che cosa si fa adesso", che l'urgenza da sola non dice. Due segnali forti
  per l'Attivazione e un motivo di merito per l'Attenzione, per non ripetere
  l'errore della Z all'inizio della fascia (un criterio che scatta per
  tutti). Coerente con la sezione 3 di questa analisi: A1 non stima niente di
  nuovo; il livello e' contabilita' del foglio su dati validati.
- **KRI per tipo**: due per rischio. Riprende D-53 (le soglie e i valori
  interni non li puo' inventare A1): il tipo dice chi fornisce il valore,
  A1 per l'evoluzione, la Banca per l'esposizione.
- **Esposizione nella Probabilita**: una riga, non una dimensione. Una
  dimensione "Esposizione" avrebbe chiesto ad A1 un dato interno, come
  Gap_Controlli (D-49).

Il prezzo e' nel prompt di A1: 7.917 caratteri su 8.000, ottenuti accorciando
esempi della rubrica che ripetevano altre regole.

## 11. Meno giri fra A1 e A5, testi piu' ragionati (02/10 sera, D-69)

Dopo la semplificazione l'utente trovava ancora scomodo il giro A1 → A5 →
`trimestrale` → A1, e povere le descrizioni e le motivazioni di A1. Due cause,
nella linea di questa analisi:
- **A1 non conosceva le regole con cui veniva controllato**: le aveva A5 nel
  suo prompt. Ora il testo dei nove controlli sta in un solo file del kernel e
  arriva anche ad A1, in un allegato (`Input_A1_<ciclo>.txt`, con la baseline):
  le istruzioni di A1 non hanno piu' spazio (7.963 caratteri), l'allegato si'.
- **Gli errori meccanici si scoprivano solo dopo A5**: ora li trova il comando
  `precontrollo` prima di A5, in pochi secondi e senza Excel, e scrive il
  messaggio di correzione per A1. E' la parte affidabile: l'autocontrollo di A1
  riduce gli errori, ma un modello che rilegge il proprio output tende a
  confermarlo.
- **Testi**: le istruzioni compresse non dicevano com'e' fatto un buon testo.
  La guida di scrittura nell'allegato lo dice (meccanismo causa-evento-danno,
  per ogni valore descrittore, fatto, documento e perche' non il valore
  vicino) e mostra un esempio completo.

Obiettivo della sezione 8 aggiornato: in Banca, uno o due precontrolli e un
giro di A5, oppure un giro e `--procedi-con-rilievi` sui soli rilievi di
giudizio.

