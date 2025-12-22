"""
mT5 Translation API Server
Provides endpoints for language translation using mT5 model
"""

from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import os
from datetime import datetime
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="mT5 Translation API",
    description="Multilingual T5 Translation Service",
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

class TranslateResponse(BaseModel):
    translation: str
    source_lang: str
    target_lang: str
    confidence: float = 0.95
    mode: str = "simple"

class BatchTranslateRequest(BaseModel):
    texts: List[str]
    source_lang: str
    target_lang: str

class HealthResponse(BaseModel):
    status: str
    timestamp: str
    version: str

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

# Mock translation function (replace with actual mT5 model)
def mock_translate(text: str, source_lang: str, target_lang: str, mode: str = "simple") -> str:
    """Mock translation - replace with actual mT5 model"""
    translations = {
        ("hello", "es"): "hola",
        ("hello world", "fr"): "bonjour le monde",
        ("good morning", "de"): "guten morgen",
        ("thank you", "zh"): "谢谢",
        ("i am preparing for an exam tomorrow", "en"): "నేను రేపు పరీక్షకు సిద్ధమవుతున్నాను",
    }
    
    text_lower = text.lower()
    key = (text_lower, target_lang)
    
    if key in translations:
        return translations[key]
    
    # Default mock response
    if mode == "chain":
        return f"[Chain] {text} → {target_lang}"
    return f"[Translated] {text} → {target_lang}"

# Routes

@app.get("/health", response_model=HealthResponse)
async def health_check(user: str = Depends(verify_api_key)):
    """Check API health"""
    return {
        "status": "ok",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }

@app.post("/translate", response_model=TranslateResponse)
async def translate(
    request: TranslateRequest,
    user: str = Depends(verify_api_key)
):
    """Translate text using mT5"""
    
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    if request.source_lang == request.target_lang:
        raise HTTPException(status_code=400, detail="Source and target languages must be different")
    
    try:
        # Get translation (mock for now)
        translation = mock_translate(
            request.text,
            request.source_lang,
            request.target_lang,
            request.mode
        )
        
        logger.info(f"Translation: {request.source_lang}→{request.target_lang} | User: {user}")
        
        return {
            "translation": translation,
            "source_lang": request.source_lang,
            "target_lang": request.target_lang,
            "confidence": 0.95,
            "mode": request.mode
        }
    
    except Exception as e:
        logger.error(f"Translation error: {str(e)}")
        raise HTTPException(status_code=500, detail="Translation failed")

@app.post("/translate-batch")
async def translate_batch(
    request: BatchTranslateRequest,
    user: str = Depends(verify_api_key)
):
    """Batch translate multiple texts"""
    
    if not request.texts:
        raise HTTPException(status_code=400, detail="Texts list cannot be empty")
    
    try:
        translations = []
        for text in request.texts:
            translation = mock_translate(text, request.source_lang, request.target_lang)
            translations.append({
                "original": text,
                "translation": translation
            })
        
        logger.info(f"Batch translation: {len(translations)} items | User: {user}")
        
        return {
            "count": len(translations),
            "translations": translations
        }
    
    except Exception as e:
        logger.error(f"Batch translation error: {str(e)}")
        raise HTTPException(status_code=500, detail="Batch translation failed")

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
        }
    }

@app.get("/api/models")
async def list_models(user: str = Depends(verify_api_key)):
    """List available translation models"""
    return {
        "models": [
            {
                "name": "mT5-base",
                "size": "580M",
                "parameters": 580_000_000,
                "languages": 101,
                "description": "Base multilingual T5 model"
            },
            {
                "name": "mT5-small",
                "size": "300M",
                "parameters": 300_000_000,
                "languages": 101,
                "description": "Small multilingual T5 model"
            },
            {
                "name": "mT5-large",
                "size": "1.2B",
                "parameters": 1_200_000_000,
                "languages": 101,
                "description": "Large multilingual T5 model"
            }
        ]
    }

@app.get("/")
async def root():
    """API root endpoint"""
    return {
        "service": "mT5 Translation API",
        "version": "1.0.0",
        "documentation": "/docs",
        "health": "/health"
    }

# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return {
        "error": exc.detail,
        "status_code": exc.status_code,
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
