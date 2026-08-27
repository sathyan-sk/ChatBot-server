from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ApplicationSettings:
    id: str
    application_id: str
    conversation_retention_hours: int
    chat_context_message_limit: int
    chunk_size: int
    chunk_overlap: int
    top_k: int
    rerank_top_n: int
    rate_limit_per_minute: int
    grounding_instructions: str | None = None
