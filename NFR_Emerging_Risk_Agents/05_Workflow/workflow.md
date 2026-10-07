# Workflow — W0, W1, W2, W3

Specifica per chi configura Power Automate e Copilot Studio. Ogni passo e'
etichettato **[Piattaforma]** (lo esegue il sistema) o **[Umano]** (lo esegue
una persona, e resta traccia di chi). Per l'ambiente senza Copilot Studio vedi
`07_Senza_Studio/README_variante_locale.md`: i passi sono gli stessi, cambia
chi li esegue.

## Scelta di fondo: una sola implementazione della scrittura

Validazione, controlli meccanizzati di A5, scrittura nel workbook e verifica
di copertura sono gia' implementati e collaudati in
`07_Senza_Studio/esegui_ciclo_locale.py`. Nella variante con Power Automate
**si riusa lo stesso strumento**, lanciato da un desktop flow (Power Automate
Desktop, azione "Esegui script" su una postazione Windows con Excel), invece
di riscrivere la logica con le azioni del connettore Excel. Motivi:

- una sola implementazione delle regole: nessuna seconda versione da tenere
  allineata, e il collaudo di `99_Collaudo` vale anche per questa variante;
- "Analizza JSON" di Power Automate controlla tipi e campi obbligatori, ma NON
  pattern, enum, minimi/massimi, `additionalProperties` ne' i controlli di A5:
  da solo lascerebbe passare proprio i difetti che contano.

Requisito: una postazione (o VM) Windows con Excel e Python, e la licenza per
i desktop flow (attended se lanciato da un utente, unattended se
schedulato). Se non e' disponibile, l'alternativa e' eseguire lo script a mano
come nella variante locale: il resto del workflow non cambia.

## W0 — Raccolta fonti (giornaliero)

L'elenco delle fonti e' `01_Kernel/fonti.md` (unica fonte; validato il 24/09:
tutte approvate tranne FNT-19, esclusa, vedi `08_Deploy/DECISIONI.md`). Tre
canali, usati insieme:

| Canale | Chi lo legge | Dove arriva |
|---|---|---|
| `rss` | W0, deterministico | `News_Inbox/<lunedi'>/Raccolta_<data>.txt`, ogni voce col codice fonte |
| `sito` | l'agente (knowledge web, al massimo 4 siti) o l'analista | l'analista salva in `News_Inbox/<lunedi'>/Manuali/` |
| `share` | l'agente (knowledge SharePoint) | `Analisi_Interne`, o `Manuali` per i contenuti a licenza |

1. [Piattaforma] Trigger giornaliero (o settimanale, il lunedi' prima di W2).
2. [Piattaforma] Legge le fonti `rss` con stato `approvata`:
   `raccogli_notizie.py` (lo stesso script in entrambe le varianti: in Power
   Automate da un desktop flow, come la scrittura).
3. [Piattaforma] Tiene le voci degli ultimi 7 giorni, scarta le parole
   `escludi` della fonte e i link gia' raccolti (`News_Inbox/_visti.json`), e
   scrive la raccolta della settimana. Le fonti irraggiungibili sono elencate
   in testa al file.
4. [Umano] Gli analisti salvano in `Manuali/` cio' che non arriva da un feed
   (siti senza feed, threat intelligence a pagamento, newsletter).
5. [Umano] Una volta all'anno, la funzione di rischio rivede l'elenco delle fonti
   e le licenze d'uso (vedi `06_Governance`); nel frattempo, controlla le fonti
   che risultano irraggiungibili o senza notizie da settimane.

Nessun LLM in W0: e' raccolta deterministica, la selezione di merito la fa A3.
Lasciarlo girare almeno due settimane prima del primo ciclo, per avere notizie
in `News_Inbox`.

## W1 — Ciclo trimestrale

1. [Piattaforma] Trigger: primo giorno lavorativo dopo la fine del trimestre, o
   avvio manuale.
2. [Piattaforma] Esporta la baseline: `esegui_ciclo_locale.py baseline`. Produce
   `Baseline_corrente.json` (ciclo precedente e sua data, ciclo da valutare,
   rischi con score e fonti, storico di due cicli, KRI in vigore, azioni aperte,
   voci della lista di osservazione, D-73)
   e, accanto, l'allegato di A1 `Input_A1_<ciclo>.txt` (D-69): la baseline, i
   nove controlli di A5 (`01_Kernel/controlli_A5.md`, lo stesso testo del
   prompt di A5) e la guida di scrittura (`01_Kernel/guida_scrittura_A1.md`).
3. [Piattaforma] Esegue A1 passando l'allegato `Input_A1_<ciclo>.txt` come
   input; A1 verifica il proprio output con controlli e guida prima di
   rispondere (passo 10 del prompt). Salva l'output (JSON) in un file.
3-bis. [Piattaforma] Precontrollo, facoltativo (D-69, D-71):
   `esegui_ciclo_locale.py precontrollo --payload A1_<ciclo>.json`. Senza
   Excel e senza aprire il registro applica schema, controlli meccanizzati e
   parti del razionale (D-68) rispetto a `Baseline_corrente.json`; se trova
   qualcosa scrive `Cicli/<ciclo>/Correzione_A1_<ciclo>.txt`, il messaggio di
   correzione per A1, e si torna al punto 3. Codice 1 con punti che
   fermerebbero la scrittura, 0 altrimenti. I controlli sono gli stessi del
   punto 5.2: il precontrollo li anticipa (prima di A5, se lo si usa) senza
   scrivere niente.
4. [Piattaforma] **Facoltativo** (D-71): esegue A5 passando SOLO l'output di A1
   e la baseline (nessuna knowledge, nessuna notizia); salva l'output in un
   file. **Quando**: dopo A1 e prima della scrittura, e di nuovo ogni volta che
   A1 viene rifatto (l'esito vale solo per l'output esaminato). I suoi rilievi
   non fermano la scrittura: vanno in validazione. A5 non si lancia per W2, per
   i pareri di A4 ne' dopo la validazione.
5. [Piattaforma] Esegue la scrittura:
   `esegui_ciclo_locale.py trimestrale --payload A1_<ciclo>.json [--challenger A5_<ciclo>.json]`
   (`--procedi-con-rilievi` di D-56 resta accettata ma non serve piu', D-71).
   Lo strumento, in ordine:
   0. **arresto** se il ciclo precedente ha ancora righe da validare (storico
      delle validazioni, Stato "Da decidere"): un ciclo nuovo non si costruisce
      su valutazioni non accettate (passo 8 del ciclo precedente);
   1. valida A1 contro lo schema — **arresto** se non conforme;
   2. applica i controlli meccanizzati e, se c'e', legge l'esito dell'agente
      A5 — **arresto** solo per un Bloccante dei controlli, cioe' un difetto di
      integrita' (C1, C2, C7, identificativi dei KRI), con il messaggio per A1
      in `Cicli/<ciclo>/Correzione_A1_<ciclo>.txt`; **arresto** anche se
      l'esito di A5 e' di un altro ciclo o cita rischi che non sono nell'output
      di A1. C3, le date di C5, la coppia e le soglie dei KRI e i Bloccanti di
      A5 sono **da motivare** (D-71): non fermano, finiscono sui rischi
      (colonna Rilievi del RiskRegister, colonna Segnalazioni della griglia) o
      sul ciclo (Sintesi_Cicli), il loro numero in Sintesi_Cicli e in
      `Esito_controlli_<ciclo>.json`;
   3. prende i KRI in vigore nel ciclo precedente e ne scrive la riga del
      ciclo con il valore riletto ora (valore, fonte, nota, data; vuoto se non
      rilevato, mai ricopiato: A1 rilegge solo i valori che trova);
   4. aggiorna la definizione dei KRI riproposti (un KRI riproposto senza
      soglie conserva quelle gia' validate); mette `In_Vigore = No` ai
      KRI non riproposti (ultima riga della loro serie); aggiunge i KRI nuovi
      con il primo progressivo libero del rischio (mai la posizione
      nell'array). Tutto **in coda** allo storico KRI: le righe dei cicli
      prima non si toccano;
   5. aggiorna l'anagrafica (rischi nuovi con Owner "Da assegnare" e
      Presidio_Controlli "Non verificato"; Owner, Anni_Adeguamento,
      Attenzione_Supervisore e Presidio_Controlli, input umani, restano come sono);
   6. prima di scrivere toglie dalle fonti i codici interni dello strumento
      di ricerca (`turn…`), calcola l'esito di ogni rischio e aggiunge "da" e
      "a" alle variazioni dalla baseline (D-51); poi
      fa append su RiskRegister, Azioni e Sintesi_Cicli (la `sintesi` di A1,
      cioe' il commento per il comitato, e quella di A5), relativo alla TABELLA;
   6-ter. scrive la **lista di osservazione** (D-73) in coda a tblOsservazione:
      le voci di A1 (codice nuovo = primo OSS-nn libero, mai riusato) e, dopo,
      le voci "In osservazione" del ciclo prima che A1 non ha toccato, con Esito
      Invariata: ogni ciclo ha la fotografia intera della lista. I controlli
      del punto 2 hanno gia' fermato codici e promozioni incoerenti (C1);
   6-bis. aggiunge allo storico delle validazioni (tabella tblValidazione,
      foglio Storico_Validazioni) una riga "Da decidere" per ogni campo
      proposto (5 per rischio: Impatto, Velocity, Prossimita, Probabilita,
      Anni_Adeguamento; 3 per KRI; 2 per azione; 3 per voce in osservazione
      proposta da A1: impatto potenziale, orizzonte, plausibilita') e riscrive la griglia del
      foglio Validazione, una riga per oggetto con le celle gialle uguali alle
      proposte (D-67), conservando cio' che il validatore ha gia' scritto per
      altri periodi ancora da validare (le settimane);
   7. imposta il ciclo corrente;
   8. ricalcola in Excel e verifica: formule integre, zero errori, copertura
      calcolata in Python uguale a quella del foglio (Registro, nomi coperturaAnagrafica e coperturaValutati), ciclo
      completo — **arresto senza salvare** se una verifica fallisce (gate);
   9. adatta l'impaginazione del report (altezze delle righe con testi
      calcolati: commento e rischi segnalati del Quadro, motivi del Delta,
      con il grafico del Delta che non deve coprire la nota sottostante) e
      solo ora salva, dopo il backup
      del file. Prima di tutto, all'apertura, si ferma se il registro e' nato
      da un template di un'altra versione (`versioneTemplate`: vedi
      "Aggiornamento del template" sotto);
   10. archivia in `Archivio_Cicli/Cicli/<ciclo>/` l'**Excel di output**
       `NFR_Registro_<ciclo>.xlsx` (copia congelata del registro dopo il
       ciclo), gli output di A1 e A5, la baseline usata, l'esito dei controlli
       e `Righe_liste_<ciclo>.json` (valori ancora da validare: il passo 9 lo
       riscrive); aggiorna `Baseline_corrente.json`. Se l'anagrafica ha 2 posti
       liberi o meno, lo dice (`MAX_RISCHI`).
   Codice di uscita: 0 eseguito, 1 fermato (workbook intatto), 2 errore tecnico.
   Con 2 il messaggio distingue: prima del salvataggio (nulla scritto) o
   **dopo** (registro gia' scritto, baseline gia' aggiornata, archivio da
   completare a mano — tipicamente un Excel dell'archivio aperto da qualcuno:
   **non rilanciare** il ciclo).
6. [Piattaforma] Se il codice e' 1 o 2 il ciclo si ferma; il motivo e' in
   `Cicli/<ciclo>/tentativo_<ora>/Esito_controlli_<ciclo>.json` (ogni tentativo resta archiviato). Il ciclo si rilancia
   dopo la correzione (nuovo run di A1, o correzione a mano del payload con
   traccia in `Archivio_Cicli`).
7. (Il caricamento delle liste avviene DOPO la validazione, passo 9-bis: prima
   le liste riceverebbero valori non ancora accettati dalla Banca.)
8. [Umano] **Validazione.** Il validatore (funzione di rischio o comitato)
   legge l'Excel di output del ciclo e, nel registro vivo, il foglio
   Validazione: una riga per rischio, KRI e azione (D-67), con la proposta in
   grigio e accanto la cella gialla gia' compilata con la proposta. Una riga
   che non tocca vale come accettata. Se non e' d'accordo:
   - cambia il valore nella cella gialla (anche piu' d'uno nella stessa riga) e
     scrive la `Motivazione` della riga, almeno 10 caratteri (per un rischio,
     un intero 1-5 a non piu' di un punto dal ciclo precedente — la Velocity
     puo' restare vuota, "non valutata", e da vuota entra con qualunque
     valore; per un KRI un numero, con le due soglie entrambe o nessuna; per
     gli anni di adeguamento un numero da 0 a 30 o vuoto, e il valore deciso va
     nell'anagrafica (D-60); per un'azione owner, una funzione e non una
     persona, o orizzonte);
   - scrive `Respingi = Sì` + `Motivazione` (KRI, azione o notizia da
     scartare per intero; un rischio non si respinge, si rettifica).
   Score composito e Margine di Mosca della riga di ogni rischio si
   ricalcolano mentre scrive. La colonna Segnalazioni dei controlli mostra
   cio' che lo script e A5 hanno trovato sul rischio; un rischio con una
   segnalazione da motivare (⚑ davanti al nome; "DA MOTIVARE") chiede la
   Motivazione anche se i valori restano quelli proposti, e `valida` non
   accetta un salto di piu' di un punto ne' soglie invertite, anche se proposti
   da A1 (D-71).
   Per le azioni la decisione del validatore e' la delibera: accettata o
   rettificata = Approvata, respinta = Respinta. Nell'anagrafica il validatore
   aggiorna quando serve il Presidio_Controlli (colonna O). Salva e chiude il file.
9. [Piattaforma] `esegui_ciclo_locale.py valida --periodo <ciclo> --validatore "<chi>"`:
   legge la griglia e trasforma ogni riga nelle decisioni campo per campo
   (cella gialla uguale alla proposta = Accettato, diversa = Rettificato,
   Respingi = Respinto per tutti i campi dell'oggetto); controlla TUTTE le
   righe (se una non va, non applica niente e le elenca con il numero di
   riga; si ferma anche se la griglia non corrisponde alle proposte, e indica
   il comando `griglia` che la ricostruisce), le applica ai dati (valori;
   esito ricalcolato e Variazioni riscritte in modo coerente con i valori
   validati, con la motivazione della rettifica come evidenza; KRI respinti
   fuori vigore; valore di un KRI rettificato con data e fonte della
   rilevazione; stato delle azioni), scrive `Approvato_Da`,
   `Data_Validazione`, `Validazione`, compila lo storico (Decisione,
   Valore_Validato, Motivazione, Validato_Da, Data_Validazione) e mette le sue
   righe in Stato "Applicata", toglie il periodo dalla griglia, salva (backup
   prima), archivia `Validazione_<ciclo>.json` e
   `NFR_Registro_<ciclo>_validato.xlsx`, **riscrive `Righe_liste_<ciclo>.json`
   con i valori validati** e aggiorna la baseline. **Mai auto-approvazione per
   decorrenza dei termini**: finche' ci sono righe "Da decidere" il ciclo non
   e' validato (Registro, riga 4; fascia del titolo "da validare") e il ciclo
   dopo non parte.
   La proposta dell'agente non si cancella mai: le righe Rettificato
   (proposta, valore deciso, motivo) sono la base dati per l'apprendimento
   futuro degli agenti.
9-bis. [Piattaforma] Carica `Righe_liste_<ciclo>.json` (quello riscritto dal
    passo 9) nelle tre liste (un "Crea elemento" per riga, nessuna logica).
10. [Umano] Copia in `Cicli/<ciclo>/` il testo dei prompt in uso (i prompt si
    modificano nell'interfaccia senza traccia).
11. [Piattaforma, facoltativo ma consigliato] **Schede dei rischi** (D-40):
    `esegui_ciclo_locale.py schede-input` scrive
    `Cicli/<ciclo>/Schede_input_<ciclo>.json` dal registro validato (si ferma
    se il ciclo ha ancora decisioni da prendere); lo si allega, da solo,
    all'agente **A6**; il suo output si salva come `A6_<ciclo>.json` e
    `esegui_ciclo_locale.py schede --payload A6_<ciclo>.json` lo controlla
    (schema; stessi rischi, quattro dimensioni — Impatto, Probabilita,
    Prossimita, Velocity —, stesse fonti, nessun numero fuori dai dati) e scrive `Cicli/<ciclo>/Schede_<ciclo>.xlsx`, un indice e una scheda per
    rischio in ordine di classifica. Senza `--payload` le schede escono con i
    testi del registro. Il registro non si tocca. Dal 02/10/2026 (D-68) il
    razionale di A1 e' diviso in parti (RISCHIO:, IMPATTO:, PROBABILITA:,
    PROSSIMITA:, VELOCITY:, ADEGUAMENTO:) e quello di azioni e KRI finisce con
    EFFETTO:: la scheda mette il Razionale (il fenomeno) dopo il rischio, il
    perche' di ogni valore accanto al valore e, sotto ogni azione e KRI, il
    perche' e l'effetto atteso, anche senza A6. Al passo 5 `trimestrale` avvisa
    se un razionale non e' diviso (istruzioni di A1 non aggiornate).
12. [Piattaforma] **Report al comitato** (decisioni D-31, D-32, D-39, D-62):
    `esegui_ciclo_locale.py report [--con-lavoro] [--file <xlsx>]` rigenera
    `Cicli/<ciclo>/Report_comitato_<ciclo>.pdf` (Quadro, Classifica,
    Radar_Mosca, Matrice, Delta, Fenomeni, Metodologia; con `--con-lavoro` anche Registro
    e Parametri, in orizzontale su una pagina di larghezza) dal registro vivo,
    in sola lettura; si ferma se il ciclo ha decisioni da prendere. Si rilancia
    dopo ogni modifica manuale dei validatori (presidio, anni di adeguamento,
    attenzione del supervisore, stato delle azioni): la versione precedente
    del PDF resta con la data nel nome. Si allega il file delle schede. Il Quadro
    contiene il commento di A1 (messaggio e decisioni) scritto prima della
    validazione: se ci sono state rettifiche lo dice ("Dopo il commento") e
    valgono i numeri validati; i rischi segnalati e il loro perche' li calcola il
    foglio dai dati validati.

## Eventi fuori ciclo

- **Ciclo straordinario** (D-41, D-75): A3 (`proposta_straordinario`) o A4 propongono,
  con la regola del segnale critico della rubrica (sezione 6); la funzione di rischio
  decide con `esegui_ciclo_locale.py baseline --straordinario --rischi ... --motivo ...
  --decisore ... [--data ...]`, che archivia la decisione in
  `Cicli/<AAAAQn-Sk>/Straordinario_<AAAAQn-Sk>.json` e scrive baseline e allegato di A1
  per il periodo `AAAAQn-Sk` (il trimestre del ciclo corrente, primo numero libero).
  A1 rivaluta solo i rischi indicati (guida di scrittura, "Ciclo straordinario"); i
  controlli in modo straordinario fermano un rischio indicato assente o un rischio
  esistente non indicato (C1). `trimestrale` riconosce il periodo dal payload: scrive i
  rischi rivalutati da validare e riporta gli altri dal ciclo prima, validati come
  allora, con `Periodo_Valutazione` = periodo d'origine (da cui il Radar_Mosca prende la
  Y); i KRI dei rischi non rivalutati restano con valore e validazione; Sintesi_Cicli
  ha la colonna Straordinario. La validazione mette in griglia solo cio' che e' stato
  rivalutato; la regola del punto si misura sul periodo prima (lo straordinario conta
  come ciclo). I periodi delle viste (precedente, trend, data di riferimento) li scrive
  lo script in Parametri; il trimestre dopo parte dai valori dello straordinario.

- **Primo uso**: `esegui_ciclo_locale.py inizializza --ciclo-precedente <AAAAQn> --settimana <lunedi'>`
  crea il registro vivo dal template senza dati di esempio (non sovrascrive un
  file esistente). Il primo ciclo trimestrale propone tutti i rischi come Nuovi:
  uno per meccanismo di perdita sostenuto da almeno una fonte specifica,
  nessuna categoria obbligatoria (D-55); le categorie rimaste senza rischi
  sono elencate nella sintesi di A1.
- **Tassonomia interna** (D-74, dal 08/10/2026): le categorie sono le nove in
  perimetro della tassonomia della Banca. Un registro aggiornato da una versione
  precedente ha i codici di Basilea: al primo ciclo A1 li riclassifica
  (Osservazione C1) o segna FP i rischi fuori perimetro (da motivare, poi
  `dismetti`); fino ad allora il radar non li mostra.
- **Dismissione di un rischio** (decisione della funzione di rischio):
  `esegui_ciclo_locale.py dismetti --rischio NFR-nn --motivazione "..." --decisore "..."`.
  Toglie il rischio dall'anagrafica senza lasciare righe vuote (le viste
  leggono le prime N righe), mette `In_Vigore = No` ai suoi KRI del
  ciclo corrente, porta le sue azioni aperte ad "Annullata", aggiorna la
  baseline e archivia l'atto in `Archivio_Cicli/Dismissioni/`. La storia resta.
  Non si svuotano MAI a mano righe dell'anagrafica.
- **Anni di adeguamento di un rischio** (decisione del validatore): nel
  registro vivo, Parametri, colonna M dell'anagrafica, gli anni che servono per
  un adeguamento strutturale (es. migrazione crittografica, uscita da un
  fornitore). Diventano la Y minima del Radar_Mosca; la scrittura dei cicli li
  conserva.
- **Attenzione del supervisore** (decisione del validatore, D-35): nel
  registro vivo, Parametri, colonna N dell'anagrafica, "Sì" per i rischi il
  cui tema e' nelle priorita' o nelle comunicazioni di BCE, EBA o Banca
  d'Italia. Nel Radar_Mosca l'ID del rischio ha il ◆ (dal 01/10: il colore del cerchio e' il livello di allerta, D-63), nelle
  tabelle compare ◆; la scrittura dei cicli lo conserva.
- **Presidio dei controlli** (decisione del validatore, D-49): nel registro
  vivo, Parametri, colonna O dell'anagrafica, il giudizio della Banca sui
  controlli esistenti del rischio: Non verificato (valore iniziale), Adeguato,
  Parziale, Assente. Gli agenti non vedono i controlli interni: il dato si
  legge nel Registro e nelle schede e non entra nello score; la scrittura dei
  cicli lo conserva.
- **Avanzamento delle azioni**: la funzione di rischio porta un'azione
  approvata a "In corso" o "Completata" nella colonna Stato del foglio Azioni
  (unica colonna dei dati modificabile a mano), quando l'owner lo comunica.
  Le azioni non Completate, Respinte o Annullate passano ad A1 come aperte.
  Il foglio Piano_azioni le mostra tutte, prima le proposte da decidere, con
  la scadenza (data della decisione + orizzonte).
- **Aggiornamento del template**: quando cambia la struttura del workbook
  (nuova `versioneTemplate`), ogni comando si ferma sul registro vecchio e
  indica `esegui_ciclo_locale.py aggiorna-registro`. Il comando copia per nome
  di colonna tutte le righe, l'anagrafica (con owner e anni di adeguamento) e
  i parametri di calendario nel template nuovo, ricalcola, verifica (stesse
  righe, zero errori, stessa copertura, baseline identica) e solo allora
  sostituisce il file, lasciando il vecchio in `Backup`. Pesi, soglie e Z per
  Prossimita restano quelli del template nuovo (lo script stampa i vecchi).
  Le colonne tolte dal modello (`colonne_dismesse` della mappa: Gap_Controlli,
  Confidence, Dimensione delle azioni) restano solo nel backup; quelle
  rinominate (`colonne_rinominate`: Severity -> Impatto, D-57) passano alla
  nuova; le righe ancora da validare passano nella griglia del foglio
  Validazione con cio' che il validatore aveva gia' scritto (anche nel vecchio
  foglio Validazione, una riga per campo, D-67); si ferma solo se ci sono righe
  da validare su campi tolti dal modello.
- **Griglia di validazione rovinata a mano** (righe cancellate o inserite, ID
  cambiati): `esegui_ciclo_locale.py griglia` la ricostruisce dalle proposte
  ancora da decidere, conservando i valori gialli, le Motivazioni e i Respingi
  delle righe intatte.

## W2 — Aggiornamento settimanale

1. [Piattaforma] Trigger settimanale (lunedi', dopo W0).
2. [Piattaforma] Esegue A3 con la baseline e le notizie della settimana dai tre
   canali; salva l'output.
3. [Piattaforma] `esegui_ciclo_locale.py settimanale --payload A3_<settimana>.json`:
   valida, verifica che ogni notizia abbia le nove intensita' (una per categoria), un codice fonte
   dell'elenco (o MAN), un id non ripetuto nell'output, che i rischi
   collegati e quelli dei flag esistano e che le voci della lista di
   osservazione indicate da A3 (`voce_osservazione` delle notizie,
   `segnali_osservazione`, D-73) siano in osservazione nel ciclo corrente, aggiunge le notizie (ogni testo scritto
   come testo: un titolo che inizia con "=" non diventa una formula)
   senza duplicati, fa scorrere la
   settimana corrente in Parametri (l'unica manutenzione settimanale del
   workbook: se saltata non c'e' errore, ma segnali netti e pressione mostrano un
   passato sempre piu' vecchio), ricalcola, verifica, salva, e archivia in
   `Archivio_Cicli/Settimane/<lunedi'>/` l'Excel di output
   `NFR_Registro_<lunedi'>.xlsx` e l'output di A3. A video: segnali netti oltre la soglia,
   aree non presidiate, numero di flag proposti, notizie e segnali sulla lista di
   osservazione. I segnali (Avvicina, Segnale verificato, Allontana) vanno nella
   colonna Segnali_Osservazione di Sintesi_Settimane e, con le notizie collegate,
   nella baseline del ciclo dopo (`notizie_a3`, `segnali_a3` di ogni voce): A1 li
   verifica come evidenza.
4. [Umano] La funzione di rischio apre l'Excel della settimana e legge la
   sintesi di A3. I flag sono proposte per il
   prossimo ciclo trimestrale: nessuno score cambia in W2.
5. [Umano, consigliato] Validazione delle notizie: nel foglio Validazione, una
   riga per notizia (rischio collegato, segnale e voce della lista di
   osservazione, colonna Settimana), si
   cambiano o si respingono come nel W1, poi
   `valida --periodo <lunedi'> --validatore "<chi>"`. Una notizia respinta
   diventa "Non rilevante" con impatti 0: non pesa piu' su segnali netti e
   pressione. Non e' bloccante: la settimana dopo parte comunque; le notizie
   non validate restano nella griglia (oltre 200 il settimanale si ferma e
   chiede di validare le settimane piu' vecchie).

## W3 — A4 su richiesta

Nessun flow. A4 e' pubblicato solo al gruppo Teams della funzione di rischio,
con `Baseline_corrente.txt` in knowledge (copia della .json: la knowledge non
legge .json). Il parere non scrive nulla e non e'
vincolante. Se un parere suggerisce di rivedere un rischio, la via e' il
prossimo ciclo trimestrale.

## W4 — A7 su richiesta (spiegazioni, D-72)

Nessun flow e nessun comando: A7 Assistente del registro risponde in chat e legge
la cartella `Kernel/Spiegazioni` (`Ciclo.txt` e `Rischio_01.txt` ... `Rischio_20.txt`, uno per
posto dell'anagrafica, nomi fissi), che
`trimestrale`, `valida` e `dismetti` riscrivono alla fine dal registro aperto
(`07_Senza_Studio/spiegazioni.py`; un errore e' solo un avviso). Con il kernel del
pacchetto (collaudo, demo) la cartella va in quella di uscita. A7 non scrive
nulla; la sua "sintesi per il Quadro" la incolla l'analista nelle Note
dell'analista (cella `quadroNote`), che `trimestrale` archivia in
`tblSintesi.Note_Analista` del ciclo precedente quando inizia il ciclo nuovo.
I fenomeni considerati e non censiti da A1 (`fenomeni_non_censiti`, facoltativo,
D-72) restano nell'output archiviato di A1 e vanno in `Ciclo.txt`, con la lista
di osservazione del ciclo e le decisioni del validatore sulle voci (D-73).

## Campi derivati

Campi che la scrittura calcola, non l'agente. Sono i nomi `derivato:` di
`01_Kernel/mappatura_campi.json`, implementati nel dizionario `DERIVATI` di
`esegui_ciclo_locale.py` (il collaudo verifica che coincidano).

| Derivato | Valore |
|---|---|
| `vuoto` | cella vuota (Approvato_Da, Data_Decisione, Decisa_Da) |
| `data_scrittura` | data di esecuzione della scrittura |
| `owner_da_anagrafica` | Owner del rischio in anagrafica; "Da assegnare" se nuovo |
| `owner_esistente_o_da_assegnare` | in anagrafica: conserva l'Owner esistente, "Da assegnare" per un rischio nuovo |
| `attenzione_supervisore_esistente` | in anagrafica: conserva l'indicazione del validatore (Sì/No; vuoto per un rischio nuovo); ◆ nel Radar_Mosca |
| `anni_adeguamento_esistente` | in anagrafica: conserva gli anni di adeguamento scritti dal validatore (vuoto per un rischio nuovo); Y minima del Radar_Mosca |
| `sintesi_a5` | in Sintesi_Cicli: la `sintesi` dell'output di A5 esaminato insieme ad A1 |
| `osservazioni_controlli` | in Sintesi_Cicli: numero di rilievi non bloccanti (A5 + controlli meccanizzati) |
| `stato_azione_iniziale` | "Proposta — da valutare" |
| `id_azione` | `<ciclo>-<ID_Rischio>-A<n>`, n = posizione dell'azione nel rischio (anche se due azioni sono identiche) |
| `kri_id` | kri_id del payload se valorizzato; altrimenti primo progressivo libero del rischio (NFR-nn-Kn), mai riusato |
| `data_rilevazione` | vuota per un KRI nuovo; per un KRI in vigore la scrive la rilettura: data di riferimento del ciclo se c'e' un valore, vuota altrimenti |
| `in_vigore` | "Sì" per i KRI proposti; "No" nella riga del ciclo in cui un KRI non e' riproposto (poi la serie finisce) |
| `ciclo_definizione` | ciclo in cui il KRI e' nato; non cambia agli aggiornamenti |
| `da_validare` | "Da validare" nella colonna Validazione; il comando `valida` la porta ad Accettato, Rettificato o Respinto |
| `numero_notizie` | in Sintesi_Settimane: quante notizie ha valutato A3 nella settimana (D-66) |
| `flag_proposti` | in Sintesi_Settimane: i flag di A3, uno per riga, "NFR-nn · direzione: motivazione"; "Nessun flag proposto" se non ce ne sono (D-66) |
| `esito` | Nuovo se il rischio non e' nella baseline; Variato se cambia Impatto, Probabilita, Prossimita o Velocity (anche da vuota a un valore); altrimenti Confermato. Ricalcolato dopo la validazione (D-51) |
| `presidio_esistente_o_non_verificato` | in anagrafica: conserva il Presidio_Controlli del validatore, "Non verificato" per un rischio nuovo (D-49) |
| `rilievi_rischio` | nel RiskRegister: le segnalazioni di A5 e dei controlli sul rischio, una per riga `gravita' · controllo · origine: testo`, prima quelle "⚑ DA MOTIVARE" (D-71); le stesse nella colonna Segnalazioni della griglia |
| `rilievi_ciclo` | in Sintesi_Cicli: i rilievi sul ciclo nel suo insieme (senza rischio), stesso formato |
| `rilievi_superati` | in Sintesi_Cicli: quante segnalazioni sono da motivare in validazione, dai controlli e da A5 (D-71) |
| `oss_id` | in Lista_Osservazione: oss_id del payload per una voce esistente; per una voce nuova primo progressivo libero OSS-nn, mai riusato (D-73) |
| `esito_osservazione` | in Lista_Osservazione: l'esito di A1 (Nuova, Confermata, Avvicinata, Promossa, Archiviata); Invariata per le voci in osservazione che A1 non ha toccato, riportate dal ciclo prima |
| `stato_osservazione` | in Lista_Osservazione: In osservazione; Promossa o Archiviata secondo l'esito; la validazione scrive Respinta per una voce nuova respinta |
| `prima_osservazione` | in Lista_Osservazione: il ciclo in cui la voce e' entrata nella lista (dalle righe precedenti; il ciclo corrente per una voce nuova) |
| `segnali_osservazione` | in Sintesi_Settimane: i segnali di A3 sulle voci della lista di osservazione, uno per riga, "OSS-nn · direzione: motivazione"; "Nessun segnale sulla lista di osservazione" se non ce ne sono (D-73) |
| `periodo_valutazione` | nel RiskRegister: il ciclo della riga; per un rischio riportato in un ciclo straordinario, il periodo da cui viene (D-75) |
| `straordinario` | in Sintesi_Cicli: per un ciclo straordinario chi l'ha deciso, quando, il motivo e i rischi rivalutati; vuoto per un trimestre (D-75) |
| `proposta_straordinario` | in Sintesi_Settimane: "PROPOSTA DI CICLO STRAORDINARIO per ...: motivo" se A3 la fa, altrimenti "—" (D-75) |
| `validazione_osservazione` | in Lista_Osservazione: "Da validare" per le voci con un esito di A1, vuota per le voci invariate (gia' validate) |

## Test in ambiente (prima del primo ciclo reale)

1. [Umano] Partire da una copia **vuota** del workbook (nessun trimestre gia'
   valutato a mano: il primo ciclo individua i rischi da zero).
2. [Piattaforma] Eseguire W1 sulla copia, **due volte** sullo stesso input.
3. [Umano] Confrontare i due output con `99_Collaudo/confronta.py
   --primo-ciclo` (abbina i rischi per categoria e nome, perche' nel primo
   ciclo A1 li numera da se'): misura la riproducibilita' reale, retrieval
   incluso (il collaudo a secco non la include). Rischi presenti in un solo run
   o punteggi diversi = il giudizio non e' abbastanza ancorato: rivedere
   descrittori o istruzioni prima di andare in esercizio.
4. [Umano] La funzione di rischio legge l'analisi (aree coperte, motivazioni,
   fonti) e il validatore valida il ciclo di prova: quota di rettifiche e
   criteri di accettazione in `DECISIONI.md`.
