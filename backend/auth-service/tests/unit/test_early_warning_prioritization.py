import pytest
from app.services.threat_intelligence_fusion.threat_early_warning_engine import ThreatEarlyWarningEngine

def test_early_warning_filtering():
    engine = ThreatEarlyWarningEngine()
    crit_warnings = engine.list_warnings(urgency="CRITICAL")
    assert len(crit_warnings) >= 1
