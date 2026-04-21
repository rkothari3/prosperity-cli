from pathlib import Path
from unittest.mock import patch
from typer.testing import CliRunner
from prosperity_cli.cli import app

runner = CliRunner()


def test_visualize_missing_log_file():
    result = runner.invoke(app, ["visualize", "nonexistent.log"])
    assert result.exit_code != 0
    assert "not found" in result.output.lower()


def test_visualize_opens_browser():
    with patch("prosperity_cli.visualize.webbrowser.open") as mock_open:
        result = runner.invoke(app, ["visualize"])
    assert result.exit_code == 0
    mock_open.assert_called_once()
    assert "imc-prosperity-4-visualizer.vercel.app" in mock_open.call_args[0][0]


def test_visualize_prints_log_path(tmp_path):
    log = tmp_path / "result.log"
    log.write_text("data")
    with patch("prosperity_cli.visualize.webbrowser.open"):
        result = runner.invoke(app, ["visualize", str(log)])
    assert result.exit_code == 0
    assert str(log.resolve()) in result.output
