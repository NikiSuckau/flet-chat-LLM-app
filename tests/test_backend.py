import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1] / 'src'))

import requests
import pytest
from backend import ChatBackend, ChatConnectionError


def test_generate_reply_connection_error(monkeypatch):
    def fake_post(*args, **kwargs):
        raise requests.ConnectionError("boom")

    monkeypatch.setattr(requests, "post", fake_post)
    backend = ChatBackend("http://invalid")
    backend.add_user_message("hi")
    with pytest.raises(ChatConnectionError):
        backend.generate_reply()
