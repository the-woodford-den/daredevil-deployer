from fastapi import APIRouter
from dependency import CookieTokenDepend, GitInstallationServiceDepend
from models.git.installation import GitInstallationResponse, GitInstallationRead
from routes.external.git import installation

api = APIRouter(prefix="/git/installation")


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
    cookie: CookieTokenDepend,
    service: GitInstallationServiceDepend,
):
    ins_resp = await installation.get(service=service, cookie=cookie)
    return await service.add(GitInstallationResponse.model_validate(ins_resp))
