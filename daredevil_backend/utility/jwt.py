import logfire
import jwt
from jwt import PyJWTError
from datetime import datetime, timedelta, timezone
from configs import get_settings
from fastapi import HTTPException, status

settings = get_settings()


def decode_token(token: str) -> dict:
    """Decodes tokens"""
    try:
        return jwt.decode(
            algorithms=[settings.jwt_alg],
            key=settings.app_secret,
            jwt=token,
        )
    except PyJWTError as e:
        logfire.error(f"Failed to decode token: {e.args}")
        raise HTTPException(
            detail="Failed to decode token, unauthorized",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )


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
