import pytest
from app.services.global_intelligence.emerging_threat_detection_engine import EmergingThreatDetectionEngine

def test_multidimensional_signal_scoring():
    engine = EmergingThreatDetectionEngine()
    signals = engine.list_signals()
    assert len(signals) >= 1
    assert signals[0].velocity_score >= 0.80
    assert signals[0].novelty_score >= 0.70
