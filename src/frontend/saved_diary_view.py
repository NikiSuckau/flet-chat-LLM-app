"""UI for listing saved diary entries."""

from typing import Callable, Iterable, Optional

import flet as ft

from backend import DiaryEntry


class SavedDiaryView(ft.Column):
    """View showing diary entries in reverse chronological order."""

    def __init__(
        self,
        open_callback: Optional[Callable[[DiaryEntry], None]] = None,
        delete_callback: Optional[Callable[[int], None]] = None,
    ) -> None:
        self.open_callback = open_callback
        self.delete_callback = delete_callback
        self.entries = ft.ListView(expand=True, spacing=10)
        self.confirm_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Delete entry?"),
            content=ft.Text("Do you really want to delete this entry?"),
            actions=[
                ft.TextButton("Yes", on_click=self._confirm_delete),
                ft.TextButton("No", on_click=self._cancel_delete),
            ],
        )
        self._pending_delete: tuple[DiaryEntry, ft.IconButton] | None = None
        super().__init__([self.entries], visible=False, expand=True)

    def set_entries(self, entries: Iterable[DiaryEntry]) -> None:
        """Populate the list view with diary entries sorted by date."""
        sorted_entries = sorted(entries, key=lambda e: e.timestamp, reverse=True)
        tiles: list[ft.ListTile] = []
        for entry in sorted_entries:
            delete_btn = ft.IconButton(icon=ft.Icons.DELETE, visible=False)
            delete_btn.on_click = lambda e, entry=entry, btn=delete_btn: self._request_delete(entry, btn)

            tile = ft.ListTile(
                title=ft.Text(entry.timestamp),
                subtitle=ft.Text(entry.text, selectable=True),
                trailing=delete_btn,
            )
            tile.on_click = lambda e, entry=entry, btn=delete_btn, t=tile: (
                self._open_entry(entry)
                if getattr(e, "control", t) is t and not btn.visible
                else None
            )
            tile.on_long_press = lambda e, btn=delete_btn: self._show_delete(btn)
            tiles.append(tile)
        self.entries.controls = tiles
        if self.page:
            self.update()

    def _open_entry(self, entry: DiaryEntry) -> None:
        if self.open_callback:
            self.open_callback(entry)

    def _show_delete(self, button: ft.IconButton) -> None:
        button.visible = True
        if self.page:
            self.update()

    def _request_delete(self, entry: DiaryEntry, button: ft.IconButton) -> None:
        self._pending_delete = (entry, button)
        if self.page:
            self.page.open(self.confirm_dialog)

    def _confirm_delete(self, e: ft.ControlEvent) -> None:
        if not self._pending_delete:
            return
        entry, button = self._pending_delete
        if self.delete_callback and entry.id is not None:
            self.delete_callback(entry.id)
        if self.page:
            self.page.close(self.confirm_dialog)
        else:
            self.confirm_dialog.open = False
        button.visible = False
        self._pending_delete = None

    def _cancel_delete(self, e: ft.ControlEvent) -> None:
        if self._pending_delete:
            _, button = self._pending_delete
            button.visible = False
        self._pending_delete = None
        if self.page:
            self.page.close(self.confirm_dialog)
        else:
            self.confirm_dialog.open = False

