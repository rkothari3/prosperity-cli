import subprocess
import typer
from pathlib import Path
from typing import Optional
from rich import print as rprint


def run(
    algorithm: Path = typer.Argument(..., help="Path to trader.py"),
    rounds: list[str] = typer.Argument(..., help="Round(s) e.g. 1 or 1-0"),
    vis: bool = typer.Option(False, "--vis", help="Open visualizer after backtest"),
    merge_pnl: bool = typer.Option(False, "--merge-pnl", help="Merge PnL across days"),
    print_output: bool = typer.Option(False, "--print", help="Stream trader output"),
    out: Optional[Path] = typer.Option(None, "--out", help="Output log path"),
    no_out: bool = typer.Option(False, "--no-out", help="Disable log output"),
):
    """Run backtester on a trader algorithm."""
    if not algorithm.exists():
        rprint(f"[red]Error:[/red] File not found: {algorithm}")
        raise typer.Exit(1)

    cmd = ["prosperity4btest", str(algorithm)] + list(rounds)

    if vis:
        cmd.append("--vis")
    if merge_pnl:
        cmd.append("--merge-pnl")
    if print_output:
        cmd.append("--print")
    if out:
        cmd += ["--out", str(out)]
    if no_out:
        cmd.append("--no-out")

    rprint(f"[cyan]Running:[/cyan] {' '.join(cmd)}")
    result = subprocess.run(cmd)
    raise typer.Exit(result.returncode)
