import pytest
from app.services.zero_trust_exposure.privilege_governance_engine import PrivilegeGovernanceEngine

def test_jit_privilege_workflow():
    engine = PrivilegeGovernanceEngine()
    req = engine.request_jit_elevation("JIT-10", "t1", "USR-1", "SUPER_ADMIN", "Emergency database migration", duration_minutes=30)
    assert req["status"] == "PENDING"
    
    # Self-approval prohibited
    denied = engine.approve_jit_elevation("JIT-10", "t1", "USR-1")
    assert denied["status"] == "FAILED"
    assert denied["reason"] == "SELF_APPROVAL_PROHIBITED"
    
    # Peer approval succeeds
    approved = engine.approve_jit_elevation("JIT-10", "t1", "SECOPS-DIRECTOR")
    assert approved["status"] == "APPROVED"
    assert approved["expires_at"] is not None
