#!/usr/bin/env bash
# Termux (Android) setup. Keeps deps minimal and avoids root.
set -euo pipefail

echo "==> Goat AI Agent setup (Termux)"

pkg update -y
pkg install -y python python-pip

pip install --upgrade pip
pip install -r requirements.txt
[ -f requirements-termux.txt ] && pip install -r requirements-termux.txt || true

mkdir -p data/memory data/cache data/logs

echo "==> Done. Try:"
echo "    python -m agent.main models"
echo "    MODEL_PROVIDER=groq GROQ_API_KEY=... python -m agent.main run \"List files\""
