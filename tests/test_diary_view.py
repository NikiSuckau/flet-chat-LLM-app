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


def test_insert_summary_prepends_text():
    prev_called = []

    def prev_entry():
        prev_called.append(True)
        return "Yesterday was bad"

    def summary_callback(text: str):
        assert text == "Yesterday was bad"
        return "Summary"

    view = DiaryView(None, summary_callback, prev_entry)
    view.editor.value = "Current entry"
    view._insert_summary(None)
    assert prev_called == [True]
    assert view.editor.value.startswith("Summary")
    assert view.editor.value.endswith("Current entry")


def test_command_popup_contains_two_buttons():
    view = DiaryView()
    column = view.command_popup.content
    assert len(column.controls) == 2



