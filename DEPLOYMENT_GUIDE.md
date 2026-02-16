# 🚀 Deployment Guide - Future You

## Quick Deploy (Recommended)

### Option 1: Railway (Easiest - 10 mins)
**Backend + Database**
1. Go to [railway.app](https://railway.app)
2. Click "Start a New Project" → "Deploy from GitHub"
3. Connect repo, select `backend` folder
4. Add PostgreSQL database (auto-configured)
5. Set environment variables (see below)
6. Deploy! Get your backend URL

**Frontend**
1. Go to [vercel.com](https://vercel.com)
2. Import GitHub repo
3. Set root directory to `frontend`
4. Add env: `REACT_APP_API_URL=<your-railway-backend-url>`
5. Deploy! Get your frontend URL

**Cost**: $5/month (Railway) + $0 (Vercel free tier)

---

## Environment Variables (Production)

### Backend (.env)
```bash
# Database (Railway auto-provides)
DATABASE_URL=postgresql://...
REDIS_URL=redis://...

# Security (GENERATE NEW KEYS!)
SECRET_KEY=<run: openssl rand -hex 32>
ENCRYPTION_KEY=<run: openssl rand -hex 32>

# OpenAI
OPENAI_API_KEY=sk-...

# Stripe
STRIPE_SECRET_KEY=sk_live_...
STRIPE_PUBLISHABLE_KEY=pk_live_...
STRIPE_WEBHOOK_SECRET=whsec_...

# Email (Gmail)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=<app-password>

# App
ENVIRONMENT=production
DEBUG=False
CORS_ORIGINS=https://your-frontend-url.vercel.app
```

### Frontend (.env.production)
```bash
REACT_APP_API_URL=https://your-backend.railway.app
```

---

## Pre-Launch Checklist

### Security ✅
- [ ] Generate new SECRET_KEY and ENCRYPTION_KEY
- [ ] Set DEBUG=False in production
- [ ] Update CORS_ORIGINS to production URL
- [ ] Enable HTTPS only
- [ ] Set up Stripe webhook endpoint

### Database ✅
- [ ] Migrate from SQLite to PostgreSQL
- [ ] Run migrations: `alembic upgrade head`
- [ ] Backup strategy in place

### Monitoring 📊
- [ ] Set up error tracking (Sentry)
- [ ] Enable logging
- [ ] Monitor API performance

### Business 💰
- [ ] Stripe account in live mode
- [ ] Payment webhooks configured
- [ ] Email sending configured
- [ ] Terms of Service page
- [ ] Privacy Policy page

---

## Post-Launch (Week 1)

1. **Monitor**: Check logs daily for errors
2. **Test**: Create test account, send test message
3. **Iterate**: Fix critical bugs immediately
4. **Market**: Share on Twitter, Reddit, Product Hunt
5. **Collect**: Get user feedback via email/chat

---

## Alternative Hosting Options

### Option 2: AWS (Scalable)
- **Backend**: Elastic Beanstalk or ECS
- **Frontend**: S3 + CloudFront
- **Database**: RDS PostgreSQL
- **Cost**: ~$20-50/month

### Option 3: DigitalOcean (Simple)
- **Backend**: App Platform
- **Frontend**: App Platform
- **Database**: Managed PostgreSQL
- **Cost**: ~$12-25/month

---

## Need Help?
- Railway docs: https://docs.railway.app
- Vercel docs: https://vercel.com/docs
- Stripe webhooks: https://stripe.com/docs/webhooks

**You're ready to launch! 🎉**
