# Istruzioni per Claude in questo repository

## Rami git

- I rami ammessi sono **due**, ognuno nella **sua cartella** (git worktree, dal 23/10/2026):

  | Ramo | Cartella | Versione |
  |---|---|---|
  | `main` | `Documents\NFR Horizon Agents` | in uso: Agent Builder, motore Python sul PC (`esegui_ciclo_locale.py`) |
  | `copilot-studio-pieno` | `Documents\NFR Horizon Agents CS` | tutta in Copilot Studio, senza Python sul PC (D-82) |

- **Lavora sul ramo della cartella in cui sei** e non cambiare ramo dentro una cartella (niente `git switch` o
  `git checkout` di un altro ramo): l'altra cartella puo' essere aperta da un'altra sessione.
- **Le modifiche comuni nascono su `main`**: kernel (rubrica, tassonomia, controlli, guida di scrittura), prompt degli
  agenti, motore e regole, collaudo. Poi, nella cartella del ramo `copilot-studio-pieno`, `git merge main` per
  riceverle e `genera_CS.py` per rigenerare le versioni Copilot Studio.
- Sul ramo `copilot-studio-pieno` va solo cio' che e' di Copilot Studio (argomenti, flussi, prompt CS, prove T0-T8).
  Se serve una modifica comune mentre lavori li', fermati e dillo all'utente: va fatta prima su `main`.
- **Mai unire `copilot-studio-pieno` in `main`** se l'utente non lo decide.
- **Non creare altri rami**, compresi quelli `claude/...` delle sessioni remote. L'eccezione e' quando l'utente lo dice
  esplicitamente, oppure quando lo chiedi tu prima e l'utente accetta.
- Se l'ambiente della sessione ti mette d'ufficio su un altro ramo, chiedi all'utente come procedere prima di
  modificare qualcosa.
- A inizio lavoro: `git fetch` e `git pull` sul ramo della cartella, per partire dalla versione piu' recente. Poi si
  legge la sezione 0 del registro vivo del ramo, che dice da dove si riparte, e a fine intervento la si aggiorna:
  `NFR_Emerging_Risk_Agents/TODO_possibili_sviluppi.md` su `main` (voci comuni e di `main`),
  `NFR_Emerging_Risk_Agents/09_Copilot_Studio/TODO_Copilot_Studio.md` su `copilot-studio-pieno` (solo voci del ramo).
- Commit e push solo quando l'utente lo chiede.
