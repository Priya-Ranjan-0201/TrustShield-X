import pytest
from app.services.threat_intelligence.threat_intelligence_graph_engine import ThreatIntelligenceGraphEngine


def test_threat_graph_bounded_traversal_and_shortest_path():
    engine = ThreatIntelligenceGraphEngine()

    # Bounded subgraph retrieval
    sub = engine.get_subgraph("node_camp_shadow", max_depth=3)
    assert len(sub.nodes) >= 3
    assert len(sub.edges) >= 2

    # Shortest path between campaign and infrastructure IP
    path = engine.shortest_path("node_camp_shadow", "node_asset_checkout")
    assert len(path) == 2
    assert path[0] == "node_camp_shadow"
    assert path[1] == "node_asset_checkout"
