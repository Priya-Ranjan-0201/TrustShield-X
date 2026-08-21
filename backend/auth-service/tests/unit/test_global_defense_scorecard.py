import pytest
from app.services.global_defense.global_defense_scorecard_engine import GlobalDefenseScorecardEngine

def test_global_defense_scorecard_dimensions():
    engine = GlobalDefenseScorecardEngine()
    sc = engine.evaluate_scorecard()
    assert sc.threat_readiness_score == 0.94
    assert sc.detection_readiness_score == 0.96
    assert sc.response_readiness_score == 0.92
    assert sc.recovery_readiness_score == 0.95
