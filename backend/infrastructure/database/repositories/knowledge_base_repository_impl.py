from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.entities.knowledge_base import KnowledgeBase
from domain.repository_interfaces.knowledge_base_repository import (
    KnowledgeBaseRepositoryInterface,
)
from infrastructure.database.models.knowledge_base_model import KnowledgeBaseModel


def _to_entity(model: KnowledgeBaseModel) -> KnowledgeBase:
    return KnowledgeBase(
        id=model.id, application_id=model.application_id, created_at=model.created_at
    )


class KnowledgeBaseRepository(KnowledgeBaseRepositoryInterface):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, knowledge_base: KnowledgeBase) -> KnowledgeBase:
        model = KnowledgeBaseModel(
            id=knowledge_base.id, application_id=knowledge_base.application_id
        )
        self._session.add(model)
        await self._session.flush()
        return _to_entity(model)

    async def get_by_application_id(self, application_id: str) -> KnowledgeBase | None:
        result = await self._session.execute(
            select(KnowledgeBaseModel).where(KnowledgeBaseModel.application_id == application_id)
        )
        model = result.scalar_one_or_none()
        return _to_entity(model) if model else None
