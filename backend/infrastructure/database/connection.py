"""Async engine, session factory, and connection pooling. Configured entirely
from typed settings — no hardcoded pool values (Section 10)."""

from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from core.config import Settings


def create_engine_from_settings(settings: Settings):  # type: ignore[no-untyped-def]
    return create_async_engine(
        settings.database_url,
        pool_size=settings.database_pool_size,
        max_overflow=settings.database_max_overflow,
        pool_timeout=settings.database_pool_timeout,
        pool_recycle=settings.database_pool_recycle,
        pool_pre_ping=True,
    )


def create_session_factory(engine):  # type: ignore[no-untyped-def]
    return async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def get_db_session(session_factory) -> AsyncIterator[AsyncSession]:  # type: ignore[no-untyped-def]
    """FastAPI dependency. Yields a session scoped to a single request/unit of
    work — never held open across an LLM/provider call (Section 10)."""
    async with session_factory() as session:
        yield session
