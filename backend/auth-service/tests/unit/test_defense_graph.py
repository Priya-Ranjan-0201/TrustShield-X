import pytest
from app.services.adaptive_defense.adaptive_defense_fabric import AdaptiveDefenseFabric


def test_adaptive_defense_graph_topology():
    fabric = AdaptiveDefenseFabric()
    graph = fabric.get_defense_graph()

    assert len(graph.nodes) >= 3
    assert len(graph.edges) >= 2
    assert any(e["relation"] == "MITIGATED_BY" for e in graph.edges)
