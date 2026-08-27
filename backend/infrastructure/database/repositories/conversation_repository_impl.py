from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.entities.conversation import Conversation, ConversationState
from domain.repository_interfaces.conversation_repository import (
    ConversationRepositoryInterface,
)
from infrastructure.database.models.conversation_model import ConversationModel


def _to_entity(model: ConversationModel) -> Conversation:
    return Conversation(
        id=model.id,
        application_id=model.application_id,
        conversation_identity=model.conversation_identity,
        state=ConversationState(model.state),
        created_at=model.created_at,
        last_activity_at=model.last_activity_at,
        expires_at=model.expires_at,
    )


class ConversationRepository(ConversationRepositoryInterface):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, conversation: Conversation) -> Conversation:
        model = ConversationModel(
            id=conversation.id,
            application_id=conversation.application_id,
            conversation_identity=conversation.conversation_identity,
            state=conversation.state.value,
            last_activity_at=conversation.last_activity_at,
            expires_at=conversation.expires_at,
        )
        self._session.add(model)
        await self._session.flush()
        return _to_entity(model)

    async def get_by_identity(
        self, application_id: str, conversation_identity: str
    ) -> Conversation | None:
        result = await self._session.execute(
            select(ConversationModel).where(
                ConversationModel.application_id == application_id,
                ConversationModel.conversation_identity == conversation_identity,
                ConversationModel.state == ConversationState.ACTIVE.value,
            )
        )
        model = result.scalar_one_or_none()
        return _to_entity(model) if model else None

    async def touch_last_activity(self, conversation_id: str) -> None:
        result = await self._session.execute(
            select(ConversationModel).where(ConversationModel.id == conversation_id)
        )
        model = result.scalar_one()
        model.last_activity_at = datetime.now(UTC)
        await self._session.flush()

    async def list_expired(self, before_timestamp: str) -> list[Conversation]:
        result = await self._session.execute(
            select(ConversationModel).where(
                ConversationModel.expires_at < before_timestamp,
                ConversationModel.state == ConversationState.ACTIVE.value,
            )
        )
        return [_to_entity(m) for m in result.scalars().all()]

    async def archive(self, conversation_id: str) -> None:
        result = await self._session.execute(
            select(ConversationModel).where(ConversationModel.id == conversation_id)
        )
        model = result.scalar_one()
        model.state = ConversationState.ARCHIVED.value
        await self._session.flush()
