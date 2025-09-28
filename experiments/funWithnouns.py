"""Experiment: map verbs to derivationally related noun lemmas via '+' pointers.

Uses the extracted English WordNet data under data/raw/english-wordnet-2024_*/oewn2024.
Outputs verbs having at least N related noun lemmas (default 3).
"""
from __future__ import annotations

from pathlib import Path
from collections import defaultdict
import argparse
import re

RAW_ROOT = Path("data/raw")
WN_PREFIX = "english-wordnet-2024_"
INNER = "oewn2024"

TOKEN_RE = re.compile(r"^[a-z][a-z_\-]*$")


def latest_wordnet_dir() -> Path:
    if not RAW_ROOT.exists():
        raise SystemExit("Run scripts/fetch_en_word.py first (data/raw missing)")
    candidates = []
    for p in RAW_ROOT.iterdir():
        if p.is_dir() and p.name.startswith(WN_PREFIX):
            parts = p.name.rsplit("_", 1)
            if len(parts) == 2 and parts[1].isdigit():
                candidates.append((parts[1], p))
    if not candidates:
        raise SystemExit("No english-wordnet-2024_* directories found under data/raw")
    return max(candidates, key=lambda t: t[0])[1] / INNER


def pick_rep(lemmas):
    """Pick a single display lemma per synset (simple heuristics)."""
    def score(w):
        brit = ("isation" in w) or w.endswith("ise")
        has_us = ("ization" in w) or w.endswith("ize")
        return (
            w.count("_"),
            1 if brit else 0,
            0 if has_us else 1,
            len(w),
            w.lower()
        )
    return sorted(lemmas, key=score)[0] if lemmas else None


def verb_noun_pairs_clean():
    base = latest_wordnet_dir()
    data_verb = base / "data.verb"
    data_noun = base / "data.noun"
    if not data_verb.exists() or not data_noun.exists():
        raise SystemExit("Expected data.verb and data.noun files in WordNet directory")

    verb_words, noun_words = {}, {}
    for pos, data_file, store in (("verb", data_verb, verb_words), ("noun", data_noun, noun_words)):
        with data_file.open(encoding="utf-8", errors="ignore") as f:
            for line in f:
                if not line or not line[0].isdigit():
                    continue
                head = line.split("|", 1)[0].split()
                if len(head) < 4:
                    continue
                off, p = head[0], head[2]
                if p[0] != pos[0]:
                    continue
                try:
                    w_cnt = int(head[3], 16)
                except ValueError:
                    continue
                store[off] = [head[j] for j in range(4, 4 + 2 * w_cnt, 2)]

    syn_pairs = set()
    with data_verb.open(encoding="utf-8", errors="ignore") as f:
        for line in f:
            if not line or not line[0].isdigit():
                continue
            head = line.split("|", 1)[0].split()
            if len(head) < 5:
                continue
            src_off = head[0]
            try:
                w_cnt = int(head[3], 16)
            except ValueError:
                continue
            i = 4 + 2 * w_cnt
            if i >= len(head):
                continue
            try:
                p_cnt = int(head[i])
            except ValueError:
                continue
            i += 1
            for _ in range(p_cnt):
                if i + 3 >= len(head):
                    break
                sym, tgt_off, tgt_pos, _st = head[i:i + 4]
                i += 4
                if sym == "+" and tgt_pos == "n":
                    syn_pairs.add((src_off, tgt_off))

    pairs = []
    for v_off, n_off in sorted(syn_pairs):
        v = pick_rep(verb_words.get(v_off, []))
        n = pick_rep(noun_words.get(n_off, []))
        if v and n and TOKEN_RE.match(v) and TOKEN_RE.match(n):
            pairs.append((v.replace('_', ' '), n.replace('_', ' ')))
    return pairs


def verb_to_nouns():
    mapping = defaultdict(set)
    for v, n in verb_noun_pairs_clean():
        mapping[v].add(n)
    return {v: sorted(ns) for v, ns in mapping.items()}


def verb_to_nouns_filtered(min_nouns=3):
    return {v: ns for v, ns in verb_to_nouns().items() if len(ns) >= min_nouns}


def main(argv=None):
    ap = argparse.ArgumentParser(description="List verbs with ≥N derivationally-related noun forms")
    ap.add_argument('-n', '--min-nouns', type=int, default=3, help='Minimum related noun lemmas (default 3)')
    ap.add_argument('--limit', type=int, help='Optional limit on number of verbs displayed')
    args = ap.parse_args(argv)

    filtered = verb_to_nouns_filtered(args.min_nouns)
    verbs = sorted(filtered.keys())
    if args.limit:
        verbs = verbs[:args.limit]
    print(f"verbs with >={args.min_nouns} noun matches: {len(filtered)}\n")
    for v in verbs:
        print(f"{v} -> {', '.join(filtered[v])}")


if __name__ == '__main__':  # pragma: no cover
    main()