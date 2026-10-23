# 15. CS-2 approfondita: che cosa del Python non gira in Copilot Studio, e con che cosa sostituirlo

Data: 11/10/2026. Richiesta dell'utente:

> Rianalizza bene la soluzione CS 2 (tutto copilot studio) da realizzare post CS-1. Fammi capire in particolare quali
> parti dei python attuali non possono girare in copilot studio. Trova e valuta con attenzione se ci sono librerie o
> strade alternative, ad esempio con Agent Flow; vedi se l'uso dell'XML potrebbe semplificare la scrittura di macro
> Excel di compilazione. Analisi approfondita tra costi, benefici e vincoli architetturali: dove piu' standard, meno
> componenti Office e librerie usi, meglio e'.

Approfondisce la CS-2 di `14_Tre_strade.md` (14.5), che resta il quadro delle tre strade. Fatti verificati su
Microsoft Learn l'11/10/2026, fonti in fondo.

> **Nota del 23/10/2026.** Sul ramo `copilot-studio-pieno` la V2 e' progettata per la costruzione (D-82,
> `NFR_Emerging_Risk_Agents/09_Copilot_Studio/Copilot_Studio_pieno.md`, sezione 6), con una riserva nuova, **F2**, se
> Office Scripts non e' disponibile:
> - un registro dati `NFR_Dati.xlsx` scritto dal Python del code interpreter (openpyxl: nessun grafico da perdere);
> - la presentazione con i grafici in un file che lo legge con Power Query, oppure HTML (A-16);
> - gli ingressi nella busta con il connettore standard Excel Online.
>
> La "busta" del prompt con code interpreter (un solo file in ingresso, Learn 30/09/2026) e' gia' pronta per la prova
> K9: codice a blocchi nel foglio `_Motore`, ingressi in `tblIngresso`, impronta del codice stampata dal programma.

## 15.0 In breve

1. **Il Python di oggi ha tre parti che in Copilot Studio non girano cosi' come sono.**
   - L'accesso a Excel desktop via COM (`excel_com.py` e circa 1.400 righe del motore che lo usano), compreso il
     PDF del report.
   - Il disco del PC: archivio, backup, baseline, spiegazioni per A7, cartelle sincronizzate.
   - La rete del PC: la raccolta notizie con il proxy.

   Il resto, cioe' controlli, regola del radar, validatore, precontrollo, allegato di A1, schede e spiegazioni (circa
   2.000 righe), e' **solo libreria standard** (le schede usano openpyxl, che il sandbox ha). Gira gia' nel sandbox
   di Copilot Studio: l'ha mostrato T1.2.
2. **Il problema vero non sono le librerie ma chi esegue il codice.** In Copilot Studio esistono due soli posti in cui
   gira codice nostro:
   - il **code interpreter**, che esegue Python perche' il modello decide di farlo;
   - gli **Office Scripts**, cioe' TypeScript eseguito dentro Excel, deterministico e lanciato da un flusso con un
     connettore standard.

   Flussi e argomenti (Power Fx) sono deterministici, ma non sono un posto per 2.000 righe di regole.
3. **Le strade per la CS-2 sono tre** (15.4):

   | Variante | Logica | Scrittura del registro |
   |---|---|---|
   | **V1** | tutto in TypeScript negli Office Scripts | Office Scripts |
   | **V2** | Python, lo stesso codice, nel code interpreter | un unico Office Script generico, che esegue le scritture descritte in JSON: "Python decide, Excel esegue" |
   | **V3** | Python nel code interpreter | Python stesso, modificando l'XML del file `.xlsx`, poi il file intero sostituito |
4. **L'XML** (15.3) serve solo nella V3, per scrivere un `.xlsx` senza Excel con la libreria standard di Python.
   - Nei flussi non serve: si puo' estrarre uno zip ma non crearlo, quindi non si puo' ricomporre un `.xlsx`.
   - Le mappe XML di Excel e le macro VBA non esistono in Excel per il web ne' in Power Automate.
   - Come formato per descrivere "che cosa scrivere", JSON e' nativo per flussi, Office Scripts e Python; XML non
     aggiunge niente.
5. **Raccomandazione** (15.7): la **V2**, che tiene il Python del collaudo come unica fonte delle regole. Il registro
   lo scrive solo uno script piccolo e deterministico dentro il vero Excel: formule, tabelle, grafici, ricalcolo e
   controllo degli errori restano.

   Il cancello e' "a prova di guasto": un esito si scrive solo se porta l'impronta del motore vero, che il flusso
   confronta con quella attesa.

   Si arriva a tappe. Le prime (separare logica e accesso a Excel, esecutore in Office Script) servono anche alla
   CS-1. La scelta finale dipende da tre prove brevi: K8 (Office Scripts), K9 (code interpreter nei prompt), K10 (PDF).

   Se K9 fallisce resta la V1, piu' lunga. La V3 la sconsiglio.
6. **Se il criterio fosse solo "meno componenti", vincerebbe la V1**, perche' non ha nessuna IA nel percorso di
   scrittura. Pero' riscrive in un secondo linguaggio proprio la parte con il collaudo piu' ricco: oltre 800 verifiche.
   Per una banca, due implementazioni delle regole che possono divergere sono un rischio piu' grande di un componente
   in piu'.

## 15.1 Il Python di oggi, pezzo per pezzo

### I moduli in esercizio

| Modulo | Righe | Dipendenze | Che cosa fa | Nel sandbox di Copilot Studio |
|---|---|---|---|---|
| `valida_output.py` | 162 | solo standard | validatore degli schemi JSON | **gira** |
| `controlli_a5.py` | 400 | solo standard | controlli C1-C9 | **gira** |
| `radar.py` | 158 | nessuna | regola del registro unico | **gira** |
| `precontrollo.py` | 94 | solo standard | precontrollo e impronta | **gira** (T1.2) |
| `input_a1.py` | 97 | solo standard | allegato di A1 | gira, se riceve i testi invece dei percorsi |
| `fonti.py` | 65 | solo standard | fonti dal kernel | gira, come sopra |
| `schede.py` | 630 | standard e **openpyxl** (crea un file nuovo) | input di A6 e file delle schede | gira: openpyxl c'e'; il file esce come file del prompt |
| `spiegazioni.py` | 311 | solo standard | testi per A7 | gira, se restituisce testi invece di scrivere file |
| `excel_com.py` | 132 | **pywin32, Excel desktop** | apre Excel, ricalcola, cerca errori, legge tabelle | **non gira in nessun cloud** |
| `esegui_ciclo_locale.py` | 2.993 | standard, piu' `excel_com` | comandi, logica, scrittura | **solo la logica, separata dall'accesso a Excel** |
| `raccogli_notizie.py` | 241 | standard e **pypac** (proxy), rete | raccolta RSS | **non gira**: il sandbox non ha rete. Al suo posto un cloud flow con il connettore RSS |

Restano sul PC del manutentore, fuori dalla Banca, `genera_dashboard.py` (4.083 righe, openpyxl), `componi_prompt.py`,
`prepara_kit.py` e il collaudo. Producono template, prompt e kit, non girano in esercizio.

### Che cosa chiede il motore a Excel

Il motore e' gia' quasi separato: quasi tutto passa per la classe `Scrittore` e per poche chiamate alla sessione.

| Richiesta a Excel | Quante volte nel codice | Chi la puo' fare in Copilot Studio |
|---|---|---|
| leggere le righe di una tabella (`scr.righe`) | 42 | Office Script; connettore Excel Online "List rows"; Python che legge il file |
| aggiungere righe con valori e formule (`append`) | 7 | Office Script; "Add a row" (una riga per chiamata); Python sull'XML |
| aggiornare righe (`aggiorna`) | 9 | Office Script; "Update a row" (serve una colonna chiave); Python sull'XML |
| leggere e scrivere l'anagrafica e le celle con nome (`intervallo_nome`) | circa 50 | Office Script; Python sull'XML (il connettore non scrive celle sciolte) |
| ricalcolo completo (`ricalcola`) | 12 | **solo Excel**: Office Script, o l'apertura del file in Excel per il web |
| cercare errori di formula e formule mancanti | 9 | **solo dopo un ricalcolo**: Office Script |
| leggere valori calcolati dalle formule (copertura, segnali, presidio) | 4 | Office Script; oppure Python li ricalcola (la copertura gia' lo fa) |
| impaginare il report (altezze delle righe, zoom, spazio per il grafico) | 5 funzioni | Office Script (righe, zoom, area di stampa e grafici si leggono e si impostano) |
| PDF di 7 fogli | 1 | flusso: copia del file, fogli non del report nascosti, **Convert file** in PDF (da provare, K10) |
| salvataggio, backup, archivio, versione del template | vari | azioni SharePoint/OneDrive (copia, crea, sposta); la versione e' un nome definito da leggere |

### Le tre pareti

1. **Excel desktop.** Nel cloud il ricalcolo e il controllo degli errori li fanno solo Excel per il web e gli Office
   Scripts, che girano dentro di lui. Una libreria Python che scrive il file non ricalcola: i valori delle formule
   restano quelli dell'ultimo salvataggio in Excel.
2. **Disco e rete del PC.** Si sostituiscono con le azioni dei connettori SharePoint, OneDrive e RSS: lavoro di
   flusso, non di codice.
3. **Chi esegue il codice.** E' la parete che decide l'architettura (15.2).

### Quanto resta nella V2, fatto 100 tutto cio' che gira in esercizio (domanda dell'utente, 11/10)

Misura in caratteri, l'unica comune a prompt, kernel e Python. Il totale e' di circa 493 KB: prompt degli agenti,
`01_Kernel` e Python di `07_Senza_Studio`. Restano fuori, perche' non girano in esercizio, gli strumenti del
manutentore (generatore del template, composizione dei prompt, kit) e il collaudo, circa 600 KB, che restano sul PC
del manutentore.

| Parte | Quota | Destino nella V2 |
|---|---|---|
| Prompt degli agenti | 10,3% | invariati: si reincollano |
| Kernel (rubrica, tassonomia, fonti, schemi, mappa) | 24,7% | invariato: knowledge e file letti dal motore |
| Moduli Python senza Excel (controlli, radar, validatore, precontrollo, allegato, fonti, schede, spiegazioni) | 23,7% | invariati nel sandbox; quattro piccoli ritocchi, perche' ricevono testi invece di percorsi |
| Logica del motore (`esegui_ciclo_locale.py` senza Excel e senza riga di comando) | 28,6% | resta Python: lavora sull'adattatore del registro invece che su Excel |
| **Esclusa: accesso a Excel** (`Scrittore`, `excel_com.py`, impaginazione, controllo errori e formule, backup) | **4,7%** | Office Script esecutore, circa 250-350 righe di TypeScript |
| **Esclusa: regia dei comandi** (sessioni, cartelle, archivio, messaggi; circa meta' delle 920 righe dei comandi) | **5,9%** | agent flow e argomenti: configurazione, non codice |
| **Esclusa: raccolta notizie** (`raccogli_notizie.py`) | **2,1%** | cloud flow con il connettore RSS |

Quindi l'**87% resta com'e'** o con ritocchi leggeri, e il **13% si sostituisce**. Del solo Python, il 19,5%.

Si aggiunge codice nuovo, che oggi non c'e':
- l'adattatore del registro, circa 300-400 righe Python;
- il caricatore del motore nel prompt, con `_Scambio` e la verifica dell'impronta, circa 150 righe piu' le istruzioni
  del prompt.

**Complessita' di quel 13% e delle parti nuove**:

| Pezzo | Volume | Complessita' | Perche' |
|---|---|---|---|
| Flusso RSS | piccolo | bassa | connettore standard, oggi la logica e' poca |
| Agent flow e argomenti | circa 10 comandi | media | ognuno e' semplice, ma sono tanti; si provano solo nel tenant; si versionano esportando la soluzione |
| Adattatore del registro | 300-400 righe Python | media | va riprodotta esattamente la semantica di oggi: riga segnaposto, capienza delle tabelle, formule scritte riga per riga, anagrafica senza buchi. Il collaudo esistente lo verifica, eseguendo le stesse catene sui due backend |
| Office Script esecutore | 250-350 righe TypeScript | media | generico e stabile, ma deve fare dentro Excel per il web cio' che oggi fa COM: ricalcolo, errori, impaginazione, lucchetto. Limiti di 120 secondi e 3 chiamate ogni 10 secondi; si prova nel tenant |
| Motore nel prompt (caricatore e verifica) | circa 150 righe e il prompt | **alta, per incertezza** | dipende da come il code interpreter si comporta (un file in ingresso, 100 secondi, input senza istruzioni, esecuzione affidata al modello). E' il punto che la prova K9 deve chiarire per primo |

Il volume da rifare e' piccolo. Il rischio sta quasi tutto nell'ultima riga, ed e' per questo che K9 viene prima di
tutto il resto.

## 15.2 Che cosa offre Copilot Studio per eseguire codice e scrivere file

| Strumento | Che cosa esegue | Limiti che contano | Classe |
|---|---|---|---|
| **Code interpreter nell'agente** (chat) | Python che il modello scrive o esegue (T1.2: esegue lo script allegato) | file fino a 16 MB, al massimo 10; sui file strutturati e' **in anteprima**; i file prodotti sono solo **scaricabili dalla chat**: non c'e' una strada deterministica verso SharePoint | incluso, con abilitazione dell'ambiente |
| **Prompt con code interpreter** in un agent flow ("Run a prompt") | Python scritto o eseguito dal modello. La risposta contiene il **codice eseguito** (`code`), il **log** (`logs`) e i **file prodotti** in base64, che il flusso salva con "Create file" | **un solo file in ingresso** (con il code interpreter, Word, Excel o PowerPoint, oltre a PDF e immagini; non `.json` ne' `.txt`); **un solo file in uscita**; elaborazione dei documenti al massimo **100 secondi**; 25 MB; "gli input non possono contenere istruzioni"; i prompt con file in ingresso non si possono usare come strumento diretto dell'agente, solo dentro un flusso | "text and generative AI tools (premium)": per gli utenti Microsoft 365 Copilot "No charge" (da confermare con l'IT) |
| **Office Scripts** (connettore Excel Online, "Run script") | **il nostro TypeScript, sempre uguale**, dentro Excel per il web: tabelle, formule, ricalcolo, formati, grafici, impaginazione | 120 secondi per chiamata; 1.600 chiamate al giorno per utente, 3 ogni 10 secondi; 5 MB per richiesta; niente chiamate esterne; **niente aggiornamento di Power Query** nei flussi; niente PDF; l'amministratore li puo' spegnere. Gli script si possono tenere in una **library SharePoint** (file `.osts`) e lanciare da li' | **standard** |
| **Connettore Excel Online, azioni sulle righe** | nessun codice: aggiunge, aggiorna, cancella, legge righe di tabelle | una riga per chiamata; 100 chiamate al minuto; il file puo' restare **bloccato fino a 6 minuti** dopo l'uso; modifiche visibili fino a 30 secondi dopo; con formule pesanti, timeout e **righe inserite due volte** per i tentativi automatici; modifiche contemporanee non supportate | **standard** |
| **Azioni SharePoint / OneDrive** | file: crea, aggiorna, copia, sposta, estrae uno zip, **converte in PDF** | non creano zip; la conversione in PDF va provata sul nostro report | **standard** |
| **Espressioni dei flussi** | trasformazioni deterministiche (JSON, `xml()`, `xpath()`, filtri, cicli) | nessuna funzione di hash; cicli lenti; non si collaudano fuori dal tenant | standard |
| **Power Fx negli argomenti** | formule deterministiche | adatte a controlli piccoli, non a centinaia di regole | standard |
| **Connettori premium negli agent flow** (per esempio HTTP con Microsoft Entra ID verso le API Excel di Microsoft Graph) | chiamate dirette alle API | ammessi negli agent flow e senza costi per gli utenti Microsoft 365 Copilot, ma tipicamente **bloccati dalle data policy** di una banca; un componente in piu' senza vantaggi rispetto agli Office Scripts | premium |
| **Power Query** in Excel per il web | aggiorna query da file JSON, XML o CSV, cartelle e liste SharePoint | l'aggiornamento e' **manuale**: un Office Script lanciato da un flusso non lo fa | incluso |

## 15.3 XML: dove aiuta e dove no

| Idea | Si puo'? | Valutazione |
|---|---|---|
| **Scrivere il `.xlsx` modificando il suo XML** (un `.xlsx` e' uno zip di file XML) **in Python**, con `zipfile` e `xml.etree` della libreria standard | **si'**, nel sandbox | E' l'unico modo di scrivere il registro senza Excel e **senza perdere** grafici, convalide e formattazioni condizionali, che openpyxl invece perde. Si toccano solo le parti dei fogli e delle tabelle. Costa circa 600-900 righe e va trattato con cura: stringhe condivise, stili delle righe nuove, intervallo delle tabelle, catena di calcolo. Il file non e' ricalcolato: si imposta "ricalcola all'apertura", ma i valori in cache restano vecchi finche' qualcuno non lo apre in Excel. E' la "macro di compilazione" in senso stretto: riempie un modello. Si usa solo nella V3 |
| **Scrivere il `.xlsx` via XML in un flusso** | **no** | I flussi estraggono uno zip ("Extract archive to folder") ma non lo ricreano, e le espressioni non calcolano il CRC degli zip |
| **Mappe XML di Excel** (importare un XML in tabelle mappate) | **no** | Solo in Excel desktop, non in Excel per il web ne' negli Office Scripts |
| **Macro VBA** | **no** | Non girano in Excel per il web ne' da Power Automate: "Run script" accetta i `.xlsm` ma esegue Office Scripts, non VBA |
| **Formato "XML Spreadsheet 2003"** prodotto come testo da un flusso | in parte | Niente tabelle, grafici ne' formule del nostro registro; Excel per il web non lo apre come un `.xlsx`. Non serve |
| **Descrivere in XML che cosa scrivere** (le operazioni) | si', ma inutile | JSON e' nativo per flussi, Office Scripts e Python; XML aggiungerebbe solo un parser in piu' |
| **Dati in file JSON o XML in SharePoint, letti da Power Query** (il registro diventa una vista) | si' | Multiutenza robusta, ma serve un registro riprogettato attorno alle query, e l'aggiornamento resta manuale: chi fa il PDF deve prima aprire e aggiornare. E' la CS-3 del piano 10: non conviene ora |

**In sintesi**: l'idea giusta dietro "XML per compilare" e' **descrivere in modo dichiarativo le scritture** e
lasciarle eseguire a un compilatore piccolo e sempre uguale. La V2 lo fa con un elenco JSON di operazioni e un
Office Script come compilatore; la V3 con Python che compila direttamente l'XML del file.

## 15.4 Le tre varianti della CS-2

Parti comuni a tutte:
- l'Operatore della CS-1 con argomenti a passi fissi (K6);
- un argomento e un agent flow per comando (trimestrale, settimanale, straordinario, valida, riapri, dismetti, schede,
  report, baseline);
- il lucchetto del registro (14.5-bis);
- l'archivio e le spiegazioni di A7 scritti con azioni SharePoint;
- la raccolta notizie con un cloud flow RSS;
- i JSON degli agenti che passano solo per i flussi.

### V1. Tutto negli Office Scripts (TypeScript)

**Come**: la logica di oggi, circa 4.000 righe Python, si porta in TypeScript. Ogni comando diventa uno script:
`trimestrale` riceve l'output di A1 come parametro, controlla, scrive, ricalcola, verifica e restituisce esito e testi.
Gli script non hanno moduli, quindi un generatore li compone da sorgenti comuni (come `prepara_kit.py`). I file
`.osts` si tengono in una library SharePoint.

**Pro**:
- nel percorso di scrittura nessuna IA e nessuna funzione in anteprima;
- cancello deterministico e completo;
- D-11 resta;
- connettori solo standard;
- **il minor numero di componenti in esercizio**.

**Contro**:
- **riscrittura di tutte le regole** in un secondo linguaggio: arrotondamenti (trappola 105), espressioni regolari,
  date (Power Automate lavora in UTC), validatore degli schemi da riscrivere a mano (negli Office Scripts non si
  importano librerie);
- il collaudo Python diventa l'oracolo, e il confronto Python/TypeScript richiede Node.js sul PC del manutentore;
- i test di integrazione si fanno solo nel tenant;
- D-02 va sostituita.

**Impegno**: 40-55 giorni (8-11 settimane).

### V2. "Python decide, Excel esegue" (raccomandata)

**Come**, per esempio `trimestrale`, in un solo agent flow:
1. **Esecutore, "prepara"**. Un unico Office Script generico, circa 250-350 righe di TypeScript che cambiano di rado,
   scrive in un foglio nascosto `_Scambio` del registro tre cose:
   - l'istantanea JSON delle tabelle e dei nomi che servono, con i valori appena ricalcolati;
   - l'output di A1 e i parametri del comando;
   - il codice del motore, che il flusso legge dalla library Kernel.

   Le celle tengono 32.767 caratteri l'una: il codice, circa 300 KB, ne occupa una decina.
2. **Prompt con code interpreter**, con un solo file in ingresso, il registro. Python legge `_Scambio`, calcola lo SHA-256
   del codice, lo esegue e produce un file `esito.json`:
   - la versione e l'impronta del motore;
   - l'esito dei controlli;
   - l'**elenco delle operazioni** da fare sul registro;
   - i testi per l'archivio e per A7.
3. **Verifica nel flusso**: l'impronta del motore nell'esito deve essere uguale a quella attesa, scritta accanto al
   codice nella library Kernel. Il modello non la conosce.
   - Se non coincide, o se l'esito manca, il flusso si ferma e non scrive niente.
   - Il codice eseguito e il log che il prompt restituisce si archiviano.
4. **Esecutore, "applica"**, cioe' il cancello di integrita' deterministico. Lo script:
   - prende il lucchetto;
   - applica le operazioni, solo su tabelle e nomi in lista bianca, senza toccare righe gia' validate;
   - ricalcola;
   - cerca errori di formula e formule mancanti;
   - confronta i valori di controllo (per esempio la copertura) con quelli attesi dal Python;
   - svuota `_Scambio` e rilascia il lucchetto.

   Il flusso fa prima una copia di sicurezza e, se lo script segnala un errore, rimette quella.
5. **Flusso**: crea i file nell'archivio e in `Kernel\Spiegazioni`, poi risponde all'Operatore.

Il motore Python cambia in un solo punto: un **adattatore del registro** con la stessa interfaccia di `Scrittore`
(`righe`, `append`, `aggiorna`, anagrafica, celle con nome).
- Una versione lavora sull'istantanea JSON e accumula le operazioni (cloud).
- Una versione resta su Excel via COM (PC, collaudo, riserva).

Le regole restano **lo stesso codice** del collaudo. Le schede si generano nel prompt con openpyxl, come oggi, e
escono come file. Il PDF si fa da una copia del registro con i soli fogli del report visibili e "Convert file".

**Pro**:
- le regole restano Python, collaudate e uniche;
- il TypeScript e' poco e generico: un compilatore di operazioni, non le regole;
- scrittura dentro il vero Excel, con ricalcolo, errori, grafici e convalide intatti;
- connettori standard;
- **riserva vera**: lo stesso motore gira ancora sul PC con il backend COM;
- l'adattatore rende il collaudo della logica piu' veloce, perche' non serve Excel.

**Contro**:
- **due componenti di esecuzione**: prompt con code interpreter e Office Scripts;
- il motore lo esegue un modello. L'effetto e' a prova di guasto, cioe' senza esito verificato non si scrive. Pero'
  un cambio di modello da parte di Microsoft puo' fermare il processo: allora serve la riserva sul PC;
- limiti da misurare: 100 secondi, un file in ingresso, "gli input non possono contenere istruzioni";
- D-11 cade per il prompt del motore, e D-10 va riscritta (15.6).

**Impegno**: 30-42 giorni (6-8 settimane). Dopo la CS-1, circa 5-7 settimane: Operatore e flussi in parte ci sono gia'.

### V3. Python anche per scrivere: XML del file e sostituzione

**Come**: come la V2, ma niente Office Scripts.
- Il codice del motore e l'output di A1 entrano nel registro con il connettore Excel Online ("Add a row" in una
  tabella nascosta).
- Il prompt riceve il registro, lo modifica direttamente nell'XML (15.3) e lo restituisce come file.
- Il flusso sostituisce il file in SharePoint.

**Pro**: un solo linguaggio, nessun TypeScript.

**Contro**:
- **nessun ricalcolo**: niente controllo degli errori di formula, valori in cache vecchi fino all'apertura in Excel;
  il PDF fatto subito dopo potrebbe mostrare numeri vecchi;
- **il file intero viene sostituito**: se qualcuno lo sta modificando sul web, le sue modifiche si perdono;
- dopo "Add a row" il connettore puo' tenere il file **bloccato fino a 6 minuti**, e la sostituzione fallisce;
- il compilatore XML va scritto e collaudato contro Excel su tutto il template.

**Impegno**: 32-46 giorni, con rischi che restano aperti. **Sconsigliata**.

### Una tappa intermedia possibile: CS-1b

Con l'esecutore della V2 gia' fatto, il PC esecutore della CS-1 puo' **smettere di usare Excel**:
- riceve l'istantanea JSON in `In_arrivo`;
- calcola in Python;
- restituisce le operazioni, che il flusso applica nel cloud.

Spariscono i conflitti di sincronizzazione del registro (K7a) e la fragilita' di Excel via COM. Resta Python sul PC.
La CS-2 poi sposta solo il punto in cui gira il Python: dal PC al code interpreter.

## 15.5 Il cancello nelle tre varianti

| Livello | V1 | V2 | V3 |
|---|---|---|---|
| Regole di metodo e di integrita' | TypeScript, deterministico | Python eseguito dal modello, **verificato**: impronta del motore nell'esito, codice e log archiviati | come V2 |
| Integrita' prima della scrittura | lo stesso script | **Office Script** deterministico: lista bianca, righe validate intoccabili, ricalcolo, errori, valori di controllo | Python, senza ricalcolo |
| Se qualcosa non va | fermo | **fermo a prova di guasto**: senza esito verificato non si scrive | file non sostituito |
| Validazione umana | invariata | invariata | invariata |

La V2 non ha il gate "codice che nessun modello puo' saltare" di oggi, ma ha la proprieta' che conta: **nessuna
scrittura senza un esito prodotto dal motore vero**.

Il rischio residuo e' un modello che inventa un esito con l'impronta giusta: dovrebbe calcolare l'impronta del codice e
fabbricare operazioni coerenti, e non ha motivo di farlo. Va scritto in `controlli_e_model_risk.md`.

## 15.6 Costi, licenze e vincoli architetturali

| Tema | V1 | V2 | V3 |
|---|---|---|---|
| Componenti in esercizio | Copilot Studio, agent flow, Office Scripts, SharePoint | in piu' il prompt con code interpreter | Copilot Studio, agent flow, prompt con code interpreter, connettore Excel Online, SharePoint |
| Linguaggi da mantenere | TypeScript (regole e accesso), Python (collaudo, template) | Python (regole), poco TypeScript (esecutore) | Python |
| Connettori | standard | standard | standard |
| Costi a consumo | nessuno | nessuno per gli utenti Microsoft 365 Copilot (prompt e agent flow "No charge"), **da confermare con l'IT** | come V2 |
| Impostazioni del tenant necessarie | Office Scripts attivi | Office Scripts **e** code interpreter attivi nell'ambiente (gia' attivo: T1.2) | code interpreter |
| Funzioni in anteprima nel percorso | nessuna | il code interpreter nei prompt e' documentato senza "anteprima"; quello sui file strutturati nella chat lo e' (non serve) | come V2 |
| Decisioni da rivedere | D-02 (niente Office Scripts), D-10 | D-02, D-10 ("scrive solo codice deterministico, dopo il controllo dell'impronta del motore"), D-11 (code interpreter nel prompt del motore) | D-02, D-10, D-11 |
| Collaudo | Python come oracolo, confronto con TypeScript su Node.js, prove nel tenant | **invariato per le regole**, piu' l'adattatore e le prove di accettazione nel tenant | invariato per le regole, piu' il compilatore XML contro Excel |
| Riserva se il cloud si ferma | il Python di oggi sul PC (le regole vanno tenute allineate a mano) | **lo stesso motore sul PC**, con il backend COM | come V2 |
| Impegno | 8-11 settimane | **6-8 settimane** (5-7 dopo la CS-1) | 6-9 settimane, con rischi aperti |

## 15.7 Raccomandazione e percorso dopo la CS-1

**Obiettivo: la V2.** Le ragioni:
- e' l'unica che toglie il PC senza riscrivere le regole e senza rinunciare al vero Excel;
- l'IA nel percorso fa solo da esecutore del nostro codice, ed e' verificata.

**Percorso a tappe**, ognuna utilizzabile da sola:

| Tappa | Che cosa | Serve anche se ci si ferma qui |
|---|---|---|
| 0 | CS-1 (14.4) con le prove di `Prove_CS1.md` | si' |
| 1 | **Adattatore del registro** nel motore (istantanea e operazioni, piu' il backend COM di oggi) | collaudo della logica senza Excel, piu' veloce |
| 2 | **Prova K8** (Office Scripts nel tenant) e **esecutore** in Office Script | con la CS-1, il PC non apre piu' Excel (CS-1b) |
| 3 | **Prove K9 e K10**: il motore nel prompt, 10 esecuzioni uguali sotto i 100 secondi; il PDF del report con "Convert file" | decidono la CS-2 |
| 4 | **CS-2 / V2**: argomenti e flussi per ogni comando, PDF, schede, raccolta RSS; D-02, D-10 e D-11 riscritte | obiettivo dell'utente |

**Se le prove vanno male**:

| Esito | Che cosa si fa |
|---|---|
| K8 fallisce (Office Scripts spenti e non attivabili) | niente V1 ne' V2. Resta la CS-1. La V3 si considera solo se l'IT non ammette il PC esecutore, sapendo dei suoi rischi |
| K9 fallisce (il modello non esegue il motore in modo affidabile, o i 100 secondi non bastano) | V1, se l'obiettivo "niente PC" resta fermo; altrimenti CS-1b |
| K10 fallisce (PDF non fedele) | il PDF lo fa a mano chi apre il report in Excel per il web e lo stampa in PDF. E' un gesto, non un blocco |

## 15.8 Le prove nel tenant per la CS-2

| Prova | Che cosa verifica | Come, in breve | Superata se |
|---|---|---|---|
| **K8** Office Scripts | che esistano e siano lanciabili da un agent flow; tempi | uno script `.osts` in una library SharePoint che legge una tabella del registro di prova, aggiunge 50 righe con formule, ricalcola, cerca errori e restituisce un JSON; "Run script from SharePoint library" da un agent flow | gira; meno di 30 secondi; formule e grafici intatti; nessun errore del lucchetto |
| **K9** motore nel prompt | che il code interpreter esegua il nostro codice dal foglio `_Scambio` e restituisca il file | prompt con il registro di prova come file; istruzioni: leggi `_Scambio`, calcola lo SHA-256, esegui, restituisci `esito.json`; **10 esecuzioni** | 10 su 10 con lo stesso esito e la stessa impronta; meno di 100 secondi; codice e log restituiti; nessun rifiuto per "istruzioni negli input" |
| **K10** PDF | fedelta' del PDF del report | copia del registro, fogli non del report nascosti da uno script, "Convert file" in PDF | stessa impaginazione del PDF fatto da Excel desktop (pagine, altezze, grafici) |
| **K13** concorrenza | lucchetto e coautoraggio | registro aperto sul web da una persona mentre l'esecutore scrive | nessuna perdita di dati; il lucchetto ferma la seconda scrittura |

Le prove K6, K4, K11 e K12 della CS-1 valgono anche qui. Le domande D1 e D2 (`Prove_CS1.md`) vanno completate con due
punti:
- i prompt con code interpreter negli agent flow non consumano crediti per gli utenti Microsoft 365 Copilot?
- gli Office Scripts restano attivi in futuro?

## Fonti (consultate l'11/10/2026)

- Microsoft Learn, Copilot Studio:
  - [Use code interpreter in a prompt](https://learn.microsoft.com/en-us/microsoft-copilot-studio/code-interpreter-for-prompts) (30/09/2026): file in uscita, Excel in ingresso e in uscita, un solo file per prompt, conteggio come "text and generative AI tools (premium)".
  - [Code interpreter prompts examples](https://learn.microsoft.com/en-us/microsoft-copilot-studio/code-interpreter-prompts-examples): "Run a prompt" in un agent flow; uscite `artifacts` con `base64Content`.
  - [Code interpreter for developers](https://learn.microsoft.com/en-us/power-apps/developer/data-platform/code-interpreter): la risposta contiene `code`, `logs`, `files`, `signature`.
  - [Add inputs to your prompt](https://learn.microsoft.com/en-us/microsoft-copilot-studio/add-inputs-prompt): tipi di file, 25 MB, **100 secondi**, input senza istruzioni, niente file per i prompt usati come strumento diretto dell'agente.
  - [Use code interpreter to analyze structured data (preview)](https://learn.microsoft.com/en-us/microsoft-copilot-studio/knowledge-code-interpreter-structured-data): 16 MB, 10 file, SharePoint come knowledge.
  - [Agent flows FAQ](https://learn.microsoft.com/en-us/microsoft-copilot-studio/flows-faqs): connettori premium ammessi negli agent flow, fatturazione in Copilot Studio.
  - [Pass files to agent flows, connectors, and tools](https://learn.microsoft.com/en-us/microsoft-copilot-studio/guidance/pass-files-to-connectors): file come `contentBytes` e `name`.
  - [Billing rates and management](https://learn.microsoft.com/en-us/microsoft-copilot-studio/requirements-messages-management): "No charge" per gli utenti Microsoft 365 Copilot.
- Microsoft Learn, connettori:
  - [Excel Online (Business)](https://learn.microsoft.com/en-us/connectors/excelonlinebusiness/): 25 MB, blocco fino a 6 minuti, 100 chiamate al minuto, righe duplicate per i tentativi, "Run script from SharePoint library".
  - [OneDrive for Business](https://learn.microsoft.com/en-us/connectors/onedriveforbusiness/): "Convert file", "Extract archive to folder" (50 MB, 100 file), nessuna creazione di zip.
- Microsoft Learn, Office Scripts:
  - [Platform limits](https://learn.microsoft.com/en-us/office/dev/scripts/testing/platform-limits): 5 MB, 120 secondi, 1.600 chiamate al giorno, nessuna chiamata esterna, controlli dell'amministratore.
  - [Troubleshoot Office Scripts in Power Automate](https://learn.microsoft.com/en-us/office/dev/scripts/testing/power-automate-troubleshooting): `refreshAllDataConnections` aggiorna solo Power BI; niente `Crypto` ne' `TextEncoder`.
- Altre fonti:
  - [Power Query data sources in Excel versions](https://support.microsoft.com/en-us/Excel/power-query-data-sources-in-excel-versions): aggiornamento in Excel per il web da file e liste SharePoint, manuale.
  - [Copilot Studio: .pptx/.xlsx con il code interpreter](https://dev.classmethod.jp/en/articles/copilot-studio-native-pptx-excel/) (23/06/2026): openpyxl disponibile, 1-1,5 minuti per generare un file.
