"""
Complete Launcher for mT5 Translation System
Starts API server and Streamlit app
"""

import subprocess
import sys
import time
import os
from pathlib import Path

def install_dependencies():
    """Install required packages"""
    print("📦 Installing dependencies...")
    subprocess.run([
        sys.executable, "-m", "pip", "install", "-q", "-r", "requirements_enhanced.txt"
    ])
    print("✅ Dependencies installed")

def start_api_server():
    """Start FastAPI server in background"""
    print("\n🚀 Starting API Server...")
    print("   URL: http://localhost:8000")
    print("   Docs: http://localhost:8000/docs")
    print("   API Key (for testing): test-key-12345")
    
    process = subprocess.Popen([
        sys.executable, "api_server.py"
    ])
    time.sleep(2)
    return process

def start_streamlit_app():
    """Start Streamlit app"""
    print("\n💬 Starting Streamlit Dashboard...")
    print("   URL: http://localhost:8501")
    
    subprocess.run([
        "streamlit", "run", "app_enhanced.py"
    ])

def main():
    """Main launcher"""
    print("=" * 60)
    print("🌍 mT5 TRANSLATION SYSTEM - LAUNCHER")
    print("=" * 60)
    
    # Check for requirements file
    if not Path("requirements_enhanced.txt").exists():
        print("❌ requirements_enhanced.txt not found!")
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
        api_process = start_api_server()
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
