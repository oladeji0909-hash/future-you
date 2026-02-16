from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.models.user import User
from app.models.companion import AICompanion, CompanionConversation, CompanionPersonality
from app.services.companion_service import AICompanionService
from app.api.auth import get_current_user
from pydantic import BaseModel

router = APIRouter()

class ChatMessage(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    detected_emotion: str
    suggestions: List[str]

class PersonalityUpdate(BaseModel):
    personality: CompanionPersonality
    custom_instructions: str = None

@router.post("/chat", response_model=ChatResponse)
async def chat_with_companion(
    chat_data: ChatMessage,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Chat with AI companion"""
    
    # Get or create user's companion
    companion = db.query(AICompanion).filter(
        AICompanion.user_id == current_user.id
    ).first()
    
    if not companion:
        companion = AICompanion(
            user_id=current_user.id,
            personality=CompanionPersonality.SUPPORTIVE_FRIEND
        )
        db.add(companion)
        db.commit()
        db.refresh(companion)
    
    # Get conversation history
    conversations = db.query(CompanionConversation).filter(
        CompanionConversation.companion_id == companion.id
    ).order_by(CompanionConversation.created_at.desc()).limit(10).all()
    
    conversation_history = [
        {
            "user_message": conv.user_message,
            "companion_response": conv.companion_response
        }
        for conv in reversed(conversations)
    ]
    
    # Generate response
    result = await AICompanionService.generate_response(
        user_message=chat_data.message,
        personality=companion.personality,
        conversation_history=conversation_history,
        user_context=companion.user_context or {},
        custom_instructions=companion.custom_instructions
    )
    
    # Save conversation
    conversation = CompanionConversation(
        companion_id=companion.id,
        user_message=chat_data.message,
        companion_response=result["response"],
        detected_emotion=result["detected_emotion"],
        message_count=len(conversations) + 1
    )
    db.add(conversation)
    
    # Update companion stats
    companion.last_interaction = conversation.created_at
    companion.total_conversations += 1
    
    db.commit()
    
    return ChatResponse(
        response=result["response"],
        detected_emotion=result["detected_emotion"],
        suggestions=result["suggestions"]
    )

@router.put("/personality")
async def update_personality(
    update_data: PersonalityUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update companion personality"""
    
    companion = db.query(AICompanion).filter(
        AICompanion.user_id == current_user.id
    ).first()
    
    if not companion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Companion not found"
        )
    
    companion.personality = update_data.personality
    companion.custom_instructions = update_data.custom_instructions
    
    db.commit()
    
    return {"message": "Personality updated successfully"}

@router.get("/daily-checkin")
async def get_daily_checkin(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get daily check-in message"""
    
    companion = db.query(AICompanion).filter(
        AICompanion.user_id == current_user.id
    ).first()
    
    if not companion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Companion not found"
        )
    
    checkin_message = await AICompanionService.generate_daily_checkin(
        personality=companion.personality,
        user_context=companion.user_context or {}
    )
    
    return {"message": checkin_message}

class MessageCraftRequest(BaseModel):
    intent: str

@router.post("/help-craft-message")
async def help_craft_message(
    request: MessageCraftRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get help crafting a message to future self"""
    
    companion = db.query(AICompanion).filter(
        AICompanion.user_id == current_user.id
    ).first()
    
    if not companion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Companion not found"
        )
    
    result = await AICompanionService.help_craft_message(
        user_intent=request.intent,
        personality=companion.personality,
        user_context=companion.user_context or {}
    )
    
    return result
