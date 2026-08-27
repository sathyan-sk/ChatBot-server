from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from domain.entities.application_credential import ApplicationCredential


class ApplicationCredentialRepositoryInterface(ABC):
    @abstractmethod
    async def create(self, credential: "ApplicationCredential") -> "ApplicationCredential":
        raise NotImplementedError

    @abstractmethod
    async def get_by_api_key_hash(self, api_key_hash: str) -> "ApplicationCredential | None":
        raise NotImplementedError

    @abstractmethod
    async def get_by_widget_key(self, widget_key: str) -> "ApplicationCredential | None":
        raise NotImplementedError

    @abstractmethod
    async def list_by_application(self, application_id: str) -> list["ApplicationCredential"]:
        raise NotImplementedError

    @abstractmethod
    async def revoke(self, credential_id: str) -> None:
        raise NotImplementedError
