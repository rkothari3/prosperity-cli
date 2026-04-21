from datetime import datetime
from typing import Optional
from rich.text import Text


def format_countdown(deadline_str: str) -> Optional[Text]:
    try:
        deadline = datetime.strptime(deadline_str, "%Y-%m-%d %H:%M")
    except ValueError:
        return None
    remaining = deadline - datetime.now()
    total = int(remaining.total_seconds())
    if total <= 0:
        return Text("Round ended", style="dim")
    d, rem = divmod(total, 86400)
    h, rem = divmod(rem, 3600)
    m, s = divmod(rem, 60)
    t = Text()
    t.append("  Round ends in  ", style="bold white")
    t.append(f"{d}d {h:02d}h {m:02d}m {s:02d}s", style="bold #FF6B2B")
    return t