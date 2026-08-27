from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from domain.entities.conversation import Conversation


class ConversationRepositoryInterface(ABC):
    @abstractmethod
    async def create(self, conversation: "Conversation") -> "Conversation":
        raise NotImplementedError

    @abstractmethod
    async def get_by_identity(
        self, application_id: str, conversation_identity: str
    ) -> "Conversation | None":
        raise NotImplementedError

    @abstractmethod
    async def touch_last_activity(self, conversation_id: str) -> None:
        raise NotImplementedError

    @abstractmethod
    async def list_expired(self, before_timestamp: str) -> list["Conversation"]:
        """Supports the background conversation-cleanup job (Section 20.11)."""
        raise NotImplementedError

    @abstractmethod
    async def archive(self, conversation_id: str) -> None:
        raise NotImplementedError
