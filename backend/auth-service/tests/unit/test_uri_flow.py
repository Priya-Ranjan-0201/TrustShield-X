"""Unit tests for URI Dataflow (Phase 3.9 Part 1A.21)."""

import pytest
from app.schemas.dataflow_models import DataflowEdgeDTO


def test_uri_edge_dto():
    edge = DataflowEdgeDTO(
        source_node_id="str_url",
        target_node_id="uri_obj",
        edge_type="URI_PARSE",
        caller_method="com.bank.DeepLink.handle",
    )

    assert edge.edge_type == "URI_PARSE"
