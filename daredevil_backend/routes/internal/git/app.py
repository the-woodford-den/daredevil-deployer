from fastapi import APIRouter, HTTPException

# import logfire
# import debugpy
from dependency import CookieTokenDepend, GitAppServiceDepend
from models.git import GitAppRead, GitAppResponse
from routes.external.git import app

api = APIRouter(prefix="/git/app")


@api.get("/", response_model=GitAppRead)
async def get(
    *,
    cookie: CookieTokenDepend,
    service: GitAppServiceDepend,
):
    return service.get_by_username(cookie["username"])


@api.post("/create", response_model=GitAppRead | None)
async def create(
    *,
    cookie: CookieTokenDepend,
    service: GitAppServiceDepend,
):
    try:
        new_app = await app.get(service=service, cookie=cookie)

        app_resp = GitAppResponse(**new_app.model_dump())
        return await service.add(data=app_resp)

    except HTTPException:
        return None
