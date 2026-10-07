# 4. Confronto e raccomandazione

> **Aggiornamento del 28/09/2026.** Dopo questa analisi del 23/09 le scelte
> sono cambiate:
> - C senza Python (piano 07) e' **in riserva**: Python resta il motore (D-43);
> - l'automazione per l'analista segue il piano 10, con un confronto nuovo
>   (10.16) fra la procedura guidata (strada A) e Copilot Studio con il motore
>   Python in background (CS-1). La CS-1 e' vicina a R2, ma senza riscrivere i
>   controlli;
> - Copilot Studio e' disponibile (D-44); se usarlo e' la decisione A-15.
>
> Il documento resta l'analisi com'era alla sua data.

> **Aggiornamento del 25/09/2026 sera (struttura del workbook 2026-09-25c,
> DECISIONI D-39 e D-40).** Il registro e il report sono ora un solo file
> ridisegnato; le schede dei rischi sono un file a parte, `Schede_<ciclo>.xlsx`,
> con i testi dell'agente **A6**, che si lancia dopo la validazione con un solo
> allegato preparato dallo script (che ne controlla l'output). I nomi dei fogli
> citati qui si leggono cosi': Dashboard -> **Registro** (tabella per rischio,
> controlli di validazione e copertura) e **Quadro** (report); Sintesi ->
> **Quadro**; Trend -> **Storico**; KRI_Correnti e Andamento_KRI ->
> **Indicatori**; Analisi_News -> **Notizie**; Approfondimento e Schede -> file
> delle schede; Leggimi -> **Guida**; il radar a tre cicli della Dashboard non
> c'e' piu' (lo sostituiscono Matrice e Radar_Mosca). Fogli nuovi: **Matrice**,
> **Piano_azioni**, **Dizionario**. Qualunque alternativa architetturale deve
> riprodurre questa struttura del report e il passo delle schede; il resto del
> documento e' l'analisi com'era alla sua data.

## 4.1 Criteri e pesi

Pesi pensati per una banca significativa con la richiesta esplicita di
semplicita' di gestione. Si possono cambiare: la tabella si ricalcola a mano
in un minuto.

| Criterio | Peso | Cosa misura |
|---|---|---|
| Governance e tracciabilita' | 20% | controlli deterministici prima della scrittura, audit, validazione, evidenze |
| Semplicita' di gestione e modifica | 20% | quanto costa cambiare metodologia, viste, grafici, dati |
| Operativita' per l'utente | 15% | passi manuali, competenze richieste, probabilita' di errore |
| Robustezza | 15% | resistenza a errori, blocchi, file aperti, volumi |
| Dipendenze e approvazioni IT | 10% | installazioni, ruoli, licenze da chiedere (5 = nessuna) |
| Tempo e costo per arrivarci | 10% | partendo da oggi (5 = gia' fatto) |
| Evolvibilita' | 10% | quanto regge piu' rischi, piu' utenti, nuove funzioni |

## 4.2 Punteggi (1 = debole, 5 = forte)

| Soluzione | Gov. | Sempl. | Operat. | Robust. | Dip. IT | Tempo | Evolv. | **Totale pesato** |
|---|---|---|---|---|---|---|---|---|
| Attuale | 5 | 2 | 2 | 3 | 3 | 5 | 2 | **3,15** |
| A Office Scripts | 3 | 3 | 3 | 3 | 5 | 2 | 2 | **3,00** |
| B Agenti piccoli (pieno) | 4 | 3 | 1 | 4 | 3 | 3 | 4 | **3,15** |
| C Piu' workbook + report | 5 | 4 | 3 | 4 | 3 | 3 | 4 | **3,85** |
| D Report generato (aggiunta) | 5 | 3 | 4 | 3 | 3 | 4 | 3 | **3,65** |
| **C + D** | 5 | 4 | 4 | 4 | 3 | 3 | 4 | **4,00** |
| R1 Pipeline Copilot Studio | 4 | 3 | 5 | 4 | 2 | 2 | 5 | **3,65** |
| R2 Agente operativo | 3 | 5 | 5 | 3 | 3 | 4 | 4 | **3,90** |

Motivazioni sintetiche dei punteggi piu' discutibili:
- **A, governance 3**: si perde quasi tutto il collaudo automatico e le regole
  dello schema vanno ricopiate nello script.
- **B, operativita' 1**: senza orchestratore ogni agente in piu' e' una chat e un
  JSON in piu' da salvare.
- **C, semplicita' 4**: il report diventa sostituibile e le viste sono query
  leggibili; resta il PC con Python.
- **R1, dipendenze 2 e tempo 2**: ambiente Power Platform, ruoli, DLP, crediti,
  eventualmente Power BI Pro; costruzione e collaudo piu' lunghi.
- **R2, governance 3**: i controlli sono deterministici solo se la scrittura
  passa per uno strumento unico "controlla e scrivi".

## 4.3 Raccomandazione

**Se i vincoli restano (niente Copilot Studio): evolvere l'attuale verso C + D,
per gradi, senza rifare il resto.**
1. **D subito**: il report trimestrale in PowerPoint generato dopo la
   validazione (e' quello che il comitato legge; basso rischio).
2. **C poi**: staccare le viste in `NFR_Report.xlsx` alimentato da Power Query;
   i dati restano nel workbook attuale finche' non conviene separarli in piu'
   file. Questo chiude anche la voce G4 (migrazione) del TODO.
3. **B solo in parte e solo se serve**: separare A1 in "Evidenze" e
   "Punteggi/mitigazioni" quando il test in tenant mostra che la qualita' o il
   limite di caratteri lo richiedono.
4. **A no**, salvo che l'installazione di Python sia impossibile.

**Se Copilot Studio e' abilitabile (verificare subito con l'IT, la licenza
Microsoft 365 Copilot potrebbe gia' bastare): R2, poi i pezzi di R1 che
servono.** Con R2 spariscono i passi di copia e il PC dedicato; gli agenti
piccoli diventano gratuiti da orchestrare; lo stato passa nelle liste.

## 4.4 Cosa NON cambierei in nessun caso

Sono il valore vero del progetto e sopravvivono a qualunque architettura:
- il **kernel** (rubrica, tassonomia, fonti) come fonte unica, e i prompt
  composti da esso;
- gli **schemi JSON** come contratto fra agenti e scrittura;
- la **separazione giudizio/calcolo** (composito e urgenza calcolati);
- i **controlli deterministici prima della scrittura** con fermo pulito;
- la **validazione umana tracciata** e la base dati delle rettifiche;
- il **collaudo dei contratti** (schemi, controlli, riferimenti), anche se la
  parte operativa passa alla Power Platform.

## 4.5 Rischi che nessuna alternativa elimina

- **Qualita' reale degli agenti nel tenant** (retrieval, riproducibilita'): si
  misura solo con un trimestre gia' valutato a mano e il doppio run.
- **Decisioni della Banca** ancora aperte: descrittori, pesi, soglie, fonti,
  metodo dell'urgenza, chi valida.
- **Compliance** sull'elaborazione in Agent Builder o Copilot Studio.
