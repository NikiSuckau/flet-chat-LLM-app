import flet as ft
from dataclasses import asdict
from typing import Callable

from backend import (
    AppSettings,
    ChatBackend,
    DiaryEntry,
    Message,
    add_entry,
    delete_entry,
    load_entries,
    save_settings,
    update_entry,
)

from .chat_view import ChatView
from .settings_view import SettingsView
from .diary_view import DiaryView
from .saved_diary_view import SavedDiaryView


class FletChatApp:
    """Main Flet application class."""

    def __init__(self, backend: ChatBackend, settings: AppSettings):
        """Store backend instance and loaded settings."""
        self.backend = backend
        self.settings = settings

    def build(self, page: ft.Page):
        """Construct all UI controls and wire up event callbacks."""
        settings_dirty = False
        settings_snapshot = asdict(self.settings)
        pending_nav: Callable | None = None

        def mark_dirty(e=None):
            nonlocal settings_dirty
            current = asdict(_view_to_settings())
            settings_dirty = current != settings_snapshot

        def _view_to_settings() -> AppSettings:
            return AppSettings(
                api_url=settings_view.get_url(),
                system_prompt=settings_view.get_system_prompt(),
                temperature=settings_view.get_temperature(),
                max_tokens=settings_view.get_max_tokens(),
                diary_system_prompt=settings_view.get_diary_system_prompt(),
                diary_prompt=settings_view.get_diary_prompt(),
                diary_temperature=settings_view.get_diary_temperature(),
                diary_max_tokens=settings_view.get_diary_max_tokens(),
                user_name=settings_view.get_user_name(),
                avatar_color=settings_view.get_avatar_color(),
            )

        confirm_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Unsaved Changes"),
            content=ft.Text("Discard your changes?"),
            actions=[
                ft.TextButton(
                    "Cancel",
                    on_click=lambda e: _close_dialog(),
                ),
                ft.TextButton(
                    "Discard",
                    on_click=lambda e: _discard_changes(),
                ),
            ],
        )

        def _close_dialog() -> None:
            confirm_dialog.open = False
            page.update()

        def _discard_changes() -> None:
            nonlocal settings_dirty, pending_nav
            confirm_dialog.open = False
            page.update()
            settings_dirty = False
            if pending_nav:
                pending_nav()
                pending_nav = None

        def _maybe_navigate(fn):
            nonlocal pending_nav
            if settings_view.visible and settings_dirty:
                pending_nav = fn
                page.dialog = confirm_dialog
                confirm_dialog.open = True
                page.update()
            else:
                fn()

        def _navigate_drawer(e):
            """Handle drawer navigation between views."""
            if e.control.selected_index == 0:
                _maybe_navigate(show_chat)
            elif e.control.selected_index == 1:
                _maybe_navigate(show_settings)
            elif e.control.selected_index == 2:
                _maybe_navigate(show_diary)
            elif e.control.selected_index == 3:
                _maybe_navigate(show_saved)
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
                ft.NavigationDrawerDestination(
                    icon=ft.Icons.SAVE_OUTLINED,
                    label="Saved",
                ),
            ],
        )

        page.appbar = ft.AppBar(
            leading=ft.IconButton(icon=ft.Icons.MENU, on_click=lambda _: page.open(drawer)),
            title=ft.Text("Flet Chat"),
        )
        page.horizontal_alignment = ft.CrossAxisAlignment.STRETCH
        page.title = "Flet + KoboldCPP: Voller Chatkontext"



        def send_message_click(e):
            """Send the current input box content to all clients and the LLM."""
            text = chat_view.new_message.value.strip()
            if not text:
                return

            user_name = self.settings.user_name

            chat_view.add_message(Message(user_name=user_name, text=text, message_type="chat_message"))
            self.backend.add_user_message(text)

            chat_view.new_message.value = ""
            chat_view.new_message.focus()
            page.update()

            bot_message = Message(user_name="Bot", text="", message_type="chat_message")
            msg_control = chat_view.add_message(bot_message)
            page.update()

            bot_reply = ""
            for delta in self.backend.stream_reply():
                bot_reply += delta
                msg_control.text_control.value = bot_reply
                page.update()

            self.backend.add_assistant_message(bot_reply)

        chat_view = ChatView(self.backend, send_message_click, self.settings)

        def save_diary_click(e):
            """Persist a new or edited diary entry."""

            text = diary_view.get_text().strip()
            if not text:
                return

            if diary_view.current_entry_id is None:
                add_entry(text)
            else:
                update_entry(diary_view.current_entry_id, text)

            diary_view.clear_text()
            saved_diary_view.set_entries(load_entries())
            page.snack_bar = ft.SnackBar(ft.Text("Diary entry saved"), open=True)
            page.update()

        def save_settings_click(e):
            """Persist the edited settings and notify the user."""
            nonlocal settings_snapshot, settings_dirty
            if not settings_dirty:
                return
            self.backend.api_url = settings_view.get_url()
            self.backend.system_prompt = settings_view.get_system_prompt()
            self.backend.temperature = settings_view.get_temperature()
            self.backend.max_tokens = settings_view.get_max_tokens()
            self.backend.diary_system_prompt = settings_view.get_diary_system_prompt()
            self.backend.diary_prompt = settings_view.get_diary_prompt()
            self.backend.diary_temperature = settings_view.get_diary_temperature()
            self.backend.diary_max_tokens = settings_view.get_diary_max_tokens()
            self.settings.user_name = settings_view.get_user_name()
            self.settings.avatar_color = settings_view.get_avatar_color()
            self.settings.api_url = settings_view.get_url()
            self.settings.system_prompt = settings_view.get_system_prompt()
            self.settings.temperature = settings_view.get_temperature()
            self.settings.max_tokens = settings_view.get_max_tokens()
            self.settings.diary_system_prompt = settings_view.get_diary_system_prompt()
            self.settings.diary_prompt = settings_view.get_diary_prompt()
            self.settings.diary_temperature = settings_view.get_diary_temperature()
            self.settings.diary_max_tokens = settings_view.get_diary_max_tokens()
            chat_view.set_user(self.settings.user_name)
            save_settings(self.settings)
            settings_snapshot = asdict(self.settings)
            settings_dirty = False
            page.snack_bar = ft.SnackBar(ft.Text("Settings saved"), open=True)
            page.update()

        settings_view = SettingsView(self.settings, mark_dirty)

        diary_view = DiaryView(self.backend.generate_diary_question)

        def open_saved_entry(entry: DiaryEntry) -> None:
            diary_view.set_entry(entry)
            show_diary()

        def delete_saved_entry(entry_id: int) -> None:
            delete_entry(entry_id)
            saved_diary_view.set_entries(load_entries())

        saved_diary_view = SavedDiaryView(open_saved_entry, delete_saved_entry)


        def show_chat():
            """Display the chat view and hide the settings view."""
            chat_view.visible = True
            settings_view.visible = False
            diary_view.visible = False
            saved_diary_view.visible = False
            page.floating_action_button = None
            drawer.selected_index = 0
            page.appbar.title = ft.Text("Flet Chat")
            page.update()

        def show_settings():
            """Display the settings view and hide the chat view."""
            settings_view.set_url(self.backend.api_url)
            settings_view.set_system_prompt(self.backend.system_prompt)
            settings_view.set_temperature(self.backend.temperature)
            settings_view.set_max_tokens(self.backend.max_tokens)
            settings_view.set_diary_system_prompt(self.backend.diary_system_prompt)
            settings_view.set_diary_prompt(self.backend.diary_prompt)
            settings_view.set_diary_temperature(self.backend.diary_temperature)
            settings_view.set_diary_max_tokens(self.backend.diary_max_tokens)
            settings_view.set_user_name(self.settings.user_name)
            settings_view.set_avatar_color(self.settings.avatar_color)
            nonlocal settings_snapshot, settings_dirty
            settings_snapshot = asdict(self.settings)
            settings_dirty = False
            chat_view.visible = False
            diary_view.visible = False
            saved_diary_view.visible = False
            settings_view.visible = True
            page.floating_action_button = ft.FloatingActionButton(
                icon=ft.Icons.SAVE, on_click=save_settings_click
            )
            drawer.selected_index = 1
            page.appbar.title = ft.Text("Settings")
            page.update()

        def show_diary():
            """Display the diary editor view."""
            chat_view.visible = False
            settings_view.visible = False
            saved_diary_view.visible = False
            diary_view.visible = True
            drawer.selected_index = 2
            page.appbar.title = ft.Text("Diary")
            page.floating_action_button = ft.FloatingActionButton(
                icon=ft.Icons.SAVE, on_click=save_diary_click
            )
            page.update()

        def show_saved():
            """Display saved diary entries."""
            chat_view.visible = False
            settings_view.visible = False
            diary_view.visible = False
            saved_diary_view.visible = True
            saved_diary_view.set_entries(load_entries())
            drawer.selected_index = 3
            page.appbar.title = ft.Text("Saved")
            page.floating_action_button = None
            page.update()

        page.add(chat_view, settings_view, diary_view, saved_diary_view)

        show_chat()

