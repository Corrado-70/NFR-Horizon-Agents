# 19. Confronto con una proposta esterna di osservatorio NFR con agenti

Data: 30/10/2026. Richiesta dell'utente: valutare punto per punto una proposta di una societa' di consulenza (23 slide,
bozza dell'ottobre 2026) sulla stessa attivita' del pacchetto, poi rileggere tutto in modo critico. Il documento
originale non e' nel repository (e' di un terzo): qui i contenuti sono riassunti con parole nostre. Le osservazioni
sono state riportate anche come note sulle slide, in due copie del file (interna e per i consulenti), consegnate in
chat il 30/10.

Indicazioni dell'utente dopo la prima stesura: **scale a 6 livelli date per assodate**; **nessuna conversione dello
storico, si riparte da zero**; forma schematica.

## 19.0 In breve

- **Base comune.** Coincidono alla lettera con il pacchetto: pesi 0,35 / 0,25 / 0,20 / 0,20 (e 0,4375 / 0,3125 / 0,25
  senza Velocity), otto codici DRV-*, livelli Monitoraggio / Attenzione / Attivazione, "QUANTO / QUANDO", "aziende
  ampie e complesse". Compatibilita' alta per costruzione.
- **Le loro aggiunte**: scale a 6 livelli, alberi decisionali con un "decision model" a regole, rischio residuo,
  agente avversariale, 11 driver, long list di ~370 fonti, cinque STOP.
- **Perimetro diverso**: il loro e' "ICT e cyber"; il nostro nove categorie NFR. Quasi tutti i loro ancoraggi sono ICT
  (CISA KEV, EPSS, TRL, classificazione DORA).
- **Da adottare**: scale a 6 livelli (deciso), avversariale in prova, sotto-dimensioni dell'impatto, coerenza
  probabilita' x prossimita' come segnalazioni, driver per prevalenza (piu' SOV e NOR), "agisce su" per le azioni,
  casi reali nella scheda.
- **Da adattare**: residuo, pavimento di evidenza, profilo di esposizione, fonti di orizzonte, radar per driver.
- **Da non adottare**: STOP bloccanti nel ciclo, media degli abbattimenti e 90% per "implementata", azione dal solo
  score medio, due radar, scraping di centinaia di siti, ripetizioni in Agent Builder.

## 19.1 La proposta nel suo insieme

| Loro | Noi | Differenza |
|---|---|---|
| 0 Set up e pilota | cicli di prova, collaudo | "fase 0" formale da riprendere con la Banca |
| 1 Revisione fonti (STOP 1) | `fonti.md`, revisione annuale | loro trimestrale, su proposta dell'agente |
| 2 Scouting, scraping (STOP 2) | raccolta RSS deterministica, manuali | loro leggono interi siti |
| 3 Identificazione temi | A1 (+ fenomeni non censiti), A3 | equivalente |
| 4a Approfondimento (STOP 3) | A1 sulla knowledge | loro registro dei documenti per dimensione |
| 4b Valutazione + decision model | A1 sceglie, lo script calcola | loro: domande chiuse, le regole assegnano il livello |
| 5 Avversariale | A5 + A9 progettato (A-17) | il loro e' il nostro A9 |
| 6 Radar inerente | Radar_Mosca | anelli = prossimita', settori = driver |
| 7 Schede | A6, `schede.py` | + contro-scenari, casi reali, misure |
| 8 Copertura, radar residuo (STOP 4) | presidio qualitativo (D-49) | noi nessun residuo |
| 9 Report + validazione (STOP 5) | `valida` per valore, report PDF/HTML | la nostra validazione e' piu' fine |
| Monitoraggio quindicinale | settimanale (A3, KRI, livello) | il nostro e' piu' frequente |
| — | A8 straordinario, urgenza di Mosca | loro non li hanno |

Architettura compatibile per circa nove decimi. Orchestratore con skill, strumento a regole e memoria condivisa
presuppongono una piattaforma con strumenti (Copilot Studio o pro-code), non Agent Builder: e' vicina al ramo
`copilot-studio-pieno` (D-82).

## 19.2 Agente avversariale

- **Loro**: agente separato; assume che la valutazione sia sbagliata, costruisce lo scenario opposto, segnala le
  assunzioni fragili; i contro-scenari tornano allo step 4b.
- **Noi**: A9 Contraddittore (A-17, analisi 17), progettato e non provato.
- **Il punto dell'utente** ("perche' non si verifica", parere di mitigazione): e' la tesi "sopravvalutato" estesa ai
  presidi (controlli, azioni in corso, esposizione assente, condizioni abilitanti mancanti). Utile contro la conferma
  per inerzia.
- **Perche' in fase iniziale**: con la ripartenza da zero il primo ciclo assegna tutti i valori senza storia;
  l'ancoraggio alla prima impressione e' massimo e la regola del punto lo trascina per cicli.
- **Condizioni**:
  1. solo su un output di A1 che ha passato il precontrollo;
  2. 5-8 rischi principali (radar top, AGIRE ORA, Attivazione);
  3. ingresso con presidio, azioni aperte e stato, KRI, anni di adeguamento (senza, inventa mitigazioni);
  4. nessun valore proposto, al massimo 2 tesi per rischio (una per verso), ogni tesi con presidio o documento oppure
     "ipotesi";
  5. le tesi vanno in validazione come osservazioni, non indietro nel ciclo (D-71);
  6. chat separata, prima una ricerca propria;
  7. circa 15 minuti + 30-45 di lettura per ciclo; dopo 2 cicli si spegne se meno di un terzo delle tesi e' utile.
- **Rischi**: contraddittorio di maniera, pressione al ribasso (sempre entrambi i versi), presidi inventati (solo
  quelli dell'ingresso).
- **Proposta**: prova K15 sul primo ciclo con le scale nuove, mandato esteso.

## 19.3 Processo e STOP

| STOP | Valore | Costo | Giudizio |
|---|---|---|---|
| 1 Fonti | governance | basso | tenere, **prima** del ciclo |
| 2 Scouting | contro documenti inventati o fuori tema | alto | con la raccolta deterministica bastano controlli automatici (link, data, fonte in elenco) |
| 3 Approfondimento | attendibilita', TRL | alto | non bloccante, note in validazione |
| 4 Bassa confidenza / misure | le misure sono un input | medio | misure come input, confidenza come segnalazione |
| 5 Validazione | indispensabile | — | tenere |

**Controargomento: gli errori a monte si propagano** (fonti → documenti → temi → evidenze → punteggi).
- *Commissione* (documento sbagliato, fonte debole, inventato): visibili in validazione, il razionale li cita.
- *Omissione* (fonte mancante, tema non raccolto, driver senza documenti): **invisibili alla fine**, nessun controllo
  di coerenza le vede (nemmeno A5). E' la vera ragione per controllare a monte.
- In piu': costo di rifare la catena; prova documentale del presidio per audit e model risk.

**Sintesi: STOP morbidi**, a quattro condizioni:
1. mostrano le omissioni: copertura per driver e categoria ("nessun documento su DRV-CLI", "FNT-15 senza voci da 6
   settimane");
2. lasciano traccia (chi ha proseguito, quando, con quali punti aperti, perche');
3. portano i punti aperti in validazione ("note di processo");
4. si possono richiudere dopo, rilanciando solo quel passo.

Bloccanti solo su condizioni strutturali (zero documenti per una categoria, fonti non riviste da oltre un anno), come
la D-71.

**Impatti qualitativi**: (+) il ciclo arriva sempre in fondo, il validatore vede tutto insieme, meno conferme
automatiche; (−) carico concentrato in validazione (pochi indicatori), rischio "clic e via" (la condizione 1 e' la
piu' importante), responsabilita' meno netta (la compensa la traccia), corpus incompleto = output coerente ma
parziale che A5 non nota.

## 19.4 Radar inerente e residuo, calcolo, scheda

**Loro**: copertura per impatto e probabilita' = **media** degli abbattimenti delle misure (Implementata 90%, In gran
parte 60%, Parziale 30%, Assente 0%); I_res = I x (1 − copertura), idem P, minimo 1; velocita' e prossimita'
invariate; azione dallo score residuo arrotondato (1-2 Monitoraggio, 3-4 Attenzione, 5-6 Attivazione); due radar con
le stesse posizioni. Conti verificati: 4,55 → 3,05 (−33%); R05 3,9 → 2,3.

**Il concetto (condiviso)**: l'inerente dice quanto e' serio in se' (dove guardare); il residuo e la distanza fra i due
dicono dove siamo scoperti (dove investire). Per i rischi emergenti: i controlli sono pensati per i rischi noti (la
copertura e' un'ipotesi) e le misure che contano sono spesso future.

**Dubbi di meccanismo**:
1. **La media premia chi propone meno**: una misura implementata = 90%; aggiungendone una nuova "Assente" si scende al
   45% e il residuo sale. Meglio 1 − Π(1 − a) o il massimo, escludendo le misure solo proposte.
2. **Implementata non e' efficace**: in un RCSA si usa l'efficacia verificata (formazione completata, efficacia
   ignota; DLP sui servizi noti, non sui nuovi). L'autodichiarazione rende ottimisti.
3. **Scala ordinale**: moltiplicare un livello per una percentuale e' improprio; con il 90% qualunque impatto diventa
   1 "Trascurabile", anche "Critico o sistemico".
4. **Le misure agiscono soprattutto sulla probabilita'**: l'impatto lo riducono contenimento, continuita',
   ripristino, assicurazione.
5. **Il secondo radar ripete il primo** (anelli e settori uguali): meglio un radar solo, pieno = inerente, vuoto =
   residuo, o una colonna.
6. **Sei canali visivi per punto**: troppi per un comitato (il Radar_Mosca ne usa tre).
7. **La media comprime gli estremi**: impatto 6 e il resto a 3 = 4,05 "Attenzione"; l'Attivazione arriva solo per i
   rischi gia' materializzati. Il nostro livello di allerta non passa dalla media.
8. **Manca il tempo per agire** (vedi 19.8): R06 (crittografia e quantum) resta 4,1; con Mosca e' AGIRE ORA.

**Noi e loro**:

| Domanda | Loro | Noi |
|---|---|---|
| Quanto e' serio? | score inerente | composito (stessi pesi) |
| Quanto siamo coperti? | copertura autodichiarata | presidio deciso dal validatore, fuori dallo score |
| Azioni a che punto? | grado in 4 valori | stato del ciclo di vita |
| Facciamo in tempo? | — | Mosca |
| Che cosa si fa? | azione dallo score residuo | livello di allerta |
| Chi decide? | override di score, azione, alert | decisione su ogni valore |

Residuo e Mosca sono **complementari** ("quanto siamo coperti" e "facciamo in tempo").

**Proposta per il residuo**: prima dal presidio (esiste gia'); poi per misura, solo approvate, in corso o completate,
"agisce su" confermato dal validatore, abbattimenti 0 / 15 / 30 / 50% (di piu' solo con efficacia verificata),
combinazione 1 − Π(1 − a), impatto abbattuto solo da contenimento o continuita'. Alternativa ordinale: < 30% nessuna
riduzione, 30-60% un livello, ≥ 60% due livelli, minimo 1. L'inerente resta il criterio del radar.

**Scheda: cosa prendere**: driver in ordine di prevalenza (alto, costo minimo, abilita un radar per driver);
motivazione = gradino soddisfatto + fonte (alto); casi reali dalle notizie collegate (alto); misure con "agisce su" e
grado (alto, serve al residuo); contro-scenari (se A9); "altre categorie toccate" solo informative (D-55); confidenza
solo se calcolata (D-58).

## 19.5 Le scale a 6 livelli (date per assodate)

| Dimensione | Scala | Esempi | Cautele |
|---|---|---|---|
| Probabilita' | diffusione dell'evidenza: teorica, PoC, un caso o altri settori, ≥ 2 casi nel settore finanziario in 24 mesi, fornitore o componente in uso, Banca (anche tentativi e near miss) | frodi con voce clonata: casi in due banche UE = 4, tentativi alla Banca = 6 (vuol dire "gia' tentato", non perdita certa); greenwashing: due sanzioni ad altre banche = 4; "raccolti oggi, decifrati domani": 2 per anni | esposizione assente fino al 4 (tenere D-65); manca la tendenza (19.9) |
| Impatto | da trascurabile a critico o sistemico; massimo di sei sotto-dimensioni (economica, continuita', clientela, dati, regolamentare, reputazionale) | cloud: funzione critica ferma con notifica = 4, pagamenti fermi oltre la BIA = 5; dati su AI esterne: Garante + eco nazionale = 4 (guardando solo la perdita sarebbe 2); alluvione: DC secondario 3, entrambi 5 | soglie RAF di gruppo altissime; niente cifre di perdita stimate dall'AI |
| Velocita' | da oltre 24 mesi a entro 1 mese | ransomware supply chain 6; obsolescenza core 1; frammentazione normativa 2 | resta possibile non valutarla |
| Prossimita' | da 7-10 anni a "in atto" | quantum TRL 4-6 = 3 (prima 1 con tutto oltre 3 anni); frodi con agenti AI 5; clima cronico 1 | fascia 1-3 anni larga: Z di Mosca e segnale di avvicinamento |

**Coerenza**: CO1-CO3 vietano 13 combinazioni su 36; lo stesso fatto alza probabilita' e prossimita' (45% del peso
dello score): lo score premia i rischi gia' vicini.

**Impatti nel pacchetto** (si parte con "Nuovo registro" della finestra Admin):

| Area | Cambiamenti |
|---|---|
| Kernel | rubrica a 6 livelli con ancore non ICT; schemi di A1 e A8 (1-6); guida; C3, C5 |
| Prompt | A1 a 7.988 caratteri: descrittori nell'allegato `Input_A1` (D-69); verificare A5-A8 |
| Script | `radar.py` (soglie, per esempio prossimita' ≥ 3); Z di Mosca 0 / 0,5 / 2 / 4 / 6 / 8,5; soglia PxI del livello su 36; colori; numeri ammessi in A6 |
| Template | versione nuova (liste, formati, radar fino a ~8 anni) |
| Collaudo / demo | dati di prova rivalutati, demo, kit di Copilot Studio, ramo CS |

Stima: 4-6 giorni piu' un ciclo di prova.

## 19.6 Metodologia ad alberi e decision model

**Loro**: passo 0 (fatti); domande chiuse si'/no/n.d. con fonte; un ancoraggio decide il "si'"; il primo "si'"
dall'alto da' il livello; regole CO e CF (n.d., ripetizioni indipendenti); incerti allo STOP 4.

**Perche' e' piu' da threat intelligence che da horizon scan**:
- l'horizon scan vede presto cio' che non e' ancora evidente (segnali deboli, driver, condizioni, giudizio esperto):
  il valore e' il tempo guadagnato;
- la threat intelligence misura cio' che sta gia' accadendo (campagne, vulnerabilita' sfruttate, casi presso pari e
  fornitori);
- negli alberi **ogni gradino alto richiede un fatto gia' osservato** (probabilita': casi contati; velocita': ≥ 3
  casi con date; prossimita': casi, strumenti in vendita, TRL; impatto: soglie interne);
- effetti: 1) **arriva tardi** (con ≥ 2 casi nel settore il rischio e' gia' affermato; in cima il cyber gia' noto);
  2) **penalizza la novita'** (piu' n.d., piu' STOP); 3) **esclude il giudizio esperto** (una previsione non e' un
  caso); 4) **fuori dall'ICT non ha ancore** (greenwashing, competenze, contenzioso, clima);
- dove eccelle: cyber e terze parti a breve termine. Pregio generale: **verificabilita'** del voto.

**Fattibilita'**: domande chiuse si', ma l'output di A1 si allunga; ancoraggi interni solo con dati della Banca;
velocita' da ≥ 3 casi raramente; TRL solo tecnologico e stimato dall'AI; decision model si' (e' lo script); coerenza
si' come segnalazioni; ripetizioni no in Agent Builder.

**Alternativa A (raccomandata) — l'evidenza fa da pavimento, il giudizio decide**:
1. A1 sceglie il livello sulla scala a 6, come oggi;
2. scrive il **gradino documentato** (dove, quanti casi, data dell'ultimo; per la prossimita' casi, strumenti,
   scadenze, TRL), con fonte;
3. un livello sopra il gradino richiede un **fattore prospettico** con fonte (tendenza, strumenti pronti, esposizione,
   driver in accelerazione, analisti convergenti);
4. lo script calcola il minimo e segnala, mai blocca: sotto il minimo "sottovalutato?"; oltre un livello sopra senza
   fattore di rilevanza alta "sopravvalutato?";
5. CO1-CO3 adattate come segnalazioni; 6. n.d. come nota;
7. sotto-dimensioni dell'impatto come lista di controllo nella guida, senza soglie RAF;
8. ancore non ICT con la funzione di rischio (caso = sanzione, sentenza; scadenze normative).

Pro: verificabile, dichiara il giudizio, corregge P13. Contro: output piu' lungo; 3-4 giorni.

**Alternativa B — doppio binario**: alberi interi nello script per i driver CYB, TPR, TEC (A1 si discosta motivando);
alternativa A per gli altri. Pro: usa il metodo dove funziona. Contro: due metodi nello stesso radar; servono dati
interni.

**Variante di prova C — secondo parere calcolato**: per 2 cicli il livello degli alberi accanto a quello di A1 in
validazione, senza effetto; si misura la divergenza e poi si sceglie fra A e B.

## 19.7 Fonti: segnali deboli e segnali forti

**Loro**: 370 fonti, 10 criteri 1-5, media pesata, top 50 per ognuna di quattro short list (allerta precoce, segnali
deboli, approfondimento, monitoraggio); scraping; revisione trimestrale.

**I segnali forti degli analisti affermati** (WEF, Allianz Risk Barometer, Swiss Re SONAR, ORX, CRO Forum, analisti
tecnologici, rating) **possono sparire**:
1. la media mescola qualita' e comodita': un rapporto a pagamento, annuale, senza feed prende voti bassi su
   accessibilita', facilita', volume, tempestivita' ed esce dalla top 50; "volume" premia chi pubblica molto;
2. un documento = una riga: 50 articoli sullo stesso tema caldo pesano 50 volte un rapporto;
3. soglia unica di attendibilita': ammette o esclude, non pesa;
4. gli alberi contano solo i casi: una previsione non sposta il livello.

L'appiattimento aiuta i segnali deboli: **i deboli nascono dalla varieta', i forti dall'autorevolezza**.

**Come integrarli**:
1. qualita' (decide se entra) separata dalla convenienza (decide il canale: RSS, manuale, abbonamento);
2. **nucleo protetto** di 10-20 fonti di orizzonte fuori ranking, lette per intero da A1 ogni trimestre (PDF in
   `Analisi_Esterne`): WEF, Allianz, Swiss Re SONAR, ORX, CRO Forum, mappe dei rischi BCE/SSM/EBA/ESRB, ENISA Threat
   Landscape e Foresight, Europol IOCTA, analisti in abbonamento, rating e riassicuratori (Legal, D-27);
3. **natura della fonte**: fatto (caso, dato, sanzione) → pavimento; giudizio esperto → sopra il pavimento e temi
   nuovi; due analisti indipendenti convergenti = rilevanza alta;
4. contare per fonte indipendente ("stesso ente o stesso fatto = una fonte");
5. due rilevatori: deboli nel settimanale (varieta', A3, soglia di direzione); forti nel trimestrale (autorevolezza,
   A1 sul nucleo);
6. dalle loro liste: "segnali deboli" (la nostra lacuna: 32 fonti, soprattutto regolatori, CERT e stampa) e le fonti
   per dimensione;
7. non adottare: scraping (licenze, proxy, volume, 4 siti in Agent Builder), mappatura di 370 fonti con pesi da
   definire.

**Driver**: SOV e NOR utili; PQC piu' rischio che driver. **Tassonomia**: loro 13 categorie, noi 9 in perimetro
(D-74); il loro esempio "frodi AI" per noi e' fuori perimetro: da chiarire con la Banca.

## 19.8 Precisazione: Mosca nella loro proposta (nota 21 della copia interna)

Non basta disegnare una soglia sul loro radar: serve un indicatore calcolato per rischio.
- Z = anni prima che il rischio si manifesti (dalla prossimita': 0 / 0,5 / 2 / 4 / 6 / 8,5 sulla scala a 6); X =
  tempo per decidere e avviare (un trimestre); Y = anni per completare la mitigazione (azioni o anni di adeguamento).
  X + Y > Z = AGIRE ORA.
- R06: prossimita' 3 (3-5 anni) → Z ≈ 4; migrazione post-quantistica Y ≈ 5-6; X = 0,25 → AGIRE ORA; da loro resta
  4,1 "Attenzione".
- I loro anelli sono la prossimita' (solo Z): la soglia dipende anche da Y, che cambia per rischio, quindi un cerchio
  fisso non funziona. Tre modi: un segno sul punto (bordo rosso o "AGIRE ORA"); un radar dove la distanza e' il
  margine Z − (X + Y), come il Radar_Mosca, con la linea a margine 0; nella regola d'azione AGIRE ORA → Attivazione
  qualunque sia lo score.
- Serve un dato che loro non hanno: il tempo per completare la mitigazione, per misura o per rischio.

## 19.9 Precisazione: la tendenza (nota sulla slide della probabilita')

Tendenza = come cambia il fenomeno nel tempo (cresce, accelera, e' stabile, cala). La loro scala guarda dove e quanti
casi in 24 mesi (una fotografia), non la dinamica.
- Esempio: due fenomeni con "≥ 2 casi nel settore in 24 mesi" sono entrambi 4; A ha due casi a inizio 2025 e poi
  niente (in calo), B due casi nell'ultimo trimestre con tentativi raddoppiati e kit in vendita (in accelerazione).
- Si misura con fonti datate: casi per periodo, volume dei tentativi (CERT, threat intelligence, antifrode), strumenti
  disponibili, KRI di evoluzione.
- Noi: Probabilita 4 "crescita documentata", 5 "rapida accelerazione"; A3 conta i segnali concordanti (soglia di
  direzione).
- Integrazione: un livello sopra il pavimento con una crescita documentata (per esempio casi o tentativi almeno
  raddoppiati fra due periodi, con una fonte di rilevanza alta); una tendenza in calo e' materia della tesi
  "sopravvalutato".
- Le frecce del loro radar non sono tendenza: mostrano lo spostamento della valutazione.

## 19.10 Rilettura critica

1. **Contro di noi**: anche il nostro giudizio e' conservativo (P13); il pavimento di evidenza corregge un nostro
   difetto.
2. **Contro di loro**: azione dallo score medio, residuo autodichiarato con la media, niente tempo, due radar, STOP
   bloccanti.
3. **Governance**: la validazione per valore e' piu' forte del loro override; da mantenere.
4. **Costo ricorrente**: loro dati interni, scraping, cinque STOP; noi qualche ora per ciclo.
5. **Strategia**: scale comuni a 6 livelli evitano due radar incompatibili; il pacchetto puo' essere la base del
   pilota ("fase 0").
6. **Variabilita' dell'AI**: si sposta nelle risposte alle domande; senza ripetizioni il guadagno e' parziale.
7. **Riservatezza**: il documento esterno non va nel repository.

| Adottare | Adattare | Non adottare |
|---|---|---|
| scale a 6 livelli (deciso) | residuo (prima dal presidio, poi per misura) | STOP bloccanti nel ciclo |
| avversariale in prova K15 | pavimento di evidenza (A, prova C) | media degli abbattimenti, 90% |
| sotto-dimensioni dell'impatto | profilo di esposizione interno | azione solo dallo score |
| coerenza P x prossimita' come segnalazioni | fonti di orizzonte, natura della fonte | due radar |
| driver per prevalenza, SOV e NOR | radar per driver | scraping, 370 fonti, media di 10 criteri |
| "agisce su", casi reali in scheda | | ripetizioni in Agent Builder |

## 19.11 Lavori proposti, uno per volta su richiesta

| # | Lavoro | Stima | Decisione |
|---|---|---|---|
| 1 | scale a 6 livelli e registro nuovo, con lista dell'impatto e ancore non ICT | 4-6 giorni + ciclo di prova | A-19 |
| 2 | prova K15 dell'avversariale con il mandato esteso | mezza giornata | A-17 |
| 3 | pavimento di evidenza (alternativa A) con la prova C | 3-4 giorni | A-20 |
| 4 | driver per prevalenza, SOV e NOR, "agisce su", casi reali nella scheda | 3-4 giorni | A-24 |
| 5 | nucleo di fonti di orizzonte e natura della fonte | 1 giorno + scelta con la Banca | A-22 |
| 6 | residuo: dal presidio, poi per misura | 1,5-2 + 3-4 giorni | A-21 |
| 7 | STOP morbidi nell'app con la copertura del corpus | 2-3 giorni | A-23 |

Le modifiche comuni nascono su `main`, poi `git merge main` e `genera_CS.py` sul ramo `copilot-studio-pieno`.
