# prosperity-cli

Unified CLI for IMC Prosperity 4 trading competition: backtest, visualize, and submit algorithms.

## Prerequisites

- Python 3.11+
- [prosperity4btest](https://github.com/your-backtester-repo) installed (`pip install -e IMC_P4_Backtester/`)
- [IMC_P4_Visualizer](https://github.com/your-visualizer-repo) cloned
- Node.js + pnpm (for visualizer)

## Install

```bash
pip install prosperity-cli
```

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

Enter your IMC email, password, round deadline, and visualizer path when prompted.

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
- `rounds` — Round numbers to backtest
- `--vis` — Show visualization
- `--merge-pnl` — Merge PnL across rounds
- `--print` — Print output to console
- `--out <file>` — Write output to file
- `--no-out` — Suppress output files

### prosperity visualize

Launch the visualizer in your browser:

```bash
prosperity visualize
prosperity visualize result.log
prosperity visualize --port 3000
```

Options:
- `log_file` — Log file to load (shown as reminder to drag-and-drop)
- `--port, -p` — Port to run on (default: 5173)

### prosperity submit

Submit your algorithm to IMC Prosperity, wait for results, and open visualizer:

```bash
prosperity submit trader.py
prosperity submit trader.py --no-vis --port 3000
```

This command:
1. Authenticates with IMC Prosperity
2. Uploads your algorithm
3. Polls for results
4. Downloads the log file
5. Opens the visualizer

**Note:** Endpoint discovery in progress — may need manual API capture.

### prosperity config

Configure your credentials and settings:

```bash
prosperity config          # Interactive prompts
prosperity config --show  # Show config path
```

## Countdown Timer

If a deadline is configured, `prosperity` shows a countdown panel on each command:

```
╭───────────────────────────────╮
│  Round ends in  2d 05h 12m 43s │
╰───────────────────────────────╯
```

## Contributing

1. Fork the repo
2. Install in dev mode: `pip install -e .`
3. Run tests: `pytest tests/ -v`
4. Submit PR

## License

MIT