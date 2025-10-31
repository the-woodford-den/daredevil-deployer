from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from dbs import get_async_session
from models.user import User, UserCreate
from services import UserService

api = APIRouter(prefix="/user")


@api.post("/create", response_model=User)
async def create_user(
    *,
    create_user: UserCreate,
    session: AsyncSession = Depends(get_async_session),
):
    user_service = UserService(session=session)
    return await user_service.add(create_user)
