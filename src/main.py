import flet as ft

from backend import ChatBackend
from frontend_flet import FletChatApp

# KOBOLDCPP_API_URL = "http://localhost:5001/v1/chat/completions"
KOBOLDCPP_API_URL = "http://home:5001/v1/chat/completions"

backend = ChatBackend(KOBOLDCPP_API_URL)


def main(page: ft.Page):
    app = FletChatApp(backend)
    app.build(page)


if __name__ == "__main__":
    ft.app(target=main)
