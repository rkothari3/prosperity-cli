import typer
from pathlib import Path

def run(
    algorithm: Path = typer.Argument(...),
):
    """Submit algorithm to IMC Prosperity, wait for results, open visualizer."""
    pass
