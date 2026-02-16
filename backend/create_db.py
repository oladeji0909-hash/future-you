import sys
sys.path.insert(0, 'C:\\Projects\\FutureYou\\backend')

from app.core.database import Base, engine
from app.models.user import User
from app.models.message import Message
from app.models.companion import AICompanion, CompanionConversation
from app.models import UserSession, AuditLog, MessageReaction

print("Creating database tables...")
Base.metadata.create_all(bind=engine)
print("✅ Database tables created successfully!")
print("Tables created: users, messages, ai_companions, companion_conversations, user_sessions, audit_logs, message_reactions")
