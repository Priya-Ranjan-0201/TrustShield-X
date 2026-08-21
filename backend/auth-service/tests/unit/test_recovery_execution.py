import pytest
from app.services.resilience.recovery_execution_engine import RecoveryExecutionEngine
from app.services.resilience.recovery_plan_engine import RecoveryPlanEngine

def test_recovery_execution():
    exec_engine = RecoveryExecutionEngine()
    plan_engine = RecoveryPlanEngine()
    plan = plan_engine.get_plan("recplan_checkout_recovery")
    res = exec_engine.execute_step(plan, "step_1", "ast_net_vpc", "VERIFY_NETWORK", "usr_requester", "usr_approver")
    assert res.execution_state == "EXECUTED"
