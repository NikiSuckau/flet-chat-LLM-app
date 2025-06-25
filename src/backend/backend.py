import json
import requests


class ChatBackend:
    """Simple backend handling chat history and LLM interaction."""

    DEFAULT_SYSTEM_PROMPT = "Du bist ein hilfreicher Assistent."
    DEFAULT_DIARY_PROMPT = (
        "Stelle eine kurze, selbstreflektierende Frage basierend auf folgendem Tagebucheintrag:\n"
    )
    DEFAULT_SUMMARY_PROMPT = (
        "Fasse kurz den folgenden Tagebucheintrag zusammen:\n"
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
        summary_system_prompt: str | None = None,
        summary_prompt: str | None = None,
        summary_temperature: float = 0.5,
        summary_max_tokens: int = 50,
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
        self.summary_system_prompt = summary_system_prompt or self.DEFAULT_SYSTEM_PROMPT
        self.summary_prompt = summary_prompt or self.DEFAULT_SUMMARY_PROMPT
        self.summary_temperature = summary_temperature
        self.summary_max_tokens = summary_max_tokens
        # Seed conversation with a system prompt so the LLM knows how to behave
        self.chat_history = [
            {"role": "system", "content": self.system_prompt}
        ]

    def add_user_message(self, text: str) -> None:
        """Append a user message to the in-memory history."""
        self.chat_history.append({"role": "user", "content": text})

    def add_assistant_message(self, text: str) -> None:
        """Append an assistant message to the in-memory history."""
        self.chat_history.append({"role": "assistant", "content": text})

    def stream_reply(
        self,
        max_tokens: int | None = None,
        temperature: float | None = None,
    ):
        """Yield assistant reply tokens as they arrive from the API."""
        max_tokens = max_tokens if max_tokens is not None else self.max_tokens
        temperature = temperature if temperature is not None else self.temperature
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
            yield f"[error connecting to KoboldCPP: {ex}]"
            return

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
                    yield delta
                if j["choices"][0].get("finish_reason") == "stop":
                    break

    def generate_reply(
        self,
        max_tokens: int | None = None,
        temperature: float | None = None,
    ) -> str:
        """Return the full assistant reply after streaming completes."""
        return "".join(self.stream_reply(max_tokens=max_tokens, temperature=temperature))

    def stream_diary_question(
        self,
        diary_text: str,
        prompt: str | None = None,
        max_tokens: int | None = None,
        temperature: float | None = None,
        system_prompt: str | None = None,
    ):
        """Yield a diary self-reflection question token by token."""

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
                    "stream": True,
                },
                timeout=120,
                stream=True,
            )
            response.raise_for_status()
        except Exception as ex:  # pragma: no cover - network errors
            yield f"[error connecting to KoboldCPP: {ex}]"
            return

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
                    yield delta
                if j["choices"][0].get("finish_reason") == "stop":
                    break

    def generate_diary_question(
        self,
        diary_text: str,
        prompt: str | None = None,
        max_tokens: int | None = None,
        temperature: float | None = None,
        system_prompt: str | None = None,
    ) -> str:
        """Return the full diary question after streaming completes."""

        return "".join(
            self.stream_diary_question(
                diary_text,
                prompt=prompt,
                max_tokens=max_tokens,
                temperature=temperature,
                system_prompt=system_prompt,
            )
        )

    def stream_diary_summary(
        self,
        diary_text: str,
        prompt: str | None = None,
        max_tokens: int | None = None,
        temperature: float | None = None,
        system_prompt: str | None = None,
    ):
        """Yield a summary of the given diary text token by token."""

        prompt_text = (prompt or self.summary_prompt) + f"{diary_text}"
        max_tokens = (
            max_tokens if max_tokens is not None else self.summary_max_tokens
        )
        temperature = (
            temperature if temperature is not None else self.summary_temperature
        )
        system_prompt = system_prompt or self.summary_system_prompt

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
                    "stream": True,
                },
                timeout=120,
                stream=True,
            )
            response.raise_for_status()
        except Exception as ex:  # pragma: no cover - network errors
            yield f"[error connecting to KoboldCPP: {ex}]"
            return

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
                    yield delta
                if j["choices"][0].get("finish_reason") == "stop":
                    break

    def generate_diary_summary(
        self,
        diary_text: str,
        prompt: str | None = None,
        max_tokens: int | None = None,
        temperature: float | None = None,
        system_prompt: str | None = None,
    ) -> str:
        """Return the full diary summary after streaming completes."""

        return "".join(
            self.stream_diary_summary(
                diary_text,
                prompt=prompt,
                max_tokens=max_tokens,
                temperature=temperature,
                system_prompt=system_prompt,
            )
        )
