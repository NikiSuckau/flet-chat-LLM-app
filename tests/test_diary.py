import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1] / 'src'))

from backend import add_entry, delete_entry, load_entries, update_entry, DiaryEntry


def test_add_and_load_entries(tmp_path):
    path = tmp_path / 'diary.db'
    entry = add_entry('hello', path)
    assert entry.text == 'hello'
    assert isinstance(entry.timestamp, str)

    entries = load_entries(path)
    assert isinstance(entries[-1], DiaryEntry)
    assert entries[-1].text == 'hello'


def test_update_entry(tmp_path):
    path = tmp_path / 'diary.db'
    entry = add_entry('old text', path)
    updated = update_entry(entry.id, 'new text', path)
    assert updated.id == entry.id
    assert updated.timestamp == entry.timestamp
    assert updated.text == 'new text'
    entries = load_entries(path)
    assert entries[0].text == 'new text'


def test_delete_entry(tmp_path):
    path = tmp_path / 'diary.db'
    entry1 = add_entry('to delete', path)
    entry2 = add_entry('to keep', path)
    delete_entry(entry1.id, path)
    entries = load_entries(path)
    assert len(entries) == 1
    assert entries[0].id == entry2.id
