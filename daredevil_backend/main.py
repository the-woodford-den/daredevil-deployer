import logfire
from dotenv import dotenv_values
from fastapi import FastAPI

from .routes import github as git_routes
from .routes import user as user_routes

config = dotenv_values(".env")
logfire_token = config.get("LOGFIRE_TOKEN")


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(git_routes.api)
    app.include_router(user_routes.api)

    logfire.configure(token=logfire_token)
    logfire.instrument_fastapi(app, capture_headers=True)

    # basicConfig(handlers=[logfire.LogfireLoggingHandler()])
    # logger = getLogger(__name__)
    # logger.info("~Daredevil Backend~")

    return app


app = create_app()
