# Xernel

A minimal, extensible terminal interface for development.

## Install as a Python CLI package

Requires Python 3.10 or newer. The package publishes a `xernel` console command through its Python project entry point. For an isolated installation, use `pipx`:

```bash
pipx install git+https://github.com/ardakooza/xernel.git
xernel
```

If the `xernel` command is not found after installing pipx, run `pipx ensurepath` once and restart the terminal. Alternatively, install from an active virtual environment with `python -m pip install git+https://github.com/ardakooza/xernel.git`; activating that environment makes `xernel` available.

To upgrade a pipx installation, run `pipx upgrade xernel-cli`.

### Termux (without pipx)

Termux does not necessarily provide `pipx` as a `pkg` command. Install Git and Python with Termux, remove a stale source-launcher symlink if you previously deleted the cloned folder, then install the Python CLI package:

```bash
pkg install python git
rm -f "$PREFIX/bin/xernel"
python -m pip install --no-cache-dir --force-reinstall git+https://github.com/ardakooza/xernel.git
hash -r
xernel
```

The package entry point installs `xernel` into Termux’s `$PREFIX/bin`, which is already on the standard Termux `PATH`.

## Run from a source checkout

If you prefer not to install the Python package, the repository also has a direct source launcher:

```bash
git clone https://github.com/ardakooza/xernel.git
sh xernel/install.sh
xernel
```

On Termux, the source installer places the launcher in `$PREFIX/bin`. On other Linux systems it uses `~/.local/bin`; add that directory to `PATH` if prompted.

Optional commands:

```bash
xernel run
xernel update
xernel --version
xernel --help
```

For a source-checkout installation, `xernel update` fetches changes with a fast-forward-only Git pull and stops if local changes are present. For a pipx package installation, use `pipx upgrade xernel-cli`. You can also type `/update` inside the TUI when running from a source checkout.

## Development install

Both the standalone launcher and installed console command use the same implementation in `src/xernel/core.py`.

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
- `xernel init` — create a starter configuration
- `xernel --version` — show the version
- `xernel --help` — show help

## Versioning

`src/xernel/VERSION` is the single source of truth. The standalone launcher, Python CLI, and package metadata all read the version from this file. Change it once for a release, then commit and push; `xernel update` retrieves the new version along with the code.

This is the initial TUI foundation. AI providers, MCP, file tools, and agents are intentionally out of scope for this first step.
