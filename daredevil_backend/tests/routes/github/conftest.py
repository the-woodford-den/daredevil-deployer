"""Test fixtures for routes/github tests."""

import os
from typing import AsyncGenerator

import pytest_asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from configs import get_settings
from dbs import get_async_session
from main import app
from models.github import AppRecord, InstallationRecord, Repository
from models.user import User

"""testing database"""
engine = create_async_engine(url = settings.db_url)
test_session = sessionmaker(
    bind=engine. class_=AsyncSession, expire_on_commit=False
)


@pytest_asyncio.fixture
async def get_session_override() -> AsyncGenerator[AsyncSession, None]:
    """async test session for db activities"""
    async with test_session() as session:
        yield session


@pytest_asyncio.fixture(scope="session")
async def client():
    async with AsyncClient(
        transport=ASGITransport(app),
        base_url="http://test",            
        ) as client:
        yield client


@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_and_tear_down_test_db():
    """Setup test database for each test."""
    """and tear it down tear it down after """
    """each test for isolation."""

    settings = get_settings()
    if settings.env != "test":
        raise Exception("STOP, wrong environment, set it up again please...")

    app.dependency_overrides[get_async_session] = get_session_override

    async with engine.begin() as connection:
        await connection.run_sync(SQLModel.metadata.create_all)

    async with test_session() as session:
        await sample_app_record(session)

    yield

    async with cleanup_engine.begin() as connection:
        await connection.run_sync(SQLModel.metadata.drop_all)

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
    async with test_session() as session:
        session.add(app_record)
        await session.commit()
        await session.refresh(app_record)

        return app_record
