import webbrowser
import typer
from pathlib import Path
from rich import print as rprint

VISUALIZER_URL = "https://imc-prosperity-4-visualizer.vercel.app/"


def run(
    log_file: Path | None = typer.Argument(None, help="Log file to load in the visualizer"),
):
    """Open the IMC Prosperity visualizer in your browser."""
    if log_file and not log_file.exists():
        rprint(f"[red]Error:[/red] Log file not found: {log_file}")
        raise typer.Exit(1)

    rprint(f"[cyan]Opening visualizer →[/cyan] {VISUALIZER_URL}")
    if log_file:
        rprint(f"[yellow]Load this file in the UI:[/yellow] {log_file.resolve()}")

    webbrowser.open(VISUALIZER_URL)
