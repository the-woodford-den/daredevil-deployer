import logfire
from fastapi import APIRouter
from httpx import AsyncClient
from rich import inspect

from dependency import CookieTokenDepend
from models.git import GitAppResponse
from starlette.exceptions import HTTPException
from utility import GitLib

api = APIRouter(prefix="/git/hub/app")


@api.get(
    "/",
    response_model=GitAppResponse,
    response_model_exclude_unset=True,
)
async def get(
    *,
    client_id: str,
):
    """This GET request searches Github Api for a Github App with a token.
    In addition to returning App, it returns install count with the App"""

    git_lib = GitLib()
    jwt = git_lib.create_jwt(client_id=client_id)

    endpoint = "https://api.github.com/app"
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {jwt}",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    with logfire.span("Sending request for github app data."):
        async with AsyncClient(timeout=60.0) as viper:
            response = await viper.get(url=endpoint, headers=headers)
            response.raise_for_status()
            data = response.json()

        if data["id"] is None:
            raise HTTPException(status_code=404, detail="Git app not found")

        logfire.info(f"Git app: #{data['id']}")
        return data

    # except HTTPStatusError as e:
    #     status_code = int(e.response.status_code)
    #     status_detail = (
    #         f"Response Error: {status_code} No git app for"
    #         f"{cookie['username']} with client_id {cookie['client_id']}."
    #     )
    # except RequestError as e:
    #     status_detail = (
    #         f"Request Error: {e.request.url!s} No git app for "
    #         f"{cookie['username']} with client_id {cookie['client_id']}"
    #     )
