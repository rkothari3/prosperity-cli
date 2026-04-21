from datetime import datetime, timedelta
from prosperity_cli.timer import format_countdown


def test_future_deadline():
    future = (datetime.now() + timedelta(days=2, hours=3)).strftime("%Y-%m-%d %H:%M")
    result = format_countdown(future)
    assert result is not None
    assert "d" in result.plain


def test_past_deadline():
    result = format_countdown("2020-01-01 00:00")
    assert "ended" in result.plain


def test_invalid_format():
    result = format_countdown("not-a-date")
    assert result is None