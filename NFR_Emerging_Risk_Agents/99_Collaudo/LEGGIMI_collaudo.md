# Collaudo a secco

Verifica gli artefatti prima del deploy, senza tenant. Non sostituisce il test
in ambiente (`04_Riferimenti/workflow.md`, "Test in ambiente"): non include il retrieval dalle
knowledge source ne' la variabilita' dell'agente Copilot reale.

## Come si esegue

```
python 99_Collaudo/esegui_collaudo.py               # tutto (serve Excel desktop): catena in 3 processi, circa 40 minuti
python 99_Collaudo/esegui_collaudo.py --mirato      # la catena solo se e' cambiato un file che la riguarda
python 99_Collaudo/esegui_collaudo.py --senza-excel # tutto tranne la catena (pochi secondi)
python 99_Collaudo/esegui_collaudo.py --in-sequenza # la catena con i gruppi uno dopo l'altro (circa 50 minuti)
python 99_Collaudo/esegui_collaudo.py -v            # mostra anche le verifiche superate
python 99_Collaudo/run_catena.py --passo riapertura # un gruppo della catena solo (nomi: run_catena.py, in testa)
```

**Collaudo mirato** (M1, 08/10/2026). Dopo un collaudo completo e verde, `esegui_collaudo.py` scrive le impronte dei
file che la catena mette alla prova:
- script di campo, generatore e template;
- kernel;
- codice e dati del collaudo.

Le impronte stanno in `%LOCALAPPDATA%\NFR_collaudo`, fuori dal pacchetto. `--mirato` lancia la catena solo se uno di
quei file e' cambiato. Per prompt, guida e documenti bastano le suite veloci, che girano comunque.

Da lanciare dopo **ogni** modifica a kernel, schemi, mappa, prompt, generatore
o script di campo. Requisiti: Python 3.10+, `openpyxl` (per leggere il
template), `pywin32` ed Excel desktop per la catena. Per collaudare un
template costruito a mano: variabile d'ambiente `NFR_TEMPLATE=<percorso>`.

## Cosa verifica

| File | Verifica | Excel |
|---|---|---|
| `02_Agenti/componi_prompt.py --verifica` | prompt allineati al kernel e sotto gli 8.000 caratteri | no |
| `test_mappatura.py` | ogni campo degli schemi ha una destinazione, ogni colonna una sorgente e un significato; tabelle del template = mappa; nomi `VG_...` della griglia del foglio Validazione per ogni campo validabile; liste documentate | no |
| `test_controlli.py` | validatore su payload conformi e difettosi (anche i campi tolti il 30/09: gap_controlli, esito, da/a, dimensione); controlli di A5 su un ciclo pulito e su un difetto per controllo, piu' cio' che non deve fermare (Velocity da non valutata a un valore, KRI non riletto); A5 facoltativo e Bloccanti di A5 "Da motivare" in `combina`, C3, date di C5 e soglie di C9 che non fermano (D-71); D-72: `fenomeni_non_censiti` nello schema di A1 (facoltativo, motivo fuori elenco rifiutato), testi della knowledge di A7 (file del rischio e `Ciclo.txt`), file dei rischi tolti, cartella nella library Kernel o in quella di uscita; D-79: registro unico (la regola di `radar.py`: soglie, eccezioni, capienza, uscita in due cicli, massimo delle viste; lo stato previsto dai controlli sui dati di prova; un difetto per regola sui rischi in osservazione e su chi entra; 21 rischi in osservazione fermano, 20 no; decisione sullo stato nelle rettifiche; rischi in osservazione ed entrati/usciti in `Ciclo.txt`); dati di esempio conformi alla rubrica, con l'esito calcolato dallo script; regole delle rettifiche umane; consistenza fra due run; una mappa delle colonne di un'altra versione ferma lo script; output di A6 (schema e controlli, un difetto per controllo) e file delle schede, compreso il razionale in parti (D-68: lettura delle etichette, perche' accanto a ogni valore, Razionale con il fenomeno, azioni e KRI con perche' ed effetto atteso; un razionale scritto prima resta intero); D-69: C8 su un'azione uguale a un'azione aperta (e nessuna nei cicli di prova), `precontrollo` (schema, controlli, forma del razionale, messaggio di correzione, codici di uscita, comando senza registro e senza baseline), allegato di A1 (baseline identica, controlli = testo del prompt di A5, guida senza note, sostituzione del file del ciclo prima, kernel senza i file nuovi); D-70: impronta dell'output nel comando `precontrollo`, lettura della baseline dall'allegato, kit della prova di Copilot Studio (lo script della skill contiene esattamente i moduli e lo schema del pacchetto, gli zip contengono `SKILL.md` e lo script attuali, `name` e `description` della skill nel formato richiesto; lo script eseguito come processo a parte da' la stessa prima riga, la stessa impronta e lo stesso messaggio del comando, legge anche una risposta con i recinti o `Baseline_corrente.json`, codice 2 su file illeggibili); D-82 (ramo `copilot-studio-pieno`): istruzioni dei sotto-agenti A1, A8, A3 e testi dei prompt aggiornati rispetto agli A*.md, un segnaposto per variabile globale, sotto il limite; ingressi dei prompt; argomenti YAML (trigger, id unici, segnaposto e globali ammessi, con un difetto per controllo); busta K9 con il codice attuale del motore, che riunito dai blocchi stampa la riga attesa con l'impronta del proprio codice; D-80: `diagnosi` su righe finte (valori all'ingresso dei soli rischi nuovi, verso delle rettifiche per rischi nuovi e riapertura, Velocity da n.v. senza verso, KRI esclusi, margine di Mosca dei rischi lontani, segnalazione di chi non ha gli anni di adeguamento) e istruzione sugli anni di adeguamento dei rischi in osservazione nell'allegato di A1; D-81: la frase "ESPOSIZIONE NON NOTA" (Da motivare con i due valori e il limite di un punto, Osservazione senza un valore maggiore, nessun Bloccante in piu', nessuna segnalazione senza la frase), conteggio in `diagnosi`, frase nell'allegato | no |
| `test_fonti.py` | `fonti.md` leggibile, codici unici e conformi allo schema A3, al massimo 4 siti per l'agente con URL validi per Agent Builder, codici dei dati di esempio nell'elenco, elenco nel prompt di A3; raccolta notizie con feed finti (RSS, Atom, voci senza data, finestra, esclusioni, doppioni, fonte giu'), senza rete | no |
| `test_app.py` | l'app e i piu' analisti (D-83), senza Excel: ingresso delle risposte (BOM, recinti, testo attorno, risposta tagliata in due parti, agente dallo schema compreso A8, nomi, In_arrivo con originali e precedenti, parere di A4, risposta di un altro agente), stato e prossimo passo su archivi finti (baseline, validazione, riapertura, report, schede, trimestre chiuso, straordinario, settimana, lucchetto), flussi con un Ambiente finto (trimestrale con il giro di correzione, ripresa da In_arrivo, risposta tagliata, validazione, settimanale con il fermo di A3, annullamento), `NFR.cmd` solo ASCII; lucchetto (preso e lasciato anche dopo un errore; di un collega: fermo, e il suo resta; scaduto: si prende; il proprio rimasto: si riprende; copia in conflitto di OneDrive: ritiro), `sblocca` registrato; sostituzione dalla copia di lavoro (originale cambiato: fermo, niente segnato come salvato; invariato: sostituito senza file temporanei); registro aperto in esclusiva da un programma | no |
| `verifica_riferimenti.py` | tassonomia, controlli C1-C10 (anche nel testo unico `01_Kernel/controlli_A5.md` e senza copie nel modello di A5, D-69), numeri di passo, campi derivati, formule e nomi del manuale, indice di 00_LEGGIMI, comandi e opzioni citati nella guida e nei README (anche con il trattino, come `aggiorna-registro`), versione della struttura uguale in generatore, script, mappa e template | no |
| `run_catena.py` | due cicli trimestrali e due settimane con lo strumento di campo vero, su una copia del template, verificati aprendo il workbook in Excel; validazione nella griglia del foglio Validazione, come la fa il validatore (D-67); primo uso (`inizializza`) e dismissione di un rischio; registro di produzione dal vuoto al secondo ciclo; aggiornamento di un registro del template del 23/09 e del 2026-09-25c (colonne dismesse); A5 facoltativo e segnalazioni in validazione (D-71); knowledge di A7 dopo trimestrale, valida e dismetti e Note dell'analista archiviate al ciclo dopo (D-72); registro unico (D-79): NFR-16 nuovo in osservazione nel 2026Q3 con i tre del template riportati, pagina Fenomeni per score con il perche', NFR-16 che entra nel radar nel 2026Q4 con KRI e azioni; passo 14 con uscita in due cicli, decisioni del validatore sullo stato, capienza ridotta e dismissione di un rischio in osservazione; passo 11c con la conversione della lista di un registro 2026-10-08b; report al comitato confrontato con calcoli indipendenti, rigenerato da `valida` (D-83); schede dei rischi con A6 (controlli sull'output, file); passo 15, piu' analisti (D-83): lucchetto di un collega, `sblocca`, scrittura dalla copia di lavoro, registro aperto sul PC, allegati di A3 e A4, prompt archiviati; traccia della riapertura | **si'** |
| `osserva_cartella.py` | strumento della prova K7a della CS-1 (`09_Copilot_Studio/Prove_CS1.md`): ora in cui i file compaiono sul PC da SharePoint, e file segnale per misurare il caricamento; non fa parte del processo |
| `confronta.py` | strumento: confronta due output di A1 (usato dai test e, in tenant, per il doppio run); `--primo-ciclo` abbina i rischi per event type e nome quando, da registro vuoto, A1 li numera da se' | no |
| `comune.py` | percorsi e utilita' condivise | — |

La suite **non ha copie del codice di campo**: importa
`07_Senza_Studio/` e lancia `esegui_ciclo_locale.py` come farebbe un analista.
Cosi' collauda esattamente il codice che gira in esercizio.

## I dati di prova (`dati/`)

| File | Cos'e' |
|---|---|
| `baseline_2026Q3.json` | baseline estratta dal template (ciclo precedente 2026Q2): 12 rischi nel radar, 3 in osservazione (NFR-13, 14, 15) e la regola del radar |
| `run1_A1_2026Q3.json` | output A1 per il 2026Q3 nel formato del 30/09 sera (impatto, niente confidence, rilevanza sulle fonti, anni_adeguamento; senza gap_controlli, esito, da/a, dimensione delle azioni): conferme, un aumento su evidenza esterna (NFR-03), NFR-11 con 3 anni di adeguamento, NFR-10 con Velocity non valutata, NFR-10-K1 senza soglie, NFR-03-K1 riproposto senza soglie, un KRI sostituito (NFR-02-K2 esce, il nuovo diventa NFR-02-K3); dal 01/10 due KRI per rischio con il `tipo` (Esposizione, Evoluzione: D-64); dall'08/10 (D-79) NFR-16, rischio nuovo sui rapporti di impiego, in osservazione (Prossimita 1, orizzonte e segnale, niente KRI ne' azioni) |
| `run2_A1_2026Q3.json` | secondo run sullo stesso input: stessi giudizi, prosa diversa |
| `run_A5_2026Q3.json` | esito di A5 per il 2026Q3 (approvato, un'osservazione C5 su NFR-06) |
| `run_A3_2026-10-12.json` | settimana con tre segnali concordanti su NFR-01 e una notizia sui rapporti di impiego collegata a NFR-16, in osservazione, con un flag (il suo segnale si verifica); ogni notizia ha un codice fonte dell'elenco |
| `baseline_2026Q4.json` | baseline estratta dopo la scrittura del 2026Q3 |
| `run3_A1_2026Q4.json` | output A1 per il 2026Q4: NFR-16 entra nel radar (Probabilita e Prossimita su di un punto, KRI e azioni; D-79), NFR-14 in osservazione aggiornato con evidenza nuova, NFR-13 confermato con una fonte nuova, aumento su evidenza interna; dal 02/10 (D-68) razionali nel formato a parti (RISCHIO, IMPATTO, PROBABILITA, PROSSIMITA, VELOCITY, ADEGUAMENTO per NFR-11) e razionali di azioni e KRI con EFFETTO. I dati del 2026Q3 (`run1`, `run2`) restano nel formato di prima: provano la lettura dei razionali senza parti. Dal 02/10 (D-69) nei tre run A1 non ripropone le azioni aperte: dove prima le ripeteva propone il passo successivo (in `run3`, per esempio, NFR-11: sostituzione nel 2026Q2, isolamento nel 2026Q3, supporto esteso nel 2026Q4); `baseline_2026Q4.json` ha le descrizioni nuove delle azioni del 2026Q3 |
| `decisioni_validatore_2026Q3.json` | cio' che il validatore scrive nel foglio Validazione per il 2026Q3: anni di adeguamento di NFR-06 (1, vanno nell'anagrafica), Velocity di NFR-10 da non valutata a 3, le due soglie di NFR-10-K1 fissate dalla Banca, un valore di KRI, un'azione respinta |
| `decisioni_validatore_2026-10-12.json` | una rettifica del segnale di una notizia |
| `run_A5_2026Q4.json` | esito di A5 per il 2026Q4 |
| `run4_A1_2026Q4-S1.json` | output di **A8** per lo straordinario 2026Q4-S1 (D-75, D-77): solo NFR-01, Probabilita da 4 a 5, con l'analisi dell'evento (NFR-07 toccato e non indicato: un'osservazione) e i due KRI di NFR-01 riletti |
| `registro_template_2026-09-23.xlsx`, `baseline_registro_template_2026-09-23.json` | registro nato dal template del 23/09 e la sua baseline attesa dopo `aggiorna-registro` (passo 11) |
| `registro_template_2026-09-25c.xlsx`, `baseline_registro_template_2026-09-25c.json` | registro nato dal template 2026-09-25c (un ciclo validato, con Gap_Controlli e Dimensione) e la sua baseline attesa dopo `aggiorna-registro` (passo 11b) |
| `registro_template_2026-10-08b.xlsx` | il template di esempio del 07/10 (lista di osservazione D-73, tre voci in osservazione) per la conversione al registro unico (passo 11c, D-79) |

Le baseline attese (`baseline_*.json`) sono state rigenerate il 30/09 con il
codice della semplificazione e di nuovo la sera (D-57...D-60): rispetto alle
precedenti non hanno Gap_Controlli ne' Confidence, hanno `impatto` al posto di
`severity`, il presidio dei controlli e gli anni di adeguamento
dell'anagrafica, e le fonti con la rilevanza. Il 01/10 (D-64) di nuovo: due
KRI per rischio e il `tipo` di ogni KRI in vigore (null nelle baseline dei
registri di prima, che non lo avevano).
| `registro_template_2026-09-23.xlsx` | registro nato dal template del 23/09, come quello in produzione: costruito il 25/09 con lo script del 24/09 (inizializza, una settimana validata, il primo ciclo con run1 tutto "Nuovo", validato con due rettifiche). Non si rigenera: e' la fotografia di un registro vecchio |
| `baseline_registro_template_2026-09-23.json` | la baseline di quel registro, estratta prima dell'aggiornamento: dopo `aggiorna-registro` deve risultare identica |

**Importante:** i payload degli agenti (run1, run2, run3, A3, A5) sono stati
scritti da Claude durante la generazione del pacchetto, seguendo i prompt
operativi sulle baseline estratte dallo script. **Non sono output dell'agente
Copilot reale.** Servono a collaudare la catena deterministica (schema,
controlli, scrittura, formule); la riproducibilita' e la qualita' del giudizio
dell'agente vero si misurano solo in tenant, con `confronta.py` sul doppio run.

I payload difettosi non sono file: i test li producono modificando `run1` un
difetto alla volta, cosi' ogni caso isola un solo controllo.

## La catena, in breve

Durata: circa 40 minuti in parallelo, circa 50 in sequenza (08/10/2026: Excel si apre e ricalcola circa 150 volte).
La catena e' divisa in **tredici gruppi indipendenti**, ognuno su copie proprie del template:
- `catena` (passi 0-5, 7, 7b, 8s, 8a);
- `gate` (6);
- `errore` (8, 8b);
- `primo_uso` (9);
- `produzione` (10);
- `aggiornamento` (11);
- `notizie` (3b);
- `aggiornamento_25c` (11b);
- `segnalazioni` (12);
- `riapertura` (13);
- `registro_unico` (14);
- `aggiornamento_08b` (11c);
- `piu_analisti` (15).

Con `--parallelo 3` (il default di `esegui_collaudo.py`) girano in tre processi, ognuno con la sua istanza di Excel:
`SessioneExcel` usa `DispatchEx` e non condivide l'istanza. La durata e' quella del gruppo `catena`, che resta in
sequenza perche' ogni passo parte dallo stato del precedente. Prova dell'08/10: 331/331 in 40 minuti.

Non lanciare due collaudi completi insieme: oltre ai tre Excel della catena, la demo o un altro collaudo
rallentano tutto e possono far scadere i tentativi di avvio di Excel. Se Excel non
parte al primo colpo, `excel_com.py` riprova fino a cinque volte: prima di
questa correzione la catena falliva a caso in 2 esecuzioni su 3.

1. Payload difettosi (fuori schema, soglie invertite, senza A5, A5 di un altro
   ciclo, A5 che cita rischi assenti, file che non e' JSON): fermo, checksum
   del workbook identico, nessun backup.
1-bis. Precontrollo (D-69) dal comando vero: le soglie invertite si vedono gia'
   prima di A5 (codice 1, messaggio per A1 in `Cicli/2026Q3/Correzione_A1_2026Q3.txt`,
   registro intatto); run1 non ha niente che fermi il ciclo (codice 0).
2. Ciclo 2026Q3 scritto (12 rischi, da un file salvato "UTF-8 con BOM"): zero errori, formule integre, copertura Python = foglio,
   storico KRI in coda (le righe del 2026Q2 restano identiche), rilettura per
   id con la data giusta, KRI nuovo con il primo progressivo libero e senza
   valore ereditato, KRI del ciclo nel foglio Indicatori = KRI in vigore,
   baseline anche in .txt, allegato di A1 `Input_A1_2026Q4.txt` con la stessa
   baseline, i controlli e la guida (D-69), righe per le liste SharePoint. **Report al
   comitato**: score composito = formula D-50 calcolata a parte (media pesata
   delle dimensioni valutate, ROUND di Excel); Classifica
   ordinata come un ordinamento indipendente (a parita', ordine
   dell'anagrafica); grafici della Classifica e lente di Mosca con un punto per
   rischio; **livello di allerta** del Radar_Mosca uguale a un calcolo
   indipendente (D-63), con il motivo; Quadro: rischi segnalati uguali a una
   selezione indipendente (primi tre, in attivazione o attenzione, variati,
   nuovi, in ordine di classifica), commento di
   run1 diviso in messaggio e decisioni ("MESSAGGIO: ... DECISIONI: ...");
   Quadro in due pagine anche con molti rischi segnalati (scala adattata);
   Delta con un motivo per rischio e grafico che non copre la nota sulla scala
   dopo l'adattamento delle altezze; Sintesi_Cicli ha la sintesi di A5 e il
   numero di osservazioni, senza avviso. Esito e "da/a" calcolati dallo
   script (NFR-03 Variato da 3 a 4; NFR-02 e NFR-06 Confermati); Velocity di
   NFR-10 vuota, non zero; NFR-10-K1 "Soglie da definire"; NFR-03-K1
   riproposto senza soglie conserva quelle del 2026Q2.
2b. Validazione del 2026Q3 nella griglia del foglio Validazione (D-67): lo
   storico ha una riga "Da decidere" per campo, la griglia una per rischio,
   KRI e azione (52), con le celle gialle uguali alle proposte e Score e
   Margine di Mosca uguali a quelli del Registro e del Radar_Mosca; il 2026Q4
   non parte prima; righe non valide (Impatto oltre un punto e senza
   motivazione, valore non numerico, Respingi sbagliato, motivazione corta, una
   soglia sola) rifiutate tutte insieme, con la riga del foglio, senza toccare
   niente; il margine della griglia si ricalcola mentre si scrive (NFR-06 con un
   anno di adeguamento, NFR-08 senza l'azione respinta) e Score e Margine
   calcolati PRIMA di `valida` sono quelli del registro DOPO; poi 4 righe
   rettificate (5 valori) e un'azione respinta applicate (Respingi vale per
   tutti i campi dell'azione, con la motivazione della riga), il ciclo esce
   dalla griglia, Variazioni coerenti con i valori validati (NFR-10 con
   la variazione "da n.v." a 3 ed esito Variato), anni di adeguamento di NFR-06
   rettificati a 1 e scritti nell'anagrafica senza variazione (D-60), soglie
   di NFR-10-K1 fissate e stato calcolato, proposta dell'agente conservata,
   archivio, righe per le liste e baseline aggiornati. Il Quadro avvisa che il
   commento di A1 precede 6 rettifiche o respingimenti. `schede-input` e
   `report` si fermano finche' il ciclo non e' validato; dopo, `report` scrive il
   PDF del report al comitato e, rilanciato con `--con-lavoro`, conserva la
   versione precedente (D-62).
2c. Schede dei rischi sul 2026Q3 validato: `schede-input` scrive un rischio
   per rischio valutato, in ordine di classifica, con valori, urgenza, storia e
   KRI, senza toccare il registro; il razionale scritto senza parti resta
   intero (`motivazioni` null) e azioni e KRI portano il loro razionale (D-68). Un output di A6 (costruito dal test con i
   soli dati dell'input) con un rischio mancante, una fonte cambiata, un numero
   inventato o una dimensione ripetuta (servono le quattro) ferma `schede` senza file; quello
   corretto produce `Schede_2026Q3.xlsx` (indice e una scheda per rischio in
   ordine di classifica, con la descrizione di A6) e archivia `A6_2026Q3.json`;
   senza A6 il file esce con i testi del registro.
3. Settimana: codice fonte fuori elenco e id ripetuti fermati; titoli che
   iniziano con "=" o sembrano date scritti come testo; segnali netti in
   peggioramento per NFR-01, 9.11 "In osservazione" (la notizia va su NFR-16, D-79), rilancio senza duplicati;
   nello storico due righe per notizia, nella griglia una; una riga cancellata a
   mano dalla griglia ferma `valida`, che indica il comando `griglia`; `griglia`
   la ripara conservando cio' che il validatore aveva scritto nelle altre;
   validazione delle notizie senza `--accetta-il-resto`.
4. Baseline estratta = baseline su cui e' stato scritto run3.
5. Ciclo 2026Q4: NFR-16 entra nel radar dall'osservazione (Entrato) e in anagrafica, copertura 13/13,
   KRI NFR-16-K1..K2, **9.11 ora presidiata**: la catena si chiude; NFR-14 resta in osservazione. La storia di un KRI
   (Indicatori) coincide con lo
   storico (5 cicli per NFR-01-K1); un KRI uscito ha la storia che si ferma al
   suo ultimo ciclo; l'elenco a discesa ha i 27 KRI mai definiti (due per rischio, D-64). Radar_Mosca:
   P x I e margine di Mosca uguali a un calcolo indipendente in Python; il
   Registro ha esattamente una riga per ciascuno dei 13 rischi. Anni di adeguamento
   dell'anagrafica (NFR-11, 3 anni nei dati di esempio) conservati dalla
   scrittura e usati come Y: NFR-11 "AGIRE ORA". Attenzione del supervisore
   conservata dalla scrittura: ◆ nell'etichetta esattamente per NFR-01, 02,
   07, 09; un solo cerchio per rischio, nella serie del colore del suo livello
   di allerta. Report del 2026Q4 come al passo 2.
3b. Notizie validate nelle viste (D-66): una settimana scritta sul template
   (due peggiorativi su NFR-08, una notizia su L1-03 senza rischi, una neutra su
   NFR-09) e' gia' nei segnali netti del Registro, nel foglio Notizie e nel
   livello di allerta (F3 su NFR-08); dopo la validazione (una notizia respinta,
   un segnale rettificato) le stesse viste contano i valori validati e il
   livello di NFR-08 torna quello di prima; Quadro coerente prima e dopo.
   Con lo Stato delle righe della settimana cancellato a mano nello storico,
   `valida` si ferma e indica il rimedio (rimettere "Da decidere" e lanciare
   `griglia`, che riporta le notizie nel foglio Validazione).
   Sintesi_Settimane ha la riga della settimana ("Nessun flag proposto"); al
   passo 3 la sintesi e i flag di A3 sono anche nel riquadro del foglio Notizie
   e il rilancio della stessa settimana aggiorna la riga senza duplicarla.
6. Gate: un ciclo scritto a meta' viene fermato prima del salvataggio.
7. Finestra settimanale: quattro settimane dopo i segnali di NFR-01 tornano stabili.
7b. Proposta di ciclo straordinario di A3 (D-75): a video e nel riquadro del foglio Notizie.
8s. Ciclo straordinario 2026Q4-S1 (D-75): parte solo da un ciclo validato; un rischio
   da rivalutare fuori anagrafica e' un fermo; decisione archiviata, baseline e allegato
   per il periodo `-S1`; un output che riscrive un rischio non indicato e' fermato (C1);
   l'output di A8 (`run4`, con l'analisi dell'evento) rivaluta NFR-01 e riporta gli
   altri 12 rischi gia' validati, con Periodo_Valutazione e margini di Mosca invariati;
   in validazione solo cio' che e' rivalutato; regola del punto sul 2026Q4; dopo la
   validazione il ciclo dopo e' il 2027Q1; un secondo straordinario e' il `-S2`.
8a. Straordinario di solo censimento con A8 (D-77): `baseline --straordinario` senza
   `--rischi`, allegato che lo dice; precontrollo con i messaggi per A8; NFR-17 scritto
   come nuovo, nel radar e da validare, gli altri 16 riportati (13 nel radar, 3 in osservazione); Sintesi_Cicli con il rischio nuovo
   e l'evento; `Ciclo.txt` di A7 con l'analisi dell'evento.
8. Errore dopo il salvataggio (Excel di output non scrivibile, come quando un
   file dell'archivio e' aperto): il messaggio dice che il registro e' scritto
   e di non rilanciare; la baseline e' gia' aggiornata. Poi la rettifica del
   valore di un KRI mai rilevato compila data e fonte della rilevazione.
9. Primo uso: `inizializza` crea il registro vuoto dal template (senza esempi,
   guida in testa e significato delle colonne conservati, zero errori) e non sovrascrive un file esistente;
   il primo ciclo con tutti i rischi nuovi si scrive (24 KRI da K1, due per rischio); `dismetti`
   toglie NFR-04 senza buchi nell'anagrafica (Registro con 11 righe), KRI fuori
   vigore, azioni annullate, baseline senza il rischio, atto archiviato.
10. Registro di produzione, dal vuoto al secondo ciclo: e' il percorso reale
   fino al primo ciclo (DECISIONI D-07, D-22). Registro inizializzato senza
   rischi; settimane senza rischi a cui collegare le notizie (tutte NON
   PRESIDIATO, aree non presidiate segnalate, zero errori; una notizia
   collegata a un rischio inesistente e' fermata; validazione della
   settimana); primo ciclo con tutti i rischi nuovi, notizie intatte; secondo
   ciclo bloccato finche' il primo non e' validato; validazione (ogni rischio
   accettato, validatore registrato); baseline del secondo ciclo con 12 rischi
   e 24 KRI in vigore. `produzione(e, template=...)` rifa' il percorso su un
   altro template della stessa versione (un template di una versione diversa
   viene rifiutato da `inizializza`: per quello c'e' il passo 11).
11. Aggiornamento del registro in produzione (DECISIONI D-34), su
   `dati/registro_template_2026-09-23.xlsx`: `settimanale` e `baseline` si
   fermano indicando `aggiorna-registro`, senza scrivere; `aggiorna-registro`
   porta il registro alla versione nuova con zero errori, stesse righe in ogni
   tabella, vecchio in `Backup` e baseline uguale a quella attesa; i
   compositi sono ricalcolati con i pesi D-50; rilanciarlo non fa niente. Poi
   un ciclo 2026Q4 intero sul registro aggiornato, con un anno di adeguamento
   scritto a mano nell'anagrafica: conservato dalla scrittura e usato dal
   Radar_Mosca, report corretto.
11b. Aggiornamento di un registro del template 2026-09-25c (D-49, D-54): con
   righe "Da decidere" su campi tolti dal modello `aggiorna-registro` si ferma
   senza toccare niente; righe "Da decidere" su campi attuali passano nella
   griglia con la decisione scritta nel vecchio foglio (una riga per campo) e
   si validano con `valida` (D-67); versione nuova, zero errori, stesse righe, Gap_Controlli e
   Dimensione non copiate (restano nel backup), colonna Rilievi presente,
   presidio "Non verificato" per ogni rischio, baseline uguale a quella attesa,
   report corretto.
12. A5 facoltativo e segnalazioni in validazione (D-71), con un Bloccante di
   A5 su NFR-12, un salto di due punti su NFR-03 (C3) e soglie invertite su un KRI
   di NFR-01 (C9): un difetto di integrita' (rischio mancante) ferma comunque,
   con il messaggio per A1; il resto non ferma: il ciclo si scrive, ogni
   segnalazione sta sul suo rischio (DA MOTIVARE), l'osservazione di A5 resta
   osservazione, Sintesi_Cicli, Quadro ed `Esito_controlli` dicono quante sono;
   nella griglia ⚑ sui soli tre rischi e la colonna Segnalazioni uguale al
   registro; `--procedi-con-rilievi` accettata ma inutile. `valida` su righe non
   toccate chiede le motivazioni e non accetta il salto ne' le soglie invertite.
   Un settimanale scritto durante la validazione aggiunge le notizie alla
   griglia, conserva cio' che e' gia' scritto (anche le segnalazioni) e non si
   ferma per un valore sbagliato rimasto li', che `valida` poi segnala; con le
   motivazioni, il salto riportato a un punto e le soglie corrette la
   validazione si applica e nella griglia restano solo le notizie della
   settimana. Il primo ciclo del passo 10 si scrive senza A5.
13. Riapertura della validazione (D-76), sul ciclo 2026Q2 del template, gia'
   validato: `riapri` rimette nella griglia tutti i rischi (anche in osservazione), i KRI
   in vigore e le azioni aperte senza cambiare il registro; una seconda
   `riapri` si ferma; un valore cambiato senza Motivazione ferma `valida` senza
   scrivere; poi due punti in piu' su NFR-02 e su NFR-05 passano (nessun limite in
   riapertura), il KRI respinto esce di vigore, con la decisione sullo stato NFR-14 entra
   nel radar (Entrato) e NFR-12 esce subito (KRI fuori vigore, anagrafica senza buchi),
   l'azione con l'owner cambiato resta Approvata, le righe non toccate restano
   identiche; storico con le decisioni "(riapertura)", griglia vuota, integrita' e
   report. Una seconda riapertura (`--rischi NFR-02`) porta solo quel rischio con
   i suoi KRI e azioni e, validata senza cambiare niente, lascia il registro
   com'era. Dal 23/10 (D-83): `riapri` lascia `Riapertura_<ciclo>.json`, `valida` la
   chiude con chi ha validato e rigenera il report; `valida --senza-report` no.
14. Registro unico (D-79), sul template: nel 2026Q3 NFR-08 scende sotto la soglia di
   Probabilita e resta un ciclo "Radar, in uscita" (con KRI e azioni); in validazione
   una decisione sullo stato senza Motivazione ferma `valida`; poi NFR-12 va in
   osservazione (esce subito, KRI fuori vigore) e NFR-16 nel radar; nel 2026Q4, con
   la capienza a 10, NFR-08 esce al secondo ciclo e il piu' basso per score resta un
   ciclo in uscita per capienza (11 nel radar), NFR-12 resta fuori per decisione;
   `dismetti` toglie un rischio in osservazione.
15. Piu' analisti (D-83), sul template: con il lucchetto valido di un collega `griglia` si
   ferma e il registro non cambia; `diagnosi`, che non scrive, non lo guarda; `sblocca`
   lo toglie e lo registra; con un lucchetto scaduto `griglia` scrive dalla copia di
   lavoro (nessun file accanto al registro, cartella di lavoro vuota alla fine); con il
   registro aperto in esclusiva da un programma del PC si ferma prima di scrivere;
   `baseline` scrive `Input_A3_A4.txt` con la baseline del `.json` (AU7);
   `trimestrale` archivia i prompt del pacchetto in `Prompt_in_uso/`.
11c. Aggiornamento di un registro del template 2026-10-08b (lista di osservazione,
   `dati/registro_template_2026-10-08b.xlsx`): le tre voci in osservazione diventano
   NFR-13, 14, 15 in osservazione (accettate, "Conversione D-79", valori provvisori),
   le righe del registro restano nel radar, pagina Fenomeni e baseline con i tre.
