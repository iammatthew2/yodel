from __future__ import annotations

from dataclasses import dataclass
import os


@dataclass(frozen=True)
class Settings:
    brightness: int = int(os.getenv("YODEL_BRIGHTNESS", "40"))
    daily_seed_salt: str = os.getenv("YODEL_SEED_SALT", "changeme")


def load_settings() -> Settings:
    return Settings()
