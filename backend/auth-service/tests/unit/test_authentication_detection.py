"""Unit tests for Authentication Mechanisms & Secret Redaction (Phase 3.8 Part 1A.19)."""

import pytest
from app.schemas.network_models import NetworkAuthenticationDTO


def test_authentication_redaction():
    auth = NetworkAuthenticationDTO(
        caller_method="com.bank.Auth.setToken",
        auth_type="BEARER",
        header_name="Authorization",
        redacted_token="[REDACTED_BEARER_TOKEN]",
    )

    assert auth.auth_type == "BEARER"
    assert auth.redacted_token == "[REDACTED_BEARER_TOKEN]"
    assert "secret" not in auth.redacted_token.lower()
