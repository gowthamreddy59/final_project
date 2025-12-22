# Quick Start - mT5 Chatbot & API

## 🎯 What You're About to Launch

✅ **Streamlit Dashboard** - Chatbot interface for translations
✅ **FastAPI Server** - Backend translation API with auth
✅ **API Documentation** - Interactive Swagger docs
✅ **Language Support** - 20+ languages

---

## 🚀 STEP-BY-STEP LAUNCH

### Windows Users

#### Option 1: Automatic (Recommended)
```powershell
# Open PowerShell and run:
python run_full_system.py
```

OR

```cmd
# Double-click:
run_full_system.bat
```

#### Option 2: Manual

**Terminal 1 - API Server:**
```powershell
python api_server.py
```

**Terminal 2 - Dashboard:**
```powershell
streamlit run app_enhanced.py
```

---

### macOS / Linux Users

#### Complete System
```bash
python run_full_system.py
```

#### Manual

**Terminal 1:**
```bash
python api_server.py
```

**Terminal 2:**
```bash
streamlit run app_enhanced.py
```

---

## ✅ Verify It's Running

### Dashboard
Open: **http://localhost:8501**

You should see:
- Chatbot interface
- API configuration sidebar
- Language selection

### API Server
Open: **http://localhost:8000/docs**

You should see:
- Swagger API documentation
- All endpoints listed
- Try-it-out feature

---

## 🔑 First Time Setup

1. **Open Dashboard** (http://localhost:8501)

2. **Configure API Key** (Sidebar):
   - API Key: `test-key-12345`
   - API URL: `http://localhost:8000`
   - Click "Test Connection" ✓

3. **Start Translating**:
   - Select source & target languages
   - Type a message
   - Click "Send"

---

## 💬 Try These Examples

### English → Spanish
**Input:** "Hello, how are you?"
**Output:** [Translated text]

### English → French
**Input:** "Good morning"
**Output:** [Translated text]

### English → Chinese
**Input:** "Thank you very much"
**Output:** [Translated text]

---

## 🔌 API Testing

### Using Python
```python
import requests

# Test API
response = requests.post(
    "http://localhost:8000/translate",
    json={
        "text": "Hello world",
        "source_lang": "en",
        "target_lang": "es",
        "mode": "simple"
    },
    headers={"Authorization": "Bearer test-key-12345"}
)

print(response.json())
```

### Using cURL
```bash
curl -X POST "http://localhost:8000/translate" \
  -H "Authorization: Bearer test-key-12345" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Hello world",
    "source_lang": "en",
    "target_lang": "es",
    "mode": "simple"
  }'
```

---

## 🐛 Troubleshooting

### "Port already in use"
Kill the process using the port:
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# macOS/Linux
lsof -ti:8000 | xargs kill
```

### "API Connection Failed"
1. Check API Key in sidebar
2. Verify API URL is correct
3. Click "Test Connection"
4. Check if `python api_server.py` is running

### "Module not found"
```bash
pip install -r requirements_enhanced.txt
```

### "Permission denied on Windows"
Run PowerShell as Administrator

---

## 📊 Features Overview

### Dashboard Tabs

1. **Chatbot Translator**
   - Real-time translation
   - Language selection
   - Message history

2. **Translation History**
   - View all past translations
   - Export as JSON/CSV
   - Statistics

3. **API Documentation**
   - Endpoint reference
   - Language codes
   - Error codes
   - Request/response examples

4. **Advanced Settings**
   - Debug information
   - API configuration
   - Session details
   - Recent logs

---

## 🔒 Security Notes

1. **API Keys**
   - Test key: `test-key-12345` (demo only)
   - Create production keys
   - Never hardcode in code

2. **Storage**
   - Keys stored in: `~/.mt5_config.json`
   - Keep this file secure
   - Don't commit to Git

3. **Communication**
   - Use HTTPS in production
   - Validate all inputs
   - Check API responses

---

## 📈 Next Steps

1. ✅ Get API working (test key)
2. ✅ Create production API key
3. ✅ Integrate with your app
4. ✅ Set up monitoring
5. ✅ Scale infrastructure

---

## 🎓 Understanding the Flow

```
User Input (Dashboard)
    ↓
Streamlit App (app_enhanced.py)
    ↓
API Request (POST /translate)
    ↓
FastAPI Server (api_server.py)
    ↓
Authentication (Bearer token)
    ↓
Mock Translation (Replace with real mT5 model)
    ↓
Response to Dashboard
    ↓
Chat History Update
    ↓
User Sees Translation
```

---

## 📚 Files Included

| File | Purpose |
|------|---------|
| `app_enhanced.py` | Streamlit chatbot interface |
| `api_server.py` | FastAPI backend server |
| `run_full_system.py` | Python launcher (all systems) |
| `run_full_system.bat` | Windows batch launcher |
| `requirements_enhanced.txt` | Python dependencies |
| `CHATBOT_API_GUIDE.md` | Detailed documentation |
| `QUICKSTART.md` | This file |

---

## 💡 Tips

- **Prompt Chain Mode**: Better for complex sentences
- **Batch API**: Use for processing many texts at once
- **Export History**: Download translations for records
- **Debug Tab**: Check system status anytime

---

## 🆘 Need Help?

1. Check Debug tab in Advanced Settings
2. Review API docs at `/docs`
3. Test connection in sidebar
4. Check terminal for error messages

---

**Ready to go?** Run: `python run_full_system.py` 🚀

**Questions?** See: `CHATBOT_API_GUIDE.md`
