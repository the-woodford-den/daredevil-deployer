from typing import Annotated
from uuid import UUID

from fastapi import Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession

from dbs import get_async_session
from models.user import User
from security import CookieDepend, oauth2_scheme
from services import UserService
from services.git import (GitAppService, GitInstallationService,
                          GitRepositoryService)
from utility import decode_token

SessionDepend = Annotated[AsyncSession, Depends(get_async_session)]


def get_cookie_token(cookie_token: CookieDepend) -> dict:
    """A helper to retrieve cookie data"""
    data = decode_token(cookie_token)
    if data is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token.",
        )
    return data


def get_access_token(
    token: Annotated[str, Depends(oauth2_scheme)],
) -> dict:
    """A helper dedicated to retrieving token."""
    data = decode_token(token)
    if data is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token.",
        )
    return data


async def get_current_user(
    access_token: Annotated[dict, Depends(get_cookie_token)],
    session: SessionDepend,
):
    """Returns the current user from token"""
    return await session.get(User, UUID(access_token["user_id"]))


def get_git_app_service(session: SessionDepend):
    return GitAppService(session)


def get_git_installation_service(session: SessionDepend):
    return GitInstallationService(session)


def get_git_repository_service(session: SessionDepend):
    return GitRepositoryService(session)


def get_user_service(session: SessionDepend):
    return UserService(session)


CookieTokenDepend = Annotated[dict, Depends(get_cookie_token)]
CurrentUserDepend = Annotated[User, Depends(get_current_user)]
GitAppServiceDepend = Annotated[GitAppService, Depends(get_git_app_service)]
GitInstallationServiceDepend = Annotated[
    GitInstallationService, Depends(get_git_installation_service)
]
GitRepositoryServiceDepend = Annotated[
    GitRepositoryService, Depends(get_git_repository_service)
]
UserServiceDepend = Annotated[UserService, Depends(get_user_service)]
