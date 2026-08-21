"""Unit tests for Socket Communication Analysis (Phase 3.8 Part 1A.19)."""

import pytest
from app.schemas.network_models import NetworkSocketDTO


def test_socket_dto():
    sock = NetworkSocketDTO(
        caller_method="com.bank.SocketClient.connect",
        socket_type="TCP",
        host="socket.bank.com",
        port=9000,
        is_server=False,
    )

    assert sock.socket_type == "TCP"
    assert sock.port == 9000
    assert sock.is_server is False
