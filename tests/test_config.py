import json
from pathlib import Path
from unittest.mock import patch
from prosperity_cli.config import load, save, CONFIG_PATH


def test_save_and_load(tmp_path):
    test_path = tmp_path / "config.json"
    with patch("prosperity_cli.config.CONFIG_PATH", test_path):
        save({"email": "a@b.com", "password": "secret"})
        data = load()
    assert data["email"] == "a@b.com"
    assert data["password"] == "secret"


def test_load_missing_returns_empty(tmp_path):
    test_path = tmp_path / "nonexistent.json"
    with patch("prosperity_cli.config.CONFIG_PATH", test_path):
        assert load() == {}
