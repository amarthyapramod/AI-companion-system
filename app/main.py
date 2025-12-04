"""
FastAPI Application - AI Companion System
"""
import os
import json
from typing import Dict
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.models import (
    MemoryExtractionRequest,
    UserMemory,
    PersonalityRequest,
    PersonalityResponse,
    ComparePersonalitiesRequest,
    PersonalityComparison
)
from app.core.memory_extractor import MemoryExtractor
from app.core.personality_engine import PersonalityEngine

# Initialize FastAPI app
app = FastAPI(
    title="AI Companion System",
    description="Memory extraction and personality transformation engine",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize AI modules
memory_extractor = MemoryExtractor()
personality_engine = PersonalityEngine()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def root():
    """Serve the main HTML page"""
    return FileResponse("static/index.html")


@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "AI Companion System",
        "version": "1.0.0"
    }


@app.get("/api/personalities")
async def get_personalities():
    """Get available personality types"""
    return personality_engine.get_available_personalities()


@app.get("/api/sample-messages")
async def get_sample_messages():
    with open("static/sample_messages.json", "r") as f:
        return json.load(f)


@app.post("/api/extract-memory", response_model=UserMemory)
async def extract_memory(request: MemoryExtractionRequest):
    memory = memory_extractor.extract_memory(request.messages)
    return memory


@app.post("/api/transform-personality", response_model=PersonalityResponse)
async def transform_personality(request: PersonalityRequest):
    original, transformed = personality_engine.transform_response(
        message=request.message,
        personality=request.personality,
        context=request.context,
        history=request.history
    )
    
    return PersonalityResponse(
        original_response=original,
        transformed_response=transformed,
        personality_used=request.personality
    )


@app.post("/api/compare-personalities", response_model=PersonalityComparison)
async def compare_personalities(request: ComparePersonalitiesRequest):
    responses = personality_engine.compare_all_personalities(
        message=request.message,
        context=request.context
    )
    
    return PersonalityComparison(
        message=request.message,
        responses=responses
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
