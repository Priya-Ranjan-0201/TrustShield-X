import pytest
from app.services.fusion.event_normalization_service import EventNormalizationService


def test_event_normalization_fields():
    service = EventNormalizationService()
    event = service.ingest_and_normalize(
        event_type="THREAT_SIGNAL",
        source="WEB_DETECTOR",
        entity_id="domain:phish-portal.net",
        severity="critical",
        confidence=1.2,  # Should clamp to 1.0
        risk_score=150.0,  # Should clamp to 100.0
        trust_score=-10.0,  # Should clamp to 0.0
        exposure_score=85.0,
        tenant_id="tenant_norm",
    )
    assert event.severity == "CRITICAL"
    assert event.confidence == 1.0
    assert event.risk_score == 100.0
    assert event.trust_score == 0.0
    assert event.exposure_score == 85.0
