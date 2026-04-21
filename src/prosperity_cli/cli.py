import typer
from prosperity_cli import config as config_cmd
from prosperity_cli import backtest, visualize, submit
from prosperity_cli.config import load as load_config
from prosperity_cli.timer import format_countdown
from rich.console import Console
from rich.panel import Panel

app = typer.Typer(
    name="prosperity",
    help="IMC Prosperity CLI — backtest, visualize, submit",
    no_args_is_help=True,
)


@app.callback()
def _callback():
    cfg = load_config()
    if deadline := cfg.get("deadline"):
        text = format_countdown(deadline)
        if text:
            Console().print(Panel(text, border_style="#00B4B4", expand=False))


app.command("config")(config_cmd.run)
app.command("backtest")(backtest.run)
app.command("visualize")(visualize.run)
app.command("submit")(submit.run)

if __name__ == "__main__":
    app()
