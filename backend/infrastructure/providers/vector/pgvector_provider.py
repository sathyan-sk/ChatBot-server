"""pgvector implementation of VectorSearchProviderInterface. This is the ONLY
file in the codebase that runs a raw vector similarity SQL query — RAG
services call VectorSearchProviderInterface, never this class or raw SQL
directly (Section 20.5)."""

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from domain.provider_interfaces.vector_search_provider import (
    VectorSearchFilter,
    VectorSearchMatch,
    VectorSearchProviderInterface,
)
from exceptions.domain_exceptions import ProviderError


class PgVectorSearchProvider(VectorSearchProviderInterface):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def upsert_vector(
        self, chunk_id: str, embedding: list[float], metadata: dict[str, str]
    ) -> None:
        try:
            await self._session.execute(
                text("UPDATE document_chunks SET embedding = :embedding WHERE id = :chunk_id"),
                {"embedding": str(embedding), "chunk_id": chunk_id},
            )
            await self._session.flush()
        except Exception as exc:
            raise ProviderError(f"pgvector upsert failed: {exc}") from exc

    async def search(
        self, query_embedding: list[float], search_filter: VectorSearchFilter, top_k: int
    ) -> list[VectorSearchMatch]:
        try:
            result = await self._session.execute(
                text(
                    """
                    SELECT id, content, metadata_json,
                           1 - (embedding <=> CAST(:query_embedding AS vector)) AS score
                    FROM document_chunks
                    WHERE application_id = :application_id
                      AND knowledge_base_id = :knowledge_base_id
                    ORDER BY embedding <=> CAST(:query_embedding AS vector)
                    LIMIT :top_k
                    """
                ),
                {
                    "query_embedding": str(query_embedding),
                    "application_id": search_filter.application_id,
                    "knowledge_base_id": search_filter.knowledge_base_id,
                    "top_k": top_k,
                },
            )
            rows = result.fetchall()
        except Exception as exc:
            raise ProviderError(f"pgvector search failed: {exc}") from exc

        return [
            VectorSearchMatch(
                chunk_id=row.id,
                content=row.content,
                score=float(row.score),
                metadata=row.metadata_json or {},
            )
            for row in rows
        ]

    async def delete_vector(self, chunk_id: str) -> None:
        try:
            await self._session.execute(
                text("UPDATE document_chunks SET embedding = NULL WHERE id = :chunk_id"),
                {"chunk_id": chunk_id},
            )
            await self._session.flush()
        except Exception as exc:
            raise ProviderError(f"pgvector delete failed: {exc}") from exc

    async def health_check(self) -> bool:
        try:
            await self._session.execute(text("SELECT 1"))
            return True
        except Exception:
            return False
