import pytest
from app.schemas.fusion_models import SecurityEventDTO


def test_security_event_creation():
    event = SecurityEventDTO(
        event_id="sev_101",
        event_type="DETECTION",
        source="DEX_PARSER_AI",
        entity_id="apk:sha256_sample",
        severity="HIGH",
        confidence=0.95,
        risk_score=80.0,
        trust_score=25.0,
        exposure_score=60.0,
    )
    assert event.event_id == "sev_101"
    assert event.event_type == "DETECTION"
    assert event.confidence == 0.95
    assert event.status == "PROCESSED"
