from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class DocumentChunk:
    id: str
    application_id: str
    knowledge_base_id: str
    data_source_id: str
    content: str
    chunk_order: int
    embedding_model: str
    embedding_dimension: int
    created_at: datetime
    metadata: dict[str, str] = field(default_factory=dict)
