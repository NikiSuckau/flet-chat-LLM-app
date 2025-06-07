import flet as ft

from backend import ChatBackend
from frontend_flet import FletChatApp
from settings import SettingsManager

# KOBOLDCPP_API_URL = "http://localhost:5001/v1/chat/completions"
KOBOLDCPP_API_URL = "http://home:5001/v1/chat/completions"

settings_manager = SettingsManager()
app_settings = settings_manager.load()
backend = ChatBackend(KOBOLDCPP_API_URL, api_key=app_settings.api_key)


def main(page: ft.Page):
    app = FletChatApp(backend, settings_manager, app_settings)
    app.build(page)


if __name__ == "__main__":
    ft.app(target=main)
