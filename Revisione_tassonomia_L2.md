# Tassonomia NFR — event type di secondo livello (Tassonomia Interna, L2)

> **Superato il 07/10/2026 (D-74).** Su indicazione dell'utente la classificazione usa la
> tassonomia interna della Banca (`NFR_Emerging_Risk_Agents/01_Kernel/Tassonomia dei Rischi.csv`,
> solo le nove categorie marcate SI), che sostituisce del tutto gli event type di Basilea:
> vedi `01_Kernel/tassonomia_nfr.md` e `08_Deploy/DECISIONI.md`, D-74. Questo file resta
> come traccia della bozza.

> Fonte unica degli event type di secondo livello (D-74, 07/10/2026): ogni
> rischio del registro si classifica qui; tutto il resto (settori del radar,
> foglio Notizie, aree non presidiate, intensita' delle notizie di A3 e A4)
> resta sul primo livello, che e' il prefisso del codice (L1-02.2 -> L1-02) e
> sta in tassonomia_nfr.md.
> Questo file NON entra nei prompt (che includono solo tassonomia_nfr.md): lo
> riceve A1 nell'allegato Input_A1_<ciclo>.txt (07_Senza_Studio/input_a1.py,
> parte 4) e lo leggono lo schema di A1 (enum), il generatore del template
> (nomi, elenco a discesa) e il collaudo (verifica_riferimenti.py).
> Nomi e descrizione delle categorie di rischio di primo e secondo livello della banca. 
> Nell'ambito dell'agente NFR sono rilevanti i rischi con seconda colonna valorizzata a SI.

Ogni rischio ha UN codice di secondo livello: quello del meccanismo di perdita, cioe' come la perdita si manifesterebbe per la Banca. Il codice comincia con il codice di primo livello del suo event type. Un rischio gia' censito con un codice di primo livello (L1-0n) riceve un codice di secondo livello dello stesso primo livello: e' una riclassificazione, non un cambio di meccanismo.

## Event type di secondo livello
| Codice | Primo livello | Secondo livello | Esempi |
|---|---|---|---|
| L1-01.1 | Frode interna | Attivita' non autorizzate | operazioni non registrate o non autorizzate, abuso di posizione. |
| L1-01.2 | Frode interna | Furto e frode | appropriazione indebita, furto di dati da parte di dipendenti, corruzione. |
| L1-02.1 | Frode esterna | Furto e frode | truffe ai clienti, frodi sui pagamenti, falsificazioni, social engineering. |
| L1-02.2 | Frode esterna | Sicurezza dei sistemi | attacchi informatici, intrusioni, ransomware, furto di dati da parte di terzi. |
| L1-03.1 | Rapporti di impiego e sicurezza sul lavoro | Rapporti con il personale | vertenze, retribuzioni, licenziamenti, attivita' sindacale. |
| L1-03.2 | Rapporti di impiego e sicurezza sul lavoro | Sicurezza sul lavoro | salute e sicurezza dei dipendenti, infortuni. |
| L1-03.3 | Rapporti di impiego e sicurezza sul lavoro | Diversita' e discriminazione | discriminazioni, molestie, parita' di trattamento. |
| L1-04.1 | Clientela, prodotti e prassi professionali | Idoneita', informativa e obblighi fiduciari | adeguatezza, trasparenza, riservatezza e uso dei dati dei clienti. |
| L1-04.2 | Clientela, prodotti e prassi professionali | Pratiche commerciali o di mercato improprie | concorrenza, abusi di mercato, riciclaggio, sanzioni internazionali, greenwashing. |
| L1-04.3 | Clientela, prodotti e prassi professionali | Prodotti difettosi | difetti di prodotti o modelli, errori dei servizi offerti ai clienti. |
| L1-04.4 | Clientela, prodotti e prassi professionali | Selezione, sponsorizzazione ed esposizione | selezione della clientela, limiti di esposizione verso un cliente. |
| L1-04.5 | Clientela, prodotti e prassi professionali | Consulenza | controversie sulla consulenza prestata. |
| L1-05.1 | Danni a beni materiali | Disastri e altri eventi | eventi naturali, eventi climatici estremi, terrorismo, vandalismo. |
| L1-06.1 | Interruzione dell'operativita' e disfunzione dei sistemi | Sistemi | guasti hardware o software, telecomunicazioni, indisponibilita' di servizi, anche di terzi. |
| L1-07.1 | Esecuzione, consegna e gestione dei processi | Esecuzione, consegna e gestione delle operazioni | errori di esecuzione, migrazioni, gestione dei modelli e dei dati. |
| L1-07.2 | Esecuzione, consegna e gestione dei processi | Monitoraggio e reporting | segnalazioni obbligatorie, reporting inesatto. |
| L1-07.3 | Esecuzione, consegna e gestione dei processi | Acquisizione della clientela e documentazione | documentazione mancante o incompleta, autorizzazioni dei clienti. |
| L1-07.4 | Esecuzione, consegna e gestione dei processi | Gestione dei conti della clientela | accessi non autorizzati ai conti, registrazioni errate, danni ai beni dei clienti. |
| L1-07.5 | Esecuzione, consegna e gestione dei processi | Controparti commerciali | controversie con controparti non clienti. |
| L1-07.6 | Esecuzione, consegna e gestione dei processi | Fornitori | esternalizzazioni, inadempienze e controversie con i fornitori. |


