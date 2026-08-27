from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ApplicationContext:
    application_id: str
    knowledge_base_id: str
