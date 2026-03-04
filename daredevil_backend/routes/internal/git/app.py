from fastapi import APIRouter

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


@api.post("/create", response_model=GitAppResponse)
async def create(
    *,
    cookie: CookieTokenDepend,
    service: GitAppServiceDepend,
):
    new_app = await app.get(cookie=cookie)
    return await service.add(new_app)
