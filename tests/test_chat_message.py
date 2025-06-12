import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1] / 'src'))

from frontend.chat_message import ChatMessage


def test_get_initials():
    assert ChatMessage._get_initials('Bob') == 'B'
    assert ChatMessage._get_initials('') == '?'


def test_avatar_color_deterministic():
    assert ChatMessage._get_avatar_color('Alice') == ChatMessage._get_avatar_color('Alice')
