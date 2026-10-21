# Xernel

A minimal, extensible terminal interface for development.

## Run with the `xernel` command

Requires Python 3, but no third-party libraries. Install the launcher once after cloning:

```bash
git clone https://github.com/ardakooza/xernel.git
sh xernel/install.sh
xernel
```

On Termux, the installer puts `xernel` in `$PREFIX/bin`. On other Linux systems it uses `~/.local/bin`; add that directory to `PATH` if the installer says it is not already there. A Git clone alone cannot register a command with the shell, so this one-time install step is required.

Optional commands:

```bash
xernel run
xernel update
xernel --version
xernel --help
```

`update` fetches the latest changes with a fast-forward-only Git pull. It stops without changing files if the clone has uncommitted changes. You can also type `/update` inside the TUI.

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

- `xernel` — open the dependency-free prompt
- `xernel run` — start an interactive prompt session
- `xernel update` — safely fetch and apply the latest version
- `xernel --version` — show the version
- `xernel --help` — show help

## Versioning

`src/xernel/VERSION` is the single source of truth. The standalone launcher, Python CLI, and package metadata all read the version from this file. Change it once for a release, then commit and push; `xernel update` retrieves the new version along with the code.

This is the initial TUI foundation. AI providers, MCP, file tools, and agents are intentionally out of scope for this first step.
