# 🧠 AI Companion System

An advanced AI companion system demonstrating memory extraction and personality transformation capabilities.

## 🎯 Overview

This system showcases:
- **Memory Extraction Module**: Analyzes chat messages to extract user preferences, emotional patterns, and important facts
- **Personality Engine**: Transforms AI responses across 5 distinct personalities
- **Interactive Chat**: Continuous conversation with context awareness

## ✨ Features

### Memory Extraction
Analyzes conversations to identify:
- **User Preferences**: Likes, dislikes, habits, and interests
- **Emotional Patterns**: Dominant emotions, triggers, communication style, stress indicators
- **Important Facts**: Personal info, relationships, goals, and events

### Personality Engine
5 distinct personalities with unique response styles:
- **Calm Mentor**: Wise, patient, guidance-focused
- **Witty Friend**: Casual, humorous, relatable
- **Therapist**: Empathetic, reflective, supportive
- **Professional Coach**: Direct, goal-oriented, motivational
- **Curious Explorer**: Inquisitive, enthusiastic, discovery-focused

### Interactive Chat
- Real-time conversation with selected personality
- Context-aware responses using chat history
- Typing indicators for better UX
- Distinct message bubbles for user and AI

## 🏗️ Architecture

```
mvp1/
├── app/
│   ├── core/
│   │   ├── memory_extractor.py    # Memory extraction logic
│   │   └── personality_engine.py   # Personality transformation
│   ├── models.py                   # Pydantic data models
│   └── main.py                     # FastAPI application
├── static/
│   ├── index.html                  # Frontend interface
│   ├── styles.css                  # Modern styling
│   ├── script.js                   # API interactions
│   └── sample_messages.json        # Test data
├── requirements.txt                # Python dependencies
└── README.md
```

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Google Generative AI API key ([Get one here](https://makersuite.google.com/app/apikey))

### Installation

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd mvp1
```

2. **Create virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env and add your GOOGLE_API_KEY
```

5. **Run the application**
```bash
uvicorn app.main:app --reload
```

6. **Open browser**
Navigate to `http://localhost:8000`

## 📡 API Endpoints

### Health Check
```
GET /api/health
```

### Get Available Personalities
```
GET /api/personalities
```

### Get Sample Messages
```
GET /api/sample-messages
```

### Extract Memory
```
POST /api/extract-memory
Body: {
  "messages": [
    {"content": "message text", "sender": "user"}
  ]
}
```

### Transform with Personality
```
POST /api/transform-personality
Body: {
  "message": "user message",
  "personality": "calm_mentor",
  "history": []  // optional chat history
}
```

### Compare All Personalities
```
POST /api/compare-personalities
Body: {
  "message": "user message"
}
```

## 🧪 Testing

### Using the Web Interface
1. Open `http://localhost:8000`
2. **Memory Extraction**: Click "Load Sample Messages" → "Extract Memory"
3. **Personality Comparison**: Enter a message → "Compare All Personalities"
4. **Interactive Chat**: Select a personality → Start chatting

### API Documentation
Visit `http://localhost:8000/docs` for interactive API documentation

## 🎨 Design Decisions

### Technology Stack
- **FastAPI**: High-performance async framework
- **Google Generative AI (Gemini 2.5 Flash)**: Fast, cost-effective LLM
- **Pydantic**: Type-safe data validation
- **Vanilla JS**: Minimal frontend, no framework overhead

### Architectural Patterns
- **Separation of Concerns**: Core AI logic separated from API layer
- **Structured Prompting**: Carefully designed prompts for consistent outputs
- **Error Handling**: Graceful degradation with informative error messages
- **Modular Design**: Easy to extend with new personalities or memory types

### Key Features
- **Parallel Processing**: Compare all personalities 5x faster using ThreadPoolExecutor
- **Context Awareness**: Chat history integration for coherent conversations
- **Graceful Degradation**: Fallback responses if AI service is unavailable
- **Modern UI**: Dark theme with glassmorphism effects

## 🎓 Alignment with GuppShupp Requirements

### LLM Prompting Pipelines ✅
- Advanced prompt engineering for memory extraction
- Context-aware personality transformations
- Structured output parsing with JSON schemas

### AI Memory Systems ✅
- Persistent memory extraction from conversations
- Multi-dimensional user profiling (preferences, emotions, facts)
- Context integration in personality responses

### Production-Ready Code ✅
- Type-safe with Pydantic models
- Proper error handling and logging
- Scalable FastAPI architecture
- Clean, maintainable codebase

### First-Principles Thinking ✅
- Modular system design from ground up
- Clear separation between extraction and transformation
- Extensible architecture for future enhancements

## 🚢 Deployment

### Render (Recommended)
1. Push code to GitHub
2. Create new Web Service on [Render](https://render.com)
3. Connect your repository
4. Configure:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Add environment variable: `GOOGLE_API_KEY`
6. Deploy!

### Railway
1. Push code to GitHub
2. Create new project on [Railway](https://railway.app)
3. Connect repository
4. Add `GOOGLE_API_KEY` environment variable
5. Railway auto-deploys

### Vercel (Serverless)
1. Install Vercel CLI: `npm i -g vercel`
2. Run `vercel` in project directory
3. Add `GOOGLE_API_KEY` in dashboard
4. Deploy

## 🔧 Environment Variables

```bash
GOOGLE_API_KEY=your_api_key_here  # Required
```

## 📊 Performance

- **Memory Extraction**: ~2-3 seconds for 30 messages
- **Personality Transformation**: ~1-2 seconds per response
- **Parallel Comparison**: ~2-3 seconds for all 5 personalities (vs ~10 seconds sequential)

## 🛠️ Tech Stack

- **Backend**: FastAPI, Python 3.9+
- **AI**: Google Generative AI (Gemini 2.5 Flash)
- **Validation**: Pydantic
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Deployment**: Render/Railway/Vercel

## 📝 License

MIT License

---

**Built with ❤️ for AI companion systems**
