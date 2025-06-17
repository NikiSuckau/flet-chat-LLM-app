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


def test_save_and_load_settings(tmp_path):
    path = tmp_path / 'settings.json'
    settings = AppSettings(
        api_url='http://example.com',
        system_prompt='hello',
        temperature=0.5,
        max_tokens=150,
    )
    save_settings(settings, path)
    loaded = load_settings(path)
    assert loaded == settings
