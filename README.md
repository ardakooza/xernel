# Xernel

A minimal, extensible terminal interface for development.

## Development install

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e .
xernel
xernel run
```

On Termux, install Python first with `pkg install python`.

## Initial commands

- `xernel` — open the minimal welcome screen
- `xernel run` — start an interactive prompt session
- `xernel --version` — show the version
- `xernel --help` — show help

This is the initial TUI foundation. AI providers, MCP, file tools, and agents are intentionally out of scope for this first step.
