from typing import List

import logfire
from fastapi import APIRouter, HTTPException
from httpx import AsyncClient
from rich import inspect
from sqlmodel import select

from dbs import get_async_session
from models.github import AppRecord, RepositoryResponse

api = APIRouter(prefix="/repository")


@api.get("/collect")
async def collect_repositories(
    *, app_record_id: str
) -> List[RepositoryResponse]:
    """Searches the Github Api and returns the Github App's associated Repositories."""
    """This includes the organization and other users who installed the App."""

    with logfire.span("Finding AppRecord in ..."):
        session = await get_async_session()
        async with session:
            statement = select(AppRecord).where(
                AppRecord.github_app_id == app_record_id
            )
            app_record = (await session.exec(statement)).one_or_none()
            if app_record is None:
                logfire.error(f"AppRecord not located: ${app_record_id}")
                return {"status_code": 404, "message": "Not Found."}

            logfire.info(f"AppRecord located: ${app_record.slug}")
            user_token = app_record.token

        endpoint = "https://api.github.com/user/repos"
        header = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "Authorization": f"Bearer {user_token}",
        }

    with logfire.span("Searching Github App's list of repositories ..."):
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
                    logfire.info(f"Iterating through repository: ${repo.name}")
                    repo_response.append(repo_obj)

            return repo_list

        except HTTPException as e:
            logfire.error("Error Message {msg=}", msg=e)
            raise HTTPException(status_code=e.status_code, detail=e.detail)
