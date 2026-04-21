import typer
from prosperity_cli import config as config_cmd
from prosperity_cli import backtest, visualize, submit

app = typer.Typer(
    name="prosperity",
    help="IMC Prosperity CLI — backtest, visualize, submit",
    no_args_is_help=True,
)

app.command("config")(config_cmd.run)
app.command("backtest")(backtest.run)
app.command("visualize")(visualize.run)
app.command("submit")(submit.run)

if __name__ == "__main__":
    app()
