from fastapi import APIRouter

# import logfire
# import debugpy
from dependency import CookieTokenDepend, GitAppServiceDepend
from models.git import GitAppCreate, GitAppRead, GitAppResponse
from routes.external.git import app

api = APIRouter(prefix="/git/app")


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
    body: GitAppCreate,
    cookie: CookieTokenDepend,
    service: GitAppServiceDepend,
):

    new_app = await app.get(client_id=body.client_id)
    return await service.add(new_app)
