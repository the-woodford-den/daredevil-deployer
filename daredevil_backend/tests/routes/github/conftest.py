"""Test fixtures for routes/github tests."""

import os
from typing import AsyncGenerator

import pytest_asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession

from configs import get_settings
from dbs import get_async_session, init_db
from models.github import AppRecord


@pytest_asyncio.fixture(scope="function")
async def setup_test_db():
    """Setup test database for each test."""
    os.environ["ENVIRONMENT"] = "test"
    await init_db()
    yield


@pytest_asyncio.fixture
async def async_test_session() -> AsyncGenerator[AsyncSession, None]:
    """async test session for db activities"""
    session = await get_async_session()
    try:
        yield session
    finally:
        await session.rollback()
        await session.close()


@pytest_asyncio.fixture(autouse=False)
async def cleanup_tables():
    """Remove tables after each test for isolation."""
    yield

    settings = get_settings()
    db_url = settings.db_url.rsplit("/", 1)[0] + "/daredevil_test"
    cleanup_engine = create_async_engine(db_url)

    try:
        async with cleanup_engine.begin() as connection:
            await connection.execute(
                text(
                    """
                    TRUNCATE TABLE github_app_records,
                                   github_installation_records,
                                   github_repositories,
                                   users
                    RESTART IDENTITY CASCADE
                    """
                )
            )
    finally:
        await cleanup_engine.dispose()


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
