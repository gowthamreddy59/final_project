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
    page_title="mT5 Translator with Groq AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom styling - Black & Blue Theme
st.markdown("""
    <style>
    body {
        background-color: #000000;
        color: #ffffff;
    }
    
    .main-header {
        font-size: 3em;
        color: #00bfff;
        text-align: center;
        margin-bottom: 0.5em;
        font-weight: bold;
        text-shadow: 0 0 10px rgba(0, 191, 255, 0.5);
    }
    
    .groq-badge {
        display: inline-block;
        background: linear-gradient(135deg, #0066ff 0%, #00ccff 100%);
        color: #ffffff;
        padding: 8px 16px;
        border-radius: 20px;
        font-weight: bold;
        margin: 10px 0;
        border: 2px solid #0066ff;
    }
    
    .chat-message {
        padding: 12px;
        margin: 8px 0;
        border-radius: 8px;
        color: #ffffff;
    }
    
    .user-message {
        background-color: #001a4d;
        border-left: 4px solid #00bfff;
        margin-left: 20px;
        color: #e0e0e0;
    }
    
    .bot-message {
        background-color: #0d0d0d;
        border-left: 4px solid #0066ff;
        margin-right: 20px;
        color: #ffffff;
    }
    
    .groq-connected {
        background-color: #001a00;
        border-left: 4px solid #00ff00;
        padding: 12px;
        margin: 10px 0;
        border-radius: 4px;
        color: #00ff00;
    }
    
    .groq-disconnected {
        background-color: #330000;
        border-left: 4px solid #ff0000;
        padding: 12px;
        margin: 10px 0;
        border-radius: 4px;
        color: #ff6b6b;
    }
    
    .info-box {
        background-color: #001a4d;
        border-left: 4px solid #0066ff;
        padding: 12px;
        margin: 10px 0;
        border-radius: 4px;
        color: #00bfff;
    }
    
    /* Streamlit overrides */
    .stApp {
        background-color: #000000;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        background-color: #0d0d0d;
    }
    
    .stTabs [data-baseweb="tab"] {
        color: #00bfff;
    }
    
    .stButton>button {
        background-color: #0066ff;
        color: #ffffff;
        border: 2px solid #00bfff;
    }
    
    .stButton>button:hover {
        background-color: #0080ff;
        border-color: #00ffff;
    }
    
    .stTextInput>div>div>input {
        background-color: #1a1a1a;
        color: #ffffff;
        border: 2px solid #0066ff;
    }
    
    .stTextArea>div>div>textarea {
        background-color: #1a1a1a;
        color: #ffffff;
        border: 2px solid #0066ff;
    }
    
    .stSelectbox>div>div>select {
        background-color: #1a1a1a;
        color: #ffffff;
    }
    
    .stRadio>div>div>label {
        color: #00bfff;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state
if "groq_api_key" not in st.session_state:
    st.session_state.groq_api_key = ""
if "mcp_api_key" not in st.session_state:
    st.session_state.mcp_api_key = "test-key-12345"
if "api_base_url" not in st.session_state:
    st.session_state.api_base_url = "http://localhost:8002"
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "groq_connected" not in st.session_state:
    st.session_state.groq_connected = False

# Supported languages
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

# Sidebar - Configuration
with st.sidebar:
    st.header("⚙️ AI Configuration")
    
    st.markdown('<div class="groq-badge">🚀 Powered by Groq AI</div>', unsafe_allow_html=True)
    
    st.subheader("🔑 Groq API Key")
    
    groq_key = st.text_input(
        "Groq API Key",
        value=st.session_state.groq_api_key,
        type="password",
        help="Get your free API key from https://console.groq.com"
    )
    
    if groq_key:
        st.session_state.groq_api_key = groq_key
    
    # Show Groq info
    if st.button("📖 Get Groq API Key", use_container_width=True):
        st.info("""
        **How to get a Groq API Key:**
        1. Go to https://console.groq.com
        2. Sign up (free account)
        3. Create new API key
        4. Paste it above
        
        **Groq Benefits:**
        ✅ Fastest inference speed
        ✅ Free tier available
        ✅ Multiple AI models
        ✅ Great for translations
        """)
    
    st.divider()
    
    st.subheader("🔌 Server Configuration")
    
    mcp_key = st.text_input(
        "MCP API Key",
        value=st.session_state.mcp_api_key,
        type="password",
        help="Your app's API key (default: test-key-12345)"
    )
    
    if mcp_key:
        st.session_state.mcp_api_key = mcp_key
    
    api_url = st.text_input(
        "API Server URL",
        value=st.session_state.api_base_url,
        help="Base URL of API server"
    )
    
    if api_url:
        st.session_state.api_base_url = api_url
    
    # Test connection
    if st.button("🔌 Test Connection", use_container_width=True):
        if st.session_state.groq_api_key and st.session_state.mcp_api_key:
            try:
                response = requests.get(
                    f"{st.session_state.api_base_url}/health",
                    headers={"Authorization": f"Bearer {st.session_state.mcp_api_key}"},
                    timeout=5
                )
                if response.status_code == 200:
                    st.session_state.groq_connected = True
                    st.success("✅ Connection Successful!")
                else:
                    st.session_state.groq_connected = False
                    st.error(f"❌ Connection Failed: {response.status_code}")
            except Exception as e:
                st.session_state.groq_connected = False
                st.error(f"❌ Error: {str(e)}")
        else:
            st.error("Please enter all required keys")
    
    # Status
    if st.session_state.groq_connected:
        st.markdown("""<div class="groq-connected">
            <strong>✅ Groq AI Ready</strong>
            </div>""", unsafe_allow_html=True)
    elif st.session_state.groq_api_key:
        st.markdown("""<div class="groq-disconnected">
            <strong>⚠️ Not Connected</strong><br>
            Click "Test Connection" to verify
            </div>""", unsafe_allow_html=True)
    
    st.divider()
    
    st.subheader("⚙️ Translation Settings")
    
    translation_mode = st.radio(
        "Translation Mode",
        ["Simple & Fast", "Accurate (Chain)"],
        help="Simple: Quick translation\nChain: Multi-step for better accuracy"
    )
    
    st.divider()
    
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.chat_history = []
        st.success("✅ Chat history cleared")

# Main content
st.markdown('<h1 class="main-header">🤖 AI Translator with Groq</h1>', unsafe_allow_html=True)

# Create tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "💬 Translation Chat",
    "🎯 General AI Chat",
    "📊 History",
    "📖 API Docs",
    "⚙️ Settings"
])

# TAB 1: Translation Chat
with tab1:
    st.subheader("🌐 Multilingual Translation with Groq AI")
    
    if not st.session_state.groq_api_key:
        st.warning("⚠️ Please enter your Groq API key in the sidebar to start translating.")
    elif not st.session_state.groq_connected:
        st.info("ℹ️ Click 'Test Connection' in sidebar to verify setup.")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        source_lang = st.selectbox(
            "Source Language",
            options=list(SUPPORTED_LANGUAGES.keys()),
            key="source_lang_trans"
        )
    
    with col2:
        target_lang = st.selectbox(
            "Target Language",
            options=list(SUPPORTED_LANGUAGES.keys()),
            index=1,
            key="target_lang_trans"
        )
    
    st.divider()
    
    # Chat display
    st.subheader("Chat History")
    chat_container = st.container(height=400, border=True)
    
    with chat_container:
        if st.session_state.chat_history:
            for message in st.session_state.chat_history:
                if message["type"] == "user":
                    st.markdown(f"""
                    <div class="chat-message user-message">
                    <strong>📝 You ({message.get('source_lang', 'Unknown')}):</strong><br>
                    {message['text']}<br>
                    <small>⏱️ {message.get('timestamp', 'N/A')}</small>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="chat-message bot-message">
                    <strong>🤖 Groq AI ({message.get('target_lang', 'Unknown')}):</strong><br>
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
            key="trans_input"
        )
    
    with col2:
        st.write("")
        st.write("")
        send_button = st.button("📤 Send", use_container_width=True, key="trans_send")
    
    if send_button and user_input.strip():
        st.session_state.chat_history.append({
            "type": "user",
            "text": user_input,
            "source_lang": source_lang,
            "target_lang": target_lang,
            "timestamp": datetime.now().strftime("%H:%M:%S")
        })
        
        if st.session_state.groq_api_key and st.session_state.groq_connected:
            try:
                with st.spinner("🤖 Groq AI is translating..."):
                    payload = {
                        "text": user_input,
                        "source_lang": SUPPORTED_LANGUAGES[source_lang],
                        "target_lang": SUPPORTED_LANGUAGES[target_lang],
                        "mode": "chain" if translation_mode == "Accurate (Chain)" else "simple",
                        "groq_api_key": st.session_state.groq_api_key
                    }
                    
                    response = requests.post(
                        f"{st.session_state.api_base_url}/translate",
                        json=payload,
                        headers={"Authorization": f"Bearer {st.session_state.mcp_api_key}"},
                        timeout=30
                    )
                    
                    if response.status_code == 200:
                        translation = response.json().get("translation", "Translation failed")
                    else:
                        translation = f"Error: {response.status_code} - {response.text}"
                
            except Exception as e:
                translation = f"Error: {str(e)}"
        else:
            translation = "⚠️ Please configure Groq API key and test connection"
        
        st.session_state.chat_history.append({
            "type": "bot",
            "text": translation,
            "source_lang": source_lang,
            "target_lang": target_lang,
            "timestamp": datetime.now().strftime("%H:%M:%S")
        })
        
        st.rerun()

# TAB 2: General AI Chat
with tab2:
    st.subheader("💬 Chat with Groq AI")
    
    if not st.session_state.groq_api_key:
        st.warning("⚠️ Please enter your Groq API key in the sidebar.")
    
    # Initialize AI chat history
    if "ai_chat_history" not in st.session_state:
        st.session_state.ai_chat_history = []
    
    # Display chat
    st.subheader("Conversation")
    chat_container = st.container(height=400, border=True)
    
    with chat_container:
        if st.session_state.ai_chat_history:
            for msg in st.session_state.ai_chat_history:
                if msg["role"] == "user":
                    st.markdown(f"""
                    <div class="chat-message user-message">
                    <strong>👤 You:</strong><br>
                    {msg['content']}
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="chat-message bot-message">
                    <strong>🤖 Groq AI:</strong><br>
                    {msg['content']}
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("💡 Start chatting with Groq AI...")
    
    st.divider()
    
    # Chat input
    col1, col2 = st.columns([5, 1])
    
    with col1:
        ai_input = st.text_area(
            "Your message",
            height=80,
            placeholder="Ask Groq AI anything...",
            key="ai_input"
        )
    
    with col2:
        st.write("")
        st.write("")
        ai_send = st.button("📤 Send", use_container_width=True, key="ai_send")
    
    if ai_send and ai_input.strip():
        st.session_state.ai_chat_history.append({
            "role": "user",
            "content": ai_input
        })
        
        if st.session_state.groq_api_key:
            try:
                with st.spinner("🤖 Groq AI is thinking..."):
                    # Prepare messages for API
                    messages = []
                    for msg in st.session_state.ai_chat_history:
                        messages.append({
                            "role": msg["role"],
                            "content": msg["content"]
                        })
                    
                    payload = {
                        "message": ai_input,
                        "conversation_history": messages[:-1],  # Exclude current message
                        "groq_api_key": st.session_state.groq_api_key
                    }
                    
                    response = requests.post(
                        f"{st.session_state.api_base_url}/chat",
                        json=payload,
                        headers={"Authorization": f"Bearer {st.session_state.mcp_api_key}"},
                        timeout=30
                    )
                    
                    if response.status_code == 200:
                        ai_response = response.json().get("response", "No response")
                    else:
                        ai_response = f"Error: {response.status_code}"
                
            except Exception as e:
                ai_response = f"Error: {str(e)}"
        else:
            ai_response = "⚠️ Please configure Groq API key"
        
        st.session_state.ai_chat_history.append({
            "role": "assistant",
            "content": ai_response
        })
        
        st.rerun()

# TAB 3: History
with tab3:
    st.subheader("📋 Translation History")
    
    if st.session_state.chat_history:
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
            
            import pandas as pd
            df = pd.DataFrame(df_data)
            st.dataframe(df, use_container_width=True)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("📥 Export JSON"):
                    json_str = json.dumps(st.session_state.chat_history, indent=2)
                    st.download_button(
                        "Download JSON",
                        json_str,
                        "translations.json",
                        "application/json"
                    )
            
            with col2:
                if st.button("📥 Export CSV"):
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
        st.info("💡 Start a translation to see history")

# TAB 4: API Documentation
with tab4:
    st.subheader("📖 API Documentation")
    
    st.markdown("""
    ### Groq-Powered Translation API
    
    #### Authentication
    All endpoints require Bearer token:
    ```
    Authorization: Bearer YOUR_MCP_API_KEY
    ```
    
    #### Endpoints
    
    **1. Translate Text**
    ```
    POST /translate
    {
        "text": "Hello world",
        "source_lang": "en",
        "target_lang": "es",
        "mode": "simple",
        "groq_api_key": "YOUR_GROQ_KEY"
    }
    ```
    
    **2. Batch Translate**
    ```
    POST /translate-batch
    {
        "texts": ["Hello", "World"],
        "source_lang": "en",
        "target_lang": "es",
        "groq_api_key": "YOUR_GROQ_KEY"
    }
    ```
    
    **3. AI Chat**
    ```
    POST /chat
    {
        "message": "Translate hello to Spanish",
        "groq_api_key": "YOUR_GROQ_KEY"
    }
    ```
    
    **4. Health Check**
    ```
    GET /health
    ```
    
    ### Groq AI Models Available
    - **mixtral-8x7b-32768** - Fast, powerful, 32K context
    - **llama2-70b-4096** - Advanced reasoning, 4K context
    """)
    
    st.subheader("Languages Supported")
    
    lang_data = []
    for name, code in SUPPORTED_LANGUAGES.items():
        lang_data.append({"Language": name, "Code": code})
    
    import pandas as pd
    df_langs = pd.DataFrame(lang_data)
    st.dataframe(df_langs, use_container_width=True, hide_index=True)

# TAB 5: Settings
with tab5:
    st.subheader("⚙️ Advanced Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("About Groq")
        st.info("""
        **Groq AI Benefits:**
        
        ✅ **Ultra-fast Inference**
        - Specialized hardware (LPU)
        - Sub-second response times
        
        ✅ **Free Tier**
        - No credit card needed
        - Generous free quota
        
        ✅ **Multiple Models**
        - Mixtral 8x7B
        - Llama 2 70B
        - More coming soon
        
        ✅ **Perfect for Translation**
        - Context awareness
        - Nuanced understanding
        - Cultural sensitivity
        """)
    
    with col2:
        st.subheader("Debug Info")
        
        debug_info = {
            "Groq Connected": "✅ Yes" if st.session_state.groq_connected else "❌ No",
            "Groq Key Set": "✅ Yes" if st.session_state.groq_api_key else "❌ No",
            "API URL": st.session_state.api_base_url,
            "Chat Messages": len(st.session_state.chat_history),
            "AI Chat Messages": len(st.session_state.ai_chat_history) if "ai_chat_history" in st.session_state else 0
        }
        
        for key, value in debug_info.items():
            st.write(f"**{key}**: {value}")

# Footer
st.divider()
st.markdown("""
<div style="text-align: center; color: #00bfff; padding: 20px; border-top: 2px solid #0066ff;">
    <small>
        🤖 AI-Powered Translation with Groq | Powered by Groq AI & mT5<br>
        © 2025 | Fast, Accurate, Intelligent Translation<br>
        <span style="color: #ffffff;">Black & Blue Theme</span>
    </small>
</div>
""", unsafe_allow_html=True)
