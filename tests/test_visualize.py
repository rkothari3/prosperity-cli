from pathlib import Path
from unittest.mock import patch, MagicMock
from typer.testing import CliRunner
from prosperity_cli.cli import app

runner = CliRunner()


def test_visualize_missing_log_file():
    result = runner.invoke(app, ["visualize", "nonexistent.log"])
    assert result.exit_code != 0
    assert "not found" in result.output.lower()


def test_visualize_missing_visualizer_dir(tmp_path):
    with patch("prosperity_cli.visualize._find_visualizer", return_value=None):
        result = runner.invoke(app, ["visualize"])
    assert result.exit_code != 0
    assert "not found" in result.output.lower() or "config" in result.output.lower()


def test_visualize_port_option(tmp_path):
    vis_dir = tmp_path / "IMC_P4_Visualizer"
    vis_dir.mkdir()
    (vis_dir / "package.json").write_text("{}")

    with patch("prosperity_cli.visualize._find_visualizer", return_value=vis_dir):
        with patch("prosperity_cli.visualize.subprocess.Popen") as mock_popen:
            with patch("prosperity_cli.visualize.webbrowser.open"):
                mock_popen.return_value = MagicMock()
                result = runner.invoke(app, ["visualize", "--port", "3000"])
    assert result.exit_code == 0