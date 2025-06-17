import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1] / 'src'))

from backend import AppSettings, ChatBackend, load_settings, save_settings


def test_load_settings_defaults(tmp_path):
    path = tmp_path / 'settings.json'
    settings = load_settings(path)
    assert isinstance(settings, AppSettings)
    assert settings.api_url == "http://localhost:5001/v1/chat/completions"
    assert settings.system_prompt == ChatBackend.DEFAULT_SYSTEM_PROMPT
    assert settings.temperature == 0.8
    assert settings.max_tokens == 200
    assert settings.diary_system_prompt == ChatBackend.DEFAULT_SYSTEM_PROMPT
    assert settings.diary_prompt == ChatBackend.DEFAULT_DIARY_PROMPT
    assert settings.diary_temperature == 0.7
    assert settings.diary_max_tokens == 50
    assert settings.user_name == "User"
    assert settings.avatar_color == "blue"


def test_save_and_load_settings(tmp_path):
    path = tmp_path / 'settings.json'
    settings = AppSettings(
        api_url='http://example.com',
        system_prompt='hello',
        temperature=0.5,
        max_tokens=150,
        diary_system_prompt='dsp',
        diary_prompt='dp',
        diary_temperature=0.6,
        diary_max_tokens=75,
        user_name="Alice",
        avatar_color="red",
    )
    save_settings(settings, path)
    loaded = load_settings(path)
    assert loaded == settings
