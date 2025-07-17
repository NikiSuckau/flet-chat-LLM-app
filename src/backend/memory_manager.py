"""Simple memory manager using LangMem for long-term conversation memory."""

import json
import os
from dataclasses import asdict, dataclass
from typing import List, Dict, Any, Optional
from datetime import datetime
import asyncio
import sqlite3

from pydantic import BaseModel


STORAGE_DIR = "storage/data"
MEMORY_DB = os.path.join(STORAGE_DIR, "memory.db")


class UserMemory(BaseModel):
    """Store user preferences and information."""
    category: str
    content: str
    context: str
    timestamp: str


@dataclass
class SimpleMemoryStore:
    """Simple file-based memory store that mimics basic LangMem functionality."""
    
    def __init__(self, db_path: str = MEMORY_DB):
        """Initialize the memory store with SQLite database."""
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        """Initialize the SQLite database for memory storage."""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS memories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category TEXT NOT NULL,
                    content TEXT NOT NULL,
                    context TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()
    
    def store_memory(self, memory: UserMemory) -> None:
        """Store a new memory in the database."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT INTO memories (category, content, context, timestamp) VALUES (?, ?, ?, ?)",
                (memory.category, memory.content, memory.context, memory.timestamp)
            )
            conn.commit()
    
    def search_memories(self, query: str, limit: int = 5) -> List[UserMemory]:
        """Search for relevant memories based on a query."""
        with sqlite3.connect(self.db_path) as conn:
            # Simple text search - in production this could use vector similarity
            # Search in content, context, and category fields
            search_pattern = f'%{query}%'
            cursor = conn.execute("""
                SELECT category, content, context, timestamp
                FROM memories 
                WHERE content LIKE ? OR context LIKE ? OR category LIKE ?
                ORDER BY id DESC
                LIMIT ?
            """, (search_pattern, search_pattern, search_pattern, limit))
            
            results = []
            for row in cursor.fetchall():
                results.append(UserMemory(
                    category=row[0],
                    content=row[1], 
                    context=row[2],
                    timestamp=row[3]
                ))
            
            # If no direct matches, try broader search with individual words
            if not results and ' ' in query:
                words = query.split()
                for word in words:
                    if len(word) > 2:  # Skip very short words
                        word_pattern = f'%{word}%'
                        cursor = conn.execute("""
                            SELECT category, content, context, timestamp
                            FROM memories 
                            WHERE content LIKE ? OR context LIKE ? OR category LIKE ?
                            ORDER BY id DESC
                            LIMIT ?
                        """, (word_pattern, word_pattern, word_pattern, limit))
                        
                        for row in cursor.fetchall():
                            memory = UserMemory(
                                category=row[0],
                                content=row[1],
                                context=row[2],
                                timestamp=row[3]
                            )
                            if memory not in results:  # Avoid duplicates
                                results.append(memory)
                                if len(results) >= limit:
                                    break
                        if len(results) >= limit:
                            break
            
            return results
    
    def get_recent_memories(self, limit: int = 10) -> List[UserMemory]:
        """Get the most recent memories."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                SELECT category, content, context, timestamp
                FROM memories 
                ORDER BY id DESC
                LIMIT ?
            """, (limit,))
            
            results = []
            for row in cursor.fetchall():
                results.append(UserMemory(
                    category=row[0],
                    content=row[1],
                    context=row[2],
                    timestamp=row[3]
                ))
            return results


class MemoryManager:
    """Manages long-term memory extraction and retrieval."""
    
    def __init__(self, store: SimpleMemoryStore = None):
        """Initialize with a memory store."""
        self.store = store or SimpleMemoryStore()
    
    def extract_memories_from_conversation(self, messages: List[Dict[str, str]], user_name: str = "User") -> List[UserMemory]:
        """Extract important information from conversation messages."""
        memories = []
        
        # Simple rule-based extraction - could be enhanced with LLM analysis
        user_messages = [msg for msg in messages if msg.get("role") == "user"]
        
        for msg in user_messages:
            content = msg.get("content", "")
            
            # Extract preferences
            if any(word in content.lower() for word in ["prefer", "like", "love", "favorite", "hate", "dislike"]):
                memories.append(UserMemory(
                    category="preference",
                    content=content,
                    context=f"User expressed preferences",
                    timestamp=datetime.now().isoformat()
                ))
            
            # Extract personal information
            if any(word in content.lower() for word in ["my name is", "i am", "i work", "i live", "my job"]):
                memories.append(UserMemory(
                    category="personal_info",
                    content=content,
                    context=f"User shared personal information",
                    timestamp=datetime.now().isoformat()
                ))
            
            # Extract goals and interests
            if any(word in content.lower() for word in ["want to", "trying to", "learning", "interested in", "goal"]):
                memories.append(UserMemory(
                    category="goals_interests",
                    content=content,
                    context=f"User mentioned goals or interests",
                    timestamp=datetime.now().isoformat()
                ))
        
        return memories
    
    def store_memories(self, memories: List[UserMemory]) -> None:
        """Store multiple memories."""
        for memory in memories:
            self.store.store_memory(memory)
    
    def get_relevant_context(self, current_message: str, limit: int = 3) -> str:
        """Get relevant memories to include in chat context."""
        # Try direct search first
        relevant_memories = self.store.search_memories(current_message, limit=limit)
        
        # If no direct matches, try searching for theme-related concepts if message is about themes/UI
        if not relevant_memories and any(word in current_message.lower() for word in ['theme', 'mode', 'appearance', 'ui', 'interface']):
            relevant_memories = self.store.search_memories("mode", limit=limit)
            if not relevant_memories:
                relevant_memories = self.store.search_memories("preference", limit=limit)
        
        # If still no relevant memories, get some recent memories
        if not relevant_memories:
            relevant_memories = self.store.get_recent_memories(limit=min(limit, 2))
        
        if not relevant_memories:
            return ""
        
        context_parts = ["Relevant information about the user:"]
        for memory in relevant_memories:
            context_parts.append(f"- {memory.category}: {memory.content}")
        
        return "\n".join(context_parts)
    
    def process_conversation(self, messages: List[Dict[str, str]], user_name: str = "User") -> str:
        """Process conversation and return relevant context for the LLM."""
        # Extract and store new memories
        new_memories = self.extract_memories_from_conversation(messages, user_name)
        if new_memories:
            self.store_memories(new_memories)
        
        # Get relevant context for current conversation
        if messages:
            last_message = messages[-1].get("content", "")
            return self.get_relevant_context(last_message)
        
        return ""