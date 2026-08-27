"""FastAPI dependencies building repository instances scoped to the current
request's session. Nothing outside this module constructs a repository
directly — routes and services depend on these functions."""

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.database import get_session
from infrastructure.database.repositories.application_credential_repository_impl import (
    ApplicationCredentialRepository,
)
from infrastructure.database.repositories.application_repository_impl import (
    ApplicationRepository,
)
from infrastructure.database.repositories.application_settings_repository_impl import (
    ApplicationSettingsRepository,
)
from infrastructure.database.repositories.chat_message_repository_impl import (
    ChatMessageRepository,
)
from infrastructure.database.repositories.conversation_repository_impl import (
    ConversationRepository,
)
from infrastructure.database.repositories.data_source_repository_impl import (
    DataSourceRepository,
)
from infrastructure.database.repositories.document_chunk_repository_impl import (
    DocumentChunkRepository,
)
from infrastructure.database.repositories.ingestion_job_repository_impl import (
    IngestionJobRepository,
)
from infrastructure.database.repositories.knowledge_base_repository_impl import (
    KnowledgeBaseRepository,
)
from infrastructure.database.repositories.message_citation_repository_impl import (
    MessageCitationRepository,
)
from infrastructure.database.repositories.widget_configuration_repository_impl import (
    WidgetConfigurationRepository,
)


def get_application_repository(
    session: AsyncSession = Depends(get_session),
) -> ApplicationRepository:
    return ApplicationRepository(session)


def get_application_credential_repository(
    session: AsyncSession = Depends(get_session),
) -> ApplicationCredentialRepository:
    return ApplicationCredentialRepository(session)


def get_knowledge_base_repository(
    session: AsyncSession = Depends(get_session),
) -> KnowledgeBaseRepository:
    return KnowledgeBaseRepository(session)


def get_data_source_repository(
    session: AsyncSession = Depends(get_session),
) -> DataSourceRepository:
    return DataSourceRepository(session)


def get_ingestion_job_repository(
    session: AsyncSession = Depends(get_session),
) -> IngestionJobRepository:
    return IngestionJobRepository(session)


def get_document_chunk_repository(
    session: AsyncSession = Depends(get_session),
) -> DocumentChunkRepository:
    return DocumentChunkRepository(session)


def get_application_settings_repository(
    session: AsyncSession = Depends(get_session),
) -> ApplicationSettingsRepository:
    return ApplicationSettingsRepository(session)


def get_widget_configuration_repository(
    session: AsyncSession = Depends(get_session),
) -> WidgetConfigurationRepository:
    return WidgetConfigurationRepository(session)


def get_conversation_repository(
    session: AsyncSession = Depends(get_session),
) -> ConversationRepository:
    return ConversationRepository(session)


def get_chat_message_repository(
    session: AsyncSession = Depends(get_session),
) -> ChatMessageRepository:
    return ChatMessageRepository(session)


def get_message_citation_repository(
    session: AsyncSession = Depends(get_session),
) -> MessageCitationRepository:
    return MessageCitationRepository(session)
