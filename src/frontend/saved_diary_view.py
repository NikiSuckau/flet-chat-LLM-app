"""UI for listing saved diary entries."""

from typing import Iterable

import flet as ft

from backend import DiaryEntry


class SavedDiaryView(ft.Column):
    """View showing diary entries in reverse chronological order."""

    def __init__(self) -> None:
        self.entries = ft.ListView(expand=True, spacing=10)
        super().__init__([self.entries], visible=False, expand=True)

    def set_entries(self, entries: Iterable[DiaryEntry]) -> None:
        """Populate the list view with diary entries sorted by date."""
        sorted_entries = sorted(entries, key=lambda e: e.timestamp, reverse=True)
        self.entries.controls = [
            ft.ListTile(title=ft.Text(entry.timestamp), subtitle=ft.Text(entry.text, selectable=True))
            for entry in sorted_entries
        ]
        if self.page:
            self.update()

