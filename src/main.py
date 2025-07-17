import flet as ft

from backend import ChatBackend, load_settings
from frontend import FletChatApp

settings = load_settings()
backend = ChatBackend(
    settings.api_url,
    system_prompt=settings.system_prompt,
    temperature=settings.temperature,
    max_tokens=settings.max_tokens,
    diary_system_prompt=settings.diary_system_prompt,
    diary_prompt=settings.diary_prompt,
    diary_temperature=settings.diary_temperature,
    diary_max_tokens=settings.diary_max_tokens,
    summary_system_prompt=settings.summary_system_prompt,
    summary_prompt=settings.summary_prompt,
    summary_temperature=settings.summary_temperature,
    summary_max_tokens=settings.summary_max_tokens,
    enable_memory=settings.enable_memory,
)


def main(page: ft.Page):
    """Entry point for Flet when running `flet run`."""
    app = FletChatApp(backend, settings)
    app.build(page)


if __name__ == "__main__":
    ft.app(target=main)
