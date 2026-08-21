"""Unit tests for Reachability Analysis & Metrics (Phase 3.7 Part 1A.15)."""

import pytest
from app.schemas.program_graph_models import ProgramGraphMetricsDTO


def test_program_graph_metrics_dto():
    metrics = ProgramGraphMetricsDTO(
        cfg_count=120,
        call_graph_nodes_count=250,
        call_graph_edges_count=800,
        cyclomatic_complexity=2.4,
        reachable_methods_count=240,
        reachability_percentage=96.0,
    )

    assert metrics.cfg_count == 120
    assert metrics.call_graph_nodes_count == 250
    assert metrics.call_graph_edges_count == 800
    assert metrics.cyclomatic_complexity == 2.4
    assert metrics.reachability_percentage == 96.0
