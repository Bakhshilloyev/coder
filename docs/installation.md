# Installation

The engine uses **only the Python standard library** by default, so it works on
Termux and 32-bit systems without native builds. Install third-party SDKs only
when you use the corresponding provider or integration.

## Prerequisites

- Python 3.9+ (3.10+ recommended)
- `pip` (usually bundled)
- No GPU, Docker, or root required

## Linux / macOS

```bash
git clone https://github.com/yourname/unified-ai-agent.git
cd unified-ai-agent
bash scripts/setup.sh
```

`setup.sh` creates a venv (if possible), installs `requirements*.txt`, and makes
the `data/` directories.

## Windows

```powershell
git clone https://github.com/yourname/unified-ai-agent.git
cd unified-ai-agent
pwsh scripts/setup.ps1
```

Or double-click `scripts/run_dev.bat`.

## Termux (Android)

```bash
pkg install -y python python-pip git
git clone https://github.com/yourname/unified-ai-agent.git
cd unified-ai-agent
bash scripts/setup_termux.sh
```

Termux keeps data inside its sandbox (`~/.termux/unified-agent/data`) to avoid
permission issues.

## Verify

```bash
python -m agent.main info
```

You should see platform details and `provider: local`.
