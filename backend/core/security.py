"""Security primitives using bcrypt directly.

Why not passlib?
- passlib 1.7.4 has compatibility issues with newer bcrypt releases.
- bcrypt itself supports the exact hash/verify operations we need.
"""

from __future__ import annotations

import base64
import hashlib
import hmac
import secrets

import bcrypt

from exceptions.domain_exceptions import ValidationFailedError

_BCRYPT_MAX_BYTES = 72


def _validate_bcrypt_input(password: str) -> bytes:
    password_bytes = password.encode("utf-8")
    if len(password_bytes) > _BCRYPT_MAX_BYTES:
        raise ValidationFailedError("Password exceeds bcrypt maximum length of 72 bytes.")
    return password_bytes


def hash_password(plain_password: str) -> str:
    password_bytes = _validate_bcrypt_input(plain_password)
    hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    return hashed.decode("utf-8")


def verify_password(plain_password: str, password_hash: str) -> bool:
    password_bytes = _validate_bcrypt_input(plain_password)
    return bcrypt.checkpw(password_bytes, password_hash.encode("utf-8"))


def generate_api_key() -> str:
    return secrets.token_urlsafe(32)


def hash_api_key(raw_key: str, salt: str) -> str:
    return hmac.new(salt.encode("utf-8"), raw_key.encode("utf-8"), hashlib.sha256).hexdigest()


def constant_time_compare(a: str, b: str) -> bool:
    return hmac.compare_digest(a, b)


def prehash_for_bcrypt(value: str) -> str:
    """Optional helper if you ever need long secret support with bcrypt.

    bcrypt only supports 72 bytes. A standard workaround is SHA-256 + base64
    before bcrypt, as recommended by bcrypt project docs.
    """
    digest = hashlib.sha256(value.encode("utf-8")).digest()
    return base64.b64encode(digest).decode("ascii")
