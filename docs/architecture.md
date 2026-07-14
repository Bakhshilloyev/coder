# Architecture

The agent is built in layered modules so it stays portable and easy to extend.

## Layers

1. **Core layer** (`src/agent/core`) — platform-independent brain.
   - `agent.py` — orchestrates provider, memory, router, planner, executor.
   - `planner.py` — decomposes a goal into steps (LLM or local heuristic).
   - `executor.py` — runs a routed tool, handles confirmation gates.
   - `verifier.py` — checks whether the result satisfies the goal.
   - `tool_router.py` — maps natural language to the best tool + args.
   - `workflow.py` — the Understand → Plan → Execute → Verify → Improve loop.
   - `safety.py` — policy guard that blocks destructive commands.

2. **Adapters layer** (`src/agent/adapters`) — OS/architecture specific.
   - `common/arch.py`, `common/env.py`, `common/paths.py` — shared detection.
   - `linux/`, `windows/`, `termux/` — per-platform `describe()`.

3. **LLM layer** (`src/agent/llm`) — provider abstraction.
   - `provider_base.py` — `BaseProvider` + stdlib HTTP helpers.
   - `local_client.py` (offline), `openai_client.py`, `anthropic_client.py`,
     `gemini_client.py`, `groq_client.py`, `custom_client.py`.
   - `model_registry.py` — builds a provider from env/config, degrades to `local`.

4. **Tools layer** (`src/agent/tools`) — file, shell, web, api, memory, db.
   - Each tool is a `Tool` registered in a global `REGISTRY`.

5. **Memory layer** (`src/agent/memory`) — SQLite store, sessions, short/long-term,
   and a dependency-free keyword `VectorStore` for RAG.

6. **Runtime layer** (`src/agent/runtime`) — bootstrap, logging, cache, errors.

7. **API layer** (`src/agent/api`) — stdlib HTTP server (no framework).

8. **Integrations** (`src/agent/integrations`) — Telegram/Discord/Slack/GitHub
   (optional SDKs imported lazily).

## Data flow

```
user -> CLI/API -> Dispatcher -> Agent.chat/run
                                   |-> Planner -> steps
                                   |-> ToolRouter -> Executor -> Tool
                                   |-> Verifier
                                   |-> Memory (SQLite)
```

## Weak vs strong device strategy

| Aspect | Weak device | Strong device |
|--------|-------------|---------------|
| Default provider | `local` | remote (configurable) |
| Memory | bounded short-term + SQLite | + optional vector index |
| Concurrency | single-threaded | more parallelism |
| Features | core only | integrations enabled |
