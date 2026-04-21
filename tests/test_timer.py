from datetime import datetime, timedelta, timezone
from unittest.mock import patch
from prosperity_cli.timer import format_countdown, get_current_countdown, CEST, SCHEDULE


def test_format_countdown_future():
    future = (datetime.now(tz=CEST) + timedelta(days=2, hours=3)).strftime("%Y-%m-%d %H:%M")
    result = format_countdown(future)
    assert result is not None
    assert "d" in result.plain


def test_format_countdown_past():
    result = format_countdown("2020-01-01 00:00")
    assert result is None


def test_format_countdown_invalid():
    assert format_countdown("not-a-date") is None


def test_get_current_countdown_during_active_phase():
    _, start, end = SCHEDULE[0]
    mid = start + (end - start) / 2
    with patch("prosperity_cli.timer.datetime") as mock_dt:
        mock_dt.now.return_value = mid
        result = get_current_countdown()
    assert result is not None
    assert "Round 1" in result.plain


def test_get_current_countdown_outside_schedule():
    past = datetime(2025, 1, 1, tzinfo=CEST)
    with patch("prosperity_cli.timer.datetime") as mock_dt:
        mock_dt.now.return_value = past
        result = get_current_countdown()
    assert result is None
