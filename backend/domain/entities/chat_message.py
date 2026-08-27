from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"


@dataclass
class ChatMessage:
    id: str
    conversation_id: str
    role: MessageRole
    content: str
    created_at: datetime
