import pytest
from app.services.global_defense.collective_threat_detection_engine import CollectiveThreatDetectionEngine

def test_global_campaign_view_affected_tenants():
    engine = CollectiveThreatDetectionEngine()
    events = [
        {"campaign_id": "cmp_storm_44", "tenant_id": "t1"},
        {"campaign_id": "cmp_storm_44", "tenant_id": "t2"},
        {"campaign_id": "cmp_storm_44", "tenant_id": "t3"},
    ]
    detected = engine.detect_collective_campaigns(events)
    assert detected[0]["affected_tenant_count"] == 3
