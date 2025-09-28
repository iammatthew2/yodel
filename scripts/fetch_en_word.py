#!/usr/bin/env python3
"""Fetch English WordNet dataset archive only (no processing yet).

Usage:
    python scripts/fetch_en_word.py               # download dated copy if missing
    python scripts/fetch_en_word.py --force       # re-download even if exists
    python scripts/fetch_en_word.py --url <zip>   # custom URL

Output:
    data/raw/english-wordnet-2024_<DATE>.zip

All further parsing / extraction will be handled by a separate script later.
"""
from __future__ import annotations

import argparse
import hashlib
import zipfile
from datetime import datetime, UTC
from pathlib import Path
import sys
import urllib.request

RAW_DIR = Path("data/raw")
DEFAULT_URL = "https://en-word.net/static/english-wordnet-2024.zip"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def download(url: str) -> bytes:
    with urllib.request.urlopen(url) as resp:  # nosec: trusted source specified by user
        return resp.read()


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Fetch English WordNet archive")
    p.add_argument("--url", default=DEFAULT_URL, help="Archive URL (zip)")
    p.add_argument("--out-dir", default=str(RAW_DIR), help="Raw output directory")
    p.add_argument("--force", action="store_true", help="Re-download even if existing")
    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    raw_dir = Path(args.out_dir)
    raw_dir.mkdir(parents=True, exist_ok=True)
    date_tag = datetime.now(UTC).strftime("%Y%m%d")
    base_name = Path(args.url).name.replace('.zip', '')
    archive_path = raw_dir / f"{base_name}_{date_tag}.zip"

    if archive_path.exists() and not args.force:
        print(f"Archive exists: {archive_path} (use --force to re-download)", file=sys.stderr)
    else:
        print(f"Downloading {args.url} ...", file=sys.stderr)
        data = download(args.url)
        digest = sha256_bytes(data)[:16]
        archive_path.write_bytes(data)
        print(f"Saved {archive_path} (sha256 {digest}...)")

    # Extract (always) into sibling directory without .zip suffix
    extract_dir = archive_path.with_suffix("")
    if not extract_dir.exists():
        with zipfile.ZipFile(archive_path, 'r') as zf:
            zf.extractall(extract_dir)
        print(f"Extracted to {extract_dir}")
    else:
        print(f"Extraction directory exists: {extract_dir}")

    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
