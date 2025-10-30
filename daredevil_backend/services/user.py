from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from models.user import User, UserCreate, UserUpdate


class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, id: int) -> User | None:
        query = select(User).where(User.git_id == id)
        user = (await self.session.execute(query)).scalar_one_or_none()
        return user

    async def get_by_username(self, username: str) -> User | None:
        query = select(User).where(User.login == username)
        user = (await self.session.execute(query)).scalar_one_or_none()
        return user

    async def add(self, user_create: UserCreate) -> User:
        new_user = User(
            **user_create.model_dump(exclude="id"),
            git_id=user_create.id,
        )
        self.session.add(new_user)
        await self.session.commit()
        await self.session.refresh(new_user)
        return new_user

    def update(self, user_update: UserUpdate) -> User:
        pass

    def delete(self, id: int) -> None:
        pass
