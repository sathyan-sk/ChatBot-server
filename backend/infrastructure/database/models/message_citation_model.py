from sqlalchemy import Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.database.models.base import Base, UUIDPrimaryKeyMixin


class MessageCitationModel(Base, UUIDPrimaryKeyMixin):
    __tablename__ = "message_citations"

    message_id: Mapped[str] = mapped_column(
        ForeignKey("chat_messages.id", ondelete="CASCADE"), nullable=False
    )
    chunk_id: Mapped[str] = mapped_column(
        ForeignKey("document_chunks.id", ondelete="SET NULL"), nullable=True
    )
    relevance_score: Mapped[float] = mapped_column(Float, nullable=False)


"""Note: chunk_id uses ondelete="SET NULL" rather than CASCADE — a citation record should remain 
visible in message history for audit purposes even if the underlying chunk is later deleted, 
but it must not block deletion of the chunk itself."""
