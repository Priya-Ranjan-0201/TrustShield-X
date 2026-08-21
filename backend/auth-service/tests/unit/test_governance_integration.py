import pytest
from app.services.cyber_digital_twin.digital_twin_validation_governance_engine import DigitalTwinValidationGovernanceEngine

def test_cryptographic_audit_chaining():
    engine = DigitalTwinValidationGovernanceEngine()
    e1 = engine.record_audit_event("EV-1", "t1", "SCENARIO_CREATED", {"name": "Test1"})
    e2 = engine.record_audit_event("EV-2", "t1", "SIMULATION_EXECUTED", {"run_id": "R1"})
    
    assert e2["previous_hash"] == e1["current_hash"]
    assert e2["current_hash"] is not None
