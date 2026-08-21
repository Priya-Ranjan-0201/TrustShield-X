"""Unit tests for Large Call Graph Dataflow Handling (Phase 3.9 Part 1A.21)."""

import pytest
from app.schemas.dataflow_models import DataflowMetricsDTO


def test_large_call_graph_dto():
    metrics = DataflowMetricsDTO(
        methods_analyzed=5000,
        instructions_analyzed=60000,
        sources_count=10,
        sinks_count=15,
        paths_count=25,
    )

    assert metrics.methods_analyzed == 5000
