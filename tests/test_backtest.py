from unittest.mock import patch, MagicMock
from pathlib import Path
from typer.testing import CliRunner
from prosperity_cli.cli import app

runner = CliRunner()


def test_backtest_missing_file():
    result = runner.invoke(app, ["backtest", "nonexistent.py", "1"])
    assert result.exit_code != 0
    assert "not found" in result.output.lower()


def test_backtest_builds_correct_command(tmp_path):
    algo = tmp_path / "trader.py"
    algo.write_text("# trader")
    with patch("subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(returncode=0)
        result = runner.invoke(app, ["backtest", str(algo), "1"])
    mock_run.assert_called_once()
    cmd = mock_run.call_args[0][0]
    assert "prosperity4btest" in cmd
    assert "1" in cmd


def test_backtest_passes_vis_flag(tmp_path):
    algo = tmp_path / "trader.py"
    algo.write_text("# trader")
    with patch("subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(returncode=0)
        runner.invoke(app, ["backtest", str(algo), "1", "--vis"])
    cmd = mock_run.call_args[0][0]
    assert "--vis" in cmd
