import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.core.config import settings
from typing import Optional
from datetime import datetime

class EmailService:
    """Handle email notifications for message delivery and user engagement"""
    
    @staticmethod
    def _send_email(to_email: str, subject: str, html_content: str, text_content: str) -> bool:
        """Send email using SMTP"""
        
        # Skip if SMTP not configured
        if not settings.SMTP_HOST or settings.SMTP_HOST == "smtp.gmail.com":
            print(f"[EMAIL MOCK] To: {to_email}, Subject: {subject}")
            return True  # Mock success for development
        
        try:
            msg = MIMEMultipart('alternative')
            msg['From'] = settings.SMTP_USER
            msg['To'] = to_email
            msg['Subject'] = subject
            
            # Attach both plain text and HTML versions
            part1 = MIMEText(text_content, 'plain')
            part2 = MIMEText(html_content, 'html')
            
            msg.attach(part1)
            msg.attach(part2)
            
            # Send email
            with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
                server.starttls()
                server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
                server.send_message(msg)
            
            return True
        except Exception as e:
            print(f"Email send failed: {str(e)}")
            return False
    
    @staticmethod
    def send_message_ready_notification(
        user_email: str,
        user_name: str,
        message_preview: str,
        message_id: int,
        created_date: datetime
    ) -> bool:
        """Notify user that their message from the past is ready"""
        
        days_ago = (datetime.utcnow() - created_date).days
        
        subject = "📬 A message from your past self is waiting"
        
        text_content = f"""
Hi {user_name},

A message you wrote to yourself {days_ago} days ago is now ready to be opened.

Preview: "{message_preview[:100]}..."

Open your message: https://futureyou.app/messages/{message_id}

This moment was chosen specifically for you based on AI analysis of your patterns and the message's context.

Take a moment to reflect on how far you've come.

- Future You Team
        """
        
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
        .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
        .preview {{ background: white; padding: 20px; border-left: 4px solid #667eea; margin: 20px 0; font-style: italic; }}
        .button {{ display: inline-block; background: #667eea; color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
        .footer {{ text-align: center; color: #999; font-size: 12px; margin-top: 30px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📬 A Message From Your Past</h1>
        </div>
        <div class="content">
            <p>Hi {user_name},</p>
            
            <p>A message you wrote to yourself <strong>{days_ago} days ago</strong> is now ready to be opened.</p>
            
            <div class="preview">
                "{message_preview[:150]}..."
            </div>
            
            <p>This moment was chosen specifically for you based on AI analysis of your patterns and the message's context.</p>
            
            <center>
                <a href="https://futureyou.app/messages/{message_id}" class="button">Open Your Message</a>
            </center>
            
            <p>Take a moment to reflect on how far you've come since you wrote this.</p>
            
            <div class="footer">
                <p>Future You - Messages from your past, delivered at the perfect moment</p>
                <p>Don't want these emails? <a href="https://futureyou.app/settings">Update preferences</a></p>
            </div>
        </div>
    </div>
</body>
</html>
        """
        
        return EmailService._send_email(user_email, subject, html_content, text_content)
    
    @staticmethod
    def send_welcome_email(user_email: str, user_name: str) -> bool:
        """Send welcome email to new users"""
        
        subject = "🎉 Welcome to Future You!"
        
        text_content = f"""
Hi {user_name},

Welcome to Future You! We're excited to help you connect with your future self.

Here's how it works:
1. Write a message to your future self
2. Choose when you want to receive it (or let AI decide)
3. Receive it at the perfect moment

Your first message is waiting to be created. What will you tell your future self?

Get started: https://futureyou.app/messages/new

- Future You Team
        """
        
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 40px; text-align: center; border-radius: 10px 10px 0 0; }}
        .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
        .feature {{ background: white; padding: 15px; margin: 10px 0; border-radius: 5px; }}
        .button {{ display: inline-block; background: #667eea; color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎉 Welcome to Future You!</h1>
            <p>Messages from your past, delivered at the perfect moment</p>
        </div>
        <div class="content">
            <p>Hi {user_name},</p>
            
            <p>We're excited to help you connect with your future self through the power of time-delayed messages.</p>
            
            <h3>How it works:</h3>
            
            <div class="feature">
                <strong>✍️ Write</strong> - Create a message to your future self
            </div>
            
            <div class="feature">
                <strong>🤖 AI Timing</strong> - Let AI determine the perfect moment to deliver it
            </div>
            
            <div class="feature">
                <strong>📬 Receive</strong> - Get your message when you need it most
            </div>
            
            <center>
                <a href="https://futureyou.app/messages/new" class="button">Create Your First Message</a>
            </center>
            
            <p>What will you tell your future self?</p>
        </div>
    </div>
</body>
</html>
        """
        
        return EmailService._send_email(user_email, subject, html_content, text_content)
    
    @staticmethod
    def send_daily_reminder(user_email: str, user_name: str, pending_count: int) -> bool:
        """Send daily reminder about pending messages"""
        
        subject = f"💭 You have {pending_count} message{'s' if pending_count != 1 else ''} waiting"
        
        text_content = f"""
Hi {user_name},

You have {pending_count} message{'s' if pending_count != 1 else ''} from your past self ready to be opened.

Don't let these moments pass by. Your past self took the time to write to you - take a moment to read and reflect.

View your messages: https://futureyou.app/messages

- Future You Team
        """
        
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .content {{ background: #f9f9f9; padding: 30px; border-radius: 10px; }}
        .count {{ font-size: 48px; color: #667eea; text-align: center; margin: 20px 0; }}
        .button {{ display: inline-block; background: #667eea; color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="content">
            <h2>💭 Messages Waiting</h2>
            
            <div class="count">{pending_count}</div>
            
            <p>Hi {user_name},</p>
            
            <p>You have <strong>{pending_count} message{'s' if pending_count != 1 else ''}</strong> from your past self ready to be opened.</p>
            
            <p>Don't let these moments pass by. Your past self took the time to write to you - take a moment to read and reflect.</p>
            
            <center>
                <a href="https://futureyou.app/messages" class="button">View Your Messages</a>
            </center>
        </div>
    </div>
</body>
</html>
        """
        
        return EmailService._send_email(user_email, subject, html_content, text_content)
    
    @staticmethod
    def send_upgrade_prompt(user_email: str, user_name: str, messages_used: int, limit: int) -> bool:
        """Prompt user to upgrade when approaching limit"""
        
        subject = f"⚠️ You've used {messages_used}/{limit} messages this month"
        
        text_content = f"""
Hi {user_name},

You've used {messages_used} out of {limit} messages this month on your Free plan.

Upgrade to Premium for unlimited messages and unlock:
- AI-powered optimal timing
- Priority delivery
- Advanced analytics
- Custom companion personality
- And more!

Upgrade now: https://futureyou.app/pricing

- Future You Team
        """
        
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .content {{ background: #f9f9f9; padding: 30px; border-radius: 10px; }}
        .progress {{ background: #e0e0e0; height: 20px; border-radius: 10px; margin: 20px 0; }}
        .progress-bar {{ background: #667eea; height: 100%; border-radius: 10px; width: {(messages_used/limit)*100}%; }}
        .button {{ display: inline-block; background: #667eea; color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
        .features {{ background: white; padding: 20px; margin: 20px 0; border-radius: 5px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="content">
            <h2>⚠️ Approaching Your Message Limit</h2>
            
            <p>Hi {user_name},</p>
            
            <p>You've used <strong>{messages_used} out of {limit} messages</strong> this month on your Free plan.</p>
            
            <div class="progress">
                <div class="progress-bar"></div>
            </div>
            
            <div class="features">
                <h3>Upgrade to Premium for:</h3>
                <ul>
                    <li>✨ Unlimited messages</li>
                    <li>🤖 AI-powered optimal timing</li>
                    <li>⚡ Priority delivery</li>
                    <li>📊 Advanced analytics</li>
                    <li>🎭 Custom companion personality</li>
                </ul>
            </div>
            
            <center>
                <a href="https://futureyou.app/pricing" class="button">Upgrade to Premium - $9.99/mo</a>
            </center>
        </div>
    </div>
</body>
</html>
        """
        
        return EmailService._send_email(user_email, subject, html_content, text_content)
