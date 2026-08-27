"""Ollama embedding provider — runs locally, no API key/cost. Matches your
stated preference for cost-effective, self-hosted providers. Swappable via
EMBEDDING_PROVIDER config without touching any calling code."""

import httpx

from domain.provider_interfaces.embedding_provider import (
    EmbeddingProviderInterface,
    EmbeddingResult,
)
from exceptions.domain_exceptions import ProviderError


class OllamaEmbeddingProvider(EmbeddingProviderInterface):
    def __init__(
        self, base_url: str, model: str, dimension: int, timeout_seconds: float = 30.0
    ) -> None:
        self._base_url = base_url.rstrip("/")
        self._model = model
        self._dimension = dimension
        self._timeout = timeout_seconds

    @property
    def dimension(self) -> int:
        return self._dimension

    async def embed_text(self, text: str) -> EmbeddingResult:
        results = await self.embed_batch([text])
        return results[0]

    async def embed_batch(self, texts: list[str]) -> list[EmbeddingResult]:
        results: list[EmbeddingResult] = []
        try:
            async with httpx.AsyncClient(timeout=self._timeout) as client:
                for text in texts:
                    response = await client.post(
                        f"{self._base_url}/api/embeddings",
                        json={"model": self._model, "prompt": text},
                    )
                    response.raise_for_status()
                    data = response.json()
                    vector = data.get("embedding")
                    if not vector or len(vector) != self._dimension:
                        raise ProviderError(
                            f"Ollama returned embedding of unexpected dimension: "
                            f"expected {self._dimension}, got {len(vector) if vector else 0}"
                        )
                    results.append(
                        EmbeddingResult(vector=vector, dimension=len(vector), model=self._model)
                    )
        except httpx.HTTPError as exc:
            raise ProviderError(f"Ollama embedding request failed: {exc}") from exc
        return results

    async def health_check(self) -> bool:
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(f"{self._base_url}/api/tags")
                return response.status_code == 200
        except httpx.HTTPError:
            return False
