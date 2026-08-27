from __future__ import annotations

from base64 import b64decode
from typing import Annotated

from domain.entities.application_context import ApplicationContext
from fastapi import Depends, Header, Request

from app.dependencies.repositories import (
    get_application_credential_repository,
    get_knowledge_base_repository,
    get_widget_configuration_repository,
)
from core.security import hash_api_key
from exceptions.domain_exceptions import UnauthorizedError
from infrastructure.database.repositories.application_credential_repository_impl import (
    ApplicationCredentialRepository,
)
from infrastructure.database.repositories.knowledge_base_repository_impl import (
    KnowledgeBaseRepository,
)
from infrastructure.database.repositories.widget_configuration_repository_impl import (
    WidgetConfigurationRepository,
)
from services.admin_auth_service import AdminAuthService
from services.client_access_service import ClientAccessService
from services.widget_access_service import WidgetAccessService


def _parse_basic_auth(authorization: str | None) -> tuple[str, str]:
    if not authorization:
        raise UnauthorizedError("Missing Authorization header.")

    scheme, _, encoded = authorization.partition(" ")
    if scheme.lower() != "basic" or not encoded:
        raise UnauthorizedError("Invalid Authorization scheme.")

    try:
        decoded = b64decode(encoded).decode("utf-8")
        login_id, password = decoded.split(":", 1)
    except Exception as exc:
        raise UnauthorizedError("Invalid Basic authorization format.") from exc

    return login_id, password


def get_admin_auth_service(request: Request) -> AdminAuthService:
    settings = request.app.state.container.settings
    return AdminAuthService(settings=settings)


def require_admin_access(
    authorization: Annotated[str | None, Header()] = None,
    service: Annotated[AdminAuthService, Depends(get_admin_auth_service)] = None,
) -> None:
    if service is None:
        raise UnauthorizedError("Admin authentication service is unavailable.")
    login_id, password = _parse_basic_auth(authorization)
    service.validate_credentials(login_id=login_id, password=password)


def get_client_access_service(
    credential_repository: Annotated[
        ApplicationCredentialRepository, Depends(get_application_credential_repository)
    ],
    knowledge_base_repository: Annotated[
        KnowledgeBaseRepository, Depends(get_knowledge_base_repository)
    ],
) -> ClientAccessService:
    return ClientAccessService(
        credential_repository=credential_repository,
        knowledge_base_repository=knowledge_base_repository,
    )


async def require_client_application_context(
    request: Request,
    x_api_key: Annotated[str | None, Header(alias="X-API-Key")] = None,
    service: Annotated[ClientAccessService, Depends(get_client_access_service)] = None,
) -> ApplicationContext:
    if service is None:
        raise UnauthorizedError("Client access service is unavailable.")

    if not x_api_key:
        raise UnauthorizedError("Missing X-API-Key header.")

    salt = request.app.state.container.settings.api_key_hash_salt
    api_key_hash = hash_api_key(x_api_key, salt)
    return await service.resolve_application_context(api_key_hash=api_key_hash)


def get_widget_access_service(
    credential_repository: Annotated[
        ApplicationCredentialRepository, Depends(get_application_credential_repository)
    ],
    knowledge_base_repository: Annotated[
        KnowledgeBaseRepository, Depends(get_knowledge_base_repository)
    ],
    widget_configuration_repository: Annotated[
        WidgetConfigurationRepository, Depends(get_widget_configuration_repository)
    ],
) -> WidgetAccessService:
    return WidgetAccessService(
        credential_repository=credential_repository,
        knowledge_base_repository=knowledge_base_repository,
        widget_configuration_repository=widget_configuration_repository,
    )


async def require_widget_application_context(
    x_widget_key: Annotated[str | None, Header(alias="X-Widget-Key")] = None,
    origin: Annotated[str | None, Header(alias="Origin")] = None,
    service: Annotated[WidgetAccessService, Depends(get_widget_access_service)] = None,
) -> ApplicationContext:
    if service is None:
        raise UnauthorizedError("Widget access service is unavailable.")

    if not x_widget_key:
        raise UnauthorizedError("Missing X-Widget-Key header.")

    return await service.resolve_application_context(
        widget_key=x_widget_key,
        request_origin=origin,
    )
