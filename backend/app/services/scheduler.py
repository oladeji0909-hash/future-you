from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.message import Message, MessageStatus
from app.models.user import User
from app.core.security import MessageEncryption
from app.services.email_service import EmailService
import logging

logger = logging.getLogger(__name__)

class MessageDeliveryScheduler:
    """Background scheduler for automatic message delivery"""
    
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.scheduler.add_job(
            func=self.check_and_deliver_messages,
            trigger="interval",
            minutes=1,  # Check every minute for testing
            id="message_delivery_job",
            name="Check and deliver scheduled messages",
            replace_existing=True
        )
    
    def start(self):
        """Start the scheduler"""
        if not self.scheduler.running:
            self.scheduler.start()
            print("✅ Message delivery scheduler started - checking every minute")
            logger.info("Message delivery scheduler started")
    
    def shutdown(self):
        """Shutdown the scheduler"""
        if self.scheduler.running:
            self.scheduler.shutdown()
            logger.info("Message delivery scheduler stopped")
    
    @staticmethod
    def check_and_deliver_messages():
        """Check for messages ready to be delivered and send them"""
        
        print(f"🔍 Checking for messages to deliver at {datetime.utcnow()}")
        
        db: Session = SessionLocal()
        
        try:
            # Find messages scheduled for delivery
            messages_to_deliver = db.query(Message).filter(
                Message.status == MessageStatus.SCHEDULED,
                Message.scheduled_for <= datetime.utcnow()
            ).all()
            
            logger.info(f"Found {len(messages_to_deliver)} messages ready for delivery")
            
            for message in messages_to_deliver:
                try:
                    # Get user
                    user = db.query(User).filter(User.id == message.user_id).first()
                    if not user:
                        continue
                    
                    # Decrypt message for email preview
                    decrypted_content = MessageEncryption.decrypt(
                        message.encrypted_content,
                        user.encryption_key
                    )
                    
                    # Send email notification
                    email_sent = EmailService.send_message_ready_notification(
                        user_email=user.email,
                        user_name=user.full_name or "there",
                        message_preview=decrypted_content,
                        message_id=message.id,
                        created_date=message.created_at
                    )
                    
                    # Update message status
                    message.status = MessageStatus.DELIVERED
                    message.delivered_at = datetime.utcnow()
                    
                    db.commit()
                    
                    logger.info(f"Delivered message {message.id} to user {user.email}")
                    
                except Exception as e:
                    logger.error(f"Failed to deliver message {message.id}: {str(e)}")
                    db.rollback()
                    continue
            
        except Exception as e:
            logger.error(f"Error in message delivery job: {str(e)}")
        finally:
            db.close()
    
    @staticmethod
    def send_daily_reminders():
        """Send daily reminders to users with unread messages"""
        
        db: Session = SessionLocal()
        
        try:
            # Find users with delivered but unread messages
            users_with_unread = db.query(User).join(Message).filter(
                Message.status == MessageStatus.DELIVERED
            ).distinct().all()
            
            for user in users_with_unread:
                # Count unread messages
                unread_count = db.query(Message).filter(
                    Message.user_id == user.id,
                    Message.status == MessageStatus.DELIVERED
                ).count()
                
                if unread_count > 0:
                    EmailService.send_daily_reminder(
                        user_email=user.email,
                        user_name=user.full_name or "there",
                        pending_count=unread_count
                    )
                    logger.info(f"Sent daily reminder to {user.email} ({unread_count} messages)")
        
        except Exception as e:
            logger.error(f"Error in daily reminder job: {str(e)}")
        finally:
            db.close()
    
    def add_daily_reminder_job(self):
        """Add job to send daily reminders at 9 AM"""
        self.scheduler.add_job(
            func=self.send_daily_reminders,
            trigger="cron",
            hour=9,
            minute=0,
            id="daily_reminder_job",
            name="Send daily reminders",
            replace_existing=True
        )

# Global scheduler instance
scheduler = MessageDeliveryScheduler()
