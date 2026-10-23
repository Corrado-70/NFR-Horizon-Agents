// Prova K8 (Copilot Studio pieno, D-82): un Office Script scrive nel registro, ricalcola e controlla.
// Da eseguire SOLO su una COPIA del registro con dati (NFR_Registro_prova_K8.xlsx), mai sul registro vero.
// Excel per il web -> Automatizza -> Nuovo script -> incollare tutto -> Salva con il nome K8_prova -> Esegui.
// Poi lo stesso script da un flusso: azione Excel Online (Business) "Esegui script" (passo T5.2).
//
// Che cosa fa: aggiunge `righe` copie dell'ultima riga di una tabella (formule comprese), ricalcola tutto,
// conta gli errori di formula e i grafici, e restituisce una riga JSON. E' quello che faranno gli script del
// motore V2 ("applica"): scrivere righe, ricalcolare, cercare errori, senza toccare grafici e formattazione.
function main(workbook: ExcelScript.Workbook, nomeTabella: string = "tblNews", righe: number = 50): string {
  const inizio = Date.now();
  const tabella = workbook.getTable(nomeTabella);
  if (!tabella) {
    return JSON.stringify({ esito: "errore", motivo: `tabella ${nomeTabella} non trovata` });
  }
  const prima = tabella.getRowCount();
  if (prima === 0) {
    return JSON.stringify({ esito: "errore", motivo: "tabella vuota: usare una copia del registro con dati" });
  }
  let graficiPrima = 0;
  for (const foglio of workbook.getWorksheets()) {
    graficiPrima += foglio.getCharts().length;
  }
  // Ultima riga com'e' scritta: le colonne calcolate restano formule.
  const formule = tabella.getRangeBetweenHeaderAndTotal().getFormulas();
  const ultima = formule[formule.length - 1];
  const nuove: (string | number | boolean)[][] = [];
  for (let i = 0; i < righe; i++) {
    nuove.push(ultima.slice());
  }
  tabella.addRows(-1, nuove);
  workbook.getApplication().calculate(ExcelScript.CalculationType.full);
  // Errori di formula su tutti i fogli; #N/A a parte, perche' il modello lo usa di proposito (NA()).
  let errori = 0;
  let na = 0;
  const erroreExcel = /^#(VALUE!|REF!|DIV\/0!|NUM!|NAME\?|NULL!|SPILL!|CALC!|FIELD!|BLOCKED!|CONNECT!|BUSY!|UNKNOWN!)/;
  for (const foglio of workbook.getWorksheets()) {
    const usato = foglio.getUsedRange(true);
    if (!usato) {
      continue;
    }
    for (const riga of usato.getValues()) {
      for (const v of riga) {
        if (typeof v === "string" && v === "#N/A") {
          na++;
        } else if (typeof v === "string" && erroreExcel.test(v)) {
          errori++;
        }
      }
    }
  }
  let grafici = 0;
  for (const foglio of workbook.getWorksheets()) {
    grafici += foglio.getCharts().length;
  }
  return JSON.stringify({
    esito: "ok",
    tabella: nomeTabella,
    righe_prima: prima,
    righe_dopo: tabella.getRowCount(),
    errori_formula: errori,
    celle_na: na,
    grafici_prima: graficiPrima,
    grafici_dopo: grafici,
    millisecondi: Date.now() - inizio,
  });
}
