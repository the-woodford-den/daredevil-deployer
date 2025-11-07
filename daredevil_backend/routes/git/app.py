from typing import Annotated

import debugpy
import logfire
from fastapi import APIRouter, Depends, HTTPException, status
from httpx import AsyncClient, HTTPStatusError
from rich import inspect, print
from sqlmodel import select

from dependency import SessionDependency, get_daredevil_token
from models import CreateGitToken, GitToken, User
from models.git import GitApp, GitAppResponse, GitInstall, GitInstallResponse
from services.git import GitAppService, GitInstallService
from utility import GitLib

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

    github_library = GitLib()
    jwt = github_library.create_jwt(client_id=token.client_id)

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
            git_app = await app_service.get(git_id=data["id"])

            if git_app is None:
                app_resp = GitAppResponse(**data)
                git_app = await app_service.add(data=app_resp)
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

    github_library = GitLib()
    jwt = github_library.create_jwt(client_id=token["client_id"])

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
            for git_json in data:
                install_service = GitInstallService(session)
                if git_json["account"]["login"] == token["username"]:
                    logfire.info("username matched, checking db record...")

                    install_obj = GitInstallResponse(**git_json)
                    installation = await install_service.get(
                        git_id=install_obj.id
                    ).scalar_one_or_none()

                    if installation is None:
                        logfire.info(
                            f"Adding GitInstallation: {install_obj.id}"
                        )

                        installation = await install_service.add(install_obj)
                    return installation

            return {"status_code": 404, "msg": "No Installation Found"}

        except HTTPStatusError as e:
            logfire.error(f"Internal Error: {e}")
            raise HTTPException(
                status=status.HTTP_40O_BAD_REQUEST,
                detail="Incorrect Request.",
            )


@api.post(
    "/token",
    response_model=GitToken,
)
async def create_token(
    *,
    params: CreateGitToken,
    session: SessionDependency,
    token: Annotated[str, Depends(get_daredevil_token)],
):
    """This POST request creates an access token on behalf of the Github App
    Searches db by user installation id.
    Only returns if username matches an installation.
    Access token expires in 1 hour."""

    user = await session.get(User, token["user_id"]).scalar_one_or_none()
    if user is None:
        logfire.error(f"No user found with user_id: {token['user_id']}")
        raise HTTPException(status_code=404, detail="User not found")

    statement = select(GitInstall).where(GitInstall.login == user.username)
    user_install = (await session.execute(statement)).scalar_one_or_none()

    if user_install is None:
        logfire.error(f"No installation found for user: {user.username}")
        raise HTTPException(status_code=404, detail="GitInstall not found")

    gha_lib = GitLib()
    app_jwt = gha_lib.create_jwt(client_id=user.client_id)
    id = str(user_install.git_id)

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
            git_token = GitToken(
                **token_json,
                client_id=user.client_id,
                user_id=user.id,
                install_id=user_install.id,
            )

            logfire.info("Responding with token ...")
            return git_token

        except HTTPStatusError as e:
            logfire.error(f"Internal Error: {e}")
            raise HTTPException(
                status=status.HTTP_40O_BAD_REQUEST,
                detail="Incorrect Request, No Token.",
            )
