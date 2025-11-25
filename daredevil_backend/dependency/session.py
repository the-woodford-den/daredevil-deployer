from typing import Annotated

from fastapi import Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession

from dbs import get_async_session
from models.user import User
from security import CookieDepend, oauth2_scheme
from services import UserService
from services.git import GitAppService, GitInstallService, GitRepoService
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
    return await session.get(User, access_token["user_id"])


def get_gitapp_service(session: SessionDepend):
    return GitAppService(session)


def get_gitinstall_service(session: SessionDepend):
    return GitInstallService(session)


def get_gitrepo_service(session: SessionDepend):
    return GitRepoService(session)


def get_user_service(session: SessionDepend):
    return UserService(session)


CookieTokenDepend = Annotated[dict, Depends(get_cookie_token)]
CurrentUserDepend = Annotated[User, Depends(get_current_user)]
GitAppServiceDepend = Annotated[GitAppService, Depends(get_gitapp_service)]
GitInstallServiceDepend = Annotated[
    GitInstallService, Depends(get_gitinstall_service)
]
GitRepoServiceDepend = Annotated[GitRepoService, Depends(get_gitrepo_service)]
UserServiceDepend = Annotated[UserService, Depends(get_user_service)]
