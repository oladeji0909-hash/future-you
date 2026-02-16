from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from app.core.config import settings
from app.core.database import engine, Base
from app.services.scheduler import scheduler

# Create tables
Base.metadata.create_all(bind=engine)

# Rate limiter
limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title="Future You API",
    description="Messages from your past, delivered at the perfect moment",
    version="1.0.0",
    docs_url="/api/docs" if settings.DEBUG else None,
    redoc_url="/api/redoc" if settings.DEBUG else None,
)

# Rate limiting
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins in development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security headers middleware
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    if not settings.DEBUG:
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    return response

@app.on_event("startup")
async def startup_event():
    """Start background scheduler on app startup"""
    scheduler.start()
    scheduler.add_daily_reminder_job()

@app.on_event("shutdown")
async def shutdown_event():
    """Stop background scheduler on app shutdown"""
    scheduler.shutdown()

@app.get("/")
async def root():
    return {
        "message": "Future You API",
        "version": "1.0.0",
        "status": "operational"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Import and include routers
from app.api import auth, messages, companion, payments, analytics, delivery

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(messages.router, prefix="/api/messages", tags=["messages"])
app.include_router(companion.router, prefix="/api/companion", tags=["companion"])
app.include_router(payments.router, prefix="/api/payments", tags=["payments"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["analytics"])
app.include_router(delivery.router, prefix="/api/delivery", tags=["delivery"])
