from typing import List

import logfire
from fastapi import APIRouter, HTTPException
from httpx import AsyncClient
from rich import inspect
from sqlmodel import select

from ...dbs import get_async_session
from ...models import App, RepositoryResponse

api = APIRouter(prefix="/repository")


@api.get("/")
async def get_repos(*, gha_id: str) -> List[RepositoryResponse]:
    session = await get_async_session()
    async with session:
        statement = select(App).where(App.github_app_id == gha_id)
        g_app = (await session.exec(statement)).one_or_none()
        if g_app is None:
            return {"status_code": 404, "message": "Not Found."}

        user_token = g_app.token

    endpoint = "https://api.github.com/user/repos"
    header = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "Authorization": f"Bearer {user_token}",
    }

    with logfire.span("... grabbing list of user repositories ..."):
        try:
            async with AsyncClient(timeout=60) as viper:
                response = await viper.get(
                    headers=header,
                    url=endpoint,
                )
                repo_list = response.json()
                repo_response = []
                for repo in repo_list:
                    repo_obj = RepositoryResponse.model_validate(repo)
                    inspect(repo_obj)
                    repo_response.append(repo_obj)

            return repo_list

        except HTTPException as e:
            logfire.error("Error Message {msg=}", msg=e)
            raise HTTPException(status_code=e.status_code, detail=e.detail)
