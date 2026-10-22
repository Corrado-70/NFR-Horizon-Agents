# Revisione di Bologna del 21/10/2026 — in sospeso

> **Parcheggiata il 22/10/2026 su indicazione dell'utente.** Le modifiche del 21/10 a `01_Kernel/rubrica_scoring.md`
> (commit 13fa1dc, "Seconda revisione con a Bologna") e a `01_Kernel/tassonomia_nfr.md` (commit bd82006, "Revisione
> con i colleghi a Bologna") sono state tolte dal kernel. Il pacchetto torna alla versione in uso sul PC: Probabilita
> e Prossimita a 5 livelli, otto driver. Questo file NON entra nei prompt e nessuno script lo legge: conserva il testo
> della revisione per riprenderla. Prima di riattivarla vanno fatti gli allineamenti della sezione 3.

## 1. Rubrica di scoring (commit 13fa1dc)

### Impatto: titolo
- In uso: `Impatto — danno se il rischio si manifesta`
- Proposta: `Impatto — danno se il rischio si manifesta ipotizzando sulla capogruppo (si escludono valutazioni di
  impatto su società del gruppo di dimensione inferiore)`

Descrittori invariati.

### Probabilita: da 5 a 6 livelli
Titolo proposto: `Probabilita — plausibilita' per la Banca per una unica cross rischio`.

| Score | In uso | Proposta |
|---|---|---|
| 1 | Remota: solo teorica, nessun caso noto. | Bassa: solo teorica |
| 2 | Improbabile: casi solo in altri settori o paesi, o Banca poco esposta. | Medio Bassa: nessun caso noto |
| 3 | Possibile: casi in altri settori anche non finanziari; Banca esposta. | Media: casi in altri settori anche non finanziari; esposizione banca non nota |
| 4 | Probabile: casi ripetuti in aziende strutturate o banche, o crescita del fenomeno documentata. | Medio Alta: casi in altri settori anche non finanziari; Banca esposta. |
| 5 | Quasi certa: gia' osservato presso istituzioni finanziarie o la loro filiera, anche di fornitori, o fenomeno in rapida accelerazione. | Alta: casi ripetuti in aziende strutturate o banche, o crescita del fenomeno documentata. |
| 6 | — | Molto Alta: osservato presso istituzioni finanziarie o la loro filiera, anche di fornitori, o fenomeno in rapida accelerazione. |

Regola rimasta invariata nella proposta: "4-5 solo se la Banca e' esposta".

### Prossimita: da 5 a 6 livelli

| Score | In uso | Proposta |
|---|---|---|
| 1 | Oltre 3 anni. | Oltre 5 anni. |
| 2 | Da 2 a 3 anni. | Da 3 a 5 anni. |
| 3 | Da 1 a 2 anni. | Da 2 a 3 anni. |
| 4 | Entro 12 mesi. | Da 1 a 2 anni. |
| 5 | In corso o imminente presso la Banca, la sua filiera o aziende ampie e complesse. | Entro 12 mesi. |
| 6 | — | In corso o imminente presso la Banca, la sua filiera o aziende ampie e complesse. |

Regola rimasta invariata nella proposta: "4-5 solo con casi documentati ... o un evento certo; deroga ...".

## 2. Tassonomia (commit bd82006)

### DRV-AI: descrizione estesa
- In uso: `uso interno di modelli, attacchi abilitati da AI.`
- Proposta: `uso interno di modelli, attacchi abilitati da AI, trasformazioni che impattano sul capitale umano e i
  processi interni ed esterni alla banca. Limitata regolamentazione e assenza di meccanismi condivisi di guard
  railing sul tema. Proprietà intellettuale di artefatti generati dall'IA.`

### Tre driver nuovi

| Codice | Driver | Esempi |
|---|---|---|
| DRV-SOV | Sovranità digitale | carenza o limitato controllo su infrastrutture, servizi e dati gestiti dalla banca attraverso fornitori non UE |
| DRV-PQC | Quantum Readiness | evoluzione tecniche crittografia quantistica, migrazione ad algoritmi resistenti a tecniche di decrittazione quantistica |
| DRV-NOR | Frammentazione Normativa | continue nuove normative in parte sovrapposte da molteplici enti nazionali e sovranazionali su temi di pertinenza Non Financial Risk |

## 3. Cosa allineare prima di riattivarla

Il kernel da solo non basta: la revisione tocca schema, script, fogli e prompt.

**Probabilita e Prossimita a 6 livelli**
- Intestazione della rubrica ("Interi 1-5") e regole sui livelli alti:
  - "4-5 solo se la Banca e' esposta";
  - "4-5 solo con casi documentati";
  - "Probabilita 5 o Prossimita 4-5: almeno una fonte di rilevanza 3".
- `schema_output_A1.json` (`punteggio` 1-5) e gli schemi degli altri agenti che riportano gli score.
- Controlli C3-C5 e il loro codice (`07_Senza_Studio/controlli_a5.py`), precontrollo, collaudo.
- Fogli e parametri:
  - Matrice 5x5 e soglie P x I (verde fino a 6, ambra 8-12, rosso da 15; `livelloPxI` 12);
  - area dei cerchi del radar;
  - Delta;
  - validazione (valori interi 1-5).
- Tabella Z di Mosca (`anniProssimita`, 5 valori, Parametri B51:B55): va ridefinita sulle nuove fasce, con un valore
  per il livello 6.
- Regola d'ingresso nel radar (Prossimita almeno 2): con le nuove fasce significa "entro 5 anni", non piu' "entro 3".
- Registro esistente: gli score storici sono su 5 livelli. Serve una regola di conversione, altrimenti il trend e il
  limite di "un punto per ciclo" non sono confrontabili.
- Foglio Metodologia (testo "da Remota a Quasi certa"), guida, documenti commentati, DECISIONI.

**Driver nuovi**
- Enum `driver` di `schema_output_A1.json` (oggi 8 codici).
- Lista `DRIVER` di `03_Excel/genera_dashboard.py`.
- Elenchi a discesa del template.

**Lunghezza dei prompt**
- A1 e' a 7.988 caratteri su 8.000: i driver nuovi e la descrizione estesa di DRV-AI non ci stanno senza accorciare
  altro.
- Dopo ogni modifica rilanciare `02_Agenti/componi_prompt.py`.
