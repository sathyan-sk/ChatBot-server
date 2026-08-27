"""Embedding provider contract. Dimension is a property of the resolved
provider+model pair and must be validated against the vector index at startup
(Golden Rule 7: embedding configuration must stay compatible with the vector
index)."""

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class EmbeddingResult:
    vector: list[float]
    dimension: int
    model: str


class EmbeddingProviderInterface(ABC):
    @property
    @abstractmethod
    def dimension(self) -> int:
        """The vector dimension this provider+model produces. Used at startup
        to validate compatibility with the configured vector index."""
        raise NotImplementedError

    @abstractmethod
    async def embed_text(self, text: str) -> EmbeddingResult:
        raise NotImplementedError

    @abstractmethod
    async def embed_batch(self, texts: list[str]) -> list[EmbeddingResult]:
        """Batch embedding for ingestion throughput. Implementations should
        respect provider-side batch size limits internally."""
        raise NotImplementedError

    @abstractmethod
    async def health_check(self) -> bool:
        raise NotImplementedError
