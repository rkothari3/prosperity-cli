import socket
import subprocess
import time
import typer
import webbrowser
from pathlib import Path

from rich import print as rprint
from prosperity_cli.config import load as load_config

VISUALIZER_PATH_KEY = "visualizer_path"


def _find_visualizer() -> Path | None:
    cfg = load_config()
    if p := cfg.get(VISUALIZER_PATH_KEY):
        path = Path(p)
        if (path / "package.json").exists():
            return path

    candidates = [
        Path(__file__).parent.parent.parent / "IMC_P4_Visualizer",
        Path.home() / "IMC_P4_Visualizer",
    ]
    for c in candidates:
        if (c / "package.json").exists():
            return c
    return None


def _wait_for_port(port: int, timeout: float = 30.0) -> bool:
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            with socket.create_connection(("localhost", port), timeout=1):
                return True
        except OSError:
            time.sleep(0.25)
    return False


def run(
    log_file: Path | None = typer.Argument(None, help="Log file to load (shown as reminder)"),
    port: int = typer.Option(5173, "--port", "-p"),
):
    """Launch the visualizer in your browser."""
    vis_dir = _find_visualizer()
    if not vis_dir:
        rprint("[red]Error:[/red] Visualizer not found. Set its path with: prosperity config")
        rprint("[dim]Example: prosperity config → enter path like ~/IMC_P4_Visualizer[/dim]")
        raise typer.Exit(1)

    if log_file and not log_file.exists():
        rprint(f"[red]Error:[/red] Log file not found: {log_file}")
        raise typer.Exit(1)

    rprint(f"[cyan]Starting visualizer at[/cyan] http://localhost:{port}")
    if log_file:
        rprint(f"[yellow]Load this file in the UI:[/yellow] {log_file.resolve()}")

    proc = subprocess.Popen(
        ["pnpm", "dev", "--port", str(port)],
        cwd=str(vis_dir),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    if _wait_for_port(port):
        webbrowser.open(f"http://localhost:{port}")
        rprint(f"[green]✓[/green] Visualizer running at [link]http://localhost:{port}[/link] (Ctrl+C to stop)")
    else:
        rprint(f"[yellow]Warning:[/yellow] Server didn't respond on port {port} within 30s")

    try:
        proc.wait()
    except KeyboardInterrupt:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
        rprint("\n[yellow]Visualizer stopped.[/yellow]")
