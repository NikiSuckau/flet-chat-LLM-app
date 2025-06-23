from __future__ import annotations

"""UI view for displaying user memories."""

from typing import Iterable

import flet as ft

from backend import MemoryRecord


class MemoriesView(ft.Column):
    """Simple list view presenting stored memories."""

    def __init__(self) -> None:
        self.memories = ft.ListView(expand=True, spacing=10)
        super().__init__([self.memories], visible=False, expand=True)

    def set_memories(self, memories: Iterable[MemoryRecord]) -> None:
        """Populate list with memory records."""
        tiles: list[ft.ListTile] = []
        for mem in memories:
            tiles.append(
                ft.ListTile(
                    title=ft.Text(mem.kind),
                    subtitle=ft.Text(mem.content, selectable=True),
                )
            )
        self.memories.controls = tiles
        if self.page:
            self.update()
