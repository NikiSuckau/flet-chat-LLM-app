import flet as ft
from models import Message
from backend import ChatBackend


class ChatMessage(ft.Row):
    def __init__(self, message: Message):
        super().__init__()
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
                spacing=5,
            ),
        ]

    @staticmethod
    def _get_initials(user_name: str) -> str:
        return user_name[:1].upper() if user_name else "?"

    @staticmethod
    def _get_avatar_color(user_name: str):
        colors_lookup = [
            ft.Colors.AMBER, ft.Colors.BLUE, ft.Colors.BROWN,
            ft.Colors.CYAN, ft.Colors.GREEN, ft.Colors.INDIGO,
            ft.Colors.LIME, ft.Colors.ORANGE, ft.Colors.PINK,
            ft.Colors.PURPLE, ft.Colors.RED, ft.Colors.TEAL,
            ft.Colors.YELLOW,
        ]
        return colors_lookup[hash(user_name) % len(colors_lookup)]


class FletChatApp:
    def __init__(self, backend: ChatBackend):
        self.backend = backend

    def build(self, page: ft.Page):
        def _close_drawer(e):
            page.close(drawer)

        drawer = ft.NavigationDrawer(
            on_change=_close_drawer,
            controls=[
                ft.Container(height=12),
                ft.NavigationDrawerDestination(
                    icon_content=ft.Icon(ft.icons.CHAT_OUTLINED),
                    label="Chat",
                ),
                ft.Divider(thickness=2),
                ft.NavigationDrawerDestination(
                    icon_content=ft.Icon(ft.icons.SETTINGS_OUTLINED),
                    label="Settings",
                ),
            ]
        )

        page.appbar = ft.AppBar(
            leading=ft.IconButton(
                icon=ft.icons.MENU,
                on_click=lambda _: page.open(drawer),
            ),
            title=ft.Text("Flet Chat"),
        )
        page.horizontal_alignment = ft.CrossAxisAlignment.STRETCH
        page.title = "Flet + KoboldCPP: Voller Chatkontext"

        join_user_name = ft.TextField(
            label="Enter your name to join the chat",
            autofocus=True,
            on_submit=lambda e: join_chat_click(e),
        )
        welcome_dlg = ft.AlertDialog(
            open=True,
            modal=True,
            title=ft.Text("Welcome!"),
            content=ft.Column([join_user_name], width=300, height=70, tight=True),
            actions=[ft.ElevatedButton(text="Join chat", on_click=lambda e: join_chat_click(e))],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        page.overlay.append(welcome_dlg)

        chat = ft.ListView(expand=True, spacing=10, auto_scroll=True)
        new_message = ft.TextField(
            hint_text="Write a message...",
            autofocus=True,
            shift_enter=True,
            min_lines=1,
            max_lines=5,
            filled=True,
            expand=True,
            on_submit=lambda e: send_message_click(e),
        )

        def join_chat_click(e):
            if not join_user_name.value:
                join_user_name.error_text = "Name cannot be blank!"
                join_user_name.update()
                return

            page.session.set("user_name", join_user_name.value)
            welcome_dlg.open = False
            new_message.prefix = ft.Text(f"{join_user_name.value}: ")
            page.pubsub.send_all(
                Message(
                    user_name=join_user_name.value,
                    text=f"{join_user_name.value} has joined the chat.",
                    message_type="login_message",
                )
            )
            page.update()

        def send_message_click(e):
            text = new_message.value.strip()
            if not text:
                return

            user_name = page.session.get("user_name") or "Unknown"

            page.pubsub.send_all(
                Message(
                    user_name=user_name,
                    text=text,
                    message_type="chat_message",
                )
            )

            self.backend.add_user_message(text)

            new_message.value = ""
            new_message.focus()
            page.update()

            bot_reply = self.backend.generate_reply()
            self.backend.add_assistant_message(bot_reply)

            page.pubsub.send_all(
                Message(
                    user_name="Bot",
                    text=bot_reply,
                    message_type="chat_message",
                )
            )
            page.update()

        def on_message(message: Message):
            if message.message_type == "chat_message":
                m = ChatMessage(message)
            elif message.message_type == "login_message":
                m = ft.Text(message.text, italic=True, color=ft.Colors.BLACK45, size=12)
            else:
                return

            chat.controls.append(m)
            page.update()

        page.pubsub.subscribe(on_message)

        page.add(
            ft.Container(
                content=chat,
                border=ft.border.all(1, ft.Colors.OUTLINE),
                border_radius=5,
                padding=10,
                expand=True,
            ),
            ft.Row(
                [
                    new_message,
                    ft.IconButton(
                        icon=ft.Icons.SEND_ROUNDED,
                        tooltip="Send message",
                        on_click=lambda e: send_message_click(e),
                    ),
                ]
            ),
        )
