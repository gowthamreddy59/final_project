@echo off
echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║    Multilingual T5 - Streamlit Dashboard Starting...          ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

REM Check if streamlit is installed
python -m pip show streamlit >nul 2>&1
if errorlevel 1 (
    echo Installing Streamlit and dependencies...
    python -m pip install -r requirements_streamlit.txt
)

echo.
echo ✓ Starting Streamlit app...
echo.
echo 🌐 Open your browser at: http://localhost:8501
echo.
echo Press Ctrl+C to stop the server
echo.

python -m streamlit run app.py

pause
