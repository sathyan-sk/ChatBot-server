from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.entities.application import Application
from domain.repository_interfaces.application_repository import ApplicationRepositoryInterface
from infrastructure.database.models.application_model import ApplicationModel


def _to_entity(model: ApplicationModel) -> Application:
    return Application(
        id=model.id,
        name=model.name,
        slug=model.slug,
        created_at=model.created_at,
        updated_at=model.updated_at,
        is_active=model.is_active,
    )


class ApplicationRepository(ApplicationRepositoryInterface):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, application: Application) -> Application:
        model = ApplicationModel(
            id=application.id,
            name=application.name,
            slug=application.slug,
            is_active=application.is_active,
        )
        self._session.add(model)
        await self._session.flush()
        return _to_entity(model)

    async def get_by_id(self, application_id: str) -> Application | None:
        result = await self._session.execute(
            select(ApplicationModel).where(ApplicationModel.id == application_id)
        )
        model = result.scalar_one_or_none()
        return _to_entity(model) if model else None

    async def get_by_slug(self, slug: str) -> Application | None:
        result = await self._session.execute(
            select(ApplicationModel).where(ApplicationModel.slug == slug)
        )
        model = result.scalar_one_or_none()
        return _to_entity(model) if model else None

    async def list_all(self, limit: int = 50, offset: int = 0) -> list[Application]:
        result = await self._session.execute(
            select(ApplicationModel)
            .order_by(ApplicationModel.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        return [_to_entity(m) for m in result.scalars().all()]

    async def update(self, application: Application) -> Application:
        result = await self._session.execute(
            select(ApplicationModel).where(ApplicationModel.id == application.id)
        )
        model = result.scalar_one()
        model.name = application.name
        model.is_active = application.is_active
        await self._session.flush()
        return _to_entity(model)

    async def delete(self, application_id: str) -> None:
        result = await self._session.execute(
            select(ApplicationModel).where(ApplicationModel.id == application_id)
        )
        model = result.scalar_one_or_none()
        if model:
            await self._session.delete(model)
            await self._session.flush()
