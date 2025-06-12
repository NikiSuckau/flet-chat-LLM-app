import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1] / 'src'))

from backend import AppSettings, load_settings, save_settings


def test_load_settings_defaults(tmp_path):
    path = tmp_path / 'settings.json'
    settings = load_settings(path)
    assert isinstance(settings, AppSettings)
    assert settings.api_url == "http://localhost:5001/v1/chat/completions"


def test_save_and_load_settings(tmp_path):
    path = tmp_path / 'settings.json'
    settings = AppSettings(api_url='http://example.com')
    save_settings(settings, path)
    loaded = load_settings(path)
    assert loaded == settings
