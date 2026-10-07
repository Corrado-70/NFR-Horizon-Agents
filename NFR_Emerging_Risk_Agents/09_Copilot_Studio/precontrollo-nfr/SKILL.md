---
name: precontrollo-nfr
description: Precontrollo della Banca sull'output JSON di A1 Horizon Scanner (registro dei rischi NFR emergenti), da fare prima di consegnarlo. Esegue senza modificarlo lo script scripts/precontrollo_nfr.py sull'output di A1 e sull'allegato Input_A1 del ciclo, e dice cosa correggere (schema, controlli meccanizzati C1-C9, parti del razionale). Usala ogni volta che hai scritto o corretto l'output JSON di A1, prima di consegnarlo, e quando l'utente chiede il precontrollo.
---

# Precontrollo NFR dell'output di A1

Lo script e' lo stesso codice che la Banca lancia sul PC (`python esegui_ciclo_locale.py precontrollo`):
stessi controlli, stesso messaggio di correzione. Serve a consegnare un output che A5 Challenger e lo
script della Banca non fermeranno. Non giudica la plausibilita' dei valori (C4: resta ad A5) e non
scrive nel registro.

## Procedura

1. Scrivi l'output JSON completo del ciclo nel file `A1_<ciclo>.json`: solo il JSON, UTF-8, senza
   recinti ``` e senza testo attorno.
2. Individua fra i file della conversazione l'allegato `Input_A1_<ciclo>.txt` (contiene la baseline
   nella parte 1).
3. Esegui lo script cosi' com'e', dalla cartella della skill o con il suo percorso:

   `python scripts/precontrollo_nfr.py A1_<ciclo>.json Input_A1_<ciclo>.txt`

4. Leggi la prima riga dell'esito:
   - `nessun rilievo`: vai al punto 6;
   - `N punti da correggere`: correggi nel JSON esattamente i punti delle sezioni "Schema" e "Da
     correggere" del messaggio, senza cambiare cio' che non e' citato; salva lo stesso file e
     rilancia lo script (punto 3). Al massimo tre giri;
   - punti "Da verificare" e "Forma dei testi": correggili se fondati; se confermi un valore,
     scrivi il perche' nel razionale del rischio.
5. Se dopo tre giri restano punti da correggere, consegna comunque e dillo nel messaggio.
6. Consegna il file `A1_<ciclo>.json` finale e, nel messaggio, le prime due righe dell'ultimo esito
   dello script copiate senza cambiarle (l'esito e l'impronta), con il numero di giri fatti.

## Regole

- Non modificare, riscrivere o imitare lo script. Se non parte, riporta l'errore com'e' e consegna
  senza precontrollo, dicendolo.
- Non dichiarare un esito che lo script non ha stampato. L'impronta della seconda riga serve alla
  Banca per verificare che l'esito sia proprio del file consegnato.
- Lo script non usa la rete e non scrive nel registro: nel registro scrive solo il motore della
  Banca, dopo A5 e i suoi controlli.
