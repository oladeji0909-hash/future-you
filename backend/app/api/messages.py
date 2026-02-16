from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.core.database import get_db
from app.core.security import MessageEncryption
from app.models.user import User
from app.models.message import Message, MessageType, MessageStatus, DeliveryTiming
from app.api.auth import get_current_user
from app.services.timing_service import AITimingService
from app.services.payment_service import PaymentService
from pydantic import BaseModel

router = APIRouter()

class MessageCreate(BaseModel):
    content: str
    message_type: MessageType = MessageType.TEXT
    delivery_timing: DeliveryTiming = DeliveryTiming.AI_OPTIMAL
    scheduled_for: datetime = None
    tags: List[str] = []
    category: str = None

class MessageResponse(BaseModel):
    id: int
    content: str
    message_type: str
    status: str
    delivery_timing: str
    scheduled_for: datetime | None = None
    delivered_at: datetime | None = None
    created_at: datetime
    tags: List[str]
    delivery_explanation: str | None = None
    
    class Config:
        from_attributes = True

@router.post("/", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
async def create_message(
    message_data: MessageCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new message to future self"""
    
    # Check message limit based on subscription tier
    limit_check = PaymentService.check_message_limit(current_user, db)
    if not limit_check["allowed"]:
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail={
                "message": "Message limit reached for your tier",
                "limit": limit_check["limit"],
                "upgrade_required": True
            }
        )
    
    # Encrypt message content
    encrypted_content = MessageEncryption.encrypt(
        message_data.content,
        current_user.encryption_key
    )
    
    # Calculate optimal delivery time using AI
    optimal_delivery = AITimingService.calculate_optimal_delivery(
        message_content=message_data.content,
        user_id=current_user.id,
        delivery_timing=message_data.delivery_timing,
        db=db,
        scheduled_for=message_data.scheduled_for
    )
    
    # Get message context for explanation
    message_context = AITimingService._analyze_message_context(message_data.content)
    delivery_explanation = AITimingService.get_delivery_explanation(
        message_data.delivery_timing,
        optimal_delivery,
        message_context
    )
    
    # Create message
    message = Message(
        user_id=current_user.id,
        encrypted_content=encrypted_content,
        message_type=message_data.message_type,
        delivery_timing=message_data.delivery_timing,
        scheduled_for=optimal_delivery,
        tags=message_data.tags,
        category=message_data.category,
        status=MessageStatus.SCHEDULED
    )
    
    db.add(message)
    db.commit()
    db.refresh(message)
    
    # Decrypt for response
    decrypted_content = MessageEncryption.decrypt(
        message.encrypted_content,
        current_user.encryption_key
    )
    
    response = MessageResponse(
        id=message.id,
        content=decrypted_content,
        message_type=message.message_type.value,
        status=message.status.value,
        delivery_timing=message.delivery_timing.value,
        scheduled_for=message.scheduled_for,
        delivered_at=message.delivered_at,
        created_at=message.created_at,
        tags=message.tags,
        delivery_explanation=delivery_explanation
    )
    
    return response

@router.get("/", response_model=List[MessageResponse])
async def get_messages(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    status: MessageStatus = None
):
    """Get all messages for current user"""
    
    query = db.query(Message).filter(Message.user_id == current_user.id)
    
    if status:
        query = query.filter(Message.status == status)
    
    messages = query.order_by(Message.created_at.desc()).all()
    
    # Decrypt messages
    response = []
    for message in messages:
        decrypted_content = MessageEncryption.decrypt(
            message.encrypted_content,
            current_user.encryption_key
        )
        response.append(MessageResponse(
            id=message.id,
            content=decrypted_content,
            message_type=message.message_type.value,
            status=message.status.value,
            delivery_timing=message.delivery_timing.value,
            scheduled_for=message.scheduled_for,
            delivered_at=message.delivered_at,
            created_at=message.created_at,
            tags=message.tags
        ))
    
    return response

@router.get("/{message_id}", response_model=MessageResponse)
async def get_message(
    message_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get specific message"""
    
    message = db.query(Message).filter(
        Message.id == message_id,
        Message.user_id == current_user.id
    ).first()
    
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found"
        )
    
    decrypted_content = MessageEncryption.decrypt(
        message.encrypted_content,
        current_user.encryption_key
    )
    
    return MessageResponse(
        id=message.id,
        content=decrypted_content,
        message_type=message.message_type.value,
        status=message.status.value,
        delivery_timing=message.delivery_timing.value,
        scheduled_for=message.scheduled_for,
        delivered_at=message.delivered_at,
        created_at=message.created_at,
        tags=message.tags
    )

@router.delete("/{message_id}")
async def delete_message(
    message_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a message"""
    
    message = db.query(Message).filter(
        Message.id == message_id,
        Message.user_id == current_user.id
    ).first()
    
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found"
        )
    
    db.delete(message)
    db.commit()
    
    return {"message": "Message deleted successfully"}
