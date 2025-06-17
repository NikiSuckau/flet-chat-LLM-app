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


def test_click_calls_open_callback():
    captured: list[DiaryEntry] = []

    def _open(entry: DiaryEntry) -> None:
        captured.append(entry)

    view = SavedDiaryView(_open)
    entry = DiaryEntry(text='foo', timestamp='2025-01-01T00:00:00', id=1)
    view.set_entries([entry])
    # Simulate user click
    view.entries.controls[0].on_click(None)
    assert captured[0] == entry


def test_long_press_shows_delete_button():
    view = SavedDiaryView()
    entry = DiaryEntry(text='foo', timestamp='2025-01-01T00:00:00', id=1)
    view.set_entries([entry])
    tile = view.entries.controls[0]
    delete_btn = tile.trailing
    assert delete_btn.visible is False
    # Simulate long press
    tile.on_long_press(None)
    assert delete_btn.visible is True


def test_confirm_delete_calls_callback():
    deleted: list[int] = []

    def _delete(entry_id: int) -> None:
        deleted.append(entry_id)

    view = SavedDiaryView(delete_callback=_delete)
    entry = DiaryEntry(text='bar', timestamp='2025-01-01T00:00:00', id=7)
    view.set_entries([entry])
    tile = view.entries.controls[0]
    delete_btn = tile.trailing
    tile.on_long_press(None)
    view._request_delete(entry, delete_btn)
    view._confirm_delete(None)
    assert deleted == [7]


def test_delete_button_opens_dialog():
    view = SavedDiaryView()
    entry = DiaryEntry(text='bar', timestamp='2025-01-01T00:00:00', id=7)
    view.set_entries([entry])
    tile = view.entries.controls[0]
    delete_btn = tile.trailing
    tile.on_long_press(None)
    delete_btn.on_click(None)
    assert view._pending_delete is not None


def test_click_ignored_when_delete_visible():
    opened: list[DiaryEntry] = []

    def _open(entry: DiaryEntry) -> None:
        opened.append(entry)

    view = SavedDiaryView(_open)
    entry = DiaryEntry(text='baz', timestamp='2025-01-01T00:00:00', id=9)
    view.set_entries([entry])
    tile = view.entries.controls[0]
    tile.on_long_press(None)
    # Click tile while delete icon visible
    tile.on_click(None)
    assert opened == []

