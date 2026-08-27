from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class DataSourceType(str, Enum):
    DOCUMENT = "document"
    WEBSITE = "website"
    CSV = "csv"


class DataSourceStatus(str, Enum):
    UPLOADED = "uploaded"
    PROCESSING = "processing"
    READY = "ready"
    FAILED = "failed"


@dataclass
class DataSource:
    id: str
    application_id: str
    knowledge_base_id: str
    source_type: DataSourceType
    status: DataSourceStatus
    storage_path: str | None
    original_filename: str | None
    source_url: str | None
    created_at: datetime
    updated_at: datetime
    error_message: str | None = None
