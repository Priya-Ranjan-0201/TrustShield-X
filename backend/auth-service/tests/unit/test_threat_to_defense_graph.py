import pytest
from app.services.global_defense.threat_to_defense_graph_engine import ThreatToDefenseGraphEngine

def test_threat_to_defense_graph_full_trace():
    engine = ThreatToDefenseGraphEngine()
    trace = engine.build_threat_defense_trace("cmp_darkstorm_2026")
    assert trace["threat_actor"] == "DarkStorm Threat Cluster"
    assert trace["security_control"] == "WAF Rate-Limiter + Adaptive MFA"
