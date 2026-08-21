import pytest
from app.services.cyber_digital_twin.autonomous_defense_engine import AutonomousDefenseEngine

def test_four_eyes_dual_approval_requirement():
    engine = AutonomousDefenseEngine()
    act = engine.propose_defensive_action("ACT-4EYES", "t1", "HOST-PROD", "ISOLATE_HOST", category="HIGH_IMPACT")
    assert act["approval_requirement"] == "FOUR_EYES_DUAL_APPROVAL_REQUIRED"
    
    # First approval
    app1 = engine.record_approval("ACT-4EYES", "t1", "ANALYST-1")
    assert app1["status"] == "SIMULATED"
    
    # Duplicate approval blocked (Four-Eyes invariant)
    with pytest.raises(ValueError):
        engine.record_approval("ACT-4EYES", "t1", "ANALYST-1")
        
    # Second approval satisfies condition
    app2 = engine.record_approval("ACT-4EYES", "t1", "ANALYST-2")
    assert app2["status"] == "APPROVED"
