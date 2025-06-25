from dataclasses import asdict, dataclass
import json
import os

from .backend import ChatBackend


STORAGE_DIR = "storage"
SETTINGS_FILE = os.path.join(STORAGE_DIR, "settings.json")


@dataclass
class AppSettings:
    """User configurable settings persisted between runs."""
    api_url: str = "http://localhost:5001/v1/chat/completions"
    system_prompt: str = ChatBackend.DEFAULT_SYSTEM_PROMPT
    temperature: float = 0.8
    max_tokens: int = 200
    diary_system_prompt: str = ChatBackend.DEFAULT_SYSTEM_PROMPT
    diary_prompt: str = ChatBackend.DEFAULT_DIARY_PROMPT
    diary_temperature: float = 0.7
    diary_max_tokens: int = 50
    summary_system_prompt: str = ChatBackend.DEFAULT_SYSTEM_PROMPT
    summary_prompt: str = ChatBackend.DEFAULT_SUMMARY_PROMPT
    summary_temperature: float = 0.7
    summary_max_tokens: int = 50
    user_name: str = "User"
    avatar_color: str = "blue"


def load_settings(path: str = SETTINGS_FILE) -> AppSettings:
    """Load settings from JSON file, returning defaults if reading fails."""
    # Attempt to read user's settings. If anything goes wrong we simply
    # return an instance with default values to keep the app running.
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if os.path.isfile(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            defaults = asdict(AppSettings())
            defaults.update(data)
            return AppSettings(**defaults)
        except Exception:
            pass
    return AppSettings()


def save_settings(settings: AppSettings, path: str = SETTINGS_FILE) -> None:
    """Persist settings to JSON file."""
    # Serialize the dataclass and store it on disk for next app launch.
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(asdict(settings), f, indent=2)
