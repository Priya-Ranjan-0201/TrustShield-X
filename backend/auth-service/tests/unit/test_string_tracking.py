"""Unit tests for String Dataflow & Concatenation (Phase 3.9 Part 1A.21)."""

import pytest
from app.schemas.dataflow_models import DataflowEdgeDTO


def test_string_edge_dto():
    edge = DataflowEdgeDTO(
        source_node_id="str_const",
        target_node_id="sb_append",
        edge_type="CONCATENATE",
        caller_method="com.bank.UrlBuilder.build",
    )

    assert edge.edge_type == "CONCATENATE"
