import pytest
from app.services.global_intelligence.threat_early_warning_engine import ThreatEarlyWarningEngine

def test_early_warning_state_transitions():
    engine = ThreatEarlyWarningEngine()
    w = engine.trigger_warning("Emerging Malicious Domain Burst", "CRITICAL", velocity_score=0.95, affected_assets=["ast_auth_cluster"])
    assert w.severity == "CRITICAL"
    assert w.velocity_score == 0.95
