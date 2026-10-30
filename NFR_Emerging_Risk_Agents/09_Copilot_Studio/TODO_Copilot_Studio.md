# TODO Copilot Studio — registro vivo del ramo `copilot-studio-pieno`

**Su questo ramo si parte da qui.** Questo file dice a che punto e' la versione tutta in Copilot Studio (D-82) e che
cosa viene dopo: per riprendere basta la sezione 0.

**Aggiornato al 30/10/2026.**

Contiene solo le voci di questo ramo. Le voci comuni (kernel, prompt, motore, regole, collaudo) stanno in
`NFR_Emerging_Risk_Agents/TODO_possibili_sviluppi.md`, che arriva da `main` con il merge: su questo ramo non si modifica.
Se serve una modifica comune ci si ferma e si fa prima su `main`.

Come si tiene vivo, a ogni intervento:
1. all'inizio si legge la sezione 0; alla fine si aggiornano la data, il quadro, gli impegni in sospeso e il prossimo
   passo;
2. una voce finita esce dalla sua sezione e diventa una riga di "Fatto" (sezione 5); una voce che non serve piu'
   diventa una riga di "Superate", con il motivo;
3. una prova fatta si annota lo stesso giorno: qui lo stato, in `Copilot_Studio_pieno.md` (sezione 9) l'esito con i
   numeri;
4. qui non si copia cio' che ha gia' un posto: progetto e passi di costruzione in `Copilot_Studio_pieno.md`, decisioni in
   `04_Riferimenti/DECISIONI.md`, racconto nell'HANDOFF.

## 0. Da dove si riparte

| Quadro | |
|---|---|
| Obiettivo | versione del processo tutta nel tenant, senza Python sul PC (D-82); la scelta per l'esercizio fra le due versioni si fa sui risultati delle prove T0-T8 (D-83) |
| Strada del motore | **da capire** (utente, 30/10; D-91). V1 (regole in TypeScript, eseguite da Office Scripts lanciati dai flussi) e' l'ipotesi di lavoro del 23/10, non ancora una scelta definitiva. V2 e F2 sono cadute con T4.1 (K9): il code interpreter dei prompt non esegue il nostro codice |
| Agenti | Copilot Studio o Agent Builder si scelgono dopo, con il confronto di qualita': il motore e' lo stesso nei due casi |
| Allineamento a `main` | fino a D-91 (30/10), con `genera_CS.py` |
| Motore V1 | non iniziato: nel ramo ci sono solo gli script delle prove (`Da_caricare/prove`). Stima 8-11 settimane, da misurare |

**In sospeso**:

| # | Cosa | Stato |
|---|---|---|
| 1 | Causa dei 6 errori di formula nella colonna `Settimana` di NewsLog (T5.2): serve la riga `dettaglio_errori_prima` dello script nuovo, eseguito a mano e dal flusso. Se ci sono anche a mano e' un difetto del registro, da correggere su `main` | da fare |

**Prossimo passo**: la scelta della strada del motore (sezione 1-bis). Node.js e' installato su questo PC
(v24, solo sviluppo), se serve la misura di V1.

**Da tenere presente**: le scale a 6 livelli (A-19, TODO comune, P15) sono una modifica comune: nascono su `main` e
arrivano qui con il merge. Cambiano le soglie e i numeri ammessi che il motore V1 deve tradurre: conviene fare il
precontrollo in TypeScript sulle regole nuove, o mettere in conto di rifarne quella parte.

## 1. Ordine di lavoro

| Passo | Voci | Perche' qui | Stato |
|---|---|---|---|
| 1 | **T0.3, T0.4**: risposte dell'IT (costi, connettori) e cartelle | prerequisiti: un no dell'IT cambia il resto | da fare |
| 2 | **Scelta della strada del motore** (sezione 1-bis). Se resta V1, la prima misura: scheletro (logica pura in moduli TypeScript che girano sotto Node e nello script, adattatore sottile per le tabelle di Excel, generatore del file unico per Office Scripts); il precontrollo in TypeScript; collaudo che esegue TypeScript e Python sugli stessi casi di `99_Collaudo/dati` e pretende esiti identici | tutto il resto dipende da qui; la misura dice il costo vero della traduzione | da fare |
| 3 | **T1-T3**: agente, flussi, A1 e A8 come sotto-agenti, correzione dai file | la spina dorsale della versione | da fare |
| 4 | **Il motore** sulla strada scelta; con V1 anche **T5.3** concorrenza | e' il lavoro piu' grande del ramo | da fare |
| 5 | **T6-T8**: A5, A3 e Raccolta_notizie, A6, Teams, A4 e A7 | completano i comandi | da fare |
| 6 | **Confronto di qualita'** con Agent Builder (K4, sezione 3), parere della DPO, decisioni della sezione 4 | serve alla scelta per l'esercizio | da fare |

## 1-bis. La strada del motore: da capire

Su `main` il motore e' Python e resta tale (D-91): qualunque strada qui va confrontata con quel punto fermo.

| Strada | Che cosa vuol dire | Pro | Contro |
|---|---|---|---|
| **V1** | regole del motore tradotte in TypeScript, eseguite da Office Scripts | niente Python sul PC; T5 e K8-bis riuscite | 8-11 settimane stimate; **due motori da tenere allineati** con `main`: ogni regola nuova (per esempio le scale a 6 livelli) va fatta due volte, con un collaudo incrociato |
| **CS-1b** | agenti e flussi nel tenant, motore Python su un PC esecutore | un motore solo, quello di `main` | un PC da tenere acceso; contro la direzione "niente Python sul PC" (09/10) |
| **Agenti in Copilot Studio, app Python** | gli agenti di questo ramo con l'app di `main`, che accetta gia' le risposte di Copilot Studio | un motore solo, lavoro minimo; serve il confronto di qualita' degli agenti | Python resta sul PC dell'analista: non e' la versione "tutta nel tenant" |

V2, F2 e F1 non sono piu' strade: tutte e tre dipendevano dal Python eseguito nel code interpreter, negativa in T4.1.

**Fatto quando**: la strada e' scelta dall'utente, con il motivo, in questa sezione e in `Copilot_Studio_pieno.md`,
sezione 7. Per scegliere servono: la misura di V1 (passo 2 dell'ordine), le risposte dell'IT (T0.3) e quanto pesa avere
due motori.

## 2. Prove T0-T8

Passi e criteri in `Copilot_Studio_pieno.md`, sezione 7; esiti con i numeri nella sezione 9.

| Prova | Stato |
|---|---|
| T0 Prerequisiti | **T0.1 e T0.2 si'** (23/10); T0.3 (mail all'IT, testo pronto) e T0.4 (cartelle) da fare |
| T1 Fondamenta: agente, variabili, flussi | da fare |
| T2 A1 e A8 come sotto-agenti | da fare |
| T3 Correzione dai file | da fare |
| T4 K9, motore nel code interpreter | **negativa** (T4.1, 23/10): T4.2 e T4.3 non applicabili |
| T5 K8, Office Scripts sul registro | **T5.1, T5.2 e K8-bis riuscite** (23/10); T5.3 concorrenza rinviata all'implementazione; resta la causa degli errori (sezione 0) |
| T6 Gli altri agenti | da fare |
| T7 Teams | da fare |
| T8 A4 e A7 | da fare |

## 3. Prove della CS-1 ereditate da `main` (B5)

Su `main` sono chiuse dal 30/10 (A-15 chiusa da D-83). Protocollo in `Prove_CS1.md`, con i tempi, i testi e la tabella
dei risultati. I codici B5.x restano quelli citati nei documenti.

| # | Prova | Con la strada V1 | Stato |
|---|---|---|---|
| B5.1 | **D1 e D2**: domande all'IT e alla compliance | D1 e' sostituita da T0.3; resta **D2**, il parere su trascrizioni di Copilot Studio ed etichette di riservatezza | D2 da fare |
| B5.2 | Preparazione: registro di prova, due run di A1 in Agent Builder (`A1_AB_run1.json`, `A1_AB_run2.json`) | serve come base di confronto di K4 | da fare |
| B5.4 | **K4** qualita' di A1 in Copilot Studio: `confronta.py` AB/AB, CS/CS, AB/CS | resta: e' il confronto di qualita' (D-21) | da fare |
| B5.5 | **K11** piu' utenti, con un collega: identita' nel flusso, connessione dei flussi, lancio simultaneo, trascrizioni | resta: multiutenza | da fare |
| B5.6 | **K12** A7 come sotto-agente | resta, con T8 | da fare |
| B5.7 | **K7a** sincronizzazione SharePoint <-> PC | **da rivalutare**: senza PC esecutore serve solo per chi tiene il registro sincronizzato | da decidere |
| B5.8 | **K7b** Excel senza nessuno davanti | **da rivalutare**: V1 non ha un PC esecutore | da decidere |

Le voci B5.3 (K6) e B5.9 (K0 ripetuta) sono fra le superate (sezione 5).

## 4. Da decidere

Da `Copilot_Studio_pieno.md`, sezione 10:
- **D-02** (niente Office Scripts), **D-01** (niente Copilot Studio e Power Automate), **D-10** (JSON portato a mano allo
  script) e **D-11** (niente capability) cambiano per questa versione: vanno formalizzate;
- **governance** (`04_Riferimenti/controlli_e_model_risk.md`) della versione tutta nel tenant;
- **trascrizioni** e dati nelle conversazioni: parere della DPO (D2).

## 5. Fatto e superate

| Voce | Cosa | Quando | Dove vive |
|---|---|---|---|
| K0, K6, K6-bis, K6-ter | Prove di fattibilita': cio' che funziona e cio' che non funziona | 09-22/10 | `Prova_K6_Operatore.md`, `Prova_con_Copilot_Studio.md`; tabella in testa a `Copilot_Studio_pieno.md` |
| Progetto | Agente con un argomento per comando, comunicazione via file in SharePoint e variabili globali, flusso `NFR_Motore` | 23/10 | D-82; `Copilot_Studio_pieno.md`, sezioni 1-6 |
| Strada del motore | T0.1, T0.2, T4.1, T5.1, T5.2, K8-bis e scelta di V1 | 23/10 | HANDOFF, 2-tretricesies; `Copilot_Studio_pieno.md`, sezione 9 |

| Superata | Perche' | Dove resta |
|---|---|---|
| B5.3 K6 Operatore a passi fissi | sostituita dalle prove T0-T8 | `Prova_K6_Operatore.md` |
| B5.9 K0 ripetuta | sostituita dalle prove T0-T8 | `Prova_con_Copilot_Studio.md` |
| B5.10 K14 report HTML | A-16 chiusa da D-83: niente variante V4 | `Analisi_Architettura/16_Report_HTML.md`, 16.9 |
| V2, F2, F1 e T4.2, T4.3 | T4.1 negativa: la sandbox del code interpreter non esegue il nostro codice | `Copilot_Studio_pieno.md`, sezioni 6 e 9 |
