"""
mT5 CHATBOT & API SYSTEM - ARCHITECTURE OVERVIEW

This document explains how all components work together
"""

# ============================================================================
#  SYSTEM ARCHITECTURE
# ============================================================================

                    ┌─────────────────────────────────┐
                    │   USER (Web Browser)            │
                    │   http://localhost:8501         │
                    └────────────────┬────────────────┘
                                     │
                    ┌────────────────▼────────────────┐
                    │   STREAMLIT DASHBOARD           │
                    │   (app_enhanced.py)             │
                    │                                 │
                    │   ├─ 💬 Chatbot Interface       │
                    │   ├─ 🔑 API Key Manager        │
                    │   ├─ 📊 History & Export       │
                    │   ├─ 📖 API Documentation      │
                    │   └─ ⚙️  Advanced Settings      │
                    └────────────────┬────────────────┘
                                     │
                    ┌────────────────▼────────────────┐
                    │   HTTP REQUESTS (JSON)          │
                    │   + Bearer Token Auth           │
                    └────────────────┬────────────────┘
                                     │
                    ┌────────────────▼────────────────┐
                    │   FASTAPI SERVER                │
                    │   (api_server.py)               │
                    │   http://localhost:8000         │
                    │                                 │
                    │   ├─ POST /translate            │
                    │   ├─ POST /translate-batch      │
                    │   ├─ GET /health                │
                    │   ├─ GET /languages             │
                    │   └─ GET /api/models            │
                    └────────────────┬────────────────┘
                                     │
                    ┌────────────────▼────────────────┐
                    │   TRANSLATION ENGINE            │
                    │   (mT5 Model - Mock)            │
                    │                                 │
                    │   Production: Use actual mT5    │
                    └─────────────────────────────────┘


# ============================================================================
#  COMPONENT INTERACTIONS
# ============================================================================

┌─────────────────────────────────────────────────────────────────────────┐
│ FLOW 1: USER SENDS TRANSLATION REQUEST                                 │
└─────────────────────────────────────────────────────────────────────────┘

1. User opens Dashboard (http://localhost:8501)
   └─ Streamlit renders UI with chatbot interface

2. User configures API
   ├─ Enters API Key: "test-key-12345"
   ├─ Verifies API URL: "http://localhost:8000"
   └─ Clicks "Test Connection" button

3. User selects languages
   ├─ Source: English
   └─ Target: Spanish

4. User types message
   └─ "Hello, how are you?"

5. User clicks "Send" button
   ├─ Message added to chat_history
   └─ HTTP POST sent to API

6. API Server receives request
   ├─ Validates API Key (Bearer token)
   ├─ Checks input format
   ├─ Performs translation
   └─ Sends response back

7. Dashboard receives translation
   ├─ Displays bot message
   ├─ Updates chat history
   └─ Shows timestamp

8. User sees result
   └─ "¡Hola, ¿cómo estás?"


┌─────────────────────────────────────────────────────────────────────────┐
│ FLOW 2: EXPORTING TRANSLATION HISTORY                                   │
└─────────────────────────────────────────────────────────────────────────┘

1. User navigates to "Translation History" tab
2. All translations from session displayed in table
3. User clicks "Export as JSON"
4. Browser downloads translations.json file
5. Format:
   {
     "type": "bot",
     "text": "translated text",
     "source_lang": "en",
     "target_lang": "es",
     "timestamp": "10:30:45"
   }


# ============================================================================
#  API AUTHENTICATION FLOW
# ============================================================================

REQUEST:
  POST /translate
  Headers: Authorization: Bearer test-key-12345
  Body: {
    "text": "Hello world",
    "source_lang": "en",
    "target_lang": "es",
    "mode": "simple"
  }

SERVER RECEIVES:
  1. Extracts Bearer token from header
  2. Looks up token in VALID_API_KEYS dictionary
  3. If found, returns associated user
  4. If not found, returns 401 Unauthorized

RESPONSE (Success):
  Status: 200 OK
  Body: {
    "translation": "Hola mundo",
    "source_lang": "en",
    "target_lang": "es",
    "confidence": 0.95,
    "mode": "simple"
  }

RESPONSE (Failed Auth):
  Status: 401 Unauthorized
  Body: {
    "error": "Invalid API key",
    "status_code": 401,
    "timestamp": "2025-12-21T10:30:45"
  }


# ============================================================================
#  DATA STORAGE & SESSION STATE
# ============================================================================

STREAMLIT SESSION STATE (In-Memory):
  session_state = {
    "api_key": "test-key-12345",
    "api_base_url": "http://localhost:8000",
    "api_connected": True,
    "chat_history": [
      {
        "type": "user",
        "text": "Hello world",
        "source_lang": "English",
        "target_lang": "Spanish",
        "timestamp": "10:30:45"
      },
      {
        "type": "bot",
        "text": "Hola mundo",
        "source_lang": "English",
        "target_lang": "Spanish",
        "timestamp": "10:30:46"
      }
    ]
  }

LOCAL FILE STORAGE (~/.mt5_config.json):
  {
    "api_key": "test-key-12345",
    "api_url": "http://localhost:8000",
    "saved_at": "2025-12-21T10:30:45.123456"
  }


# ============================================================================
#  TRANSLATION MODES
# ============================================================================

SIMPLE MODE:
  Input: "Hello world"
  └─ Direct translation using model
  Output: "Hola mundo"
  Time: ~100-500ms

PROMPT CHAIN MODE:
  Input: "I am preparing for an exam tomorrow"
  │
  ├─ Step 1: Language Detection
  │  └─ Output: "English"
  │
  ├─ Step 2: Meaning Extraction
  │  └─ Output: "Speaker is preparing for tomorrow's exam"
  │
  ├─ Step 3: Core Translation
  │  └─ Output: "Me estoy preparando para el examen de mañana"
  │
  └─ Step 4: Grammar Refinement
     └─ Output: "Me estoy preparando para un examen mañana"
  
  Time: ~500ms-2s


# ============================================================================
#  DEPLOYMENT OPTIONS
# ============================================================================

DEVELOPMENT:
  Terminal 1: python api_server.py
  Terminal 2: streamlit run app_enhanced.py
  Access: http://localhost:8501

PRODUCTION:
  1. Replace mock_translate() with real mT5 model
  2. Use environment variables for API keys
  3. Enable HTTPS/SSL
  4. Deploy on cloud platform
  5. Add database for history persistence
  6. Set up monitoring/logging


# ============================================================================
#  SUPPORTED LANGUAGES (20+)
# ============================================================================

English (en)           Spanish (es)           French (fr)
German (de)            Chinese (zh)           Japanese (ja)
Russian (ru)           Portuguese (pt)        Italian (it)
Arabic (ar)            Hindi (hi)             Bengali (bn)
Telugu (te)            Kannada (kn)           Tamil (ta)
Turkish (tr)           Vietnamese (vi)        Thai (th)
Korean (ko)            Polish (pl)


# ============================================================================
#  ERROR HANDLING
# ============================================================================

Invalid API Key:
  ├─ Streamlit: Shows red warning box
  ├─ API: Returns 401 Unauthorized
  └─ Solution: Correct API key in sidebar

Port Already in Use:
  ├─ Error: "Address already in use"
  ├─ Cause: Previous process still running
  └─ Solution: Kill process or use different port

Network Error:
  ├─ Streamlit: Shows "Connection Failed"
  ├─ Cause: API server not running
  └─ Solution: Start API server (python api_server.py)

Invalid Input:
  ├─ Error: "Text cannot be empty"
  ├─ Cause: User sent empty message
  └─ Solution: Type something and try again


# ============================================================================
#  SECURITY CONSIDERATIONS
# ============================================================================

API KEYS:
  ✓ Masked input in Streamlit UI
  ✓ Bearer token in API requests
  ✓ Stored in ~/.mt5_config.json (not committed)
  ✓ Demo key: test-key-12345

DATA PRIVACY:
  ✓ Session state cleared on browser close
  ✓ Translations not stored server-side
  ✓ Export allows user control

COMMUNICATION:
  ✓ CORS enabled for local testing
  ✓ Production: Use HTTPS only
  ✓ Production: Restrict CORS to known domains

DEPLOYMENT:
  ✓ Never hardcode API keys
  ✓ Use environment variables
  ✓ Rotate keys regularly
  ✓ Monitor usage and logs


# ============================================================================
#  PERFORMANCE CHARACTERISTICS
# ============================================================================

DASHBOARD:
  Startup Time: ~5-10 seconds
  Response Time: ~100-500ms per translation
  Memory: ~150-200MB (Python + Streamlit)

API SERVER:
  Startup Time: ~2-3 seconds
  Request Handling: ~50-100ms
  Batch Processing: ~20-30ms per text

DATABASE (Future):
  Translation Latency: +5-10ms
  History Queries: ~50-200ms

SCALING:
  Current: Single instance (localhost)
  Horizontal: Multiple API instances with load balancer
  Vertical: More CPU/RAM for mT5 model


# ============================================================================
#  FUTURE ENHANCEMENTS
# ============================================================================

SHORT TERM (v1.1):
  □ Replace mock translation with real mT5
  □ Add database for persistent history
  □ User authentication system
  □ Rate limiting
  □ Caching for common translations

MEDIUM TERM (v1.2):
  □ Multi-user support
  □ Advanced analytics
  □ Custom model fine-tuning
  □ Translation quality metrics
  □ Mobile app

LONG TERM (v2.0):
  □ Multi-model support
  □ Real-time collaboration
  □ Advanced NLP features
  □ Enterprise integrations
  □ On-premises deployment


# ============================================================================
#  DEBUGGING GUIDE
# ============================================================================

CHECK STREAMLIT LOGS:
  Look for errors in Terminal 2

CHECK API LOGS:
  Look for errors in Terminal 1

TEST API DIRECTLY:
  curl -X POST http://localhost:8000/translate \
    -H "Authorization: Bearer test-key-12345" \
    -H "Content-Type: application/json" \
    -d '{"text":"hello","source_lang":"en","target_lang":"es"}'

CHECK API DOCS:
  http://localhost:8000/docs

VIEW DEBUG INFO:
  Open dashboard → Advanced Settings tab

CHECK SESSION STATE:
  Debug tab shows all session variables

═══════════════════════════════════════════════════════════════════════════════
Version: 1.0.0 | Last Updated: 2025-12-21
═══════════════════════════════════════════════════════════════════════════════
