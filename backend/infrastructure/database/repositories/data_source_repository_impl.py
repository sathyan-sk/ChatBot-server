from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.entities.data_source import DataSource, DataSourceStatus, DataSourceType
from domain.repository_interfaces.data_source_repository import DataSourceRepositoryInterface
from infrastructure.database.models.data_source_model import DataSourceModel


def _to_entity(model: DataSourceModel) -> DataSource:
    return DataSource(
        id=model.id,
        application_id=model.application_id,
        knowledge_base_id=model.knowledge_base_id,
        source_type=DataSourceType(model.source_type),
        status=DataSourceStatus(model.status),
        storage_path=model.storage_path,
        original_filename=model.original_filename,
        source_url=model.source_url,
        created_at=model.created_at,
        updated_at=model.updated_at,
        error_message=model.error_message,
    )


class DataSourceRepository(DataSourceRepositoryInterface):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, data_source: DataSource) -> DataSource:
        model = DataSourceModel(
            id=data_source.id,
            application_id=data_source.application_id,
            knowledge_base_id=data_source.knowledge_base_id,
            source_type=data_source.source_type.value,
            status=data_source.status.value,
            storage_path=data_source.storage_path,
            original_filename=data_source.original_filename,
            source_url=data_source.source_url,
        )
        self._session.add(model)
        await self._session.flush()
        return _to_entity(model)

    async def get_by_id(self, application_id: str, data_source_id: str) -> DataSource | None:
        result = await self._session.execute(
            select(DataSourceModel).where(
                DataSourceModel.id == data_source_id,
                DataSourceModel.application_id == application_id,
            )
        )
        model = result.scalar_one_or_none()
        return _to_entity(model) if model else None

    async def list_by_knowledge_base(
        self, application_id: str, knowledge_base_id: str, limit: int = 50, offset: int = 0
    ) -> list[DataSource]:
        result = await self._session.execute(
            select(DataSourceModel)
            .where(
                DataSourceModel.application_id == application_id,
                DataSourceModel.knowledge_base_id == knowledge_base_id,
            )
            .order_by(DataSourceModel.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        return [_to_entity(m) for m in result.scalars().all()]

    async def update_status(self, application_id: str, data_source_id: str, status: str) -> None:
        result = await self._session.execute(
            select(DataSourceModel).where(
                DataSourceModel.id == data_source_id,
                DataSourceModel.application_id == application_id,
            )
        )
        model = result.scalar_one()
        model.status = status
        await self._session.flush()

    async def delete(self, application_id: str, data_source_id: str) -> None:
        result = await self._session.execute(
            select(DataSourceModel).where(
                DataSourceModel.id == data_source_id,
                DataSourceModel.application_id == application_id,
            )
        )
        model = result.scalar_one_or_none()
        if model:
            await self._session.delete(model)
            await self._session.flush()
