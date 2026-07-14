# Troubleshooting

## `ModuleNotFoundError: No module named 'agent'`
Run from the repo root with `src` on the path:
```bash
PYTHONPATH=src python -m agent.main info
```
Or install editable: `pip install -e .`

## Provider returns "OFFLINE FALLBACK"
No API key is set for the chosen provider. Either set the key
(e.g. `GROQ_API_KEY`) or use the default `local` provider. The agent always
degrades gracefully to `local` instead of crashing.

## Shell command blocked
The safety policy guard blocks destructive patterns (`rm -rf /`, `mkfs`,
`dd if=/dev/...`, fork bombs). Adjust `configs/permissions.json` if needed, but
do so carefully.

## `CONFIRMATION_REQUIRED` on a shell command
Mutating commands require confirmation. In non-interactive use, set
`AUTO_APPROVE_SHELL=1` (only on trusted input), or pass a `confirm` callback to
`Executor`.

## Termux: permission denied writing files
Termux sandboxes storage. The agent uses `~/.termux/unified-agent/data` by
default. Set `AGENT_DATA_DIR` or grant storage permissions.

## Web search returns nothing
The search uses the DuckDuckGo HTML endpoint; if it is unreachable you'll get a
clear error rather than a crash. Check network/`allow_network`.

## 32-bit / low-RAM device is slow
Keep `weak_device_mode: true` (default). This limits context windows and avoids
heavy optional modules. Avoid installing the integration SDKs.
