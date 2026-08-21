import pytest
from app.services.soc.security_operations_orchestrator import SecurityOperationsOrchestrator


def test_response_execution_success():
    orch = SecurityOperationsOrchestrator()
    action, ver = orch.execute_and_verify_action(
        incident_id="inc_exec_01",
        target="srv_checkout_production",
        provider="AWS_SECURITY_GROUP",
        requester_id="usr_analyst_01",
        approver_id="usr_admin_01",
    )

    assert action.action_state == "EXECUTED"
    assert ver.verification_status == "VERIFIED_SUCCESS"
    assert ver.divergence_detected is False
