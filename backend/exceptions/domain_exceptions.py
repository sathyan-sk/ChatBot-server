"""Application-level exception hierarchy. Every raised business error inherits
from AppError so a single exception handler can produce a consistent response."""


class AppError(Exception):
    error_code: str = "APP_ERROR"
    http_status: int = 500

    def __init__(self, message: str, *, error_code: str | None = None) -> None:
        super().__init__(message)
        self.message = message
        if error_code:
            self.error_code = error_code


class ConfigurationError(AppError):
    error_code = "CONFIGURATION_ERROR"
    http_status = 500


class NotFoundError(AppError):
    error_code = "NOT_FOUND"
    http_status = 404


class ValidationFailedError(AppError):
    error_code = "VALIDATION_FAILED"
    http_status = 422


class ConflictError(AppError):
    error_code = "CONFLICT"
    http_status = 409


class UnauthorizedError(AppError):
    error_code = "UNAUTHORIZED"
    http_status = 401


class ForbiddenError(AppError):
    error_code = "FORBIDDEN"
    http_status = 403


class RateLimitExceededError(AppError):
    error_code = "RATE_LIMIT_EXCEEDED"
    http_status = 429


class ProviderError(AppError):
    """Raised when an external provider (LLM, embedding, storage, etc.) fails."""

    error_code = "PROVIDER_ERROR"
    http_status = 502
