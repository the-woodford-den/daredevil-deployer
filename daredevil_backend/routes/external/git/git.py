from typing import List

import logfire
from fastapi import APIRouter, HTTPException, WebSocket
from httpx import AsyncClient, HTTPStatusError

api = APIRouter(prefix="/git")


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


@api.get("/status")
async def check_github_status():
    """Check Github Status"""

    url = "https://www.githubstatus.com/api/v2/summary.json"
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "daredevil-deployer",
    }

    try:
        async with AsyncClient() as viper:
            response = await viper.get(url=url, headers=headers)
            data = response.json()

        return data

    except HTTPStatusError as e:
        logfire.error(f"HTTP Status Error: {e.response.status_code}")

        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"GitHub error: {e.response.text}",
        )
