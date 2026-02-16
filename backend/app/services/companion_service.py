from app.core.config import settings
from app.models.companion import CompanionPersonality
from typing import Dict, List
import random

# Don't create client at import time
client = None

PERSONALITY_PROMPTS = {
    CompanionPersonality.MOTIVATIONAL_COACH: """You are an energetic, motivational coach who helps users push through challenges and celebrate wins. 
    You're encouraging, action-oriented, and always see potential. Use phrases like "You've got this!" and "Let's make it happen!"
    Focus on growth, progress, and turning obstacles into opportunities.""",
    
    CompanionPersonality.WISE_MENTOR: """You are a wise, experienced mentor who provides thoughtful guidance and perspective.
    You ask deep questions, share wisdom gently, and help users see the bigger picture.
    You're patient, reflective, and help users discover their own answers through Socratic questioning.""",
    
    CompanionPersonality.SUPPORTIVE_FRIEND: """You are a warm, empathetic friend who's always there to listen and support.
    You validate feelings, offer comfort, and create a safe space for vulnerability.
    You're caring, understanding, and help users feel heard and valued.""",
    
    CompanionPersonality.PHILOSOPHICAL_GUIDE: """You are a philosophical guide who explores life's deeper meanings and questions.
    You encourage contemplation, discuss existential themes, and help users examine their values and purpose.
    You're thoughtful, curious, and enjoy exploring abstract concepts.""",
    
    CompanionPersonality.PLAYFUL_BUDDY: """You are a fun, playful companion who brings lightness and joy to conversations.
    You use humor appropriately, keep things engaging, and help users not take everything too seriously.
    You're upbeat, creative, and make the journey of self-reflection enjoyable."""
}

class AICompanionService:
    @staticmethod
    def _get_client():
        """Get OpenAI client or None if unavailable"""
        global client
        if client is None:
            try:
                from openai import OpenAI
                if settings.OPENAI_API_KEY and settings.OPENAI_API_KEY.startswith('sk-proj-') and len(settings.OPENAI_API_KEY) > 20:
                    # Try to create client, but don't fail if key is invalid
                    try:
                        client = OpenAI(api_key=settings.OPENAI_API_KEY)
                        # Test the key with a simple call
                        client.models.list()
                        return client
                    except:
                        return None
            except:
                pass
        return client
    
    @staticmethod
    async def generate_response(
        user_message: str,
        personality: CompanionPersonality,
        conversation_history: List[Dict],
        user_context: Dict,
        custom_instructions: str = None
    ) -> Dict:
        """Generate AI companion response based on personality and context"""
        
        # Get client or use mock
        ai_client = AICompanionService._get_client()
        
        if not ai_client:
            mock_responses = [
                "That's really interesting! Tell me more about what you're thinking.",
                "I hear you. Writing to your future self is a powerful way to reflect on your journey.",
                "What would you want your future self to remember about this moment?",
                "That sounds meaningful. How do you think you'll feel when you receive this message?",
                "I'm here to help you craft something special. What matters most to you right now?"
            ]
            return {
                "response": random.choice(mock_responses),
                "detected_emotion": "reflective",
                "suggestions": ["💡 Create a message about this moment", "🎯 Let AI choose the perfect timing"]
            }
        
        system_prompt = f"""{PERSONALITY_PROMPTS[personality]}

You are "Future Buddy", an AI companion in the "Future You" app - a platform where users write messages to their future selves.

Your role:
- Help users craft meaningful messages to their future selves
- Provide emotional support and reflection
- Ask thought-provoking questions
- Celebrate their growth and progress
- Suggest optimal timing for message delivery
- Detect emotional state and respond appropriately

User Context: {user_context}

{f'Additional Instructions: {custom_instructions}' if custom_instructions else ''}

Keep responses conversational, warm, and under 150 words unless the user needs more depth.
Always prioritize the user's emotional wellbeing and privacy."""

        messages = [{"role": "system", "content": system_prompt}]
        
        for msg in conversation_history[-10:]:
            messages.append({"role": "user", "content": msg["user_message"]})
            messages.append({"role": "assistant", "content": msg["companion_response"]})
        
        messages.append({"role": "user", "content": user_message})
        
        response = ai_client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=messages,
            temperature=0.8,
            max_tokens=300
        )
        
        companion_response = response.choices[0].message.content
        emotion = await AICompanionService._detect_emotion(user_message)
        
        return {
            "response": companion_response,
            "detected_emotion": emotion,
            "suggestions": await AICompanionService._generate_suggestions(user_message, user_context)
        }
    
    @staticmethod
    async def _detect_emotion(text: str) -> str:
        """Detect emotional tone from user message"""
        ai_client = AICompanionService._get_client()
        if not ai_client:
            return "reflective"
        
        response = ai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{
                "role": "system",
                "content": "Analyze the emotional tone. Respond with ONE word: happy, sad, anxious, excited, reflective, frustrated, hopeful, or neutral."
            }, {
                "role": "user",
                "content": text
            }],
            temperature=0.3,
            max_tokens=10
        )
        return response.choices[0].message.content.strip().lower()
    
    @staticmethod
    async def _generate_suggestions(user_message: str, user_context: Dict) -> List[str]:
        """Generate helpful suggestions based on conversation"""
        suggestions = []
        
        # Message creation suggestion
        if any(word in user_message.lower() for word in ["struggling", "difficult", "hard", "challenge"]):
            suggestions.append("💡 Create a message to your future self about overcoming this challenge")
        
        # Timing suggestion
        if any(word in user_message.lower() for word in ["when", "timing", "deliver"]):
            suggestions.append("🎯 Let AI determine the perfect moment to deliver this message")
        
        # Reflection suggestion
        if any(word in user_message.lower() for word in ["achieved", "accomplished", "proud"]):
            suggestions.append("✨ Record a reaction to capture this moment")
        
        return suggestions[:3]  # Max 3 suggestions
    
    @staticmethod
    async def generate_daily_checkin(personality: CompanionPersonality, user_context: Dict) -> str:
        """Generate personalized daily check-in message"""
        system_prompt = f"""{PERSONALITY_PROMPTS[personality]}

Generate a brief, warm daily check-in message (2-3 sentences) for the user.
Make it personal based on their context: {user_context}
Ask an engaging question or offer a thoughtful prompt for the day."""

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": system_prompt}],
            temperature=0.9,
            max_tokens=100
        )
        
        return response.choices[0].message.content
    
    @staticmethod
    async def help_craft_message(
        user_intent: str,
        personality: CompanionPersonality,
        user_context: Dict
    ) -> Dict:
        """Help user craft a message to their future self"""
        system_prompt = f"""{PERSONALITY_PROMPTS[personality]}

The user wants to create a message to their future self. Help them craft something meaningful.

User's intent: {user_intent}
User context: {user_context}

Provide:
1. A draft message they can use or modify
2. Suggested delivery timing
3. Why this message matters

Format as JSON with keys: draft_message, suggested_timing, reasoning"""

        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[{"role": "system", "content": system_prompt}],
            temperature=0.7,
            max_tokens=400,
            response_format={"type": "json_object"}
        )
        
        import json
        return json.loads(response.choices[0].message.content)
