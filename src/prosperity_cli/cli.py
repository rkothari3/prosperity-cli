import typer
from prosperity_cli import config as config_cmd
from prosperity_cli import backtest, visualize, submit
from prosperity_cli import __version__
from prosperity_cli.config import load as load_config
from prosperity_cli.timer import get_current_countdown, format_countdown
from rich.console import Console
from rich.panel import Panel

app = typer.Typer(
    name="prosperity",
    help="IMC Prosperity CLI — backtest, visualize, submit",
    no_args_is_help=True,
)


def _show_countdown():
    text = get_current_countdown()
    if text is None:
        cfg = load_config()
        if deadline := cfg.get("deadline"):
            text = format_countdown(deadline)
    if text:
        Console().print(Panel(text, border_style="#00B4B4", expand=False))


@app.callback(invoke_without_command=True)
def _callback(
    ctx: typer.Context,
    version: bool = typer.Option(False, "--version", "-V", is_eager=True, help="Show version and exit"),
):
    if version:
        Console().print(f"prosperity-cli {__version__}")
        raise typer.Exit()
    _show_countdown()


app.command("config")(config_cmd.run)
app.command("backtest")(backtest.run)
app.command("visualize")(visualize.run)
app.command("submit")(submit.run)

if __name__ == "__main__":
    app()
