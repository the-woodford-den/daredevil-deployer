"""Test fixtures for routes/github tests."""

import os
from typing import AsyncGenerator

import pytest_asyncio
from sqlmodel.ext.asyncio.session import AsyncSession

from dbs import get_async_session, init_db
from models.github import AppRecord


@pytest_asyncio.fixture(scope="function", autouse=True)
async def setup_test_db():
    """Setup test database before each test and cleanup after."""

    os.environ["ENVIRONMENT"] = "test"
    await init_db()

    yield


@pytest_asyncio.fixture
async def async_test_session() -> AsyncGenerator[AsyncSession, None]:
    """Create an async test session for database operations."""
    session = await get_async_session()
    try:
        yield session
    finally:
        await session.close()


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
    async_test_session.add(app_record)
    await async_test_session.commit()
    await async_test_session.refresh(app_record)
    return app_record
