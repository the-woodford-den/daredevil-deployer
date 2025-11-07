from typing import Annotated

import debugpy
import logfire
from fastapi import APIRouter, Depends, HTTPException, status
from httpx import AsyncClient, HTTPStatusError
from rich import inspect, print
from sqlmodel import select

from configs import GithubLibrary
from dependency import SessionDependency, get_daredevil_token
from models import User
from models.git import (CreateGitAppToken, GitApp, GitAppResponse, GitAppToken,
                        GitInstall, GitInstallResponse)
from services import UserService
from services.git import GitAppService, GitInstallService

api = APIRouter(prefix="/git/app")


@api.get(
    "/",
    response_model=GitApp,
    response_model_exclude_unset=True,
)
async def get_app(
    *,
    session: SessionDependency,
    token: Annotated[str, Depends(get_daredevil_token)],
):
    """This GET request searches Github Api for a Github App with a token.
    In addition to returning App, it returns installations_count with the App"""

    user = await session.get(token["user"]["id"])

    github_library = GithubLibrary()
    jwt = github_library.create_jwt(client_id=user.client_id)

    endpoint = "https://api.github.com/app"
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "Authorization": f"Bearer {jwt}",
    }

    try:
        async with AsyncClient() as viper:
            response = await viper.get(url=endpoint, headers=headers)
            response.raise_for_status()
            data = response.json()

            app_service = GitAppService(session=session)
            git_app_obj = GitAppResponse.model_validate(data)
            git_app = await app_service.get(git_id=git_app_obj.id)

            if git_app is None:
                git_app = await app_service.add(app_create=git_app_obj)
                logfire.info("GitHub App Validated & Stored in DB")
            else:
                logfire.info("GitHub App Exists in DB")

            return git_app

    except HTTPStatusError as e:
        logfire.error(f"HTTP Status Error: {e}")
        raise HTTPException(
            status=status.HTTP_40O_BAD_REQUEST,
            detail="Incorrect Request.",
        )


@api.get(
    "/installation",
    response_model=GitInstall,
)
async def get_installation(
    *,
    session: SessionDependency,
    token: Annotated[str, Depends(get_daredevil_token)],
):
    """This GET request searches Github Api for Github App Installations.
    Searches by username, token required
    Only returns if username matches an installation."""

    user = await session.get(User, token["user"]["id"])
    github_library = GithubLibrary()
    jwt = github_library.create_jwt(client_id=user.client_id)

    endpoint = "https://api.github.com/app/installations"
    header = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "Authorization": f"Bearer {jwt}",
    }

    with logfire.span("Sending request for app installations list"):
        try:
            async with AsyncClient() as viper:
                response = await viper.get(url=endpoint, headers=header)
                response.raise_for_status()
                data = response.json()

            logfire.info("checking returned list of installations...")
            for git_install_json in data:
                git_install_service = GitInstallService(session)
                if git_install_json["account"]["login"] == user.username:
                    git_install_obj = GitInstallResponse.model_validate(
                        git_install_json
                    )
                    logfire.info("username matched, checking db record...")
                    git_install = await git_install_service.get(
                        git_id=git_install_obj.id
                    )
                    if git_install is None:
                        logfire.info(f"Adding GitInstall: {git_install_obj.id}")
                        git_install = await git_install_service.add(
                            git_install_obj
                        )
                    return git_install

            return {"status_code": 404, "msg": "No Installation Found"}

        except HTTPStatusError as e:
            logfire.error(f"Internal Error: {e}")
            raise HTTPException(
                status=status.HTTP_40O_BAD_REQUEST,
                detail="Incorrect Request.",
            )


@api.post(
    "/token",
    response_model=GitAppToken,
)
async def create_token(
    *,
    params: CreateGitAppToken,
    session: SessionDependency,
):
    """This POST request creates an access token on behalf of the Github App
    Searches db by user installation id.
    Only returns if username matches an installation.
    Access token expires in 1 hour."""

    username = params.get("username")
    user_service = UserService(session=session)
    user = await user_service.get_by_username(username)

    statement = select(GitInstall).where(GitInstall.login == user.username)
    git_app_install = (await session.execute(statement)).scalar_one_or_none()

    if not git_app_install:
        logfire.error(f"No installation found for user: {user.username}")
        raise HTTPException(status_code=404, detail="GitInstall not found")

    github_app_library = GithubLibrary()
    app_jwt = github_app_library.create_jwt(client_id=user.client_id)
    id = str(git_app_install.git_id)

    endpoint = f"https://api.github.com/app/installations/{id}/access_tokens"
    header = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "Authorization": f"Bearer {app_jwt}",
    }

    with logfire.span("Sending request for installation access token..."):
        try:
            async with AsyncClient() as client:
                response = await client.post(url=endpoint, headers=header)
                response.raise_for_status()
                token_json = response.json()

            logfire.info("validating access token ...")
            git_app_token = GitAppToken.model_validate(token_json)

            logfire.info("Responding with token ...")
            return git_app_token

        except HTTPStatusError as e:
            logfire.error(f"Internal Error: {e}")
            raise HTTPException(
                status=status.HTTP_40O_BAD_REQUEST,
                detail="Incorrect Request, No Token.",
            )
