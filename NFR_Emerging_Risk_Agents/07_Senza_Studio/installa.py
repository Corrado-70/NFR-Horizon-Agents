"""Installazione dell'app NFR su questo PC (D-83, tappa M3). Si lancia con un doppio clic su installa.cmd.

Passi, ognuno con il suo esito nel Prompt dei comandi:
  1. Python 3.10+ e tkinter;
  2. i moduli (pywin32, openpyxl, pypac): cio' che manca si installa con pip --user, senza diritti di amministratore,
     dalla rete o, se c'e', dalla cartella 'pacchetti' accanto a 07_Senza_Studio;
  3. configurazione.json con una finestra: cartelle sincronizzate, utente, validatore, PC della raccolta, versione e
     link degli agenti. I valori di una configurazione che c'e' gia' si propongono; la precedente resta accanto;
  4. i collegamenti: "NFR Horizon Scan" sul Desktop, "NFR notizie manuali" in Invia a;
  5. sul PC della raccolta, l'attivita' pianificata del lunedi' alle 7;
  6. a richiesta, le cartelle sincronizzate "sempre su questo dispositivo" (attrib +P);
  7. la Verifica del PC (verifica_pc.py), salvata nell'archivio.
Rilanciarlo non fa danni: ogni passo controlla prima che cosa c'e'.

Uso: python installa.py [--senza-finestra] [--senza-collegamenti] [--senza-attivita] [--solo-verifica]
"""

import argparse
import os
import subprocess
import sys
import tempfile
from pathlib import Path

import installazione as ins

QUI = Path(__file__).resolve().parent
FILE_CONF = QUI / "configurazione.json"
NASCOSTO = getattr(subprocess, "CREATE_NO_WINDOW", 0)


def titolo(n, testo):
    print(f"\n=== {n}. {testo} ===")


def esegui(cmd, **opzioni):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, creationflags=NASCOSTO, **opzioni)
        return r.returncode, (r.stdout or "") + (r.stderr or "")
    except (OSError, subprocess.SubprocessError) as ex:
        return 1, str(ex)


# ------------------------------------------------------------ 1-2. Python e moduli
def passo_python():
    titolo(1, "Python")
    v = ".".join(map(str, sys.version_info[:3]))
    if not ins.python_adatto():
        print(f"NO: Python {v}. Serve Python 3.10 o piu' recente: chiederlo all'IT, poi rilanciare installa.cmd.")
        return False
    print(f"OK: Python {v} ({sys.executable})")
    try:
        import tkinter  # noqa: F401
        print("OK: tkinter (la finestra dell'app)")
    except ImportError:
        print("NO: manca tkinter, la finestra dell'app non si aprirebbe. Reinstallare Python con l'opzione tcl/tk.")
        return False
    return True


def passo_moduli():
    titolo(2, "Moduli Python")
    mancanti = ins.moduli_mancanti()
    if not mancanti:
        print("OK: pywin32, openpyxl, pypac gia' installati")
        return True
    for pacchetto, uso in mancanti:
        print(f"manca {pacchetto} ({uso})")
    cartella = ins.cartella_pacchetti()
    cmd = ins.comando_pip([p for p, _ in mancanti], cartella)
    print(("Installazione dalla cartella " + str(cartella) if cartella else "Installazione dalla rete") + ":\n  " + " ".join(cmd))
    codice, uscita = esegui(cmd)
    print(uscita.strip()[-3000:])
    ancora = ins.moduli_mancanti()
    if not ancora:
        print("OK: moduli installati")
        return True
    print(f"NO: mancano ancora {', '.join(p for p, _ in ancora)}: {ins.spiega_pip(uscita)}")
    if any(p == "pywin32" for p, _ in ancora) and codice == 0:
        print("pywin32 risulta installato ma non si carica: lanciare  python -m pywin32_postinstall -install  "
              "(se chiede i diritti, chiederlo all'IT).")
    return not any(p == "pywin32" for p, _ in ancora)     # senza openpyxl o pypac si lavora lo stesso


# ------------------------------------------------------------ 3. configurazione
def finestra_configurazione(vecchia):
    """La finestra della configurazione. Restituisce la configurazione da salvare, o None (Annulla)."""
    import tkinter as tk
    from tkinter import filedialog, messagebox, ttk

    origine_iniziale = vecchia.get("agenti") if vecchia.get("agenti") in ins.ORIGINI else ins.ORIGINI[0]
    root = tk.Tk()
    root.title("NFR Horizon Scan - configurazione di questo PC")
    try:
        import ctypes
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except Exception:                                # noqa: BLE001 - non Windows o Windows vecchio
        pass
    corpo = ttk.Frame(root, padding=12)
    corpo.pack(fill="both", expand=True)
    var, esito = {}, {}
    r = 0

    def etichetta(testo, nota=""):
        nonlocal r
        ttk.Label(corpo, text=testo, font=("Segoe UI", 10, "bold")).grid(row=r, column=0, sticky="w", pady=(6, 0))
        if nota:
            ttk.Label(corpo, text=nota, foreground="#555555", wraplength=520).grid(row=r + 1, column=0, columnspan=3, sticky="w")
        r += 2 if nota else 1

    def percorso(chiave, testo, nota, file=False):
        nonlocal r
        etichetta(testo, nota)
        v = tk.StringVar(value=str(vecchia.get(chiave) or ""))
        ttk.Entry(corpo, textvariable=v, width=80).grid(row=r, column=0, columnspan=2, sticky="we")

        def scegli():
            iniziale = Path(v.get()).parent if file and v.get() else (v.get() or str(Path.home()))
            nome = (filedialog.askopenfilename(parent=root, title=testo, initialdir=iniziale,
                                               filetypes=[("Excel", "*.xlsx"), ("Tutti i file", "*.*")]) if file else
                    filedialog.askdirectory(parent=root, title=testo, initialdir=iniziale))
            if nome:
                v.set(str(Path(nome)))
        ttk.Button(corpo, text="Sfoglia...", command=scegli).grid(row=r, column=2, padx=(6, 0))
        r += 1
        var[chiave] = v

    def testo_libero(chiave, testo, nota="", predefinito=""):
        nonlocal r
        etichetta(testo, nota)
        v = tk.StringVar(value=str(vecchia.get(chiave) or predefinito))
        ttk.Entry(corpo, textvariable=v, width=80).grid(row=r, column=0, columnspan=2, sticky="we")
        r += 1
        var[chiave] = v

    def casella(chiave, testo, predefinito):
        nonlocal r
        v = tk.BooleanVar(value=bool(vecchia.get(chiave, predefinito)))
        ttk.Checkbutton(corpo, text=testo, variable=v).grid(row=r, column=0, columnspan=3, sticky="w", pady=(4, 0))
        r += 1
        var[chiave] = v

    percorso("workbook", "Registro (NFR_Registro.xlsx)", "Nella cartella sincronizzata di Report_Trimestrali. Se non "
             "c'e' ancora, scegliere la cartella e scrivere il nome NFR_Registro.xlsx: si crea con inizializza (guida, 0.4).", file=True)
    percorso("kernel", "Cartella Kernel", "La cartella sincronizzata della library Kernel.")
    percorso("cartella_uscita", "Cartella Archivio_Cicli", "La cartella sincronizzata della library Archivio_Cicli.")
    percorso("news_inbox", "Cartella News_Inbox", "La cartella sincronizzata della library News_Inbox.")
    testo_libero("utente", "Il tuo nome e la funzione", "Lo vedono i colleghi quando stai scrivendo nel registro.")
    testo_libero("validatore_predefinito", "Chi valida di solito", "L'app lo propone; si cambia ogni volta.",
                 "Funzione Risk Management")
    casella("raccolta_su_questo_pc", "Questo e' il PC che raccoglie le notizie il lunedi' (uno solo per tutti)", True)
    casella("ascolta_appunti", "Prendere da sola la risposta dell'agente quando premo Copia", True)
    casella("chiedi_a5", "Chiedere se usare A5 Challenger dopo il precontrollo", True)

    etichetta("Agenti", "Versione degli agenti e i loro link (Agent Builder: ... -> Copia collegamento; guida 0.2, "
              "punto 3-bis). Un link vuoto: l'agente si apre a mano.")
    origine = tk.StringVar(value=origine_iniziale)
    scelta = ttk.Combobox(corpo, textvariable=origine, values=ins.ORIGINI, state="readonly", width=20)
    scelta.grid(row=r, column=0, sticky="w")
    r += 1
    riquadro = ttk.Frame(corpo)
    riquadro.grid(row=r, column=0, columnspan=3, sticky="we")
    r += 1
    link_var = {}
    for i, agente in enumerate(ins.AGENTI):
        ttk.Label(riquadro, text=agente, width=4).grid(row=i, column=0, sticky="w")
        link_var[agente] = tk.StringVar()
        ttk.Entry(riquadro, textvariable=link_var[agente], width=90).grid(row=i, column=1, sticky="we", pady=1)
    # link piatti (una versione sola): sono della versione in uso; l'altra parte vuota
    per_versione = any(isinstance(v, dict) for v in (vecchia.get("link_agenti") or {}).values())
    letti = {o: {a: ("" if ins.SEGNAPOSTO in v else v) for a, v in ins.link_della_versione(vecchia, o).items()}
             if per_versione or o == origine_iniziale else {a: "" for a in ins.AGENTI} for o in ins.ORIGINI}

    def mostra_link(*_):
        for a, v in link_var.items():
            valore = letti[origine.get()].get(a, "")
            v.set("" if ins.SEGNAPOSTO in valore else valore)
    precedente = {"o": origine.get()}

    def cambia_origine(_):
        letti[precedente["o"]] = {a: v.get().strip() for a, v in link_var.items()}
        precedente["o"] = origine.get()
        mostra_link()
    scelta.bind("<<ComboboxSelected>>", cambia_origine)
    mostra_link()

    def salva():
        letti[origine.get()] = {a: v.get().strip() for a, v in link_var.items()}
        nuova = {k: (v.get().strip() if isinstance(v, tk.StringVar) else bool(v.get())) for k, v in var.items()}
        nuova["agenti"] = origine.get()
        conf = vecchia
        for o in ins.ORIGINI:                        # i link di entrambe le versioni, se scritti
            if any(letti[o].values()) or o == origine.get() or o == origine_iniziale:
                conf = ins.unisci(conf, {"link_agenti": letti[o]}, o)
        conf = ins.unisci(conf, nuova, origine.get())
        gravi, avvisi = ins.problemi(conf)
        if gravi and not messagebox.askyesno("Configurazione", "Da sistemare:\n- " + "\n- ".join(gravi) +
                                             "\n\nSalvare lo stesso?", parent=root):
            return
        esito["conf"] = conf
        root.destroy()
    pulsanti = ttk.Frame(corpo)
    pulsanti.grid(row=r, column=0, columnspan=3, sticky="e", pady=(12, 0))
    ttk.Button(pulsanti, text="Annulla", command=root.destroy).pack(side="left", padx=6)
    ttk.Button(pulsanti, text="Salva", command=salva).pack(side="left")
    corpo.columnconfigure(0, weight=1)
    root.mainloop()
    return esito.get("conf")


def passo_configurazione(con_finestra=True):
    titolo(3, "Configurazione (configurazione.json)")
    vecchia = ins.carica_configurazione(FILE_CONF)
    if not vecchia and (QUI / "configurazione_esempio.json").exists() and not con_finestra:
        print("NO: configurazione.json non c'e' e --senza-finestra: copiare configurazione_esempio.json e compilarlo "
              "(guida, 0.3).")
        return {}
    if con_finestra:
        if vecchia:
            print("Si apre la finestra con i valori di adesso: correggere cio' che serve e Salva.")
        else:
            print("Si apre la finestra: indicare cartelle, nome e link, poi Salva.")
        conf = finestra_configurazione(vecchia)
        if conf is None:
            print("Annullato: configurazione.json non cambiato.")
            conf = vecchia
        else:
            print(f"OK: salvato {ins.salva_configurazione(FILE_CONF, conf)}")
    else:
        conf = vecchia
    gravi, avvisi = ins.problemi(conf)
    for g in gravi:
        print(f"NO: {g}")
    for a in avvisi:
        print(f"ATTENZIONE: {a}")
    if not gravi and not avvisi:
        print("OK: configurazione completa")
    return conf


# ------------------------------------------------------------ 4-6. collegamenti, attivita', OneDrive
def passo_collegamenti():
    titolo(4, "Collegamenti")
    if os.name != "nt":
        print("Saltato: non e' Windows.")
        return
    for speciale, nome, dest, argomenti, cartella, descrizione in ins.collegamenti():
        codice, uscita = esegui(ins.comando_powershell(ins.script_collegamento(speciale, nome, dest, argomenti, cartella, descrizione)))
        if codice == 0:
            print(f"OK: {uscita.strip().splitlines()[-1] if uscita.strip() else nome}")
        else:
            print(f"ATTENZIONE: {nome} non creato ({uscita.strip()[-400:]}). A mano: tasto destro sul file -> Mostra "
                  "altre opzioni -> Invia a -> Desktop (crea collegamento).")


def passo_attivita(conf):
    titolo(5, "Raccolta delle notizie del lunedi'")
    if not conf.get("raccolta_su_questo_pc", True):
        print("Saltato: questo non e' il PC della raccolta (raccolta_su_questo_pc = false).")
        return
    if os.name != "nt":
        print("Saltato: non e' Windows.")
        return
    xml = ins.xml_attivita(ins.eseguibile_senza_finestra(), QUI / "raccogli_notizie.py", QUI)
    with tempfile.TemporaryDirectory() as tmp:
        file = Path(tmp) / "attivita.xml"
        file.write_text(xml, encoding="utf-16")
        codice, uscita = esegui(ins.comando_attivita(file))
    if codice == 0:
        print(f"OK: attivita' \"{ins.NOME_ATTIVITA}\" ogni lunedi' alle 7 (se il PC e' spento, appena si accende).")
    else:
        print(f"ATTENZIONE: attivita' non creata ({uscita.strip()[-400:]}). Se le regole del PC non lo permettono, "
              "a mano dall'Utilita' di pianificazione (guida, sezione 1) o chiedere all'IT.")


def passo_onedrive(conf, chiedi=input):
    titolo(6, "Cartelle sincronizzate sempre su questo PC")
    if os.name != "nt":
        print("Saltato: non e' Windows.")
        return
    cartelle = [Path(conf[k]) for k in ("kernel", "cartella_uscita", "news_inbox") if conf.get(k) and Path(conf[k]).is_dir()]
    if conf.get("workbook") and Path(conf["workbook"]).parent.is_dir():
        cartelle.append(Path(conf["workbook"]).parent)
    if not cartelle:
        print("Saltato: nessuna cartella sincronizzata trovata.")
        return
    risposta = chiedi("Tenere sempre su questo PC le cartelle sincronizzate (Mantieni sempre su questo dispositivo)? "
                      "Consigliato: Excel e lo script non aspettano i download. [S/n] ").strip().lower()
    if risposta not in ("", "s", "si", "si'", "y"):
        print("Saltato.")
        return
    for c in cartelle:
        esiti = [esegui(cmd)[0] for cmd in ins.comandi_mantieni_sul_pc(c)]
        print(("OK: " if not any(esiti) else "ATTENZIONE (da fare con il tasto destro -> Mantieni sempre su questo "
               "dispositivo): ") + str(c))


# ------------------------------------------------------------ 7. verifica
def passo_verifica():
    titolo(7, "Verifica del PC")
    import verifica_pc
    return verifica_pc.main([])


def main(argv=None):
    p = argparse.ArgumentParser(description="Installazione dell'app NFR su questo PC")
    p.add_argument("--senza-finestra", action="store_true", help="non apre la finestra della configurazione")
    p.add_argument("--senza-collegamenti", action="store_true")
    p.add_argument("--senza-attivita", action="store_true", help="non crea l'attivita' della raccolta")
    p.add_argument("--solo-verifica", action="store_true")
    arg = p.parse_args(argv)
    if arg.solo_verifica:
        return passo_verifica()
    print("Installazione dell'app NFR Horizon Scan su questo PC. Rilanciarla non fa danni.")
    if not passo_python() or not passo_moduli():
        print("\nInstallazione ferma: sistemare il punto NO qui sopra e rilanciare installa.cmd.")
        return 1
    conf = passo_configurazione(not arg.senza_finestra)
    if not arg.senza_collegamenti:
        passo_collegamenti()
    if not arg.senza_attivita:
        passo_attivita(conf)
    passo_onedrive(conf)
    codice = passo_verifica()
    print("\nInstallazione finita." + (" Aprire l'app dal collegamento \"NFR Horizon Scan\" sul Desktop." if codice == 0 else
                                       " Ci sono punti NO nella verifica: sistemarli e rilanciare installa.cmd."))
    return codice


if __name__ == "__main__":
    sys.exit(main())
