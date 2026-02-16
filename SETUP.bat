@echo off
echo ========================================
echo   Future You - First Time Setup
echo ========================================
echo.

echo [1/4] Checking Python...
python --version
if %errorlevel% neq 0 (
    echo ERROR: Python not found. Install from python.org
    pause
    exit /b 1
)

echo.
echo [2/4] Installing Backend Dependencies...
cd backend
pip install fastapi uvicorn sqlalchemy pydantic pydantic-settings python-jose passlib python-multipart email-validator cryptography pycryptodome openai python-dotenv httpx aiofiles pillow pyotp qrcode slowapi alembic bcrypt
cd ..

echo.
echo [3/4] Checking Node.js...
node --version
if %errorlevel% neq 0 (
    echo ERROR: Node.js not found. Install from nodejs.org
    pause
    exit /b 1
)

echo.
echo [4/4] Installing Frontend Dependencies...
cd frontend
call npm install --legacy-peer-deps
cd ..

echo.
echo ========================================
echo   Setup Complete!
echo ========================================
echo.
echo Next: Run START_SIMPLE.bat to launch the app
echo.
pause
