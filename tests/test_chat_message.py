import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1] / 'src'))

from frontend.chat_message import ChatMessage
from backend import Message


def test_get_initials():
    assert ChatMessage._get_initials('Bob') == 'B'
    assert ChatMessage._get_initials('') == '?'


def test_avatar_color_applied():
    msg = Message(user_name='Alice', text='hi', message_type='chat_message')
    cm = ChatMessage(msg, 'red')
    assert cm.controls[0].bgcolor == 'red'
