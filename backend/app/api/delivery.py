from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.user import User
from app.api.auth import get_current_user
from app.services.delivery_service import DeliveryService

router = APIRouter()

@router.get("/stats")
async def get_delivery_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get overall delivery statistics"""
    return DeliveryService.get_delivery_stats(db)

@router.get("/upcoming")
async def get_upcoming_deliveries(
    days: int = 7,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get messages scheduled for delivery in the next N days"""
    return DeliveryService.get_upcoming_deliveries(db, days)

@router.get("/overdue")
async def get_overdue_deliveries(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get messages that should have been delivered but weren't"""
    return DeliveryService.get_overdue_deliveries(db)

@router.get("/timeline")
async def get_delivery_timeline(
    days: int = 30,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get delivery timeline for charts"""
    return DeliveryService.get_delivery_timeline(db, days)

@router.get("/my-stats")
async def get_my_delivery_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get delivery stats for current user"""
    return DeliveryService.get_user_delivery_stats(current_user.id, db)

@router.post("/mark-read/{message_id}")
async def mark_message_as_read(
    message_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Mark a message as read"""
    success = DeliveryService.mark_as_read(message_id, current_user.id, db)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found or already read"
        )
    
    return {"message": "Message marked as read"}

@router.get("/performance")
async def get_delivery_performance(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get delivery performance metrics"""
    return DeliveryService.get_delivery_performance(db)
