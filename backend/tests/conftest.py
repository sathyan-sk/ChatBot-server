"""
Shared pytest fixtures for unit and integration tests.

This file is intentionally minimal at Phase 0 — it will be extended in later
phases once the database connection, composition root, and FastAPI app
factory exist. No fixtures depending on undefined contracts are added here.
"""

import pytest


@pytest.fixture(scope="session")
def anyio_backend() -> str:
    return "asyncio"
