from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from domain.entities.chat_message import ChatMessage


class ChatMessageRepositoryInterface(ABC):
    @abstractmethod
    async def create(self, message: "ChatMessage") -> "ChatMessage":
        raise NotImplementedError

    @abstractmethod
    async def list_recent_by_conversation(
        self, conversation_id: str, limit: int
    ) -> list["ChatMessage"]:
        """Bounded query — ORDER BY created_at DESC LIMIT N. Never loads the
        full conversation history (Section 6). This is where the
        context-window policy is enforced, separately from retention."""
        raise NotImplementedError
