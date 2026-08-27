from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from domain.entities.widget_configuration import WidgetConfiguration


class WidgetConfigurationRepositoryInterface(ABC):
    @abstractmethod
    async def create(self, config: "WidgetConfiguration") -> "WidgetConfiguration":
        raise NotImplementedError

    @abstractmethod
    async def get_by_application_id(self, application_id: str) -> "WidgetConfiguration | None":
        raise NotImplementedError

    @abstractmethod
    async def update(self, config: "WidgetConfiguration") -> "WidgetConfiguration":
        raise NotImplementedError
