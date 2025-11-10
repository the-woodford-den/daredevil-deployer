from typing import List

import logfire
from fastapi import APIRouter, HTTPException
from httpx import AsyncClient, HTTPStatusError
from rich import inspect

from dependency import CookieTokenDepend, GitRepoServiceDepend, SessionDepend
from models.git import Repository
from models.user import User
from utility import GitLib

api = APIRouter(prefix="/git/repo")


@api.get("/all", response_model=List[Repository])
async def get_repos(
    *,
    session: SessionDepend,
    service: GitRepoServiceDepend,
    token: CookieTokenDepend,
):
    """Searches the Github Api and returns the Github App's associated Repositories.
    This includes the organization and other users who installed the App."""
    user = await session.get(User, token["user"]["id"])
    gh_lib = GitLib(session)
    jwt = gh_lib.create_jwt(client_id=user.client_id)

    endpoint = "https://api.github.com/user/repos"
    header = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "Authorization": f"Bearer {jwt}",
    }

    with logfire.span("Searching Github App's list of repositories ..."):
        try:
            repo_list = []
            async with AsyncClient() as viper:
                response = await viper.get(url=endpoint, headers=header)
                response.raise_for_status()
                data = response.json()
                logfire.info("Iterating through repositories ...")

                for repo in data:
                    repo_in_db = await service.get(repo["id"])
                    if not repo_in_db:
                        repo_in_db = await service.add(repo)
                    repo_list.append(repo_in_db)

            return repo_list

        except HTTPStatusError as e:
            logfire.error(f"Internal Error: {e}")
            raise HTTPException(
                status=e.status_code,
                detail="Incorrect Request.",
            )
