# Controlli di A5 Challenger (C1-C9)

> Fonte unica dei nove controlli (D-69, 02/10/2026). Lo stesso testo entra:
> - nelle istruzioni di A5 (segnaposto {{CONTROLLI}} di 02_Agenti/componi_prompt.py);
> - nell'allegato Input_A1_<ciclo>.txt che lo script scrive con la baseline
>   (07_Senza_Studio/input_a1.py): A1 verifica il proprio output con gli stessi
>   controlli prima di rispondere.
> La parte meccanizzabile (tutto tranne C4) e' in 07_Senza_Studio/controlli_a5.py
> e la usa anche il comando precontrollo: se cambia un controllo qui, cambiare
> il codice, il collaudo (99_Collaudo/test_controlli.py) e la tabella dei
> controlli in 04_Riferimenti/controlli_e_model_risk.md. Le righe che iniziano
> con ">" non entrano ne' nel prompt ne' nell'allegato.
> Dal 06/10/2026 (D-71) A5 e' facoltativo e nessun suo rilievo ferma il ciclo:
> lo script ferma solo C1, C2, C7 e gli identificativi dei KRI di C9 (integrita'
> del registro); C3, le date di C5, la coppia e le soglie dei KRI di C9 e i
> Bloccanti di A5 sono "Da motivare": colonna Segnalazioni del foglio
> Validazione, Motivazione obbligatoria.

> D-81 (19/10/2026): la parte meccanizzata di C5 legge anche la frase "ESPOSIZIONE NON NOTA: con l'esposizione
> documentata sarebbe N" che A1 scrive nella parte PROBABILITA del razionale (guida di scrittura) e la porta in
> validazione come "Da motivare", con i due valori: decide il validatore. Il testo di C5 qui sotto non cambia (il
> prompt di A5 e' a 7.990 caratteri).

- C1 Completezza: ogni rischio di "rischi" della baseline (il radar) e' valutato, con la stessa categoria; nessun id_rischio ripetuto; un rischio nuovo ha un id non presente in baseline.
- C2 Variazioni: una voce per ogni valore cambiato rispetto alla baseline e solo per quelli; nessuna per un rischio nuovo.
- C3 Evidenza delle variazioni: data_evidenza dopo data_riferimento_precedente e non dopo data_riferimento; evidenza specifica, non una frase generica; nessun valore cambiato di piu' di un punto (una velocity prima null puo' entrare con qualunque valore).
- C4 Plausibilita': gli score corrispondono ai descrittori della rubrica, dati razionale e fonti (Probabilita 4-5 con la Banca esposta); categoria coerente con la tassonomia; un rischio = un meccanismo di perdita; velocity solo se le fonti documentano i tempi; la deroga alla Prossimita 4-5 e' dichiarata e riguarda un fenomeno ad altissimo impatto; anni_adeguamento motivati; una riduzione ha lo stesso onere di un aumento; un numero senza fonte non dichiarato come valutazione e' un'Osservazione.
- C5 Fonti: rilevanza coerente con i descrittori della rubrica; Probabilita 5 o Prossimita 4-5 con almeno una fonte di rilevanza 3, salvo deroga dichiarata; nessuna fonte datata dopo data_riferimento; un rischio confermato con meno fonti della baseline rivede i valori.
- C6 Deriva: aumenti sostenuti solo dallo stesso fatto ripetuto o da copertura mediatica; aumenti su piu' della meta' dei rischi senza fonti nuove (inflazione progressiva).
- C7 Rilettura KRI: ogni kri_id riletto e' in vigore nella baseline e compare una sola volta.
- C8 Azioni (sempre Osservazione): owner e' una funzione, mai una persona; l'azione e' pertinente al meccanismo di perdita e non ripete un'azione aperta della baseline.
- C9 KRI: due per rischio del radar, uno di Esposizione e uno di Evoluzione, coerenti con cio' che misurano; fonte_dati identificabile; soglie entrambe o nessuna, soglia_allerta >= soglia_attenzione; valore crescente = peggio; un kri_id valorizzato esiste in baseline ed e' dello stesso rischio; nessun kri_id ripetuto.
