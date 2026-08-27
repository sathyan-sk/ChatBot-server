from __future__ import annotations

from dataclasses import dataclass


@dataclass
class MessageCitation:
    id: str
    message_id: str
    chunk_id: str
    relevance_score: float
