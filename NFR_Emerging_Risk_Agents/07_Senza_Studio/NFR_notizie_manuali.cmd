@echo off
rem "Invia a -> NFR notizie manuali" (D-83, tappa M3): copia i file scelti in News_Inbox\<lunedi>\Manuali.
rem Solo testo ASCII in questo file.
chcp 65001 >nul
set PYTHONIOENCODING=utf-8
cd /d "%~dp0"
where py >nul 2>nul && (py -3 "%~dp0notizie_manuali.py" %* & goto fine)
where python >nul 2>nul && (python "%~dp0notizie_manuali.py" %* & goto fine)
echo Python non trovato: lanciare installa.cmd (guida, sezione 0.3).
:fine
timeout /t 8
