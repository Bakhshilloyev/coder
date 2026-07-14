#!/usr/bin/env bash
# Linux / macOS setup for the Goat AI Agent (pure-Python, minimal deps).
set -euo pipefail

echo "==> Goat AI Agent setup (Linux/macOS)"

python3 -m venv .venv 2>/dev/null || true
if [ -d .venv ]; then
  # shellcheck disable=SC1091
  source .venv/bin/activate
fi

python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
[ -f requirements-linux.txt ] && python3 -m pip install -r requirements-linux.txt || true

mkdir -p data/memory data/cache data/logs

echo "==> Done. Try:"
echo "    python3 -m agent.main models"
echo "    MODEL_PROVIDER=groq GROQ_API_KEY=... python3 -m agent.main run \"List files\""
