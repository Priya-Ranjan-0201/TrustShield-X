import pytest
from app.services.zero_trust_exposure.privilege_governance_engine import PrivilegeGovernanceEngine

def test_break_glass_access_flow():
    engine = PrivilegeGovernanceEngine()
    
    # Missing MFA token is blocked
    blocked = engine.request_break_glass_access("BG-1", "t1", "USR-ADMIN", "P1 Sev outage response", mfa_token="")
    assert blocked["status"] == "BLOCKED"
    assert blocked["reason"] == "STRONG_MFA_AUTHENTICATION_REQUIRED"
    
    # Valid break-glass request succeeds with audit hash
    granted = engine.request_break_glass_access("BG-2", "t1", "USR-ADMIN", "P1 Sev outage core router failure", mfa_token="998811", duration_minutes=15)
    assert granted["status"] == "ACTIVE_EMERGENCY_ACCESS"
    assert granted["audit_hash"] is not None
    assert granted["mandatory_review_required"] is True
    
    # Post-incident review
    reviewed = engine.conduct_break_glass_review("BG-2", "t1", "SECOPS-LEAD", "Emergency access was justified", verdict="JUSTIFIED")
    assert reviewed["review_status"] == "JUSTIFIED"
