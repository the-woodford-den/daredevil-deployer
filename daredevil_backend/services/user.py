from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from models.user import User, UserCreate, UserUpdate


class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, id: int):
        query = select(User).where(User.github_id == id)
        user = (await self.session.exec(query)).one_or_none()
        return user

    async def add(self, user_create: UserCreate) -> User:
        user_id = user_create.id
        new_user_obj = user_create.model_dump(exclude="id")
        new_user_obj["github_id"] = user_id
        user = User.model_validate(new_user_obj)
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    def update(self, user_update: UserUpdate) -> User:
        pass

    def delete(self, id: int) -> None:
        pass
