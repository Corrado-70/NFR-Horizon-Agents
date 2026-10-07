# A3, A4, A5, A6 — perche' di ogni blocco

Documentazione dei prompt generati da `02_Agenti/modelli/A3.md`, `A4.md`,
`A5.md`, `A6.md`. Numeri di passo, sezioni e controlli sono quelli dei modelli; il
collaudo (`verifica_riferimenti.py`) controlla che coincidano.

# A3 Interim Update (settimanale)

## Input
"Usa sempre lo strumento di ricerca file o gli strumenti di ricerca aziendale:
non rispondere a memoria" (anche in A1 e A4): obbliga a leggere davvero
`News_Inbox`, `Analisi_Interne` e la baseline in knowledge. Senza, su un
compito che sembra chiaro il planner puo' saltare il recupero.

## Ruolo
"Non modifichi score e non proponi numeri": principio 3 del sistema. Senza,
il registro deriverebbe dietro il ciclo delle notizie e smetterebbe di misurare
il rischio.

## Procedura

### Passo 1 — Settimana = lunedi'
Il foglio raggruppa le notizie per lunedi' (formula `Settimana` di NewsLog) e
la scrittura rifiuta una settimana che non e' un lunedi': i due devono parlare
la stessa lingua.

### Passo 2 — Tre canali, deduplica per fatto, codice fonte
I tre canali (raccolta automatica dei feed e file manuali in `News_Inbox`,
siti configurati, documenti interni) coprono cose diverse: i feed danno
regolarita', i siti le autorita' senza feed, i documenti interni la
prossimita' vera. L'elenco delle fonti e' nelle istruzioni (segnaposto
`{{FONTI}}`, da `01_Kernel/fonti.md`) e non in una knowledge: cio' che e'
recuperabile e' ignorabile.

Regola "la copertura mediatica non e' evidenza": dieci articoli sullo stesso
fatto sono un segnale, non dieci. Senza deduplica la soglia di 3 segnali
netti si supererebbe con una sola notizia molto ripresa.

`codice_fonte` rende la regola "solo fonti dell'elenco" verificabile: lo
schema ne impone il formato, la scrittura settimanale ferma un codice che non
e' nell'elenco o e' escluso. `MAN` lascia entrare cio' che un analista ha
scelto di caricare, ma lo rende visibile in NewsLog (colonna Codice_Fonte).

### Passo 3 — id_notizia
Formato fisso: la scrittura deduplica per id, quindi rilanciare la stessa
settimana non duplica le righe.

### Passo 4 — Nove intensita', sempre
Ogni notizia e' valutata su tutte le categorie, non solo sulla piu' ovvia: e'
cosi' che emergono le aree non presidiate (una notizia su una categoria senza
rischi censiti). Esattamente nove voci, una per categoria della tassonomia
interna (D-74; fino al 07/10 sette, gli event type di Basilea): la scrittura lo
verifica.

### Passo 5 — Rischio collegato o null
Null e' un'informazione, non un errore: alimenta "Notizie non collegate" e il
presidio per categoria nel foglio Notizie.

Passo 5-bis (D-73): la voce della lista di osservazione toccata dalla notizia e i
segnali sulle voci (Avvicina, Segnale verificato, Allontana). Lo script ferma una voce
che non e' in osservazione; notizie e segnali arrivano ad A1 nella baseline del ciclo
dopo, come evidenza da verificare: A3 non promuove ne' archivia.

### Passo 6 — Flag proposti
Un flag cita un descrittore della rubrica: e' un argomento per il prossimo
ciclo, non una variazione. I segnali netti del Registro (conteggio delle
notizie peggiorative meno migliorative) restano deterministici e indipendenti
dal flag.

Passo 6-bis (D-75): la proposta di ciclo straordinario, solo con la regola del
segnale critico della rubrica (sezione 6). Una regola esplicita evita due errori
opposti: proporlo a ogni notizia forte (la funzione di rischio smetterebbe di
leggerlo) o mai. Decide la funzione di rischio; lo script la mette a video e nel
foglio Notizie. Per stare negli 8.000 caratteri il prompt e' stato accorciato senza
togliere regole (7.914).

### Passo 7 — Sintesi
Le aree non presidiate sono dette esplicitamente perche' sono il segnale piu'
utile di A3 per il ciclo successivo (catena verificata in `run_catena.py`).

### Passo 8 — Autocontrollo
I quattro valori letterali: il foglio conta per testo esatto, un sinonimo vale
zero in silenzio.

# A4 News Assessor (su richiesta)

## Regole
- "Mai una cifra nuova": un numero in un parere viene citato come se fosse una
  valutazione. Gli score vigenti si possono citare, dicendo che sono deliberati.
- "Mai una persona nominata": il parere circola in Teams; i nomi nelle notizie
  non aggiungono informazione sul rischio della Banca.
- Notizie: il foglio aggrega le notizie scritte da A3; A4 non scrive nulla.
  Promettere che la notizia compaia li' sarebbe falso.

## Struttura della risposta

### Sezione 1 — Il fatto
Separare il fatto dall'interpretazione e' la prima difesa contro la deriva
mediatica.

### Sezione 2 — Nove categorie
Stessa regola di A3: analisi di impatto su tutte e nove le categorie della
tassonomia interna (D-74), per trovare le aree non presidiate.

### Sezione 3 — Rischi toccati
Ancora il parere alla valutazione deliberata (la baseline), non a un giudizio
da zero.

### Sezione 4 — Coerenza
"Un solo segnale non e' una tendenza": la soglia di direzione in parole.

### Sezione 5 — Cosa suggerisco
Verifiche, non variazioni: la via per cambiare uno score e' il ciclo
trimestrale. Dal 07/10 (D-75), se la notizia soddisfa la regola del segnale
critico, A4 scrive in testa "PROPOSTA DI CICLO STRAORDINARIO" con i rischi e il
motivo: la stessa regola di A3, perche' una notizia portata a mano ad A4 puo'
essere proprio quella critica.

### Sezione 6 — Limiti
Un parere senza limiti dichiarati viene letto come piu' solido di quanto sia.

# A5 Challenger (trimestrale, dopo A1)

## Input ristretto
A5 riceve solo l'output di A1 e la baseline, mai le notizie: giudica se la
valutazione e' sostenuta da cio' che essa stessa cita. Se leggesse le stesse
fonti di A1 tenderebbe a rifare la valutazione invece di controllarla. In
Agent Builder: nessuna knowledge source. Per lo stesso motivo A5 **non** ha la
frase "Usa sempre lo strumento di ricerca file", che hanno A1, A3 e A4: le due
istruzioni sono in conflitto per scelta, non per svista.

## I nove controlli
Ogni controllo ha una controparte in `07_Senza_Studio/controlli_a5.py` nella
misura in cui e' esprimibile come regola (vedi `06_Governance`, tabella dei
controlli). Il 30/09/2026 (D-49...D-56) i controlli sono stati ridotti a cio'
che A1 scrive davvero: stessa numerazione, contenuto piu' snello.

Dal 02/10 (D-69) il testo dei nove controlli non sta piu' nel modello di A5 ma
in `01_Kernel/controlli_A5.md`, e `componi_prompt.py` lo inserisce al posto di
`{{CONTROLLI}}`: lo stesso testo entra nell'allegato di A1
(`Input_A1_<ciclo>.txt`), che verifica il proprio output con le stesse regole
prima di rispondere. Il prompt composto di A5 e' identico a prima, salvo la
frase nuova di C8. A5 non perde indipendenza: non vede la knowledge ne' la
chat di A1, e giudica cio' che A1 consegna. Gli errori meccanici gli arrivano
piu' di rado, perche' il precontrollo dello script li ferma prima.

### C1 — Completezza
Un rischio mancante, scritto a meta', sul radar si legge come un crollo. Un
rischio esistente non cambia categoria (D-74: salvo la riclassificazione di un
codice di Basilea, che e' un'Osservazione): se il meccanismo di perdita e' un
altro, e' un rischio nuovo con un id nuovo. Fino al 29/09 C1 guardava anche
l'esito, che ora calcola lo script (D-51).

### C2 — Variazioni
Una voce per ogni valore cambiato, e solo per quelli: nessuna variazione
nascosta dietro una conferma. Il confronto "da/a" non c'e' piu' perche' i due
valori li aggiunge lo script dalla baseline; resta il controllo che ogni
cambio abbia la sua evidenza, compreso il passaggio di una Velocity da un
valore a non valutata.

### C3 — Evidenza delle variazioni
Data nella finestra del ciclo, evidenza specifica, massimo un punto: le regole
di variazione 2 e 3. Una Velocity prima non valutata entra con qualunque
valore.

### C4 — Plausibilita'
L'unico controllo senza controparte deterministica: dire se un 4 corrisponde
al descrittore 4 e' giudizio. E' il motivo per cui lo script si ferma se manca
l'esito di A5. Guarda anche: un rischio = un meccanismo di perdita (D-55); la
Velocity valorizzata solo se le fonti documentano i tempi (D-50); i numeri del
razionale (D-36: un numero senza fonte, non dichiarato come valutazione, e'
un'Osservazione). Niente piu' Gap_Controlli e pavimento D-47: il 29/09 fermavano
7 rischi su 7 su un dato che A1 non poteva vedere. La Prossimita 4-5 chiede un
caso nominato, ma dentro il descrittore (D-48). Dal 01/10 (D-65) "Probabilita
4-5 con la Banca esposta": un fenomeno diffuso non e' probabile per una Banca
che non ha il bersaglio; e' giudizio, quindi sta in C4 e non nello script.

### C5 — Fonti
Dal 30/09 sera (D-58) la Confidence del rischio non c'e' piu': ogni fonte ha
una rilevanza 1-3. C5 ferma una fonte datata dopo il ciclo e segnala come
Osservazione una Probabilita 5 o una Prossimita 4-5 senza una fonte di
rilevanza 3 (A5 giudica in C4 se la deroga per un fenomeno ad altissimo
impatto e' dichiarata e sostenibile) e le fonti perse con i valori invariati.
Prima la confidence misurava l'evidenza contando le fonti, e le fonti
dello stesso ente o sullo stesso fatto contano una volta.

### C6 — Deriva
Inflazione progressiva e deriva mediatica sono i due modi in cui il sistema
peggiora da solo. Il controllo meccanico guarda gli aumenti senza fonti nuove.

### C7 — Rilettura KRI
Solo KRI in vigore, ciascuno una volta. Un KRI in vigore non riletto non e' un
errore: A1 rilegge solo i valori che trova (D-53) e il foglio lo mostra come
"Non rilevato".

### C8 — Azioni
Sempre Osservazione dal 30/09 (D-54): l'euristica "sembra una persona" sbaglia
in entrambe le direzioni ("Immobili, Infrastrutture e Procurement" il 29/09).
La regola vera sta nella validazione: `valida` non accetta un owner che sembra
una persona, neanche "Accettato". Dal 02/10 (D-69) C8 guarda anche che
un'azione non ripeta un'azione aperta della baseline: nei dati di prova A1
riproponeva ogni trimestre le azioni gia' approvate. Lo script segnala la
stessa descrizione (a meno di maiuscole, spazi e punto finale) di un'azione
aperta dello stesso rischio; un'azione solo simile la giudica A5.

### C9 — KRI
Due per rischio, uno di Esposizione e uno di Evoluzione (D-64; prima da 1 a 3,
D-53); soglie entrambe o nessuna (D-53). "Uno per tipo" e le soglie invertite
non sono esprimibili in JSON Schema: C9 e la formula Stato del foglio sono i
presidi. Un KRI in vigore non riproposto e' un'Osservazione: esce di vigore;
anche un tipo diverso da quello della baseline e' un'Osservazione (un KRI non
cambia natura). Il prompt chiede ad A5 anche che i tipi siano "coerenti con
cio' che misurano": e' giudizio, lo script non lo controlla.

## Esito
"Da rivedere" se almeno un Bloccante. Dal 06/10 (D-71) A5 e' **facoltativo** e
nessun suo rilievo ferma il ciclo: lo script trasforma i suoi Bloccanti in
segnalazioni "Da motivare", che stanno sui rischi (colonna Rilievi), nella
colonna Segnalazioni del foglio Validazione e, contate, in Sintesi_Cicli e nel
Quadro; in validazione ogni rischio interessato chiede una Motivazione. Per
questo il ruolo nel prompt dice "I tuoi rilievi vanno al validatore: un
Bloccante lo obbliga a motivare la decisione" (prima: "Puoi arrestare il
ciclo"). Restano cancelli solo i difetti di integrita' dei controlli
meccanizzati (D-10). Fino al 05/10 (D-56) i Bloccanti di A5 fermavano il ciclo e
si superavano con `trimestrale --procedi-con-rilievi --motivo --decisore`.

# A6 Schede dei rischi (trimestrale, dopo la validazione)

Decisione D-40 (25/09): le schede di focus sui rischi sono un file a parte
rispetto al registro, e i loro testi lunghi li scrive un agente dedicato. Il
registro resta compatto (descrizione e razionale brevi di A1); la scheda
spiega a chi non conosce il tema.

## Ruolo
A6 non valuta: spiega una valutazione gia' validata. Per questo si lancia
DOPO il comando valida, e lo script rifiuta di preparargli l'input se il ciclo
ha ancora decisioni da prendere. Cosi' la scheda non puo' contraddire un
valore rettificato dal validatore.

## Input
Un solo allegato, `Schede_input_<ciclo>.json`, scritto dal comando
`schede-input` dal registro validato: per ogni rischio le quattro dimensioni
(Impatto, Probabilita, Prossimita, Velocity; la Velocity puo'
essere "non valutata"), gli anni di adeguamento, il presidio dei controlli
indicato dalla Banca, score,
urgenza (X, Y, Z, margine), livello di allerta con il motivo (D-63), variazioni
con l'evidenza, fonti, azioni, KRI con il tipo (D-64), storia degli score. Niente notizie, knowledge o ricerche: la scheda non deve
introdurre fatti che il ciclo non ha valutato. Dal 02/10 (D-68) lo script
divide il razionale di A1 nelle sue parti: `razionale_rischio` (il fenomeno) e
`motivazioni` (il perche' di ogni valore, con i documenti; null se A1 non ha
diviso il razionale); azioni e KRI arrivano con il loro razionale e
l'effetto atteso. Dividere nello script, non chiederlo ad A6, rende certo che
la motivazione di Impatto vada accanto all'Impatto.

## Regole
1. Una scheda per rischio, stesso id: controllato dallo script.
2. Valori immutabili: A6 non ne propone altri.
3. **Nessun numero nuovo**: ogni numero dei testi deve stare nei dati del
   rischio o nella rubrica. E' la controparte deterministica del divieto di
   inventare: `schede.controlla_a6` estrae i numeri (una data in italiano e in
   ISO sono gli stessi numeri; 4,2 = 4.2) e ferma le schede se uno non c'e'.
   Una stima dell'agente ("circa il 30%") non passa.
4. Descrizione estesa: il fenomeno in termini di rischio (causa, evento,
   danno per la Banca) per chi non conosce il tema, senza i motivi dei
   punteggi, che vanno nelle dimensioni (D-68, richiesta dell'utente).
5. Una spiegazione per ognuna delle quattro dimensioni, con le informazioni e
   i documenti che sostengono il valore (per una Velocity non valutata:
   perche' manca); parte dalla motivazione di A1 e **non attribuisce a un
   documento cio' che A1 non gli attribuisce**: A6 non ha letto i documenti,
   vede solo i riferimenti. Se il valore e' stato rettificato, con il motivo
   del validatore (che lo script scrive nelle variazioni come "Rettifica del
   validatore: ...").
6. Fonti copiate identiche: lo script confronta i riferimenti con quelli
   dell'input, carattere per carattere; A6 aggiunge solo "a sostegno di".
7. Niente nomi di persone: non verificabile dallo script, lo guarda chi
   legge le schede prima del comitato.

La rubrica (sezioni 1 e 2) e' nel prompt perche' A6 spiega un valore con il
descrittore: e' anche l'unica fonte di numeri ammessa oltre ai dati.

## Controlli dello script (comando schede)
Schema (`schema_output_A6.json`), poi `controlla_a6`: ciclo uguale all'input,
stessi rischi senza ripetizioni, quattro dimensioni ciascuna una volta, stesse
fonti, nessun numero fuori dai dati. Un problema ferma il comando: nessun file,
il registro non si tocca mai. Senza l'output di A6 il comando produce comunque
le schede con i testi del registro (dal 02/10 il Razionale, il perche' di ogni
valore e, per azioni e KRI, perche' ed effetto atteso, tutti di A1): A6
migliora la lettura, non e' un prerequisito del report. A6 non scrive i testi
di azioni e KRI: li mostra lo script dal registro. Aggiungerli all'output di A6
lo allungherebbe di molto (una risposta troppo lunga in Agent Builder rischia
di arrivare troncata) per riformulare testi gia' brevi.

# A7 Assistente del registro (D-72, 07/10/2026)

**Perche' esiste.** Chi legge il radar chiede "perche'": perche' un rischio ha quei valori, quell'urgenza, quel
livello; perche' un tema dei documenti non e' un rischio. Le risposte stanno gia' nel registro (motivazioni di A1,
decisioni del validatore, segnalazioni, parametri), ma sparse in fogli e archivi.

**Perche' senza allegati.** L'utente vuole un agente "completamente interattivo": lo script scrive la knowledge
(cartella `Kernel/Spiegazioni`) alla fine dei comandi che si lanciano gia'. Un file per posto dell'anagrafica
(`Rischio_01..20.txt`), con nomi fissi, cosi' anche un rischio appena censito e' subito visibile:
la ricerca della knowledge trova il pezzo giusto (un file unico di decine di KB verrebbe letto a pezzi) e un file
aggiornato si reindicizza subito.

**Regole del prompt e perche'.**
- REGISTRATO / CALCOLATO / LETTURA MIA: il rischio vero di un agente che spiega e' presentare una ricostruzione
  plausibile come se fosse il motivo di chi ha deciso. Dichiarare la natura di ogni frase lo rende verificabile.
- Nessun valore nuovo: come A4 e A6, A7 non valuta (D-41); per "dovrebbe essere piu' alto?" indica il descrittore
  e l'evidenza che servirebbe.
- Fenomeni non censiti: il motivo lo scrive A1 nel ciclo (campo `fenomeni_non_censiti`); se manca, A7 cerca nei
  documenti e lo dice. Senza questo campo ogni risposta sarebbe una ricostruzione. Dal 07/10 sera (D-73) anche la
  lista di osservazione e' in `Ciclo.txt`: per un fenomeno in osservazione A7 riporta valutazione preliminare,
  motivazione e segnale di avvicinamento (regola 4).
- Sintesi per il Quadro: al massimo 600 caratteri, perche' sta in una riga della prima pagina del report.

**Rubrica**: sezioni 1, 2, 3, 8 (dimensioni, rilevanza delle fonti, regole di variazione, urgenza). Prompt 6.726
caratteri (6.575 fino al 07/10 pomeriggio): lo spazio restante serve al modo manutenzione della fase 4.

