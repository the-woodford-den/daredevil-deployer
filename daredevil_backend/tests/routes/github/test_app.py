"""Feature tests for routes/github/app.py"""

import pytest
from unittest.mock import AsyncMock, patch

from models.github import AppRecordResponse


@pytest.fixture
def mock_github_response():
    """Fixture to provide mock GitHub API response data"""
    return {
        "id": 777247,
        "slug": "batman",
        "node_id": "19020",
        "client_id": "1e43tf3",
        "name": "batman",
        "description": "I am batman",
        "external_url": "https://batman.batman",
        "html_url": "https://github.com/apps/batman",
        "owner": None,
        "events": [],
        "permissions": None,
    }


class TestGithubAppRoutes:
    """test suite --> routes/github/app.py"""

    @pytest.mark.asyncio
    async def test_response_app_search_slug(self, session, mock_github_response):
        """Test searching for a GitHub App by slug - unit test with mocked httpx"""
        from routes.github.app import search_apps

        # Create fully custom mocks without AsyncMock
        class MockResponse:
            def json(self):
                return mock_github_response

        class MockAsyncClient:
            async def __aenter__(self):
                return self

            async def __aexit__(self, exc_type, exc_val, exc_tb):
                return None

            async def get(self, url, headers=None):
                return MockResponse()

        # Patch AsyncClient at the module level before calling
        with patch('routes.github.app.AsyncClient', MockAsyncClient):
            # Call the route function directly
            result = await search_apps(slug="batman", session=session)

            # Verify the result
            assert isinstance(result, AppRecordResponse)
            assert result.slug == "batman"
            assert result.id == 777247
            assert result.name == "batman"
            assert result.description == "I am batman"
            assert result.external_url == "https://batman.batman"
            assert result.html_url == "https://github.com/apps/batman"
