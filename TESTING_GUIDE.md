# 🧪 Testing Guide - See Your App in Action!

## 🚀 Quick Start (5 Minutes)

### Step 1: Setup Environment Variables
```bash
cd backend
copy .env.example .env
```

Edit `.env` file and add:
```env
DATABASE_URL=postgresql://futureyou:futureyou_dev@localhost:5432/futureyou
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=your-secret-key-change-this-in-production
ENCRYPTION_KEY=your-encryption-key-32-characters
OPENAI_API_KEY=sk-your-openai-api-key-here
```

### Step 2: Start with Docker (Easiest)
```bash
# From project root
docker-compose up
```

**That's it!** 🎉
- Backend: http://localhost:8000
- Frontend: http://localhost:3000
- API Docs: http://localhost:8000/api/docs

---

## 🎯 Manual Setup (If Docker Issues)

### Backend Setup
```bash
# 1. Install Python dependencies
cd backend
pip install -r requirements.txt

# 2. Start PostgreSQL (install if needed)
# Windows: Download from postgresql.org
# Or use Docker: docker run -p 5432:5432 -e POSTGRES_PASSWORD=futureyou_dev postgres

# 3. Start Redis (install if needed)
# Windows: Download from redis.io
# Or use Docker: docker run -p 6379:6379 redis

# 4. Run migrations
alembic upgrade head

# 5. Start backend
python -m uvicorn app.main:app --reload
```

Backend running at: http://localhost:8000

### Frontend Setup
```bash
# Open new terminal
cd frontend
npm install
npm start
```

Frontend running at: http://localhost:3000

---

## ✅ Testing Checklist

### 1. Test Authentication ✨
1. Go to http://localhost:3000
2. Click "Sign up"
3. Enter:
   - Name: Test User
   - Email: test@example.com
   - Password: password123
4. Click "Sign Up"
5. ✅ You should be logged in and see Dashboard

### 2. Test Message Creation 📝
1. Click "Messages" card
2. Click "New Message"
3. Type: "Hey future me! Remember to stay positive!"
4. Click "Create Message"
5. ✅ Message appears in list with "AI will choose perfect timing"

### 3. Test AI Companion 🤖
1. Go back to Dashboard
2. Click "Future Buddy" card
3. Type: "Hi! I'm feeling stressed about work"
4. Press Enter or click "Send"
5. ✅ AI responds with supportive message
6. Try: "Help me write a message to my future self"
7. ✅ AI helps craft a message

### 4. Test API Directly 🔧
Visit: http://localhost:8000/api/docs

Try these endpoints:
- POST `/api/auth/signup` - Create user
- POST `/api/auth/login` - Login
- GET `/api/messages/` - Get messages
- POST `/api/companion/chat` - Chat with AI

---

## 🎨 What You Should See

### Dashboard
```
┌─────────────────────────────────────┐
│  Welcome, Test User        [Logout] │
├─────────────────────────────────────┤
│  ┌─────────┐  ┌─────────┐  ┌──────┐│
│  │Messages │  │ Future  │  │Time- ││
│  │    📝   │  │ Buddy🤖 │  │line📊││
│  └─────────┘  └─────────┘  └──────┘│
└─────────────────────────────────────┘
```

### Messages Page
```
┌─────────────────────────────────────┐
│  Your Messages      [New Message]   │
├─────────────────────────────────────┤
│  ┌───────────────────────────────┐  │
│  │ Hey future me! Stay positive! │  │
│  │ [scheduled] [ai_optimal]      │  │
│  └───────────────────────────────┘  │
└─────────────────────────────────────┘
```

### AI Companion Chat
```
┌─────────────────────────────────────┐
│  Future Buddy 🤖                    │
├─────────────────────────────────────┤
│  🤖 Hi! I'm here to support you.   │
│     How are you feeling today?      │
│                                      │
│              I'm stressed 😟  👤    │
│                                      │
│  🤖 I hear you. Let's talk about   │
│     what's causing the stress...    │
└─────────────────────────────────────┘
│ [Type message...]          [Send]   │
└─────────────────────────────────────┘
```

---

## 🧪 Advanced Testing

### Test Encryption
```bash
# In Python console
cd backend
python

>>> from app.core.security import MessageEncryption
>>> key = MessageEncryption.generate_user_key()
>>> encrypted = MessageEncryption.encrypt("Secret message", key)
>>> print(encrypted)  # Should be gibberish
>>> decrypted = MessageEncryption.decrypt(encrypted, key)
>>> print(decrypted)  # "Secret message"
```

### Test AI Companion Personalities
In the app, try different conversation styles:
1. Motivational: "I need motivation"
2. Supportive: "I'm feeling down"
3. Philosophical: "What's the meaning of life?"

### Test Multiple Users
1. Logout
2. Create another account
3. Messages are separate ✅
4. Each has own AI companion ✅

---

## 📊 Performance Testing

### Load Test (Optional)
```bash
# Install locust
pip install locust

# Create locustfile.py
# Run: locust -f locustfile.py
# Open: http://localhost:8089
```

### Check Response Times
```bash
# Backend health
curl http://localhost:8000/health

# Should respond in < 100ms
```

---

## 🐛 Troubleshooting

### Backend won't start
```bash
# Check if port 8000 is in use
netstat -ano | findstr :8000

# Kill process or use different port
python -m uvicorn app.main:app --reload --port 8001
```

### Frontend won't start
```bash
# Clear cache
cd frontend
rm -rf node_modules package-lock.json
npm install
npm start
```

### Database connection error
```bash
# Check PostgreSQL is running
# Windows: Services → PostgreSQL
# Or start Docker container
docker run -p 5432:5432 -e POSTGRES_PASSWORD=futureyou_dev postgres
```

### AI Companion not responding
- Check OPENAI_API_KEY in .env
- Verify you have API credits
- Check backend logs for errors

### CORS errors
- Ensure backend is running on port 8000
- Check CORS_ORIGINS in backend/.env

---

## 📸 Screenshot Checklist

Take screenshots of:
- [ ] Login page
- [ ] Dashboard with 3 cards
- [ ] Message creation form
- [ ] Message list
- [ ] AI Companion chat
- [ ] API documentation page

---

## 🎯 Feature Testing Matrix

| Feature | Status | Test |
|---------|--------|------|
| User Signup | ✅ | Create account |
| User Login | ✅ | Login with credentials |
| JWT Auth | ✅ | Token in localStorage |
| Message Creation | ✅ | Create text message |
| Message Encryption | ✅ | Content encrypted in DB |
| Message List | ✅ | View all messages |
| AI Companion Chat | ✅ | Send/receive messages |
| Personality System | ✅ | Different responses |
| Emotion Detection | ✅ | AI detects mood |
| Dashboard Navigation | ✅ | Navigate between pages |
| Logout | ✅ | Clear session |
| API Documentation | ✅ | Swagger UI works |

---

## 🚀 What's Working

### ✅ Backend (13 Endpoints)
- Authentication (signup, login, 2FA)
- Messages (create, read, delete)
- AI Companion (chat, personality, help)
- Health checks
- API documentation

### ✅ Frontend (5 Pages)
- Login/Signup pages
- Dashboard
- Messages page
- AI Companion chat
- Routing & navigation

### ✅ Security
- Password hashing (bcrypt)
- JWT tokens
- AES-256 encryption
- CORS protection
- Rate limiting
- Security headers

### ✅ AI Features
- 5 personality types
- Emotion detection
- Conversation memory
- Message crafting help
- Context awareness

---

## 📈 Next Steps After Testing

1. **Add more messages** - Test AI timing
2. **Chat with companion** - Test different personalities
3. **Invite friends** - Test multi-user
4. **Check database** - See encrypted data
5. **Review API docs** - Explore all endpoints
6. **Test on mobile** - Responsive design
7. **Deploy to cloud** - See it live!

---

## 🎉 Success Criteria

You've successfully tested when:
- ✅ Can create account and login
- ✅ Can create and view messages
- ✅ AI Companion responds intelligently
- ✅ Navigation works smoothly
- ✅ No console errors
- ✅ Data persists after refresh
- ✅ Encryption working (check DB)

---

## 💡 Testing Tips

1. **Open DevTools** (F12) - Check for errors
2. **Check Network tab** - See API calls
3. **View localStorage** - See JWT token
4. **Check backend logs** - See requests
5. **Test edge cases** - Empty inputs, long text
6. **Test logout/login** - Session management

---

## 🎬 Demo Script

**Show to others:**
1. "This is Future You - messages to your future self"
2. Sign up → "Creating account with encryption"
3. Create message → "AI will deliver at perfect time"
4. Chat with buddy → "Meet my AI companion"
5. Show dashboard → "Clean, intuitive interface"
6. Show API docs → "Full REST API"

---

**Ready to test? Run `docker-compose up` and go to http://localhost:3000!** 🚀
