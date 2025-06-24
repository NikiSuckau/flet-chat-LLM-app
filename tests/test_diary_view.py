import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1] / 'src'))

from frontend.diary_view import DiaryView



def test_popup_visibility_toggle():
    view = DiaryView()
    view._toggle_popup(None)
    assert view.command_popup.visible is True
    view._toggle_popup(None)
    assert view.command_popup.visible is False


def test_popup_position_constant():
    view = DiaryView()
    assert view.command_popup.bottom == DiaryView.POPUP_BOTTOM


def test_insert_question_appends_text():
    called = []

    def callback(text: str):
        called.append(text)
        yield "What "
        yield "do "
        yield "you "
        yield "feel "
        yield "right "
        yield "now?"

    view = DiaryView(callback)
    view.editor.value = "Today was good"
    view._insert_question(None)
    assert called == ["Today was good"]
    assert view.editor.value.endswith("What do you feel right now?")



