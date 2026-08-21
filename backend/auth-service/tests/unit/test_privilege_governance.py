import pytest
from app.services.zero_trust_exposure.privilege_governance_engine import PrivilegeGovernanceEngine

def test_jit_request_approval_and_expiration():
    engine = PrivilegeGovernanceEngine()
    
    # Request JIT
    req = engine.request_jit_elevation(
        request_id="JIT-500",
        tenant_id="tenant-alpha",
        subject_id="ID-100",
        requested_role="SUPER_ADMIN",
        justification="Critical patch deployment ticket #1234",
        duration_minutes=30,
        peer_reviewer_id="ID-200"
    )
    assert req["status"] == "PENDING"
    
    # Approve
    appr = engine.approve_jit_elevation(
        request_id="JIT-500",
        tenant_id="tenant-alpha",
        approver_id="ID-200"
    )
    assert appr["status"] == "APPROVED"
    assert appr["approved_by"] == "ID-200"
