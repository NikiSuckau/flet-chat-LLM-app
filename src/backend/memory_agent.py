"""LangMem agent storing user memories using the hot path approach."""

from __future__ import annotations

from langgraph.store.memory import InMemoryStore
from langmem import create_manage_memory_tool


class LangMemAgent:
    """Minimal wrapper around LangMem's manage_memory tool."""

    def __init__(self, store: InMemoryStore | None = None) -> None:
        self.store = store or InMemoryStore()
        self._tool = create_manage_memory_tool(namespace=("memories",), store=self.store)

    def save(self, text: str) -> None:
        """Persist a new memory about the user."""
        self._tool.invoke({"content": text})


