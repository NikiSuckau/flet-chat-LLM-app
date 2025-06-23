import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1] / 'src'))

from backend import ChatBackend
from backend.memory_agent import LangMemAgent


class DummyAgent(LangMemAgent):
    def __init__(self):
        self.saved: list[str] = []

    def save(self, text: str) -> None:  # type: ignore[override]
        self.saved.append(text)


def test_user_messages_saved():
    mem = DummyAgent()
    backend = ChatBackend('http://api', memory_agent=mem)
    backend.add_user_message('hello')
    assert mem.saved == ['hello']

