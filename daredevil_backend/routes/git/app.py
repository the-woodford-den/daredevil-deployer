import debugpy
import logfire
from fastapi import APIRouter, Depends, HTTPException
from httpx import AsyncClient, HTTPStatusError
from rich import inspect, print
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from configs import GithubLibrary
from dbs import get_async_session
from depends import SessionDepend
from models.git import (CreateGitInstallToken, GitApp, GitAppResponse,
                        GitInstall, GitInstallResponse,
                        GitInstallTokenResponse)
from models.user import User, UserCreate
from services import UserService
from services.git import GitAppService, GitInstallService

api = APIRouter(prefix="/git/app")


@api.get(
    "/search/{slug}",
    response_model=GitAppResponse,
    response_model_exclude_unset=True,
)
async def search_apps(*, slug: str, session: SessionDepend):
    """This GET request searches Github Api for a Github App without a token."""
    """It uses a slug to search."""
    """Checks the database, adds &&|| returns App"""

    url = f"https://api.github.com/apps/{slug}"
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "daredevil-deployer",
    }

    try:
        async with AsyncClient() as viper:
            response = await viper.get(url=url, headers=headers)
            response.raise_for_status()
            data = response.json()
            app_service = GitAppService(session=session)

            github_app_obj = GitAppResponse.model_validate(data)
            github_app = await app_service.get(id=github_app_obj.id)
            if github_app is None:
                github_app = await app_service.add(app_create=github_app_obj)
                logfire.info("GitHub App Validated & Stored in DB")
            else:
                logfire.info("GitHub App Exists in DB")

            user_service = UserService(session=session)
            data["owner"]["client_id"] = github_app.client_id
            user_obj = UserCreate.model_validate(data["owner"])
            user = await user_service.get(id=user_obj.id)
            if user is None:
                user = await user_service.add(user_create=user_obj)
                logfire.info("User Validated & Stored in DB")
            else:
                logfire.info("User Exists in DB")

        return github_app_obj

    except HTTPStatusError as e:
        logfire.error(f"HTTP Status Error: {e}")

        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"GitHub API error: {e}",
        )
    except Exception as e:
        logfire.error(f"App Error in search_apps: {e}:{e}")
        raise Exception(f"App Error in search_apps: {e}:{e}")


@api.get(
    "/access/{client_id}",
    response_model=GitAppResponse,
    response_model_exclude_unset=True,
)
async def authenticated_access_app(
    *, client_id: str, session: AsyncSession = Depends(get_async_session)
):
    """This GET request searches Github Api for a Github App with a token."""
    """In addition to returning App, it returns installations_count."""
    """Not sure if keeping..."""

    if client_id is None:
        logfire.error("No Client Id means no JWT")
        raise Exception("No Client Id means no JWT")

    jwt = GithubLibrary().create_jwt(client_id=client_id)
    endpoint = "https://api.github.com/app"
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "Authorization": f"Bearer {jwt}",
    }

    try:
        async with AsyncClient() as viper:
            response = await viper.get(url=endpoint, headers=headers)
            data = response.json()
            github_app_obj = GitAppResponse.model_validate(data)

            app_search = select(GitApp).where(
                GitApp.github_app_id == github_app_obj.id
            )
            app_owner_obj = github_app_obj.owner
            user_search = select(User).where(User.git_id == app_owner_obj.id)
            user_record = (await session.execute(user_search)).one_or_none()
            app_record = (await session.execute(app_search)).one_or_none()

            if app_record is None:
                app_id = app_record.id
                app_dict = GitAppResponse.model_dump(github_app_obj)
                app_dict["github_app_id"] = app_id
                del app_dict["id"]
                app_obj = GitApp.model_validate(app_dict)
                session.add(app_obj)
                await session.commit()
                await session.refresh(app_obj)
                logfire.info(f"GitHub App in DB, {app_dict}")
            else:
                logfire.info("GitHub App Exists in DB")

            if user_record is None:
                user_id = app_owner_obj.id
                app_owner_obj = data["owner"]
                app_owner_obj["git_id"] = user_id
                del app_owner_obj["id"]
                user_obj = User.model_validate(app_owner_obj)
                session.add(user_obj)
                await session.commit()
                await session.refresh(user_obj)
                logfire.info(f"GitHub User in DB, {user_obj}")
            else:
                logfire.info("Github User Exists in DB")

            logfire.info(
                f"App Record Response has been returned ...{github_app_obj}"
            )
            return github_app_obj

        response.raise_for_status()
    except HTTPStatusError as e:
        logfire.error(f"HTTP Status Error: {e}")
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"GitHub API error: {e}",
        )

    except Exception as e:
        logfire.error(f"App Error in get_authenticated_app: {e}:{e}")
        raise Exception(f"App Error in get_authenticated_app: {e}:{e}")


@api.get(
    "/installs/search/{username}",
    response_model=GitInstall,
)
async def search_installations(
    *, username: str, session: AsyncSession = Depends(get_async_session)
):
    """This GET request searches Github Api for Github App Installations."""
    """Searches by username, token required"""
    """Only returns if username matches an installation."""

    user_service = UserService(session)
    user = await user_service.get_by_username(username)

    if user is None:
        logfire.error("No User means no JWT")
        raise Exception("No User means no JWT")
    elif user.client_id is None:
        logfire.error("No Client Id means no JWT")
        raise Exception("No Client Id means no JWT")
    logfire.info("Found user with client_id ...")

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
                i_responses = response.json()

            logfire.info("checking returned list of installations...")
            for i_response in i_responses:
                installation_service = GitInstallService(session)
                if i_response["account"]["login"] == "woodFordR":
                    install_obj = GitInstallResponse.model_validate(i_response)
                    logfire.info("username matched, checking db record...")
                    installation = await installation_service.get(
                        install_obj.id
                    )
                    if installation is None:
                        logfire.info(f"Adding GitInstall: {install_obj.id}")
                        installation = await installation_service.add(
                            install_obj
                        )
                    return installation
                else:
                    return {"status_code": 404, "msg": "No Installation Found"}

        except HTTPStatusError as e:
            logfire.error(f"Internal Error: {e}")
            raise HTTPException(
                status_code=e,
                detail=f"Internal Error: {e}",
            )


@api.post(
    "/install/token",
    response_model=GitInstallTokenResponse,
)
async def installation_token(
    *,
    params: CreateGitInstallToken,
    session: AsyncSession = Depends(get_async_session),
):
    """This POST request creates an access token on behalf of the Github App"""
    """Searches db by user installation id."""
    """Only returns if username matches an installation."""
    """Access token expires in 1 hour."""

    statement = (
        select(
            GitInstall.app_id,
            GitApp.git_id,
            GitApp.client_id,
        )
        .where(GitInstall.app_id == GitApp.git_id)
        .where(GitInstall.git_id == params.git_id)
    )
    results = (await session.execute(statement)).all()

    if not results:
        logfire.error("No installation found with that install_id")
        raise HTTPException(status_code=404, detail="GitInstall not found")

    client_id = results[-1].client_id
    logfire.info(f"Found GitInstall with id: {params.git_id}")
    github_app_library = GithubLibrary()
    app_jwt = github_app_library.create_jwt(client_id=client_id)

    endpoint = f"https://api.github.com/app/installations/{str(params.git_id)}/access_tokens"
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
            token_obj = GitInstallTokenResponse.model_validate(token_json)

            logfire.info("Responding with token ...")
            return token_obj

        except HTTPStatusError as e:
            logfire.error(f"Internal Error: {e}")
            raise HTTPException(
                status_code=e,
                detail=f"Internal Error: {e}",
            )
