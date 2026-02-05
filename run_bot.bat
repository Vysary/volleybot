@echo off
REM Script batch pour lancer le bot avec redémarrage automatique

setlocal enabledelayedexpansion
cd /d "c:\Users\Lilia\iCloudDrive\Volley\VolleyBot"

echo [%date% %time%] Demarrage du bot VolleyBot... >> bot_logs.txt

:start_bot
python main.py
echo [%date% %time%] Bot arrête. Redemarrage dans 10 secondes... >> bot_logs.txt
echo Le bot s'est arrete. Redemarrage dans 10 secondes...
timeout /t 10 /nobreak
goto start_bot
