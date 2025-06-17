import flet as ft

from backend import AppSettings, ChatBackend, Message

from .chat_message import ChatMessage


class ChatView(ft.Column):
    """Main chat view containing the message list and input field."""

    def __init__(self, backend: ChatBackend, send_message_callback, settings: AppSettings):
        """Initialize widgets and wire up the send message callback."""
        self.backend = backend
        self.settings = settings
        self.chat = ft.ListView(expand=True, spacing=10, auto_scroll=True)
        self.new_message = ft.TextField(
            hint_text="Write a message...",
            autofocus=True,
            shift_enter=True,
            min_lines=1,
            max_lines=5,
            filled=True,
            expand=True,
            on_submit=send_message_callback,
        )
        super().__init__(
            [
                ft.Container(
                    content=self.chat,
                    border=ft.border.all(1, ft.Colors.OUTLINE),
                    border_radius=5,
                    padding=10,
                    expand=True,
                ),
                ft.Row(
                    [
                        self.new_message,
                        ft.IconButton(
                            icon=ft.Icons.SEND_ROUNDED,
                            tooltip="Send message",
                            on_click=send_message_callback,
                        ),
                    ]
                ),
            ],
            expand=True,
            visible=True,
        )
        self.set_user(self.settings.user_name)

    def set_user(self, user_name: str) -> None:
        """Update message prefix with the current user name."""
        self.new_message.prefix = ft.Text(f"{user_name}: ")

    def add_message(self, message: Message) -> None:
        """Append a message to the chat list."""
        if message.message_type != "chat_message":
            return
        color = (
            self.settings.avatar_color
            if message.user_name != "Bot"
            else ft.Colors.GREY_300
        )
        control = ChatMessage(message, color)
        self.chat.controls.append(control)

