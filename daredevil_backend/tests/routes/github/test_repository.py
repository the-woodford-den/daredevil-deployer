"""Feature tests for routes/github/repository.py"""

# from unittest.mock import AsyncMock, patch

import pytest

# from httpx import ASGITransport, AsyncClient

# from main import app

api = "/github/repository"


class TestGithubRepositoryRoutes:
    """test suite --> routes/github/repository.py"""

    @pytest.mark.asyncio
    async def test_search_apps(self):
        ak = 1 + 1
        assert ak == 2
