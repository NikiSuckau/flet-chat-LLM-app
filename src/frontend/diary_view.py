import flet as ft


class DiaryView(ft.Column):
    """Full-screen diary entry editor view."""

    def __init__(self):
        self.editor = ft.TextField(
            multiline=True,
            expand=True,
            min_lines=30,
            hint_text="Write your diary entry here...",
            text_vertical_align=ft.VerticalAlignment.START,
            autofocus=True,
            border=ft.InputBorder.NONE,
        )
        super().__init__(
            [self.editor],
            visible=False,
            expand=True,
        )

    def get_text(self) -> str:
        return self.editor.value

    def clear_text(self) -> None:
        self.editor.value = ""
