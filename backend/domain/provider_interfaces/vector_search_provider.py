"""Vector search provider contract. RAG services depend on this interface,
never on pgvector directly (architectural rule: RAG service -> VectorSearchProvider
-> pgvector, not RAG service -> pgvector implementation).

Application/knowledge-base scoping is a required parameter on every method —
this is what makes SQL-enforced isolation possible at the provider boundary."""

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class VectorSearchFilter:
    application_id: str
    knowledge_base_id: str
    metadata_filters: dict[str, str] | None = None


@dataclass
class VectorSearchMatch:
    chunk_id: str
    content: str
    score: float
    metadata: dict[str, str]


class VectorSearchProviderInterface(ABC):
    @abstractmethod
    async def upsert_vector(
        self, chunk_id: str, embedding: list[float], metadata: dict[str, str]
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def search(
        self, query_embedding: list[float], search_filter: VectorSearchFilter, top_k: int
    ) -> list[VectorSearchMatch]:
        """Application/knowledge-base isolation MUST be enforced inside this
        query — never applied as a post-fetch Python filter by the caller."""
        raise NotImplementedError

    @abstractmethod
    async def delete_vector(self, chunk_id: str) -> None:
        raise NotImplementedError

    @abstractmethod
    async def health_check(self) -> bool:
        raise NotImplementedError
