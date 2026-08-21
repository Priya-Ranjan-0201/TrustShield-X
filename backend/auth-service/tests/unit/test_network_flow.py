"""Unit tests for Network Dataflow (Phase 3.9 Part 1A.21)."""

import pytest
from app.schemas.dataflow_models import DataflowEdgeDTO


def test_network_edge_dto():
    edge = DataflowEdgeDTO(
        source_node_id="payload_json",
        target_node_id="net_endpoint",
        edge_type="NETWORK_SEND",
        caller_method="com.bank.Network.post",
    )

    assert edge.edge_type == "NETWORK_SEND"
