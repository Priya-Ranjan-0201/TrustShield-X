import pytest
from app.services.global_defense.coordination_approval_gate import CoordinationApprovalGate

def test_four_eyes_approval_flow():
    gate = CoordinationApprovalGate()
    
    # 1. Single approver
    res1 = gate.approve_action("act_isolate_c2", "SOC_LEAD")
    assert res1["four_eyes_satisfied"] is False
    assert res1["status"] == "PENDING_ADDITIONAL_APPROVAL"
    assert gate.verify_execution_authorization("act_isolate_c2") is False
    
    # 2. Second independent approver (CISO)
    res2 = gate.approve_action("act_isolate_c2", "CISO")
    assert res2["four_eyes_satisfied"] is True
    assert res2["status"] == "APPROVED"
    assert gate.verify_execution_authorization("act_isolate_c2") is True
