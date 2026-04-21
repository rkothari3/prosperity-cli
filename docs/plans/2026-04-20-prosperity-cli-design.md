# prosperity-cli Design

## Overview

A single pip-installable Python CLI that unifies IMC Prosperity tooling:
backtesting, visualization, and submission — with a live countdown timer.

## Commands

```
prosperity backtest <trader.py> <round> [options]
prosperity visualize [log_file]
prosperity submit <trader.py>
prosperity config
```

## Architecture

**Package:** `prosperity-cli` on PyPI  
**Language:** Python  
**Dependencies:** `typer`, `rich`, `requests`, `prosperity4bt`  
**Config:** `~/.prosperity/config.json` (email, password, deadline)

### Visualizer bundling

The Vite build output (`dist/`) from IMC_P4_Visualizer is bundled inside the
Python package as static files. `prosperity visualize` serves them via Python's
built-in HTTP server on `localhost:8080`. No Node.js required at runtime.

A tiny local endpoint (or query param) pre-loads the log file when passed:
```
prosperity visualize backtests/result.log
→ http://localhost:8080?log=backtests/result.log
```

### Countdown timer

Shown as a persistent footer on every command using `Rich Live`:
```
┌─────────────────────────────────────────────┐
│  Round 2 ends in  2d 14h 32m 09s            │
└─────────────────────────────────────────────┘
```
Hidden if no deadline is configured. Set via `prosperity config`.

## Command Details

### `prosperity backtest <trader.py> <round> [options]`
- Thin wrapper around `prosperity4btest`
- All args passed through
- Rich progress display during execution
- Saves log to `backtests/<timestamp>.log`
- Optionally auto-opens visualizer on completion

### `prosperity visualize [log_file]`
- Serves bundled visualizer on `localhost:8080`
- Opens browser automatically
- If log_file passed, pre-loads it in the UI

### `prosperity submit <trader.py>`
1. Auth — POST login, cache token in config
2. Upload — POST trader.py to submission endpoint
3. Poll — GET status every 5s with Rich spinner + elapsed time
4. Download — save result to `backtests/<timestamp>-live.log`
5. Visualize — auto-launch visualizer with result log

Output:
```
  Submitting trader.py...       ✓
  Waiting for results...        ⠸  (42s elapsed)
  Results ready!                ✓
  Saved → backtests/2026-04-20-1400-live.log
  Opening visualizer at http://localhost:8080
```

### `prosperity config`
Interactive prompts for email, password, and optional deadline.
Credentials never hardcoded — users configure for themselves.

## Color Palette (from IMC Prosperity aesthetic)

- Teal `#00B4B4` — success states, headers, command names
- Orange-amber `#FF6B2B` — countdown timer, warnings
- Cream white `#F5F0E8` — body text
- Dark panel borders — Rich Panel outlines

## Install Story

```bash
pip install prosperity-cli
prosperity config
prosperity backtest trader.py 1
prosperity submit trader.py
```

## Platform Support

Windows and Linux. Rich and Typer both support both platforms.
HTTP server approach avoids any platform-specific subprocess issues with pnpm.
