import asyncio
import time
from typing import List

import logfire
from fastapi import APIRouter, HTTPException, WebSocket
from httpx import AsyncClient
from rich import inspect, print
from sqlmodel import select

from ..dbs.engine import get_async_session
from ..models.github import (CreateTokenResponse, OAuthAccessTokenResponse,
                             RepositoryResponse, UserResponse)
from ..models.user import User

api = APIRouter(prefix="/github")


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_update(self, msg: str, websocket: WebSocket):
        await websocket.send_text(msg)

    async def broadcast(self, msg: str):
        for connection in self.active_connections:
            await connection.send_text(msg)


manager = ConnectionManager()


@api.websocket("/poll-create-token/{id}")
async def poll_create_token(*, id: str, websocket: WebSocket):
    await manager.connect(websocket)
    session = await get_async_session()
    async with session:
        statement = select(User).where(User.id == id)
        user = (await session.exec(statement)).one_or_none()
        inspect(user)
    interval = user.interval or 15
    logfire.info(f"Starting polling with interval: {interval} seconds")

    while True:
        token_link = "https://github.com/login/oauth/access_token"
        header = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "daredevil-token-depot",
        }
        grant_type = "urn:ietf:params:oauth:grant-type:device_code"

        logfire.info("polling user access token with code ...")
        await manager.send_update(
            f"polling user access token at github (waiting {interval}s) ...",
            websocket,
        )
        start_time = time.time()
        try:
            while time.time() - start_time < user.expires_in:
                # Wait for the interval before polling
                logfire.info(f"Waiting {interval}s before next poll...")
                await asyncio.sleep(interval)

                async with AsyncClient() as viper:
                    response = await viper.post(
                        url=token_link,
                        headers=header,
                        data={
                            "client_id": user.client_id,
                            "device_code": user.device_code,
                            "grant_type": grant_type,
                        },
                    )

                    oauth_response = response.json()
                    logfire.info(f"GitHub response: {oauth_response}")

                    if "access_token" in oauth_response:
                        oa_atr_model = OAuthAccessTokenResponse.model_validate(
                            oauth_response
                        )
                        logfire.info("GH user access token collected")
                        await manager.send_update(
                            f"OAuth token retrieved: {oa_atr_model.access_token}",
                            websocket,
                        )
                        async with session:
                            user.access_token = oa_atr_model.access_token
                            session.add(user)
                            await session.commit()
                            await session.refresh(user)
                            print(user)

                        manager.disconnect(websocket)
                        inspect(user)
                        break
                    elif "error" in oauth_response:
                        error = oauth_response.get("error")
                        match error:
                            case "authorization_pending":
                                logfire.info("Authorization is Pending")
                                await manager.send_update(
                                    "Authorization is Pending", websocket
                                )
                            case "slow_down":
                                interval += 10
                                logfire.info(
                                    f"authorization slow down - increasing interval to {interval}s"
                                )
                                await manager.send_update(
                                    f"Authorization Slow Down - waiting {interval}s",
                                    websocket,
                                )
                            case "incorrect_device_code":
                                logfire.info(
                                    "Incorrect Device Code, Try Again."
                                )
                                await manager.send_update(
                                    "Incorrect Device Code, Try Again.",
                                    websocket,
                                )
                            case _:
                                if error in [
                                    "expired_token",
                                    "access_denied",
                                    "device_flow_disabled",
                                    "unsupported_grant_type",
                                    "incorrect_client_credentials",
                                ]:
                                    raise Exception(error)
                        continue

        except Exception as e:
            logfire.error(f"GitHub OAuth Polling Error: {e.msg}")
            await manager.send_update(
                f"GitHub OAuth Polling Error: {e.msg}", websocket
            )
            manager.disconnect(websocket)
            raise Exception(f"Error: {e.msg}")
        finally:
            logfire.info("GitHub OAuth polling closed")
            await manager.send_update("GitHub OAuth polling closed.", websocket)
            manager.disconnect(websocket)


# OAuth Device Authorization
@api.post("/create-token")
async def create_token(*, client_id: str) -> UserResponse:
    endpoint = "https://github.com/login/device/code"
    header = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "daredevil-token-depot",
    }

    with logfire.span("requesting github device-flow user token ..."):
        try:
            async with AsyncClient() as viper:
                response = await viper.post(
                    url=endpoint, headers=header, data={"client_id": client_id}
                )

            if response.status_code == 200:
                ctr_model = CreateTokenResponse.model_validate(response.json())

                logfire.info(f"github token response: {ctr_model}")
                session = await get_async_session()
                async with session:
                    user = User.model_validate(response.json())
                    user.client_id = client_id
                    session.add(user)
                    await session.commit()
                    await session.refresh(user)
                    data = user.model_dump()
                    inspect(data)
                    return data
            else:
                return response

        except Exception as e:
            logfire.error(f"Authentication request failed with : {e}")
            raise Exception(f"Authentication request failed with : {e}")


@api.get("/repos")
async def get_repos(*, user_token: str) -> List[RepositoryResponse]:
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
