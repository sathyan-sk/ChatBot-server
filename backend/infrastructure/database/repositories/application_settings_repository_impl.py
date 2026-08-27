from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.entities.application_settings import ApplicationSettings
from domain.repository_interfaces.application_settings_repository import (
    ApplicationSettingsRepositoryInterface,
)
from infrastructure.database.models.application_settings_model import (
    ApplicationSettingsModel,
)


def _to_entity(model: ApplicationSettingsModel) -> ApplicationSettings:
    return ApplicationSettings(
        id=model.id,
        application_id=model.application_id,
        conversation_retention_hours=model.conversation_retention_hours,
        chat_context_message_limit=model.chat_context_message_limit,
        chunk_size=model.chunk_size,
        chunk_overlap=model.chunk_overlap,
        top_k=model.top_k,
        rerank_top_n=model.rerank_top_n,
        rate_limit_per_minute=model.rate_limit_per_minute,
        grounding_instructions=model.grounding_instructions,
    )


class ApplicationSettingsRepository(ApplicationSettingsRepositoryInterface):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, settings: ApplicationSettings) -> ApplicationSettings:
        model = ApplicationSettingsModel(
            id=settings.id,
            application_id=settings.application_id,
            conversation_retention_hours=settings.conversation_retention_hours,
            chat_context_message_limit=settings.chat_context_message_limit,
            chunk_size=settings.chunk_size,
            chunk_overlap=settings.chunk_overlap,
            top_k=settings.top_k,
            rerank_top_n=settings.rerank_top_n,
            rate_limit_per_minute=settings.rate_limit_per_minute,
            grounding_instructions=settings.grounding_instructions,
        )
        self._session.add(model)
        await self._session.flush()
        return _to_entity(model)

    async def get_by_application_id(self, application_id: str) -> ApplicationSettings | None:
        result = await self._session.execute(
            select(ApplicationSettingsModel).where(
                ApplicationSettingsModel.application_id == application_id
            )
        )
        model = result.scalar_one_or_none()
        return _to_entity(model) if model else None

    async def update(self, settings: ApplicationSettings) -> ApplicationSettings:
        result = await self._session.execute(
            select(ApplicationSettingsModel).where(
                ApplicationSettingsModel.application_id == settings.application_id
            )
        )
        model = result.scalar_one()
        model.conversation_retention_hours = settings.conversation_retention_hours
        model.chat_context_message_limit = settings.chat_context_message_limit
        model.chunk_size = settings.chunk_size
        model.chunk_overlap = settings.chunk_overlap
        model.top_k = settings.top_k
        model.rerank_top_n = settings.rerank_top_n
        model.rate_limit_per_minute = settings.rate_limit_per_minute
        model.grounding_instructions = settings.grounding_instructions
        await self._session.flush()
        return _to_entity(model)
