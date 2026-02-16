@echo off
echo ========================================
echo   Future You - Quick Start
echo ========================================
echo.

echo Checking Docker...
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Docker not found. Please install Docker Desktop.
    echo Download from: https://www.docker.com/products/docker-desktop
    pause
    exit /b 1
)

echo.
echo Starting Future You...
echo.
echo Backend will be at: http://localhost:8000
echo Frontend will be at: http://localhost:3000
echo API Docs will be at: http://localhost:8000/api/docs
echo.

docker-compose up

pause
