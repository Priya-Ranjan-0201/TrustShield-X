import pytest
from app.schemas.collective_defense_models import IntelligenceSourceReliabilityDTO, ThreatIntelligenceObjectDTO


def test_source_reliability_separated_from_confidence():
    rel = IntelligenceSourceReliabilityDTO(
        source_id="src_commercial_feed_01",
        historical_accuracy=0.92,
        false_positive_rate=0.03,
        freshness_score=0.88,
        provenance_quality=0.95,
        reliability_score=0.91,
    )

    # An indicator may have lower confidence even if source has high reliability
    obj = ThreatIntelligenceObjectDTO(
        intelligence_type="DOMAIN",
        raw_indicator="suspicious-domain-x.xyz",
        confidence=0.45,  # Low indicator confidence
        reliability=rel.reliability_score,  # High source reliability
    )

    assert obj.confidence != obj.reliability
    assert obj.reliability == 0.91
    assert obj.confidence == 0.45
