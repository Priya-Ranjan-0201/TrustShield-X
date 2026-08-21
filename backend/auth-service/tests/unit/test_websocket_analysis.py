"""Unit tests for WebSocket Communication Detection (Phase 3.8 Part 1A.19)."""

import pytest
from app.schemas.network_models import NetworkWebSocketDTO


def test_websocket_dto():
    ws = NetworkWebSocketDTO(
        caller_method="com.bank.WS.start",
        endpoint="wss://ws.bank.com/live",
        subprotocol="json",
        library="OkHttp WebSocket",
    )

    assert ws.endpoint == "wss://ws.bank.com/live"
    assert ws.library == "OkHttp WebSocket"
