import debugpy
import logfire
from fastapi import APIRouter, HTTPException, status
from httpx import AsyncClient, HTTPStatusError
from rich import inspect, print

from dependency import (CookieTokenDepend, CurrentUserDepend,
                        GitInstallServiceDepend)
from models import CreateGitToken, GitToken
from utility import GitLib

api = APIRouter(prefix="/git/hub/auth")


@api.post(
    "/token",
    response_model=GitToken,
)
async def create_token(
    *,
    user: CurrentUserDepend,
    params: CreateGitToken,
    service: GitInstallServiceDepend,
    token: CookieTokenDepend,
):
    """This POST request creates an access token on behalf of the Github App.
    Access token expires in 1 hour."""

    git_install = service.get_by_username(user.username)

    if git_install is None:
        logfire.error(f"No installation found for user: {user.username}")
        raise HTTPException(status_code=404, detail="GitInstall not found")

    gha_lib = GitLib()
    app_jwt = gha_lib.create_jwt(client_id=user.client_id)
    id = str(git_install.git_id)

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
                install_id=git_install.id,
            )

            logfire.info("Responding with token ...")
            return git_token

        except HTTPStatusError as e:
            logfire.error(f"Internal Error: {e}")
            raise HTTPException(
                status=status.HTTP_40O_BAD_REQUEST,
                detail="Incorrect Request, No Token.",
            )
