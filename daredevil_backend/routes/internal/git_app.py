import logfire
from fastapi import APIRouter, Depends, HTTPException

from dependency import CookieTokenDepend, GitAppServiceDepend
from models.git import GitAppRead, GitAppResponse
from routes import git_api

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
    new_app = await git_api.get_app(token=cookie_data)
    app_resp = GitAppResponse(**new_app)
    git_app = await service.add(data=app_resp)
    logfire.info("GitHub App Validated & Stored in DB")
    return git_app
