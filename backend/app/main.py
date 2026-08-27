"""FastAPI application factory. Stateless process — no ingestion execution here."""

import uuid
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from pydantic import ValidationError

from app.api.system.health import router as health_router
from core.composition import AppContainer, build_application_container
from core.logging import get_logger, request_id_ctx
from exceptions.handlers import register_exception_handlers

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    try:
        container: AppContainer = build_application_container()
    except ValidationError as exc:
        # Fail fast: required configuration is missing or invalid.
        print(f"STARTUP FAILED — invalid configuration: {exc}")
        raise SystemExit(1) from exc

    app.state.container = container
    logger.info("application_startup_complete", app_env=container.settings.app_env)
    yield
    logger.info("application_shutdown")


def create_app() -> FastAPI:
    app = FastAPI(title="AI Knowledge Platform", lifespan=lifespan)

    @app.middleware("http")
    async def request_id_middleware(request: Request, call_next):  # type: ignore[no-untyped-def]
        request_id = str(uuid.uuid4())
        request_id_ctx.set(request_id)
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response

    register_exception_handlers(app)
    app.include_router(health_router, prefix="/api/system")

    return app


app = create_app()


@app.get("/")
async def root():
    return {
        "service": "ChatBot backend system",
        "status": "running",
    }
