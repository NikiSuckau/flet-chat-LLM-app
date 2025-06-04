from dataclasses import dataclass

@dataclass
class Message:
    user_name: str
    text: str
    message_type: str
