import flet as ft

from backend import AppSettings


class SettingsView(ft.Column):
    """View for editing application settings."""

    def __init__(self, settings: AppSettings, save_callback):
        self.settings = settings
        self.url_field = ft.TextField(
            label="KoboldCPP URL",
            value=self.settings.api_url,
            expand=True,
        )
        super().__init__(
            [
                self.url_field,
                ft.Row([ft.ElevatedButton("Save", on_click=save_callback)]),
            ],
            visible=False,
            expand=True,
        )

    def get_url(self) -> str:
        """Return the current API URL from the field."""
        return self.url_field.value

    def set_url(self, url: str) -> None:
        """Update the text field with the given URL."""
        self.url_field.value = url

