#!/usr/bin/env python
"""
Run Streamlit app for Multilingual T5 Dashboard
"""

import subprocess
import sys
import os

def main():
    print("\n" + "="*70)
    print("  Multilingual T5 - Streamlit Dashboard")
    print("="*70)
    
    # Install streamlit if not already installed
    try:
        import streamlit
        print("\n✓ Streamlit already installed")
    except ImportError:
        print("\n📦 Installing Streamlit...")
        subprocess.run([sys.executable, "-m", "pip", "install", "streamlit==1.31.0", "-q"])
    
    print("\n🌐 Starting Streamlit app...")
    print("\n📍 Open your browser at: http://localhost:8501")
    print("\n⚡ Dashboard will load in a moment...\n")
    
    # Run streamlit
    subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])

if __name__ == "__main__":
    main()
