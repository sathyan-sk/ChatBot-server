from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Index, String
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.database.models.base import Base, UUIDPrimaryKeyMixin


class ApplicationCredentialModel(Base, UUIDPrimaryKeyMixin):
    __tablename__ = "application_credentials"
    __table_args__ = (
        Index("ix_credentials_api_key_hash", "api_key_hash"),
        Index("ix_credentials_widget_key", "widget_key"),
    )

    application_id: Mapped[str] = mapped_column(
        ForeignKey("applications.id", ondelete="CASCADE"), nullable=False
    )
    api_key_hash: Mapped[str] = mapped_column(String(128), nullable=False, unique=True)
    widget_key: Mapped[str] = mapped_column(String(128), nullable=False, unique=True)
    status: Mapped[str] = mapped_column(String(20), default="active", nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    revoked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
