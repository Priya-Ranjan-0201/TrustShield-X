"""Unit tests for Network Communication Graph Construction (Phase 3.8 Part 1A.19)."""

import pytest
from app.schemas.network_models import NetworkGraphEdgeDTO, NetworkMetricsDTO


def test_network_graph_dtos():
    edge = NetworkGraphEdgeDTO(
        source_node="com.bank.NetClient",
        target_node="api.bank.com",
        relationship="CONNECTS_TO",
    )
    metrics = NetworkMetricsDTO(
        endpoints_count=10,
        domains_count=3,
        ips_count=2,
        libraries_count=2,
        cleartext_count=0,
    )

    assert edge.source_node == "com.bank.NetClient"
    assert edge.target_node == "api.bank.com"
    assert metrics.endpoints_count == 10
