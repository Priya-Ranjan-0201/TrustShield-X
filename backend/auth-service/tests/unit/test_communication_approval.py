import pytest
from app.services.cyber_crisis_command.crisis_communication_engine import CrisisCommunicationEngine

def test_regulated_communication_requires_approval():
    engine = CrisisCommunicationEngine()
    engine.create_communication_draft("COMM-REG", "C-01", "t1", "REGULATORY_DRAFT", "Regulator", [], [], [], "Draft text")
    
    # Direct send without approval raises PermissionError
    with pytest.raises(PermissionError):
        engine.send_communication("COMM-REG", "t1", "Analyst")
        
    # Once approved, send succeeds
    engine.approve_communication("COMM-REG", "t1", "Legal Counsel")
    sent = engine.send_communication("COMM-REG", "t1", "Analyst")
    assert sent["status"] == "SENT"
