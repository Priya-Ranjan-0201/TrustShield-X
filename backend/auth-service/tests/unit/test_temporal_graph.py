import pytest
from app.services.global_intelligence.temporal_threat_graph_engine import TemporalThreatGraphEngine

def test_temporal_threat_graph_queries():
    engine = TemporalThreatGraphEngine()
    edges = engine.query_temporal_relationships("node_darkstorm_c2", "2026-08-15T00:00:00Z")
    assert len(edges) >= 1
    assert edges[0]["relation"] == "TARGETS"
