import debugpy
import logfire
from fastapi import APIRouter, HTTPException, status
from httpx import AsyncClient, HTTPStatusError
from rich import inspect, print

from dependency import CookieTokenDepend, GitAppServiceDepend
from models.git import GitAppResponse
from utility import GitLib

api = APIRouter(prefix="/git/hub/app")


@api.get(
    "/",
    response_model=GitAppResponse,
    response_model_exclude_unset=True,
)
async def get(
    *,
    service: GitAppServiceDepend,
    cookie: CookieTokenDepend,
):
    """This GET request searches Github Api for a Github App with a token.
    In addition to returning App, it returns installations_count with the App"""

    inspect(cookie)
    git_lib = GitLib()
    jwt = git_lib.create_jwt(client_id=cookie["client_id"])

    endpoint = "https://api.github.com/app"
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "Authorization": f"Bearer {jwt}",
    }

    with logfire.span("Sending request for github app data."):
        try:
            async with AsyncClient() as viper:
                response = await viper.get(url=endpoint, headers=headers)
                response.raise_for_status()
                data = response.json()

                if data["id"] is not None:
                    logfire.info(f"Found github app id #{data['id']}")
                    git_app = await service.get(git_id=data["id"])
                    return git_app

            logfire.info(
                "Did not find github app for username"
                + f"#{cookie['username']} with client_id #{cookie['client_id']}."
            )
            return None

        except HTTPStatusError as e:
            logfire.error(f"HTTP Status Error: {e}")
            raise HTTPException(
                status=status.HTTP_40O_BAD_REQUEST,
                detail="Incorrect Request.",
            )
