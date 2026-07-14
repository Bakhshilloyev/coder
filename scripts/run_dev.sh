#!/usr/bin/env bash
# Run the agent in development mode with verbose logging.
set -euo pipefail
export LOG_LEVEL=DEBUG
export PYTHONPATH="$(pwd)/src:${PYTHONPATH:-}"
exec python3 -m agent.main "$@"
