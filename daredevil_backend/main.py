from contextlib import asynccontextmanager

import logfire
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from configs import get_settings
from dbs import data_store
from routes.github import app_api, github_api, repository_api

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize database on startup
    data_store.init(settings.db_url)
    yield
    # Cleanup on shutdown
    if data_store._engine is not None:
        await data_store.close()


app = FastAPI(lifespan=lifespan, title=settings.app_title)
app.include_router(github_api)
app.include_router(app_api)
app.include_router(repository_api)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logfire.configure(
    token=settings.logfire_token,
    environment=settings.environment,
    service_name=settings.logfire_name,
)
logfire.instrument_fastapi(app, capture_headers=True)


@app.get("/")
async def get_root():
    logfire.info("Daredevil Deployer Application")
    return {"message": "Daredevil Deployer Application"}


# end
