# 14. Tre strade: tutto sul PC, ibrida, tutto in Copilot Studio

Data: 09/10/2026. Richiesta dell'utente, dopo la prima tornata della prova K0 di Copilot Studio:
- "una volta implementato voglio che nessun python giri su PC, solo via agenti copilot studio";
- "a cosa mai mi servirebbe l'agente copilot se tengo python su PC?";
- "tieni CS-1 e approfondisci i pro e contro delle 3".

Aggiorna `12_Due_opzioni.md`, che teneva due opzioni: l'app Python e la CS-1. Le strade diventano tre:

| Strada | In una riga |
|---|---|
| **A. Tutto sul PC** | agenti in Agent Builder come oggi; un'app Python guida l'analista; il motore Python controlla e scrive (12.3) |
| **CS-1. Ibrida** | un Operatore in Copilot Studio orchestra gli agenti e consegna i JSON in SharePoint; il motore Python resta su un PC esecutore, in background (12.4; piano 10, 10.12) |
| **CS-2. Tutto in Copilot Studio** | come la CS-1, ma senza PC: i controlli sono lo stesso codice Python, eseguito nel code interpreter dell'agente; registro e report si leggono e scrivono con Office Scripts lanciati dai flussi |

La CS-2 di qui riprende quella del piano 10 (10.11), con un cambiamento: dal 05/10 si sa che il code interpreter
puo' eseguire il nostro script cosi' com'e', e T1.2 del 09/10 l'ha mostrato. Per questo i controlli non vanno piu'
riscritti in TypeScript: si riscrive solo la parte che parla con Excel. La CS-3 del piano 10 (Power Query) non si
riprende: e' una CS-2 con un motore peggiore.

**In breve**: A e' la sola che si puo' fare subito con certezza. La CS-1 aggiunge comodita' e piu' utenti, ma
lascia un PC acceso. Solo la CS-2 realizza l'obiettivo dell'utente, a prezzo di settimane di lavoro e di un
controllo prima della scrittura meno forte di oggi. La raccomandazione (14.7) e' puntare alla CS-2 con un percorso a
tappe. Le prime tappe servono a tutte e tre le strade; la scelta si fa sugli esiti di tre prove brevi nel tenant
(K6, K8, K9).

## 14.1 Cosa e' cambiato dal 07/10

| Fatto | Fonte | Conseguenza |
|---|---|---|
| Copilot Studio, esperienza standard con code interpreter: A1 funziona nel riquadro di prova; lo script del precontrollo allegato viene eseguito (T1.2); una richiesta di aggirarlo viene rifiutata (T1.4); una ripetizione e' andata una volta in errore (T1.3) | prova K0, 09/10 | il nostro Python **puo'** girare nel cloud senza riscriverlo; l'affidabilita' su compiti lunghi e' da misurare |
| Nuova esperienza (skill) non disponibile in Banca | K0, 09/10 | si lavora solo con il code interpreter dell'esperienza standard: per gli utenti Microsoft 365 Copilot e' "No charge" |
| Un JSON di A1 da 40-60 KB passa intero da un agente a SharePoint con un agent flow (impronta uguale) | K0, B3, 09/10 | la consegna dei file senza appunti funziona |
| In Teams l'agente risponde spesso con errori. Causa probabile: i messaggi oltre circa 100 KB in UTF-16 | K0, 09/10; Learn | i JSON non devono passare nei messaggi, solo nei flussi e nelle variabili (forma della prova K6) |
| La knowledge SharePoint dell'agente funziona | utente, 09/10 | cade il vincolo "knowledge bloccata" del 06/10 (12.2) |
| Un argomento puo' chiamare un sotto-agente con input e output e un flusso; uno strumento puo' essere riservato all'argomento | Learn, 09/10 | la sequenza la decide l'argomento, non il modello (prova K6) |
| Office Scripts da un flusso: fino a 1.600 chiamate al giorno, 3 ogni 10 secondi, 5 MB per richiesta e risposta, nessuna chiamata esterna | Learn, Platform limits | bastano per un registro da circa 0,5 MB; l'amministratore li puo' spegnere (da verificare, K8) |

## 14.2 Le tre strade in figura

```
A. Tutto sul PC
  Analista ─> app NFR (Python) ─> Agent Builder: allega, incolla, Copia (3 gesti per agente)
                 └─> motore Python ─> registro Excel (COM), archivio, PDF

CS-1. Ibrida
  Analista ─> Teams: Operatore (Copilot Studio) ─> sotto-agenti A1, A3, A5, A6, A8
                 └─> agent flow ─> SharePoint Archivio_Cicli\In_arrivo
                                       │ app OneDrive: copia sul PC delle library SharePoint
                                       ▼
            PC esecutore (sempre acceso, utente collegato) ─> motore Python ─> registro (COM), PDF

CS-2. Tutto in Copilot Studio
  Analista ─> Teams: Operatore ─> sotto-agenti
                 ├─> code interpreter: logica Python del pacchetto (controlli, radar, righe da scrivere) su JSON
                 └─> agent flow ─> Office Scripts sul registro in SharePoint (legge tabelle -> JSON, scrive righe)
                               └─> SharePoint: archivio, knowledge di A7, conversione in PDF
```

## 14.3 Strada A — Tutto sul PC

Descritta in 12.3 (app NFR, stato del processo, appunti, lucchetto, installazione).

**Pro**
- Si fa subito: sta in tutti i vincoli noti e non dipende da prove nel tenant.
- Il controllo prima della scrittura resta codice sempre uguale (D-10). Il collaudo resta intatto, con oltre 800
  verifiche. Lo stesso codice gira in collaudo e in esercizio (D-02).
- Nessuna piattaforma in piu' da governare; nessun costo a consumo.
- E' la piu' veloce: 10-14 giorni.
- Non dipende da funzioni in anteprima di Copilot Studio ne' dai limiti di Teams.

**Contro**
- Python su ogni PC che usa il sistema: installazione, aggiornamenti, antivirus, approvazione dell'IT.
- **Non realizza l'obiettivo dell'utente.**
- Restano i tre gesti per agente, perche' Agent Builder non ha API.
- Si lavora al PC: una persona alla volta sul registro, con il lucchetto.
- La raccolta notizie dipende dal proxy del PC e dal PC acceso.
- Restano le fragilita' note di Excel via COM: le trappole del PROMPT_MASTER.

**Quando conviene**: pilota a una persona (D-13); IT che non apre Office Scripts o il code interpreter; serve un
processo stabile prima del primo ciclo vero.

## 14.4 CS-1 — Ibrida

Descritta nel piano 10 (10.12) e in 12.4. **A che cosa serve Copilot Studio, se Python resta sul PC?**
- **Togliere i gesti**: A1, A5 e il salvataggio in sequenza con un comando, senza allegati ne' appunti.
- **Piu' utenti e un'interfaccia sola**: analisti e validatore lavorano da Teams, da qualunque posto, senza Python
  sul loro PC.
- **Raccolta notizie nel cloud**: un cloud flow del lunedi'.
- **Fare da prima tappa della CS-2**: Operatore, sotto-agenti, argomenti, flussi e cartella `In_arrivo` sono gli
  stessi. Si butta solo il motore in ascolto, che e' poco codice.

Senza questi bisogni, la CS-1 da sola vale poco: e' l'obiezione dell'utente, ed e' fondata.

**Pro**
- Motore, gate e collaudo identici a oggi: D-10 e D-02 restano come sono.
- Nessun code interpreter in esercizio: D-11 resta.
- Python su un solo PC, invisibile agli utenti.
- Nessun costo a consumo: uso interattivo e flussi con "When an agent calls the flow".
- Rischio tecnico basso: le parti nuove sono orchestrazione e consegna, gia' provate in K0 (B3) e in prova con K6.

**Contro**
- **Un PC esecutore sempre acceso**, con un utente collegato: Excel via COM non gira come servizio. Se e' spento,
  le richieste restano in coda.
- **Dipende dalla sincronizzazione delle library SharePoint sul PC**, fatta dall'app OneDrive: i file restano in
  SharePoint, ma Excel via COM lavora solo su un file locale. Ritardi, copie in conflitto, registro aperto sul web mentre il
  motore scrive. Il piano 10 ha le contromisure (copia di lavoro, attesa della data di modifica), ma restano
  punti di rottura.
- **Due piattaforme da governare**: Copilot Studio e Power Automate da una parte, PC e Python dall'altra. Somma
  i costi di manutenzione di A e della CS-2.
- **Un PC che fa da server**: in una banca e' un tema di governo dell'IT ("shadow IT"), da chiarire prima.
- **Non realizza l'obiettivo dell'utente.**
- Latenza: l'esito arriva dopo la sincronizzazione, da minuti a decine di minuti.

**Impegno**: la parte comune (piano 10, 10.14: circa 6-7 giorni) piu' 13-15 giorni, cioe' circa 4 settimane.

**Quando conviene**: se si vogliono subito Teams e piu' utenti, ma la CS-2 non e' ancora fattibile (K8 o K9 falliti)
o pronta; oppure come tappa verso la CS-2.

## 14.5 CS-2 — Tutto in Copilot Studio

### Come funziona

Il motore di oggi, `esegui_ciclo_locale.py` (circa 3.000 righe), mescola due cose:
- la **logica**: righe da scrivere, regola del radar, applicazione della validazione, baseline, verifiche;
- l'**accesso a Excel**: la classe `Scrittore`, `excel_com.py`, la lettura delle tabelle, i PDF.

I moduli senza Excel (controlli, validatore, radar, schede, precontrollo, allegato di A1: circa 1.700 righe) sono
gia' separati. Nella CS-2 il motore si divide in due strati:

| Strato | Dove gira | Cosa fa | Linguaggio |
|---|---|---|---|
| **Logica** | code interpreter dell'Operatore: uno script unico composto dal pacchetto, come `precontrollo_nfr.txt` (D-70) | dal JSON delle tabelle e dall'output dell'agente calcola esito dei controlli, segnalazioni, stati del radar, righe da scrivere, baseline, testi per A7 | **Python, lo stesso codice del collaudo** |
| **Accesso al registro** | Office Scripts lanciati da agent flow (connettore Excel Online, "Run script") | legge le tabelle e le restituisce come JSON; scrive le righe ricevute; ricontrolla l'integrita' prima di scrivere; copia di sicurezza e archivio con il connettore SharePoint | TypeScript, nuovo |
| **Orchestrazione** | argomenti dell'Operatore | per ogni comando: leggi, calcola, scrivi, rispondi | Copilot Studio |

Un comando come `trimestrale` diventa una sequenza fissa di un argomento:
1. Office Script "Leggi": tabelle in JSON;
2. code interpreter: logica;
3. Office Script "Scrivi": righe nel registro;
4. flussi: archivio e testi per A7;
5. messaggio con l'esito.

Il JSON passa solo nelle variabili e nei flussi, mai nei messaggi.

Altri pezzi:
- **PDF** del report: conversione con un flusso (OneDrive, "Convert file"). Da provare: aree di stampa, fogli
  scelti, altezze delle righe (trappola 107).
- **Schede**: oggi un file creato da Python. Diventano una copia del modello riempita da un Office Script, oppure
  un file prodotto nel code interpreter e salvato da un flusso (da provare).
- **Raccolta notizie**: cloud flow RSS (piano 10).
- **Validazione**: il validatore lavora nella griglia del registro in Excel per il web; "Applica la validazione"
  e' un argomento (Leggi -> logica di `valida` -> Scrivi).

### Il controllo prima della scrittura: il punto debole

Oggi il gate e' codice che nessun modello puo' saltare. Nella CS-2 la logica la esegue il code interpreter
**perche' il modello lo fa**: T1.4 dice che rifiuta di aggirarla, ma non e' una garanzia (trappola 83). E senza un
PC nessuno ricalcola l'impronta in modo indipendente. La proposta e' su tre livelli:

1. **Integrita', deterministica, nell'Office Script "Scrivi".** Prima di scrivere ricontrolla da solo i motivi di
   fermo della D-71:
   - struttura delle righe;
   - ciclo atteso;
   - identificativi esistenti e non duplicati;
   - nessuna riga gia' validata toccata;
   - valori nei domini dei Parametri.

   Se qualcosa non torna, non scrive. Sono poche regole, riscritte in TypeScript, con il Python come oracolo nel
   collaudo differenziale.
2. **Metodo, nel code interpreter.** C3, C5, C9, regola del radar e segnalazioni restano Python, lo stesso codice.
   Ogni riga porta versione dello script e impronta. Se mancano, l'Office Script non scrive.

   Resta un rischio residuo: un modello che inventa righe plausibili con versione e impronta. Si documenta in
   `controlli_e_model_risk.md`.
3. **Validazione umana**, invariata: tutto o niente, con il blocco del ciclo dopo.

Rispetto a oggi il gate scende di un gradino: integrita' sempre garantita, metodo garantito "quasi sempre". Va
deciso apertamente, rivedendo D-02 (niente Office Scripts), D-10 ("scrive solo codice deterministico, dopo i controlli di integrita'") e D-11
(code interpreter negli agenti in esercizio).

### Pro e contro

**Pro**
- **Realizza l'obiettivo dell'utente**: nessuna installazione, nessun PC acceso, tutto nel tenant.
- Piu' utenti, da Teams, senza gesti per agente.
- I controlli restano **lo stesso codice Python** del collaudo: la parte piu' preziosa non si riscrive.
- Office Scripts scrive dentro il vero Excel: formule, tabelle, grafici e convalide del template restano intatti.
  Con openpyxl nel sandbox i circa 10 grafici del template andrebbero persi.
- Nessun costo a consumo, se tutto e' interattivo da utenti Microsoft 365 Copilot. La raccolta pianificata e' un
  cloud flow, che usa la licenza di Power Automate.
- Niente sincronizzazione sul PC nel percorso di scrittura: Office Scripts lavora direttamente sul file in
  SharePoint.

**Contro**
- **Lavoro**: circa 6-8 settimane, stima grezza (14.6). E' la strada piu' lunga.
- **Gate meno forte di oggi** (sopra), con decisioni da rivedere: D-10, D-11, model risk.
- **Due linguaggi**: TypeScript per l'accesso e l'integrita', Python per la logica. Il collaudo si allarga con il
  confronto fra i due; la parte TypeScript si prova anche nel tenant, non solo sul PC del manutentore.
- **Dipende dalle impostazioni del tenant**: Office Scripts e code interpreter abilitati, connettori Excel Online
  e SharePoint ammessi dalle data policy. L'amministratore li puo' spegnere.
- **Affidabilita' del code interpreter su compiti lunghi**: sessioni che scadono, T1.3 andato una volta in
  errore. Uno script unico da qualche centinaio di KB eseguito a ogni comando e' da misurare (K9).
- **Funzioni in anteprima**: il code interpreter sui file strutturati e' in anteprima.
- **Limiti della piattaforma**:
  - Office Scripts: 5 MB per chiamata, 1.600 al giorno;
  - flussi chiamati dall'agente: 100 secondi;
  - i turni lunghi in Teams.
- Pubblicare gli Office Scripts e' un gesto a mano: si caricano nel tenant, non si installano da un pacchetto.
  Va scritto nella guida e controllato con un'impronta, come i prompt.
- Manutenzione: Python resta al manutentore, fuori dalla Banca, per collaudo, prompt e template. Senza collaudo
  automatico ogni cambio di regola sarebbe molto piu' rischioso.

## 14.5-bis Piu' utenti (domanda dell'utente del 09/10)

Oggi il pilota e' a una persona (D-13), e per questo si accetta che chi esegue gli agenti validi anche (D-30). Con
piu' utenti vanno risolte cinque cose, in tutte e tre le strade:

| Tema | A. Tutto sul PC | CS-1. Ibrida | CS-2. Tutto in Copilot Studio |
|---|---|---|---|
| **Accesso** | app e Python su ogni PC; agenti condivisi in Agent Builder | solo Teams: l'Operatore pubblicato per il gruppo della funzione di rischio | come CS-1 |
| **Due scritture insieme** | lucchetto: un file in SharePoint dice chi sta scrivendo; l'app non parte se il lucchetto e' di un altro (12.3) | le serializza il PC esecutore: una richiesta alla volta, in ordine di arrivo | lucchetto nel registro: una riga "in uso da, dalle" che l'Office Script "Scrivi" controlla e mette prima di scrivere, e toglie alla fine; scade dopo un tempo massimo |
| **Chi fa cosa** (analista, validatore) | ruoli in `configurazione.json` su ogni PC | l'identita' arriva da Teams nel flusso; il motore accetta `valida` solo dai validatori in configurazione (10.12, regola 3) | come CS-1, con l'elenco dei validatori nei Parametri del registro, controllato dall'Office Script |
| **Stato del processo** (ciclo in corso, A1 fatto, validato?) | file di stato per periodo, letto dall'app di ognuno | `Stato_processo.json` scritto dal motore e letto dall'Operatore | una tabella di stato nel registro, letta e scritta dagli Office Scripts |
| **Permessi in SharePoint** | chi lancia il motore deve poter scrivere il registro | il registro lo scrive solo l'esecutore; gli altri in sola lettura, tranne il validatore sulla griglia | i flussi possono usare le credenziali dell'utente (serve scrittura sul registro) o una connessione unica di servizio. Con la seconda nessuno scrive a mano fuori dalla griglia, ma l'amministratore la puo' vietare (errore `FlowMakerConnectionBlocked`): da verificare |

Altre conseguenze:
- **La segregazione dei compiti torna possibile.** Con un validatore diverso dall'analista cade il limite di D-30.
  E' un vantaggio di governo che vale soprattutto per CS-1 e CS-2, dove il validatore non ha bisogno di Python.
- **Le conversazioni con gli agenti sono personali.** Quello che conta si deposita in SharePoint (JSON, esiti,
  archivio), con l'identita' di chi ha lanciato, e non nelle chat.
- **Un utente lancia A1, un altro ne chiede il perche' ad A7: si puo', in tutte e tre le strade.** A7 non legge
  la chat di chi ha lanciato A1. Legge `Kernel\Spiegazioni`, che il motore riscrive alla fine di `trimestrale`,
  `valida` e `dismetti` con le motivazioni di A1 per dimensione (D-68), le segnalazioni e le decisioni. Valgono tre
  condizioni:
  - la proposta deve essere gia' scritta: prima di `trimestrale` il JSON e' solo in `In_arrivo`, e A7 spiega il
    ciclo precedente;
  - chi chiede deve poter leggere `Kernel\Spiegazioni`, perche' la knowledge rispetta i permessi dell'utente;
  - i file hanno nomi fissi, cosi' l'indicizzazione e' rapida: in Copilot Studio va verificato quanto ci mette.

  Nella CS-1 e nella CS-2 A7 puo' essere un sotto-agente dell'Operatore lasciato alla scelta del modello, perche'
  legge soltanto e non scrive. E' anche lo strumento naturale di un validatore diverso dall'analista.
- **La griglia di validazione e' nel registro.** Mentre il validatore la compila in Excel per il web, gli Office
  Scripts (CS-2) o il motore (CS-1) non devono scrivere: il lucchetto vale anche per la validazione. In
  alternativa la griglia si sposta in un file a parte per ciclo; e' una scelta da fare con la strada.

Nella strada A la multiutenza costa di piu' (Python su ogni PC, un lucchetto che non impedisce di aprire il file
fuori dall'app). Nella CS-1 e' quasi gratuita, perche' l'esecutore e' uno solo. Nella CS-2 richiede il lucchetto
nel registro e una scelta sui permessi dei flussi.

## 14.5-ter Collaudo nelle tre strade (domanda dell'utente del 09/10)

| Parte | A | CS-1 | CS-2 |
|---|---|---|---|
| Motore, controlli, regole (oggi: prompt, mappa, controlli, fonti, riferimenti in pochi minuti; catena con Excel in circa 60 minuti, o meno con `--mirato`) | sul PC del manutentore, come oggi | **identico, sul PC del manutentore** | la logica Python si', come oggi; l'accesso al registro e' TypeScript e va provato anche nel tenant, con il Python come oracolo |
| Parti nuove in Python (app, motore in ascolto, coda delle richieste) | sul PC, con file e appunti simulati | sul PC: si mettono in `In_arrivo` richieste finte e si controllano esiti, lista bianca, schema, ordine. Pochi secondi, senza Copilot Studio | — |
| Copilot Studio (Operatore, argomenti, sotto-agenti, flussi) | — | **nel tenant**: riquadro di prova, flussi provati da soli, una lista di controllo come quella di K6 dopo ogni modifica; soluzione esportata e conservata nel pacchetto | come CS-1, in piu' gli Office Scripts |
| Confine fra le due parti | — | i file in `In_arrivo` ed `Esiti` hanno uno schema (`schema_richiesta.json`): il PC verifica che il motore accetti solo richieste conformi, il tenant che l'Operatore le produca conformi | i JSON fra flussi, code interpreter e Office Scripts |

Nella CS-1 il collaudo veloce sul PC resta com'e' e copre tutto cio' che decide i valori del registro. La parte
in Copilot Studio non decide valori: chiama agenti, consegna file, mostra esiti. Le sue prove sono di accettazione,
a mano nel tenant, e brevi.

## 14.6 Confronto

| Criterio | A. Tutto sul PC | CS-1. Ibrida | CS-2. Tutto in Copilot Studio |
|---|---|---|---|
| Obiettivo dell'utente (niente Python sul PC) | no | no: un PC esecutore | **si'** |
| Gesti dell'analista per ciclo | 3 per agente, piu' la validazione | un comando, 2-3 pulsanti, la validazione | come CS-1 |
| Chi puo' lavorare | chi ha l'app, al PC | tutti da Teams, se l'esecutore e' acceso | tutti da Teams |
| Piu' utenti e scritture contemporanee (14.5-bis) | lucchetto, Python su ogni PC | serializzate dall'esecutore | lucchetto nel registro, permessi dei flussi da decidere |
| Gate prima della scrittura | deterministico, completo | deterministico, completo | integrita' deterministica, metodo eseguito dal modello |
| Stesso codice in collaudo e in esercizio (D-02) | si' | si' | si' per la logica; no per l'accesso al registro (TypeScript) |
| Decisioni da rivedere | nessuna | D-01 | D-01, D-02, D-10, D-11, model risk |
| Piattaforme da governare | PC e Python | PC e Python, piu' Copilot Studio e Power Automate | Copilot Studio, Power Automate, Office Scripts |
| Punti di rottura principali | PC dell'analista, Excel via COM | PC esecutore, sincronizzazione delle library sul PC | impostazioni del tenant, code interpreter, limiti delle piattaforme |
| Costo a consumo | no | no | no, se interattivo |
| Impegno | 10-14 giorni | circa 4 settimane | circa 6-8 settimane |
| Prove nel tenant prima di decidere | nessuna | K6, K7 | K6, K8, K9, K10 |
| Reversibilita' | — | torna ad A togliendo l'Operatore | torna a CS-1 o ad A: logica e collaudo restano in Python |

Stima della CS-2:

| Lavoro | Giorni |
|---|---|
| separare nel motore la logica (JSON -> JSON) dall'accesso a Excel, con il collaudo intatto | 5-8 |
| Office Scripts "Leggi", "Scrivi" con l'integrita', archivio | 8-12 |
| script unico per il code interpreter (come `prepara_kit.py`), argomenti e flussi per ogni comando | 6-8 |
| PDF, schede, raccolta notizie | 3-4 |
| collaudo differenziale Python/TypeScript, documenti, guida | 5-7 |
| **Totale** | **27-39**, cioe' 6-8 settimane |

## 14.7 Raccomandazione: puntare alla CS-2, a tappe

L'obiettivo dell'utente indica la CS-2, ma oggi poggia su tre cose non provate: Office Scripts nel tenant,
affidabilita' del code interpreter su compiti lunghi, PDF dal cloud. Conviene un percorso in cui ogni tappa serva
comunque e la scelta arrivi con i dati.

| Tappa | Cosa | Serve a | Se va male |
|---|---|---|---|
| 1 | **Prova K6** (protocollo pronto): Operatore, sotto-agente A1, consegna in `In_arrivo` | CS-1 e CS-2 | resta A |
| 2 | **Prova K8**: un flusso lancia un Office Script che legge una tabella del registro e ci scrive una riga | CS-2 | CS-2 impossibile se gli Office Scripts sono spenti: CS-1 o A |
| 3 | **Prova K9**: il code interpreter esegue uno script unico grande, la logica di `trimestrale` su JSON, dieci volte di fila; stesso esito e impronta ogni volta | CS-2 | logica anche in TypeScript (la CS-2 del piano 10, circa 4 settimane in piu') oppure CS-1 |
| 4 | **Decisione A-15** fra le tre strade, con gli esiti di K6, K8, K9 | tutte | — |
| 5 | Separare logica e accesso a Excel nel motore (sul PC del manutentore, collaudo intatto) | CS-2; rende anche A e CS-1 piu' facili da provare | nessun danno: il motore resta uguale fuori |
| 6 | Costruzione della strada scelta; **prova K10** (PDF dal cloud) prima di togliere il PC | strada scelta | il PDF lo fa a mano chi ha Excel, oppure resta un passo sul PC |

Le prove K8 e K9 richiedono poche ore ciascuna e non toccano il registro vero. Fino alla decisione la Banca lavora
come oggi: Agent Builder piu' gli script, che restano la riserva di tutte e tre le strade.

## 14.8 Decisioni toccate

- **A-15** (strada): si chiude fra A, CS-1 e CS-2 dopo K6, K8 e K9.
- **D-01** (solo Agent Builder, senza Copilot Studio ne' Power Automate): gia' rivedibile con A-15; la CS-1 e la
  CS-2 la superano.
- **D-10** (scrive solo lo script dopo i controlli): con la CS-2 diventa "scrive solo codice deterministico (Office
  Script) dopo i controlli di integrita'; i controlli di metodo li esegue il code interpreter".
- **D-11** (agenti senza capability in esercizio): con la CS-2 cade per il code interpreter dell'Operatore.
- **D-02** (parte deterministica in Python sul PC, scrittura via Excel desktop, "niente TypeScript/Office Scripts";
  motivo: un solo linguaggio e lo stesso codice in collaudo e in esercizio): la CS-2 la **contraddice** e va
  sostituita. Il motivo resta vero per la logica, che rimane Python; per l'accesso al registro serve il collaudo
  differenziale. La CS-1 la rispetta, con il PC esecutore al posto del PC dell'analista.
- **D-13** (pilota a una persona): la CS-1 e la CS-2 servono soprattutto se gli utenti diventano piu' di uno.

## 14.9 Le prove che dicono se la CS-1 e' possibile (domanda dell'utente del 09/10)

Riprende le prove K1-K7 di 12.4 e le verifiche V-H..V-P del piano 10 (10.18), con gli esiti noti al 09/10.

**Gia' superate**

| Prova | Esito |
|---|---|
| V-H: Copilot Studio e ruolo di autore | superata il 28/09 (D-44); pubblicazione in Teams e Microsoft 365 Copilot riuscita il 09/10 |
| K2 / V-J: un JSON di A1 da 40-60 KB arriva intero in SharePoint con un agent flow | superata il 09/10: impronta uguale (K0, B3) |
| K1: la knowledge SharePoint funziona nell'agente | il 09/10, secondo l'utente; da confermare nel sotto-agente (K6) |
| V-I, in parte: connettore SharePoint ammesso nei flussi | superata con B3; RSS da verificare solo per la raccolta |

**Da fare nel tenant**

| # | Prova | Che cosa decide | Se va male |
|---|---|---|---|
| 1 | **K6** (protocollo pronto): l'Operatore esegue la sequenza fissa. L'allegato da 50-80 KB arriva al sotto-agente A1 (V-K) e il JSON torna intero; la prova negativa non fa partire niente | il cuore della CS-1 | piani B nel protocollo; se cadono tutti, strada A |
| 2 | **K6.5 in Teams**: la stessa sequenza, con un turno di diversi minuti; nessun errore di dimensione o di tempo | la CS-1 vive in Teams | turno spezzato ("A1 avviato", poi l'esito); come riserva il riquadro di prova, scomodo |
| 3 | **Qualita' di A1** (K4, V-L): doppio run in Copilot Studio e `confronta.py`, confrontati con A1 in Agent Builder sullo stesso input; modello annotato e fisso | che spostare A1 non peggiori le valutazioni (criteri di D-21) | A1 resta in Agent Builder e l'Operatore orchestra gli altri; perde molto del vantaggio |
| 4 | **Piu' utenti**: l'Operatore pubblicato per un gruppo; una seconda persona lo usa; il flusso riceve l'identita' di chi lancia | multiutenza e ruoli (14.5-bis) | si resta a una persona |
| 5 | **A7 in Copilot Studio**: dopo una riscrittura di `Kernel\Spiegazioni`, quanto tempo passa prima che A7 risponda con i dati nuovi | consultazione da parte di altri utenti | A7 resta in Agent Builder, dove i nomi fissi lo rendono rapido |

**Da fare sul PC esecutore in Banca**

Per queste due prove non serve ancora il motore in ascolto: bastano `99_Collaudo/osserva_cartella.py` e un
`.cmd` che lancia due comandi di oggi. Il prototipo del motore in ascolto (1-2 giorni) si fa dopo la decisione.

| # | Prova | Che cosa decide | Se va male |
|---|---|---|---|
| 6 | **K7 / V-P, sincronizzazione**: tempo fra il file scritto dal flusso in `In_arrivo` e il file visto dal PC, e fra l'esito scritto dal PC e l'esito visto in SharePoint (obiettivo: sotto i 2 minuti); copie in conflitto con il registro aperto sul web | tempi e sicurezza della scrittura | "Mantieni sempre su questo dispositivo"; attese dichiarate piu' lunghe; registro chiuso prima di scrivere |
| 7 | **Excel in background**: il motore scrive con lo schermo bloccato, dopo un riavvio, con l'avvio automatico all'accesso a Windows | che il PC possa fare da esecutore senza nessuno davanti | l'esecutore va tenuto sbloccato o si resta alla strada A |

**Domande, non prove**

| # | A chi | Domanda | Se la risposta e' no |
|---|---|---|---|
| 8 | IT | Un PC sempre acceso, con un utente collegato, che fa da esecutore e' ammesso? Di chi e', con quali orari e quali aggiornamenti? | la CS-1 non si fa |
| 9 | DPO / compliance | Le trascrizioni delle conversazioni conservate da Copilot Studio (V-N) e le etichette di riservatezza su `Kernel` e `Analisi_Interne` (V-O) | V-N: strada A; V-O: i file come allegati |

**La CS-1 e' possibile se**:
- passano le prove 1, 2 e 3;
- la 6 sta nei tempi;
- la 7 regge;
- l'IT dice si' alla domanda 8;
- la compliance dice si' alla 9.

Le prove 4 e 5 servono alla multiutenza, che e' il motivo principale per sceglierla. Le prove 1-5 sono anche le
prime della CS-2.

**Protocollo preciso**: `NFR_Emerging_Risk_Agents/09_Copilot_Studio/Prove_CS1.md`, con i testi delle domande, i
comandi e la tabella dei risultati. Nel TODO e' il passo B5, dopo l'allineamento al pacchetto (B1-B4). Le prove
hanno questi nomi: 1 = K6, 2 = K6.5, 3 = K4, 4 = K11, 5 = K12, 6 = K7a, 7 = K7b, 8-9 = D1-D2.

## Fonti (Microsoft Learn, consultate il 09/10/2026)

- [Billing rates and management](https://learn.microsoft.com/en-us/microsoft-copilot-studio/requirements-messages-management): "No charge" per gli utenti Microsoft 365 Copilot; agent flow solo con "When an agent calls the flow"; i cloud flow usano la licenza di Power Automate.
- [Add other agents overview](https://learn.microsoft.com/en-us/microsoft-copilot-studio/authoring-add-other-agents) e [Add a child agent](https://learn.microsoft.com/en-us/microsoft-copilot-studio/add-agent-child-agent): sotto-agenti chiamati da un argomento, input e output.
- [Office Scripts: platform limits](https://learn.microsoft.com/en-us/office/dev/scripts/testing/platform-limits): "Run script" 1.600 chiamate al giorno, 3 ogni 10 secondi, 5 MB, nessuna chiamata esterna da Power Automate.
- [FAQ for code interpreter](https://learn.microsoft.com/microsoft-copilot-studio/faq-code-interpreter): sessioni che scadono sui compiti lunghi, calcolo temporaneo, abilitazione dell'amministratore.
- [Understand error codes](https://learn.microsoft.com/en-us/troubleshoot/power-platform/copilot-studio/authoring/error-codes) e [Format your bot messages](https://learn.microsoft.com/en-us/microsoftteams/platform/bots/how-to/format-your-bot-messages): flussi oltre i 100 secondi, messaggi di Teams fino a circa 100 KB.
