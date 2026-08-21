import pytest
from app.services.resilience.resilience_score_engine import ResilienceScoreEngine
from app.services.resilience_twin.cyber_resilience_scorer import CyberResilienceScorer

def test_phase23_resilience_score():
    engine = ResilienceScoreEngine()
    score = engine.evaluate_scorecard(has_empirical_tests=True, backup_verified=True, failover_ready=True)
    assert score.overall_score >= 90.0
    assert score.maturity_level == "LEVEL_5_CONTINUOUSLY_VALIDATED"

def test_seven_dimensional_resilience_score():
    scorer = CyberResilienceScorer()
    score = scorer.calculate_resilience(
        tenant_id="tenant_bank",
        prevention=90.0,
        detection=95.0,
        containment=88.0,
        recovery=82.0,
        adaptability=91.0,
        dependency_resilience=85.0,
        governance_readiness=96.0,
    )
    assert score.prevention == 90.0
    assert score.recovery == 82.0
    assert score.overall_resilience_score > 85.0
