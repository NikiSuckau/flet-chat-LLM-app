from dataclasses import dataclass, asdict
from datetime import datetime
import json
import os

DIARY_DIR = "storage"
DIARY_FILE = os.path.join(DIARY_DIR, "diary_entries.json")


@dataclass
class DiaryEntry:
    """Simple diary entry data structure."""
    text: str
    timestamp: str


def load_entries(path: str = DIARY_FILE) -> list[DiaryEntry]:
    """Load all diary entries from JSON file."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if os.path.isfile(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return [DiaryEntry(**d) for d in data]
        except Exception:
            pass
    return []


def add_entry(text: str, path: str = DIARY_FILE) -> DiaryEntry:
    """Append a new diary entry and persist it."""
    entries = load_entries(path)
    entry = DiaryEntry(text=text, timestamp=datetime.now().isoformat(timespec="seconds"))
    entries.append(entry)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump([asdict(e) for e in entries], f, indent=2)
    return entry
