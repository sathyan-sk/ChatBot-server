# quick_test_repo.py — run once from backend/, then delete
import asyncio
import uuid
from datetime import UTC, datetime

from core.config import get_settings
from domain.entities.application import Application
from infrastructure.database.connection import create_engine_from_settings, create_session_factory
from infrastructure.database.repositories.application_repository_impl import ApplicationRepository


async def main():
    settings = get_settings()
    engine = create_engine_from_settings(settings)
    factory = create_session_factory(engine)
    async with factory() as session:
        repo = ApplicationRepository(session)
        app = Application(
            id=str(uuid.uuid4()),
            name="Test App",
            slug="test-app-" + str(uuid.uuid4())[:8],
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC),
        )
        created = await repo.create(app)
        await session.commit()
        print("Created:", created)
        fetched = await repo.get_by_id(created.id)
        print("Fetched:", fetched)


asyncio.run(main())
