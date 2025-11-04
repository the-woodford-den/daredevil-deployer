from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from depends import SessionDepend
from models.user import User, UserCreate, UserLogin
from services import UserService

api = APIRouter(prefix="/user")


@api.post("/create", response_model=User)
async def create_user(
    *,
    create_user: UserCreate,
    session: SessionDepend,
):
    """Creates a user with a username & password"""

    user_service = UserService(session=session)
    return await user_service.add(create_user)


@api.post("/login", response_model=UserLogin)
async def login_user(
    *,
    form: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: SessionDepend,
):
    """Validates username & password, then returns a jwt token"""

    user_service = UserService(session=session)
    token = await user_service(form.username, form.password)

    return {"access_token": token, "type": "jwt"}
