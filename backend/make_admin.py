"""
Make a user admin by email
Usage: python make_admin.py
"""

from app.core.database import SessionLocal
from app.models.user import User
from app.models.message import Message
from app.models.companion import AICompanion
from app.models import MessageReaction, UserSession, AuditLog

def make_admin():
    email = input("Enter email address to make admin: ").strip()
    
    if not email:
        print("❌ Email cannot be empty")
        return
    
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == email).first()
        
        if not user:
            print(f"❌ User with email '{email}' not found")
            return
        
        if user.is_admin:
            print(f"✅ User '{email}' is already an admin")
            return
        
        user.is_admin = True
        db.commit()
        
        print(f"✅ Successfully made '{email}' an admin!")
        print(f"   User ID: {user.id}")
        print(f"   Name: {user.full_name or 'N/A'}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    make_admin()
