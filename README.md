# Unified AI Agent

A compact, cross-platform AI agent engine built to run anywhere: **Linux**,
**Windows**, **Termux (Android)**, and **32-bit / weak devices**.

- **Zero hard dependencies** — runs offline with the built-in `local` provider.
- **Layered design** — core, adapters, fallback, and optional layers.
- **Pluggable LLM providers** — local, OpenAI, Anthropic, Gemini, Groq, custom.
- **Tools** — file, shell, web, api, memory, sqlite.
- **Safety first** — a policy guard blocks destructive commands.
- **HTTP API + CLI + optional web UI + chat integrations** (Telegram/Discord/Slack/GitHub).

---

## Quick start

```bash
git clone https://github.com/yourname/unified-ai-agent.git
cd unified-ai-agent
pip install -r requirements.txt          # optional; runs with stdlib only
python -m agent.main models              # list configured models
python -m agent.main info                # show platform + agent info
python -m agent.main chat "hello"        # single chat message
python -m agent.main run "list files in the current directory"
```

### With a remote provider

```bash
MODEL_PROVIDER=groq GROQ_API_KEY=... python -m agent.main run "Build a JSON parser"
MODEL_PROVIDER=claude ANTHROPIC_API_KEY=... python -m agent.main run "Refactor this code"
MODEL_PROVIDER=gemini GEMINI_API_KEY=... python -m agent.main run "Summarize this task"
MODEL_PROVIDER=custom CUSTOM_API_URL=https://... python -m agent.main run "Call my API"
```

### API server

```bash
python -m agent.main server --host 127.0.0.1 --port 8000
# endpoints: /health /v1/models /v1/info /v1/chat /v1/run
# optional auth: set API_TOKEN (Bearer) 
```

### Web UI

Serve the `web/` folder (e.g. `python -m http.server 8080 --directory web`) and open
`http://127.0.0.1:8080` — it talks to the API server on port 8000.

---

## Provider selection

| Env | Provider |
|-----|----------|
| `MODEL_PROVIDER=local` | offline heuristic (default, no key) |
| `MODEL_PROVIDER=claude` | Anthropic Claude (`ANTHROPIC_API_KEY`) |
| `MODEL_PROVIDER=gemini` | Google Gemini (`GEMINI_API_KEY`) |
| `MODEL_PROVIDER=groq` | Groq (`GROQ_API_KEY`) |
| `MODEL_PROVIDER=custom` | any OpenAI-compatible endpoint |

See `.env.example` for all variables, including `CUSTOM_API_*` knobs.

---

## Architecture

See [`docs/architecture.md`](docs/architecture.md). In short:

```
adapters (platform) -> runtime (bootstrap/logging/cache) -> core (agent/planner/executor/verifier/router)
        |                                                              |
        v                                                              v
      llm (providers)  <----- tools (file/shell/web/api/memory/db) <--+
```

## Installation per platform

- Linux/macOS: `bash scripts/setup.sh`
- Windows: `pwsh scripts/setup.ps1` (or `run_dev.bat`)
- Termux: `bash scripts/setup_termux.sh`

## License

MIT — see [`LICENSE`](LICENSE).
