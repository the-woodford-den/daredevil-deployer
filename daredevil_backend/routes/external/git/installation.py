import logfire
from fastapi import APIRouter
from httpx import AsyncClient
from starlette.exceptions import HTTPException

from dependency import CookieTokenDepend
from models.git import GitInstallationResponse as Git_I_Resp
from utility import GitLib

api = APIRouter(prefix="/git/hub/installation")


@api.get(
    "/",
    response_model=Git_I_Resp,
    response_model_exclude_unset=True,
)
async def get(
    *,
    cookie: CookieTokenDepend,
):
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
        async with AsyncClient() as viper:
            response = await viper.get(url=endpoint, headers=header)
            response.raise_for_status()
            data = response.json()

        for i in data:
            if (
                i["account"]["login"] == cookie["username"]
                and i["client_id"] == cookie["client_id"]
            ):
                logfire.info(f"Git installation: #{i['id']}")
                return Git_I_Resp.model_validate(**i)

        raise HTTPException(status_code=404, detail="Git install not found")

    # except HTTPStatusError as e:
    #     logfire.error(f"Internal Error: {e}")
    #     raise HTTPException(
    #         status=status.HTTP_40O_BAD_REQUEST,
    #         detail="Incorrect Request.",
    #     )
