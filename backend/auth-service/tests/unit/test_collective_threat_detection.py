import pytest
from app.services.global_defense.collective_threat_detection_engine import CollectiveThreatDetectionEngine

def test_collective_campaign_surge_detection():
    engine = CollectiveThreatDetectionEngine()
    events = [
        {"campaign_id": "cmp_darkstorm_2026", "tenant_id": "tenant_a"},
        {"campaign_id": "cmp_darkstorm_2026", "tenant_id": "tenant_b"},
        {"campaign_id": "cmp_isolated", "tenant_id": "tenant_a"},
    ]
    detected = engine.detect_collective_campaigns(events)
    assert len(detected) == 1
    assert detected[0]["campaign_id"] == "cmp_darkstorm_2026"
    assert detected[0]["affected_tenant_count"] == 2
