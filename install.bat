@echo off
title House of Shinobi - Mod Installer
color 0B
echo ========================================================
echo        House of Shinobi (HoS) - Mod Installer
echo ========================================================
echo.

set "TARGET_DIR=%~dp0"
if exist "%TARGET_DIR%HoS.py" goto INSTALL_HERE
if exist "%TARGET_DIR%HoS.exe" goto INSTALL_HERE

echo Looking for House of Shinobi directory...
set /p "TARGET_DIR=Enter path to your House of Shinobi game folder: "

:INSTALL_HERE
if not exist "%TARGET_DIR%\game\python-packages" (
    echo [ERROR] Could not find 'game\python-packages' in %TARGET_DIR%
    echo Please make sure you selected the main game directory.
    pause
    exit /b 1
)

echo.
echo Installing mod files into "%TARGET_DIR%\game\python-packages\"...
copy /Y "%~dp0game\python-packages\hos_mod.py" "%TARGET_DIR%\game\python-packages\" >nul
copy /Y "%~dp0game\python-packages\guide_logic.py" "%TARGET_DIR%\game\python-packages\" >nul

if exist "%TARGET_DIR%\game\cache" (
    echo Cleaning stale cache files...
    del /Q "%TARGET_DIR%\game\cache\*.rpyb" 2>nul
)

echo.
echo ========================================================
echo   [SUCCESS] House of Shinobi Mod Installed Successfully!
echo ========================================================
echo.
echo Controls in Game:
echo   - Click the [MOD] button in the top-right corner
echo   - Press F8 or ~ (backtick) anytime during gameplay
echo.
pause
