"""Test fixtures for routes/github tests."""

from typing import AsyncGenerator

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from rich import inspect
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from configs import GithubAppLib, get_settings
from dbs import get_async_session
from main import app
from models.github import AppRecord, InstallationRecord, Repository
from models.user import User

"""testing database"""

settings = get_settings()

# Don't create engine at module level - create in fixtures instead
_engine = None
_test_session_maker = None


def get_engine():
    """Get or create the async engine"""
    global _engine
    if _engine is None:
        from sqlalchemy.pool import NullPool
        # Use NullPool to avoid connection pooling issues across event loops
        _engine = create_async_engine(
            url=settings.db_url,
            poolclass=NullPool,
            echo=False
        )
    return _engine


def get_test_session_maker():
    """Get or create the session maker"""
    global _test_session_maker
    if _test_session_maker is None:
        _test_session_maker = async_sessionmaker(
            bind=get_engine(), class_=AsyncSession, expire_on_commit=False
        )
    return _test_session_maker


async def get_session_override() -> AsyncGenerator[AsyncSession, None]:
    """async test session for db activities - used for FastAPI dependency override"""
    session_maker = get_test_session_maker()
    async with session_maker() as session:
        yield session


@pytest_asyncio.fixture
async def session() -> AsyncGenerator[AsyncSession, None]:
    """async test session fixture for use in tests"""
    session_maker = get_test_session_maker()
    async with session_maker() as session:
        yield session


@pytest_asyncio.fixture
async def async_client():
    async with AsyncClient(
        transport=ASGITransport(app),
        base_url="http://test",
    ) as client:
        yield client


@pytest.fixture
def client():
    from starlette.testclient import TestClient
    with TestClient(app) as client:
        yield client


@pytest_asyncio.fixture
async def jwt_token(token: str):
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "Authorization": f"Bearer {token}",
    }
    return headers


@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    """Setup test database once for the entire test session (synchronous)."""
    import asyncio

    inspect(settings)
    if settings.environment != "test":
        raise Exception("STOP, wrong environment, set it up again please...")

    app.dependency_overrides[get_async_session] = get_session_override

    # Create tables synchronously
    async def create_tables():
        engine = get_engine()
        async with engine.begin() as connection:
            await connection.run_sync(SQLModel.metadata.create_all)

    asyncio.run(create_tables())

    yield

    # Drop tables synchronously
    async def drop_tables():
        engine = get_engine()
        async with engine.begin() as connection:
            await connection.run_sync(SQLModel.metadata.drop_all)

    asyncio.run(drop_tables())
    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def sample_app_record(async_test_session: AsyncSession) -> AppRecord:
    """Create test AppRecord in the test database."""
    app_record = AppRecord(
        github_app_id=777247,
        slug="batman",
        node_id="19020",
        client_id="1e43tf3",
        name="batman",
        description="I am batman",
        external_url="https://batman.batman",
        html_url="https://github.com/apps/batman",
    )
    async with async_test_session() as session:
        session.add(app_record)
        await session.commit()
        await session.refresh(app_record)

        return app_record
