"""
Memory Extraction Module
Identifies user preferences, emotional patterns, and important facts from chat messages
"""
import os
import json
from typing import List
import google.generativeai as genai
from dotenv import load_dotenv

from app.models import (
    ChatMessage, UserMemory, UserPreferences, 
    EmotionalPatterns, ImportantFacts
)

load_dotenv()


class MemoryExtractor:
    """Extract and structure user memory from chat messages"""
    
    def __init__(self):
        """Initialize the memory extractor with Google Generative AI"""
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')
    
    def extract_memory(self, messages: List[ChatMessage]) -> UserMemory:
        conversation = self._format_messages(messages)
        prompt = self._create_extraction_prompt(conversation)
        response = self.model.generate_content(prompt)
        memory = self._parse_memory_response(response.text)
        return memory
    
    def _format_messages(self, messages: List[ChatMessage]) -> str:
        formatted = []
        for i, msg in enumerate(messages, 1):
            formatted.append(f"Message {i}: {msg.content}")
        return "\n".join(formatted)
    
    def _create_extraction_prompt(self, conversation: str) -> str:
        return f"""You are an expert at analyzing conversations and extracting meaningful insights about users.

Analyze the following conversation and extract structured information about the user.

CONVERSATION:
{conversation}

Extract the following information in JSON format:

1. PREFERENCES:
   - likes: Things the user enjoys, prefers, or shows positive sentiment toward
   - dislikes: Things the user dislikes, avoids, or shows negative sentiment toward
   - habits: Recurring behaviors, routines, or patterns
   - interests: Topics, hobbies, or areas the user is interested in

2. EMOTIONAL_PATTERNS:
   - dominant_emotions: Most frequently expressed emotions (e.g., anxious, excited, frustrated, happy)
   - emotional_triggers: Topics or situations that evoke strong emotions
   - communication_style: How the user communicates (e.g., direct, verbose, casual, formal)
   - stress_indicators: Signs of stress, worry, or overwhelm

3. FACTS:
   - personal_info: Factual information about the user (name, age, location, occupation, etc.)
   - relationships: Information about family, friends, colleagues, pets
   - goals: Aspirations, objectives, or things they're working toward
   - events: Important events, milestones, or experiences mentioned

4. SUMMARY: A brief 2-3 sentence summary of the user's overall profile

Return ONLY valid JSON in this exact structure:
{{
  "preferences": {{
    "likes": ["item1", "item2"],
    "dislikes": ["item1", "item2"],
    "habits": ["habit1", "habit2"],
    "interests": ["interest1", "interest2"]
  }},
  "emotional_patterns": {{
    "dominant_emotions": ["emotion1", "emotion2"],
    "emotional_triggers": ["trigger1", "trigger2"],
    "communication_style": "description",
    "stress_indicators": ["indicator1", "indicator2"]
  }},
  "facts": {{
    "personal_info": ["fact1", "fact2"],
    "relationships": ["relationship1", "relationship2"],
    "goals": ["goal1", "goal2"],
    "events": ["event1", "event2"]
  }},
  "summary": "Brief summary of the user"
}}

Be specific and extract actual details from the conversation. If a category has no information, use an empty list or empty string."""
    
    def _parse_memory_response(self, response_text: str) -> UserMemory:
        try:
            # Extract JSON from response (handle markdown code blocks)
            json_text = response_text.strip()
            if json_text.startswith("```json"):
                json_text = json_text[7:]
            if json_text.startswith("```"):
                json_text = json_text[3:]
            if json_text.endswith("```"):
                json_text = json_text[:-3]
            json_text = json_text.strip()
            
            # Parse JSON
            data = json.loads(json_text)
            
            # Create structured objects
            preferences = UserPreferences(**data.get("preferences", {}))
            emotional_patterns = EmotionalPatterns(**data.get("emotional_patterns", {}))
            facts = ImportantFacts(**data.get("facts", {}))
            
            return UserMemory(
                preferences=preferences,
                emotional_patterns=emotional_patterns,
                facts=facts,
                summary=data.get("summary", "")
            )
        except Exception as e:
            print(f"Error parsing memory: {e}")
            return UserMemory(
                preferences=UserPreferences(),
                emotional_patterns=EmotionalPatterns(),
                facts=ImportantFacts(),
                summary="Unable to extract memory"
            )

