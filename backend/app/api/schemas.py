from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)
    full_name: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: "UserResponse"

class UserResponse(BaseModel):
    id: int
    email: str
    full_name: Optional[str]
    is_active: bool
    is_verified: bool
    is_admin: bool
    subscription_tier: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class TwoFactorSetup(BaseModel):
    secret: str
    qr_code: str

class TwoFactorVerify(BaseModel):
    code: str
