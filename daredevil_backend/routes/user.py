from typing import Annotated

import logfire
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm

from configs import get_settings
from dependency import SessionDependency, get_daredevil_token
from models.user import User, UserCreate
from services import UserService

settings = get_settings()
api = APIRouter(prefix="/user")


@api.post("/create", response_model=User)
async def create_user(
    *,
    create_user: UserCreate,
    session: SessionDependency,
):
    """Creates a user with a username & password"""

    user_service = UserService(session=session)
    return await user_service.add(create_user)


@api.post("/login")
async def login_user(
    *,
    form: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: SessionDependency,
) -> dict:
    """Validates username & password, creates a jwt, adds jwt to cookie,
    then returns jwt plus user id, clientId, install_id"""

    try:
        user_service = UserService(session=session)
        token = await user_service.token(form.username, form.password)

        response = JSONResponse(content=token)

        # Only set domain in production, not in local development
        cookie_kwargs = {
            "key": "daredevil_token",
            "value": token["token"],
            "httponly": True,
            "samesite": "lax",
            "path": "/",
            "expires": token["expires_at"],
        }

        # Only set domain and secure flag in production
        if settings.env == "production":
            cookie_kwargs["secure"] = True
            if settings.domain:
                cookie_kwargs["domain"] = settings.domain

        response.set_cookie(**cookie_kwargs)

        return response

    except HTTPException as e:
        logfire.error(f"HTTP Error {e.status_code}: {e.detail}")
        raise


@api.get("/me", response_model=User)
async def get_current_user(
    *,
    session: SessionDependency,
    token: Annotated[dict, Depends(get_daredevil_token)],
):
    """Returns the current authenticated user from token"""

    try:
        user = await session.get(User, token["user_id"])
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
    session: SessionDependency,
    token: Annotated[str, Depends(get_daredevil_token)],
):
    """Decodes token and user logouts."""

    try:
        user = await session.get(User, token["user_id"])
        content = {
            "status": 200,
            "detail": f"{user.username} is offline.",
            "user_id": f"{user.id}",
        }

        response = JSONResponse(content=content)
        response.delete_cookie(key="daredevil_token", path="/")

        return response

    except Exception:
        logfire.error("Logging out error!")
        return {"status": 404, "detail": "Error while logging out!"}
