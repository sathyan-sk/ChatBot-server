"""Centralized provider resolver. Reads Settings and returns the configured
provider instance for each capability. This is the single point of provider
selection — services and pipelines never instantiate providers themselves."""

from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from core.config import Settings
from domain.provider_interfaces.embedding_provider import EmbeddingProviderInterface
from domain.provider_interfaces.llm_provider import LLMProviderInterface
from domain.provider_interfaces.parser_provider import ParserProviderInterface
from domain.provider_interfaces.reranker_provider import RerankerProviderInterface
from domain.provider_interfaces.storage_provider import StorageProviderInterface
from domain.provider_interfaces.vector_search_provider import VectorSearchProviderInterface
from exceptions.domain_exceptions import ConfigurationError
from infrastructure.providers.embeddings.ollama_provider import (
    OllamaEmbeddingProvider,
)
from infrastructure.providers.llm.openrouter_provider import OpenRouterLLMProvider
from infrastructure.providers.parsing.docx_parser_provider import DocxParserProvider
from infrastructure.providers.parsing.pdf_parser_provider import PdfParserProvider
from infrastructure.providers.parsing.plain_text_provider import (
    PlainTextParserProvider,
)
from infrastructure.providers.reranking.cross_encoder_provider import (
    CrossEncoderRerankerProvider,
)
from infrastructure.providers.storage.supabase_storage_provider import (
    SupabaseStorageProvider,
)
from infrastructure.providers.vector.pgvector_provider import PgVectorSearchProvider


def resolve_llm_provider(settings: Settings) -> LLMProviderInterface:
    if settings.llm_provider == "openrouter":
        return OpenRouterLLMProvider(api_key=settings.openrouter_api_key)
    raise ConfigurationError(f"Unknown LLM_PROVIDER: {settings.llm_provider}")


def resolve_embedding_provider(settings: Settings) -> EmbeddingProviderInterface:
    if settings.embedding_provider == "ollama":
        return OllamaEmbeddingProvider(
            base_url=settings.ollama_base_url,
            model=settings.embedding_model,
            dimension=settings.embedding_dimension,
        )
    raise ConfigurationError(f"Unknown EMBEDDING_PROVIDER: {settings.embedding_provider}")


def resolve_reranker_provider(settings: Settings) -> RerankerProviderInterface:
    if settings.reranker_provider == "cross_encoder":
        return CrossEncoderRerankerProvider()
    raise ConfigurationError(f"Unknown RERANKER_PROVIDER: {settings.reranker_provider}")


def resolve_parser_provider(content_type: str) -> ParserProviderInterface:
    parsers: list[ParserProviderInterface] = [
        PdfParserProvider(),
        DocxParserProvider(),
        PlainTextParserProvider(),
    ]
    for parser in parsers:
        if parser.supports(content_type):
            return parser
    raise ConfigurationError(f"No parser registered for content_type: {content_type}")


def resolve_storage_provider(settings: Settings) -> StorageProviderInterface:
    if settings.storage_provider == "supabase":
        return SupabaseStorageProvider(
            supabase_url=settings.supabase_url,
            supabase_key=settings.supabase_key,
            bucket=settings.supabase_bucket,
        )
    raise ConfigurationError(f"Unknown STORAGE_PROVIDER: {settings.storage_provider}")


def resolve_vector_search_provider(
    settings: Settings, session: AsyncSession
) -> VectorSearchProviderInterface:
    if settings.vector_search_provider == "pgvector":
        return PgVectorSearchProvider(session=session)
    raise ConfigurationError(f"Unknown VECTOR_SEARCH_PROVIDER: {settings.vector_search_provider}")
