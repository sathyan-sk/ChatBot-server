from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class IngestionJobStatus(str, Enum):
    QUEUED = "queued"
    PROCESSING = "processing"
    READY = "ready"
    FAILED = "failed"


@dataclass
class IngestionJob:
    id: str
    application_id: str
    data_source_id: str
    status: IngestionJobStatus
    created_at: datetime
    updated_at: datetime
    started_at: datetime | None = None
    completed_at: datetime | None = None
    error_message: str | None = None
