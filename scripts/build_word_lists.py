#!/usr/bin/env python3
"""Build curated game word lists from raw en-word data (stub).

Future steps:
- Load latest raw file(s)
- Apply filters (length, frequency, profanity blacklist, ASCII only)
- Output data/processed/game_words.txt and optional metadata parquet/JSON
- Produce SHA256 checksums
"""
from __future__ import annotations

from pathlib import Path

RAW_DIR = Path("data/raw")
PROC_DIR = Path("data/processed")


def main() -> None:
    PROC_DIR.mkdir(parents=True, exist_ok=True)
    out_words = PROC_DIR / "game_words.txt"
    # Placeholder content until filters implemented
    out_words.write_text("YODEL\nHELLO\nWORLD\n", encoding="utf-8")
    print(f"Wrote placeholder word list: {out_words}")

if __name__ == "__main__":  # pragma: no cover
    main()
