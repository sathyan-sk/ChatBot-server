from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class CredentialStatus(str, Enum):
    ACTIVE = "active"
    REVOKED = "revoked"


@dataclass
class ApplicationCredential:
    id: str
    application_id: str
    api_key_hash: str
    widget_key: str
    status: CredentialStatus
    created_at: datetime
    revoked_at: datetime | None = None
