from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache

from dotenv import load_dotenv

load_dotenv()


def _to_bool(value: str) -> bool:
    return value.strip().lower() in {"1", "true", "yes", "y", "on"}


@dataclass(frozen=True)
class Settings:
    browser: str
    headless: bool
    base_url: str
    timeout: int
    window_width: int
    window_height: int
    log_level: str


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings(
        browser=os.getenv("BROWSER", "chrome").lower(),
        headless=_to_bool(os.getenv("HEADLESS", "true")),
        base_url=os.getenv("BASE_URL", "https://example.com"),
        timeout=int(os.getenv("TIMEOUT", "10")),
        window_width=int(os.getenv("WINDOW_WIDTH", "1366")),
        window_height=int(os.getenv("WINDOW_HEIGHT", "768")),
        log_level=os.getenv("LOG_LEVEL", "INFO").upper(),
    )
