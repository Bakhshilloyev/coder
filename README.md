# Unified AI Agent

Cross-platform AI agent starter for Linux, Windows, and Termux.

## Providers
- Local fallback
- Claude via Anthropic API
- Gemini via Google API
- Groq via Groq API
- Custom API via configurable endpoint

## Quick start
```bash
git clone https://github.com/yourname/unified-ai-agent.git
cd unified-ai-agent
python -m agent.main models
```

## Environment variables
See `.env.example`.

### Provider selection
- `MODEL_PROVIDER=local`
- `MODEL_PROVIDER=claude`
- `MODEL_PROVIDER=gemini`
- `MODEL_PROVIDER=groq`
- `MODEL_PROVIDER=custom`

### Custom API
- `CUSTOM_API_URL`
- `CUSTOM_API_KEY`
- `CUSTOM_API_MODEL`
- `CUSTOM_API_AUTH_HEADER`
- `CUSTOM_API_AUTH_PREFIX`
- `CUSTOM_API_PROMPT_FIELD`
- `CUSTOM_API_MODEL_FIELD`
- `CUSTOM_API_RESPONSE_PATH`

## Examples
```bash
MODEL_PROVIDER=groq GROQ_API_KEY=... python -m agent.main run "Build a JSON parser"
MODEL_PROVIDER=claude ANTHROPIC_API_KEY=... python -m agent.main run "Refactor this code"
MODEL_PROVIDER=gemini GEMINI_API_KEY=... python -m agent.main run "Summarize this task"
MODEL_PROVIDER=custom CUSTOM_API_URL=https://... python -m agent.main run "Call my API"
```

## API server
```bash
python -m agent.api.server
```
