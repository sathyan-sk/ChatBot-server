"""Local cross-encoder reranker. Runs in-process via sentence-transformers.
No network dependency, no API cost — matches budget-conscious stack choice."""

from sentence_transformers import CrossEncoder

from domain.provider_interfaces.reranker_provider import (
    RerankCandidate,
    RerankedResult,
    RerankerProviderInterface,
)
from exceptions.domain_exceptions import ProviderError


class CrossEncoderRerankerProvider(RerankerProviderInterface):
    def __init__(self, model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2") -> None:
        try:
            self._model = CrossEncoder(model_name)
        except Exception as exc:
            raise ProviderError(f"Failed to load cross-encoder model: {exc}") from exc

    async def rerank(
        self, query: str, candidates: list[RerankCandidate], top_n: int
    ) -> list[RerankedResult]:
        if not candidates:
            return []
        pairs = [(query, c.text) for c in candidates]
        try:
            scores = self._model.predict(pairs)
        except Exception as exc:
            raise ProviderError(f"Cross-encoder inference failed: {exc}") from exc

        ranked = sorted(
            zip(candidates, scores, strict=True), key=lambda pair: pair[1], reverse=True
        )
        return [
            RerankedResult(chunk_id=c.chunk_id, relevance_score=float(score))
            for c, score in ranked[:top_n]
        ]

    async def health_check(self) -> bool:
        return self._model is not None
