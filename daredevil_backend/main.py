import logfire
from fastapi import FastAPI

from .configs.settings import get_settings
from .dbs.engine import init_db
from .routes import github as git_routes
from .routes import user as user_routes

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
app.include_router(user_routes.api)


@app.on_event("startup")
async def startup_event():
    settings = get_settings()
    logfire_token = settings.logfire_token

    logfire.configure(
        token=logfire_token, environment="dev", service_name="daredevil-backend"
    )
    logfire.instrument_fastapi(app, capture_headers=True)

    await init_db()
