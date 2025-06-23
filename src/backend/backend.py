import json
import requests


class ChatBackend:
    """Simple backend handling chat history and LLM interaction."""

    DEFAULT_SYSTEM_PROMPT = "Du bist ein hilfreicher Assistent."
    DEFAULT_DIARY_PROMPT = (
        "Stelle eine kurze, selbstreflektierende Frage basierend auf folgendem Tagebucheintrag:\n"
    )

    def __init__(
        self,
        api_url: str,
        system_prompt: str | None = None,
        temperature: float = 0.8,
        max_tokens: int = 200,
        diary_system_prompt: str | None = None,
        diary_prompt: str | None = None,
        diary_temperature: float = 0.7,
        diary_max_tokens: int = 50,
        *,
        memory_agent: "LangMemAgent | None" = None,
        user_name: str | None = None,
    ) -> None:
        """Initialize backend with all LLM parameters."""
        self.api_url = api_url
        self.system_prompt = system_prompt or self.DEFAULT_SYSTEM_PROMPT
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.diary_system_prompt = diary_system_prompt or self.DEFAULT_SYSTEM_PROMPT
        self.diary_prompt = diary_prompt or self.DEFAULT_DIARY_PROMPT
        self.diary_temperature = diary_temperature
        self.diary_max_tokens = diary_max_tokens
        self.memory_agent = memory_agent
        self.user_name = user_name or "User"
        # Seed conversation with a system prompt so the LLM knows how to behave
        self.chat_history = [
            {"role": "system", "content": self.system_prompt}
        ]

    def add_user_message(self, text: str) -> None:
        """Append a user message to the in-memory history."""
        self.chat_history.append({"role": "user", "content": text})
        if self.memory_agent:
            self.memory_agent.add_memory(self.user_name, "user", text)

    def add_assistant_message(self, text: str) -> None:
        """Append an assistant message to the in-memory history."""
        self.chat_history.append({"role": "assistant", "content": text})
        if self.memory_agent:
            self.memory_agent.add_memory(self.user_name, "assistant", text)

    def generate_reply(
        self,
        max_tokens: int | None = None,
        temperature: float | None = None,
    ) -> str:
        """Generate a reply using the entire chat history."""
        max_tokens = max_tokens if max_tokens is not None else self.max_tokens
        temperature = temperature if temperature is not None else self.temperature
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
        # Return the full assistant response after streaming ends
        return bot_reply

    def generate_diary_question(
        self,
        diary_text: str,
        prompt: str | None = None,
        max_tokens: int | None = None,
        temperature: float | None = None,
        system_prompt: str | None = None,
    ) -> str:
        """Generate a self-reflection question for a diary entry."""
        prompt_text = (prompt or self.diary_prompt) + f"{diary_text}"
        max_tokens = max_tokens if max_tokens is not None else self.diary_max_tokens
        temperature = temperature if temperature is not None else self.diary_temperature
        system_prompt = system_prompt or self.diary_system_prompt
        try:
            response = requests.post(
                self.api_url,
                json={
                    "model": "kobold_chat_v2",
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": prompt_text},
                    ],
                    "max_tokens": max_tokens,
                    "temperature": temperature,
                },
                timeout=120,
            )
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"].strip()
        except Exception as ex:  # pragma: no cover - network errors
            return f"[error connecting to KoboldCPP: {ex}]"
