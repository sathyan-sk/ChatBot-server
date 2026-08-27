from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.database.models.base import Base, UUIDPrimaryKeyMixin


class ApplicationSettingsModel(Base, UUIDPrimaryKeyMixin):
    __tablename__ = "application_settings"

    application_id: Mapped[str] = mapped_column(
        ForeignKey("applications.id", ondelete="CASCADE"), nullable=False, unique=True
    )
    conversation_retention_hours: Mapped[int] = mapped_column(Integer, default=720, nullable=False)
    chat_context_message_limit: Mapped[int] = mapped_column(Integer, default=10, nullable=False)
    chunk_size: Mapped[int] = mapped_column(Integer, default=800, nullable=False)
    chunk_overlap: Mapped[int] = mapped_column(Integer, default=100, nullable=False)
    top_k: Mapped[int] = mapped_column(Integer, default=20, nullable=False)
    rerank_top_n: Mapped[int] = mapped_column(Integer, default=5, nullable=False)
    rate_limit_per_minute: Mapped[int] = mapped_column(Integer, default=60, nullable=False)
    grounding_instructions: Mapped[str | None] = mapped_column(String(2000), nullable=True)
