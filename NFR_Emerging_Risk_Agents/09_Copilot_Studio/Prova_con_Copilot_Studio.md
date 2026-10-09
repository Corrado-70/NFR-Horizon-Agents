# Prova di Copilot Studio: A1 e il precontrollo, in due modi di eseguire il codice

Prova K0 del piano 10 (`Analisi_Architettura/Archivio/10`, 10.15; TODO, AU4), estesa alla domanda del 05/10: in
Copilot Studio funziona? Con quali limiti? Conviene attivare l'opzione del codice?
Si misura su **A1**, il compito piu' pesante:
- legge molti documenti;
- risponde con un JSON di 40-60 KB;
- e' l'agente che oggi costa piu' giri.

Si prova anche il **precontrollo** eseguito dentro l'agente. Se funziona, A1 consegna un output gia'
controllato e sparisce l'andata e ritorno con il PC.

Si usa lo stesso input della prova senza Copilot Studio (`04_Riferimenti/Prove/Prova_senza_Copilot_Studio.md`,
parte 2): `C:\NFR_Prova\Archivio\Input_A1_2026Q4.txt`. Cosi' i risultati si confrontano con A1 in Agent
Builder, a parita' di tutto. Copilot Studio in questa prova produce solo file: nel registro scrive solo
lo script, dopo i controlli (D-10).

## Le due opzioni del codice

Verificate su Microsoft Learn il 05/10/2026 (fonti in fondo). Da settembre 2026 Copilot Studio ha due
"harness", cioe' due motori diversi per gli agenti:
- la **esperienza standard**: gli agenti classici, simili a quelli di Agent Builder;
- la **nuova esperienza**, basata sul "GitHub Copilot harness": interruttore **New experience** nella
  home.

Un agente nasce in una delle due e non si sposta nell'altra.

| | Opzione 1: esperienza standard, **Code interpreter** | Opzione 2: nuova esperienza, **skill nel sandbox** |
|---|---|---|
| Dove si accende | Settings -> Generative AI -> File processing capabilities -> **Code interpreter**. Prima l'amministratore lo deve abilitare nel Power Platform admin center: **spento di default** | non c'e' un interruttore: il sandbox (Python 3.12, circa 99 librerie, niente rete) e' parte della nuova esperienza; la skill si carica dalla scheda Build |
| Quale codice gira | quello che il modello scrive a ogni richiesta. Il nostro script gira solo se l'utente lo **allega** in chat e il modello lo esegue cosi' com'e' | lo script della skill, **sempre lo stesso**: e' il caso d'uso dichiarato da Microsoft ("pre-written script") |
| Costi | per chi ha la licenza Microsoft 365 Copilot, uso interno autenticato: **"No charge"**, anche per gli strumenti premium | **Copilot Credits dal primo minuto**: costruire, provare nel riquadro di prova e usare. Serve capacita' assegnata all'ambiente; senza, l'agente non risponde |
| Stato | il code interpreter sui file strutturati e' in anteprima | file creati dall'agente in anteprima |
| Limiti noti | file fino a 16 MB, fino a 10 per messaggio; richiede l'autenticazione Microsoft | file creati fino a 10 MB; allegati e file conservati 28 giorni; nessuna rete, nessun pacchetto installabile; allegati .txt, .md, .csv (non .json ne' .py) |

Probabilmente "attivare l'opzione code" vuol dire l'interruttore **Code interpreter** dell'opzione 1.
La prova le copre entrambe, perche' fanno cose diverse:
- con l'opzione 1 il modello scrive codice nuovo ogni volta: non e' un controllo ripetibile (piano 10,
  10.10), salvo eseguire il nostro file allegato;
- con l'opzione 2 gira il nostro script, ma si paga a consumo.

**I file da caricare** sono in `09_Copilot_Studio\Da_caricare\`:

| File | Opzione | Cos'e' |
|---|---|---|
| `precontrollo-nfr.zip` | 2 | la skill: `SKILL.md` (le istruzioni) e `scripts/precontrollo_nfr.py` |
| `precontrollo-nfr_senza_cartella.zip` | 2 | la stessa, con `SKILL.md` alla radice dello zip: da usare se la prima viene rifiutata |
| `precontrollo_nfr.txt` | 1 | lo stesso script, in .txt perche' i .py non si allegano |
| `Messaggi_da_incollare.txt` | 1 e 2 | i messaggi di ogni test |

Lo script e' lo stesso codice del comando `precontrollo` sul PC: stessi controlli, stesso messaggio,
stessa **impronta** dell'output di A1 (verificato dal collaudo). Se l'impronta riportata dall'agente e'
uguale a quella che il PC calcola sul file scaricato, l'agente ha davvero eseguito lo script sul file
che ha consegnato.

## B0. Prima di cominciare: domande all'IT (10 minuti)

1. **Ambiente**: in quale ambiente Power Platform ho il ruolo di autore di Copilot Studio? Meglio un
   ambiente di prova o sviluppatore, non quello di produzione.
2. **Opzione 1**: il code interpreter di Copilot Studio e' abilitato nel Power Platform admin center
   per quell'ambiente? E' spento di default. Le capability di Agent Builder risultavano non abilitate
   nel tenant (01/10): probabilmente serve una richiesta.
3. **Opzione 2**:
   - nella home di Copilot Studio si vede l'interruttore **New experience**?
   - l'ambiente ha Copilot Credits assegnati, o un contatore a consumo?
   - si puo' fissare un tetto mensile per l'agente di prova? (Licensing -> Copilot Studio -> Manage
     Agents)
4. **Modelli**: quali modelli si possono scegliere? I modelli di ragionamento sono soprattutto nella
   nuova esperienza; i modelli Anthropic sono spenti di default nella UE.
5. **Dati**: A1 legge `Analisi_Interne` (documenti della Banca), come in Agent Builder. Copilot Studio
   conserva le trascrizioni delle conversazioni, e su questo manca ancora il parere della compliance
   (V-N, estensione di D-24). Se il parere non c'e', fare la prova con le sole `Analisi_Esterne`,
   `News_Inbox` e i siti, e scriverlo nella tabella. `Input_A1_2026Q4.txt` del registro di prova non
   contiene rischi della Banca: la baseline e' vuota.

Se l'opzione 1 non e' abilitata e l'opzione 2 non ha crediti, si fanno solo i test T1.1 e B3: dicono
gia' se A1 regge in Copilot Studio senza codice.

D-11 (agenti senza capability) resta in vigore per gli agenti in esercizio. Il codice si accende solo
sugli agenti di prova; adottarlo sarebbe una decisione nuova.

## B1. Opzione 1: esperienza standard con il Code interpreter

### Costruzione dell'agente "NFR A1 prova standard" (20 minuti)

Le etichette sono quelle della documentazione Microsoft in inglese; nell'interfaccia in italiano
possono essere tradotte. Se una voce non c'e', annotarlo: e' un risultato della prova.

1. Aprire `https://copilotstudio.microsoft.com` e scegliere l'ambiente (in alto a destra).
2. Nella home **spegnere New experience** (oppure **Other ways to build**), poi **Create** -> **New
   agent**. Passare alla scheda **Configure**, non alla descrizione in linguaggio naturale, che
   riscriverebbe le istruzioni.
3. Compilare:
   - Name: `NFR A1 prova standard`;
   - Description: `Prova K0: A1 Horizon Scanner in Copilot Studio`;
   - Instructions: il file intero `02_Agenti\A1_Horizon_Scanner.md`, 7.963 caratteri su 8.000.
4. Knowledge, come A1 in Agent Builder (guida, 0.2):
   - SharePoint: le cartelle `Analisi_Interne`, `Analisi_Esterne`, `News_Inbox`;
   - Public websites: i 4 siti, cioe' Banca d'Italia vigilanza, CONSOB, Garante privacy, Protezione
     Civile.
5. **Settings -> Generative AI**:
   - orchestrazione generativa (predefinita);
   - modello: il piu' capace disponibile, un modello di ragionamento se c'e'; annotarne il nome;
   - **Use general knowledge** e **Web search** spenti, come "Search all websites" in Agent Builder;
   - **File processing capabilities**: **File uploads** acceso, **Code interpreter** acceso;
   - **Save**.
6. **Settings -> Security -> Authentication**: "Authenticate with Microsoft", quella predefinita. Il
   code interpreter la richiede.

### Test (il riquadro **Test** a destra; una conversazione nuova per T1.1 e per T1.2)

| Test | Allegati | Messaggio | Cosa annotare |
|---|---|---|---|
| **T1.1** A1 senza codice | `Input_A1_2026Q4.txt` | `Esegui il ciclo` | Risponde con il JSON intero o si tronca? Tempo e numero di rischi. Copiare la risposta in `C:\NFR_Prova\pacchetto\07_Senza_Studio\A1_CS1_testo.json` e lanciare `python esegui_ciclo_locale.py precontrollo --payload A1_CS1_testo.json`: prima riga e impronta. "non e' un JSON valido" = risposta troncata o con testo attorno |
| **T1.2** con lo script | `Input_A1_2026Q4.txt` e `Da_caricare\precontrollo_nfr.txt` | testo T1.2 di `Messaggi_da_incollare.txt` | Lo script e' partito? Quanti giri? Le prime due righe riportate. Il file `A1_2026Q4.json` e' scaricabile? Salvarlo come `A1_CS1_codice.json` e lanciare il precontrollo sul PC: **stessa prima riga e stessa impronta** di quelle riportate dall'agente? |
| **T1.3** ripetibilita' | — (stessa chat) | testo T1.3 | Stesse due righe di T1.2? |
| **T1.4** richiesta da rifiutare | — (stessa chat) | testo T1.4 | Rifiuta? In ogni caso non deve dichiarare un esito che lo script non ha stampato |

## B2. Opzione 2: nuova esperienza con la skill

**Al 09/10 in Banca la nuova esperienza non c'e': B2 non si puo' fare.** Resta descritta per quando l'IT la rendesse
disponibile.

Ogni minuto di costruzione e di prova consuma crediti: tenere aperta la scheda **Monitor** e annotare
i crediti all'inizio e alla fine.

### Costruzione dell'agente "NFR A1 prova skill" (20 minuti)

1. Nella home **accendere New experience** e creare un agente nuovo. Se chiede una descrizione,
   scrivere solo `Agente di prova NFR`: le istruzioni si sostituiscono al punto 2.
2. Scheda **Build**:
   - nome `NFR A1 prova skill`;
   - **Instructions**: cancellare il testo generato e incollare il file intero
     `02_Agenti\A1_Horizon_Scanner.md`.
3. **Knowledge**: le stesse fonti del punto 4 di B1.
4. **Model**: il modello di ragionamento piu' capace disponibile; annotarne il nome.
5. **Skills** -> **Add skill** -> **Upload a skill** -> `Da_caricare\precontrollo-nfr.zip`.
   - Se viene rifiutato, provare `precontrollo-nfr_senza_cartella.zip`.
   - Se vengono rifiutati entrambi, annotare il messaggio: la prova dell'opzione 2 finisce qui.
6. **Save**.

### Test (scheda **Preview**, conversazione nuova)

| Test | Allegati | Messaggio | Cosa annotare |
|---|---|---|---|
| **T2.0** A1 senza skill (facoltativo, costa crediti) | `Input_A1_2026Q4.txt` | `Esegui il ciclo` | Come T1.1, file `A1_CS2_testo.json`. L'agente puo' usare la skill anche se non gliela si chiede: annotarlo |
| **T2.1** con la skill | `Input_A1_2026Q4.txt` | testo T2.1 | Come T1.2, file `A1_CS2_skill.json`: la skill e' stata usata (la si vede nei passaggi della risposta)? Quanti giri? Stessa prima riga e stessa impronta del PC? |
| **T2.2** ripetibilita' | — | testo T1.3 / T2.2 | Stesse due righe? |
| **T2.3** richiesta da rifiutare | — | testo T1.4 / T2.3 | Come T1.4 |
| **Crediti** | | | crediti consumati da costruzione e test (scheda Monitor) |

## B3. Facoltativo: Teams e salvataggio in SharePoint (K0 originale)

Solo sull'opzione che ha funzionato meglio.

1. **Pubblicazione in Teams** (V-H):
   - esperienza standard: **Channels** -> **Teams and Microsoft 365 Copilot** -> aggiungere il
     canale, poi **Publish**;
   - nuova esperienza: **Publish** e il canale Teams.

   Aprire l'agente in Teams e ripetere T1.2 o T2.1: allegati, codice e file scaricabile funzionano
   anche li'?
2. **Agent flow che salva il JSON in SharePoint** (V-J, esperienza standard):
   1. In SharePoint, creare la cartella di prova `Archivio_Cicli\Prova_K0`.
   2. Nell'agente: **Tools** -> **Add a tool** -> **New agent flow**.
      - Trigger **When an agent calls the flow** con due input di testo, `nome_file` e `contenuto`.
      - Azione SharePoint **Create file**: il sito NFR; Folder Path `/Archivio_Cicli/Prova_K0`.
        **File Name** e **File Content** non si scrivono a mano: si sceglie, dal contenuto dinamico
        (icona del fulmine, oppure `/`), la **variabile del flusso** `nome_file` e la variabile
        `contenuto`, cioe' gli input del trigger. Se si scrive il nome come testo, il flusso usa quelle
        parole e non il valore passato dall'agente. Questo passo mancava fino al 09/10.
      - Azione **Respond to the agent** con un output di testo `esito` = `salvato`.
   3. Salvare e pubblicare il flusso con il nome `Salva_JSON`.
   4. Nell'agente, scheda **Tools**, aprire lo strumento `Salva_JSON`:
      - **Description**: e' cio' che l'agente legge per decidere quando usarlo. Una descrizione generica
        lo fa partire anche senza richiesta. Incollare:

        `Salva in SharePoint il JSON finale di A1. Usalo SOLO quando l'utente scrive il comando Scrivi_JSON; in ogni altro caso non usarlo, nemmeno se sembra utile: non dopo il ciclo, non dopo il precontrollo, non per altri file. nome_file: il nome del file indicato nel comando. contenuto: il JSON intero del file A1_2026Q4.json consegnato, senza modifiche e senza testo attorno.`
      - **Inputs**: `nome_file` e `contenuto` li riempie l'agente. Come descrizione di ciascuno, la frase
        corrispondente della descrizione qui sopra.
      - **Save**. Poi **ripubblicare l'agente**: Teams usa solo la versione pubblicata.
   5. Nella chat di T1.2, prima la prova negativa: scrivere `Salva il lavoro`. L'agente **non** deve
      chiamare lo strumento: niente esecuzione nella cronologia del flusso, niente file nuovo in
      SharePoint.
   6. Poi il testo B3 di `Messaggi_da_incollare.txt`, che comincia con il comando `Scrivi_JSON`.
   7. Sul PC, dalla cartella sincronizzata, lanciare il precontrollo su
      `Archivio_Cicli\Prova_K0\A1_2026Q4_CS.json`. **Stessa impronta del file scaricato** = un JSON
      di 40-60 KB passa intero per un flusso.

   Con il trigger "When an agent calls the flow" e utenti con licenza Microsoft 365 Copilot, il flusso
   non consuma crediti.

## B4. Alla fine

- Scollegare i canali pubblicati e, se non si prosegue, eliminare i due agenti.
- Se l'IT ha acceso il code interpreter solo per la prova, chiedere di rispegnerlo, oppure lasciarlo
  acceso sull'ambiente di prova.
- Mandare a chi mantiene il pacchetto la tabella qui sotto. Se le regole della Banca lo consentono,
  anche i file `A1_CS*.json`, le prime righe riportate dagli agenti e un'immagine dei passaggi della
  risposta di T1.2 e T2.1.

## Tabella dei risultati

Prima tornata del 09/10, parziale: alcuni file erano disallineati (trimestre e tassonomia vecchi, altri file sulla
tassonomia nuova del 07/10). Valgono le risposte "funziona / non funziona"; numero di rischi, punti del precontrollo
e qualita' di A1 vanno rimisurati (vedi "Prima di ripetere").

| Voce | Opzione 1 (standard + Code interpreter) | Opzione 2 (nuova esperienza + skill) |
|---|---|---|
| B0: ambiente; code interpreter abilitato; New experience visibile; crediti; modelli disponibili | 09/10: code interpreter disponibile (T1.2 funziona) | 09/10: **nuova esperienza non disponibile in Banca**, prova non fattibile |
| Costruzione: istruzioni intere accettate (7.963 caratteri)? knowledge aggiunta? skill caricata (quale zip)? modello scelto | 09/10: agente costruito; modello da annotare | — |
| T1.1 / T2.0, senza codice: JSON intero o troncato (caratteri), numero di rischi, tempo; precontrollo sul PC (prima riga, impronta) | 09/10: **funziona**; caratteri, rischi e tempo da rimisurare sui file allineati | — |
| T1.2 / T2.1, con lo script: partito? giri; prime due righe riportate; file scaricabile? | 09/10: **funziona**; giri e righe da annotare | — |
| Precontrollo sul PC del file scaricato: stessa prima riga? **stessa impronta**? | da annotare: e' la prova che lo script e' girato davvero | — |
| T1.3 / T2.2, ripetibilita': stesse righe? | 09/10: **una volta in errore**; da annotare il testo dell'errore e, quando gira, se le righe sono uguali | — |
| T1.4 / T2.3, richiesta da rifiutare: cosa ha fatto | 09/10: **rifiutata** (esito giusto) | — |
| Crediti consumati e tempo totale | (nessun credito atteso) | — |
| B3: Teams (codice, allegati, file) | 09/10: pubblicato, visibile in Teams e in Microsoft 365 Copilot; **spesso risponde con errori**, 1-2 volte ha funzionato | — |
| B3: agent flow, impronta del file in SharePoint uguale? | 09/10: prima il file finiva **nel OneDrive personale**; poi corretto dall'utente: File Name e File Content vanno impostati con le variabili del flusso, e lo strumento deve avere una descrizione che lo limita al comando (B3, punti 2 e 4). Ora **l'agente salva nella cartella SharePoint** a comando, e il JSON arriva intero: **impronta del file in SharePoint uguale a quella del file scaricato** (09/10). B3 superato: un JSON di A1 passa intero per un flusso |
| B3: prova negativa, lo strumento parte solo con `Scrivi_JSON`? | da fare | — | — |
| Qualita' di A1 rispetto ad Agent Builder (parte 2 dell'altra prova): numero di rischi, testi, punti del precontrollo al primo giro | da rimisurare sui file allineati | — |

### Prima di ripetere: un solo pacchetto per tutti i file

- Registro di prova e `Input_A1_2026Q4.txt` rifatti con il pacchetto dell'08/10 sera: in `C:\NFR_Prova`, parte 2.1-2.2
  dell'altra prova. Struttura 2026-10-09, tassonomia interna D-74, registro unico D-79.
- Istruzioni dell'agente = `02_Agenti\A1_Horizon_Scanner.md` dello stesso pacchetto, reincollate.
- Script allegato = `Da_caricare\precontrollo_nfr.txt` dello stesso pacchetto: quello dell'08/10 contiene la regola
  del radar. Lo script del 05/10 non la contiene e su un output nuovo darebbe esiti diversi dal PC.
- Il precontrollo sul PC si lancia da `C:\NFR_Prova\pacchetto\07_Senza_Studio`, cioe' con lo stesso codice.

### B3: perche' Teams da' errori e il flusso salva nel OneDrive (cause probabili, da verificare)

Il salvataggio nel OneDrive e' stato risolto dall'utente il 09/10, con le variabili del flusso in Create file e la
descrizione dello strumento limitata al comando `Scrivi_JSON` (B3, punti 2 e 4). Il punto 4 qui sotto resta come
guida se si ripresenta.

Nel riquadro di prova di Copilot Studio queste cose non si vedono: Teams aggiunge limiti suoi.

1. **Messaggio troppo grande.** Teams accetta da un agente messaggi fino a circa 100 KB contati in UTF-16, cioe'
   circa due byte per carattere; Microsoft consiglia di restare sotto gli 80 KB. Un JSON di A1 di 40-60 KB scritto
   nel messaggio diventa 80-120 KB: oltre il limite, e l'agente risponde con un errore.

   Le volte che ha funzionato, probabilmente l'output era piu' corto, oppure l'agente ha consegnato solo il file.

   In Teams l'agente non deve mai scrivere il JSON nel messaggio, solo il file e le due righe dell'esito: va
   per questo la richiesta T1.2 di `Messaggi_da_incollare.txt` dal 09/10 dice `Non scrivere il JSON nel messaggio:
   solo il file e le due righe.`
2. **Sessione del code interpreter scaduta.** Il calcolo e' temporaneo e i compiti lunghi possono andare in timeout
   (FAQ di Microsoft). Probabilmente spiega anche l'errore di T1.3: se nel turno dopo il file `A1_2026Q4.json` non c'e'
   piu', lo script non trova il file. Lo script in se' da' sempre lo stesso risultato sullo stesso file. Conta il
   testo dell'errore: "file non trovato" vuol dire sessione scaduta, non un problema di ripetibilita'.
3. **Il codice dell'errore.** Ogni errore in Teams ha un codice: annotarlo, insieme all'ora. Per esempio:
   - `OutgoingMessageSizeTooBig`: messaggio troppo grande, punto 1;
   - `ConsentNotProvidedByUser`: manca il consenso alla connessione, si conferma la scheda di accesso;
   - `FlowActionTimedOut`: il flusso ha superato i 100 secondi;
   - `FlowActionException` o `FlowActionBadRequest`: errore nel flusso, si guarda la cronologia delle esecuzioni.

   I codici si leggono nella pagina "Understand error codes" di Learn.
4. **Il file nel OneDrive non lo ha scritto per forza il flusso.** Se il flusso lanciato da solo scrive in
   SharePoint, l'azione Create file e' giusta: un'azione SharePoint non scrive in un OneDrive. Probabilmente in
   Teams il flusso non e' partito, e il file nel OneDrive e' quello consegnato dall'agente nella chat: Teams e
   Microsoft 365 Copilot conservano nel OneDrive di chi chatta i file della conversazione. Per verificarlo:
   1. in Power Automate, cronologia delle esecuzioni di `Salva_JSON`: c'e' un'esecuzione all'ora della prova in
      Teams? Se c'e', con quale esito, e che cosa ha restituito Create file?
   2. il file nel OneDrive: in quale cartella, con quale nome (`A1_2026Q4_CS.json` o `A1_2026Q4.json`) e a che ora?
   3. in Copilot Studio, scheda Activity della conversazione di Teams: l'agente ha chiamato lo strumento?
   4. l'agente e' stato ripubblicato **dopo** aver aggiunto lo strumento? Teams usa solo la versione pubblicata.

   Se non c'e' nessuna esecuzione, l'agente non ha chiamato lo strumento (punto 4.4, oppure la risposta "salvato" e'
   inventata: vale la trappola dell'esito riferito). Se c'e', l'impronta del file in SharePoint dice se un JSON di
   40-60 KB passa intero come testo. Il dubbio e' fondato: il modello deve riscriverlo tutto come parametro dello
   strumento, e il flusso ha 100 secondi.

## Come si leggono i risultati

- **L'opzione 2 funziona** se:
  - la skill si carica;
  - l'impronta coincide;
  - T2.2 ripete le stesse righe;
  - i crediti sono sostenibili.

  In questo caso A1 consegna un output gia' passato dal precontrollo vero, e per il PC resta solo la
  scrittura, che rifa' comunque tutti i controlli. Si riaprono la decisione A-15 (strada) e D-11
  (capability) con un dato in mano.
- **Funziona solo l'opzione 1** (script allegato eseguito, impronta che coincide): stesso vantaggio
  senza costi, con un allegato in piu' a ogni ciclo e un modello che potrebbe non eseguire il file
  cosi' com'e'. Lo dice T1.3.
- **Il codice non c'e' o non e' affidabile**: Copilot Studio vale solo per l'orchestrazione
  (variante CS-1 del piano 10) oppure si resta alla strada A. In tutti i casi il precontrollo e la
  scrittura restano sul PC, come oggi.
- **T1.1 si tronca**: A1 in Copilot Studio deve consegnare il JSON come file (code interpreter o file
  creato), oppure dividersi in due agenti (V-K).

## Fonti (Microsoft Learn, consultate il 05/10/2026)

- [Harnesses in Copilot Studio](https://learn.microsoft.com/en-us/microsoft-copilot-studio/harnesses-overview) e [Compare Copilot Studio agent harnesses](https://learn.microsoft.com/en-us/microsoft-copilot-studio/guidance/choose-harness) (30/09/2026): standard e GitHub Copilot harness, sandbox Bash, modelli di ragionamento solo nel secondo.
- [Access standard harness agents and agent flows](https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/switch-experiences): interruttore New experience, "Other ways to build".
- [Skills overview](https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/skills-overview) e [Add an existing skill](https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/skills-add-existing): SKILL.md o .zip con script.
- [Copilot Studio agent sandbox](https://microsoft.github.io/mcscatblog/posts/copilot-studio-agent-sandbox/) (blog del CAT Microsoft, 20/07/2026, agg. 11/08): Python 3.12.9, 99 librerie, niente rete, script delle skill.
- [Files the agent creates](https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/created-files-overview) e [Attach files to a conversation](https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/attachments-overview): 10 MB, 16 MiB, 28 giorni, tipi di file.
- [Overview of usage-based billing](https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/billing-credit-overview) (10/09/2026): crediti dalla costruzione. [Billing rates and management](https://learn.microsoft.com/en-us/microsoft-copilot-studio/requirements-messages-management): "No charge" per gli utenti Microsoft 365 Copilot nell'esperienza standard.
- Consultate il 09/10/2026 per B3:
  - [Understand error codes](https://learn.microsoft.com/en-us/troubleshoot/power-platform/copilot-studio/authoring/error-codes) (04/06/2026): `OutgoingMessageSizeTooBig`, `ConsentNotProvidedByUser`, agent flow oltre i 100 secondi;
  - [Format your bot messages](https://learn.microsoft.com/en-us/microsoftteams/platform/bots/how-to/format-your-bot-messages): messaggi in Teams fino a circa 100 KB in UTF-16, consigliati 80 KB.
- [Use code interpreter to analyze structured data](https://learn.microsoft.com/en-us/microsoft-copilot-studio/knowledge-code-interpreter-structured-data) (04/08/2026), [Code interpreter in a prompt](https://learn.microsoft.com/en-us/microsoft-copilot-studio/code-interpreter-for-prompts) (30/09/2026), [FAQ for code interpreter](https://learn.microsoft.com/en-us/microsoft-copilot-studio/faq-code-interpreter): interruttori, autenticazione, abilitazione dell'amministratore spenta di default.
