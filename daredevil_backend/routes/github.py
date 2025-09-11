import logfire
from dotenv import dotenv_values
from fastapi import APIRouter, HTTPException
from httpx import AsyncClient
from rich import inspect

# from ..models.github import GithubUserRead

api = APIRouter(prefix="/github")

logfire.configure(service_name="daredevil")

config = dotenv_values(".env")
GITHUB_TOKEN = config.get("PERSONAL_ACCESS_TOKEN")


@api.get("/repos")
async def get_repos():
    endpoint = f"https://api.github.com/users/woodFordR/repos"
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "Authorization": f"Bearer {config.get('PERSONAL_ACCESS_TOKEN')}",
    }

    with logfire.span("... authentication user & github ..."):
        async with AsyncClient(timeout=60) as radar:
            try:
                response = await radar.get(
                    headers=headers,
                    url=endpoint,
                )

                return response.json()

            except HTTPException as e:
                logfire.error("Error Message {msg=}", msg=e)
