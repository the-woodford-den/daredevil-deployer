"""Test fixtures for routes/git tests."""

import os
from typing import AsyncGenerator

os.environ["ENVFILE"] = ".env.example"

import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from configs import get_settings
from dbs import get_async_session
from main import app
from models.git import GitApp, GitInstall, Repository
from models.user import User

settings = get_settings()

"""testing database"""
engine = create_async_engine(url=settings.db_url)
test_session = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


async def get_session_override() -> AsyncGenerator[AsyncSession, None]:
    """async test session for db activities - used for dependency override"""
    async with test_session() as session:
        yield session


@pytest_asyncio.fixture
async def async_test_session() -> AsyncGenerator[AsyncSession, None]:
    """async test session fixture for direct use in tests"""
    async with test_session() as session:
        yield session


@pytest_asyncio.fixture
async def client():
    async with AsyncClient(
        transport=ASGITransport(app),
        base_url="http://test",
    ) as client:
        yield client


@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_and_tear_down_test_db():
    """Setup test database once for all tests in this session."""
    """Tear it down after all tests complete."""
    settings = get_settings()

    if settings.env != "test":
        raise Exception("STOP, wrong environment, set it up again please...")

    app.dependency_overrides[get_async_session] = get_session_override

    async with engine.begin() as connection:
        await connection.run_sync(SQLModel.metadata.create_all)

    # Dispose of all connections so new ones are created per test on correct event loop
    await engine.dispose()

    yield

    # Clean up - wrap in try/except to handle event loop issues on teardown
    try:
        async with engine.begin() as connection:
            await connection.run_sync(SQLModel.metadata.drop_all)
    except Exception:
        pass  # Ignore errors during teardown cleanup

    app.dependency_overrides.clear()
    await engine.dispose()


@pytest_asyncio.fixture
async def sample_app_record(async_test_session: AsyncSession) -> GitApp:
    """Create test GitApp in the test database."""
    git_app = GitApp(
        github_app_id=777247,
        slug="batman",
        node_id="19020",
        client_id="1e43tf3",
        name="batman",
        description="I am batman",
        external_url="https://batman.batman",
        html_url="https://github.com/apps/batman",
    )
    async with test_session() as session:
        session.add(git_app)
        await session.commit()
        await session.refresh(git_app)

        return app
