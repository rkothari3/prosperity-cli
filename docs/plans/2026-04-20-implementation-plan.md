# prosperity-cli Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development to implement remaining tasks.

**Goal:** Build `prosperity-cli`, a pip-installable Python CLI that unifies IMC Prosperity backtesting, visualization, and algorithm submission into one tool.

**Architecture:** Single `typer`-based CLI package. Backtester shells out to `prosperity4btest` CLI. Visualizer launches the existing `pnpm dev` server (dev-server approach — simpler, no build/bundle needed). Submission reverse-engineers the IMC Prosperity web API using `requests`.

**Tech Stack:** Python 3.11+, `typer`, `rich`, `requests`. Node.js/pnpm required at runtime for visualizer (users already have it).

**Package location:** `/mnt/c/Users/rajg6/OneDrive/Desktop/IMC_P4/Round_2/prosperity-cli/`

---

## Progress

- [x] Task 1: Package scaffold
- [x] Task 2: Config command
- [x] Task 3: Backtest command
- [ ] Task 4: Visualize command (dev-server approach)
- [ ] Task 5: ~~Visualizer auto-load React patch~~ — **REPLACED** by passing log path via CLI arg to pnpm dev or a query param
- [ ] Task 6: Submit API discovery
- [ ] Task 7: Submit command implementation
- [ ] Task 8: Countdown timer
- [ ] Task 9: README + PyPI prep

---

## Completed Work

### What exists in `src/prosperity_cli/`

**`__init__.py`** — `__version__ = "0.1.0"`

**`cli.py`** — Typer app with 4 commands wired via explicit names:
```python
app.command("config")(config_cmd.run)
app.command("backtest")(backtest.run)
app.command("visualize")(visualize.run)
app.command("submit")(submit.run)
```

**`config.py`** — Full implementation:
- `CONFIG_PATH = Path.home() / ".prosperity" / "config.json"`
- `load() -> dict` — returns {} if missing, handles JSONDecodeError
- `save(data)` — writes with `chmod(0o600)` for security
- `run()` — interactive prompts for email, password (masked, doesn't echo existing), deadline (validated YYYY-MM-DD HH:MM format). Empty email/password raises error.

**`backtest.py`** — Thin subprocess wrapper around `prosperity4btest`:
- Args: `algorithm: Path`, `rounds: list[str]`
- Flags: `--vis`, `--merge-pnl`, `--print` (as `print_output`), `--out`, `--no-out`
- Validates file exists, builds command, runs subprocess, propagates exit code

**`visualize.py`** — STUB only (not yet implemented)

**`submit.py`** — STUB only (not yet implemented)

### Tests passing
- `tests/test_config.py` — 3 tests (save/load, missing file, file permissions 0o600)
- `tests/test_backtest.py` — 3 tests (missing file, correct command, --vis flag)

### Key decisions made
- `prosperity4bt` removed from pip dependencies — it's not on PyPI, users install the backtester repo separately
- Visualizer: **dev-server approach** — `prosperity visualize` launches `pnpm dev` in the visualizer repo dir
- Credentials stored at `~/.prosperity/config.json` with restricted permissions
- Color palette: teal `#00B4B4` for success/headers, orange `#FF6B2B` for countdown/warnings

---

## Remaining Tasks

### Task 4: Visualize command (dev-server approach)

**Files:**
- Modify: `src/prosperity_cli/visualize.py`

**What it should do:**
1. Find the visualizer directory — look for it relative to a config key `visualizer_path`, or default to a path next to the package, or prompt user to configure it via `prosperity config`
2. Run `pnpm dev --port <port>` (or `npx vite --port <port>`) as a subprocess in that directory
3. Wait briefly then open browser at `http://localhost:<port>`
4. If `log_file` argument provided, print a message telling user to load it manually in the UI (auto-load React patch is deferred — not worth the complexity)
5. Block until Ctrl+C, then kill the subprocess

**Implementation sketch:**
```python
import subprocess, time, webbrowser, signal, typer
from pathlib import Path
from typing import Optional
from rich import print as rprint
from prosperity_cli.config import load as load_config, save as save_config

VISUALIZER_PATH_KEY = "visualizer_path"

def _find_visualizer() -> Optional[Path]:
    cfg = load_config()
    if p := cfg.get(VISUALIZER_PATH_KEY):
        return Path(p)
    # Try sibling directory
    candidates = [
        Path(__file__).parent.parent.parent.parent / "IMC_P4_Visualizer",
        Path.home() / "IMC_P4_Visualizer",
    ]
    for c in candidates:
        if (c / "package.json").exists():
            return c
    return None

def run(
    log_file: Optional[Path] = typer.Argument(None, help="Log file to load (shown as reminder)"),
    port: int = typer.Option(5173, "--port", "-p"),
):
    """Launch the visualizer in your browser."""
    vis_dir = _find_visualizer()
    if not vis_dir:
        rprint("[red]Error:[/red] Visualizer not found. Set its path with: prosperity config --visualizer-path /path/to/IMC_P4_Visualizer")
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
    )

    time.sleep(2)
    webbrowser.open(f"http://localhost:{port}")

    try:
        proc.wait()
    except KeyboardInterrupt:
        proc.terminate()
        rprint("\n[yellow]Visualizer stopped.[/yellow]")
```

**Also update `prosperity config`** to accept a `--visualizer-path` flag or add `visualizer_path` to the interactive prompts.

**Tests:**
```python
def test_visualize_missing_log_file():
    result = runner.invoke(app, ["visualize", "nonexistent.log"])
    assert result.exit_code != 0
    assert "not found" in result.output.lower()
```

**Commit:** `feat: add visualize command (pnpm dev launcher)`

---

### Task 5: ~~Visualizer auto-load React patch~~ SKIPPED

Replaced by: when `prosperity visualize result.log` is run, the CLI prints the resolved path and tells the user to drag-and-drop it. Simple and reliable.

---

### Task 6: Submit API discovery

**Goal:** Figure out the IMC Prosperity web API endpoints without Playwright.

**Credentials for testing:**
- Email: `rkothari40@gatech.edu`
- Password: `Internships_123$`
- URL: `https://prosperity.imc.com`

**Approach — inspect the Next.js JS bundle:**

```bash
# Find the JS chunk URLs
curl -s https://prosperity.imc.com/ | grep -oE '"/_next/static/[^"]+\.js"' | head -20

# Fetch a chunk and search for API strings
curl -s "https://prosperity.imc.com/_next/static/chunks/pages/index-<hash>.js" | \
  grep -oE '"/api/[^"]*"' | sort -u
```

**Try common auth patterns:**
```python
import requests

# Try these in order:
endpoints_to_try = [
    ("POST", "https://prosperity.imc.com/api/auth/login"),
    ("POST", "https://prosperity.imc.com/api/login"),
    ("POST", "https://prosperity.imc.com/api/user/login"),
    ("POST", "https://prosperity.imc.com/api/auth/signin"),
]

for method, url in endpoints_to_try:
    r = requests.post(url, json={"email": "rkothari40@gatech.edu", "password": "Internships_123$"})
    print(url, r.status_code, r.text[:200])
```

**Document findings in `docs/api-notes.md`:**
- Auth endpoint + request/response shape
- Submission endpoint + payload
- Status polling endpoint
- Log download endpoint

**Commit:** `docs: document IMC Prosperity API endpoints`

---

### Task 7: Submit command implementation

**Files:**
- Modify: `src/prosperity_cli/submit.py`
- Create: `tests/test_submit.py`

**Full flow:**
1. Load config, check credentials
2. Auth → get token (cache in config)
3. Upload `trader.py` → get submission ID
4. Poll status every 5s with `Rich Live` spinner showing elapsed time
5. Download result log → save to `backtests/<timestamp>-live.log`
6. Call `visualize.run(log_file=log_path)`

**Implementation:**
```python
import time, requests, typer
from datetime import datetime
from pathlib import Path
from typing import Optional
from rich.console import Console
from rich.live import Live
from rich.text import Text
from rich import print as rprint
from prosperity_cli.config import load as load_config, save as save_config

console = Console()

# Fill in after Task 6:
BASE_URL = "https://prosperity.imc.com"
AUTH_ENDPOINT = "/api/..."
SUBMIT_ENDPOINT = "/api/..."
STATUS_ENDPOINT = "/api/..."
LOG_ENDPOINT = "/api/..."

def _get_token(cfg):
    if cfg.get("token"):
        # TODO: check expiry
        return cfg["token"]
    r = requests.post(BASE_URL + AUTH_ENDPOINT,
        json={"email": cfg["email"], "password": cfg["password"]}, timeout=15)
    r.raise_for_status()
    token = r.json()["token"]  # key TBD from Task 6
    cfg["token"] = token
    save_config(cfg)
    return token

def _upload(token, algorithm: Path):
    r = requests.post(BASE_URL + SUBMIT_ENDPOINT,
        headers={"Authorization": f"Bearer {token}"},
        files={"algorithm": algorithm.read_bytes()}, timeout=30)
    r.raise_for_status()
    return r.json()["id"]  # key TBD

def _poll(token, submission_id):
    start = time.time()
    while True:
        r = requests.get(BASE_URL + STATUS_ENDPOINT + f"/{submission_id}",
            headers={"Authorization": f"Bearer {token}"}, timeout=15)
        r.raise_for_status()
        data = r.json()
        if data.get("status") == "complete":
            return data
        if data.get("status") == "failed":
            raise RuntimeError(f"Submission failed: {data}")
        elapsed = int(time.time() - start)
        yield elapsed
        time.sleep(5)

def run(
    algorithm: Path = typer.Argument(...),
    no_vis: bool = typer.Option(False, "--no-vis"),
    port: int = typer.Option(5173, "--port"),
):
    """Submit algorithm to IMC Prosperity, wait for results, open visualizer."""
    cfg = load_config()
    if not cfg.get("email") or not cfg.get("password"):
        rprint("[red]Error:[/red] No credentials. Run: prosperity config")
        raise typer.Exit(1)
    if not algorithm.exists():
        rprint(f"[red]Error:[/red] File not found: {algorithm}")
        raise typer.Exit(1)

    with console.status("[cyan]Authenticating...[/cyan]"):
        token = _get_token(cfg)
    rprint("[green]✓[/green] Authenticated")

    with console.status(f"[cyan]Submitting {algorithm.name}...[/cyan]"):
        submission_id = _upload(token, algorithm)
    rprint(f"[green]✓[/green] Submitted")

    with Live(console=console, refresh_per_second=4) as live:
        for elapsed in _poll(token, submission_id):
            live.update(Text(f"  Waiting for results...  {elapsed}s", style="yellow"))
    rprint("[green]✓[/green] Results ready!")

    ts = datetime.now().strftime("%Y-%m-%d-%H%M")
    log_path = Path("backtests") / f"{ts}-live.log"
    log_path.parent.mkdir(exist_ok=True)
    # download log — endpoint TBD from Task 6
    rprint(f"[green]✓[/green] Saved → {log_path}")

    if not no_vis:
        from prosperity_cli import visualize
        visualize.run(log_file=log_path, port=port)
```

**Tests:**
```python
def test_submit_no_config():
    with patch("prosperity_cli.config.load", return_value={}):
        result = runner.invoke(app, ["submit", "trader.py"])
    assert result.exit_code != 0
    assert "config" in result.output.lower()

def test_submit_missing_file():
    with patch("prosperity_cli.config.load", return_value={"email": "a@b.com", "password": "x"}):
        result = runner.invoke(app, ["submit", "nonexistent.py"])
    assert result.exit_code != 0
```

**Commit:** `feat: add submit command`

---

### Task 8: Countdown timer

**Files:**
- Create: `src/prosperity_cli/timer.py`
- Modify: `src/prosperity_cli/cli.py`

**`timer.py`:**
```python
from datetime import datetime
from typing import Optional
from rich.text import Text

def format_countdown(deadline_str: str) -> Optional[Text]:
    try:
        deadline = datetime.strptime(deadline_str, "%Y-%m-%d %H:%M")
    except ValueError:
        return None
    remaining = deadline - datetime.now()
    total = int(remaining.total_seconds())
    if total <= 0:
        return Text("Round ended", style="dim")
    d, rem = divmod(total, 86400)
    h, rem = divmod(rem, 3600)
    m, s = divmod(rem, 60)
    t = Text()
    t.append("  Round ends in  ", style="bold white")
    t.append(f"{d}d {h:02d}h {m:02d}m {s:02d}s", style="bold #FF6B2B")
    return t
```

**Wire into `cli.py`** via `@app.callback()`:
```python
@app.callback()
def _callback():
    cfg = load_config()
    if deadline := cfg.get("deadline"):
        from rich.console import Console
        from rich.panel import Panel
        text = format_countdown(deadline)
        if text:
            Console().print(Panel(text, border_style="#00B4B4", expand=False))
```

**Tests:**
```python
def test_future_deadline():
    future = (datetime.now() + timedelta(days=2, hours=3)).strftime("%Y-%m-%d %H:%M")
    assert format_countdown(future) is not None

def test_past_deadline():
    assert "ended" in format_countdown("2020-01-01 00:00").plain

def test_invalid_format():
    assert format_countdown("not-a-date") is None
```

**Commit:** `feat: add countdown timer`

---

### Task 9: README + PyPI prep

Write `README.md`:
- What it is (1 sentence)
- Prerequisites: Python 3.11+, pnpm + IMC_P4_Visualizer cloned, prosperity4btest installed
- `pip install prosperity-cli`
- `prosperity config` (note: credentials are personal, configure yourself)
- `prosperity backtest trader.py 1`
- `prosperity submit trader.py`
- `prosperity visualize result.log`
- Contributing section

**Commit:** `docs: add README`

---

## Color Palette

| Element | Color |
|---------|-------|
| Headers / success | `#00B4B4` (teal) |
| Countdown / warnings | `#FF6B2B` (orange-amber) |
| Panel borders | `#00B4B4` |
| Errors | `red` |
