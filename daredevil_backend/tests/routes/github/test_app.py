"""Feature tests for routes/github/app.py"""

from unittest.mock import AsyncMock, patch

import pytest
from httpx import ASGITransport, AsyncClient

from main import app

api = "/github/app"


class TestGithubAppRoutes:
    """test suite --> routes/github/app.py"""

    @pytest.mark.asyncio
    async def test_search_apps(self, client: AsyncClient):
        """Test searching for a GitHub app by slug - mocks GitHub API"""
        test_slug = "batman"

        mock_github_response = {
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

        with patch("routes.github.app.AsyncClient") as MockAsyncClient:
            mock_client = MockAsyncClient.return_value.__aenter__.return_value

            mock_response = AsyncMock()
            mock_response.json = lambda: mock_github_response

            mock_client.get = AsyncMock(return_value=mock_response)

            async with AsyncClient(
                transport=ASGITransport(app=app), base_url="http://test"
            ) as client:
                response = await client.get(f"{api}/search/{test_slug}")

                assert response.status_code == 200
                response_data = response.json()
                assert response_data["slug"] == "batman"
                assert response_data["id"] == 777247
                assert response_data["name"] == "batman"
