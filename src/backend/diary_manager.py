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
    id: int | None = None

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
    rows = conn.execute(
        "SELECT id, text, timestamp FROM entries ORDER BY id"
    ).fetchall()
    conn.close()
    return [DiaryEntry(text=row[1], timestamp=row[2], id=row[0]) for row in rows]


def add_entry(text: str, path: str = DIARY_DB) -> DiaryEntry:
    """Append a new diary entry and persist it in SQLite."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    conn = sqlite3.connect(path)
    _ensure_table(conn)
    timestamp = datetime.now().isoformat(timespec="seconds")
    cursor = conn.execute(
        "INSERT INTO entries (text, timestamp) VALUES (?, ?)", (text, timestamp)
    )
    conn.commit()
    entry_id = cursor.lastrowid
    conn.close()
    return DiaryEntry(text=text, timestamp=timestamp, id=entry_id)


def update_entry(entry_id: int, text: str, path: str = DIARY_DB) -> DiaryEntry:
    """Update the text of an existing entry while keeping the timestamp."""

    conn = sqlite3.connect(path)
    _ensure_table(conn)
    conn.execute("UPDATE entries SET text=? WHERE id=?", (text, entry_id))
    conn.commit()
    row = conn.execute(
        "SELECT id, text, timestamp FROM entries WHERE id=?", (entry_id,)
    ).fetchone()
    conn.close()
    return DiaryEntry(text=row[1], timestamp=row[2], id=row[0])
