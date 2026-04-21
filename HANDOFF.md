# prosperity-cli — Handoff for New Session

## What This Project Is

`prosperity-cli` is a pip-installable Python CLI that unifies IMC Prosperity 4 trading competition tooling into one tool. Currently players need two separate repos; this wraps both plus adds submission.

**Four commands:**
```
prosperity config    — set email, password, round deadline
prosperity backtest  — run backtester (wraps prosperity4btest)
prosperity visualize — launch the visualizer (pnpm dev)
prosperity submit    — upload trader.py, wait for results, open visualizer
```

## Repo Structure

```
/mnt/c/Users/rajg6/OneDrive/Desktop/IMC_P4/Round_2/prosperity-cli/
├── pyproject.toml                          # hatchling, typer+rich+requests deps
├── src/prosperity_cli/
│   ├── __init__.py                         # __version__ = "0.1.0"
│   ├── cli.py                              # Typer app, 4 commands wired
│   ├── config.py                           # DONE — full implementation
│   ├── backtest.py                         # DONE — full implementation
│   ├── visualize.py                        # STUB — needs Task 4
│   └── submit.py                           # STUB — needs Tasks 6+7
├── tests/
│   ├── test_config.py                      # 3 tests passing
│   └── test_backtest.py                    # 3 tests passing
└── docs/plans/2026-04-20-implementation-plan.md   # full plan with remaining tasks
```

**Related repos (NOT this repo):**
- `/mnt/c/Users/rajg6/OneDrive/Desktop/IMC_P4/IMC_P4_Backtester` — prosperity4btest CLI
- `/mnt/c/Users/rajg6/OneDrive/Desktop/IMC_P4/IMC_P4_Visualizer` — React/Vite visualizer

## Package Setup

Already installed in dev mode. To reinstall:
```bash
cd /mnt/c/Users/rajg6/OneDrive/Desktop/IMC_P4/Round_2/prosperity-cli
pip install -e .
prosperity --help   # should show all 4 commands
pytest tests/ -v    # 6 tests should pass
```

## What's Done

### Task 1 ✅ — Package scaffold
`pyproject.toml`, all 4 stub modules, `prosperity --help` works.

### Task 2 ✅ — Config command (`src/prosperity_cli/config.py`)
- `load()` / `save()` — reads/writes `~/.prosperity/config.json`
- `save()` calls `chmod(0o600)` — credentials not world-readable
- `run()` — interactive prompts: email, password (masked, doesn't echo existing), deadline (validated YYYY-MM-DD HH:MM)
- Empty email/password raises error with message
- `JSONDecodeError` handled gracefully in `load()`
- Tests: save/load round-trip, missing file returns {}, file permissions 0o600

### Task 3 ✅ — Backtest command (`src/prosperity_cli/backtest.py`)
- Validates file exists, builds `["prosperity4btest", str(algo)] + rounds + flags`
- Flags: `--vis`, `--merge-pnl`, `--print` (as `print_output` internally), `--out`, `--no-out`
- Propagates subprocess exit code via `typer.Exit(result.returncode)`
- Tests use `patch("prosperity_cli.backtest.subprocess.run")` (correct patch target)

## What's Left

See `docs/plans/2026-04-20-implementation-plan.md` for full task specs with code.

### Task 4 — Visualize command
Launch `pnpm dev --port <port>` as subprocess in the IMC_P4_Visualizer directory. Find visualizer dir via config key `visualizer_path` or sibling directory heuristic. If `log_file` passed, just print the resolved path as a reminder to load it manually. Open browser after 2s delay. Block until Ctrl+C.

Also add `visualizer_path` to `prosperity config` prompts.

### Task 5 — SKIPPED
Originally planned React auto-load patch. Replaced by "print path, user loads manually" approach.

### Task 6 — Submit API discovery
Reverse-engineer IMC Prosperity web API (no Playwright).
- Credentials: email `rkothari40@gatech.edu`, password `Internships_123$`
- URL: `https://prosperity.imc.com`
- Approach: inspect Next.js JS bundles for `/api/` strings, try common auth endpoint patterns
- Document in `docs/api-notes.md`

### Task 7 — Submit command
Full flow: auth → upload trader.py → poll with Rich Live spinner → download log → open visualizer.
Endpoint constants are placeholders until Task 6 fills them in.

### Task 8 — Countdown timer
`timer.py` with `format_countdown()`. Wire into `cli.py` via `@app.callback()`. Shows orange `#FF6B2B` countdown panel if deadline is configured. Tests for future/past/invalid.

### Task 9 — README
Prerequisites, install, all 4 commands, credentials note.

## Key Decisions

1. **Visualizer: dev-server approach** — `pnpm dev`, not bundled static files. WSL struggles with the Vite build but it works fine on Windows PowerShell. Simpler to implement.
2. **`prosperity4bt` not a pip dep** — it's not on PyPI. Users install the backtester repo separately (`pip install -e IMC_P4_Backtester/`). The backtest command just shells out to `prosperity4btest`.
3. **Typer command names explicit** — `app.command("config")(func)` not `app.command()(func)` — all stubs are named `run` so Typer needs explicit names.
4. **Subprocess mock target** — `patch("prosperity_cli.backtest.subprocess.run")` not `patch("subprocess.run")`.

## Color Palette (from IMC aesthetic)
- Teal `#00B4B4` — success, headers, panel borders
- Orange `#FF6B2B` — countdown timer, warnings
- Errors: `red`

## How to Continue

Use `superpowers:subagent-driven-development` skill. The plan is at:
`docs/plans/2026-04-20-implementation-plan.md`

Start with Task 4. Each remaining task has full implementation code in the plan.

For Task 6 (API discovery), run the requests-based probing in a Python script — no Playwright. If endpoints can't be found automatically, ask the user to open DevTools Network tab and capture a submission.
