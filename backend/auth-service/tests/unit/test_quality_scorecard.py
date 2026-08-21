import pytest
from app.services.threat_intelligence_fusion.intelligence_quality_scorecard_engine import IntelligenceQualityScorecardEngine

def test_quality_scorecard_dimensions():
    engine = IntelligenceQualityScorecardEngine()
    card = engine.evaluate_quality(
        source_reliability="A",
        information_credibility="1",
        age_in_days=2,
        independent_sources_count=3,
        has_techniques=True,
        has_affected_assets=True,
        has_sha256_provenance=True
    )
    assert card.source_reliability == "A"
    assert card.information_credibility == "1"
    assert card.freshness_score >= 0.90
    assert card.corroboration_count == 3
    assert card.provenance_verified is True
    assert card.overall_quality_assessment == "HIGH_QUALITY_GROUNDED"
