import flet as ft

from backend import (
    ChatBackend,
    Message,
    AppSettings,
    save_settings,
    add_entry,
)

from .chat_view import ChatView
from .settings_view import SettingsView
from .diary_view import DiaryView


class FletChatApp:
    """Main Flet application class."""

    def __init__(self, backend: ChatBackend, settings: AppSettings):
        """Store backend instance and loaded settings."""
        self.backend = backend
        self.settings = settings

    def build(self, page: ft.Page):
        """Construct all UI controls and wire up event callbacks."""
        def _navigate_drawer(e):
            """Handle drawer navigation between views."""
            if e.control.selected_index == 0:
                show_chat()
            elif e.control.selected_index == 1:
                show_settings()
            elif e.control.selected_index == 2:
                show_diary()
            page.close(drawer)

        drawer = ft.NavigationDrawer(
            on_change=_navigate_drawer,
            controls=[
                ft.Container(height=12),
                ft.NavigationDrawerDestination(
                    icon=ft.Icons.CHAT_OUTLINED,
                    label="Chat",
                ),
                ft.Divider(thickness=2),
                ft.NavigationDrawerDestination(
                    icon=ft.Icons.SETTINGS_OUTLINED,
                    label="Settings",
                ),
                ft.NavigationDrawerDestination(
                    icon=ft.Icons.BOOK_OUTLINED,
                    label="Diary",
                ),
            ],
        )

        page.appbar = ft.AppBar(
            leading=ft.IconButton(icon=ft.Icons.MENU, on_click=lambda _: page.open(drawer)),
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

        def send_message_click(e):
            """Send the current input box content to all clients and the LLM."""
            text = chat_view.new_message.value.strip()
            if not text:
                return

            user_name = page.session.get("user_name") or "Unknown"

            page.pubsub.send_all(Message(user_name=user_name, text=text, message_type="chat_message"))

            self.backend.add_user_message(text)

            chat_view.new_message.value = ""
            chat_view.new_message.focus()
            page.update()

            bot_reply = self.backend.generate_reply()
            self.backend.add_assistant_message(bot_reply)

            page.pubsub.send_all(Message(user_name="Bot", text=bot_reply, message_type="chat_message"))
            page.update()

        chat_view = ChatView(self.backend, send_message_click)

        def save_diary_click(e):
            """Persist a diary entry and clear the editor."""
            text = diary_view.get_text().strip()
            if not text:
                return
            add_entry(text)
            diary_view.clear_text()
            page.snack_bar = ft.SnackBar(ft.Text("Diary entry saved"), open=True)
            page.update()

        def save_settings_click(e):
            """Persist the edited settings and notify the user."""
            self.backend.api_url = settings_view.get_url()
            self.settings.api_url = settings_view.get_url()
            save_settings(self.settings)
            page.snack_bar = ft.SnackBar(ft.Text("Settings saved"), open=True)
            page.update()

        settings_view = SettingsView(self.settings, save_settings_click)

        diary_view = DiaryView()

        def join_chat_click(e):
            """Validate the user name and broadcast the join event."""
            if not join_user_name.value:
                join_user_name.error_text = "Name cannot be blank!"
                join_user_name.update()
                return

            page.session.set("user_name", join_user_name.value)
            welcome_dlg.open = False
            chat_view.set_user(join_user_name.value)
            page.pubsub.send_all(
                Message(
                    user_name=join_user_name.value,
                    text=f"{join_user_name.value} has joined the chat.",
                    message_type="login_message",
                )
            )
            page.update()

        def on_message(message: Message):
            """Receive published messages and show them in the chat view."""
            chat_view.add_message(message)
            page.update()

        page.pubsub.subscribe(on_message)

        def show_chat():
            """Display the chat view and hide the settings view."""
            chat_view.visible = True
            settings_view.visible = False
            diary_view.visible = False
            page.floating_action_button = None
            drawer.selected_index = 0
            page.appbar.title = ft.Text("Flet Chat")
            page.update()

        def show_settings():
            """Display the settings view and hide the chat view."""
            settings_view.set_url(self.backend.api_url)
            chat_view.visible = False
            diary_view.visible = False
            settings_view.visible = True
            page.floating_action_button = None
            drawer.selected_index = 1
            page.appbar.title = ft.Text("Settings")
            page.update()

        def show_diary():
            """Display the diary editor view."""
            chat_view.visible = False
            settings_view.visible = False
            diary_view.visible = True
            drawer.selected_index = 2
            page.appbar.title = ft.Text("Diary")
            page.floating_action_button = ft.FloatingActionButton(
                icon=ft.Icons.SAVE, on_click=save_diary_click
            )
            page.update()

        page.add(chat_view, settings_view, diary_view)

        show_chat()

