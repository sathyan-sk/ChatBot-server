from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.entities.message_citation import MessageCitation
from domain.repository_interfaces.message_citation_repository import (
    MessageCitationRepositoryInterface,
)
from infrastructure.database.models.message_citation_model import MessageCitationModel


def _to_entity(model: MessageCitationModel) -> MessageCitation:
    return MessageCitation(
        id=model.id,
        message_id=model.message_id,
        chunk_id=model.chunk_id,
        relevance_score=model.relevance_score,
    )


class MessageCitationRepository(MessageCitationRepositoryInterface):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create_many(self, citations: list[MessageCitation]) -> list[MessageCitation]:
        models = [
            MessageCitationModel(
                id=c.id,
                message_id=c.message_id,
                chunk_id=c.chunk_id,
                relevance_score=c.relevance_score,
            )
            for c in citations
        ]
        self._session.add_all(models)
        await self._session.flush()
        return [_to_entity(m) for m in models]

    async def list_by_message(self, message_id: str) -> list[MessageCitation]:
        result = await self._session.execute(
            select(MessageCitationModel).where(MessageCitationModel.message_id == message_id)
        )
        return [_to_entity(m) for m in result.scalars().all()]
