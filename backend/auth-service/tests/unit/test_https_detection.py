"""Unit tests for HTTPS Communication Detection (Phase 3.8 Part 1A.19)."""

import pytest
from app.schemas.network_models import NetworkEndpointDTO


def test_https_endpoint():
    ep = NetworkEndpointDTO(
        url="https://secure.bank.com/api",
        scheme="https",
        host="secure.bank.com",
        port=443,
        source_class="com.bank.SecureNet",
        source_method="com.bank.SecureNet.fetch",
        is_cleartext=False,
    )

    assert ep.scheme == "https"
    assert ep.is_cleartext is False
