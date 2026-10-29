# Guida di scrittura di A1

> Come si scrivono descrizione, razionale, azioni e KRI (D-69, 02/10/2026), i fenomeni
> non censiti (D-72) e i rischi in osservazione del registro unico (D-79, 08/10/2026, al
> posto della lista di osservazione della D-73).
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

> D-86 (29/10/2026): la tabella qui sotto e' la stessa di 07_Senza_Studio/controlli_a5.py (LUNGHEZZE): il controllo C10
> usa i minimi; il collaudo (verifica_riferimenti.py) verifica che coincidano. I massimi dello schema restano il limite.

## Lunghezze dei testi
Scrivi testi completi, non sintetici: ogni testo deve stare almeno al minimo e conviene avvicinarsi al consigliato. Un testo piu' corto del minimo e' un rilievo C10: lo script ti chiede di allungarlo. Le lunghezze sono in caratteri, spazi compresi.

| Testo | Minimo | Consigliato fino a |
|---|---|---|
| descrizione del rischio | 500 | 900 |
| razionale, parte RISCHIO: | 300 | 450 |
| razionale, ogni parte IMPATTO:, PROBABILITA:, PROSSIMITA:, VELOCITY: (VELOCITY null esclusa) | 300 | 400 |
| razionale, parte ADEGUAMENTO: (se anni_adeguamento non e' null) | 150 | 300 |
| evidenza di una variazione | 250 | 500 |
| segnale di avvicinamento (se lo scrivi) | 150 | 300 |
| azione: descrizione | 200 | 400 |
| azione: razionale (con EFFETTO:) | 300 | 600 |
| KRI: razionale (con EFFETTO:) | 300 | 600 |
| ciclo straordinario, analisi_evento: evento | 300 | 700 |
| ciclo straordinario, analisi_evento: catena_causale | 600 | 1300 |
| ciclo straordinario, analisi_evento: effetto su ogni rischio toccato | 150 | 350 |
| ciclo straordinario, analisi_evento: uso di ogni documento | 100 | 250 |
| ciclo straordinario, analisi_evento: limiti | 150 | 500 |

Si allunga con contenuto, non con ripetizioni: piu' dettagli sul meccanismo, sui processi e sui fornitori della Banca toccati, sui fatti delle fonti e sul perche' del valore. Niente frasi generiche.

## Categoria di rischio
event_type e' il codice della categoria della tassonomia interna (sezione "Categorie di rischio" delle istruzioni) in cui ricade la perdita per la Banca. Un rischio della baseline con un codice di Basilea (L1-01 ... L1-07) va riclassificato: scrivi la categoria in cui ricade il suo meccanismo di perdita, senza cambiare id ne' valori (non e' un cambio di meccanismo). Se il meccanismo non ricade in nessuna categoria in perimetro (per esempio una frode o un tema di financial crime), scrivi "FP" (fuori perimetro) e nel razionale perche': la funzione di rischio lo togliera' dal registro. Un rischio nuovo non e' mai FP: un tema fuori perimetro va fra i fenomeni non censiti (motivo fuori_perimetro).

## Descrizione del rischio
Da 5 a 8 frasi (500-900 caratteri), comprensibili senza leggere le fonti:
1. il meccanismo di perdita: la causa (cosa lo innesca), l'evento (cosa accade alla Banca), il danno (perdita, sanzione, clienti, continuita');
2. dove tocca la Banca: processi, sistemi, fornitori o clientela esposti;
3. perche' e' emergente oggi: il driver e cio' che sta cambiando.
Niente punteggi, niente frasi generiche ("contesto in evoluzione"), niente elenco di fonti. Il nome dice il meccanismo, non solo il tema: "Frode con voce clonata sui bonifici corporate", non "Intelligenza artificiale".

## Razionale
Le parti in quest'ordine, ognuna con la sua etichetta seguita dai due punti:
- RISCHIO: il fenomeno in termini di rischio per la Banca, in 3-5 frasi: causa, evento, danno e quanto la Banca e' esposta. Non ripete la descrizione e non motiva i numeri.
- IMPATTO:, PROBABILITA:, PROSSIMITA:, VELOCITY: per ciascuna, il valore e
  1. il descrittore della rubrica a cui corrisponde;
  2. il fatto che lo sostiene, con il documento e la data (lo stesso riferimento delle fonti);
  3. perche' non il valore vicino, in una frase: cosa manca per salire o cosa esclude il valore piu' basso;
  4. se il valore cambia, da quanto a quanto e per quale evidenza nuova; se resta, quali fonti lo sostengono ancora.
  Velocity null: "VELOCITY: nessuna fonte documenta i tempi." Prossimita 4-5 con la deroga: dichiarala qui.
  Esposizione della Banca: Probabilita 4-5 solo se la Banca e' esposta (ha il prodotto, il processo o il fornitore colpito). Se le fonti non lo dicono, non scegliere in silenzio il valore piu' basso: scrivi il valore che le fonti sostengono senza l'esposizione e, nella parte PROBABILITA, la frase "ESPOSIZIONE NON NOTA: con l'esposizione documentata sarebbe N." con N maggiore del valore scritto. Decide il validatore, che l'esposizione la conosce. Se le fonti documentano o escludono l'esposizione, niente frase.
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
- troppo_lontano: meccanismo plausibile ma lontano o poco plausibile, quando i rischi in osservazione sono gia' 20; altrimenti il fenomeno e' un rischio in osservazione (sezione seguente), non va qui;
- fuori_perimetro: il meccanismo esiste ma ricade in un tipo di rischio fuori dal perimetro della tassonomia (per esempio frode o financial crime);
- altro: spiega nella spiegazione.
Se non hai scartato niente, scrivi "fenomeni_non_censiti": [].

## Radar e osservazione
Il registro e' unico: ogni rischio e' nel radar di Mosca (gestione completa: KRI, azioni, urgenza) oppure in osservazione (stessa scala e stesso score, niente KRI ne' azioni). Lo stato lo calcola lo script, non tu, con la regola della baseline (chiave "regola_radar"):
1. nel radar un rischio con prossimita >= soglia_prossimita e probabilita >= soglia_probabilita, fino ai posti della capienza, i piu' alti per score;
2. sempre nel radar, anche sotto le soglie: un rischio AGIRE ORA, un tema del supervisore, una decisione del validatore;
3. un rischio del radar che scende sotto le soglie resta un ciclo "in uscita", poi passa in osservazione.
Nella baseline i rischi del radar sono in "rischi", quelli in osservazione in "rischi_in_osservazione".
- Rischi del radar: valutali TUTTI, ogni ciclo, con due KRI e da 1 a 5 azioni.
- Rischi in osservazione: riscrivili SOLO se le fonti del ciclo portano evidenza nuova, con lo stesso id e le stesse regole di variazione (un punto per ciclo); gli altri restano com'erano. Per ognuno che scrivi: le quattro dimensioni, fonti, descrizione, razionale con RISCHIO: e una parte per dimensione, orizzonte_anni (anni stimati prima che possa manifestarsi: 5, 10...) e segnale_avvicinamento (il fatto osservabile e verificabile che lo farebbe salire, "primo caso documentato presso una banca europea", non una tendenza); kri_proposti e azioni_mitigazione vuoti. Se i nuovi valori lo portano sopra le soglie, entra nel radar: allora scrivi anche i due KRI e le azioni.
- Un rischio nuovo va nel radar o in osservazione secondo la regola: serve sempre un meccanismo di perdita per la Banca e almeno una fonte specifica; in osservazione bastano dimensioni, fonti, orizzonte e segnale (e gli anni di adeguamento, punto seguente). Un tema senza meccanismo va fra i fenomeni non censiti.
- Rischi in osservazione con Impatto 4 o 5: stima anche anni_adeguamento quando difendersi richiede un adeguamento strutturale di anni (migrazione crittografica, sostituzione di sistemi, uscita da un fornitore), con la parte ADEGUAMENTO: nel razionale; null se non serve. Vale anche per un rischio in osservazione della baseline senza anni_adeguamento: riscrivilo per aggiungerli anche senza evidenza nuova, con le stesse dimensioni e le stesse fonti (gli anni non sono una variazione). Se mosca_x + anni_adeguamento supera la Z della sua Prossimita (anni_prossimita della regola: Prossimita 1 = 3,5 anni), il rischio e' AGIRE ORA ed entra nel radar: scrivi anche i due KRI e le azioni.
- Ogni rischio in osservazione porta nella baseline le notizie che A3 vi ha collegato dopo il ciclo precedente (notizie_a3) e i suoi flag (flag_a3): verificali nelle fonti, sono proposte.
- Al massimo 20 rischi in osservazione: oltre, il fenomeno meno rilevante va fra i non censiti (troppo_lontano). Un rischio in osservazione non piu' plausibile non si cancella riscrivendolo: dillo nel razionale, lo toglie la funzione di rischio.
Lo script ferma il ciclo se manca un rischio del radar o se i rischi in osservazione superano 20; segnala al validatore, da motivare, un rischio che entra nel radar senza i due KRI o senza azioni.

## Ciclo straordinario
Se la baseline ha la chiave "straordinario" (ciclo_da_valutare AAAAQn-Sk), il ciclo e' straordinario, deciso dalla funzione di rischio per un evento critico: valuta SOLO i rischi in "rischi_da_rivalutare" (tutti), per il motivo indicato, e censisci un rischio nuovo solo se l'evento lo crea; non riscrivere gli altri rischi della baseline (lo script li riporta com'erano). Le regole sono quelle del trimestre: evidenza datata dopo data_riferimento_precedente, al massimo un punto per dimensione rispetto ai valori della baseline, due KRI e azioni per ogni rischio scritto; in ricalcolo_kri_ciclo_precedente rileggi ogni KRI in vigore dei rischi che riscrivi (un KRI non riletto resta Non rilevato e il validatore deve scriverne il valore o motivare: il livello di allerta perderebbe l'aggravante proprio quando il rischio sale), mai ricopiando il valore della baseline. rischi_da_rivalutare puo' indicare anche un rischio in osservazione: se l'evento lo porta sopra le soglie entra nel radar, con i due KRI e le azioni. La sintesi spiega l'evento e che cosa cambia.
Se rischi_da_rivalutare e' vuoto lo straordinario e' di solo censimento: scrivi solo i rischi nuovi che l'evento crea (almeno uno).
Lo script ferma il ciclo se manca un rischio da rivalutare, se scrivi un rischio esistente non indicato o se un censimento non ha rischi nuovi.
Nello straordinario scrivi anche "analisi_evento" (agente A8), l'analisi approfondita sui documenti dell'evento:
- evento: il fatto, quando, dove, chi (ruoli, mai persone), con data e documento;
- catena_causale: causa, evento, danno possibile per la Banca, per ogni meccanismo di perdita; distingui fatti e tua lettura;
- rischi_toccati: ogni rischio che scrivi (rivalutato o nuovo) e ogni rischio esistente che l'evento tocca senza che tu possa riscriverlo, con l'effetto (quale dimensione e descrittore cambia o potrebbe cambiare);
- rischi_non_toccati: i rischi vicini del registro che l'evento non cambia, e perche';
- documenti: ogni documento letto, con data e a che cosa serve nell'analisi (non dopo data_riferimento);
- limiti: che cosa non si sa ancora e quale dato servirebbe.
{"evento":"","catena_causale":"","rischi_toccati":[{"id_rischio":"NFR-01","effetto":""}],"rischi_non_toccati":"","documenti":[{"riferimento":"","data":"","uso":""}],"limiti":""}
L'analisi non porta valori: i valori sono nei rischi e passano dalla validazione. Lo script segnala al validatore (senza fermare) un rischio scritto che non e' fra i toccati e un rischio toccato non indicato per lo straordinario.

## Esempio di forma
Fatti, importi e documenti dell'esempio sono inventati: non usarli e non citarli. Mostra solo come si scrive.
"descrizione": "Truffatori clonano con l'intelligenza artificiale la voce dell'amministratore di un'impresa cliente e chiedono per telefono al gestore di eseguire un bonifico urgente. La Banca e' esposta sui pagamenti corporate confermati per telefono, dove la verifica si basa sul riconoscimento della voce. Il danno e' la perdita del bonifico, il contenzioso con il cliente e il danno reputazionale. E' emergente perche' gli strumenti di clonazione sono gratuiti e bastano pochi secondi di registrazione."
"razionale": "RISCHIO: la conferma telefonica dei bonifici corporate si fonda sulla voce, che oggi si puo' clonare; un solo bonifico eseguito su richiesta falsa vale centinaia di migliaia di euro e il rimborso al cliente e' probabile. La Banca e' esposta: circa un terzo delle conferme corporate passa dal telefono (stima da Documento A). IMPATTO: 4, grave: una serie di casi porterebbe a una segnalazione all'autorita' e a un danno reputazionale nazionale (Documento B, 2026-07-15: due banche europee, perdite fra 0,4 e 1,2 milioni di euro). Non 5: non tocca la continuita' ne' la solvibilita' della Banca. PROBABILITA: 5, quasi certa: gia' osservato presso banche europee (Documento B) e la Banca ha il bersaglio, le conferme telefoniche (Documento A). Non 4: il fenomeno non e' solo in crescita, e' gia' presso istituzioni finanziarie. PROSSIMITA: 4, entro 12 mesi: sale da 3 a 4 per i casi del Documento B, in banche comparabili. Non 5: nessun tentativo presso la Banca o i suoi fornitori (Documento C, 2026-08-02, rapporto frodi del trimestre). VELOCITY: 5, entro 1 mese: il danno si produce il giorno del bonifico (Documento B)."
"azioni_mitigazione": [{"descrizione": "Introdurre la richiamata su numero registrato per i bonifici corporate sopra 50.000 euro richiesti o confermati per telefono", "owner": "Direzione Operations", "orizzonte": "3 mesi", "razionale": "Interrompe l'evento: una voce clonata non supera la richiamata su un numero gia' censito. Agisce sulla Probabilita. EFFETTO: i tentativi restano tentativi; il KRI di Esposizione scende con la quota di conferme richiamate."}]
"kri_proposti" (uno dei due): {"kri_id": null, "tipo": "Esposizione", "nome": "Quota di bonifici corporate sopra 50.000 euro confermati solo per telefono", "unita": "%", "fonte_dati": "Report mensile dei canali di disposizione (Operations)", "soglia_attenzione": null, "soglia_allerta": null, "razionale": "Misura quanta parte dei pagamenti di importo alto dipende dalla sola voce, cioe' l'esposizione al meccanismo. EFFETTO: atteso in calo con la richiamata; se cresce, la Banca e' piu' esposta."}
