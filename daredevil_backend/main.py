import logfire
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .configs import get_settings
from .dbs import init_db
from .routes import user as user_routes
from .routes.github import authenticate as git_routes
from .routes.github import repository as repo_routes

# async def create_app() -> FastAPI:
#     app = FastAPI()
#     app.include_router(git_routes.api)
#     app.include_router(user_routes.api)
#     settings = get_settings()
#     logfire_token = settings.logfire_token
#
#     logfire.configure(
#         token=logfire_token, environment="dev", service_name="daredevil-backend"
#     )
#     logfire.instrument_fastapi(app, capture_headers=True)
#
#     await init_db()
#
#     return app


app = FastAPI()
app.include_router(git_routes.api)
app.include_router(repo_routes.api)
app.include_router(user_routes.api)
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
