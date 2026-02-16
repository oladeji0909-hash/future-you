from datetime import datetime, timedelta
from typing import Dict, List, Optional
from sqlalchemy.orm import Session
from app.models.message import Message, DeliveryTiming
from app.models.companion import CompanionConversation
import random

class AITimingService:
    """Determines optimal message delivery timing based on user patterns and context"""
    
    @staticmethod
    def calculate_optimal_delivery(
        message_content: str,
        user_id: int,
        delivery_timing: DeliveryTiming,
        db: Session,
        scheduled_for: Optional[datetime] = None
    ) -> datetime:
        """Calculate when to deliver a message based on AI analysis"""
        
        if delivery_timing == DeliveryTiming.SPECIFIC_DATE and scheduled_for:
            return scheduled_for
        
        # AI-based timing
        user_patterns = AITimingService._analyze_user_patterns(user_id, db)
        message_context = AITimingService._analyze_message_context(message_content)
        
        if delivery_timing == DeliveryTiming.AI_OPTIMAL:
            return AITimingService._calculate_ai_optimal(user_patterns, message_context)
        
        elif delivery_timing == DeliveryTiming.MILESTONE:
            return AITimingService._calculate_milestone_timing(user_patterns, message_context)
        
        elif delivery_timing == DeliveryTiming.EMOTIONAL:
            return AITimingService._calculate_emotional_timing(user_patterns, message_context)
        
        elif delivery_timing == DeliveryTiming.RANDOM:
            # Random between 30-365 days
            random_days = random.randint(30, 365)
            return datetime.utcnow() + timedelta(days=random_days)
        
        # Default fallback
        return datetime.utcnow() + timedelta(days=30)
    
    @staticmethod
    def _analyze_user_patterns(user_id: int, db: Session) -> Dict:
        """Analyze user's historical patterns"""
        
        # Get user's message history
        messages = db.query(Message).filter(Message.user_id == user_id).all()
        
        # Get companion conversations for emotional patterns
        conversations = db.query(CompanionConversation).join(
            CompanionConversation.companion
        ).filter(
            CompanionConversation.companion.has(user_id=user_id)
        ).order_by(CompanionConversation.created_at.desc()).limit(50).all()
        
        patterns = {
            "total_messages": len(messages),
            "avg_gap_days": 30,  # Default
            "emotional_trend": "stable",
            "engagement_level": "medium",
            "preferred_timing": "morning"
        }
        
        # Calculate average gap between messages
        if len(messages) > 1:
            sorted_msgs = sorted(messages, key=lambda m: m.created_at)
            gaps = []
            for i in range(1, len(sorted_msgs)):
                gap = (sorted_msgs[i].created_at - sorted_msgs[i-1].created_at).days
                gaps.append(gap)
            if gaps:
                patterns["avg_gap_days"] = sum(gaps) / len(gaps)
        
        # Analyze emotional trends from conversations
        if conversations:
            emotions = [conv.detected_emotion for conv in conversations if conv.detected_emotion]
            if emotions:
                positive_emotions = sum(1 for e in emotions if e in ["happy", "excited", "hopeful"])
                if positive_emotions > len(emotions) * 0.6:
                    patterns["emotional_trend"] = "positive"
                elif positive_emotions < len(emotions) * 0.3:
                    patterns["emotional_trend"] = "challenging"
        
        return patterns
    
    @staticmethod
    def _analyze_message_context(content: str) -> Dict:
        """Analyze message content for context clues"""
        
        content_lower = content.lower()
        
        context = {
            "urgency": "low",
            "emotional_weight": "medium",
            "category": "general",
            "suggested_delay_days": 30
        }
        
        # Detect urgency
        urgent_words = ["important", "remember", "don't forget", "crucial", "critical"]
        if any(word in content_lower for word in urgent_words):
            context["urgency"] = "high"
            context["suggested_delay_days"] = 7
        
        # Detect emotional weight
        heavy_words = ["struggle", "difficult", "pain", "loss", "grief", "hard time"]
        if any(word in content_lower for word in heavy_words):
            context["emotional_weight"] = "high"
            context["suggested_delay_days"] = 90  # Give more time for healing
        
        # Detect achievement/goal context
        achievement_words = ["goal", "achieve", "accomplish", "succeed", "dream"]
        if any(word in content_lower for word in achievement_words):
            context["category"] = "achievement"
            context["suggested_delay_days"] = 180  # 6 months for goals
        
        # Detect reflection/wisdom
        reflection_words = ["learned", "realized", "understand", "wisdom", "insight"]
        if any(word in content_lower for word in reflection_words):
            context["category"] = "reflection"
            context["suggested_delay_days"] = 365  # 1 year for perspective
        
        # Detect celebration
        celebration_words = ["celebrate", "proud", "happy", "excited", "joy"]
        if any(word in content_lower for word in celebration_words):
            context["category"] = "celebration"
            context["suggested_delay_days"] = 30  # Sooner for positive reinforcement
        
        return context
    
    @staticmethod
    def _calculate_ai_optimal(user_patterns: Dict, message_context: Dict) -> datetime:
        """Calculate optimal timing using AI logic"""
        
        base_delay = message_context["suggested_delay_days"]
        
        # Adjust based on user patterns
        if user_patterns["emotional_trend"] == "challenging":
            base_delay = max(base_delay, 60)  # Give more time if struggling
        elif user_patterns["emotional_trend"] == "positive":
            base_delay = min(base_delay, 90)  # Can deliver sooner if doing well
        
        # Adjust based on engagement
        if user_patterns["engagement_level"] == "high":
            base_delay *= 0.8  # Engaged users can handle more frequent messages
        
        # Add some randomness for natural feel (±20%)
        variance = base_delay * 0.2
        final_delay = base_delay + random.uniform(-variance, variance)
        
        return datetime.utcnow() + timedelta(days=int(final_delay))
    
    @staticmethod
    def _calculate_milestone_timing(user_patterns: Dict, message_context: Dict) -> datetime:
        """Calculate timing based on life milestones"""
        
        # Common milestone intervals: 3 months, 6 months, 1 year, 2 years, 5 years
        milestone_days = [90, 180, 365, 730, 1825]
        
        # Choose based on message weight
        if message_context["emotional_weight"] == "high":
            delay = 365  # 1 year for heavy topics
        elif message_context["category"] == "achievement":
            delay = 180  # 6 months for goals
        else:
            delay = random.choice(milestone_days[:3])  # Random shorter milestone
        
        return datetime.utcnow() + timedelta(days=delay)
    
    @staticmethod
    def _calculate_emotional_timing(user_patterns: Dict, message_context: Dict) -> datetime:
        """Calculate timing based on emotional readiness"""
        
        base_delay = 60  # 2 months default
        
        # If message is emotionally heavy, wait longer
        if message_context["emotional_weight"] == "high":
            base_delay = 120  # 4 months
        
        # If user is currently struggling, delay further
        if user_patterns["emotional_trend"] == "challenging":
            base_delay += 30
        
        # If message is positive/celebratory, can be sooner
        if message_context["category"] == "celebration":
            base_delay = 30
        
        return datetime.utcnow() + timedelta(days=base_delay)
    
    @staticmethod
    def should_deliver_now(message: Message, db: Session) -> bool:
        """Check if a scheduled message should be delivered now"""
        
        if not message.scheduled_for:
            return False
        
        if message.scheduled_for <= datetime.utcnow():
            return True
        
        return False
    
    @staticmethod
    def get_delivery_explanation(
        delivery_timing: DeliveryTiming,
        scheduled_for: datetime,
        message_context: Dict
    ) -> str:
        """Generate human-readable explanation for delivery timing"""
        
        days_until = (scheduled_for - datetime.utcnow()).days
        
        if delivery_timing == DeliveryTiming.SPECIFIC_DATE:
            return f"Scheduled for delivery in {days_until} days."
        
        elif delivery_timing == DeliveryTiming.AI_OPTIMAL:
            if message_context["category"] == "achievement":
                return f"AI suggests delivering in {days_until} days - giving you time to work toward your goals."
            elif message_context["category"] == "reflection":
                return f"AI suggests delivering in {days_until} days - allowing perspective and growth."
            elif message_context["emotional_weight"] == "high":
                return f"AI suggests delivering in {days_until} days - giving you time to heal and grow stronger."
            else:
                return f"AI determined {days_until} days is optimal based on your patterns and this message's context."
        
        elif delivery_timing == DeliveryTiming.MILESTONE:
            return f"This message will arrive at a meaningful milestone in {days_until} days."
        
        elif delivery_timing == DeliveryTiming.EMOTIONAL:
            return f"AI will deliver this in {days_until} days when you're emotionally ready to receive it."
        
        elif delivery_timing == DeliveryTiming.RANDOM:
            return f"Randomly scheduled for delivery in {days_until} days - a surprise from your past self!"
        
        else:
            return f"Scheduled for delivery in {days_until} days."
