from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from domain.entities.document_chunk import DocumentChunk


class DocumentChunkRepositoryInterface(ABC):
    @abstractmethod
    async def create_many(self, chunks: list["DocumentChunk"]) -> list["DocumentChunk"]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_data_source(
        self, application_id: str, data_source_id: str
    ) -> list["DocumentChunk"]:
        raise NotImplementedError

    @abstractmethod
    async def delete_by_data_source(self, application_id: str, data_source_id: str) -> None:
        """Prevents orphaned retrieval data when a DataSource is deleted (Section 4)."""
        raise NotImplementedError

    @abstractmethod
    async def keyword_search(
        self, application_id: str, knowledge_base_id: str, query: str, limit: int
    ) -> list["DocumentChunk"]:
        """Application/knowledge-base isolation enforced inside this query,
        never as a post-fetch Python filter (Section 3)."""
        raise NotImplementedError
