from __future__ import annotations

import typer
from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from rich.console import Console
from rich.text import Text

from xernel import __version__

app = typer.Typer(
    name="xernel",
    help="A minimal, extensible development terminal.",
    no_args_is_help=False,
    add_completion=False,
)
console = Console()


def show_welcome() -> None:
    console.print()
    console.print(Text("XERNEL", style="bold white"))
    console.print(Text("A MINIMAL DEVELOPMENT ENVIRONMENT", style="dim"))
    console.print()
    console.print(Text("Build. Think. Execute.", style="white"))
    console.print()
    console.print(Text(f"Version   {__version__}", style="dim"))
    console.print(Text("Status    Ready", style="dim"))
    console.print()
    console.print(Text("Type a request to begin, or /help for commands.", style="white"))
    console.print(Text("This initial build does not connect to an AI model yet.", style="dim"))
    console.print()


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    version: bool = typer.Option(
        False, "--version", "-v", help="Show the installed version."
    ),
) -> None:
    """Open Xernel's minimal terminal interface."""
    if version:
        console.print(f"xernel {__version__}")
        raise typer.Exit()

    if ctx.invoked_subcommand is None:
        run_session()


@app.command()
def run() -> None:
    """Start the interactive terminal session."""
    run_session()


@app.command()
def init() -> None:
    """Create a starter Xernel configuration in the current directory."""
    from pathlib import Path

    config = Path(".xernel.toml")
    if config.exists():
        console.print("[yellow]Configuration already exists:[/yellow] .xernel.toml")
        raise typer.Exit(code=1)

    config.write_text(
        'version = 1\n\n[ui]\ntheme = "dark"\n', encoding="utf-8"
    )
    console.print("[white]Created[/white] .xernel.toml")


def run_session() -> None:
    show_welcome()
    session = PromptSession(history=FileHistory("~/.xernel_history"))

    while True:
        try:
            value = session.prompt(
                [("class:prompt", "> ")],
                style=None,
            ).strip()
        except (EOFError, KeyboardInterrupt):
            console.print()
            break

        if not value:
            continue

        command = value.lower()
        if command in {"/exit", "/quit", "exit", "quit"}:
            break
        if command in {"/help", "help"}:
            console.print("Commands: /help  /clear  /version  /exit")
            continue
        if command in {"/version", "version"}:
            console.print(f"xernel {__version__}")
            continue
        if command in {"/clear", "clear"}:
            console.clear()
            continue

        console.print(
            "[dim]The interactive shell is ready. AI execution will be added in a later stage.[/dim]"
        )

    console.print(Text("Session ended.", style="dim"))


if __name__ == "__main__":
    app()
