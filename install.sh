#!/bin/sh
set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
if ! command -v python3 >/dev/null 2>&1; then
    echo "Python 3 is required. On Termux, run: pkg install python" >&2
    exit 1
fi
if ! python3 -c 'import sys; raise SystemExit(0 if sys.version_info >= (3, 10) else 1)'; then
    PYTHON_VERSION=$(python3 --version 2>&1 || true)
    echo "Xernel requires Python 3.10 or newer; found ${PYTHON_VERSION}. Upgrade Python and retry." >&2
    exit 1
fi

if [ -n "${PREFIX:-}" ] && [ -d "$PREFIX/bin" ] && [ -w "$PREFIX/bin" ]; then
    BIN_DIR="$PREFIX/bin"
else
    BIN_DIR="$HOME/.local/bin"
    mkdir -p "$BIN_DIR"
fi
TARGET="$BIN_DIR/xernel"

if [ -e "$TARGET" ] || [ -L "$TARGET" ]; then
    if [ -L "$TARGET" ] && [ "$(readlink "$TARGET")" = "$SCRIPT_DIR/xernel" ]; then
        echo "Xernel is already installed at $TARGET"
        exit 0
    fi
    echo "Refusing to replace existing command: $TARGET" >&2
    exit 1
fi

ln -s "$SCRIPT_DIR/xernel" "$TARGET"
echo "Installed xernel at $TARGET"
case ":$PATH:" in
    *":$BIN_DIR:"*) echo "Run it with: xernel" ;;
    *) echo "Add $BIN_DIR to PATH in your shell configuration, then run: xernel" ;;
esac
