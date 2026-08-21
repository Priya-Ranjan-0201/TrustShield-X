"""Unit tests for Crypto Knowledge Graph (Phase 3.7 Part 1A.18)."""

import pytest
from app.schemas.cryptography_models import CryptoGraphEdgeDTO, CryptoMetricsDTO


def test_crypto_graph_edge_dto():
    edge = CryptoGraphEdgeDTO(source_node="com.bank.Crypto.encrypt", target_node="AES-256-GCM", relationship="USES_ALGORITHM")
    metrics = CryptoMetricsDTO(algorithms_count=3, operations_count=10, keys_count=2, tls_sessions_count=1)

    assert edge.source_node == "com.bank.Crypto.encrypt"
    assert edge.target_node == "AES-256-GCM"
    assert metrics.algorithms_count == 3
