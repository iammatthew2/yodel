"""Basic structural scan of English WordNet data files.

Reads data.{noun,verb,adj,adv} inside the latest extracted english-wordnet-2024_* directory
under data/raw and reports:
- synset counts per POS
- total lemma tokens per POS
- pointer symbol frequency (aggregate across POS)
- top pointer symbols by count
- average lemmas per synset per POS

This is intentionally lightweight and avoids external deps.
"""
from __future__ import annotations

from pathlib import Path
from collections import Counter
import argparse
import sys
from io import StringIO

RAW_ROOT = Path("data/raw")
PREFIX = "english-wordnet-2024_"
INNER = "oewn2024"


def latest_wordnet_dir() -> Path:
    if not RAW_ROOT.exists():
        raise SystemExit("data/raw does not exist. Run scripts/fetch_en_word.py first.")
    candidates = []
    for p in RAW_ROOT.iterdir():
        if p.is_dir() and p.name.startswith(PREFIX):
            parts = p.name.rsplit("_", 1)
            if len(parts) == 2 and parts[1].isdigit():
                candidates.append((parts[1], p))
    if not candidates:
        raise SystemExit("No english-wordnet-2024_* directories found.")
    return max(candidates, key=lambda t: t[0])[1] / INNER


def parse_data_file(path: Path):
    synset_count = 0
    lemma_tokens = 0
    pointer_counter = Counter()
    with path.open(encoding="utf-8", errors="ignore") as f:
        for line in f:
            if not line or not line[0].isdigit():
                continue
            # split before gloss
            pre, *_ = line.split("|", 1)
            parts = pre.split()
            if len(parts) < 4:
                continue
            synset_count += 1
            w_cnt_hex = parts[3]
            try:
                w_cnt = int(w_cnt_hex, 16)
            except ValueError:
                continue
            # lemmas start at index 4, alternating lemma lex_id
            lemma_tokens += w_cnt
            after_lemmas = 4 + 2 * w_cnt
            if after_lemmas >= len(parts):
                continue
            try:
                p_cnt = int(parts[after_lemmas])
            except ValueError:
                p_cnt = 0
            i = after_lemmas + 1
            for _ in range(p_cnt):
                if i + 3 >= len(parts):
                    break
                symbol = parts[i]
                pointer_counter[symbol] += 1
                i += 4  # symbol target_offset target_pos source/target
    return synset_count, lemma_tokens, pointer_counter


def main(argv=None):
    parser = argparse.ArgumentParser(description="Inspect basic WordNet data file structure.")
    parser.add_argument("--top", type=int, default=10, help="Show top N pointer symbols (default 10)")
    parser.add_argument("--out", type=Path, help="Optional path to write summary text.")
    args = parser.parse_args(argv)

    buf = StringIO()
    def w(line=""):
        buf.write(line + "\n")
        print(line)

    base = latest_wordnet_dir()
    pos_files = {pos: base / f"data.{pos}" for pos in ("noun", "verb", "adj", "adv")}

    all_pointer_counts = Counter()
    results = {}
    for pos, path in pos_files.items():
        if not path.exists():
            w(f"[warn] missing {path}")
            continue
        syn_ct, lem_ct, ptrs = parse_data_file(path)
        results[pos] = (syn_ct, lem_ct, ptrs)
        all_pointer_counts.update(ptrs)

    w("=== WordNet Basic Structure Summary ===")
    for pos, (syn_ct, lem_ct, ptrs) in results.items():
        avg_lem = lem_ct / syn_ct if syn_ct else 0
        w(f"POS {pos:4} | synsets: {syn_ct:6} | lemma_tokens: {lem_ct:6} | avg_lemmas_per_synset: {avg_lem:4.2f}")
    w()
    w(f"Total distinct pointer symbols: {len(all_pointer_counts)}")
    top_n = all_pointer_counts.most_common(args.top)
    if top_n:
        w(f"Top {len(top_n)} pointer symbols:")
        for sym, cnt in top_n:
            w(f"  {sym:3} {cnt}")
    else:
        w("No pointer symbols parsed.")

    w("\nPer-POS pointer symbol top 5:")
    for pos, (syn_ct, lem_ct, ptrs) in results.items():
        w(f"  {pos}:")
        for sym, cnt in ptrs.most_common(5):
            w(f"    {sym:3} {cnt}")

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(buf.getvalue(), encoding="utf-8")
        print(f"\n[written] {args.out}")


if __name__ == "__main__":  # pragma: no cover (experiment script)
    main()
