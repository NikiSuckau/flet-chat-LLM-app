import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1] / 'src'))

from frontend.diary_view import DiaryView


class DummyEvent:
    def __init__(self, control):
        self.control = control


def test_popup_visibility_on_backslash():
    view = DiaryView()
    view.editor.value = 'Hello\\'
    view._on_editor_change(DummyEvent(view.editor))
    assert view.command_popup.visible is True
    view.editor.value = 'Hello'
    view._on_editor_change(DummyEvent(view.editor))
    assert view.command_popup.visible is False


def test_popup_position_below_line():
    view = DiaryView()
    view.editor.value = 'First line\nSecond\\'
    view._on_editor_change(DummyEvent(view.editor))
    expected_top = len(view.editor.value.splitlines()) * DiaryView.LINE_HEIGHT
    assert view.command_popup.top == expected_top


def test_insert_question_appends_text():
    called = []

    def callback(text: str) -> str:
        called.append(text)
        return "What do you feel right now?"

    view = DiaryView(callback)
    view.editor.value = "Today was good"
    view._insert_question(None)
    assert called == ["Today was good"]
    assert view.editor.value.endswith("What do you feel right now?")


def test_insert_question_removes_backslash():
    def callback(_: str) -> str:
        return "Question?"

    view = DiaryView(callback)
    view.editor.value = "Entry\\"
    view._insert_question(None)
    assert "\\" not in view.editor.value
