from functools import lru_cache

import logfire
from fastapi import FastAPI

from .config.settings import Settings
from .routes import github as git_routes
from .routes import user as user_routes


@lru_cache
def get_settings() -> Settings:
    return Settings()


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(git_routes.api)
    app.include_router(user_routes.api)
    settings = get_settings()
    print(settings.gh_username)
    logfire_token = settings.logfire_token

    logfire.configure(token=logfire_token)
    logfire.instrument_fastapi(app, capture_headers=True)

    # basicConfig(handlers=[logfire.LogfireLoggingHandler()])
    # logger = getLogger(__name__)
    # logger.info("~Daredevil Backend~")

    return app


app = create_app()
