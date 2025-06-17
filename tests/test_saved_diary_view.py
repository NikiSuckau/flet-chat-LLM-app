import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1] / 'src'))

from backend import DiaryEntry
from frontend.saved_diary_view import SavedDiaryView


def test_entries_sorted_descending():
    view = SavedDiaryView()
    entries = [
        DiaryEntry(text='old', timestamp='2024-01-01T10:00:00'),
        DiaryEntry(text='new', timestamp='2024-01-02T09:00:00'),
    ]
    # Pass in unsorted entries
    view.set_entries(entries)
    assert len(view.entries.controls) == 2
    first = view.entries.controls[0]
    assert first.title.value == '2024-01-02T09:00:00'
    assert first.subtitle.value == 'new'

