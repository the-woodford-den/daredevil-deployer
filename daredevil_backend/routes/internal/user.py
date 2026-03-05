import logfire
from fastapi import APIRouter, HTTPException
from uuid import UUID

from configs import get_settings
from dependency import CookieTokenDepend, SessionDepend, UserServiceDepend
from models.user import User, UserCreate

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


@api.get("/me", response_model=User)
async def get_current_user(
    *,
    session: SessionDepend,
    cookie: CookieTokenDepend,
):
    """Returns the current authenticated user from token"""
    user = await session.get(User, UUID(cookie["user_id"]))
    if user is None:
        raise HTTPException(status_code=404, detail="User is not here.")

    logfire.info(f"User {user.username} authenticated successfully")
    return user
