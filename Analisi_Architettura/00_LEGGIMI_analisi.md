# Analisi dell'architettura — due opzioni

Aggiornato il 07/10/2026, su richiesta dell'utente: l'analisi tiene **due sole opzioni**.

| Opzione | In breve | Documento |
|---|---|---|
| **1. App Python unica sul PC** | un'app che si apre con un doppio clic e guida ogni processo (trimestre, settimana, straordinario, validazione, manutenzione, schede e report, raccolta notizie, installazione); stato del processo con ripresa dopo stop e riavvii; ascolto degli appunti per le risposte degli agenti; lucchetto sul registro. Restano tre gesti per agente (Agent Builder non ha API) | `12_Due_opzioni.md`, sezione 12.3 |
| **2. Copilot Studio nei vincoli della Banca** | un Operatore in Teams (esperienza standard) che orchestra gli agenti e consegna le risposte in SharePoint con gli agent flow; il motore Python resta il gate su un PC esecutore (variante CS-1). Oggi limitato da knowledge SharePoint bloccata, solo esperienza standard, Power Automate da verificare: si esplora con sette prove (K1-K7) | `12_Due_opzioni.md`, sezione 12.4 |

**Raccomandazione** (12.6): fare subito l'opzione 1, che sta nei vincoli di oggi ed e' comunque la base della
2; esplorare la 2 in parallelo con le prove K1-K7 e decidere la A-15 sui loro esiti.

Comune alle due: kernel, schemi, controlli prima della scrittura, validazione umana, registro Excel, collaudo,
motore `esegui_ciclo_locale.py` che resta l'unico a scrivere (D-10).

## Archivio

Le analisi dal 23/09 al 06/10 sono in `Archivio/`, come storia delle decisioni: architettura attuale e
alternative (01-04), piano di rigenerazione (05), agente operativo R2 (06), piano senza Python (07), confronto
con lo Horizon Scanning fatto a mano (08), proposta grafica e anteprime del registro (09), piano di
automazione con l'opzione Copilot Studio (10), semplificazione dello scoring (11). L'indice di allora, con le
note datate, e' `Archivio/00_LEGGIMI_analisi_fino_al_2026-10-07.md`. Le decisioni prese su quelle analisi
restano in `NFR_Emerging_Risk_Agents/08_Deploy/DECISIONI.md`; i riferimenti dei documenti del pacchetto
puntano ai file in `Archivio/`.
