from datetime import datetime, timedelta, timezone

import base64
import hashlib
import hmac
import os

import jwt

from fastapi import Request

from .config import settings


ALGORITHM = "HS256"

COOKIE_NAME = "pocketsmart_token"


def hash_password(password: str) -> str:
    """
    Hash password using Python's built-in scrypt.
    """

    salt = os.urandom(16)

    digest = hashlib.scrypt(
        password.encode("utf-8"),
        salt=salt,
        n=2**14,
        r=8,
        p=1
    )

    salt_encoded = base64.urlsafe_b64encode(
        salt
    ).decode()

    digest_encoded = base64.urlsafe_b64encode(
        digest
    ).decode()

    return (
        "scrypt$"
        + salt_encoded
        + "$"
        + digest_encoded
    )


def verify_password(
    password: str,
    encoded: str
) -> bool:

    try:
        _, salt_b64, digest_b64 = encoded.split(
            "$",
            2
        )

        salt = base64.urlsafe_b64decode(
            salt_b64.encode()
        )

        expected = base64.urlsafe_b64decode(
            digest_b64.encode()
        )

        actual = hashlib.scrypt(
            password.encode("utf-8"),
            salt=salt,
            n=2**14,
            r=8,
            p=1
        )

        return hmac.compare_digest(
            actual,
            expected
        )

    except (
        ValueError,
        TypeError
    ):
        return False


def create_token(user_id: int) -> str:

    now = datetime.now(timezone.utc)

    payload = {
        "sub": str(user_id),
        "iat": now,
        "exp": (
            now
            + timedelta(
                minutes=settings.TOKEN_EXPIRE_MINUTES
            )
        )
    }

    return jwt.encode(
        payload,
        settings.JWT_SECRET,
        algorithm=ALGORITHM
    )


def get_current_user_id(
    request: Request
):

    token = request.cookies.get(
        COOKIE_NAME
    )

    if not token:
        return None

    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[ALGORITHM]
        )

        return int(payload["sub"])

    except (
        jwt.InvalidTokenError,
        KeyError,
        ValueError
    ):
        return None