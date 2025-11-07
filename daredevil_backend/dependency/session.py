from typing import Annotated

import logfire
from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from dbs import get_async_session
from security import daredevil_user_cookie
from utility import decode_user_token

SessionDependency = Annotated[AsyncSession, Depends(get_async_session)]


def get_daredevil_token(
    token: Annotated[str, Depends(daredevil_user_cookie)],
):
    try:
        data = decode_user_token(token)
        if data is not None:
            return data

    except Exception:
        logfire.error("Decoding Cookie Error!")
        return {"status": 401, "detail": "Unauthorized, no token in cookie!"}
