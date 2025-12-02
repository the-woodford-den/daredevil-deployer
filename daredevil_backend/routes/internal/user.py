import logfire
from fastapi import APIRouter, HTTPException

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

    try:
        user = await session.get(User, cookie["user_id"])
        if user is None:
            logfire.error(f"User not found for user_id: {cookie['user_id']}")
            raise HTTPException(status_code=404, detail="User not found")

        logfire.info(f"User {user.username} authenticated successfully")
        return user

    except HTTPException:
        raise
    except Exception as e:
        logfire.error(f"Error getting current user: {e}")
        raise HTTPException(status_code=401, detail="Invalid authentication")
