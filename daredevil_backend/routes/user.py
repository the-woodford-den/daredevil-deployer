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
        response.set_cookie(
            httponly=True,
            domain=settings.domain,
            expires=token["expires_at"],
            path="/user/login",
            key="daredevil_token",
            value=token["token"],
        )

        return response

    except HTTPException as e:
        logfire.error(f"HTTP Error {e.status}: {e.message}")


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
        response.delete_cookie(key="daredevil_token")

        return response

    except Exception:
        logfire.error("Logging out error!")
        return {"status": 404, "detail": "Error while logging out!"}
