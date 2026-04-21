import typer
from pathlib import Path

def run(
    algorithm: Path = typer.Argument(...),
    rounds: list[str] = typer.Argument(...),
):
    """Run backtester on a trader algorithm."""
    pass
