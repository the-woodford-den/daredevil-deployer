import asyncio
import time

import logfire
from fastapi import APIRouter
from httpx import AsyncClient
from rich import inspect, print

from ..configs.auth import GithubJWT

api = APIRouter(prefix="/user")


#
@api.get("/get-github-app")
async def get_github_app():
    session = GithubJWT()
    jwt = session.generate()

    endpoint = f"https://api.github.com/app"
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "Authorization": f"Bearer {jwt}",
    }

    with logfire.span("asking github api for user access..."):
        try:
            async with AsyncClient() as viper:
                response = await viper.get(url=endpoint, headers=headers)
                auth_response = response.json()

            return auth_response
        except Exception as e:
            logfire.error("error message: {msg=}", msg=e)
