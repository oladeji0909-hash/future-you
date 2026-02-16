# 🚀 SIMPLE START GUIDE (No Docker Needed!)

## Step 1: Install Requirements

### Install Python (if not installed)
1. Go to https://www.python.org/downloads/
2. Download Python 3.11+
3. Install (check "Add to PATH")

### Install Node.js (if not installed)
1. Go to https://nodejs.org/
2. Download LTS version
3. Install

## Step 2: Setup (First Time Only)

```bash
# Run this once
SETUP.bat
```

This installs all dependencies (~5 minutes)

## Step 3: Start the App

```bash
# Run this every time
START_SIMPLE.bat
```

Two windows will open:
- Backend (black window)
- Frontend (opens browser automatically)

## Step 4: Test!

Browser opens to: http://localhost:3000

### Quick Test:
1. Click "Sign up"
2. Enter email: test@test.com
3. Enter password: password123
4. Click "Sign Up"
5. ✅ You're in!

## 🎯 What Works Without Docker:

✅ User signup/login  
✅ Create messages  
✅ View messages  
✅ Dashboard  
⚠️ AI Companion (needs OpenAI API key)  

## 🔧 Add AI Companion (Optional):

1. Get free API key: https://platform.openai.com/api-keys
2. Edit `backend\.env`
3. Change: `OPENAI_API_KEY=your-key-here`
4. Restart backend
5. ✅ AI Companion works!

## 🛑 To Stop:

Press `Ctrl+C` in both windows

## ❓ Troubleshooting:

### "Python not found"
- Install Python from python.org
- Restart terminal

### "Node not found"
- Install Node.js from nodejs.org
- Restart terminal

### "Port already in use"
- Close other apps using port 8000 or 3000
- Or restart computer

### Backend errors
- Check `backend\.env` file exists
- Run `SETUP.bat` again

---

**Just run: `SETUP.bat` then `START_SIMPLE.bat`** 🎉
