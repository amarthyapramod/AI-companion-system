"""
Personality Engine
Transforms agent responses based on different personality profiles
"""
import os
from typing import Dict, Optional, List
import google.generativeai as genai
from dotenv import load_dotenv

from app.models import UserMemory, ChatMessage

load_dotenv()


class PersonalityEngine:
    """Transform responses based on personality profiles"""
    
    # Define personality profiles
    PERSONALITIES = {
        "calm_mentor": {
            "name": "Calm Mentor",
            "description": "Wise, patient, and guidance-focused. Speaks with measured wisdom and encourages reflection.",
            "traits": [
                "Uses thoughtful, measured language",
                "Asks reflective questions",
                "Shares wisdom through analogies and examples",
                "Patient and non-judgmental",
                "Focuses on long-term growth and learning"
            ],
            "tone": "calm, wise, encouraging, patient"
        },
        "witty_friend": {
            "name": "Witty Friend",
            "description": "Casual, humorous, and relatable. Like chatting with a close friend who makes you laugh.",
            "traits": [
                "Uses casual, conversational language",
                "Incorporates humor and wit",
                "Relatable and down-to-earth",
                "Uses modern slang appropriately",
                "Supportive but keeps things light"
            ],
            "tone": "casual, funny, relatable, friendly"
        },
        "therapist": {
            "name": "Therapist",
            "description": "Empathetic, reflective, and supportive. Creates a safe space for emotional exploration.",
            "traits": [
                "Deeply empathetic and validating",
                "Asks open-ended questions",
                "Reflects feelings back to the user",
                "Non-directive and supportive",
                "Focuses on emotional processing"
            ],
            "tone": "empathetic, gentle, validating, supportive"
        },
        "professional_coach": {
            "name": "Professional Coach",
            "description": "Direct, goal-oriented, and motivational. Pushes you toward action and results.",
            "traits": [
                "Direct and action-oriented",
                "Focuses on goals and outcomes",
                "Motivational and energizing",
                "Holds you accountable",
                "Provides structured frameworks"
            ],
            "tone": "direct, motivating, energetic, results-focused"
        },
        "curious_explorer": {
            "name": "Curious Explorer",
            "description": "Inquisitive, enthusiastic, and discovery-focused. Loves diving deep into ideas.",
            "traits": [
                "Asks lots of curious questions",
                "Enthusiastic about learning",
                "Explores ideas from multiple angles",
                "Encourages experimentation",
                "Shares interesting connections and insights"
            ],
            "tone": "curious, enthusiastic, exploratory, wonder-filled"
        }
    }
    
    def __init__(self):
        api_key = os.getenv("GOOGLE_API_KEY")
        if api_key:
            try:
                genai.configure(api_key=api_key)
                self.model = genai.GenerativeModel('gemini-2.5-flash')
            except Exception as e:
                print(f"[PersonalityEngine] Failed to initialize AI: {e}")
                self.model = None
        else:
            print("[PersonalityEngine] No API key found, using fallback mode")
            self.model = None
    
    def get_available_personalities(self) -> Dict[str, Dict[str, str]]:
        """Get list of available personalities"""
        return {
            key: {
                "name": profile["name"],
                "description": profile["description"]
            }
            for key, profile in self.PERSONALITIES.items()
        }
    
    def transform_response(
        self, 
        message: str, 
        personality: str,
        context: Optional[UserMemory] = None,
        history: Optional[List[ChatMessage]] = None
    ) -> tuple[str, str]:
        original_response = self._generate_base_response(message, context, history)
        
        # Transform with personality
        if personality not in self.PERSONALITIES:
            personality = "calm_mentor"  # Default fallback
        
        transformed_response = self._apply_personality(
            message, 
            original_response, 
            personality,
            context,
            history
        )
        
        return original_response, transformed_response
    
    def compare_all_personalities(
        self, 
        message: str,
        context: Optional[UserMemory] = None
    ) -> Dict[str, str]:
        import concurrent.futures
        
        responses = {}
        
        def get_response(p_key):
            _, t_response = self.transform_response(message, p_key, context)
            return self.PERSONALITIES[p_key]["name"], t_response

        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            future_to_name = {
                executor.submit(get_response, key): key 
                for key in self.PERSONALITIES.keys()
            }
            
            for future in concurrent.futures.as_completed(future_to_name):
                try:
                    name, response = future.result()
                    responses[name] = response
                except Exception as e:
                    print(f"Error generating response for {future_to_name[future]}: {e}")
                    key = future_to_name[future]
                    name = self.PERSONALITIES[key]["name"]
                    responses[name] = f"[{name}] (Generation failed)"
        
        return responses
    
    def _generate_base_response(
        self, 
        message: str,
        context: Optional[UserMemory] = None,
        history: Optional[List[ChatMessage]] = None
    ) -> str:
        context_str = ""
        if context:
            context_str = f"\n\nUser Context:\n{context.summary}"
        
        history_str = ""
        if history:
            history_str = "\n\nPrevious Conversation:\n" + "\n".join(
                f"{msg.sender}: {msg.content}" for msg in history
            )

        prompt = f"""Generate a helpful, neutral response to the user's message.{context_str}{history_str}
 
User Message: {message}
 
Provide a clear, informative response that addresses their message."""
        
        if self.model:
            try:
                response = self.model.generate_content(prompt)
                return response.text.strip()
            except Exception as e:
                print(f"[PersonalityEngine] Warning: generate_content failed: {e}")
        # Fallback: simple deterministic response
        return f"[Base response] {message}"
    
    def _apply_personality(
        self,
        message: str,
        base_response: str,
        personality: str,
        context: Optional[UserMemory] = None,
        history: Optional[List[ChatMessage]] = None
    ) -> str:
        profile = self.PERSONALITIES[personality]
        
        context_str = ""
        if context:
            context_str = f"\n\nUser Context:\n{context.summary}"
            
        history_str = ""
        if history:
            history_str = "\n\nPrevious Conversation:\n" + "\n".join(
                f"{msg.sender}: {msg.content}" for msg in history
            )
        
        traits_str = "\n".join(f"- {trait}" for trait in profile["traits"])
        
        prompt = f"""You are transforming a response to match a specific personality profile.

PERSONALITY: {profile['name']}
DESCRIPTION: {profile['description']}
TONE: {profile['tone']}

KEY TRAITS:
{traits_str}

USER MESSAGE: {message}{history_str}
 
BASE RESPONSE: {base_response}{context_str}

Transform the base response to fully embody the {profile['name']} personality. 
- Rewrite it completely in this personality's voice and style
- Maintain the core helpful information
- Make it feel authentic to this personality
- Keep it natural and conversational
- Use the personality's characteristic language patterns and approach
- DO NOT include the personality name or "[Base response]" in your output.
- DO NOT prefix the response with "TRANSFORMED RESPONSE:".
- Just provide the transformed message directly.

TRANSFORMED RESPONSE:"""
        
        if self.model:
            try:
                response = self.model.generate_content(prompt)
                text = response.text.strip()
                return text
            except Exception as e:
                print(f"[PersonalityEngine] Warning: generate_content failed: {e}")
        # Fallback: prepend personality name to base response
        return f"[{self.PERSONALITIES[personality]['name']}] {base_response}"
