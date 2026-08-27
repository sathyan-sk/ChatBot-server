from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from domain.entities.knowledge_base import KnowledgeBase


class KnowledgeBaseRepositoryInterface(ABC):
    @abstractmethod
    async def create(self, knowledge_base: "KnowledgeBase") -> "KnowledgeBase":
        raise NotImplementedError

    @abstractmethod
    async def get_by_application_id(self, application_id: str) -> "KnowledgeBase | None":
        raise NotImplementedError
