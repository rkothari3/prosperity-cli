import io
import time
import zipfile
from datetime import datetime
from pathlib import Path

import requests
import typer
from rich import print as rprint
from rich.console import Console
from rich.live import Live
from rich.text import Text

from prosperity_cli.config import load as load_config, save as save_config

console = Console()

USER_POOL_ID = "eu-west-1_wKiTmHXUE"
CLIENT_ID = "5kgp0jm69aeb91paqj1hnps838"
API_BASE = "https://3dzqiahkw1.execute-api.eu-west-1.amazonaws.com/prod"
TERMINAL_STATUSES = {"FINISHED", "ERROR", "ERROR_FINISHED", "TIMEOUT"}
ERROR_STATUSES = TERMINAL_STATUSES - {"FINISHED"}


def _authenticate(email: str, password: str) -> tuple[str, str]:
    from pycognito import Cognito
    user = Cognito(USER_POOL_ID, CLIENT_ID, username=email)
    user.authenticate(password=password)
    return user.id_token, user.refresh_token


def _refresh_token(refresh_token: str) -> str:
    from pycognito import Cognito
    user = Cognito(USER_POOL_ID, CLIENT_ID)
    user.refresh_token = refresh_token
    user.renew_access_token()
    return user.id_token


def _get_token(cfg: dict) -> str:
    refresh = cfg.get("refresh_token")
    if refresh:
        try:
            token = _refresh_token(refresh)
            if cfg.get("id_token") != token:
                cfg["id_token"] = token
                save_config(cfg)
            return token
        except Exception:
            pass

    token, refresh = _authenticate(cfg["email"], cfg["password"])
    cfg["id_token"] = token
    cfg["refresh_token"] = refresh
    save_config(cfg)
    return token


def _api(method: str, path: str, token: str, **kwargs) -> requests.Response:
    r = requests.request(
        method,
        API_BASE + path,
        headers={"Authorization": f"Bearer {token}"},
        timeout=30,
        **kwargs,
    )
    r.raise_for_status()
    return r


def _current_round(token: str) -> str:
    rounds = _api("GET", "/rounds", token).json()
    active = [r for r in rounds if r.get("state") != "FINISHED"]
    return str((active or rounds)[-1]["id"])


def _submit(token: str, algorithm: Path) -> dict:
    with algorithm.open("rb") as f:
        return _api("POST", "/submission/algo", token,
                    files={"file": (algorithm.name, f, "text/plain")}).json()


def _poll(token: str, round_id: str, submission_id: str):
    """Yield elapsed seconds; return final submission dict when terminal status reached."""
    start = time.time()
    while True:
        subs = _api("GET", f"/submissions/algo/{round_id}?page=1&pageSize=50", token).json()
        items = subs if isinstance(subs, list) else subs.get("submissions", subs.get("items", []))
        match = next((s for s in items if s.get("id") == submission_id), None)
        if match and match.get("status") in TERMINAL_STATUSES:
            return match
        yield int(time.time() - start)
        time.sleep(5)


def _download_log(token: str, submission_id: str, dest: Path) -> Path:
    body = _api("GET", f"/submissions/algo/{submission_id}/zip", token).json()
    zip_url = body.get("url") or body.get("signedUrl") or body

    zip_bytes = requests.get(zip_url, timeout=60).content if isinstance(zip_url, str) else zip_url

    dest.parent.mkdir(parents=True, exist_ok=True)
    try:
        with zipfile.ZipFile(io.BytesIO(zip_bytes)) as zf:
            log_names = [n for n in zf.namelist() if n.endswith(".log")]
            if log_names:
                dest.write_bytes(zf.read(log_names[0]))
                return dest
    except zipfile.BadZipFile:
        pass

    dest.write_bytes(zip_bytes)
    return dest


def run(
    algorithm: Path = typer.Argument(..., help="Path to trader.py"),
    no_vis: bool = typer.Option(False, "--no-vis", help="Skip visualizer after submit"),
    port: int = typer.Option(5173, "--port", help="Visualizer port"),
):
    """Submit algorithm to IMC Prosperity, wait for results, open visualizer."""
    cfg = load_config()
    if not cfg.get("email") or not cfg.get("password"):
        rprint("[red]Error:[/red] No credentials configured. Run: prosperity config")
        raise typer.Exit(1)

    if not algorithm.exists():
        rprint(f"[red]Error:[/red] File not found: {algorithm}")
        raise typer.Exit(1)

    with console.status("[cyan]Authenticating...[/cyan]"):
        try:
            token = _get_token(cfg)
        except Exception as e:
            rprint(f"[red]Error:[/red] Authentication failed: {e}")
            raise typer.Exit(1)
    rprint("[green]✓[/green] Authenticated")

    with console.status("[cyan]Getting current round...[/cyan]"):
        try:
            round_id = _current_round(token)
        except Exception as e:
            rprint(f"[red]Error:[/red] Could not fetch rounds: {e}")
            raise typer.Exit(1)

    with console.status(f"[cyan]Submitting {algorithm.name}...[/cyan]"):
        try:
            submission = _submit(token, algorithm)
        except Exception as e:
            rprint(f"[red]Error:[/red] Submission failed: {e}")
            raise typer.Exit(1)

    submission_id = submission.get("id")
    round_id = str(submission.get("roundId", round_id))
    rprint(f"[green]✓[/green] Submitted (id: [dim]{submission_id}[/dim])")

    rprint("[cyan]Waiting for results...[/cyan]")
    try:
        gen = _poll(token, round_id, submission_id)
        with Live(console=console, refresh_per_second=4) as live:
            while True:
                try:
                    elapsed = next(gen)
                    live.update(Text(f"  Simulating...  {elapsed}s elapsed", style="yellow"))
                except StopIteration as exc:
                    final = exc.value
                    break
    except Exception as e:
        rprint(f"[red]Error:[/red] Polling failed: {e}")
        raise typer.Exit(1)

    status = (final or {}).get("status", "UNKNOWN")
    if status in ERROR_STATUSES:
        rprint(f"[red]✗[/red] Simulation ended with status: [bold]{status}[/bold]")
    else:
        rprint("[green]✓[/green] Results ready!")

    ts = datetime.now().strftime("%Y-%m-%d-%H%M")
    log_path = Path("backtests") / f"{ts}-live.log"
    with console.status("[cyan]Downloading results...[/cyan]"):
        try:
            log_path = _download_log(token, submission_id, log_path)
            rprint(f"[green]✓[/green] Saved → {log_path}")
        except Exception as e:
            rprint(f"[yellow]Warning:[/yellow] Could not download results: {e}")

    if not no_vis:
        from prosperity_cli import visualize
        visualize.run(log_file=log_path if log_path.exists() else None, port=port)
