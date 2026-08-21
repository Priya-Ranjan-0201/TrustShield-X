"""Unit tests for Interprocedural Dataflow Tracking (Phase 3.9 Part 1A.21)."""

import pytest
from app.schemas.dataflow_models import DataflowEdgeDTO


def test_interprocedural_edge_dto():
    edge = DataflowEdgeDTO(
        source_node_id="caller_arg0",
        target_node_id="callee_param0",
        edge_type="ARGUMENT",
        caller_method="com.bank.Caller.invoke",
        confidence="HIGH",
    )

    assert edge.edge_type == "ARGUMENT"
