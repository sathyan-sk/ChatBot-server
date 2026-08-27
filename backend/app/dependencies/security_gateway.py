from __future__ import annotations

from typing import Annotated

from fastapi import Depends

from app.dependencies.auth import (
    require_admin_access,
    require_client_application_context,
    require_widget_application_context,
)
from domain.entities.application_context import ApplicationContext


def require_admin_gateway(
    _admin: Annotated[None, Depends(require_admin_access)],
) -> None:
    return None


def require_client_gateway(
    context: Annotated[ApplicationContext, Depends(require_client_application_context)],
) -> ApplicationContext:
    return context


def require_widget_gateway(
    context: Annotated[ApplicationContext, Depends(require_widget_application_context)],
) -> ApplicationContext:
    return context
