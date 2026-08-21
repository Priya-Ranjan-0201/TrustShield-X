"""Unit tests for Information-Flow Graph Construction (Phase 3.9 Part 1A.21)."""

import pytest
from app.schemas.dataflow_models import InformationFlowGraphDTO


def test_info_graph_dto():
    graph = InformationFlowGraphDTO(
        nodes_count=10,
        edges_count=15,
        sources_count=2,
        sinks_count=2,
    )

    assert graph.nodes_count == 10
    assert graph.edges_count == 15
