from fastapi import APIRouter

from .external import (ConnectionManager, git_hub_api, git_hub_app_api,
                       git_hub_installation_api, git_hub_repository_api)
from .internal import auth_api, git_app_api, git_installation_api, user_api

main_router = APIRouter()
main_router.include_router(auth_api)
main_router.include_router(git_app_api)
main_router.include_router(git_installation_api)
main_router.include_router(git_hub_api)
main_router.include_router(git_hub_app_api)
main_router.include_router(git_hub_installation_api)
main_router.include_router(git_hub_repository_api)
main_router.include_router(user_api)

__all__ = ["ConnectionManager", "main_router"]
