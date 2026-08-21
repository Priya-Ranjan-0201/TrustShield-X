import pytest
from app.services.resilience.recovery_execution_engine import RecoveryExecutionEngine
from app.services.resilience.recovery_plan_engine import RecoveryPlanEngine

def test_resilience_rbac():
    exec_engine = RecoveryExecutionEngine()
    plan_engine = RecoveryPlanEngine()
    plan = plan_engine.get_plan("recplan_checkout_recovery")
    # Requester and approver must be distinct (Four-Eyes)
    with pytest.raises(PermissionError, match="Four-Eyes Violation"):
        exec_engine.execute_step(plan, "step_1", "ast_net_vpc", "VERIFY", "usr_same", "usr_same")
