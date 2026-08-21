import pytest
from app.services.cyber_crisis_command.crisis_decision_engine import CrisisDecisionEngine

def test_immutable_decision_history():
    engine = CrisisDecisionEngine()
    engine.record_decision("DEC-LOG", "C-01", "t1", "Question?", [], "OPT-A", "Commander", "Reason")
    revised = engine.revise_decision("DEC-LOG", "t1", "REVISED", "Commander", "New evidence discovered", "OPT-B")
    assert revised["status"] == "REVISED"
    assert len(revised["history"]) == 1
    assert revised["selected_option_id"] == "OPT-B"
