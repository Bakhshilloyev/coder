# Windows setup for the Goat AI Agent (PowerShell).
$ErrorActionPreference = "Stop"

Write-Host "==> Goat AI Agent setup (Windows)"

python -m venv .venv
.\.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
python -m pip install -r requirements.txt
if (Test-Path requirements-windows.txt) { python -m pip install -r requirements-windows.txt }

New-Item -ItemType Directory -Force -Path data/memory, data/cache, data/logs | Out-Null

Write-Host "==> Done. Try:"
Write-Host "    python -m agent.main models"
Write-Host '    set MODEL_PROVIDER=groq && set GROQ_API_KEY=... && python -m agent.main run "List files"'
