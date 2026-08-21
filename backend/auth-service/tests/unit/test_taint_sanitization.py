"""Unit tests for Taint Sanitization Boundaries (Phase 3.9 Part 1A.21)."""

import pytest
from app.schemas.dataflow_models import DataflowTaintLabelDTO


def test_taint_sanitization_dto():
    t = DataflowTaintLabelDTO(
        node_id="hashed_node",
        taint_label="TAINT_TOKEN",
        original_taint="TOKEN",
        is_sanitized=True,
    )

    assert t.is_sanitized is True
