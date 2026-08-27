"""Liveness endpoint only. No dependency calls here — readiness (DB/storage
checks) is added in a later phase once those dependencies exist."""

from fastapi import APIRouter

router = APIRouter(tags=["system"])


@router.get("/health")
async def liveness() -> dict[str, str]:
    return {"status": "ok"}
