import flet as ft

from backend import Message


class ChatMessage(ft.Row):
    """UI widget representing a single chat message."""

    def __init__(self, message: Message, avatar_color: str):
        """Create visual representation of a message for the chat list."""
        super().__init__()
        self.vertical_alignment = ft.CrossAxisAlignment.START
        self.controls = [
            ft.CircleAvatar(
                content=ft.Text(self._get_initials(message.user_name)),
                color=ft.Colors.WHITE,
                bgcolor=avatar_color,
            ),
            ft.Column(
                [
                    ft.Text(message.user_name),
                    ft.Text(message.text, selectable=True),
                ],
                tight=True,
                spacing=5,
            ),
        ]

    @staticmethod
    def _get_initials(user_name: str) -> str:
        """Return first letter of the user name for the avatar."""
        return user_name[:1].upper() if user_name else "?"

