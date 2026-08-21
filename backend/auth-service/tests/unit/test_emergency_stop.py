import pytest
from app.services.soc.security_operations_orchestrator import SecurityOperationsOrchestrator


def test_emergency_stop_blocks_all_actions():
    orch = SecurityOperationsOrchestrator()
    orch.guardrails_engine.pause_automation("tenant_stop", "usr_ciso", "Emergency stop triggered")

    # Attempt to execute action should raise RuntimeError
    with pytest.raises(RuntimeError, match="Automation is currently PAUSED"):
        orch.execute_and_verify_action(
            incident_id="inc_stop",
            target="srv_checkout",
            requester_id="usr_analyst",
            approver_id="usr_admin",
            tenant_id="tenant_stop",
        )
