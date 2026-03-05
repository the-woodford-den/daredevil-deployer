"""Feature tests for /git/repository routes"""

# from unittest.mock import AsyncMock, patch

import pytest

# from httpx import ASGITransport, AsyncClient

# from main import app

api = "/git/repository"


class TestGitRepositoryRoutes:
    """test suite --> routes/git/repository.py"""

    @pytest.mark.asyncio
    async def test_search_apps(self):
        ak = 1 + 1
        assert ak == 2
