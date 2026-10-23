# SharePoint — sito, library e liste

Un sito dedicato (es. `NFR-Emerging-Risk`) con **sette library** e **tre liste**.
Le tabelle dati del workbook sono gia' storiche (RiskRegister, Azioni, KRI:
una riga per soggetto per ciclo, solo in coda); le liste ne sono una copia
interrogabile da SharePoint, caricata da Power Automate.

> Le colonne delle liste NON si decidono qui: derivano dalle tabelle del
> workbook secondo `01_Kernel/mappatura_campi.json` (sezione
> `liste_sharepoint`). Se si cambia una colonna, si cambia la mappa, si
> aggiorna questo documento e si rilancia `99_Collaudo/test_mappatura.py`, che
> segnala ogni colonna mancante qui.

## Library

| Library | Contenuto | Chi scrive | Chi legge |
|---|---|---|---|
| `Kernel` | tassonomia, rubrica, `fonti.md`, `controlli_A5.md` e `guida_scrittura_A1.md` (allegato di A1, D-69), gli schemi JSON, `mappatura_campi.json`, template master, `Baseline_corrente.json` e la sua copia `.txt`; la cartella `Spiegazioni` (`Ciclo.txt` e `Rischio_01..20.txt`, uno per posto dell'anagrafica, D-72) | manutentore del kernel; lo script di campo (baseline e cartella `Spiegazioni`) | agenti (knowledge di A3 e A4: la `.txt`; di A7: la cartella `Spiegazioni`), script di campo |
| `Analisi_Interne` | SOLO documenti della Banca su se stessa: report di audit, test dei controlli, incident report, report di funzione; sottocartelle come negli indirizzi delle fonti `share` di tipo interno in `fonti.md` (FNT-30..33) | funzioni aziendali | A1, A3 (knowledge) |
| `Analisi_Esterne` | report di settore, analisi di terzi, database di perdite di consorzio (es. ORX): materiale esterno salvato per uso ripetuto, anche se non ha un feed proprio; FNT-35 in `fonti.md`. Separata da `Analisi_Interne` apposta: un documento esterno qui non deve mai essere scambiato per uno della Banca (D-45) | analisti | A1, A3 (knowledge) |
| `News_Inbox` | una cartella per settimana (`<lunedi'>/`): `Raccolta_<data>.txt` scritto da W0 dai feed dell'elenco fonti, e `Manuali/` per i file salvati dagli analisti; `_visti.json` alla radice (link gia' raccolti) | W0 (`raccogli_notizie.py`), analisti | A1, A3 (knowledge) |
| `Report_Trimestrali` | workbook vivo `NFR_Registro.xlsx` (registro e report in un solo file, D-39). Il PDF del report al comitato lo scrive il comando `report` in `Archivio_Cicli/Cicli/<ciclo>/Report_comitato_<ciclo>.pdf` (D-62): da li' si condivide | scrittura A2, analisti | comitato, funzione di rischio |
| `Report_Settimanali` | **non usata nella variante senza Copilot Studio** (`07_Senza_Studio`): l'output della settimana va in `Archivio_Cicli/Settimane/<lunedi'>/`, la sintesi di A3 e i flag nel foglio Sintesi_Settimane del registro (D-66) e la vista settimanale e' nel registro (foglio Notizie, segnali netti del Registro). Serviva al disegno con Copilot Studio, dove un flusso vi salvava la sintesi di A3; si puo' non creare | — | — |
| `Archivio_Cicli` | `Baseline_corrente.json` e gli allegati degli agenti `Input_<agente>` (D-69, D-84: `Input_A1_<ciclo>.txt`, `Input_A8_<periodo>.txt`, `Input_A3_A4.txt`, `Input_A5_<ciclo>.txt`); `In_arrivo/` (risposte degli agenti dall'app), `Pareri/` (A4), `Log/` (comandi lanciati dall'app), `_Lucchetto/` (chi scrive nel registro, D-83); `Cicli/<ciclo>/` con l'Excel di output `NFR_Registro_<ciclo>.xlsx` e quello validato, output di A1 e A5, baseline usata, esito dei controlli, `Righe_liste_<ciclo>.json`, `Validazione_<ciclo>.json`, l'ultimo messaggio per A1 `Correzione_A1_<ciclo>.txt` (precontrollo o `trimestrale` fermato, D-71), **testo dei prompt in uso** (copiato a mano), e una sottocartella per ogni tentativo, anche fermato; `Settimane/<lunedi'>/` con l'Excel di output della settimana e l'output di A3; `Dismissioni/` (un atto per rischio dismesso); `Backup/` | script (A2); l'analista per i prompt | analisti, audit, model risk |

Impostazioni: controllo versione attivo su tutte le library (e' la traccia di
ogni modifica al workbook e al kernel); `Kernel` e `Archivio_Cicli` in sola
lettura per chi non e' manutentore; A5 **non** ha accesso a `News_Inbox`
(riceve solo l'output di A1 e la baseline).

## Liste

Tutte e tre sono **storiche**: una riga per soggetto per ciclo, mai
aggiornate in sostituzione, come le tabelle del workbook da cui derivano
(senza le colonne formula). Servono a chi interroga SharePoint senza aprire
il workbook, e come seconda copia della storia.

Le righe da caricare le produce lo script (`esegui_ciclo_locale.py`) nel
file `Righe_liste_<ciclo>.json`, gia' complete dei campi derivati (KRI_ID
assegnati, Owner, stato delle azioni). La scrittura trimestrale lo crea con i
valori ancora da validare; il comando `valida` lo **riscrive con i valori
validati** (compresi `Approvato_Da`, `Validazione`, `Data_Validazione`). Si
carica **dopo la validazione**: chi carica (Power Automate, o l'analista nella
variante locale) copia i valori, senza logica propria. Una dismissione
(comando `dismetti`) cambia `In_Vigore` dei KRI e `Stato` delle azioni del
ciclo corrente: se le liste sono gia' caricate, aggiornare quelle righe (l'atto
in `Archivio_Cicli/Dismissioni/` elenca KRI e azioni toccati).

### RiskRegister_Storico

Una riga per rischio per ciclo. Chiave logica: `Ciclo` + `ID_Rischio`.

| Colonna | Tipo | Note |
|---|---|---|
| `Ciclo` | testo | formato AAAAQn |
| `Data_Riferimento` | data | ultimo giorno del trimestre |
| `ID_Rischio` | testo | NFR-nn, stabile per sempre |
| `Nome` | testo | |
| `Event_Type` | scelta | categoria della tassonomia interna: 9.1 ... 9.13, FP (D-74) |
| `Driver` | testo | codici separati da virgola |
| `Impatto` | numero intero | 1-5 (era Severity, D-57) |
| `Velocity` | numero intero | 1-5, o vuota = non valutata (D-50) |
| `Prossimita` | numero intero | 1-5 |
| `Probabilita` | numero intero | 1-5, plausibilita' per la Banca (D-52); nel composito; area del Radar_Mosca |
| `Anni_Adeguamento` | numero | 0-30 o vuoto: stima di A1 del ciclo (D-60); il valore validato va nell'anagrafica |
| `Esito` | scelta | Confermato / Variato / Nuovo (calcolato dallo script, D-51) |
| `Descrizione` | testo multiriga | |
| `Razionale` | testo multiriga | |
| `Variazioni` | testo multiriga | array JSON serializzato |
| `Fonti` | testo multiriga | array JSON serializzato, con la rilevanza 1-3 di ogni fonte (D-58) |
| `Rilievi` | testo multiriga | segnalazioni di A5 e dei controlli sul rischio, una per riga; DA MOTIVARE = la validazione chiede una Motivazione (D-71; BLOCCANTE SUPERATO nei registri fino al 2026-10-02) |
| `Owner` | testo | funzione, dall'anagrafica |
| `Data_Scrittura` | data | |
| `Approvato_Da` | testo | **vuoto = ciclo non validato**; lo scrive il comando `valida` (chi ha validato) |
| `Validazione` | scelta | Da validare / Accettato / Rettificato |
| `Data_Validazione` | data | quando e' stato validato |
| `Periodo_Valutazione` | testo | periodo in cui il rischio e' stato valutato: il Ciclo, o per un rischio riportato (non rivalutato in un ciclo straordinario, D-75; in osservazione e non toccato da A1, D-79) il periodo da cui la riga viene |
| `Stato` | scelta | registro unico (D-79): Radar / Radar, in uscita / Osservazione / Dismesso |
| `Motivo_Stato` | testo multiriga | perche' quello stato (soglie di Prossimita e Probabilita, eccezione, capienza) |
| `Movimento` | scelta | Entrato / Uscito dal radar nel ciclo, o vuoto |
| `Decisione_Stato` | scelta | Automatico / Radar / Osservazione: la decisione del validatore |
| `Orizzonte_Anni` | numero intero | 1-30 o vuoto: per un rischio in osservazione, gli anni stimati da A1 |
| `Segnale_Avvicinamento` | testo multiriga | per un rischio in osservazione: il fatto che lo porterebbe nel radar |

I rischi in osservazione stanno nella stessa lista con `Stato` = Osservazione
(D-79): una vista filtrata su `Stato` separa il radar dall'osservazione.

Non c'e' lo score composito: e' una formula del workbook. Chi interroga la
lista lo ricalcola con i pesi di `rubrica_scoring.md` (D-50: se la Velocity e' vuota
i pesi si ridistribuiscono sulle altre tre dimensioni).

### Azioni_Storico

Una riga per azione proposta. Chiave: `ID_Azione`.

| Colonna | Tipo | Note |
|---|---|---|
| `Ciclo` | testo | |
| `ID_Rischio` | testo | |
| `ID_Azione` | testo | `<ciclo>-<ID_Rischio>-A<n>` |
| `Descrizione` | testo multiriga | |
| `Owner` | testo | funzione, mai persona |
| `Orizzonte` | scelta | 3 mesi / 6 mesi / 12 mesi |
| `Razionale` | testo multiriga | |
| `Stato` | scelta | Proposta — da valutare / Approvata / Respinta / In corso / Completata / Annullata (rischio dismesso) |
| `Data_Decisione` | data | vuota finche' non deliberata |
| `Decisa_Da` | testo | vuoto finche' non deliberata |
| `Validazione` | scelta | Da validare / Accettato / Rettificato / Respinto |

### KRI_Storico

Una riga per KRI per ciclo, identica alla tabella KRI del workbook. Chiave
logica: `Ciclo` + `KRI_ID`.

| Colonna | Tipo | Note |
|---|---|---|
| `Ciclo` | testo | ciclo della fotografia |
| `KRI_ID` | testo | NFR-nn-Kn, stabile per sempre, mai riusato |
| `ID_Rischio` | testo | |
| `Nome` | testo | |
| `Tipo` | scelta | Esposizione / Evoluzione: uno per tipo per rischio (D-64); vuoto nei KRI scritti prima del 01/10/2026 |
| `Unita` | testo | |
| `Fonte_Dati` | testo | |
| `Soglia_Attenzione` | numero | vuota finche' la Banca non la fissa (D-53) |
| `Soglia_Allerta` | numero | >= Soglia_Attenzione; vuota insieme a lei |
| `Valore_Corrente` | numero | valore rilevato in QUESTO ciclo; vuoto se non rilevato, **mai** il valore del ciclo prima |
| `Data_Rilevazione` | data | vuota se il valore e' vuoto |
| `Fonte_Rilevazione` | testo | |
| `Nota_Rilevazione` | testo | |
| `In_Vigore` | scelta | Sì / No (No = sostituito in questo ciclo) |
| `Ciclo_Definizione` | testo | ciclo in cui il KRI e' nato |
| `Ciclo_Aggiornamento` | testo | ultimo ciclo che ne ha rivisto la definizione |
| `Razionale` | testo multiriga | |
| `Validazione` | scelta | Da validare / Accettato / Rettificato / Respinto (Respinto = In_Vigore No) |

## Validazioni (nessuna lista)

La base dati delle validazioni e' la tabella `tblValidazione` del workbook
(foglio dati Storico_Validazioni, dal 02/10/2026): una riga per ogni campo
proposto da un agente, con la proposta, la decisione umana, il valore validato
e il motivo. La scrive il comando `valida` da cio' che il validatore ha deciso
nella griglia del foglio Validazione, una riga per oggetto (D-67). Ogni validazione
ne archivia una copia in `Archivio_Cicli/Cicli/<ciclo>/Validazione_<ciclo>.json`
(o `Settimane/<lunedi'>/`). E' la base per l'apprendimento futuro degli agenti:
le righe "Rettificato" sono coppie proposta -> correzione con motivazione.

## Variante senza Copilot Studio

Senza Power Automate nessuno carica le liste e lo script di campo non usa
API: le liste si possono non creare. La storia completa sta comunque nel
workbook vivo, le cui tabelle dati sono tutte storiche (KRI compreso), con la
cronologia versioni di SharePoint; in piu' ci sono gli Excel di output
congelati e i file per ciclo in `Archivio_Cicli`
(`Righe_liste_<ciclo>.json`, baseline, esiti) e i backup dello script.
