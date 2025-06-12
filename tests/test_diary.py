import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1] / 'src'))

from backend import add_entry, load_entries, DiaryEntry


def test_add_and_load_entries(tmp_path):
    path = tmp_path / 'diary.json'
    entry = add_entry('hello', path)
    assert entry.text == 'hello'
    assert isinstance(entry.timestamp, str)

    entries = load_entries(path)
    assert isinstance(entries[-1], DiaryEntry)
    assert entries[-1].text == 'hello'
