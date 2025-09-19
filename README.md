# Yodel

LED matrix word game (work in progress) leveraging the en-word.net lexicon and reusable hardware code from `phyllis_bot`.

## Features (Early Stage)
- Curated word list pipeline (`fetch_en_word.py`, `build_word_lists.py`).
- Simple terminal demo game loop (`yodel` CLI entry point).
- Hardware abstraction layer with fallback (mock or stdout if no matrix present).
- Scrolling matrix text display via `MatrixDisplay`.

## Project Layout
```
src/yodel/
	cli.py            # CLI entry (yodel)
	game.py           # Core loop (demo)
	dictionary.py     # Word loading/validation
	scoring.py        # Scoring logic
	config.py         # Settings dataclass
	display/          # MatrixDisplay abstraction
	hardware/         # Board interfaces + stubs
scripts/
	fetch_en_word.py  # Fetch raw dataset (stub)
	build_word_lists.py # Build processed word list (stub)
data/
	raw/              # Immutable raw dumps
	processed/        # Derived word lists
```

## Quick Start
Create a virtual environment and install in editable mode:
```
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
```

Run the demo game loop:
```
yodel
```

Scroll a message (hardware present) using Python REPL:
```python
from yodel.display import MatrixDisplay
d = MatrixDisplay()
d.scroll_once("HELLO WORLD")
```

Without hardware it prints a fallback line.

## Data Pipeline (Planned)
1. `python scripts/fetch_en_word.py` – download & cache dated raw file under `data/raw/`.
2. `python scripts/build_word_lists.py` – produce `data/processed/game_words.txt` + optional metadata.
3. Deterministic filtering (length, frequency, profanity) to ensure reproducibility.

## Environment Variables
| Variable | Purpose | Default |
|----------|---------|---------|
| YODEL_BRIGHTNESS | Text brightness scaling (0–100, internal 0–1 conversion optional later) | 40 (planned) |
| YODEL_SEED_SALT  | Salt for daily word deterministic selection | changeme |

## Hardware
Reuses matrix + font assets from `phyllis_bot`. Adapter implementation pending (`PhyllisBoard`). If `rgbmatrix` module is missing, display falls back to stdout.

## Development Notes
- Keep experimental scripts in `experiments/` (not yet added) and remove once logic is stabilized.
- Target Python 3.11+.

## License
TBD

