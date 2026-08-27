"""Implements atomic job claiming with SELECT ... FOR UPDATE SKIP LOCKED —
claim and ownership decision happen in one DB statement (Section 20.8),
preventing two workers from processing the same job."""

from datetime import UTC, datetime, timedelta

from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from domain.entities.ingestion_job import IngestionJob, IngestionJobStatus
from domain.repository_interfaces.ingestion_job_repository import (
    IngestionJobRepositoryInterface,
)
from infrastructure.database.models.ingestion_job_model import IngestionJobModel


def _to_entity(model: IngestionJobModel) -> IngestionJob:
    return IngestionJob(
        id=model.id,
        application_id=model.application_id,
        data_source_id=model.data_source_id,
        status=IngestionJobStatus(model.status),
        created_at=model.created_at,
        updated_at=model.updated_at,
        started_at=model.started_at,
        completed_at=model.completed_at,
        error_message=model.error_message,
    )


class IngestionJobRepository(IngestionJobRepositoryInterface):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, job: IngestionJob) -> IngestionJob:
        model = IngestionJobModel(
            id=job.id,
            application_id=job.application_id,
            data_source_id=job.data_source_id,
            status=job.status.value,
        )
        self._session.add(model)
        await self._session.flush()
        return _to_entity(model)

    async def claim_next_queued(self) -> IngestionJob | None:
        result = await self._session.execute(
            text(
                """
                SELECT id FROM ingestion_jobs
                WHERE status = 'queued'
                ORDER BY created_at ASC
                LIMIT 1
                FOR UPDATE SKIP LOCKED
                """
            )
        )
        row = result.first()
        if row is None:
            return None

        job_id = row[0]
        update_result = await self._session.execute(
            select(IngestionJobModel).where(IngestionJobModel.id == job_id)
        )
        model = update_result.scalar_one()
        model.status = IngestionJobStatus.PROCESSING.value
        model.started_at = datetime.now(UTC)
        await self._session.flush()
        return _to_entity(model)

    async def update_status(
        self, job_id: str, status: str, error_message: str | None = None
    ) -> None:
        result = await self._session.execute(
            select(IngestionJobModel).where(IngestionJobModel.id == job_id)
        )
        model = result.scalar_one()
        model.status = status
        model.error_message = error_message
        if status in (IngestionJobStatus.READY.value, IngestionJobStatus.FAILED.value):
            model.completed_at = datetime.now(UTC)
        await self._session.flush()

    async def get_by_data_source_id(self, data_source_id: str) -> IngestionJob | None:
        result = await self._session.execute(
            select(IngestionJobModel)
            .where(IngestionJobModel.data_source_id == data_source_id)
            .order_by(IngestionJobModel.created_at.desc())
        )
        model = result.scalars().first()
        return _to_entity(model) if model else None

    async def list_stuck_processing(self, timeout_minutes: int) -> list[IngestionJob]:
        cutoff = datetime.now(UTC) - timedelta(minutes=timeout_minutes)
        result = await self._session.execute(
            select(IngestionJobModel).where(
                IngestionJobModel.status == IngestionJobStatus.PROCESSING.value,
                IngestionJobModel.started_at < cutoff,
            )
        )
        return [_to_entity(m) for m in result.scalars().all()]
