from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum, JSON, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.core.database import Base

class CompanionPersonality(str, enum.Enum):
    MOTIVATIONAL_COACH = "motivational_coach"
    WISE_MENTOR = "wise_mentor"
    SUPPORTIVE_FRIEND = "supportive_friend"
    PHILOSOPHICAL_GUIDE = "philosophical_guide"
    PLAYFUL_BUDDY = "playful_buddy"

class AICompanion(Base):
    __tablename__ = "ai_companions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    
    # Companion Configuration
    name = Column(String, default="Future Buddy")
    personality = Column(Enum(CompanionPersonality), default=CompanionPersonality.SUPPORTIVE_FRIEND)
    custom_instructions = Column(Text, nullable=True)
    
    # Learning & Memory
    user_context = Column(JSON, default=dict)  # Learned patterns, preferences
    conversation_summary = Column(Text, nullable=True)  # Rolling summary of past conversations
    
    # Engagement
    daily_checkin_enabled = Column(Boolean, default=False)
    checkin_time = Column(String, nullable=True)  # "09:00" format
    last_interaction = Column(DateTime, nullable=True)
    total_conversations = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", backref="companion")
    conversations = relationship("CompanionConversation", back_populates="companion", cascade="all, delete-orphan")

class CompanionConversation(Base):
    __tablename__ = "companion_conversations"
    
    id = Column(Integer, primary_key=True, index=True)
    companion_id = Column(Integer, ForeignKey("ai_companions.id"), nullable=False)
    
    # Message Content (encrypted)
    user_message = Column(Text, nullable=False)
    companion_response = Column(Text, nullable=False)
    
    # Context
    conversation_context = Column(JSON, default=dict)  # Mood, topic, related messages
    detected_emotion = Column(String, nullable=True)
    
    # Metadata
    message_count = Column(Integer, default=0)  # Position in conversation thread
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Relationships
    companion = relationship("AICompanion", back_populates="conversations")
