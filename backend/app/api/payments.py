from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.core.database import get_db
from app.models.user import User, SubscriptionTier
from app.api.auth import get_current_user
from app.services.payment_service import PaymentService

router = APIRouter()

class CheckoutRequest(BaseModel):
    tier: SubscriptionTier
    success_url: str
    cancel_url: str

class CheckoutResponse(BaseModel):
    session_id: str
    url: str

@router.post("/create-checkout-session", response_model=CheckoutResponse)
async def create_checkout_session(
    request: CheckoutRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create Stripe checkout session for subscription upgrade"""
    
    if request.tier == SubscriptionTier.FREE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot checkout for free tier"
        )
    
    if current_user.subscription_tier != SubscriptionTier.FREE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Already subscribed. Use customer portal to manage subscription."
        )
    
    result = PaymentService.create_checkout_session(
        user_id=current_user.id,
        user_email=current_user.email,
        tier=request.tier,
        success_url=request.success_url,
        cancel_url=request.cancel_url
    )
    
    if "error" in result:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=result["error"]
        )
    
    return result

@router.post("/create-portal-session")
async def create_portal_session(
    return_url: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create Stripe customer portal session for managing subscription"""
    
    if not current_user.stripe_customer_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No active subscription found"
        )
    
    result = PaymentService.create_customer_portal_session(
        customer_id=current_user.stripe_customer_id,
        return_url=return_url
    )
    
    if "error" in result:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=result["error"]
        )
    
    return result

@router.post("/webhook")
async def stripe_webhook(
    request: Request,
    db: Session = Depends(get_db)
):
    """Handle Stripe webhook events"""
    
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")
    
    if not sig_header:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing stripe-signature header"
        )
    
    result = PaymentService.handle_webhook_event(payload, sig_header)
    
    if "error" in result:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result["error"]
        )
    
    # Process the webhook action
    if result.get("action") == "upgrade_user":
        user = db.query(User).filter(User.id == result["user_id"]).first()
        if user:
            user.subscription_tier = SubscriptionTier(result["tier"])
            user.subscription_status = "active"
            user.stripe_customer_id = result.get("stripe_customer_id")
            user.stripe_subscription_id = result.get("stripe_subscription_id")
            db.commit()
    
    elif result.get("action") == "downgrade_user":
        user = db.query(User).filter(User.id == result["user_id"]).first()
        if user:
            user.subscription_tier = SubscriptionTier.FREE
            user.subscription_status = "cancelled"
            db.commit()
    
    elif result.get("action") == "update_subscription_status":
        user = db.query(User).filter(User.id == result["user_id"]).first()
        if user:
            user.subscription_status = result["status"]
            db.commit()
    
    return {"status": "success"}

@router.get("/pricing")
async def get_pricing():
    """Get pricing information for all tiers"""
    return PaymentService.get_pricing_info()

@router.get("/check-limit")
async def check_message_limit(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Check if user can create more messages"""
    return PaymentService.check_message_limit(current_user, db)

@router.get("/mrr")
async def get_mrr(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get Monthly Recurring Revenue (admin only)"""
    
    # In production, add admin check here
    # For now, anyone can see it
    
    return PaymentService.calculate_mrr(db)

@router.get("/subscription")
async def get_subscription_info(
    current_user: User = Depends(get_current_user)
):
    """Get current user's subscription information"""
    
    pricing = PaymentService.get_pricing_info()
    current_tier_info = pricing[current_user.subscription_tier]
    
    return {
        "tier": current_user.subscription_tier.value,
        "status": current_user.subscription_status,
        "features": current_tier_info["features"],
        "message_limit": current_tier_info["message_limit"],
        "price": current_tier_info["price"]
    }
