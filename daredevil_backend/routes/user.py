from depends import SessionDepend
from fastapi import APIRouter

from models.user import User, UserCreate
from services import UserService

api = APIRouter(prefix="/user")


@api.post("/create", response_model=User)
async def create_user(
    *,
    create_user: UserCreate,
    session: SessionDepend,
):
    user_service = UserService(session=session)
    return await user_service.add(create_user)
