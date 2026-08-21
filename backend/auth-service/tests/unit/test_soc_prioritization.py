import pytest
from app.services.global_intelligence.threat_early_warning_engine import ThreatEarlyWarningEngine

def test_soc_early_warning_prioritization():
    engine = ThreatEarlyWarningEngine()
    warnings = engine.list_warnings()
    assert len(warnings) >= 1
    assert warnings[0].severity == "HIGH"
    assert "Pre-position rate-limiting" in warnings[0].recommended_action
