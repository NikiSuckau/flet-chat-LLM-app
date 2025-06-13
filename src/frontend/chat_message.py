import flet as ft

from backend import Message


class ChatMessage(ft.Row):
    """UI widget representing a single chat message."""

    def __init__(self, message: Message):
        """Create visual representation of a message for the chat list."""
        super().__init__(expand=True)
        self.vertical_alignment = ft.CrossAxisAlignment.START
        self.controls = [
            ft.CircleAvatar(
                content=ft.Text(self._get_initials(message.user_name)),
                color=ft.Colors.WHITE,
                bgcolor=self._get_avatar_color(message.user_name),
            ),
            ft.Column(
                [
                    ft.Text(message.user_name),
                    ft.Text(message.text, selectable=True),
                ],
                tight=True,
                expand=True,
                spacing=5,
            ),
        ]

    @staticmethod
    def _get_initials(user_name: str) -> str:
        """Return first letter of the user name for the avatar."""
        return user_name[:1].upper() if user_name else "?"

    @staticmethod
    def _get_avatar_color(user_name: str):
        """Deterministically pick a color based on the user name."""
        colors_lookup = [
            ft.Colors.AMBER,
            ft.Colors.BLUE,
            ft.Colors.BROWN,
            ft.Colors.CYAN,
            ft.Colors.GREEN,
            ft.Colors.INDIGO,
            ft.Colors.LIME,
            ft.Colors.ORANGE,
            ft.Colors.PINK,
            ft.Colors.PURPLE,
            ft.Colors.RED,
            ft.Colors.TEAL,
            ft.Colors.YELLOW,
        ]
        return colors_lookup[hash(user_name) % len(colors_lookup)]
