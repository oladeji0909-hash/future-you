from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from datetime import timedelta
from jose import JWTError, jwt
import pyotp
import qrcode
import io
import base64

from app.core.database import get_db
from app.core.security import (
    verify_password, 
    get_password_hash, 
    create_access_token,
    MessageEncryption
)
from app.core.config import settings
from app.models.user import User
from app.models.companion import AICompanion, CompanionPersonality
from app.api.schemas import UserCreate, UserLogin, Token, UserResponse, TwoFactorSetup, TwoFactorVerify
from app.services.email_service import EmailService

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

# Dependency to get current user from token
async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """Get current authenticated user"""
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception
    
    return user

@router.post("/signup", response_model=Token, status_code=status.HTTP_201_CREATED)
async def signup(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    
    # Check if user exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create user
    user = User(
        email=user_data.email,
        hashed_password=get_password_hash(user_data.password),
        full_name=user_data.full_name,
        encryption_key=MessageEncryption.generate_user_key()
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    # Create AI Companion for user
    companion = AICompanion(
        user_id=user.id,
        personality=CompanionPersonality.SUPPORTIVE_FRIEND
    )
    db.add(companion)
    db.commit()
    
    # Send welcome email
    EmailService.send_welcome_email(
        user_email=user.email,
        user_name=user.full_name or "there"
    )
    
    # Generate access token
    access_token = create_access_token(
        data={"sub": user.email, "user_id": user.id}
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }

@router.post("/login", response_model=Token)
async def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """Login user"""
    
    # Find user
    user = db.query(User).filter(User.email == credentials.email).first()
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    # Check if account is active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is disabled"
        )
    
    # Generate access token
    access_token = create_access_token(
        data={"sub": user.email, "user_id": user.id}
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }

@router.post("/2fa/setup", response_model=TwoFactorSetup)
async def setup_2fa(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Setup 2FA for user"""
    
    # Generate TOTP secret
    secret = pyotp.random_base32()
    
    # Create provisioning URI
    totp_uri = pyotp.totp.TOTP(secret).provisioning_uri(
        name=current_user.email,
        issuer_name="Future You"
    )
    
    # Generate QR code
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(totp_uri)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    qr_code_base64 = base64.b64encode(buffer.getvalue()).decode()
    
    # Save secret (not enabled yet)
    current_user.totp_secret = secret
    db.commit()
    
    return {
        "secret": secret,
        "qr_code": f"data:image/png;base64,{qr_code_base64}"
    }

@router.post("/2fa/verify")
async def verify_2fa(
    verification: TwoFactorVerify,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Verify and enable 2FA"""
    
    if not current_user.totp_secret:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="2FA not set up"
        )
    
    # Verify code
    totp = pyotp.TOTP(current_user.totp_secret)
    if not totp.verify(verification.code):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid verification code"
        )
    
    # Enable 2FA
    current_user.is_2fa_enabled = True
    db.commit()
    
    return {"message": "2FA enabled successfully"}

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current user information"""
    return current_user
