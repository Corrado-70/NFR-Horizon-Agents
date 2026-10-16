# Analisi dell'architettura — tre strade

**Dal 09/10/2026 le strade sono tre: `14_Tre_strade.md`** (A tutto sul PC, CS-1 ibrida, CS-2 tutto in Copilot
Studio), dopo la direzione dell'utente "nessun Python sul PC, solo via agenti Copilot Studio" e la richiesta di
tenere la CS-1 e confrontare le tre. Raccomandazione: puntare alla CS-2 a tappe, decidendo A-15 sugli esiti delle
prove K6, K8, K9 (14.7). **Dal 14/10 c'e' una quarta variante, la V4** (`16_Report_HTML.md`): report e grafici in HTML generati da Python, registro come file di dati senza formule, Excel solo per la griglia di validazione; vale in tutte e tre le strade e, nella CS-2, sostituirebbe la V2. Il testo qui sotto e' l'indice del 07/10, con due opzioni.

Aggiornato il 07/10/2026, su richiesta dell'utente: l'analisi tiene **due sole opzioni**.

| Opzione | In breve | Documento |
|---|---|---|
| **1. App Python unica sul PC** | un'app che si apre con un doppio clic e guida ogni processo (trimestre, settimana, straordinario, validazione, manutenzione, schede e report, raccolta notizie, installazione); stato del processo con ripresa dopo stop e riavvii; ascolto degli appunti per le risposte degli agenti; lucchetto sul registro. Restano tre gesti per agente (Agent Builder non ha API) | `12_Due_opzioni.md`, sezione 12.3 |
| **2. Copilot Studio nei vincoli della Banca** | un Operatore in Teams (esperienza standard) che orchestra gli agenti e consegna le risposte in SharePoint con gli agent flow; il motore Python resta il gate su un PC esecutore (variante CS-1). Oggi limitato da knowledge SharePoint bloccata, solo esperienza standard, Power Automate da verificare: si esplora con sette prove (K1-K7) | `12_Due_opzioni.md`, sezione 12.4 |

**Raccomandazione** (12.6): fare subito l'opzione 1, che sta nei vincoli di oggi ed e' comunque la base della
2; esplorare la 2 in parallelo con le prove K1-K7 e decidere la A-15 sui loro esiti.

Comune alle due: kernel, schemi, controlli prima della scrittura, validazione umana, registro Excel, collaudo,
motore `esegui_ciclo_locale.py` che resta l'unico a scrivere (D-10).

## Altre analisi aperte

| Documento | Tema | Stato |
|---|---|---|
| `16_Report_HTML.md` | report e grafici in HTML al posto dei fogli di Excel (variante **V4**, valida in tutte e tre le strade): i tre lavori di Excel (archivio, input, vista), file dei dati senza formule scritto con openpyxl, griglia di validazione a parte, pubblicazione (SharePoint, server interno, Teams, PDF), vincoli, confronto con la V2, tappe, prova K14. Anteprima in `16_Anteprima_HTML/` (un report per ciclo, 17 viste e 16 schede), generata da `16_genera_anteprima_html.py`: 118 numeri su 118 uguali a Excel | 14/10/2026: proposta la decisione A-16; si decide dopo K14 e la tappa T2 |
| `15_CS2_approfondita.md` | CS-2 approfondita: parti del Python che non girano in Copilot Studio; che cosa offrono code interpreter, prompt, Office Scripts, connettori e flussi; ruolo dell'XML; varianti V1 (Office Scripts), V2 ("Python decide, Excel esegue") e V3 (XML del file); cancello, costi, vincoli, percorso dopo la CS-1, prove K8, K9, K10, K13 | 11/10/2026: raccomandata la V2, a tappe; si decide dopo le prove |
| `14_Tre_strade.md` | tre strade per l'automazione: A, CS-1, CS-2 senza PC (code interpreter per la logica Python, Office Scripts per il registro); pro e contro, confronto, gate, stima, tappe | 09/10/2026: in attesa delle prove K6, K8, K9 e della decisione A-15 |
| `13_Scala_unica.md` | scala unica per rischi e fenomeni in osservazione (TODO P10): opzione A, la lista sulla scala della rubrica; opzione B, un registro con due stati e una regola calcolata | 08/10/2026: scelta la B dall'utente, anteprima approvata, fatta la sera (D-79, registro unico, struttura 2026-10-09; 13.8) |

## Archivio

Le analisi dal 23/09 al 06/10 sono in `Archivio/`, come storia delle decisioni: architettura attuale e
alternative (01-04), piano di rigenerazione (05), agente operativo R2 (06), piano senza Python (07), confronto
con lo Horizon Scanning fatto a mano (08), proposta grafica e anteprime del registro (09), piano di
automazione con l'opzione Copilot Studio (10), semplificazione dello scoring (11). L'indice di allora, con le
note datate, e' `Archivio/00_LEGGIMI_analisi_fino_al_2026-10-07.md`. Le decisioni prese su quelle analisi
restano in `NFR_Emerging_Risk_Agents/04_Riferimenti/DECISIONI.md`; i riferimenti dei documenti del pacchetto
puntano ai file in `Archivio/`.
