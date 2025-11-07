import jwt

from configs import get_settings

settings = get_settings()


def decode_user_token(token: str) -> dict | None:
    try:
        return jwt.decode(
            algorithms=[settings.jwt_alg],
            key=settings.app_secret,
            jwt=token,
        )
    except jwt.PyJWTError:
        return None


def encode_user_token(
    data: dict,
) -> str:
    return jwt.encode(
        algorithm=settings.jwt_alg,
        key=settings.app_secret,
        payload={
            **data,
        },
    )
