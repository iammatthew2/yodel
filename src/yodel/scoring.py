from __future__ import annotations

def score_guess(guess: str, target: str) -> int:
    """Naive scoring: +1 for each correct position letter.
    Length mismatch is tolerated by zipping shortest.
    """
    guess_u = guess.upper()
    target_u = target.upper()
    return sum(g == t for g, t in zip(guess_u, target_u))
