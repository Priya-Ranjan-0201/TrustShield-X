"""Unit tests for TLS & Certificate Pinning Analysis (Phase 3.7 Part 1A.18)."""

import pytest
from app.schemas.cryptography_models import TLSSessionDTO


def test_tls_session_dto():
    tls = TLSSessionDTO(caller_method="com.bank.Net.initTLS", tls_version="TLSv1.3", hostname_verifier="STRICT", pinning_enabled=True)

    assert tls.caller_method == "com.bank.Net.initTLS"
    assert tls.tls_version == "TLSv1.3"
    assert tls.pinning_enabled is True
