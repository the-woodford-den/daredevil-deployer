"""tests for routes/github/app.py"""

import asyncio

import pytest
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)
api = "/github/app"
headers = {
    "Accept": "application/abc.xyz+json",
    "X-GitHub-Api-Version": "1999-12-31",
    "User-Agent": "superman",
}


class TestGithubAppRoutes:
    """test suite --> /github/app"""

    @pytest.mark.asyncio
    async def test_search_apps():
        test_slug = "test-app"
        response = client.get(f"/{api}/search/test-app", headers=headers)
        assert response.status_code == 200
        assert response.json() == {
            "id": "foo",
            "title": "Foo",
            "description": "There goes my hero",
        }
