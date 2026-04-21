from unittest.mock import patch, MagicMock
from pathlib import Path
from typer.testing import CliRunner
from prosperity_cli.cli import app

runner = CliRunner()
LOAD = "prosperity_cli.submit.load_config"
NO_INTERMISSION = patch("prosperity_cli.submit.is_intermission", return_value=False)


def test_submit_intermission_block():
    """During intermission the command exits 0 with a friendly message."""
    result = runner.invoke(app, ["submit", "trader.py"])
    assert result.exit_code == 0
    assert "intermission" in result.output.lower()


def test_submit_no_credentials():
    with NO_INTERMISSION:
        with patch(LOAD, return_value={}):
            result = runner.invoke(app, ["submit", "trader.py"])
    assert result.exit_code != 0
    assert "config" in result.output.lower()


def test_submit_missing_file():
    with NO_INTERMISSION:
        with patch(LOAD, return_value={"email": "a@b.com", "password": "x"}):
            result = runner.invoke(app, ["submit", "nonexistent.py"])
    assert result.exit_code != 0
    assert "not found" in result.output.lower()


def test_submit_auth_failure(tmp_path):
    algo = tmp_path / "trader.py"
    algo.write_text("# trader")
    with NO_INTERMISSION:
        with patch(LOAD, return_value={"email": "a@b.com", "password": "x"}):
            with patch("prosperity_cli.submit._get_token", side_effect=Exception("bad credentials")):
                result = runner.invoke(app, ["submit", str(algo)])
    assert result.exit_code != 0
    assert "authentication failed" in result.output.lower()
