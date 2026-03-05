from contextlib import asynccontextmanager
import datetime as dt

import logfire
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from configs import get_settings
from dbs import data_store
from routes import main_router

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
app.include_router(main_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logfire.configure(
    token=settings.logfire_token,
    environment=settings.env,
    service_name=settings.logfire_name,
)
logfire.instrument_fastapi(app, capture_headers=True)


@app.get("/")
async def get_root():
    logfire.info("Daredevil Deployer Application")
    return {"message": "Daredevil Deployer Application"}


@app.exception_handler(HTTPException)
async def http_exception(req: Request, exc):
    logfire.error(
        f"||{getattr(req.client, 'host', 'X.X.X.X')}::"
        + f"{getattr(req.client, 'port', 'XXXX')}||::"
        + f"{dt.datetime.now(dt.timezone.utc)}||\n||{exc.message}"
    )
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": "Oof! Something is wrong."},
    )


@app.middleware("http")
async def req_time_header(request: Request, call_next):
    request.state.start_time = dt.datetime.now(dt.timezone.utc)
    resp = await call_next(request)

    end_time = dt.datetime.now(dt.timezone.utc) - request.state.end_time
    resp.headers["X-Req-Time"] = f"||{end_time.strftime('%H:%M:%%S')}||"
    return resp
