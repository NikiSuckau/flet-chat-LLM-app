"""Tests for memory manager functionality."""

import pytest
import tempfile
import os
from datetime import datetime

from backend.memory_manager import MemoryManager, SimpleMemoryStore, UserMemory


def test_memory_store_init():
    """Test that memory store initializes correctly."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        db_path = os.path.join(tmp_dir, "test_memory.db")
        store = SimpleMemoryStore(db_path)
        assert os.path.exists(db_path)


def test_store_and_retrieve_memory():
    """Test storing and retrieving memories."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        db_path = os.path.join(tmp_dir, "test_memory.db")
        store = SimpleMemoryStore(db_path)
        
        memory = UserMemory(
            category="preference",
            content="I prefer dark mode",
            context="User expressed UI preference",
            timestamp=datetime.now().isoformat()
        )
        
        store.store_memory(memory)
        
        # Search for the memory
        results = store.search_memories("dark mode")
        assert len(results) == 1
        assert results[0].content == "I prefer dark mode"
        assert results[0].category == "preference"


def test_memory_extraction():
    """Test memory extraction from conversations."""
    manager = MemoryManager()
    
    messages = [
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "Hi, I prefer dark mode in all my apps"},
        {"role": "assistant", "content": "I'll remember that you prefer dark mode"},
        {"role": "user", "content": "My name is John and I work as a software engineer"}
    ]
    
    memories = manager.extract_memories_from_conversation(messages, "John")
    
    # Should extract at least 2 memories: preference and personal info
    assert len(memories) >= 2
    
    # Check for preference memory
    preference_memories = [m for m in memories if m.category == "preference"]
    assert len(preference_memories) >= 1
    assert "dark mode" in preference_memories[0].content.lower()
    
    # Check for personal info memory
    personal_memories = [m for m in memories if m.category == "personal_info"]
    assert len(personal_memories) >= 1
    assert "john" in personal_memories[0].content.lower()


def test_relevant_context_generation():
    """Test that relevant context is generated from stored memories."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        db_path = os.path.join(tmp_dir, "test_memory.db")
        manager = MemoryManager(SimpleMemoryStore(db_path))
        
        # Store some memories
        memories = [
            UserMemory(
                category="preference",
                content="I prefer dark mode",
                context="UI preference",
                timestamp=datetime.now().isoformat()
            ),
            UserMemory(
                category="personal_info", 
                content="My name is Alice",
                context="Personal info",
                timestamp=datetime.now().isoformat()
            )
        ]
        
        manager.store_memories(memories)
        
        # Get relevant context
        context = manager.get_relevant_context("What theme should I use?")
        
        assert "dark mode" in context.lower()
        assert "preference" in context.lower()


def test_process_conversation():
    """Test full conversation processing with memory extraction and context generation."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        db_path = os.path.join(tmp_dir, "test_memory.db")
        manager = MemoryManager(SimpleMemoryStore(db_path))
        
        messages = [
            {"role": "system", "content": "You are helpful"},
            {"role": "user", "content": "I love learning about artificial intelligence"},
            {"role": "assistant", "content": "That's great!"}
        ]
        
        # Process conversation
        context = manager.process_conversation(messages, "TestUser")
        
        # Context might be empty for the first message, but memories should be stored
        stored_memories = manager.store.get_recent_memories(10)
        
        # Should have extracted the interest in AI
        ai_memories = [m for m in stored_memories if "artificial intelligence" in m.content.lower()]
        assert len(ai_memories) >= 1


def test_search_memories_with_no_results():
    """Test searching for memories when none match."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        db_path = os.path.join(tmp_dir, "test_memory.db")
        store = SimpleMemoryStore(db_path)
        
        results = store.search_memories("nonexistent topic")
        assert len(results) == 0


def test_get_recent_memories():
    """Test getting recent memories."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        db_path = os.path.join(tmp_dir, "test_memory.db")
        store = SimpleMemoryStore(db_path)
        
        # Store multiple memories
        for i in range(5):
            memory = UserMemory(
                category="test",
                content=f"Test memory {i}",
                context=f"Test context {i}",
                timestamp=datetime.now().isoformat()
            )
            store.store_memory(memory)
        
        recent = store.get_recent_memories(3)
        assert len(recent) == 3
        
        # Should be in reverse chronological order (most recent first)
        # The most recent memory should be "Test memory 4" and should be first in the list
        assert "Test memory 4" in recent[0].content