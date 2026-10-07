# Analisi dell'architettura — sintesi e indice

Data: 23/09/2026. Oggetto: il sistema di agenti NFR Emerging Risk
(`NFR_Emerging_Risk_Agents/`), con suite di collaudo verde e demo rigirata lo
stesso giorno.

## Sintesi in dieci righe

1. L'architettura attuale e' **solida nella governance** (controlli prima della
   scrittura, tracciabilita', validazione umana, collaudo eseguibile) e
   **debole nell'esercizio e nella manutenzione**: copia a mano dei JSON, un PC
   con Python dedicato, workbook usato come database (3.154 formule, 113 nomi),
   template che non aggiorna il registro in uso, generatore monolitico.
2. Con gli **stessi vincoli**, la strada migliore e' **C + D**: separare i dati
   dal report (report alimentato da Power Query, sostituibile) e generare il
   **report trimestrale per il comitato in PowerPoint**. Punteggio 4,00 su 5
   contro 3,15 dell'attuale.
3. **Office Scripts al posto di Python** (A) elimina le installazioni ma fa
   perdere quasi tutto il collaudo automatico: solo se Python e' impossibile.
4. **Agenti piu' piccoli** (B) migliorano la qualita' misurabile ma, senza
   orchestratore, aumentano i passi manuali: solo A1 in due, se serve.
5. **Copilot Studio potrebbe essere gia' coperto dalla licenza Microsoft 365
   Copilot** (Microsoft Learn, 03/08/2026): il blocco puo' essere organizzativo.
   Da chiedere subito all'IT.
6. Se e' abilitabile: **R2, un agente operativo in Teams** con sotto-agenti,
   strumenti "controlla e scrivi" e stato nelle Liste SharePoint (3,90), poi i
   pezzi di **R1 (pipeline pianificata)** che servono (3,65).
7. In ogni caso si conservano kernel, schemi, separazione giudizio/calcolo,
   controlli deterministici, validazione tracciata e collaudo dei contratti.
8. Il rischio piu' grande resta **la qualita' reale degli agenti nel tenant**:
   nessuna architettura lo toglie, lo misura solo un trimestre gia' valutato
   a mano.
9. Per questo la rigenerazione proposta **parte dal report trimestrale** con
   dati inseriti a mano, e procede per **otto fasi con cancelli** (verifiche
   automatiche piu' un si' esplicito di una persona).
10. Ogni fase ha il prompt pronto da dare a Claude Code.

> **Correzione del 24/09 (decisione dell'utente)**: il sistema parte dal
> registro **vuoto**, senza un trimestre gia' valutato a mano. Dove i documenti
> 01, 04, 05 e 06 usano il "trimestre di riferimento" come metro (punto 8 qui
> sopra, fase 0 del documento 5), il metro diventa il **doppio run**
> (`confronta.py --primo-ciclo`) piu' la **validazione umana** del primo
> ciclo, con criteri fissati prima in `DECISIONI.md`. I documenti restano come
> analisi datate del 23/09.

> **Aggiornamento del 25/09 sera**: approvata e applicata la proposta 09 (anteprima
> v3): registro e report in un solo file ridisegnato (D-39, template
> 2026-09-25c) e schede dei rischi in un file a parte scritto dall'agente A6
> dopo la validazione (D-40). I documenti da 01 a 07 hanno in testa
> la corrispondenza fra i fogli di allora e quelli di oggi.

> **26/09**: la scelta del piano 07 (senza Python in esercizio) e l'analisi
> dei processi (trimestrale, settimanale, spot) sono tracciate come voci del
> TODO del pacchetto: AR1, P1-P7, Q1 (`NFR_Emerging_Risk_Agents/TODO_possibili_sviluppi.md`).

> **27/09**: rianalisi di software e architettura orientata all'automazione
> (documento 10, proposta non ancora approvata). Scelte dell'utente: Python
> resta il motore con uno strato di automazione per l'analista (procedura
> guidata a menu, risposte degli agenti prese dagli appunti, lanciatori
> `.cmd`); il piano 07 passa in riserva.

> **28/09**: il documento 10 ha una parte seconda (10.9-10.19), l'opzione
> separata **Copilot Studio**. Esito: si automatizza molto di piu'; Python si
> toglie dall'esercizio solo riscrivendo il motore. La variante consigliata e'
> la **CS-1 ibrida**: Operatore in Teams, agenti che consegnano in
> `In_arrivo`, motore Python invariato in background su un solo PC. Circa due
> terzi del piano 10 sono **comuni alle due strade** (C1-C9, 6-7 giorni) e si
> possono fare subito.

> **28/09, dopo**:
> - Copilot Studio e Power Query sono **disponibili** (D-44, chiude A-05). Se
>   usare Copilot Studio non e' deciso, perche' e' piu' complesso: e' la
>   decisione aperta **A-15**.
> - Registrata **D-43**: Python resta il motore, il piano 07 e' in riserva, AR1
>   e' chiusa.
> - Il TODO del pacchetto e' il **piano unico**: le voci del documento 10 sono
>   AU1-AU6, con un solo ordine di lavoro insieme a P, Q e G.

> **30/09**: documento 11, semplificazione dello scoring e della selezione dei
> rischi di A1 dopo il collaudo del primo ciclo (29/09). Approvata
> dall'utente: Gap_Controlli esce dal modello (resta un dato qualitativo della
> Banca), Velocity facoltativa, esito e da/a calcolati dallo script, KRI da 1 a
> 3 con soglie della Banca, un rischio per meccanismo senza copertura forzata
> degli event type, opzione per superare i rilievi di A5 con motivazione
> (D-49..D-56). Voce S1 del TODO, prima di AU1.

> **02/10**: la validazione si fa in una **griglia**, una riga per rischio,
> KRI, azione e notizia, con le celle gialle gia' compilate con le proposte e
> Score e Margine di Mosca calcolati mentre si scrive (D-67, struttura
> 2026-10-02). I documenti 01, 06, 07, 10 e 11 hanno una nota; nel 10 sono
> corretti i passi della validazione della procedura guidata.

> **02/10 pomeriggio**: schede dei rischi con il perche' di ogni numero (D-68):
> A1 scrive il razionale in parti (il fenomeno in termini di rischio e il
> perche' di ogni valore con i documenti) e l'effetto atteso di azioni e KRI;
> la scheda li mette accanto ai valori, alle azioni e ai KRI. Nota nel
> documento 09.

> **02/10 sera**: meno giri fra A1 e A5 (D-69): A1 riceve in un allegato
> (`Input_A1_<ciclo>.txt`) baseline, controlli di A5 e una guida di scrittura
> con un esempio, e li applica prima di rispondere; il comando `precontrollo`
> controlla l'output di A1 prima di A5 e scrive il messaggio di correzione;
> A1 propone azioni nuove invece di ripetere quelle aperte. Note nei documenti
> 10 (`messaggio_correzione` per A1 gia' fatto) e 11 (giri A1-A5).

> **05/10**: documento 10, sezione 10.20. Copilot Studio ha ora due motori.
> Nella **nuova esperienza** una skill esegue un nostro script sempre uguale,
> e questo supera in parte la conclusione del 28/09 sul code interpreter;
> pero' consuma crediti dalla costruzione. L'**esperienza standard** e'
> gratuita per gli utenti Microsoft 365 Copilot, ma il codice lo scrive il
> modello. Prova K0 estesa (D-70, `09_Copilot_Studio`): il precontrollo dentro
> A1 nelle due opzioni, sullo stesso input della prova della versione senza
> Copilot Studio.

> **06/10**: A5 facoltativo e segnalazioni in validazione (D-71, struttura
> 2026-10-06): lo script ferma solo i difetti di integrita' (schema, C1, C2,
> C7, identificativi dei KRI); C3, le date di C5, coppia e soglie dei KRI e i
> Bloccanti di A5 vanno nella colonna Segnalazioni della griglia e chiedono una
> Motivazione. Il trimestre perde un passo con l'agente (A5) e il giro "rifai
> A1, rifai A5". In Banca Copilot Studio ha solo l'esperienza standard e la
> knowledge SharePoint risulta bloccata (probabile data policy). Note nei
> documenti 10 e 11.

> **07/10**: piano degli agenti nuovi (TODO, "Agenti nuovi") e fase 1: A7
> Assistente del registro risponde in chat sul perche' delle valutazioni, senza
> allegati, leggendo una knowledge scritta dallo script (D-72); seguiranno lista di
> osservazione, periodo straordinario, manutenzione in Excel e A8 evento critico.
> La sera del 07/10 la fase 2: **lista di osservazione** (D-73), fenomeni lontani
> con una valutazione preliminare fuori dal registro, validati nella griglia e
> mostrati nella pagina Fenomeni del report.

## Documenti

| File | Contenuto |
|---|---|
| `01_Architettura_attuale.md` | figura, misure, punti di forza, dieci debolezze con gravita', dove si spende la manutenzione |
| `02_Alternative_stessi_vincoli.md` | A Office Scripts (e variante senza script), B agenti piccoli, C piu' workbook + report di aggregazione, D report generato e opzioni JavaScript |
| `03_Alternative_vincoli_rilassati.md` | verifica della licenza, R1 pipeline Copilot Studio + Liste + Power BI, R2 agente operativo conversazionale |
| `04_Confronto_e_raccomandazione.md` | criteri pesati, punteggi motivati, raccomandazione con e senza Copilot Studio, cosa non cambiare |
| `05_Piano_rigenerazione_progressiva.md` | fasi 0-8 dal report trimestrale, prompt per Claude Code, verifiche, validazioni umane, cancelli, varianti per R2, tempi |
| `06_Focus_R2_agente_operativo.md` | R2 nel dettaglio: esperienza di analista e validatore, componenti, sei regole di governo, riuso del materiale, piano R0-R9 con prompt, verifiche e cancelli, tempi, ruoli, domande per l'IT |
| `07_Piano_semplificazione_senza_Python.md` | (24/09; **in riserva dal 27/09, D-43**) C + D senza Python in esercizio: gli agenti consegnano file, Power Query controlla e consolida, gate = spostamento in `Validati`; cosa permette davvero Agent Builder; ogni punto di impatto con l'intervento; fasi S0-S7; rischi; decisioni |
| `08_Confronto_Horizon_Scanning_Copilot.md` | (25/09) confronto con un Horizon Scanning fatto a mano con Copilot M365 (prompt cumulativo, Word + Excel): modello a confronto, proposte P1-P11 (sintesi executive, classifica e lente di Mosca, schede e metodologia nel report, Y strutturale di Mosca, D-19, colore per interesse del supervisore), cosa non copiare con le prove, ordine e decisioni. **Priorita' A approvate e applicate il 25/09** (D-19, D-32..D-34); poi P3, P6, P11 (D-35..D-37); la sera il report ridisegnato (D-39) e le schede con A6 (D-40); P7, P8, P10 da decidere |
| `09_Proposta_grafica_report.md` | (25/09) proposta per l'aspetto del report al comitato e percorso delle tre anteprime; in testa, com'e' stata realizzata nel pacchetto. **Approvata e applicata** (D-39, D-40) |
| `09_Anteprima_v3_registro.xlsx`, `09_Anteprima_v3_schede.xlsx` | (25/09) terza anteprima, approvata senza note: Quadro d'insieme, Delta con motivi, Registro con Δ 6 mesi, Dizionario, legende, Piano azioni, andamento nelle schede. Le anteprime v1 e v2 con le valutazioni sono nello zip del pacchetto 2026-09-25b |
| `09_genera_anteprima.py`, `09_genera_anteprima_v2.py`, `09_genera_anteprima_v3.py` | generatori delle tre anteprime (la v3 riusa v1 e v2); dati di esempio del pacchetto, non collegati al registro |
| `10_Piano_automazione_processo.md` | (27/09) rianalisi orientata all'automazione: passi manuali di oggi, cosa resta umano, rischio del Salvataggio automatico di OneDrive, opzioni scartate (browser, VBA, `.ps1`, Copilot Studio), procedura guidata a menu con cattura dagli appunti, installazione con un doppio clic, PDF automatici, copia di lavoro locale; fasi F1-F7, verifiche V-A..V-G. **Proposta, non ancora approvata**; piano 07 in riserva per scelta dell'utente. **Parte seconda (28/09)**: opzione separata Copilot Studio. Cosa porta (verificato su Learn), varianti CS-1 ibrida / CS-2 tutto nel cloud / CS-3 Power Query, Python pezzo per pezzo, passi comuni alle due strade C1-C9 con il testo per l'IT, fasi K0-K6, confronto, raccomandazione, verifiche V-H..V-Q. Dal 28/09 le voci di lavoro sono nel TODO del pacchetto (AU1-AU6); scelta della strada: A-15 |
| `11_Semplificazione_scoring_A1.md` | (30/09) revisione campo per campo di cio' che produce A1 (dove finisce, a cosa serve, se serve), analisi dell'output del primo ciclo di prova, modello semplificato (Gap alla Banca, Velocity facoltativa, esito e da/a allo script, KRI con soglie della Banca, un rischio per meccanismo, opzione per superare i rilievi di A5), ordine di lavoro. **Approvata** (D-49..D-56) e **realizzata nel pacchetto il 30/09** (struttura 2026-09-30; sezione 8: cosa resta) |

## Fonti consultate (23/09/2026)

- Microsoft Learn, [Standard harness licensing — Copilot Studio](https://learn.microsoft.com/en-us/microsoft-copilot-studio/billing-licensing), agg. 03/08/2026: la licenza Microsoft 365 Copilot fra le configurazioni per usare Copilot Studio; uso zero-rated per risposte e grounding; Copilot Credits.
- Microsoft Learn, [Add a prompt node to an agent flow](https://learn.microsoft.com/en-us/microsoft-copilot-studio/prompt-node-workflow), agg. 25/06/2026: nodo prompt con uscita JSON; agent flow e workflows.
- Microsoft Learn, [Add knowledge sources — Agent Builder](https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/agent-builder-add-knowledge), agg. 29/07/2026: 4 siti, tipi di file.
- Microsoft Learn, [Office Scripts: platform limits](https://learn.microsoft.com/en-us/office/dev/scripts/testing/platform-limits) e [External API calls](https://learn.microsoft.com/en-us/office/dev/scripts/develop/external-calls): 5 MB, chiamate esterne non disponibili da Power Automate, API solo web.
- Microsoft Learn, [Excel Online (Business) connector](https://learn.microsoft.com/en-us/connectors/excelonlinebusiness/): file bloccato fino a 12 minuti, scritture concorrenti non supportate, 256 righe per lettura senza paginazione.
- Microsoft Learn, [Power Query SharePoint Online list connector](https://learn.microsoft.com/en-us/power-query/connectors/sharepoint-online-list) e [Embed a report web part in SharePoint Online](https://learn.microsoft.com/en-us/power-bi/collaborate-share/office-integration/service-embed-report-spo): Power BI Pro per condividere e incorporare.
- Microsoft Support, [Data security and Python in Excel](https://support.microsoft.com/en-us/office/data-security-and-python-in-excel-33cc88a4-4a87-485e-9ff9-f35958278327): esecuzione nel cloud, niente accesso a file locali o rete.

Verificato il 25/09/2026 (conferma dell'utente): **Power Query e' abilitato**
sull'Excel aziendale. Verificato il 28/09/2026 (conferma dell'utente):
**Copilot Studio e' disponibile** (D-44). Da verificare nel tenant della Banca
prima di decidere:
- criteri DLP;
- disponibilita' di Power BI Pro;
- Office Scripts abilitati;
- comportamento di SharePoint con i file .html;
- per la variante CS-1, le verifiche V-H..V-Q del documento 10 (10.18).
