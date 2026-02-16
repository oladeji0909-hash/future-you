from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from datetime import datetime, timedelta
from typing import Dict, List
from app.models.user import User, SubscriptionTier
from app.models.message import Message, MessageStatus
from app.models.companion import CompanionConversation

class AnalyticsService:
    """Track and analyze platform metrics for business insights"""
    
    @staticmethod
    def get_user_analytics(user_id: int, db: Session) -> Dict:
        """Get analytics for a specific user"""
        
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return {"error": "User not found"}
        
        # Message stats
        total_messages = db.query(func.count(Message.id)).filter(
            Message.user_id == user_id
        ).scalar() or 0
        
        scheduled_messages = db.query(func.count(Message.id)).filter(
            Message.user_id == user_id,
            Message.status == MessageStatus.SCHEDULED
        ).scalar() or 0
        
        delivered_messages = db.query(func.count(Message.id)).filter(
            Message.user_id == user_id,
            Message.status == MessageStatus.DELIVERED
        ).scalar() or 0
        
        read_messages = db.query(func.count(Message.id)).filter(
            Message.user_id == user_id,
            Message.status == MessageStatus.READ
        ).scalar() or 0
        
        # Companion stats
        total_conversations = db.query(func.count(CompanionConversation.id)).join(
            CompanionConversation.companion
        ).filter(
            CompanionConversation.companion.has(user_id=user_id)
        ).scalar() or 0
        
        # This month's messages
        current_month = datetime.utcnow().month
        current_year = datetime.utcnow().year
        
        messages_this_month = db.query(func.count(Message.id)).filter(
            Message.user_id == user_id,
            extract('month', Message.created_at) == current_month,
            extract('year', Message.created_at) == current_year
        ).scalar() or 0
        
        # Account age
        account_age_days = (datetime.utcnow() - user.created_at).days
        
        # Average messages per month
        months_active = max(1, account_age_days / 30)
        avg_messages_per_month = total_messages / months_active
        
        return {
            "user_id": user_id,
            "subscription_tier": user.subscription_tier.value,
            "account_age_days": account_age_days,
            "messages": {
                "total": total_messages,
                "scheduled": scheduled_messages,
                "delivered": delivered_messages,
                "read": read_messages,
                "this_month": messages_this_month,
                "avg_per_month": round(avg_messages_per_month, 1)
            },
            "companion": {
                "total_conversations": total_conversations
            },
            "engagement_score": AnalyticsService._calculate_engagement_score(
                total_messages, total_conversations, account_age_days
            )
        }
    
    @staticmethod
    def get_platform_analytics(db: Session) -> Dict:
        """Get overall platform analytics (admin view)"""
        
        # User stats
        total_users = db.query(func.count(User.id)).scalar() or 0
        
        free_users = db.query(func.count(User.id)).filter(
            User.subscription_tier == SubscriptionTier.FREE
        ).scalar() or 0
        
        premium_users = db.query(func.count(User.id)).filter(
            User.subscription_tier == SubscriptionTier.PREMIUM
        ).scalar() or 0
        
        lifetime_users = db.query(func.count(User.id)).filter(
            User.subscription_tier == SubscriptionTier.LIFETIME
        ).scalar() or 0
        
        # Message stats
        total_messages = db.query(func.count(Message.id)).scalar() or 0
        
        scheduled_messages = db.query(func.count(Message.id)).filter(
            Message.status == MessageStatus.SCHEDULED
        ).scalar() or 0
        
        delivered_messages = db.query(func.count(Message.id)).filter(
            Message.status == MessageStatus.DELIVERED
        ).scalar() or 0
        
        # Revenue metrics
        from app.services.payment_service import PaymentService
        mrr_data = PaymentService.calculate_mrr(db)
        
        # Growth metrics (last 30 days)
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        
        new_users_30d = db.query(func.count(User.id)).filter(
            User.created_at >= thirty_days_ago
        ).scalar() or 0
        
        new_messages_30d = db.query(func.count(Message.id)).filter(
            Message.created_at >= thirty_days_ago
        ).scalar() or 0
        
        # Conversion rate
        conversion_rate = ((premium_users + lifetime_users) / total_users * 100) if total_users > 0 else 0
        
        return {
            "users": {
                "total": total_users,
                "free": free_users,
                "premium": premium_users,
                "lifetime": lifetime_users,
                "new_last_30d": new_users_30d
            },
            "messages": {
                "total": total_messages,
                "scheduled": scheduled_messages,
                "delivered": delivered_messages,
                "new_last_30d": new_messages_30d,
                "avg_per_user": round(total_messages / total_users, 1) if total_users > 0 else 0
            },
            "revenue": {
                "mrr": mrr_data["total_mrr"],
                "goal": mrr_data["goal"],
                "progress_percentage": mrr_data["progress_percentage"],
                "paying_customers": premium_users + lifetime_users,
                "conversion_rate": round(conversion_rate, 2)
            },
            "engagement": {
                "messages_per_user": round(total_messages / total_users, 1) if total_users > 0 else 0,
                "active_users_30d": new_users_30d
            }
        }
    
    @staticmethod
    def get_message_timeline(user_id: int, db: Session) -> List[Dict]:
        """Get timeline of user's messages for visualization"""
        
        messages = db.query(Message).filter(
            Message.user_id == user_id
        ).order_by(Message.created_at).all()
        
        timeline = []
        for msg in messages:
            timeline.append({
                "id": msg.id,
                "created_at": msg.created_at.isoformat(),
                "scheduled_for": msg.scheduled_for.isoformat() if msg.scheduled_for else None,
                "delivered_at": msg.delivered_at.isoformat() if msg.delivered_at else None,
                "status": msg.status.value,
                "delivery_timing": msg.delivery_timing.value,
                "category": msg.category,
                "tags": msg.tags
            })
        
        return timeline
    
    @staticmethod
    def get_growth_chart_data(db: Session, days: int = 30) -> Dict:
        """Get data for growth charts"""
        
        start_date = datetime.utcnow() - timedelta(days=days)
        
        # Daily user signups
        daily_signups = []
        for i in range(days):
            date = start_date + timedelta(days=i)
            count = db.query(func.count(User.id)).filter(
                func.date(User.created_at) == date.date()
            ).scalar()
            daily_signups.append({
                "date": date.date().isoformat(),
                "count": count
            })
        
        # Daily message creation
        daily_messages = []
        for i in range(days):
            date = start_date + timedelta(days=i)
            count = db.query(func.count(Message.id)).filter(
                func.date(Message.created_at) == date.date()
            ).scalar()
            daily_messages.append({
                "date": date.date().isoformat(),
                "count": count
            })
        
        return {
            "daily_signups": daily_signups,
            "daily_messages": daily_messages
        }
    
    @staticmethod
    def _calculate_engagement_score(
        total_messages: int,
        total_conversations: int,
        account_age_days: int
    ) -> int:
        """Calculate user engagement score (0-100)"""
        
        if account_age_days == 0:
            return 0
        
        # Messages per day
        messages_per_day = total_messages / max(1, account_age_days)
        message_score = min(messages_per_day * 20, 50)  # Max 50 points
        
        # Conversations per day
        conversations_per_day = total_conversations / max(1, account_age_days)
        conversation_score = min(conversations_per_day * 10, 30)  # Max 30 points
        
        # Consistency bonus (if active for more than 7 days)
        consistency_score = 20 if account_age_days > 7 and total_messages > 3 else 0
        
        total_score = message_score + conversation_score + consistency_score
        
        return min(int(total_score), 100)
    
    @staticmethod
    def get_retention_metrics(db: Session) -> Dict:
        """Calculate user retention metrics"""
        
        # Users who created messages in last 7 days
        seven_days_ago = datetime.utcnow() - timedelta(days=7)
        active_7d = db.query(func.count(func.distinct(Message.user_id))).filter(
            Message.created_at >= seven_days_ago
        ).scalar()
        
        # Users who created messages in last 30 days
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        active_30d = db.query(func.count(func.distinct(Message.user_id))).filter(
            Message.created_at >= thirty_days_ago
        ).scalar()
        
        # Total users
        total_users = db.query(func.count(User.id)).scalar()
        
        return {
            "active_7d": active_7d,
            "active_30d": active_30d,
            "total_users": total_users,
            "retention_7d": round((active_7d / total_users * 100), 2) if total_users > 0 else 0,
            "retention_30d": round((active_30d / total_users * 100), 2) if total_users > 0 else 0
        }
