"""Unit tests for Obfuscated Dataflow Reconstruction (Phase 3.9 Part 1A.21)."""

import pytest
from app.schemas.dataflow_models import DataflowNodeDTO


def test_obfuscated_dataflow_dto():
    node = DataflowNodeDTO(
        node_id="obf_node",
        node_type="VARIABLE",
        label="a.b.c.d",
        class_name="a.b.c",
        method_name="d",
        confidence="MEDIUM",
        resolution_status="PARTIALLY_RESOLVED",
    )

    assert node.resolution_status == "PARTIALLY_RESOLVED"
