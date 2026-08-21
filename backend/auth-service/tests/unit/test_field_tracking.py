"""Unit tests for Object Field Tracking (Phase 3.9 Part 1A.21)."""

import pytest
from app.schemas.dataflow_models import DataflowNodeDTO, DataflowEdgeDTO


def test_field_tracking_dtos():
    node = DataflowNodeDTO(
        node_id="field_user_token",
        node_type="FIELD",
        label="Field: com.bank.User.token",
        class_name="com.bank.User",
        method_name="setToken",
    )
    edge = DataflowEdgeDTO(
        source_node_id="reg_val",
        target_node_id="field_user_token",
        edge_type="FIELD_WRITE",
        caller_method="com.bank.User.setToken",
    )

    assert node.node_type == "FIELD"
    assert edge.edge_type == "FIELD_WRITE"
