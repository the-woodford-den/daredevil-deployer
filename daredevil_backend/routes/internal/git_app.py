from fastapi import APIRouter, Depends, HTTPException

from dependency import CookieTokenDepend, GitAppServiceDepend
from models.git import GitAppRead

api = APIRouter("/git_app")


@api.get("/", response_model=GitAppRead)
async def get_git_app(
    *,
    service: GitAppServiceDepend,
    cookie_data: CookieTokenDepend,
):
    return service.get(cookie_data["user_id"])


@api.post("/create", response_model=GitAppRead)
async def create_git_app(
    *,
    service: GitAppServiceDepend,
    cookie_data: CookieTokenDepend,
):
    pass
