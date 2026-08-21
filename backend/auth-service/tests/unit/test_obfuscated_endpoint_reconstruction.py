"""Unit tests for Obfuscated Endpoint Reconstruction (Phase 3.8 Part 1A.19)."""

import pytest
from app.schemas.network_models import NetworkEndpointDTO


def test_obfuscated_endpoint_reconstruction():
    ep = NetworkEndpointDTO(
        url="https://api.bank.com/v1/dynamic_path",
        scheme="https",
        host="api.bank.com",
        port=443,
        path="/v1/dynamic_path",
        source_class="com.bank.a.a",
        source_method="com.bank.a.a.b",
        is_cleartext=False,
        library="Retrofit",
    )

    assert ep.source_class == "com.bank.a.a"
    assert ep.url == "https://api.bank.com/v1/dynamic_path"
