import streamlit as st
import os
import sys
import json
from pathlib import Path
from datetime import datetime
import requests

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

st.set_page_config(
    page_title="mT5 Translator - Chatbot & API",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom styling
st.markdown("""
    <style>
    .main-header {
        font-size: 3em;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 0.5em;
    }
    .chat-message {
        padding: 12px;
        margin: 8px 0;
        border-radius: 8px;
    }
    .user-message {
        background-color: #e3f2fd;
        border-left: 4px solid #2196F3;
        margin-left: 20px;
    }
    .bot-message {
        background-color: #f5f5f5;
        border-left: 4px solid #4caf50;
        margin-right: 20px;
    }
    .api-status-active {
        background-color: #d4edda;
        border-left: 4px solid #28a745;
        padding: 12px;
        margin: 10px 0;
        border-radius: 4px;
    }
    .api-status-inactive {
        background-color: #f8d7da;
        border-left: 4px solid #dc3545;
        padding: 12px;
        margin: 10px 0;
        border-radius: 4px;
    }
    .info-box {
        background-color: #e7f3ff;
        border-left: 4px solid #2196F3;
        padding: 12px;
        margin: 10px 0;
        border-radius: 4px;
    }
    .warning-box {
        background-color: #fff3cd;
        border-left: 4px solid #ffc107;
        padding: 12px;
        margin: 10px 0;
        border-radius: 4px;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state
if "api_key" not in st.session_state:
    st.session_state.api_key = ""
if "api_base_url" not in st.session_state:
    st.session_state.api_base_url = "http://localhost:8000"
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "show_api_settings" not in st.session_state:
    st.session_state.show_api_settings = False
if "api_connected" not in st.session_state:
    st.session_state.api_connected = False

# Supported languages for mT5
SUPPORTED_LANGUAGES = {
    "English": "en",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Chinese (Simplified)": "zh",
    "Japanese": "ja",
    "Russian": "ru",
    "Portuguese": "pt",
    "Italian": "it",
    "Arabic": "ar",
    "Hindi": "hi",
    "Bengali": "bn",
    "Telugu": "te",
    "Kannada": "kn",
    "Tamil": "ta",
    "Turkish": "tr",
    "Vietnamese": "vi",
    "Thai": "th",
    "Korean": "ko",
    "Polish": "pl",
}

# Sidebar - API Configuration
with st.sidebar:
    st.header("⚙️ API Configuration")
    
    # API Key input
    api_key = st.text_input(
        "API Key",
        value=st.session_state.api_key,
        type="password",
        help="Enter your API key for mT5 translation service"
    )
    
    if api_key:
        st.session_state.api_key = api_key
    
    # API Base URL
    api_url = st.text_input(
        "API Base URL",
        value=st.session_state.api_base_url,
        help="Enter the base URL of your mT5 API server"
    )
    
    if api_url:
        st.session_state.api_base_url = api_url
    
    # Test connection button
    if st.button("🔌 Test Connection", use_container_width=True):
        if st.session_state.api_key and st.session_state.api_base_url:
            try:
                response = requests.get(
                    f"{st.session_state.api_base_url}/health",
                    headers={"Authorization": f"Bearer {st.session_state.api_key}"},
                    timeout=5
                )
                if response.status_code == 200:
                    st.session_state.api_connected = True
                    st.success("✅ API Connection Successful!")
                else:
                    st.session_state.api_connected = False
                    st.error(f"❌ Connection Failed: {response.status_code}")
            except Exception as e:
                st.session_state.api_connected = False
                st.error(f"❌ Error: {str(e)}")
        else:
            st.error("Please enter API key and URL")
    
    # Connection status
    if st.session_state.api_connected:
        st.markdown("""<div class="api-status-active">
            <strong>✅ API Connected</strong>
            </div>""", unsafe_allow_html=True)
    elif st.session_state.api_key:
        st.markdown("""<div class="api-status-inactive">
            <strong>❌ API Not Connected</strong><br>
            Click "Test Connection" to verify
            </div>""", unsafe_allow_html=True)
    
    st.divider()
    
    # API Key Management
    st.subheader("🔑 Key Management")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("💾 Save Key", use_container_width=True):
            if st.session_state.api_key:
                # Save to local config file
                config = {
                    "api_key": st.session_state.api_key,
                    "api_url": st.session_state.api_base_url,
                    "saved_at": datetime.now().isoformat()
                }
                config_path = Path.home() / ".mt5_config.json"
                with open(config_path, 'w') as f:
                    json.dump(config, f)
                st.success("✅ Key saved locally")
    
    with col2:
        if st.button("🗑️ Clear Key", use_container_width=True):
            st.session_state.api_key = ""
            st.session_state.api_connected = False
            st.success("✅ Key cleared")
    
    st.divider()
    
    # Translation Settings
    st.subheader("🌐 Translation Settings")
    
    translation_mode = st.radio(
        "Translation Mode",
        ["Single Translation", "Prompt Chain (Advanced)"],
        help="Single: Direct translation\nPrompt Chain: Multi-step for better accuracy"
    )
    
    st.divider()
    
    # Clear chat history
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.chat_history = []
        st.success("✅ Chat history cleared")

# Main content
st.markdown('<h1 class="main-header">🌍 mT5 Multilingual Translator</h1>', unsafe_allow_html=True)

# Create tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "💬 Chatbot Translator",
    "📊 Translation History",
    "🔗 API Documentation",
    "⚙️ Advanced Settings"
])

# TAB 1: Chatbot Interface
with tab1:
    st.subheader("🤖 Chat with Translation Bot")
    
    if not st.session_state.api_connected and st.session_state.api_key:
        st.warning("⚠️ API not connected. Configure and test connection in sidebar.")
    elif not st.session_state.api_key:
        st.info("ℹ️ Please enter an API key and test connection to start translating.")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        source_lang = st.selectbox(
            "Source Language",
            options=list(SUPPORTED_LANGUAGES.keys()),
            key="source_lang"
        )
    
    with col2:
        target_lang = st.selectbox(
            "Target Language",
            options=list(SUPPORTED_LANGUAGES.keys()),
            index=1,
            key="target_lang"
        )
    
    st.divider()
    
    # Chat display
    st.subheader("Chat History")
    chat_container = st.container(height=400, border=True)
    
    with chat_container:
        if st.session_state.chat_history:
            for idx, message in enumerate(st.session_state.chat_history):
                if message["type"] == "user":
                    st.markdown(f"""
                    <div class="chat-message user-message">
                    <strong>📝 You ({message['source_lang']}):</strong><br>
                    {message['text']}
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="chat-message bot-message">
                    <strong>🤖 Translator ({message['target_lang']}):</strong><br>
                    {message['text']}<br>
                    <small>⏱️ {message.get('timestamp', 'N/A')}</small>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("💡 Start a conversation by typing a message below...")
    
    st.divider()
    
    # Input area
    col1, col2 = st.columns([5, 1])
    
    with col1:
        user_input = st.text_area(
            "Type your message here",
            height=80,
            placeholder="Enter text to translate...",
            key="user_input"
        )
    
    with col2:
        st.write("")
        st.write("")
        send_button = st.button("📤 Send", use_container_width=True)
    
    if send_button and user_input.strip():
        # Add user message to history
        st.session_state.chat_history.append({
            "type": "user",
            "text": user_input,
            "source_lang": source_lang,
            "target_lang": target_lang,
            "timestamp": datetime.now().strftime("%H:%M:%S")
        })
        
        # Simulate translation (replace with actual API call)
        if st.session_state.api_connected:
            try:
                # Make API call
                payload = {
                    "text": user_input,
                    "source_lang": SUPPORTED_LANGUAGES[source_lang],
                    "target_lang": SUPPORTED_LANGUAGES[target_lang],
                    "mode": "simple"
                }
                
                response = requests.post(
                    f"{st.session_state.api_base_url}/translate",
                    json=payload,
                    headers={"Authorization": f"Bearer {st.session_state.api_key}"},
                    timeout=30
                )
                
                if response.status_code == 200:
                    translation = response.json().get("translation", "Translation failed")
                else:
                    translation = f"Error: {response.status_code}"
                
            except Exception as e:
                translation = f"Connection error: {str(e)}"
        else:
            # Demo mode
            translation = f"[DEMO] Translation: {user_input} → {target_lang}"
        
        # Add bot response to history
        st.session_state.chat_history.append({
            "type": "bot",
            "text": translation,
            "source_lang": source_lang,
            "target_lang": target_lang,
            "timestamp": datetime.now().strftime("%H:%M:%S")
        })
        
        st.rerun()

# TAB 2: Translation History
with tab2:
    st.subheader("📋 Translation History")
    
    if st.session_state.chat_history:
        # Filter translations only
        translations = [msg for msg in st.session_state.chat_history if msg["type"] == "bot"]
        
        if translations:
            df_data = []
            for t in translations:
                df_data.append({
                    "Time": t.get("timestamp", "N/A"),
                    "From": t.get("source_lang", "N/A"),
                    "To": t.get("target_lang", "N/A"),
                    "Translation": t["text"][:50] + "..." if len(t["text"]) > 50 else t["text"]
                })
            
            df = pd.DataFrame(df_data)
            st.dataframe(df, use_container_width=True)
            
            # Export options
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("📥 Export as JSON"):
                    json_str = json.dumps(st.session_state.chat_history, indent=2)
                    st.download_button(
                        "Download JSON",
                        json_str,
                        "translations.json",
                        "application/json"
                    )
            
            with col2:
                if st.button("📥 Export as CSV"):
                    csv_str = df.to_csv(index=False)
                    st.download_button(
                        "Download CSV",
                        csv_str,
                        "translations.csv",
                        "text/csv"
                    )
        else:
            st.info("No translations yet")
    else:
        st.info("💡 Start a conversation in the Chatbot tab to see translation history")

# TAB 3: API Documentation
with tab3:
    st.subheader("📖 API Documentation")
    
    st.markdown("""
    ### Endpoints
    
    #### 1. Health Check
    ```
    GET /health
    Headers: Authorization: Bearer YOUR_API_KEY
    Response: {"status": "ok"}
    ```
    
    #### 2. Translate Text
    ```
    POST /translate
    Headers: Authorization: Bearer YOUR_API_KEY
    
    Request Body:
    {
        "text": "Hello world",
        "source_lang": "en",
        "target_lang": "es",
        "mode": "simple" | "chain"
    }
    
    Response:
    {
        "translation": "Hola mundo",
        "source_lang": "en",
        "target_lang": "es",
        "confidence": 0.95
    }
    ```
    
    #### 3. Batch Translation
    ```
    POST /translate-batch
    Headers: Authorization: Bearer YOUR_API_KEY
    
    Request Body:
    {
        "texts": ["Hello", "World"],
        "source_lang": "en",
        "target_lang": "es"
    }
    ```
    
    ### Supported Languages
    """)
    
    # Create language table
    lang_table = []
    for name, code in SUPPORTED_LANGUAGES.items():
        lang_table.append({"Language": name, "Code": code})
    
    df_langs = pd.DataFrame(lang_table)
    st.dataframe(df_langs, use_container_width=True, hide_index=True)
    
    st.markdown("""
    ### Error Codes
    - `400`: Bad request
    - `401`: Unauthorized (invalid API key)
    - `403`: Forbidden
    - `500`: Server error
    - `503`: Service unavailable
    """)

# TAB 4: Advanced Settings
with tab4:
    st.subheader("⚙️ Advanced Configuration")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Translation Mode")
        st.info("""
        **Simple Mode**: Direct translation
        - Fast
        - Good for simple sentences
        
        **Prompt Chain Mode**: Multi-step translation
        - Step 1: Language detection
        - Step 2: Meaning extraction
        - Step 3: Translation
        - Step 4: Grammar refinement
        - More accurate for complex text
        """)
    
    with col2:
        st.subheader("API Configuration")
        st.warning("""
        **Security Tips**:
        - Never share your API key
        - Use environment variables
        - Rotate keys regularly
        - Monitor usage
        
        **Setup Local Server**:
        ```bash
        pip install fastapi uvicorn
        python api_server.py
        ```
        """)
    
    st.divider()
    
    st.subheader("🔍 Debug Information")
    
    debug_info = {
        "API Connected": "✅ Yes" if st.session_state.api_connected else "❌ No",
        "API Key Set": "✅ Yes" if st.session_state.api_key else "❌ No",
        "API URL": st.session_state.api_base_url,
        "Chat Messages": len(st.session_state.chat_history),
        "Session ID": st.session_state.get("session_id", "N/A")
    }
    
    df_debug = pd.DataFrame(list(debug_info.items()), columns=["Property", "Value"])
    st.dataframe(df_debug, use_container_width=True, hide_index=True)
    
    st.divider()
    
    st.subheader("📝 Logs")
    
    if st.session_state.chat_history:
        st.code(json.dumps(st.session_state.chat_history[-5:], indent=2))
    else:
        st.info("No logs yet")

# Footer
st.divider()
st.markdown("""
<div style="text-align: center; color: #666; padding: 20px;">
    <small>
        🌍 Multilingual T5 Translator | Built with Streamlit & mT5<br>
        © 2025 | API-Powered Translation Service
    </small>
</div>
""", unsafe_allow_html=True)
