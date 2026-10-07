# 08 — Confronto con l'Horizon Scanning fatto con Copilot M365

Data: 25/09/2026. Stato: **priorita' A approvate e applicate lo stesso
giorno** (P1, P2, P4, P5, P9: decisioni D-19, D-32, D-33, D-34 in
`08_Deploy/DECISIONI.md`; template versione 2026-09-25, collaudo completo
verde, catena con Excel compresa). Nel pomeriggio applicate anche **P3**
(bordo giallo invece del colore, D-35), **P6** (regola 7 della rubrica e C4,
D-36; descrittori di plausibilita' rimandati ad A-12) e **P11** (sette rischi
di riferimento in `Piano_deploy.md`, 7.5, D-37); template versione
2026-09-25b. La sera del 25/09 il report e' stato ridisegnato (documento 09,
D-39) e le schede sono passate a un file a parte scritto dall'agente A6 (D-40):
la "pagina di sintesi executive" di P1 e' ora il **Quadro** (commento di A1
nella forma "MESSAGGIO: ... DECISIONI: ...", rischi segnalati e perche'
calcolati dal foglio), le Schede di P9 sono `Schede_<ciclo>.xlsx`; template
versione 2026-09-25c. **P7, P8, P10 restano proposte da decidere.** Il testo qui sotto e' l'analisi com'era prima delle modifiche:
dove dice "oggi" descrive il pacchetto del 24/09.

Differenze fra proposta e realizzazione:
- P1: il commento di A1 va in una tabella nuova, Sintesi_Cicli (non
  `SintesiCicli`); la struttura della `sintesi` e' una riga dell'Output di A1.
  Per farla stare (A1 ora a 7.959 caratteri) sono stati tolti i pesi dai
  titoli della rubrica e accorciati tre passi, senza toccare la tassonomia.
- P9: fogli Schede e Metodologia come proposto; l'ordine dei fogli nel
  workbook e' quello del PDF (Sintesi, Classifica, Radar_Mosca, Delta,
  Schede, Metodologia). Dal 25/09 sera (D-39, D-40): Quadro, Classifica,
  Radar_Mosca, Matrice, Delta, Metodologia; schede in un file a parte (A6).
- Aggiunto (non era una proposta): il registro in uso, nato dal template del
  23/09, si porta sul template nuovo con `aggiorna-registro` (D-34), e lo
  script si ferma su un registro o una mappa di un'altra versione.
- Trovato durante il lavoro: nel Radar_Mosca "Agire entro l'anno" era colorato
  di rosso come "AGIRE ORA" (Excel confronta ignorando le maiuscole): corretto.
- P3: su richiesta dell'utente il riempimento non cambia colore; i temi
  all'attenzione del supervisore hanno il bordo giallo spesso. La trasparenza
  del riempimento e' nella proposta grafica (`09_Proposta_grafica_report.md`).
- P6: niente campo nuovo; spazio in A1 ricavato accorciando rubrica e passo 9
  (A1 7.951 caratteri).
- Nota del 30/09 (`11_Semplificazione_scoring_A1.md`, D-49..D-56): dopo il
  primo ciclo reale il modello e' stato semplificato. Gap_Controlli esce dallo
  score e torna vicino al "Presidio" dell'esempio, ma come giudizio
  qualitativo della Banca nell'anagrafica, fuori dallo score; i pesi di D-19
  sono sostituiti da D-50 (Severity 0,35, Probabilita 0,25, Prossimita 0,20,
  Velocity 0,20, Velocity facoltativa); la Probabilita ha descrittori di
  plausibilita' (anticipati da A-12, come chiedeva P6); P7 resta non
  approvata ma le azioni non dichiarano piu' la dimensione che riducono (D-54).
  Le tabelle della sezione 2 descrivono il modello al 25/09.

## 1. Cosa e' stato analizzato

- **PDF "Horizon Scanning"** (17 pagine): la trascrizione della chat con
  Copilot. Contiene i 13 prompt dati in sequenza e il **prompt cumulativo
  finale**, che produce in un colpo solo un Word e un Excel.
- **Excel** `Horizon_Scanning_Rischi_Emergenti_2026_COMPLETA_STANDALONE_CON_PROMPT_FINALE.xlsx`,
  8 fogli: Sintesi, Registro e KRI, Esempi mitigazione, Radar e grafici
  (2 immagini: radar e barre), Metodologia Mosca, Fonti, Documenti allegati,
  Prompt cumulativo.
- **Il Word non c'e'.** Il file `Horizon Scanning.docx` e' la stessa
  trascrizione del PDF. La struttura del Word e' nota solo dal prompt: 11
  sezioni, piu' l'Appendice A (Mosca) e l'Appendice B (prompt).

## 2. I due modelli a confronto

| Aspetto | Esempio Copilot | Nostro pacchetto |
|---|---|---|
| Cosa produce | Un esercizio una tantum, "primo output completo", Word + Excel | Un ciclo trimestrale ripetibile, con registro storico e aggiornamento settimanale |
| Individuazione dei rischi | **Lista di 7 rischi imposta nel prompt** (l'analisi la conferma) | A1 individua i rischi da zero su tutti e 7 gli event type (primo ciclo), poi li rivaluta |
| Classificazione | Fenomeni liberi (5 su 7 tecnologici o cyber) | 1 event type L1 + driver; copertura obbligata dei 7 event type |
| Dimensioni | Probabilita, Impatto, Urgenza, Presidio (1-5) | Severity, Velocity, Prossimita, Gap_Controlli, Probabilita, Confidence (1-5, descrittori ancorati) |
| Score | P x 0,25 + I x 0,30 + U x 0,30 + (6 - Presidio) x 0,15 | 0,40 Sev + 0,20 (Vel + Pross + Gap); **D-19 decisa**: Sev 0,30, Prob 0,20, Gap 0,20, Vel 0,15, Pross 0,15 |
| Urgenza | **Stimata dal modello** "applicando la logica di Mosca" | **Calcolata dal foglio**: Z dalla Prossimita, X = un ciclo, Y = orizzonte delle azioni |
| Presidio | Maturita' (5 = buono), poi invertita | Gap (5 = peggio): nessun errore di segno |
| Fonti | Codici S1-S12 senza data | Riferimento + data + tipo; evidenza datata obbligatoria per ogni variazione |
| KRI | Solo nomi ("# agenti AI registrati") | 3 per rischio con unita', fonte dati, soglie; storico e rilettura ogni ciclo |
| Owner | 6-7 funzioni per rischio | Una funzione per azione |
| Azioni | Approfondimento + mitigazione + 4 "esempi pratici" per rischio | Da 1 a 5 azioni con owner, dimensione ridotta e orizzonte (che alimenta la Y di Mosca) |
| Controllo | Checklist finale eseguita dal modello stesso | Controlli deterministici C1-C9, A5 indipendente, validazione umana tracciata |
| Radar | Centro = piu' urgente; pallino = impatto; rosso/verde = interesse del regulator | Centro = piu' urgente (margine di Mosca); area = Probabilita x Severity; un solo colore |
| Report | Word autosufficiente: **executive summary**, metodologia, registro analitico, raccomandazioni, fonti, appendici | PDF di Dashboard, Radar_Mosca e Delta (D-31): **nessuna pagina di commento** |

In sintesi: il nostro **modello di valutazione e' piu' robusto**. Il
**deliverable per il comitato** dell'esempio e' molto piu' completo del
nostro.

## 3. Cosa prendere dall'esempio: le proposte

Priorita': **A** = da fare prima del primo report al comitato, **B** = utile,
**C** = facoltativa.

### P1 (A) — Pagina di sintesi executive

- **Lacuna trovata.** A1 produce gia' la `sintesi` (100-3000 caratteri,
  "memo trimestrale"), ma **oggi non arriva da nessuna parte**.
  `mappatura_campi.json` dice "testo del report, non una colonna": lo script
  non la scrive, resta solo nel JSON archiviato. Il PDF di D-31 contiene solo
  numeri e grafici. Anche il testo dei limiti che `06_Governance`, sezione 5,
  vuole "in ogni memo" non compare in nessun output.
- **Proposta.** Un foglio `Sintesi`, primo nell'ordine di stampa.
  - **Blocco calcolato** (solo formule):
    - ciclo e stato della validazione;
    - copertura;
    - quanti rischi sono Nuovi, Variati o Confermati;
    - i primi 5 per score composito;
    - i rischi "AGIRE ORA";
    - azioni proposte e approvate;
    - KRI in allerta.
  - **Commento**: la `sintesi` di A1. Lo script la scrive in una tabella
    append-only `SintesiCicli` (ciclo, testo di A1, esito e sintesi di A5).
    Il foglio mostra la riga del ciclo corrente.
  - **Limiti**: il testo fisso di `06_Governance`, sezione 5.
  - **Avviso automatico** se il validatore ha rettificato qualcosa: "commento
    redatto prima della validazione: N rettifiche applicate". La `sintesi`
    nasce prima della validazione.
- **Prompt di A1.** Serve una riga sulla struttura della `sintesi`:
  - messaggio chiave;
  - 3 priorita' con id_rischio;
  - rischi nuovi e variazioni;
  - decisioni chieste al comitato;
  - tono da CRO, nessun dato che non stia nelle fonti.

  Costa circa 200 caratteri e **A1 e' a 7.972 su 8.000**: prima bisogna
  liberare spazio (vedi P6).
- **Impegno**: medio. Toccherebbe schema, mappatura, script, generatore,
  collaudo e documenti.

### P2 (A) — Grafici per chi decide: classifica e "lente di Mosca"

- **Classifica.** Barre orizzontali **ordinate** per score composito, colorate
  per esito dell'urgenza (AGIRE ORA / entro l'anno / margine). E' il grafico
  piu' leggibile dell'esempio ("Priorita' residua"), ma li' non e' ordinato.
  Oggi da noi la cosa piu' vicina e' il radar a tre cicli della Dashboard, che
  per un comitato si legge male. L'ordine si ottiene con colonne di appoggio
  (GRANDE con spareggio), senza matrici dinamiche.
- **Lente di Mosca.** Per ogni rischio una barra X + Y, con un segno a Z: se
  la barra supera il segno, il rischio e' in ritardo. Mostra *perche'* un
  rischio e' "AGIRE ORA". Il prompt dell'esempio la chiedeva, ma nel file
  consegnato non c'e'. I dati sono gia' nel foglio Radar_Mosca (colonne H-K).
- **Impegno**: basso.

### P3 (B) — Radar: colore per interesse del supervisore, riempimento trasparente

- Rosso = tema all'attenzione di BCE, EBA o Banca d'Italia; verde = no.
  Risolve il difetto noto "un solo colore" (`TODO_possibili_sviluppi.md`,
  G5).
- **Chi lo decide.** Nell'esempio il colore l'ha imposto l'utente ("tutti
  rossi tranne R6"): e' un giudizio umano. Proposta: una **cella di input
  gialla nell'anagrafica** (`Attenzione_Supervisore` Si'/No), decisa dal
  validatore. Nessuna modifica ai prompt. In alternativa, A1 lo propone citando
  una fonte di vigilanza (FNT-01..05, FNT-20): costa caratteri e un controllo
  in piu'.
- **Impatto sul grafico.** Le serie raddoppiano (una per valore di P x I e per
  colore). Riempimento semitrasparente, cosi' i cerchi vicini restano
  leggibili.
- **Impegno**: basso-medio.

### P4 (A) — Y di Mosca per i rischi strutturali

- **Difetto del nostro modello, trovato grazie all'esempio.** Oggi Y =
  l'orizzonte piu' lungo fra le azioni, **al massimo 12 mesi** (la rubrica,
  sezione 8, lo dichiara fra i limiti). Per un rischio come il
  quantum/PQC la migrazione dura anni: con Prossimita 2 (Z = 2,5 anni) il
  margine e' 2,5 - (0,25 + 1) = 1,25, cioe' "Margine 1,3 anni". Con Y = 5 anni
  sarebbe -2,75: **AGIRE ORA**. E' proprio il caso per cui Mosca ha inventato
  la disuguaglianza. L'esempio include nell'urgenza "tempo per prepararsi" e
  "complessita' del presidio".
- **Proposta.** Una colonna `Anni_Adeguamento` nell'anagrafica (input, vuota
  di default), con Y = max(orizzonte delle azioni, Anni_Adeguamento). La
  valorizza il validatore, eventualmente su proposta di A1.
- **Impegno**: basso: una colonna, una formula, un caso nel collaudo di
  Mosca.

### P5 (A) — Conferma di D-19: implementarla

- I pesi dell'esempio hanno la **stessa struttura** di D-19:

  | | Impatto | Probabilita | Tempo | Presidio |
  |---|---|---|---|---|
  | Esempio | 0,30 | 0,25 | 0,30 (Urgenza) | 0,15 |
  | D-19 | 0,30 (Severity) | 0,20 | 0,30 (Velocity + Prossimita) | 0,20 (Gap) |

  Cambia solo come si misura il tempo: da noi con descrittori ancorati,
  nell'esempio con un'urgenza a giudizio.
- **Proposta.** Implementare D-19 insieme a P1-P2, cosi' il primo report ha
  gia' lo score definitivo. Nella Dashboard aggiungere la colonna Probabilita,
  che oggi manca fra le dimensioni mostrate.

### P6 (B) — Evidenza quantitativa e numeri dichiarati

- **Regola dell'esempio da prendere.** "Non inventare dati quantitativi; se
  un numero e' valutativo dichiaralo come valutazione". L'esempio tiene anche
  separate motivazione qualitativa ed evidenze quantitative.
- **Proposta.** Niente campo nuovo. Nella rubrica, sezione 3, una regola che
  entra in A1 e in A5: "il razionale cita almeno un dato numerico con la sua
  fonte quando esiste; un numero senza fonte e' una valutazione e va detto".
  A5 lo verifica in C4.
- **Spazio nei prompt.** P1 + P6 chiedono circa 400 caratteri in A1. Proposta:
  accorciare i descrittori della rubrica, sezione 1: sono segnaposto e vanno
  comunque riscritti dalla funzione di rischio (D-18/D-20).
- **Descrittori della Probabilita.** Da rivedere nella stessa occasione. I
  nostri sono di frequenza ("una volta in 2-5 anni"), difficili per rischi
  senza storia. Quelli dell'esempio sono di plausibilita' ("5 = fenomeno gia'
  osservabile o in rapida accelerazione"). Decide la funzione di rischio.

### P7 (B) — Azioni di approfondimento distinte dalla mitigazione

- **Perche'.** L'esempio distingue *approfondimento* (censire, mappare,
  testare) e *mitigazione*. Per un rischio emergente la prima azione e' spesso
  capire. Da noi un'azione di approfondimento deve comunque "ridurre una
  dimensione" (C8), il che e' forzato. Soprattutto, **entra nella Y di
  Mosca**, ma capire non e' mitigare.
- **Proposta.** Un campo `tipo` nelle azioni (Approfondimento | Mitigazione).
  - Solo le azioni di mitigazione entrano in Y.
  - C8 chiede la dimensione solo alle azioni di mitigazione.
  - Gli "esempi pratici" dell'esempio **non** servono: le nostre azioni sono
    gia' proposte concrete, con owner e orizzonte.
- **Impegno**: medio: schema, mappatura, colonna Azioni, C8, collaudo, prompt.

### P8 (B) — Report di settore annuali fra le fonti

- **Perche'.** Quasi tutte le evidenze quantitative dell'esempio vengono da
  report di settore: ORX Operational Risk Horizon e Cyber Horizon (graduatorie
  e percentuali), ORX Top Risk Review, priorita' di vigilanza BCE, BIS Papers
  158 sul quantum. Nel nostro catalogo c'e' solo FNT-35 (database di perdite
  esterne, ORX News). Le priorita' BCE sono coperte da FNT-01/02.
- **Proposta.** Una voce di catalogo "Report di settore annuali" (es. FNT-37),
  con i PDF in `Analisi_Interne` o in una cartella di riferimento della
  knowledge.
- **Da verificare.**
  - La licenza: i report ORX sono riservati ai membri.
  - Il limite di 20 fonti di knowledge per agente.
  - Decisione sulle fonti: spetta alla funzione di rischio (D-15).

### P9 (A) — Report autosufficiente: schede dei rischi e metodologia

- **Il principio dell'esempio vale anche per noi.** "Il documento deve essere
  autosufficiente, leggibile senza conoscere le iterazioni precedenti". Il PDF
  di oggi mostra score e grafici, ma non **che cosa** e' ogni rischio ne'
  **perche'** ha quel punteggio.
- **Proposta.** Due fogli di stampa, solo formule sul ciclo corrente:
  - `Schede`: una riga per rischio con descrizione, razionale, fonti con data,
    azioni e KRI con soglie. Equivale al "registro analitico" dell'esempio.
  - `Metodologia`: scale, pesi (letti dalle celle di Parametri, quindi sempre
    veri), Mosca, come si legge il radar, limiti. Equivale all'Appendice A.
- **Impostazione di stampa.**
  - Ordine: Sintesi, Classifica, Radar_Mosca, Delta, Schede, Metodologia.
  - Intestazione con l'etichetta di riservatezza (il PDF dell'esempio porta
    "Internal Use Only").
  - Piede con ciclo, data e pagina.
- Con P1 e P2 forma il **pacchetto "report al comitato"**. D-31 va aggiornata
  con il nuovo elenco dei fogli.

### P10 (C) — Tracciabilita' dell'esercizio

- **Cosa fa l'esempio.** Allega il prompt e l'elenco dei documenti
  (Appendice B).
- **Nostro equivalente.** Nel foglio Metodologia: data della versione delle
  istruzioni degli agenti e del kernel, e nome del file JSON archiviato del
  ciclo. Le fonti del ciclo sono gia' nelle Schede (P9). E' utile per il
  model risk (`06_Governance`).

### P11 (B) — I 7 rischi dell'esempio come verifica del primo ciclo

- **Perche'.** La lista dell'esempio e' un riferimento indipendente, costruito
  da una persona con i report ORX. Nel collaudo in ambiente (Piano_deploy,
  fase 7), dopo il doppio run, il validatore controlla se A1 li ha trovati o
  perche' no.
- **Cosa non cambia.** Non e' un criterio di accettazione (D-21 resta com'e'):
  e' un'osservazione da portare nella validazione.
- **Mappatura sulla nostra tassonomia** (proposta):

  | Rischio dell'esempio | Event type | Driver | Nota |
  |---|---|---|---|
  | R1 AI agentica, identita' non umane | L1-06 | DRV-AI, DRV-CYB | se l'agente sottrae dati: secondo rischio L1-02 |
  | R2 Attacco ai modelli AI, data poisoning | L1-02 | DRV-AI, DRV-CYB | il degrado non doloso (drift) e' un altro rischio, L1-07 |
  | R3 Frodi con AI, deepfake | L1-02 | DRV-AI, DRV-CYB | |
  | R4 Terze parti, concentrazione cloud | L1-06 | DRV-TPR, DRV-CYB | |
  | R5 Quantum / PQC | L1-02 | DRV-CYB, DRV-TEC | "raccogli ora, decifra dopo" = furto di informazioni; caso tipico di P4 |
  | R6 Frammentazione normativa e sanzioni | L1-04 | DRV-GEO, DRV-CON | serve un meccanismo di perdita (es. violazione di sanzioni), altrimenti e' fuori perimetro |
  | R7 Competenze, eccessivo affidamento sull'AI | L1-07 | DRV-HUM, DRV-AI | |

  Nella lista dell'esempio mancano L1-01 (frode interna), L1-03 e L1-05
  (danni fisici, clima): e' la distorsione che la nostra copertura obbligata
  dei 7 event type evita.

## 4. Cosa NON prendere, con le prove dal file

| Pratica dell'esempio | Perche' no | Prova |
|---|---|---|
| Lista dei rischi scritta nel prompt | L'analisi conferma cio' che le si chiede di trovare | Prompt, "OBIETTIVO DELL'ANALISI" |
| Punteggi cambiati per far venire meglio il grafico | Il grafico guida lo score, non l'evidenza: rischio di modello | Prompt 8: "rivalutare l'impatto relativo tra i pallini, cosi' da differenziare meglio le dimensioni" |
| Urgenza stimata a giudizio | Non riproducibile, non verificabile | Prompt, "LOGICA DI URGENZA" |
| Autocontrollo affidato al modello | Il modello dichiara controlli che il file non rispetta | Dice "4 grafici/immagini", il file ne ha 2 (mancano lente di Mosca e matrice delle interconnessioni); "spiegazione completa di Mosca in un foglio dedicato", il foglio ha 3 righe; ENISA richiesta, assente fra le fonti; S11 mancante; S12 = "riferimento di conversazione" senza URL, contro "fonti in chiaro" |
| Pallini proporzionali all'impatto | Nel radar consegnato R5 (impatto 5) appare piu' grande di R1 (impatto 5); R1 e R4 (urgenza 5) sono sovrapposti | Foglio Radar e grafici, immagine 1 |
| Fonti senza data | Nessuna regola di variazione applicabile | Foglio Fonti |
| KRI senza unita', soglie e fonte dati | Non si misurano | Foglio Registro e KRI |
| 6-7 owner per rischio | Nessuno e' responsabile | Foglio Sintesi |

Il nostro radar di Mosca resta migliore:
- anelli in anni di margine, con la linea di Mosca, invece di "Urg.1-5";
- rischi distribuiti nel settore, senza sovrapposizioni;
- area proporzionale a P x I invece di un "impatto relativo" ritoccato.

Dall'esempio prendiamo solo il colore e la trasparenza (P3).

## 5. Ordine proposto

1. **Pacchetto report al comitato**: P1 + P2 + P9, con D-19 (P5) e P4. E' cio'
   che il comitato vede. Va fatto prima del primo ciclo 2026Q4 (D-22), altrimenti
   il primo report esce senza commento.
2. **Spazio nei prompt**: rubrica piu' corta, poi P6 e la riga della
   `sintesi` di P1.
3. P3, P7, P8, P11 quando si fa il collaudo in ambiente.
4. P10 insieme al primo aggiornamento di `06_Governance`.

Decisioni richieste (candidate per `DECISIONI.md`):
- approvare il pacchetto report (P1, P2, P9) e aggiornare D-31;
- P4: chi valorizza Anni_Adeguamento;
- P3: colore da input umano o proposto da A1;
- P6: descrittori della Probabilita;
- P8: ammissione dei report di settore fra le fonti e licenza ORX.
