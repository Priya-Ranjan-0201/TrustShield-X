"""Unit tests for TLS Correlation with Cryptography Intelligence (Phase 3.8 Part 1A.19)."""

import pytest
from app.schemas.network_models import NetworkGraphEdgeDTO


def test_tls_correlation_edge():
    edge = NetworkGraphEdgeDTO(
        source_node="https://api.bank.com",
        target_node="TLSv1.3(OkHttpPinning)",
        relationship="PROTECTED_BY_TLS",
    )

    assert edge.source_node == "https://api.bank.com"
    assert edge.relationship == "PROTECTED_BY_TLS"
