from pydantic_settings import BaseSettings
from typing import List, Optional

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "sqlite:///./futureyou.db"
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # Security
    SECRET_KEY: str = "dev-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ENCRYPTION_KEY: str = "dev-encryption-key-change-in-production"
    
    # OpenAI
    OPENAI_API_KEY: str = "sk-test"
    
    # AWS (optional)
    AWS_ACCESS_KEY_ID: str = ""
    AWS_SECRET_ACCESS_KEY: str = ""
    AWS_S3_BUCKET: str = ""
    AWS_REGION: str = "us-east-1"
    
    # Stripe
    STRIPE_SECRET_KEY: str = "sk_test_"
    STRIPE_PUBLISHABLE_KEY: str = "pk_test_"
    STRIPE_WEBHOOK_SECRET: str = "whsec_test"
    
    # Email (optional)
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    
    # Blockchain (optional)
    WEB3_PROVIDER_URL: str = ""
    CONTRACT_ADDRESS: str = ""
    
    # IPFS (optional)
    IPFS_HOST: str = "127.0.0.1"
    IPFS_PORT: int = 5001
    
    # App
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    CORS_ORIGINS: str = "http://localhost:3000"
    
    @property
    def cors_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
