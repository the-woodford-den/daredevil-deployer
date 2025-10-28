"""Test fixtures for route tests."""

from typing import List
from unittest.mock import AsyncMock

import pytest


@pytest.fixture
def mock_websocket_factory():
    """A factory fixture which builds multiple mock websockets"""

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
    """Build New ConnectionManager Instance"""
    from routes.git import ConnectionManager

    return ConnectionManager()
