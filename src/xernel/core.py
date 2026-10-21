"""Shared, dependency-free Xernel CLI and terminal UI."""

from __future__ import annotations

import shutil
import subprocess
import sys
import unicodedata
from pathlib import Path

from xernel import __version__ as VERSION

RESET = "\033[0m"
BORDER = "\033[38;5;252m"
NOTICE_BORDER = "\033[38;5;88m"
NOTICE_TEXT = "\033[38;5;160m"
MUTED = "\033[38;5;245m"
WHITE = "\033[38;5;255m"
GREEN = "\033[38;5;114m"


def paint(text: str, color: str) -> str:
    return f"{color}{text}{RESET}" if sys.stdout.isatty() else text


def character_width(char: str) -> int:
    """Approximate terminal cell width using the Unicode database in stdlib."""
    code = ord(char)
    category = unicodedata.category(char)
    if (
        unicodedata.combining(char)
        or category in {"Mn", "Me", "Cf"}
        or 0xFE00 <= code <= 0xFE0F
        or 0xE0100 <= code <= 0xE01EF
        or 0x1F3FB <= code <= 0x1F3FF
        or code == 0x200D
    ):
        return 0
    return 2 if unicodedata.east_asian_width(char) in {"W", "F"} else 1


def display_width(text: str) -> int:
    """Return approximate terminal columns, accounting for wide/joined glyphs."""
    width = 0
    joined = False
    cluster_width = 0
    regional = False
    for char in text:
        code = ord(char)
        if code == 0x200D:
            joined = True
            continue
        char_cells = character_width(char)
        if char_cells == 0:
            continue
        if 0x1F1E6 <= code <= 0x1F1FF:
            if regional:
                regional = False
                continue
            regional = True
        else:
            regional = False
        if joined:
            width += max(0, char_cells - cluster_width)
            cluster_width = max(cluster_width, char_cells)
            joined = False
        else:
            width += char_cells
            cluster_width = char_cells
    return width


def break_long_word(word: str, width: int) -> list[str]:
    chunks: list[str] = []
    current = ""
    for char in word:
        candidate = current + char
        if current and display_width(candidate) > width:
            chunks.append(current)
            current = char
        else:
            current = candidate
    if current or not chunks:
        chunks.append(current)
    return chunks


def wrap_text(text: str, width: int) -> list[str]:
    """Wrap at word boundaries, splitting only words wider than the card."""
    wrapped: list[str] = []
    for paragraph in text.splitlines() or [""]:
        words = paragraph.split()
        if not words:
            wrapped.append("")
            continue
        line = ""
        for word in words:
            if display_width(word) > width:
                if line:
                    wrapped.append(line)
                    line = ""
                parts = break_long_word(word, width)
                wrapped.extend(parts[:-1])
                line = parts[-1]
            elif not line:
                line = word
            elif display_width(line) + 1 + display_width(word) <= width:
                line += " " + word
            else:
                wrapped.append(line)
                line = word
        if line:
            wrapped.append(line)
    return wrapped


def centered(text: str, width: int) -> str:
    spare = max(0, width - display_width(text))
    return " " * (spare // 2) + text + " " * (spare - spare // 2)


def card(
    title: str | None,
    lines: list[str],
    *,
    width: int | None = None,
    centered_lines: set[str] | None = None,
    border_color: str = BORDER,
    text_color: str = WHITE,
) -> None:
    terminal_width = shutil.get_terminal_size((80, 24)).columns
    inner = min(width or 68, max(20, terminal_width - 8))
    centered_lines = centered_lines or set()
    print(paint("  ╭" + "─" * (inner + 2) + "╮", border_color))
    content_lines = ([title] if title is not None else []) + lines
    for line in content_lines:
        is_centered = line == title or line in centered_lines
        chunks = wrap_text(line, inner)
        for chunk in chunks:
            text = centered(chunk, inner) if is_centered else chunk
            content = " " + text + " " * (inner - display_width(text) + 1)
            print(paint("  │", border_color) + paint(content, text_color) + paint("│", border_color))
    print(paint("  ╰" + "─" * (inner + 2) + "╯", border_color))


def clear_terminal() -> None:
    if sys.stdout.isatty():
        print("\033[2J\033[H", end="", flush=True)


def show_welcome() -> None:
    print()
    card(
        "Xernel",
        [f"READY    v{VERSION}", "", "A minimal development environment.", "Build. Think. Execute."],
        centered_lines={"Xernel"},
    )
    print()


def update_card(lines: list[str], *, initial: bool = False, final: bool = False) -> None:
    if not sys.stdout.isatty():
        if final:
            card(None, lines)
        return
    if initial:
        card(None, lines)
        return
    inner = min(68, max(20, shutil.get_terminal_size((80, 24)).columns - 8))
    for index, line in enumerate(lines):
        # Update status rows in place; the fixed progress copy fits narrow cards.
        text = wrap_text(line, inner)[0]
        content = " " + text + " " * (inner - display_width(text) + 1)
        up = 4 - index
        down = 3 - index
        sys.stdout.write(
            f"\033[{up}A\r\033[2K"
            + paint("  │", BORDER)
            + paint(content, WHITE)
            + paint("│", BORDER)
            + f"\033[{down}B\r"
            + paint("  ╰" + "─" * (inner + 2) + "╯", BORDER)
            + "\n"
        )
        sys.stdout.flush()


def run_git_animated(args: list[str], lines: list[str], active_line: int, message: str):
    try:
        process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    except OSError:
        return None, None, 1
    dots = 0
    while True:
        try:
            stdout, stderr = process.communicate(timeout=0.25)
            return stdout, stderr, process.returncode
        except subprocess.TimeoutExpired:
            if sys.stdout.isatty():
                dots = dots % 3 + 1
                lines[active_line] = message + "." * dots
                update_card(lines)


def update() -> int:
    repo = Path(__file__).resolve().parents[2]
    lines = ["Checking status", "Waiting for updates", "Fast-forward only"]
    if not (repo / ".git").exists():
        update_card(["No Git repository", "Cannot update", ""], final=True)
        return 1

    update_card(lines, initial=True)
    stdout, _, status_code = run_git_animated(
        ["git", "-C", str(repo), "status", "--porcelain"], lines, 0, "Checking status"
    )
    if status_code != 0:
        update_card(["Git status failed", "Install Git first", ""], final=True)
        return status_code
    if stdout and stdout.strip():
        update_card(["Local changes found", "Nothing was changed", "Commit or stash first"], final=True)
        return 1

    lines[:] = ["Repository clean", "Fetching updates", "Fast-forward only"]
    update_card(lines)
    stdout, _, pull_code = run_git_animated(
        ["git", "-C", str(repo), "pull", "--ff-only"], lines, 1, "Fetching updates"
    )
    if pull_code != 0:
        update_card(["Update failed", "Check network or Git", "Retry later"], final=True)
        return pull_code
    if stdout and "Already up to date" in stdout:
        update_card(["Already up to date", "No update needed", ""], final=True)
    else:
        update_card(["Update complete", "Restart Xernel", "New version ready"], final=True)
    return 0


def run_session() -> int:
    clear_terminal()
    show_welcome()
    while True:
        try:
            value = input(paint("  › ", GREEN)).strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not value:
            continue
        command = value.lower()
        if command.startswith("/"):
            if command in {"/exit", "/quit"}:
                break
            if command == "/update":
                update()
            elif command == "/help":
                card(None, ["/help     Show available commands", "/clear    Redraw the welcome screen", "/version  Print the current version", "/update   Pull latest code safely", "/exit     Close Xernel"])
            elif command == "/version":
                card(None, [f"xernel {VERSION}"])
            elif command == "/clear":
                clear_terminal()
                show_welcome()
            else:
                card(
                    None,
                    [f"{value} is not a Xernel command.", "Type /help to see available commands."],
                    border_color=NOTICE_BORDER,
                    text_color=NOTICE_TEXT,
                )
        else:
            card(
                None,
                ["Commands must start with /.", "Type /help to see available commands."],
                border_color=NOTICE_BORDER,
                text_color=NOTICE_TEXT,
            )
    print(paint("\n  Session closed. See you soon.\n", MUTED))
    return 0


def init_config() -> int:
    config = Path(".xernel.toml")
    if config.exists():
        card(None, ["Configuration already exists", ".xernel.toml"])
        return 1
    config.write_text('version = 1\n\n[ui]\ntheme = "dark"\n', encoding="utf-8")
    card(None, ["Created .xernel.toml"])
    return 0


def print_help() -> None:
    print(
        "Usage: xernel [run|update|init|--version|--help]\n\n"
        "Commands:\n"
        "  run       Start the Xernel terminal interface\n"
        "  update    Safely fetch the latest version\n"
        "  init      Create a starter configuration\n"
        "  --version Show the current version\n"
        "  --help    Show this help"
    )


def main() -> int:
    args = sys.argv[1:]
    if args in (["--version"], ["-v"]):
        print(f"xernel {VERSION}")
        return 0
    if args in (["--help"], ["-h"]):
        print_help()
        return 0
    if args == ["update"]:
        return update()
    if args == ["init"]:
        return init_config()
    if not args or args == ["run"]:
        return run_session()
    print(f"Unknown command: {' '.join(args)}", file=sys.stderr)
    print("Run 'xernel --help' for usage.", file=sys.stderr)
    return 2
