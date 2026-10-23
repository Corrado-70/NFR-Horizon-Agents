@echo off
rem App NFR Horizon Scan (D-83): doppio clic per aprire la finestra. Solo testo ASCII in questo file.
chcp 65001 >nul
set PYTHONIOENCODING=utf-8
cd /d "%~dp0"
where pyw >nul 2>nul && (start "" pyw -3 "%~dp0app_nfr.py" & exit /b 0)
where pythonw >nul 2>nul && (start "" pythonw "%~dp0app_nfr.py" & exit /b 0)
where python >nul 2>nul && (python "%~dp0app_nfr.py" & exit /b 0)
echo Python non trovato. Installarlo (guida, sezione 0.3) e riprovare.
pause
