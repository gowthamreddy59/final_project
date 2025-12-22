@echo off
REM mT5 Translator - Complete System Launcher (Windows)

echo.
echo ╔═══════════════════════════════════════════════════════════╗
echo ║   🌍 mT5 MULTILINGUAL TRANSLATOR - SYSTEM LAUNCHER       ║
echo ║                   Complete Package                        ║
echo ╚═══════════════════════════════════════════════════════════╝
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found! Please install Python 3.8+
    pause
    exit /b 1
)

echo ✅ Python found
echo.

REM Install dependencies
echo 📦 Installing dependencies...
python -m pip install -q -r requirements_enhanced.txt
if errorlevel 1 (
    echo ❌ Failed to install dependencies
    pause
    exit /b 1
)

echo ✅ Dependencies installed
echo.

REM Start API Server
echo 🚀 Starting API Server (http://localhost:8000)...
start "mT5 API Server" python api_server.py

REM Wait for server to start
timeout /t 3 /nobreak

REM Start Streamlit
echo 💬 Starting Streamlit Dashboard (http://localhost:8501)...
timeout /t 1 /nobreak
streamlit run app_enhanced.py

echo.
echo ⏹️  System shutdown
pause
