from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from domain.entities.ingestion_job import IngestionJob


class IngestionJobRepositoryInterface(ABC):
    @abstractmethod
    async def create(self, job: "IngestionJob") -> "IngestionJob":
        raise NotImplementedError

    @abstractmethod
    async def claim_next_queued(self) -> "IngestionJob | None":
        """Must be implemented using SELECT ... FOR UPDATE SKIP LOCKED — the
        claim and the ownership decision happen atomically in one DB statement
        (Section 20.8), never as two separate application-level steps."""
        raise NotImplementedError

    @abstractmethod
    async def update_status(
        self, job_id: str, status: str, error_message: str | None = None
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_data_source_id(self, data_source_id: str) -> "IngestionJob | None":
        raise NotImplementedError

    @abstractmethod
    async def list_stuck_processing(self, timeout_minutes: int) -> list["IngestionJob"]:
        """Supports the timeout-handling cautionary rule — jobs stuck in
        'processing' past the configured timeout are auto-failed."""
        raise NotImplementedError
