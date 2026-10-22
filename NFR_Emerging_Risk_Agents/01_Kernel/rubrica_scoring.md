# Rubrica di scoring — scale, pesi, regole di variazione

> Tutto il sistema si ancora a questo file. Le sezioni numerate vengono
> inserite nei prompt degli agenti da 02_Agenti/componi_prompt.py; le righe che
> iniziano con ">" (come questa) sono note per chi legge e NON entrano nei
> prompt. I descrittori sono segnaposto verosimili: la funzione di rischio della
> Banca li deve riscrivere nel proprio linguaggio prima del deploy. Il limite
> di 8.000 caratteri delle istruzioni di un agente impone descrittori brevi:
> dopo ogni modifica rilanciare componi_prompt.py, che segnala il superamento.
>
> Semplificazione del 30/09/2026 (`Analisi_Architettura/Archivio/11`, D-49..D-56): A1
> valuta solo cio' che le fonti possono sostenere. Gap_Controlli esce dal
> modello (dato qualitativo della Banca, D-49); la Velocity e' facoltativa
> (D-50); esito e "da/a" delle variazioni li calcola lo script (D-51); la
> Probabilita ha descrittori di plausibilita' (D-52); i KRI sono da 1 a 3 con
> soglie della Banca (D-53).
>
> Revisione del responsabile del 30/09/2026 sera (D-57..D-61): descrittori di
> Impatto, Probabilita, Prossimita e Velocity riscritti; Severity si chiama
> **Impatto** (D-57); la Confidence del rischio e' sostituita dalla
> **rilevanza di ogni fonte** (D-58); Z di Mosca = meta' della fascia della
> Prossimita, scritta accanto ai descrittori (D-59); gli **anni di adeguamento** li stima A1 e li valida la
> Banca (D-60); soglia di direzione 2 e soglia del Delta 0,30 (D-61).
>
> Ancora il 30/09 sera (D-63..D-65): **livello di allerta** calcolato dal
> foglio (sezione 8), due **KRI per rischio**, uno di esposizione e uno di
> evoluzione (sezione 4), **Probabilita 4-5 solo se la Banca e' esposta**
> (sezione 1). A1 ragiona analizzando nel dettaglio ogni fonte (prompt).

## 1. Dimensioni del rischio

Interi 1-5, 5 = peggiore: scegli il descrittore piu' aderente all'evidenza, non interpolare.

### Impatto — danno se il rischio si manifesta
| Score | Descrittore |
|---|---|
| 1 | Limitato: nessun cliente toccato, perdita entro 100.000 euro. |
| 2 | Contenuto: alcuni clienti coinvolti o un processo non critico. |
| 3 | Rilevante: processo critico degradato o clientela ampia; segnalazione all'autorita' possibile. |
| 4 | Grave: interruzione di una funzione essenziale, sanzione probabile, danno reputazionale nazionale. |
| 5 | Critico: effetto sulla continuita', sui prodotti o sulla solvibilita' della Banca; intervento dell'autorita' certo. |

> D-57 (30/09/2026): "Severity" rinominata "Impatto" ovunque (schema di A1,
> registro, fogli, controlli). Un registro nato prima si aggiorna con
> `aggiorna-registro`, che copia la colonna Severity nella colonna Impatto.

### Probabilita — plausibilita' per la Banca
| Score | Descrittore |
|---|---|
| 1 | Remota: solo teorica, nessun caso noto. |
| 2 | Improbabile: casi solo in altri settori o paesi, o Banca poco esposta. |
| 3 | Possibile: casi in altri settori anche non finanziari; Banca esposta. |
| 4 | Probabile: casi ripetuti in aziende strutturate o banche, o crescita del fenomeno documentata. |
| 5 | Quasi certa: gia' osservato presso istituzioni finanziarie o la loro filiera, anche di fornitori, o fenomeno in rapida accelerazione. |

4-5 solo se la Banca e' esposta.

> D-81 (19/10/2026, analisi 17, 17.10): A1 non conosce l'esposizione interna
> (D-49) e, nel dubbio, sceglieva in silenzio il valore piu' basso: i rischi
> nuovi entravano tutti con Probabilita 3 o meno. Ora, se le fonti non dicono se
> la Banca e' esposta, A1 scrive il valore senza esposizione e la frase
> "ESPOSIZIONE NON NOTA: con l'esposizione documentata sarebbe N" (guida di
> scrittura); il controllo C5 la porta in validazione e decide il validatore.
> La frase sta nel razionale, non in un campo: l'esposizione decisa non resta
> registrata (variante 3b dell'analisi, da fare se la nota si ripete).
>
> D-65 (30/09/2026 sera): un fenomeno diffuso non e' probabile per una Banca
> che non ha il bersaglio (il prodotto, il processo o il fornitore colpito).
> I livelli 2 e 3 lo dicevano gia' ("Banca poco esposta", "Banca esposta");
> ora vale anche per 4 e 5. Niente dimensione "Esposizione" a parte: A1 non
> conosce l'esposizione interna meglio di quanto conoscesse i controlli
> (D-49); l'esposizione si misura con il KRI di esposizione (sezione 4).
>
> D-52 (30/09/2026): descrittori di plausibilita' al posto di quelli di
> frequenza ("una volta in 2-5 anni"), che per un rischio senza storia non si
> possono osservare. Riscritti dal responsabile il 30/09 sera (D-61).
> Probabilita dice QUANTO e' plausibile che il meccanismo colpisca la Banca;
> Prossimita dice QUANDO. Probabilita x Impatto e' la "magnitudo" (area del
> cerchio nel Radar_Mosca, cella della Matrice).

### Prossimita — quando puo' manifestarsi
| Score | Descrittore |
|---|---|
| 1 | Oltre 3 anni. |
| 2 | Da 2 a 3 anni. |
| 3 | Da 1 a 2 anni. |
| 4 | Entro 12 mesi. |
| 5 | In corso o imminente presso la Banca, la sua filiera o aziende ampie e complesse. |

4-5 solo con casi documentati (banca comparabile, fornitore, quasi-incidente in aziende complesse) o un evento certo; deroga, dichiarata nel razionale, per fenomeni ad altissimo impatto (es. nuovo Mythos, GenAI imprevista, superintelligenza).

> Z di Mosca per livello (D-59, 30/09/2026): e' la meta' della fascia del
> descrittore (per "oltre 3 anni", convenzionalmente 3,5):
>
> | Prossimita | Descrittore | Z (anni) |
> |---|---|---|
> | 5 | in corso o imminente | 0 |
> | 4 | entro 12 mesi | 0,5 |
> | 3 | da 1 a 2 anni | 1,5 |
> | 2 | da 2 a 3 anni | 2,5 |
> | 1 | oltre 3 anni | 3,5 |
>
> Prima del 30/09 sera la tabella era 0 / 0,5 / 1,5 / 2,5 / 4, senza
> corrispondenza scritta con i descrittori. Provato anche l'inizio della
> fascia (0 / 0 / 1 / 2 / 3): la Prossimita 4 valeva 0 come la 5 e quasi tutti
> i rischi finivano in AGIRE ORA, un'urgenza che non distingue piu' niente.
>
> D-48 (29/09/2026), qui dentro la regola: nel primo ciclo di prova A1
> assegnava 4-5 su evidenza settoriale generica ("il tema e' diffuso"). La
> deroga per i fenomeni ad altissimo impatto e' del responsabile (D-61): A5 la
> valuta in C4, e C5 la segnala come Osservazione se manca una fonte di
> rilevanza alta.

### Velocity — tempo fra innesco e pieno impatto
| Score | Descrittore |
|---|---|
| 1 | Oltre 12 mesi. |
| 2 | Da 6 a 12 mesi. |
| 3 | Da 3 a 6 mesi. |
| 4 | Da 1 a 3 mesi. |
| 5 | Entro 1 mese. |

Facoltativa: null se nessuna fonte ne documenta i tempi.

> D-50 (30/09/2026): per un rischio senza storia la Velocity era speculativa.
> Si valuta quando c'e' evidenza sui tempi e acquista peso con le iterazioni:
> una Velocity prima non valutata puo' entrare con qualunque valore (sezione
> 3, regola 2). Nel composito pesa solo quando c'e'.

### Anni di adeguamento
Facoltativo (null se non serve): anni di un adeguamento strutturale della Banca (migrazione, uscita da un fornitore) oltre le azioni; stima motivata nel razionale.

> D-60 (30/09/2026 sera): prima (D-33) era un input del validatore. Ora lo
> stima A1 dalle sue conoscenze e dalle fonti, e il validatore lo accetta o lo
> rettifica nel foglio Validazione; il valore validato va nell'anagrafica
> (Parametri, colonna M), dove resta correggibile a mano. E' la Y minima di
> Mosca (sezione 8). Una proposta null non cancella un valore gia' in
> anagrafica.
>
> Rischi in osservazione (analisi 17, 17.10, 19/10/2026): A1 stima gli anni
> di adeguamento anche per i rischi in osservazione con Impatto 4-5 (guida di
> scrittura, allegato di A1). Il valore validato resta nella riga del
> RiskRegister (l'anagrafica e' il radar) e conta nel margine di Mosca della
> regola del radar: con X + Y > Z il rischio e' AGIRE ORA ed entra nel radar
> anche con Prossimita 1. Senza, il margine usa la Y di riserva (1 anno) e un
> rischio lontano a mitigazione lunga, il caso della crittografia
> post-quantistica, non puo' risultare urgente.

> Formula (D-50, in vigore dal template del 30/09/2026): media pesata delle
> dimensioni valutate, 0,35 x Impatto + 0,25 x Probabilita + 0,20 x
> Prossimita + 0,20 x Velocity, divisa per la somma dei pesi presenti: se la
> Velocity manca, i pesi si ridistribuiscono sulle altre tre (0,4375 / 0,3125
> / 0,25). Pesi provvisori, da rivedere dopo il primo ciclo (D-20). Prima:
> D-19 con Gap_Controlli (0,30 Sev + 0,20 Prob + 0,20 Gap + 0,15 Vel + 0,15
> Pross). Il foglio ricalcola con i pesi nuovi anche i cicli passati, quindi il
> trend resta confrontabile.
> I pesi non stanno nei prompt: gli agenti non calcolano il composito (lo schema
> di A1 non ha il campo; la frase "non calcolare lo score" e' tolta il 30/09 sera
> per fare spazio).
> Perche' non l'agente: una media pesata fatta a mente sbaglia in modo plausibile, cioe'
> non rilevabile. Il foglio usa i pesi delle celle di input in Parametri.

> Gap_Controlli esce dal modello (D-49, 30/09/2026; sostituisce D-47): descrive
> lo stato dei controlli DELLA BANCA, che A1 non vede. Con poche fonti esterne
> era un pavimento (4 su 7 rischi su 7 nel ciclo di prova) e fermava A5. Resta
> come dato qualitativo della Banca, `Presidio_Controlli` nell'anagrafica
> (Parametri), deciso dal validatore: Non verificato, Adeguato, Parziale,
> Assente. Non entra nello score; si vede nel Registro e nelle schede.

## 2. Rilevanza delle fonti

Rilevanza 1-3 di ogni fonte per la previsione; stesso ente o stesso fatto = una fonte.
| Score | Descrittore |
|---|---|
| 1 | Bassa: stampa generalista, opinioni. |
| 2 | Media: fonte specializzata con dati o casi (report di settore, threat intelligence). |
| 3 | Alta: regolatore o autorita', consorzio di dati (es. ORX); caso documentato presso la Banca, una banca comparabile o un fornitore. |

Probabilita 5 o Prossimita 4-5: almeno una fonte di rilevanza 3 (salvo deroga).

> D-58 (30/09/2026 sera): la Confidence del rischio (1-5) e' tolta. Il
> responsabile preferisce vedere quanto conta ogni fonte per la previsione:
> la rilevanza sta su ogni fonte (colonna Fonti del registro, schede), non
> e' un numero del rischio e non entra nello score. I descrittori della
> Confidence del 30/09 (due o tre fonti indipendenti, una primaria) sono
> diventati questi livelli e la regola sulle valutazioni alte. C5 controlla
> date, fonti perse e la regola; il giudizio sul livello resta ad A5 (C4).
>
> D-46 (29/09/2026) e D-52 (30/09/2026): nessun livello richiede una fonte
> INTERNA. Un rischio davvero emergente non ha ancora una traccia interna (es.
> un evento tipo "Mythos", tutto annunciato da fonti esterne). "Stesso ente o
> stesso fatto = una fonte" resta il freno contro l'inflazione (regola 6,
> sezione 3): nel ciclo di prova tre report ORX contavano come tre fonti.

## 3. Regole di variazione fra cicli

1. Senza evidenza nuova il valore resta quello del ciclo precedente.
2. Al massimo un punto per dimensione fra due cicli consecutivi; una Velocity prima null entra con qualunque valore.
3. Ogni valore cambiato cita un'evidenza specifica datata dopo il ciclo precedente; frasi generiche non sono evidenza.
4. Una riduzione ha lo stesso onere di un aumento: l'Impatto scende solo se cambia il danno possibile.
5. Confermare = riprendere le fonti che giustificavano il valore; se non valgono piu', il valore va rivisto.
6. La copertura mediatica non e' evidenza.
7. Un numero nel razionale cita la sua fonte, o e' dichiarato come valutazione.

> Esito e "da/a" delle variazioni li calcola lo script dal confronto con la
> baseline (D-51): "Nuovo" se l'id non c'era, "Variato" se cambia Impatto,
> Probabilita, Prossimita o Velocity, "Confermato" altrimenti.

> Regola 7 (decisione D-36, dal 25/09/2026): separa i fatti misurati dalle
> stime. A5 la verifica nel controllo C4 (Osservazione, non Bloccante).

## 4. KRI

Due per rischio: Esposizione (quanto la Banca e' esposta) ed Evoluzione (quanto cresce il fenomeno). Valore crescente = peggio (altrimenti il complemento). fonte_dati = sistema o report dove la Banca prenderebbe il dato. Soglie solo se una fonte le sostiene, entrambe, allerta >= attenzione; altrimenti null (le fissa la Banca).

> D-64 (30/09/2026 sera, dal suggerimento di una proposta esterna): ogni
> rischio ha esattamente due KRI, assegnati da A1 con il campo `tipo`: uno di
> **esposizione** (es. quota di servizi critici su un fornitore, componenti
> fuori supporto, dipendenti non formati: di solito un dato interno, che
> fornisce la Banca) e uno di **evoluzione** (es. tentativi di frode,
> incidenti dei fornitori, vulnerabilita' senza patch: quanto il fenomeno
> cresce, anche da fonti esterne che A1 puo' rileggere). Il tipo dice anche chi
> fornisce il valore. Un KRI in vigore conserva kri_id, tipo e soglie; un
> rischio che aveva tre KRI ne ripropone due (il terzo esce di vigore, C9 lo
> segnala). Prima (D-53) erano da 1 a 3.
>
> D-53 (30/09/2026): senza dati interni fonte, soglie e valori erano inventati
> (21 KRI con soglie nel ciclo di prova). Un KRI senza soglie ha stato "Soglie
> da definire" finche' il validatore non le rettifica; le soglie validate
> restano quando A1 ripropone il KRI senza soglie. La rilettura riguarda solo
> i KRI per cui A1 trova un valore: gli altri restano "Non rilevato".

## 5. Intensita' di impatto di una notizia

Intero 0-3 per ciascuna delle nove categorie, separato dalla direzione.
| Intensita | Descrittore |
|---|---|
| 0 | Nessun nesso con la categoria. |
| 1 | Nesso indiretto o solo teorico per la Banca. |
| 2 | Nesso diretto con un meccanismo di perdita presente nella Banca. |
| 3 | Nesso diretto e immediato: evento in corso su controparti, sistemi o prodotti che la Banca usa. |

## 6. Segnali e soglia di direzione

La direzione usa solo quattro valori letterali: Peggiorativo, Migliorativo, Neutro, Non rilevante. Nessun sinonimo.
Una tendenza e' tale solo con almeno 2 segnali netti concordanti in 4 settimane sullo stesso rischio. Una notizia ripresa da piu' testate e' un solo segnale. Il superamento della soglia produce un flag proposto, mai una variazione di score: solo il ciclo trimestrale modifica uno score.

> Il foglio conta i segnali per testo esatto: un sinonimo vale zero, in
> silenzio. La soglia (2 dal 30/09 sera, D-61; prima 3) sta in una cella di
> input di Parametri.

Segnale critico: proponi un ciclo straordinario solo se una notizia (a) ha intensita' 3 su un rischio con Impatto 4 o 5, (b) riporta un evento in corso presso la Banca, un suo fornitore o una controparte, o (c) mostra una capacita' nuova di una minaccia che rende superato il descrittore vigente di un rischio. Indica i rischi e il motivo; decide la funzione di rischio.

> Proposta di ciclo straordinario (D-75, 07/10/2026): campo `proposta_straordinario`
> di A3 e sezione "Cosa suggerisco" di A4. Il ciclo straordinario (periodo
> AAAAQn-Sk) rivaluta solo i rischi indicati, con la stessa catena del trimestre;
> conta come ciclo per la regola 2 della sezione 3 (al massimo un punto per
> dimensione rispetto al periodo validato prima, trimestre o straordinario).

## 7. Parametri numerici e dove vivono

> Sezione per chi mantiene il workbook: non entra nei prompt.
>
> | Parametro | Valore iniziale | Dove |
> |---|---|---|
> | Pesi Impatto / Probabilita / Prossimita / Velocity | 0,35 / 0,25 / 0,20 / 0,20 | Parametri!B4:B7 (pesoImpatto, pesoProbabilita, pesoProssimita, pesoVelocity); somma controllata in B8 |
> | Soglia di direzione | 2 | Parametri!B11 (sogliaDirezione) |
> | Soglia di evidenziazione del Delta composito | 0,30 | Parametri!B12 (sogliaDelta) |
> | Soglie dei KRI | per indicatore; vuote = da definire | tabella tblKRI |
> | Anni alla manifestazione (Z) per Prossimita 5..1 | 0 / 0,5 / 1,5 / 2,5 / 3,5 (meta' della fascia, D-59) | Parametri, tabella "Urgenza" (anniProssimita) |
> | Livello di allerta: P x I alta (aggravante A1) | da 12 | Parametri (livelloPxI) |
> | Livello di allerta: quota di KRI in ambra o rosso (aggravante A3) | 0,5 | Parametri (livelloQuotaKRI) |
> | Livello di allerta: margine stretto (anni) | sotto 1 | Parametri (livelloMargine) |
> | Livello di allerta: segnali forti per l'Attivazione | 2 | Parametri (livelloForti) |
> | Tempo per decidere e avviare (X) | 0,25 anni (un ciclo) | Parametri (moscaX) |
> | Tempo di mitigazione senza azioni (Y di riserva) | 1 anno | Parametri (moscaYDefault) |
> | Anni di adeguamento strutturale di un rischio (Y minima) | proposto da A1, validato (D-60) | Parametri, anagrafica, colonna Anni_Adeguamento (M): la scrive la validazione, correggibile a mano |
> | Presidio dei controlli della Banca (qualitativo, D-49) | Non verificato | Parametri, anagrafica, colonna Presidio_Controlli (O), input del validatore |
> | Registro unico: capienza del radar (D-79) | 15, fino a 20 | Parametri!B66 (capienzaRadar) |
> | Registro unico: soglie di Prossimita e Probabilita per entrare nel radar | 2 e 2 | Parametri!B67:B68 (sogliaProssimitaRadar, sogliaProbabilitaRadar) |
> | Registro unico: cicli sotto la regola prima di uscire | 2 | Parametri!B69 (cicliUscitaRadar) |
> | Registro unico: rischi in osservazione al massimo | 20 (fisso) | Parametri!B70 (capienzaOsservazione); per cambiarlo, il generatore del template |

## 8. Urgenza: disuguaglianza di Mosca

> Sezione per chi legge: non entra nei prompt. L'urgenza la CALCOLA il foglio
> Radar_Mosca, nessun agente la stima.
>
> Origine. Michele Mosca (2015), per la migrazione alla crittografia
> post-quantistica: se X + Y > Z bisogna agire ORA, dove X = per quanto tempo i
> dati devono restare protetti, Y = tempo per migrare, Z = tempo prima che la
> minaccia arrivi. Se la somma dei tempi necessari supera il tempo disponibile,
> si e' gia' in ritardo.
>
> Adattamento ai rischi emergenti (scelta del pacchetto, da validare):
>
> | Termine | Significato qui | Da dove viene |
> |---|---|---|
> | Z | anni prima che il rischio possa manifestarsi | Prossimita, tramite la tabella anniProssimita di Parametri: meta' della fascia del descrittore (5 → 0, 4 → 0,5, 3 → 1,5, 2 → 2,5, 1 → 3,5; D-59) |
> | X | anni per decidere e avviare la mitigazione | parametro unico moscaX: un ciclo trimestrale (0,25) |
> | Y | anni per completare la mitigazione | il maggiore fra: orizzonte piu' lungo delle azioni del ciclo corrente non respinte (3/6/12 mesi), oppure moscaYDefault se non ce ne sono; e Anni_Adeguamento dell'anagrafica, se valorizzato |
>
> Margine = Z - (X + Y). Margine < 0: "AGIRE ORA" (X + Y > Z, gia' in ritardo).
> Da 0 a 1 anno: "Agire entro l'anno". Oltre: margine in anni.
>
> Nel radar: distanza dal centro = Margine + 2, fra 0,6 e 6 (piu' vicino al
> centro = agire prima; rischi dello stesso settore a distanze angolari uguali); area del cerchio di ogni rischio proporzionale a
> Probabilita x Impatto; angolo = settore dell'event type. Cerchi: margine 0
> (linea di Mosca, rossa), 1, 2 e 3 anni (con i parametri iniziali il margine
> massimo e' 3 anni). Colore del cerchio = livello di allerta (sotto); ◆ accanto
> all'ID = tema all'attenzione del supervisore.
>
> Anni_Adeguamento (dal 25/09/2026): le azioni hanno orizzonti di 3, 6 o 12
> mesi, ma alcuni rischi chiedono un adeguamento di anni (migrazione alla
> crittografia post-quantistica, sostituzione di sistemi legacy, uscita da un
> fornitore). Senza questo dato Y non supera un anno e l'urgenza di quei
> rischi e' sottostimata: e' il caso per cui Mosca ha scritto la
> disuguaglianza. Dal 30/09 sera (D-60) il valore lo propone A1 e lo decide il
> validatore nel foglio Validazione; la validazione lo scrive nell'anagrafica
> (Parametri, colonna M), dove resta correggibile a mano e da cui lo legge il
> Radar_Mosca. La scrittura di un ciclo non lo tocca.
>
> Limiti: Z ha cinque valori possibili (la meta' della fascia della
> Prossimita), Y viene dagli orizzonti delle azioni o dagli anni di
> adeguamento: l'urgenza e' una graduatoria ancorata, non una previsione.
> Cambiare le tabelle in Parametri cambia il radar senza toccare nessun prompt.
>
> ### Livello di allerta (D-63, 30/09/2026 sera)
>
> Lo calcola il foglio Radar_Mosca dai dati che il registro ha gia' (nessun
> campo nuovo, nessun agente): e' il colore del cerchio nel radar (rosso,
> giallo, verde), il fondo dell'ID nel Registro, il numero del Quadro e la
> colonna "Livello" dei rischi segnalati. Unisce segnali che altrimenti stanno
> in colonne diverse in una decisione con una conseguenza.
>
> | Segnali forti | |
> |---|---|
> | F1 | AGIRE ORA (X + Y > Z) |
> | F2 | almeno un KRI in rosso |
> | F3 | segnali netti delle notizie oltre la soglia di direzione (▲) |
>
> | Aggravanti (contano solo con margine stretto) | |
> |---|---|
> | A1 | Probabilita x Impatto da 12 (Parametri, livelloPxI) |
> | A2 | presidio dei controlli "Assente" |
> | A3 | meta' o piu' dei KRI in vigore in ambra o rosso (livelloQuotaKRI; con due KRI basta uno) |
>
> | Livello | Quando | Conseguenza (da decidere con la funzione di rischio) |
> |---|---|---|
> | Attivazione (rosso) | 2 o piu' segnali forti (livelloForti) | al comitato con un piano d'azione; se nasce nel settimanale, proposta di ciclo straordinario |
> | Attenzione (giallo) | 1 segnale forte, oppure margine sotto 1 anno (livelloMargine) con almeno un aggravante | l'owner conferma azioni e KRI entro il ciclo; il rischio va nel report |
> | Monitoraggio (verde) | gli altri casi | ciclo trimestrale ordinario |
>
> Due segnali forti per l'Attivazione, e un motivo di merito oltre al margine
> per l'Attenzione: un solo criterio che scatta per tutti non informa (come la
> Z all'inizio della fascia, provata e scartata). Il livello non e' uno score:
> i segnali netti cambiano ogni settimana e con loro il livello, senza
> contraddire D-41 (solo il trimestre modifica uno score). Un rischio nuovo,
> senza KRI rilevati ne' segnali, parte di solito in Monitoraggio. Tema del
> supervisore: non alza il livello (e' evidenziato a parte, ◆).

## 9. Registro unico: radar e osservazione

> D-79 (08/10/2026): sostituisce la lista di osservazione della D-73. La regola la
> applica lo script (07_Senza_Studio/radar.py), nessun agente; i parametri sono
> celle gialle di Parametri. Nessun prompt riceve questa sezione: A1 la trova
> nella guida di scrittura dell'allegato.

Il registro e' unico: tutti i rischi NFR-nn, valutati con le stesse dimensioni e lo stesso score. I primi sono nel radar di Mosca, con gestione completa (KRI, azioni, urgenza, livello di allerta, report, schede); gli altri sono in osservazione: stessa scala, niente KRI ne' azioni, rivalutati solo con evidenza nuova.

### Chi entra nel radar
1. Candidato: Prossimita almeno 2 (puo' manifestarsi entro 3 anni) e Probabilita almeno 2 (non solo teorico).
2. Sempre nel radar, anche sotto le soglie: un rischio AGIRE ORA (X + Y > Z), un tema all'attenzione del supervisore, un rischio che il validatore mette nel radar con la Motivazione. Mai nel radar: un rischio che il validatore mette in osservazione con la Motivazione.
3. Se i candidati superano i posti (capienza del radar, 15 all'inizio, fino a 20): prima le eccezioni, poi i piu' alti per score composito; gli altri restano in osservazione "fuori per capienza".
4. Un rischio del radar che non soddisfa piu' la regola resta un ciclo come "Radar, in uscita" e passa in osservazione solo se lo e' anche al ciclo dopo. Un rischio che sale entra subito, con i due KRI e le azioni.

### In osservazione
Al massimo 20 rischi. Oltre alle quattro dimensioni: l'orizzonte in anni (la Prossimita non distingue oltre i 3 anni) e il segnale di avvicinamento, il fatto osservabile che lo farebbe salire. Sono note: non entrano nello score.
