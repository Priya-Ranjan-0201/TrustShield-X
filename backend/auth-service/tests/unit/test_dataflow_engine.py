"""Unit tests for Core Dataflow Engine (Phase 3.9 Part 1A.21)."""

import pytest
from app.schemas.dataflow_models import DataflowNodeDTO, DataflowEdgeDTO


def test_dataflow_node_dto():
    node = DataflowNodeDTO(
        node_id="src_1",
        node_type="SOURCE",
        label="Location Source",
        class_name="com.bank.LocationClient",
        method_name="getLocation",
        confidence="HIGH",
        resolution_status="RESOLVED",
    )

    assert node.node_type == "SOURCE"
    assert node.resolution_status == "RESOLVED"
