"""Shared test fixtures for route tests."""

from typing import List
from unittest.mock import AsyncMock

import pytest


@pytest.fixture
def mock_websocket_factory():
    """Factory fixture to create multiple mock WebSocket instances."""

    def _create_mock_websocket():
        websocket = AsyncMock()
        websocket.accept = AsyncMock()
        websocket.send_text = AsyncMock()
        websocket.send_json = AsyncMock()
        websocket.close = AsyncMock()
        websocket.sent_messages: List[str] = []

        async def track_send_text(message: str):
            websocket.sent_messages.append(message)

        websocket.send_text.side_effect = track_send_text

        return websocket

    return _create_mock_websocket


@pytest.fixture
def connection_manager():
    """Create a fresh ConnectionManager instance for each test."""
    from routes.github.authenticate import ConnectionManager

    return ConnectionManager()
