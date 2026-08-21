import pytest
from app.services.adaptive_defense.adaptive_detection_engine import AdaptiveDetectionEngine


def test_adaptive_detection_rule_versioning():
    engine = AdaptiveDetectionEngine()
    rule_v1 = engine.deploy_rule("C2 Beacon Pattern", "pattern_v1_hex", "rule_beacon")
    assert rule_v1.version == 1

    rule_v2 = engine.deploy_rule("C2 Beacon Pattern Updated", "pattern_v2_hex", "rule_beacon")
    assert rule_v2.version == 2
    assert rule_v2.previous_version == 1


def test_adaptive_detection_volume_spike_alert():
    engine = AdaptiveDetectionEngine()
    spike_warning = engine.check_alert_volume("rule_beacon", 150)
    assert spike_warning is not None
    assert "ADAPTATION_WARNING" in spike_warning
