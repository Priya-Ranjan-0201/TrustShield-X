import pytest
from app.services.governance_fabric.governance_exception_engine import GovernanceExceptionEngine


def test_governance_security_exception_self_approval_blocked():
    engine = GovernanceExceptionEngine()

    with pytest.raises(PermissionError):
        engine.request_exception(
            requirement_id="req_soc2_cc6_1",
            control_id="ctrl_iso_01",
            reason="Self-approval attempt",
            business_justification="Test",
            owner="user_123",
            approver="user_123",
        )
