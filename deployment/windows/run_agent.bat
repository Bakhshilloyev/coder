@echo off
REM Windows: run the Goat AI Agent API server.
set PYTHONPATH=%cd%\src
set MODEL_PROVIDER=local
python -m agent.main server --host 127.0.0.1 --port 8000
