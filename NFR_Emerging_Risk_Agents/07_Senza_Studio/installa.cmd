@echo off
rem Installazione dell'app NFR su questo PC (D-83, tappa M3). Solo testo ASCII in questo file.
rem Controlla Python e i moduli, installa con pip --user cio' che manca, chiede la configurazione,
rem crea i collegamenti e, sul PC della raccolta, l'attivita' del lunedi'; alla fine la Verifica del PC.
chcp 65001 >nul
set PYTHONIOENCODING=utf-8
cd /d "%~dp0"
where py >nul 2>nul && (py -3 "%~dp0installa.py" %* & goto fine)
where python >nul 2>nul && (python "%~dp0installa.py" %* & goto fine)
echo Python non trovato. Chiedere all'informatica Python 3.10 o piu' recente (python.org o Software Center),
echo con l'opzione "Add python.exe to PATH"; poi rilanciare installa.cmd.
:fine
pause
