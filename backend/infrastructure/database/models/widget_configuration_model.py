from sqlalchemy import JSON, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.database.models.base import Base, UUIDPrimaryKeyMixin


class WidgetConfigurationModel(Base, UUIDPrimaryKeyMixin):
    __tablename__ = "widget_configurations"

    application_id: Mapped[str] = mapped_column(
        ForeignKey("applications.id", ondelete="CASCADE"), nullable=False, unique=True
    )
    allowed_origins: Mapped[list] = mapped_column(JSON, default=list, nullable=False)
    theme_color: Mapped[str] = mapped_column(String(20), default="#01696f", nullable=False)
    welcome_message: Mapped[str] = mapped_column(
        String(500), default="Hi! How can I help you today?", nullable=False
    )
    launcher_label: Mapped[str] = mapped_column(String(100), default="Chat with us", nullable=False)
