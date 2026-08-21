import pytest
from app.services.threat_intelligence_fusion.intelligence_graph_fusion_engine import IntelligenceGraphFusionEngine

def test_graph_nodes_creation():
    engine = IntelligenceGraphFusionEngine()
    node = engine.add_node("node_test_01", "TECHNIQUE", {"name": "Test Technique"})
    assert node["node_id"] == "node_test_01"
    assert node["node_type"] == "TECHNIQUE"
