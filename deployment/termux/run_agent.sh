#!/usr/bin/env bash
# Termux: keep the agent server alive with a simple restart loop.
cd "$(dirname "$0")/../.." || exit 1
export PYTHONPATH="$(pwd)/src"
export MODEL_PROVIDER="${MODEL_PROVIDER:-local}"
while true; do
  echo "[termux] starting agent server..."
  python -m agent.main server --host 127.0.0.1 --port 8000
  echo "[termux] server stopped; restarting in 3s"
  sleep 3
done
