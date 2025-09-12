import logfire
from fastapi import APIRouter, HTTPException
from httpx import AsyncClient
from rich import inspect

api = APIRouter(prefix="/github")

logfire.configure(service_name="daredevil")


@api.get("/repos")
async def get_repos(*, username: str, client_id: str):
    endpoint = f"https://api.github.com/{username}/woodFordR/repos"
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "Authorization": f"Bearer {client_id}",
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
