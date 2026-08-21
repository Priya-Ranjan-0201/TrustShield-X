"""Unit tests for Return Value Tracking (Phase 3.9 Part 1A.21)."""

import pytest
from app.schemas.dataflow_models import DataflowNodeDTO


def test_return_node_dto():
    node = DataflowNodeDTO(
        node_id="ret_val",
        node_type="RETURN_VALUE",
        label="Return Value",
        class_name="com.bank.Fetcher",
        method_name="fetchSecret",
    )

    assert node.node_type == "RETURN_VALUE"
