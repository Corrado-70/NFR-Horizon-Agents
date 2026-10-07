# Parere A4 — "Autorita' europea: rimborso obbligatorio delle frodi APP dal 2027"

*(Output simulato di A4 News Assessor, richiesto da un analista il 12/10/2026,
con `Baseline_corrente.json` dopo il ciclo 2026Q3. Parere non vincolante.)*

**1. Il fatto**
L'Autorita' bancaria europea (comunicazione del 9 ottobre 2026) indica che dal
2027 il rimborso delle frodi con bonifico autorizzato dal cliente (APP) sara' a
carico del prestatore di servizi di pagamento. Il fatto e' la comunicazione;
tempi e perimetro esatti dipendono dal testo definitivo, non ancora pubblicato.

**2. Impatto sui sette event type**

| Event type | Intensita' | Direzione | Motivazione |
|---|---|---|---|
| L1-01 Frode interna | 0 | Non rilevante | nessun nesso con condotte interne |
| L1-02 Frode esterna | 2 | Peggiorativo | la perdita di una frode APP passa dal cliente alla Banca |
| L1-03 Rapporti di impiego | 0 | Non rilevante | — |
| L1-04 Clientela, prodotti e prassi | 2 | Peggiorativo | contenzioso e reclami sui rimborsi, obblighi informativi |
| L1-05 Danni a beni materiali | 0 | Non rilevante | — |
| L1-06 Interruzione dei sistemi | 0 | Non rilevante | — |
| L1-07 Esecuzione dei processi | 1 | Peggiorativo | nuovo processo di gestione dei rimborsi da disegnare |

**3. Rischi del registro toccati**
- **NFR-01 Frodi su pagamenti istantanei abilitate da AI generativa** — score
  vigenti deliberati nel 2026Q3: Severity 4, Velocity 4, Prossimita' 4,
  Gap_Controlli 3, Confidence 4. La notizia puo' mettere in discussione il
  descrittore di **Severity**: oggi la perdita ricade soprattutto sul cliente;
  con il rimborso obbligatorio ricadrebbe sulla Banca.
- Nessun rischio del registro copre in modo specifico il **processo di
  rimborso** (L1-07): non e' un'area scoperta in senso stretto, perche' L1-07 e'
  presidiato da NFR-05, ma il meccanismo e' diverso.

**4. Coerenza con la valutazione deliberata**
La notizia non contraddice la valutazione vigente: la rafforza nella
direzione gia' presa. E' un segnale, non una tendenza: la soglia di direzione
richiede tre segnali netti concordanti in quattro settimane (nella settimana
del 12/10 il foglio ne conta tre su NFR-01, incluso questo).

**5. Cosa suggerisco**
- Chiedere alla Funzione Antifrode una stima interna degli importi delle frodi
  APP oggi rimborsati volontariamente, per preparare la rivalutazione della
  Severity al prossimo ciclo trimestrale.
- Verificare con la Funzione Compliance lo stato del testo normativo.
- Nessuna variazione di score ora: la via e' il ciclo 2026Q4.

**6. Limiti del parere**
Basato su una comunicazione, non sul testo definitivo. Non conosco gli importi
interni delle frodi APP. Questa notizia non comparira' nel foglio Notizie finche'
non la registra l'aggiornamento settimanale (A3); nella demo l'ha gia'
registrata la settimana del 12/10.
