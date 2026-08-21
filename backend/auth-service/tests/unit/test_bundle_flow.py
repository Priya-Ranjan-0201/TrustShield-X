"""Unit tests for Bundle Dataflow (Phase 3.9 Part 1A.21)."""

import pytest
from app.schemas.dataflow_models import DataflowEdgeDTO


def test_bundle_edge_dto():
    edge = DataflowEdgeDTO(
        source_node_id="val_reg",
        target_node_id="bundle_obj",
        edge_type="BUNDLE_PUT",
        caller_method="com.bank.Fragment.onSaveInstanceState",
    )

    assert edge.edge_type == "BUNDLE_PUT"
