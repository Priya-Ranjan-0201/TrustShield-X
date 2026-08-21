import pytest
from app.services.global_intelligence.emerging_threat_detection_engine import EmergingThreatDetectionEngine

def test_emerging_weak_signal_detection():
    engine = EmergingThreatDetectionEngine()
    signal = engine.detect_emerging_signal("DarkStorm ASN Surge", velocity_score=0.88, novelty_score=0.92, affected_assets=["ast_api_gw"])
    assert signal.velocity_score == 0.88
    assert signal.severity == "HIGH"
