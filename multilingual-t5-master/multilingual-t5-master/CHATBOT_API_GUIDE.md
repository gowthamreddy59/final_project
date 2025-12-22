# mT5 Translator with Chatbot & API - Complete Guide

## 🎯 Overview

This system provides a complete multilingual translation solution with:
- **Chatbot Interface** - Conversational translation via Streamlit
- **FastAPI Backend** - RESTful API server with authentication
- **API Key Management** - Secure key storage and management
- **Translation History** - Track and export translations
- **Multiple Modes** - Simple or prompt-chain translation

## 📋 Features

### 1. Chatbot Translator
- Real-time conversation interface
- Support for 20+ languages
- Message history with timestamps
- Language pair selection

### 2. API Key Management
- Secure API key input (masked input)
- Local key storage
- Connection testing
- Key validation

### 3. FastAPI Backend
- RESTful endpoints for translation
- Bearer token authentication
- Health check endpoint
- Batch translation support
- CORS enabled

### 4. Translation Modes
- **Simple Mode**: Direct translation
- **Prompt Chain Mode**: Multi-step for better accuracy
  - Step 1: Language detection
  - Step 2: Meaning extraction
  - Step 3: Translation
  - Step 4: Grammar refinement

## 🚀 Quick Start

### Option 1: Complete System (Recommended)
```bash
# Install dependencies
pip install -r requirements_enhanced.txt

# Start API + Dashboard
python run_full_system.py
```

Then:
- API: http://localhost:8000 (Docs at /docs)
- Dashboard: http://localhost:8501

### Option 2: Dashboard Only
```bash
pip install -r requirements_enhanced.txt
streamlit run app_enhanced.py
```

### Option 3: API Server Only
```bash
pip install -r requirements_enhanced.txt
python api_server.py
```

## 🔑 API Key Configuration

### Testing
Use the demo key for testing:
```
API Key: test-key-12345
API URL: http://localhost:8000
```

### Production
1. Generate secure API key
2. Set environment variable:
   ```bash
   export API_KEY=your-production-key
   ```
3. Configure in dashboard

## 📡 API Endpoints

### Health Check
```
GET /health
Authorization: Bearer YOUR_API_KEY

Response:
{
  "status": "ok",
  "timestamp": "2025-12-21T10:30:45.123456",
  "version": "1.0.0"
}
```

### Translate Single Text
```
POST /translate
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json

Request:
{
  "text": "Hello world",
  "source_lang": "en",
  "target_lang": "es",
  "mode": "simple"
}

Response:
{
  "translation": "Hola mundo",
  "source_lang": "en",
  "target_lang": "es",
  "confidence": 0.95,
  "mode": "simple"
}
```

### Batch Translation
```
POST /translate-batch
Authorization: Bearer YOUR_API_KEY

Request:
{
  "texts": ["Hello", "Goodbye"],
  "source_lang": "en",
  "target_lang": "es"
}

Response:
{
  "count": 2,
  "translations": [
    {"original": "Hello", "translation": "Hola"},
    {"original": "Goodbye", "translation": "Adiós"}
  ]
}
```

### Supported Languages
```
GET /languages
Authorization: Bearer YOUR_API_KEY
```

## 🛠️ Configuration

### Sidebar Settings
1. **API Key** - Masked input field
2. **API URL** - Base URL for API server
3. **Connection Test** - Verify API connectivity
4. **Translation Mode** - Simple or Prompt Chain
5. **Key Management** - Save/Clear keys

### Advanced Settings Tab
- Debug information
- API configuration tips
- Recent logs
- Session details

## 💾 Data Storage

### Local Configuration
API keys are stored in:
```
~/.mt5_config.json
```

Format:
```json
{
  "api_key": "your-key",
  "api_url": "http://localhost:8000",
  "saved_at": "2025-12-21T10:30:45.123456"
}
```

### Translation History
Stored in session state:
- Export as JSON
- Export as CSV
- Clear history option

## 🔐 Security Best Practices

1. **API Key Management**
   - Use strong, random keys
   - Rotate regularly
   - Never commit to version control
   - Use environment variables in production

2. **Request Validation**
   - All endpoints require Bearer token
   - Input sanitization on backend
   - Error messages don't leak sensitive info

3. **CORS Configuration**
   - Configure allowed origins
   - Restrict in production
   - Currently set to "*" for development

## 🐛 Troubleshooting

### API Connection Failed
```
❌ "Connection Failed: 401"
→ Check API key in sidebar
→ Verify API URL is correct
→ Ensure API server is running
```

### Port Already in Use
```
Error: Port 8000 or 8501 already in use
→ Kill existing process: lsof -ti:8000 | xargs kill
→ Or use different port
```

### Missing Dependencies
```
ModuleNotFoundError
→ pip install -r requirements_enhanced.txt
→ Verify Python 3.8+
```

## 📊 Supported Languages

| Language | Code |
|----------|------|
| English | en |
| Spanish | es |
| French | fr |
| German | de |
| Chinese (Simplified) | zh |
| Japanese | ja |
| Russian | ru |
| Portuguese | pt |
| Italian | it |
| Arabic | ar |
| Hindi | hi |
| Bengali | bn |
| Telugu | te |
| Kannada | kn |
| Tamil | ta |
| Turkish | tr |
| Vietnamese | vi |
| Thai | th |
| Korean | ko |
| Polish | pl |

## 📈 Performance

- **Simple Mode**: ~100-500ms per translation
- **Prompt Chain Mode**: ~500ms-2s per translation
- **Batch Processing**: ~50-100ms per text

## 🔄 Workflow Example

### Scenario: Translate English to Spanish

1. **User Input**
   - Selects: English → Spanish
   - Types: "Hello world"

2. **API Request**
   - Sends POST to /translate
   - Includes: text, languages, mode, API key

3. **API Processing** (Simple Mode)
   - Validates API key ✓
   - Checks input ✓
   - Returns translation ✓

4. **Chat Display**
   - Shows user message
   - Shows bot response
   - Records timestamp

5. **History**
   - Message added to chat_history
   - Exportable as JSON/CSV

## 🚀 Advanced Usage

### Prompt Chain Translation
Enable in sidebar for multi-step translation:
1. Language detection (what language is this?)
2. Meaning extraction (what does it mean?)
3. Translation (translate the meaning)
4. Grammar refinement (make it natural)

### Batch Processing
Use API for bulk translations:
```python
import requests

payload = {
    "texts": ["Hello", "Goodbye", "Thank you"],
    "source_lang": "en",
    "target_lang": "es"
}

response = requests.post(
    "http://localhost:8000/translate-batch",
    json=payload,
    headers={"Authorization": "Bearer test-key-12345"}
)
```

## 📝 Integration Example

### Python Client
```python
import requests

class MT5Translator:
    def __init__(self, api_key, base_url="http://localhost:8000"):
        self.api_key = api_key
        self.base_url = base_url
    
    def translate(self, text, source, target):
        response = requests.post(
            f"{self.base_url}/translate",
            json={
                "text": text,
                "source_lang": source,
                "target_lang": target,
                "mode": "simple"
            },
            headers={"Authorization": f"Bearer {self.api_key}"}
        )
        return response.json()

# Usage
translator = MT5Translator("test-key-12345")
result = translator.translate("Hello", "en", "es")
print(result["translation"])
```

## 📚 Additional Resources

- Streamlit docs: https://docs.streamlit.io
- FastAPI docs: https://fastapi.tiangolo.com
- mT5 model: https://github.com/google-research/multilingual-t5
- API Standards: https://www.rfc-editor.org/rfc/rfc7235

## 🤝 Support

For issues or questions:
1. Check the Advanced Settings tab for debug info
2. Review API documentation in app
3. Test API connection in sidebar
4. Check logs in Terminal

## 📄 Files

- `app_enhanced.py` - Streamlit chatbot interface
- `api_server.py` - FastAPI backend server
- `run_full_system.py` - Complete system launcher
- `requirements_enhanced.txt` - Dependencies
- `CHATBOT_API_GUIDE.md` - This file

---

**Version**: 1.0.0 | **Last Updated**: 2025-12-21
