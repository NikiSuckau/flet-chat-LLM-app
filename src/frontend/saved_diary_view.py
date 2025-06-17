"""UI for listing saved diary entries."""

from typing import Callable, Iterable, Optional

import flet as ft

from backend import DiaryEntry


class SavedDiaryView(ft.Column):
    """View showing diary entries in reverse chronological order."""

    def __init__(self, open_callback: Optional[Callable[[DiaryEntry], None]] = None) -> None:
        self.open_callback = open_callback
        self.entries = ft.ListView(expand=True, spacing=10)
        super().__init__([self.entries], visible=False, expand=True)

    def set_entries(self, entries: Iterable[DiaryEntry]) -> None:
        """Populate the list view with diary entries sorted by date."""
        sorted_entries = sorted(entries, key=lambda e: e.timestamp, reverse=True)
        self.entries.controls = [
            ft.ListTile(
                title=ft.Text(entry.timestamp),
                subtitle=ft.Text(entry.text, selectable=True),
                on_click=lambda e, entry=entry: self._open_entry(entry),
            )
            for entry in sorted_entries
        ]
        if self.page:
            self.update()

    def _open_entry(self, entry: DiaryEntry) -> None:
        if self.open_callback:
            self.open_callback(entry)

