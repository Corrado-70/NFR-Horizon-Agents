"""Appunti di Windows per l'app NFR (D-83, tappa M2).

L'analista preme "Copia" sotto la risposta di un agente: l'app se ne accorge dal numero di sequenza degli appunti
(cambia a ogni copia) e legge il testo. Le copie fatte dall'app stessa (la richiesta per l'agente, un messaggio di
correzione) si ignorano. Con pywin32 (gia' richiesto dal motore); se manca o se le politiche del PC bloccano gli
appunti, l'app lo dice e resta il pulsante "Scegli file...".
"""

import time

try:
    import win32clipboard
    import win32con
except ImportError:                                  # senza pywin32: l'app usa solo i file
    win32clipboard = None


def disponibili():
    return win32clipboard is not None


def sequenza():
    return win32clipboard.GetClipboardSequenceNumber() if win32clipboard else 0


def _con_appunti(funzione):
    """Gli appunti possono essere occupati da un altro programma per qualche millisecondo: si riprova."""
    for tentativo in range(10):
        try:
            win32clipboard.OpenClipboard()
        except Exception:                            # noqa: BLE001 - occupati: si riprova
            time.sleep(0.05 * (tentativo + 1))
            continue
        try:
            return funzione()
        finally:
            win32clipboard.CloseClipboard()
    raise OSError("appunti occupati da un altro programma")


def leggi():
    """Il testo negli appunti, o '' se non c'e' testo."""
    if not win32clipboard:
        return ""

    def _leggi():
        if win32clipboard.IsClipboardFormatAvailable(win32con.CF_UNICODETEXT):
            return win32clipboard.GetClipboardData(win32con.CF_UNICODETEXT) or ""
        return ""
    return _con_appunti(_leggi)


def scrivi(testo):
    """Mette il testo negli appunti; restituisce il numero di sequenza della propria copia (da ignorare)."""
    if not win32clipboard:
        return 0

    def _scrivi():
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32con.CF_UNICODETEXT, str(testo))
    _con_appunti(_scrivi)
    return sequenza()


class Ascolto:
    """Segnala una copia nuova, fatta da un altro programma dopo l'inizio dell'ascolto."""

    def __init__(self):
        self.ultima = sequenza()
        self.mie = set()

    def ricomincia(self):
        self.ultima = sequenza()

    def scritta_da_me(self, numero):
        self.mie.add(numero)
        self.ultima = max(self.ultima, numero)

    def nuova(self):
        """Il testo di una copia nuova, o None."""
        n = sequenza()
        if not n or n == self.ultima:
            return None
        self.ultima = n
        if n in self.mie:
            return None
        try:
            return leggi() or None
        except OSError:
            return None
