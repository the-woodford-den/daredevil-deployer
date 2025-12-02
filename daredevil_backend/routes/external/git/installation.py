import debugpy
import logfire
from fastapi import APIRouter, HTTPException, status
from httpx import AsyncClient, HTTPStatusError
from rich import inspect, print

from dependency import CookieTokenDepend, GitInstallationServiceDepend
from models.git import GitInstallationResponse
from utility import GitLib

api = APIRouter(prefix="/git/hub/installation")


@api.get(
    "/",
    response_model=GitInstallationResponse,
    response_model_exclude_unset=True,
)
async def get(
    *,
    service: GitInstallationServiceDepend,
    cookie: CookieTokenDepend,
) -> GitInstallationResponse | None:
    """This GET request searches Github Api for Github App Installations.
    Searches by username, token required"""

    github_library = GitLib()
    jwt = github_library.create_jwt(client_id=cookie["client_id"])

    endpoint = "https://api.github.com/app/installations"
    header = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "Authorization": f"Bearer {jwt}",
    }

    with logfire.span("Sending request for github app installations list"):
        try:
            async with AsyncClient() as viper:
                response = await viper.get(url=endpoint, headers=header)
                response.raise_for_status()
                data = response.json()

            for installation in data:
                if (
                    installation["account"]["login"] == cookie["username"]
                    and installation["client_id"] == cookie["client_id"]
                ):
                    logfire.info(
                        f"Found github app installation id #{installation['id']}"
                    )
                    return GitInstallationResponse(**installation)

            logfire.info(
                "Did not find github app installation for username"
                + f"#{cookie['username']} with client_id #{cookie['client_id']}."
            )
            return None

        except HTTPStatusError as e:
            logfire.error(f"Internal Error: {e}")
            raise HTTPException(
                status=status.HTTP_40O_BAD_REQUEST,
                detail="Incorrect Request.",
            )
