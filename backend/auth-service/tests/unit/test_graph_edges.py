import pytest
from app.services.threat_intelligence_fusion.intelligence_graph_fusion_engine import IntelligenceGraphFusionEngine

def test_graph_edges_with_provenance():
    engine = IntelligenceGraphFusionEngine()
    edge = engine.add_edge("cmp_darkstorm_apac", "TARGETS", "ast_payment_gw_01", "ev_pcap_evidence")
    assert edge["source"] == "cmp_darkstorm_apac"
    assert edge["relationship"] == "TARGETS"
    assert edge["provenance"] == "ev_pcap_evidence"
