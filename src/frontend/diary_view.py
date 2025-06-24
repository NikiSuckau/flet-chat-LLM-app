from typing import Callable, Optional

from backend import DiaryEntry

import flet as ft


class DiaryView(ft.Column):
    """Full-screen diary entry editor view."""

    POPUP_BOTTOM: int = 70

    def __init__(self, question_callback: Optional[Callable[[str], str]] = None):
        self.question_callback = question_callback
        self.current_entry_id: int | None = None
        self.current_entry_timestamp: str | None = None
        self.command_popup = ft.Container(
            content=ft.Column(
                [ft.TextButton("Self-reflection question", on_click=self._insert_question)]
            ),
            bgcolor=ft.Colors.WHITE,
            border=ft.border.all(1, ft.Colors.OUTLINE),
            padding=10,
            visible=False,
            bottom=self.POPUP_BOTTOM,
            left=0,
            right=0,
            alignment=ft.alignment.bottom_center,
        )
        self.command_button = ft.FloatingActionButton(
            icon=ft.Icons.QUESTION_MARK_ROUNDED,
            on_click=self._toggle_popup,
        )
        self.command_button.bottom = 10
        self.command_button.left = 0
        self.command_button.right = 0
        self.command_button.alignment = ft.alignment.bottom_center
        self.editor = ft.TextField(
            multiline=True,
            expand=True,
            min_lines=30,
            hint_text="Write your diary entry here...",
            text_vertical_align=ft.VerticalAlignment.START,
            autofocus=True,
            border=ft.InputBorder.NONE,
        )
        self.stack = ft.Stack([self.editor, self.command_popup, self.command_button], expand=True)
        super().__init__(
            [self.stack],
            visible=False,
            expand=True,
        )

    def _toggle_popup(self, e: ft.ControlEvent) -> None:
        """Show or hide the command popup when the button is pressed."""
        self.command_popup.visible = not self.command_popup.visible
        if self.page:
            self.update()

    def _insert_question(self, e: ft.ControlEvent) -> None:
        """Insert a generated question below the current diary text."""
        if not self.question_callback:
            return
        question = self.question_callback(self.editor.value)
        if self.editor.value and not self.editor.value.endswith("\n"):
            self.editor.value += "\n"
        self.editor.value += question
        self.command_popup.visible = False
        if self.page:
            self.update()

    def get_text(self) -> str:
        return self.editor.value

    def clear_text(self) -> None:
        self.editor.value = ""
        self.current_entry_id = None
        self.current_entry_timestamp = None

    def set_entry(self, entry: "DiaryEntry") -> None:
        """Load a diary entry for editing."""

        self.editor.value = entry.text
        self.current_entry_id = entry.id
        self.current_entry_timestamp = entry.timestamp
        if self.page:
            self.update()
