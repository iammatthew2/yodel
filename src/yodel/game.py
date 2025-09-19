from __future__ import annotations

from .dictionary import is_valid, load_words
from .scoring import score_guess


class Game:
    """Core game loop placeholder.

    Responsibilities (future):
      - Manage target word selection
      - Track guesses & scoring
      - Interact with hardware board abstraction
    """

    def __init__(self, target: str | None = None) -> None:
        load_words()  # warm cache
        self.target = (target or "YODEL").upper()
        self.guesses: list[tuple[str, int]] = []

    def apply_guess(self, guess: str) -> tuple[bool, str | int]:
        g = guess.strip().upper()
        if not is_valid(g):
            return False, "INVALID"
        score = score_guess(g, self.target)
        self.guesses.append((g, score))
        return True, score

    def start(self) -> None:
        print("Starting game (demo mode). Type guesses or blank to quit.")
        try:
            while True:
                raw = input("> ").strip()
                if not raw:
                    print("Bye.")
                    break
                ok, result = self.apply_guess(raw)
                if ok:
                    print(f"Score: {result}")
                    if raw.upper() == self.target:
                        print("You win!")
                        break
                else:
                    print("Invalid word")
        except KeyboardInterrupt:
            print("\nInterrupted.")
