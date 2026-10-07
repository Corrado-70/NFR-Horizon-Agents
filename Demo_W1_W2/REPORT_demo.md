# Demo W1 e W2 — cosa produce ogni agente, e cosa decide il validatore

Sequenza eseguita la prima volta il 23/09/2026 e **rilanciata il 07/10/2026**
sul pacchetto con la struttura 2026-10-07: **knowledge di A7** (D-72: dopo ogni
`trimestrale` e `valida` la cartella `Archivio_Cicli/Spiegazioni`, qui nella cartella di uscita perche' il
kernel e' quello del pacchetto, con `Ciclo.txt` e `Rischio_01..20.txt`; i fenomeni non censiti da A1 nel
2026Q4; Note dell'analista nel Quadro, vuote nella demo); **A5 facoltativo e segnalazioni in
validazione** (D-71: il ciclo si ferma solo per difetti di integrita' e
`trimestrale` scrive il messaggio per A1; il 2026Q4 si scrive senza A5; le
regole di metodo e i rilievi di A5 vanno nella colonna Segnalazioni della
griglia); il precontrollo stampa l'**impronta** dell'output di A1 (D-70); **allegato di A1 e
precontrollo** (D-69: A1 riceve baseline, controlli di A5 e guida di scrittura
in `Input_A1_<ciclo>.txt`; il comando `precontrollo` controlla l'output di A1
prima di A5 e scrive il messaggio di correzione; A1 propone azioni nuove);
**schede con il perche' di ogni
numero** (D-68: razionale di A1 in parti, effetto atteso di azioni e KRI);
**validazione in una griglia**, una
riga per rischio, KRI, azione e notizia, con le celle gialle gia' compilate e
Score e Margine di Mosca calcolati mentre si scrive (D-67); sintesi settimanale di A3 e flag nel foglio **Sintesi_Settimane** e nel foglio Notizie (D-66); **livello di allerta** nel radar
(D-63: rosso Attivazione, giallo Attenzione, verde Monitoraggio, calcolato dal
foglio), **due KRI per rischio**, uno di esposizione e uno di evoluzione
(D-64), Probabilita 4-5 solo con la Banca esposta (D-65); rubrica rivista dal
responsabile (D-57..D-62: **Impatto** al posto di Severity, niente Confidence e
**rilevanza 1-3 di ogni fonte**, **anni di adeguamento** stimati da A1 e
validati, Z di Mosca a meta' della fascia della Prossimita, comando **`report`**
per il PDF); scoring semplificato (D-49..D-56:
niente Gap_Controlli, presidio dei controlli della Banca, Velocity
facoltativa, pesi D-50, esito e "da/a" calcolati dallo script, KRI con soglie
della Banca), registro e report in un solo file (D-39), schede in un file a
parte (D-40). Si rilancia con `python esegui_demo.py` (circa 7 minuti).

| # | Passo | Periodo | Esito |
|---|---|---|---|
| 0 | W0 raccolta notizie, **reale** (rete vera, feed di oggi) | settimana del 28/09/2026 | 144 notizie da 17 delle 18 fonti interrogate, tutte raggiungibili |
| 1 | Precontrollo e W1 con un output di A1 difettoso | 2026Q3 | **fermato** dal precontrollo (2 punti da correggere: un KRI con l'identificativo di un altro rischio; messaggio per A1 in `Correzione_A1_2026Q3.txt`), poi anche da `trimestrale`, che riscrive lo stesso messaggio; registro intatto |
| 2 | Precontrollo e W1 con l'output corretto | 2026Q3 | precontrollo: 0 punti da correggere, 13 da verificare (1 osservazione, 12 punti di forma: razionale scritto prima del 02/10); scritto, 12/12 rischi |
| 3 | W1 del trimestre dopo, **prima** di validare | 2026Q4 | **fermato**: 52 righe ancora da validare |
| 4 | Validazione nella griglia | 2026Q3 | 52 righe: 47 accettate (non toccate), 4 rettificate (5 valori), 1 respinta |
| 5 | W2 + validazione delle notizie | settimana del 12/10/2026 | 5 notizie, 1 segnale rettificato; sintesi di A3 e 1 flag in Sintesi_Settimane e nel foglio Notizie |
| 6 | W3 su richiesta (A4) | 12/10/2026 | parere su una notizia |
| 7 | Precontrollo, W1 **senza A5** + validazione | 2026Q4 | precontrollo: nessun rilievo; scritto senza A5 ("A5: non usato (facoltativo)"), 13/13 rischi (uno nuovo); tutto accettato (53 righe della griglia non toccate) |
| 8 | Schede dei rischi | 2026Q4 | `Schede_2026Q4.xlsx`, 13 schede, senza A6 (testi del registro) |
| 9 | Report al comitato (`report`) | 2026Q4 | `Report_comitato_2026Q4.pdf`, 12 pagine: Quadro (2, scala adattata al 69% per gli 8 rischi segnalati), Classifica, Radar_Mosca, Matrice, Delta (2), Metodologia (5) |
| 10 | Correzione manuale del validatore e report rigenerato (`report --con-lavoro`) | 2026Q4 | presidio di NFR-02 da Non verificato a Parziale; PDF di 14 pagine (piu' Registro e Parametri, una pagina ciascuno in orizzontale); la versione di prima resta come `Report_comitato_2026Q4_<data>.pdf` |

> **Chi ha fatto cosa.** Gli output degli agenti (A1, A3, A4, A5, cartella
> `1_Input_agenti`) e le decisioni del validatore
> (`Decisioni_validatore_*.json`) li ho scritti io, Claude, seguendo prompt e
> regole: sono **simulati**. Lo script, i controlli e l'Excel girano
> **davvero**; la raccolta W0 ha scaricato davvero i feed del 02/10/2026 (rilancio della sera).
> Le notizie della settimana del 12/10 restano simulate: la demo si svolge
> nel futuro (2026Q3-Q4). L'output di **A6 non e' simulato** nella demo: le
> schede escono con i testi di A1 dal registro; i controlli su A6 li prova il
> collaudo (`run_catena.py`, passo 2c).

---

## Il registro di partenza: 12 rischi

Il template ha 12 rischi di esempio su tre cicli (2025Q4-2026Q2). Nessuno su
L1-03 (rapporti di impiego): e' l'area che la catena scopre con A3 e copre nel
2026Q4. NFR-01, 02, 07 e 09 sono temi all'attenzione del supervisore (◆,
anche nel radar accanto all'ID); due KRI per rischio, uno di esposizione e uno
di evoluzione (NFR-02: K1 quota dei servizi critici sul cloud, K2 incidenti dei
fornitori cloud); NFR-11 ha 3 anni di adeguamento strutturale (sistemi
di pagamento legacy), nella colonna dell'anagrafica. Presidio dei controlli (giudizio della Banca, fuori
dallo score): Adeguato NFR-05, Parziale NFR-01, 07, 12, Assente NFR-06, 11,
gli altri Non verificato. NFR-10 ha la Velocity non valutata (nessuna fonte
ne documenta i tempi); NFR-10-K1 non ha soglie ("Soglie da definire"); nel
2026Q2 NFR-12 ha una segnalazione da motivare (un Bloccante di A5 portato in
validazione, D-71), decisa con una motivazione.

---

## W0 — raccolta notizie (reale)

`raccogli_notizie.py --anche-da-validare` ha scritto
`News_Inbox/2026-09-28/Raccolta_2026-10-02.txt`: una voce per notizia, ognuna
con il **codice fonte** che A3 riporta. Estratto:

```text
Finestra: dal 2026-09-25 al 2026-10-02. Fonti interrogate: 18; con notizie: 17; notizie: 144.
== FNT-01 BCE Vigilanza bancaria, comunicati ==
- [FNT-01] 2026-10-01 | Patrick Montagner: Remaining vigilant in a changing risk environment
- [FNT-01] 2026-10-01 | Pedro Machado: The exit test: why the single market in banking depends on how banks fa...
- [FNT-01] 2026-09-30 | Sharon Donnery: Interview with banko.ro
```

---

## W1 — ciclo 2026Q3

**A1** (`A1_2026Q3.json`, formato del 30/09 sera: niente esito, niente
"da/a", niente confidence): 12 rischi. Cambia un valore solo per NFR-03
(Prossimita 3→4 dopo una sanzione a una banca comparabile): **lo script** lo
scrive "Variato" e aggiunge "da 3 a 4". Ogni fonte ha la sua rilevanza (30 di
rilevanza 3, 2 di rilevanza 2): ogni rischio con Prossimita 4 ha almeno una
fonte di rilevanza 3. Anni di adeguamento stimati solo per NFR-11 (3); per gli
altri null (non serve un adeguamento strutturale). NFR-10 lascia la Velocity non
valutata; NFR-10-K1 e' proposto senza soglie e NFR-03-K1 e' riproposto senza
soglie (restano quelle in vigore). 15 azioni, **due KRI per rischio con il
tipo** (Esposizione, Evoluzione); NFR-02-K2 (evoluzione) e' sostituito da un
KRI nuovo dello stesso tipo, che diventa NFR-02-K3; rilettura dei KRI di cui
trova un valore. Il
commento per il comitato ha la forma "MESSAGGIO: ... DECISIONI: ..." e
dichiara l'event type senza rischi (L1-03).

**A5**: Approvato, con un'osservazione C5 (Fonti) su NFR-06: "fonti interne e
recenti; manca un riscontro esterno sul fenomeno".

**Allegato di A1** (D-69): il comando `baseline` scrive accanto alla baseline
`Input_A1_2026Q3.txt` (copia in `1_Input_agenti`): la baseline, i nove
controlli di A5 con le stesse parole del suo prompt e la guida di scrittura con
l'esempio. In Banca e' il file da allegare ad A1.

**Tentativo con un A1 difettoso**: un KRI di NFR-01 con l'identificativo di
NFR-02 (difetto di integrita') e un'evidenza generica su NFR-03 (regola di
metodo). Il **precontrollo** (pochi secondi, senza Excel) lo ferma per il
primo e scrive il messaggio da incollare nella chat di A1:

```
Precontrollo dell'output di A1 (2026Q3): 2 punti da correggere, 15 da verificare.
Impronta dell'output di A1: 10d39b80ce9e
Messaggio per A1: ...\Archivio_Cicli\Cicli\2026Q3\Correzione_A1_2026Q3.txt

Da correggere (fermerebbero il ciclo):
1. NFR-01 · C9: KRI NFR-02-K1 appartiene a un altro rischio.
2. ciclo · C9: kri_id NFR-02-K1 usato piu' di una volta.

Da verificare (correggi se fondati; se confermi, spiega il perche' nel razionale):
1. NFR-01 · C9: KRI in vigore non riproposti, escono di vigore: NFR-01-K1.
2. NFR-02 · C9: KRI in vigore non riproposti, escono di vigore: NFR-02-K2.
3. NFR-03 · C3: Evidenza su prossimita generica (contesto in evoluzione, maggiore attenzione mediatica): serve un fatto specifico.

Forma dei testi (serve alle schede dei rischi):
[... una riga per ciascuno dei 12 rischi: i dati del 2026Q3 sono nel formato di prima del 02/10]
```

Lanciato comunque (per mostrarlo), anche `trimestrale` si ferma, solo per il
difetto di integrita', e riscrive lo stesso messaggio per A1:

```
FERMATO — il workbook non e' stato modificato.
Ciclo da rivedere (difetti che renderebbero incoerente il registro):
  - C9 NFR-01 KRI NFR-02-K1 appartiene a un altro rischio.
  - C9  kri_id NFR-02-K1 usato piu' di una volta.
Messaggio per A1: ...\Archivio_Cicli\Cicli\2026Q3\Correzione_A1_2026Q3.txt
```

L'evidenza generica di NFR-03 da sola non avrebbe fermato il ciclo (D-71):
sarebbe arrivata al validatore come segnalazione da motivare, nella colonna
Segnalazioni della griglia.

**Con l'A1 corretto**: il precontrollo dice `0 punti da correggere, 13 da
verificare` ("Nessun punto ferma il ciclo: si puo' lanciare trimestrale"), con
un'impronta diversa (`bbf341c797d2`): e' un altro output; poi
`Ciclo 2026Q3 scritto: 12/12 rischi, zero errori di
formula`; 25 righe di storico KRI (24 in vigore e quella di NFR-02-K2 che esce); e l'invito a validare.
Nei dati di prova A1 non ripropone piu' le azioni gia' aperte: dove prima le
ripeteva propone il passo successivo (NFR-11: isolare le componenti fuori
supporto, mentre la loro sostituzione, approvata nel 2026Q2, e' in corso).

## Il ciclo dopo non parte senza validazione

```
FERMATO — il workbook non e' stato modificato.
Il ciclo precedente 2026Q3 non e' ancora validato: 52 righe da validare nel foglio Validazione. Validarlo prima (comando valida): un ciclo nuovo non si costruisce su valutazioni non accettate.
```

52 = 12 rischi + 25 KRI + 15 azioni: una riga della griglia per oggetto. Dietro
ci sono 165 valori proposti (12 x 5 campi: Impatto, Velocity, Prossimita,
Probabilita, Anni di adeguamento; 25 x 3; 15 x 2), che `valida` registra uno per
uno nel foglio dati Storico_Validazioni. La fascia blu in cima a ogni foglio
dice "da validare" finche' non si decide.

## Validazione del 2026Q3

Il validatore (Comitato Rischi) ha cambiato nella griglia sei celle, con la
Motivazione, e non ha toccato le altre righe, che valgono come accettate. La
griglia compilata, prima di `valida`, e' in
[Grafici/Validazione_2026Q3.pdf](Grafici/Validazione_2026Q3.pdf) (tre pagine
A4 orizzontali: le celle cambiate sono arancio; nelle righe dei rischi Score e
Margine di Mosca ricalcolati, con "(era …)" dove la validazione li cambia: NFR-06
da 0,75 a 0,25 per l'anno di adeguamento, NFR-08 da 1,00 a 0,25 perche' la sua
azione e' respinta). Le decisioni:

| Oggetto | Campo | Proposta dell'agente | Decisione | Valore validato | Motivazione |
|---|---|---|---|---|---|
| Rischio NFR-06 | Anni_Adeguamento | (nessuna stima) | Rettificato | 1 | Estendere il DLP e rivedere i profili di accesso ai servizi di AI richiede circa un anno di lavori |
| Rischio NFR-10 | Velocity | (non valutata) | Rettificato | 3 | Il registro reclami mostra che le risposte errate arrivano ai clienti in giorni |
| KRI NFR-10-K1 | Soglia_Attenzione, Soglia_Allerta | (vuote) | Rettificato | 2 e 5 | Soglie fissate dalla funzione di rischio sullo storico reclami |
| KRI NFR-01-K1 | Valore_Corrente | 5,1 | Rettificato | 5,3 | Dato definitivo del report antifrode di ottobre |
| Azione 2026Q3-NFR-08-A1 | (intera) | proposta | Respinto | — | Gia' prevista dal piano IAM: azione duplicata |

Risultato: `Validazione del periodo 2026Q3 applicata: 52 righe — accettate 47,
rettificate 4 (5 valori cambiati), respinte 1`. NFR-06 ha 1 anno di
adeguamento, scritto da `valida` nell'anagrafica (Parametri, colonna M), senza
variazioni ne' cambio di esito: non e' una dimensione, ma allunga la Y
dell'urgenza; NFR-10 ha Velocity 3, con la
variazione "da n.v. a 3" che cita la motivazione, ed e' "Variato"; NFR-10-K1
esce da "Soglie da definire"; il KRI NFR-01-K1 vale 5,3; l'azione e'
"Respinta" e non entra nell'urgenza. Il Quadro del 2026Q3 avvisa ("Dopo il
commento") che il commento di A1 precede 6 rettifiche o respingimenti. La
baseline del 2026Q4 parte dai valori **validati**.

---

## W2 — settimana del 12/10/2026

| Notizia | Codice fonte | Rischio | Segnale | Impatti principali (0-3) |
|---|---|---|---|---|
| Sciopero nazionale e carenza di tecnici IT | FNT-17 ANSA | **nessuno** | Peggiorativo | L1-03: 2, L1-06: 1, L1-07: 1 |
| Frode con voce clonata del direttore finanziario | FNT-18 Sole 24 Ore | NFR-01 | Peggiorativo | L1-02: 3, L1-04: 1 |
| Kit di clonazione vocale in vendita | FNT-34 CERTFin (Manuali) | NFR-01 | Peggiorativo | L1-02: 2 |
| Nuova region italiana del fornitore cloud | MAN (comunicato del fornitore) | NFR-02 | Neutro → **Migliorativo** (rettificato) | L1-06: 1 |
| Rimborso obbligatorio delle frodi APP dal 2027 | FNT-03 EBA | NFR-01 | Peggiorativo | L1-02: 2, L1-04: 2 |

Script: segnali netti **▲ +3 per NFR-01** (colonna "Segnali netti" del
Registro), **L1-03 AREA NON PRESIDIATA** (foglio Notizie):

![Notizie per event type nella settimana del 12/10: L1-03 non presidiata](Grafici/Notizie_settimana_2026-10-12.png)

**Sintesi della settimana** (D-66): lo script scrive la sintesi di A3 e il
flag proposto nel foglio dati **Sintesi_Settimane** (una riga per settimana,
accanto a quelle d'esempio del template) e il foglio Notizie le mostra in un
riquadro a destra della tabella:

> Settimana dominata da nuove frodi con voce sintetica (tre notizie concordanti
> su NFR-01) e da una vertenza sindacale nazionale del settore con carenza di
> tecnici IT: nessun rischio del registro copre i rapporti di impiego (L1-03),
> possibile area non presidiata.
>
> Flag: NFR-01 · Peggiorativo: l'obbligo di rimborso delle frodi APP dal 2027
> sposta la perdita sulla Banca; il descrittore di impatto 4 potrebbe non
> bastare. Da valutare nel prossimo ciclo trimestrale.

Validazione della settimana (5 righe nella sezione Notizie della griglia): il
segnale della notizia sulla region e' rettificato in Migliorativo, le altre
righe non toccate valgono come accettate; segnali netti, foglio Notizie
e livello di allerta contano il valore validato (NFR-02: ● -1). Il collaudo
lo verifica anche per una notizia respinta (passo 3b).

## W3 — A4 su richiesta

Parere in `A4_parere_esempio.md` sulla notizia del rimborso obbligatorio:
nessuno score proposto, nessuna persona nominata, nessuna scrittura.

---

## W1 — ciclo 2026Q4, validazione, schede e report

A1 propone **NFR-13 "Vertenze e carenza di competenze in funzioni IT
critiche"** su L1-03 (recepisce l'area scoperta segnalata da A3), alza la
Prossimita di NFR-01 4→5 dopo i primi casi su clienti della Banca, conferma
gli altri undici; nessuna azione ripete un'azione aperta. Il precontrollo dice
"nessun rilievo": razionale in parti ed EFFETTO in tutte le azioni e i KRI.
Scritto: 13/13 rischi, 26 KRI in vigore (NFR-13 nasce con
un KRI di esposizione, ruoli IT critici senza sostituto, e uno di evoluzione,
turnover del personale IT). Validazione: 53 righe della griglia (171 valori
proposti), tutte accettate senza toccarle. **L1-03 diventa "Presidiata"**. Il commento di A1
di questo ciclo e' nella forma vecchia (senza marcatori): il Quadro lo mette
tutto nel "Messaggio chiave" e scrive "—" nelle decisioni.

### Quadro d'insieme (prima pagina del report)

Cinque numeri: **13** rischi valutati su 13 (completo); livello di allerta
**2 · 5** (in attivazione NFR-01 e NFR-11; 6 in monitoraggio); **1 · 1**
variati · nuovi rispetto al 2026Q3; **2** KRI in rosso su 26 in vigore;
validazione ✓. Rischi segnalati a pagina 2, otto, ciascuno con il livello e il
perche' calcolato dal foglio: NFR-01 (Attivazione: 1° per score, AGIRE ORA,
variato, supervisore, KRI rosso, notizie in peggioramento), NFR-07 e NFR-12
(Attenzione: 2° e 3° per score, margine sotto l'anno con P x I alta e KRI in
ambra), NFR-03, NFR-04 e NFR-06 (Attenzione: margine sotto l'anno con KRI in
ambra o, per NFR-06, presidio assente), NFR-13 (nuovo, Monitoraggio), NFR-11
(Attivazione: AGIRE ORA con X + Y = 3,25 anni, 3 di adeguamento strutturale,
contro Z = 1,5, e un KRI in rosso). Con otto rischi segnalati la seconda pagina
non bastava: lo script riduce la scala del Quadro (69%) perche' resti in due
pagine. La riga "Segnalazioni da motivare" e' vuota: in questo ciclo non ce ne
sono, e il controllo dice "A5 non usato in questo ciclo" (D-71).

![Radar di Mosca nel Quadro: colore = livello di allerta, ◆ = supervisore](Grafici/Quadro_radar.png)

### Registro (foglio di lavoro, "il ciclo corrente")

Righe 4-5: "Ciclo validato", "Ciclo completo" 13 su 13. Il fondo dell'ID e' il
colore del livello di allerta (nessuna colonna in piu'). Un rischio per riga,
dal piu' alto per score (1-5, 5 = peggiore; pesi D-50: 0,35 Impatto, 0,25
Probabilita, 0,20 Prossimita, 0,20 Velocity). Presidio dopo la correzione
manuale del passo 10:

| ID (livello) | Imp | Prob | Pross | Vel | Score | Δ | Δ 6 mesi | Urgenza | ◆ | KRI R/A/V | Segnali | Presidio |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| NFR-01 (Attivazione) | 4 | 4 | 5 | 5 | 4,40 | +0,20 | +0,20 | AGIRE ORA | ◆ | 1/0/1 | ▲ +3 | Parziale |
| NFR-07 (Attenzione) | 4 | 3 | 3 | 5 | 3,75 | 0 | 0 | Entro l'anno | ◆ | 0/1/1 | ● 0 | Parziale |
| NFR-12 (Attenzione) | 3 | 4 | 4 | 4 | 3,65 | 0 | 0 | Entro l'anno |  | 0/1/1 | ● 0 | Parziale |
| NFR-02 (Monitoraggio) | 4 | 2 | 3 | 4 | 3,30 | 0 | 0 | Margine 1 anno | ◆ | 0/1/1 | ● -1 | Parziale (era Non verificato) |
| NFR-03 (Attenzione) | 3 | 3 | 4 | 2 | 3,00 | 0 | +0,20 | Entro l'anno |  | 0/2/0 | ● 0 | Non verificato |
| NFR-05 (Monitoraggio) | 3 | 3 | 3 | 3 | 3,00 | 0 | 0 | Margine 1 anno |  | 0/0/2 | ● 0 | Adeguato |
| NFR-06 (Attenzione) | 3 | 3 | 3 | 3 | 3,00 | 0 | 0 | Entro l'anno |  | 0/0/2 | ● 0 | Assente |
| NFR-10 (Monitoraggio) | 3 | 3 | 3 | 3 | 3,00 | 0 | 0 | Margine 1 anno |  | 0/2/0 | ● 0 | Non verificato |
| NFR-13 (Monitoraggio) | 3 | 3 | 3 | 3 | 3,00 | nuovo | nuovo | Entro l'anno |  | 0/0/0 | ● 0 | Non verificato |
| NFR-09 (Monitoraggio) | 4 | 2 | 2 | 3 | 2,90 | 0 | 0 | Margine 1,3 anni | ◆ | 0/2/0 | ● 0 | Non verificato |
| NFR-04 (Attenzione) | 3 | 3 | 3 | 2 | 2,80 | 0 | 0 | Entro l'anno |  | 0/1/1 | ● 0 | Non verificato |
| NFR-11 (Attivazione) | 3 | 3 | 3 | 2 | 2,80 | 0 | 0 | AGIRE ORA |  | 1/1/0 | ● 0 | Assente |
| NFR-08 (Monitoraggio) | 3 | 2 | 3 | 3 | 2,75 | 0 | 0 | Margine 1 anno |  | 0/0/2 | ● 0 | Non verificato |

NFR-10: Δ 0 anche se nel 2026Q3 la Velocity e' passata da non valutata a 3
(il composito del 2026Q2 era calcolato su tre dimensioni: 3,00 in entrambi i
cicli). La colonna Rilievi e' vuota nel 2026Q4.

### Classifica e lente di Mosca

![Classifica: 2 da affrontare subito (AGIRE ORA), NFR-01 e NFR-11](Grafici/Classifica.png)
![Lente di Mosca: chi e' in ritardo, e di quanto](Grafici/Lente_Mosca.png)

### Radar_Mosca: quanto presto agire, quanto e' grande

Z = anni prima che il rischio possa manifestarsi (dalla Prossimita, a meta'
della fascia del descrittore: 5 → 0, 4 → 0,5, 3 → 1,5, 2 → 2,5, 1 → 3,5); X =
0,25 anni per decidere e avviare; Y = orizzonte piu' lungo delle azioni non
respinte o, se maggiori, gli anni di adeguamento. Agire ora se X + Y > Z.
Risultato: 2 AGIRE ORA, 6 entro l'anno, 5 con almeno un anno di margine (con
Z all'inizio della fascia, provata e scartata, nessun rischio avrebbe avuto
un anno di margine).

**Livello di allerta** (colonne U-AB, colore dei cerchi): **Attivazione**
NFR-01 (AGIRE ORA, KRI in rosso, notizie in peggioramento) e NFR-11 (AGIRE ORA,
KRI in rosso); **Attenzione** NFR-03, 04, 06, 07, 12 (margine sotto l'anno con
un aggravante: KRI in ambra, P x I da 12 o presidio assente); **Monitoraggio**
gli altri sei, fra cui NFR-13 appena nato (KRI non ancora rilevati) e NFR-02,
tema del supervisore ma con un anno di margine. L'urgenza da sola mette sei
rischi "entro l'anno"; il livello ne separa cinque da seguire e uno no.

| ID | Impatto | Probabilita | P x I | Z | X | Y | Margine | Urgenza |
|---|---|---|---|---|---|---|---|---|
| NFR-01 | 4 | 4 | 16 | 0 | 0,25 | 0,25 | -0,50 | **AGIRE ORA** |
| NFR-11 | 3 | 3 | 9 | 1,5 | 0,25 | 3 | -1,75 | **AGIRE ORA** (adeguamento di 3 anni) |
| NFR-03, 12 | 3 | 3-4 | 9-12 | 0,5 | 0,25 | 0,25 | 0,00 | Agire entro l'anno |
| NFR-06 | 3 | 3 | 9 | 1,5 | 0,25 | 1 | 0,25 | Agire entro l'anno (adeguamento di 1 anno, validato) |
| NFR-04, 07, 13 | 3-4 | 3 | 9-12 | 1,5 | 0,25 | 0,5 | 0,75 | Agire entro l'anno |
| NFR-02, 05, 08, 10 | 3-4 | 2-3 | 6-9 | 1,5 | 0,25 | 0,25 | 1,00 | Margine 1 anno |
| NFR-09 | 4 | 2 | 8 | 2,5 | 0,25 | 1 | 1,25 | Margine 1,3 anni |

![Radar di Mosca: vicino al centro = agire prima; area = probabilita x impatto; colore = livello di allerta; ◆ = attenzione del supervisore](Grafici/Radar_Mosca.png)

### Delta, Storico, Indicatori, Notizie

Delta: 1 in aumento (NFR-01, +0,20: Prossimita 4 → 5), 0 in diminuzione, 11
invariati, con il motivo di ciascuno a fianco; sotto, la scala calcolata dai
pesi (con Velocity: Impatto ±0,35 ... Velocity ±0,20; senza: Impatto ±0,44
...); nessuna variazione supera la soglia di evidenziazione (0,30). Indicatori: 26 KRI in vigore, due per rischio — 11 Verde, 11 Ambra, 2 Rosso, 2 Non
rilevato (i due di NFR-13, appena nati), 0 Soglie da definire (le soglie di
NFR-10-K1 le ha fissate il validatore nel 2026Q3); colonna Tipo accanto.

| KRI | Tipo | Soglie | Valore 2026Q4 | Stato | 2026Q3 (validato) | Tendenza |
|---|---|---|---|---|---|---|
| NFR-01-K1 Tentativi di frode APP /10k | Evoluzione | 3 / 6 | 6,4 | Rosso | 5,3 | ▲ peggiora |
| NFR-01-K3 Tempo medio di blocco di un beneficiario fraudolento | Esposizione | 4 / 12 | 3,5 | Verde | 3 | ▲ peggiora |
| NFR-02-K1 Servizi critici sul cloud principale | Esposizione | 60 / 75 | 70 | Ambra | 72 | ▼ migliora |
| NFR-02-K3 Interruzioni di servizi critici presso il fornitore (nato nel 2026Q3) | Evoluzione | 1 / 3 | 0 | Verde | — | |
| NFR-11-K2 Vulnerabilita' senza patch sui sistemi legacy | Evoluzione | 2 / 6 | 6 | Rosso | 5 | ▲ peggiora |
| NFR-13-K1 Ruoli IT critici senza sostituto (nato nel 2026Q4) | Esposizione | 3 / 6 | — | Non rilevato | — | |

![Delta 2026Q4 contro 2026Q3](Grafici/Delta.png)
![Storico su otto cicli](Grafici/Storico.png)
![Storia di NFR-01-K1](Grafici/Indicatori_KRI_NFR-01-K1.png)
![Storia di NFR-02-K2, uscito nel 2026Q3](Grafici/Indicatori_KRI_NFR-02-K2.png)
![Notizie delle ultime 4 settimane per event type, dopo il 2026Q4: L1-03 ora presidiata](Grafici/Notizie.png)

### Schede dei rischi e report al comitato

`schede-input` ha scritto `Schede_input_2026Q4.json` (13 rischi in ordine di
classifica, con valori validati, urgenza, livello di allerta con il motivo,
storia e KRI con il tipo); `schede`, senza
l'output di A6, ha prodotto `Schede_2026Q4.xlsx`: indice e una scheda per
rischio. Dal 02/10 (D-68) l'output di A1 del 2026Q4 ha il razionale diviso in
parti, quindi ogni scheda ha, in quest'ordine: il rischio; il **Razionale**,
cioe' il fenomeno in termini di rischio (per NFR-11: componenti senza
supporto e competenze in calo, una vulnerabilita' sfruttata o un guasto non
riparabile, pagamenti degradati o fermi); la tabella dei valori con, accanto a
ognuno, **il perche' e il documento** (Impatto 3: "Rilevante. L'Inventario
delle componenti fuori supporto (IT) riguarda il sistema di pagamento..."); l'urgenza
con il motivo dei 3 anni di adeguamento; cosa e' cambiato; l'andamento; le
fonti; le **azioni** e i **KRI in vigore**, ognuno con "Perche'" ed "Effetto
atteso". Per NFR-11 le azioni sono tre e diverse, una per ciclo (prima della
D-69 erano tre volte la stessa): la sostituzione delle componenti fuori
supporto (2026Q2), il loro isolamento in rete (2026Q3), il supporto esteso del
produttore (2026Q4, con il perche' che richiama le due precedenti). Le azioni
ancora aperte dei cicli 2026Q2 e 2026Q3 hanno il razionale
scritto prima, senza EFFETTO: la scheda dice "non indicato nel razionale di
A1". Anche i razionali dei dati del 2026Q3 sono nel formato vecchio: per quel
ciclo `trimestrale` stampa l'avviso "il razionale ... non e' diviso in parti".
Con A6 le stesse schede avrebbero la descrizione estesa e i perche' riscritti
per chi non conosce il tema, e a cosa serve ogni fonte. Il report al comitato lo scrive il
comando `report`: `Report_comitato_2026Q4.pdf`, i sei fogli da Quadro a
Metodologia del registro validato.

**Correzione manuale e report rigenerato** (D-62): dopo la validazione il
validatore cambia a mano, nel registro, il presidio dei controlli di NFR-02
(da Non verificato a Parziale). `report --con-lavoro` rigenera il PDF dal
registro com'e' ora: 14 pagine, con in coda Registro e Parametri, ciascuno in
una pagina in orizzontale con tutte le colonne. Il PDF di prima resta come
`Report_comitato_2026Q4_<data e ora>.pdf`.

---

## Cosa la demo non mostra (ma il collaudo si')

La demo parte dal template con i dati di esempio. Il **primo uso reale**
(`inizializza`: registro vuoto, primo ciclo con tutti i rischi nuovi), la
**dismissione di un rischio** (`dismetti`), l'**aggiornamento di un registro
vecchio** (`aggiorna-registro`, anche dal 2026-09-25c con le colonne dismesse),
l'opzione **`--procedi-con-rilievi`** (passo 12) e i **controlli sull'output di A6** (rischio
mancante, fonte cambiata, numero inventato) sono provati dalla catena di
collaudo (`99_Collaudo/run_catena.py`), insieme ai casi di errore (esito di A5
di un altro ciclo, titoli che iniziano con "=", file non JSON o con BOM).

## Dove sono i file

```text
Demo_W1_W2/
  NFR_Registro.xlsx                     registro VIVO: cresce a ogni run
  News_Inbox/2026-09-28/                raccolta REALE dai feed + Manuali/
  1_Input_agenti/                       output simulati degli agenti, decisioni simulate del validatore, baseline date agli agenti,
                                        allegati di A1 Input_A1_2026Q3.txt e Input_A1_2026Q4.txt
  A4_parere_esempio.md                  parere di A4
  Archivio_Cicli/
    Baseline_corrente.json / .txt       input degli agenti per il prossimo run (valori validati)
    Input_A1_2027Q1.txt                 allegato di A1 per il prossimo ciclo (baseline, controlli, guida)
    Cicli/2026Q3/                       NFR_Registro_2026Q3.xlsx (appena scritto) e NFR_Registro_2026Q3_validato.xlsx,
                                        A1, A5, baseline usata, esito dei controlli, righe liste, Validazione_2026Q3.json,
                                        Correzione_A1_2026Q3.txt (ultimo messaggio del precontrollo per A1)
    Cicli/2026Q3/tentativo_<ora>/       ogni tentativo, anche quello fermato
    Cicli/2026Q4/                       idem per il 2026Q4, piu' Schede_input_2026Q4.json, Schede_2026Q4.xlsx,
                                        Report_comitato_2026Q4.pdf e la versione precedente con data e ora
    Settimane/2026-10-12/               Excel della settimana, validato, output di A3, Validazione_2026-10-12.json
    Backup/                             il registro vivo prima di ogni scrittura
  Grafici/                              immagini esportate dall'Excel finale e Validazione_2026Q3.pdf (la griglia compilata prima di valida)
```
