"""
Pydantic models for request/response validation
"""
from typing import List, Dict, Optional
from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    """Individual chat message"""
    content: str = Field(..., description="Message content")
    timestamp: Optional[str] = Field(None, description="Message timestamp")
    sender: str = Field(default="user", description="Message sender")


class MemoryExtractionRequest(BaseModel):
    """Request for memory extraction from chat messages"""
    messages: List[ChatMessage] = Field(..., min_length=1, max_length=50)


class UserPreferences(BaseModel):
    """Extracted user preferences"""
    likes: List[str] = Field(default_factory=list)
    dislikes: List[str] = Field(default_factory=list)
    habits: List[str] = Field(default_factory=list)
    interests: List[str] = Field(default_factory=list)


class EmotionalPatterns(BaseModel):
    """Extracted emotional patterns"""
    dominant_emotions: List[str] = Field(default_factory=list)
    emotional_triggers: List[str] = Field(default_factory=list)
    communication_style: str = Field(default="neutral")
    stress_indicators: List[str] = Field(default_factory=list)


class ImportantFacts(BaseModel):
    """Extracted important facts"""
    personal_info: List[str] = Field(default_factory=list)
    relationships: List[str] = Field(default_factory=list)
    goals: List[str] = Field(default_factory=list)
    events: List[str] = Field(default_factory=list)


class UserMemory(BaseModel):
    """Complete user memory structure"""
    preferences: UserPreferences
    emotional_patterns: EmotionalPatterns
    facts: ImportantFacts
    summary: str = Field(default="")


class PersonalityType(BaseModel):
    """Available personality types"""
    name: str = Field(..., description="Personality name")
    description: str = Field(..., description="Personality description")


class PersonalityRequest(BaseModel):
    """Request for personality transformation"""
    message: str = Field(..., description="User message to respond to")
    personality: str = Field(..., description="Personality type to use")
    context: Optional[UserMemory] = Field(None, description="User memory context")
    history: Optional[List[ChatMessage]] = Field(default=None, description="Chat history for context")


class PersonalityResponse(BaseModel):
    """Response with personality transformation"""
    original_response: str
    transformed_response: str
    personality_used: str


class ComparePersonalitiesRequest(BaseModel):
    """Request to compare all personalities"""
    message: str = Field(..., description="User message to respond to")
    context: Optional[UserMemory] = Field(None, description="User memory context")


class PersonalityComparison(BaseModel):
    """Comparison of all personality responses"""
    message: str
    responses: Dict[str, str] = Field(..., description="Personality name -> response mapping")
