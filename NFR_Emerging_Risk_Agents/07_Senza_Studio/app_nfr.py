"""App NFR Horizon Scan: la finestra che guida l'analista (D-83, tappa M2; TODO AU5).

Si apre con un doppio clic su NFR.cmd. In alto lo stato del processo, letto dall'archivio condiviso (stato.py) e
aggiornato ogni mezzo minuto; sotto il pulsante del prossimo passo e uno per processo; al centro il passo in corso, con
le istruzioni per l'agente; in basso l'uscita del motore e l'esito colorato.

I processi sono in flussi.py: qui c'e' solo l'Ambiente che li collega alla finestra. Ogni processo gira in un thread
a parte, perche' il motore impiega minuti; le richieste di un processo alla finestra (un messaggio, una domanda, la
risposta di un agente) passano da una coda al thread della finestra, l'unico che puo' toccare tkinter.

Le risposte degli agenti si incollano (Ctrl+V) nel riquadro "Risposta dell'agente" della finestra; in piu', se
ascolta_appunti e' acceso, l'app le prende da sola quando si preme Copia sotto la risposta (appunti.py); oppure da un
file ("Scegli file..."). La casella "Agenti" dice se le risposte vengono da Agent Builder o da Copilot Studio: nomi,
cartella e registro sono gli stessi, l'origine si annota. Il registro lo apre Excel, visibile, solo per la griglia di validazione e per i testi a mano;
nel registro scrive solo il motore.
"""

import os
import queue
import threading
import time
import tkinter as tk
import webbrowser
from pathlib import Path
from tkinter import filedialog, messagebox, scrolledtext, ttk

import appunti
import esecutore
import flussi
import stato
from esegui_ciclo_locale import aperto_qui

COLORI = {"ok": "#2E7D32", "avviso": "#B26A00", "errore": "#C62828", "info": "#1F3864"}
AGGIORNA_MS = 30000


class AmbienteTk:
    """L'Ambiente di flussi.py sulla finestra. I metodi si chiamano dal thread del processo."""

    def __init__(self, app):
        self.app = app

    # chiamata al thread della finestra e attesa del risultato
    def _main(self, funzione, *argomenti):
        if threading.current_thread() is threading.main_thread():
            return funzione(*argomenti)
        evento, scatola = threading.Event(), {}

        def esegui():
            try:
                scatola["v"] = funzione(*argomenti)
            except Exception as ex:                  # noqa: BLE001 - riportata al thread del processo
                scatola["e"] = ex
            evento.set()
        self.app.coda.put(esegui)
        evento.wait()
        if "e" in scatola:
            raise scatola["e"]
        return scatola.get("v")

    def esegui(self, argomenti, script=None):
        self.app.scrivi_log(f"\n> {Path(script).stem if script else 'esegui_ciclo_locale'} {' '.join(argomenti)}", "comando")
        return esecutore.esegui(argomenti, self.app.conf["cartella_uscita"], self.app.conf.get("utente") or "",
                                su_riga=lambda r: self.app.coda.put(lambda: self.app.scrivi_log(r)),
                                script=script or esecutore.MOTORE)

    def apri(self, cosa):
        testo = str(cosa)
        if testo.startswith("http"):
            webbrowser.open(testo)
        else:
            os.startfile(testo)                      # noqa: S606 - file e cartelle dell'archivio, scelti dall'app

    def copia(self, testo):
        self._main(self.app.metti_negli_appunti, testo)

    def mostra(self, testo, tipo="info"):
        self.app.coda.put(lambda: self.app.mostra(testo, tipo))

    def conferma(self, domanda):
        return self._main(lambda: messagebox.askyesno("NFR Horizon Scan", domanda, parent=self.app.root))

    def chiedi(self, titolo, campi):
        return self._main(self.app.modulo, titolo, campi)

    def risposta(self, agente, istruzioni):
        attesa = threading.Event()
        self._main(self.app.aspetta_risposta, agente, istruzioni, attesa)
        attesa.wait()
        return self._main(self.app.prendi_risposta)

    def attendi_chiusura(self, file):
        file = Path(file)
        blocco = file.with_name("~$" + file.name)
        chiuso = threading.Event()
        self._main(self.app.aspetta_chiusura, file, chiuso)
        inizio = time.time()
        aperto = False
        while not chiuso.is_set():                   # prima si aspetta che Excel lo apra, poi che lo chiuda
            occupato = aperto_qui(file) or blocco.exists()
            if occupato:
                aperto = True
            elif aperto or time.time() - inizio > 120:
                break
            time.sleep(2)
        annullato = self._main(self.app.fine_attesa)
        if annullato:
            raise flussi.Annullato("attesa del registro annullata")


class App:
    def __init__(self, root):
        self.root = root
        self.coda = queue.Queue()
        self.conf = flussi.configurazione()
        self.amb = AmbienteTk(self)
        self.flussi = flussi.Flussi(self.amb, self.conf)
        self.ascolto = appunti.Ascolto() if appunti.disponibili() and self.conf.get("ascolta_appunti", True) else None
        self.in_corso = None
        self.attesa = None                           # (agente, Event) mentre si aspetta una risposta
        self.testo_risposta = None
        root.title("NFR Horizon Scan")
        larghezza, altezza = root.winfo_screenwidth(), root.winfo_screenheight()
        root.geometry(f"{int(larghezza * 0.62)}x{int(altezza * 0.82)}+{int(larghezza * 0.05)}+{int(altezza * 0.04)}")
        root.minsize(int(larghezza * 0.45), int(altezza * 0.6))
        if altezza <= 1200:                              # 1920x1080 e simili: tutto lo schermo, anche con la scala al 150%
            root.state("zoomed")
        self.costruisci()
        self.aggiorna_stato()
        root.after(100, self.svuota_coda)
        root.after(500, self.guarda_appunti)
        root.after(AGGIORNA_MS, self.aggiorna_periodico)

    # ------------------------------------------------------------ finestra
    def costruisci(self):
        stile = ttk.Style()
        stile.configure("Grande.TButton", font=("Segoe UI", 12, "bold"), padding=8)
        stile.configure("TButton", font=("Segoe UI", 10), padding=4)
        alto = ttk.Frame(self.root, padding=10)
        alto.pack(fill="x")
        self.righe_stato = ttk.Label(alto, font=("Segoe UI", 11), justify="left")
        self.righe_stato.pack(anchor="w")
        self.prossimo = ttk.Button(alto, style="Grande.TButton", command=lambda: self.avvia(self.flussi.prossimo))
        self.prossimo.pack(fill="x", pady=(8, 4))

        processi = ttk.Frame(self.root, padding=(10, 0))
        processi.pack(fill="x")
        self.con_a5 = tk.BooleanVar(value=False)
        voci = [("Settimana", self.flussi.settimanale), ("Trimestre", lambda: self.flussi.trimestrale(self.con_a5.get())),
                ("Straordinario", lambda: self.flussi.straordinario(self.con_a5.get())), ("Validazione", self.flussi.validazione),
                ("Schede", self.flussi.schede), ("Report", self.flussi.report), ("Riapri un ciclo", self.flussi.riapertura),
                ("Testi a mano", self.flussi.testi_a_mano), ("Parere di A4", self.flussi.parere_a4),
                ("Chiedi ad A7", self.flussi.assistente_a7), ("Diagnosi", self.flussi.diagnosi), ("Dismetti", self.flussi.dismetti)]
        self.pulsanti = [self.prossimo]
        for i, (testo, azione) in enumerate(voci):
            b = ttk.Button(processi, text=testo, command=lambda a=azione: self.avvia(a))
            b.grid(row=i // 6, column=i % 6, sticky="ew", padx=2, pady=2)
            self.pulsanti.append(b)
        for c in range(6):
            processi.columnconfigure(c, weight=1)
        opzioni = ttk.Frame(processi)
        opzioni.grid(row=2, column=0, columnspan=6, sticky="w", pady=(4, 0))
        ttk.Checkbutton(opzioni, text="Con A5 Challenger (facoltativo)", variable=self.con_a5).pack(side="left")
        ttk.Label(opzioni, text="   Agenti:").pack(side="left")
        self.origine = tk.StringVar(value=self.flussi.origine)
        scelta = ttk.Combobox(opzioni, textvariable=self.origine, values=list(flussi.ingresso.ORIGINI), state="readonly", width=16)
        scelta.pack(side="left")
        scelta.bind("<<ComboboxSelected>>", lambda ev: setattr(self.flussi, "origine", self.origine.get()))
        altro = ttk.Menubutton(opzioni, text="Altro")
        menu = tk.Menu(altro, tearoff=False)
        menu.add_command(label="Apri il registro (sola consultazione)", command=lambda: self.amb.apri(self.conf["workbook"]))
        menu.add_command(label="Apri l'archivio", command=lambda: self.amb.apri(self.conf["cartella_uscita"]))
        menu.add_command(label="Aggiorna lo stato", command=self.aggiorna_stato)
        menu.add_separator()
        menu.add_command(label="Togli il lucchetto rimasto (sblocca)", command=lambda: self.avvia(self.flussi.sblocca))
        menu.add_command(label="Ricostruisci la griglia di validazione",
                         command=lambda: self.avvia(lambda: self.flussi.motore("griglia")))
        altro["menu"] = menu
        altro.pack(side="left", padx=12)

        self.passo = ttk.LabelFrame(self.root, text="Passo in corso", padding=8)
        self.passo.pack(fill="x", padx=10, pady=8)
        self.istruzioni = ttk.Label(self.passo, text="Nessun processo in corso.", justify="left", font=("Segoe UI", 10))
        self.istruzioni.pack(anchor="w", fill="x")
        self.passo.bind("<Configure>", lambda ev: self.istruzioni.config(wraplength=max(300, ev.width - 30)))
        ttk.Label(self.passo, text="Risposta dell'agente: copiala dalla chat e incollala qui (Ctrl+V)").pack(anchor="w", pady=(6, 0))
        self.incolla = tk.Text(self.passo, height=3, font=("Consolas", 9), wrap="char")
        self.incolla.pack(fill="x", pady=(2, 0))
        self.incolla.bind("<<Paste>>", lambda ev: self.root.after(150, self.usa_incollato))
        bottoni = ttk.Frame(self.passo)
        bottoni.pack(anchor="w", pady=(6, 0))
        self.b_usa = ttk.Button(bottoni, text="Usa il testo incollato", command=self.usa_incollato)
        self.b_appunti = ttk.Button(bottoni, text="Leggi gli appunti adesso", command=self.leggi_appunti_adesso)
        self.b_file = ttk.Button(bottoni, text="Scegli file...", command=self.scegli_file)
        self.b_chiuso = ttk.Button(bottoni, text="Ho chiuso il registro", command=self.chiuso_a_mano)
        self.b_annulla = ttk.Button(bottoni, text="Annulla il passo", command=self.annulla)
        for b in (self.b_usa, self.b_appunti, self.b_file, self.b_chiuso, self.b_annulla):
            b.pack(side="left", padx=(0, 6))
        self.mostra_bottoni()

        self.fascia = tk.Label(self.root, text="", font=("Segoe UI", 11, "bold"), fg="white", bg="#FFFFFF", anchor="w", padx=10)
        self.fascia.pack(fill="x", padx=10)
        self.log = scrolledtext.ScrolledText(self.root, font=("Consolas", 9), height=18, wrap="word")
        self.log.pack(fill="both", expand=True, padx=10, pady=(4, 10))
        self.log.tag_configure("comando", foreground="#1F3864", font=("Consolas", 9, "bold"))
        for tipo, colore in COLORI.items():
            self.log.tag_configure(tipo, foreground=colore, font=("Segoe UI", 10, "bold"))
        if not self.ascolto and self.conf.get("ascolta_appunti", True):
            self.mostra("Ascolto degli appunti non disponibile su questo PC (pywin32 mancante): incollare le risposte nel "
                        "riquadro, o sceglierle come file.", "avviso")

    def mostra_bottoni(self, risposta=False, chiusura=False):
        for b, visibile in ((self.b_usa, risposta), (self.b_appunti, risposta and self.ascolto), (self.b_file, risposta),
                            (self.b_chiuso, chiusura), (self.b_annulla, risposta or chiusura)):
            b.state(["!disabled"] if visibile else ["disabled"])

    # ------------------------------------------------------------ stato
    def aggiorna_stato(self):
        try:
            s = stato.leggi(self.conf)
        except Exception as ex:                      # noqa: BLE001 - lo stato non deve chiudere la finestra
            self.righe_stato.config(text=f"Stato non leggibile: {ex}")
            return
        r = s["righe"]                               # due righe: lo spazio va al passo in corso e all'uscita
        self.righe_stato.config(text="   ·   ".join(r[:2]) + "\n" + "   ·   ".join(r[2:]))
        p = s["prossimo"]
        self.prossimo.config(text=f"▶  Prossimo passo: {p['titolo']}\n{p['chi']}: {p['perche']}")

    def aggiorna_periodico(self):
        if not self.in_corso:
            self.aggiorna_stato()
        self.root.after(AGGIORNA_MS, self.aggiorna_periodico)

    # ------------------------------------------------------------ processi
    def avvia(self, azione):
        if self.in_corso:
            messagebox.showinfo("NFR Horizon Scan", "C'e' gia' un processo in corso: finiscilo o annullalo.", parent=self.root)
            return
        for b in self.pulsanti:
            b.state(["disabled"])
        self.fascia.config(text="  In corso...", bg=COLORI["info"])

        def lavoro():
            try:
                azione()
            except flussi.Annullato as ex:
                self.amb.mostra(f"Processo interrotto ({ex}): si riprende dal passo giusto con il pulsante del prossimo passo.",
                                "avviso")
            except Exception as ex:                  # noqa: BLE001 - mostrato, mai una finestra che si chiude
                self.amb.mostra(f"Errore dell'app: {type(ex).__name__}: {ex}", "errore")
            finally:
                self.coda.put(self.fine_processo)
        self.in_corso = threading.Thread(target=lavoro, daemon=True)
        self.in_corso.start()

    def fine_processo(self):
        self.in_corso = None
        self.attesa = None
        for b in self.pulsanti:
            b.state(["!disabled"])
        self.istruzioni.config(text="Nessun processo in corso.")
        self.mostra_bottoni()
        self.aggiorna_stato()

    def svuota_coda(self):
        try:
            while True:
                self.coda.get_nowait()()
        except queue.Empty:
            pass
        self.root.after(100, self.svuota_coda)

    # ------------------------------------------------------------ messaggi
    def scrivi_log(self, testo, tag=None):
        self.log.insert("end", testo + "\n", tag or ())
        self.log.see("end")

    def mostra(self, testo, tipo="info"):
        self.scrivi_log(testo, tipo)
        if tipo in ("ok", "avviso", "errore"):
            self.fascia.config(text="  " + testo.splitlines()[0][:160], bg=COLORI[tipo])

    def metti_negli_appunti(self, testo):
        if self.ascolto:
            self.ascolto.scritta_da_me(appunti.scrivi(testo))
        else:
            self.root.clipboard_clear()
            self.root.clipboard_append(testo)
        self.scrivi_log("(negli appunti: " + testo.splitlines()[0][:100] + ("..." if len(testo) > 100 else "") + ")", "info")

    def modulo(self, titolo, campi):
        finestra = tk.Toplevel(self.root)
        finestra.title(titolo)
        finestra.transient(self.root)
        finestra.grab_set()
        valori, esito = {}, {}
        ttk.Label(finestra, text=titolo, font=("Segoe UI", 11, "bold")).grid(row=0, column=0, columnspan=2, sticky="w", padx=10, pady=8)
        for i, (chiave, etichetta, predefinito) in enumerate(campi, start=1):
            ttk.Label(finestra, text=etichetta, wraplength=380).grid(row=i, column=0, sticky="w", padx=10, pady=3)
            v = tk.StringVar(value=predefinito)
            ttk.Entry(finestra, textvariable=v, width=60).grid(row=i, column=1, padx=10, pady=3)
            valori[chiave] = v

        def ok():
            esito["v"] = {k: v.get().strip() for k, v in valori.items()}
            finestra.destroy()
        riga = len(campi) + 1
        ttk.Button(finestra, text="Conferma", command=ok).grid(row=riga, column=1, sticky="e", padx=10, pady=10)
        ttk.Button(finestra, text="Annulla", command=finestra.destroy).grid(row=riga, column=0, sticky="w", padx=10, pady=10)
        self.root.wait_window(finestra)
        return esito.get("v")

    # ------------------------------------------------------------ risposte degli agenti
    def aspetta_risposta(self, agente, istruzioni, evento):
        self.attesa = (agente, evento)
        self.testo_risposta = None
        if self.ascolto:
            self.ascolto.ricomincia()
        self.istruzioni.config(text=f"In attesa della risposta di {agente}.\n{istruzioni}")
        self.mostra_bottoni(risposta=True)

    def consegna(self, testo):
        if not self.attesa:
            return
        agente, evento = self.attesa
        self.testo_risposta, self.attesa = testo, None
        self.mostra_bottoni()
        if testo is not None:
            self.scrivi_log(f"(risposta di {agente} ricevuta: {len(testo)} caratteri)", "info")
        evento.set()

    def prendi_risposta(self):
        return self.testo_risposta

    def guarda_appunti(self):
        if self.attesa and self.ascolto:
            testo = self.ascolto.nuova()
            if testo and ("{" in testo or self.attesa[0] == "A4"):
                self.consegna(testo)
        self.root.after(500, self.guarda_appunti)

    def usa_incollato(self):
        """La risposta incollata nel riquadro: si consegna al processo che la aspetta, e il riquadro si svuota."""
        testo = self.incolla.get("1.0", "end").strip()
        if not self.attesa or not testo:
            return
        if "{" not in testo and self.attesa[0] != "A4":
            return                                   # incollato a meta' o testo sbagliato: si aspetta il pulsante
        self.incolla.delete("1.0", "end")
        self.consegna(testo)

    def leggi_appunti_adesso(self):
        if self.attesa and self.ascolto:
            testo = appunti.leggi()
            if testo:
                self.consegna(testo)

    def scegli_file(self):
        if not self.attesa:
            return
        nome = filedialog.askopenfilename(parent=self.root, title=f"Risposta di {self.attesa[0]}",
                                          filetypes=[("Risposte", "*.json *.txt"), ("Tutti i file", "*.*")])
        if nome:
            self.consegna(Path(nome).read_text(encoding="utf-8-sig", errors="replace"))

    def annulla(self):
        if self.attesa:
            self.consegna(None)
        elif getattr(self, "chiusura", None):
            self.chiusura_annullata = True
            self.chiusura.set()

    # ------------------------------------------------------------ registro aperto in Excel
    def aspetta_chiusura(self, file, evento):
        self.chiusura, self.chiusura_annullata = evento, False
        self.istruzioni.config(text=f"Il registro e' aperto in Excel ({Path(file).name}): lavora nelle celle gialle, salva e "
                                    "chiudi Excel. L'app prosegue da sola quando il file e' chiuso.")
        self.mostra_bottoni(chiusura=True)

    def chiuso_a_mano(self):
        if getattr(self, "chiusura", None):
            self.chiusura.set()

    def fine_attesa(self):
        self.chiusura = None
        self.istruzioni.config(text="Registro chiuso: il processo continua.")
        self.mostra_bottoni()
        return getattr(self, "chiusura_annullata", False)


def nitido():
    """Testi nitidi sugli schermi con la scala di Windows oltre il 100% (altrimenti la finestra e' sfocata)."""
    try:
        import ctypes
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except Exception:                                # noqa: BLE001 - Windows vecchio o non Windows: si vede lo stesso
        pass


def main():
    nitido()
    root = tk.Tk()
    try:
        App(root)
    except Exception as ex:                          # noqa: BLE001 - configurazione mancante o illeggibile
        messagebox.showerror("NFR Horizon Scan", f"L'app non parte: {type(ex).__name__}: {ex}\n\nControllare "
                             "configurazione.json accanto agli script (guida, sezione 0.3).")
        root.destroy()
        return
    root.mainloop()


if __name__ == "__main__":
    main()
