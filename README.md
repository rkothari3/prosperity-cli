# prosperity-cli

Unified CLI for IMC Prosperity 4 trading competition: backtest, visualize, and submit algorithms.

## Prerequisites

- Python 3.11+

## Install

```bash
pip install prosperity-cli
```

This also installs `imc-p4-bt` (the backtester) as a dependency — no extra cloning needed.

Or for development:

```bash
cd prosperity-cli
pip install -e .
```

## Configure

Run the interactive setup to save your credentials:

```bash
prosperity config
```

Enter your IMC email and password when prompted.

**Note:** Credentials are stored in `~/.prosperity/config.json` with restricted permissions (600).

## Commands

### prosperity backtest

Run the backtester on your algorithm:

```bash
prosperity backtest trader.py 1
prosperity backtest trader.py 1 2 3 --vis --merge-pnl
```

Options:
- `algorithm` — Path to your trader.py file
- `rounds` — Round numbers to backtest (e.g. `1`, `1 2 3`, `1-0`)
- `--vis` — Open the visualizer after backtest
- `--merge-pnl` — Merge PnL across rounds
- `--print` — Print trader output to console
- `--out <file>` — Write output to file
- `--no-out` — Suppress output files

### prosperity visualize

Open the visualizer in your browser:

```bash
prosperity visualize
prosperity visualize result.log
```

Opens [https://imc-prosperity-4-visualizer.vercel.app/](https://imc-prosperity-4-visualizer.vercel.app/) — paste or load your log file there to analyze results.

Options:
- `log_file` — (Optional) Prints the log path as a reminder to load it in the UI

### prosperity submit

Submit your algorithm to IMC Prosperity, wait for results, and open visualizer:

```bash
prosperity submit trader.py
prosperity submit trader.py --no-vis
```

This command:
1. Authenticates with IMC Prosperity
2. Uploads your algorithm
3. Polls for results
4. Downloads the log file to `backtests/`
5. Opens the visualizer

### prosperity config

Configure your credentials:

```bash
prosperity config          # Interactive prompts
prosperity config --show  # Show config path
```

## Countdown Timer

`prosperity` shows a countdown panel on every command during active rounds or intermission:

```
╭───────────────────────────────────╮
│  Intermission ends in  2d 05h 12m 43s │
╰───────────────────────────────────╯
```

## Contributing

1. Fork the repo
2. Install in dev mode: `pip install -e .`
3. Run tests: `pytest tests/ -v`
4. Submit PR

## License

MIT
