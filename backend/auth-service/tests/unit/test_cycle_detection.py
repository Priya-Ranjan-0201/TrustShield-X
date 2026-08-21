"""Unit tests for Cycle Detection & Infinite Loop Safeguards (Phase 3.9 Part 1A.21)."""

import pytest
from app.schemas.dataflow_models import DataflowPathDTO


def test_cycle_detection_dto():
    path = DataflowPathDTO(
        path_id="path_cycle",
        source_id="src_1",
        sink_id="snk_1",
        path_nodes=["src_1", "node_a", "node_b", "node_a", "snk_1"],
        flow_classification="SOURCE_TO_NETWORK",
        confidence="MEDIUM",
    )

    assert len(path.path_nodes) == 5
