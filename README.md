# Xernel

A minimal, extensible terminal interface for development.

## Run directly after cloning (no dependencies)

Requires Python 3, but no package installation or third-party libraries.

```bash
git clone https://github.com/ardakooza/xernel.git
cd xernel
./xernel
```

Optional commands:

```bash
./xernel run
./xernel --version
./xernel --help
```

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

- `./xernel` — open the dependency-free prompt directly from the repository
- `./xernel run` — start an interactive prompt session
- `./xernel --version` — show the version
- `./xernel --help` — show help

This is the initial TUI foundation. AI providers, MCP, file tools, and agents are intentionally out of scope for this first step.
