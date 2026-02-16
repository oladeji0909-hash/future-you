@echo off
echo ========================================
echo   Future You - Simple Start
echo ========================================
echo.

echo [1/2] Starting Backend...
start cmd /k "cd backend && python -m uvicorn app.main:app --reload --port 8005"
timeout /t 3 >nul

echo [2/2] Starting Frontend...
start cmd /k "cd frontend && set PORT=3005 && npm start"

echo.
echo ========================================
echo   Starting...
echo ========================================
echo.
echo Backend: http://localhost:8005
echo Frontend: http://localhost:3005 (opens automatically)
echo API Docs: http://localhost:8005/api/docs
echo.
echo Press Ctrl+C in each window to stop
echo.
pause
