import pytest
from app.services.threat_intelligence_fusion.intelligence_graph_fusion_engine import IntelligenceGraphFusionEngine

def test_graph_query_subgraph():
    engine = IntelligenceGraphFusionEngine()
    subgraph = engine.query_graph("act_apt_ember_bear")
    assert len(subgraph["nodes"]) >= 2
    assert len(subgraph["edges"]) >= 1
