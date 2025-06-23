from __future__ import annotations

"""LangMem based long term memory agent."""

from dataclasses import dataclass
from uuid import uuid4

from langgraph.store.memory import InMemoryStore


@dataclass
class MemoryRecord:
    """Single memory entry."""

    key: str
    kind: str
    content: str


class LangMemAgent:
    """Simple wrapper storing memories in an InMemoryStore."""

    def __init__(self) -> None:
        self.store = InMemoryStore()

    def add_memory(self, user: str, kind: str, content: str) -> None:
        """Store a memory entry under the user namespace."""
        key = str(uuid4())
        self.store.put(("memories", user), key, {"kind": kind, "content": content})

    def list_memories(self, user: str) -> list[MemoryRecord]:
        """Return all memories for the given user."""
        items = self.store.search(("memories", user), limit=100)
        return [
            MemoryRecord(key=item.key, kind=item.value.get("kind", ""), content=item.value.get("content", ""))
            for item in items
        ]
