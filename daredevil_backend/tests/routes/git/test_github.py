"""tests for routes/git/github.py"""

import pytest


class TestConnectionManager:
    """test suite --> websockets & ConnectionManager"""

    @pytest.mark.asyncio
    async def test_connect_accepts_and_adds_websocket(
        self, connection_manager, mock_websocket_factory
    ):
        websocket = mock_websocket_factory()
        await connection_manager.connect(websocket)
        websocket.accept.assert_awaited_once()

        assert websocket in connection_manager.active_connections
        assert len(connection_manager.active_connections) == 1

    @pytest.mark.asyncio
    async def test_send_update_only_to_target_websocket(
        self, connection_manager, mock_websocket_factory
    ):
        ws1 = mock_websocket_factory()
        ws2 = mock_websocket_factory()
        connection_manager.active_connections.extend([ws1, ws2])
        test_message = "Message for ws1 only"
        await connection_manager.send_update(test_message, ws1)

        ws1.send_text.assert_awaited_once_with(test_message)
        ws2.send_text.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_connection_manager_full_lifecycle(
        self, connection_manager, mock_websocket_factory
    ):
        """Integration test: connect, send updates, broadcast, then disconnect."""
        ws1 = mock_websocket_factory()
        ws2 = mock_websocket_factory()

        await connection_manager.connect(ws1)
        await connection_manager.connect(ws2)
        assert len(connection_manager.active_connections) == 2

        await connection_manager.send_update("Update for ws1", ws1)
        assert "Update for ws1" in ws1.sent_messages
        assert "Update for ws1" not in ws2.sent_messages

        await connection_manager.broadcast("Broadcast message")
        assert "Broadcast message" in ws1.sent_messages
        assert "Broadcast message" in ws2.sent_messages

        connection_manager.disconnect(ws1)
        assert len(connection_manager.active_connections) == 1
        assert ws2 in connection_manager.active_connections

        ws1.send_text.reset_mock()
        ws2.send_text.reset_mock()
        await connection_manager.broadcast("Final broadcast")
        ws1.send_text.assert_not_awaited()
        ws2.send_text.assert_awaited_once_with("Final broadcast")
