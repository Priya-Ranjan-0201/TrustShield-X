import pytest
from app.services.cyber_crisis_command.crisis_decision_engine import CrisisDecisionEngine

def test_digital_twin_what_if_decision_support():
    engine = CrisisDecisionEngine()
    opts = engine.analyze_response_options("C-TWIN", "t1", "CORE-DB", "Exfiltration")
    assert any("risk_reduction" in opt for opt in opts)
