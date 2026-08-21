import pytest
from app.schemas.threat_intelligence_fabric_models import ThreatIntelligenceObjectDTO


def test_intelligence_confidence_bounds():
    obj = ThreatIntelligenceObjectDTO(
        object_type="DOMAIN",
        value="api.c2.io",
        canonical_value="api.c2.io",
        source_id="src_commercial",
        confidence=0.98,
    )
    assert 0.0 <= obj.confidence <= 1.0
    assert obj.confidence == 0.98
