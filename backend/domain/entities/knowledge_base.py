from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass
class KnowledgeBase:
    id: str
    application_id: str
    created_at: datetime
