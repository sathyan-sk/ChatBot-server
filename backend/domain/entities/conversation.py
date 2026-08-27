from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class ConversationState(str, Enum):
    ACTIVE = "active"
    ARCHIVED = "archived"


@dataclass
class Conversation:
    id: str
    application_id: str
    conversation_identity: str
    state: ConversationState
    created_at: datetime
    last_activity_at: datetime
    expires_at: datetime
