# Costruire il template a mano, senza Python

Per chi non puo' eseguire `genera_dashboard.py`. Il risultato deve essere
equivalente al file generato: stessi fogli, stesse tabelle con le stesse
colonne, stessi nomi definiti, stesse formule. Le formule riportate qui sono
controllate dal collaudo (`99_Collaudo/verifica_riferimenti.py`): ognuna
esiste identica nel template generato.

Se il Python e' disponibile, rigenerare e' sempre preferibile:
`python 03_Excel/genera_dashboard.py`. Questo manuale descrive la struttura
del 25/09/2026 sera (DECISIONI D-39): un solo file con report e registro,
senza viste doppie; le schede dei rischi sono un file a parte (D-40). Con la
versione 2026-09-30 (semplificazione dello scoring, D-49...D-56): niente
Gap_Controlli e niente "Riduce" delle azioni, Velocity facoltativa, pesi in
B4:B7, presidio dei controlli nell'anagrafica, colonna Rilievi, 20 rischi. Con
la 2026-09-30b (D-57...D-62): Severity diventa Impatto, niente Confidence
(rilevanza sulle fonti), colonna Anni_Adeguamento nel RiskRegister, Z = meta'
della fascia, soglie 2 e 0,30, Registro e Parametri stampabili in orizzontale.
Con la 2026-10-01 (D-66): foglio dati Sintesi_Settimane (tabella `tblSettimane`, nomi
`SE_...`: Settimana, Notizie, Sintesi_A3, Flag_Proposti, Data_Scrittura) e, nel
foglio Notizie, il riquadro L4:S13 con la sintesi e i flag della settimana
corrente: `=IFERROR(INDEX(SE_Sintesi_A3,MATCH(settimanaCorrente,SE_Settimana,0))&"","Nessuna sintesi di A3 per la settimana corrente.")`
in L5 e la stessa formula su `SE_Flag_Proposti` (testo di riserva "—") in L11.
Con la 2026-09-30c (D-63...D-65, 01/10): livello di allerta nel Radar_Mosca
(colonne U-AB) e colore dei cerchi del radar, ◆ al posto del bordo giallo,
fondo dell'ID del Registro, riquadro del Quadro; colonna Tipo dei KRI; soglie
del livello in Parametri B60:B63.
Con la 2026-10-02 (D-67, 02/10): il foglio Validazione diventa la griglia di
lavoro del validatore, una riga per rischio, KRI, azione e notizia (sezione
8-bis); la tabella `tblValidazione`, invariata, passa nel foglio dati nuovo
Storico_Validazioni; "Righe da validare" (Registro D4) conta gli oggetti, non i
campi.
Con la 2026-10-06 (D-71, 06/10): nella sezione Rischi del foglio Validazione la
colonna P "Segnalazioni dei controlli" (e, nella riga del titolo, le
segnalazioni sul ciclo); la colonna Rilievi del Registro mostra "⚑ da motivare";
nel Quadro la riga "Segnalazioni da motivare" al posto di "Rilievi di A5
superati".
Con la 2026-10-07 (D-72, 07/10): nel Quadro, riga 16 (prima pagina), le **Note
dell'analista**: A16:B16 etichetta, C16:O16 unite, fondo giallo FFF2CC, testo a
capo, altezza 34, nome `quadroNote` (C16), unica cella del report scritta a
mano; in `tblSintesi` la colonna `Note_Analista` (le note archiviate dei cicli
passati).
Con la 2026-10-07b (D-73, 07/10): la **lista di osservazione**. Tabella nuova
`tblOsservazione` nel foglio dati Lista_Osservazione (nomi `OS_...`, colonna
formula Ordine), foglio di lavoro Osservazione, pagina del report Fenomeni
prima della Metodologia, sezione Lista di osservazione nella griglia di
validazione (fra Azioni e Notizie), nomi `nomiL1`, `codiciDriver`,
`nomiDriver`; "Righe da validare" conta anche le voci in osservazione.
Con la 2026-10-07c (D-73, punto 6): A3 collega le notizie alle voci. Colonna
`Voce_Osservazione` in `tblNews` (prima di Validazione) e `Segnali_Osservazione`
in `tblSettimane` (prima di Flag_Proposti); nel foglio Notizie, L15 etichetta e
L16:S19 unite, `=IFERROR(INDEX(SE_Segnali_Osservazione,MATCH(settimanaCorrente,SE_Settimana,0))&"","—")`;
nella griglia, sezione Notizie, colonne K/L "Voce oss." (proposta e valore);
foglio Osservazione colonna O e pagina Fenomeni colonna K: le notizie di A3
collegate alla voce nelle ultime 4 settimane (Fenomeni stampa A1:K47).

Con la 2026-10-08 (D-75, 07/10): il **ciclo straordinario** `AAAAQn-Sk`. In
Parametri i periodi delle viste diventano valori scritti dallo script (sezione
4) e c'e' `dataRiferimento` (B18), usata dall'etichetta del ciclo; colonna
`Periodo_Valutazione` in fondo a `tblRegister` e colonna nascosta AC del
Radar_Mosca (periodo di valutazione del rischio, da cui la Y prende le azioni);
colonna `Straordinario` in fondo a `tblSintesi`; colonna `Proposta_Straordinario`
in `tblSettimane` (prima di Flag_Proposti) e, nel foglio Notizie, L21 etichetta e
L22:S24 unite con `=IFERROR(INDEX(SE_Proposta_Straordinario,MATCH(settimanaCorrente,SE_Settimana,0))&"","—")`,
in rosso se comincia con "PROPOSTA".

Con la 2026-10-08b (D-74, 07/10): la **tassonomia interna della Banca** al posto
degli event type di Basilea: nove categorie (9.1 Condotta ... 9.13 Processo) in
Parametri E4:F12 (driver spostati in E15:F22), nove settori del radar, nove righe
del foglio Notizie (righe sotto spostate di due), colonne `Imp_9_1` ... `Imp_9_13` di
`tblNews` al posto di `Imp_L1_01` ... `Imp_L1_07` (che aggiorna-registro non copia),
colonne "Categoria" al posto di "Event type" nelle viste; nel foglio Osservazione la
matrice ha nove colonne (Q-Y, totale in Z) e l'appoggio delle liste passa in AF.

Con la 2026-10-09 (D-79, 08/10): il **registro unico**. Spariscono `tblOsservazione`
e il foglio dati Lista_Osservazione, la colonna `Voce_Osservazione` di `tblNews`,
`Segnali_Osservazione` di `tblSettimane` e la sezione Lista di osservazione della
griglia. In fondo a `tblRegister` sette colonne: `Stato`, `Motivo_Stato`,
`Movimento`, `Decisione_Stato` (scritte dallo script), `Orizzonte_Anni`,
`Segnale_Avvicinamento` (di A1) e la formula `Ordine_Osservazione`. I fogli
Osservazione e Fenomeni leggono i rischi del RiskRegister con Stato
"Osservazione" (sotto, entrati e usciti dal radar); in Parametri, righe 65-75, la
regola del radar (`capienzaRadar`, `sogliaProssimitaRadar`,
`sogliaProbabilitaRadar`, `cicliUscitaRadar`, gialli; `capienzaOsservazione` = 20
fisso); nella griglia, sezione Rischi, le colonne W (stato calcolato), X/Y
(decisione sullo stato in vigore e gialla); nel Quadro il riquadro "Variati ·
nuovi (radar)" con sotto entrati, usciti e in osservazione; nel foglio Notizie lo
stato "In osservazione" del presidio e, in L15:S19, quante notizie toccano i rischi
in osservazione. I dati di esempio hanno tre rischi in osservazione (NFR-13, 14,
15: le tre voci della vecchia lista, rivalutate con la rubrica).

## 1. Fogli, in quest'ordine

| Gruppo (colore della linguetta) | Fogli |
|---|---|
| Guida (ocra BF8F00) | Guida |
| Report al comitato (blu notte 1F3864) | Quadro, Classifica, Radar_Mosca, Matrice, Delta, Fenomeni, Metodologia |
| Lavoro (blu 2E75B6) | Registro, Storico, Indicatori, Notizie, Piano_azioni, Osservazione, Validazione, Parametri, Dizionario |
| Dati, li scrive solo lo script (grigio A6A6A6) | RiskRegister, Azioni, KRI, NewsLog, Sintesi_Cicli, Sintesi_Settimane, Storico_Validazioni |

I fogli del report stanno di seguito: si selezionano insieme e si salvano in
PDF. Griglia nascosta in tutti i fogli tranne quelli dei dati. Il foglio attivo
all'apertura e' il Quadro.

Versione della struttura: nome definito `versioneTemplate` = `="2026-10-08b"`.
Lo script di campo si ferma su un registro con un'altra versione; un template
costruito a mano deve avere tutto quello che dice questo manuale per dichiarare
la versione corrente.

## 1-bis. Testata, guida e colori dei processi

**Riga 1, fascia del titolo**: celle unite da A all'ultima colonna del foglio,
fondo 1F3864, testo bianco 14 pt grassetto, formula
`="Horizon Scan NFR — <titolo del foglio>   ·   "&etichettaCiclo`.
`etichettaCiclo` (Parametri!B57) dice ciclo, data di riferimento, stato di
validazione e riservatezza:

```excel
=IF(cicloCorrente="","nessun ciclo",IF(ISNUMBER(SEARCH("-S",cicloCorrente)),"Ciclo straordinario ","Ciclo ")&cicloCorrente&IF(ISNUMBER(dataRiferimento)," · dati al "&DAY(dataRiferimento)&"/"&RIGHT("0"&MONTH(dataRiferimento),2)&"/"&YEAR(dataRiferimento),"")&" · "&IF(decisioniDaPrendere>0,"da validare","validato"))&" · Uso interno"
```

Niente funzione TESTO: il formato dipende dalla lingua di Excel.

**Riga 2, guida**: una cella unita (testo a capo) la cui prima riga, in
grassetto, dice quale processo aggiorna il foglio; poi cosa contiene, come si
legge e cosa fare. I testi sono nel dizionario `GUIDE` di `genera_dashboard.py`.
Fondo della guida e intestazioni colorate secondo chi agisce:

| Processo | Fondo | Testo |
|---|---|---|
| Ciclo trimestrale (A1, A5) | DDEBF7 azzurro | 1F4E79 |
| Ciclo settimanale (A3) | E2EFDA verde | 375623 |
| Validatore (decisione umana, celle di input) | FFF2CC giallo | 7F6000 |
| Script o formula | EDEDED grigio | 404040 |

Nei formati condizionali il riempimento va dato come colore di **sfondo**:
con il solo colore di primo piano Excel lascia la cella bianca.

## 2. Tabelle dati (livello DATI)

Le colonne di ogni tabella, nell'ordine, sono quelle di
`01_Kernel/mappatura_campi.json` (chiave `tabelle`). Per ciascuna tabella:
riga 1 titolo, riga 2 guida; in **riga 3** la fascia dei gruppi di colonne
(colonne consecutive scritte dallo stesso attore, unite: per esempio "A1 ·
ciclo trimestrale, poi validato", "Script · alla scrittura", "Validazione ·
comando valida"); in **riga 4** il significato di ogni colonna (chiave
`significato` della mappa, preceduto da chi la scrive: A1, A3, A5, Script,
Formula, Validazione, Validatore; corsivo 8 pt, a capo); in **riga 5** le
intestazioni a partire da A5, colorate come sopra secondo chi scrive la
colonna. Selezionarle con una riga vuota sotto, *Inserisci > Tabella*, e
rinominarla (*Progettazione tabella > Nome tabella*). Niente riquadri
bloccati.

| Tabella | Foglio | Colonne formula |
|---|---|---|
| `tblRegister` | RiskRegister | Score_Composito (J), Chiave (T), Ordine_Osservazione (AF, D-79) |
| `tblAzioni` | Azioni | Mesi_Orizzonte (G) |
| `tblKRI` | KRI | Stato (M), Chiave (R) |
| `tblNews` | NewsLog | Settimana (B) |
| `tblValidazione` | Storico_Validazioni | nessuna (colonne dalla sezione `validazione` della mappa) |
| `tblSintesi` | Sintesi_Cicli | nessuna (una riga per ciclo: commento di A1, sintesi del challenger se usato, segnalazioni sul ciclo e quante sono da motivare) |

Formule della prima riga dati, la 6 (Excel le estende alle righe nuove):

```excel
=IF(COUNT(G6,I6,K6)<3,"",ROUND((pesoImpatto*G6+pesoProbabilita*K6+pesoProssimita*I6+IF(ISNUMBER(H6),pesoVelocity*H6,0))/(pesoImpatto+pesoProbabilita+pesoProssimita+IF(ISNUMBER(H6),pesoVelocity,0)),2))
=A6&"|"&C6
=IF(OR(H6="",I6=""),"Soglie da definire",IF(I6<H6,"SOGLIE INVERTITE — correggere",IF(J6="","Non rilevato",IF(J6>=I6,"Rosso",IF(J6>=H6,"Ambra","Verde")))))
=A6&"|"&B6
=A6-WEEKDAY(A6,2)+1
=IFERROR(VALUE(LEFT(F6,FIND(" ",F6)-1)),"")
```

(nell'ordine: RiskRegister!J6, RiskRegister!T6, KRI!M6, KRI!R6, NewsLog!B6,
Azioni!G6). RiskRegister!AF6 (`Ordine_Osservazione`, D-79), chiave d'ordine delle
viste dei rischi in osservazione, solo per le righe del ciclo corrente con Stato
"Osservazione" (score piu' alto prima; la riga rende unica la chiave):

```excel
=IF(AND(A6=cicloCorrente,Z6="Osservazione"),N(J6)*100000+1-ROW()/1000000,"")
```

Convalide a elenco su RiskRegister: Stato (Radar, Radar, in uscita, Osservazione,
Dismesso), Decisione_Stato (Automatico, Radar, Osservazione). Lo score (D-50) e' la media pesata delle dimensioni valutate: vuoto
se manca Impatto, Probabilita o Prossimita; se manca la Velocity (non
valutata) il suo peso esce dal numeratore e dal denominatore. Lo stato del KRI
controlla per prime le soglie vuote: una soglia vuota varrebbe 0 e darebbe un
falso Rosso (D-53). Nel foglio Storico_Validazioni (non e' un foglio di input:
nessun elenco a discesa): formattazione ambra se Stato = "Da decidere",
azzurra se Decisione = Rettificato, rossa se Respinto. `tblKRI` e' STORICA: una
riga per KRI per ciclo (colonna A `Ciclo`), la chiave e' `Ciclo|KRI_ID`.
Formato data (gg/mm/aaaa) sulle colonne di data; formato 0,00 su
Score_Composito.

Note di testo: sempre SOPRA la tabella (righe 1-4), mai sotto: la tabella
cresce verso il basso e inglobera' una nota come riga di dati.

## 3. Nomi definiti

*Formule > Gestione nomi > Nuovo*. In un nome definito ogni intervallo porta
il nome del foglio (`Delta!$AJ$5:$AJ$24`, non `$AJ$5:$AJ$24`): senza, Excel
rifiuta di aprire il file.

**Colonne delle tabelle**: un nome per ogni colonna, su intervallo ASSOLUTO
dalla prima riga dati (6) alla 20000, con prefisso `RR_` (tblRegister), `AZ_`
(tblAzioni), `KRI_` (tblKRI), `NW_` (tblNews), `SI_` (tblSintesi), `SE_`
(tblSettimane), `OS_` (tblOsservazione), `VAL_` (tblValidazione): per esempio `RR_ID_Rischio` = `=RiskRegister!$C$6:$C$20000`.
Non usare riferimenti strutturati di tabella nelle formule di vista.

**Parametri**: `pesoImpatto` B4, `pesoProbabilita` B5, `pesoProssimita` B6,
`pesoVelocity` B7, `sogliaDirezione` B11, `sogliaDelta` B12,
`cicloCorrente` B15, `cicloPrecedente` B16, `cicloMeno2` B17, `dataRiferimento` B18 (D-75), `cicliTrend`
B20:B27, `settimanaCorrente` B30, `inizioFinestra4` B31, `settimane12`
B34:B45, `moscaX` B48, `moscaYDefault` B49, `anniProssimita` B51:B55,
`etichettaCiclo` B57, `livelloPxI` B60, `livelloQuotaKRI` B61,
`livelloMargine` B62, `livelloForti` B63 (D-63), `codiciL1` E4:E12, `nomiL1` F4:F12 (le nove categorie della
tassonomia interna, D-74: il nome resta quello di prima), `codiciDriver` E15:E22, `nomiDriver` F15:F22 (D-73), `anagrafica` H4:O23, e `ANA_ID`,
`ANA_Nome`, `ANA_Event_Type`, `ANA_Driver`, `ANA_Owner`,
`ANA_Anni_Adeguamento`, `ANA_Attenzione_Supervisore`,
`ANA_Presidio_Controlli` sulle singole colonne H..O dell'anagrafica (righe
4-23, 20 rischi: `MAX_RISCHI` del generatore).

**Viste** (lo script e il collaudo leggono questi nomi, mai celle):
`decisioniDaPrendere` Registro!D4, `rettificheApplicate` G4,
`statoValidazione` H4, `coperturaAnagrafica` D5, `coperturaValutati` G5,
`statoCopertura` H5; blocco per posizione `posID`, `posNome`, `posImpatto`,
`posProbabilita`, `posProssimita`, `posVelocity`, `posScore`,
`posScorePrec`, `posScore2`, `posNetti`, `posBadge`, `posLivello`
(Registro!AA9:AK28 e AN9:AN28, una colonna ciascuno); `rmID`, `rmPxI`, `rmZ`, `rmX`,
`rmY`, `rmMargine`, `rmUrgenza`, `rmLivello`, `rmMotivoLivello` (Radar_Mosca
A, F, H, I, J, K, L, AA, AB, righe 5-24);
`presidioCodici` e `presidioStato` (Notizie!A5:A13 e F5:F13); `quadroCommento`
(Quadro!A41:O45), `quadroSegnalati` (Quadro!A50:O69), `deltaMotivi`
(Delta!K6:Q25), `fenomeniLista` (Fenomeni!A7:K26), `fenomeniUscite`
(Fenomeni!A30:K35): righe con testi calcolati, di cui lo script adatta l'altezza
(dal 08/10 anche `fenomeniUscite`: con l'altezza del template, 3 punti, entrati e usciti non si vedevano).
Nomi dinamici dei grafici: sezione 6.

**Costanti** che lo script legge per non superare le righe delle viste:
`capienzaKRICorrenti` = `=60` (KRI del ciclo nel foglio Indicatori),
`capienzaElencoKRI` = `=150` (elenco a discesa degli Indicatori),
`capienzaPianoAzioni` = `=150` (righe del Piano_azioni), `capienzaOsservazione`
= `=20` (rischi in osservazione al massimo, D-79; anche in Parametri B70).

Stati ammessi per `tblAzioni.Stato` (convalida a elenco): Proposta — da
valutare, Approvata, Respinta, In corso, Completata, Annullata (azione di un
rischio dismesso). "In corso" e "Completata" li scrive a mano la funzione di
rischio: e' l'unica colonna dei dati modificabile a mano.

## 4. Parametri

Celle gialle = input: pesi in B4:B7 (Impatto 0,35, Probabilita 0,25,
Prossimita 0,20, Velocity 0,20: decisione D-50; la Velocity pesa solo quando e'
valutata), somma in B8 con il controllo in C8; soglia di direzione (2), soglia
del Delta (0,30) (D-61), ciclo corrente, settimana corrente (un lunedi'). Z per
Prossimita in B51:B55 (`anniProssimita`, dalla Prossimita 1 alla 5): 3,5, 2,5,
1,5, 0,5, 0 = meta' della fascia del descrittore (D-59). Livello di allerta
(D-63) in B60:B63: P x I alta da 12, quota dei KRI in ambra o rosso da 0,5
(formato percentuale), margine stretto sotto 1 anno, 2 segnali forti per
l'Attivazione. Tassonomia interna (D-74: codice e nome delle nove categorie) in
E4:F12, driver in E15:F22, anagrafica in H3:O23 con intestazioni ID, Nome,
Event_Type, Driver, Owner, Anni_Adeguamento, Attenzione_Supervisore,
Presidio_Controlli (H-K azzurre, L-O gialle). L4:O23 sono celle gialle di input
del validatore: Owner, Anni_Adeguamento (convalida "numero decimale da 0 a
30"; lo scrive la validazione dalla stima di A1, D-60, e resta correggibile a
mano), Attenzione_Supervisore (convalida a elenco "Sì,No") e
Presidio_Controlli (convalida a elenco "Non verificato,Adeguato,Parziale,
Assente"; giudizio della Banca sui controlli, fuori dallo score: D-49). Nota
dell'anagrafica in H2:O2 (unite).

```excel
=IF(ROUND(B8,6)=1,"OK","I PESI NON SOMMANO A 1")
=settimanaCorrente-21
=settimanaCorrente-7*11
```

Dalla 2026-10-08 (D-75) B16 (periodo precedente, anche uno straordinario
`AAAAQn-Sk`), B17 (trimestre di due trimestri prima, per il Delta 6 mesi), B18
(`dataRiferimento`, data di riferimento del ciclo corrente) e B20:B27 (gli otto
periodi del trend, dal piu' vecchio; B27 = ciclo corrente) sono **valori** che lo
script scrive quando cambia il ciclo corrente (trimestrale, inizializza,
aggiorna-registro); prima erano formule che contavano solo trimestri. Nel
template: 2026Q1, 2025Q4, 30/06/2026 e i trimestri da 2024Q3 a 2026Q2. Le dodici settimane in
B34:B45 vanno da `settimanaCorrente-7*11` a `settimanaCorrente-7*0`.

## 5. Registro (il ciclo corrente)

**Controlli** in righe 4 e 5, sopra la tabella: stato della validazione e
copertura del ciclo. COUNTIF con "NFR-*", non COUNTA, che conterebbe altre celle.

```excel
=COUNTIFS(VAL_Periodo,cicloCorrente,VAL_Stato,"Da decidere",VAL_Oggetto,"Rischio",VAL_Campo,"Impatto")+COUNTIFS(VAL_Periodo,cicloCorrente,VAL_Stato,"Da decidere",VAL_Oggetto,"KRI",VAL_Campo,"Valore_Corrente")+COUNTIFS(VAL_Periodo,cicloCorrente,VAL_Stato,"Da decidere",VAL_Oggetto,"Azione",VAL_Campo,"Owner")
=COUNTIFS(VAL_Periodo,cicloCorrente,VAL_Decisione,"Rettificato",VAL_Stato,"Applicata")
=IF(D4>0,"CICLO NON ANCORA VALIDATO — vedi foglio Validazione","Ciclo validato")
=COUNTIF(ANA_ID,"NFR-*")
=SUMPRODUCT((ANA_ID<>"")*(COUNTIFS(RR_ID_Rischio,ANA_ID,RR_Ciclo,cicloCorrente)>0))
=IF(D5=G5,"Ciclo completo","CICLO INCOMPLETO — i rischi mancanti non sono valutazioni")
```

(D4, G4, H4, D5, G5, H5; H4 ambra se D4>0, verde altrimenti; H5 rosso se
D5<>G5, verde se uguali). D4 "Righe da validare" conta le righe della griglia
del foglio Validazione (rischi, KRI, azioni del ciclo): lo storico ha una riga
per campo, quindi si conta un campo per oggetto, il primo della mappa (D-67).

**Blocco per posizione** (colonne nascoste AA-AN, righe 9-28, una per
posizione dell'anagrafica): e' il calcolo che tutte le viste riusano. AA ID,
AB nome, AC-AF Impatto, Probabilita, Prossimita, Velocity del ciclo corrente,
AG score corrente, AH del ciclo precedente, AI di due cicli prima, AJ segnali
netti, AK etichetta dei segnali, AL chiave d'ordine (score meno uno spareggio
minimo per posizione), AM posizione del k-esimo per score (dal 30/09 sera
senza la Confidence, D-58). Nel generatore le colonne si calcolano dai nomi del blocco, mai
scritte a mano. Riga 9:

```excel
=IF(Parametri!$H4="","",Parametri!$H4)
=IF($AA9="","",Parametri!$I4)
=IF($AA9="",NA(),IF(COUNTIFS(RR_ID_Rischio,$AA9,RR_Ciclo,cicloCorrente,RR_Impatto,"<>")=0,NA(),SUMIFS(RR_Impatto,RR_ID_Rischio,$AA9,RR_Ciclo,cicloCorrente)))
=IF($AA9="",NA(),IF(COUNTIFS(RR_ID_Rischio,$AA9,RR_Ciclo,cicloPrecedente,RR_Score_Composito,"<>")=0,NA(),SUMIFS(RR_Score_Composito,RR_ID_Rischio,$AA9,RR_Ciclo,cicloPrecedente)))
=IF($AA9="","",COUNTIFS(NW_Rischio_ID,$AA9,NW_Segnale,"Peggiorativo",NW_Settimana,">="&inizioFinestra4,NW_Settimana,"<="&settimanaCorrente)-COUNTIFS(NW_Rischio_ID,$AA9,NW_Segnale,"Migliorativo",NW_Settimana,">="&inizioFinestra4,NW_Settimana,"<="&settimanaCorrente))
=IF($AA9="","",IF(AJ9>=sogliaDirezione,"▲ +"&AJ9,IF(AJ9<=-sogliaDirezione,"▼ "&AJ9,"● "&IF(AJ9>0,"+","")&AJ9)))
=IF($AA9="","",IF(ISNUMBER(AG9),AG9,-1)-1/100000)
=IFERROR(MATCH(AGGREGATE(14,6,$AL$9:$AL$28,1),$AL$9:$AL$28,0),"")
```

(AA9, AB9, AC9, AH9, AJ9, AK9, AL9, AM9). AN9 = livello di allerta della
posizione, `=IF($AA9="","",Radar_Mosca!$AA$5&"")` (AA$6 nella riga 10...):
serve solo al fondo dell'ID della tabella visibile (formattazione
condizionale `INDEX($AN$9:$AN$28,$AM9)="Attivazione"`, fondo F4CCCC; FFF2CC
Attenzione; D9EAD3 Monitoraggio; D-63, nessuna colonna visibile in piu'). AD-AG e AI come AC/AH cambiando
colonna e ciclo; nella chiave d'ordine lo spareggio e' k/100000 e, in AM,
l'ultimo argomento di AGGREGATE va da 1 a 20. AGGREGATE(14, 6, ...) = LARGE che
ignora gli errori: niente formule matriciali. NA() invece di zero: un rischio
non valutato deve essere un buco sul grafico, non un "rischio nullo". Il
COUNTIFS delle dimensioni ha anche la condizione `"<>"` sulla colonna letta
(cella non vuota): una Velocity non valutata e' vuota e SUMIFS la leggerebbe
come 0.

**Tabella visibile** in righe 9-28, ordinata per score (un rischio non
valutato in fondo). Riga 7: fascia dei gruppi (Rischio · Dimensioni 1-5 ·
Calcolati dal foglio · Sup. · KRI del ciclo · Notizie 4 settimane · Banca · A5
e controlli · Anagrafica) sui colori dei processi; riga 8: intestazioni.
Colonne A ID, B nome, C event type, D-G Imp, Prob, Pross, Vel, H Score, I Δ sul
ciclo prima, J Δ 6 mesi, K urgenza, L margine, M ◆, N-P KRI rossi, ambra,
verdi, Q segnali netti, R presidio dei controlli, S rilievi, T owner:

```excel
=IF($AM9="","",INDEX(posID,$AM9))
=IF($AM9="","",INDEX(ANA_Event_Type,$AM9)&"")
=IF($AM9="","",IF(ISNUMBER(INDEX(posImpatto,$AM9)),INDEX(posImpatto,$AM9),NA()))
=IF($AM9="","",IF(ISNUMBER(INDEX(posScorePrec,$AM9)),IFERROR(H9-INDEX(posScorePrec,$AM9),""),IF(ISNUMBER(H9),"nuovo","")))
=IF($AM9="","",INDEX(Radar_Mosca!$L$5:$L$24,$AM9)&"")
=IF($AM9="","",IF(INDEX(ANA_Attenzione_Supervisore,$AM9)="Sì","◆",""))
=IF($A9="","",COUNTIFS(KRI_ID_Rischio,$A9,KRI_Ciclo,cicloCorrente,KRI_In_Vigore,"Sì",KRI_Stato,"Rosso"))
=IF($AM9="","",INDEX(posBadge,$AM9))
```

(A9, C9, D9, I9, K9, M9, N9, Q9; B, E-F, H, J, L, O-P, T allo stesso modo).
G9 (Velocity) scrive "n.v." invece di NA() quando la dimensione non e'
valutata: `=IF($AM9="","",IF(ISNUMBER(INDEX(posVelocity,$AM9)),INDEX(posVelocity,$AM9),"n.v."))`,
in grigio. R9 = `INDEX(ANA_Presidio_Controlli,$AM9)&""` (fondo rosso tenue
Assente, ambra Parziale, verde Adeguato, grigio Non verificato). S9 legge la
colonna Rilievi del RiskRegister del ciclo: "⚑ da motivare" (rosso) se contiene
DA MOTIVARE (o BLOCCANTE SUPERATO, registri fino al 2026-10-02), altrimenti il
numero di segnalazioni, una per riga ("2 oss."). Il
NA() esplicito in D9 serve al controllo degli errori dello script, che
considera voluto solo un #N/D prodotto da una formula con NA(). Formati:
dimensioni colorate da grigio chiaro (1) ad arancio scuro (5); barra dei dati
sullo score (0-5); Δ rosso in aumento, blu in diminuzione
(formato `"▲ "+0.00;"▼ "-0.00;"● "0.00`); urgenza come etichetta (rosso
AGIRE ORA, ambra entro l'anno, grigio margine); KRI colorati se maggiori di 0.
Legenda delle abbreviazioni in riga 30. Stampa (D-62): A4 orizzontale, tutte
le colonne visibili (A-T) in una pagina di larghezza, righe 7-8 ripetute in
ogni pagina; lo stesso per Parametri (A-O).

## 6. Report al comitato

Solo formule sul ciclo corrente. I numeri nei testi passano da `FIXED` (in
italiano FISSO). Grafici con "Mostra dati in righe e colonne nascoste" attivo
(senza, Excel scarta le serie in colonne nascoste). I titoli dei grafici della
Classifica e del Delta sono collegati a una cella che dice il messaggio.

### Classifica

Righe 5-24. Colonne nascoste di appoggio: T chiave d'ordine, U posizione in
anagrafica del k-esimo rischio:

```excel
=IF(ISNUMBER(INDEX(posScore,1)),INDEX(posScore,1)-1/100000,"")
=IFERROR(MATCH(AGGREGATE(14,6,$T$5:$T$24,1),$T$5:$T$24,0),"")
=IF($U5="","",INDEX(posID,$U5))
=IF($U5="","",INDEX(posScore,$U5))
=IF($U5="","",IFERROR(INDEX(posScorePrec,$U5),"—"))
=IF($U5="","",INDEX(Radar_Mosca!$L$5:$L$24,$U5))
=IF($U5="","",B5&" "&IF(ISNUMBER(F5),IF(F5>0,"▲",IF(F5<0,"▼","●")),"○")&"  "&LEFT(C5,34)&IF(LEN(C5)>34,"…",""))
=IF($U5="",NA(),IF(LEFT(H5,9)="AGIRE ORA",D5,0))
```

(T5, U5, B5, D5, E5, H5, K5, V5). Colonne visibili A pos., B ID, C nome, D
score, E score del ciclo prima, F Δ, G esito, H urgenza, I margine, J owner, K
etichetta del grafico. V, W, X = score solo se l'urgenza e' "AGIRE ORA",
"Agire entro", altrimenti (zero, non NA(), negli altri casi: l'etichetta di un
punto #N/D si vedrebbe; le celle hanno formato `0.00;-0.00;;`, che nasconde lo
zero); Y, Z, AA = X, Y, Z di Radar_Mosca. Lente di Mosca ordinata dal piu' in
ritardo (margine crescente) in AD-AJ:

```excel
=IF(ISNUMBER(I5),I5+1/100000,"")
=IFERROR(MATCH(AGGREGATE(15,6,$AD$5:$AD$24,1),$AD$5:$AD$24,0),"")
=IF($AE5="","",INDEX($B$5:$B$24,$AE5)&" ("&IF(INDEX($I$5:$I$24,$AE5)<0,"−","+")&FIXED(ABS(INDEX($I$5:$I$24,$AE5)),2)&")")
=IF($AE5="",NA(),IF(INDEX($Y$5:$Y$24,$AE5)+INDEX($Z$5:$Z$24,$AE5)>INDEX($AA$5:$AA$24,$AE5),NA(),INDEX($Z$5:$Z$24,$AE5)))
=IF(COUNTIF(H5:H24,"AGIRE ORA*")=0,"Nessun rischio da affrontare subito",COUNTIF(H5:H24,"AGIRE ORA*")&" da affrontare subito: "&TEXTJOIN(", ",TRUE,AB5:AB24))
```

(AD5, AE5, AF5 etichetta, AH5 "Y entro Z"; AI5 e' la stessa condizione con i
rami scambiati, "Y oltre Z"; AG5 = X, AJ5 = Z; AL2 titolo del grafico).
Nomi dinamici `classificaEtichette` (K), `classificaID` (B), `classificaAgire`
(V), `classificaEntro` (W), `classificaMargine` (X), `lenteEtichette` (AF),
`lenteX` (AG), `lenteY` (AH), `lenteYOltre` (AI), `lenteZ` (AJ), tutti
`=OFFSET(Classifica!$K$5,0,0,MAX(1,COUNT(Classifica!$D$5:$D$24)),1)` cambiando
la colonna; nella finestra "Seleziona dati" si scrive
`=NFR_Registro.xlsx!classificaAgire` (Excel lo salva come `[0]!classificaAgire`).
Due grafici affiancati sotto la tabella:
- barre orizzontali raggruppate, sovrapposizione 100, serie V rossa, W ambra,
  X grigia, etichetta del valore in fondo alla barra, categorie
  `classificaEtichette`, ordine inverso delle categorie, asse fisso 0-5,
  titolo = AL2;
- lente di Mosca: colonne impilate X (grigio), Y entro Z (arancio), Y oltre Z
  (rosso) piu' una serie a linee Z senza linea, marcatore rombo blu, categorie
  `lenteEtichette`, asse verticale da 0.

### Radar_Mosca

Una riga per posizione dell'anagrafica (5-24). Colonne: A-C ID, nome, event
type; D Impatto, E Probabilita, G Prossimita del ciclo corrente; F = P x I; H
= Z; I = X; J = Y; K = margine; L = urgenza; M-P settore e angolo; Q raggio;
R, S coordinate; T attenzione del supervisore; U-AB livello di allerta (D-63):
U F1 AGIRE ORA, V F2 KRI in rosso, W F3 segnali netti oltre la soglia, X A1
P x I alta, Y A2 presidio assente, Z A3 KRI in ambra o rosso (1 o 0), AA il
livello, AB il motivo.

```excel
=IF(AND(ISNUMBER(D5),ISNUMBER(E5)),D5*E5,NA())
=IF(ISNUMBER(G5),INDEX(anniProssimita,G5),NA())
=IF($A5="",NA(),moscaX)
=IF($A5="","",IFERROR(IF(INDEX(RR_Periodo_Valutazione,MATCH(cicloCorrente&"|"&$A5,RR_Chiave,0))="",cicloCorrente,INDEX(RR_Periodo_Valutazione,MATCH(cicloCorrente&"|"&$A5,RR_Chiave,0))&""),cicloCorrente))
=IF($A5="",NA(),MAX(IF(COUNTIFS(AZ_ID_Rischio,$A5,AZ_Ciclo,$AC5,AZ_Stato,"<>Respinta",AZ_Mesi_Orizzonte,">0")=0,moscaYDefault,MAXIFS(AZ_Mesi_Orizzonte,AZ_ID_Rischio,$A5,AZ_Ciclo,$AC5,AZ_Stato,"<>Respinta")/12),N(Parametri!$M4)))
=IF(AND(ISNUMBER(H5),ISNUMBER(J5)),H5-(I5+J5),NA())
=IF(NOT(ISNUMBER(K5)),"",IF(K5<0,"AGIRE ORA: X+Y > Z",IF(K5<1,"Agire entro l'anno","Margine "&ROUND(K5,1)&IF(ROUND(K5,1)=1," anno"," anni"))))
=IF($A5="",NA(),MATCH(C5,codiciL1,0)-1)
=IF($A5="",NA(),COUNTIF($C$4:C4,C5))
=IF($A5="",NA(),COUNTIF(ANA_Event_Type,C5))
=IF($A5="",NA(),2*PI()*(M5+(N5+0.5)/O5)/ROWS(codiciL1))
=IF(ISNUMBER(K5),MAX(0.6,MIN(6,K5+2)),NA())
=IF(AND(ISNUMBER(Q5),ISNUMBER(P5)),Q5*SIN(P5),NA())
=IF(AND(ISNUMBER(Q5),ISNUMBER(P5)),Q5*COS(P5),NA())
=IF($A5="","",IF(Parametri!$N4="Sì","Sì",""))
=IF(OR($A5="",NOT(ISNUMBER(K5))),"",IF(K5<0,1,0))
=IF(OR($A5="",NOT(ISNUMBER(K5))),"",IF(COUNTIFS(KRI_ID_Rischio,$A5,KRI_Ciclo,cicloCorrente,KRI_In_Vigore,"Sì",KRI_Stato,"Rosso")>0,1,0))
=IF(OR($A5="",NOT(ISNUMBER(K5))),"",IF(N(INDEX(posNetti,1))>=sogliaDirezione,1,0))
=IF(OR($A5="",NOT(ISNUMBER(K5))),"",IF(AND(ISNUMBER(F5),F5>=livelloPxI),1,0))
=IF(OR($A5="",NOT(ISNUMBER(K5))),"",IF(Parametri!$O4="Assente",1,0))
=IF(OR($A5="",NOT(ISNUMBER(K5))),"",IF((U5+V5+W5)>=livelloForti,"Attivazione",IF(OR((U5+V5+W5)>=1,AND(K5<livelloMargine,(X5+Y5+Z5)>=1)),"Attenzione","Monitoraggio")))
```

(U5, V5, W5 — in W la posizione, 1 nella riga 5, 2 nella 6... —, X5, Y5,
AA5). Z5 = 1 se i KRI in vigore del rischio in ambra o rosso sono almeno
`livelloQuotaKRI` per il loro numero (COUNTIFS su KRI_Stato "Rosso" e
"Ambra" contro COUNTIFS dei KRI in vigore, che deve essere > 0). AB5 = il
motivo con TEXTJOIN: "nessun segnale forte" per il Monitoraggio, altrimenti i
segnali forti presenti ("AGIRE ORA", "KRI in rosso", "notizie in
peggioramento") o, se non ce ne sono, "margine sotto l'anno con " e gli
aggravanti. Formattazione di AA: fondo E06666 Attivazione (testo bianco),
F6C342 Attenzione, 93C47D Monitoraggio.

(F5, H5, I5, J5, K5, L5, M5, N5, O5, P5, Q5, R5, S5, T5). J = Y: l'orizzonte
piu' lungo delle azioni non respinte (o `moscaYDefault`) oppure, se maggiori,
gli anni di adeguamento dell'anagrafica (Parametri!M; N() vale 0 se vuota).
Formattazione di L: rosso se `LEFT(L5,9)="AGIRE ORA"`, ambra se
`LEFT(L5,11)="Agire entro"`, grigio se inizia con "Margine". Non
`LEFT(L5,5)="AGIRE"`: il confronto "=" di Excel ignora le maiuscole.
Raggio = margine + 2, fra 0,6 e 6. I rischi dello stesso settore stanno a
distanze angolari uguali.

Grafico a **dispersione** (non a bolle: un grafico a bolle non sa disegnare
linee), assi da -7,6 a 7,6 nascosti, niente griglia, grafico quadrato. Le serie
leggono colonne di appoggio nascoste da AD (colonna base 30, dopo le colonne
del livello):
- quattro cerchi, 73 punti ciascuno, linea smussata senza marcatori: margine 0
  ("Mosca", rosso 2,25 pt), 1 anno (grigio tratteggiato), 2 e 3 anni (grigio
  chiaro); etichetta sul raggio fra il 2o e il 3o settore;
- nove raggi di separazione dei settori, grigio chiaro (uno per categoria, D-74);
- nove etichette dei settori su due righe, il codice e il nome della categoria
  (Condotta, Legale, Fiscale, Tecnologico, Sicurezza informatica, Sicurezza
  fisica, Terze parti, Employer, Processo); un rischio FP (fuori perimetro) o con
  un codice di Basilea non riclassificato non ha settore e non compare;
- una serie per ogni valore possibile di P x I (1, 2, 3, 4, 5, 6, 8, 9, 10,
  12, 15, 16, 20, 25) per ciascun livello di allerta (42 serie, colonne
  AU-CJ), riga 4 = il valore, riga 3 = il livello (D-63). Formula di AU5:

```excel
=IF(AND(ISNUMBER($F5),ISNUMBER($S5)),IF(AND($F5=AU$4,$AA5=AU$3),$S5,NA()),NA())
```

  x = colonna CK, copia di R; marcatore cerchio di lato 10 x radice del valore,
  cosi' l'AREA e' proporzionale a P x I; riempimento del colore del livello
  (E06666 Attivazione, F6C342 Attenzione, 93C47D Monitoraggio) con
  trasparenza (il generatore la aggiunge nell'XML del grafico, un colore alla
  volta; a mano: *Formato serie > Riempimento > Trasparenza 45%*); bordo
  grigio sottile. Fino al 30/09 le serie erano raddoppiate per l'attenzione
  del supervisore, con il bordo giallo (D-35);
- una serie per rischio senza marcatore, solo per l'etichetta (x = CK, y = CM,
  nome = CL): l'ID con ◆ se il tema e' all'attenzione del supervisore:

```excel
=IF($A5="","",$A5&IF($T5="Sì"," ◆",""))
```

- legenda nel grafico: in basso a sinistra tre cerchi dei livelli
  (Attivazione, Attenzione, Monitoraggio) e sotto una linea rossa ("dentro il
  cerchio rosso: AGIRE ORA (X + Y > Z)"); in basso a destra tre cerchi di
  riferimento per P x I = 4, 12, 25.

### Matrice

Gravita': ogni rischio nella cella della sua Probabilita (righe 5-9, da 5 a 1)
e Impatto (colonne C-G, da 1 a 5), fondo per fascia di P x I (verde fino a 6,
ambra 8-12, rosso da 15; bordi bianchi). Appoggio nascosto da L:

```excel
=INDEX(posID,1)&""
=IF(AND(ISNUMBER(INDEX(posProbabilita,1)),ISNUMBER(INDEX(posImpatto,1))),INDEX(posProbabilita,1)*10+INDEX(posImpatto,1),"")
=IF(M5="","",INDEX(posProbabilita,1)*INDEX(posImpatto,1))
=IF(M5="","",L5&IF(INDEX(ANA_Attenzione_Supervisore,1)="Sì"," ◆",""))
=IF(N5="","",N5-1/1000)
=IFERROR(MATCH(AGGREGATE(14,6,$P$5:$P$24,1),$P$5:$P$24,0),"")
=IF($M5=S$4,$O5,"")
=TEXTJOIN("   ",TRUE,S5:S24)
```

(L5 ID, M5 codice della cella P*10+S, N5 P x I, O5 etichetta, P5 chiave, Q5
posizione del k-esimo; da S a AQ una colonna per ciascuna delle 25 celle, con
il codice in riga 4; C5 = la cella P5-S1 della matrice). Sotto, righe 16-35, i
rischi dal piu' grave:

```excel
=IF($Q$5="","",INDEX(posID,$Q$5))
=IF($Q$5="","",INDEX(posProbabilita,$Q$5)&" · "&INDEX(posImpatto,$Q$5))
=IF($Q$5="","",INDEX($N$5:$N$24,$Q$5))
```

(A16, F16, G16; C16 nome con ◆).

### Delta

Appoggio nascosto da AD (righe 5-24): AD ID per posizione, AE-AI delta di
Impatto, Probabilita, Prossimita, Velocity, Score; AJ chiave d'ordine, AK
posizione del k-esimo (dal maggiore aumento); AL-AO le serie del grafico gia'
ordinate. Il delta c'e' solo se il valore e' presente in entrambi i
cicli (COUNTIFS con `"<>"`): una Velocity non valutata in uno dei due cicli da'
#N/D, non un salto dal falso zero.

```excel
=IF($AD5="",NA(),IF(COUNTIFS(RR_ID_Rischio,$AD5,RR_Ciclo,cicloCorrente,RR_Impatto,"<>")*COUNTIFS(RR_ID_Rischio,$AD5,RR_Ciclo,cicloPrecedente,RR_Impatto,"<>")=0,NA(),SUMIFS(RR_Impatto,RR_ID_Rischio,$AD5,RR_Ciclo,cicloCorrente)-SUMIFS(RR_Impatto,RR_ID_Rischio,$AD5,RR_Ciclo,cicloPrecedente)))
=IF($AD5="","",IF(ISNUMBER(AI5),AI5,-9)-1/100000)
=IFERROR(MATCH(AGGREGATE(14,6,$AJ$5:$AJ$24,1),$AJ$5:$AJ$24,0),"")
=IF($AK5="",NA(),IF(ISNUMBER(INDEX($AI$5:$AI$24,$AK5)),IF(INDEX($AI$5:$AI$24,$AK5)>0,INDEX($AI$5:$AI$24,$AK5),0),NA()))
=COUNTIF($AI$5:$AI$24,">0")&" in aumento, "&COUNTIF($AI$5:$AI$24,"<0")&" in diminuzione, "&COUNTIF($AI$5:$AI$24,0)&" invariati"
```

(AE5, AJ5, AK5, AM5 "in aumento" — AN5 "in diminuzione" con `<0`, AO5
"invariato" —, AT2 titolo del grafico). Nomi dinamici `deltaEtichette` (AL),
`deltaSu`, `deltaGiu`, `deltaZero` (AM-AO), come
`=OFFSET(Delta!$AM$5,0,0,MAX(1,COUNT(Delta!$AI$5:$AI$24)),1)`. Grafico a barre
orizzontali raggruppate, sovrapposizione 100, rosso / blu / grigio, "Inverti
se negativo" DISATTIVATO (altrimenti Excel disegna bianca la barra negativa),
asse fisso da -1,5 a +1,5, passo 0,5 (quando la Velocity entra o esce i pesi si
ridistribuiscono e il Δ puo' superare un punto).

A fianco (K-Q, righe 6-25, `deltaMotivi`) il motivo di ogni variazione nello
stesso ordine: ID, Δ, e il JSON delle Variazioni reso leggibile con
SUBSTITUTE annidati ("• Impatto 3 → 4: evidenza (data)"), oppure "Invariato:
nessuna evidenza nuova..." o "Rischio nuovo nel ciclo.". La formula e' lunga:
copiarla dal template generato. Lo script scrive le chiavi del JSON sempre
nello stesso ordine (dimensione, da, a, evidenza, data_evidenza), su cui
contano i SUBSTITUTE (i "da" e "a" li aggiunge lo script, D-51). Sotto (riga
27) come si legge la scala: una formula che calcola quanto vale un punto di
ogni dimensione dai pesi di Parametri, con e senza Velocity (`FIXED`; nessun
peso scritto nel testo; ogni testo fra virgolette al massimo 255 caratteri,
altrimenti Excel non apre il file). Poi (righe 31-50) il dettaglio per
dimensione (C-F Impatto, Probabilita, Prossimita, Velocity; G Score), con la
nota in K (AGGREGATE ignora i #N/D di una Velocity non
valutata):

```excel
=IF($A31="","",IF(NOT(ISNUMBER(G31)),"Nuovo o non valutato in uno dei due cicli",IF(AGGREGATE(4,6,C31:F31)>1,"Aumento > 1 punto: viola la rubrica",IF(AGGREGATE(5,6,C31:F31)<-1,"Riduzione > 1 punto: viola la rubrica",IF(ISNA(F31),"Velocity non valutata in uno dei due cicli: lo score ridistribuisce i pesi","")))))
```

Interruzione di pagina prima della scala: pagina 1 grafico e motivi, pagina 2
dettaglio.

### Quadro (prima pagina del report)

Colonne A-O larghe 10,5 (I 3). Righe 4-6: cinque riquadri (A-C, D-F, G-I, J-L,
M-O) con didascalia, numero grande e riga sotto:

```excel
=coperturaValutati
="su "&coperturaAnagrafica&" in anagrafica · "&IF(coperturaValutati=coperturaAnagrafica,"completo","INCOMPLETO")
=$T$4&" · "&COUNTIF(Radar_Mosca!$AA$5:$AA$24,"Attenzione")
=IF($T$4=0,"nessun rischio in attivazione","in attivazione: "&TEXTJOIN(", ",TRUE,$T$5:$T$24))&" · in monitoraggio "&COUNTIF(Radar_Mosca!$AA$5:$AA$24,"Monitoraggio")
=COUNTIFS(RR_Ciclo,cicloCorrente,RR_Stato,"Radar*",RR_Esito,"Variato")&" · "&COUNTIFS(RR_Ciclo,cicloCorrente,RR_Stato,"Radar*",RR_Esito,"Nuovo")
=COUNTIFS(KRI_Ciclo,cicloCorrente,KRI_In_Vigore,"Sì",KRI_Stato,"Rosso")
=IF(decisioniDaPrendere>0,decisioniDaPrendere,"✓")
```

(A5, A6, D5, D6, G5, J5, M5). Il secondo riquadro e' il **livello di
allerta** (D-63): T4 nascosta = `COUNTIF(Radar_Mosca!$AA$5:$AA$24,"Attivazione")`,
T5:T24 = ID dei rischi in Attivazione; grigio se T4 = 0.
Righe 8-15: a sinistra i primi cinque della Classifica (score con barra, Δ,
urgenza come etichetta), a destra la matrice in piccolo (J-O) con i soli numeri
dei rischi:

```excel
=IF(Classifica!$B$5="","",IF(LEFT(Classifica!$H$5,9)="AGIRE ORA","AGIRE ORA",IF(LEFT(Classifica!$H$5,11)="Agire entro","Entro l'anno",Classifica!$H$5)))
=SUBSTITUTE(SUBSTITUTE(Matrice!C5," ◆",""),"NFR-","")
```

(H10, K10). Righe 17-38: il radar di Mosca in piccolo (8,5 cm; stesso grafico
del Radar_Mosca con appoggio nel foglio stesso, colonne nascoste da BH) e a
destra l'elenco dei rischi del ciclo (J-O, righe alte 12 punti: venti righe
stanno nella prima pagina). Interruzione di pagina alla riga 38.

Pagina 2. Righe 41-45 (`quadroCommento`): messaggio chiave, decisioni
richieste, controlli (sintesi di A5, se usato), avviso dopo le rettifiche,
segnalazioni da motivare. A1 scrive il commento nella forma "MESSAGGIO: ... DECISIONI: ...";
T41 e T42 (nascoste) lo leggono e trovano il marcatore:

```excel
=IFERROR(INDEX(SI_Sintesi_A1,MATCH(cicloCorrente,SI_Ciclo,0))&"","")
=IFERROR(SEARCH("DECISIONI:",T41),0)
=IF(T41="","Nessun commento registrato per il ciclo corrente.",TRIM(SUBSTITUTE(SUBSTITUTE(IF(T42>0,LEFT(T41,T42-1),T41),"MESSAGGIO:",""),"Messaggio:","")))
=IF(T42>0,TRIM(MID(T41,T42+10,4000)),"—")
```

(T41, T42, D41, D42). Senza marcatore tutto il testo va nel messaggio. D44 e'
l'avviso "Il validatore ha applicato n rettifiche o respingimenti..." (valori
rettificati dello storico piu' oggetti respinti, contati sul primo campo: un'azione
respinta conta una volta, D-67); D45 legge
`SI_Rilievi_Superati` del ciclo (quante segnalazioni sono da motivare in
validazione, dai controlli e da A5: D-71). Entrambe con fondo ambra se
non vuote.

Righe 50-69 (`quadroSegnalati`): i rischi segnalati e perche'. In U, per
posizione di classifica, il numero se il rischio e' fra i primi tre, in
Attivazione o in Attenzione (livello di allerta del Radar_Mosca, colonna AA,
D-63), Variato o Nuovo; in V il k-esimo segnalato; in W il perche' (primi tre
per score con il Δ, AGIRE ORA con X + Y, anni di adeguamento e Z, margine sotto
l'anno, variato o nuovo, attenzione del supervisore, presidio assente, KRI
rossi, notizie oltre la soglia):

```excel
=IFERROR(AGGREGATE(15,6,$U$50:$U$69,1),"")
=IF($W50="","",LEFT($W50,LEN($W50)-2)&".")
```

(V50, E50). Colonne visibili: A-C rischio (ID, nome, ◆), D **livello di
allerta** come etichetta (INDEX della colonna AA del Radar_Mosca per la
posizione in anagrafica; colori del radar), E-H perche', I-O cosa e' cambiato (le variazioni leggibili, come nel
Delta). Bordo solo sulle righe con un rischio (formattazione condizionale).
Sotto: i limiti (04_Riferimenti/controlli_e_model_risk.md, sezione 5) e la legenda delle abbreviazioni.
Stampa: A4 orizzontale, scala 74% (dalla 2026-10-07; prima 78%), margini superiore e inferiore 1,27 cm; con molti rischi segnalati lo script (`prepara_report`) riduce la scala, fino al 60%, perche' il Quadro resti in due pagine.

### Fenomeni (rischi in osservazione, D-79)

Pagina del report fra Delta e Metodologia. A4:K4 unite: quanti rischi nel radar
(con la capienza) e in osservazione, entrati, usciti e in uscita nel ciclo.
Intestazioni in riga 6, un rischio per riga in 7-26 (20, `capienzaOsservazione`);
L (nascosta) = riga del RiskRegister del k-esimo rischio in osservazione per
`Ordine_Osservazione`. Colonne: A numero, B ID, C rischio, D categoria con il
nome, E "Imp · Prob · Pross · Vel" (— = non valutata), F score, G perche' fuori
dal radar (Motivo_Stato), H orizzonte in anni, I segnale di avvicinamento, J
driver con i nomi, K notizie di A3 delle ultime 4 settimane (`NW_Rischio_ID`).
Righe 28-35: "Entrati e usciti dal radar in questo ciclo" (B ID, C rischio, D
movimento, E:K unite il motivo), L = riga della k-esima riga del ciclo con un
Movimento. Legenda in riga 37; stampa A1:K37, A4 orizzontale.

```excel
=IFERROR(MATCH(AGGREGATE(14,6,RR_Ordine_Osservazione,1),RR_Ordine_Osservazione,0)+5,"")
=IF($L7="","",INDEX(RiskRegister!$E:$E,$L7)&" "&IFERROR(INDEX(nomiL1,MATCH(INDEX(RiskRegister!$E:$E,$L7),codiciL1,0)),""))
=IF($L7="","",INDEX(RiskRegister!$G:$G,$L7)&" · "&INDEX(RiskRegister!$K:$K,$L7)&" · "&INDEX(RiskRegister!$I:$I,$L7)&" · "&IF(INDEX(RiskRegister!$H:$H,$L7)="","—",INDEX(RiskRegister!$H:$H,$L7)))
=IFERROR(AGGREGATE(15,6,ROW(RR_Ciclo)/((RR_Ciclo=cicloCorrente)*(RR_Movimento<>"")),1),"")
```

(L7 con k = 1..20, D7, E7, L30 con k = 1..6). J7 sostituisce nei codici dei
driver i nomi: otto SUBSTITUTE annidati, uno per riga di `codiciDriver` /
`nomiDriver`. Le altre colonne leggono la tabella come il Piano_azioni.

### Metodologia

Testo in sezioni (chi produce i numeri, schede e A6 compresi; fonti ed
evidenze; analisi per dimensioni; score composito; scale; regole di
variazione; urgenza; KRI; registro unico, radar e osservazione, con la regola dai nomi di Parametri; come si leggono i grafici; validazione); pesi e
parametri come riferimenti ai nomi di Parametri; scale e regole di variazione
copiate dalla rubrica.

**Stampa** dei sette fogli del report: A4 orizzontale (Radar_Mosca verticale),
adatta a 1 pagina in larghezza (Classifica e Matrice anche in altezza),
intestazione con nome del foglio, "Uso interno" e "Horizon Scan NFR", piede
con nome del file e "Pagina n di N". Lo script adatta le altezze delle righe
di `quadroCommento`, `quadroSegnalati`, `deltaMotivi` e `fenomeniLista` ai testi del ciclo.

## 7. Fogli di lavoro

**Storico**: righe 5-24 (A e B = `posID`, `posNome`), colonne C-J = i cicli
di `cicliTrend` in riga 4 (`=Parametri!$B$20` ...); grafico a linee, una serie
per riga, asse fisso 0-5.

```excel
=IF(OR($A5="",C$4=""),NA(),IF(COUNTIFS(RR_ID_Rischio,$A5,RR_Ciclo,C$4)=0,NA(),SUMIFS(RR_Score_Composito,RR_ID_Rischio,$A5,RR_Ciclo,C$4)))
```

**Indicatori**, a sinistra i KRI in vigore nel ciclo corrente. Conteggi per
stato in riga 4 (Verde, Ambra, Rosso, Non rilevato, Soglie da definire);
intestazioni in riga 6; righe 7-66. Z7:Z66 e' la colonna di
appoggio nascosta (riga del k-esimo KRI corrente); A-I leggono lo storico con
INDEX su quella riga (testo con `&""`, numeri e date lasciati vuoti se vuoti);
J = valore del ciclo precedente; K = tendenza. L = tipo del KRI (D-64), `=IF($Z7="","",INDEX(KRI!$E:$E,$Z7)&"")`; il nome del KRI scelto in N5 riporta il tipo fra parentesi.

```excel
=COUNTIFS(KRI_Ciclo,cicloCorrente,KRI_In_Vigore,"Sì",KRI_Stato,"Verde")
=IFERROR(AGGREGATE(15,6,ROW(KRI_Ciclo)/((KRI_Ciclo=cicloCorrente)*(KRI_In_Vigore="Sì")),1),"")
=IF($Z7="","",INDEX(KRI!$B:$B,$Z7)&"")
=IF($Z7="","",IF(INDEX(KRI!$I:$I,$Z7)="","",INDEX(KRI!$I:$I,$Z7)))
=IF($A7="","",IF(COUNTIFS(KRI_KRI_ID,$A7,KRI_Ciclo,cicloPrecedente,KRI_Valore_Corrente,"<>")=0,"—",SUMIFS(KRI_Valore_Corrente,KRI_KRI_ID,$A7,KRI_Ciclo,cicloPrecedente)))
=IF(OR(G7="",NOT(ISNUMBER(J7))),"",IF(G7>J7,"▲ peggiora",IF(G7<J7,"▼ migliora","● invariato")))
```

(B4, Z7, A7, G7, J7, K7). A destra (M-T) la storia di un KRI: N4 = input
(unica cella gialla), convalida a elenco `=elencoKRI`. L'elenco sta nella
colonna nascosta AB12:AB161: un KRI per riga, preso dalla riga dello storico in
cui `Ciclo` = `Ciclo_Definizione` (la prima di ogni KRI, anche se poi e' uscito
di vigore). Il nome `elencoKRI` e'
`=OFFSET(Indicatori!$AB$12,0,0,MAX(1,COUNTIF(Indicatori!$AB$12:$AB$161,"?*")),1)`.
AA4 (nascosta) = riga dell'ultima fotografia del KRI, da cui N5:N9 leggono
nome, rischio, unita', fonte, ciclo di definizione. Tabella in righe 12-19 sui
cicli di `cicliTrend`:

```excel
=IFERROR(INDEX(KRI_KRI_ID,AGGREGATE(15,6,(ROW(KRI_KRI_ID)-5)/((KRI_Ciclo_Definizione=KRI_Ciclo)*(KRI_KRI_ID<>"")),1)),"")
=IFERROR(AGGREGATE(14,6,ROW(KRI_KRI_ID)/(KRI_KRI_ID=$N$4),1),"")
=IF($M12="",NA(),IF(COUNTIFS(KRI_KRI_ID,$N$4,KRI_Ciclo,$M12,KRI_Valore_Corrente,"<>")=0,NA(),SUMIFS(KRI_Valore_Corrente,KRI_KRI_ID,$N$4,KRI_Ciclo,$M12)))
=IF($M12="",NA(),IF(COUNTIFS(KRI_KRI_ID,$N$4,KRI_Ciclo,$M12,KRI_Soglia_Attenzione,"<>")=0,NA(),SUMIFS(KRI_Soglia_Attenzione,KRI_KRI_ID,$N$4,KRI_Ciclo,$M12)))
=IFERROR(INDEX(KRI_Stato,MATCH($M12&"|"&$N$4,KRI_Chiave,0)),"—")
```

(AB12: il 5 e' la prima riga dati meno uno, per passare dalla riga del foglio
alla posizione nel nome; AA4; N12 valore; O12 soglia di attenzione — P12
uguale con `KRI_Soglia_Allerta` —; Q12 stato; R-T data, fonte e nota della
rilevazione). Un valore non rilevato o una soglia non ancora fissata e' #N/D,
un buco nel grafico, non uno zero. Grafico a linee di N11:P19 (valore con marcatori, soglie tratteggiate
ambra e rossa) in M22, asse verticale con minimo 0 e massimo automatico.

**Notizie**: una riga per categoria della tassonomia interna (5-13, D-74):

```excel
=MAXIFS(NW_Imp_9_1,NW_Settimana,">="&inizioFinestra4,NW_Settimana,"<="&settimanaCorrente)
=COUNTIFS(NW_Imp_9_1,">=2",NW_Settimana,">="&inizioFinestra4,NW_Settimana,"<="&settimanaCorrente)
=COUNTIF(ANA_Event_Type,A5)
=IF(E5>0,"Presidiata",IF(COUNTIFS(RR_Ciclo,cicloCorrente,RR_Stato,"Osservazione",RR_Event_Type,A5)>0,"In osservazione",IF(D5>0,"AREA NON PRESIDIATA","Nessun rischio censito")))
=COUNTIFS(NW_Imp_9_1,1,NW_Settimana,">="&inizioFinestra4,NW_Settimana,"<="&settimanaCorrente)
=IF(F5="AREA NON PRESIDIATA","NON PRESIDIATA ► ","")&A5&" "&B5
```

(C5, D5, E5, F5, G5 — con 2 e 3 in H5 e I5 —, J5; nelle righe successive
`NW_Imp_9_4` ... `NW_Imp_9_13`). D15 = notizie non collegate a un rischio
censito. Pressione settimanale in righe 19-30: settimana,
`=COUNTIFS(NW_Settimana,A19)`, peggiorativi, migliorativi, netto. Grafici sotto
le tabelle (A33, A54): barre orizzontali **impilate** di G4:I13 con categorie
J5:J13 (ordine inverso, la prima categoria in alto, colori dal chiaro allo scuro) e barre dei
segnali per settimana.

**Piano_azioni**: righe 6-155. N (nascosta) = riga del foglio Azioni della
k-esima azione da mostrare: prima le proposte da decidere, poi le azioni
aperte di ogni ciclo, poi le chiuse (completate, respinte, annullate) del ciclo
corrente e del precedente. La storia intera resta nel foglio Azioni.

```excel
=IFERROR(MOD(AGGREGATE(15,6,(ROW(AZ_Stato)+1000000*((AZ_Stato<>"Proposta — da valutare")+((AZ_Stato="Completata")+(AZ_Stato="Respinta")+(AZ_Stato="Annullata"))))/((AZ_ID_Azione<>"")*((1-((AZ_Stato="Completata")+(AZ_Stato="Respinta")+(AZ_Stato="Annullata")))+((AZ_Stato="Completata")+(AZ_Stato="Respinta")+(AZ_Stato="Annullata"))*((AZ_Ciclo=cicloCorrente)+(AZ_Ciclo=cicloPrecedente)))>0),1),1000000),"")
=IF(OR($N6="",H6=""),"",IF(OR(G6="Approvata",G6="In corso"),EDATE(H6,N(INDEX(Azioni!$G:$G,$N6))),""))
```

(N6 con k = 1..150; I6 scadenza = data della decisione + orizzonte). Colonne A
ciclo, B rischio, C ID azione, D azione, E owner, F orizzonte, G stato
(colorato: giallo da decidere, azzurro approvata, verde in corso o completata,
grigio respinta o annullata), H decisa il, I scadenza, J validazione. Riga 4:
fascia "La proposta (A1)" su A-F e "La decisione (validazione) e
l'avanzamento" su G-I. Nessuna colonna "Riduce": dal 30/09 l'azione non dichiara
la dimensione che riduce (D-54).

**Osservazione** (D-79): a sinistra i rischi in osservazione del ciclo corrente
(intestazione in riga 5, righe 6-25, AF nascosta = stessa formula di
Fenomeni!L7): A ID, B rischio, C categoria, D driver, E-H Impatto, Probabilita,
Prossimita, Velocity (scala dei colori delle dimensioni), I score, J perche' fuori
dal radar, K orizzonte, L segnale di avvicinamento, M descrizione, N validazione,
O notizie di A3 delle ultime 4 settimane; righe 27-38 entrati e usciti dal radar
(AF = stessa formula di Fenomeni!L30: A ID, B rischio, C movimento, D stato ora,
E-I dimensioni e score, J:N unite il motivo). A destra, da P4, la concentrazione:
driver (righe, `=INDEX(nomiDriver,1)` ...) per categoria (colonne Q-Y, codici in
riga 5) con il totale in Z, prima i rischi in osservazione, poi (da P16) i rischi
del radar (anagrafica) con lo stesso incrocio; fondo FCE4D6 da 1, F8CBAD da 2,
F4B183 da 3.

```excel
=IF(COUNTIFS(RR_Ciclo,cicloCorrente,RR_Stato,"Osservazione",RR_Event_Type,Q$5,RR_Driver,"*"&INDEX(codiciDriver,1)&"*")=0,"",COUNTIFS(RR_Ciclo,cicloCorrente,RR_Stato,"Osservazione",RR_Event_Type,Q$5,RR_Driver,"*"&INDEX(codiciDriver,1)&"*"))
=IF(COUNTIFS(ANA_Event_Type,Q$17,ANA_Driver,"*"&INDEX(codiciDriver,1)&"*")=0,"",COUNTIFS(ANA_Event_Type,Q$17,ANA_Driver,"*"&INDEX(codiciDriver,1)&"*"))
```

(Q6 e Q18). Riquadri bloccati in C6.

**Validazione** (griglia di lavoro del validatore, D-67): quattro sezioni una
sotto l'altra, a capienza fissa, con le righe libere **nascoste** (nel template
tutto e' validato, quindi sono nascoste tutte); le scrive lo script, che le
legge e le riscrive solo tramite i nomi `VG_...`. Riga 3 (A3:O3 unite, nome
`valStato`): i periodi da validare. Ogni sezione ha il titolo (nome
`VG_<oggetto>_titolo`), l'intestazione e le righe:

| Sezione | Titolo | Righe | Colonne |
|---|---|---|---|
| Rischio | A5 | 7-26 (20) | A ID, B rischio, C/D Impatto proposto/giallo, E/F Probabilita, G/H Prossimita, I/J Velocity, K/L anni di adeguamento, M Motivazione, N Score composito, O Margine di Mosca, P Segnalazioni dei controlli (larga 60, a capo; fondo FCE4D6 se contiene DA MOTIVARE; P5 = segnalazioni sul ciclo); dopo le colonne nascoste (D-79) W stato calcolato con il motivo (larga 36, a capo; lilla se Osservazione, ambra se in uscita), X/Y decisione sullo stato in vigore e gialla (elenco Automatico, Radar, Osservazione) |
| KRI | A28 | 30-109 (80) | A KRI, B indicatore, C tipo, D/E valore, F/G soglia di attenzione, H/I soglia di allerta, J Respingi, M Motivazione |
| Azione | A111 | 113-212 (100) | A azione, B descrizione, C:D owner proposto e E:F owner giallo (celle unite), G/H orizzonte, I Respingi, M Motivazione |
| Notizia | A214 | 216-415 (200) | A notizia, B titolo, C:D rischio proposto e E:F rischio giallo (unite), G/H segnale, I Respingi, J settimana, M Motivazione |

Colonne nascoste: Q periodo, R appoggio (rischio: 1 = segnalazione da motivare;
azione: il suo rischio), S-V calcoli. Proposte su fondo F2F2F2 con
testo grigio, valori e Motivazione su fondo giallo FFF2CC. Nomi definiti, per
ogni sezione: `VG_<oggetto>_ID`, `_Nome`, `_Motivazione`, `_Periodo`,
`_Appoggio`, `_<campo>` (cella gialla) e `_<campo>_P` (proposta) per ogni campo
della sezione `validazione` della mappa, `_Respingi` (KRI, azioni, notizie),
`_Tipo` (KRI), `_Settimana` (notizie), `_righe` (A:V della sezione); per i
rischi `VG_Rischio_Segnalazioni` (P), `VG_Rischio_SegnalazioniCiclo` (P5),
`VG_Rischio_Stato` (W), `VG_Rischio_Decisione_Stato_P` (X) e
`VG_Rischio_Decisione_Stato` (Y); inoltre
`VG_Rischio_Score`, `VG_Rischio_Margine`, `VG_Rischio_ScoreNum` (U),
`VG_Rischio_MargineNum` (S), `VG_Azione_Mesi` (S). Formule della prima riga
(si ripetono in tutte le righe della sezione):

```excel
=IF($A113="","",IF(OR($I113="Sì",$I113="Si"),0,IFERROR(VALUE(LEFT($H113,FIND(" ",$H113)-1)),0)))
=IFERROR(IF(COUNT($D7,$F7,$H7)<3,"",ROUND((pesoImpatto*$D7+pesoProbabilita*$F7+pesoProssimita*$H7+IF(ISNUMBER($J7),pesoVelocity*$J7,0))/(pesoImpatto+pesoProbabilita+pesoProssimita+IF(ISNUMBER($J7),pesoVelocity,0)),2)),"")
=IFERROR(IF(NOT(ISNUMBER($H7)),"",INDEX(anniProssimita,$H7)-(moscaX+MAX(IF(COUNTIFS($R$113:$R$212,$A7,$Q$113:$Q$212,$Q7,$S$113:$S$212,">0")=0,moscaYDefault,MAXIFS($S$113:$S$212,$R$113:$R$212,$A7,$Q$113:$Q$212,$Q7)/12),IF(ISNUMBER($L7),$L7,IFERROR(N(INDEX(ANA_Anni_Adeguamento,MATCH($A7,ANA_ID,0))),0))))),"")
=IF(NOT(ISNUMBER($U7)),"",FIXED($U7,2)&IF(AND(ISNUMBER($V7),$V7<>$U7),"  (era "&FIXED($V7,2)&")",""))
```

(S113: mesi dell'orizzonte giallo, 0 se l'azione e' respinta; T113 uguale sul
proposto, colonna G, senza Respingi. U7: score con i valori gialli; V7 uguale
sulle proposte C, E, G, I. S7: margine di Mosca con i valori gialli e le azioni
non respinte della griglia; T7 uguale su G, K e T113:T212. N7: lo score come
testo, con "(era ...)" se la validazione lo cambia; O7 allo stesso modo il
margine, con l'urgenza davanti: AGIRE ORA sotto 0, Entro l'anno sotto 1,
Margine oltre.) Tutte dentro IFERROR: un valore sbagliato scritto nella griglia
non deve produrre errori di formula, che fermerebbero ogni scrittura.
Formattazione condizionale: cella gialla diversa dalla proposta = arancio
F8CBAD (anche da "n.v." o "—" a un valore); Motivazione F4B183 se la riga ha un
cambio, un Respingi o l'appoggio 1 e meno di 10 caratteri; Respingi = Sì
F8CBAD; O come le etichette dell'urgenza; N arancio se contiene "(era".
Convalide: interi 1-5 sulle dimensioni gialle (vuoto ammesso), decimale 0-30
sugli anni, elenco "Sì" su Respingi, "3 mesi,6 mesi,12 mesi" sull'orizzonte,
i quattro segnali sul segnale, le tre decisioni sullo stato. In fondo (riga 417)
la nota sullo storico. Stampa A1:O417, A4 orizzontale, una pagina in larghezza (le
righe nascoste non si stampano).

**Dizionario**: una riga per ogni colonna di ogni tabella dati (dalla mappa),
per i valori calcolati nelle viste e per parametri e anagrafica: dato, dove,
chi lo scrive e quando (cella sul colore del processo), che cosa significa,
come si calcola, valori ammessi, esempio. I testi sono in `COME`, `VALORI`,
`CALCOLATI` e `PARAMETRI_DIZ` di `genera_dashboard.py`.

**Guida**: a cosa serve il workbook; tabella "chi aggiorna cosa e quando"
(foglio per foglio, colonne settimanale, trimestrale, validatore, a che cosa
serve); quando si lanciano A5 e A6; dove si scrive a mano; regole; primo uso
reale.

## 8. Verifica finale

Aprire il file, *Formule > Calcola ora*: nessun errore diverso da #N/D (che
e' voluto dove la formula contiene NA()). Registro!H5 deve dire "Ciclo
completo" sui dati di esempio. Meglio ancora: eseguire
`99_Collaudo/run_catena.py` puntando al file costruito a mano.

Il registro vivo NON si ricava da questo file cancellando a mano gli esempi:
lo crea il comando `inizializza` dello script (guida passo passo, sezione 0).
