import pytest
from app.services.soc.approval_engine import ApprovalEngine, ApprovalPolicyViolationError
from app.schemas.soc_operations_models import ResponseActionDTO


def test_four_eyes_approval_separation_of_duties():
    engine = ApprovalEngine()
    action = ResponseActionDTO(
        action_id="act_01",
        incident_id="inc_01",
        action_type="ISOLATE_DEVICE",
        target="host_laptop_12",
        requested_by="analyst_priya",
        reason="Malware infection detected",
    )

    appr = engine.create_approval_request(
        action=action,
        requested_by="analyst_priya",
        reason="Active Trojan beaconing",
    )
    assert appr.status == "PENDING"

    # Self-approval MUST BE REJECTED
    with pytest.raises(ApprovalPolicyViolationError):
        engine.decide_approval(
            approval_id=appr.approval_id,
            approver_id="analyst_priya",
            decision="APPROVED",
            decision_reason="Self-approval attempt",
            enforce_separation_of_duties=True,
        )

    # Different approver succeeds
    approved_appr = engine.decide_approval(
        approval_id=appr.approval_id,
        approver_id="soc_lead_arjun",
        decision="APPROVED",
        decision_reason="Authorized post-investigation",
        enforce_separation_of_duties=True,
    )
    assert approved_appr.status == "APPROVED"
    assert approved_appr.decided_by == "soc_lead_arjun"
