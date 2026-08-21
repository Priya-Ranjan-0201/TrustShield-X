"""Unit tests for Behavioral Graph Construction (Phase 3.9 Part 1A.22)."""

import pytest
from app.schemas.behavioral_correlation_models import BehaviorGraphDTO


def test_behavior_graph_dto():
    graph = BehaviorGraphDTO(
        nodes_count=20,
        edges_count=35,
    )

    assert graph.nodes_count == 20
    assert graph.edges_count == 35
