# Schemi JSON — campo per campo

Tre contratti: l'output di A1 (`schema_output_A1.json`), di A3
(`schema_output_A3.json`) e di A5 (`schema_output_A5.json`). La scrittura si
ferma se un payload non e' conforme. Il validatore (`07_Senza_Studio/valida_output.py`)
interpreta gli schemi, non li ricopia: una regola cambia solo nello schema.
La destinazione di ogni campo sta in `mappatura_campi.json`.

## Regole trasversali, tutte da errori reali

- `additionalProperties: false` ovunque: il modello tende ad AGGIUNGERE campi mai
  chiesti (raccomandazioni, impatto stimato, score composito) che nessuno valida.
- Punteggi **interi**: un 3,5 significa che il modello ha interpolato invece di
  scegliere un descrittore. Il validatore rifiuta anche `true` al posto di 1.
- Date `AAAA-MM-GG` e ciclo `AAAAQn` con pattern: diventano criteri di formule
  e confronti di date, devono combaciare al carattere.
- Nessun campo `score_composito`: lo calcola il foglio.
- Dal 30/09/2026 (D-49...D-56) A1 non scrive `gap_controlli`, `esito`, i
  "da/a" delle variazioni e la `dimensione` delle azioni: con
  `additionalProperties: false` un output che li riscrive e' rifiutato. Esito
  e "da/a" li aggiunge lo script dopo i controlli (`completa_payload`), e
  sono quelli che finiscono nel registro.

## A1 — radice

| Campo | Regola | Perche' | Destinazione |
|---|---|---|---|
| `ciclo` | `^[0-9]{4}Q[1-4](-S[1-9])?$`: un trimestre o, dal 07/10 (D-75), un ciclo straordinario `AAAAQn-Sk` (anche negli schemi di A5 e A6); con la baseline di uno straordinario (chiave `straordinario`: rischi_da_rivalutare, motivo, decisore, data_decisione) A1 scrive solo i rischi indicati | criterio delle SUMIFS | RiskRegister.Ciclo, Azioni.Ciclo, KRI.Ciclo_Aggiornamento, Parametri cicloCorrente |
| `data_riferimento` | data | finestra dell'evidenza (C3, C5) | RiskRegister.Data_Riferimento; data dei KRI riletti |
| `rischi` | almeno 1 | | una riga RiskRegister per elemento |
| `ricalcolo_kri_ciclo_precedente` | array, a livello CICLO | la rilettura riguarda i KRI in vigore anche dei rischi non rivalutati | KRI (aggiornamento per KRI_ID) |
| `sintesi` | 100-3000 caratteri | commento per il comitato nella forma "MESSAGGIO: ... DECISIONI: ..." (messaggio chiave, 3 priorita', nuovi e variati; poi decisioni richieste) | Sintesi_Cicli.Sintesi_A1; foglio Quadro del report, diviso in messaggio e decisioni (D-32, D-39) |
| `fenomeni_non_censiti` | facoltativo, al massimo 15: fenomeno, event_type (o null), fonti (fino a 3, riferimento e data), motivo fra `nessun_meccanismo`, `fonte_non_specifica`, `gia_coperto`, `troppo_lontano`, `altro`, spiegazione fino a 300 caratteri | i fenomeni esaminati nelle fonti e non censiti, con il motivo; istruzioni nella guida di scrittura dell'allegato (prompt invariato) | nessuna colonna: output archiviato di A1 e `Ciclo.txt` della knowledge di A7 (D-72) |
| `osservazione` | facoltativo, al massimo 30 voci (sezione "A1 — voce della lista di osservazione") | solo le voci nuove e quelle con evidenza nuova; le altre le riporta lo script (D-73) | tblOsservazione, una riga per voce per ciclo |

## A1 — voce della lista di osservazione (D-73)

Istruzioni per A1 nella guida di scrittura dell'allegato (`guida_scrittura_A1.md`, sezione "Lista di osservazione"); prompt di A1 invariato. Controlli solo dello script (`controlla_osservazione`).

| Campo | Regola | Destinazione |
|---|---|---|
| `oss_id` | `^OSS-[0-9]{2}$` per una voce della baseline, **null** per una voce nuova (il codice lo assegna lo script: primo libero, mai riusato) | tblOsservazione.OSS_ID |
| `esito` | `nuova`, `confermata`, `avvicinata`, `promossa`, `archiviata`; codice e esito coerenti (C1 Bloccante) | Esito (Nuova...; Invariata per le voci riportate dallo script) e Stato (In osservazione, Promossa, Archiviata; Respinta dalla validazione) |
| `nome`, `descrizione` | 5-120 e 20-500 caratteri: il meccanismo di perdita, anche lontano | Nome, Descrizione |
| `driver`, `event_type` | da 1 a 3 driver della tassonomia; una categoria (D-74) | Driver ("a, b"), Event_Type |
| `rischi_toccati` | da 0 a 5 `NFR-nn` (un codice che non esiste = Osservazione) | Rischi_Toccati |
| `impatto_potenziale` | intero 1-5, descrittori della rubrica | Impatto_Potenziale (validato) |
| `orizzonte_anni` | intero 1-20 | Orizzonte_Anni (validato) |
| `plausibilita` | `teorica`, `possibile`, `in crescita` | Plausibilita (validata) |
| `segnale_avvicinamento` | 10-300 caratteri: il fatto osservabile che lo farebbe diventare un rischio | Segnale_Avvicinamento |
| `motivazione` | 20-600 caratteri, con l'evidenza nuova per una voce esistente | Motivazione |
| `fonti` | da 1 a 3, riferimento e data (data dopo la data di riferimento = Osservazione; voce aggiornata senza una fonte nuova = Osservazione) | Fonti (JSON) |
| `promosso_a` | `NFR-nn` di un rischio **nuovo** del ciclo, solo con esito `promossa`; altrimenti null (C1 Bloccante) | Promosso_A |

Al massimo 30 voci in osservazione dopo il ciclo (C1 Bloccante).

## A1 — rischio

| Campo | Regola | Destinazione |
|---|---|---|
| `id_rischio` | `^NFR-[0-9]{2}$`, stabile per sempre | RiskRegister.ID_Rischio, anagrafica |
| `nome`, `descrizione` | lunghezze | RiskRegister, anagrafica (nome) |
| `event_type` | una delle nove categorie della tassonomia interna (9.1 ... 9.13) o `FP` (rischio esistente fuori perimetro, D-74); un codice di Basilea della baseline si riclassifica | RiskRegister.Event_Type, anagrafica |
| `driver` | enum, almeno 1, senza ripetizioni | RiskRegister.Driver (testo "a, b") |
| `impatto`, `prossimita` | interi 1-5 | colonne Impatto (era Severity, D-57) e Prossimita; lo Score_Composito e' formula (pesi D-50) |
| `velocity` | intero 1-5 **o null** (obbligatorio): null = non valutata, se nessuna fonte ne documenta i tempi (D-50) | RiskRegister.Velocity (vuota); nel composito solo se valutata, i pesi si ridistribuiscono |
| `anni_adeguamento` | numero 0-30 o null (obbligatorio): anni di un adeguamento strutturale stimati da A1, motivati nel razionale (D-60) | RiskRegister.Anni_Adeguamento; il valore validato va nell'anagrafica (Y minima di Mosca) |
| `variazioni[]` | dimensione (impatto, velocity, prossimita, probabilita), evidenza (>= 20 caratteri), data_evidenza | RiskRegister.Variazioni (JSON), con "da" e "a" aggiunti dallo script dalla baseline (D-51) |
| `fonti[]` | almeno 1; riferimento, data, tipo Interna/Esterna | RiskRegister.Fonti (JSON); C5 conta le fonti |
| `razionale` | 50-2500 caratteri; **in parti con etichette fisse** (D-68, chieste dallo scheletro del prompt): `RISCHIO:` il fenomeno in termini di rischio (causa, evento, danno); `IMPATTO:`, `PROBABILITA:`, `PROSSIMITA:`, `VELOCITY:` perche' quel valore, con il fatto e il documento; `ADEGUAMENTO:` se c'e' una stima. Cita un dato numerico con la fonte, se esiste, e dichiara come valutazione un numero senza fonte (rubrica, regola 7; A5 in C4). Il formato non e' imposto dallo schema: un razionale senza etichette passa, `trimestrale` lo segnala con un avviso e la scheda lo mostra intero | RiskRegister.Razionale; le parti le legge `schede.parti_razionale` |
| `azioni_mitigazione[]` | 1-5; descrizione, owner, orizzonte (3/6/12 mesi), razionale (20-700 caratteri: perche', poi `EFFETTO:` che cosa dovrebbe cambiare, D-68; niente `dimensione`, D-54) | una riga in Azioni per elemento |
| `probabilita` | intero 1-5, obbligatorio; descrittori di plausibilita' (D-52, D-61) | RiskRegister.Probabilita; nel composito; area del Radar_Mosca (x Impatto) |
| `kri_proposti[]` | **esattamente 2** (D-64; prima da 1 a 3, D-53) | storico KRI, una riga per KRI nel ciclo; kri_id riusato = stessa serie |

L'esito (Nuovo se l'id non e' nella baseline; Variato se cambia Impatto,
Probabilita, Prossimita o Velocity, anche da vuota a un valore; altrimenti
Confermato) non e' un campo dello schema: lo
calcola lo script e va in RiskRegister.Esito (D-51).

### KRI proposto

| Campo | Regola | Nota |
|---|---|---|
| `kri_id` | `["string","null"]`, pattern `^NFR-[0-9]{2}-K[0-9]+$`, **non obbligatorio** | presente per un KRI in vigore; assente o null per uno nuovo: l'id lo assegna la scrittura |
| `tipo` | obbligatorio, "Esposizione" o "Evoluzione" (D-64) | KRI.Tipo. Esposizione = quanto la Banca e' esposta (di solito un dato interno); Evoluzione = quanto cresce il fenomeno (anche da fonti esterne). "Uno per tipo" non e' esprimibile in JSON Schema: lo presidia C9. Un KRI in vigore conserva il tipo (C9, Osservazione) |
| `nome`, `unita`, `razionale` | lunghezze; il razionale (20-700 caratteri) dice perche' il KRI misura il rischio e, dopo `EFFETTO:`, l'andamento atteso e cosa segnala oltre soglia (D-68) | KRI.Razionale; nelle schede "Perche' lo misuriamo" ed "Effetto atteso" |
| `fonte_dati` | almeno 5 caratteri | un sistema o report identificabile |
| `soglia_attenzione`, `soglia_allerta` | numero **o null** (obbligatori) | null se nessuna fonte le sostiene: le fissa la Banca in validazione, stato "Soglie da definire"; un KRI riproposto senza soglie conserva quelle in vigore (D-53). **"Entrambe o nessuna" e `soglia_allerta >= soglia_attenzione` NON sono esprimibili in JSON Schema** (vincoli fra due campi): li presidiano il controllo C9 e la formula Stato del foglio ("SOGLIE INVERTITE — correggere"). Il collaudo verifica che il validatore li lasci passare e C9 li fermi. |

### Rilettura del KRI

| Campo | Regola | Nota |
|---|---|---|
| `kri_id` | obbligatorio, pattern | KRI in vigore a cui appartiene il valore rilevato nel ciclo |
| `valore` | numero o null | null = non rilevato; mai il valore precedente ricopiato. Si rileggono solo i KRI di cui A1 trova un valore (D-53): gli altri restano "Non rilevato" |
| `fonte`, `commento` | lunghezze | KRI.Fonte_Rilevazione, KRI.Nota_Rilevazione |

## A3 — blocco settimanale

| Campo | Regola | Destinazione |
|---|---|---|
| `settimana` | data (lunedi', verificato dalla scrittura) | Parametri settimanaCorrente |
| `notizie[].id_notizia` | `^N-[0-9]{8}-[0-9]{2}$` | NewsLog.ID_Notizia (chiave anti-duplicato) |
| `notizie[].fonte` | 3-150 caratteri, per esteso | NewsLog.Fonte |
| `notizie[].codice_fonte` | `^(FNT-[0-9]{2}\|MAN)$`; la scrittura verifica che sia in `fonti.md` e non escluso | NewsLog.Codice_Fonte |
| `notizie[].rischio_collegato` | NFR-nn o null | NewsLog.Rischio_ID ("NON PRESIDIATO" se null) |
| `notizie[].segnale` | quattro valori letterali | NewsLog.Segnale |
| `notizie[].impatti` | esattamente 9, una per categoria (D-74); intensita 0-3; direzione | NewsLog.Imp_9_n (intensita'); la direzione per categoria va nel report |
| `flag_proposti[]` | id, direzione, motivazione | report settimanale |
| `notizie[].voce_osservazione` | facoltativo: OSS-nn di una voce in osservazione (la scrittura lo verifica) o null (D-73) | NewsLog.Voce_Osservazione (validabile) |
| `segnali_osservazione[]` | facoltativo: oss_id, direzione Avvicina / Segnale verificato / Allontana, motivazione (D-73) | Sintesi_Settimane.Segnali_Osservazione; baseline del ciclo dopo (notizie_a3, segnali_a3 della voce) |
| `proposta_straordinario` | facoltativo: rischi (in anagrafica) e motivo, oppure null; regola del segnale critico, rubrica sezione 6 (D-75) | Sintesi_Settimane.Proposta_Straordinario, riquadro del foglio Notizie, messaggio di `settimanale` |
| `sintesi` | | report settimanale |

Che le nove intensita' coprano ciascuna categoria una volta sola non e'
esprimibile nello schema: lo verifica la scrittura settimanale.

## A5 — esito

`ciclo`, `esito` (Approvato / Da rivedere), `rilievi[]` (controllo C1-C9,
id_rischio o null, gravita' Bloccante/Osservazione, descrizione), `sintesi`.
Gli stessi campi li produce `controlli_a5.py`: i due esiti si leggono e si
combinano allo stesso modo. Tutti i rilievi vanno nel registro: colonna
Rilievi del RiskRegister (per rischio) e Rilievi_Ciclo di Sintesi_Cicli; con
D-71 (06/10/2026) A5 e' facoltativo, un suo Bloccante non ferma il ciclo e
le segnalazioni da motivare, dei controlli e di A5, sono marcate DA MOTIVARE,
compaiono nella colonna Segnalazioni del foglio Validazione e il loro numero
va in Rilievi_Superati (fino al 05/10, con `--procedi-con-rilievi` e D-56, i
Bloccanti dell'agente superati erano marcati BLOCCANTE SUPERATO).

## A6 — schede dei rischi

`ciclo`; `schede[]`, una per rischio del ciclo: `id_rischio`,
`descrizione_estesa` (300-1800 caratteri; il prompt chiede 400-1500: il
fenomeno in termini di rischio, senza i motivi dei punteggi),
`dimensioni[]` (esattamente quattro: `dimensione` fra impatto, probabilita,
prossimita, velocity; `spiegazione` 40-600 caratteri, il prompt chiede 80-500:
perche' il valore, con le informazioni e i documenti, partendo dalla
motivazione di A1, D-68; per una
Velocity non valutata si spiega perche' manca), `fonti[]` (`riferimento` identico a quello dell'input,
`a_sostegno_di` 10-400 caratteri). Cio' che lo schema non puo' vedere lo
controlla `07_Senza_Studio/schede.py` (`controlla_a6`): stessi rischi
dell'input, quattro dimensioni diverse, stesse fonti, nessun numero fuori dai dati
del rischio e dalla rubrica. Destinazione: il file `Schede_<ciclo>.xlsx`, mai
il registro.

## Input delle schede (prodotto dallo script, non da un agente)

`esegui_ciclo_locale.py schede-input` scrive `Cicli/<ciclo>/Schede_input_<ciclo>.json`
dal registro validato: `ciclo`, `data_riferimento`, `ciclo_precedente`,
`pesi`, `rischi[]` in ordine di classifica (id, nome, event type e nome,
driver, owner, attenzione del supervisore, anni di adeguamento, presidio dei
controlli, esito, descrizione, `razionale_rischio` (la parte RISCHIO del
razionale; il razionale intero se A1 non l'ha diviso) e `motivazioni` (impatto,
probabilita, prossimita, velocity, adeguamento; null se il razionale non e'
diviso, D-68), `valori` (impatto, probabilita,
prossimita, velocity; null = non valutata), score e score del
ciclo prima, `urgenza` con esito, x, y, z e margine, segnali netti delle
ultime 4 settimane, `livello_allerta` (livello e motivo, D-63), variazioni,
fonti, azioni del ciclo o aperte (con `razionale` ed `effetto_atteso`), KRI in
vigore con tipo, valore, valore del ciclo prima, soglie, stato, `razionale` ed
`effetto_atteso`, `storia` degli
ultimi otto cicli, posizione in classifica). Come la baseline, e' codice: non
ha uno schema proprio.

## Baseline (prodotta dallo script, non da un agente)

`esegui_ciclo_locale.py baseline` scrive `Baseline_corrente.json` (e una copia
identica `Baseline_corrente.txt`, perche' la knowledge di Agent Builder non
legge .json), input di
A1, A3, A4 e A5: `ciclo_precedente`, `data_riferimento_precedente`,
`ciclo_da_valutare`, `data_riferimento`, `rischi[]` (id, nome, event_type,
driver, owner, presidio dei controlli, anni di adeguamento (dall'anagrafica), impatto,
velocity (null = non valutata), prossimita, probabilita, esito_precedente, razionale, fonti,
storico dei due cicli prima), `kri_in_vigore[]` (con valore e data
dell'ultima rilevazione), `azioni_aperte[]`. E' codice, non un contratto con
un LLM: non ha uno schema proprio, e il collaudo verifica che sia
esattamente quella usata per scrivere i payload di prova.

Accanto alla baseline lo script scrive l'**allegato di A1**
`Input_A1_<ciclo>.txt` (D-69, `07_Senza_Studio/input_a1.py`): un testo in tre
parti, la baseline (lo stesso JSON), i nove controlli di A5
(`controlli_A5.md`) e la guida di scrittura (`guida_scrittura_A1.md`). Lo
riscrive ogni volta che aggiorna la baseline e toglie quello del ciclo
precedente. Con `baseline --uscita <file>` scrive solo il file indicato.

Il comando `precontrollo --payload A1.json` confronta l'output di A1 con
`Baseline_corrente.json` prima di A5: schema, controlli meccanizzati e parti
del razionale. Se trova qualcosa scrive `Cicli/<ciclo>/Correzione_A1_<ciclo>.txt`,
il messaggio di correzione per A1. Non apre il registro.
