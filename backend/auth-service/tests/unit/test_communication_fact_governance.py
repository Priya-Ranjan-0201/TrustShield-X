import pytest
from app.services.cyber_crisis_command.crisis_communication_engine import CrisisCommunicationEngine

def test_fact_governance_separation():
    engine = CrisisCommunicationEngine()
    draft = engine.create_communication_draft(
        "COMM-FACT", "C-01", "t1", "INTERNAL_SECURITY", "SOC",
        confirmed_facts=["No exfiltration"],
        suspected_facts=["Credential dump"],
        unknowns=["Dwell time"],
        draft_content="Internal update"
    )
    facts = draft["fact_governance"]
    assert len(facts["confirmed_facts"]) == 1
    assert len(facts["suspected_facts"]) == 1
    assert len(facts["unknowns"]) == 1
