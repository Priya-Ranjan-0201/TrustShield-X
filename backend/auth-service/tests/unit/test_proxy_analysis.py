"""Unit tests for Proxy Configuration Detection (Phase 3.8 Part 1A.19)."""

import pytest
from app.schemas.network_models import NetworkProxyDTO


def test_proxy_dto():
    proxy = NetworkProxyDTO(
        caller_method="com.bank.Proxy.setProxy",
        proxy_type="HTTP",
        host="127.0.0.1",
        port=8080,
    )

    assert proxy.proxy_type == "HTTP"
    assert proxy.port == 8080
