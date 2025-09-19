from __future__ import annotations

from pathlib import Path
from functools import lru_cache

_DEFAULT_PATH = Path("data/words.txt")


@lru_cache(maxsize=1)
def load_words(path: str | Path = _DEFAULT_PATH) -> set[str]:
    p = Path(path)
    if not p.exists():
        # fallback minimal list
        return {"YODEL", "HELLO", "WORLD"}
    with p.open("r", encoding="utf-8") as f:
        return {line.strip().upper() for line in f if line.strip()}


def is_valid(word: str) -> bool:
    return word.upper() in load_words()
