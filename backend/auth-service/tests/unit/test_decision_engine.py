import pytest
from app.services.cyber_crisis_command.crisis_decision_engine import CrisisDecisionEngine

def test_decision_record():
    engine = CrisisDecisionEngine()
    dec = engine.record_decision(
        "DEC-01", "C-01", "t1", "Isolate or microsegment?",
        [{"id": "OPT-A", "name": "Microsegment"}], "OPT-A", "Commander", "Low downtime"
    )
    assert dec["status"] == "RECORDED"
    assert dec["selected_option_id"] == "OPT-A"
