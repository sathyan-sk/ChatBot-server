from typing import Annotated

from fastapi import APIRouter, Depends

from app.dependencies.security_gateway import (
    require_admin_gateway,
    require_client_gateway,
    require_widget_gateway,
)
from domain.entities.application_context import ApplicationContext

router = APIRouter(tags=["system"])


@router.get("/auth-probe/admin")
async def admin_probe(
    _admin: Annotated[None, Depends(require_admin_gateway)],
) -> dict[str, str]:
    return {"status": "ok", "access": "admin"}


@router.get("/auth-probe/client")
async def client_probe(
    context: Annotated[ApplicationContext, Depends(require_client_gateway)],
) -> dict[str, str]:
    return {
        "status": "ok",
        "access": "client",
        "application_id": context.application_id,
        "knowledge_base_id": context.knowledge_base_id,
    }


@router.get("/auth-probe/widget")
async def widget_probe(
    context: Annotated[ApplicationContext, Depends(require_widget_gateway)],
) -> dict[str, str]:
    return {
        "status": "ok",
        "access": "widget",
        "application_id": context.application_id,
        "knowledge_base_id": context.knowledge_base_id,
    }
