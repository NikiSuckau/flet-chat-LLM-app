from typing import Callable, Iterable, Optional

from backend import DiaryEntry

import flet as ft


class DiaryView(ft.Column):
    """Full-screen diary entry editor view."""

    POPUP_BOTTOM: int = 70
    BUTTONS_BOTTOM: int = 10

    def __init__(
        self,
        question_callback: Optional[Callable[[str], Iterable[str] | str]] = None,
        save_callback: Optional[Callable[[ft.ControlEvent], None]] = None,
    ) -> None:
        self.question_callback = question_callback
        self.save_callback = save_callback
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
        self.left_button = ft.FloatingActionButton(mini=True, icon=ft.Icons.CIRCLE)
        self.command_button = ft.FloatingActionButton(
            icon=ft.Icons.QUESTION_MARK_ROUNDED,
            on_click=self._toggle_popup,
            width=60,
            height=60,
        )
        self.save_button = ft.FloatingActionButton(icon=ft.Icons.SAVE, on_click=save_callback)
        self.button_row = ft.Container(
            content=ft.Row(
                [self.left_button, self.command_button, self.save_button],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.END,
            ),
            padding=ft.padding.symmetric(horizontal=10),
            bottom=self.BUTTONS_BOTTOM,
            left=0,
            right=0,
        )
        self.editor = ft.TextField(
            multiline=True,
            expand=True,
            min_lines=30,
            hint_text="Write your diary entry here...",
            text_vertical_align=ft.VerticalAlignment.START,
            autofocus=True,
            border=ft.InputBorder.NONE,
        )
        self.stack = ft.Stack([self.editor, self.command_popup, self.button_row], expand=True)
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
        result = self.question_callback(self.editor.value)

        if isinstance(result, str) or not hasattr(result, "__iter__"):
            question = str(result)
            if self.editor.value and not self.editor.value.endswith("\n"):
                self.editor.value += "\n"
            self.editor.value += question
            self.command_popup.visible = False
            if self.page:
                self.update()
            return

        if self.editor.value and not self.editor.value.endswith("\n"):
            self.editor.value += "\n"
        prefix = self.editor.value
        question = ""
        for delta in result:
            question += delta
            self.editor.value = prefix + question
            if self.page:
                self.update()
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
