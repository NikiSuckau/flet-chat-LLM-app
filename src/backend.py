import json
import requests
from typing import Optional


class ChatBackend:
    """Simple backend handling chat history and LLM interaction."""

    DEFAULT_SYSTEM_PROMPT = "Du bist ein hilfreicher Assistent."

    def __init__(self, api_url: str, api_key: str = ""):
        self.api_url = api_url
        self.api_key = api_key
        self.chat_history = [
            {"role": "system", "content": self.DEFAULT_SYSTEM_PROMPT}
        ]

    def set_api_key(self, api_key: str) -> None:
        self.api_key = api_key

    def add_user_message(self, text: str) -> None:
        self.chat_history.append({"role": "user", "content": text})

    def add_assistant_message(self, text: str) -> None:
        self.chat_history.append({"role": "assistant", "content": text})

    def generate_reply(self, max_tokens: int = 200, temperature: float = 0.8) -> str:
        """Generate a reply using the entire chat history."""
        try:
            headers = {}
            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"
            response = requests.post(
                self.api_url,
                json={
                    "model": "kobold_chat_v2",
                    "messages": self.chat_history,
                    "max_tokens": max_tokens,
                    "temperature": temperature,
                    "stream": True,
                },
                headers=headers,
                timeout=120,
                stream=True,
            )
            response.raise_for_status()
        except Exception as ex:  # pragma: no cover - network errors
            return f"[error connecting to KoboldCPP: {ex}]"

        bot_reply = ""
        for chunk in response.iter_lines(decode_unicode=True):
            if not chunk:
                continue
            if chunk.startswith("data:"):
                json_str = chunk[len("data:"):].strip()
                try:
                    j = json.loads(json_str)
                except json.JSONDecodeError:
                    continue
                delta = j["choices"][0]["delta"].get("content", "")
                if delta:
                    bot_reply += delta
                if j["choices"][0].get("finish_reason") == "stop":
                    break
        return bot_reply
