import logfire
from fastapi import APIRouter, Depends, HTTPException

from dependency import CookieTokenDepend, GitInstallServiceDepend
from models.git import GitInstallRead, GitInstallResponse
from routes import git_api

api = APIRouter("/git_install")


@api.get("/", response_model=GitInstallRead)
async def get_git_install(
    *,
    service: GitInstallServiceDepend,
    cookie_data: CookieTokenDepend,
):
    return service.get(cookie_data["user_id"])


@api.post("/create", response_model=GitInstallRead)
async def create_git_install(
    *,
    service: GitInstallServiceDepend,
    cookie_data: CookieTokenDepend,
):
    installations = []
    new_installs = await git_api.get_install(token=cookie_data)
    for git_install in new_installs:
        if git_install["account"]["login"] == cookie_data["username"]:
            logfire.info("username matched, checking db record...")
            install_obj = GitInstallResponse(**git_install)
            logfire.info(f"Adding GitInstallation: {install_obj.id}")
            installation = await service.add(install_obj)
            installations.append(installation)
    return installations[0]
