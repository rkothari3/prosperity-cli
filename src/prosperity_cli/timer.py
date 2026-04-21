from datetime import datetime, timezone, timedelta
from rich.text import Text

CEST = timezone(timedelta(hours=2))

SCHEDULE = [
    ("Round 1",      datetime(2026, 4, 14, 12, 0, tzinfo=CEST), datetime(2026, 4, 17, 12, 0, tzinfo=CEST)),
    ("Round 2",      datetime(2026, 4, 17, 12, 0, tzinfo=CEST), datetime(2026, 4, 20, 12, 0, tzinfo=CEST)),
    ("Intermission", datetime(2026, 4, 20, 12, 0, tzinfo=CEST), datetime(2026, 4, 24, 12, 0, tzinfo=CEST)),
    ("Round 3",      datetime(2026, 4, 24, 12, 0, tzinfo=CEST), datetime(2026, 4, 26, 12, 0, tzinfo=CEST)),
    ("Round 4",      datetime(2026, 4, 26, 12, 0, tzinfo=CEST), datetime(2026, 4, 28, 12, 0, tzinfo=CEST)),
    ("Round 5",      datetime(2026, 4, 28, 12, 0, tzinfo=CEST), datetime(2026, 4, 30, 12, 0, tzinfo=CEST)),
]


def _format_remaining(label: str, end: datetime) -> Text | None:
    total = int((end - datetime.now(tz=CEST)).total_seconds())
    if total <= 0:
        return None
    d, rem = divmod(total, 86400)
    h, rem = divmod(rem, 3600)
    m, s = divmod(rem, 60)
    t = Text()
    t.append(f"  {label} ends in  ", style="bold white")
    t.append(f"{d}d {h:02d}h {m:02d}m {s:02d}s", style="bold #FF6B2B")
    return t


def get_current_countdown() -> Text | None:
    """Return countdown for the active round/intermission, or None if between competitions."""
    now = datetime.now(tz=CEST)
    for label, start, end in SCHEDULE:
        if start <= now < end:
            return _format_remaining(label, end)
    return None


def is_intermission() -> bool:
    """Return True if the current time falls within the Intermission window."""
    now = datetime.now(tz=CEST)
    for label, start, end in SCHEDULE:
        if label == "Intermission" and start <= now < end:
            return True
    return False


def intermission_end() -> datetime:
    """Return the end datetime of the Intermission period."""
    for label, _, end in SCHEDULE:
        if label == "Intermission":
            return end
    raise RuntimeError("No intermission in schedule")


def format_countdown(deadline_str: str) -> Text | None:
    """Fallback: format countdown from a manually configured deadline string (YYYY-MM-DD HH:MM)."""
    try:
        deadline = datetime.strptime(deadline_str, "%Y-%m-%d %H:%M").replace(tzinfo=CEST)
    except ValueError:
        return None
    return _format_remaining("Round", deadline)
