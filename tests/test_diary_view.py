import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1] / 'src'))

from frontend.diary_view import DiaryView


def test_popup_visibility_on_backslash():
    view = DiaryView()
    view.editor.value = 'Hello\\'
    view._on_editor_change(None)
    assert view.command_popup.visible is True
    view.editor.value = 'Hello'
    view._on_editor_change(None)
    assert view.command_popup.visible is False
