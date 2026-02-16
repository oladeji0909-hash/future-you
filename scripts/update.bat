@echo off
echo ========================================
echo   Future You - Quick Update Script
echo ========================================
echo.

echo [1/4] Pulling latest changes...
git pull origin main
if %errorlevel% neq 0 (
    echo ERROR: Failed to pull changes
    pause
    exit /b 1
)

echo.
echo [2/4] Installing backend dependencies...
cd backend
pip install -r requirements.txt
cd ..

echo.
echo [3/4] Installing frontend dependencies...
cd frontend
call npm install
cd ..

echo.
echo [4/4] Running database migrations...
cd backend
alembic upgrade head
cd ..

echo.
echo ========================================
echo   Update Complete! 
echo ========================================
echo.
echo To start the app:
echo   Backend:  cd backend ^&^& python -m uvicorn app.main:app --reload
echo   Frontend: cd frontend ^&^& npm start
echo.
pause
