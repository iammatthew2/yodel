"""CLI for yodel.

Subcommands:
  play          Run interactive demo game loop.
  scroll TEXT   Scroll a message on the matrix (or stdout fallback).
  diag          Show environment & resource diagnostics.
  update-words  Rebuild processed word list via build script.
"""
from __future__ import annotations

import argparse
import importlib
import os
import sys
import subprocess
from pathlib import Path
from typing import Callable

from .game import Game
from .dictionary import load_words
from .display import MatrixDisplay


def _cmd_play(_args: argparse.Namespace) -> int:
    game = Game()
    game.start()
    return 0


def _cmd_scroll(args: argparse.Namespace) -> int:
    disp = MatrixDisplay()
    disp.scroll_once(args.text)
    return 0


def _cmd_diag(_args: argparse.Namespace) -> int:
    info = {}
    # Python / platform
    info["python_version"] = sys.version.split()[0]
    # Words
    words = load_words()
    info["word_count"] = len(words)
    # Display availability
    disp = MatrixDisplay()
    info["display_available"] = disp.available()
    # rgbmatrix presence
    try:
        importlib.import_module("rgbmatrix")
        info["rgbmatrix"] = True
    except ImportError:
        info["rgbmatrix"] = False
    for k, v in info.items():
        print(f"{k}: {v}")
    return 0


def _cmd_update_words(_args: argparse.Namespace) -> int:
    script = Path("scripts/build_word_lists.py")
    if not script.exists():
        print("build_word_lists.py not found", file=sys.stderr)
        return 1
    # Run script in a subprocess with current interpreter
    result = subprocess.run([sys.executable, str(script)], capture_output=True, text=True)
    if result.returncode != 0:
        print(result.stdout)
        print(result.stderr, file=sys.stderr)
        return result.returncode
    print(result.stdout.strip())
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="yodel", description="Yodel LED word game utilities")
    sub = p.add_subparsers(dest="command", required=True)

    sp_play = sub.add_parser("play", help="Run demo game loop")
    sp_play.set_defaults(func=_cmd_play)

    sp_scroll = sub.add_parser("scroll", help="Scroll text once")
    sp_scroll.add_argument("text", help="Text to scroll")
    sp_scroll.set_defaults(func=_cmd_scroll)

    sp_diag = sub.add_parser("diag", help="Show diagnostics")
    sp_diag.set_defaults(func=_cmd_diag)

    sp_update = sub.add_parser("update-words", help="Rebuild processed word list")
    sp_update.set_defaults(func=_cmd_update_words)
    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    func: Callable[[argparse.Namespace], int] = getattr(args, "func")
    return func(args)


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
