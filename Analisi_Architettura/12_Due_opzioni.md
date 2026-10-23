# 12. Le due opzioni architetturali

> **Esito, 23/10/2026 (D-83)**: l'opzione 1 (12.3, app Python unica sul PC) e' la strada di `main`, con una finestra tkinter, le risposte dagli appunti o da un file e piu' analisti sullo stesso registro (lucchetto e copia di lavoro). Piano a tappe M1-M4 nel TODO, sezione 4; la tappa M1 (motore) e' fatta.

> **Dal 09/10/2026 superato in parte da `14_Tre_strade.md`**: le strade sono tre (A, CS-1, CS-2 senza PC). Le
> descrizioni dell'opzione 1 (12.3) e della CS-1 (12.4) restano valide e il 14 le richiama.

Data: 07/10/2026. Su richiesta dell'utente l'analisi architetturale tiene **due sole opzioni**:

1. un'**app Python unica** sul PC degli utenti, che automatizza tutto cio' che si puo';
2. **Copilot Studio**, esplorato dentro i vincoli che ha oggi in Banca.

Le analisi precedenti (01-11, dal 23/09 al 06/10) sono in `Archivio/`. Restano come storia delle decisioni,
ma non sono piu' opzioni aperte. Dove servono, questo documento ne riprende i fatti: soprattutto la procedura
guidata del documento 10 (parte prima) e la variante Copilot Studio CS-1 (parte seconda e sezione 10.20).

## 12.1 Cosa e' comune alle due opzioni

Nessuna delle due tocca il valore del pacchetto:

- il **kernel** come fonte unica: tassonomia interna (D-74), rubrica, fonti, controlli e guida di scrittura;
- gli **schemi JSON** come contratto fra agenti e scrittura;
- i **controlli deterministici prima della scrittura**: fermo solo per l'integrita', il resto in validazione (D-71);
- la **validazione umana** nella griglia, tutto o niente, con il blocco del ciclo dopo;
- il **registro Excel** con il report al comitato, le schede e la knowledge di A7;
- il **collaudo**: unita', mappa, riferimenti e catena con Excel;
- il **motore** `esegui_ciclo_locale.py`: in tutte e due le opzioni scrive solo lui, perche' il gate deve essere
  codice sempre uguale (D-10).

Cambia **come l'utente arriva al motore e agli agenti**: con un'app sul PC (opzione 1) o con un agente in Teams
che orchestra (opzione 2).

## 12.2 I vincoli della Banca noti oggi

| Vincolo | Stato | Fonte |
|---|---|---|
| Agent Builder non ha API, ne' azioni, ne' scrittura di file | certo | documento 10, 10.2 |
| Agent Builder: code interpreter e immagini non abilitati nel tenant | verificato il 01/10 | D-11 |
| Copilot Studio disponibile | si' | D-44 |
| Copilot Studio: solo l'**esperienza standard** (agenti classici); la nuova esperienza (skill, sandbox Python) consuma crediti | verificato il 05-06/10 | D-70, documento 10, 10.20 |
| Copilot Studio: **knowledge da SharePoint bloccata** (probabile data policy) | verificato il 06/10 | note del 06/10 |
| Code interpreter di Copilot Studio standard: spento di default, va abilitato dall'amministratore; il codice lo scrive il modello | da verificare | 10.20 |
| Power Query abilitato in Excel | si' | 25/09 |
| Macro VBA non bloccate | detto dall'utente il 05/10 | conversazione |
| Python installabile sui PC degli analisti (pywin32, pypac, openpyxl) | in uso dal 24/09 | guida, sezione 0.3 |
| Power Automate (cloud flow con connettori standard) | da verificare | 10.10 |
| Modelli Anthropic in Copilot Studio fuori dall'EU Data Boundary, spenti nella UE | certo | 10.10 |
| Istruzioni di un agente: 8.000 caratteri | certo | tutti i prompt |
| File del registro su OneDrive con il Salvataggio automatico | rischio noto | 10.2 |

## 12.3 Opzione 1 — App Python unica sul PC

**L'idea.** Oggi l'utente usa una dozzina di comandi Python, la guida e Blocco note. Al loro posto un'**app
"NFR"** che si apre con un doppio clic e accompagna ogni processo dall'inizio alla fine. Comprende:

- i cicli trimestrale, settimanale e straordinario;
- la validazione, la manutenzione, le schede e il report;
- la raccolta delle notizie;
- l'installazione e gli aggiornamenti.

Il motore resta quello di oggi; l'app lo chiama.

**Cosa automatizza** (riprende e allarga il documento 10, parte prima, voci AU1-AU6 del TODO):

| Passo di oggi | Con l'app |
|---|---|
| Scrivere i comandi, con `cd`, nomi di file, `--periodo`, `--validatore` | un pulsante per passo; periodo e nomi li sa l'app dallo stato del registro |
| Salvare le risposte degli agenti in Blocco note, UTF-8, con il nome giusto | l'app **ascolta gli appunti**: premuto "Copia" sotto la risposta, estrae il JSON, riconosce l'agente dallo schema, controlla, salva con il nome giusto |
| Preparare e allegare i file per gli agenti | cartella "Da allegare" aperta dall'app, con il file pronto (`Input_A1`, `Input_A6`...); il testo della richiesta e' gia' negli appunti |
| Leggere un FERMATO e riscriverlo all'agente | il messaggio di correzione e' gia' negli appunti: va incollato nella chat dell'agente |
| Copiare `Baseline_corrente.txt` nel Kernel, i prompt nell'archivio | automatico |
| Ricordare dove si e' arrivati (A1 fatto? validato?) | **stato del processo** in un file per periodo: l'app riparte dal passo giusto dopo una chiusura, un errore o un riavvio del PC, e dice chi deve fare cosa |
| Validare (aprire Excel, salvare, chiudere, comando `valida`) | l'app apre il registro sulla griglia, aspetta che sia chiuso, valida; gli errori sono una lista cliccabile con la riga |
| Manutenzione (fase 4 del piano agenti) | una finestra con elenchi a discesa (rischio, campo, valore, motivo, decisore) o le righe preparate da A7, applicate subito |
| Ciclo straordinario | una finestra con i rischi da rivalutare, il motivo e il decisore, poi gli stessi passi del trimestre |
| Raccolta notizie | pianificata dall'app stessa (attivita' di Windows creata all'installazione), con il riepilogo delle fonti non raggiungibili |
| Installazione e aggiornamenti | `installa.cmd`: controlla Python e pacchetti, crea `configurazione.json` chiedendo le cartelle, verifica Excel e rete; a ogni pacchetto nuovo l'app propone `aggiorna-registro` |
| Due analisti sullo stesso registro | **lucchetto** sul registro in SharePoint: l'app impedisce due scritture insieme e dice chi sta lavorando |

**Cosa resta manuale, e perche'.** Agent Builder non ha API: con ogni agente restano **tre gesti**, cioe'
trascinare il file preparato, incollare la richiesta e premere Copia. Restano umane per scelta le decisioni di
validazione, i file portati a mano in `Manuali` e il caricamento delle istruzioni degli agenti quando cambiano.

**Come e' fatta.**

```
Analista ──doppio clic──> NFR.cmd ──> app (Python, interfaccia tkinter della libreria standard)
                                        │  stato del processo, appunti, lucchetto, pianificazione
                                        ▼
                         esegui_ciclo_locale.py (motore, invariato) ──> registro Excel, archivio, PDF, knowledge di A7
```

- **Interfaccia con tkinter** (nella libreria standard di Python: niente da installare). Un'interfaccia web
  locale richiederebbe pacchetti in piu' e una porta aperta sul PC; un eseguibile unico (PyInstaller) e' comodo,
  ma spesso lo bloccano le regole della Banca. Si parte da tkinter e lanciatore `.cmd`.
- Le risposte degli agenti entrano da un **solo ingresso**, `Archivio_Cicli\In_arrivo\` (appunti o file
  trascinato). E' lo stesso punto in cui un giorno potrebbe scrivere un agente: l'app resta valida se si passa
  all'opzione 2.
- **Salvataggio automatico di OneDrive**: il motore lavora su una copia locale e sostituisce il registro solo dopo
  le verifiche (documento 10, fase F5). Cosi' un fermo non lascia righe scritte a meta'.

**Pro**: si puo' fare subito, perche' sta tutto dentro i vincoli noti. Il gate e il collaudo restano identici.
Nessun costo a consumo. E' il prerequisito anche della variante ibrida dell'opzione 2: il motore in ascolto e
l'ingresso unico sono gli stessi.

**Contro**: Python resta su ogni PC che usa l'app, con installazione, aggiornamenti e antivirus. I tre gesti per
agente restano. La raccolta notizie dipende dal proxy del PC.

**Impegno indicativo**: 10-14 giorni con collaudo e documentazione:

- automatismi nel motore, appunti, menu e stato: le fasi F1-F3 del documento 10;
- installazione e robustezza della scrittura: F4-F5;
- le finestre di manutenzione e di straordinario;
- il lucchetto.

**Rischi**:

- l'ascolto degli appunti puo' essere limitato dalle politiche del PC; in quel caso si trascina il file;
- un registro aperto da un collega blocca la scrittura; il lucchetto lo rende visibile, ma non lo impedisce del
  tutto se il collega apre il file fuori dall'app.

## 12.4 Opzione 2 — Copilot Studio, dentro i vincoli della Banca

**L'idea.** Un **Operatore NFR** in Teams, costruito con Copilot Studio nell'esperienza standard. Orchestra gli
agenti come sotto-agenti o strumenti, chiede le conferme con dei pulsanti e consegna le risposte in SharePoint
con un agent flow. Il motore Python resta il gate e gira da solo su un PC "esecutore" che ascolta la cartella di
consegna: e' la variante ibrida **CS-1** del documento 10. Riscrivere il motore in Office Scripts o Power Query
(CS-2, CS-3) costerebbe circa quattro settimane in piu' e perderebbe la regola "stesso codice in collaudo e in
esercizio": non si propone.

**Cosa porterebbe, se i vincoli lo permettono:**

- i tre gesti per agente spariscono: A1 e A5 si concatenano e la risposta finisce in un file senza appunti;
- il trimestre diventa un messaggio in Teams, due o tre pulsanti e la validazione;
- la raccolta notizie esce dal PC: un cloud flow con il connettore RSS;
- gli agent flow chiamati da un agente ("When an agent calls the flow") non consumano crediti per gli utenti con
  licenza Microsoft 365 Copilot (documento 10, 10.10).

**Cosa i vincoli di oggi impediscono o mettono in dubbio:**

| Vincolo | Effetto | Alternativa |
|---|---|---|
| Knowledge da SharePoint bloccata | A1, A3, A4 e A7 non leggono `Analisi_*`, `News_Inbox`, la cartella `Spiegazioni` | knowledge caricata come file nell'agente (manuale, a ogni aggiornamento); oppure un agent flow che legge i file con il connettore SharePoint e passa il testo all'agente, se la data policy non blocca anche il connettore (prova K1) |
| Solo esperienza standard | niente skill: il precontrollo non gira dentro l'agente come script sempre uguale | il precontrollo resta nel motore; con il code interpreter abilitato si puo' provare lo script allegato, misurando se il modello lo esegue cosi' com'e' (prova K5) |
| Power Automate da verificare | senza cloud flow e agent flow l'Operatore non consegna file | senza flussi l'opzione 2 si riduce a un agente in Teams che fa le stesse cose di Agent Builder: vantaggio minimo |
| Modelli disponibili diversi da quelli di Agent Builder | la qualita' di A1 cambia | rimisurarla con il doppio run e `confronta.py`, come per il primo ciclo |
| 8.000 caratteri per istruzioni | uguale ad Agent Builder | i sotto-agenti permettono di dividere A1 se serve |

**Esplorazione a passi.** Ogni prova ha un esito che decide se si va avanti. Riprende il protocollo
`NFR_Emerging_Risk_Agents/09_Copilot_Studio/Prova_con_Copilot_Studio.md`. Il 09/10, dopo la prima tornata di K0, l'utente ha
scelto di procedere con K6 nella forma "argomento a passi fissi": i passi li decide l'argomento, non il modello, e il JSON
passa solo per i flussi, mai nei messaggi. Protocollo in `09_Copilot_Studio/Prova_K6_Operatore.md`; si scrive solo in
`Archivio_Cicli\In_arrivo`.

| Prova | Che cosa | Se riesce | Se no |
|---|---|---|---|
| K1 | Un agent flow legge un file di `Analisi_Interne` con il connettore SharePoint e lo passa all'agente | la knowledge bloccata si aggira con i flussi | knowledge solo per file caricati: l'opzione 2 perde molto per A1, A3, A7 |
| K2 | Un agent flow salva il JSON di un agente in `Archivio_Cicli\In_arrivo` (V-J) | consegna senza appunti | si resta agli appunti, cioe' all'opzione 1 |
| K3 | Pubblicare l'Operatore in Teams per il gruppo della funzione di rischio (V-H) | interfaccia unica per analisti e validatore | si usa il riquadro di prova di Copilot Studio (scomodo) |
| K4 | A1 in Copilot Studio sullo stesso input della prova senza Studio: lunghezza della risposta, qualita' (V-K) | A1 si puo' spostare | A1 resta in Agent Builder; l'Operatore orchestra gli altri |
| K5 | Code interpreter abilitato dall'amministratore, con il precontrollo allegato | correzione dentro l'agente | il precontrollo resta nel motore |
| K6 | Orchestratore con A1 -> precontrollo -> correzione in sequenza, con pulsanti | il giro A1-correzione esce dal PC | sequenza guidata a mano in Teams |
| K7 | Motore in ascolto su `In_arrivo` sul PC esecutore (programma Python, nessuna licenza in piu') | CS-1 completa | il motore lo lancia l'analista dall'app (opzione 1) |

**Pro**: meno gesti per l'utente; niente Python su ogni PC (solo sull'esecutore); Teams come interfaccia
unica; raccolta notizie nel cloud.

**Contro**:

- dipende da vincoli oggi aperti (K1, K2, Power Automate);
- un PC esecutore acceso;
- un altro strumento da governare (ambiente, flussi, pubblicazione);
- con la nuova esperienza, costo a consumo.

**Impegno indicativo**: 13-15 giorni dopo l'opzione 1, perche' il motore in ascolto e l'ingresso unico vengono
da li', e solo se le prove K1, K2 e K7 riescono.

## 12.5 Confronto

| Criterio | Opzione 1: app Python | Opzione 2: Copilot Studio (CS-1) |
|---|---|---|
| Fattibile con i vincoli di oggi | si' | dipende da K1, K2, Power Automate |
| Gesti per agente | tre (trascina, incolla, copia) | nessuno, se K2 e K6 riescono |
| Python sui PC | su ogni PC che usa l'app | solo sull'esecutore |
| Gate e collaudo | identici | identici (il motore e' lo stesso) |
| Costo a consumo | nessuno | nessuno nell'esperienza standard con agent flow chiamati dall'agente; si' con la nuova esperienza o con i flussi pianificati |
| Qualita' degli agenti | quella di Agent Builder, gia' misurata | da rimisurare (K4) |
| Dipendenza da terzi | Python, Excel, OneDrive | Copilot Studio, Power Automate, Teams, oltre al motore |
| Tempi | 10-14 giorni | 13-15 giorni dopo l'opzione 1, piu' le prove |

## 12.6 Raccomandazione

Fare **subito l'opzione 1**: sta nei vincoli di oggi, toglie quasi tutti i passi manuali che non dipendono da
Agent Builder ed e' comunque la base dell'opzione 2, perche' motore, ingresso unico e stato del processo sono
gli stessi.

Esplorare **in parallelo l'opzione 2** con le prove K1-K7: costano poche ore ciascuna e non toccano il registro.
Si decide la decisione aperta **A-15** solo con i loro esiti. Se K1 e K2 riescono, CS-1 si aggiunge sopra l'app
senza buttare niente; se non riescono, l'app e' la soluzione.

In tutte e due le opzioni restano in vigore D-10 (scrive solo il motore) e D-11 (agenti senza code interpreter
in esercizio) finche' non si decide diversamente.
