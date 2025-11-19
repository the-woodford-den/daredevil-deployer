from datetime import datetime, timezone
from typing import Annotated

import logfire
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm

from configs import get_settings
from dependency import CookieTokenDepend, SessionDepend, UserServiceDepend
from models.user import User, UserCreate
from utility import decode_token

settings = get_settings()
api = APIRouter(prefix="/user")


@api.post("/create", response_model=User)
async def create_user(
    *,
    create_user: UserCreate,
    service: UserServiceDepend,
):
    """Creates a user with a username & password"""

    return await service.add(create_user)


@api.post("/login")
async def login_user(
    *,
    form: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: UserServiceDepend,
) -> dict:
    """Validates username & password, creates a jwt, adds jwt to cookie,
    then returns response"""

    try:
        data = await service.create_token(form.username, form.password)
        cookie_data = await service.create_cookie(data["token"])

        response = JSONResponse(content=data["user"])
        response.set_cookie(**cookie_data)

        return response

    except HTTPException as e:
        logfire.error(f"HTTP Error {e.status_code}: {e.detail}")
        raise HTTPException(status=e.status_code, detail=f"{e.detail}")


@api.get("/me", response_model=User)
async def get_current_user(
    *,
    session: SessionDepend,
    cookie_data: CookieTokenDepend,
):
    """Returns the current authenticated user from token"""

    try:
        user = await session.get(User, cookie_data["user_id"])
        if user is None:
            logfire.error(f"User not found for user_id: {token['user_id']}")
            raise HTTPException(status_code=404, detail="User not found")

        logfire.info(f"User {user.username} authenticated successfully")
        return user

    except HTTPException:
        raise
    except Exception as e:
        logfire.error(f"Error getting current user: {e}")
        raise HTTPException(status_code=401, detail="Invalid authentication")


@api.delete("/logout")
async def logout_user(
    *,
    session: SessionDepend,
    cookie_data: CookieTokenDepend,
):
    """Deactivates cookie and logout."""

    try:
        token = decode_token(cookie_data)
        user = await session.get(User, token["user_id"])

        if user is None:
            logfire.error(f"User not found for user_id: {token['user_id']}")
            raise HTTPException(status_code=404, detail="User not found")

        content = {
            "key": "daredevil_token",
            "value": "",
            "httponly": True,
            "samesite": "lax",
            "path": "/",
            "expires": datetime.now(timezone.utc),
        }

        response = JSONResponse(content={"message": "deleted"})
        response.set_cookie(**content)
        response.delete_cookie()

        return response

    except Exception:
        logfire.error("Logging out error!")
        return {"status": 404, "detail": "Error while logging out!"}
