import flet as ft

from backend import ChatBackend
from frontend import FletChatApp
from settings_manager import load_settings

settings = load_settings()
backend = ChatBackend(settings.api_url)


def main(page: ft.Page):
    app = FletChatApp(backend, settings)
    app.build(page)


if __name__ == "__main__":
    ft.app(target=main)
