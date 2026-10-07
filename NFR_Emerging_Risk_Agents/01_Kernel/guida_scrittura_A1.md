# Guida di scrittura di A1

> Come si scrivono descrizione, razionale, azioni e KRI (D-69, 02/10/2026), i fenomeni
> non censiti (D-72) e la lista di osservazione (D-73, 07/10/2026).
> Le istruzioni di A1 sono al limite degli 8.000 caratteri: questa guida entra
> nell'allegato Input_A1_<ciclo>.txt che lo script scrive con la baseline
> (07_Senza_Studio/input_a1.py), insieme ai controlli di A5
> (01_Kernel/controlli_A5.md). A1 la legge a ogni ciclo. Le righe che iniziano
> con ">" non entrano nell'allegato. L'esempio in fondo e' di forma: fatti e
> documenti sono inventati, e la guida lo dice ad A1.
> Le etichette del razionale (RISCHIO:, IMPATTO:, ..., EFFETTO:) sono quelle
> che 07_Senza_Studio/schede.py riconosce (D-68): non cambiarle qui senza
> cambiare anche lo scheletro del prompt di A1 e il codice.

I tuoi testi finiscono nel registro e nelle schede dei rischi per il comitato: chi legge non conosce le fonti e deve capire perche' un rischio conta e da dove viene ogni numero.

## Categoria di rischio
event_type e' il codice della categoria della tassonomia interna (sezione "Categorie di rischio" delle istruzioni) in cui ricade la perdita per la Banca. Un rischio della baseline con un codice di Basilea (L1-01 ... L1-07) va riclassificato: scrivi la categoria in cui ricade il suo meccanismo di perdita, senza cambiare id ne' valori (non e' un cambio di meccanismo). Se il meccanismo non ricade in nessuna categoria in perimetro (per esempio una frode o un tema di financial crime), scrivi "FP" (fuori perimetro) e nel razionale perche': la funzione di rischio lo togliera' dal registro. Un rischio nuovo non e' mai FP: un tema fuori perimetro va fra i fenomeni non censiti (motivo fuori_perimetro).

## Descrizione del rischio
Da 3 a 5 frasi, comprensibili senza leggere le fonti:
1. il meccanismo di perdita: la causa (cosa lo innesca), l'evento (cosa accade alla Banca), il danno (perdita, sanzione, clienti, continuita');
2. dove tocca la Banca: processi, sistemi, fornitori o clientela esposti;
3. perche' e' emergente oggi: il driver e cio' che sta cambiando.
Niente punteggi, niente frasi generiche ("contesto in evoluzione"), niente elenco di fonti. Il nome dice il meccanismo, non solo il tema: "Frode con voce clonata sui bonifici corporate", non "Intelligenza artificiale".

## Razionale
Le parti in quest'ordine, ognuna con la sua etichetta seguita dai due punti:
- RISCHIO: il fenomeno in termini di rischio per la Banca, in 2-3 frasi: causa, evento, danno e quanto la Banca e' esposta. Non ripete la descrizione e non motiva i numeri.
- IMPATTO:, PROBABILITA:, PROSSIMITA:, VELOCITY: per ciascuna, il valore e
  1. il descrittore della rubrica a cui corrisponde;
  2. il fatto che lo sostiene, con il documento e la data (lo stesso riferimento delle fonti);
  3. perche' non il valore vicino, in una frase: cosa manca per salire o cosa esclude il valore piu' basso;
  4. se il valore cambia, da quanto a quanto e per quale evidenza nuova; se resta, quali fonti lo sostengono ancora.
  Velocity null: "VELOCITY: nessuna fonte documenta i tempi." Prossimita 4-5 con la deroga: dichiarala qui.
- ADEGUAMENTO: solo se anni_adeguamento non e' null: che cosa va adeguato e perche' servono quegli anni.
Un numero (importo, percentuale, conteggio) cita la sua fonte o e' dichiarato come stima. Attribuisci a un documento solo cio' che il documento dice.

## Azioni di mitigazione
- descrizione: verbo, oggetto e risultato verificabile ("Introdurre la richiamata su numero registrato per i bonifici corporate sopra 50.000 euro"), non un'intenzione ("rafforzare i controlli").
- razionale: quale anello del meccanismo interrompe (causa, evento o danno) e su quale dimensione agisce; poi "EFFETTO:" che cosa cambia in modo osservabile (un KRI che scende, una dimensione che puo' ridursi al ciclo successivo).
- Un'azione aperta (azioni_aperte della baseline) non si ripropone uguale: se e' ancora valida, richiamala nel razionale e proponi il passo successivo o un'azione complementare.

## KRI
- razionale: che cosa misura e perche' anticipa il rischio (Esposizione: quanto la Banca e' esposta; Evoluzione: quanto cresce il fenomeno); poi "EFFETTO:" l'andamento atteso e che cosa segnalerebbe una crescita.

## Fenomeni considerati e non censiti
Chi legge il registro chiede anche perche' un tema presente nei documenti non e' diventato un rischio. Nel JSON, accanto a "rischi", aggiungi "fenomeni_non_censiti": i fenomeni che hai esaminato nelle fonti del ciclo e non hai censito, al massimo 15, i piu' visibili nei documenti. Per ciascuno:
{"fenomeno": "nome breve", "event_type": "codice della categoria o null", "fonti": [{"riferimento": "", "data": "AAAA-MM-GG"}], "motivo": "nessun_meccanismo|fonte_non_specifica|gia_coperto|troppo_lontano|fuori_perimetro|altro", "spiegazione": "una o due frasi, fino a 300 caratteri"}
- nessun_meccanismo: non c'e' un meccanismo di perdita per la Banca (il tema esiste, ma non tocca processi, sistemi, fornitori o clientela della Banca);
- fonte_non_specifica: nessuna fonte specifica e datata nella finestra del ciclo lo sostiene;
- gia_coperto: il meccanismo e' gia' quello di un rischio del registro: scrivi quale (NFR-nn) nella spiegazione;
- troppo_lontano: meccanismo plausibile ma oltre l'orizzonte della Prossimita 1, quando la lista di osservazione e' piena; altrimenti il fenomeno va nella lista di osservazione (sezione seguente), non qui;
- fuori_perimetro: il meccanismo esiste ma ricade in un tipo di rischio fuori dal perimetro della tassonomia (per esempio frode o financial crime);
- altro: spiega nella spiegazione.
Se non hai scartato niente, scrivi "fenomeni_non_censiti": [].

## Lista di osservazione
La lista di osservazione tiene i fenomeni che hanno un meccanismo di perdita per la Banca ma oggi sono troppo lontani o troppo poco plausibili per essere rischi del registro: oltre l'orizzonte della Prossimita 1 (piu' di 3 anni) o solo teorici. Non hanno KRI, azioni ne' score e non entrano in radar e classifica. Le voci in osservazione sono nella baseline, chiave "osservazione". Nel JSON, accanto a "rischi", scrivi "osservazione" con SOLO:
- le voci nuove: esito "nuova", oss_id null (il codice lo assegna lo script);
- le voci della baseline per cui le fonti del ciclo portano evidenza nuova, con il loro oss_id: esito confermata, avvicinata, promossa o archiviata.
Una voce senza evidenza nuova non si scrive: resta com'e'. Nella baseline ogni voce porta anche le notizie che A3 le ha collegato dopo il ciclo precedente (notizie_a3) e i suoi segnali settimanali (segnali_a3: Avvicina, Segnale verificato, Allontana): verificali nelle fonti; sono proposte, non decisioni, ma una voce con un "Segnale verificato" va riesaminata (promossa se il segnale si e' davvero verificato). Al massimo 30 voci in osservazione in tutto: per aggiungerne oltre, archivia le meno rilevanti. Se non hai niente da proporre, scrivi "osservazione": [].
{"oss_id": "OSS-nn o null", "esito": "nuova|confermata|avvicinata|promossa|archiviata", "nome": "", "descrizione": "", "driver": ["DRV-..."], "event_type": "9.n", "rischi_toccati": ["NFR-nn"], "impatto_potenziale": 1, "orizzonte_anni": 5, "plausibilita": "teorica|possibile|in crescita", "segnale_avvicinamento": "", "motivazione": "", "fonti": [{"riferimento": "", "data": "AAAA-MM-GG"}], "promosso_a": null}
- ingresso: serve un meccanismo di perdita per la Banca (causa, evento, danno), anche lontano, e almeno una fonte. Un tema senza meccanismo va fra i fenomeni non censiti (nessun_meccanismo); un fenomeno in osservazione non va anche fra i non censiti;
- nome e descrizione: come per un rischio, il meccanismo e non solo il tema; descrizione in 2-3 frasi;
- driver, event_type: la collocazione nella tassonomia (perche' emerge, dove si manifesterebbe la perdita); rischi_toccati: i rischi del registro che toccherebbe se si avvicina, anche nessuno;
- impatto_potenziale: il descrittore della rubrica, se il fenomeno si manifestasse; orizzonte_anni: anni stimati prima che possa manifestarsi (5, 10...);
- plausibilita: teorica (possibile in principio, nessun caso noto), possibile (casi o prototipi fuori dal settore finanziario), in crescita (segnali che aumentano nel settore finanziario);
- segnale_avvicinamento: il fatto osservabile e verificabile che lo farebbe diventare un rischio ("primo caso documentato presso una banca europea"), non una tendenza generica;
- motivazione: perche' questa valutazione; per una voce esistente, l'evidenza nuova del ciclo e che cosa cambia;
- esiti: confermata = evidenza nuova, il fenomeno resta lontano; avvicinata = il segnale si sta verificando in parte o l'orizzonte si accorcia; promossa = il segnale si e' verificato: censisci il rischio nuovo in "rischi", valutato con la rubrica, e scrivi il suo id_rischio in promosso_a; archiviata = il fenomeno non e' piu' plausibile o e' assorbito da un rischio del registro (scrivi quale nella motivazione).
Lo script ferma il ciclo, e il JSON torna a te, se: un oss_id non e' nella baseline; una voce nuova ha un oss_id o una voce esistente non ce l'ha; un oss_id e' ripetuto; una voce promossa non indica in promosso_a un rischio nuovo del ciclo, o promosso_a e' scritto senza esito promossa; le voci in osservazione superano 30.

## Ciclo straordinario
Se la baseline ha la chiave "straordinario" (ciclo_da_valutare AAAAQn-Sk), il ciclo e' straordinario, deciso dalla funzione di rischio per un evento critico: valuta SOLO i rischi in "rischi_da_rivalutare" (tutti), per il motivo indicato, e censisci un rischio nuovo solo se l'evento lo crea; non riscrivere gli altri rischi della baseline (lo script li riporta com'erano). Le regole sono quelle del trimestre: evidenza datata dopo data_riferimento_precedente, al massimo un punto per dimensione rispetto ai valori della baseline, due KRI e azioni per ogni rischio scritto; ricalcolo_kri_ciclo_precedente solo per i valori che trovi. La lista di osservazione resta facoltativa (una voce il cui segnale si e' verificato si promuove). La sintesi spiega l'evento e che cosa cambia.
Lo script ferma il ciclo se manca un rischio da rivalutare o se scrivi un rischio esistente non indicato.

## Esempio di forma
Fatti, importi e documenti dell'esempio sono inventati: non usarli e non citarli. Mostra solo come si scrive.
"descrizione": "Truffatori clonano con l'intelligenza artificiale la voce dell'amministratore di un'impresa cliente e chiedono per telefono al gestore di eseguire un bonifico urgente. La Banca e' esposta sui pagamenti corporate confermati per telefono, dove la verifica si basa sul riconoscimento della voce. Il danno e' la perdita del bonifico, il contenzioso con il cliente e il danno reputazionale. E' emergente perche' gli strumenti di clonazione sono gratuiti e bastano pochi secondi di registrazione."
"razionale": "RISCHIO: la conferma telefonica dei bonifici corporate si fonda sulla voce, che oggi si puo' clonare; un solo bonifico eseguito su richiesta falsa vale centinaia di migliaia di euro e il rimborso al cliente e' probabile. La Banca e' esposta: circa un terzo delle conferme corporate passa dal telefono (stima da Documento A). IMPATTO: 4, grave: una serie di casi porterebbe a una segnalazione all'autorita' e a un danno reputazionale nazionale (Documento B, 2026-07-15: due banche europee, perdite fra 0,4 e 1,2 milioni di euro). Non 5: non tocca la continuita' ne' la solvibilita' della Banca. PROBABILITA: 5, quasi certa: gia' osservato presso banche europee (Documento B) e la Banca ha il bersaglio, le conferme telefoniche (Documento A). Non 4: il fenomeno non e' solo in crescita, e' gia' presso istituzioni finanziarie. PROSSIMITA: 4, entro 12 mesi: sale da 3 a 4 per i casi del Documento B, in banche comparabili. Non 5: nessun tentativo presso la Banca o i suoi fornitori (Documento C, 2026-08-02, rapporto frodi del trimestre). VELOCITY: 5, entro 1 mese: il danno si produce il giorno del bonifico (Documento B)."
"azioni_mitigazione": [{"descrizione": "Introdurre la richiamata su numero registrato per i bonifici corporate sopra 50.000 euro richiesti o confermati per telefono", "owner": "Direzione Operations", "orizzonte": "3 mesi", "razionale": "Interrompe l'evento: una voce clonata non supera la richiamata su un numero gia' censito. Agisce sulla Probabilita. EFFETTO: i tentativi restano tentativi; il KRI di Esposizione scende con la quota di conferme richiamate."}]
"kri_proposti" (uno dei due): {"kri_id": null, "tipo": "Esposizione", "nome": "Quota di bonifici corporate sopra 50.000 euro confermati solo per telefono", "unita": "%", "fonte_dati": "Report mensile dei canali di disposizione (Operations)", "soglia_attenzione": null, "soglia_allerta": null, "razionale": "Misura quanta parte dei pagamenti di importo alto dipende dalla sola voce, cioe' l'esposizione al meccanismo. EFFETTO: atteso in calo con la richiamata; se cresce, la Banca e' piu' esposta."}
