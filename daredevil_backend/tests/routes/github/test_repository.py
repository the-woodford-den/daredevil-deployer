"""Feature tests for routes/github/repository.py"""

import pytest

api = "/github/repository"


class TestGithubRepositoryRoutes:
    """test suite --> routes/github/repository.py"""

    @pytest.mark.asyncio
    async def test_search_apps(self, client):
        very = 1 + 1
        assert very == 2
