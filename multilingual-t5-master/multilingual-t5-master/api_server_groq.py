"""
mT5 Translation API with Groq AI Integration
Uses Groq's LLM for intelligent multilingual translations
"""

from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
from groq import Groq
import os
from datetime import datetime
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="mT5 Translation API with Groq AI",
    description="Multilingual Translation Service powered by Groq",
    version="2.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Groq Client (will be initialized with API key from request)
def get_groq_client(api_key: str) -> Groq:
    """Initialize Groq client with provided API key"""
    return Groq(api_key=api_key)

# API Key validation
VALID_API_KEYS = {
    "test-key-12345": "demo_user",
    os.getenv("API_KEY", "your-api-key-here"): "admin"
}

# Pydantic models
class TranslateRequest(BaseModel):
    text: str
    source_lang: str
    target_lang: str
    mode: Optional[str] = "simple"
    groq_api_key: Optional[str] = None

class TranslateResponse(BaseModel):
    translation: str
    source_lang: str
    target_lang: str
    confidence: float = 0.95
    mode: str = "simple"
    model: str = "groq"

class BatchTranslateRequest(BaseModel):
    texts: List[str]
    source_lang: str
    target_lang: str
    groq_api_key: Optional[str] = None

class ChatRequest(BaseModel):
    message: str
    conversation_history: Optional[List[dict]] = None
    groq_api_key: Optional[str] = None

class HealthResponse(BaseModel):
    status: str
    timestamp: str
    version: str
    ai_engine: str = "groq"

# API Key dependency
async def verify_api_key(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing authorization header")
    
    try:
        scheme, credentials = authorization.split()
        if scheme.lower() != "bearer":
            raise HTTPException(status_code=401, detail="Invalid authorization scheme")
        
        if credentials not in VALID_API_KEYS:
            raise HTTPException(status_code=401, detail="Invalid API key")
        
        return VALID_API_KEYS[credentials]
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid authorization header")

# Translation with Groq AI
def translate_with_groq(text: str, source_lang: str, target_lang: str, groq_api_key: str, mode: str = "simple") -> str:
    """Translate using Groq API"""
    try:
        client = get_groq_client(groq_api_key)
        
        if mode == "chain":
            # Prompt chain approach for better accuracy
            prompts = [
                f"Detect the language of this text and respond with ONLY the language name:\n'{text}'",
                f"Explain the meaning of this text in simple English (meaning only, no translation):\n'{text}'",
                f"Translate this meaning to {target_lang} naturally (translate only, no explanation):\n'{text}'",
                f"Refine this translation for grammar and fluency (improve only):\n'[translation]'"
            ]
        else:
            # Simple direct translation
            prompts = [
                f"Translate this text from {source_lang} to {target_lang}. Respond with ONLY the translation, no explanation:\n'{text}'"
            ]
        
        for prompt in prompts:
            message = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                model="llama-3.1-8b-instant",  # Updated Groq model
                max_tokens=1024,
                temperature=0.3,  # Lower temperature for consistency
            )
            result = message.choices[0].message.content.strip()
        
        return result
    
    except Exception as e:
        logger.error(f"Groq translation error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Translation error: {str(e)}")

# Routes

@app.get("/health", response_model=HealthResponse)
async def health_check(user: str = Depends(verify_api_key)):
    """Check API health"""
    return {
        "status": "ok",
        "timestamp": datetime.now().isoformat(),
        "version": "2.0.0",
        "ai_engine": "groq"
    }

@app.post("/translate", response_model=TranslateResponse)
async def translate(
    request: TranslateRequest,
    user: str = Depends(verify_api_key)
):
    """Translate text using Groq AI"""
    
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    if not request.groq_api_key:
        raise HTTPException(status_code=400, detail="Groq API key is required")
    
    if request.source_lang == request.target_lang:
        raise HTTPException(status_code=400, detail="Source and target languages must be different")
    
    try:
        # Get translation from Groq
        translation = translate_with_groq(
            request.text,
            request.source_lang,
            request.target_lang,
            request.groq_api_key,
            request.mode
        )
        
        logger.info(f"Translation: {request.source_lang}→{request.target_lang} | User: {user} | Mode: {request.mode}")
        
        return {
            "translation": translation,
            "source_lang": request.source_lang,
            "target_lang": request.target_lang,
            "confidence": 0.95,
            "mode": request.mode,
            "model": "groq-mixtral-8x7b"
        }
    
    except Exception as e:
        logger.error(f"Translation error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Translation failed: {str(e)}")

@app.post("/translate-batch")
async def translate_batch(
    request: BatchTranslateRequest,
    user: str = Depends(verify_api_key)
):
    """Batch translate multiple texts with Groq"""
    
    if not request.texts:
        raise HTTPException(status_code=400, detail="Texts list cannot be empty")
    
    if not request.groq_api_key:
        raise HTTPException(status_code=400, detail="Groq API key is required")
    
    try:
        translations = []
        for text in request.texts:
            translation = translate_with_groq(
                text,
                request.source_lang,
                request.target_lang,
                request.groq_api_key
            )
            translations.append({
                "original": text,
                "translation": translation
            })
        
        logger.info(f"Batch translation: {len(translations)} items | User: {user}")
        
        return {
            "count": len(translations),
            "translations": translations,
            "model": "groq-mixtral-8x7b"
        }
    
    except Exception as e:
        logger.error(f"Batch translation error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Batch translation failed: {str(e)}")

@app.post("/chat")
async def chat_with_ai(
    request: ChatRequest,
    user: str = Depends(verify_api_key)
):
    """General AI chat endpoint using Groq"""
    
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")
    
    if not request.groq_api_key:
        raise HTTPException(status_code=400, detail="Groq API key is required")
    
    try:
        client = get_groq_client(request.groq_api_key)
        
        # Build conversation history
        messages = request.conversation_history or []
        messages.append({
            "role": "user",
            "content": request.message
        })
        
        # Get response from Groq
        response = client.chat.completions.create(
            messages=messages,
            model="llama-3.1-8b-instant",  # Updated Groq model
            max_tokens=2048,
            temperature=0.7,
        )
        
        assistant_message = response.choices[0].message.content
        
        logger.info(f"Chat: {user} | Tokens used")
        
        return {
            "response": assistant_message,
            "timestamp": datetime.now().isoformat(),
            "model": "groq-mixtral-8x7b"
        }
    
    except Exception as e:
        logger.error(f"Chat error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Chat failed: {str(e)}")

@app.get("/languages")
async def get_languages(user: str = Depends(verify_api_key)):
    """Get supported languages"""
    return {
        "languages": {
            "en": "English",
            "es": "Spanish",
            "fr": "French",
            "de": "German",
            "zh": "Chinese (Simplified)",
            "ja": "Japanese",
            "ru": "Russian",
            "pt": "Portuguese",
            "it": "Italian",
            "ar": "Arabic",
            "hi": "Hindi",
            "bn": "Bengali",
            "te": "Telugu",
            "kn": "Kannada",
            "ta": "Tamil",
            "tr": "Turkish",
            "vi": "Vietnamese",
            "th": "Thai",
            "ko": "Korean",
            "pl": "Polish",
        },
        "total": 20,
        "ai_engine": "groq"
    }

@app.get("/api/models")
async def list_models(user: str = Depends(verify_api_key)):
    """List available Groq models"""
    return {
        "models": [
            {
                "name": "mixtral-8x7b-32768",
                "provider": "Groq",
                "speed": "Ultra-fast",
                "capabilities": ["Translation", "Chat", "Analysis"],
                "context": "32K tokens",
                "description": "Powerful open-source model optimized for speed"
            },
            {
                "name": "llama2-70b-4096",
                "provider": "Groq",
                "speed": "Fast",
                "capabilities": ["Translation", "Chat", "Analysis"],
                "context": "4K tokens",
                "description": "Meta's Llama 2 large model"
            }
        ],
        "recommended": "mixtral-8x7b-32768"
    }

@app.get("/")
async def root():
    """API root endpoint"""
    return {
        "service": "mT5 Translation API with Groq AI",
        "version": "2.0.0",
        "ai_engine": "Groq - Fast Inference API",
        "documentation": "/docs",
        "health": "/health"
    }

# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    from fastapi.responses import JSONResponse
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code,
            "timestamp": datetime.now().isoformat()
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
