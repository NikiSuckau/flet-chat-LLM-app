import flet as ft


class DiaryView(ft.Column):
    """Full-screen diary entry editor view."""

    LINE_HEIGHT: int = 24

    def __init__(self):
        self.command_popup = ft.Container(
            content=ft.Column([ft.Text("Command 1"), ft.Text("Command 2")]),
            bgcolor=ft.Colors.WHITE,
            border=ft.border.all(1, ft.Colors.OUTLINE),
            padding=10,
            visible=False,
            left=0,
            top=0,
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
        self.stack = ft.Stack([self.editor, self.command_popup], expand=True)
        super().__init__(
            [self.stack],
            visible=False,
            expand=True,
        )

    def _on_editor_change(self, e: ft.ControlEvent) -> None:
        """Toggle command popup visibility when a backslash is typed."""
        last_char = e.control.value[-1:] if e.control.value else ""
        self.command_popup.visible = last_char == "\\"
        if self.command_popup.visible:
            line_count = len(e.control.value.splitlines())
            self.command_popup.top = line_count * self.LINE_HEIGHT
            self.command_popup.left = 0
        if self.page:
            self.update()

    def get_text(self) -> str:
        return self.editor.value

    def clear_text(self) -> None:
        self.editor.value = ""
