import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1] / 'src'))

from frontend.chat_view import ChatView
from backend import ChatBackend

class DummyPage:
    def __init__(self):
        self.banner = None
        self.open_called = False
        self.task = None
    def open(self, banner):
        self.banner = banner
        self.open_called = True
    def close(self, banner):
        self.banner = None
    def run_task(self, coro):
        self.task = coro

def test_show_error_opens_banner():
    view = ChatView(ChatBackend("http://invalid"), lambda e: None)
    dummy = DummyPage()
    view.page = dummy
    view.show_error("boom")
    assert dummy.banner is view.error_banner
    assert dummy.open_called
    assert dummy.task is not None
    assert view.error_banner.content.value == "boom"
