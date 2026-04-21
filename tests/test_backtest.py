from unittest.mock import patch, MagicMock
from pathlib import Path
from typer.testing import CliRunner
from prosperity_cli.cli import app

runner = CliRunner()
PATCH = "prosperity_cli.backtest.subprocess.run"


def test_backtest_missing_file():
    result = runner.invoke(app, ["backtest", "nonexistent.py", "1"])
    assert result.exit_code != 0
    assert "not found" in result.output.lower()


def test_backtest_builds_correct_command(tmp_path):
    algo = tmp_path / "trader.py"
    algo.write_text("# trader")
    with patch(PATCH) as mock_run:
        mock_run.return_value = MagicMock(returncode=0)
        runner.invoke(app, ["backtest", str(algo), "1"])
    mock_run.assert_called_once()
    cmd = mock_run.call_args[0][0]
    assert cmd[0] == "imc-p4-bt"
    assert cmd[1] == str(algo)
    assert cmd[2] == "1"


def test_backtest_vis_opens_browser(tmp_path):
    algo = tmp_path / "trader.py"
    algo.write_text("# trader")
    with patch(PATCH) as mock_run:
        with patch("prosperity_cli.backtest.webbrowser.open") as mock_open:
            mock_run.return_value = MagicMock(returncode=0)
            runner.invoke(app, ["backtest", str(algo), "1", "--vis"])
    mock_open.assert_called_once()
    assert "imc-prosperity-4-visualizer.vercel.app" in mock_open.call_args[0][0]
    cmd = mock_run.call_args[0][0]
    assert "--vis" not in cmd
