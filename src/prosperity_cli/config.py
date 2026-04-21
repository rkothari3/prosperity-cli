import json
import typer
from datetime import datetime
from pathlib import Path
from rich.prompt import Prompt
from rich import print as rprint

CONFIG_PATH = Path.home() / ".prosperity" / "config.json"


def load() -> dict:
    if not CONFIG_PATH.exists():
        return {}
    try:
        return json.loads(CONFIG_PATH.read_text())
    except json.JSONDecodeError:
        return {}


def save(data: dict) -> None:
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    CONFIG_PATH.write_text(json.dumps(data, indent=2))
    CONFIG_PATH.chmod(0o600)


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
    if not email.strip():
        rprint("[red]Error:[/red] Email cannot be empty.")
        raise typer.Exit(1)

    has_existing_password = bool(existing.get("password"))
    password_prompt = "[cyan]Password[/cyan] (press Enter to keep existing)" if has_existing_password else "[cyan]Password[/cyan]"
    password = Prompt.ask(
        password_prompt,
        password=True,
        show_default=False,
    )
    if not password and has_existing_password:
        password = existing["password"]

    if not password:
        rprint("[red]Error:[/red] Password cannot be empty.")
        raise typer.Exit(1)

    deadline = Prompt.ask(
        "[cyan]Round deadline[/cyan] (YYYY-MM-DD HH:MM, optional)",
        default=existing.get("deadline", ""),
    )

    visualizer_path = Prompt.ask(
        "[cyan]Visualizer path[/cyan] (optional, e.g. ~/IMC_P4_Visualizer)",
        default=existing.get("visualizer_path", ""),
    )

    data = {"email": email, "password": password}
    if deadline.strip():
        try:
            datetime.strptime(deadline.strip(), "%Y-%m-%d %H:%M")
        except ValueError:
            rprint("[red]Error:[/red] Deadline must be in YYYY-MM-DD HH:MM format.")
            raise typer.Exit(1)
        data["deadline"] = deadline.strip()

    if visualizer_path.strip():
        path = Path(visualizer_path.strip()).expanduser()
        if not path.exists():
            rprint("[red]Error:[/red] Visualizer path does not exist.")
            raise typer.Exit(1)
        if not (path / "package.json").exists():
            rprint("[red]Error:[/red] No package.json found in visualizer path.")
            raise typer.Exit(1)
        data["visualizer_path"] = str(path)

    save(data)
    rprint("[green]✓[/green] Config saved.")
