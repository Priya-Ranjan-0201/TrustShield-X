import pytest
from app.schemas.collective_defense_models import ThreatIntelligenceObjectDTO


def test_threat_intelligence_object_creation():
    obj = ThreatIntelligenceObjectDTO(
        intelligence_type="DOMAIN",
        raw_indicator="malicious-c2-node.com",
        tenant_id="tenant_alpha",
        confidence=0.88,
        reliability=0.92,
        severity="HIGH",
    )
    assert obj.intelligence_id.startswith("tio_")
    assert obj.intelligence_type == "DOMAIN"
    assert obj.validation_state == "OBSERVED"
    assert obj.sharing_state == "PRIVATE"
    assert obj.confidence == 0.88


def test_threat_intelligence_types_supported():
    types = [
        "DOMAIN", "URL", "IP", "CERTIFICATE", "FILE_HASH",
        "APK_SIGNATURE", "EMAIL_INDICATOR", "PHONE_IDENTIFIER",
        "PAYMENT_IDENTIFIER", "QR_INDICATOR", "VOICE_SIGNATURE",
        "IDENTITY_PATTERN", "CAMPAIGN", "ATTACK_PATTERN",
        "INFRASTRUCTURE_CLUSTER", "BEHAVIORAL_PATTERN"
    ]
    for t in types:
        dto = ThreatIntelligenceObjectDTO(intelligence_type=t, raw_indicator="test_val")  # type: ignore
        assert dto.intelligence_type == t
