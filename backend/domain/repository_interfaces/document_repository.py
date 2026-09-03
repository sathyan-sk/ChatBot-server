from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from domain.entities.data_source import DataSource


class DataSourceRepositoryInterface(ABC):
    @abstractmethod
    async def create(self, data_source: "DataSource") -> "DataSource":
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, application_id: str, data_source_id: str) -> "DataSource | None":
        raise NotImplementedError

    @abstractmethod
    async def list_by_knowledge_base(
        self, application_id: str, knowledge_base_id: str, limit: int = 50, offset: int = 0
    ) -> list["DataSource"]:
        raise NotImplementedError

    @abstractmethod
    async def update_status(self, application_id: str, data_source_id: str, status: str) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, application_id: str, data_source_id: str) -> None:
        """DB-level cascade removes its DocumentChunks and IngestionJobs (Section 4)."""
        raise NotImplementedError
