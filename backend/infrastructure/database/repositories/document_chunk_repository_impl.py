from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.entities.document_chunk import DocumentChunk
from domain.repository_interfaces.document_chunk_repository import (
    DocumentChunkRepositoryInterface,
)
from infrastructure.database.models.document_chunk_model import DocumentChunkModel


def _to_entity(model: DocumentChunkModel) -> DocumentChunk:
    return DocumentChunk(
        id=model.id,
        application_id=model.application_id,
        knowledge_base_id=model.knowledge_base_id,
        data_source_id=model.data_source_id,
        content=model.content,
        chunk_order=model.chunk_order,
        embedding_model=model.embedding_model,
        embedding_dimension=model.embedding_dimension,
        created_at=model.created_at,
        metadata=model.metadata_json or {},
    )


class DocumentChunkRepository(DocumentChunkRepositoryInterface):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create_many(self, chunks: list[DocumentChunk]) -> list[DocumentChunk]:
        models = [
            DocumentChunkModel(
                id=c.id,
                application_id=c.application_id,
                knowledge_base_id=c.knowledge_base_id,
                data_source_id=c.data_source_id,
                content=c.content,
                chunk_order=c.chunk_order,
                embedding=[],  # populated by ingestion pipeline via VectorSearchProvider.upsert_vector
                embedding_model=c.embedding_model,
                embedding_dimension=c.embedding_dimension,
                metadata_json=c.metadata,
            )
            for c in chunks
        ]
        self._session.add_all(models)
        await self._session.flush()
        return [_to_entity(m) for m in models]

    async def list_by_data_source(
        self, application_id: str, data_source_id: str
    ) -> list[DocumentChunk]:
        result = await self._session.execute(
            select(DocumentChunkModel)
            .where(
                DocumentChunkModel.application_id == application_id,
                DocumentChunkModel.data_source_id == data_source_id,
            )
            .order_by(DocumentChunkModel.chunk_order.asc())
        )
        return [_to_entity(m) for m in result.scalars().all()]

    async def delete_by_data_source(self, application_id: str, data_source_id: str) -> None:
        result = await self._session.execute(
            select(DocumentChunkModel).where(
                DocumentChunkModel.application_id == application_id,
                DocumentChunkModel.data_source_id == data_source_id,
            )
        )
        for model in result.scalars().all():
            await self._session.delete(model)
        await self._session.flush()

    async def keyword_search(
        self, application_id: str, knowledge_base_id: str, query: str, limit: int
    ) -> list[DocumentChunk]:
        result = await self._session.execute(
            select(DocumentChunkModel)
            .where(
                DocumentChunkModel.application_id == application_id,
                DocumentChunkModel.knowledge_base_id == knowledge_base_id,
                DocumentChunkModel.content.ilike(f"%{query}%"),
            )
            .limit(limit)
        )
        return [_to_entity(m) for m in result.scalars().all()]


"""
Note: embedding=[] in create_many is intentional — chunk rows are created first for their IDs,then
the ingestion pipeline calls VectorSearchProvider.upsert_vector() per chunk to populate the actual vector,
keeping the vector-write path exclusively behind the VectorSearchProviderInterface (Section 20.5),
never written directly by the repository
"""
