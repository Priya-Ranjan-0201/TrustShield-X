import pytest
from app.services.zero_trust_exposure.security_graph_engine import SecurityGraphEngine

def test_graph_temporal_reconstruction():
    engine = SecurityGraphEngine()
    engine.add_node("t1", "N-1", "IDENTITY", valid_from="2026-01-01T00:00:00Z", valid_until="2026-06-01T00:00:00Z")
    engine.add_node("t1", "N-2", "RESOURCE", valid_from="2026-01-01T00:00:00Z")
    
    # Query at 2026-03-01 (N-1 is valid)
    g1 = engine.query_graph_at_time("t1", "2026-03-01T00:00:00Z")
    assert g1["nodes_count"] == 2
    
    # Query at 2026-08-01 (N-1 is expired)
    g2 = engine.query_graph_at_time("t1", "2026-08-01T00:00:00Z")
    assert g2["nodes_count"] == 1
