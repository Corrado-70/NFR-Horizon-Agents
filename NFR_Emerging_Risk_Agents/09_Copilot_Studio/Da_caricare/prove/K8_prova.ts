// Prova K8 (Copilot Studio pieno, D-82): un Office Script scrive nel registro, ricalcola e controlla.
// Da eseguire SOLO su una COPIA del registro con dati (NFR_Registro_prova_K8.xlsx), mai sul registro vero.
// Excel per il web -> Automatizza -> Nuovo script -> incollare tutto -> Salva con il nome K8_prova -> Esegui.
// Poi lo stesso script da un flusso: azione Excel Online (Business) "Esegui script" (passo T5.2).
//
// Che cosa fa: aggiunge `righe` copie dell'ultima riga di una tabella (formule comprese), ricalcola tutto,
// conta gli errori di formula prima e dopo e i grafici, e restituisce una riga JSON. E' quello che faranno gli
// script del motore ("applica"): scrivere righe, ricalcolare, cercare errori, senza toccare grafici e formattazione.
// Gli errori si riconoscono dal tipo della cella, non dal testo: a mano Excel in italiano scrive #N/D e #RIF!, dal
// flusso #N/A e #REF! (T5.1 e T5.2 del 23/10). #N/A a parte, perche' il modello lo usa di proposito (NA()).
// La riga JSON va anche nel riquadro Output (console.log): eseguito a mano, Excel non mostra il valore restituito.

interface Conteggio {
  errori: number;
  na: number;
  dettaglio: string[];
}

function esci(esito: object): string {
  const riga = JSON.stringify(esito);
  console.log(riga);
  return riga;
}

function contaErrori(workbook: ExcelScript.Workbook, massimo: number): Conteggio {
  const c: Conteggio = { errori: 0, na: 0, dettaglio: [] };
  for (const foglio of workbook.getWorksheets()) {
    const usato = foglio.getUsedRange(true);
    if (!usato) {
      continue;
    }
    const tipi = usato.getValueTypes();
    const valori = usato.getValues();
    for (let i = 0; i < tipi.length; i++) {
      for (let j = 0; j < tipi[i].length; j++) {
        if (tipi[i][j] !== ExcelScript.RangeValueType.error) {
          continue;
        }
        const v = String(valori[i][j]);
        if (v === "#N/A" || v === "#N/D") {
          c.na++;
          continue;
        }
        c.errori++;
        if (c.dettaglio.length < massimo) {
          const cella = usato.getCell(i, j);
          c.dettaglio.push(`${cella.getAddress()} ${v} ${cella.getFormula()}`);
        }
      }
    }
  }
  return c;
}

function main(workbook: ExcelScript.Workbook, nomeTabella: string = "tblNews", righe: number = 50): string {
  const inizio = Date.now();
  const tabella = workbook.getTable(nomeTabella);
  if (!tabella) {
    return esci({ esito: "errore", motivo: `tabella ${nomeTabella} non trovata` });
  }
  const prima = tabella.getRowCount();
  if (prima === 0) {
    return esci({ esito: "errore", motivo: "tabella vuota: usare una copia del registro con dati" });
  }
  let graficiPrima = 0;
  for (const foglio of workbook.getWorksheets()) {
    graficiPrima += foglio.getCharts().length;
  }
  const errPrima = contaErrori(workbook, 20);
  // Ultima riga com'e' scritta: le colonne calcolate restano formule.
  const formule = tabella.getRangeBetweenHeaderAndTotal().getFormulas();
  const ultima = formule[formule.length - 1];
  const nuove: (string | number | boolean)[][] = [];
  for (let i = 0; i < righe; i++) {
    nuove.push(ultima.slice());
  }
  tabella.addRows(-1, nuove);
  workbook.getApplication().calculate(ExcelScript.CalculationType.full);
  const errDopo = contaErrori(workbook, 20);
  let grafici = 0;
  for (const foglio of workbook.getWorksheets()) {
    grafici += foglio.getCharts().length;
  }
  return esci({
    esito: "ok",
    tabella: nomeTabella,
    righe_prima: prima,
    righe_dopo: tabella.getRowCount(),
    errori_prima: errPrima.errori,
    errori_dopo: errDopo.errori,
    na_prima: errPrima.na,
    na_dopo: errDopo.na,
    grafici_prima: graficiPrima,
    grafici_dopo: grafici,
    millisecondi: Date.now() - inizio,
    dettaglio_errori_prima: errPrima.dettaglio,
    dettaglio_errori_dopo: errDopo.dettaglio,
  });
}
