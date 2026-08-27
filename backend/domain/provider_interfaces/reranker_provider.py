"""Reranker provider contract. Takes a bounded candidate set (already reduced
by retrieval) and returns a relevance-ordered subset — never operates on an
unbounded result set."""

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class RerankCandidate:
    chunk_id: str
    text: str
    initial_score: float


@dataclass
class RerankedResult:
    chunk_id: str
    relevance_score: float


class RerankerProviderInterface(ABC):
    @abstractmethod
    async def rerank(
        self, query: str, candidates: list[RerankCandidate], top_n: int
    ) -> list[RerankedResult]:
        """Returns at most top_n results, ordered by descending relevance."""
        raise NotImplementedError

    @abstractmethod
    async def health_check(self) -> bool:
        raise NotImplementedError
