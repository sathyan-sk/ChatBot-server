from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class WidgetConfiguration:
    id: str
    application_id: str
    allowed_origins: list[str] = field(default_factory=list)
    theme_color: str = "#01696f"
    welcome_message: str = "Hi! How can I help you today?"
    launcher_label: str = "Chat with us"
