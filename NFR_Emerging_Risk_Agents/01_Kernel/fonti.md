# Fonti esterne e interne — elenco validato

> **Stato al 24/09/2026** (`04_Riferimenti/DECISIONI.md`): **tutte approvate**
> tranne FNT-19. D-15: RSS istituzionali e i quattro siti della knowledge web.
> D-27: fonti a licenza e di stampa, dopo la verifica di Legal. D-29: CERTFin,
> ENISA e fonti interne. **FNT-19 e' esclusa** (D-28): il monitoraggio dei
> fornitori ICT critici e' gia' fatto in altre sedi. Ogni cambio di `stato`
> (`approvata` / `esclusa`) si registra in DECISIONI.md. Revisione almeno
> annuale (`04_Riferimenti/controlli_e_model_risk.md`, sezione 4).
>
> Questo file e' l'UNICA fonte dell'elenco. Lo leggono:
> - `02_Agenti/componi_prompt.py`: l'elenco compatto (codice, nome, canale)
>   entra nelle istruzioni di A3, segnaposto `{{FONTI}}`;
> - `07_Senza_Studio/raccogli_notizie.py`: legge i feed delle fonti `rss`
>   e scrive la raccolta della settimana in `News_Inbox`;
> - `07_Senza_Studio/esegui_ciclo_locale.py settimanale`: rifiuta una notizia
>   di A3 con un `codice_fonte` che non e' qui, o che e' `esclusa`;
> - `99_Collaudo/test_fonti.py`: formato, codici unici, limiti di Agent Builder.
>
> Tre canali, tutti insieme:
> - `rss`: raccolta automatica, deterministica, senza LLM (W0). Lo script
>   scarica i feed e scrive `News_Inbox/<lunedi'>/Raccolta_<data>.txt`, che A3
>   legge come knowledge SharePoint.
> - `sito`: siti pubblici senza un feed utilizzabile. Quelli con
>   `sito_agente: si` vanno configurati come knowledge web dell'agente.
>   **Agent Builder ne accetta al massimo quattro**, con URL di al massimo due
>   livelli e senza parametri (Microsoft Learn, "Add knowledge sources", agg.
>   29/07/2026); il collaudo lo verifica. Gli altri li consulta l'analista, che
>   salva cio' che serve in `News_Inbox/<lunedi'>/Manuali/`.
> - `share`: documenti interni o a licenza, gia' in SharePoint
>   (`Analisi_Interne`) o caricati a mano in `News_Inbox/<lunedi'>/Manuali/`.
>
> Una notizia portata da un analista da una fonte fuori elenco ha codice
> `MAN`: e' ammessa, ma la sua fonte va scritta per esteso nel campo `fonte`.
>
> Formato di ogni voce (lo legge `07_Senza_Studio/fonti.py`): un titolo
> `### FNT-nn Nome`, poi righe `- chiave: valore`. Chiavi: `canale` (rss, sito,
> share), `indirizzo`, `temi` (codici di tassonomia e driver), `stato`
> (da validare, approvata, esclusa), `licenza`; facoltative `sito_agente`
> (si/no), `max_voci` (default 20), `escludi` (parole nel titolo da scartare,
> separate da `;`), `verificato`. Le righe `>` sono commento e non entrano
> nel prompt.
>
> `verificato` = data in cui l'indirizzo ha risposto con un feed valido dal
> PC che ha preparato l'elenco (23/09/2026). Non e' una validazione di merito.

## Vigilanza e regolazione

### FNT-01 BCE Vigilanza bancaria, comunicati
- canale: rss
- indirizzo: https://www.bankingsupervision.europa.eu/rss/press.html
- temi: 9.6, 9.9, 9.13, 9.1, 9.4, DRV-TPR, DRV-CYB, DRV-CLI
- stato: approvata
- licenza: pubblico
- verificato: 2026-09-23, 15 voci
> Priorita' SSM, esiti SREP aggregati, lettere alle banche su cyber, terze parti,
> rischio climatico. E' la voce del supervisore diretto di una banca significativa.

### FNT-02 BCE Vigilanza bancaria, pubblicazioni
- canale: rss
- indirizzo: https://www.bankingsupervision.europa.eu/rss/pub.html
- temi: 9.6, 9.9, 9.13, DRV-TPR, DRV-CYB, DRV-TEC
- stato: approvata
- licenza: pubblico
- verificato: 2026-09-23, 15 voci
> Guide e rapporti (es. esiti degli stress test cyber, guida sull'outsourcing
> cloud). Poche voci, alto valore per A1.

### FNT-03 EBA, notizie e comunicati
- canale: rss
- indirizzo: https://www.eba.europa.eu/news-press/news/rss.xml
- temi: 9.7, 9.1, 9.4, 9.6, 9.9, DRV-TPR, DRV-CYB, DRV-CON
- stato: approvata
- licenza: pubblico
- verificato: 2026-09-23, 10 voci
> Linee guida (ICT e sicurezza, frodi nei pagamenti), comunicati congiunti delle
> ESAs su DORA. Attenzione: il vecchio feed www.eba.europa.eu/rss.xml esiste ma
> e' fermo al 2024.

### FNT-04 ESMA, notizie
- canale: rss
- indirizzo: https://www.esma.europa.eu/rss.xml
- temi: 9.1, 9.4, DRV-CON, DRV-CLI
- stato: approvata
- licenza: pubblico
- verificato: 2026-09-23, 10 voci senza data
> Greenwashing, nomi dei fondi ESG, condotta nei servizi di investimento.
> Il feed non porta date: lo script usa la data di prima raccolta.

### FNT-05 Banca d'Italia, aggiornamenti del sito
- canale: rss
- indirizzo: https://www.bancaditalia.it/util/index.rss.html?lingua=it
- temi: 9.7, 9.1, 9.4, 9.6, 9.9, 9.13, DRV-CYB, DRV-TPR, DRV-CON
- stato: approvata
- licenza: pubblico
- escludi: Cambi di riferimento; Annuncio; Titoli; Graduatoria; concors; assunzion; Bilancia dei pagamenti; Questioni di economia; Consolidated financial statement
- verificato: 2026-09-23, 41 voci
> E' il feed di TUTTO il sito: senza `escludi` sarebbe dominato da cambi e aste.
> Tenere d'occhio: comunicazioni di vigilanza, UIF, sistema dei pagamenti. Se la
> Banca d'Italia pubblica feed tematici, sostituirlo.

### FNT-06 Commissione europea, sala stampa
- canale: rss
- indirizzo: https://ec.europa.eu/commission/presscorner/api/rss?language=it
- temi: 9.1, 9.4, 9.6, 9.9, DRV-AI, DRV-GEO, DRV-CLI
- stato: approvata
- licenza: pubblico
- max_voci: 15
- verificato: 2026-09-23, 10 voci
> Sanzioni internazionali, pacchetti normativi (AI Act, pagamenti). Molte voci
> fuori tema: A3 le scarta. L'indirizzo ha parametri: va bene per lo script,
> non come knowledge web dell'agente.

### FNT-07 FSB, pubblicazioni e comunicati
- canale: rss
- indirizzo: https://www.fsb.org/feed/
- temi: 9.6, 9.9, DRV-TPR, DRV-CYB, DRV-AI
- stato: approvata
- licenza: pubblico
- verificato: 2026-09-23, 10 voci
> Terze parti critiche, resilienza operativa, AI nel settore finanziario: vista
> internazionale, anticipa di mesi i temi europei.

### FNT-08 BIS, comunicati (incluso il Comitato di Basilea)
- canale: rss
- indirizzo: https://www.bis.org/doclist/all_pressrels.rss
- temi: 9.6, 9.9, 9.13, DRV-CYB, DRV-TPR
- stato: approvata
- licenza: pubblico
- verificato: 2026-09-23, 10 voci
> Il BIS non espone un feed dedicato al solo Comitato di Basilea: i suoi
> documenti escono in questo feed dei comunicati.

### FNT-09 Commissione europea, strategia digitale
- canale: rss
- indirizzo: https://digital-strategy.ec.europa.eu/en/rss.xml
- temi: 9.6, 9.9, DRV-AI, DRV-CYB
- stato: approvata
- licenza: pubblico
- verificato: 2026-09-23, 10 voci
> AI Act (obblighi e scadenze), NIS2, cyber resilience act.

## Cyber e frodi

### FNT-10 ACN, CSIRT Italia: avvisi e allerte
- canale: rss
- indirizzo: https://www.acn.gov.it/portale/feedrss/-/journal/rss/20119/723192
- temi: 9.7, 9.6, 9.9, DRV-CYB
- stato: approvata
- licenza: pubblico
- max_voci: 25
- verificato: 2026-09-23, 50 voci
> Molto volume (vulnerabilita' singole). Serve per campagne e vulnerabilita'
> sfruttate su prodotti diffusi in banca, non per il singolo bollettino.
> Il vecchio indirizzo www.csirt.gov.it/data/indexer/rss risponde 403.

### FNT-11 CERT-EU, threat intelligence
- canale: rss
- indirizzo: https://cert.europa.eu/publications/threat-intelligence-rss
- temi: 9.7, 9.6, 9.9, DRV-CYB, DRV-GEO
- stato: approvata
- licenza: pubblico
- verificato: 2026-09-23, 10 voci
> Cyber Brief mensile: sintesi di minacce e campagne sull'Europa. Poche voci,
> alta densita'.

### FNT-12 CERT-EU, security advisories
- canale: rss
- indirizzo: https://cert.europa.eu/publications/security-advisories-rss
- temi: 9.6, 9.9, DRV-CYB
- stato: approvata
- licenza: pubblico
- verificato: 2026-09-23, 10 voci
> Solo vulnerabilita' critiche: da tenere se la Banca non ha gia' un servizio di
> vulnerability intelligence (in quel caso, meglio FNT-34).

### FNT-13 NCSC Regno Unito, notizie e guide
- canale: rss
- indirizzo: https://www.ncsc.gov.uk/api/1/services/v1/all-rss-feed.xml
- temi: 9.6, 9.9, DRV-CYB, DRV-AI
- stato: approvata
- licenza: pubblico
- verificato: 2026-09-23, 20 voci
> Analisi di tendenza di qualita' (ransomware, AI offensiva). Fuori dall'UE:
> segnale anticipatore, non prova di prossimita'.

### FNT-14 Europol, notizie
- canale: rss
- indirizzo: https://www.europol.europa.eu/cms/api/rss/news
- temi: 9.7, DRV-CYB, DRV-AI
- stato: approvata
- licenza: pubblico
- verificato: 2026-09-23, 10 voci senza data
> Operazioni contro reti di frode, money mule, criminalita' informatica.
> Feed senza date: vale la data di prima raccolta.

### FNT-15 BleepingComputer, stampa specializzata cyber
- canale: rss
- indirizzo: https://www.bleepingcomputer.com/feed/
- temi: 9.7, 9.6, 9.9, DRV-CYB
- stato: approvata
- licenza: verificata da Legal il 2026-09-24 (D-27); stampa commerciale
- max_voci: 15
- verificato: 2026-09-23, 15 voci
> Arriva prima delle fonti istituzionali su incidenti a fornitori e banche.
> Stampa, non fonte ufficiale: per A1 conta come segnale, da confermare.

## Clima ed eventi fisici

### FNT-16 Aeronautica Militare, notizie meteo e clima
- canale: rss
- indirizzo: https://www.meteoam.it/it/rss
- temi: 9.8, 9.6, 9.9, DRV-CLI
- stato: approvata
- licenza: pubblico
- max_voci: 15
- verificato: 2026-09-23, 155 voci senza data
> Unico feed istituzionale italiano trovato su meteo e clima. Molto volume:
> `max_voci` lo limita. Per le allerte vere vedi FNT-23.

## Stampa generalista

### FNT-17 ANSA, Economia
- canale: rss
- indirizzo: https://www.ansa.it/sito/notizie/economia/economia_rss.xml
- temi: 9.11, 9.1, 9.4, 9.13, 9.9, DRV-HUM, DRV-GEO
- stato: approvata
- licenza: verificata da Legal il 2026-09-24 (D-27); uso dei feed soggetto alle condizioni ANSA
- max_voci: 20
- verificato: 2026-09-23, 67 voci
> Scioperi, vertenze, fatti di settore: e' l'unica fonte dell'elenco che copre
> la categoria 9.11 Employer (rapporti di lavoro, D-74). Il feed ANSA Tecnologia e' fermo al 2023.

### FNT-18 Il Sole 24 Ore, Finanza
- canale: rss
- indirizzo: https://www.ilsole24ore.com/rss/finanza.xml
- temi: 9.1, 9.4, 9.13, 9.9, DRV-CON, DRV-TEC
- stato: approvata
- licenza: verificata da Legal il 2026-09-24 (D-27); abbonamento aziendale
- verificato: 2026-09-23, 4 voci
> Il feed porta solo titoli e poche voci; il testo richiede l'abbonamento.

## Terze parti critiche

### FNT-19 Stato dei servizi dei fornitori ICT critici
- canale: rss
- indirizzo: da compilare
- temi: 9.6, 9.9, DRV-TPR
- stato: esclusa
- licenza: pubblico
> ESCLUSA il 24/09/2026 (D-28): il monitoraggio dei fornitori ICT critici e' gia'
> fatto in altre sedi. Resta nell'elenco come traccia della scelta.
> Una voce per ciascun fornitore critico del registro DORA che pubblica una
> pagina di stato con feed. Esempio verificato il 23/09/2026:
> https://status.aws.amazon.com/rss/all.rss (38 voci). Finche' l'indirizzo e'
> "da compilare" lo script salta la voce.

## Siti senza feed (knowledge web dell'agente, al massimo quattro)

### FNT-20 Banca d'Italia, vigilanza
- canale: sito
- indirizzo: https://www.bancaditalia.it/compiti/vigilanza
- temi: 9.1, 9.4, 9.6, 9.9, 9.13, DRV-TPR, DRV-CON
- stato: approvata
- licenza: pubblico
- sito_agente: si
> Normativa e comunicazioni di vigilanza nazionali: complemento tematico al feed
> generico FNT-05.

### FNT-21 CONSOB
- canale: sito
- indirizzo: https://www.consob.it
- temi: 9.1, 9.4, DRV-CON, DRV-CLI
- stato: approvata
- licenza: pubblico
- sito_agente: si
> Sanzioni e richiami su trasparenza e greenwashing. Nessun feed RSS trovato.

### FNT-22 Garante per la protezione dei dati personali
- canale: sito
- indirizzo: https://www.garanteprivacy.it
- temi: 9.1, 9.4, 9.7, DRV-AI, DRV-CON
- stato: approvata
- licenza: pubblico
- sito_agente: si
> Provvedimenti su dati dei clienti, AI e sistemi di sorveglianza. Nessun feed
> RSS trovato.

### FNT-23 Protezione Civile, rischi e allerte
- canale: sito
- indirizzo: https://www.protezionecivile.gov.it/it
- temi: 9.8, 9.6, 9.9, DRV-CLI
- stato: approvata
- licenza: pubblico
- sito_agente: si
> Allerte meteo-idro e bollettini: la prossimita' degli eventi fisici alle sedi.

### FNT-24 CERTFin
- canale: sito
- indirizzo: https://www.certfin.it
- temi: 9.7, 9.6, 9.9, DRV-CYB
- stato: approvata
- licenza: circolari riservate agli aderenti
- sito_agente: no
> Il sito pubblico dice poco; le circolari agli aderenti sono la parte utile e
> passano da FNT-34.

### FNT-25 ENISA
- canale: sito
- indirizzo: https://www.enisa.europa.eu
- temi: 9.6, 9.9, DRV-CYB, DRV-TPR
- stato: approvata
- licenza: pubblico
- sito_agente: no
> Threat Landscape annuale e rapporti settoriali: scaricarli in
> `Analisi_Interne` quando escono. Nessun feed RSS trovato.

## Documenti interni e a licenza (SharePoint)

### FNT-30 Incident report e perdite operative interne
- canale: share
- indirizzo: Analisi_Interne/Incidenti
- temi: 9.7, 9.11, 9.1, 9.4, 9.8, 9.6, 9.9, 9.13
- stato: approvata
- licenza: interno
> La prova piu' forte di prossimita': l'evento e' gia' successo in Banca.

### FNT-31 Report della Funzione Antifrode
- canale: share
- indirizzo: Analisi_Interne/Antifrode
- temi: 9.7, DRV-AI, DRV-CYB
- stato: approvata
- licenza: interno
> Fonte dei valori di molti KRI di frode.

### FNT-32 Relazioni di audit interno e follow-up
- canale: share
- indirizzo: Analisi_Interne/Audit
- temi: 9.7, 9.1, 9.4, 9.6, 9.9, 9.13
- stato: approvata
- licenza: interno
> L'evidenza con cui la Banca aggiorna il presidio dei controlli
> dell'anagrafica (controlli testati; D-49: non e' piu' una dimensione dello score).

### FNT-33 Registro DORA, test di continuita' e di uscita
- canale: share
- indirizzo: Analisi_Interne/ICT_e_Continuita
- temi: 9.8, 9.6, 9.9, DRV-TPR, DRV-CLI
- stato: approvata
- licenza: interno
> Registro delle informazioni, esiti dei test BCM e delle exit strategy.

### FNT-34 Threat intelligence a pagamento e circolari CERTFin
- canale: share
- indirizzo: News_Inbox/<lunedi'>/Manuali
- temi: 9.7, 9.6, 9.9, DRV-CYB, DRV-AI
- stato: approvata
- licenza: contratto del fornitore; circolari riservate agli aderenti
> Contenuti che non si possono raccogliere con un feed: l'analista salva il
> rapporto della settimana nella cartella Manuali. Verificare che la licenza
> permetta l'uso in un agente di AI.

### FNT-35 Fonti esterne di orizzonte (perdite di settore, report, analisi)
- canale: share
- indirizzo: Analisi_Esterne
- temi: 9.7, 9.11, 9.1, 9.4, 9.8, 9.6, 9.9, 9.13
- stato: approvata
- licenza: mista (consorzi a pagamento es. ORX News; report pubblici; analisi di terzi)
> Non solo un database di perdite: qualunque fonte esterna di orizzonte (report
> di settore, analisi, ricerche) che l'analista salva per uso ripetuto. E' la
> fonte piu' rilevante per l'Horizon Scanning: un rischio davvero emergente non
> ha ancora una traccia interna (audit, incidente), quindi l'evidenza arriva
> quasi sempre da fuori. Library separata da Analisi_Interne apposta (D-45):
> un documento esterno non deve mai essere scambiabile con uno della Banca in
> fonti[].tipo (vedi Input di A1). Prova anche di prossimita' "banca
> comparabile" quando descrive eventi presso altre banche.

### FNT-36 Newsletter e alert in abbonamento
- canale: share
- indirizzo: News_Inbox/<lunedi'>/Manuali
- temi: 9.1, 9.4, 9.13, 9.9, DRV-CON, DRV-GEO
- stato: approvata
- licenza: verificata da Legal il 2026-09-24 (D-27) per ciascun abbonamento
> Newsletter di studi legali e consulenti. L'analista salva il numero della
> settimana (PDF o testo) nella cartella Manuali.
