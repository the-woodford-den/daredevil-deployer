import asyncio

import logfire
from dotenv import dotenv_values
from fastapi import FastAPI

from daredevil_backend.routes import github as git_routes

config = dotenv_values(".env")


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(git_routes.api)
    logfire.configure(token=config.get("LOGFIRE_TOKEN"))
    logfire.instrument_fastapi(app, capture_headers=True)
    return app


app = create_app()
