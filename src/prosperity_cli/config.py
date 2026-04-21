import json
import typer
from pathlib import Path
from rich.console import Console
from rich.prompt import Prompt
from rich import print as rprint

CONFIG_PATH = Path.home() / ".prosperity" / "config.json"
console = Console()


def load() -> dict:
    if not CONFIG_PATH.exists():
        return {}
    return json.loads(CONFIG_PATH.read_text())


def save(data: dict) -> None:
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    CONFIG_PATH.write_text(json.dumps(data, indent=2))


def run(
    show: bool = typer.Option(False, "--show", help="Print current config path"),
):
    """Configure email, password, and round deadline."""
    if show:
        rprint(f"Config at: [cyan]{CONFIG_PATH}[/cyan]")
        return

    existing = load()

    email = Prompt.ask(
        "[cyan]Email[/cyan]",
        default=existing.get("email", ""),
    )
    password = Prompt.ask(
        "[cyan]Password[/cyan]",
        password=True,
        default=existing.get("password", "") or "",
    )
    deadline = Prompt.ask(
        "[cyan]Round deadline[/cyan] (YYYY-MM-DD HH:MM, optional)",
        default=existing.get("deadline", ""),
    )

    data = {"email": email, "password": password}
    if deadline.strip():
        data["deadline"] = deadline.strip()

    save(data)
    rprint("[green]✓[/green] Config saved.")
