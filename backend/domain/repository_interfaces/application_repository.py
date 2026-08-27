from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from domain.entities.application import Application


class ApplicationRepositoryInterface(ABC):
    @abstractmethod
    async def create(self, application: "Application") -> "Application":
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, application_id: str) -> "Application | None":
        raise NotImplementedError

    @abstractmethod
    async def get_by_slug(self, slug: str) -> "Application | None":
        raise NotImplementedError

    @abstractmethod
    async def list_all(self, limit: int = 50, offset: int = 0) -> list["Application"]:
        raise NotImplementedError

    @abstractmethod
    async def update(self, application: "Application") -> "Application":
        raise NotImplementedError

    @abstractmethod
    async def delete(self, application_id: str) -> None:
        """DB-level cascade removes all owned entities (Section 4)."""
        raise NotImplementedError
