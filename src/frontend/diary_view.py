import flet as ft


class DiaryView(ft.Column):
    """Simple diary entry editor view."""

    def __init__(self, save_callback):
        self.editor = ft.TextField(
            multiline=True,
            expand=True,
            hint_text="Write your diary entry here...",
            text_vertical_align=ft.VerticalAlignment.START,
            autofocus=True,
        )
        super().__init__(
            [
                self.editor,
                ft.Row([ft.ElevatedButton("Save", on_click=save_callback)]),
            ],
            visible=False,
            expand=True,
        )

    def get_text(self) -> str:
        return self.editor.value

    def clear_text(self) -> None:
        self.editor.value = ""
