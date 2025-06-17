import flet as ft

from backend import AppSettings


class SettingsView(ft.Column):
    """View for editing application settings."""

    def __init__(self, settings: AppSettings, save_callback):
        """Create settings form and hook up save button."""
        self.settings = settings
        self.url_field = ft.TextField(
            label="KoboldCPP URL",
            value=self.settings.api_url,
            expand=True,
        )
        self.prompt_field = ft.TextField(
            label="System Prompt",
            multiline=True,
            value=self.settings.system_prompt,
            expand=True,
        )
        self.temp_slider = ft.Slider(
            min=0.0,
            max=1.0,
            divisions=10,
            value=self.settings.temperature,
            label="{value}",
        )
        self.tokens_field = ft.TextField(
            label="Max Tokens",
            value=str(self.settings.max_tokens),
            width=150,
        )
        super().__init__(
            [
                self.url_field,
                self.prompt_field,
                self.temp_slider,
                self.tokens_field,
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

    def get_system_prompt(self) -> str:
        """Return the system prompt from the field."""
        return self.prompt_field.value

    def set_system_prompt(self, text: str) -> None:
        """Update the system prompt field."""
        self.prompt_field.value = text

    def get_temperature(self) -> float:
        """Return the slider temperature value."""
        return float(self.temp_slider.value)

    def set_temperature(self, value: float) -> None:
        """Update the temperature slider."""
        self.temp_slider.value = value

    def get_max_tokens(self) -> int:
        """Return the max tokens value from the text field."""
        try:
            return int(self.tokens_field.value)
        except ValueError:
            return 0

    def set_max_tokens(self, value: int) -> None:
        """Update the max tokens text field."""
        self.tokens_field.value = str(value)

