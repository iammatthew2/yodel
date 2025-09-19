#!/usr/bin/env python3
"""Fetch en-word.net dataset (initial stub).

Planned:
- Download TSV/JSON export (URL TBD)
- Save to data/raw/en_word_YYYYMMDD.tsv (never overwrite existing)
"""
from __future__ import annotations

from datetime import datetime
from pathlib import Path
import sys

RAW_DIR = Path("data/raw")


def main() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    date_tag = datetime.utcnow().strftime("%Y%m%d")
    target = RAW_DIR / f"en_word_{date_tag}.tsv"
    if target.exists():
        print(f"Already exists: {target}", file=sys.stderr)
        return
    # TODO: perform real download; placeholder file
    target.write_text("word\tfrequency\nYODEL\t1000\n", encoding="utf-8")
    print(f"Wrote stub dataset to {target}")

if __name__ == "__main__":  # pragma: no cover
    main()
