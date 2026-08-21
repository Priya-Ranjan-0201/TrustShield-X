import pytest
from app.services.assurance_fabric.security_drift_engine import SecurityDriftEngine

def test_detection_drift():
    engine = SecurityDriftEngine()
    d = engine.detect_drift("DETECTION", "rule_sqli_waf", "WAF rule disabled by operator")
    assert d.drift_type == "DETECTION"
