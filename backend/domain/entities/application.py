from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass
class Application:
    id: str
    name: str
    slug: str
    created_at: datetime
    updated_at: datetime
    is_active: bool = True
