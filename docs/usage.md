# Usage

## CLI

```bash
# List configured models
python -m agent.main models

# Platform + agent info (OS, arch, memory, tools)
python -m agent.main info

# One-off chat (routes to a tool when it matches, else uses the LLM)
python -m agent.main chat "list files in the current directory"

# Goal-driven run: plan -> execute tools -> verify
python -m agent.main run "search the web for python tips"
python -m agent.main run "read README.md and summarize it"

# Start the HTTP API
python -m agent.main server --host 127.0.0.1 --port 8000
```

Common flags: `--provider`, `--model`, `--weak` (force weak-device mode).

## API

| Method | Path | Body |
|--------|------|------|
| GET | `/health` | — |
| GET | `/v1/models` | — |
| GET | `/v1/info` | — |
| POST | `/v1/chat` | `{"message": "..."}` |
| POST | `/v1/run` | `{"goal": "..."}` |

If `API_TOKEN` is set, send `Authorization: Bearer <token>`.

## Python

```python
from agent.app import get_agent
agent = get_agent(provider="local")
print(agent.chat("hello"))
result = agent.run("list files in the current directory")
print(result["summary"], result["verification"])
```

## Configuration

Config lives in `configs/` (falls back to repo-root JSON). Edit
`configs/default.json` for `log_level`, `weak_device_mode`, `memory_db`, etc.
`configs/permissions.json` controls `allow_shell` / `allow_network` /
`blocked_commands`.

## Environment variables

See `.env.example`. Key ones:

- `MODEL_PROVIDER` — local | openai | claude | gemini | groq | custom
- `LOG_LEVEL` — DEBUG | INFO | WARNING | ERROR
- `WEAK_DEVICE_MODE` — true/false
- `AUTO_APPROVE_SHELL` — set to `1` to auto-approve safe shell commands
- `API_TOKEN` — enable API auth
