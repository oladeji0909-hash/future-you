from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Enum, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.core.database import Base

class MessageType(str, enum.Enum):
    TEXT = "text"
    VOICE = "voice"
    VIDEO = "video"

class MessageStatus(str, enum.Enum):
    DRAFT = "draft"
    SCHEDULED = "scheduled"
    DELIVERED = "delivered"
    READ = "read"
    ARCHIVED = "archived"

class DeliveryTiming(str, enum.Enum):
    SPECIFIC_DATE = "specific_date"
    AI_OPTIMAL = "ai_optimal"
    RANDOM = "random"
    MILESTONE = "milestone"
    EMOTIONAL = "emotional"
    LOCATION = "location"
    ACHIEVEMENT = "achievement"

class Message(Base):
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Content (encrypted)
    encrypted_content = Column(Text, nullable=False)
    message_type = Column(Enum(MessageType), default=MessageType.TEXT)
    
    # Attachments
    attachment_urls = Column(JSON, default=list)
    
    # Delivery
    status = Column(Enum(MessageStatus), default=MessageStatus.DRAFT)
    delivery_timing = Column(Enum(DeliveryTiming), default=DeliveryTiming.SPECIFIC_DATE)
    scheduled_for = Column(DateTime, nullable=True)
    delivered_at = Column(DateTime, nullable=True)
    read_at = Column(DateTime, nullable=True)
    
    # AI Context
    ai_context = Column(JSON, default=dict)  # Stores user patterns, emotional state, etc.
    ai_confidence_score = Column(Integer, default=0)  # 0-100
    
    # Metadata
    tags = Column(JSON, default=list)
    category = Column(String, nullable=True)
    is_public = Column(Boolean, default=False)  # For Message Roulette
    
    # Blockchain
    blockchain_hash = Column(String, nullable=True)
    ipfs_cid = Column(String, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="messages")
    reactions = relationship("MessageReaction", back_populates="message", cascade="all, delete-orphan")
