from datetime import datetime, timedelta

import logfire
from fastapi import HTTPException, status
from passlib.context import CryptContext
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from configs import get_settings
from models.user import User, UserCreate, UserUpdate
from utility import encode_user_token

settings = get_settings()
password_context = CryptContext(schemes=[settings.cc_alg], deprecated="auto")


class UserService:
    """The UserService handles database actions for creating, searching,
    updating, and deleting users.
    get() finds user by id
    get_by_username() finds user by username
    add() creates a user
    update() updates a user
    delete() deletes a user
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, id: int) -> User | None:
        query = select(User).where(User.git_id == id)
        user = (await self.session.execute(query)).scalar_one_or_none()
        return user

    async def get_by_username(self, username: str) -> User | None:
        query = select(User).where(User.username == username)
        user = (await self.session.execute(query)).scalar_one_or_none()
        return user

    async def add(self, user_create: UserCreate) -> User:
        new_user = User(
            **user_create.model_dump(exclude=["password", "id"]),
            client_id=settings.client_id,
            password_hash=password_context.hash(user_create.password),
        )
        self.session.add(new_user)
        await self.session.commit()
        await self.session.refresh(new_user)
        return new_user

    def update(self, user_update: UserUpdate) -> User:
        pass

    def delete(self, id: int) -> None:
        pass

    async def token(self, username, password) -> dict:
        user = await self.session.get_by_username(username)
        password_correct = password_context.verify(
            password,
            user.password_hash,
        )

        if user is None:
            raise HTTPException(
                message=f"User '{username}' not found.",
                status_code=status.HTTP_404_NOT_FOUND,
            )

        if not password_correct:
            raise HTTPException(
                message="Password is incorrect.",
                status_code=status.HTTP_401_UNAUTHORIZED,
            )

        content = {
            "client_id": user.client_id,
            "expires_at": datetime.now() + timedelta(days=1),
            "user_id": user.id,
            "username": username,
        }
        token = encode_user_token(data={**content})

        return {**content, "token": token}


#
