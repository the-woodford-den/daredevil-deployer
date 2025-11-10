from datetime import datetime, timedelta, timezone

import jwt
import logfire

from configs import get_settings

settings = get_settings()


def decode_token(token: str) -> dict | None:
    """Decodes tokens"""
    try:
        return jwt.decode(
            algorithms=[settings.jwt_alg],
            key=settings.app_secret,
            jwt=token,
        )
    except jwt.PyJWTError as e:
        logfire.error(f"Utility decode token error: {e}")
        return None


def encode_token(data: dict, expiry: timedelta = timedelta(days=1)) -> str:
    """Encodes tokens"""
    return jwt.encode(
        algorithm=settings.jwt_alg,
        key=settings.app_secret,
        payload={
            **data,
            "exp": datetime.now(timezone.utc) + expiry,
        },
    )
