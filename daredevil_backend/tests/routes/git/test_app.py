"""Feature tests for routes/git/app.py"""

from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import UUID

import pytest
from httpx import ASGITransport, AsyncClient

from dependency.session import get_cookie_token, get_gitapp_service
from main import app
from models.git import GitApp

api = "/git/app"


class TestGithubAppRoutes:
    """test suite --> routes/git/app.py"""

    @pytest.mark.asyncio
    async def test_get_app(self, client: AsyncClient):
        """Test searching for a GitHub app by slug - mocks GitHub API"""

        mock_gitapp_json = {
            "id": 4567,
            "slug": "batman",
            "node_id": "19020",
            "client_id": "1e43tf3",
            "name": "batman",
            "description": "I am batman",
            "external_url": "https://batman.batman",
            "html_url": "https://github.com/apps/batman",
            "owner": {
                "avatar_url": "http://test.com/photo.png",
                "client_id": "kj231k413",
                "events_url": "http://test.com",
                "followers_url": "http://test.com",
                "following_url": "http://test.com",
                "gists_url": "http://test.com",
                "html_url": "http://test.com",
                "login": "sqlRunner",
                "node_id": "123456",
                "organizations_url": "http://test.com",
                "received_events_url": "http://test.com",
                "repos_url": "http://test.com",
                "site_admin": False,
                "starred_url": "http://test.com",
                "subscriptions_url": "http://test.com",
                "type": "Organization",
                "url": "http://test.com",
                "user_view_type": "public",
                "id": 1234,
            },
            "events": [],
            "permissions": None,
        }

        mock_gitapp = GitApp(
            id=UUID("99945678123453331234567812345555"),
            git_id=4567,
            slug="batman",
            name="batman",
            description="I am batman",
            external_url="https://batman.batman",
            html_url="https://github.com/apps/batman",
            node_id="19020",
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

        def override_gitapp_service():
            return mock_service

        def override_cookie_token():
            return {
                "client_id": "12345678123456781234567812345678",
                "user_id": "test-user-id",
            }

        app.dependency_overrides[get_cookie_token] = override_cookie_token
        app.dependency_overrides[get_gitapp_service] = override_gitapp_service

        mock_service = AsyncMock()
        mock_service.get = AsyncMock(return_value=None)
        mock_service.add = AsyncMock(return_value=mock_gitapp)

        mock_http_response = MagicMock()
        mock_http_response.json.return_value = mock_gitapp_json
        mock_http_response.raise_for_status.return_value = None

        with (
            patch("routes.git.app.GitLib") as mock_gitlib,
            patch("routes.git.app.AsyncClient") as mock_async_client,
        ):
            mock_gitlib_instance = mock_gitlib.return_value
            mock_gitlib_instance.create_jwt.return_value = "fake_jwt_token"

            mock_client_instance = AsyncMock()
            mock_client_instance.get = AsyncMock(
                return_value=mock_http_response
            )
            mock_async_client.return_value.__aenter__.return_value = (
                mock_client_instance
            )

            async with AsyncClient(
                transport=ASGITransport(app=app), base_url="http://test"
            ) as test_client:
                response = await test_client.get(f"{api}/")

        app.dependency_overrides.clear()

        assert response.status_code == 200
        response_data = response.json()
        assert response_data["slug"] == "batman"
        assert response_data["gitId"] == 4567
        assert response_data["name"] == "batman"
        assert response_data["description"] == "I am batman"
        assert response_data["externalUrl"] == "https://batman.batman"
        assert response_data["htmlUrl"] == "https://github.com/apps/batman"
