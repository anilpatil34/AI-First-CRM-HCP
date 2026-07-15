"""
Conversation memory store.
Maintains chat history per session for multi-turn conversations.
"""

from typing import Optional
from collections import defaultdict

MAX_HISTORY = 20  # Max messages per session


class MemoryStore:
    """In-memory conversation history store keyed by session_id."""

    def __init__(self):
        self._store: dict[str, list[dict]] = defaultdict(list)

    def add_message(self, session_id: str, role: str, content: str):
        """Add a message to the session history."""
        self._store[session_id].append({"role": role, "content": content})
        # Trim to max history (keep system prompt + last N messages)
        if len(self._store[session_id]) > MAX_HISTORY:
            self._store[session_id] = self._store[session_id][-MAX_HISTORY:]

    def get_history(self, session_id: str) -> list[dict]:
        """Get conversation history for a session."""
        return list(self._store[session_id])

    def clear_session(self, session_id: str):
        """Clear history for a specific session."""
        self._store.pop(session_id, None)

    def get_session_count(self) -> int:
        """Get number of active sessions."""
        return len(self._store)


# Singleton instance
_memory_store: Optional[MemoryStore] = None


def get_memory_store() -> MemoryStore:
    """Get or create the memory store singleton."""
    global _memory_store
    if _memory_store is None:
        _memory_store = MemoryStore()
    return _memory_store
