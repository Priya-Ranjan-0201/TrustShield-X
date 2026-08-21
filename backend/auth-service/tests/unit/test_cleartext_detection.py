"""Unit tests for Cleartext Traffic Detection (Phase 3.8 Part 1A.19)."""

import pytest
from app.schemas.network_models import NetworkEndpointDTO


def test_cleartext_traffic():
    ep = NetworkEndpointDTO(
        url="http://insecure.bank.com/api",
        scheme="http",
        host="insecure.bank.com",
        port=80,
        source_class="com.bank.LegacyNet",
        source_method="com.bank.LegacyNet.connect",
        is_cleartext=True,
    )

    assert ep.scheme == "http"
    assert ep.is_cleartext is True
