@echo off
REM Run the agent in development mode (Windows).
set LOG_LEVEL=DEBUG
set PYTHONPATH=%cd%\src;%PYTHONPATH%
python -m agent.main %*
