"""
Groq AI Chatbot & Translation System Launcher
Starts API server with Groq integration and Streamlit dashboard
"""

import subprocess
import sys
import time
import os
from pathlib import Path

def install_dependencies():
    """Install required packages"""
    print("📦 Installing dependencies (including Groq)...")
    subprocess.run([
        sys.executable, "-m", "pip", "install", "-q", "-r", "requirements_groq.txt"
    ])
    print("✅ Dependencies installed")

def start_groq_api_server():
    """Start FastAPI server with Groq support"""
    print("\n🚀 Starting Groq-Powered API Server...")
    print("   URL: http://localhost:8000")
    print("   Docs: http://localhost:8000/docs")
    print("   Using: Groq's fastest inference LLM API")
    
    process = subprocess.Popen([
        sys.executable, "api_server_groq.py"
    ])
    time.sleep(3)
    return process

def start_streamlit_app():
    """Start Streamlit app with Groq UI"""
    print("\n💬 Starting Groq AI Chatbot Dashboard...")
    print("   URL: http://localhost:8501")
    print("   Features: Translation + General AI Chat")
    
    subprocess.run([
        "streamlit", "run", "app_groq.py"
    ])

def main():
    """Main launcher"""
    print("=" * 70)
    print("🤖 GROQ AI CHATBOT & TRANSLATION SYSTEM - LAUNCHER")
    print("=" * 70)
    print("\nThis system integrates Groq's ultra-fast AI for:")
    print("  • Multilingual Translation (20+ languages)")
    print("  • General AI Chat & Assistance")
    print("  • Powered by Groq's LPU Inference Engine")
    print("\n")
    
    # Check for requirements file
    if not Path("requirements_groq.txt").exists():
        print("❌ requirements_groq.txt not found!")
        sys.exit(1)
    
    # Install dependencies
    try:
        install_dependencies()
    except Exception as e:
        print(f"❌ Failed to install dependencies: {e}")
        sys.exit(1)
    
    # Start API server
    api_process = None
    try:
        api_process = start_groq_api_server()
    except Exception as e:
        print(f"❌ Failed to start API server: {e}")
        sys.exit(1)
    
    # Start Streamlit app
    try:
        start_streamlit_app()
    except KeyboardInterrupt:
        print("\n\n⏹️  Shutting down...")
    finally:
        if api_process:
            api_process.terminate()
            print("✅ API server stopped")

if __name__ == "__main__":
    main()
