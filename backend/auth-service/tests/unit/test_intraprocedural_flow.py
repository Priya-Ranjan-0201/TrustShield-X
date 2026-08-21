"""Unit tests for Intraprocedural Dataflow Tracking (Phase 3.9 Part 1A.21)."""

import pytest
from app.schemas.dataflow_models import DataflowEdgeDTO


def test_intraprocedural_edge_dto():
    edge = DataflowEdgeDTO(
        source_node_id="reg_v0",
        target_node_id="reg_v1",
        edge_type="MOVE_OBJECT",
        caller_method="com.bank.Process.handle",
        instruction_offset=12,
    )

    assert edge.edge_type == "MOVE_OBJECT"
    assert edge.instruction_offset == 12
