"""Unit tests for Taint Propagation Engine (Phase 3.9 Part 1A.21)."""

import pytest
from app.schemas.dataflow_models import DataflowTaintLabelDTO


def test_taint_label_dto():
    t = DataflowTaintLabelDTO(
        node_id="loc_node",
        taint_label="TAINT_LOCATION",
        original_taint="LOCATION",
        is_sanitized=False,
    )

    assert t.taint_label == "TAINT_LOCATION"
    assert t.is_sanitized is False
