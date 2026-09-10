from __future__ import annotations

import json
from pathlib import Path


def _score_path() -> Path:
    base = Path.home() / ".local" / "share" / "snake-game"
    base.mkdir(parents=True, exist_ok=True)
    return base / "highscore.json"


def load_high_score() -> int:
    path = _score_path()
    if not path.exists():
        return 0
    try:
        data = json.loads(path.read_text())
        return int(data.get("high_score", 0))
    except (json.JSONDecodeError, ValueError, OSError):
        return 0


def save_high_score(score: int) -> None:
    path = _score_path()
    try:
        path.write_text(json.dumps({"high_score": score}))
    except OSError:
        pass
