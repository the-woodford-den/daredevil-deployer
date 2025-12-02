import logfire
from fastapi import APIRouter

from dependency import CookieTokenDepend, GitAppServiceDepend
from models.git import GitAppCreate, GitAppRead, GitAppResponse
from routes import git_api

api = APIRouter("/git/app")


@api.get("/", response_model=GitAppRead)
async def get(
    *,
    cookie: CookieTokenDepend,
    service: GitAppServiceDepend,
):
    return service.get_by_username(cookie["username"])


@api.post("/create", response_model=GitAppRead)
async def create(
    *,
    cookie: CookieTokenDepend,
    create_app: GitAppCreate,
    service: GitAppServiceDepend,
):
    new_app = await git_api.get_app(data=GitAppCreate, token=cookie)
    app_resp = GitAppResponse(**new_app)
    git_app = await service.add(data=app_resp)
    logfire.info("GitHub App Validated & Stored in DB")
    return git_app
