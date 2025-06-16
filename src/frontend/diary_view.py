import flet as ft


class DiaryView(ft.Column):
    """Full-screen diary entry editor view."""

    def __init__(self):
        self.command_popup = ft.Container(
            content=ft.Column([ft.Text("Command 1"), ft.Text("Command 2")]),
            bgcolor=ft.Colors.WHITE,
            border=ft.border.all(1, ft.Colors.OUTLINE),
            padding=10,
            visible=False,
        )
        self.editor = ft.TextField(
            multiline=True,
            expand=True,
            min_lines=30,
            hint_text="Write your diary entry here...",
            text_vertical_align=ft.VerticalAlignment.START,
            autofocus=True,
            border=ft.InputBorder.NONE,
            on_change=self._on_editor_change,
        )
        super().__init__(
            [self.editor, self.command_popup],
            visible=False,
            expand=True,
        )

    def _on_editor_change(self, e):
        """Show command popup when a backslash is typed."""
        if self.editor.value.endswith("\\"):
            self.command_popup.visible = True
        else:
            self.command_popup.visible = False

    def get_text(self) -> str:
        return self.editor.value

    def clear_text(self) -> None:
        self.editor.value = ""
