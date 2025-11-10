from fastapi import APIRouter

from .git import app_api, git_api, repo_api
from .user import user_api

main_router = APIRouter()
main_router.include_router(app_api)
main_router.include_router(git_api)
main_router.include_router(user_api)
main_router.include_router(repo_api)

__all__ = ["main_router"]
