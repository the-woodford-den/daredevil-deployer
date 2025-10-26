from fastapi import Depends
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from dbs import get_async_session
from models import User, UserCreate, UserUpdate


class UserService:
    def __init__(self):
        pass

    async def get(
        self, id: int, session: AsyncSession = Depends(get_async_session)
    ):
        query = select(User).where(User.id == id)
        user = (await session.execute(query)).one_or_none()
        return user

    async def add(
        self,
        user_create: UserCreate,
        session: AsyncSession = Depends(get_async_session),
    ) -> User:
        user_id = user_create.id
        new_user_obj = user_create["owner"]
        new_user_obj["github_id"] = user_id
        del new_user_obj["id"]
        user = User.model_validate(new_user_obj)
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user

    def update(self, user_update: UserUpdate) -> User:
        pass

    def delete(self, id: int) -> None:
        pass
