from typing import List

import logfire
from fastapi import APIRouter, Depends, HTTPException
from httpx import AsyncClient
from rich import inspect
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from dbs import get_async_session
from models.github import Repository, RepositoryResponse

api = APIRouter(prefix="/github/repository")


@api.get("/all", response_model=List[RepositoryResponse])
async def get_all_repositories(
    *,
    token: str,
    session: AsyncSession = Depends(get_async_session),
):
    """Searches the Github Api and returns the Github App's associated Repositories."""
    """This includes the organization and other users who installed the App."""

    endpoint = "https://api.github.com/user/repos"
    header = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "Authorization": f"Bearer {token}",
    }

    with logfire.span("Searching Github App's list of repositories ..."):
        try:
            async with AsyncClient(timeout=60) as viper:
                response = await viper.get(headers=header, url=endpoint)
                repository_list = response.json()
                inspect(repository_list)
                responses = []
                logfire.info("Iterating through repositories ...")
                for repo in repository_list:
                    inspect(repo)
                    repository_dict = repo.json()
                    repo_obj = RepositoryResponse.model_validate(
                        repository_dict
                    )
                    responses.append(repo_obj)

                    statement = select(Repository).where(
                        Repository.github_repository_id == repo_obj.id
                    )
                    result = (await session.execute(statement)).first()

                    if result:
                        repo_id = repo_obj.id
                        repository_obj = RepositoryResponse.model_dump(repo_obj)
                        del repository_obj["id"]
                        repository_obj["github_repository_id"] = repo_id
                        repository = Repository.model_validate(repository_obj)

                        session.add(repository)
                        await session.commit()
                        await session.refresh(repository)

            return responses

        except HTTPException as e:
            logfire.error("Error Message {msg=}", msg=e)
            raise HTTPException(status_code=e.status_code, detail=e.detail)
