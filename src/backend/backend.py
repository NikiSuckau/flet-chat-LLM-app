import json
import requests


class ChatBackend:
    """Simple backend handling chat history and LLM interaction."""

    DEFAULT_SYSTEM_PROMPT = "Du bist ein hilfreicher Assistent."

    def __init__(self, api_url: str):
        """Initialize backend with API URL and starting system prompt."""
        self.api_url = api_url
        # Seed conversation with a system prompt so the LLM knows how to behave
        self.chat_history = [
            {"role": "system", "content": self.DEFAULT_SYSTEM_PROMPT}
        ]

    def add_user_message(self, text: str) -> None:
        """Append a user message to the in-memory history."""
        self.chat_history.append({"role": "user", "content": text})

    def add_assistant_message(self, text: str) -> None:
        """Append an assistant message to the in-memory history."""
        self.chat_history.append({"role": "assistant", "content": text})

    def generate_reply(self, max_tokens: int = 200, temperature: float = 0.8) -> str:
        """Generate a reply using the entire chat history."""
        # Send the accumulated conversation to the KoboldCPP API and stream back
        # the assistant's response. Errors are swallowed and returned as a string
        # so the UI can display them directly.
        try:
            response = requests.post(
                self.api_url,
                json={
                    "model": "kobold_chat_v2",
                    "messages": self.chat_history,
                    "max_tokens": max_tokens,
                    "temperature": temperature,
                    "stream": True,
                },
                timeout=(5, 120),
                stream=True,
            )
            response.raise_for_status()
        except requests.RequestException as ex:  # pragma: no cover - network errors
            return f"[error connecting to KoboldCPP: {ex}]"

        bot_reply = ""
        try:
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
        except requests.RequestException as ex:  # pragma: no cover - network errors
            return f"[error connecting to KoboldCPP: {ex}]"
        # Return the full assistant response after streaming ends
        return bot_reply
