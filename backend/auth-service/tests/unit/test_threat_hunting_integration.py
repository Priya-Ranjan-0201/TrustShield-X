import pytest
from app.services.global_intelligence.threat_early_warning_engine import ThreatEarlyWarningEngine

def test_threat_hunting_hypothesis_trigger():
    engine = ThreatEarlyWarningEngine()
    warn = engine.trigger_warning("Storm Surge", "ELEVATED", velocity_score=0.75, affected_assets=["ast_api_gw"])
    assert "Initiate SOC threat hunt" in warn.recommended_action
