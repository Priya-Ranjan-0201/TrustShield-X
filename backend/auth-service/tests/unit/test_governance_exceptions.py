import pytest
from app.services.governance_fabric.governance_exception_engine import GovernanceExceptionEngine


def test_governance_exceptions_and_four_eyes():
    engine = GovernanceExceptionEngine()

    # 1. Requester approving own exception -> Error
    with pytest.raises(PermissionError) as exc_info:
        engine.request_exception(
            requirement_id="req_iso_a9_4",
            control_id="ctrl_rbac_01",
            reason="Legacy service migration",
            business_justification="Required for 14-day transition",
            owner="developer_alice",
            approver="developer_alice",
        )
    assert "Four-Eyes Governance Violation" in str(exc_info.value)

    # 2. Valid four-eyes approval
    exp = engine.request_exception(
        requirement_id="req_iso_a9_4",
        control_id="ctrl_rbac_01",
        reason="Legacy service migration",
        business_justification="Required for 14-day transition",
        owner="developer_alice",
        approver="ciso_bob",
        duration_days=14,
    )
    assert exp.exception_id.startswith("exp_")
    assert exp.status == "ACTIVE"
