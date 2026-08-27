from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from domain.entities.message_citation import MessageCitation


class MessageCitationRepositoryInterface(ABC):
    @abstractmethod
    async def create_many(self, citations: list["MessageCitation"]) -> list["MessageCitation"]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_message(self, message_id: str) -> list["MessageCitation"]:
        raise NotImplementedError
