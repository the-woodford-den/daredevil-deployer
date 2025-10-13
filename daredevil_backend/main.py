import logfire
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .configs import get_settings
from .dbs import init_db
from .routes.github import app_api, github_api, repository_api

app = FastAPI()


@app.get("/")
async def get_root():
    logfire.info("Daredevil Deployer Application")
    return {"message": "Daredevil Deployer Application"}


app.include_router(github_api)
app.include_router(app_api)
app.include_router(repository_api)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    settings = get_settings()
    logfire_token = settings.logfire_token

    logfire.configure(
        token=logfire_token, environment="dev", service_name="daredevil-backend"
    )
    logfire.instrument_fastapi(app, capture_headers=True)

    await init_db()
