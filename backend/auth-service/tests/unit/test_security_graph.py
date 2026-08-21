import pytest
from app.services.zero_trust_exposure.security_graph_engine import SecurityGraphEngine

def test_security_graph_nodes_and_edges():
    engine = SecurityGraphEngine()
    n1 = engine.add_node("t1", "ID-1", "IDENTITY", {"name": "Alice"})
    n2 = engine.add_node("t1", "DEV-1", "DEVICE", {"hostname": "mac-01"})
    n3 = engine.add_node("t1", "RES-1", "RESOURCE", {"name": "Vault"})
    
    e1 = engine.add_edge("t1", "E-1", "ID-1", "DEV-1", "AUTHENTICATES")
    e2 = engine.add_edge("t1", "E-2", "ID-1", "RES-1", "ACCESSES")
    
    nodes = engine.get_nodes("t1")
    edges = engine.get_edges("t1")
    assert len(nodes) == 3
    assert len(edges) == 2
