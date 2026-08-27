from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker

from core.config import Settings, get_settings
from core.logging import configure_logging, get_logger
from core.provider_resolver import (
    resolve_embedding_provider,
    resolve_llm_provider,
    resolve_reranker_provider,
    resolve_storage_provider,
)
from domain.provider_interfaces.embedding_provider import EmbeddingProviderInterface
from domain.provider_interfaces.llm_provider import LLMProviderInterface
from domain.provider_interfaces.reranker_provider import RerankerProviderInterface
from domain.provider_interfaces.storage_provider import StorageProviderInterface
from infrastructure.database.connection import create_engine_from_settings, create_session_factory
from services.rate_limit_service import RateLimitService


@dataclass
class AppContainer:
    settings: Settings
    engine: AsyncEngine
    session_factory: async_sessionmaker
    llm_provider: LLMProviderInterface
    embedding_provider: EmbeddingProviderInterface
    reranker_provider: RerankerProviderInterface
    storage_provider: StorageProviderInterface
    rate_limit_service: RateLimitService


def build_application_container() -> AppContainer:
    settings = get_settings()
    configure_logging(log_level=settings.log_level, log_format=settings.log_format)
    logger = get_logger(__name__)

    engine = create_engine_from_settings(settings)
    session_factory = create_session_factory(engine)

    llm_provider = resolve_llm_provider(settings)
    embedding_provider = resolve_embedding_provider(settings)
    reranker_provider = resolve_reranker_provider(settings)
    storage_provider = resolve_storage_provider(settings)
    rate_limit_service = RateLimitService()

    if embedding_provider.dimension != settings.embedding_dimension:
        raise ValueError(
            f"EMBEDDING_DIMENSION ({settings.embedding_dimension}) does not match "
            f"resolved provider dimension ({embedding_provider.dimension}). "
            "The vector index (Vector(768) in document_chunk_model.py) must also match."
        )

    logger.info(
        "composition_root_initialized",
        app_env=settings.app_env,
        llm_provider=settings.llm_provider,
        embedding_provider=settings.embedding_provider,
        embedding_dimension=embedding_provider.dimension,
    )

    return AppContainer(
        settings=settings,
        engine=engine,
        session_factory=session_factory,
        llm_provider=llm_provider,
        embedding_provider=embedding_provider,
        reranker_provider=reranker_provider,
        storage_provider=storage_provider,
        rate_limit_service=rate_limit_service,
    )
