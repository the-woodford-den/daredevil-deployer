import asyncio
import time
from typing import Annotated

import logfire
from fastapi import APIRouter, Depends
from httpx import AsyncClient
from rich import inspect, print
from sqlmodel import select

from ..configs.auth import GithubJWT
from ..dbs.engine import get_async_session
from ..models.github import App
from ..models.user import User

api = APIRouter(prefix="/user")


#
@api.get("/github-app")
async def github_app():
    session = GithubJWT()
    jwt = session.generate()

    endpoint = "https://api.github.com/app"
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

            session = await get_async_session()
            async with session:
                statement = select(User).where(
                    User.github_owner_id == auth_response["owner"]["id"]
                )
                user = (await session.exec(statement)).one_or_none()
                if user is None:
                    github_id_value = auth_response["owner"]["id"]
                    del auth_response["owner"]["id"]
                    auth_response["owner"]["github_owner_id"] = github_id_value
                    create_user = auth_response["owner"]
                    user_obj = User.model_validate(create_user)
                    session.add(user_obj)
                    await session.commit()
                    await session.refresh(user_obj)
                    user = user_obj
                    logfire.info(f"User {user_obj.login} created!")

                del auth_response["owner"]
                statement = select(App).where(
                    App.github_app_id == auth_response["id"]
                )
                github_app = (await session.exec(statement)).one_or_none()
                if github_app is None:
                    app_id_value = auth_response["id"]
                    del auth_response["id"]
                    auth_response["github_app_id"] = app_id_value
                    create_github_app = auth_response
                    app_obj = App.model_validate(create_github_app)
                    session.add(app_obj)
                    await session.commit()
                    await session.refresh(app_obj)
                    logfire.info(f"Github App {app_obj.slug} created!")

            return auth_response
        except Exception as e:
            logfire.error("error message: {msg=}", msg=e)
