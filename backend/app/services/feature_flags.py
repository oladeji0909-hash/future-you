from enum import Enum
from typing import Dict, Any
import redis
from app.core.config import settings

class FeatureFlag(str, Enum):
    AI_COMPANION = "ai_companion"
    MESSAGE_ROULETTE = "message_roulette"
    LEGACY_MODE = "legacy_mode"
    VOICE_MESSAGES = "voice_messages"
    VIDEO_MESSAGES = "video_messages"
    WISDOM_MARKETPLACE = "wisdom_marketplace"
    BLOCKCHAIN_VERIFICATION = "blockchain_verification"

class FeatureFlagService:
    def __init__(self):
        self.redis_client = redis.from_url(settings.REDIS_URL)
        self.default_flags = {
            FeatureFlag.AI_COMPANION: True,
            FeatureFlag.MESSAGE_ROULETTE: False,
            FeatureFlag.LEGACY_MODE: False,
            FeatureFlag.VOICE_MESSAGES: False,
            FeatureFlag.VIDEO_MESSAGES: False,
            FeatureFlag.WISDOM_MARKETPLACE: False,
            FeatureFlag.BLOCKCHAIN_VERIFICATION: False,
        }
    
    def is_enabled(self, flag: FeatureFlag, user_id: int = None) -> bool:
        """Check if feature is enabled globally or for specific user"""
        
        # Check user-specific override
        if user_id:
            user_key = f"feature_flag:{flag.value}:user:{user_id}"
            user_override = self.redis_client.get(user_key)
            if user_override is not None:
                return user_override.decode() == "true"
        
        # Check global flag
        global_key = f"feature_flag:{flag.value}"
        global_value = self.redis_client.get(global_key)
        
        if global_value is not None:
            return global_value.decode() == "true"
        
        # Return default
        return self.default_flags.get(flag, False)
    
    def enable(self, flag: FeatureFlag, user_id: int = None):
        """Enable feature globally or for specific user"""
        if user_id:
            key = f"feature_flag:{flag.value}:user:{user_id}"
        else:
            key = f"feature_flag:{flag.value}"
        self.redis_client.set(key, "true")
    
    def disable(self, flag: FeatureFlag, user_id: int = None):
        """Disable feature globally or for specific user"""
        if user_id:
            key = f"feature_flag:{flag.value}:user:{user_id}"
        else:
            key = f"feature_flag:{flag.value}"
        self.redis_client.set(key, "false")
    
    def enable_for_percentage(self, flag: FeatureFlag, percentage: int):
        """Enable feature for percentage of users (canary release)"""
        key = f"feature_flag:{flag.value}:percentage"
        self.redis_client.set(key, str(percentage))
    
    def is_enabled_for_user(self, flag: FeatureFlag, user_id: int) -> bool:
        """Check if feature enabled considering percentage rollout"""
        
        # Check explicit enable/disable first
        if self.is_enabled(flag, user_id):
            return True
        
        # Check percentage rollout
        percentage_key = f"feature_flag:{flag.value}:percentage"
        percentage = self.redis_client.get(percentage_key)
        
        if percentage:
            percentage = int(percentage.decode())
            # Use user_id hash to determine if in percentage
            return (user_id % 100) < percentage
        
        return False

# Global instance
feature_flags = FeatureFlagService()

# Usage in endpoints:
# if feature_flags.is_enabled(FeatureFlag.AI_COMPANION, current_user.id):
#     # Show AI companion feature
