from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from typing import Dict, List
from app.models.message import Message, MessageStatus
from app.models.user import User

class DeliveryService:
    """Track and manage message delivery performance"""
    
    @staticmethod
    def get_delivery_stats(db: Session) -> Dict:
        """Get overall delivery statistics"""
        
        # Total messages by status
        total_scheduled = db.query(func.count(Message.id)).filter(
            Message.status == MessageStatus.SCHEDULED
        ).scalar() or 0
        
        total_delivered = db.query(func.count(Message.id)).filter(
            Message.status == MessageStatus.DELIVERED
        ).scalar() or 0
        
        total_read = db.query(func.count(Message.id)).filter(
            Message.status == MessageStatus.READ
        ).scalar() or 0
        
        # Messages ready for delivery (scheduled_for <= now)
        ready_for_delivery = db.query(func.count(Message.id)).filter(
            Message.status == MessageStatus.SCHEDULED,
            Message.scheduled_for <= datetime.utcnow()
        ).scalar() or 0
        
        # Upcoming deliveries (next 7 days)
        seven_days_from_now = datetime.utcnow() + timedelta(days=7)
        upcoming_deliveries = db.query(func.count(Message.id)).filter(
            Message.status == MessageStatus.SCHEDULED,
            Message.scheduled_for <= seven_days_from_now,
            Message.scheduled_for > datetime.utcnow()
        ).scalar() or 0
        
        # Delivery rate (delivered / total)
        total_messages = total_scheduled + total_delivered + total_read
        delivery_rate = (total_delivered + total_read) / total_messages * 100 if total_messages > 0 else 0
        
        # Read rate (read / delivered)
        read_rate = total_read / (total_delivered + total_read) * 100 if (total_delivered + total_read) > 0 else 0
        
        return {
            "total_messages": total_messages,
            "scheduled": total_scheduled,
            "delivered": total_delivered,
            "read": total_read,
            "ready_for_delivery": ready_for_delivery,
            "upcoming_7_days": upcoming_deliveries,
            "delivery_rate": round(delivery_rate, 2),
            "read_rate": round(read_rate, 2)
        }
    
    @staticmethod
    def get_upcoming_deliveries(db: Session, days: int = 7) -> List[Dict]:
        """Get messages scheduled for delivery in the next N days"""
        
        end_date = datetime.utcnow() + timedelta(days=days)
        
        messages = db.query(Message).filter(
            Message.status == MessageStatus.SCHEDULED,
            Message.scheduled_for <= end_date,
            Message.scheduled_for > datetime.utcnow()
        ).order_by(Message.scheduled_for).all()
        
        result = []
        for msg in messages:
            user = db.query(User).filter(User.id == msg.user_id).first()
            days_until = (msg.scheduled_for - datetime.utcnow()).days
            
            result.append({
                "message_id": msg.id,
                "user_email": user.email if user else "Unknown",
                "scheduled_for": msg.scheduled_for.isoformat(),
                "days_until": days_until,
                "delivery_timing": msg.delivery_timing.value,
                "category": msg.category,
                "tags": msg.tags
            })
        
        return result
    
    @staticmethod
    def get_overdue_deliveries(db: Session) -> List[Dict]:
        """Get messages that should have been delivered but weren't"""
        
        messages = db.query(Message).filter(
            Message.status == MessageStatus.SCHEDULED,
            Message.scheduled_for <= datetime.utcnow()
        ).order_by(Message.scheduled_for).all()
        
        result = []
        for msg in messages:
            user = db.query(User).filter(User.id == msg.user_id).first()
            days_overdue = (datetime.utcnow() - msg.scheduled_for).days
            
            result.append({
                "message_id": msg.id,
                "user_email": user.email if user else "Unknown",
                "scheduled_for": msg.scheduled_for.isoformat(),
                "days_overdue": days_overdue,
                "delivery_timing": msg.delivery_timing.value
            })
        
        return result
    
    @staticmethod
    def get_delivery_timeline(db: Session, days: int = 30) -> Dict:
        """Get delivery timeline for charts"""
        
        start_date = datetime.utcnow() - timedelta(days=days)
        
        # Daily deliveries
        daily_deliveries = []
        for i in range(days):
            date = start_date + timedelta(days=i)
            count = db.query(func.count(Message.id)).filter(
                func.date(Message.delivered_at) == date.date(),
                Message.status.in_([MessageStatus.DELIVERED, MessageStatus.READ])
            ).scalar() or 0
            
            daily_deliveries.append({
                "date": date.date().isoformat(),
                "count": count
            })
        
        # Daily reads
        daily_reads = []
        for i in range(days):
            date = start_date + timedelta(days=i)
            count = db.query(func.count(Message.id)).filter(
                func.date(Message.read_at) == date.date(),
                Message.status == MessageStatus.READ
            ).scalar() or 0
            
            daily_reads.append({
                "date": date.date().isoformat(),
                "count": count
            })
        
        return {
            "daily_deliveries": daily_deliveries,
            "daily_reads": daily_reads
        }
    
    @staticmethod
    def get_user_delivery_stats(user_id: int, db: Session) -> Dict:
        """Get delivery stats for a specific user"""
        
        total_messages = db.query(func.count(Message.id)).filter(
            Message.user_id == user_id
        ).scalar() or 0
        
        scheduled = db.query(func.count(Message.id)).filter(
            Message.user_id == user_id,
            Message.status == MessageStatus.SCHEDULED
        ).scalar() or 0
        
        delivered = db.query(func.count(Message.id)).filter(
            Message.user_id == user_id,
            Message.status == MessageStatus.DELIVERED
        ).scalar() or 0
        
        read = db.query(func.count(Message.id)).filter(
            Message.user_id == user_id,
            Message.status == MessageStatus.READ
        ).scalar() or 0
        
        # Next delivery
        next_message = db.query(Message).filter(
            Message.user_id == user_id,
            Message.status == MessageStatus.SCHEDULED,
            Message.scheduled_for > datetime.utcnow()
        ).order_by(Message.scheduled_for).first()
        
        next_delivery = None
        if next_message:
            days_until = (next_message.scheduled_for - datetime.utcnow()).days
            next_delivery = {
                "message_id": next_message.id,
                "scheduled_for": next_message.scheduled_for.isoformat(),
                "days_until": days_until,
                "category": next_message.category
            }
        
        # Unread messages
        unread_count = db.query(func.count(Message.id)).filter(
            Message.user_id == user_id,
            Message.status == MessageStatus.DELIVERED
        ).scalar() or 0
        
        return {
            "total_messages": total_messages,
            "scheduled": scheduled,
            "delivered": delivered,
            "read": read,
            "unread": unread_count,
            "next_delivery": next_delivery,
            "read_rate": round(read / (delivered + read) * 100, 2) if (delivered + read) > 0 else 0
        }
    
    @staticmethod
    def mark_as_read(message_id: int, user_id: int, db: Session) -> bool:
        """Mark a message as read"""
        
        message = db.query(Message).filter(
            Message.id == message_id,
            Message.user_id == user_id,
            Message.status == MessageStatus.DELIVERED
        ).first()
        
        if not message:
            return False
        
        message.status = MessageStatus.READ
        message.read_at = datetime.utcnow()
        db.commit()
        
        return True
    
    @staticmethod
    def get_delivery_performance(db: Session) -> Dict:
        """Get delivery performance metrics"""
        
        # Average time from creation to delivery
        delivered_messages = db.query(Message).filter(
            Message.status.in_([MessageStatus.DELIVERED, MessageStatus.READ]),
            Message.delivered_at.isnot(None)
        ).all()
        
        if delivered_messages:
            total_wait_time = sum(
                (msg.delivered_at - msg.created_at).total_seconds() / 86400  # Convert to days
                for msg in delivered_messages
            )
            avg_wait_days = total_wait_time / len(delivered_messages)
        else:
            avg_wait_days = 0
        
        # Average time from delivery to read
        read_messages = db.query(Message).filter(
            Message.status == MessageStatus.READ,
            Message.read_at.isnot(None),
            Message.delivered_at.isnot(None)
        ).all()
        
        if read_messages:
            total_read_time = sum(
                (msg.read_at - msg.delivered_at).total_seconds() / 3600  # Convert to hours
                for msg in read_messages
            )
            avg_read_hours = total_read_time / len(read_messages)
        else:
            avg_read_hours = 0
        
        return {
            "avg_wait_days": round(avg_wait_days, 1),
            "avg_read_hours": round(avg_read_hours, 1),
            "total_delivered": len(delivered_messages),
            "total_read": len(read_messages)
        }
