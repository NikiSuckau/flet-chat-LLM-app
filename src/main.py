import flet as ft

from backend import ChatBackend
from config import load_config
from frontend_flet import FletChatApp


config = load_config()
backend = ChatBackend(config["api_url"])


def main(page: ft.Page):
    app = FletChatApp(backend, config)
    app.build(page)


if __name__ == "__main__":
    ft.app(target=main)
