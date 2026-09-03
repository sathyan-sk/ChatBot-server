from __future__ import annotations

from domain.entities.application_context import ApplicationContext

from domain.repository_interfaces.application_credential_repository import (
    ApplicationCredentialRepositoryInterface,
)
from domain.repository_interfaces.knowledge_base_repository import (
    KnowledgeBaseRepositoryInterface,
)
from domain.repository_interfaces.widget_configuration_repository import (
    WidgetConfigurationRepositoryInterface,
)
from exceptions.domain_exceptions import ForbiddenError, UnauthorizedError


class WidgetAccessService:
    """Widget boundary only.

    public widget key
        -> resolve application
        -> validate origin
        -> ApplicationContext

    No business/chat logic lives here.
    """

    def __init__(
        self,
        credential_repository: ApplicationCredentialRepositoryInterface,
        knowledge_base_repository: KnowledgeBaseRepositoryInterface,
        widget_configuration_repository: WidgetConfigurationRepositoryInterface,
    ) -> None:
        self._credential_repository = credential_repository
        self._knowledge_base_repository = knowledge_base_repository
        self._widget_configuration_repository = widget_configuration_repository

    async def resolve_application_context(
        self, widget_key: str, request_origin: str | None
    ) -> ApplicationContext:
        credential = await self._credential_repository.get_by_widget_key(widget_key)
        if credential is None:
            raise UnauthorizedError("Invalid widget key.")

        widget_config = await self._widget_configuration_repository.get_by_application_id(
            credential.application_id
        )
        if widget_config is None:
            raise ForbiddenError("Widget configuration is not available.")

        self._validate_origin(
            allowed_origins=widget_config.allowed_origins,
            request_origin=request_origin,
        )

        knowledge_base = await self._knowledge_base_repository.get_by_application_id(
            credential.application_id
        )
        if knowledge_base is None:
            raise ForbiddenError("Knowledge base is not configured for this application.")

        return ApplicationContext(
            application_id=credential.application_id,
            knowledge_base_id=knowledge_base.id,
        )

    def _validate_origin(self, allowed_origins: list[str], request_origin: str | None) -> None:
        if not allowed_origins:
            raise ForbiddenError("Widget origin is not configured.")

        if request_origin is None:
            raise ForbiddenError("Request origin header is required for widget access.")

        normalized_origin = request_origin.strip().lower()
        normalized_allowed = {origin.strip().lower() for origin in allowed_origins}

        if normalized_origin not in normalized_allowed:
            raise ForbiddenError("Widget origin is not allowed.")
