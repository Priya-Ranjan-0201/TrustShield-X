import pytest
from app.services.knowledge.digital_trust_score_engine import DigitalTrustScoreEngine


def test_multi_dimensional_trust_score_calculation():
    engine = DigitalTrustScoreEngine()
    score = engine.calculate_trust_score(
        entity_id="domain:bank-legitimate.com",
        identity_score=95.0,
        content_score=90.0,
        source_score=95.0,
        infrastructure_score=85.0,
        behavior_score=90.0,
        evidence_score=95.0,
    )
    assert score.trust_score >= 90.0
    assert "IDENTITY_TRUST" in score.dimension_scores
    assert score.dimension_scores["IDENTITY_TRUST"] == 95.0
    assert score.decay_applied is False


def test_trust_score_temporal_decay():
    engine = DigitalTrustScoreEngine()
    # Inactive for 120 days -> applies decay
    score = engine.calculate_trust_score(
        entity_id="domain:stale-entity.com",
        identity_score=90.0,
        content_score=90.0,
        source_score=90.0,
        infrastructure_score=90.0,
        behavior_score=90.0,
        evidence_score=90.0,
        apply_decay=True,
        days_since_last_seen=120,
    )
    assert score.decay_applied is True
    assert score.trust_score < 90.0
    assert len(score.limitations) >= 1
