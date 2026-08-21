import pytest
from app.services.global_defense.coordination_approval_gate import CoordinationApprovalGate

def test_coordination_approval_bypass_blocked():
    gate = CoordinationApprovalGate()
    assert gate.verify_execution_authorization("unapproved_action") is False
