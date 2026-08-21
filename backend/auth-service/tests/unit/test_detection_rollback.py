import pytest
from app.services.adaptive_defense.adaptive_detection_engine import AdaptiveDetectionEngine


def test_adaptive_detection_rollback_lifecycle():
    engine = AdaptiveDetectionEngine()
    engine.deploy_rule("Signature A", "sig_v1", "rule_001")
    engine.deploy_rule("Signature A Updated", "sig_v2", "rule_001")

    # Rollback to v1
    rolled_back = engine.rollback_rule("rule_001")
    assert rolled_back is not None
    assert rolled_back.version == 1
    assert rolled_back.pattern == "sig_v1"
