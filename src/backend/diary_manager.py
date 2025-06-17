from dataclasses import dataclass
from datetime import datetime
import os
import sqlite3

DIARY_DIR = "storage"
DIARY_DB = os.path.join(DIARY_DIR, "diary.db")


@dataclass
class DiaryEntry:
    """Simple diary entry data structure."""
    text: str
    timestamp: str

def _ensure_table(conn: sqlite3.Connection) -> None:
    conn.execute(
        """CREATE TABLE IF NOT EXISTS entries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT NOT NULL,
        timestamp TEXT NOT NULL
    )"""
    )


def load_entries(path: str = DIARY_DB) -> list[DiaryEntry]:
    """Load all diary entries from the SQLite database."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    conn = sqlite3.connect(path)
    _ensure_table(conn)
    rows = conn.execute("SELECT text, timestamp FROM entries ORDER BY id").fetchall()
    conn.close()
    return [DiaryEntry(text=row[0], timestamp=row[1]) for row in rows]


def add_entry(text: str, path: str = DIARY_DB) -> DiaryEntry:
    """Append a new diary entry and persist it in SQLite."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    conn = sqlite3.connect(path)
    _ensure_table(conn)
    timestamp = datetime.now().isoformat(timespec="seconds")
    conn.execute("INSERT INTO entries (text, timestamp) VALUES (?, ?)", (text, timestamp))
    conn.commit()
    conn.close()
    return DiaryEntry(text=text, timestamp=timestamp)
