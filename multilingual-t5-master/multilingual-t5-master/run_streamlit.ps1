#!/usr/bin/env pwsh

Write-Host "`n╔════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║    Multilingual T5 - Streamlit Dashboard Starting...          ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════════╝`n" -ForegroundColor Cyan

# Check if streamlit is installed
$streamlitExists = python -m pip show streamlit 2>$null
if (-not $streamlitExists) {
    Write-Host "Installing Streamlit and dependencies..." -ForegroundColor Yellow
    python -m pip install -r requirements_streamlit.txt
}

Write-Host "`n✓ Starting Streamlit app...`n" -ForegroundColor Green
Write-Host "🌐 Open your browser at: http://localhost:8501" -ForegroundColor Cyan
Write-Host "`nPress Ctrl+C to stop the server`n" -ForegroundColor Yellow

python -m streamlit run app.py
