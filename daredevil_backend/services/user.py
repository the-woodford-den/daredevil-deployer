from datetime import datetime, timedelta, timezone

import logfire
from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerifyMismatchError
from fastapi import HTTPException, status
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from configs import get_settings
from models.user import User, UserCreate, UserUpdate
from utility import encode_token

settings = get_settings()
ph = PasswordHasher()


class UserService:
    """The UserService handles database actions and creating cookies
    for users.
    """

    def __init__(
        self,
        session: AsyncSession,
    ):
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
        password_hash = ph.hash(user_create.password)
        new_user = User(
            **user_create.model_dump(exclude=["password", "id"]),
            git_id=1234,
            password_hash=password_hash,
        )
        log_dump = new_user.model_dump()
        logfire.info(f"Adding User to Database {log_dump}")

        self.session.add(new_user)
        await self.session.commit()
        await self.session.refresh(new_user)
        return new_user

    def update(self, user_update: UserUpdate) -> User:
        pass

    def delete(self, id: int) -> None:
        pass

    async def create_token(self, username, password) -> dict | None:
        user = await self.get_by_username(username)

        try:
            if user is None:
                raise HTTPException(
                    detail=f"User '{username}' not found.",
                    status_code=status.HTTP_404_NOT_FOUND,
                )
            isValid = ph.verify(user.password_hash, password)

            if not isValid:
                raise HTTPException(
                    detail="Password is incorrect.",
                    status_code=status.HTTP_401_UNAUTHORIZED,
                )

            content = {
                "user_id": str(user.id),
                "username": username,
            }
            token = encode_token(data={**content})
            user_res = UserUpdate.model_validate(user)

            return {
                "user": {
                    **user_res.model_dump(),
                },
                "token": token,
            }

        except (InvalidHashError, VerifyMismatchError, HTTPException) as e:
            logfire.error(f"User service create cookie error: {type(e)}: {e}")
            return None

    async def create_cookie(
        self, token: str, expiry: timedelta = timedelta(days=1)
    ) -> dict:
        cookie_kwargs = {
            "key": "daredevil_token",
            "value": token,
            "httponly": True,
            "samesite": "lax",
            "path": "/",
            "expires": datetime.now(timezone.utc) + expiry,
        }

        if settings.env == "production":
            cookie_kwargs["secure"] = True
            if settings.domain:
                cookie_kwargs["domain"] = settings.domain

        return cookie_kwargs
