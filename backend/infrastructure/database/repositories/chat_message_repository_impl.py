from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.entities.chat_message import ChatMessage, MessageRole
from domain.repository_interfaces.chat_message_repository import (
    ChatMessageRepositoryInterface,
)
from infrastructure.database.models.chat_message_model import ChatMessageModel


def _to_entity(model: ChatMessageModel) -> ChatMessage:
    return ChatMessage(
        id=model.id,
        conversation_id=model.conversation_id,
        role=MessageRole(model.role),
        content=model.content,
        created_at=model.created_at,
    )


class ChatMessageRepository(ChatMessageRepositoryInterface):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, message: ChatMessage) -> ChatMessage:
        model = ChatMessageModel(
            id=message.id,
            conversation_id=message.conversation_id,
            role=message.role.value,
            content=message.content,
        )
        self._session.add(model)
        await self._session.flush()
        return _to_entity(model)

    async def list_recent_by_conversation(
        self, conversation_id: str, limit: int
    ) -> list[ChatMessage]:
        result = await self._session.execute(
            select(ChatMessageModel)
            .where(ChatMessageModel.conversation_id == conversation_id)
            .order_by(ChatMessageModel.created_at.desc())
            .limit(limit)
        )
        return [_to_entity(m) for m in reversed(result.scalars().all())]
