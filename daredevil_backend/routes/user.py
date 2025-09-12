import asyncio
import time

import logfire
from fastapi import APIRouter
from httpx import AsyncClient
from rich import inspect, print

api = APIRouter(prefix="/user")

logfire.configure(service_name="daredevil")


# Example API request with user access token
@api.get("/github/user")
async def get_github_user(*, access_token: str):
    endpoint = f"https://api.github.com/user"
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "Authorization": f"Bearer {access_token}",
    }

    with logfire.span("accessing github api for user with token ..."):
        try:
            async with AsyncClient() as viper:
                response = await viper.post(url=endpoint, headers=headers)

            print(response)
            return response.json()
        except Exception as e:
            logfire.error("error message: {msg=}", msg=e)
