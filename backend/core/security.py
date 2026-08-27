"""Password hashing and credential-verification primitives.

Used by admin authentication (env-configured, no DB lifecycle) and, in later
phases, by application API-key validation. This module has zero DB dependency.
"""

import hashlib
import hmac
import secrets

from passlib.context import CryptContext

_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(plain_password: str) -> str:
    return _pwd_context.hash(plain_password)


def verify_password(plain_password: str, password_hash: str) -> bool:
    return _pwd_context.verify(plain_password, password_hash)


def generate_api_key() -> str:
    """Generates a cryptographically strong, opaque credential value."""
    return secrets.token_urlsafe(32)


def hash_api_key(raw_key: str, salt: str) -> str:
    """Deterministic hash so a raw key can be re-hashed and compared on lookup,
    without ever storing the raw key itself."""
    return hmac.new(salt.encode("utf-8"), raw_key.encode("utf-8"), hashlib.sha256).hexdigest()


def constant_time_compare(a: str, b: str) -> bool:
    return hmac.compare_digest(a, b)
