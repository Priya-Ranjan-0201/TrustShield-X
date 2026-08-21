import pytest
from app.services.soc.security_operations_orchestrator import SecurityOperationsOrchestrator


def test_soc_audit_action_verification_ledger():
    orch = SecurityOperationsOrchestrator()
    action, ver = orch.execute_and_verify_action(
        incident_id="inc_audit",
        target="srv_checkout",
        requester_id="usr_analyst",
        approver_id="usr_admin",
    )

    assert action.action_id in orch._actions
    assert action.action_id in orch._verifications
    assert ver.evidence_reference is not None
