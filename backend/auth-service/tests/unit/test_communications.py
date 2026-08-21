import pytest
from app.services.cyber_crisis_command.crisis_communication_engine import CrisisCommunicationEngine

def test_communication_draft():
    engine = CrisisCommunicationEngine()
    draft = engine.create_communication_draft(
        "COMM-01", "C-01", "t1", "EXECUTIVE_BRIEFING", "Board",
        confirmed_facts=["Containment active"],
        suspected_facts=["APT29 attribution"],
        unknowns=["Entry vector"],
        draft_content="Executive briefing content"
    )
    assert draft["status"] == "DRAFT"
    assert draft["requires_approval"] is True
