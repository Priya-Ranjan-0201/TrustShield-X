"""Unit tests for URL Extraction (Phase 3.8 Part 1A.19)."""

import pytest
from app.schemas.network_models import NetworkEndpointDTO


def test_url_extraction_dto():
    ep = NetworkEndpointDTO(
        url="https://api.bank.com/v1/login",
        scheme="https",
        host="api.bank.com",
        port=443,
        path="/v1/login",
        source_class="com.bank.Auth",
        source_method="com.bank.Auth.login",
        is_cleartext=False,
        library="OkHttp",
    )

    assert ep.url == "https://api.bank.com/v1/login"
    assert ep.host == "api.bank.com"
    assert ep.port == 443
    assert ep.is_cleartext is False
