"""Unit tests for Correlation Graph Construction (Phase 3.9 Part 1A.22)."""

import pytest
from app.schemas.behavioral_correlation_models import CorrelationGraphDTO


def test_correlation_graph_dto():
    cg = CorrelationGraphDTO(
        source_node="com.bank.Location",
        target_node="https://api.bank.com",
        relationship="FLOWS_TO",
    )

    assert cg.source_node == "com.bank.Location"
    assert cg.relationship == "FLOWS_TO"
