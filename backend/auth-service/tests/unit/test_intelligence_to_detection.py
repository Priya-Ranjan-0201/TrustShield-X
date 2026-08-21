import pytest
from app.services.threat_intelligence.intelligence_operationalization_engine import IntelligenceOperationalizationEngine


def test_intelligence_to_detection_ip_rule():
    engine = IntelligenceOperationalizationEngine()
    rule = engine.generate_detection_rule("198.51.100.42", "IP", "ShadowStrike C2")

    assert "destination.ip" in rule["syntax"]
    assert rule["validation_status"] == "SYNTAX_VERIFIED"
