import pytest
from app.services.resilience.recovery_plan_engine import RecoveryPlanEngine

def test_recovery_rollback():
    engine = RecoveryPlanEngine()
    plan = engine.get_plan("recplan_checkout_recovery")
    assert len(plan.rollback_steps) >= 2
