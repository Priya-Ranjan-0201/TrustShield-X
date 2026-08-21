"""Unit tests for Argument Tracking (Phase 3.9 Part 1A.21)."""

import pytest
from app.schemas.dataflow_models import DataflowNodeDTO


def test_argument_node_dto():
    node = DataflowNodeDTO(
        node_id="param_0",
        node_type="PARAMETER",
        label="Method Parameter 0",
        class_name="com.bank.Handler",
        method_name="processInput",
    )

    assert node.node_type == "PARAMETER"
