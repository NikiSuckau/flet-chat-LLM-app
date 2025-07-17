"""Integration tests for memory functionality with the backend."""

import tempfile
import os
from backend import ChatBackend


def test_backend_memory_integration():
    """Test that backend integrates memory context properly."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        # Create backend with memory enabled and custom memory database path
        backend = ChatBackend(
            api_url="http://test-url",
            enable_memory=True
        )
        
        # Override the memory manager's store path to use temp directory
        memory_db_path = os.path.join(tmp_dir, "test_memory.db")
        backend.memory_manager.store.db_path = memory_db_path
        backend.memory_manager.store._init_db()
        
        # Add some user messages with preferences
        backend.add_user_message("Hi, I prefer dark mode in all my applications")
        backend.add_assistant_message("I'll remember that preference")
        backend.add_user_message("My name is Alice and I work as a software developer")
        backend.add_assistant_message("Nice to meet you Alice!")
        
        # Get context-enriched messages
        messages = backend.get_context_enriched_messages("Alice")
        
        # Should have the original system message
        assert messages[0]["role"] == "system"
        
        # The system message should now include memory context about the user
        system_content = messages[0]["content"]
        assert "dark mode" in system_content.lower() or "preference" in system_content.lower()


def test_backend_memory_disabled():
    """Test that backend works correctly when memory is disabled."""
    backend = ChatBackend(
        api_url="http://test-url", 
        enable_memory=False
    )
    
    # Memory manager should be None
    assert backend.memory_manager is None
    
    # Add some messages
    backend.add_user_message("I prefer dark mode")
    backend.add_assistant_message("OK")
    
    # Get messages - should be unchanged from original
    messages = backend.get_context_enriched_messages("TestUser")
    
    # Should have original system message without memory context
    assert messages[0]["role"] == "system"
    assert "dark mode" not in messages[0]["content"].lower()


def test_memory_context_with_relevant_conversation():
    """Test that memory context is added when there's a relevant conversation."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        backend = ChatBackend(
            api_url="http://test-url",
            enable_memory=True
        )
        
        # Override the memory manager's store path
        memory_db_path = os.path.join(tmp_dir, "test_memory.db")
        backend.memory_manager.store.db_path = memory_db_path
        backend.memory_manager.store._init_db()
        
        # First conversation - establish preferences
        backend.add_user_message("I love using dark themes")
        backend.add_assistant_message("Noted!")
        
        # Process the conversation to extract memories
        backend.get_context_enriched_messages("User")
        
        # Clear chat history but keep the system message
        backend.chat_history = [backend.chat_history[0]]  # Keep system message only
        
        # New conversation about themes
        backend.add_user_message("What's the best theme for coding?")
        
        # Get enriched messages - should include memory about dark themes
        messages = backend.get_context_enriched_messages("User")
        
        system_content = messages[0]["content"]
        assert "dark" in system_content.lower() or "preference" in system_content.lower()


def test_memory_extraction_from_conversation():
    """Test that memories are extracted and stored during conversation processing."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        backend = ChatBackend(
            api_url="http://test-url",
            enable_memory=True
        )
        
        # Override the memory manager's store path
        memory_db_path = os.path.join(tmp_dir, "test_memory.db")
        backend.memory_manager.store.db_path = memory_db_path
        backend.memory_manager.store._init_db()
        
        # Add messages that should create memories
        backend.add_user_message("I prefer working late at night")
        backend.add_user_message("My goal is to learn machine learning")
        
        # Process the conversation
        context = backend.memory_manager.process_conversation(backend.chat_history, "TestUser")
        
        # Check that memories were stored
        stored_memories = backend.memory_manager.store.get_recent_memories(10)
        
        # Should have extracted preferences and goals
        preference_memories = [m for m in stored_memories if m.category == "preference"]
        goal_memories = [m for m in stored_memories if m.category == "goals_interests"]
        
        assert len(preference_memories) >= 1
        assert len(goal_memories) >= 1
        
        # Check content
        assert any("late at night" in m.content for m in preference_memories)
        assert any("machine learning" in m.content for m in goal_memories)