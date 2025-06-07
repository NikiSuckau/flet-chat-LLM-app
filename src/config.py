import json
from pathlib import Path

CONFIG_FILE = Path(__file__).resolve().parent.parent / "config.json"
DEFAULT_CONFIG = {"api_url": "http://localhost:5001/v1/chat/completions"}


def load_config() -> dict:
    if CONFIG_FILE.exists():
        try:
            with CONFIG_FILE.open() as f:
                return json.load(f)
        except json.JSONDecodeError:
            pass
    return DEFAULT_CONFIG.copy()


def save_config(config: dict) -> None:
    with CONFIG_FILE.open("w") as f:
        json.dump(config, f, indent=2)
