import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1] / 'src'))

from frontend.chat_message import ChatMessage
from backend import Message


def test_get_initials():
    assert ChatMessage._get_initials('Bob') == 'B'
    assert ChatMessage._get_initials('') == '?'


def test_avatar_color_deterministic():
    assert ChatMessage._get_avatar_color('Alice') == ChatMessage._get_avatar_color('Alice')


def test_message_expands_to_width():
    msg = ChatMessage(Message(user_name="Bob", text="Hello", message_type="chat_message"))
    # Row should expand to fill parent width for wrapping
    assert msg.expand is True
    # Column containing the text should also expand
    column = msg.controls[1]
    assert column.expand is True
