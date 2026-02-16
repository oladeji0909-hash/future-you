@echo off
echo ========================================
echo   Moving Project Out of OneDrive
echo ========================================
echo.

echo Creating new location: C:\Projects\FutureYou
mkdir C:\Projects 2>nul
mkdir C:\Projects\FutureYou 2>nul

echo.
echo Copying files...
xcopy /E /I /Y "%~dp0*" "C:\Projects\FutureYou\"

echo.
echo ========================================
echo   Move Complete!
echo ========================================
echo.
echo New location: C:\Projects\FutureYou
echo.
echo Next steps:
echo 1. Close this window
echo 2. Open: C:\Projects\FutureYou
echo 3. Run: START_SIMPLE.bat
echo.
pause

cd /d C:\Projects\FutureYou
explorer .
