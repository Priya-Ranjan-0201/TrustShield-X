"""Unit tests for Array Element Tracking (Phase 3.9 Part 1A.21)."""

import pytest
from app.schemas.dataflow_models import DataflowNodeDTO, DataflowEdgeDTO


def test_array_tracking_dtos():
    node = DataflowNodeDTO(
        node_id="arr_elem_0",
        node_type="ARRAY_ELEMENT",
        label="Array[0]",
        class_name="com.bank.Buffer",
        method_name="put",
    )
    edge = DataflowEdgeDTO(
        source_node_id="src_val",
        target_node_id="arr_elem_0",
        edge_type="ARRAY_WRITE",
        caller_method="com.bank.Buffer.put",
    )

    assert node.node_type == "ARRAY_ELEMENT"
    assert edge.edge_type == "ARRAY_WRITE"
