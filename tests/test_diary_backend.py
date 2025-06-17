import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1] / 'src'))

import requests
from backend import ChatBackend


def test_generate_diary_question_uses_settings(monkeypatch):
    captured = {}

    def fake_post(url, json, timeout):
        captured.update(json)
        class Resp:
            def raise_for_status(self):
                pass
            def json(self):
                return {"choices": [{"message": {"content": "ok"}}]}
        return Resp()

    monkeypatch.setattr(requests, "post", fake_post)
    backend = ChatBackend(
        "http://api",
        diary_system_prompt="SYS",
        diary_prompt="PROMPT\n",
        diary_temperature=0.6,
        diary_max_tokens=12,
    )
    backend.generate_diary_question("text")
    assert captured["messages"][0]["content"] == "SYS"
    assert captured["messages"][1]["content"] == "PROMPT\ntext"
    assert captured["temperature"] == 0.6
    assert captured["max_tokens"] == 12
