from __future__ import annotations

from pathlib import Path
from functools import lru_cache
import os
import re
from datetime import datetime

_DEFAULT_PATH = Path("data/words.txt")  # Optional curated list (preferred once generated)
_RAW_ROOT = Path("data/raw")

WORD_RE = re.compile(r"^[A-Za-z]{3,}$")  # basic token filter; adjust later


def _latest_wordnet_dir() -> Path | None:
    """Return newest extracted english-wordnet directory (based on date suffix)."""
    if not _RAW_ROOT.exists():
        return None
    candidates = []
    for p in _RAW_ROOT.iterdir():
        if p.is_dir() and p.name.startswith("english-wordnet-2024_"):
            # extract date portion after last underscore if numeric
            parts = p.name.rsplit("_", 1)
            if len(parts) == 2 and parts[1].isdigit():
                candidates.append((parts[1], p))
    if not candidates:
        return None
    # pick max date string (YYYYMMDD lexical works)
    return max(candidates, key=lambda t: t[0])[1]


def _load_from_wordnet_dir(d: Path) -> set[str]:
    words: set[str] = set()
    # Common index files
    for fname in ["index.noun", "index.verb", "index.adj", "index.adv"]:
        fpath = next(d.rglob(fname), None)
        if not fpath or not fpath.is_file():
            continue
        try:
            with fpath.open("r", encoding="utf-8", errors="ignore") as fh:
                for line in fh:
                    if not line or line.startswith(" ") or line.startswith("#"):
                        continue
                    token = line.split()[0]
                    if WORD_RE.match(token):
                        words.add(token.upper())
        except Exception:
            continue
    return words


@lru_cache(maxsize=1)
def load_words(path: str | Path = _DEFAULT_PATH) -> set[str]:
    # 1. If explicit YODEL_WORDS_PATH provided, use it.
    env_path = os.getenv("YODEL_WORDS_PATH")
    if env_path:
        p = Path(env_path)
        if p.is_file():
            with p.open("r", encoding="utf-8") as f:
                return {line.strip().upper() for line in f if line.strip()}

    # 2. If curated file exists at default, use it.
    p = Path(path)
    if p.is_file():
        with p.open("r", encoding="utf-8") as f:
            return {line.strip().upper() for line in f if line.strip()}

    # 3. Fallback: derive from latest extracted WordNet directory.
    wn_dir = _latest_wordnet_dir()
    if wn_dir:
        wn_words = _load_from_wordnet_dir(wn_dir)
        if wn_words:
            return wn_words

    # 4. Final minimal fallback.
    return {"YODEL", "HELLO", "WORLD"}


def is_valid(word: str) -> bool:
    return word.upper() in load_words()
