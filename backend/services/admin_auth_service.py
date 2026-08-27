from __future__ import annotations

from core.config import Settings
from core.security import verify_password
from exceptions.domain_exceptions import UnauthorizedError, ValidationFailedError


class AdminAuthService:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    def validate_credentials(self, login_id: str, password: str) -> None:
        if login_id != self._settings.admin_login_id:
            raise UnauthorizedError("Invalid admin credentials.")

        try:
            is_valid = verify_password(password, self._settings.admin_password_hash)
        except ValidationFailedError as exc:
            raise UnauthorizedError("Invalid admin credentials.") from exc

        if not is_valid:
            raise UnauthorizedError("Invalid admin credentials.")
