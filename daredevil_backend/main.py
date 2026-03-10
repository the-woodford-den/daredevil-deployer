import json
from contextlib import asynccontextmanager
import time as t
import logfire

from fastapi.exceptions import RequestValidationError
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse, Response
from typing import Callable, Awaitable

from configs import get_settings
from dbs import data_store
from routes import main_router

settings = get_settings()


class ASGIMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        await self.app(scope, receive, send)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        contact={
            "email": "den@woodford.life",
            "name": "woodFordR",
            "status": "chocolate chunky",
        },
        title="DDDD: DareDevilDeployerDocs",
        version="1.0.0",
        description="Interact & try our schema",
        routes=app.routes,
    )
    for path in [
        "/git/hub/app/",
        "/git/hub/installation/",
        "/git/hub/repository/all",
    ]:
        openapi_schema["paths"].pop(path, None)
    app.openapi_schema = openapi_schema

    return app.openapi_schema


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize database on startup
    data_store.init(settings.db_url)
    yield
    # Cleanup on shutdown
    if data_store._engine is not None:
        await data_store.close()


app = FastAPI(
    version="1.0.0",
    lifespan=lifespan,
    title=settings.app_title,
)
app.include_router(main_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["localhost", "127.0.0.1"],
)
app.add_middleware(ASGIMiddleware)

logfire.configure(
    token=settings.logfire_token,
    environment=settings.env,
    service_name=settings.logfire_name,
)
logfire.instrument_fastapi(app, capture_headers=True)
app.openapi = custom_openapi


@app.get("/")
async def get_root():
    logfire.info("Daredevil Deployer Application")
    return {"message": "Daredevil Deployer Application"}


@app.middleware("http")
async def req_time_header(
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
):
    request.state.start_time = t.time()
    resp = await call_next(request)

    end_time = t.time() - request.state.start_time
    resp.headers["X-Req-Time"] = (
        f"||{t.strftime('%H:%M:%S', t.gmtime(end_time))}||"
    )
    return resp


@app.exception_handler(RequestValidationError)
async def validation_exception(req: Request, err: RequestValidationError):
    sts = status.HTTP_400_BAD_REQUEST

    logfire.error(
        f"||Request error on validation: {req.url}||\n"
        f"{json.dumps(err.errors(), indent=4)}",
        status=sts,
    )
    return JSONResponse(
        status_code=400,
        content=err.body,
    )


@app.exception_handler(HTTPException)
async def http_exception(req: Request, err: HTTPException):
    logfire.error(
        f"||{getattr(req.client, 'host', 'X.X.X.X')}::"
        + f"{getattr(req.client, 'port', 'XXXX')}||::"
        + f"{t.time()}||\n||{err.detail}"
    )
    return JSONResponse(
        status_code=err.status_code,
        content=err.detail,
    )
