from dataclasses import dataclass, asdict
import json
import os


SETTINGS_FILE = "settings.json"


@dataclass
class AppSettings:
    """User configurable settings persisted between runs."""
    api_url: str = "http://localhost:5001/v1/chat/completions"


def load_settings(path: str = SETTINGS_FILE) -> AppSettings:
    """Load settings from JSON file, returning defaults if reading fails."""
    # Attempt to read user's settings. If anything goes wrong we simply
    # return an instance with default values to keep the app running.
    if os.path.isfile(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return AppSettings(**data)
        except Exception:
            pass
    return AppSettings()


def save_settings(settings: AppSettings, path: str = SETTINGS_FILE) -> None:
    """Persist settings to JSON file."""
    # Serialize the dataclass and store it on disk for next app launch.
    with open(path, "w", encoding="utf-8") as f:
        json.dump(asdict(settings), f, indent=2)
