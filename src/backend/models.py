from dataclasses import dataclass

@dataclass
class Message:
    """Container representing a chat message with metadata."""
    user_name: str
    text: str
    message_type: str
