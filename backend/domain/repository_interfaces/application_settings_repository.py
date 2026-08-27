from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from domain.entities.application_settings import ApplicationSettings


class ApplicationSettingsRepositoryInterface(ABC):
    @abstractmethod
    async def create(self, settings: "ApplicationSettings") -> "ApplicationSettings":
        raise NotImplementedError

    @abstractmethod
    async def get_by_application_id(self, application_id: str) -> "ApplicationSettings | None":
        raise NotImplementedError

    @abstractmethod
    async def update(self, settings: "ApplicationSettings") -> "ApplicationSettings":
        raise NotImplementedError
