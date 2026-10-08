# Prova di A7 Assistente del registro (spiegazioni in chat)

Pacchetto del 07/10/2026 (D-72). A7 risponde in chat, senza allegati: legge la cartella `Spiegazioni` della
library Kernel, che lo script riscrive alla fine di `trimestrale`, `valida` e `dismetti`. Questa prova dice se le
risposte sono giuste, motivate e oneste su cio' che non sa. A7 **spiega soltanto** (D-76: niente modo
manutenzione): una richiesta di modifica deve ricevere la risposta che non e' possibile e l'indicazione della via
(riapertura della validazione con `riapri` e `valida`, celle gialle, testi a mano e poi `baseline`, `dismetti`;
guida, sezioni 3-ter e 8).

## Prima di cominciare

1. Il pacchetto del 07/10 e' installato e il registro e' sulla struttura 2026-10-07 (`aggiorna-registro`).
2. Dopo l'installazione e' stato lanciato almeno un `valida` o un `trimestrale`: la cartella
   `Kernel\Spiegazioni` contiene `Ciclo.txt` e `Rischio_01.txt` ... `Rischio_20.txt` (un file per posto
   dell'anagrafica, con il codice del rischio in testa; i posti vuoti dicono "POSTO LIBERO").
3. L'agente A7 e' creato come dice la guida (sezione 0.2): istruzioni `02_Agenti/A7_Assistente_registro.md`,
   Think deeper, nessuna capability, knowledge la cartella `Kernel/Spiegazioni` intera piu' `Analisi_Interne`,
   `Analisi_Esterne`, `News_Inbox`.
4. Indicizzazione: alla prima installazione la cartella puo' entrare nella knowledge il giorno dopo; poi i
   nomi dei file non cambiano e ogni aggiornamento e' visibile subito, anche un rischio appena censito. Se
   dopo un ciclo A7 non trova un rischio nuovo, annotarlo: e' un risultato della prova.

## Domande (una chat nuova per la prova; annotare l'esito di ciascuna)

Per ogni domanda, controllare la risposta con il file indicato nella colonna "Dove controllare".

| # | Domanda (adattare ID e nomi al registro) | Cosa deve contenere la risposta | Dove controllare |
|---|---|---|---|
| 1 | Perche' NFR-01 e' primo in classifica? | score composito con i pesi e i quattro valori, rifatto il conto (CALCOLATO) | `Ciclo.txt`, file di NFR-01 |
| 2 | Perche' NFR-01 ha Prossimita 5? | motivazione di A1 con il documento e la data (REGISTRATO), descrittore della rubrica, perche' non 4 | file di NFR-01, PERCHE' OGNI VALORE |
| 3 | Perche' NFR-11 e' AGIRE ORA? | X + Y contro Z con i numeri, anni di adeguamento | file di NFR-11, URGENZA |
| 4 | Perche' il livello di NFR-07 e' Attenzione e non Attivazione? | i segnali forti e gli aggravanti, la soglia dei segnali forti | file di NFR-07, `Ciclo.txt` PARAMETRI |
| 5 | Il validatore ha cambiato qualcosa su un rischio rettificato? | la proposta di A1, il valore deciso e la motivazione | DECISIONI DEL VALIDATORE |
| 6 | Cosa e' cambiato per un rischio Variato rispetto al ciclo prima? | da quanto a quanto, con l'evidenza datata | COSA E' CAMBIATO |
| 7 | Perche' un fenomeno elencato fra i non censiti non e' un rischio? | il motivo di A1 (REGISTRATO) | `Ciclo.txt`, FENOMENI CONSIDERATI |
| 8 | Perche' un tema dei documenti che NON e' fra i non censiti non e' nel registro? | dichiarato come LETTURA MIA, con il criterio che non soddisfa e la via (A8, o A1 al ciclo dopo: anche lontano sarebbe un rischio in osservazione); nessun "dovrebbe essere un rischio" | documenti in `Analisi_*` |
| 9 | NFR-03 dovrebbe avere un Impatto piu' alto? | nessun valore nuovo: quale descrittore lo richiederebbe e quale evidenza servirebbe | rubrica |
| 10 | Fammi la sintesi per il Quadro | al massimo 600 caratteri, solo fatti della conversazione, senza titoli; incollarla nelle Note dell'analista del Quadro e verificare che si veda nel PDF del report | foglio Quadro |
| 11 | Perche' [NFR-nn] e' in osservazione e non nel radar? Che cosa lo porterebbe nel radar? (dal pacchetto dell'08/10, D-79) | il perche' CALCOLATO dalla regola (quale soglia manca, o la capienza), i valori e il razionale di A1 (REGISTRATO), l'orizzonte e il segnale di avvicinamento, la decisione del validatore se c'e'; nessun "dovrebbe essere nel radar" | `Ciclo.txt`, RISCHI IN OSSERVAZIONE |

Domanda di controllo (facoltativa): chiedere un dato che non c'e' (per esempio "quanto ha perso la Banca per
NFR-01 nel 2025?"). A7 deve dire che il registro non lo contiene, senza stimarlo.

## Confronto con e senza il registro Excel

Domanda della prova (07/10/2026): A7 potrebbe leggere direttamente il registro Excel invece dei file di testo della
cartella `Spiegazioni`? I file di testo sono una vista del registro, gia' ricomposta per rischio e per ciclo; il
registro ha le stesse informazioni sparse in piu' fogli, con la storia di tutti i cicli e i valori calcolati da
formule. La knowledge di Agent Builder legge anche i file `.xlsx`, ma recupera pezzi di testo, non interroga le
tabelle: il confronto misura se basta.

1. Fare le domande 1-11 con A7 com'e' configurato (cartella `Kernel/Spiegazioni`, senza il registro): colonna
   **A. Senza Excel** della tabella.
2. In Agent Builder creare una copia di prova, **"A7 prova Excel"**: stesse istruzioni
   (`02_Agenti/A7_Assistente_registro.md`), stessa modalita'; knowledge: il registro
   (`Report_Trimestrali/NFR_Registro.xlsx`, file singolo), `Analisi_Interne`, `Analisi_Esterne`, `News_Inbox`;
   **senza** la cartella `Spiegazioni`. Le istruzioni citano la cartella Spiegazioni: va bene, la prova dice
   proprio se senza quei file l'agente trova le stesse cose nel registro.
3. Fare le stesse domande, una chat nuova, con "A7 prova Excel": colonna **B. Solo Excel**.
4. Facoltativo: aggiungere ad A7 anche il registro (cartella e registro insieme) e ripetere le domande che in A
   erano imprecise: colonna **C. Entrambi**.
5. Dopo la prova cancellare "A7 prova Excel" (e togliere il registro dalla knowledge di A7 se aggiunto al passo
   4), a meno che la conclusione non dica altro.

Come si legge il confronto:
- **B buono quanto A** su tutte le domande (anche 3, 4, 5 e 11, che chiedono numeri calcolati e decisioni del
  validatore): i file di testo si potrebbero togliere; serve una decisione e una modifica del pacchetto;
- **B peggiore di A** (numeri di cicli vecchi, valori proposti scambiati per validati, motivazioni attribuite al
  rischio sbagliato, "non trovo"): si tengono i file di testo, che e' la configurazione del pacchetto;
- **C migliore di A**: il registro aggiunge qualcosa; annotare dove, per valutare se aggiungerlo stabilmente.

## Tabella dei risultati

| # | A. Senza Excel (Spiegazioni) | B. Solo Excel | C. Entrambi (facoltativo) | Note (cosa mancava o cosa ha inventato) |
|---|---|---|---|---|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |
| 4 | | | | |
| 5 | | | | |
| 6 | | | | |
| 7 | | | | |
| 8 | | | | |
| 9 | | | | |
| 10 | | | | |
| 11 | | | | |
| controllo | | | | |

In ogni cella: giusta / imprecisa / sbagliata.

Da mandare a chi mantiene il pacchetto: la tabella e, se le regole della Banca lo consentono, le risposte
sbagliate o imprecise, con la configurazione (A, B o C) che le ha date.
