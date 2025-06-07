from dataclasses import dataclass, asdict
import json
from typing import Any


@dataclass
class Settings:
    api_key: str = ""


class SettingsManager:
    """Load and save application settings."""

    def __init__(self, path: str = "settings.json") -> None:
        self.path = path

    def load(self) -> Settings:
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return Settings(**data)
        except FileNotFoundError:
            return Settings()
        except Exception:
            return Settings()

    def save(self, settings: Settings) -> None:
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(asdict(settings), f, indent=2)

