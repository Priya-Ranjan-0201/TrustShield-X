import pytest
from app.services.cyber_crisis_command.cyber_crisis_command_engine import CyberCrisisCommandEngine
from app.services.cyber_crisis_command.crisis_decision_engine import CrisisDecisionEngine
from app.services.cyber_crisis_command.crisis_recovery_engine import CrisisRecoveryEngine

def test_crisis_lifecycle_e2e():
    engine = CyberCrisisCommandEngine()
    dec_engine = CrisisDecisionEngine()
    rec_engine = CrisisRecoveryEngine()
    
    # 1. Declare
    c = engine.declare_crisis("C-E2E", "t1", ["INC-100"], "Commander", "E2E Test Crisis")
    assert c["lifecycle_state"] == "CRISIS_DECLARED"
    
    # 2. Assign Roles
    engine.assign_role("C-E2E", "t1", "FORENSICS_LEAD", "forensics@truthshield.io", "Commander")
    
    # 3. Decision
    dec = dec_engine.record_decision("DEC-E2E", "C-E2E", "t1", "Response Action?", [], "OPT-A", "Commander", "Approved")
    assert dec["selected_option_id"] == "OPT-A"
    
    # 4. Containment -> Recovery
    engine.transition_lifecycle_state("C-E2E", "t1", "CONTAINMENT", "Commander", "Isolated")
    engine.transition_lifecycle_state("C-E2E", "t1", "RECOVERY", "Commander", "Patching complete")
    
    # 5. Recovery Verification
    ver = rec_engine.verify_recovery("C-E2E", "t1", {"security_probe_success": True})
    assert ver["overall_recovery_status"] == "RECOVERY_VERIFIED"
