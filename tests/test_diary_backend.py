import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1] / 'src'))

import requests
from backend import ChatBackend


def test_stream_diary_question_and_generate(monkeypatch):
    chunks = [
        'data: {"choices":[{"delta":{"content":"Hel"}}]}',
        'data: {"choices":[{"delta":{"content":"lo"},"finish_reason":"stop"}]}',
    ]
    captured = {}

    def fake_post(url, json, timeout, stream):
        captured.update(json)

        class Resp:
            def raise_for_status(self):
                pass

            def iter_lines(self, decode_unicode=False):
                for line in chunks:
                    yield line if decode_unicode else line.encode()

        return Resp()

    monkeypatch.setattr(requests, "post", fake_post)
    backend = ChatBackend(
        "http://api",
        diary_system_prompt="SYS",
        diary_prompt="PROMPT\n",
        diary_temperature=0.6,
        diary_max_tokens=12,
    )

    result = "".join(backend.stream_diary_question("text"))
    assert result == "Hello"
    assert captured["messages"][0]["content"] == "SYS"
    assert captured["messages"][1]["content"] == "PROMPT\ntext"
    assert captured["temperature"] == 0.6
    assert captured["max_tokens"] == 12

    monkeypatch.setattr(requests, "post", fake_post)
    assert backend.generate_diary_question("text") == "Hello"
