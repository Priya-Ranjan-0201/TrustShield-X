import pytest
from app.services.resilience.resilience_score_engine import ResilienceScoreEngine

def test_resilience_maturity():
    engine = ResilienceScoreEngine()
    score_untested = engine.evaluate_scorecard(has_empirical_tests=False)
    assert score_untested.maturity_level == "LEVEL_2_IMPLEMENTED"
