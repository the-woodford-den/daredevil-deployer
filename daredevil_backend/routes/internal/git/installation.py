import logfire
from fastapi import APIRouter

from dependency import CookieTokenDepend, GitInstallationServiceDepend
from models.git import GitInstallationCreate, GitInstallationRead
from routes import git_api

api = APIRouter("/git/installation")


@api.get("/", response_model=GitInstallationRead)
async def get(
    *,
    cookie: CookieTokenDepend,
    service: GitInstallationServiceDepend,
):
    return await service.get(cookie["username"])


@api.post("/create", response_model=GitInstallationRead)
async def create(
    *,
    cookie_data: CookieTokenDepend,
    create_installation: GitInstallationCreate,
    service: GitInstallationServiceDepend,
):
    installation_response = await git_api.get_install(token=cookie_data)
    return await service.add(installation_response)
