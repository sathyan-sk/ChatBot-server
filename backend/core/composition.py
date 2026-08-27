"""Composition Root — the single place responsible for assembling the
application's object graph at startup.

This file intentionally grows across phases: Phase 1 only wires settings and
logging (nothing else exists yet). Phase 8 will extend this to wire the
provider resolver, repositories, and services once those layers are built.
Nothing in this file should be duplicated elsewhere — main.py and worker/main.py
both call build_application_container() rather than constructing dependencies
inline.
"""

from dataclasses import dataclass

from core.config import Settings, get_settings
from core.logging import configure_logging, get_logger


@dataclass
class AppContainer:
    """Holds the fully-wired object graph. Extended in later phases with
    repositories, provider instances, and services."""

    settings: Settings


def build_application_container() -> AppContainer:
    settings = get_settings()
    configure_logging(log_level=settings.log_level, log_format=settings.log_format)
    logger = get_logger(__name__)
    logger.info("composition_root_initialized", app_env=settings.app_env)
    return AppContainer(settings=settings)
