import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1] / 'src'))

import requests
from backend import ChatBackend


def test_stream_reply_and_generate_reply(monkeypatch):
    chunks = [
        'data: {"choices":[{"delta":{"content":"Hel"}}]}',
        'data: {"choices":[{"delta":{"content":"lo"},"finish_reason":"stop"}]}',
    ]

    def fake_post(url, json, timeout, stream):
        class Resp:
            def raise_for_status(self):
                pass

            def iter_lines(self, decode_unicode=False):
                for line in chunks:
                    yield line if decode_unicode else line.encode()
        return Resp()

    monkeypatch.setattr(requests, "post", fake_post)
    backend = ChatBackend("http://api")

    result = "".join(backend.stream_reply())
    assert result == "Hello"

    monkeypatch.setattr(requests, "post", fake_post)
    assert backend.generate_reply() == "Hello"
