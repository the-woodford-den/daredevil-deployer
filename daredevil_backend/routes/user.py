from typing import Annotated

import logfire
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from dependency import SessionDependency
from models.user import User, UserCreate, UserLogin
from services import UserService

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


@api.post("/login", response_model=UserLogin)
async def login_user(
    *,
    form: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: SessionDependency,
):
    """Validates username & password, then returns a jwt token"""

    try:
        user_service = UserService(session=session)
        token = await user_service(form.username, form.password)

        return {"access_token": token, "type": "jwt"}

    except HTTPException as e:
        logfire.error(f"HTTP Error {e.status}: {e.message}")
