import asyncio
import time
from typing import List

import logfire
from fastapi import APIRouter, HTTPException, WebSocket
from httpx import AsyncClient
from rich import inspect, print

from ..models.github import RepositoryResponse

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


@api.websocket("/create-token-status/{auth_request}")
async def create_token_status(*, auth_request, websocket: WebSocket):
    await manager.connect(websocket)
    while True:
        header = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "daredevil-token-depot",
        }
        client_id = auth_request.get("client_id", "1")
        device_code = auth_request.get("device_code", "2")
        interval = auth_request.get("interval", 5)
        expires_in = auth_request.get("expires_in", 600)
        endpoint = "https://github.com/login/oauth/access_token"
        grant_type = "urn:ietf:params:oauth:grant-type:device_code"

        logfire.info("polling user access token with code ...")
        await manager.send_update(
            "polling user access token with code ...", websocket
        )
        start_time = time.time()
        async with AsyncClient() as viper:
            try:
                while time.time() - start_time < expires_in:
                    response = await viper.post(
                        url=endpoint,
                        headers=header,
                        data={
                            "client_id": client_id,
                            "device_code": device_code,
                            "grant_type": grant_type,
                        },
                    )

                response_data = response.json()

                if "access_token" in response_data:
                    token = {}
                    token["user_token"] = response_data["access_token"]

                    logfire.info(f"GH user access token {token}")
                    await manager.send_update(f"token: {token}", websocket)

                    manager.disconnect(websocket)
                    return token
                elif "error" in response_data:
                    error = response_data.get("error")
                    match error:
                        case "authorization_pending":
                            logfire.info("authorization is pending")
                            await manager.send_update(
                                "authorization is pending", websocket
                            )
                            await asyncio.sleep(interval)
                        case "slow_down":
                            logfire.info("authorization slow down")
                            await manager.send_update(
                                "authorization slow down", websocket
                            )
                            interval += 5
                            await asyncio.sleep(interval)
                        case _:
                            if error in ["expired_token", "access_denied"]:
                                logfire.error(f"GH oauth error: {error}")
                                await manager.send_update(
                                    f"GH oauth error: {error.msg}", websocket
                                )
                                manager.disconnect(websocket)
                                raise Exception(f"GH oauth fail {error.msg}")
                else:
                    logfire.error(
                        f"Github oauth error in response: {response_data}"
                    )
                    await manager.send_update(
                        f"GitHub oauth error in response: {response_data}",
                        websocket,
                    )
                    await asyncio.sleep(interval)
                continue

            finally:
                logfire.error("GitHub OAuth polling timed out")
                await manager.send_update(
                    "GitHub OAuth polling timed out", websocket
                )
                manager.disconnect(websocket)
                raise Exception("GitHub OAuth polling timed out")


# OAuth Device Authorization
@api.post("/create-token")
async def create_token(*, client_id: str) -> dict:
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

                print(response)
                auth_request = response.json()
                print(auth_request)

                if "device_code" in auth_request:
                    device_code = auth_request["device_code"]
                else:
                    raise Exception(f"no device code! {auth_request}")

                logfire.info(f"github login info: {auth_request}")
                return {"device_code": device_code, "link": endpoint}

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
