import pytest
from app.services.cyber_crisis_command.crisis_decision_engine import CrisisDecisionEngine

def test_response_option_analysis():
    engine = CrisisDecisionEngine()
    options = engine.analyze_response_options("C-OPT", "t1", "API-GW", "Ransomware")
    assert len(options) == 3
    assert options[0]["is_pareto_optimal"] is True
    assert options[0]["option_id"] == "OPT-A"
