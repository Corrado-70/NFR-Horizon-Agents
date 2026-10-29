# A1 Horizon Scanner — perche' di ogni blocco

Documentazione del prompt `02_Agenti/A1_Horizon_Scanner.md`, che e' generato
da `02_Agenti/modelli/A1.md` + kernel tramite `componi_prompt.py`. Il prompt
operativo non contiene commenti (tutto cio' che sta in un prompt e' letto come
istruzione): il perche' sta qui. I numeri di passo sono quelli del modello; il
collaudo (`verifica_riferimenti.py`) controlla che coincidano.

## Ruolo

Solo JSON (lo dice l'Output, "Solo JSON, nessun testo attorno"; fino al 02/10
lo ripeteva anche il ruolo, tolto per fare spazio al razionale in parti, D-68):
l'output e' un contratto con la scrittura, non un testo per persone. L'unico testo per persone e' la `sintesi`: lo script
la scrive nella tabella Sintesi_Cicli e il foglio Quadro del report la mostra
come commento dell'analisi (decisioni D-32 e D-39). Il resto del report viene
dal workbook. Lo score composito non e' nominato nel ruolo perche' la regola
arriva dal kernel (rubrica, sezione Dimensioni): una sola formulazione, nessuna
ripetizione da tenere allineata.

"Prima di valutare analizza nel dettaglio ogni fonte" (01/10, D-64; fino al 13/10
precedeva "Ragiona con cura", tolto per far posto alla frase sulla ricerca file): richiesta del responsabile, che vale per tutta la valutazione e non
solo per i KRI. Sta nel ruolo, non in un passo, perche' riguarda ogni passo:
il rischio che corregge e' una valutazione costruita sul titolo o sull'estratto
di una fonte invece che sul suo contenuto.

## Input

"Usa sempre lo strumento di ricerca file": obbliga a consultare la knowledge
invece di rispondere dal solo contesto della chat.

La baseline e' **allegata**, non lasciata in knowledge: e' l'unico input senza
il quale il ciclo non ha senso, e il retrieval potrebbe saltarla. Se manca, A1
si ferma con una frase fissa invece di inventare un ciclo precedente.
`Analisi_Interne` e `News_Inbox` restano knowledge: sono ampie, e ci si
aspetta un recupero selettivo.

Dal 02/10 (D-69) l'allegato e' `Input_A1_<ciclo>.txt`, che lo script scrive
accanto alla baseline (`07_Senza_Studio/input_a1.py`): la baseline (JSON), i
dieci controlli di A5 (`01_Kernel/controlli_A5.md`, lo stesso testo delle
istruzioni di A5) e la guida di scrittura (`01_Kernel/guida_scrittura_A1.md`:
descrizione, razionale in parti con descrittore, fatto, documento e "perche'
non il valore vicino", azioni, KRI, un esempio completo di forma). Perche' in un
allegato e non nelle istruzioni: le istruzioni sono al limite degli 8.000
caratteri, e un allegato, a differenza della knowledge, A1 lo riceve sempre per
intero. Perche' nella baseline e non in un secondo file: un solo gesto per chi
lancia A1. Richiesta dell'utente: il giro A1 → A5 → A1 era scomodo, e le
descrizioni e motivazioni di A1 erano povere. Se si allega la sola baseline
(pacchetto vecchio), A1 lavora come prima: la frase "Senza baseline" resta
quella.

Dal 07/10 la guida di scrittura chiede anche due campi facoltativi del JSON,
senza toccare il prompt (che resta a 7.963 caratteri): `fenomeni_non_censiti`
(D-72), i temi esaminati e non censiti con il motivo, che servono ad A7 per
rispondere "perche' questo tema non e' un rischio"; e il **registro unico**
(D-79, al posto della lista di osservazione della D-73): un fenomeno lontano o
solo teorico si censisce come rischio, con la stessa rubrica, e lo script lo
mette in osservazione (fuori dal radar, niente KRI ne' azioni) con la regola di
`regola_radar`; A1 scrive l'orizzonte in anni e il segnale di avvicinamento.
Dei rischi in osservazione della baseline A1 riscrive solo quelli con evidenza
nuova; gli altri lo script li riporta. Un rischio che sale entra nel radar e A1
gli scrive subito KRI e azioni. Perche' nella guida e non nel prompt: lo
spazio (una voce pesa circa 0,5 KB nella risposta, un rischio circa 4 KB) e il
fatto che l'allegato arriva sempre per intero.

## Procedura

Il 30/09/2026 (semplificazione dello scoring, `Analisi_Architettura/Archivio/11`,
D-49...D-56) la procedura e' stata alleggerita: A1 valuta solo cio' che le fonti
sostengono. Non scrive piu' l'esito ne' i "da/a" delle variazioni (li calcola
lo script, D-51), non valuta Gap_Controlli (dato qualitativo della Banca, D-49),
puo' lasciare la Velocity non valutata (D-50), propone KRI con soglie
facoltative (D-53; dal 01/10 due per rischio, uno per tipo, D-64), non dichiara la dimensione delle azioni (D-54) e non deve
coprire tutte le categorie (D-55). I passi restano dieci.

### Passo 1 — Ciclo e data dalla baseline
Il ciclo diventa criterio delle formule (`RR_Ciclo = cicloCorrente`) e deve
combaciare al carattere. Farlo calcolare all'agente dalla data odierna produce
errori a cavallo di trimestre; la baseline lo porta gia' calcolato dallo script.

### Passo 2 — Finestra dell'evidenza
Traduce la regola di variazione 3 (evidenza datata dopo il ciclo precedente) in
un criterio di selezione delle fonti, prima ancora del giudizio. C3 la
riverifica in modo deterministico. **Primo ciclo**: non c'e' un ciclo
precedente (`data_riferimento_precedente` e' null nella baseline di un registro
appena inizializzato), quindi vale tutta l'evidenza disponibile non datata
dopo `data_riferimento`. La recenza non si perde: la dice la data di ogni fonte.
Anche C3 accetta ogni data in questo caso.

### Passo 3 — Tutti i rischi, dai valori precedenti
"Dai valori precedenti" rende la conferma il default (regola 1). "TUTTI"
perche' un rischio dimenticato, scritto a meta', sul radar sembra un crollo del
rischio: C1 e il controllo di copertura lo intercettano, ma e' meglio non
produrlo. "Stesso id e categoria": un rischio esistente non cambia
meccanismo di perdita; se il meccanismo e' un altro, e' un rischio nuovo con un
id nuovo (C1). Dal 07/10 (D-74) la categoria e' quella della tassonomia interna
della Banca; un rischio della baseline con un codice di Basilea si riclassifica
(guida di scrittura, sezione "Categoria di rischio"), oppure si segna FP se il
meccanismo e' fuori perimetro (frode, financial crime...): non e' un cambio di
meccanismo, e lo script lo tratta come Osservazione o segnalazione da motivare.

### Passo 4 — Rischi nuovi
Un rischio per ogni **meccanismo di perdita** non ancora coperto, sostenuto da
almeno una fonte specifica; anche piu' d'uno nella stessa categoria (regola di
classificazione della tassonomia). **Nessuna categoria e' obbligatoria**: la
rassegna parte dai driver su cui le fonti mostrano pressione (D-55). Fino al
29/09 il primo ciclo chiedeva di passare in rassegna tutti e sette gli event
type: A1 l'ha letto come "uno per tipo", ha accorpato meccanismi diversi (cloud
e terze parti; deepfake e identita' sintetiche) e riempito tipi deboli. Nessuna
lista di ambiti "attesi" nel prompt: l'analisi confermerebbe cio' che le si
chiede di trovare (D-37); la prevalenza (per esempio del cyber) deve venire
dalle fonti. Una categoria rimasta scoperta resta visibile: la `sintesi` la
dichiara e le notizie su quella categoria escono come "AREA NON PRESIDIATA" nel
settimanale. "Primo NFR-nn libero": gli id sono stabili e non si riusano. Il
metro di qualita' del primo ciclo e' la **validazione umana** (foglio
Validazione) insieme al doppio run.

### Passo 5 — Variazioni
Una voce per ogni valore cambiato, con l'evidenza e la sua data; nessuna per
un rischio nuovo, che non ha un valore precedente. Il "da" e l'"a" li aggiunge
lo script dalla baseline, e l'esito (Nuovo, Variato, Confermato) lo calcola lo
script (D-51): erano contabilita' che fermava il ciclo per errori di
trascrizione senza aggiungere giudizio. Fino al 30/09 sera anche la
confidence poteva variare; dal D-58 non c'e' piu' e le variazioni riguardano
solo le quattro dimensioni. Una Velocity prima non valutata entra con
qualunque valore, sempre con la sua evidenza (regola di variazione 2).

### Nota — Rilevanza delle fonti e anni di adeguamento (30/09 sera)
Ogni fonte ha una rilevanza 1-3 per la previsione (D-58): il responsabile
vuole vedere quanto conta ciascuna, non un numero unico del rischio. La
regola "Probabilita 5 o Prossimita 4-5: almeno una fonte di rilevanza 3"
lega le valutazioni alte a una fonte primaria o a un caso documentato; la
deroga per i fenomeni ad altissimo impatto (es. un nuovo Mythos) va
dichiarata nel razionale (D-61). Gli anni di adeguamento (D-60) li stima A1
dalle sue conoscenze e li decide il validatore: il valore validato va
nell'anagrafica e allunga la Y dell'urgenza. Sono nella rubrica (sezione 1),
non in un passo, per stare nel limite di caratteri.

### Passo 6 — Fonti di un rischio confermato
Regola 5 della rubrica: confermare non cancella le fonti. Senza questo passo il
modello tende a citare solo le fonti nuove, e una conferma diventa una
rivalutazione con meno evidenza e gli stessi valori. C5 lo segnala contando
le fonti rispetto alla baseline.

### Passo 7 — Azioni
Owner = funzione: una persona cambia ruolo, la funzione resta; e nominare
persone in un registro di rischio ha implicazioni di privacy. C8 lo segnala come
Osservazione; il comando `valida` rifiuta un owner che sembra una persona anche
se "Accettato" (D-54). "Mai una persona" e' uscito dal passo il 02/10 (D-69):
lo dice C8 nell'allegato. Dal 30/09 l'azione non dichiara la dimensione che riduce:
costringeva un'azione di approfondimento a "ridurre" un punteggio
(`Analisi_Architettura/Archivio/08`, P7).

"Azioni **nuove**" (02/10, D-69): nei dati di prova A1 riproponeva ogni
trimestre le azioni gia' approvate e aperte, e la scheda di NFR-11 mostrava tre
volte la stessa azione. Un'azione aperta e' nella baseline (`azioni_aperte`):
la guida chiede di richiamarla nel razionale e di proporre il passo successivo
o un'azione complementare; C8 segnala come Osservazione un'azione con la
stessa descrizione di un'azione aperta dello stesso rischio.

### Passo 8 — KRI, id, tipo e soglie stabili
Due per rischio (D-64; prima da 1 a 3, D-53): uno di **esposizione** (quanto
la Banca e' esposta: di solito un dato che fornisce la Banca) e uno di
**evoluzione** (quanto cresce il fenomeno: A1 puo' trovarne il valore nelle
fonti). Il tipo dice chi fornisce il valore e lo legge C9; un KRI in vigore
conserva il tipo come il kri_id e le soglie. Il riuso del kri_id tiene insieme la serie
storica: lo storico KRI ha una riga per KRI per ciclo, e il foglio Indicatori
la ricompone per KRI_ID. Un KRI nuovo ha `kri_id` null perche' l'id lo
assegna la scrittura (primo progressivo libero), mai l'agente. Le soglie A1 le
propone solo se una fonte le sostiene, entrambe; altrimenti null e le fissa la
Banca in validazione (stato "Soglie da definire"). Se A1 ripropone un KRI
senza soglie, restano quelle in vigore. Il 29/09 A1 aveva proposto 21 KRI,
tutti con soglie inventate. C9. "Mai il kri_id di un altro rischio" e' uscito
dal passo il 02/10 (D-69): lo dice C9 nell'allegato e lo segnala lo script (il precontrollo, se lo si usa, o `trimestrale`).

### Passo 9 — Rilettura dei KRI del ciclo precedente
A livello ciclo, non dentro il rischio: riguarda gli indicatori in vigore anche
dei rischi confermati. Solo i KRI di cui A1 trova un valore del ciclo nelle
fonti: gli altri restano "Non rilevato" (D-53). "Mai ricopiato": un valore
ricopiato mostra uno stato che nessuno ha misurato. C7 ferma solo un KRI
sconosciuto o riletto due volte.

### Passo 10 — Autocontrollo
"Verifica con controlli e guida dell'allegato e correggi" (02/10, D-69; dal 13/10
senza "Prima di rispondere", per lo spazio): fino ad allora il passo diceva solo "regole
rispettate; nessun campo in piu'", e A1 non conosceva le regole esatte con cui
A5 e lo script l'avrebbero controllato. Ora le ha nell'allegato, con le stesse
parole del prompt di A5. Serve a ridurre gli arresti del ciclo, non a
sostituire i controlli: un modello che rilegge il proprio output tende a
confermarlo. Per questo c'e' anche il **precontrollo** dello script prima di A5, facoltativo
(`esegui_ciclo_locale.py precontrollo`), che applica la parte meccanizzabile e
scrive il messaggio di correzione da incollare nella chat di A1.

"Nessun campo in piu'" era tornato il 30/09 (dopo la semplificazione A1 tendeva
a riscrivere i campi tolti, esito e gap_controlli); dal 02/10 lo copre lo
scheletro dell'Output e lo ferma lo script (il precontrollo, facoltativo, in pochi secondi). Fino al 02/10
il passo chiedeva anche riferimenti senza i codici interni dello strumento di
ricerca di Copilot (`turn1search17` e simili): la frase e' tolta per fare spazio
al razionale in parti (D-68), perche' lo script li toglie comunque quando scrive
il ciclo (`pulisci_riferimento`).

### Nota — Probabilita e Prossimita
La Probabilita ha descrittori di **plausibilita'** per la Banca (D-52), non di
frequenza: per un rischio senza storia la frequenza non e' osservabile. Serve
al Radar_Mosca (area del cerchio = Probabilita x Impatto) ed entra nello score
composito. La Prossimita dice QUANDO, la Probabilita QUANTO E' PLAUSIBILE; il
"caso nominato" per la Prossimita 4-5 (D-48) sta dentro il descrittore. Dal
01/10 (D-65) la Probabilita 4-5 vale "solo se la Banca e' esposta": i livelli 2
e 3 citavano gia' l'esposizione, 4 e 5 no. Niente dimensione a parte: A1 non
vede l'esposizione interna, che si misura con il KRI di esposizione.

## Kernel

Tassonomia (con la regola di classificazione: un meccanismo di perdita = un
rischio) e rubrica (sezioni 1-4: dimensioni, rilevanza delle fonti, regole di variazione,
KRI) sono inserite per intero dallo script di composizione. Non
sono una knowledge source: su un compito che sembra chiaro il planner salta il
recupero, e cio' che e' recuperabile e' ignorabile. Le sezioni 5-6 (notizie e
segnali) non servono ad A1 e restano fuori per stare sotto gli 8.000 caratteri.

## Output

Lo scheletro JSON mostra i nomi dei campi e i valori ammessi; le regole
complete (pattern, lunghezze, interi) le applica il validatore sullo schema,
che e' la controparte deterministica. Lo schema intero non e' nel prompt: da
solo occuperebbe quasi meta' del limite di caratteri.

La riga sulla `sintesi` (25/09, decisione D-32) fissa la struttura del
commento per il comitato: messaggio chiave, tre priorita' con id_rischio e
motivo, rischi nuovi e variati, decisioni richieste, e solo fatti delle fonti
citate. Viene dal confronto con un Horizon Scanning fatto con Copilot
(`Analisi_Architettura/Archivio/08`, P1): li' la pagina di sintesi executive era la
parte piu' utile per il comitato, da noi la `sintesi` non arrivava in nessun
output. La sintesi e' scritta prima della validazione: il Quadro avvisa
quando dopo sono state applicate rettifiche.

Dal 25/09 sera (D-39) la sintesi ha la forma "MESSAGGIO: ... DECISIONI: ...":
il Quadro la divide in due righe (messaggio chiave, decisioni richieste)
cercando il marcatore "DECISIONI:"; senza marcatore tutto il testo va nel
messaggio, quindi un output nella forma vecchia resta leggibile. L'utente ha
scelto un commento BREVE: il "perche'" di ogni rischio segnalato (primi tre,
AGIRE ORA, variati, nuovi) lo calcola il foglio dai dati validati, senza
caratteri in piu' nel prompt e senza testo che la validazione possa smentire.

Dal 02/10 (D-68) lo scheletro mostra anche **il formato del razionale**, con
la stessa tecnica delle etichette della sintesi: `"RISCHIO: causa, evento,
danno. IMPATTO: fatto e documento. PROBABILITA: ... PROSSIMITA: ... VELOCITY:
... ADEGUAMENTO: se serve"`, e per azioni e KRI `"perche'. EFFETTO: ..."`.
Richiesta dell'utente sulle schede dei rischi: il perche' di ogni numero
accanto al numero, con le informazioni e i documenti da cui viene, e il
Razionale come spiegazione del fenomeno in termini di rischio; per azioni e KRI
anche l'effetto atteso. Il perche' di un numero lo puo' scrivere solo A1, che
legge i documenti: A6 lo riformula. Il formato sta nello scheletro, non in un
passo, perche' costa meno caratteri e si vede dove va il testo. Non e' imposto
dallo schema: un razionale senza etichette passa (un fermo per un problema di
forma costerebbe un altro giro di A1), `trimestrale` lo segnala con un avviso e
la scheda lo mostra intero.

Spazio: il 02/10 pomeriggio (D-69) A1 e' a 7.963 caratteri su 8.000.
L'allegato nella riga dell'Input e il passo 10 nuovo (circa 70 caratteri) sono
entrati togliendo cio' che l'allegato o lo schema dicono gia': "mai una
persona" nel passo 7 (C8), "mai il kri_id di un altro rischio" nel passo 8 (C9),
"punteggi interi" nell'Output (rubrica: "Interi 1-5"). La guida di scrittura
non costa caratteri: sta nell'allegato. Il 02/10 mattina A1 era a 7.971
caratteri su 8.000. Il formato del razionale
(circa 170 caratteri) e' entrato togliendo ripetizioni: "restituisci SOLO un
oggetto JSON" nel ruolo (lo dice l'Output), i codici di ricerca nel passo 10
(li toglie lo script), il rimando "(sezione 2: stesso fatto = una fonte)" nella
regola 6 (la sezione 2 lo dice), il formato del ciclo nell'Output (passo 1 e
schema) e "id_rischio" nella riga della sintesi. Il 01/10 A1 era a 7.917
caratteri su 8.000. La frase sul ragionamento,
il tipo dei KRI e la riga sull'esposizione (circa 250 caratteri) sono entrati
accorciando la riga sugli strumenti di ricerca, la regola 6 (l'esempio dei
dieci articoli ripeteva "stesso fatto = una fonte"), la regola 7, il
descrittore 1 della rilevanza e la riga degli anni di adeguamento. Dopo la
revisione della rubrica del 30/09 sera A1 era a 7.885 caratteri
(7.496 dopo la semplificazione del mattino): i descrittori riscritti dal
responsabile, la rilevanza delle fonti e gli anni di adeguamento hanno preso
quasi tutto il margine; per farli stare sono stati accorciati i passi 3, 4, 10,
la deroga della Prossimita, le regole 3 e 7 e tolta la frase "non calcolare lo
score" (lo schema non ha il campo). Prima della semplificazione A1 era a 7.977:
i campi tolti quel giorno avevano liberato lo spazio per la regola del
meccanismo di perdita, le categorie senza rischi nella `sintesi` (allora event type) e la riga
sui codici di ricerca. Il 25/09 erano gia' stati tolti i pesi dai titoli delle
dimensioni della rubrica (gli agenti non calcolano il composito).
