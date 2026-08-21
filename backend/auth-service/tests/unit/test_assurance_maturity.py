import pytest
from app.services.assurance_fabric.control_effectiveness_scorer import ControlEffectivenessScorer

def test_assurance_maturity():
    scorer = ControlEffectivenessScorer()
    score_untested = scorer.evaluate_scorecard(has_empirical_tests=False)
    assert score_untested.maturity_level == "LEVEL_2_IMPLEMENTED"
