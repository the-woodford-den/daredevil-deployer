from datetime import datetime, timezone
from typing import Annotated
from uuid import UUID

import logfire
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm

from configs import get_settings
from dependency import CookieTokenDepend, SessionDepend, UserServiceDepend
from models.user import User

settings = get_settings()
api = APIRouter(prefix="/auth")


@api.post("/login")
async def login_user(
    *,
    form: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: UserServiceDepend,
) -> JSONResponse:
    """Validates username & password, creates a jwt, adds jwt to cookie,
    then returns response"""

    data = await service.create_token(form.username, form.password)

    if data is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Oof! Not authorized.",
        )

    cookie_data = await service.create_cookie(data["token"])
    response = JSONResponse(content=data["user"])
    response.set_cookie(**cookie_data)

    return response

    # logfire.error(f"HTTP Error {e.status_code}: {e.detail}")
    # raise HTTPException(status=e.status_code, detail=f"{e.detail}")


@api.delete("/logout")
async def logout_user(
    *,
    session: SessionDepend,
    cookie: CookieTokenDepend,
):
    """Deactivates cookie and logout."""
    user = await session.get(User, UUID(cookie["user_id"]))
    if user is None:
        logfire.error(f"User not found for user_id: {cookie['user_id']}")
        raise HTTPException(status_code=404, detail="User not found")
    content = {
        "key": "daredevil_token",
        "value": "",
        "httponly": True,
        "samesite": "lax",
        "path": "/",
        "expires": datetime.now(timezone.utc),
    }

    try:
        response = JSONResponse(content={"message": "deleted"})
        response.set_cookie(**content)
        response.delete_cookie(key="daredevil_token")

        return response
    except Exception:
        logfire.error("Logging out error!")
        return {"status": 404, "detail": "Error while logging out!"}
