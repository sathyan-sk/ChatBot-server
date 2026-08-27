"""FastAPI dependencies exposing process-wide providers from the container,
plus the one provider that must be built per-request (vector search, since it
needs the request's session)."""

from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.database import get_session
from core.provider_resolver import resolve_vector_search_provider
from domain.provider_interfaces.embedding_provider import EmbeddingProviderInterface
from domain.provider_interfaces.llm_provider import LLMProviderInterface
from domain.provider_interfaces.reranker_provider import RerankerProviderInterface
from domain.provider_interfaces.storage_provider import StorageProviderInterface
from domain.provider_interfaces.vector_search_provider import VectorSearchProviderInterface


def get_llm_provider(request: Request) -> LLMProviderInterface:
    return request.app.state.container.llm_provider


def get_embedding_provider(request: Request) -> EmbeddingProviderInterface:
    return request.app.state.container.embedding_provider


def get_reranker_provider(request: Request) -> RerankerProviderInterface:
    return request.app.state.container.reranker_provider


def get_storage_provider(request: Request) -> StorageProviderInterface:
    return request.app.state.container.storage_provider


def get_vector_search_provider(
    request: Request, session: AsyncSession = Depends(get_session)
) -> VectorSearchProviderInterface:
    return resolve_vector_search_provider(request.app.state.container.settings, session)
