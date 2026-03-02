import logfire
from fastapi import APIRouter, HTTPException
from starlette.status import HTTP_400_BAD_REQUEST as status_400
from httpx import AsyncClient, HTTPStatusError, RequestError
from rich import inspect

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
    In addition to returning App, it returns install count with the App"""

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

        except HTTPStatusError as e:
            status_code = int(e.response.status_code)
            status_detail = (
                f"Response Error: {status_code} No git app for"
                f"{cookie['username']} with client_id {cookie['client_id']}."
            )
        except RequestError as e:
            status_detail = (
                f"Request Error: {e.request.url!s} No git app for "
                f"{cookie['username']} with client_id {cookie['client_id']}"
            )
        finally:
            error_code = status_400 if status_code is None else status_code
            error_msg = "unknown" if status_detail is None else status_detail
            logfire.error(error_msg)
            raise HTTPException(
                status_code=error_code,
                detail=error_msg,
            )
