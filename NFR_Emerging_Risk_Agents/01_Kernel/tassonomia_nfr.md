# Tassonomia NFR — categorie di rischio e driver emergenti

> Riferimento unico per la classificazione dei rischi. Le sezioni "##" entrano
> nei prompt degli agenti tramite 02_Agenti/componi_prompt.py; le righe ">"
> sono note per chi legge. I codici sono letterali: compaiono negli schemi
> JSON, nelle formule e nelle liste, e devono combaciare al carattere.
>
> Dal 07/10/2026 (D-74) la classificazione e' la **tassonomia interna dei rischi
> della Banca** (`04_Riferimenti/Tassonomia dei Rischi.csv`, famiglia "Rischi Non Finanziari -
> Rischi Operativi"): solo le nove categorie marcate SI, con il loro codice.
> Sostituiscono i sette event type di Basilea (L1-01..L1-07) ovunque: classifica
> dei rischi, settori del radar, intensita' delle notizie di A3 e A4, foglio
> Notizie. Nei nomi interni (campo `event_type`, colonna `Event_Type`, nome
> `codiciL1`) resta la parola di prima: il valore e' il codice della categoria.
> Se si cambia un codice, cambiarlo anche negli enum di `schema_output_A1.json` e
> `schema_output_A3.json`, nella lista TASSONOMIA di `03_Excel/genera_dashboard.py`
> e nelle colonne Imp_ di `mappatura_campi.json`; poi la procedura "Se cambia il
> kernel" di 00_LEGGIMI.md. Il collaudo segnala i disallineamenti.

## Regola di classificazione
Un rischio ha UNA sola categoria (il tipo di rischio in cui ricade la perdita per la Banca) e UNO O PIU' driver (perche' oggi e' emergente). Se sembra avere due categorie, sono due rischi; anche due meccanismi di perdita diversi nella stessa categoria sono due rischi.

> D-55 (30/09/2026): nessuna categoria e' obbligatoria; una categoria senza
> rischi si vede lo stesso: le notizie che la toccano escono come "AREA NON
> PRESIDIATA". Cyber, AI, terze parti come fenomeni sono driver: piu' rischi
> cyber = piu' righe con DRV-CYB, anche nella stessa categoria.
> Le descrizioni sono riassunte da quelle della Banca (file csv), per stare nei
> limiti di lunghezza dei prompt.

## Categorie di rischio (tassonomia interna, in perimetro)
| Codice | Categoria | Perdite da |
|---|---|---|
| 9.1 | Condotta | comportamenti non corretti verso clienti o mercati. |
| 9.4 | Legale | violazioni di leggi, responsabilita' contrattuale, controversie. |
| 9.5 | Fiscale | violazioni di norme tributarie. |
| 9.6 | Tecnologico | sistemi e servizi ICT inadeguati o non sostituibili. |
| 9.7 | Sicurezza informatica | dati e sistemi violati o indisponibili, attacchi. |
| 9.8 | Sicurezza fisica | eventi fisici su persone, sedi, beni. |
| 9.9 | Terze parti | ricorso a fornitori di beni o servizi. |
| 9.11 | Employer | rapporti di lavoro, salute e sicurezza. |
| 9.13 | Processo | errori di processo o di esecuzione delle operazioni. |

## Driver emergenti
| Codice | Driver | Esempi |
|---|---|---|
| DRV-CYB | Cyber | nuove tecniche d'attacco, vulnerabilita' diffuse. |
| DRV-TPR | Terze parti | fornitori ICT critici, concentrazione cloud. |
| DRV-AI | Intelligenza artificiale | uso interno di modelli, attacchi abilitati da AI, trasformazioni che impattano sul capitale umano e i processi interni ed esterni alla banca. Limitata regolamentazione e assenza di meccanismi condivisi di guard railing sul tema. Proprietà intellettuale di artefatti generati dall'IA. |
| DRV-CLI | Clima e ambiente | eventi fisici estremi, transizione. |
| DRV-CON | Condotta | pratiche commerciali, greenwashing. |
| DRV-GEO | Geopolitica | sanzioni, conflitti, catene di fornitura. |
| DRV-TEC | Debito tecnologico | sistemi obsoleti, migrazioni. |
| DRV-HUM | Capitale umano | carenza di competenze, turnover in ruoli chiave. |
| DRV-SOV | Sovranità digitale | carenza o limitato controllo su infrastrutture, servizi e dati gestiti dalla banca attraverso fornitori non UE |
| DRV-PQC | Quantum Readyness | evoluzione tecniche crittografia quantistica, migrazione  ad algoritmi resistenti a tecniche di decrittazione quantistica |
| DRV-NOR | Frammentazione Normativa | continue nuove normative in parte sovrapposti da molteplici enti nazionali e sovranazionali su temi di pertinenza Non Financial Risk |

## Fuori perimetro
Rischi finanziari, strategici, reputazionali e di modello; frode, financial crime, non conformita', qualita' dei dati; eventi gia' accaduti; temi senza un meccanismo di perdita per la Banca.
