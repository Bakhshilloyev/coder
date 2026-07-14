# Prompts

The `prompts/` directory holds the text prompts used by the agent. They are
plain `.txt` files so they are easy to edit without touching code.

| File | Used by |
|------|---------|
| `system_prompt.txt` | default agent persona |
| `planner_prompt.txt` | planner (when an LLM is available) |
| `coder_prompt.txt` | coding tasks |
| `researcher_prompt.txt` | research tasks |
| `tool_router_prompt.txt` | LLM-based tool selection |
| `safety_prompt.txt` | policy-guard reasoning |

The default engine uses a deterministic local planner/router (regex based) so it
works without an LLM. When a remote provider is configured, the planner and
verifier use these prompts for richer behaviour. Edit them to tune behaviour for
your use case.
