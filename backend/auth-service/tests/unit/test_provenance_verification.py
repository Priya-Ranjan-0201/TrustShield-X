import pytest
from app.services.threat_intelligence_fusion.intelligence_quality_scorecard_engine import IntelligenceQualityScorecardEngine

def test_incomplete_provenance_detection():
    engine = IntelligenceQualityScorecardEngine()
    card = engine.evaluate_quality(has_sha256_provenance=False)
    assert card.overall_quality_assessment == "PROVENANCE_INCOMPLETE"
