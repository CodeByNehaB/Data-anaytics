@echo off
echo Monitoring E:\neha work\Data Analytics for changes...
:loop
git status --porcelain | findstr /R "^" >nul
if %errorlevel% equ 0 (
    echo Notebook update detected! Syncing with GitHub...
    git add .
    git commit -m "Auto-update: %date% %time%"
    git push origin main
)
timeout /t 15 >nul
goto loop
