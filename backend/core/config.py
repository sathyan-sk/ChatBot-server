"""Typed application settings — single source of truth.

Rule: nothing outside this module calls os.getenv directly. Every other module
imports `get_settings()` and reads typed attributes. Missing required values raise
a validation error immediately at startup (fail fast), never at first request.
"""

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # --- Application ---
    app_name: str = Field(default="AI Knowledge Platform")
    app_env: str = Field(default="development")
    debug: bool = Field(default=False)

    # --- Database ---
    database_url: str = Field(...)
    database_pool_size: int = Field(default=20)
    database_max_overflow: int = Field(default=40)
    database_pool_timeout: int = Field(default=30)
    database_pool_recycle: int = Field(default=1800)

    # --- Supabase Storage ---
    supabase_url: str = Field(...)
    supabase_key: str = Field(...)
    supabase_bucket: str = Field(default="knowledge-documents")

    # --- Security ---
    admin_login_id: str = Field(...)
    admin_password_hash: str = Field(...)
    jwt_secret: str = Field(...)
    jwt_expiry_minutes: int = Field(default=60)
    api_key_hash_salt: str = Field(...)

    # --- Provider Selection (Provider != Model) ---
    llm_provider: str = Field(default="openrouter")
    llm_model: str = Field(default="")
    openrouter_api_key: str = Field(default="")

    embedding_provider: str = Field(default="nomic")
    embedding_model: str = Field(default="")
    embedding_dimension: int = Field(default=768)
    nomic_api_key: str = Field(default="")

    reranker_provider: str = Field(default="cross_encoder")
    parser_provider: str = Field(default="docling")
    storage_provider: str = Field(default="supabase")
    vector_search_provider: str = Field(default="pgvector")

    # --- Application Defaults ---
    default_conversation_retention_hours: int = Field(default=720)
    default_chat_context_message_limit: int = Field(default=10)
    default_chunk_size: int = Field(default=800)
    default_chunk_overlap: int = Field(default=100)
    default_top_k: int = Field(default=20)
    default_rerank_top_n: int = Field(default=5)
    default_rate_limit_per_minute: int = Field(default=60)
    ingestion_processing_timeout_minutes: int = Field(default=10)

    # --- Worker ---
    worker_poll_interval_seconds: int = Field(default=5)
    conversation_cleanup_interval_minutes: int = Field(default=60)

    # --- Logging ---
    log_level: str = Field(default="INFO")
    log_format: str = Field(default="json")


@lru_cache
def get_settings() -> Settings:
    """Load settings once per process. Raises pydantic.ValidationError with a
    clear field-level message if any required value is missing — this is the
    fail-fast mechanism referenced throughout the architecture spec."""
    return Settings()  # pyright: ignore[reportCallIssue]
