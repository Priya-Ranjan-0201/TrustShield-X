import pytest
from app.services.global_defense.threat_to_defense_graph_engine import ThreatToDefenseGraphEngine

def test_threat_propagation_graph_mapping():
    engine = ThreatToDefenseGraphEngine()
    trace = engine.build_threat_defense_trace("cmp_darkstorm_2026")
    assert trace["technique"] == "T1078 (Valid Accounts)"
    assert "ast_api_gw" in trace["targeted_assets"]
    assert trace["trace_status"] == "VERIFIED_COMPLETE"
